"""Prepara gli annunci del mercatino salvati dall'area di redazione (admin/) prima di generare le pagine.

Per ogni data/mercatino/*.json:
  - le foto appena caricate (in assets/img/mercatino/ con un altro nome o non in WebP) diventano WebP larghe al
    massimo 1200 px, con il nome dell'annuncio: assets/img/mercatino/<AAAA-MM-GG>-<titolo>-1.webp, -2, -3;
    l'originale viene tolto e il percorso nell'annuncio aggiornato
  - toglie le foto in assets/img/mercatino/ che nessun annuncio usa più (annunci eliminati o foto tolte)
Lo esegue il workflow .github/workflows/news.yml; serve Pillow:  pip install pillow
Uso: python scripts/prepara_mercatino.py"""
import glob, json, os, re, sys, urllib.parse
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "redesign"))
import mercatino_util  # noqa: E402

MAX_W = 1200
CARTELLA = "assets/img/mercatino"


def in_webp(src, dest):
    im = Image.open(os.path.join(ROOT, src))
    im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") and src.lower().endswith(".png") else "RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(os.path.join(ROOT, dest), "WEBP", quality=80, method=6)
    os.remove(os.path.join(ROOT, src))
    print("  foto", src, "->", dest)


def main():
    os.makedirs(os.path.join(ROOT, CARTELLA), exist_ok=True)
    usate = set()
    for a in mercatino_util.leggi_tutti():
        p = a.pop("percorso")
        base = f"{CARTELLA}/{os.path.splitext(os.path.basename(p))[0]}"
        giusto = re.compile(re.escape(base) + r"-\d+\.webp")
        foto = [urllib.parse.unquote(str(x).strip().lstrip("/")) for x in a.get("foto") or [] if x]
        prese = {f for f in foto if giusto.fullmatch(f)}
        nuove = []
        for src in foto:
            if giusto.fullmatch(src) or not os.path.exists(os.path.join(ROOT, src)):
                nuove.append(src)  # già pronta, oppure mancante (pages.py la salta)
                continue
            k = 1
            while f"{base}-{k}.webp" in prese or os.path.exists(os.path.join(ROOT, f"{base}-{k}.webp")):
                k += 1
            dest = f"{base}-{k}.webp"
            prese.add(dest)
            in_webp(src, dest)
            nuove.append(dest)
        if a.get("foto") is not None or nuove:
            a["foto"] = nuove
        usate.update(nuove)
        nuovo = json.dumps(a, ensure_ascii=False, indent=1) + "\n"
        with open(p, encoding="utf-8") as f:
            if f.read() == nuovo:
                continue
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(nuovo)

    for f in glob.glob(os.path.join(ROOT, CARTELLA, "*")):
        rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
        if os.path.isfile(f) and rel not in usate:
            os.remove(f)
            print("foto non più usata, tolta:", rel)


if __name__ == "__main__":
    main()
