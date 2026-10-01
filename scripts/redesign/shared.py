"""Parti comuni del nuovo design (intestazione, footer). Genera HTML statico."""
import hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def asset(path):
    """Percorso con impronta del contenuto (?v=…), così il browser non usa una copia vecchia in cache."""
    with open(os.path.join(ROOT, path), "rb") as f:
        return f"{path}?v={hashlib.md5(f.read()).hexdigest()[:8]}"

GITE = "https://ssl.dropnet.ch/casticino/gite/index.php"

MENU = [
    ("La Sezione", "index.html#sezione", [
        ("Introduzione", "Introduzione.html"), ("Comitato", "Comitato.html"),
        ("Organizzazione", "Organizzazione.html"), ("Sede e recapiti", "Sede.html"),
        ("Storia", "Storia.html"), ("Link utili", "Link.html")]),
    ("News", "index.html#news", None),
    ("Attività", "index.html#attivita", [
        ("Giovani", "Giovani.html"), ("Senior", "Senior.html"),
        ("Corsi", "Corsi.html"), ("Noleggio", "Noleggio.html")]),
    ("Le Capanne", "index.html#capanne", [
        ("Campo Tencia", "CampoTencia.html"), ("Cristallina", "Cristallina.html"), ("Adula", "Adula.html"),
        ("Motterascio", "Motterascio.html"), ("Monte Bar", "MonteBar.html"), ("Baita del Luca", "BaitaDelLuca.html")]),
    ("Media", "index.html#media", [
        ("Foto", "Foto.html"), ("Annuari", "Annuari.html"), ("Informazione", "Informazione.html"),
        ("Documenti", "Documenti.html")]),
    ("Adesione", "Adesione.html", None),
]

CARET = '<span class="caret" aria-hidden="true"></span>'


def head(title, description, extra=""):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_CH">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="assets/logo-cas.webp">
<link rel="preload" href="assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset("assets/site.css")}">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>"""


def nav(current_page, current_section=None):
    """current_page: nome file della pagina (per aria-current). current_section: voce di primo livello attiva."""
    items = []
    for label, href, sub in MENU:
        is_cur = label == current_section or current_page in [h for _, h in (sub or [])]
        if sub:
            links = "\n".join(
                f'<a href="{h}"{" aria-current=\"page\"" if h == current_page else ""}>{l}</a>' for l, h in sub)
            cls = "navlink dd-trigger is-current" if is_cur else "navlink dd-trigger"
            items.append(f'<div class="dd">\n<a class="{cls}" href="{href}" aria-haspopup="true">{label} {CARET}</a>\n<div class="dd-menu">\n{links}\n</div>\n</div>')
        else:
            if href == current_page:
                items.append(f'<a class="navlink" href="{href}" aria-current="page">{label}</a>')
            else:
                cls = "navlink is-current" if label == current_section else "navlink"
                items.append(f'<a class="{cls}" href="{href}">{label}</a>')
    links = "\n".join(items)
    return f"""<a class="skip-link" href="#contenuto">Vai al contenuto</a>
<header class="site-nav">
<nav aria-label="Principale" class="container nav-inner">
<a class="brand" href="index.html">
<img class="brand-logo" src="assets/logo-cas-ticino.webp" alt="CAS Ticino, Club Alpino Svizzero" width="146" height="44">
</a>
<div class="nav-links hide-sm">
{links}
</div>
<div class="nav-end">
<a class="nav-search" href="Cerca.html" aria-label="Cerca nel sito" title="Cerca nel sito"{' aria-current="page"' if current_page == "Cerca.html" else ""}><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="m13 13 5 5" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg></a>
<a class="btn btn--primary" href="{GITE}">Programma gite</a>
<button class="menu-toggle" type="button" aria-label="Apri menu"><span class="burger" aria-hidden="true"></span></button>
</div>
</nav>
</header>"""


SPONSORS = """<div class="sponsors">
<h2>Con il sostegno di</h2>
<a class="sponsor" href="https://www.bancastato.ch" target="_blank" rel="noopener"><img src="assets/sponsor/bancastato.webp" alt="BancaStato" width="172" height="24" loading="lazy"></a>
<a class="sponsor" href="https://www.ail.ch/privati.html" target="_blank" rel="noopener"><img src="assets/sponsor/ail.webp" alt="AIL" width="55" height="48" loading="lazy"></a>
<a class="sponsor" href="https://www.baechli-bergsport.ch/it" target="_blank" rel="noopener"><img src="assets/sponsor/baechli.webp" alt="Bächli Bergsport" width="52" height="48" loading="lazy"></a>
<a class="sponsor" href="https://www.dos-group.com/it/" target="_blank" rel="noopener"><img src="assets/sponsor/dos-group.webp" alt="DOS Group" width="64" height="48" loading="lazy"></a>
<span class="sponsor sponsor--white"><img src="assets/sponsor/studio-grafica-grizzi.webp" alt="Studio grafica Grizzi" width="79" height="48" loading="lazy"></span>
</div>"""


def footer():
    cols = []
    for label, _, sub in MENU:
        if not sub:
            continue
        name = {"Attività": "Attività"}.get(label, label)
        extra = [("News", "News.html")] if label == "Attività" else []
        extra_end = [("Adesione", "Adesione.html")] if label == "Attività" else []
        links = "\n".join(f'<a href="{h}">{l}</a>' for l, h in extra + sub + extra_end)
        cols.append(f'<nav class="footer-col" aria-label="{name}">\n<h2>{name}</h2>\n{links}\n</nav>')
    cols = "\n".join(cols)
    return f"""<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-brand">
<a class="brand" href="index.html">
<img class="brand-logo" src="assets/logo-cas-ticino.webp" alt="CAS Ticino, Club Alpino Svizzero" width="172" height="52" loading="lazy">
</a>
<address>Club Alpino Svizzero, Sezione Ticino<br>Casella postale 112, 6998 Monteggio 2<br>Sede: Canvetto Luganese, Molino Nuovo<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></address>
</div>
{cols}
</div>
{SPONSORS}
<div class="footer-bottom"><span>© 2026 CAS Ticino</span><span>Club Alpino Svizzero, Sezione Ticino</span><span>webmaster - michele.foletti</span></div>
</div>
</footer>
<script src="{asset("assets/site.js")}" defer></script>
</body>
</html>
"""


def pic(base, alt, sizes="100vw", mobile=None, w=None, h=None, lazy=True, cls=""):
    """Immagine con srcset 1000/2000 e, se indicata, un ritaglio dedicato per schermi stretti."""
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    dims = f' width="{w}" height="{h}"' if w else ""
    c = f' class="{cls}"' if cls else ""
    src = f'<picture>\n'
    if mobile:
        src += f'<source media="(max-width: 700px)" srcset="assets/img/{mobile}.webp">\n'
    src += f'<img src="assets/img/{base}-2000.webp" srcset="assets/img/{base}-1000.webp 1000w, assets/img/{base}-2000.webp 2000w" sizes="{sizes}" alt="{alt}"{dims}{load}{c}>\n</picture>'
    return src


def img(name, alt, w, h, lazy=True):
    load = ' loading="lazy" decoding="async"' if lazy else ""
    return f'<img src="assets/img/{name}.webp" alt="{alt}" width="{w}" height="{h}"{load}>'


def crumbs(*trail):
    """Percorso: coppie (etichetta, link); l'ultima voce è la pagina corrente (link None)."""
    parts = ['<a href="index.html">Home</a>']
    for label, href in trail:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
    return '<nav class="crumbs" aria-label="Percorso">' + "".join(parts) + "</nav>"


def page_hero(trail, title, lead, extra="", figure=None):
    """Intestazione delle pagine interne. figure: HTML di un'immagine verticale da mettere a lato."""
    body = f"""{crumbs(*trail)}
<h1 id="page-h" class="display fit">{title}</h1>
<p class="lead">{lead}</p>
{extra}"""
    if figure:
        return f"""<section class="page-hero page-hero--split" aria-labelledby="page-h">
<div class="container">
<div>
{body}
</div>
<figure>{figure}</figure>
</div>
</section>"""
    return f"""<section class="page-hero" aria-labelledby="page-h">
<div class="container">
{body}
</div>
</section>"""


def subnav(group, current_page):
    """Le altre pagine della stessa voce di menu (La Sezione, Attività)."""
    for label, _, sub in MENU:
        if label == group:
            cur = ' aria-current="page"'
            links = "\n".join(f'<a href="{h}"{cur if h == current_page else ""}>{l}</a>'
                              for l, h in sub if h.endswith(".html"))
            return f"""<section class="section" aria-label="{group}">
<div class="container subnav">
<h2 class="label">{group}</h2>
<div class="subnav-links">
{links}
</div>
</div>
</section>"""
    raise KeyError(group)


def in_sottocartella(page_html, su="../"):
    """Pagina pubblicata in una sottocartella (es. news/): i percorsi relativi salgono di un livello."""
    import re

    def fix(url):
        url = url.strip()
        if not url or url.startswith(("http:", "https:", "mailto:", "tel:", "#", "/", "data:", "../")):
            return url
        return su + url

    def attr(m):
        nome, val = m.group(1), m.group(2)
        if nome in ("srcset", "imagesrcset"):
            val = ", ".join(" ".join([fix(parte.split()[0])] + parte.split()[1:]) for parte in val.split(","))
        else:
            val = fix(val)
        return f'{nome}="{val}"'

    page_html = re.sub(r'\b(href|src|srcset|imagesrcset)="([^"]*)"', attr, page_html)
    return re.sub(r'(<meta property="og:image" content=")([^"]+)"', lambda m: m.group(1) + fix(m.group(2)) + '"', page_html)
