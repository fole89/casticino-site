"""Importa le news dal vecchio sito WordPress (casticino.ch) nel sito statico.

Scrive:
  data/news.json            elenco delle notizie (titolo, data, estratto, testo HTML ripulito, immagine)
  assets/img/news/*.webp    immagine principale e immagini nel testo, convertite in WebP (max 1400 px)
  docs/news/*.pdf           PDF allegati, scaricati dal vecchio sito

Le pagine (News.html e news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html) le genera poi scripts/redesign/pages.py leggendo data/news.json.
Serve Pillow solo per questo script:  pip install pillow
Uso: python scripts/import_news.py
"""
import html, io, json, os, re, unicodedata, urllib.parse, urllib.request
from html.parser import HTMLParser
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://casticino.ch/index.php?rest_route=/wp/v2/posts&per_page=100&_embed=1"
IMG_DIR = os.path.join(ROOT, "assets", "img", "news")
DOC_DIR = os.path.join(ROOT, "docs", "news")
MAX_W = 1400
GITE = "https://ssl.dropnet.ch/casticino/gite/index.php"

# pagine del vecchio sito citate negli articoli -> pagine nuove (percorsi relativi alla radice del sito)
VECCHIE_PAGINE = {
    "page_id=53": "Corsi.html#corso-arrampicata",       # corso di arrampicata
    "page_id=55": "Corsi.html#corso-racchette",       # corso di racchette
    "page_id=4380": "Corsi.html#corso-fuoripista",     # tecnica di sci fuori pista
    "page_id=78": GITE,                       # programma
    "/corso-di-sci-alpinismo/": "Corsi.html#corso-scialpinismo",
}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (import news CAS Ticino)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


GIORNI_MESI = set("""lun mar mer gio ven sab dom lunedi martedi mercoledi giovedi venerdi sabato domenica ma
gen feb mag giu lug ago set ott nov dic gennaio febbraio marzo aprile maggio giugno luglio agosto settembre
ottobre novembre dicembre apr ore alle h""".split())
PAROLE_VUOTE = set("""il lo la i gli le l un una uno di del dello della dei degli delle d a al allo alla ai agli alle
da dal dallo dalla dai dagli dalle in nel nello nella nei negli nelle su sul sullo sulla sui sugli sulle con per tra fra
e ed o vs""".split())


def nome_breve(slug, titolo, maxlen=40):
    """Titolo breve per il nome del file: senza giorni e date iniziali, senza articoli e preposizioni."""
    def pulisci(t):
        t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
        return [p for p in re.split(r"[^a-z0-9]+", t) if p]
    parole = pulisci(slug)
    if not parole or all(p.isdigit() for p in parole):
        parole = pulisci(titolo)
    parole = [p for p in parole if p != "copy"]  # duplicati di WordPress
    while parole and (parole[0] in GIORNI_MESI or parole[0] in PAROLE_VUOTE or parole[0].isdigit()):
        parole.pop(0)
    parole = [p for p in parole if p not in PAROLE_VUOTE] or pulisci(titolo)[:3]
    out = ""
    for p in parole:
        prova = f"{out}-{p}" if out else p
        if len(prova) > maxlen:
            break
        out = prova
    return out or parole[0][:maxlen]


def slugify(text, maxlen=70):
    text = urllib.parse.unquote(text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(text) > maxlen:
        text = text[:maxlen].rsplit("-", 1)[0]
    return text or "news"


class Risorse:
    """Scarica immagini e PDF una volta sola e restituisce il percorso locale."""

    def __init__(self):
        self.cache = {}
        self.nomi = set()

    def _nome(self, base, ext, cartella):
        nome, n = f"{base}.{ext}", 2
        while os.path.join(cartella, nome) in self.nomi:
            nome, n = f"{base}-{n}.{ext}", n + 1
        self.nomi.add(os.path.join(cartella, nome))
        return nome

    def immagine(self, url, base):
        if url in self.cache:
            return self.cache[url]
        try:
            im = Image.open(io.BytesIO(get(url)))
        except Exception as e:
            print("  immagine non scaricata:", url, e)
            self.cache[url] = None
            return None
        im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
        nome = self._nome(base, "webp", IMG_DIR)
        im.save(os.path.join(IMG_DIR, nome), "WEBP", quality=80, method=6)
        res = (f"assets/img/news/{nome}", im.width, im.height)
        self.cache[url] = res
        return res

    def pdf(self, url):
        if url in self.cache:
            return self.cache[url]
        try:
            dati = get(url)
        except Exception as e:
            print("  PDF non scaricato:", url, e)
            self.cache[url] = None
            return None
        if not dati.startswith(b"%PDF"):
            print("  non è un PDF:", url)
            self.cache[url] = None
            return None
        base = slugify(os.path.splitext(os.path.basename(urllib.parse.urlparse(url).path))[0], 60)
        nome = self._nome(base, "pdf", DOC_DIR)
        with open(os.path.join(DOC_DIR, nome), "wb") as f:
            f.write(dati)
        self.cache[url] = f"docs/news/{nome}"
        return self.cache[url]


def originale(url):
    """Da un'immagine ridimensionata da WordPress (foto-1024x768.jpg) risale all'originale."""
    return re.sub(r"-\d+x\d+(\.\w+)$", r"\1", url)


class Pulisci(HTMLParser):
    """Tiene solo l'HTML che serve al testo (paragrafi, liste, link, immagini, tabelle), senza stili."""

    TIENI = {"p", "br", "strong", "em", "a", "ul", "ol", "li", "h2", "h3", "blockquote", "figure",
             "figcaption", "img", "table", "tbody", "thead", "tr", "td", "th", "hr", "details", "summary"}
    RINOMINA = {"b": "strong", "i": "em", "h1": "h2", "h4": "h3", "h5": "h3", "h6": "h3"}
    SCARTA = {"style", "script", "svg", "object", "noscript", "iframe", "form", "button"}
    VUOTI = {"br", "img", "hr"}

    def __init__(self, risorse, slug, link_post):
        super().__init__(convert_charrefs=True)
        self.r, self.slug, self.link_post = risorse, slug, link_post
        self.out, self.skip, self.n_img = [], 0, 0

    def link(self, href):
        href = href.strip()
        if href.startswith(("mailto:", "tel:")):
            return href
        u = urllib.parse.urlparse(href)
        if "casticino.ch" not in u.netloc or u.netloc.count(".") > 1 and not u.netloc.startswith("www."):
            return href if u.scheme in ("http", "https") else None  # esterni e sottodomini delle capanne restano
        if "/wp-content/" in u.path:
            ext = u.path.rsplit(".", 1)[-1].lower()
            if ext == "pdf":
                return self.r.pdf(href)
            if ext in ("jpg", "jpeg", "png", "gif", "webp"):
                res = self.r.immagine(originale(href), f"{self.slug}-allegato")
                return res[0] if res else None
            return None
        m = re.search(r"[?&]p=(\d+)", href)
        if m and int(m.group(1)) in self.link_post:
            return self.link_post[int(m.group(1))]
        for chiave, nuovo in VECCHIE_PAGINE.items():
            if chiave in href:
                return nuovo
        return "index.html"

    def handle_starttag(self, tag, attrs):
        if self.skip or tag in self.SCARTA:
            if tag not in self.VUOTI:
                self.skip += 1
            return
        tag = self.RINOMINA.get(tag, tag)
        if tag not in self.TIENI:
            return
        a = dict(attrs)
        if tag == "a":
            href = self.link(a.get("href", "")) if a.get("href") else None
            if not href or href.startswith("#"):
                self.out.append("<a>")
                return
            ext = href.startswith(("http://", "https://"))
            self.out.append(f'<a href="{html.escape(href)}"' + (' rel="noopener"' if ext else "") + ">")
        elif tag == "img":
            src = a.get("src", "")
            if "/wp-content/" not in src:
                return
            self.n_img += 1
            res = self.r.immagine(originale(src), f"{self.slug}-{self.n_img + 1}")
            if res:
                alt = html.escape(a.get("alt", ""), quote=True)
                self.out.append(f'<img src="{res[0]}" alt="{alt}" width="{res[1]}" height="{res[2]}" loading="lazy" decoding="async">')
        else:
            self.out.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if self.skip:
            if tag in self.SCARTA or tag not in self.VUOTI:
                self.skip -= 1
            return
        tag = self.RINOMINA.get(tag, tag)
        if tag in self.TIENI and tag not in self.VUOTI:
            self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(html.escape(data, quote=False))

    def risultato(self):
        s = "".join(self.out)
        s = s.replace(" ", " ")
        s = re.sub(r"<a>(.*?)</a>", r"\1", s, flags=re.S)                  # link non più validi: resta il testo
        s = re.sub(r"<(p|li|h2|h3|figcaption|strong|em)>\s*(<br>\s*)*</\1>", "", s)  # elementi vuoti
        s = re.sub(r"(<br>\s*){3,}", "<br><br>", s)
        s = re.sub(r"<figure>\s*</figure>", "", s)
        s = re.sub(r"\n\s*\n+", "\n", s).strip()
        return ritocca(s)


def ritocca(s):
    """Allegati: il blocco file di WordPress mette due link allo stesso PDF (nome + «Download»): ne resta uno."""
    s = re.sub(r'<a href="(docs/[^"]+)">([^<]*)</a>\s*<a href="\1">[^<]*</a>',
               r'<p><a class="file-link" href="\1">\2</a></p>', s)
    s = re.sub(r'(^|</p>|</figure>|</ul>|</h[23]>)\s*<a href="(docs/[^"]+)">([^<]*)</a>(?!\s*</p>)',
               r'\1<p><a class="file-link" href="\2">\3</a></p>', s)
    return s


def testo(frammento):
    t = re.sub(r"<[^>]+>", " ", frammento)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def estratto(p, corpo):
    # dal testo ripulito: l'estratto di WordPress perde gli a capo e attacca le parole («Quando?Da lunedì»)
    t = testo(re.sub(r"<(br|/p|/li|/h[23])>", " ", corpo)) or testo(p["excerpt"]["rendered"])
    t = re.sub(r"\s*(\[…\]|\[\.\.\.\]|Continua a leggere.*)$", "", t).strip()
    if len(t) > 220:
        t = t[:220].rsplit(" ", 1)[0].rstrip(",.;:") + "…"
    return t


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    os.makedirs(DOC_DIR, exist_ok=True)
    posts = json.loads(get(API))
    posts.sort(key=lambda p: p["date"], reverse=True)
    r = Risorse()

    slugs, link_post = set(), {}
    for p in posts:
        # nome del file: data + titolo breve, in una cartella per anno (news/2026/2026-09-30-film-trail-locarno.html)
        data = p["date"][:10]
        breve = nome_breve(p["slug"] or "", html.unescape(p["title"]["rendered"]))
        s, n = f"{data}-{breve}", 2
        while s in slugs:
            s, n = f"{data}-{breve}-{n}", n + 1
        slugs.add(s)
        p["_slug"] = s
        link_post[p["id"]] = f"news/{data[:4]}/{s}.html"

    out = []
    for p in posts:
        s = p["_slug"]
        print(p["date"][:10], s)
        emb = p.get("_embedded", {})
        cat = [t["name"] for g in emb.get("wp:term", []) for t in g if t.get("taxonomy") == "category"]
        cat = next((c for c in cat if c not in ("NEWS", "Uncategorized")), "")
        img = None
        fm = (emb.get("wp:featuredmedia") or [{}])[0]
        if fm.get("source_url"):
            res = r.immagine(fm["source_url"], s)
            if res:
                img = {"src": res[0], "w": res[1], "h": res[2], "alt": html.unescape(fm.get("alt_text") or "")}
        pul = Pulisci(r, s, link_post)
        pul.feed(p["content"]["rendered"])
        corpo = pul.risultato()
        out.append({
            "id": p["id"], "slug": s, "file": link_post[p["id"]],
            "title": html.unescape(p["title"]["rendered"]).strip(),
            "date": p["date"][:10], "category": cat,
            "excerpt": estratto(p, corpo), "image": img, "html": corpo,
            "source": p["link"],
        })

    with open(os.path.join(ROOT, "data", "news.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"news": out}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(len(out), "notizie scritte in data/news.json")


if __name__ == "__main__":
    main()
