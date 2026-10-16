"""Nuovo design: genera tutte le pagine del sito.

Le pagine sono nei moduli pagine_*.py (un modulo per gruppo del menu), le funzioni comuni in comune.py,
la ricerca in ricerca.py; qui l'elenco delle pagine (PAGES), le versioni tradotte e la scrittura dei file.

Uso: python scripts/redesign/pages.py [Pagina.html ...]  (senza argomenti rigenera tutto)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import pwa
from capanne import CONTENUTI
from capanne_de import CONTENUTI_DE
from capanne_en import CONTENUTI_EN
from capanne_fr import CONTENUTI_FR
from shared import LINGUE, SITO, TRADUZIONI, senza_lingua
from urllib.parse import urljoin
from comune import *
from pagine_capanne import hut, hut_foto, hut_page, HUT_PAGES
from pagine_servizi import documenti, link, mercatino, noleggio
from pagine_media import annuari, foto, informazione, news, NEWS, news_article
from pagine_attivita import corsi, giovani, gita_pagina, gite, partecipare, senior
from pagine_home import home
from pagine_sezione import capigita, comitato, introduzione, introduzione_tradotta, organizzazione, sede, soccorso, storia, volontariato
from pagine_altre import adesione, offline_pagina, privacy
from ricerca import cerca_pagina, indice_ricerca


PAGES = {
    "index.html": home,
    "introduzione.html": introduzione, "comitato.html": comitato, "organizzazione.html": organizzazione,
    "sede.html": sede, "storia.html": storia, "link.html": link, "documenti.html": documenti,
    "news.html": news, "gite.html": gite, "gita.html": gita_pagina, "foto.html": foto, "annuari.html": annuari, "informazione.html": informazione,
    "adesione.html": adesione,
    "giovani.html": giovani, "senior.html": senior, "corsi.html": corsi, "noleggio.html": noleggio, "mercatino.html": mercatino,
    "soccorso.html": soccorso, "capigita.html": capigita, "privacy.html": privacy,
    "partecipare.html": partecipare, "volontariato.html": volontariato, "offline.html": offline_pagina,
}
for _f in HUT_PAGES:
    PAGES[_f] = (lambda f: lambda: hut(f))(_f)
for _f, _c in CONTENUTI.items():
    for _p in _c["pagine"] + ([_c["storia"]] if _c.get("storia") else []):
        PAGES[f"capanne/{_c['cartella']}/{_p['file']}.html"] = (lambda f, p: lambda: hut_page(f, p))(_f, _p)
    if _c.get("foto"):
        PAGES[f"capanne/{_c['cartella']}/foto.html"] = (lambda f: lambda: hut_foto(f))(_f)
for _i, _n in enumerate(NEWS):
    PAGES[_n["file"]] = (lambda i: lambda: news_article(i))(_i)


def in_lingua_pagina(lang, fn):
    """Genera una pagina con la lingua impostata a `lang` (de, fr, en)."""
    def genera():
        LINGUA["lang"] = lang
        try:
            return localizza(fn(), lang)
        finally:
            LINGUA["lang"] = "it"
    return genera


# Versioni tradotte (de/, fr/, en/): tutte le pagine tranne la ricerca. Restano in italiano i contenuti scritti da altri
# (news, annunci del mercatino, gite e resoconti di Droptour) e i PDF; nelle pagine tradotte sono marcati lang="it".
for _lang, _contenuti in (("de", CONTENUTI_DE), ("fr", CONTENUTI_FR), ("en", CONTENUTI_EN)):
    _pagine = {"index.html": home, "introduzione.html": introduzione_tradotta, "comitato.html": comitato,
               "organizzazione.html": organizzazione, "capigita.html": capigita, "sede.html": sede,
               "storia.html": storia, "link.html": link, "adesione.html": adesione,
               "gite.html": gite, "gita.html": gita_pagina, "privacy.html": privacy,
               "noleggio.html": noleggio, "mercatino.html": mercatino, "documenti.html": documenti,
               "partecipare.html": partecipare, "corsi.html": corsi, "giovani.html": giovani, "senior.html": senior,
               "soccorso.html": soccorso, "volontariato.html": volontariato,
               "news.html": news, "foto.html": foto, "annuari.html": annuari, "informazione.html": informazione,
               "offline.html": offline_pagina}
    for _i, _n in enumerate(NEWS):
        _pagine[_n["file"]] = (lambda i: lambda: news_article(i))(_i)
    for _f in HUT_PAGES:
        _pagine[_f] = (lambda f: lambda: hut(f))(_f)
    for _f, _c in _contenuti.items():
        for _p in _c["pagine"] + ([_c["storia"]] if _c.get("storia") else []):
            _pagine[f"capanne/{_c['cartella']}/{_p['file']}.html"] = (lambda f, p: lambda: hut_page(f, p))(_f, _p)
        if _c.get("foto"):
            _pagine[f"capanne/{_c['cartella']}/foto.html"] = (lambda f: lambda: hut_foto(f))(_f)
    PAGINE_LINGUA[_lang].update(_pagine)  # per il selettore di lingua e per i link L()
    for _f, _fn in _pagine.items():
        PAGES[f"{_lang}/" + _f] = in_lingua_pagina(_lang, _fn)


def indirizzo(name):
    """Indirizzo pubblico di una pagina, senza .html (come lo mostra site.js nella barra degli indirizzi)."""
    return SITO + re.sub(r"(^|/)index\.html$", r"\1", name).removesuffix(".html")


def metadati(name, html):
    """Aggiunge alla testa canonical, og:url, og:image con indirizzo completo e, se la pagina è tradotta, gli hreflang."""
    url = indirizzo(name)
    html = re.sub(r'(<meta property="og:image" content=")([^"]+)"', lambda m: m.group(1) + urljoin(SITO + name, m.group(2)) + '"', html, count=1)
    righe = [f'<link rel="canonical" href="{url}">', f'<meta property="og:url" content="{url}">']
    it = senza_lingua(name)
    lingue = [lang for lang in TRADUZIONI if it in PAGINE_LINGUA[lang]]
    if lingue:
        righe += [f'<link rel="alternate" hreflang="it" href="{indirizzo(it)}">']
        righe += [f'<link rel="alternate" hreflang="{lang}" href="{indirizzo(lang + "/" + it)}">' for lang in lingue]
        righe += [f'<link rel="alternate" hreflang="x-default" href="{indirizzo(it)}">']
    return html.replace("</head>", "\n".join(righe) + "\n</head>", 1)


def pagina_404():
    """Pagina mostrata da GitHub Pages per ogni indirizzo che non esiste, a qualsiasi profondità:
    <base> fa partire i percorsi relativi dalla radice del sito."""
    body = page_hero([("Pagina non trovata", None)], "Pagina non trovata",
                     "La pagina che cerchi non esiste o è stata spostata. Dal nuovo sito alcuni indirizzi sono cambiati: prova dalla home o con la ricerca.",
                     """<div class="non-trovata">
<form class="cerca-form" role="search" action="cerca.html">
<label class="visually-hidden" for="cerca-q">Cerca nel sito</label>
<input id="cerca-q" name="q" type="search" placeholder="Es. Cristallina, corso racchette, statuto…" autocomplete="off">
<button class="btn btn--primary" type="submit">Cerca</button>
</form>
<div class="actions"><a class="btn btn--secondary" href="index.html">Vai alla home</a></div>
<div class="altre-lingue">
<p class="small" lang="de">Seite nicht gefunden. <a href="de/index.html">Zur Startseite</a></p>
<p class="small" lang="fr">Page introuvable. <a href="fr/index.html">Aller à l’accueil</a></p>
<p class="small" lang="en">Page not found. <a href="en/index.html">Go to the home page</a></p>
</div>
</div>""")
    html = page("404.html", "Pagina non trovata | CAS Ticino", "La pagina cercata non esiste sul sito del CAS Ticino.", body)
    return html.replace("<head>\n", f'<head>\n<base href="{SITO}">\n<meta name="robots" content="noindex">\n', 1)


def sitemap(nomi):
    righe = "\n".join(f"<url><loc>{indirizzo(n)}</loc></url>" for n in sorted(nomi))
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{righe}\n</urlset>\n'


def scrivi(name, contenuto):
    os.makedirs(os.path.dirname(os.path.join(ROOT, name)), exist_ok=True)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", name)


if __name__ == "__main__":
    only = sys.argv[1:]
    # tutte le pagine vengono generate comunque: servono per l'indice della ricerca
    pagine = {name: metadati(name, fn()) for name, fn in PAGES.items()}
    for name, contenuto in pagine.items():
        if not only or name in only:
            scrivi(name, contenuto)
    if not only or "404.html" in only:
        scrivi("404.html", pagina_404())
    # sempre, come cerca.json: cambia quando si aggiunge o toglie una pagina (es. una news)
    # gita.html vale solo con ?id=; offline.html la mostra solo il service worker
    scrivi("sitemap.xml", sitemap([p for p in pagine if not p.endswith(("gita.html", "offline.html"))] + ["cerca.html"]))
    # sito installabile (pwa.py): manifesto per lingua e service worker
    for _lang in LINGUE:
        scrivi("manifest.webmanifest" if _lang == "it" else f"manifest-{_lang}.webmanifest", pwa.manifest(_lang))
    _essenziali = ["index.html", "partecipare.html", "soccorso.html"] + list(HUT_PAGES)
    _statici = ([asset(f) for f in ("assets/site.css", "assets/site.js", "assets/gite.js", "assets/cerca.js", "assets/foto.js", "assets/noleggio.js")]
                + [f"assets/fonts/{f}" for f in sorted(os.listdir(os.path.join(ROOT, "assets", "fonts"))) if f.endswith(".woff2")]
                + ["assets/logo-cas.webp", "assets/logo-cas-stemma.webp"] + [i["src"] for i in pwa.ICONE] + ["assets/icone/apple-touch-icon.png", pwa.BADGE]
                + ["offline.html"] + [f"{l}/offline.html" for l in TRADUZIONI])
    scrivi("sw.js", pwa.service_worker(_statici, {"it": _essenziali, **{l: [f"{l}/{p}" for p in _essenziali] for l in TRADUZIONI}}))
    scrivi("robots.txt", f"User-agent: *\nDisallow: /admin/\n\nSitemap: {SITO}sitemap.xml\n")
    with open(os.path.join(ROOT, "data", "cerca.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(indice_ricerca(pagine), f, ensure_ascii=False, separators=(",", ":"))
    print("scritto data/cerca.json")
    if not only or "cerca.html" in only:
        scrivi("cerca.html", metadati("cerca.html", cerca_pagina()))  # dopo l'indice: il link porta l'impronta di cerca.json
