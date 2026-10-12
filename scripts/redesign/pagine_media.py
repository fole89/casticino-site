"""News e media: News (NEWS, elenco e una pagina per news), Foto e resoconti, Annuari, Informazione."""
from shared import crumbs
from comune import *


def carica_news():
    """Le news di data/news/*.json (vedi news_util.py) pronte per le pagine: testo in HTML, foto con le dimensioni, estratto."""
    out, presi = [], set()
    for n in news_util.leggi_tutte():
        corpo = news_util.md_html(n["testo"]) if (n.get("testo") or "").strip() else n.get("html", "")
        corpo = "\n".join(x for x in (corpo, news_util.allegati_html(n.get("allegati"))) if x)
        corpo = re.sub(r"<a\b[^>]*>\s*</a>", "", corpo)  # link vuoti rimasti dall'import da WordPress
        if "<h2" not in corpo:  # sotto il titolo della pagina (h1) i sottotitoli partono da h2
            corpo = re.sub(r"<(/?)h3\b", r"<\1h2", corpo)
        immagine = None
        if n.get("image") and n["image"].endswith(".webp") and os.path.exists(os.path.join(ROOT, n["image"])):
            w, h = webp_size(os.path.join(ROOT, n["image"]))
            immagine = {"src": n["image"], "w": w, "h": h, "alt": n.get("alt", "")}
        file = n.get("file") or news_util.nome_file(n, presi)
        presi.add(file)
        out.append({"title": n["title"].strip(), "date": n["date"][:10], "category": n.get("category", ""), "image": immagine,
                    "excerpt": (n.get("excerpt") or "").strip() or news_util.estratto(corpo), "html": corpo, "file": file})
    return out


NEWS = carica_news()


def og_name(n):
    """Nome dell'immagine per og:image (page() aggiunge assets/img/ e .webp)."""
    return n["image"]["src"][len("assets/img/"):-len(".webp")] if n["image"] else "paesaggi/cresta-lugano-2000"


# Categorie delle news: le stesse (e nello stesso ordine) della lista in admin/config.yml (campo «category»)
CATEGORIE = {"Capanne": ("Hütten", "Huts"), "Gite": ("Touren", "Trips"), "Corsi": ("Kurse", "Courses"),
             "Giovani": ("Jugend", "Youth"), "Senior": ("Senioren", "Seniors"), "Sezione": ("Sektion", "Section"),
             "Eventi": ("Anlässe", "Events"), "Incontri": ("Vorträge", "Talks"), "Itinerario": ("Tourenidee", "Route idea"),
             "Sicurezza": ("Sicherheit", "Safety")}


def categoria_l(cat):
    """Nome della categoria nella lingua della pagina (una categoria sconosciuta resta com'è)."""
    if cat not in CATEGORIE:
        return cat
    return tr(cat, *CATEGORIE[cat])


def categoria_slug(cat):
    return slug_nome(cat) if cat else ""


def news_meta(n):
    cat = f'<span class="news-cat">{esc(categoria_l(n["category"]))}</span>' if n["category"] else ""
    return f'<p class="news-meta"><time datetime="{n["date"]}">{data_l(n["date"])}</time>{cat}</p>'


def news_card(n, feature=False, filtro=False):
    """Scheda di una notizia: foto (o blocco rosso con la data se manca), data e categoria, titolo, estratto (in italiano).
    filtro: nella pagina News la categoria va anche in data-ruoli, per il filtro (site.js)."""
    if n["image"]:
        im = n["image"]
        fig = f'<figure><img src="{im["src"]}" alt="" width="{im["w"]}" height="{im["h"]}" loading="lazy" decoding="async"></figure>'
    else:
        y, m, d = n["date"].split("-")
        fig = f'<figure class="news-noimg" aria-hidden="true"><strong>{int(d)}</strong><span>{MESI_L[LINGUA["lang"]][int(m) - 1]} {y}</span></figure>'
    cls = "news-card news-card--feature" if feature else "news-card"
    tag = "h2" if feature else "h3"
    ruoli = f' data-ruoli="{categoria_slug(n["category"])}"' if filtro else ""
    return f"""<a class="{cls}" href="{n['file']}"{ruoli}>
{fig}
<div class="news-card-body">
{news_meta(n)}
<{tag}{in_it()}>{esc(n['title'])}</{tag}>
<p{in_it()}>{esc(n['excerpt'])}</p>
</div>
</a>"""


def news():
    anni = []
    for n in NEWS[1:]:
        y = n["date"][:4]
        if not anni or anni[-1][0] != y:
            anni.append((y, []))
        anni[-1][1].append(n)
    salti = "\n".join(f'<a href="#anno-{y}">{y}</a>' for y, _ in anni)
    gruppi = "\n".join(f"""<section class="news-year" id="anno-{y}" aria-labelledby="anno-{y}-h" data-filtro-gruppo>
<h2 id="anno-{y}-h" class="news-year-h">{y}</h2>
<div class="news-grid">
{chr(10).join(news_card(n, filtro=True) for n in items)}
</div>
</section>""" for y, items in anni)
    # filtro per categoria (site.js): solo le categorie usate, nell'ordine di CATEGORIE
    conta = {}
    for n in NEWS:
        if n["category"]:
            conta[n["category"]] = conta.get(n["category"], 0) + 1
    cats = [c for c in CATEGORIE if c in conta] + sorted(c for c in conta if c not in CATEGORIE)
    filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">{tr("Tutte", "Alle", "All")} <span class="num">{len(NEWS)}</span></button>'] +
                       [f'<button type="button" data-filtro="{categoria_slug(c)}" aria-pressed="false">{esc(categoria_l(c))} <span class="num">{conta[c]}</span></button>'
                        for c in cats])
    body = page_hero([("News", None)], "News", tr(
        "Serate, eventi, corsi e avvisi della sezione: tutte le notizie, dalla più recente.",
        "Abende, Anlässe, Kurse und Hinweise der Sektion: alle Meldungen, die neuesten zuerst. Die News erscheinen auf Italienisch.",
        "Evenings, events, courses and notices from the section: all the news, most recent first. The news is published in Italian."), social()) + f"""

<div id="notizie">
<section class="section section--filtro" aria-label="{tr("Filtra per categoria", "Nach Kategorie filtern", "Filter by category")}">
<div class="container">
<div class="filtro" role="group" aria-label="{tr("Filtra per categoria", "Nach Kategorie filtern", "Filter by category")}" data-filtra="#notizie" data-uno="{tr("notizia", "Meldung", "news item")}" data-molti="{tr("notizie", "Meldungen", "news items")}" hidden>
{filtri}
</div>
<p class="small filtro-stato" id="filtro-stato" aria-live="polite"></p>
</div>
</section>

<section class="section section--dopo-filtro" aria-label="{tr("Ultima notizia", "Neueste Meldung", "Latest news")}" data-filtro-gruppo>
<div class="container">
{news_card(NEWS[0], feature=True, filtro=True)}
</div>
</section>

<section class="section section--tight" aria-label="{tr("Archivio delle notizie", "Archiv der Meldungen", "News archive")}">
<div class="container">
<nav class="subnav news-years" aria-label="{tr("Anni", "Jahre", "Years")}">
<h2 class="label">{tr("Archivio", "Archiv", "Archive")}</h2>
<div class="subnav-links">
{salti}
</div>
</nav>
{gruppi}
</div>
</section>
</div>

{subnav(NM_MENU(), L("news.html"))}"""
    return sezione_page("news.html", "News | CAS Ticino", tr(
        "Le notizie della Sezione Ticino del Club Alpino Svizzero: serate, eventi, corsi, avvisi di sicurezza e vita delle capanne.",
        "Die Meldungen der SAC-Sektion Ticino (italienisch): Abende, Anlässe, Kurse, Sicherheitshinweise und das Leben in den Hütten.",
        "News from the SAC Ticino Section (in Italian): evenings, events, courses, safety notices and life in the huts."),
        body, og=og_name(NEWS[0]), section=NM_MENU())


def news_article(i):
    n = NEWS[i]
    corpo = n["html"]
    fig = ""
    if n["image"]:
        im = n["image"]
        # l'immagine principale sta già accanto al testo: niente doppione dentro l'articolo
        src = re.escape(im["src"])
        corpo = re.sub(r'<figure>\s*<img src="' + src + r'"[^>]*>\s*(<figcaption>.*?</figcaption>)?\s*</figure>', "", corpo, flags=re.S)
        corpo = re.sub(r'<img src="' + src + r'"[^>]*>', "", corpo)
        alt = esc(im["alt"]) or esc(n["title"])
        fig = f'<figure class="article-figure"><img src="{im["src"]}" alt="{alt}" width="{im["w"]}" height="{im["h"]}" fetchpriority="high"></figure>'
    piu_recente = NEWS[i - 1] if i > 0 else None
    meno_recente = NEWS[i + 1] if i + 1 < len(NEWS) else None
    prec, succ = tr("Notizia precedente", "Vorherige Meldung", "Previous news"), tr("Notizia successiva", "Nächste Meldung", "Next news")
    prev = (f'<a class="article-prev" href="{meno_recente["file"]}"><span class="label">{prec}</span><strong{in_it()}>{esc(meno_recente["title"])}</strong></a>'
            if meno_recente else "<span></span>")
    nxt = (f'<a class="article-next" href="{piu_recente["file"]}"><span class="label">{succ}</span><strong{in_it()}>{esc(piu_recente["title"])}</strong></a>'
           if piu_recente else "<span></span>")
    altre = [x for x in NEWS[max(0, i - 2):i + 4] if x is not n][:3]
    body = f"""<section class="page-hero article-hero" aria-labelledby="page-h">
<div class="container">
{crumbs(("News", "news.html"), (f'<span{in_it()}>{esc(n["title"])}</span>' if in_it() else esc(n["title"]), None))}
{news_meta(n)}
<h1 id="page-h" class="article-title"{in_it()}>{esc(n["title"])}</h1>
</div>
</section>

<section class="section section--tight" aria-label="{tr("Testo", "Text", "Text")}">
<div class="container article{'' if fig else ' article--noimg'}">
{fig}
<div class="prose"{in_it()}>
{corpo}
</div>
</div>
</section>

<section class="section section--tight" aria-labelledby="altre-h">
<div class="container">
<nav class="article-pager" aria-label="{prec} / {succ}">{prev}{nxt}</nav>
<div class="section-row">
<h2 id="altre-h" class="h3">{tr("Altre notizie", "Weitere Meldungen", "More news")}</h2>
<a class="link" href="news.html">{tr("Tutte le news", "Alle News", "All news")}</a>
</div>
<div class="news-grid">
{chr(10).join(news_card(x) for x in altre)}
</div>
</div>
</section>"""
    return sezione_page(n["file"], f"{esc(n['title'])} | CAS Ticino", esc((n["excerpt"] or n["title"])[:155]), body,
                        og=og_name(n), section=NM_MENU())


def foto():
    su = "" if LINGUA["lang"] == "it" else "../"  # data-json non passa da pubblica()
    titolo = tr("Foto e resoconti", "Fotos und Tourenberichte", "Photos and trip reports")
    body = page_hero([nm_crumb(), (titolo, None)], titolo, tr(
        "Le foto e i resoconti delle ultime gite della sezione, pubblicati dai capigita sul portale Droptour.",
        "Fotos und Berichte der letzten Touren der Sektion, von den Tourenleitenden auf dem Portal Droptour veröffentlicht. Die Berichte sind auf Italienisch.",
        "Photos and reports from the section’s latest trips, published by the trip leaders on the Droptour portal. The reports are in Italian.")) + f"""

<section class="section" aria-label="{tr("Ultime gite", "Letzte Touren", "Latest trips")}">
<div class="container">
<div id="albums" aria-live="polite" data-json="{su}data/foto.json"><p class="albums-status">{tr("Caricamento delle foto…", "Fotos werden geladen…", "Loading photos…")}</p></div>
<div class="albums-more">
<button type="button" class="btn btn--secondary" id="load-more" hidden>{tr("Carica altre gite", "Weitere Touren laden", "Load more trips")}</button>
</div>
</div>
</section>

{subnav(NM_MENU(), L("foto.html"))}"""
    return sezione_page("foto.html", tr("Foto e resoconti delle gite", "Fotos und Tourenberichte", "Photos and trip reports") + " | CAS Ticino", tr(
        "Le foto delle ultime gite della Sezione Ticino del Club Alpino Svizzero, con i resoconti dei capigita.",
        "Die Fotos der letzten Touren der SAC-Sektion Ticino, mit den Berichten der Tourenleitenden (italienisch).",
        "Photos from the latest trips of the SAC Ticino Section, with the trip leaders’ reports (in Italian)."),
        body, og="attivita/gite-2x1", scripts=f'<script src="{asset("assets/foto.js")}" defer></script>\n')


def pubblicazioni(cartella, prefisso):
    """PDF docs/<cartella>/<prefisso>-<anno>[-<mese>].pdf, dal più recente; copertine da scripts/copertine.py."""
    out = []
    for nome in os.listdir(os.path.join(ROOT, "docs", cartella)):
        m = re.fullmatch(prefisso + r"-(\d{4})(?:-([a-z]+))?\.pdf", nome)
        if not m or (m.group(2) and m.group(2) not in MESI):
            continue
        base = nome[:-4]
        cover = os.path.join(ROOT, "assets", "img", "pubblicazioni", base + ".webp")
        if not os.path.exists(cover):
            raise SystemExit(f"manca la copertina di {nome}: lancia python scripts/copertine.py")
        w, h = webp_size(cover)
        mb = os.path.getsize(os.path.join(ROOT, "docs", cartella, nome)) / 1e6
        mese = m.group(2) or ""
        out.append({"anno": m.group(1), "mese": mese, "quando": f"{mese} {m.group(1)}".strip(),
                    "ordine": (m.group(1), MESI.index(mese) if mese else 0),
                    "pdf": f"docs/{cartella}/{nome}", "mb": f"{mb:.1f}",
                    "cover": f"assets/img/pubblicazioni/{base}.webp", "w": w, "h": h})
    return sorted(out, key=lambda x: x["ordine"], reverse=True)


def pub_card(x, titolo):
    return f"""<a class="pub" href="{x['pdf']}">
<figure><img src="{x['cover']}" alt="{tr("Copertina", "Titelseite", "Cover")}: {titolo}" width="{x['w']}" height="{x['h']}" loading="lazy" decoding="async"></figure>
<strong>{titolo}</strong>
<span class="small">PDF {x['mb']}MB</span>
</a>"""


def pub_feature(x, titolo, testo):
    return f"""<div class="pub-feature" data-reveal>
<figure><img src="{x['cover']}" alt="{tr("Copertina", "Titelseite", "Cover")}: {titolo}" width="{x['w']}" height="{x['h']}"></figure>
<div class="pub-feature-body">
<span class="label">{tr("Ultimo numero", "Neueste Ausgabe", "Latest issue")}</span>
<h2 class="h2">{titolo}</h2>
<p>{testo}</p>
<a class="btn btn--primary" href="{x['pdf']}">{tr("Leggi il PDF", "PDF lesen (italienisch)", "Read the PDF (in Italian)")} <span class="arrow" aria-hidden="true">→</span></a>
<span class="small">PDF {x['mb']}MB</span>
</div>
</div>"""


def annuari():
    items = pubblicazioni("annuari", "annuario")
    ultimo, altri = items[0], items[1:]
    nome = tr("Annuario", "Jahrbuch", "Yearbook")
    titolo = tr("Annuari", "Jahrbücher", "Yearbooks")
    body = page_hero([nm_crumb(), (titolo, None)], titolo, tr(
        "L’annuario racconta la vita della sezione: un volume per ogni anno, da sfogliare in PDF.",
        "Das Jahrbuch erzählt vom Leben der Sektion: ein Band pro Jahr, als PDF zum Durchblättern (italienisch).",
        "The yearbook tells the story of the section’s life: one volume a year, to browse as a PDF (in Italian).")) + f"""

<section class="section" aria-label="{tr("Numeri da sfogliare", "Ausgaben zum Durchblättern", "Issues to browse")}">
<div class="container">
{pub_feature(ultimo, f"{nome} {ultimo['anno']}", tr("L’ultimo annuario pubblicato dalla sezione.", "Das neueste Jahrbuch der Sektion.", "The section’s latest yearbook."))}
<div class="section-row"><h2 class="h3">{tr("Annate precedenti", "Frühere Jahrgänge", "Previous years")}</h2></div>
<div class="pubs" data-reveal>
{chr(10).join(pub_card(x, f"{nome} {x['anno']}") for x in altri)}
</div>
</div>
</section>

{subnav(NM_MENU(), L("annuari.html"))}"""
    return sezione_page("annuari.html", titolo + " | CAS Ticino", tr(
        "Gli annuari della Sezione Ticino del Club Alpino Svizzero da scaricare in PDF.",
        "Die Jahrbücher der SAC-Sektion Ticino als PDF zum Herunterladen (italienisch).",
        "The yearbooks of the SAC Ticino Section to download as PDFs (in Italian)."),
        body, og=ultimo["cover"][len("assets/img/"):-len(".webp")])


def informazione():
    items = pubblicazioni("informazione", "informazione")
    ultimo, altri = items[0], items[1:]

    def quando(x):
        mese = MESI_L[LINGUA["lang"]][MESI.index(x["mese"])] if x["mese"] else ""
        return f"Informazione, {mese} {x['anno']}".replace(",  ", ", ").strip()
    griglia = (f"""<div class="section-row"><h2 class="h3">{tr("Numeri precedenti", "Frühere Ausgaben", "Previous issues")}</h2></div>
<div class="pubs" data-reveal>
{chr(10).join(pub_card(x, quando(x)) for x in altri)}
</div>""" if altri else "")
    body = page_hero([nm_crumb(), ("Informazione", None)], "Informazione", tr(
        "Il bollettino ufficiale della sezione: notizie, attività e appuntamenti, da sfogliare in PDF.",
        "Das offizielle Mitteilungsblatt der Sektion: Neuigkeiten, Aktivitäten und Termine, als PDF zum Durchblättern (italienisch).",
        "The section’s official bulletin: news, activities and dates, to browse as a PDF (in Italian).")) + f"""

<section class="section" aria-label="{tr("Numeri da sfogliare", "Ausgaben zum Durchblättern", "Issues to browse")}">
<div class="container">
{pub_feature(ultimo, quando(ultimo), tr("Il numero più recente del bollettino ufficiale della Sezione Ticino.", "Die neueste Ausgabe des offiziellen Mitteilungsblatts der Sektion Ticino.", "The latest issue of the Ticino Section’s official bulletin."))}
{griglia}
</div>
</section>

{subnav(NM_MENU(), L("informazione.html"))}"""
    return sezione_page("informazione.html", "Informazione | CAS Ticino", tr(
        "Informazione, il bollettino ufficiale della Sezione Ticino del Club Alpino Svizzero, da scaricare in PDF.",
        "«Informazione», das offizielle Mitteilungsblatt der SAC-Sektion Ticino, als PDF zum Herunterladen (italienisch).",
        "«Informazione», the official bulletin of the SAC Ticino Section, to download as a PDF (in Italian)."),
        body, og=ultimo["cover"][len("assets/img/"):-len(".webp")])
