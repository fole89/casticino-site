"""Prepara le news salvate dall'area di redazione (admin/) prima di generare le pagine.

Per ogni data/news/*.json:
  - se manca «file», gli dà il nome della pagina: news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html
  - le foto caricate (in assets/img/news/ fuori dalle cartelle degli anni, anche quelle dentro il testo) diventano
    WebP larghe al massimo 1400 px in assets/img/news/<anno>/, con lo stesso nome della pagina (-2, -3… per le
    altre); l'originale viene tolto
  - i PDF (allegati o link nel testo) ancora in docs/news/, dove li salva l'area di redazione, vanno in
    docs/news/<anno>/ con il nome della pagina (-2, -3… per gli altri) e i link nella news vengono aggiornati;
    un PDF usato da più news segue la prima, le altre puntano al nuovo percorso
Lo esegue il workflow .github/workflows/news.yml; serve Pillow:  pip install pillow
Uso: python scripts/prepara_news.py"""
import glob, json, os, re, shutil, sys, urllib.parse
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "redesign"))
import news_util  # noqa: E402

MAX_W = 1400


def caricata(src):
    """Foto appena caricata dall'area di redazione: in assets/img/news/ (non in una cartella dell'anno) o non in WebP."""
    if not src.startswith("assets/img/news/") or not os.path.exists(os.path.join(ROOT, src)):
        return False
    return not re.fullmatch(r"assets/img/news/\d{4}/[^/]+\.webp", src)


def percorso(p):
    return urllib.parse.unquote(p.strip().lstrip("/"))


def in_webp(src, dest):
    """Converte un'immagine caricata in WebP (max 1400 px di larghezza) e toglie l'originale."""
    im = Image.open(os.path.join(ROOT, src))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and src.lower().endswith(".png") else "RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.join(ROOT, dest)), exist_ok=True)
    im.save(os.path.join(ROOT, dest), "WEBP", quality=80, method=6)
    os.remove(os.path.join(ROOT, src))
    print("  foto", src, "->", dest)


# PDF nel testo o negli allegati: docs/news/<file>.pdf, con o senza «/» davanti (fuori dalle cartelle degli anni)
PDF_DA_SPOSTARE = re.compile(r'/?docs/news/([^/"\\\s)<>]+\.pdf)', re.I)


def sposta_pdf(tutte):
    """Porta i PDF delle news da docs/news/ a docs/news/<anno>/<nome-pagina>[-N].pdf e aggiorna i link."""
    nuovi = {}  # vecchio percorso -> nuovo
    for n in sorted(tutte, key=lambda n: n["date"]):
        base = f"docs/news/{n['date'][:4]}/{os.path.splitext(os.path.basename(n['file']))[0]}"
        testo = json.dumps(n, ensure_ascii=False)
        for m in PDF_DA_SPOSTARE.finditer(testo):
            vecchio = "docs/news/" + urllib.parse.unquote(m.group(1))
            if vecchio in nuovi or not os.path.exists(os.path.join(ROOT, vecchio)):
                continue
            nome, k = base + ".pdf", 2
            while nome in nuovi.values() or os.path.exists(os.path.join(ROOT, nome)):
                nome, k = f"{base}-{k}.pdf", k + 1
            os.makedirs(os.path.dirname(os.path.join(ROOT, nome)), exist_ok=True)
            shutil.move(os.path.join(ROOT, vecchio), os.path.join(ROOT, nome))
            nuovi[vecchio] = nome
            print("  pdf", vecchio, "->", nome)

    def aggiorna(v):
        if isinstance(v, str):
            return PDF_DA_SPOSTARE.sub(lambda m: nuovi.get("docs/news/" + urllib.parse.unquote(m.group(1)), m.group(0)), v)
        if isinstance(v, list):
            return [aggiorna(x) for x in v]
        if isinstance(v, dict):
            return {k: aggiorna(x) for k, x in v.items()}
        return v
    if nuovi:
        for n in tutte:
            for k in list(n):
                if k != "percorso":
                    n[k] = aggiorna(n[k])


def main():
    tutte = news_util.leggi_tutte()
    presi = {n["file"] for n in tutte if n.get("file")}
    for n in tutte:
        if not n.get("file"):
            n["file"] = news_util.nome_file(n, presi)
            presi.add(n["file"])
            print("nuova news:", n["file"])
    sposta_pdf(tutte)
    for n in tutte:
        p = n.pop("percorso")
        base = f"assets/img/news/{n['date'][:4]}/{os.path.splitext(os.path.basename(n['file']))[0]}"
        usati = set()

        def nome_libero():
            nome, k = base + ".webp", 2
            while nome in usati or (os.path.exists(os.path.join(ROOT, nome)) and nome != n.get("image")):
                nome, k = f"{base}-{k}.webp", k + 1
            usati.add(nome)
            return nome

        if n.get("image"):
            src = percorso(n["image"])
            if caricata(src):
                n["image"] = nome_libero()
                in_webp(src, n["image"])
            else:
                n["image"] = src
                usati.add(src)

        def immagine_nel_testo(m):
            src = percorso(m.group(2))
            if not caricata(src):
                return m.group(0)
            dest = nome_libero()
            in_webp(src, dest)
            return f"{m.group(1)}({dest})"
        if n.get("testo"):
            n["testo"] = re.sub(r'(!\[[^\]]*\])\(([^)"]+?)(?:\s+"[^)]*")?\)', immagine_nel_testo, n["testo"])
        for a in n.get("allegati") or []:
            a["file"] = percorso(a.get("file", ""))

        nuovo = json.dumps(n, ensure_ascii=False, indent=1) + "\n"
        with open(p, encoding="utf-8") as f:
            if f.read() == nuovo:
                continue
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(nuovo)

    # news eliminate dall'area di redazione: via anche la loro pagina
    valide = {n["file"] for n in news_util.leggi_tutte()}
    for pagina in glob.glob(os.path.join(ROOT, "news", "*", "*.html")):
        rel = os.path.relpath(pagina, ROOT).replace(os.sep, "/")
        if rel not in valide:
            os.remove(pagina)
            print("pagina tolta:", rel)


if __name__ == "__main__":
    main()
