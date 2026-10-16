"""Funzioni e dati comuni a tutte le pagine: impaginazione (page()), gruppi del menu e briciole, testi modificabili
dalla redazione (data/testi/, testi()), date e mesi nelle quattro lingue, percorsi delle sottocartelle (pubblica()).
I moduli pagine_*.py lo importano con `from comune import *`."""
import json, mercatino_util, news_util, os, re, sys, unicodedata
from capanne_de import HUTS_DE
from capanne_en import HUTS_EN
from capanne_fr import HUTS_FR
from news_util import webp_size
from shared import GITE, L, LINGUA, PAGINE_LINGUA, TRADUZIONI, asset, de, en, fr, senza_lingua, footer, head, img, in_sottocartella, nav, page_hero, pic, social, subnav, t, tr


# Programma gite su Droptour già filtrato per gruppo o per tipo di attività (i link dei singoli corsi cambiano ogni anno)
GITE_GIOVANI = GITE + "?gruppo=Giovani"   # gite.html con il filtro già scelto (gite.js)
GITE_SENIORI = GITE + "?gruppo=Seniori"
GITE_CORSI = GITE + "?tipo=COR"

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def num(t):
    """Cifre in Geist Mono (posti, tempi): «80 posti» → «<span class="num">80</span> posti»."""
    return re.sub(r"\d+(?:[.,:’']\d+)*(?:h\d*)?", lambda m: f'<span class="num">{m.group()}</span>', t)


def schede_capanne(lista, accesso="Accesso da", prefisso=""):
    """Home: le sei capanne in schede compatte (foto, nome, quota, valle, stagione di custodia, posti e accesso).
    La stagione resta scritta così com'è (es. «Custodita giu–ott»): una pagina statica non può sapere se oggi il guardiano c'è."""
    return "\n".join(f"""<a class="hut" href="{prefisso}{f}" data-reveal>
<figure>{img(im, f'Capanna {n}', w, h)}</figure>
<div class="hut-head"><h3 class="h3">{n}</h3><span class="hut-alt">{q} m</span></div>
<div class="hut-meta"><span>{v}</span></div>
<div class="hut-meta"><span class="status">{st}</span></div>
<div class="hut-meta"><span>{num(posti)}</span><span>{accesso} {num(acc)}</span></div>
</a>""" for f, n, q, v, st, t, posti, acc, im, (w, h), big in lista)


def ATT_MENU():
    return tr("Attività", "Aktivitäten", "Activities", "Activités")


def NM_MENU():
    return tr("News e media", "News und Medien", "News and media", "News et médias")


def SEZ_MENU():
    return tr("La Sezione", "Die Sektion", "The Section", "La Section")


def att_crumb():
    return (ATT_MENU(), L("index.html") + "#attivita")


def nm_crumb():
    return (NM_MENU(), L("news.html"))


def sez_crumb():
    return (SEZ_MENU(), L("introduzione.html"))


def in_it():
    """Attributo lang="it" per i testi che restano in italiano (news, annunci, gite) nelle pagine tradotte."""
    return ' lang="it"' if LINGUA["lang"] != "it" else ""


def localizza(html, lang):
    """Pagina tradotta: i link alle pagine che esistono anche in questa lingua portano alla versione tradotta
    (i testi possono così usare i nomi italiani delle pagine). Non tocca il selettore di lingua."""
    def link(h):
        if h.group(2) in PAGINE_LINGUA[lang]:
            return f'href="{h.group(1)}{lang}/{h.group(2)}{h.group(3)}"'
        return h.group(0)

    def tag(m):
        if 'class="nav-lang"' in m.group(0):
            return m.group(0)
        return re.sub(r'href="((?:\.\./)*)([^"#?]*)([^"]*)"', link, m.group(0))
    return re.sub(r"<a\b[^>]*>", tag, html)


# ------------------------------------------------------------------ impaginazione

def page(file, title, description, body, og="paesaggi/sciatori-villaggio-2000", section=None, scripts=""):
    """Pagina completa: testa, menu, contenuto, footer."""
    html = head(title, description, f'<meta property="og:image" content="assets/img/{og}.webp">\n')
    return html + "\n<body>\n" + nav(file, section) + f"""
<main id="contenuto">

{body}

</main>
{scripts}""" + footer()


def facts(rows):
    """Lista definizioni: coppie (termine, descrizione HTML)."""
    return '<dl class="facts">\n' + "\n".join(f"<dt>{t}</dt><dd>{d}</dd>" for t, d in rows) + "\n</dl>"


def credito(autore="Michele Foletti"):
    """Autore della foto grande (figcaption in basso a destra sopra la foto, .credito in site.css)."""
    return f'<figcaption class="credito">{tr("Foto", "Foto", "Photo", "Photo")} © {autore}</figcaption>'


def salti(voci, etichetta=None):
    """Barra «In questa pagina» (.salti; capanne, Corsi): pulsanti (id, testo) verso le sezioni della pagina, nell'ordine
    in cui compaiono. Resta appiccicata sotto il menu e site.js evidenzia la sezione in cui ci si trova."""
    etichetta = etichetta or tr("In questa pagina", "Auf dieser Seite", "On this page", "Sur cette page")
    links = "\n".join(f'<a href="#{k}">{l}</a>' for k, l in voci)
    return f"""

<nav class="salti" aria-label="{etichetta}">
<div class="container subnav">
<p class="label">{etichetta}</p>
<div class="subnav-links">
{links}
</div>
</div>
</nav>"""


def band_img(name, alt, w, h):
    return f'<figure class="band">\n{img(name, alt, w, h, lazy=False)}\n</figure>'
IBAN = "CH09 0076 4128 9526 1200 6"   # conto della sezione (Banca Stato, Lugano), anche in Sede e contatti


def pubblica(nome, html):
    """Pagina in una sottocartella (de/, fr/, en/, capanne/…): i percorsi relativi salgono dei livelli giusti."""
    return in_sottocartella(html, su="../" * nome.count("/")) if "/" in nome else html


def sezione_page(file, title, description, body, **kw):
    """Pagina della sezione nella lingua corrente (tradotta: de/<file>, fr/<file>, en/<file>)."""
    nome = L(file)
    return pubblica(nome, page(nome, title, description, body, **kw))


def slug_nome(nome):
    t = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


# Testi modificabili dalla redazione (admin/, «Testi del sito»): data/testi/<pagina>.json. Ogni campo ha l'italiano e,
# facoltativi, _de, _fr e _en; se la traduzione manca, la pagina tradotta mostra l'italiano marcato lang="it".
_TESTI = {}


def testi(nome):
    if nome not in _TESTI:
        _TESTI[nome] = json.load(open(os.path.join(ROOT, "data", "testi", f"{nome}.json"), encoding="utf-8"))
    return _TESTI[nome]


def testo_md(d, k, in_riga=False):
    """Campo k scritto in Markdown (paragrafi, elenchi, grassetto, link), nella lingua della pagina;
    i link ai PDF prendono l'icona del file (.file-link). in_riga: una riga sola, senza <p> (es. in una tabella)."""
    lang = LINGUA["lang"]
    t = (d.get(f"{k}_{lang}") or "").strip() if lang != "it" else ""
    manca = not t and lang != "it"
    h = news_util.md_html(t or (d.get(k) or "").strip())
    h = re.sub(r'<a href="([^"]+\.pdf)">', r'<a class="file-link" href="\1">', h)
    if in_riga:
        h = re.sub(r"^<p>(.*)</p>$", r"\1", h, flags=re.S)
        return f'<span lang="it">{h}</span>' if manca and h else h
    return f'<div lang="it">\n{h}\n</div>' if manca and h else h


def testo_campo(d, k, semplice=False):
    """Campo k nella lingua della pagina: HTML (testo libero, a capo e indirizzi e-mail/web diventano <br> e link),
    oppure, con semplice=True, testo semplice per <title> e simili."""
    lang = LINGUA["lang"]
    t = (d.get(f"{k}_{lang}") or "").strip() if lang != "it" else ""
    manca = not t and lang != "it"
    t = t or (d.get(k) or "").strip()
    if semplice:
        return t
    h = testo_libero(t)
    return f'<span lang="it">{h}</span>' if manca and h else h


def testo_libero(t):
    """Testo scritto dalla redazione: niente HTML; e-mail e indirizzi https:// diventano link, a capo diventa <br>."""
    def link(m):
        x = m.group(0)
        if "@" in x and not x.startswith("http"):
            return f'<a href="mailto:{x}">{x}</a>'
        return f'<a href="{x}" rel="noopener">{x}</a>'
    h = esc(t)
    h = re.sub(r"https?://[^\s<]+[^\s<.,;:!?)]|[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-z]{2,}", link, h, flags=re.I)
    return h.replace("\n", "<br>")


DOC = "docs/"  # PDF della sezione, in sottocartelle per tema (nomi in minuscolo, con trattini)


def SERVIZI_MENU():
    """Nome della voce Servizi nella lingua corrente (per percorso e sotto-menu)."""
    return tr("Servizi", "Dienste", "Services", "Services")


def servizi_crumb():
    return (SERVIZI_MENU(), L("index.html") + "#servizi")
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]


def data_it(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MESI[m - 1]} {y}"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
MESI_L = {"it": MESI, "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
          "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}


def data_l(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    mese = MESI_L[LINGUA["lang"]][m - 1]
    return tr(f"{d} {mese} {y}", f"{d}. {mese} {y}", f"{d} {mese} {y}", f"{'1er' if d == 1 else d} {mese} {y}")


def blocco(id_, titolo, intro, corpo):
    """Sezione a due colonne: titolo e frase a sinistra, testo a destra (pagine Partecipare e Mettiti in gioco)."""
    return f"""<section class="section" aria-labelledby="{id_}">
<div class="container detail">
<div class="detail-intro">
<h2 id="{id_}" class="h2">{titolo}</h2>
<p>{intro}</p>
</div>
<div class="prose" data-reveal>
{corpo}
</div>
</div>
</section>"""
