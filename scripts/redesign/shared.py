"""Parti comuni del nuovo design (intestazione, footer). Genera HTML statico.

Icone Instagram e Facebook: Simple Icons (simpleicons.org, CC0)."""
import hashlib, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def asset(path):
    """Percorso con impronta del contenuto (?v=…), così il browser non usa una copia vecchia in cache."""
    with open(os.path.join(ROOT, path), "rb") as f:
        # a capo uniformati: su Windows Git può dare CRLF, su GitHub LF, e l'impronta deve essere la stessa
        return f"{path}?v={hashlib.md5(f.read().replace(b'\r\n', b'\n')).hexdigest()[:8]}"

GITE_DROPTOUR = "https://ssl.dropnet.ch/casticino/gite/index.php"  # portale delle iscrizioni
GITE = "gite.html"  # programma gite nel sito (copia aggiornata da Droptour)

# Indirizzo pubblico del sito, con la barra finale: serve per canonical, og:image, hreflang, sitemap e per la pagina 404.
# Al passaggio del dominio diventa "https://casticino.ch/" (poi rigenerare tutte le pagine).
SITO = "https://fole89.github.io/casticino-site/"

MENU = [
    ("La Sezione", "index.html#sezione", [
        ("Introduzione", "introduzione.html"), ("Comitato", "comitato.html"),
        ("Organizzazione", "organizzazione.html"), ("Capigita", "capigita.html"), ("Sede e recapiti", "sede.html"),
        ("Storia", "storia.html"), ("Link utili", "link.html")]),
    ("News", "index.html#news", None),
    ("Attività", "index.html#attivita", [
        ("Giovani", "giovani.html"), ("Senior", "senior.html"),
        ("Corsi", "corsi.html"), ("Soccorso", "soccorso.html"), ("Noleggio", "noleggio.html")]),
    ("Capanne", "index.html#capanne", [
        ("Campo Tencia", "campotencia.html"), ("Cristallina", "cristallina.html"), ("Adula", "adula.html"),
        ("Motterascio", "motterascio.html"), ("Monte Bar", "montebar.html"), ("Baita del Luca", "baitadelluca.html")]),
    ("Media", "index.html#media", [
        ("Foto e resoconti", "foto.html"), ("Annuari", "annuari.html"), ("Informazione", "informazione.html"),
        ("Documenti", "documenti.html")]),
    ("Adesione", "adesione.html", None),
]

# Versione tedesca: le pagine tradotte sono in de/ (stesso nome di file). News, attività, media e PDF restano
# solo in italiano e nel menu tedesco non compaiono.
MENU_DE = [
    ("Die Sektion", "de/introduzione.html", [
        ("Einführung", "de/introduzione.html"), ("Vorstand", "de/comitato.html"),
        ("Organisation", "de/organizzazione.html"), ("Tourenleitende", "de/capigita.html"),
        ("Sitz und Kontakt", "de/sede.html"),
        ("Geschichte", "de/storia.html"), ("Nützliche Links", "de/link.html")]),
    ("Hütten", "de/index.html#capanne", [
        ("Campo Tencia", "de/campotencia.html"), ("Cristallina", "de/cristallina.html"), ("Adula", "de/adula.html"),
        ("Motterascio", "de/motterascio.html"), ("Monte Bar", "de/montebar.html"), ("Baita del Luca", "de/baitadelluca.html")]),
    ("Mitgliedschaft", "de/adesione.html", None),
]

# Versione inglese: come quella tedesca, in en/ (stesse pagine, stessi nomi di file).
MENU_EN = [
    ("The Section", "en/introduzione.html", [
        ("Introduction", "en/introduzione.html"), ("Committee", "en/comitato.html"),
        ("Organisation", "en/organizzazione.html"), ("Trip leaders", "en/capigita.html"),
        ("Office and contacts", "en/sede.html"),
        ("History", "en/storia.html"), ("Useful links", "en/link.html")]),
    ("Huts", "en/index.html#capanne", [
        ("Campo Tencia", "en/campotencia.html"), ("Cristallina", "en/cristallina.html"), ("Adula", "en/adula.html"),
        ("Motterascio", "en/motterascio.html"), ("Monte Bar", "en/montebar.html"), ("Baita del Luca", "en/baitadelluca.html")]),
    ("Membership", "en/adesione.html", None),
]

LINGUE = ("it", "de", "en")  # l'italiano è la lingua principale; le altre hanno solo La Sezione, le capanne e Adesione
LINGUA = {"lang": "it"}      # lingua della pagina che si sta generando
PAGINE_LINGUA = {"de": set(), "en": set()}  # pagine (percorso italiano dalla radice) tradotte in ogni lingua; le riempie pages.py
NOMI_LINGUE = {"it": "Italiano", "de": "Deutsch", "en": "English"}

# testi fissi dell'interfaccia (quelli delle capanne sono in capanne_de.py)
T = {
    "it": dict(skip="Vai al contenuto", nav="Principale", menu_apri="Apri menu", menu_chiudi="Chiudi menu", menu="Menu",
               logo_sotto="Club Alpino Svizzero", cerca="Cerca nel sito", gite="Programma gite",
               lingua="Deutsch", percorso="Percorso", seguici="Seguici", sostegno="Con il sostegno di",
               indirizzo="Club Alpino Svizzero, Sezione Ticino<br>Casella postale 112, 6998 Monteggio 2<br>Sede: Canvetto Luganese, Molino Nuovo",
               sezione="Club Alpino Svizzero, Sezione Ticino", su_instagram="CAS Ticino su Instagram", su_facebook="CAS Ticino su Facebook",
               redazione="Area redazione", locale="it_CH"),
    "de": dict(skip="Zum Inhalt", nav="Hauptnavigation", menu_apri="Menü öffnen", menu_chiudi="Menü schliessen", menu="Menü",
               logo_sotto="Schweizer Alpen-Club", cerca="Suche (italienisch)", gite="Tourenprogramm",
               lingua="Italiano", percorso="Pfad", seguici="Folgen Sie uns", sostegno="Mit Unterstützung von",
               indirizzo="Schweizer Alpen-Club SAC, Sektion Ticino<br>Postfach 112, 6998 Monteggio 2<br>Sitz: Canvetto Luganese, Molino Nuovo",
               sezione="Schweizer Alpen-Club SAC, Sektion Ticino", su_instagram="CAS Ticino auf Instagram", su_facebook="CAS Ticino auf Facebook",
               redazione="Redaktion", locale="de_CH", adesione="Mitgliedschaft"),
    "en": dict(skip="Skip to content", nav="Main", menu_apri="Open menu", menu_chiudi="Close menu", menu="Menu",
               logo_sotto="Swiss Alpine Club", cerca="Search (in Italian)", gite="Trip programme",
               lingua="English", percorso="Breadcrumb", seguici="Follow us", sostegno="With the support of",
               indirizzo="Swiss Alpine Club SAC, Ticino Section<br>PO Box 112, 6998 Monteggio 2<br>Office: Canvetto Luganese, Molino Nuovo",
               sezione="Swiss Alpine Club SAC, Ticino Section", su_instagram="CAS Ticino on Instagram", su_facebook="CAS Ticino on Facebook",
               redazione="Editors", locale="en_GB", adesione="Membership"),
}


def de():
    return LINGUA["lang"] == "de"


def en():
    return LINGUA["lang"] == "en"


def tr(it, de_, en_):
    """Lo stesso testo nelle tre lingue: restituisce quello della lingua corrente."""
    return {"it": it, "de": de_, "en": en_}[LINGUA["lang"]]


def t(chiave):
    return T[LINGUA["lang"]][chiave]


def menu():
    return {"it": MENU, "de": MENU_DE, "en": MENU_EN}[LINGUA["lang"]]


def L(href):
    """Link a una pagina del sito (percorso dalla radice): nelle versioni tradotte porta alla pagina tradotta, se c'è."""
    lang = LINGUA["lang"]
    if lang != "it" and href.split("#")[0] in PAGINE_LINGUA[lang]:
        return f"{lang}/" + href
    return href


def in_lingua(pagina, lang):
    """La stessa pagina in un'altra lingua (la home di quella lingua, se la pagina non è tradotta)."""
    base = pagina[3:] if pagina[:3] in ("de/", "en/") else pagina
    if lang == "it":
        return base
    return f"{lang}/{base}" if base in PAGINE_LINGUA[lang] else f"{lang}/index.html"


CARET = '<span class="caret" aria-hidden="true"></span>'


def head(title, description, extra=""):
    return f"""<!doctype html>
<html lang="{LINGUA['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{t('locale')}">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="assets/logo-cas.webp">
<link rel="preload" href="assets/fonts/geist-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{asset("assets/site.css")}">
<script>document.documentElement.classList.add('js')</script>
{extra}</head>"""


def nav(current_page, current_section=None):
    """current_page: nome file della pagina (per aria-current). current_section: voce di primo livello attiva."""
    items = []
    for label, href, sub in menu():
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
    lingue = "\n".join(f'<a class="nav-lang" href="{in_lingua(current_page, l)}" hreflang="{l}" lang="{l}" title="{NOMI_LINGUE[l]}">{l.upper()}</a>'
                       for l in LINGUE if l != LINGUA["lang"])
    return f"""<a class="skip-link" href="#contenuto">{t('skip')}</a>
<header class="site-nav">
<nav aria-label="{t('nav')}" class="container nav-inner">
<a class="brand" href="{L('index.html')}">
<img class="brand-logo" src="assets/logo-cas-stemma.webp" alt="" width="37" height="44">
<span class="brand-text"><strong>CAS Ticino</strong><span>{t('logo_sotto')}</span></span>
</a>
<div class="nav-links hide-sm">
{links}
</div>
<div class="nav-end">
<div class="nav-langs">
{lingue}
</div>
<a class="nav-search" href="cerca.html" aria-label="{t('cerca')}" title="{t('cerca')}"{' aria-current="page"' if current_page == "cerca.html" else ""}><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="m13 13 5 5" stroke="currentColor" stroke-width="2" stroke-linecap="square"/></svg></a>
<a class="btn btn--primary" href="{GITE}"{' aria-current="page"' if current_page == "gite.html" else ""}>{t('gite')}</a>
<button class="menu-toggle" type="button" aria-label="{t('menu_apri')}" data-chiudi="{t('menu_chiudi')}" data-titolo="{t('menu')}"><span class="burger" aria-hidden="true"></span></button>
</div>
</nav>
</header>"""


SPONSORS = """<div class="sponsors">
<h2>{sostegno}</h2>
<a class="sponsor" href="https://www.bancastato.ch" target="_blank" rel="noopener"><img src="assets/sponsor/bancastato.webp" alt="BancaStato" width="172" height="24" loading="lazy"></a>
<a class="sponsor" href="https://www.ail.ch/privati.html" target="_blank" rel="noopener"><img src="assets/sponsor/ail.webp" alt="AIL" width="55" height="48" loading="lazy"></a>
<a class="sponsor" href="https://www.baechli-bergsport.ch/it" target="_blank" rel="noopener"><img src="assets/sponsor/baechli.webp" alt="Bächli Bergsport" width="52" height="48" loading="lazy"></a>
<a class="sponsor" href="https://www.dos-group.com/it/" target="_blank" rel="noopener"><img src="assets/sponsor/dos-group.webp" alt="DOS Group" width="64" height="48" loading="lazy"></a>
<span class="sponsor sponsor--white"><img src="assets/sponsor/studio-grafica-grizzi.webp" alt="Studio grafica Grizzi" width="79" height="48" loading="lazy"></span>
</div>"""



def social(cls=""):
    """Link a Instagram e Facebook della sezione (icona + nome): nel footer, in home sotto «Dalla sezione» e nella pagina News."""
    return f"""<div class="social{cls}">
<span class="social-label">{t('seguici')}</span>
<a href="https://instagram.com/casticino" rel="noopener" aria-label="{t('su_instagram')}"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/></svg><span>Instagram</span></a>
<a href="https://facebook.com/eventicasticino" rel="noopener" aria-label="{t('su_facebook')}"><svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M9.101 23.691v-7.98H6.627v-3.667h2.474v-1.58c0-4.085 1.848-5.978 5.858-5.978.401 0 .955.042 1.468.103a8.68 8.68 0 0 1 1.141.195v3.325a8.623 8.623 0 0 0-.653-.036 26.805 26.805 0 0 0-.733-.009c-.707 0-1.259.096-1.675.309a1.686 1.686 0 0 0-.679.622c-.258.42-.374.995-.374 1.752v1.297h3.919l-.386 2.103-.287 1.564h-3.246v8.245C19.396 23.238 24 18.179 24 12.044c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.628 3.874 10.35 9.101 11.647Z"/></svg><span>Facebook</span></a>
</div>"""


def footer():
    cols = []
    for label, _, sub in menu():
        if not sub:
            continue
        name = label
        extra = [("News", "news.html")] if label == "Attività" else []
        extra_end = [("Adesione", "adesione.html")] if label == "Attività" else []
        if LINGUA["lang"] != "it" and not cols:  # versioni tradotte: Adesione in fondo alla prima colonna
            extra_end = [(t("adesione"), L("adesione.html"))]
        links = "\n".join(f'<a href="{h}">{l}</a>' for l, h in extra + sub + extra_end)
        cols.append(f'<nav class="footer-col" aria-label="{name}">\n<h2>{name}</h2>\n{links}\n</nav>')
    cols = "\n".join(cols)
    return f"""<footer class="site-footer">
<div class="container">
<div class="footer-grid">
<div class="footer-brand">
<a class="brand" href="{L('index.html')}">
<img class="brand-logo" src="assets/logo-cas-stemma.webp" alt="" width="44" height="52" loading="lazy">
<span class="brand-text"><strong>CAS Ticino</strong><span>{t('logo_sotto')}</span></span>
</a>
<address>{t('indirizzo')}<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></address>
{social()}
</div>
{cols}
</div>
{SPONSORS.replace("{sostegno}", t('sostegno'))}
<div class="footer-bottom"><span>© 2026 CAS Ticino</span><span>{t('sezione')}</span><a href="admin/">{t('redazione')}</a></div>
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
    parts = [f'<a href="{L("index.html")}">Home</a>']
    for label, href in trail:
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
    return f'<nav class="crumbs" aria-label="{t("percorso")}">' + "".join(parts) + "</nav>"


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
    for label, _, sub in menu():
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
