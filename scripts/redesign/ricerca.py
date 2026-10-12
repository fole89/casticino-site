"""Ricerca: indice data/cerca.json (testo di ogni pagina, PDF, pubblicazioni, link, album foto) e pagina cerca.html."""
from html import unescape as html_unescape
from comune import *
from pagine_servizi import DOCS, LINKS
from pagine_media import NEWS, pubblicazioni
from pagine_attivita import gite_dati


TIPI = {"news/": "Notizia", "capanne/": "Capanna", "campotencia.html": "Capanna", "cristallina.html": "Capanna", "adula.html": "Capanna",
        "motterascio.html": "Capanna", "montebar.html": "Capanna", "baitadelluca.html": "Capanna"}
FUORI_INDICE = {"gita.html", "news.html", "cerca.html", "offline.html"}  # elenchi che ripetono il contenuto di altre pagine


def solo_testo(frammento):
    t = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", frammento, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r" ([,.;:!?])", r"\1", re.sub(r"\s+", " ", html_unescape(t).replace("→", " "))).strip()


def voce_pagina(file, page_html):
    """Titolo e testo principale di una pagina generata (senza menu, footer, percorso e sottomenu)."""
    titolo = re.search(r"<title>(.*?)</title>", page_html, flags=re.S).group(1)
    titolo = html_unescape(titolo.replace(" | CAS Ticino", "")).strip()
    main = page_html.split('<main id="contenuto">', 1)[1].split("</main>", 1)[0]
    main = re.sub(r'<nav class="crumbs".*?</nav>', " ", main, flags=re.S)
    main = re.sub(r'<section class="section" aria-label="[^"]*">\s*<div class="container subnav">.*?</section>', " ", main, flags=re.S)
    main = main.split('<nav class="article-pager"', 1)[0]  # articoli: niente «Altre notizie»
    tipo = next((v for k, v in TIPI.items() if file.startswith(k)), "Pagina")
    voce = {"t": titolo, "u": file, "k": tipo, "x": solo_testo(main)[:6000]}
    if file.startswith("news/"):
        n = next(n for n in NEWS if n["file"] == file)
        voce.update(d=n["date"], dt=data_it(n["date"]))
        voce["x"] = voce["x"].replace(data_it(n["date"]), "", 1).replace(voce["t"], "", 1).strip()
    if file == "index.html":
        voce["t"] = "Home"
    return voce


def indice_ricerca(pagine):
    voci = [voce_pagina(f, h) for f, h in pagine.items() if f not in FUORI_INDICE and not f.startswith(("de/", "en/"))]
    for gruppo, links in DOCS:
        for nome, url in links:
            voci.append({"t": nome, "u": url, "k": "PDF", "x": f"Documenti, {gruppo}"})
    for x in pubblicazioni("annuari", "annuario"):
        voci.append({"t": f"Annuario {x['anno']}", "u": x["pdf"], "k": "Annuario", "d": f"{x['anno']}-12-31", "x": "Annuario della sezione, PDF"})
    for x in pubblicazioni("informazione", "informazione"):
        voci.append({"t": f"Informazione, {x['quando']}", "u": x["pdf"], "k": "Informazione", "d": f"{x['anno']}-{MESI.index(x['mese']) + 1 if x['mese'] else 1:02d}-01",
                     "x": "Il bollettino della sezione, PDF"})
    for gruppo, links in LINKS:
        for nome, url in links:
            voci.append({"t": nome, "u": url, "k": "Link", "x": f"Link utili, {gruppo}"})
    albums = json.load(open(os.path.join(ROOT, "data", "foto.json"), encoding="utf-8")).get("albums", [])
    for a in albums:
        if a.get("photos"):
            # l'album si apre nella pagina Foto e resoconti (foto.js carica gli album fino a quello e ci scorre sopra)
            voci.append({"t": a["title"], "u": f"foto.html#album-{a['id']}" if a.get("id") else "foto.html", "k": "Foto e resoconto gita", "d": a.get("date", ""),
                         "dt": data_it(a["date"]) if a.get("date") else "", "x": " ".join(filter(None, [a.get("place"), a.get("text")]))[:3000]})
    for g in gite_dati():
        voci.append({"t": g["titolo"], "u": f"gita.html?id={g['id']}", "k": "Gita", "d": g["dal"], "dt": data_it(g["dal"]),
                     "x": " ".join(filter(None, [g["tipo"], ", ".join(g["gruppi"]), ", ".join(g["capigita"]), g["descrizione"]]))})
    return {"voci": voci}


def cerca_pagina():
    body = page_hero([("Cerca", None)], "Cerca", "Cerca tra pagine, notizie, capanne, documenti, annuari e foto delle gite.",
                     f"""<form class="cerca-form" id="cerca-form" role="search" action="cerca.html" data-indice="{asset("data/cerca.json")}">
<label class="visually-hidden" for="cerca-q">Cerca nel sito</label>
<input id="cerca-q" name="q" type="search" placeholder="Es. Cristallina, corso racchette, statuto…" autocomplete="off" autofocus>
<button class="btn btn--primary" type="submit">Cerca</button>
</form>""") + """

<section class="section section--tight" aria-label="Risultati">
<div class="container">
<p class="cerca-stato" id="cerca-stato" role="status" aria-live="polite"></p>
<ol class="cerca-lista" id="cerca-risultati"></ol>
<noscript><p>La ricerca ha bisogno di JavaScript attivo.</p></noscript>
</div>
</section>"""
    return page("cerca.html", "Cerca | CAS Ticino", "Cerca nel sito della Sezione Ticino del Club Alpino Svizzero.",
                body, scripts=f'<script src="{asset("assets/cerca.js")}" defer></script>\n')
