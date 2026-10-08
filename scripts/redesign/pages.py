"""Nuovo design: genera tutte le pagine del sito.

Uso: python scripts/redesign/pages.py [Pagina.html ...]  (senza argomenti rigenera tutto)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shared import head, nav, footer, social, pic, img, GITE, GITE_DROPTOUR, page_hero, subnav, asset, in_sottocartella, crumbs

# Programma gite su Droptour già filtrato per gruppo o per tipo di attività (i link dei singoli corsi cambiano ogni anno)
GITE_GIOVANI = GITE + "?gruppo=Giovani"   # gite.html con il filtro già scelto (gite.js)
GITE_SENIORI = GITE + "?gruppo=Seniori"
GITE_CORSI = GITE + "?tipo=COR"
from shared import LINGUA, PAGINE_LINGUA, SITO, de, en, tr, t, L
from shared import avviso, avviso_testo
from urllib.parse import urljoin, quote
from capanne import CONTENUTI, PRENOTA
from capanne_de import CONTENUTI_DE, HUT_DE, HUTS_DE
from capanne_en import CONTENUTI_EN, HUT_EN, HUTS_EN
import json, re, unicodedata
import news_util
from storia_oggetti import oggetto
import pwa
import mercatino_util
from news_util import webp_size
from html import unescape as html_unescape, escape as html_escape

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUTS = [
    # file, nome, quota, valle, stato, testo, posti, accesso, img 3x2 (w,h), grande
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Custodita giu–ott", "Su un terrazzo sopra la Val Piumogna, base per il Pizzo Campo Tencia: la cima più alta interamente ticinese.", "80 posti", "Dalpe 3h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Custodita estate e inverno", "Sull’omonimo passo, tra Leventina e Valle Maggia. Inaugurata nel 2003, primo rifugio moderno del CAS.", "100 posti", "Ossasco 3h30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Custodita mag–ott", "Il classico rifugio in pietra affacciato sulla Valle di Blenio: storia, accoglienza calorosa e cucina nostrana.", "24 posti", "Compietto 2h40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Custodita giu–ott", "Al margine della riserva della Greina: torbiere, alpeggi e l’arco naturale più grande del Ticino.", "70 posti", "Garzott 2h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "Tutto l’anno", "Il balcone sul Luganese, ricostruito nel 2016: vista dal Monte Rosa ai Denti della Vecchia, standard Bike Hotel.", "42 posti", "Corticiasca 1h30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Su riservazione", "Sopra Sonvico, ai piedi dei Denti della Vecchia. Ideale per famiglie e arrampicata.", "16 posti, autogestita", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

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


def banda_adesione(titolo, testo, bottone, href):
    """Home: banda «Diventa socio», bassa, con titolo e testo a sinistra e bottone a destra."""
    return f"""<section class="cta-band" id="adesione" aria-labelledby="adesione-h">
{pic("paesaggi/tramonto-larici", "", mobile="paesaggi/tramonto-larici-4x3", w=2000, h=1126)}
<div class="container">
<div class="cta-text">
<h2 id="adesione-h" class="h2">{titolo}</h2>
<p>{testo}</p>
</div>
<a class="btn btn--light" href="{href}">{bottone} <span class="arrow" aria-hidden="true">→</span></a>
</div>
</section>"""


def ATT_MENU():
    return tr("Attività", "Aktivitäten", "Activities")


def NM_MENU():
    return tr("News e media", "News und Medien", "News and media")


def SEZ_MENU():
    return tr("La Sezione", "Die Sektion", "The Section")


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


def home():
    lang = LINGUA["lang"]
    tx = TRADOTTE.get(lang, {})
    nome = L("index.html")
    prossime = prossime_gite()
    if lang == "it":
        huts = schede_capanne(HUTS)
    else:
        huts = schede_capanne({"de": HUTS_DE, "en": HUTS_EN}[lang], tx["accesso"], f"{lang}/")
    n_annunci = len(mercatino_util.attivi())
    mercatino_conta = {0: "", 1: tr(" Un annuncio online.", " Ein Inserat online.", " One listing online.")}.get(
        n_annunci, tr(f" {n_annunci} annunci online.", f" {n_annunci} Inserate online.", f" {n_annunci} listings online."))
    corso_alt = {"it": "Cordata su una cresta di neve", "de": "Seilschaft auf einem Schneegrat", "en": "Rope team on a snow ridge"}[lang]

    html = head(tx.get("home_title", "CAS Ticino | Club Alpino Svizzero, Sezione Ticino"),
                tx.get("home_desc", "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età. Da oltre un secolo, la casa dell’alpinismo ticinese."),
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n<link rel="preload" as="image" href="assets/img/paesaggi/sciatori-villaggio-2000.webp" imagesrcset="assets/img/paesaggi/sciatori-villaggio-1000.webp 1000w, assets/img/paesaggi/sciatori-villaggio-2000.webp 2000w" imagesizes="100vw" media="(min-width: 701px)">\n')
    html += "\n<body>\n" + nav(nome) + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">{tx.get("hero_h", 'In montagna<br>con <span class="accent">noi</span>.')}</h1>
<div class="hero-foot">
<div class="hero-testo">
<p class="lead">{tx.get("hero_lead", "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età.")}</p>
{social()}
</div>
<div class="actions">
<a class="btn btn--primary" href="adesione.html">{tx.get("diventa", "Diventa socio")} <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="news.html">{tr("Ultime notizie", "Neuigkeiten", "Latest news")}</a>
</div>
</div>
</div>
<figure class="band">
{pic("paesaggi/sciatori-villaggio", tx.get("hero_alt", "Scialpinisti in salita verso un villaggio innevato"), mobile="paesaggi/sciatori-villaggio-4x3", w=2000, h=901, lazy=False, cls="pos-low")}
{credito()}
</figure>
</section>

<section class="section" id="attivita" aria-labelledby="attivita-h">
<div class="container">
<div class="section-head">
<h2 id="attivita-h" class="h2">{tr("Fuori con la sezione", "Unterwegs mit der Sektion", "Out with the section")}</h2>
<p class="lead">{tr("Gite per tutti i livelli, un gruppo per ogni età e corsi per imparare a muoversi in montagna in sicurezza.",
                    "Touren für jedes Niveau, eine Gruppe für jedes Alter und Kurse, um sich sicher in den Bergen zu bewegen.",
                    "Trips for every level, a group for every age and courses to learn to move safely in the mountains.")}</p>
</div>
<div class="bento" id="gruppi">
<article class="tile tile--wide-top" data-reveal>
{img("attivita/gite-2x1", tr("Gruppo in vetta con vista sulle Alpi innevate", "Gruppe auf dem Gipfel mit Blick auf die verschneiten Alpen", "Group on a summit overlooking the snowy Alps"), 1400, 700)}
<div class="tile-body">
<h3 class="h2">{tr("Gite, escursioni e uscite della sezione", "Touren, Wanderungen und Ausflüge der Sektion", "The section’s trips, hikes and outings")}</h3>
<p>{tr("Escursionismo, alpinismo, sci alpinismo, racchette e arrampicata: il calendario completo con iscrizioni online.",
       "Wandern, Hochtouren, Skitouren, Schneeschuhtouren und Klettern: das ganze Programm mit Online-Anmeldung.",
       "Hiking, mountaineering, ski touring, snowshoeing and climbing: the full calendar with online registration.")}</p>
<div class="actions"><a class="btn btn--primary" href="{GITE}">{t("gite")}</a><a class="btn btn--ghost-light" href="foto.html">{tr("Foto e resoconti", "Fotos und Berichte", "Photos and reports")}</a></div>
</div>
</article>
<article class="tile tile--tall" data-reveal>
{img("attivita/giovani-3x4", tr("Giovane arrampicatore su una parete dei Denti della Vecchia", "Junger Kletterer an einer Wand der Denti della Vecchia", "Young climber on a face of the Denti della Vecchia"), 800, 1066)}
<div class="tile-body">
<span class="label">{tr("Gruppo giovani, dagli anni ’60", "Jugendgruppe, seit den 1960er-Jahren", "Youth group, since the 1960s")}</span>
<h3 class="h2">{tr("Giovani", "Jugend", "Youth")}</h3>
<p>{tr("Arrampicata, escursioni e settimane in montagna con monitori della sezione.", "Klettern, Wanderungen und Bergwochen mit Leitenden der Sektion.", "Climbing, hikes and mountain weeks with the section’s instructors.")}</p>
<div class="links"><a class="link" href="giovani.html">{tr("Gruppo giovani", "Jugendgruppe", "Youth group")}</a><a class="link" href="organizzazione.html#giovani">{tr("Organizzazione", "Organisation", "Organisation")}<span class="visually-hidden"> {tr("del gruppo giovani", "der Jugendgruppe", "of the youth group")}</span></a></div>
</div>
</article>
<article class="tile tile--bottom-1" data-reveal>
{img("attivita/senior-2x1", tr("Escursionisti su un sentiero di cresta", "Wandernde auf einem Gratweg", "Hikers on a ridge path"), 1000, 500)}
<div class="tile-body">
<span class="label">{tr("Gruppo senior, dal 1940", "Seniorengruppe, seit 1940", "Seniors group, since 1940")}</span>
<h3 class="h2">{tr("Senior", "Senioren", "Seniors")}</h3>
<p>{tr("Uscite settimanali con capigita esperti, al ritmo giusto e in buona compagnia, dalla Capriasca alle Alpi.",
       "Wöchentliche Touren mit erfahrenen Tourenleitenden, im richtigen Tempo und in guter Gesellschaft, von der Capriasca bis in die Alpen.",
       "Weekly outings with experienced trip leaders, at the right pace and in good company, from the Capriasca to the Alps.")}</p>
<div class="links"><a class="link" href="senior.html">{tr("Gruppo senior", "Seniorengruppe", "Seniors group")}</a><a class="link" href="organizzazione.html#senior">{tr("Organizzazione", "Organisation", "Organisation")}<span class="visually-hidden"> {tr("del gruppo senior", "der Seniorengruppe", "of the seniors group")}</span></a></div>
</div>
</article>
<article class="tile tile--bottom-2" id="corsi" data-reveal>
{img("corsi/alpinismo-4x5", corso_alt, 594, 742)}
<div class="tile-body">
<h3 class="h2">{tr("Corsi", "Kurse", "Courses")}</h3>
<p>{tr("Alpinismo, sci alpinismo, arrampicata, freeride e racchette: per imparare a muoversi in montagna in sicurezza.",
       "Hochtouren, Skitouren, Klettern, Freeride und Schneeschuhtouren: um zu lernen, sich sicher in den Bergen zu bewegen.",
       "Mountaineering, ski touring, climbing, freeride and snowshoeing: to learn to move safely in the mountains.")}</p>
<div class="links"><a class="link" href="corsi.html">{tr("Tutti i corsi", "Alle Kurse", "All courses")}</a><a class="link" href="partecipare.html">{tr("Partecipare alle gite", "An Touren teilnehmen", "Taking part in trips")}</a></div>
</div>
</article>
</div>
{f"""<div class="prossime" data-reveal>
<div class="section-row">
<h3 class="h3">{tr("Prossime gite", "Nächste Touren", "Upcoming trips")}</h3>
<a class="link" href="{GITE}">{tr("Tutto il programma", "Ganzes Programm", "Full programme")}</a>
</div>
<div class="scorri scorri--gite">
<div class="scorri-traccia">
{prossime}
</div>
</div>
</div>""" if prossime else ""}
</div>
</section>

<section class="section--surface" id="capanne" aria-labelledby="capanne-h">
<div class="container">
<div class="section-head">
<h2 id="capanne-h" class="h2">{tx.get("capanne_h", "Sei capanne, un solo Ticino")}</h2>
<p class="lead">{tx.get("capanne_lead", "Sempre aperte, custodite quando i guardiani sono presenti. Prima di partire, contatta il guardiano per verificare presenza e condizioni della montagna.")}</p>
</div>
<div class="huts">
{huts}
</div>
<div class="callout callout--accent">
<p>{tr("<strong>Cerchiamo «api operaie».</strong> I volontari aiutano i guardiani ad aprire, chiudere e mantenere le capanne, e passano qualche bella serata in quota.",
       "<strong>Wir suchen «fleissige Bienen».</strong> Freiwillige helfen den Hüttenwarten beim Öffnen, Schliessen und Unterhalten der Hütten und verbringen schöne Abende in der Höhe.",
       "<strong>We are looking for «busy bees».</strong> Volunteers help the hut keepers open, close and maintain the huts, and spend some fine evenings up high.")}</p>
<a class="btn btn--light" href="volontariato.html">{tr("Voglio aiutare", "Ich helfe mit", "I want to help")} <span class="arrow" aria-hidden="true">→</span></a>
</div>
</div>
</section>

<section class="section" id="servizi" aria-labelledby="servizi-h">
<div class="container">
<div class="section-head">
<h2 id="servizi-h" class="h2">{SERVIZI_MENU()}</h2>
<p class="lead">{tr("Materiale a noleggio, un mercatino tra soci e tutto quello che serve consultare prima di partire.",
                    "Material zur Miete, ein Marktplatz unter Mitgliedern und alles, was man vor dem Aufbruch nachschlagen sollte.",
                    "Equipment for hire, a gear market between members and everything worth checking before you set off.")}</p>
</div>
<div class="pillars pillars--servizi" data-reveal>
<article class="pillar pillar--dark pillar--wide">
<h3>{tr("Noleggio materiale", "Materialvermietung", "Equipment hire")}</h3>
<p>{tr("Ramponi, piccozze, imbragature, set ARVA con sonda e pala e molto altro, a pochi franchi al giorno: per le gite della sezione e per le uscite private.",
       "Steigeisen, Pickel, Klettergurte, LVS-Sets mit Sonde und Schaufel und vieles mehr, für wenige Franken pro Tag: für die Touren der Sektion und für private Unternehmungen.",
       "Crampons, ice axes, harnesses, transceiver sets with probe and shovel and much more, for a few francs a day: for section trips and private outings.")}</p>
<a class="link" href="noleggio.html">{tr("Richiedi il materiale", "Material anfragen", "Request equipment")}</a>
</article>
<article class="pillar pillar--accent">
<h3>{tr("Mercatino", "Marktplatz", "Gear market")}</h3>
<p>{tr("Attrezzatura di montagna tra privati: vendo, cerco, regalo.", "Bergausrüstung unter Privaten: verkaufen, suchen, verschenken.", "Mountain gear between private people: for sale, wanted, free.")}{mercatino_conta}</p>
<a class="link" href="mercatino.html">{tr("Vedi gli annunci", "Zu den Inseraten", "See the listings")}</a>
</article>
<article class="pillar">
<h3>{tr("Documenti", "Dokumente", "Documents")}</h3>
<p>{tr("Regolamento gite, scale di difficoltà, promemoria tecnici, moduli e cartine da scaricare.",
       "Tourenreglement, Schwierigkeitsskalen, technische Merkblätter, Formulare und Karten zum Herunterladen (italienisch).",
       "Trip regulations, difficulty scales, technical fact sheets, forms and maps to download (in Italian).")}</p>
<a class="link" href="documenti.html">{tr("Tutti i documenti", "Alle Dokumente", "All documents")}</a>
</article>
<article class="pillar pillar--wide">
<h3>{tr("Link utili", "Nützliche Links", "Useful links")}</h3>
<p>{tr("Meteo, bollettini valanghe, condizioni, cartine e le altre società alpinistiche del territorio: i siti da consultare prima di partire.",
       "Wetter, Lawinenbulletins, Verhältnisse, Karten und die anderen Bergsportvereine der Region: die Websites für vor dem Aufbruch.",
       "Weather, avalanche bulletins, conditions, maps and the other mountaineering clubs in the region: the sites to check before you set off.")}</p>
<a class="link" href="link.html">{tr("Vai ai link", "Zu den Links", "Go to the links")}</a>
</article>
</div>
</div>
</section>

<section class="section--surface" id="news" aria-labelledby="news-h">
<div class="container">
<div class="section-row">
<h2 id="news-h" class="h2">News</h2>
<a class="link" href="news.html">{tr("Tutte le news", "Alle News", "All news")}</a>
</div>
<div class="scorri scorri--news" data-reveal>
<div class="scorri-traccia">
{chr(10).join(news_card(n) for n in NEWS[:8])}
</div>
</div>
</div>
</section>

{banda_adesione(tx.get("cta_h", "Sali con noi."), tx.get("cta_p", "Tariffe ridotte nelle capanne CAS di tutta la Svizzera, corsi, gite e una comunità che ama la montagna quanto te."), tx.get("diventa", "Diventa socio"), "adesione.html")}

</main>
""" + footer()
    return pubblica(nome, html)


# ------------------------------------------------------------------ pagine interne

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
    return f'<figcaption class="credito">{tr("Foto", "Foto", "Photo")} © {autore}</figcaption>'


def band_img(name, alt, w, h):
    return f'<figure class="band">\n{img(name, alt, w, h, lazy=False)}\n</figure>'


# ------------------------------------------------------------------ capanne

HUT_PAGES = {
    "campotencia.html": dict(
        portale="2147000055",
        name="Campo Tencia", where="Val Piumogna, Leventina", alt_m="2140", beds="80", custody="da metà giugno a metà ottobre",
        mail="campotencia@casticino.ch", booking=PRENOTA.format(36), facebook="https://www.facebook.com/61559861696010",
        description="Capanna Campo Tencia, 2140 m, in Val Piumogna (Leventina): 80 posti letto, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
        band=("capanne/campotencia", "La Capanna Campo Tencia al tramonto, sopra la Val Piumogna", 658),
        intro="Adagiata su un terrazzo che domina l’alta Val Piumogna, è la base ideale per escursioni, traversate verso altre capanne e salite come quella al Pizzo Campo Tencia, che con i suoi 3072 m è la cima più alta interamente in territorio ticinese.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da metà giugno a metà ottobre; d’inverno non è custodita, ma la riservazione è obbligatoria; per gruppi numerosi si può aprire d’accordo con i guardiani"),
              ("Posti letto", "80"),
              ("Pasti", "Cucina calda, pasti serviti tutto il giorno dal guardiano"),
              ("Locale invernale", "Sempre aperto, con bibite e legna")],
        reach=[("Accesso estivo", "Da Dalpe 3h; dal Lago Tremorgio (funivia da Rodi) 3h30; da Fusio per il Passo Campolungo 6h"),
               ("Accesso invernale", "Da Dalpe 3h, con gli sci per la Val Piumogna"),
               ("Cartina", 'CNS 1272 Campo Tencia, coordinate <span class="num">699.430 / 144.480</span>')],
        contact=[("Guardiani", "Valeria Grandi e Paco Porcu"),
                 ("Telefono capanna", '<a class="num" href="tel:+41918671544">+41 91 867 15 44</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41767212572">+41 76 721 25 72</a>'),
                 ("E-mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "cristallina.html": dict(
        portale="2147000069",
        name="Cristallina", where="Passo Cristallina, Valle Bedretto", alt_m="2575", beds="100", custody="da giugno a metà ottobre; d’inverno nei fine settimana e nei festivi",
        mail="cristallina@casticino.ch", booking=PRENOTA.format(20), facebook="https://www.facebook.com/capannacristallinacas/",
        description="Capanna Cristallina, 2575 m, sul passo tra Leventina e Valle Maggia: 100 posti letto, custodita da giugno a metà ottobre e d’inverno nei fine settimana e festivi. Contatti e prenotazioni.",
        band=("capanne/cristallina", "La Capanna Cristallina sul passo, tra Leventina e Valle Maggia", 558),
        intro="Progettata dagli architetti Baserga e Mozzetti e inaugurata nel 2003, è il primo rifugio moderno costruito dal Club Alpino Svizzero. Sorge sul passo, in un punto strategico tra Leventina e Valle Maggia: tappa panoramica sulle traversate verso Robiei, il Naret, il Campo Tencia e il San Giacomo. Il giro dei laghi del Cristallina, di uno o due giorni, è adatto anche alle famiglie; in un’ora si raggiungono il Cristallina e la Cima di Lago. D’inverno, raggiungibile soprattutto da nord, apre pendii splendidi verso la Valle Bedretto, Robiei e la Val Formazza.",
        stay=[("Apertura", "Sempre aperta e accessibile"),
              ("Custodia", "Da giugno a metà ottobre; d’inverno, da dicembre a fine aprile, con buone condizioni, nei fine settimana, nei giorni festivi e per i gruppi"),
              ("Posti letto", "100"),
              ("Pasti", "Preparati dal guardiano tutto il giorno"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Da Ossasco 3h30; da Robiei 3h; dal Lago del Narèt 2h30; dal Passo San Giacomo 4h"),
               ("Accesso invernale", "Da Ossasco 3h; da All’Acqua 4h"),
               ("Cartina", 'CNS 1251 Bedretto, coordinate <span class="num">683.550 / 147.300</span>')],
        contact=[("Guardiano", "Emanuele Vellati"),
                 ("Telefono", '<a class="num" href="tel:+41918692330">+41 91 869 23 30</a>'),
                 ("E-mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "adula.html": dict(
        portale="2147000002",
        name="Adula", where="Alta Val Carassino, Val Soi, Blenio", alt_m="2012", beds="24", custody="da fine maggio a metà ottobre",
        mail="adula@casticino.ch", booking=PRENOTA.format(42), facebook="https://www.facebook.com/CapannaAdulaCAS",
        description="Capanna Adula, 2012 m, tra Val Carassino e Val Soi (Blenio): 24 posti letto, aperta tutto l’anno, custodita da fine maggio a metà ottobre. Contatti e prenotazioni.",
        img=("capanne/adula-3x2", "La Capanna Adula, rifugio in pietra affacciato sulla Valle di Blenio", 1000, 667),
        intro="La «Bassa», come la si chiama da sempre, ha il fascino del rifugio d’altri tempi: costruzione in pietra, un soggiorno che trasuda storia, dormitori che hanno visto passare migliaia di alpinisti, accoglienza calorosa e cucina nostrana. Da questo balcone sulla Valle di Blenio si parte per la cima dell’Adula o, su comodi sentieri, verso altre capanne; i selvaggi itinerari della Val Carassino offrono un escursionismo avventuroso. Per i meno ambiziosi: una passeggiata in valle, un buon pranzo e un pisolino al sole.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da fine maggio a metà ottobre"),
              ("Posti letto", "24"),
              ("Pasti", "Pasti preparati dal guardiano; cucina autonoma solo d’inverno o d’accordo con il guardiano"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Da Compietto per la Val Carassino 2h40 (in mountain bike circa 1h); da Dangio per la Val Soi 3h; da Cusiè (Val Malvaglia) per il Passo del Laghetto 5h"),
               ("Accesso invernale", "Da Dangio 3h30; da Ghirone 5h"),
               ("Cartina", 'CNS 1253 Olivone, coordinate <span class="num">719.510 / 150.950</span>')],
        contact=[("Guardiano", "Raffaele «Lele» Demaldi"),
                 ("Telefono capanna", '<a class="num" href="tel:+41918721532">+41 91 872 15 32</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41795352112">+41 79 535 21 12</a>'),
                 ("E-mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "motterascio.html": dict(
        portale="2147000183",
        name="Motterascio", where="Alpe Motterascio, Greina, Blenio", alt_m="2172", beds="70", custody="da metà giugno a metà ottobre",
        mail="motterascio@casticino.ch", booking=PRENOTA.format(221), facebook="https://www.facebook.com/michelamotterascio",
        description="Capanna Motterascio, 2172 m, al margine della Greina (Blenio): 70 posti letto, aperta tutto l’anno, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
        band=("capanne/motterascio", "La Capanna Motterascio sull’altopiano della Greina", 649),
        intro="Inaugurata nel 1967 e ampliata nel 1980, nel 1990 e nel 2006, sorge al margine di una riserva naturale straordinaria: la Greina, con le sue paludi, torbiere, alpeggi e una flora incontaminata. Punto di partenza per itinerari interessanti, tra cui spicca l’arco della Greina, il più grande arco naturale del Canton Ticino.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da metà giugno a metà ottobre (nel 2026 dal 13 giugno al 10 ottobre); d’inverno il locale invernale da 10 posti, su riservazione"),
              ("Posti letto", "70"),
              ("Pasti", "Pasti caldi preparati dai guardiani tutto il giorno"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Dall’Alpe Garzott (Lago di Luzzone) 2h; dalla diga del Luzzone 3h30; da Pian Geirètt 3h30; da Ghirone per la Val Camadra 6h"),
               ("Accesso invernale", "Da Ghirone per la Val Camadra e il Passo della Greina, 5-6h, solo con neve assestata"),
               ("Cartina", 'CNS 1233 Greina, coordinate <span class="num">720.075 / 161.425</span>')],
        contact=[("Guardiano", "Fabio Merzaghi"),
                 ("Prenotazioni", '<a class="num" href="tel:+41918721622">+41 91 872 16 22</a> (da metà giugno a metà ottobre)'),
                 ("Cellulare", '<a class="num" href="tel:+41797276905">+41 79 727 69 05</a>'),
                 ("E-mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "montebar.html": dict(
        portale="2147000180",
        name="Monte Bar", where="Alta Capriasca, Luganese", alt_m="1602", beds="42", custody="tutto l’anno",
        mail="montebar@casticino.ch", booking=PRENOTA.format(168), facebook="https://www.facebook.com/CapannaMonteBarCAS/",
        description="Capanna Monte Bar, 1602 m, in Alta Capriasca: 42 posti letto in camere da 2, 4 e 6, custodita tutto l’anno, standard Bike Hotel. Contatti e prenotazioni.",
        band=("capanne/montebar", "La Capanna Monte Bar con vista sul Luganese", 442),
        intro="Su un poggio di eccezionale bellezza, con una vista a 180 gradi dai Denti della Vecchia al Tamaro e, a ovest, sui 4000 vallesani dal Mischabel al Monte Rosa. Ricostruita nell’autunno 2016: camere da 2, 4 e 6 posti, servizi ai piani, refettorio per circa 80 persone, saletta riunioni per 20, ampia terrazza e un locale chiuso con caricatori per e-bike e piccola officina, secondo lo standard Bike Hotel.",
        stay=[("Apertura", "Tutto l’anno; apre anche per eventi, cene e pranzi su richiesta"),
              ("Custodia", "Da maggio a inizio novembre tutti i giorni; d’inverno dal venerdì a pranzo alla domenica a pranzo, nei festivi e nelle vacanze scolastiche"),
              ("Posti letto", "42, in camere da 2-4-6"),
              ("Pasti", "Cucina tipica con prodotti del territorio; menu speciali su riservazione"),
              ("In assenza dei custodi", "La capanna è chiusa; resta accessibile solo un piccolo atrio per le emergenze")],
        reach=[("Accesso estivo", "Da Corticiasca 1h30; da Bidogno 2h; da Isone per Val Serdena e Piandanazzo 3h; da Gola di Lago 2h30"),
               ("Mountain bike", "Strada forestale Bidogno-Rompiago con discesa verso Scareglia o Signora; Piandanazzo-Al Matro-Serdena-Isone; Piandanazzo-Alpe Pietra Rossa-San Lucio-Bogno"),
               ("Accesso invernale", "Da Corticiasca e da Gola di Lago"),
               ("Cartina", 'CNS 1333 Tesserete, coordinate <span class="num">721.800 / 106.610</span>')],
        contact=[("Guardiani", "James Mauri e Serge Santese"),
                 ("Telefono", '<a class="num" href="tel:+41919663322">+41 91 966 33 22</a>'),
                 ("E-mail", '<a href="mailto:montebar@casticino.ch">montebar@casticino.ch</a>')]),
    "baitadelluca.html": dict(
        name="Baita del Luca", where="Cioascio, Sonvico", alt_m="1070", beds="16", custody="su riservazione",
        mail="baitaluca@casticino.ch",
        description="Baita del Luca, 1070 m, sopra Sonvico ai piedi dei Denti della Vecchia: 16 posti letto, autogestita, solo su riservazione.",
        img=("capanne/baitadelluca-3x2", "La Baita del Luca su un pendio erboso sopra Sonvico", 1000, 667),
        intro="Su un ampio pendio erboso sopra Sonvico, ai piedi dei Denti della Vecchia: base ideale per escursioni, anche in famiglia, e arrampicate in un paesaggio unico.",
        stay=[("Apertura", "Tutto l’anno, solo previa riservazione"),
              ("Posti letto", "16"),
              ("Pasti", "Possibilità di cucinare"),
              ("Bibite", "Disponibili in quantità limitata"),
              ("Prenotazioni", "Il codice d’accesso viene dato dopo il versamento anticipato")],
        reach=[("Accesso estivo", "Da Rosone 45 min; da Lovarescia (sopra Sonvico) 60 min; da Car e da Luss (Villa Luganese) 60 min"),
               ("Cartina", 'CNS 1333 Tesserete, coordinate <span class="num">722.980 / 102.600</span>')],
        contact=[("Responsabile", "Priska Deluigi, 6960 Odogno"),
                 ("Cellulare", '<a class="num" href="tel:+41792033084">+41 79 203 30 84</a>'),
                 ("E-mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Prenotazioni", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}


# Scheda della capanna sul portale escursionistico del CAS (portale= in HUT_PAGES, numero della capanna sul portale).
# Il CAS sostituirà il portale con «Ridian» (annunciato per la primavera 2028): allora vanno controllati questi link.
PORTALE_CAS = {"it": "https://www.sac-cas.ch/it/capanne-e-escursioni/portale-escursionistico-del-cas/{}/",
               "de": "https://www.sac-cas.ch/de/huetten-und-touren/sac-tourenportal/{}/",
               "en": "https://www.sac-cas.ch/en/huts-and-tours/sac-route-portal/{}/"}
IBAN = "CH09 0076 4128 9526 1200 6"   # conto della sezione (Banca Stato, Lugano), anche in Sede e contatti

# testi fissi delle pagine capanna
TC = {
    "it": dict(prenota="Prenota", cucina="La cucina", team="Chi vi accoglie", vita="La cucina e i guardiani",
               tariffe="Tariffe e prenotazioni", accessi="Come arrivare", attivita="Attività", sostenitori="Sostenitori",
               storia="Storia", storia_link="La storia della capanna", foto="Foto", tutte_foto="Tutte le foto",
               in_breve="In breve", testo="Testo", itinerari="Itinerari", capanne="Le capanne", sezione_menu="Capanne",
               foto_lead="La capanna, la cucina e i dintorni", tocca="Tocca una foto per vederla grande.",
               foto_desc="Foto della Capanna {n} e dei dintorni.", avviso="Avviso", importante="Importante", altitudine="Altitudine",
               posti="Posti letto", custodia="Custodia", apertura="Apertura", la_capanna="La capanna",
               soggiorno="Soggiorno", arrivare="Arrivare", contatti_h="Senti il guardiano prima di partire",
               contatti_p="Verifica sempre la presenza del guardiano e le condizioni della montagna.",
               altre="Le altre capanne", capanna="Capanna", n_foto="foto", accesso_da="Accesso da", pdf="",
               fb_h="Dalla capanna", fb_notizie="Ultime notizie", fb_p="Le ultime notizie della capanna, pubblicate dai guardiani su Facebook.",
               fb_carica="Mostra i post", fb_privacy="I post vengono caricati da Facebook solo dopo il clic: da quel momento Facebook riceve dati sulla tua visita.",
               fb_apri="Apri la pagina Facebook",
               portale="La capanna e i suoi itinerari sul portale del CAS", sostieni_h="Sostieni la capanna",
               sostieni_p="Manutenzione, rinnovi e lavori costano: le capanne vivono anche grazie ai soci e agli amici della montagna. Puoi sostenerle con una donazione sul conto della sezione, indicando il nome della capanna.",
               conto="Conto", causale="Causale", salta="In questa pagina", s_vita="Cucina e guardiani", s_tariffe="Tariffe",
               s_contatti="Contatti", s_sostieni="Sostieni la capanna"),
    "de": dict(prenota="Reservieren", cucina="Die Küche", team="Ihre Gastgeber", vita="Küche und Hüttenteam",
               tariffe="Preise und Reservation", accessi="Anreise", attivita="Aktivitäten", sostenitori="Unterstützer",
               storia="Geschichte", storia_link="Die Geschichte der Hütte", foto="Fotos", tutte_foto="Alle Fotos",
               in_breve="Auf einen Blick", testo="Text", itinerari="Routen", capanne="Die Hütten", sezione_menu="Hütten",
               foto_lead="Die Hütte, die Küche und die Umgebung", tocca="Tippen Sie auf ein Foto, um es gross zu sehen.",
               foto_desc="Fotos der Capanna {n} und ihrer Umgebung.", avviso="Hinweis", importante="Wichtig", altitudine="Höhe",
               posti="Schlafplätze", custodia="Bewartet", apertura="Öffnung", la_capanna="Die Hütte",
               soggiorno="Aufenthalt", arrivare="Zugang", contatti_h="Vor dem Aufbruch beim Hüttenwart melden",
               contatti_p="Erkundigen Sie sich immer, ob der Hüttenwart da ist, und informieren Sie sich über die Verhältnisse am Berg.",
               altre="Die anderen Hütten", capanna="Capanna", n_foto="Foto", accesso_da="Zugang ab", pdf=" (italienisch)",
               fb_h="Aus der Hütte", fb_notizie="Aktuelles", fb_p="Die neusten Nachrichten der Hütte, vom Hüttenteam auf Facebook veröffentlicht (meist italienisch).",
               fb_carica="Beiträge anzeigen", fb_privacy="Die Beiträge werden erst nach dem Klick von Facebook geladen: ab dann erhält Facebook Daten über Ihren Besuch.",
               fb_apri="Facebook-Seite öffnen",
               portale="Die Hütte und ihre Routen im SAC-Tourenportal", sostieni_h="Die Hütte unterstützen",
               sostieni_p="Unterhalt, Erneuerungen und Arbeiten kosten: Die Hütten leben auch dank den Mitgliedern und den Freunden der Berge. Sie können sie mit einer Spende auf das Konto der Sektion unterstützen, mit dem Namen der Hütte als Vermerk.",
               conto="Konto", causale="Vermerk", salta="Auf dieser Seite", s_vita="Küche und Team", s_tariffe="Preise",
               s_contatti="Kontakt", s_sostieni="Hütte unterstützen"),
    "en": dict(prenota="Book", cucina="The kitchen", team="Your hosts", vita="Kitchen and hut team",
               tariffe="Rates and booking", accessi="Getting there", attivita="Activities", sostenitori="Supporters",
               storia="History", storia_link="The history of the hut", foto="Photos", tutte_foto="All photos",
               in_breve="At a glance", testo="Text", itinerari="Routes", capanne="The huts", sezione_menu="Huts",
               foto_lead="The hut, the kitchen and the surroundings", tocca="Tap a photo to see it full size.",
               foto_desc="Photos of Capanna {n} and its surroundings.", avviso="Notice", importante="Important", altitudine="Altitude",
               posti="Beds", custodia="Staffed", apertura="Opening", la_capanna="The hut",
               soggiorno="Your stay", arrivare="Getting there", contatti_h="Check with the hut keeper before you set out",
               contatti_p="Always check that the hut keeper is there and find out about conditions in the mountains.",
               altre="The other huts", capanna="Capanna", n_foto="photo", accesso_da="Access from", pdf=" (in Italian)",
               fb_h="From the hut", fb_notizie="Latest news", fb_p="The hut’s latest news, posted by the hut team on Facebook (mostly in Italian).",
               fb_carica="Show posts", fb_privacy="Posts are only loaded from Facebook after you click: from then on Facebook receives data about your visit.",
               fb_apri="Open the Facebook page",
               portale="The hut and its routes on the SAC route portal", sostieni_h="Support the hut",
               sostieni_p="Upkeep, renovations and building work cost money: the huts also rely on members and friends of the mountains. You can support them with a donation to the section’s account, giving the name of the hut as reference.",
               conto="Account", causale="Reference", salta="On this page", s_vita="Kitchen and team", s_tariffe="Rates",
               s_contatti="Contact", s_sostieni="Support the hut"),
}


def tc(chiave):
    return TC[LINGUA["lang"]][chiave]


def capanna(file):
    """Dati di HUT_PAGES nella lingua corrente (in tedesco e in inglese i testi vengono da capanne_de/capanne_en)."""
    d = dict(HUT_PAGES[file])
    d.update({"it": {}, "de": HUT_DE, "en": HUT_EN}[LINGUA["lang"]].get(file, {}))
    return d


def contenuti(file):
    return {"it": CONTENUTI, "de": CONTENUTI_DE, "en": CONTENUTI_EN}[LINGUA["lang"]].get(file)


def pubblica(nome, html):
    """Pagina in una sottocartella (de/, en/, capanne/…): i percorsi relativi salgono dei livelli giusti."""
    return in_sottocartella(html, su="../" * nome.count("/")) if "/" in nome else html


def prenota(d, cls="btn btn--primary"):
    """Pulsante di prenotazione: hut-reservation.org se la capanna c'è, altrimenti e-mail."""
    href = d.get("booking") or f"mailto:{d['mail']}"
    ext = ' rel="noopener"' if href.startswith("http") else ""
    return f'<a class="{cls}" href="{href}"{ext}>{tc("prenota")} <span class="arrow" aria-hidden="true">→</span></a>'


def cimg(c, name, alt, lazy=True):
    """Immagine di una capanna (assets/img/capanne/<cartella>/<name>.webp), con le dimensioni lette dal file."""
    src = f"assets/img/capanne/{c['cartella']}/{name}.webp"
    w, h = webp_size(os.path.join(ROOT, src))
    load = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="{src}" alt="{alt}" width="{w}" height="{h}"{load}>'


def logo_sostenitore(c, nome, f, url=None):
    """Logo di un sostenitore: in assets/img/capanne/<cartella>/sostenitori/<f>.webp oppure, se f contiene «/»,
    in assets/img/capanne/<f>.webp (loghi comuni a più capanne, in capanne/sostenitori/); con url porta al suo sito."""
    src = f"assets/img/capanne/{f if '/' in f else c['cartella'] + '/sostenitori/' + f}.webp"
    w, h = webp_size(os.path.join(ROOT, src))
    im = f'<img src="{src}" alt="{nome}" width="{w}" height="{h}" loading="lazy" decoding="async">'
    return f'<a href="{url}" rel="noopener">{im}</a>' if url else im


def galleria(c, gruppi, alt, quante=None):
    """Foto di uno o più gruppi (assets/img/capanne/<cartella>/foto/<gruppo>-NN-600/1200.webp): la miniatura apre la foto grande."""
    cartella = os.path.join(ROOT, "assets", "img", "capanne", c["cartella"], "foto")
    file = os.listdir(cartella)
    nomi = [n for g in ([gruppi] if isinstance(gruppi, str) else gruppi)
            for n in sorted(f[:-len("-600.webp")] for f in file if f.startswith(g + "-") and f.endswith("-600.webp"))]
    voci = []
    for i, n in enumerate(nomi[:quante], 1):
        base = f"assets/img/capanne/{c['cartella']}/foto/{n}"
        w, h = webp_size(os.path.join(ROOT, base + "-600.webp"))
        voci.append(f'<a href="{base}-1200.webp"><img src="{base}-600.webp" alt="{alt}, {tc('n_foto')} {i}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>')
    return '<div class="gallery">\n' + "\n".join(voci) + "\n</div>"


def pdf_lingua(frammento):
    """Nelle versioni tradotte i PDF (tutti in italiano) dentro i testi lo dicono, come quelli in link_capanna()."""
    if LINGUA["lang"] == "it":
        return frammento
    return re.sub(r'(<a class="file-link" href="[^"]+">)(.*?)</a>', lambda m: m.group(1) + m.group(2) + tc("pdf") + "</a>", frammento)


def link_capanna(links):
    """Link di una pagina capanna: i PDF con l'etichetta PDF, gli altri come link semplici."""
    out = []
    for label, href in links:
        if href.endswith(".pdf"):
            out.append(f'<p><a class="file-link" href="{href}">{label}{tc("pdf")}</a></p>')
        else:
            ext = ' rel="noopener"' if href.startswith("http") else ""
            out.append(f'<p><a href="{L(href) if not ext else href}"{ext}>{label}</a></p>')
    return "\n".join(out)


def hut_subnav(file, current):
    """Le pagine di una capanna: panoramica, attività, storia, foto."""
    c, d = contenuti(file), capanna(file)
    base = f"capanne/{c['cartella']}/"
    voci = [(d["name"], file)] + [(p["titolo"], base + p["file"] + ".html") for p in c["pagine"]]
    if c.get("storia"):
        voci.append((tc("storia"), base + c["storia"]["file"] + ".html"))
    if c.get("foto"):
        voci.append((tc("foto"), base + "foto.html"))
    cur = ' aria-current="page"'
    links = "\n".join(f'<a href="{L(h)}"{cur if L(h) == current else ""}>{l}</a>' for l, h in voci)
    return f"""<section class="section" aria-label="{tc('capanna')} {d['name']}">
<div class="container subnav">
<h2 class="label">{tc('capanna')} {d['name']}</h2>
<div class="subnav-links">
{links}
</div>
</div>
</section>"""


def hut_extra(file):
    """Sezioni in più della pagina capanna, da CONTENUTI: cucina e guardiani, tariffe, accessi, attività, storia, foto."""
    c, d = contenuti(file), capanna(file)
    out = []
    if c.get("cucina") or c.get("team"):
        t = c.get("team")
        cucina = f"""<div class="hut-cuisine stack">
<h2 class="h2">{c.get("cucina_titolo", tc("cucina"))}</h2>
<div class="prose">
{c["cucina"]}
</div>
</div>""" if c.get("cucina") else ""
        team = ""
        if t:
            foto = f'<figure>{cimg(c, t["img"][0], t["img"][1])}</figure>' if t.get("img") else ""
            persone = "\n".join(f'<div class="member"><div class="member-photo">{cimg(c, im, nome)}</div>'
                                f'<div class="member-body"><strong>{nome}</strong><span>{ruolo}</span></div></div>'
                                for nome, ruolo, im in t.get("persone", []))
            persone = f'<div class="members">\n{persone}\n</div>' if persone else ""
            team = f"""<div class="hut-team">
<h2 class="h2">{t.get("titolo", tc("team"))}</h2>
<div class="hut-team-body">
{foto}
<div>
<div class="prose">
{t["testo"]}
</div>
{persone}
</div>
</div>
</div>"""
        out.append(f"""<section class="section" id="vita" aria-label="{tc('vita')}">
<div class="container hut-life">
{cucina}
{team}
</div>
</section>""")
    if c.get("tariffe"):
        cards = "\n".join(f"""<div class="rate">
<h3 class="h3">{titolo}</h3>
<p class="small">{nota}</p>
{facts(righe)}
</div>""" for titolo, nota, righe in c["tariffe"])
        out.append(f"""<section class="section--surface" id="tariffe" aria-labelledby="tariffe-h">
<div class="container">
<div class="section-row">
<h2 id="tariffe-h" class="h2">{tc('tariffe')}</h2>
{prenota(d)}
</div>
<div class="rates">
{cards}
</div>
<div class="prose rates-note">
{pdf_lingua(c.get("prenotare", ""))}
</div>
</div>
</section>""")
    if c.get("accessi"):
        out.append(f"""<section class="section" id="accessi" aria-labelledby="accessi-h">
<div class="container stack">
<h2 id="accessi-h" class="h2">{tc('accessi')}</h2>
<div class="prose">
{pdf_lingua(c["accessi"])}
</div>
</div>
</section>""")
    if c.get("pagine"):
        cards = "\n".join(f"""<a class="news-card" href="{L(f"capanne/{c['cartella']}/{p['file']}.html")}">
<figure>{cimg(c, p["img"][0], p["img"][1])}</figure>
<div class="news-card-body">
<h3>{p["titolo"]}</h3>
<p>{p["lead"]}</p>
</div>
</a>""" for p in c["pagine"])
        out.append(f"""<section class="section" id="attivita" aria-labelledby="attivita-h">
<div class="container">
<div class="stack hut-activities">
<h2 id="attivita-h" class="h2">{tc('attivita')}</h2>
<div class="prose">
{c.get("attivita", "")}
</div>
</div>
<div class="news-grid">
{cards}
</div>
</div>
</section>""")
    if c.get("storia"):
        st = c["storia"]
        out.append(f"""<section class="section" id="storia" aria-labelledby="storia-h">
<div class="container hut-story">
<figure>{cimg(c, st["img"][0], st["img"][1])}</figure>
<div class="hut-story-text">
<h2 id="storia-h" class="h2">{tc('storia')}</h2>
<p>{st["lead"]}</p>
<a class="link" href="{L(f"capanne/{c['cartella']}/{st['file']}.html")}">{tc('storia_link')}</a>
</div>
</div>
</section>""")
    if c.get("foto"):
        out.append(f"""<section class="section" id="foto" aria-labelledby="foto-h">
<div class="container">
<div class="section-row">
<h2 id="foto-h" class="h2">{tc('foto')}</h2>
<a class="link" href="{L(f"capanne/{c['cartella']}/foto.html")}">{tc('tutte_foto')}</a>
</div>
{galleria(c, [g for _, g in c["foto"]], f"{tc('capanna')} {d['name']}", quante=10)}
</div>
</section>""")
    return "\n\n".join(out)


def hut_page(file, p):
    """Sottopagina di una capanna (attività, storia): testo, scheda tecnica, itinerari e foto. p: voce di CONTENUTI."""
    c, d = contenuti(file), capanna(file)
    nome = L(f"capanne/{c['cartella']}/{p['file']}.html")
    scheda = ""
    if p.get("dati") or p.get("link"):
        scheda = f"""<aside class="hut-sheet" aria-label="{tc('in_breve')}">
<h2 class="label">{tc('in_breve')}</h2>
{facts(p["dati"]) if p.get("dati") else ""}
<div class="prose">
{link_capanna(p.get("link", []))}
</div>
</aside>"""
    corpo = f"""<section class="section section--tight" aria-label="{tc('testo')}">
<div class="container article{'' if scheda else ' article--noimg'}">
<div class="prose">
{pdf_lingua(p["corpo"])}
</div>
{scheda}
</div>
</section>""" if p.get("corpo") else ""
    itinerari = ""
    if p.get("itinerari"):
        righe = "\n".join(f"""<article class="course-row" aria-labelledby="it-{i}-h" data-reveal>
<figure>{cimg(c, it["img"][0], it["img"][1])}</figure>
<div class="course-text">
<h2 id="it-{i}-h" class="h3">{it["titolo"]}</h2>
<p>{it["testo"]}</p>
<div class="prose">
{link_capanna(it.get("link", []))}
</div>
</div>
{facts(it["dati"]) if it.get("dati") else ""}
</article>""" for i, it in enumerate(p["itinerari"], 1))
        itinerari = f"""<section class="section" aria-label="{tc('itinerari')}">
<div class="container">
{righe}
</div>
</section>"""
    foto = f"""<section class="section" aria-labelledby="foto-h">
<div class="container">
<h2 id="foto-h" class="h2 gallery-h">{tc('foto')}</h2>
{galleria(c, p["foto"], p["titolo"])}
</div>
</section>""" if p.get("foto") else ""
    body = page_hero([(tc("capanne"), L("index.html#capanne")), (d["name"], L(file)), (p["titolo"], None)], p["titolo"], p["lead"]) + f"""

<figure class="band">
{cimg(c, p["img"][0], p["img"][1], lazy=False)}
</figure>

{corpo}

{itinerari}

{foto}

{hut_subnav(file, nome)}"""
    html = page(nome, f"{p['titolo']} | {tc('capanna')} {d['name']} | CAS Ticino", f"{p['lead']} {tc('capanna')} {d['name']}, CAS Ticino.",
                body, og=f"capanne/{c['cartella']}/{p['img'][0]}", section=tc("sezione_menu"))
    return pubblica(nome, html)


def hut_foto(file):
    c, d = contenuti(file), capanna(file)
    nome = L(f"capanne/{c['cartella']}/foto.html")
    gruppi = "\n\n".join(f"""<section class="section" aria-labelledby="g-{g}-h">
<div class="container">
<h2 id="g-{g}-h" class="h2 gallery-h">{titolo}</h2>
{galleria(c, g, f"{titolo}, {tc('capanna')} {d['name']}")}
</div>
</section>""" for titolo, g in c["foto"])
    body = page_hero([(tc("capanne"), L("index.html#capanne")), (d["name"], L(file)), (tc("foto"), None)], tc("foto"),
                     f"{c.get('foto_lead', tc('foto_lead'))}. {tc('tocca')}") + f"""

{gruppi}

{hut_subnav(file, nome)}"""
    html = page(nome, f"{tc('foto')} | {tc('capanna')} {d['name']} | CAS Ticino", tc("foto_desc").format(n=d["name"]),
                body, section=tc("sezione_menu"))
    return pubblica(nome, html)


def facebook(d):
    """Ultimi post della pagina Facebook della capanna: il riquadro ufficiale di Facebook
    (Page Plugin) viene caricato da site.js solo dopo il clic, così senza consenso non parte nessuna richiesta a Facebook."""
    if not d.get("facebook"):
        return ""
    return f"""
<section class="section" id="notizie" aria-labelledby="fb-h">
<div class="container">
<div class="fb" data-reveal>
<div class="contact-intro">
<h2 id="fb-h" class="h2">{tc('fb_h')}</h2>
<p>{tc('fb_p')}</p>
<a class="link" href="{d['facebook']}" rel="noopener">{tc('fb_apri')}</a>
</div>
<div class="fb-feed" data-fb="{d['facebook']}" data-lang="{tr('it_IT', 'de_DE', 'en_GB')}" data-titolo="Facebook {d['name']}">
<button type="button" class="btn btn--secondary">{tc('fb_carica')}</button>
<p class="small">{tc('fb_privacy')}</p>
</div>
</div>
</div>
</section>
"""


def avviso_capanna(file):
    """Avviso della capanna sotto la foto (data/avvisi-capanne/<capanna>.json, raccolta «Avvisi» in admin/):
    scuro, rosso se importante; uno solo per capanna. Dopo la scadenza lo toglie site.js (data-scade),
    anche se la pagina non è ancora stata rigenerata."""
    a = avviso(f"avvisi-capanne/{file.removesuffix('.html')}.json")
    if not a:
        return ""
    cls, etichetta = ("avviso-capanna avviso-capanna--importante", tc("importante")) if a.get("importante") else ("avviso-capanna", tc("avviso"))
    scade = f' data-scade="{a["scadenza"]}"' if a["scadenza"] else ""
    return f"""

<section class="section section--tight avviso-capanna-sez" aria-label="{tc('avviso')}"{scade}>
<div class="container">
<div class="{cls}">
<p class="avviso-capanna-tipo">{etichetta}</p>
<p>{avviso_testo(a)}</p>
</div>
</div>
</section>"""


def sostenitori(c):
    """Loghi dei sostenitori della capanna, in fondo alla pagina sotto «Sostieni la capanna»."""
    if not (c and c.get("sostenitori")):
        return ""
    loghi = "\n".join(f'<li>{logo_sostenitore(c, *l)}</li>' for l in c["sostenitori"]["loghi"])
    return f"""<section class="section" aria-labelledby="sostenitori-h">
<div class="container">
<div class="section-head">
<h2 id="sostenitori-h" class="h2">{tc('sostenitori')}</h2>
<p>{c["sostenitori"]["testo"]}</p>
</div>
<ul class="logos">
{loghi}
</ul>
</div>
</section>"""


def salti_capanna(c, d):
    """Pulsanti «In questa pagina» sotto la foto: portano alle sezioni della pagina capanna, nell'ordine in cui compaiono.
    La barra resta appiccicata sotto il menu e site.js evidenzia la sezione in cui ci si trova."""
    voci = [("contatti", tc("s_contatti"))]
    if c:
        if c.get("cucina") or c.get("team"):
            voci.append(("vita", tc("s_vita") if c.get("cucina") and c.get("team") else
                         c.get("cucina_titolo", tc("cucina")) if c.get("cucina") else c["team"].get("titolo", tc("team"))))
        voci += [(k, tc(l)) for k, l in (("tariffe", "s_tariffe"), ("accessi", "accessi"), ("pagine", "attivita"),
                                          ("storia", "storia"), ("foto", "foto")) if c.get(k)]
        voci = [("attivita" if k == "pagine" else k, l) for k, l in voci]
    if d.get("facebook"):
        voci.append(("notizie", tc("fb_h")))
    voci.append(("sostieni", tc("s_sostieni")))
    links = "\n".join(f'<a href="#{k}">{l}</a>' for k, l in voci)
    return f"""

<nav class="salti" aria-label="{tc('salta')}">
<div class="container subnav">
<p class="label">{tc('salta')}</p>
<div class="subnav-links">
{links}
</div>
</div>
</nav>"""


def fasce(body):
    """Pagina capanna a fasce come la home: le sezioni sotto «In questa pagina» alternano bianco e grigio nell'ordine in cui
    compaiono (ogni capanna ha sezioni diverse), contando dal fondo perché l'ultima resti bianca sopra il piè di pagina
    grigio; .fascia toglie le linee di separazione, che a fasce non servono."""
    sopra, barra, sotto = body.partition('<nav class="salti"')   # l'avviso della capanna, sopra la barra, resta com'è
    sezione = r'<section class="section(?:--surface)?((?: [\w-]+)*)"'
    n = iter(range(len(re.findall(sezione, sotto)) - 1, -1, -1))
    return sopra + barra + re.sub(sezione, lambda m: f'<section class="{"section" if next(n) % 2 == 0 else "section--surface"}{m.group(1)} fascia"', sotto)


def hut(file):
    d = capanna(file)
    c = contenuti(file)
    others = [h for h in {"it": HUTS, "de": HUTS_DE, "en": HUTS_EN}[LINGUA["lang"]] if h[0] != file]
    mini = "\n".join(f"""<a class="mini-hut" href="{L(f)}"><figure>{img(im, f"{tc('capanna')} {n}", w, h)}</figure><strong>{n}</strong><span>{q} m</span></a>"""
                     for f, n, q, v, st, t, posti, acc, im, (w, h), big in others)
    if "band" in d:
        base, alt, h = d["band"]
        band = f'<figure class="band">\n{pic(base, alt, mobile=base + "-4x3", w=2000, h=h, lazy=False)}\n</figure>'
        og = base + "-2000"
    else:
        name, alt, w, h = d["img"]
        band = band_img(name, alt, w, h)
        og = name
    custody_dt = tc("apertura") if file == "baitadelluca.html" else tc("custodia")
    # «Ultime notizie» porta alla sezione Facebook e la carica subito (site.js), senza il secondo clic
    azioni = (f'<div class="actions">{prenota(d)}<a class="btn btn--secondary" href="#notizie" data-fb-apri>{tc("fb_notizie")}</a></div>'
              if d.get("facebook") else prenota(d))
    extra = f"""<div class="keyfacts">
<dl>
<div><dt>{tc('altitudine')}</dt><dd class="num">{d['alt_m']} m</dd></div>
<div><dt>{tc('posti')}</dt><dd class="num">{d['beds']}</dd></div>
<div><dt>{custody_dt}</dt><dd>{d['custody']}</dd></div>
</dl>
{azioni}
</div>"""
    avviso = avviso_capanna(file)
    testo = f'\n<div class="prose">\n{c["capanna"]}\n</div>' if c and c.get("capanna") else ""
    body = page_hero([(tc("capanne"), L("index.html#capanne")), (d["name"], None)], d["name"], d["where"], extra) + f"""

{band}{avviso}{salti_capanna(c, d)}

<section class="section contatti-capanna" id="contatti" aria-labelledby="contatti-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="contatti-h" class="h2">{tc('contatti_h')}</h2>
<p>{tc('contatti_p')}</p>
</div>
{facts(d['contact'])}
</div>
</div>
</section>

<section class="section" aria-labelledby="capanna-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="capanna-h" class="h2">{c.get("capanna_titolo", tc("la_capanna")) if c else tc("la_capanna")}</h2>
<p>{d['intro']}</p>{testo}
</div>
<div class="factgroups" data-reveal>
<div class="factgroup">
<h3 class="h3">{tc('soggiorno')}</h3>
{facts(d['stay'])}
</div>
<div class="factgroup">
<h3 class="h3">{tc('arrivare')}</h3>
{facts([r for r in d['reach'] if not (c and c.get('accessi')) or 'CNS' in r[1]])}
{f'<p><a class="link" href="{PORTALE_CAS[LINGUA["lang"]].format(d["portale"])}" rel="noopener">{tc("portale")}</a></p>' if d.get("portale") else ""}
</div>
</div>
</div>
</section>

{hut_extra(file) if c else ""}
{facebook(d)}

<section class="section" id="sostieni" aria-labelledby="sostieni-h">
<div class="container">
<div class="contact contact--linea" data-reveal>
<div class="contact-intro">
<h2 id="sostieni-h" class="h2">{tc('sostieni_h')}</h2>
<p>{tc('sostieni_p')}</p>
</div>
{facts([(tc("conto"), f'Banca Stato, Lugano<br><span class="num">IBAN {IBAN}</span>'), (tc("causale"), f"{tc('capanna') + ' ' if file != 'baitadelluca.html' else ''}{d['name']}")])}
</div>
</div>
</section>
{sostenitori(c)}

<section class="section" aria-labelledby="altre-h">
<div class="container">
<div class="section-head"><h2 id="altre-h" class="h3">{tc('altre')}</h2></div>
<div class="mini-huts">
{mini}
</div>
</div>
</section>"""
    body = fasce(body)
    prefix = tc("capanna") + " " if file != "baitadelluca.html" else ""
    nome = L(file)
    return pubblica(nome, page(nome, f"{prefix}{d['name']} | CAS Ticino", d["description"], body, og=og))


# ------------------------------------------------------------------ la sezione

def introduzione():
    huts = ('<a href="campotencia.html">Campo Tencia</a>, <a href="cristallina.html">Cristallina</a>, <a href="adula.html">Adula</a>, '
            '<a href="motterascio.html">Motterascio (Michela)</a>, <a href="montebar.html">Monte Bar</a> e <a href="baitadelluca.html">Baita del Luca</a>')
    body = page_hero([("La Sezione", "introduzione.html"), ("Chi siamo", None)], "La sezione",
                     "Fondata a Bellinzona l’11 aprile 1886, la Sezione Ticino del Club Alpino Svizzero conta quasi 3000 soci e propone un’attività varia, pensata per tutte le età: dai più giovani ai seniori.") + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", "Gruppo di alpinisti in cammino su un ghiacciaio", mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
{credito()}
</figure>

<section class="section--accent" aria-label="La sezione in cifre">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>fondata a Bellinzona l’11 aprile</span></div>
<div class="stat"><strong>3000</strong><span>soci, dai più giovani ai seniori</span></div>
<div class="stat"><strong>6</strong><span>capanne gestite dalla sezione</span></div>
<div class="stat"><strong>5</strong><span>dicasteri accanto al comitato</span></div>
</div>
</div>
</section>

<section class="section" aria-labelledby="cosa-h">
<div class="container">
<div class="section-head">
<h2 id="cosa-h" class="h2">In montagna,<br>in ogni stagione</h2>
</div>
<div class="pillars" data-reveal>
<article class="pillar pillar--photo pillar--wide">
{img("paesaggi/cresta-lugano-2000", "Alpinisti su una cresta rocciosa", 2000, 580)}
<h3>Discipline</h3>
<p>Escursionismo, alpinismo, arrampicata, sci alpinismo, racchette e cascate di ghiaccio.</p>
</article>
<article class="pillar pillar--accent">
<h3>Per chi inizia</h3>
<p>Corsi di introduzione ad alpinismo, sci alpinismo, racchette e arrampicata in ambiente.</p>
<a class="link" href="corsi.html">Vedi i corsi</a>
</article>
<article class="pillar pillar--photo">
{img("capanne/montebar-3x2", "La Capanna Monte Bar", 663, 442)}
<h3>Capanne</h3>
<p>La sezione gestisce sei rifugi: {huts}.</p>
</article>
<article class="pillar">
<h3>Oltre lo sport</h3>
<p>Coordina il soccorso alpino nel Sottoceneri, si impegna per la tutela dell’ambiente alpino e promuove la cultura della montagna.</p>
</article>
<article class="pillar">
<h3>Come funziona</h3>
<p>Un <a href="comitato.html">comitato</a> coordina le diverse attività, affiancato da cinque <a href="organizzazione.html">dicasteri</a> e dal lavoro volontario dei soci.</p>
</article>
<article class="pillar pillar--photo pillar--wide-md">
{img("corsi/racchette-4x5", "Cresta innevata sopra un mare di nuvole", 800, 1000)}
<h3>Comunicazione</h3>
<p>Programma delle attività, sito web, un periodico semestrale e l’annuario che racconta la vita della sezione.</p>
</article>
<article class="pillar pillar--dark pillar--wide">
<h3>Statuto, visione e strategia, organigramma</h3>
<p>I documenti di riferimento della sezione. Altri documenti utili sono disponibili nella pagina <a href="documenti.html">Documenti</a>.</p>
<div class="actions"><a class="btn btn--primary" href="{DOC}statuto-visione/statuto-2025.pdf">Statuto <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/visione-strategia-2025.pdf">Visione e strategia</a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/organigramma-2025.pdf">Organigramma</a></div>
</article>
</div>
</div>
</section>

{subnav("La Sezione", "introduzione.html")}"""
    return page("introduzione.html", "La sezione | CAS Ticino",
                "La Sezione Ticino del Club Alpino Svizzero: fondata nel 1886, quasi 3000 soci, sei capanne, corsi, gite e attività per tutte le età.",
                body, og="paesaggi/gruppo-ghiacciaio-2000")


COMITATO = [
    ("Presidente", "Giovanni Galli", "giovanni-galli"),
    ("Capanne e vicepresidente", "Richard Knupfer", "richard-knupfer"),
    ("Segretaria", "Melanie Becchi", "melanie-becchi"),
    ("Consigliere giuridico", "Costantino Castelli", "costantino-castelli"),
    ("Finanze e sponsoring", "Claudio Roncoroni", "claudio-roncoroni"),
    ("Coordinazione gruppi", "Nadir Caduff", "nadir-caduff"),
    ("Sport di montagna", "Geoffroy Jolly", "geoffroy-jolly"),
    ("Comunicazione", "Flavia Spinelli", None),
]


def initials(name):
    return "".join(p[0] for p in name.split()[:2]).upper()


RUOLI_DE = {
    # comitato
    "Presidente": "Präsident", "Capanne e vicepresidente": "Hütten und Vizepräsident", "Segretaria": "Sekretärin",
    "Consigliere giuridico": "Rechtsberater", "Finanze e sponsoring": "Finanzen und Sponsoring",
    "Coordinazione gruppi": "Koordination der Gruppen", "Sport di montagna": "Bergsport", "Comunicazione": "Kommunikation",
    # dicasteri
    "Responsabile capanne": "Verantwortlicher Hütten", "Responsabile sentieri": "Verantwortlicher Wanderwege",
    "Responsabile tecnico capanne": "Technischer Verantwortlicher Hütten",
    "Coordinatore e responsabile attività": "Koordinator und Verantwortlicher Aktivitäten", "Responsabile formazione": "Verantwortlicher Ausbildung",
    "Responsabile magazzino": "Verantwortlicher Materiallager",
    "Amministratrice sito web": "Administratorin Website", "Membro": "Mitglied", "Coordinatore e comunicazione": "Koordinator und Kommunikation",
    "Coach": "Coach", "Cassiere": "Kassier", "Segretariato, giovanissimi e Spider": "Sekretariat, Jüngste und Spider",
    "Attività del mercoledì sera e arrampicata": "Mittwochabend und Klettern", "Attività estive": "Sommeraktivitäten",
    "Attività invernali": "Winteraktivitäten", "Coordinatore gite": "Tourenkoordinator", "Informatica": "Informatik",
    "Responsabile comunicazione": "Leitung Kommunikation", "Redazione Informazione": "Redaktion Informazione", "Redazione annuario": "Redaktion Jahrbuch", "Eventi": "Anlässe",
    "Grafica": "Grafik", "Responsabile ambiente": "Verantwortliche Umwelt",
}


RUOLI_EN = {
    # comitato
    "Presidente": "President", "Capanne e vicepresidente": "Huts and vice-president", "Segretaria": "Secretary",
    "Consigliere giuridico": "Legal adviser", "Finanze e sponsoring": "Finance and sponsorship",
    "Coordinazione gruppi": "Group coordination", "Sport di montagna": "Mountain sports", "Comunicazione": "Communication",
    # dicasteri
    "Responsabile capanne": "Head of huts", "Responsabile sentieri": "Head of trails",
    "Responsabile tecnico capanne": "Technical manager, huts",
    "Coordinatore e responsabile attività": "Coordinator and head of activities", "Responsabile formazione": "Head of training",
    "Responsabile magazzino": "Equipment store manager",
    "Amministratrice sito web": "Website administrator", "Membro": "Member", "Coordinatore e comunicazione": "Coordinator and communication",
    "Coach": "Coach", "Cassiere": "Treasurer", "Segretariato, giovanissimi e Spider": "Secretariat, youngest members and Spider",
    "Attività del mercoledì sera e arrampicata": "Wednesday evenings and climbing", "Attività estive": "Summer activities",
    "Attività invernali": "Winter activities", "Coordinatore gite": "Trip coordinator", "Informatica": "IT",
    "Responsabile comunicazione": "Head of communication", "Redazione Informazione": "Informazione editor", "Redazione annuario": "Yearbook editor", "Eventi": "Events",
    "Grafica": "Graphic design", "Responsabile ambiente": "Head of environment",
}


def ruolo(r):
    """Ruolo nella lingua corrente (gli ispettori delle capanne sono «Hüttenchef» in tedesco, «hut supervisor» in inglese)."""
    if LINGUA["lang"] == "it":
        return r
    if r.startswith("Ispettore "):
        capanne = r[len("Ispettore "):]
        return tr(r, "Hüttenchef " + capanne.replace(" e ", " und "), "Hut supervisor, " + capanne.replace(" e ", " and "))
    return tr(r, RUOLI_DE.get(r, r), RUOLI_EN.get(r, r))


def sezione_page(file, title, description, body, **kw):
    """Pagina della sezione nella lingua corrente (tradotta: de/<file>, en/<file>)."""
    nome = L(file)
    return pubblica(nome, page(nome, title, description, body, **kw))


def comitato():
    people = []
    ritratto = tr("Ritratto di", "Porträt von", "Portrait of")
    for role, name, photo in COMITATO:
        role = ruolo(role)
        ph = (f'<img src="assets/img/persone/comitato/{photo}.webp" alt="{ritratto} {name}" width="96" height="96" loading="lazy">'
              if photo else f'<span aria-hidden="true">{initials(name)}</span>')
        people.append(f"""<article class="person">
<div class="person-photo">{ph}</div>
<div class="person-body">
<span class="role">{role}</span>
<h2>{name}</h2>
</div>
</article>""")
    if de():
        body = page_hero([("Die Sektion", "de/introduzione.html"), ("Vorstand", None)], "Der Vorstand",
                         "Acht Personen, jede mit einem klaren Aufgabenbereich, führen die Sektion zusammen mit den <a href=\"de/organizzazione.html\">Ressorts</a> und den Freiwilligen. Kontakt: <a href=\"mailto:info@casticino.ch\">info@casticino.ch</a>.")
    elif en():
        body = page_hero([("The Section", "en/introduzione.html"), ("Committee", None)], "The committee",
                         "Eight people, each with a clear area of responsibility, lead the section together with the <a href=\"en/organizzazione.html\">departments</a> and the volunteers. Contact: <a href=\"mailto:info@casticino.ch\">info@casticino.ch</a>.")
    else:
        body = page_hero([("La Sezione", "introduzione.html"), ("Comitato", None)], "Il comitato",
                         "Otto persone, ognuna con un ambito preciso, che guidano la sezione insieme ai <a href=\"organizzazione.html\">dicasteri</a> e ai volontari. Per scrivere al comitato: <a href=\"mailto:info@casticino.ch\">info@casticino.ch</a>.")
    body += f"""

<section class="section" aria-label="{tr("Membri del comitato", "Mitglieder des Vorstands", "Committee members")}">
<div class="container">
<div class="people" data-reveal>
{chr(10).join(people)}
</div>
</div>
</section>

{subnav(tr("La Sezione", "Die Sektion", "The Section"), L("comitato.html"))}"""
    if de():
        return sezione_page("comitato.html", "Vorstand | CAS Ticino",
                            "Der Vorstand der Sektion Ticino des Schweizer Alpen-Clubs: Präsident, Vizepräsident, Sekretärin und Verantwortliche, mit Kontakten.", body)
    if en():
        return sezione_page("comitato.html", "Committee | CAS Ticino",
                            "The committee of the Ticino Section of the Swiss Alpine Club: president, vice-president, secretary and heads of area, with contacts.", body)
    return page("comitato.html", "Comitato | CAS Ticino",
                "Il comitato della Sezione Ticino del Club Alpino Svizzero: presidente, vicepresidente, segretaria e responsabili, con i recapiti.",
                body)


DICASTERI = [
    ("Dicastero infrastruttura",
     "Si occupa delle infrastrutture della sezione: capanne e sentieri. Affianca il comitato su tutte le questioni e i progetti legati ai rifugi. Tramite gli ispettori segue l’operato dei guardiani, coordina la manutenzione ordinaria e straordinaria, cura gli aspetti amministrativi e contrattuali con i guardiani e sviluppa la promozione delle capanne.",
     [("Richard Knupfer", "Responsabile capanne"),
      ("Ulisse Conrengia", "Responsabile sentieri"),
      ("Stefano Olgiati", "Responsabile sentieri"),
      ("Edgardo Bulloni", "Responsabile tecnico capanne"),
      (None, "Ispettore Capanna Michela Motterascio"),
      ("Edy Galli", "Ispettore Capanna Campo Tencia"),
      ("Fabio Savoldelli", "Ispettore Capanna Adula"),
      ("Marzio Pagani", "Ispettore Capanna Cristallina e Baita del Luca"),
      ("Francesco Mattinelli", "Ispettore Capanna Cristallina"),
      ("Erico Fogliada", "Ispettore Capanna Monte Bar"),
      ("Mauro Scalmanini", "Ispettore Capanna Monte Bar"),
      ("Roberto Grassi", "Ispettore Capanna Monte Bar")]),
    ("Dicastero sport di montagna",
     "Oltre a comporre il programma annuale delle gite, aggiorna e prepara materiale formativo, consiglia e sostiene i capigita promuovendone la formazione continua e gestisce il materiale tecnico della sezione.",
     [("Geoffroy Jolly", "Coordinatore e responsabile attività"),
      ("Enrico Zamboni", "Responsabile formazione"),
      ("David Stracquadanio", "Membro"),
      ("Michele Foletti", "Responsabile magazzino"),
      ("Valeria Demarta", "Amministratrice sito web"),
      ("Sara Della Frera", "Membro"),
      ("Thomas Arn", "Membro"),
      ("Alessandro Docimo", "Membro")]),
    ("Dicastero giovani",
     "Organizza campi settimanali e attività di arrampicata per ragazze e ragazzi dai 2 ai 25 anni e promuove la formazione di monitori Gioventù+Sport.",
     [("Diego Romelli", "Coordinatore e comunicazione"),
      ("Claudio Petrini", "Coach"),
      ("Nicola Martinoni", "Cassiere"),
      ("Giosiana Codoni", "Segretariato, giovanissimi e Spider"),
      ("Deborah Acierno", "Attività del mercoledì sera e arrampicata"),
      ("Kilian Knupfer", "Attività estive"),
      ("Jacopo Soldini", "Attività invernali")]),
    ("Dicastero senior",
     "Coordina il programma annuale del gruppo Senior: gite di un giorno, fine settimana e vacanze di più giorni. È sempre alla ricerca di nuovi capigita.",
     [("Luca Salzborn", "Presidente"),
      ("Cati Eisenhut", "Segretaria"),
      ("Christoph Rudolf von Rohr", "Cassiere"),
      ("Fausto Cattalini", "Coordinatore gite"),
      ("Fabrizio Gastori", "Informatica"),
      ("Walter Baumgartner", "Membro")]),
    ("Dicastero comunicazione",
     "Cura il periodico semestrale, l’annuario, il sito e i canali social. Organizza, anche con altri partner, eventi e iniziative che promuovono la cultura della montagna.",
     [("Flavia Spinelli", "Responsabile comunicazione"),
      ("Dario Lanfranconi", "Redazione Informazione"),
      ("Alessandro Romelli", "Redazione annuario"),
      ("Katia Papa", "Eventi"),
      ("Roberto Grizzi", "Grafica"),
      ("Zita Sartori", "Responsabile ambiente"),
      ("Maria Jannuzzi", "Membro"),
      ("Tiziano Allevi", "Membro")]),
]


DICASTERI_DE = {
    "Dicastero infrastruttura": ("Ressort Infrastruktur",
        "Kümmert sich um die Infrastruktur der Sektion: Hütten und Wanderwege. Unterstützt den Vorstand in allen Fragen und Projekten rund um die Hütten. Über die Hüttenchefs begleitet es die Arbeit der Hüttenwarte, koordiniert den laufenden und ausserordentlichen Unterhalt, betreut die administrativen und vertraglichen Fragen mit den Hüttenwarten und fördert die Hütten."),
    "Dicastero sport di montagna": ("Ressort Bergsport",
        "Stellt das jährliche Tourenprogramm zusammen, aktualisiert und erstellt Ausbildungsunterlagen, berät und unterstützt die Tourenleiter in ihrer Weiterbildung und verwaltet das technische Material der Sektion."),
    "Dicastero giovani": ("Ressort Jugend",
        "Organisiert Lagerwochen und Kletteraktivitäten für Mädchen und Jungen von 2 bis 25 Jahren und fördert die Ausbildung von Leitern Jugend+Sport."),
    "Dicastero senior": ("Ressort Senioren",
        "Koordiniert das Jahresprogramm der Seniorengruppe: Tagestouren, Wochenenden und mehrtägige Ferien. Ist immer auf der Suche nach neuen Tourenleitern."),
    "Dicastero comunicazione": ("Ressort Kommunikation",
        "Betreut das halbjährliche Bulletin, das Jahrbuch, die Website und die sozialen Medien. Organisiert, auch mit Partnern, Anlässe und Initiativen zur Bergkultur."),
}

DICASTERI_EN = {
    "Dicastero infrastruttura": ("Infrastructure department",
        "Looks after the section’s infrastructure: huts and trails. Supports the committee on all matters and projects concerning the huts. Through the hut supervisors it oversees the work of the hut keepers, coordinates routine and extraordinary maintenance, handles administrative and contractual matters with the keepers and promotes the huts."),
    "Dicastero sport di montagna": ("Mountain sports department",
        "Puts together the annual trip programme, updates and prepares training material, advises and supports trip leaders in their continuing training and manages the section’s technical equipment."),
    "Dicastero giovani": ("Youth department",
        "Organises week-long camps and climbing activities for girls and boys aged 2 to 25 and promotes the training of Youth+Sport instructors."),
    "Dicastero senior": ("Seniors department",
        "Coordinates the annual programme of the Seniors group: day trips, weekends and holidays of several days. Always looking for new trip leaders."),
    "Dicastero comunicazione": ("Communication department",
        "Looks after the half-yearly bulletin, the yearbook, the website and social media. Organises events and initiatives, also with partners, that promote mountain culture."),
}

CARTELLE_DICASTERI = {"Dicastero infrastruttura": "infrastruttura", "Dicastero sport di montagna": "sport-di-montagna",
                      "Dicastero giovani": "giovani", "Dicastero senior": "senior", "Dicastero comunicazione": "comunicazione"}
MAIL_DICASTERI = {"Dicastero infrastruttura": "infrastruttura@casticino.ch", "Dicastero sport di montagna": "sport@casticino.ch",
                  "Dicastero giovani": "giovani@casticino.ch", "Dicastero senior": "senior@casticino.ch",
                  "Dicastero comunicazione": "comunicazione@casticino.ch"}


def slug_nome(nome):
    t = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def organizzazione():
    depts = []
    for i, (title, text, members) in enumerate(DICASTERI, 1):
        ms = []
        for name, role in members:
            role = ruolo(role)
            if name is None:
                ms.append(f'<div class="member member--tbd"><div class="member-photo" aria-hidden="true"><span>?</span></div>'
                          f'<div class="member-body"><strong>{tr("Da definire", "Noch offen", "To be appointed")}</strong><span>{role}</span></div></div>')
                continue
            foto = foto_persona(name, CARTELLE_DICASTERI[title])   # anche il ritratto del comitato, se nel dicastero manca
            ph = (f'<img src="{foto}" alt="{tr("Ritratto di", "Porträt von", "Portrait of")} {name}" width="60" height="60" loading="lazy" decoding="async">'
                  if foto else f'<span aria-hidden="true">{initials(name)}</span>')
            ms.append(f'<div class="member"><div class="member-photo">{ph}</div>'
                      f'<div class="member-body"><strong>{name}</strong><span>{role}</span></div></div>')
        titolo, testo = {"it": (title, text), "de": DICASTERI_DE.get(title), "en": DICASTERI_EN.get(title)}[LINGUA["lang"]]
        depts.append(f"""<article class="dept" id="{CARTELLE_DICASTERI[title]}" aria-labelledby="d{i}-h" data-reveal>
<div class="dept-intro">
<span class="dept-count">{len(members)} {tr("membri", "Mitglieder", "members")}</span>
<h2 id="d{i}-h" class="h2">{titolo}</h2>
<p>{testo}</p>
<p><a href="mailto:{MAIL_DICASTERI[title]}">{MAIL_DICASTERI[title]}</a></p>
</div>
<div class="members">
{chr(10).join(ms)}
</div>
</article>""")
    if de():
        body = page_hero([("Die Sektion", "de/introduzione.html"), ("Organisation", None)], "Organisation",
                         'Der <a href="de/comitato.html">Vorstand</a> stützt sich auf fünf Ressorts, die je für einen Bereich des Sektionslebens verantwortlich sind.')
    elif en():
        body = page_hero([("The Section", "en/introduzione.html"), ("Organisation", None)], "Organisation",
                         'The <a href="en/comitato.html">committee</a> relies on five departments, each responsible for one area of the section’s life.')
    else:
        body = page_hero([("La Sezione", "introduzione.html"), ("Organizzazione", None)], "Organizzazione",
                         'Il <a href="comitato.html">comitato</a> si appoggia a cinque dicasteri, ognuno responsabile di un ambito della vita della sezione.')
    body += f"""

<section class="section" aria-label="{tr("Dicasteri", "Ressorts", "Departments")}">
<div class="container">
{chr(10).join(depts)}
</div>
</section>

{subnav(tr("La Sezione", "Die Sektion", "The Section"), L("organizzazione.html"))}"""
    if de():
        return sezione_page("organizzazione.html", "Organisation | CAS Ticino",
                            "Die fünf Ressorts der Sektion Ticino des SAC (Infrastruktur, Bergsport, Jugend, Senioren, Kommunikation) mit ihren Mitgliedern und Kontakten.", body)
    if en():
        return sezione_page("organizzazione.html", "Organisation | CAS Ticino",
                            "The five departments of the Ticino Section of the SAC (infrastructure, mountain sports, youth, seniors, communication) with their members and contacts.", body)
    return page("organizzazione.html", "Organizzazione | CAS Ticino",
                "I cinque dicasteri della Sezione Ticino del CAS (infrastruttura, sport di montagna, giovani, senior, comunicazione) con i loro membri e recapiti.",
                body)

# Capigita: elenco da data/capigita.json (lo scrive scripts/capigita.py dall'export Droptour, senza dati personali)
RUOLI_CAPIGITA = [("estivo", "Estivo"), ("invernale", "Invernale"), ("arrampicata", "Arrampicata"),
                  ("escursionismo", "Escursionismo"), ("seniori", "Seniori"), ("aiuto", "Aiuto capogita"),
                  ("soccorso", "Soccorso alpino")]
RUOLI_CAPIGITA_EN = {"estivo": "Summer", "invernale": "Winter", "arrampicata": "Climbing", "escursionismo": "Hiking",
                     "seniori": "Seniors", "aiuto": "Assistant leader", "soccorso": "Mountain rescue"}
RUOLI_CAPIGITA_DE = {"estivo": "Sommer", "invernale": "Winter", "arrampicata": "Klettern", "escursionismo": "Wandern",
                     "seniori": "Senioren", "aiuto": "Hilfsleitung", "soccorso": "Bergrettung"}
CAPIGITA_T = {
    "it": dict(titolo="Capigita", sezione="La Sezione", sezione_href="introduzione.html", ritratto="Ritratto di", chi="Chi è",
               dal="Capogita dal", nuovo="Nuovo", nuovi="Nel {anno} se ne sono aggiunti {k}, segnati in rosso.", tutti="Tutti", filtra="Filtra per ruolo", elenco="Elenco dei capigita",
               uno="capogita", molti="capigita",
               lead="Le gite della sezione sono preparate e guidate da soci volontari, formati nei corsi del CAS: {n} capigita attivi, ognuno con le sue discipline.",
               box="<strong>Per i capigita.</strong> Le gite si pubblicano sul portale Droptour; il promemoria raccoglie compiti e procedure del capogita.",
               portale="Portale Droptour", promemoria="Promemoria capigita (PDF)",
               desc="I {n} capigita del CAS Ticino che preparano e guidano le gite della sezione: estive e invernali, arrampicata, escursionismo e seniori."),
    "de": dict(titolo="Tourenleitende", sezione="Die Sektion", sezione_href="de/introduzione.html", ritratto="Porträt von", chi="Wer ist",
               dal="Tourenleitung seit", nuovo="Neu", nuovi="{anno} sind {k} neu dazugekommen, rot markiert.", tutti="Alle", filtra="Nach Rolle filtern", elenco="Liste der Tourenleitenden",
               uno="Tourenleitende", molti="Tourenleitende",
               lead="Die Touren der Sektion werden von ehrenamtlichen Mitgliedern vorbereitet und geleitet, ausgebildet in den Kursen des SAC: {n} aktive Tourenleitende, alle mit ihren eigenen Disziplinen.",
               box="<strong>Für Tourenleitende.</strong> Die Touren werden im Droptour-Portal veröffentlicht; das Merkblatt fasst Aufgaben und Abläufe der Tourenleitung zusammen.",
               portale="Droptour-Portal", promemoria="Merkblatt Tourenleitung (PDF, italienisch)",
               desc="Die {n} Tourenleitenden des SAC Ticino, die die Touren der Sektion vorbereiten und leiten: Sommer- und Wintertouren, Klettern, Wandern und Senioren."),
    "en": dict(titolo="Trip leaders", sezione="The Section", sezione_href="en/introduzione.html", ritratto="Portrait of", chi="Who is",
               dal="Trip leader since", nuovo="New", nuovi="{k} joined in {anno}, marked in red.", tutti="All", filtra="Filter by role", elenco="List of trip leaders",
               uno="trip leader", molti="trip leaders",
               lead="The section’s trips are prepared and led by volunteer members trained in SAC courses: {n} active trip leaders, each with their own disciplines.",
               box="<strong>For trip leaders.</strong> Trips are published on the Droptour portal; the guidelines cover the trip leader’s tasks and procedures.",
               portale="Droptour portal", promemoria="Trip leader guidelines (PDF, in Italian)",
               desc="The {n} trip leaders of CAS Ticino who prepare and lead the section’s trips: summer and winter, climbing, hiking and seniors."),
}


def foto_persona(nome, gruppo):
    """Ritratto assets/img/persone/<gruppo>/<nome-cognome>.webp; se manca, quello della stessa persona in un altro gruppo."""
    gruppi = [gruppo] + sorted(g for g in os.listdir(os.path.join(ROOT, "assets", "img", "persone")) if g != gruppo)
    for g in gruppi:
        foto = f"assets/img/persone/{g}/{slug_nome(nome)}.webp"
        if os.path.exists(os.path.join(ROOT, foto)):
            return foto
    return None


def capigita():
    """Capigita da data/capigita.json (lo scrive scripts/capigita.py dall'export Droptour, senza dati personali)."""
    persone = json.load(open(os.path.join(ROOT, "data", "capigita.json"), encoding="utf-8"))["capigita"]
    # presentazioni scritte dai capigita (in italiano anche nelle pagine tradotte): box sulla foto
    info = json.load(open(os.path.join(ROOT, "data", "capigita-info.json"), encoding="utf-8"))
    tx = CAPIGITA_T[LINGUA["lang"]]
    nomi = {k: tr(n, RUOLI_CAPIGITA_DE[k], RUOLI_CAPIGITA_EN[k]) for k, n in RUOLI_CAPIGITA}
    # i capigita nuovi (capogita dall'anno in corso) sono segnati in rosso, senza un filtro a parte
    import datetime
    anno = datetime.date.today().year
    schede = []
    for p in persone:
        nuovo = (p.get("dal") or 0) >= anno
        foto = foto_persona(p["nome"], "capigita")
        ph = (f'<img src="{foto}" alt="{tx["ritratto"]} {p["nome"]}" width="60" height="60" loading="lazy" decoding="async">'
              if foto else f'<span aria-hidden="true">{initials(p["nome"])}</span>')
        ruoli = " · ".join(nomi[r] for r in p["ruoli"])
        dal = f'<span>{tx["dal"]} <span class="num">{p["dal"]}</span></span>' if p.get("dal") else ""
        tag = f' <span class="tag-nuovo">{tx["nuovo"]}</span>' if nuovo else ""
        corpo = f'<div class="member-body"><strong>{p["nome"]}{tag}</strong><span>{ruoli}</span>{dal}</div>'
        bio = info.get(p["nome"])
        if bio:
            id_bio = "bio-" + slug_nome(p["nome"])
            lang = "" if LINGUA["lang"] == "it" else ' lang="it"'
            schede.append(f'<div class="member member--bio{" member--nuovo" if nuovo else ""}" data-ruoli="{" ".join(p["ruoli"])}">'
                          f'<button type="button" class="bio-toggle" aria-expanded="false" aria-controls="{id_bio}" aria-label="{tx["chi"]} {p["nome"]}">'
                          f'<span class="member-photo">{ph}</span><span class="bio-segno" aria-hidden="true"></span></button>'
                          f'{corpo}<p class="bio" id="{id_bio}"{lang}>{html_escape(bio)}</p></div>')
        else:
            schede.append(f'<div class="member{" member--nuovo" if nuovo else ""}" data-ruoli="{" ".join(p["ruoli"])}"><div class="member-photo">{ph}</div>{corpo}</div>')
    conta = {k: sum(k in p["ruoli"] for p in persone) for k, _ in RUOLI_CAPIGITA}
    filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">{tx["tutti"]} <span class="num">{len(persone)}</span></button>'] +
                       [f'<button type="button" data-filtro="{k}" aria-pressed="false">{nomi[k]} <span class="num">{conta[k]}</span></button>'
                        for k, _ in RUOLI_CAPIGITA if conta[k]])
    n = len(persone)
    k = sum((p.get("dal") or 0) >= anno for p in persone)
    lead = tx["lead"].format(n=n) + (" " + tx["nuovi"].format(k=k, anno=anno) if k else "")
    body = page_hero([(tx["sezione"], tx["sezione_href"]), (tx["titolo"], None)], tx["titolo"], lead) + f"""

<section class="section" aria-label="{tx['elenco']}">
<div class="container">
<div class="filtro" role="group" aria-label="{tx['filtra']}" data-filtra="#capigita" data-uno="{tx['uno']}" data-molti="{tx['molti']}" hidden>
{filtri}
</div>
<p class="small filtro-stato" id="filtro-stato" aria-live="polite"></p>
<div class="members members--griglia" id="capigita">
{chr(10).join(schede)}
</div>
<div class="callout">
<p>{tx['box']}</p>
<div class="actions"><a class="btn btn--secondary" href="https://ssl.dropnet.ch/casticino/manager/touren/index.php" rel="noopener">{tx['portale']}</a><a class="btn btn--secondary" href="{DOC}promemoria/capigita.pdf">{tx['promemoria']}</a></div>
</div>
</div>
</section>

{subnav(tx["sezione"], L("capigita.html"))}"""
    return sezione_page("capigita.html", f"{tx['titolo']} | CAS Ticino", tx["desc"].format(n=n), body)


def soccorso():
    emergenza = [("Rega", f'<a class="num" href="tel:1414">1414</a> <span class="small">{tr("dall’estero", "aus dem Ausland", "from abroad")} <a class="num" href="tel:+41333333333">+41 333 333 333</a></span>'),
                 (tr("Ambulanza", "Sanität", "Ambulance"), '<a class="num" href="tel:144">144</a>'),
                 (tr("Emergenza europeo", "Europäischer Notruf", "European emergency number"), '<a class="num" href="tel:112">112</a>')]
    titolo = tr("Soccorso", "Bergrettung", "Mountain rescue")
    body = page_hero([sez_crumb(), (titolo, None)], titolo, tr(
                         "La sezione coordina il soccorso alpino nel Sottoceneri, con volontari formati che intervengono in montagna insieme al Soccorso Alpino Svizzero e alla Rega.",
                         "Die Sektion koordiniert die Bergrettung im Sottoceneri, mit ausgebildeten Freiwilligen, die zusammen mit der Alpinen Rettung Schweiz und der Rega im Gebirge im Einsatz sind.",
                         "The section coordinates mountain rescue in the Sottoceneri, with trained volunteers who work in the mountains alongside Swiss Alpine Rescue and Rega."),
                     figure=img("attivita/soccorso-4x5", tr("Soccorritori con casco e imbragatura recuperano una persona in barella in una gola rocciosa",
                                                           "Retter mit Helm und Klettergurt bergen eine Person auf einer Trage in einer Felsschlucht",
                                                           "Rescuers with helmets and harnesses recover a person on a stretcher in a rocky gorge"), 525, 657, lazy=False)
                     .replace("<img ", '<img class="orizzontale basso" ', 1) + credito("Urs Nett")) + f"""

<section class="section" aria-labelledby="emergenza-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="emergenza-h" class="h2">{tr("In caso di emergenza", "Im Notfall", "In an emergency")}</h2>
<p>{tr("Chiama subito: indica chi sei, dove ti trovi, cosa è successo e quante persone sono coinvolte. Resta raggiungibile al telefono.",
       "Rufen Sie sofort an: Sagen Sie, wer Sie sind, wo Sie sich befinden, was passiert ist und wie viele Personen betroffen sind. Bleiben Sie telefonisch erreichbar.",
       "Call immediately: say who you are, where you are, what has happened and how many people are involved. Stay reachable by phone.")}</p>
</div>
{facts(emergenza)}
</div>
</div>
</section>

<section class="section" aria-labelledby="colonna-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="colonna-h" class="h2">{tr("La colonna<br>di soccorso", "Die Rettungs­<br>station", "The rescue<br>team")}</h2>
<p>{tr("Dal 1918, quando nacquero le prime stazioni di soccorso alpino a Faido, Airolo e Olivone, la sezione è parte del soccorso in montagna in Ticino.",
       "Seit 1918, als in Faido, Airolo und Olivone die ersten Bergrettungsstationen entstanden, ist die Sektion Teil der Bergrettung im Tessin.",
       "Since 1918, when the first mountain rescue stations were set up in Faido, Airolo and Olivone, the section has been part of mountain rescue in Ticino.")}</p>
</div>
<div class="prose" data-reveal>
<p>{tr("Qui troverai presto le informazioni sulla colonna di soccorso della sezione: chi la compone, come è organizzata, la formazione dei soccorritori e come entrare a farne parte.",
       "Hier finden Sie bald Informationen über die Rettungsstation der Sektion: wer dazugehört, wie sie organisiert ist, die Ausbildung der Retterinnen und Retter und wie man mitmachen kann.",
       "Information about the section’s rescue team will be here soon: who is in it, how it is organised, how rescuers are trained and how to join.")}</p>
<div class="actions"><a class="btn btn--secondary" href="https://www.alpinerettung.ch" rel="noopener">{tr("Soccorso Alpino Svizzero", "Alpine Rettung Schweiz", "Swiss Alpine Rescue")}</a><a class="btn btn--secondary" href="https://www.rega.ch" rel="noopener">Rega</a></div>
</div>
</div>
</section>

{subnav(SEZ_MENU(), L("soccorso.html"))}"""
    return sezione_page("soccorso.html", titolo + " | CAS Ticino", tr(
        "Il soccorso alpino del CAS Ticino nel Sottoceneri: numeri d’emergenza (Rega 1414, 144, 112) e la colonna di soccorso della sezione.",
        "Die Bergrettung der SAC-Sektion Ticino im Sottoceneri: Notrufnummern (Rega 1414, 144, 112) und die Rettungsstation der Sektion.",
        "Mountain rescue by the SAC Ticino Section in the Sottoceneri: emergency numbers (Rega 1414, 144, 112) and the section’s rescue team."),
        body)


def rubrica():
    """Indirizzi e-mail @casticino.ch della sezione (pagina Sede, in tutte le lingue): segretariato, dicasteri,
    servizi e capanne. Gli indirizzi vengono da MAIL_DICASTERI, MERCATINO_MAIL e HUT_PAGES."""
    def riga(etichetta, mail):
        return (etichetta, f'<a href="mailto:{mail}">{mail}</a>')

    def nome_dicastero(k):
        return tr(k.removeprefix("Dicastero ").capitalize(), DICASTERI_DE[k][0], DICASTERI_EN[k][0])

    gruppi = [
        (tr("Sezione", "Sektion", "Section"),
         [riga(tr("Segretariato e informazioni", "Sekretariat und Auskünfte", "Secretariat and information"), "info@casticino.ch"),
          riga(tr("Sito web", "Website", "Website"), "webmaster@casticino.ch")]),
        (tr("Dicasteri", "Ressorts", "Departments"), [riga(nome_dicastero(k), m) for k, m in MAIL_DICASTERI.items()]),
        (tr("Servizi", "Dienste", "Services"),
         [riga(tr("Noleggio materiale", "Materialvermietung", "Equipment hire"), NOLEGGIO_MAIL),
          riga(tr("Mercatino", "Mercatino (Marktplatz)", "Mercatino (gear exchange)"), MERCATINO_MAIL)]),
        (tr("Capanne", "Hütten", "Huts"), [riga(d["name"], d["mail"]) for d in HUT_PAGES.values()]),
    ]
    blocchi = "\n".join(f'<div>\n<h3 class="h3">{titolo}</h3>\n{facts(righe)}\n</div>' for titolo, righe in gruppi)
    return f"""<section class="section" aria-labelledby="rubrica-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="rubrica-h" class="h2">{tr("Indirizzi e-mail", "E-Mail-Adressen", "E-mail addresses")}</h2>
<p>{tr("Per una domanda precisa scrivi direttamente a chi se ne occupa; per tutto il resto c’è il segretariato.",
       "Für eine bestimmte Frage schreiben Sie direkt an die zuständige Stelle; für alles andere ans Sekretariat.",
       "For a specific question, write directly to whoever deals with it; for anything else, write to the secretariat.")}</p>
</div>
<div class="rubrica" data-reveal>
{blocchi}
</div>
</div>
</section>"""


def sede():
    rows = [
        ("Recapito postale", "Club Alpino Svizzero<br>Sezione Ticino<br>Casella postale 112<br>6998 Monteggio 2"),
        ("E-mail", '<a href="mailto:info@casticino.ch">info@casticino.ch</a>'),
        ("Sede", "Stabile Canvetto Luganese, Molino Nuovo (Lugano)<br>2° piano, in balconata"),
        ("Biblioteca", 'Guide e cartine da consultare, libri in prestito; in vendita libri e magliette. Per visitarla scrivi al segretariato: <a href="mailto:info@casticino.ch">info@casticino.ch</a>.'),
        ("Coordinate bancarie", f'Banca Stato, Lugano<br><span class="num">IBAN {IBAN}</span>'),
    ]
    body = page_hero([("La Sezione", "introduzione.html"), ("Sede e contatti", None)], "Sede e contatti",
                     "La sede sociale si trova nello stabile del Canvetto Luganese a Molino Nuovo, con ufficio e sala riunioni al secondo piano in balconata.") + f"""

<section class="section" aria-labelledby="sede-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="sede-h" class="h2">Il Canvetto Luganese</h2>
<p>Qui si riuniscono il comitato e i dicasteri, si tengono le serate informative dei corsi e diversi appuntamenti culturali: proiezioni di uscite, viaggi e spedizioni di soci, serate con specialisti di meteo, valanghe e primo soccorso.</p>
<div><a class="btn btn--primary" href="mailto:info@casticino.ch">Scrivi alla sezione <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
{facts(rows)}
</div>
</div>
</section>

{rubrica()}

{subnav("La Sezione", "sede.html")}"""
    return page("sede.html", "Sede e contatti | CAS Ticino",
                "Sede del CAS Ticino al Canvetto Luganese (Molino Nuovo), recapito postale, e-mail, biblioteca e coordinate bancarie.",
                body)


STORIA = [
    ("1886", "L’11 aprile, alla Birraria Gambrinus di Bellinzona, nasce il Club Alpino Ticinese, nell’anno del centenario della prima salita al Monte Bianco, compiuta nel 1786 da Jacques Balmat e Michel-Gabriel Paccard. Primo presidente è l’avvocato Curzio Curti. Lo scopo: visitare, studiare e far conoscere le montagne del Cantone e delle regioni vicine."),
    ("1887", "Il 20 marzo il club si unisce al Club Alpino Svizzero come sezione ticinese; Lugano ne diventa la sede."),
    ("1911", "Oltre confine, a Lanzo d’Intelvi, viene inaugurato il vessillo sezionale. L’anno dopo, l’11 agosto 1912, la sezione inaugura in alta Val Piumogna, ai piedi del pizzo omonimo, la Capanna Campo Tencia: la prima capanna delle montagne ticinesi."),
    ("1913", "Le donne non sono ammesse nel CAS: a Lugano le alpiniste fondano allora un club tutto loro, presieduto da Adelina Rossi-Baragiola. Diventerà la sezione di Lugano del Club Alpino Femminile Svizzero, nato nel 1918, e il 22 settembre 1924 sarà presente, con circa 300 persone, all’inaugurazione della Capanna Adula."),
    ("1918", "In Leventina e in Valle di Blenio si costituiscono le stazioni di soccorso alpino di Faido, Airolo e Olivone: per la prima volta chi si ferisce in montagna può contare su squadre organizzate. La formazione delle guide spetta alla sezione, la nomina al Consiglio di Stato."),
    ("Anni ’30", "Cresce l’arrampicata su roccia: Emilio Comici, il numero uno dell’alpinismo italiano, viene invitato ai Denti della Vecchia, dove nel 1935 apre con Tita Calvi la via che porta il suo nome; i Denti diventano la palestra di casa della sezione e anche Riccardo Cassin vi si allena. Nel 1932 Tita Calvi, don Giugni e Aldo Balmelli aprono la Nord-Est del Piz Prevat; Bruno Primi «Stüva» diventa guida e firma grandi classiche, dal Civetta al Cervino. Nel 1935 Calvi e Balmelli guidano la prima scuola di sci del Ticino, all’Alpe Musgatina."),
    ("1936", "La sezione compie cinquant’anni e li festeggia con la prima capanna sul Monte Bar: le donne di Bidogno portano i materiali nella gerla fino al cantiere, e presto la domenica sulle piste si contano più di 300 sciatori. Lo stesso anno i primi soci arrivano nell’Himalaya centrale; seguiranno la Lapponia (1959), l’Huascarán (1977) e il Pumori (1978)."),
    ("1940", "Nasce il gruppo Seniori."),
    ("Anni ’60", "Nasce il gruppo giovanile OG ed entra in servizio la colonna di soccorso del Sottoceneri. Nel 1963 l’alpinista Aldo Fontana porta nuovi stimoli; nel 1964 nasce il Gruppo Scoiattoli, che negli anni aprirà e documenterà gran parte delle vie dei Denti della Vecchia."),
    ("1980", "Le sezioni maschile e femminile si fondono, come in tutta la Svizzera: fino a quell’anno il Club Alpino Svizzero era riservato agli uomini e le alpiniste avevano un club tutto loro. Alle spalle c’è un decennio difficile: il 22 agosto 1975 un incendio distrugge la Capanna Campo Tencia, che rinasce nel 1977 con una struttura in acciaio, innovativa per l’epoca, dell’architetto sezionale Oscar Hofmann."),
    ("1982", "Prima edizione della «settimana mini» per i più piccoli."),
    ("2003", "Nel febbraio 1999 una serie di valanghe aveva distrutto la vecchia Capanna Cristallina, del 1939. La nuova, progettata dagli architetti Nicola Baserga e Christian Mozzetti, sorge sul Passo di Cristallina a 2575 m in soli otto mesi di cantiere, nelle estati 2001 e 2002; apre nel dicembre 2002 e viene inaugurata ufficialmente nel luglio 2003. È il primo rifugio moderno del CAS."),
    ("2016", "Ottant’anni dopo il primo rifugio apre la nuova Capanna Monte Bar. Il concorso del 2014 era stato vinto, tra trenta progetti, da «Barlume» degli architetti Oliviero Piffaretti e Carlo Romano: un edificio semplice in legno, costruito attorno al focolare come luogo d’incontro e pensato con il Comune di Capriasca per valorizzare tutta la regione."),
]


STORIA_DE = [
    ("1886", "Am 11. April wird in der Birraria Gambrinus in Bellinzona der Club Alpino Ticinese gegründet, im Jahr des hundertjährigen Jubiläums der Erstbesteigung des Mont Blanc durch Jacques Balmat und Michel-Gabriel Paccard (1786). Erster Präsident ist Rechtsanwalt Curzio Curti. Das Ziel: die Berge des Kantons und der Nachbarregionen besuchen, erforschen und bekannt machen."),
    ("1887", "Am 20. März schliesst sich der Club als Tessiner Sektion dem Schweizer Alpen-Club an; Sitz ist Lugano."),
    ("1911", "Jenseits der Grenze, in Lanzo d’Intelvi, wird die Sektionsfahne eingeweiht. Ein Jahr später, am 11. August 1912, weiht die Sektion im oberen Val Piumogna, am Fuss des gleichnamigen Gipfels, die Capanna Campo Tencia ein: die erste Hütte in den Tessiner Bergen."),
    ("1913", "Frauen sind im SAC nicht zugelassen: In Lugano gründen die Bergsteigerinnen deshalb einen eigenen Club unter dem Vorsitz von Adelina Rossi-Baragiola. Er wird zur Sektion Lugano des 1918 gegründeten Schweizerischen Frauen-Alpen-Clubs und ist am 22. September 1924 mit rund 300 Personen bei der Einweihung der Capanna Adula dabei."),
    ("1918", "In der Leventina und im Bleniotal entstehen die Rettungsstationen von Faido, Airolo und Olivone: Wer sich in den Bergen verletzt, kann erstmals auf organisierte Mannschaften zählen. Die Ausbildung der Bergführer liegt bei der Sektion, die Ernennung beim Staatsrat."),
    ("1930er-Jahre", "Das Felsklettern gewinnt an Bedeutung: Emilio Comici, die Nummer eins des italienischen Alpinismus, wird an die Denti della Vecchia eingeladen, wo er 1935 mit Tita Calvi die nach ihm benannte Route eröffnet; die Denti werden zum Hausklettergebiet der Sektion, auch Riccardo Cassin trainiert dort. 1932 eröffnen Tita Calvi, Don Giugni und Aldo Balmelli die Nordostwand des Piz Prevat; Bruno Primi «Stüva» wird Bergführer und begeht grosse Klassiker, von der Civetta bis zum Matterhorn. 1935 leiten Calvi und Balmelli auf der Alpe Musgatina die erste Skischule des Tessins."),
    ("1936", "Die Sektion wird fünfzig und feiert mit der ersten Hütte auf dem Monte Bar: Die Frauen von Bidogno tragen das Baumaterial in der Tragkiepe zur Baustelle hinauf, und an Sonntagen zählt man auf den Pisten bald über 300 Skifahrende. Im selben Jahr erreichen die ersten Mitglieder den zentralen Himalaya; später folgen Lappland (1959), Huascarán (1977) und Pumori (1978)."),
    ("1940", "Die Seniorengruppe wird gegründet."),
    ("1960er-Jahre", "Die Jugendorganisation JO entsteht, und die Rettungskolonne Sottoceneri nimmt ihren Dienst auf. 1963 bringt der Bergsteiger Aldo Fontana neue Impulse; 1964 entsteht die Gruppo Scoiattoli, die mit den Jahren einen grossen Teil der Routen an den Denti della Vecchia eröffnet und dokumentiert."),
    ("1980", "Die Männer- und die Frauensektion schliessen sich zusammen, wie in der ganzen Schweiz: Bis dahin war der Schweizer Alpen-Club den Männern vorbehalten, und die Bergsteigerinnen hatten ihren eigenen Club. Dahinter liegt ein schwieriges Jahrzehnt: Am 22. August 1975 zerstört ein Brand die Capanna Campo Tencia; 1977 entsteht sie neu, mit einer für die Zeit innovativen Stahlkonstruktion des Sektionsarchitekten Oscar Hofmann."),
    ("1982", "Erste Ausgabe der «Mini-Woche» für die Kleinsten."),
    ("2003", "Im Februar 1999 hatten Lawinen die alte Capanna Cristallina von 1939 zerstört. Die neue Hütte der Architekten Nicola Baserga und Christian Mozzetti entsteht in nur acht Monaten Bauzeit in den Sommern 2001 und 2002 auf dem Passo di Cristallina, auf 2575 m; sie öffnet im Dezember 2002 und wird im Juli 2003 offiziell eingeweiht. Sie ist die erste moderne Hütte des SAC."),
    ("2016", "Achtzig Jahre nach der ersten Hütte öffnet die neue Capanna Monte Bar. Den Wettbewerb von 2014 hatte unter dreissig Projekten «Barlume» der Architekten Oliviero Piffaretti und Carlo Romano gewonnen: ein schlichter Holzbau rund um die Feuerstelle als Ort der Begegnung, geplant mit der Gemeinde Capriasca, um die ganze Region aufzuwerten."),
]


STORIA_EN = [
    ("1886", "On 11 April, at the Birraria Gambrinus in Bellinzona, the Club Alpino Ticinese is founded, in the centenary year of the first ascent of Mont Blanc by Jacques Balmat and Michel-Gabriel Paccard in 1786. Its first president is the lawyer Curzio Curti. Its aim: to visit, study and make known the mountains of the canton and the neighbouring regions."),
    ("1887", "On 20 March the club joins the Swiss Alpine Club as its Ticino section, based in Lugano."),
    ("1911", "Across the border, in Lanzo d’Intelvi, the section banner is inaugurated. A year later, on 11 August 1912, the section opens Capanna Campo Tencia at the head of Val Piumogna, below the peak of the same name: the first hut in the Ticino mountains."),
    ("1913", "Women are not admitted to the SAC, so in Lugano women climbers found a club of their own, chaired by Adelina Rossi-Baragiola. It becomes the Lugano section of the Swiss Women’s Alpine Club, founded in 1918, and on 22 September 1924 it is among the some 300 people at the inauguration of Capanna Adula."),
    ("1918", "In Leventina and Valle di Blenio, mountain rescue stations are set up in Faido, Airolo and Olivone: for the first time, anyone injured in the mountains can count on organised teams. Training the guides is the section’s task; appointing them is up to the cantonal government."),
    ("1930s", "Rock climbing grows: Emilio Comici, the leading Italian alpinist of the day, is invited to the Denti della Vecchia, where in 1935 he and Tita Calvi open the route that bears his name; the Denti become the section’s home crag, and Riccardo Cassin trains there too. In 1932 Tita Calvi, Don Giugni and Aldo Balmelli open the north-east face of Piz Prevat; Bruno Primi “Stüva” becomes a guide and climbs great classics, from the Civetta to the Matterhorn. In 1935 Calvi and Balmelli run Ticino’s first ski school, at Alpe Musgatina."),
    ("1936", "The section turns fifty and celebrates with the first hut on Monte Bar: the women of Bidogno carry the building materials up in baskets on their backs, and on Sundays there are soon more than 300 skiers on the slopes. The same year the first members reach the central Himalaya, followed later by Lapland (1959), Huascarán (1977) and Pumori (1978)."),
    ("1940", "The Seniors group is founded."),
    ("1960s", "The OG youth group is founded and the Sottoceneri rescue team goes into service. In 1963 the climber Aldo Fontana brings new energy; in 1964 the Gruppo Scoiattoli is founded, which over the years opens and documents most of the routes on the Denti della Vecchia."),
    ("1980", "The men’s and women’s sections merge, as they do across Switzerland: until then the Swiss Alpine Club was for men only, and women climbers had a club of their own. Behind it lies a difficult decade: on 22 August 1975 a fire destroys Capanna Campo Tencia, which is rebuilt in 1977 with a steel structure, innovative for its time, by the section’s architect Oscar Hofmann."),
    ("1982", "First edition of the “mini week” for the youngest children."),
    ("2003", "In February 1999 a series of avalanches had destroyed the old Capanna Cristallina, built in 1939. The new hut, designed by the architects Nicola Baserga and Christian Mozzetti, goes up on the Cristallina Pass at 2575 m in just eight months of work over the summers of 2001 and 2002; it opens in December 2002 and is officially inaugurated in July 2003. It is the first modern hut of the SAC."),
    ("2016", "Eighty years after the first hut, the new Capanna Monte Bar opens. The 2014 competition had been won, out of thirty entries, by “Barlume” by the architects Oliviero Piffaretti and Carlo Romano: a simple timber building around the hearth as a meeting place, planned with the municipality of Capriasca to benefit the whole region."),
]


# disegno di ogni tappa (chiave = anno come in STORIA): oggetto di storia_oggetti.py e, per uno o due, il movimento
# legato allo scorrimento («ruota», «oscilla»): non di più, se tutto si muove stanca
STORIA_OGGETTI = {
    "1886": ("vetta", None), "1887": ("croce", None), "1911": ("bandiera", None), "1913": ("scarpone", None),
    "1918": ("lanterna", None), "Anni ’30": ("rampone", "ruota"), "1936": ("piccozza", "oscilla"), "1940": ("zaino", None),
    "Anni ’60": ("corda", None), "1980": ("moschettoni", None), "1982": ("tenda", None), "2003": ("capanna", None),
    "2016": ("capanna-moderna", None),
}
# foto storiche al posto del disegno, quando arrivano: anno come in STORIA → (immagine in assets/img/storia/ senza
# .webp, alt in italiano, tedesco, inglese). Es. "1886": ("storia/1886-fondazione", "…", "…", "…")
STORIA_FOTO = {}


def tappa(anno_it, anno, testo):
    """Una tappa della Storia: anno, testo e la foto storica se c'è, altrimenti l'oggetto disegnato."""
    if anno_it in STORIA_FOTO:
        nome, *alt = STORIA_FOTO[anno_it]
        w, h = webp_size(os.path.join(ROOT, "assets", "img", nome + ".webp"))
        figura = f'<figure class="tappa-figura tappa-figura--foto">{img(nome, tr(*alt), w, h)}</figure>'
    elif os.path.exists(os.path.join(ROOT, "assets", "img", "storia", "oggetti", STORIA_OGGETTI[anno_it][0] + ".webp")):
        # immagine dell'oggetto (Nano Banana, sfondo come --surface) al posto del disegno: decorativa come il disegno
        nome = "storia/oggetti/" + STORIA_OGGETTI[anno_it][0]
        w, h = webp_size(os.path.join(ROOT, "assets", "img", nome + ".webp"))
        moto = STORIA_OGGETTI[anno_it][1]
        moto = f' data-moto="{moto}"' if moto else ""
        figura = f'<div class="tappa-figura tappa-figura--oggetto"{moto}>{img(nome, "", w, h)}</div>'
    else:
        figura = f'<div class="tappa-figura">{oggetto(*STORIA_OGGETTI[anno_it])}</div>'
    lungo = " tappa-anno--lungo" if len(anno) > 4 else ""
    return f"""<li class="tappa" data-reveal>
<span class="tappa-nodo" aria-hidden="true"></span>
<div class="tappa-testo"><h3 class="tappa-anno{lungo}">{anno}</h3><p>{testo}</p></div>
{figura}
</li>"""


def storia():
    tl = "\n".join(tappa(a_it, a, t) for (a_it, _), (a, t) in zip(STORIA, tr(STORIA, STORIA_DE, STORIA_EN)))
    if de():
        body = page_hero([("Die Sektion", "de/introduzione.html"), ("Geschichte", None)], "Seit 1886<br>zu Fuss unterwegs.",
                         "Mehr als ein Jahrhundert Besteigungen, Hütten, Rettung und Bergkultur: die Geschichte der Sektion in Etappen.")
    elif en():
        body = page_hero([("The Section", "en/introduzione.html"), ("History", None)], "Since 1886,<br>on foot.",
                         "More than a century of climbs, huts, rescue and mountain culture: the history of the section in milestones.")
    else:
        body = page_hero([("La Sezione", "introduzione.html"), ("Storia", None)], "Dal 1886,<br>a piedi.",
                         "Più di un secolo di salite, rifugi, soccorso e cultura alpina: la storia della sezione in tappe.")
    body += f"""

<figure class="band">
{pic("paesaggi/capanna-tencia", tr("La Capanna Campo Tencia all’alba, con la bandiera svizzera e le montagne in controluce", "Die Campo-Tencia-Hütte bei Sonnenaufgang, mit Schweizer Fahne und Bergen im Gegenlicht", "Campo Tencia hut at sunrise, with the Swiss flag and backlit mountains"), mobile="paesaggi/capanna-tencia-4x3", w=2000, h=658, lazy=False)}
</figure>

<section class="section" aria-labelledby="tappe-h">
<div class="container">
<div class="section-head">
<h2 id="tappe-h" class="h2">{tr("Le tappe", "Die Etappen", "Milestones")}</h2>
<p class="lead">{tr("Accanto all’attività sul terreno, la sezione ha sempre organizzato proiezioni, conferenze e dibattiti, e documentato la propria vita in numerose pubblicazioni e negli annuari.", "Neben den Touren hat die Sektion immer Vorführungen, Vorträge und Diskussionen organisiert und ihr Leben in zahlreichen Publikationen und in den Jahrbüchern festgehalten.", "Alongside its activity in the mountains, the section has always organised slide shows, talks and debates, and recorded its life in many publications and in its yearbooks.")}</p>
</div>
<ol class="tappe">
{tl}
</ol>
</div>
</section>

{subnav(tr("La Sezione", "Die Sektion", "The Section"), L("storia.html"))}"""
    if de():
        return sezione_page("storia.html", "Geschichte | CAS Ticino",
                            "Die Geschichte der Sektion Ticino des Schweizer Alpen-Clubs seit 1886: Gründung, Bergrettung, Expeditionen, Jugend- und Seniorengruppen, Hütten.", body)
    if en():
        return sezione_page("storia.html", "History | CAS Ticino",
                            "The history of the Ticino Section of the Swiss Alpine Club since 1886: foundation, mountain rescue, expeditions, youth and seniors groups, huts.", body)
    return page("storia.html", "Storia | CAS Ticino",
                "La storia della Sezione Ticino del Club Alpino Svizzero dal 1886: fondazione, soccorso alpino, spedizioni, gruppi giovani e seniori, capanne.",
                body)


def linkgroups(groups, tag):
    out = []
    for title, links in groups:
        items = "\n".join(f'<a href="{h}"><span>{l}</span><span class="tag" aria-hidden="true">{tag}</span></a>' for l, h in links)
        out.append(f"""<div class="linkgroup">
<h2 class="h3">{title}</h2>
<div class="linklist">
{items}
</div>
</div>""")
    return '<div class="linkgroups" data-reveal>\n' + "\n".join(out) + "\n</div>"


LINKS = [
    ("Capigita", [("Portale DropTour", "https://ssl.dropnet.ch/casticino/manager/touren/index.php"),
                  ("Reset password", "https://ssl.dropnet.ch/casticino/gite/index.php?page=order_password")]),
    ("Meteo e neve", [("SLF, bollettini valanghe in Svizzera", "https://www.slf.ch/"), ("MeteoSvizzera", "https://www.meteosvizzera.ch/"),
                      ("Meteoblue, previsioni a 7 giorni", "https://www.meteoblue.com/"),
                      ("Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)", "https://lawinen.report/"), ("Servizio valanghe italiano (CAI-SVI)", "https://www.cai-svi.it/j15/"),
                      ("Météo-France, meteo e valanghe", "https://meteofrance.com/meteo-montagne")]),
    ("Condizioni e resoconti", [("Hikr", "https://www.hikr.org/"), ("On-ice, nord Italia", "http://www.on-ice.it/"),
                                ("OHM Chamonix, Monte Bianco", "https://www.ohm-chamonix.com/"), ("Camptocamp", "https://www.camptocamp.org/"),
                                ("Montagne in Valle d’Aosta", "https://www.montagneinvalledaosta.com/"), ("MonteRosa4000", "https://www.monterosa4000.it/"),
                                ("ViaFerrata.org", "https://www.viaferrata.org/")]),
    ("Mappe e guide", [("MapPlus", "https://www.mapplus.ch/"), ("swisstopo", "https://www.swisstopo.ch/"),
                       ("Piz Bube, guide e cartine", "https://www.pizbube.ch/"), ("Edizioni CAS (SAC-Verlag)", "https://www.sac-verlag.ch/")]),
    ("Società alpinistiche ticinesi", [("CAS Bellinzona e valli", "https://www.casbellinzona.ch/"), ("CAS Locarno", "https://www.cas-locarno.ch/"),
                                       ("Federazione Alpinistica Ticinese", "https://www.fat-ti.ch/"), ("Società Escursionistica Verzaschese", "https://www.sev-verzasca.ch/"),
                                       ("Gruppo Scoiattoli Denti della Vecchia", "https://www.scoiattoli.ch/")]),
    ("Formazione", [("CAS Centrale", "https://www.sac-cas.ch/"), ("Gioventù+Sport", "https://www.jugendundsport.ch/"),
                    ("Ufficio cantonale G+S", "https://www4.ti.ch/decs/sa/us/ufficio")]),
    ("Capanne, guide e soccorso", [("Capanne CAS in Svizzera", "https://www.sac-cas.ch/huetten.html"), ("Capanneti, rifugi Ticino e Mesolcina", "https://www.capanneti.ch/"),
                                   ("Gruppo Guide Alpine Ticino", "https://www.guidealpineticino.ch/"), ("Soccorso Alpino Svizzero", "https://www.alpinerettung.ch/")]),
    ("Eventi e altre società", [("Skyrace Lodrino Lavertezzo", "https://www.lodrino-lavertezzo.ch/"),
                                ("Sci Club Lodrino-Prosito", "https://www.sclp.ch/"), ("PicAlciot, vie d’arrampicata in Ticino", "https://www.picalciot.ch/")]),
    ("News di montagna", [("PlanetMountain", "https://www.planetmountain.com/"), ("Montagna.tv", "https://www.montagna.tv/")]),
]


LINKS_DE = {"Capigita": "Tourenleiter", "Meteo e neve": "Wetter und Schnee", "Condizioni e resoconti": "Verhältnisse und Tourenberichte",
            "Mappe e guide": "Karten und Führer", "Società alpinistiche ticinesi": "Tessiner Bergsteigervereine", "Formazione": "Ausbildung",
            "Capanne, guide e soccorso": "Hütten, Bergführer und Rettung", "Eventi e altre società": "Anlässe und andere Vereine",
            "News di montagna": "Bergnews",
            "SLF, bollettini valanghe in Svizzera": "SLF, Lawinenbulletin Schweiz", "MeteoSvizzera": "MeteoSchweiz",
            "Meteoblue, previsioni a 7 giorni": "Meteoblue, 7-Tage-Prognose", "Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)": "Lawinenbulletin Euregio (Tirol, Südtirol, Trentino)",
            "Servizio valanghe italiano (CAI-SVI)": "Italienischer Lawinendienst (CAI-SVI)", "Météo-France, meteo e valanghe": "Météo-France, Wetter und Lawinen",
            "On-ice, nord Italia": "On-ice, Norditalien", "OHM Chamonix, Monte Bianco": "OHM Chamonix, Mont Blanc",
            "Montagne in Valle d’Aosta": "Berge im Aostatal", "Piz Bube, guide e cartine": "Piz Bube, Führer und Karten",
            "Edizioni CAS (SAC-Verlag)": "SAC-Verlag", "Federazione Alpinistica Ticinese": "Tessiner Bergsteigerverband (FAT)",
            "CAS Centrale": "SAC Zentralverband", "Gioventù+Sport": "Jugend+Sport", "Ufficio cantonale G+S": "Kantonales J+S-Amt",
            "Capanne CAS in Svizzera": "SAC-Hütten in der Schweiz", "Capanneti, rifugi Ticino e Mesolcina": "Capanneti, Hütten im Tessin und Misox",
            "Gruppo Guide Alpine Ticino": "Tessiner Bergführer", "Soccorso Alpino Svizzero": "Alpine Rettung Schweiz",
            "PicAlciot, vie d’arrampicata in Ticino": "PicAlciot, Kletterrouten im Tessin", "Portale DropTour": "DropTour-Portal",
            "Reset password": "Passwort zurücksetzen"}


LINKS_EN = {"Capigita": "Trip leaders", "Meteo e neve": "Weather and snow", "Condizioni e resoconti": "Conditions and trip reports",
            "Mappe e guide": "Maps and guidebooks", "Società alpinistiche ticinesi": "Ticino mountaineering clubs", "Formazione": "Training",
            "Capanne, guide e soccorso": "Huts, guides and rescue", "Eventi e altre società": "Events and other clubs",
            "News di montagna": "Mountain news",
            "SLF, bollettini valanghe in Svizzera": "SLF, Swiss avalanche bulletin", "MeteoSvizzera": "MeteoSwiss",
            "Meteoblue, previsioni a 7 giorni": "Meteoblue, 7-day forecast", "Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)": "Euregio avalanche bulletin (Tyrol, South Tyrol, Trentino)",
            "Servizio valanghe italiano (CAI-SVI)": "Italian avalanche service (CAI-SVI)", "Météo-France, meteo e valanghe": "Météo-France, weather and avalanches",
            "On-ice, nord Italia": "On-ice, northern Italy", "OHM Chamonix, Monte Bianco": "OHM Chamonix, Mont Blanc",
            "Montagne in Valle d’Aosta": "Mountains in the Aosta Valley", "Piz Bube, guide e cartine": "Piz Bube, guidebooks and maps",
            "Edizioni CAS (SAC-Verlag)": "SAC publishing (SAC-Verlag)", "Federazione Alpinistica Ticinese": "Ticino Mountaineering Federation (FAT)",
            "CAS Centrale": "SAC central association", "Gioventù+Sport": "Youth+Sport", "Ufficio cantonale G+S": "Cantonal Youth+Sport office",
            "Capanne CAS in Svizzera": "SAC huts in Switzerland", "Capanneti, rifugi Ticino e Mesolcina": "Capanneti, huts in Ticino and Mesolcina",
            "Gruppo Guide Alpine Ticino": "Ticino mountain guides", "Soccorso Alpino Svizzero": "Swiss Alpine Rescue",
            "PicAlciot, vie d’arrampicata in Ticino": "PicAlciot, climbing routes in Ticino", "Portale DropTour": "DropTour portal",
            "Reset password": "Reset password"}


def link():
    if de():
        gruppi = [(LINKS_DE.get(g, g), [(LINKS_DE.get(n, n), u) for n, u in links]) for g, links in LINKS]
        hero = page_hero([("Dienste", "de/noleggio.html"), ("Nützliche Links", None)], "Nützliche Links",
                         "Wetter, Lawinenbulletins, Verhältnisse, Karten und die anderen Bergsteigervereine der Region.")
    elif en():
        gruppi = [(LINKS_EN.get(g, g), [(LINKS_EN.get(n, n), u) for n, u in links]) for g, links in LINKS]
        hero = page_hero([("Services", "en/noleggio.html"), ("Useful links", None)], "Useful links",
                         "Weather, avalanche bulletins, conditions, maps and the other mountaineering clubs in the region.")
    else:
        gruppi = LINKS
        hero = page_hero([("Servizi", "noleggio.html"), ("Link utili", None)], "Link utili",
                         "Meteo, bollettini valanghe, condizioni, cartine e le altre realtà alpinistiche del territorio.")
    body = hero + f"""

<section class="section" aria-label="Link">
<div class="container">
{linkgroups(gruppi, "↗")}
</div>
</section>

{subnav(SERVIZI_MENU(), L("link.html"))}"""
    if de():
        return sezione_page("link.html", "Nützliche Links | CAS Ticino",
                            "Nützliche Links für die Berge: Wetter und Lawinenbulletins, Verhältnisse, Karten, Tessiner Bergsteigervereine, Ausbildung und Rettung.", body)
    if en():
        return sezione_page("link.html", "Useful links | CAS Ticino",
                            "Useful links for the mountains: weather and avalanche bulletins, conditions, maps, Ticino mountaineering clubs, training and rescue.", body)
    return page("link.html", "Link utili | CAS Ticino",
                "Link utili per la montagna: meteo e bollettini valanghe, condizioni, cartine, società alpinistiche ticinesi, formazione e soccorso.",
                body)


DOC = "docs/"  # PDF della sezione, in sottocartelle per tema (nomi in minuscolo, con trattini)
DOCS = [
    ("La sezione", [("Statuto", DOC + "statuto-visione/statuto-2025.pdf"),
                    ("Visione e strategia", DOC + "statuto-visione/visione-strategia-2025.pdf"),
                    ("Organigramma", DOC + "statuto-visione/organigramma-2025.pdf"),
                    ("Regolamento gite", DOC + "statuto-visione/regolamento-gite-2026.pdf")]),
    ("Scale di difficoltà", [("Arrampicata sportiva", DOC + "scale-difficolta/arrampicata-sportiva.pdf"),
                             ("Alpinismo", DOC + "scale-difficolta/alpinismo.pdf"),
                             ("Arrampicata artificiale", DOC + "scale-difficolta/arrampicata-artificiale.pdf"),
                             ("Escursionismo e trekking", DOC + "scale-difficolta/escursionismo-trekking.pdf"),
                             ("Racchette", DOC + "scale-difficolta/racchette.pdf"),
                             ("Sci alpinismo", DOC + "scale-difficolta/sci-alpinismo.pdf"),
                             ("Vie ferrate", DOC + "scale-difficolta/vie-ferrate.pdf")]),
    ("Promemoria", [("Meteo", DOC + "promemoria/meteo.pdf"),
                    ("Orientamento", DOC + "promemoria/orientamento.pdf"),
                    ("Scalata su ghiaccio", DOC + "promemoria/scalata-su-ghiaccio.pdf"),
                    ("Tecnica alpina", DOC + "promemoria/tecnica-alpina.pdf"),
                    ("Incidente valanga e ARVA", DOC + "promemoria/incidente-valanga-arva.pdf"),
                    ("Promemoria capigita", DOC + "promemoria/capigita.pdf"),
                    ("Istruzioni DropTour", DOC + "promemoria/istruzioni-droptour-2026.pdf")]),
    ("Pianificazione", [("Formulario pianificazione gite estive", DOC + "moduli/pianificazione-gite-estive.pdf"),
                        ("Cartine CH 1:25 000", DOC + "cartine/carte-nazionali-25000.pdf"),
                        ("Cartine CH 1:50 000", DOC + "cartine/carte-nazionali-50000.pdf"),
                        ("Cartine CH 1:50 000 sci", DOC + "cartine/carte-nazionali-50000-sci.pdf")]),
]


# nomi di gruppi e documenti nelle altre lingue (i PDF restano in italiano)
DOCS_DE = {"La sezione": "Die Sektion", "Statuto": "Statuten", "Visione e strategia": "Vision und Strategie", "Organigramma": "Organigramm",
           "Regolamento gite": "Tourenreglement", "Scale di difficoltà": "Schwierigkeitsskalen", "Arrampicata sportiva": "Sportklettern",
           "Alpinismo": "Hochtouren", "Arrampicata artificiale": "Technisches Klettern", "Escursionismo e trekking": "Wandern und Trekking",
           "Racchette": "Schneeschuhtouren", "Sci alpinismo": "Skitouren", "Vie ferrate": "Klettersteige", "Promemoria": "Merkblätter",
           "Meteo": "Wetter", "Orientamento": "Orientierung", "Scalata su ghiaccio": "Eisklettern", "Tecnica alpina": "Alpine Technik",
           "Incidente valanga e ARVA": "Lawinenunfall und LVS", "Promemoria capigita": "Merkblatt für Tourenleitende",
           "Istruzioni DropTour": "DropTour-Anleitung", "Pianificazione": "Planung",
           "Formulario pianificazione gite estive": "Planungsformular Sommertouren", "Cartine CH 1:25 000": "Landeskarten 1:25 000",
           "Cartine CH 1:50 000": "Landeskarten 1:50 000", "Cartine CH 1:50 000 sci": "Skitourenkarten 1:50 000",
           "Obiettivi corsi": "Kursziele", "Equipaggiamento": "Ausrüstung", "Arrampicata": "Klettern",
           "Tecnica di sci fuori pista": "Off-Piste-Skitechnik"}
DOCS_EN = {"La sezione": "The Section", "Statuto": "Statutes", "Visione e strategia": "Vision and strategy", "Organigramma": "Organisation chart",
           "Regolamento gite": "Trip regulations", "Scale di difficoltà": "Difficulty scales", "Arrampicata sportiva": "Sport climbing",
           "Alpinismo": "Mountaineering", "Arrampicata artificiale": "Aid climbing", "Escursionismo e trekking": "Hiking and trekking",
           "Racchette": "Snowshoeing", "Sci alpinismo": "Ski touring", "Vie ferrate": "Via ferratas", "Promemoria": "Fact sheets",
           "Meteo": "Weather", "Orientamento": "Navigation", "Scalata su ghiaccio": "Ice climbing", "Tecnica alpina": "Alpine technique",
           "Incidente valanga e ARVA": "Avalanche accident and transceiver", "Promemoria capigita": "Trip leader checklist",
           "Istruzioni DropTour": "DropTour instructions", "Pianificazione": "Planning",
           "Formulario pianificazione gite estive": "Summer trip planning form", "Cartine CH 1:25 000": "Swiss maps 1:25,000",
           "Cartine CH 1:50 000": "Swiss maps 1:50,000", "Cartine CH 1:50 000 sci": "Swiss ski touring maps 1:50,000",
           "Obiettivi corsi": "Course objectives", "Equipaggiamento": "Equipment", "Arrampicata": "Climbing",
           "Tecnica di sci fuori pista": "Off-piste ski technique"}


def SERVIZI_MENU():
    """Nome della voce Servizi nella lingua corrente (per percorso e sotto-menu)."""
    return tr("Servizi", "Dienste", "Services")


def servizi_crumb():
    return (SERVIZI_MENU(), L("noleggio.html"))


def documenti():
    nomi = {"it": {}, "de": DOCS_DE, "en": DOCS_EN}[LINGUA["lang"]]
    gruppi = [(nomi.get(g, g), [(nomi.get(n, n), u) for n, u in docs]) for g, docs in DOCS]
    titolo = tr("Documenti", "Dokumente", "Documents")
    body = page_hero([servizi_crumb(), (titolo, None)], titolo, tr(
        "Statuto e documenti della sezione, scale di difficoltà, promemoria tecnici, documenti dei corsi, moduli e cartine da scaricare.",
        "Statuten und Dokumente der Sektion, Schwierigkeitsskalen, technische Merkblätter, Formulare und Karten zum Herunterladen. Die Dokumente sind auf Italienisch.",
        "The section’s statutes and documents, difficulty scales, technical fact sheets, forms and maps to download. The documents are in Italian.")) + f"""

<section class="section" aria-label="{titolo}">
<div class="container">
{linkgroups(gruppi, "PDF")}
<div class="callout">
<p>{tr("<strong>Annuari e Informazione</strong>, il bollettino della sezione, hanno una pagina propria.",
       "<strong>Jahrbücher und «Informazione»</strong>, das Mitteilungsblatt der Sektion, haben eine eigene Seite (italienisch).",
       "<strong>Yearbooks and «Informazione»</strong>, the section’s bulletin, have their own page (in Italian).")}</p>
<div class="actions"><a class="btn btn--secondary" href="annuari.html">{tr("Annuari", "Jahrbücher", "Yearbooks")}</a><a class="btn btn--secondary" href="informazione.html">Informazione</a></div>
</div>
</div>
</section>

{subnav(SERVIZI_MENU(), L("documenti.html"))}"""
    return sezione_page("documenti.html", tr("Documenti", "Dokumente", "Documents") + " | CAS Ticino", tr(
        "Documenti del CAS Ticino da scaricare: scale di difficoltà, promemoria tecnici, promemoria capigita, obiettivi ed equipaggiamento dei corsi, pianificazione e cartine.",
        "Dokumente der SAC-Sektion Ticino zum Herunterladen (italienisch): Statuten, Tourenreglement, Schwierigkeitsskalen, Merkblätter, Formulare und Karten.",
        "Documents of the SAC Ticino Section to download (in Italian): statutes, trip regulations, difficulty scales, fact sheets, forms and maps."), body)


# ------------------------------------------------------------------ news, foto, adesione

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
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]


def data_it(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MESI[m - 1]} {y}"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


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


# ------------------------------------------------------------------ programma gite (copia da Droptour)
# data/gite.json lo scrive scripts/update_gite.py; nella pagina assets/gite.js rilegge le gite in tempo reale
# dall'interfaccia pubblica di Droptour e le ridisegna con lo stesso markup di gita_html() (tenerli allineati).
GITE_ICS = "webcal://ssl.dropnet.ch/casticino/dropnetapps/tours/index.php?page=ics&amp;type=&amp;group=&amp;eventtype="
GITE_DETTAGLIO = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItem&language=it&item_id="
GITE_API = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItems&limit=500&language=it"
GIORNI_BREVI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
MESI_BREVI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
IMPEGNO = {"A": "poco impegnativo", "B": "abbastanza impegnativo", "C": "impegnativo", "D": "molto impegnativo"}
# Programma gite anche in de/ e en/: si traducono solo i testi della pagina; titoli, tipi e dettagli delle gite
# (da Droptour) restano in italiano. Gli stessi testi sono in assets/gite.js (TESTI): tenerli allineati.
GIORNI_BREVI_L = {"it": GIORNI_BREVI, "de": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
                  "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
MESI_BREVI_L = {"it": MESI_BREVI, "de": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
                "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
MESI_L = {"it": MESI, "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
          "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]}
IMPEGNO_L = {"it": IMPEGNO, "de": {"A": "wenig anspruchsvoll", "B": "ziemlich anspruchsvoll", "C": "anspruchsvoll", "D": "sehr anspruchsvoll"},
             "en": {"A": "easy", "B": "fairly demanding", "C": "demanding", "D": "very demanding"}}
GRUPPI_L = {"de": {"Tutti": "Alle", "Attivi": "Aktive", "Giovani": "Jugend", "Seniori": "Senioren", "Soccorso": "Bergrettung", "Monitori": "Leitende"},
            "en": {"Tutti": "All", "Attivi": "Active members", "Giovani": "Youth", "Seniori": "Seniors", "Soccorso": "Mountain rescue", "Monitori": "Instructors"}}


# tipi di gita (category di Droptour, sempre in italiano) per codice; un codice nuovo resta in italiano.
# Tenere allineato con TIPI in assets/gite.js
TIPI_GITA_L = {"de": {"ALP": "Hochtour", "ARR": "Klettern", "COR": "Ausbildungskurs", "CUL": "Kultur", "ESC": "Wandern", "EVE": "Anlass",
                      "FER": "Klettersteig", "MTB": "Mountainbike", "RAC": "Schneeschuhtour", "SA": "Skitour", "SOC": "Bergrettung"},
               "en": {"ALP": "Mountaineering", "ARR": "Climbing", "COR": "Training course", "CUL": "Culture", "ESC": "Hiking", "EVE": "Event",
                      "FER": "Via ferrata", "MTB": "Mountain biking", "RAC": "Snowshoeing", "SA": "Ski touring", "SOC": "Mountain rescue"}}


def nome_tipo(g):
    return TIPI_GITA_L.get(LINGUA["lang"], {}).get(g.get("sigla"), g["tipo"])


def nome_gruppo(x):
    return GRUPPI_L.get(LINGUA["lang"], {}).get(x, x)


def gite_dati():
    try:
        return json.load(open(os.path.join(ROOT, "data", "gite.json"), encoding="utf-8")).get("gite", [])
    except OSError:
        return []


def gita_stato(g, oggi):
    """(classe, testo) dello stato delle iscrizioni, calcolato come in gite.js."""
    if g["stato"] == "annullata":
        return "annullata", tr("Annullata", "Abgesagt", "Cancelled")
    if g["stato"] == "completa":
        return "completa", tr("Completa", "Ausgebucht", "Full")
    if not g["iscrizione"]:
        return "", tr("Senza iscrizione online", "Ohne Online-Anmeldung", "No online registration")
    if g["iscrizione_dal"] and oggi < g["iscrizione_dal"]:
        b = data_breve(g["iscrizione_dal"])
        return "", tr(f"Iscrizioni dal {b}", f"Anmeldung ab {b}", f"Registration from {b}")
    if g["iscrizione_al"] and oggi > g["iscrizione_al"]:
        return "", tr("Iscrizioni chiuse", "Anmeldung geschlossen", "Registration closed")
    return "aperte", tr("Iscrizioni aperte", "Anmeldung offen", "Registration open")


def fino_al(giorno):
    """«fino al 3», ma «fino all'1», «all'8», «all'11»."""
    return f"fino all’{giorno}" if giorno in (1, 8, 11) else f"fino al {giorno}"


def data_breve(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    mb = MESI_BREVI_L[LINGUA["lang"]][m - 1]
    return tr(f"{d} {mb}", f"{d}. {mb}", f"{d} {mb}")


def fino_data(d2):
    """Ultimo giorno di una gita che finisce il mese dopo: «fino all’1 nov», «bis 1. Nov.», «to 1 Nov»."""
    mb = MESI_BREVI_L[LINGUA["lang"]][d2.month - 1]
    return tr(f"{fino_al(d2.day)} {mb}", f"bis {d2.day}. {mb}", f"to {d2.day} {mb}")


def gita_html(g, oggi):
    import datetime
    gb = GIORNI_BREVI_L[LINGUA["lang"]]
    d1 = datetime.date.fromisoformat(g["dal"])
    giorno, sotto = str(d1.day), gb[d1.weekday()]
    if g["al"] and g["al"] != g["dal"]:
        d2 = datetime.date.fromisoformat(g["al"])
        if d2.month == d1.month:
            giorno, sotto = f"{d1.day}–{d2.day}", f"{sotto}–{gb[d2.weekday()]}"
        else:
            sotto += f", {fino_data(d2)}"
    classe, stato = gita_stato(g, oggi)
    gruppi = [nome_gruppo(x) for x in g["gruppi"] if x != "Tutti"] or [nome_gruppo("Tutti")]
    tipo = " · ".join(dict.fromkeys(filter(None, [esc(nome_tipo(g)), esc(", ".join(gruppi))])))
    meta = []
    if g["cond"]:
        meta.append(f'<span title="{IMPEGNO_L[LINGUA["lang"]].get(g["cond"], "")}">{tr("Impegno", "Kondition", "Fitness")} {esc(g["cond"])}</span>')
    if g["tecn"]:
        meta.append(f'<span>{tr("Difficoltà", "Technik", "Difficulty")} {esc(g["tecn"])}</span>')
    if g["capigita"]:
        piu = len(g["capigita"]) > 1
        meta.append(f'<span>{tr("Capigita" if piu else "Capogita", "Leitung", "Leaders" if piu else "Leader")}: {esc(", ".join(g["capigita"]))}</span>')
    iscritti = tr("iscritti", "Angemeldete", "registered")
    posti = (f'{g["iscritti"]}/{g["posti"]} {iscritti}' if g["posti"] else f'{g["iscritti"]} {iscritti}' if g["iscritti"] else "")
    modalita = (f'<span class="gita-nota">{tr("Iscrizione" + ("" if g["modalita"].startswith("tramite") else ":"), "Anmeldung:", "Registration:")} {esc(g["modalita"])}</span>'
                if g["modalita"] and classe != "annullata" else "")
    dettagli = (tr("Dettagli", "Details", "Details") if classe == "annullata" or not g["iscrizione"]
                else tr("Dettagli e iscrizione", "Details und Anmeldung", "Details and registration"))
    link = L("gita.html") + f"?id={g['id']}"
    return f"""<article class="gita{' gita--annullata' if classe == 'annullata' else ''}" id="gita-{g['id']}" data-fine="{g['al'] or g['dal']}" data-gruppi="{esc(' '.join(g['gruppi']))}" data-tipo="{esc(g['sigla'])}">
<p class="gita-data"><span class="gita-giorno num">{giorno}</span><span class="gita-sotto">{sotto}</span></p>
<div class="gita-corpo">
<p class="gita-tipo">{tipo}</p>
<h3 class="gita-titolo"><a href="{link}"{'' if LINGUA["lang"] == "it" else ' lang="it"'}>{esc(g['titolo'])}</a></h3>
{f'<p class="gita-meta">{"".join(meta)}</p>' if meta else ""}
</div>
<div class="gita-stato">
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
{f'<span class="gita-posti num">{posti}</span>' if posti else ""}{modalita}
<a class="link gita-link" href="{link}">{dettagli}<span class="visually-hidden">: <span{'' if LINGUA["lang"] == "it" else ' lang="it"'}>{esc(g['titolo'])}</span></span></a>
</div>
</article>"""


def gite_lista(gite, oggi):
    """Gite raggruppate per mese (ogni mese è una sezione con titolo, nascosta da gite.js se il filtro la svuota)."""
    out, mese = [], None
    for g in gite:
        m = g["dal"][:7]
        if m != mese:
            if mese:
                out.append("</div>\n</section>")
            y, mm = (int(x) for x in m.split("-"))
            out.append(f'<section class="gite-mese" aria-labelledby="mese-{m}">\n<h2 id="mese-{m}" class="h3">{MESI_L[LINGUA["lang"]][mm - 1].capitalize()} {y}</h2>\n<div class="gite-righe">')
            mese = m
        out.append(gita_html(g, oggi))
    if mese:
        out.append("</div>\n</section>")
    return "\n".join(out)



def prossime_gite(n=10):
    """Le prossime gite per la home, in una fila che scorre: senza annullate e senza le serate della colonna di soccorso.
    La pagina può restare indietro di un giorno (si rigenera ogni mattina), quindi site.js toglie quelle già passate (data-fine)."""
    import datetime
    lang = LINGUA["lang"]
    oggi = datetime.date.today().isoformat()
    scelte = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi and g["stato"] != "annullata"
              and "colonna di soccorso" not in g["titolo"].lower()][:n]
    schede = []
    for g in scelte:
        d = datetime.date.fromisoformat(g["dal"])
        quando = f"{GIORNI_BREVI_L[lang][d.weekday()]} {MESI_L[lang][d.month - 1]}"
        if g["al"] and g["al"] != g["dal"]:
            d2 = datetime.date.fromisoformat(g["al"])
            quando += ", " + (fino_data(d2) if d2.month != d.month else tr(fino_al(d2.day), f"bis {d2.day}.", f"to {d2.day}"))
        classe, stato = gita_stato(g, oggi)
        gruppi = [nome_gruppo(x) for x in g["gruppi"] if x != "Tutti"] or [nome_gruppo("Tutti")]
        tipo = " · ".join(dict.fromkeys(filter(None, [esc(nome_tipo(g)), esc(", ".join(gruppi))])))
        schede.append(f"""<a class="prossima" href="gita.html?id={g['id']}" data-fine="{g['al'] or g['dal']}">
<p class="prossima-data"><span class="prossima-giorno num">{d.day}</span><span>{quando}</span></p>
<p class="gita-tipo">{tipo}</p>
<h3 class="prossima-titolo"{in_it()}>{esc(g['titolo'])}</h3>
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
</a>""")
    return "\n".join(schede)


def gite():
    import datetime
    oggi = datetime.date.today().isoformat()
    lista = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi]
    it = LINGUA["lang"] == "it"
    nome = L("gite.html")
    su = "" if it else "../"  # data-copia non passa da pubblica()
    titolo = tr("Programma gite", "Tourenprogramm", "Trip programme")
    trail = [("Attività", "index.html#attivita"), (titolo, None)] if it else [(titolo, None)]
    body = page_hero(trail, titolo, tr(
        "Gite, corsi ed eventi della sezione, aggiornati in tempo reale dal portale Droptour, dove ci si iscrive.",
        "Touren, Kurse und Anlässe der Sektion, laufend aktualisiert aus dem Portal Droptour, wo man sich anmeldet. Titel und Beschreibungen der Touren sind auf Italienisch.",
        "Trips, courses and events of the section, updated live from the Droptour portal, where you register. Trip titles and descriptions are in Italian.")) + f"""

<section class="section" aria-label="{tr("Elenco delle gite", "Liste der Touren", "List of trips")}">
<div class="container">
<div class="gite-filtri" id="gite-filtri" hidden>
<div class="filtro" role="group" aria-label="{tr("Filtra per gruppo", "Nach Gruppe filtern", "Filter by group")}" data-campo="gruppi"></div>
<div class="filtro" role="group" aria-label="{tr("Filtra per tipo", "Nach Art filtern", "Filter by type")}" data-campo="tipo"></div>
<div class="filtri-tendina">
<label><span class="label">{tr("Gruppo", "Gruppe", "Group")}</span><select data-campo="gruppi"></select></label>
<label><span class="label">{tr("Tipo", "Art", "Type")}</span><select data-campo="tipo"></select></label>
</div>
</div>
<p class="small filtro-stato" id="gite-stato" aria-live="polite"></p>
<div class="gite" id="gite" data-api="{GITE_API}" data-copia="{su}{asset('data/gite.json')}">
{gite_lista(lista, oggi) if lista else '<p>' + tr("Il programma non è disponibile in questo momento: lo trovi su", "Das Programm ist im Moment nicht verfügbar: Sie finden es auf", "The programme is not available at the moment: you can find it on") + ' <a href="' + GITE_DROPTOUR + '">Droptour</a>.</p>'}
</div>
<div class="callout">
<p>{tr("Le iscrizioni, l’accesso per soci e capigita e i dettagli di ogni gita sono sul portale Droptour. Per le domande su una gita scrivi al capogita, dalla pagina della gita.",
       "Anmeldungen, Zugang für Mitglieder und Tourenleitende und alle Details zu jeder Tour finden Sie auf dem Portal Droptour (italienisch). Fragen zu einer Tour richten Sie an die Tourenleitung, über die Seite der Tour.",
       "Registration, access for members and trip leaders and the details of every trip are on the Droptour portal (in Italian). For questions about a trip, write to the trip leader from the trip’s page.")}</p>
<div class="actions"><a class="btn btn--secondary" href="{GITE_DROPTOUR}" rel="noopener">{tr("Programma completo su Droptour", "Ganzes Programm auf Droptour", "Full programme on Droptour")}</a><a class="btn btn--secondary" href="{GITE_ICS}">{tr("Calendario (iCal)", "Kalender (iCal)", "Calendar (iCal)")}</a>{'<a class="btn btn--secondary" href="partecipare.html">Come partecipare</a>' if it else ""}<a class="btn btn--secondary" href="documenti.html">{tr("Scale di difficoltà", "Schwierigkeitsskalen (italienisch)", "Difficulty scales (in Italian)")}</a></div>
</div>
</div>
</section>

{prima_di_partire()}
{subnav("Attività", "gite.html") if it else ""}"""
    return pubblica(nome, page(nome, f"{titolo} | CAS Ticino", tr(
        "Il programma delle gite, dei corsi e degli eventi della Sezione Ticino del Club Alpino Svizzero, con le iscrizioni su Droptour.",
        "Das Programm der Touren, Kurse und Anlässe der Sektion Ticino des Schweizer Alpen-Clubs, mit Anmeldung auf Droptour.",
        "The programme of trips, courses and events of the Ticino Section of the Swiss Alpine Club, with registration on Droptour."),
        body, og="attivita/gite-2x1", section="Attività" if it else None, scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n'))


def gita_pagina():
    """Dettaglio di una gita: gita.html?id=<numero Droptour>, riempita da gite.js (dati in tempo reale da Droptour)."""
    it = LINGUA["lang"] == "it"
    nome = L("gita.html")
    su = "" if it else "../"
    programma = tr("Programma gite", "Tourenprogramm", "Trip programme")
    gita = tr("Gita", "Tour", "Trip")
    trail = ([("Attività", "index.html#attivita")] if it else []) + [(programma, L("gite.html")), (gita, None)]
    body = page_hero(trail, gita, tr("Caricamento della gita…", "Tour wird geladen…", "Loading the trip…")
                     ).replace('class="display fit"', 'class="display display--gita fit"') + f"""

<section class="section" aria-label="{tr("Dettagli della gita", "Details der Tour", "Trip details")}">
<div class="container detail gita-dettaglio" id="gita" data-api="{GITE_API}" data-dettaglio="{GITE_DETTAGLIO}"
 data-droptour="{GITE_DROPTOUR}" data-copia="{su}{asset('data/gite.json')}" data-programma="{L('gite.html')}">
<aside class="gita-riepilogo" aria-label="{tr("La gita in breve", "Die Tour in Kürze", "The trip at a glance")}" hidden>
<p id="gita-stato"></p>
<dl class="gita-chiave" id="gita-chiave"></dl>
<div class="actions" id="gita-azioni"></div>
</aside>
<div id="gita-dati"><noscript><p>{tr("Per vedere la gita serve JavaScript: la trovi nel", "Um die Tour zu sehen, braucht es JavaScript; Sie finden sie im", "JavaScript is needed to see the trip; you can find it in the")} <a href="{GITE_DROPTOUR}">{tr("programma su Droptour", "Programm auf Droptour", "programme on Droptour")}</a>.</p></noscript></div>
</div>
</section>
{subnav("Attività", "gita.html") if it else ""}"""
    return pubblica(nome, page(nome, f"{gita} | CAS Ticino", tr(
        "Dettagli di una gita della Sezione Ticino del CAS, con l’iscrizione su Droptour.",
        "Details einer Tour der Sektion Ticino des SAC, mit Anmeldung auf Droptour.",
        "Details of a trip of the Ticino Section of the SAC, with registration on Droptour."),
        body, og="attivita/gite-2x1", section="Attività" if it else None, scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n'))


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

<section class="section" aria-label="{titolo}">
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

<section class="section" aria-label="Informazione">
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


def adesione():
    prices = [("Singolo", "Socio individuale", "105", "30"),
              ("Famiglia", "Genitori e figli fino a 17 anni", "179", "50"),
              ("Giovane", "Fino a 22 anni", "50", "30")]
    cards = "\n".join(f"""<article class="price">
<h3 class="h3">{t}</h3>
<p>{who}</p>
<div class="amount"><small>CHF</small>{amt}</div>
<p class="small">+ CHF {fee} alla prima iscrizione</p>
</article>""" for t, who, amt, fee in prices)
    rows = [("Capanne", "Fino al 50% di sconto nelle capanne di tutta la Svizzera e in alcuni paesi europei"),
            ("Portale escursionistico", "Accesso gratuito a cartine e itinerari sul portale del CAS"),
            ("Formazione", "Riduzioni sui corsi"),
            ("Pubblicazioni", "La rivista «Le Alpi», il periodico della sezione e sconti sulle edizioni CAS"),
            ("Arrampicata", "Accesso gratuito alla palestra di arrampicata San Paolo"),
            ("Tessera digitale", 'La tessera di socio è anche nell’app SAC-CAS (<a href="https://apps.apple.com/ch/app/sac-cas/id1592646841" rel="noopener">App Store</a>, <a href="https://play.google.com/store/apps/details?id=ch.sac_cas" rel="noopener">Google Play</a>): si accede con l’account del CAS, funziona anche senza rete e il codice QR vale nelle capanne')]
    join = "https://portal.sac-cas.ch/it/groups/6783/self_registration"
    body = page_hero([("Adesione", None)], "Diventa socio",
                     "Entra nella sezione ticinese del Club Alpino Svizzero: gite, corsi, capanne e una comunità che ama la montagna.",
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{join}">Iscriviti sul sito del CAS <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<figure class="band">
{pic("paesaggi/laghetto-alpino", "Laghetto alpino tra le rocce, con le montagne sullo sfondo", mobile="paesaggi/laghetto-alpino-4x3", w=2000, h=1126, lazy=False)}
{credito()}
</figure>

<section class="section" aria-labelledby="quote-h">
<div class="container">
<div class="section-head"><h2 id="quote-h" class="h2">Quote annuali</h2></div>
<div class="prices" data-reveal>
{cards}
</div>
<p class="note">Sei già socio di un’altra sezione CAS? Puoi chiedere la doppia affiliazione e pagare solo la quota della Sezione Ticino.</p>
</div>
</section>

<section class="section--surface" aria-labelledby="vantaggi-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="vantaggi-h" class="h2">Cosa ricevi</h2>
<div><a class="btn btn--primary" href="{join}">Iscriviti sul sito del CAS <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>"""
    return page("adesione.html", "Diventa socio | CAS Ticino",
                "Diventa socio della Sezione Ticino del Club Alpino Svizzero: quote annuali per singoli, famiglie e giovani, e vantaggi per i soci.",
                body, og="paesaggi/laghetto-alpino-2000")


# ------------------------------------------------------------------ attività

def giovani():
    groups = [("2-10", tr("Giovanissimi e famiglie", "Die Jüngsten und Familien", "Youngest and families"),
               tr("Arrampicata in famiglia: i bambini imparano a muoversi in corda, gli adulti ad assicurare.",
                  "Klettern mit der Familie: Die Kinder lernen, sich am Seil zu bewegen, die Erwachsenen das Sichern.",
                  "Family climbing: children learn to move on the rope, adults learn to belay.")),
              ("9-14", "Spider", tr("Arrampicata, nevai, lettura della carta e scoperta della natura, tra gioco, divertimento e spirito di gruppo.",
                                    "Klettern, Schneefelder, Kartenlesen und Naturentdeckung, mit Spiel, Spass und Teamgeist.",
                                    "Climbing, snowfields, map reading and discovering nature, with games, fun and team spirit.")),
              ("13-17", "Junior", tr("D’inverno sci alpinismo e splitboard, d’estate creste e arrampicata: prima il divertimento e la sicurezza, poi l’autonomia.",
                                     "Im Winter Skitouren und Splitboard, im Sommer Grate und Klettern: zuerst Spass und Sicherheit, dann Selbständigkeit.",
                                     "Ski touring and splitboarding in winter, ridges and climbing in summer: fun and safety first, then independence.")),
              ("16-25", "OG", tr("Sci alpinismo impegnativo, cascate di ghiaccio e arrampicata tecnica in tutto l’arco alpino. Chi vuole può formarsi come monitore.",
                                 "Anspruchsvolle Skitouren, Eisfälle und technisches Klettern im ganzen Alpenbogen. Wer will, kann sich zur Leiterin oder zum Leiter ausbilden.",
                                 "Demanding ski touring, ice falls and technical climbing across the Alps. Those who wish can train as instructors."))]
    anni = tr("anni", "Jahre", "years")
    cards = "\n".join(f"""<article class="group">
<div class="age">{a}<span>{anni}</span></div>
<h3 class="h3">{t_}</h3>
<p>{p}</p>
</article>""" for a, t_, p in groups)
    rows = [(tr("Iscrizione", "Anmeldung", "Registration"), tr(
                "Su Droptour, almeno due settimane prima per le singole attività, oppure dal coordinatore per iscrizioni a blocchi.",
                "Auf Droptour, mindestens zwei Wochen im Voraus für einzelne Aktivitäten, oder beim Koordinator für Blockanmeldungen.",
                "On Droptour, at least two weeks in advance for single activities, or through the coordinator for block registrations.")),
            (tr("Requisiti", "Voraussetzungen", "Requirements"), tr(
                'Serve essere soci del CAS Ticino, tranne per le uscite di prova. <a href="adesione.html">Diventa socio</a>',
                'Mitgliedschaft bei der SAC-Sektion Ticino, ausser für Schnuppertouren. <a href="adesione.html">Mitglied werden</a>',
                'Membership of the SAC Ticino Section, except for trial outings. <a href="adesione.html">Become a member</a>')),
            (tr("Costi", "Kosten", "Costs"), tr(
                "Coprono vitto e alloggio a mezza pensione, guida e trasporto in furgone. Dai 21 ai 25 anni si aggiungono CHF 30 al giorno, perché non ci sono contributi G+S.",
                "Sie decken Unterkunft mit Halbpension, Bergführer und Transport im Kleinbus. Von 21 bis 25 Jahren kommen CHF 30 pro Tag dazu, weil es keine J+S-Beiträge gibt.",
                "They cover half-board food and lodging, guide and minibus transport. From 21 to 25, CHF 30 a day is added, as there are no Youth+Sport contributions.")),
            (tr("Inclusione", "Inklusion", "Inclusion"), tr(
                "Ragazze e ragazzi con disabilità fisica o psichica sono i benvenuti: contatta il coordinatore per trovare insieme la soluzione giusta.",
                "Mädchen und Jungen mit körperlicher oder psychischer Beeinträchtigung sind willkommen: Kontaktieren Sie den Koordinator, um gemeinsam die richtige Lösung zu finden.",
                "Girls and boys with physical or mental disabilities are welcome: contact the coordinator to find the right solution together.")),
            (tr("Coordinatore", "Koordinator", "Coordinator"), 'Diego Romelli, <a class="num" href="tel:+393485731549">+39 348 573 1549</a>'),
            (tr("Cassiere", "Kassier", "Treasurer"), 'Nicola Martinoni, <a class="num" href="tel:+41794391691">+41 79 439 16 91</a>'),
            ("Spider", "Giosiana Codoni")]
    titolo = tr("Giovani", "Jugend", "Youth")
    programma = tr("Programma giovani", "Jugendprogramm", "Youth programme")
    body = page_hero([att_crumb(), (titolo, None)], titolo, tr(
                         "Uscite di un giorno, fine settimana e campi di più giorni: alpinismo, arrampicata, sci alpinismo e molto altro, con monitori formati e guide alpine.",
                         "Tagestouren, Wochenenden und mehrtägige Lager: Hochtouren, Klettern, Skitouren und vieles mehr, mit ausgebildeten Leitenden und Bergführern.",
                         "Day trips, weekends and camps of several days: mountaineering, climbing, ski touring and much more, with trained instructors and mountain guides."),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{GITE_GIOVANI}">{programma} <span class="arrow" aria-hidden="true">→</span></a></div>',
                     figure=img("attivita/giovani-3x4", tr("Giovane arrampicatore su una parete dei Denti della Vecchia", "Junger Kletterer an einer Wand der Denti della Vecchia", "Young climber on a face of the Denti della Vecchia"), 800, 1066, lazy=False)) + f"""

<section class="section" aria-labelledby="fasce-h">
<div class="container">
<div class="section-head"><h2 id="fasce-h" class="h2">{tr("Quattro fasce d’età", "Vier Altersgruppen", "Four age groups")}</h2></div>
<div class="groups" data-reveal>
{cards}
</div>
</div>
</section>

<section class="section--surface" aria-labelledby="iscr-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="iscr-h" class="h2">{tr("Iscrizioni<br>e costi", "Anmeldung<br>und Kosten", "Registration<br>and costs")}</h2>
<div><a class="link" href="{GITE_GIOVANI}">{programma}</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav(ATT_MENU(), L("giovani.html"))}"""
    return sezione_page("giovani.html", titolo + " | CAS Ticino", tr(
        "Il gruppo giovani del CAS Ticino: arrampicata, sci alpinismo, campi e uscite per ragazze e ragazzi dai 2 ai 25 anni, con monitori e guide alpine.",
        "Die Jugendgruppe der SAC-Sektion Ticino: Klettern, Skitouren, Lager und Touren für Mädchen und Jungen von 2 bis 25 Jahren, mit Leitenden und Bergführern.",
        "The SAC Ticino Section’s youth group: climbing, ski touring, camps and outings for girls and boys aged 2 to 25, with instructors and mountain guides."),
        body, og="attivita/giovani-3x4")


def senior():
    mail = '<a href="mailto:senior@casticino.ch">senior@casticino.ch</a>'
    tel = ('<a class="num" href="tel:+41763973390">+41 76 397 33 90</a>', '<a class="num" href="tel:+41919721010">+41 91 972 10 10</a>')
    rows = [(tr("Chi può partecipare", "Wer mitmachen kann", "Who can join"), tr(
                'Dai 60 anni, con l’affiliazione al CAS Ticino. Non c’è una tassa aggiuntiva, e tutti i soci della sezione possono partecipare alle attività. <a href="adesione.html">Diventa socio</a>',
                'Ab 60 Jahren, mit Mitgliedschaft bei der SAC-Sektion Ticino. Es gibt keinen Zusatzbeitrag, und alle Mitglieder der Sektion können an den Aktivitäten teilnehmen. <a href="adesione.html">Mitglied werden</a>',
                'From age 60, with membership of the SAC Ticino Section. There is no extra fee, and all the section’s members can take part in the activities. <a href="adesione.html">Become a member</a>')),
            (tr("Come aderire", "Beitritt", "How to join"), tr(
                f"Scrivi a {mail} con nome, data di nascita, numero di socio CAS, indirizzo, telefono ed e-mail.",
                f"Schreiben Sie an {mail} mit Name, Geburtsdatum, SAC-Mitgliedernummer, Adresse, Telefon und E-Mail.",
                f"Write to {mail} with your name, date of birth, SAC membership number, address, phone and e-mail.")),
            (tr("Uscite", "Touren", "Outings"), tr(
                "Di norma il giovedì. Il calendario aggiornato è sul programma gite online.",
                "In der Regel am Donnerstag. Der aktuelle Kalender steht im Online-Tourenprogramm.",
                "Usually on Thursdays. The up-to-date calendar is in the online trip programme.")),
            (tr("Pranzi", "Mittagessen", "Lunches"), tr(
                f"Il secondo e il quarto mercoledì del mese al Bistrot Vecchio Torchio di Viganello. Iscrizioni entro il lunedì presso Hanni Vanossi ({tel[0]}) o direttamente al ristorante ({tel[1]}).",
                f"Am zweiten und vierten Mittwoch im Monat im Bistrot Vecchio Torchio in Viganello. Anmeldung bis Montag bei Hanni Vanossi ({tel[0]}) oder direkt im Restaurant ({tel[1]}).",
                f"On the second and fourth Wednesday of the month at the Bistrot Vecchio Torchio in Viganello. Book by Monday with Hanni Vanossi ({tel[0]}) or directly with the restaurant ({tel[1]}).")),
            (tr("Capigita", "Tourenleitende", "Trip leaders"), tr(
                "Il dicastero cerca sempre nuovi capigita.", "Das Ressort sucht immer neue Tourenleitende.", "The department is always looking for new trip leaders."))]
    titolo = tr("Senior", "Senioren", "Seniors")
    body = page_hero([att_crumb(), (titolo, None)], titolo, tr(
        "Un gruppo di non più giovani con la passione per la montagna: la bellezza della natura, i piaceri della tavola e la nostra storia.",
        "Eine Gruppe nicht mehr ganz Junger mit Leidenschaft für die Berge: die Schönheit der Natur, die Freuden der Tafel und unsere Geschichte.",
        "A group of the no-longer-young with a passion for the mountains: the beauty of nature, the pleasures of the table and our history.")) + f"""

{band_img("attivita/senior-2x1", tr("Escursionisti del gruppo senior su un sentiero di cresta", "Wandernde der Seniorengruppe auf einem Gratweg", "Hikers from the seniors group on a ridge path"), 1000, 500)}

<section class="section" aria-labelledby="gruppo-h">
<div class="container detail">
<div class="detail-intro split-intro">
<span class="label">{tr("Il gruppo, dal 1940", "Die Gruppe, seit 1940", "The group, since 1940")}</span>
<h2 id="gruppo-h" class="h2">{tr("Ogni giovedì<br>in cammino", "Jeden Donnerstag<br>unterwegs", "On the trail<br>every Thursday")}</h2>
<p>{tr("Escursioni, gite di più giorni, mountain bike e racchette, con percorsi adatti a diversi livelli di allenamento.",
       "Wanderungen, mehrtägige Touren, Mountainbike und Schneeschuhe, auf Routen für verschiedene Trainingsstände.",
       "Hikes, trips of several days, mountain biking and snowshoeing, on routes suited to different levels of fitness.")}</p>
<div><a class="btn btn--primary" href="{GITE_SENIORI}">{tr("Programma senior", "Seniorenprogramm", "Seniors’ programme")} <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav(ATT_MENU(), L("senior.html"))}"""
    return sezione_page("senior.html", titolo + " | CAS Ticino", tr(
        "Il gruppo senior del CAS Ticino, dal 1940: escursioni il giovedì, gite di più giorni, mountain bike e racchette per soci dai 60 anni.",
        "Die Seniorengruppe der SAC-Sektion Ticino, seit 1940: Wanderungen am Donnerstag, mehrtägige Touren, Mountainbike und Schneeschuhe für Mitglieder ab 60.",
        "The SAC Ticino Section’s seniors group, since 1940: Thursday hikes, trips of several days, mountain biking and snowshoeing for members aged 60 and over."),
        body, og="attivita/senior-2x1")


CORSO_SLUG = {"Alpinismo": "alpinismo", "Sci alpinismo": "scialpinismo", "Arrampicata": "arrampicata",
              "Tecnica di sci fuori pista": "fuoripista", "Freeride": "fuoripista", "Racchette": "racchette"}

def pdf_corso(cartella, file, testo):
    """Link a un PDF del corso in docs/corsi/<cartella>/ (in italiano)."""
    return f'<a href="{DOC}corsi/{cartella}/{file}.pdf">{testo} ({tr("PDF", "PDF, italienisch", "PDF, in Italian")})</a>'


def schede_corso(c, x):
    """Le cinque righe di ogni corso: struttura, materiale e programma rimandano ai PDF in docs/corsi/<c>/
    (il link al programma compare solo quando c'è il PDF dell'anno)."""
    prog = x["programma"]
    if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, "programma-2027.pdf")):
        prog += " " + pdf_corso(c, "programma-2027", tr("Programma 2027", "Programm 2027", "Programme 2027"))
    return [(tr("Struttura", "Aufbau", "Structure"), f'{x["struttura"]} {pdf_corso(c, "obiettivi", tr("Obiettivi del corso", "Kursziele", "Course objectives"))}'),
            (tr("Requisiti", "Voraussetzungen", "Requirements"), x["requisiti"]),
            (tr("Partecipanti", "Teilnehmende", "Participants"), x["partecipanti"]),
            (tr("Materiale", "Material", "Equipment"), f'{x["materiale"]} {pdf_corso(c, "materiale", tr("Lista del materiale", "Materialliste", "Equipment list"))}'),
            (tr("Programma", "Programm", "Programme"), prog)]


CORSI = [
    dict(stagione="Estate", titolo="Alpinismo", cartella="alpinismo", img="corsi/alpinismo-4x5", dim=(594, 742), alt="Cordata su una cresta di neve",
         testo="Il ponte tra escursionismo e alpinismo: legarsi correttamente su ghiacciaio e in cresta, tecniche di assicurazione, uso della corda in arrampicata e dei diversi attrezzi di progressione. Teoria e pratica, con lettura della carta, pianificazione, primo soccorso e salite in vetta su roccia e ghiaccio.",
         struttura="Sette giorni in tre uscite: tre giorni alla Capanna Piansecco, in Valle Bedretto, per nodi, corda, ramponi e piccozza; un fine settimana tra il granito del Furka e il ghiacciaio del Rodano; uno al Passo del Susten, con una gita alpinistica finale. Alla fine si partecipa da secondi di cordata a gite fino al grado PD+/III.",
         requisiti="Discreta condizione fisica: 4-5 ore di cammino con uno zaino di circa 10 kg, a 350-400 m di dislivello all’ora. Esperienza escursionistica, nessuna vertigine, età minima 16 anni (con il consenso dei genitori).",
         partecipanti="Iscrizioni online dal 1° dicembre 2026. Numero di posti limitato per ragioni di sicurezza (in definizione); precedenza in ordine d’iscrizione e ai soci CAS, poi lista d’attesa. L’iscrizione è definitiva con il pagamento della quota. Serata di presentazione e uscite obbligatorie, con qualsiasi tempo.",
         materiale="L’equipaggiamento personale spetta al partecipante; il materiale tecnico lo presta il CAS a chi non ce l’ha. Alla serata di presentazione si vede cosa serve: meglio aspettarla prima di comprare.",
         programma="Serata di presentazione il 12 marzo 2027 a Bellinzona; uscite il 28-30 maggio, il 12-13 giugno e il 3-4 luglio 2027. CHF 700 per i soci, 800 per i non soci, 450 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing escluse.",
         de=dict(titolo="Hochtouren", alt="Seilschaft auf einem Schneegrat",
                 testo="Die Brücke zwischen Wandern und Hochtouren: sich auf Gletscher und Grat richtig anseilen, Sicherungstechniken, Seilhandhabung beim Klettern und der Gebrauch der verschiedenen Geräte. Theorie und Praxis, mit Kartenlesen, Planung, Erster Hilfe und Gipfelbesteigungen auf Fels und Eis.",
                 struttura="Sieben Tage in drei Blöcken: drei Tage in der Capanna Piansecco im Bedrettotal für Knoten, Seil, Steigeisen und Pickel; ein Wochenende zwischen dem Granit der Furka und dem Rhonegletscher; eines am Sustenpass, mit einer abschliessenden Hochtour. Danach nimmt man als Seilzweite oder Seilzweiter an Touren bis zum Grad ZS+/III teil.",
                 requisiti="Gute Kondition: 4–5 Stunden Gehzeit mit einem Rucksack von etwa 10 kg, bei 350–400 Höhenmetern pro Stunde. Wandererfahrung, schwindelfrei, Mindestalter 16 Jahre (mit Einverständnis der Eltern).",
                 partecipanti="Online-Anmeldung ab 1. Dezember 2026. Aus Sicherheitsgründen beschränkte Platzzahl (noch offen); Vorrang nach Anmeldeeingang und für SAC-Mitglieder, danach Warteliste. Die Anmeldung ist mit der Bezahlung definitiv. Informationsabend und Kurstage obligatorisch, bei jedem Wetter.",
                 materiale="Die persönliche Ausrüstung bringen die Teilnehmenden selbst mit; technisches Material leiht der SAC allen, die keines haben. Am Informationsabend sieht man, was es braucht: Am besten erst danach einkaufen.",
                 programma="Informationsabend am 12. März 2027 in Bellinzona; Kurstage 28.–30. Mai, 12.–13. Juni und 3.–4. Juli 2027. CHF 700 für Mitglieder, 800 für Nichtmitglieder, 450 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften nicht inbegriffen."),
         en=dict(titolo="Mountaineering", alt="Rope team on a snow ridge",
                 testo="The bridge between hiking and mountaineering: roping up correctly on glaciers and ridges, belaying techniques, rope work when climbing and the use of the various tools. Theory and practice, with map reading, planning, first aid and summit climbs on rock and ice.",
                 struttura="Seven days in three sessions: three days at Capanna Piansecco in Valle Bedretto for knots, rope, crampons and ice axe; a weekend between the Furka granite and the Rhone glacier; one at the Susten Pass, with a final mountaineering tour. Afterwards you can take part as a second on the rope in tours up to grade PD+/III.",
                 requisiti="Reasonable fitness: 4–5 hours’ walking with a pack of about 10 kg, at 350–400 m of ascent per hour. Hiking experience, no fear of heights, minimum age 16 (with parental consent).",
                 partecipanti="Online registration from 1 December 2026. Places limited for safety reasons (number to be confirmed); priority in order of registration and to SAC members, then a waiting list. Registration is final once the fee is paid. The presentation evening and outings are compulsory, whatever the weather.",
                 materiale="Personal equipment is the participant’s responsibility; the SAC lends technical gear to those who don’t have it. The presentation evening covers what you need: best wait for it before buying.",
                 programma="Presentation evening on 12 March 2027 in Bellinzona; outings on 28–30 May, 12–13 June and 3–4 July 2027. CHF 700 for members, 800 for non-members, 450 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel not included.")),
    dict(stagione="Inverno", titolo="Sci alpinismo", cartella="sci-alpinismo", img="corsi/scialpinismo-4x5", dim=(582, 728), alt="Sci alpinisti in salita su un pendio innevato",
         testo="Per muoversi in sicurezza e in autonomia nelle gite della sezione: salita con le pelli su pendii ripidi, discesa fuori pista, uso del materiale di sicurezza, valutazione del pericolo valanghe e pianificazione.",
         struttura="Sette giorni: una giornata introduttiva ad Airolo per verificare forma e tecnica, una serata di teoria su neve, ARTVA e autosoccorso, poi tre fine settimana alla Capanna Piansecco, all’Hotel Tiefenbach sul Furka e alla Camona da Maighels, con istruzione e gite fino a 800-1200 m di dislivello.",
         requisiti="Sciare bene su piste nere e reggere una gita di 1200 m di dislivello con uno zaino di 5 kg in al massimo 4 ore. Età minima 16 anni. Aperto anche agli snowboarder con splitboard. Chi dopo la giornata introduttiva non risulta idoneo riceve l’80% della quota.",
         partecipanti="Al massimo 30. Iscrizioni dal 1° ottobre al 1° dicembre 2026, o fino a esaurimento dei posti; la quota va versata entro il 10 dicembre. Uscite obbligatorie, con qualsiasi tempo; assenze e ritiri non danno diritto a rimborsi.",
         materiale="Attrezzatura completa da sci alpinismo. ARTVA, pala e sonda prestati su richiesta, compresi nella quota.",
         programma="Presentazione il 3 dicembre 2026 (anche via Teams); giornata introduttiva il 9 gennaio, teoria il 12 gennaio, uscite il 16-17 gennaio, il 20-21 febbraio e il 6-7 marzo 2027. CHF 650 per i soci, 750 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (circa CHF 100) escluse.",
         de=dict(titolo="Skitouren", alt="Skitourengeher im Aufstieg an einem verschneiten Hang",
                 testo="Um sich auf den Touren der Sektion sicher und selbständig zu bewegen: Aufstieg mit Fellen an steilen Hängen, Abfahrt abseits der Piste, Umgang mit dem Sicherheitsmaterial, Beurteilung der Lawinengefahr und Planung.",
                 struttura="Sieben Tage: ein Einführungstag in Airolo, um Form und Technik zu prüfen, ein Theorieabend über Schnee, LVS und Kameradenrettung, dann drei Wochenenden in der Capanna Piansecco, im Hotel Tiefenbach an der Furka und in der Camona da Maighels, mit Ausbildung und Touren bis 800–1200 Höhenmeter.",
                 requisiti="Sicheres Skifahren auf schwarzen Pisten und eine Tour von 1200 Höhenmetern mit 5 kg Rucksack in höchstens 4 Stunden. Mindestalter 16 Jahre. Auch für Snowboarder mit Splitboard offen. Wer sich nach dem Einführungstag als nicht geeignet erweist, erhält 80 % des Kursgelds zurück.",
                 partecipanti="Höchstens 30. Anmeldung vom 1. Oktober bis 1. Dezember 2026 oder bis die Plätze vergeben sind; das Kursgeld ist bis 10. Dezember zu bezahlen. Kurstage obligatorisch, bei jedem Wetter; Abwesenheiten und Rückzüge geben kein Recht auf Rückerstattung.",
                 materiale="Vollständige Skitourenausrüstung. LVS, Schaufel und Sonde auf Anfrage leihweise, im Kursgeld inbegriffen.",
                 programma="Präsentation am 3. Dezember 2026 (auch über Teams); Einführungstag am 9. Januar, Theorie am 12. Januar, Kurstage 16.–17. Januar, 20.–21. Februar und 6.–7. März 2027. CHF 650 für Mitglieder, 750 für Nichtmitglieder, 400 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften (etwa CHF 100) nicht inbegriffen."),
         en=dict(titolo="Ski touring", alt="Ski tourers climbing a snowy slope",
                 testo="To move safely and independently on the section’s trips: skinning up steep slopes, off-piste descents, use of safety equipment, avalanche risk assessment and planning.",
                 struttura="Seven days: an introductory day in Airolo to check fitness and technique, a theory evening on snow, transceivers and companion rescue, then three weekends at Capanna Piansecco, Hotel Tiefenbach on the Furka and Camona da Maighels, with instruction and tours of up to 800–1200 m of ascent.",
                 requisiti="Ski well on black runs and manage a 1200 m tour with a 5 kg pack in at most 4 hours. Minimum age 16. Also open to snowboarders with a splitboard. Anyone found unsuitable after the introductory day gets 80% of the fee back.",
                 partecipanti="Maximum 30. Registration from 1 October to 1 December 2026, or until places run out; the fee is due by 10 December. Outings are compulsory, whatever the weather; absences and withdrawals give no right to a refund.",
                 materiale="Full ski touring equipment. Transceiver, shovel and probe lent on request, included in the fee.",
                 programma="Presentation on 3 December 2026 (also via Teams); introductory day on 9 January, theory on 12 January, outings on 16–17 January, 20–21 February and 6–7 March 2027. CHF 650 for members, 750 for non-members, 400 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel (about CHF 100) not included.")),
    dict(stagione="Primavera", titolo="Arrampicata", cartella="arrampicata", img="corsi/arrampicata-4x5", dim=(594, 742), alt="Cordata su una parete di roccia accanto a un ghiacciaio",
         testo="Per principianti che vogliono avvicinarsi all’arrampicata in ambiente e per chi vuole consolidare la tecnica: sicurezza, manovre di corda, progressione su vie di più tiri. Dopo le basi, sempre più autonomia sotto la supervisione di un istruttore di arrampicata.",
         struttura="Sette giorni in tre fine settimana: prime arrampicate in falesia in Piemonte, vie di più tiri nel Locarnese, gite di applicazione nelle Alpi centrali; tra maggio e giugno, a volte, serate di arrampicata e ripasso dei nodi. Alla fine si arrampica in autonomia in falesia e su vie di più tiri: da secondi fino al 5a, da primi fino al 4b, con discesa in corda doppia.",
         requisiti="Nessun prerequisito tecnico: il corso è pensato per chi comincia. Età minima 16 anni.",
         partecipanti="Al massimo 26, in ordine d’iscrizione. All’iscrizione si versa un anticipo di CHF 300; l’iscrizione è definitiva con il saldo alla serata di presentazione. Serata e uscite obbligatorie, con qualsiasi tempo; le assenze vanno annunciate al capocorso entro il martedì prima.",
         materiale="Il CAS presta il materiale tecnico a chi non ce l’ha; alla serata di presentazione si vede cosa serve.",
         programma="Presentazione il 12 aprile 2027 alle 20:00 alla Scuola professionale di Trevano; uscite il 1-2 maggio, il 15-17 maggio e il 12-13 giugno 2027. CHF 600 per i soci, 650 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (CHF 40) escluse.",
         de=dict(titolo="Klettern", alt="Seilschaft an einer Felswand neben einem Gletscher",
                 testo="Für Einsteigerinnen und Einsteiger, die das Klettern draussen kennenlernen möchten, und für alle, die ihre Technik festigen wollen: Sicherheit, Seilmanöver, Mehrseillängenrouten. Nach den Grundlagen immer mehr Selbständigkeit unter Aufsicht eines Kletterlehrers.",
                 struttura="Sieben Tage an drei Wochenenden: erste Klettereien im Klettergarten im Piemont, Mehrseillängenrouten im Locarnese, Anwendungstouren in den Zentralalpen; zwischen Mai und Juni manchmal Kletterabende und Knotenrepetition. Am Ende klettert man selbständig im Klettergarten und in Mehrseillängenrouten: im Nachstieg bis 5a, im Vorstieg bis 4b, mit Abseilen.",
                 requisiti="Keine technischen Voraussetzungen: Der Kurs ist für Einsteiger gedacht. Mindestalter 16 Jahre.",
                 partecipanti="Höchstens 26, nach Anmeldeeingang. Bei der Anmeldung ist eine Anzahlung von CHF 300 zu leisten; definitiv ist die Anmeldung mit der Restzahlung am Informationsabend. Abend und Kurstage obligatorisch, bei jedem Wetter; Abwesenheiten sind dem Kursleiter bis zum Dienstag davor zu melden.",
                 materiale="Der SAC leiht technisches Material allen, die keines haben; am Informationsabend sieht man, was es braucht.",
                 programma="Präsentation am 12. April 2027 um 20:00 Uhr in der Berufsschule Trevano; Kurstage 1.–2. Mai, 15.–17. Mai und 12.–13. Juni 2027. CHF 600 für Mitglieder, 650 für Nichtmitglieder, 400 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften (CHF 40) nicht inbegriffen."),
         en=dict(titolo="Climbing", alt="Rope team on a rock face next to a glacier",
                 testo="For beginners who want to get into outdoor climbing and for those who want to consolidate their technique: safety, rope work, multi-pitch routes. After the basics, more and more independence under the supervision of a climbing instructor.",
                 struttura="Seven days over three weekends: first climbs at a crag in Piedmont, multi-pitch routes around Locarno, applied trips in the Central Alps; between May and June, sometimes, climbing evenings and knot practice. By the end you climb independently at crags and on multi-pitch routes: seconding up to 5a, leading up to 4b, with abseiling.",
                 requisiti="No technical prerequisites: the course is designed for beginners. Minimum age 16.",
                 partecipanti="Maximum 26, in order of registration. A deposit of CHF 300 is due on registration; registration is final with the balance paid at the presentation evening. The evening and outings are compulsory, whatever the weather; absences must be reported to the course leader by the Tuesday before.",
                 materiale="The SAC lends technical gear to those who don’t have it; the presentation evening covers what you need.",
                 programma="Presentation on 12 April 2027 at 20:00 at the Trevano vocational school; outings on 1–2 May, 15–17 May and 12–13 June 2027. CHF 600 for members, 650 for non-members, 400 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel (CHF 40) not included.")),
    dict(stagione="Inverno", titolo="Tecnica di sci fuori pista", cartella="freeride", img="corsi/freeride-4x5", dim=(594, 742), alt="Sciatori in discesa su un ghiacciaio",
         testo="Per chi fatica a scendere su pendii non preparati: trucchi e consigli per affrontare la neve fuori dalle piste battute. Adatto ai soci che vogliono migliorare, a chi si avvicina allo sci alpinismo e agli sciatori esperti in cerca di strategie per le condizioni difficili.",
         struttura="Quattro giorni per affinare la tecnica su diversi tipi di neve e di terreno, leggere il pendio e scegliere la tattica giusta per il gruppo, applicare le misure di riduzione del rischio e consolidare il soccorso in valanga.",
         requisiti="Le basi dello sci alpinismo (salire con le pelli, autosoccorso in valanga) e una discreta tecnica di sci fuori pista.",
         partecipanti="Numero di posti e condizioni d’iscrizione in definizione.",
         materiale="Attrezzatura completa da fuori pista e sci alpinismo, con ARTVA, pala e sonda.",
         programma="Programma 2027 in definizione: date e costi seguono.",
         de=dict(titolo="Off-Piste-Skitechnik", alt="Skifahrer in der Abfahrt auf einem Gletscher",
                 testo="Für alle, die sich an unpräparierten Hängen schwertun: Tricks und Tipps für den Schnee abseits der Pisten. Für Mitglieder, die sich verbessern wollen, für Einsteiger ins Skitourengehen und für erfahrene Skifahrer, die Strategien für schwierige Verhältnisse suchen.",
                 struttura="Vier Tage, um die Technik in verschiedenen Schnee- und Geländearten zu verfeinern, den Hang zu lesen und die richtige Taktik für die Gruppe zu wählen, Massnahmen zur Risikominderung anzuwenden und die Lawinenrettung zu festigen.",
                 requisiti="Die Grundlagen des Skitourengehens (Aufstieg mit Fellen, Kameradenrettung) und eine ordentliche Technik abseits der Piste.",
                 partecipanti="Platzzahl und Anmeldebedingungen noch offen.",
                 materiale="Vollständige Freeride- und Skitourenausrüstung mit LVS, Schaufel und Sonde.",
                 programma="Programm 2027 in Vorbereitung: Daten und Kosten folgen."),
         en=dict(titolo="Off-piste ski technique", alt="Skiers descending a glacier",
                 testo="For those who struggle on ungroomed slopes: tips and tricks for snow away from the pistes. For members who want to improve, for newcomers to ski touring and for experienced skiers looking for strategies for difficult conditions.",
                 struttura="Four days to refine technique on different kinds of snow and terrain, read the slope and choose the right tactics for the group, apply risk-reduction measures and consolidate avalanche rescue.",
                 requisiti="The basics of ski touring (skinning, avalanche companion rescue) and a reasonable off-piste technique.",
                 partecipanti="Number of places and registration conditions to be confirmed.",
                 materiale="Full off-piste and ski touring equipment, with transceiver, shovel and probe.",
                 programma="2027 programme in preparation: dates and costs to follow.")),
    dict(stagione="Inverno", titolo="Racchette", cartella="racchette", img="corsi/racchette-4x5", dim=(800, 1000), alt="Cresta innevata sopra un mare di nuvole",
         testo="Introduzione all’escursionismo con le racchette, tra teoria e pratica: riconoscere i segnali di pericolo, valutare il rischio valanghe e il terreno, pianificare con gli strumenti disponibili, ricerca dei sepolti e primo soccorso.",
         struttura="Sei giorni: una serata di nivologia, una giornata sulla sicurezza con ARTVA, pala e sonda, poi due fine settimana in capanna, alla Capanna Piansecco e alla Capanna Maighels, tra tecnica di progressione, metodo 3x3, orientamento e dinamiche di gruppo. Alla fine si sale e si scende in sicurezza su terreni semplici, segnati e non.",
         requisiti="Discreta condizione fisica: escursioni di 4-5 ore con 500-700 m di dislivello. Età minima 16 anni.",
         partecipanti="Al massimo 20, in ordine d’iscrizione. L’iscrizione è definitiva con il pagamento della quota alla serata introduttiva. Serata e uscite obbligatorie, con qualsiasi tempo; la meta può cambiare secondo le condizioni.",
         materiale="L’equipaggiamento personale viene controllato il primo giorno. ARTVA, pala e sonda prestati a chi ne ha bisogno.",
         programma="Serata introduttiva martedì 15 dicembre 2026 nel Luganese; nivologia il 12 gennaio 2027 a Mezzovico, sicurezza il 16 gennaio ad Airolo, uscite il 23-24 gennaio e il 13-14 febbraio 2027. CHF 650 per i soci, 700 per i non soci, 375 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni, trasferte comprese.",
         de=dict(titolo="Schneeschuhtouren", alt="Verschneiter Grat über einem Nebelmeer",
                 testo="Einführung ins Schneeschuhwandern, in Theorie und Praxis: Gefahrenzeichen erkennen, Lawinenrisiko und Gelände beurteilen, mit den verfügbaren Hilfsmitteln planen, Verschüttetensuche und Erste Hilfe.",
                 struttura="Sechs Tage: ein Abend Schnee- und Lawinenkunde, ein Sicherheitstag mit LVS, Schaufel und Sonde, dann zwei Wochenenden in der Capanna Piansecco und der Capanna Maighels, mit Gehtechnik, 3x3-Methode, Orientierung und Gruppendynamik. Am Ende steigt man sicher auf und ab in einfachem Gelände, markiert und unmarkiert.",
                 requisiti="Gute Kondition: Touren von 4–5 Stunden mit 500–700 Höhenmetern. Mindestalter 16 Jahre.",
                 partecipanti="Höchstens 20, nach Anmeldeeingang. Definitiv ist die Anmeldung mit der Bezahlung am Einführungsabend. Abend und Kurstage obligatorisch, bei jedem Wetter; das Ziel kann je nach Verhältnissen ändern.",
                 materiale="Die persönliche Ausrüstung wird am ersten Tag kontrolliert. LVS, Schaufel und Sonde werden bei Bedarf ausgeliehen.",
                 programma="Einführungsabend am Dienstag, 15. Dezember 2026, im Luganese; Schnee- und Lawinenkunde am 12. Januar 2027 in Mezzovico, Sicherheitstag am 16. Januar in Airolo, Kurstage 23.–24. Januar und 13.–14. Februar 2027. CHF 650 für Mitglieder, 700 für Nichtmitglieder, 375 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren, Fahrten inbegriffen."),
         en=dict(titolo="Snowshoeing", alt="Snowy ridge above a sea of clouds",
                 testo="An introduction to snowshoeing, in theory and practice: recognising danger signs, assessing avalanche risk and terrain, planning with the tools available, searching for buried people and first aid.",
                 struttura="Six days: an evening on snow science, a safety day with transceiver, shovel and probe, then two weekends at Capanna Piansecco and Capanna Maighels, covering walking technique, the 3x3 method, navigation and group dynamics. By the end you can go up and down safely on easy terrain, marked and unmarked.",
                 requisiti="Reasonable fitness: outings of 4–5 hours with 500–700 m of ascent. Minimum age 16.",
                 partecipanti="Maximum 20, in order of registration. Registration is final once the fee is paid at the introductory evening. The evening and outings are compulsory, whatever the weather; the destination may change according to conditions.",
                 materiale="Personal equipment is checked on the first day. Transceiver, shovel and probe lent to those who need them.",
                 programma="Introductory evening on Tuesday 15 December 2026 in the Lugano area; snow science on 12 January 2027 in Mezzovico, safety day on 16 January in Airolo, outings on 23–24 January and 13–14 February 2027. CHF 650 for members, 700 for non-members, 375 for OG youth up to 20 and student members aged 21 to 25, travel included.")),
]

# PDF dei corsi anche nella pagina Documenti (e quindi nella ricerca): un gruppo per tipo di documento
CARTELLE_CORSI = [("Alpinismo", "alpinismo"), ("Sci alpinismo", "sci-alpinismo"), ("Arrampicata", "arrampicata"),
                  ("Tecnica di sci fuori pista", "freeride"), ("Racchette", "racchette")]
for gruppo, file in [("Obiettivi corsi", "obiettivi"), ("Equipaggiamento", "materiale")]:
    DOCS.append((gruppo, [(nome, f"{DOC}corsi/{c}/{file}.pdf") for nome, c in CARTELLE_CORSI
                          if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, file + ".pdf"))]))


def corsi():
    lang = LINGUA["lang"]
    stagioni = {"Estate": tr("Estate", "Sommer", "Summer"), "Inverno": tr("Inverno", "Winter", "Winter"), "Primavera": tr("Primavera", "Frühling", "Spring")}
    articoli = []
    for c in CORSI:
        x = c if lang == "it" else {**c, **c[lang]}
        articoli.append(f"""<article class="course-row course-row--corso" id="corso-{CORSO_SLUG[c['titolo']]}" aria-labelledby="corso-{CORSO_SLUG[c['titolo']]}-h" data-reveal>
<figure>{img(c['img'], x['alt'], *c['dim'])}</figure>
<div class="course-text">
<span class="label">{stagioni[c['stagione']]}</span>
<h2 id="corso-{CORSO_SLUG[c['titolo']]}-h" class="h2">{x['titolo']}</h2>
<p>{x['testo']}</p>
<a class="btn btn--primary" href="{GITE_CORSI}">{tr("Iscriviti", "Anmelden", "Register")} <span class="arrow" aria-hidden="true">→</span></a>
</div>
{facts(schede_corso(c['cartella'], x))}
</article>""")
    titolo = tr("Corsi", "Kurse", "Courses")
    body = page_hero([att_crumb(), (titolo, None)], titolo, tr(
        "Corsi nei fine settimana, diretti da professionisti della montagna con monitori esperti: le basi per partecipare in sicurezza alle attività della sezione. Il programma dell’anno successivo esce entro novembre.",
        "Kurse an Wochenenden, geleitet von Bergprofis mit erfahrenen Leitenden: die Grundlagen, um sicher an den Aktivitäten der Sektion teilzunehmen. Das Programm des folgenden Jahres erscheint bis November; die Kursunterlagen (PDF) sind auf Italienisch.",
        "Weekend courses led by mountain professionals with experienced instructors: the basics for taking part safely in the section’s activities. The following year’s programme comes out by November; the course documents (PDF) are in Italian.")) + f"""

<figure class="band">
{pic("paesaggi/salita-prato", tr("Un gruppo sale in fila su un sentiero tra prati fioriti, sotto il cielo azzurro", "Eine Gruppe steigt im Gänsemarsch auf einem Weg durch Blumenwiesen, unter blauem Himmel", "A group climbs in single file along a path through flowering meadows, under a blue sky"), mobile="paesaggi/salita-prato-4x3", w=2000, h=1125, lazy=False)}
{credito()}
</figure>

<section class="section" aria-label="{tr("Corsi base", "Grundkurse", "Basic courses")}">
<div class="container">
{chr(10).join(articoli)}
</div>
</section>

<section class="section" aria-labelledby="avanzati-h">
<div class="container">
<div class="callout">
<p>{tr("<strong id=\"avanzati-h\">Verso capogita e monitore G+S.</strong> Per chi vuole approfondire o prepararsi ai corsi capogita CAS e monitore Gioventù+Sport, la sezione propone corsi avanzati di alpinismo, sci alpinismo e arrampicata, di regola ad anni alterni, e serate di formazione teorica con specialisti.",
       "<strong id=\"avanzati-h\">Auf dem Weg zur Tourenleitung und J+S-Leitung.</strong> Wer sich vertiefen oder auf die Tourenleiterkurse des SAC und die Jugend+Sport-Leiterkurse vorbereiten will, findet bei der Sektion Fortgeschrittenenkurse in Hochtouren, Skitouren und Klettern, in der Regel alle zwei Jahre, und Theorieabende mit Fachleuten.",
       "<strong id=\"avanzati-h\">Towards trip leader and Youth+Sport instructor.</strong> For those who want to go further or prepare for the SAC trip leader and Youth+Sport instructor courses, the section offers advanced courses in mountaineering, ski touring and climbing, usually every other year, and theory evenings with specialists.")}</p>
</div>
</div>
</section>

{prima_di_partire()}

{subnav(ATT_MENU(), L("corsi.html"))}"""
    return sezione_page("corsi.html", titolo + " | CAS Ticino", tr(
        "Corsi del CAS Ticino diretti da professionisti: sci alpinismo, racchette, tecnica di sci fuori pista, arrampicata e alpinismo.",
        "Kurse der SAC-Sektion Ticino mit Bergprofis: Skitouren, Schneeschuhtouren, Off-Piste-Skitechnik, Klettern und Hochtouren.",
        "Courses of the SAC Ticino Section led by professionals: ski touring, snowshoeing, off-piste ski technique, climbing and mountaineering."),
        body, og="corsi/scialpinismo-4x5")


# ------------------------------------------------------------------ noleggio materiale
# Articoli, prezzi, quantità e taglie in data/noleggio-inventario.json (lo legge anche il servizio delle richieste).
# Niente listino a parte: prezzi e taglie si vedono nel modulo.
# Il modulo (assets/noleggio.js) chiede la disponibilità e invia le richieste al Worker in scripts/noleggio/.

NOLEGGIO_MAIL = "noleggio@casticino.ch"   # indirizzo pubblico; finché la casella non è attiva il servizio usa ancora MAIL_GESTORE/MAIL_MITTENTE di scripts/noleggio/wrangler.toml
NOLEGGIO_API = "https://casticino-noleggio.fole89.workers.dev/"   # indirizzo del Worker (scripts/noleggio/LEGGIMI.md)
NOLEGGIO_TURNSTILE = "0x4AAAAAAFOZV05i6cz8NupF"   # chiave pubblica (Site Key) di Cloudflare Turnstile
NOLEGGIO_MAX_GIORNI = 30   # come MAX_GIORNI in scripts/noleggio/worker.js


def inventario_noleggio():
    return json.load(open(os.path.join(ROOT, "data", "noleggio-inventario.json"), encoding="utf-8"))["gruppi"]


def nome_l(d, chiave="nome"):
    """Nome di un gruppo o articolo dell'inventario nella lingua corrente (campi de/en, altrimenti l'italiano)."""
    return (LINGUA["lang"] != "it" and d.get(LINGUA["lang"])) or d[chiave]


def noleggio():
    gruppi = inventario_noleggio()
    mail = f'<a href="mailto:{NOLEGGIO_MAIL}">{NOLEGGIO_MAIL}</a>'
    rows = [(tr("In breve", "Kurz gesagt", "In short"), tr(
                "Scegli le date e il materiale nel modulo qui sotto: vedi subito cosa è libero. La conferma alla tua richiesta avverrà tramite e-mail. Si paga in contanti o TWINT alla riconsegna.",
                "Wählen Sie im Formular unten die Daten und das Material: Sie sehen sofort, was frei ist. Die Bestätigung Ihrer Anfrage erhalten Sie per E-Mail. Bezahlt wird bei der Rückgabe, bar oder mit TWINT.",
                "Choose the dates and the equipment in the form below: you see straight away what is free. Your request will be confirmed by e-mail. Payment in cash or by TWINT on return.")),
            (tr("Richiesta", "Anfrage", "Request"), tr("Di preferenza una settimana prima dell’attività", "Wenn möglich eine Woche vor der Aktivität", "Preferably a week before the activity")),
            (tr("Durata", "Dauer", "Duration"), tr(f"Da 1 a {NOLEGGIO_MAX_GIORNI} giorni: il prezzo è per giorno di noleggio",
                                                   f"1 bis {NOLEGGIO_MAX_GIORNI} Tage: Der Preis gilt pro Miettag",
                                                   f"1 to {NOLEGGIO_MAX_GIORNI} days: the price is per day of hire")),
            (tr("Ritiro e riconsegna", "Abholung und Rückgabe", "Pick-up and return"), tr(
                "Al magazzino di Manno, al giorno e all’orario indicato nella conferma", "Im Lager in Manno, an dem Tag und zu der Zeit, die in der Bestätigung stehen",
                "At the store in Manno, on the day and at the time given in the confirmation")),
            ("E-mail", mail)]
    # dati del modulo nella lingua della pagina: le quantità le dà il servizio, con la disponibilità per le date scelte
    dati = [{"nome": nome_l(g, "gruppo"), "articoli": [
        {"id": a["id"], "nome": nome_l(a), "prezzo": a["prezzo"], "taglie": list(a["taglie"]) if a.get("taglie") else None,
         "set": a.get("set")}
        for a in g["articoli"]]} for g in gruppi]
    dati = json.dumps(dati, ensure_ascii=False).replace("</", "<\\/")
    titolo = tr("Noleggio materiale", "Materialvermietung", "Equipment hire")
    body = page_hero([servizi_crumb(), (titolo, None)], tr("Noleggio", "Materialvermietung", "Equipment hire"), tr(
                         "Materiale in affitto per le attività della sezione e per le uscite private: alpinismo, cascate di ghiaccio, scialpinismo, arrampicata, racchette, escursionismo e bouldering.",
                         "Material zur Miete für die Aktivitäten der Sektion und für private Touren: Hochtouren, Eisfälle, Skitouren, Klettern, Schneeschuhtouren, Wandern und Bouldern.",
                         "Equipment for hire for the section’s activities and for private outings: mountaineering, ice falls, ski touring, climbing, snowshoeing, hiking and bouldering."),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="#richiesta">{tr("Richiedi il materiale", "Material anfragen", "Request equipment")} <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<section class="section" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">{tr("Come funziona", "So funktioniert’s", "How it works")}</h2>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

<section class="section--surface" id="richiesta" aria-labelledby="richiesta-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="richiesta-h" class="h2">{tr("Richiesta", "Anfrage", "Request")}</h2>
<p>{tr("Scegli le date, poi il materiale tra quello ancora libero. Ti rispondiamo per e-mail.",
       "Wählen Sie die Daten, dann das Material, das noch frei ist. Wir antworten Ihnen per E-Mail.",
       "Choose the dates, then the equipment that is still free. We reply by e-mail.")}</p>
</div>
<div>
<p class="nol-alt" id="nol-alt">{tr(f"Per chiedere il materiale scrivi a {mail} indicando le date, gli articoli e le taglie.",
                                    f"Für eine Anfrage schreiben Sie an {mail} mit Daten, Artikeln und Grössen.",
                                    f"To request equipment, write to {mail} with the dates, items and sizes.")}</p>
<form class="nol" id="nol" data-api="{NOLEGGIO_API}" data-sitekey="{NOLEGGIO_TURNSTILE}" data-max-giorni="{NOLEGGIO_MAX_GIORNI}" hidden novalidate>
<fieldset>
<legend class="h3">{tr("1. Quando", "1. Wann", "1. When")}</legend>
<div class="campi">
<label class="campo">{tr("Primo giorno", "Erster Tag", "First day")}<input type="date" name="dal" required></label>
<label class="campo">{tr("Ultimo giorno", "Letzter Tag", "Last day")}<input type="date" name="al" required></label>
</div>
<p class="small" id="nol-giorni" aria-live="polite"></p>
</fieldset>
<fieldset>
<legend class="h3">{tr("2. Materiale", "2. Material", "2. Equipment")}</legend>
<div class="nol-articoli" id="nol-articoli" aria-live="polite"><p class="small">{tr("Scegli prima le date: qui compare il materiale libero.", "Wählen Sie zuerst die Daten: Hier erscheint das freie Material.", "Choose the dates first: the free equipment appears here.")}</p></div>
</fieldset>
<fieldset>
<legend class="h3">{tr("3. I tuoi dati", "3. Ihre Angaben", "3. Your details")}</legend>
<div class="campi">
<label class="campo">{tr("Nome e cognome", "Vor- und Nachname", "Full name")}<input name="nome" autocomplete="name" maxlength="100" required></label>
<label class="campo">{tr("Telefono", "Telefon", "Phone")}<input type="tel" name="telefono" autocomplete="tel" maxlength="40" required></label>
<label class="campo campo--pieno">E-mail<input type="email" name="email" autocomplete="email" maxlength="200" required></label>
<label class="campo campo--pieno">{tr("Note (facoltative)", "Bemerkungen (freiwillig)", "Notes (optional)")}<textarea name="note" rows="3" maxlength="2000" placeholder="{tr("Per esempio l’attività o una domanda", "Zum Beispiel die Aktivität oder eine Frage", "For example the activity or a question")}"></textarea></label>
</div>
</fieldset>
<div class="nol-invio">
<p class="nol-totale" id="nol-totale" aria-live="polite"></p>
<div class="nol-verifica" id="nol-verifica"></div>
<button class="btn btn--primary" type="submit">{tr("Invia la richiesta", "Anfrage senden", "Send request")} <span class="arrow" aria-hidden="true">→</span></button>
<p class="small">{tr('I dati servono solo a gestire il noleggio: <a href="privacy.html#noleggio">protezione dei dati</a>.',
                     'Die Angaben dienen nur der Abwicklung der Miete: <a href="privacy.html#noleggio">Datenschutz</a>.',
                     'Your details are used only to handle the hire: <a href="privacy.html#noleggio">privacy policy</a>.')}</p>
</div>
<p class="nol-esito" id="nol-esito" role="status" tabindex="-1"></p>
</form>
<script type="application/json" id="nol-dati">{dati}</script>
</div>
</div>
</section>

{subnav(SERVIZI_MENU(), L("noleggio.html"))}"""
    return sezione_page("noleggio.html", tr("Noleggio", "Materialvermietung", "Equipment hire") + " | CAS Ticino", tr(
        "Noleggio materiale del CAS Ticino: alpinismo, sci alpinismo, arrampicata, racchette e altro, con ritiro al magazzino di Manno.",
        "Materialvermietung der SAC-Sektion Ticino: Hochtouren, Skitouren, Klettern, Schneeschuhe und mehr, Abholung im Lager in Manno.",
        "Equipment hire from the SAC Ticino Section: mountaineering, ski touring, climbing, snowshoeing and more, collected from the store in Manno."),
        body, scripts=f'<script src="{asset("assets/noleggio.js")}" defer></script>\n')


# ------------------------------------------------------------------ mercatino
# Annunci di materiale tra privati, inseriti dalla redazione (admin/, raccolta «Mercatino») da data/mercatino/*.json:
# campi e scadenza in mercatino_util.py. La pagina si rigenera ogni mattina (update-gite.yml): gli scaduti escono da soli.

MERCATINO_MAIL = "mercatino@casticino.ch"
MERCATINO_MODULO = {"it": """Tipo (vendo / cerco / regalo):
Titolo:
Prezzo:
Luogo:
Descrizione:

Nome:
Contatto da pubblicare (e-mail e/o telefono):

Allego fino a 3 foto.""", "de": """Art (verkaufe / suche / verschenke):
Titel:
Preis:
Ort:
Beschreibung:

Name:
Zu veröffentlichender Kontakt (E-Mail und/oder Telefon):

Ich lege bis zu 3 Fotos bei.""", "en": """Type (for sale / wanted / free):
Title:
Price:
Place:
Description:

Name:
Contact to publish (e-mail and/or phone):

I attach up to 3 photos."""}
# tipi d'annuncio nelle altre lingue (il testo degli annunci resta come è stato scritto)
TIPI_L = {"it": {}, "de": {"Vendo": "Verkaufe", "Cerco": "Suche", "Regalo": "Zu verschenken"},
          "en": {"Vendo": "For sale", "Cerco": "Wanted", "Regalo": "Free"}}


def tipo_l(tipo):
    return TIPI_L[LINGUA["lang"]].get(tipo, tipo)


def data_l(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    mese = MESI_L[LINGUA["lang"]][m - 1]
    return tr(f"{d} {mese} {y}", f"{d}. {mese} {y}", f"{d} {mese} {y}")


def contatto_html(t):
    """Contatto scritto da chi pubblica: e-mail e numeri di telefono diventano link, il resto resta testo."""
    pezzi = []
    for x in re.split(r"\s*(?:,|;|/|\n| oppure | o )\s*", t.strip()):
        if not x:
            continue
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", x, flags=re.I):
            pezzi.append(f'<a href="mailto:{esc(x)}">{esc(x)}</a>')
        elif re.fullmatch(r"\+?[\d ().-]{7,}", x):
            pezzi.append(f'<a href="tel:{re.sub(r"[^0-9+]", "", x)}">{esc(x)}</a>')
        else:
            pezzi.append(esc(x))
    return " · ".join(pezzi)


def prezzo_html(p):
    """Prezzo di un annuncio: un importo semplice diventa «Fr. 300.–» (cifre in Geist Mono); altro testo resta com'è."""
    m = re.fullmatch(r"(?:(?:Fr\.?|CHF|Sfr\.?)\s*)?(\d+(?:['’]\d{3})*)(?:[.,](?:-|–|—|00))?\s*(?:(?:Fr\.?|CHF|franchi))?", p.strip(), re.I)
    if not m:
        return esc(p)
    return f'Fr. <span class="num">{m.group(1)}.–</span>'


def annuncio_html(a):
    nome = os.path.splitext(os.path.basename(a["percorso"]))[0]
    foto = [f for f in a.get("foto") or [] if f and os.path.exists(os.path.join(ROOT, f))][:3]
    fig = ""
    if foto:
        w, h = webp_size(os.path.join(ROOT, foto[0])) if foto[0].endswith(".webp") else (1200, 900)
        altre = "".join(f'<a href="{esc(f)}" aria-label="{tr("Foto", "Foto", "Photo")} {i + 2} {tr("di", "von", "of")} «{esc(a["title"])}»"><img src="{esc(f)}" alt="" loading="lazy" decoding="async"></a>'
                        for i, f in enumerate(foto[1:]))
        fig = f"""<figure class="annuncio-foto">
<a href="{esc(foto[0])}"><img src="{esc(foto[0])}" alt="{esc(a['title'])}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>
{f'<div class="annuncio-altre">{altre}</div>' if altre else ""}
</figure>"""
    tipo = a.get("tipo") if a.get("tipo") in mercatino_util.TIPI else "Vendo"
    testo = "".join(f"<p>{esc(par).replace(chr(10), '<br>')}</p>" for par in re.split(r"\n\s*\n", (a.get("testo") or "").strip()) if par.strip())
    meta = " · ".join(filter(None, [esc(a.get("luogo") or ""), tr("pubblicato il", "veröffentlicht am", "published on") + " " + data_l(a["date"][:10])]))
    it = ' lang="it"' if LINGUA["lang"] != "it" else ""  # titolo e testo restano come li ha scritti chi pubblica
    contatto = "".join(filter(None, [esc(a["nome"]) + (": " if a.get("contatto") else "") if a.get("nome") else "",
                                     contatto_html(a["contatto"]) if a.get("contatto") else ""]))
    return f"""<article class="annuncio" id="{nome}" data-ruoli="{tipo.lower()}" data-scade="{mercatino_util.scadenza(a)}">
{fig}
<div class="annuncio-corpo">
<p class="annuncio-tipo annuncio-tipo--{tipo.lower()}">{tipo_l(tipo)}</p>
<h2 class="annuncio-titolo"{it}>{esc(a['title'])}</h2>
{f'<p class="annuncio-prezzo">{prezzo_html(a["prezzo"])}</p>' if a.get("prezzo") else ""}
{f'<div class="annuncio-testo"{it}>{testo}</div>' if testo else ""}
<p class="small">{meta}</p>
{f'<p class="annuncio-contatto">{contatto}</p>' if contatto else ""}
</div>
</article>"""


def mercatino():
    annunci = mercatino_util.attivi()
    conta = {t: sum(1 for a in annunci if (a.get("tipo") if a.get("tipo") in mercatino_util.TIPI else "Vendo") == t) for t in mercatino_util.TIPI}
    oggetto = tr("Annuncio per il mercatino", "Inserat für den Marktplatz", "Listing for the gear market")
    mailto = f"mailto:{MERCATINO_MAIL}?subject={quote(oggetto)}&body={quote(MERCATINO_MODULO[LINGUA['lang']])}"
    bottone = f'<a class="btn btn--primary" href="{esc(mailto)}">{tr("Pubblica un annuncio", "Inserat aufgeben", "Post a listing")} <span class="arrow" aria-hidden="true">→</span></a>'
    if annunci:
        filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">{tr("Tutti", "Alle", "All")} <span class="num">{len(annunci)}</span></button>'] +
                           [f'<button type="button" data-filtro="{t.lower()}" aria-pressed="false">{tipo_l(t)} <span class="num">{conta[t]}</span></button>'
                            for t in mercatino_util.TIPI if conta[t]])
        elenco = f"""<div class="filtro" role="group" aria-label="{tr("Filtra per tipo di annuncio", "Nach Art filtern", "Filter by type")}" data-filtra="#annunci" data-uno="{tr("annuncio", "Inserat", "listing")}" data-molti="{tr("annunci", "Inserate", "listings")}" hidden>
{filtri}
</div>
<p class="small filtro-stato" id="filtro-stato" aria-live="polite"></p>
<div class="annunci" id="annunci">
{chr(10).join(annuncio_html(a) for a in annunci)}
</div>"""
    else:
        elenco = f"""<div class="callout">
<p>{tr("<strong>Al momento non ci sono annunci.</strong> Hai dell’attrezzatura che non usi più, o cerchi qualcosa? Mandaci il tuo annuncio.",
       "<strong>Im Moment gibt es keine Inserate.</strong> Haben Sie Ausrüstung, die Sie nicht mehr brauchen, oder suchen Sie etwas? Senden Sie uns Ihr Inserat.",
       "<strong>There are no listings at the moment.</strong> Have some gear you no longer use, or looking for something? Send us your listing.")}</p>
{bottone.replace("btn--primary", "btn--secondary")}
</div>"""
    mail = f'<a href="{esc(mailto)}">{MERCATINO_MAIL}</a>'
    mesi = mercatino_util.GIORNI_DEFAULT // 30
    rows = [(tr("Cosa", "Was", "What"), tr("Materiale e abbigliamento per la montagna, da vendere, cercare o regalare tra privati.",
                                         "Bergausrüstung und -bekleidung, die Private verkaufen, suchen oder verschenken.",
                                         "Mountain gear and clothing to sell, find or give away between private people.")),
            (tr("Come", "Wie", "How"), tr(f"Scrivi a {mail} con tipo, titolo, prezzo, luogo, descrizione, il contatto da pubblicare e fino a 3 foto: la redazione lo mette online.",
                                        f"Schreiben Sie an {mail} mit Art, Titel, Preis, Ort, Beschreibung, dem zu veröffentlichenden Kontakt und bis zu 3 Fotos: Die Redaktion schaltet das Inserat auf.",
                                        f"Write to {mail} with type, title, price, place, description, the contact to publish and up to 3 photos: the editors put it online.")),
            (tr("Durata", "Dauer", "Duration"), tr(f"Ogni annuncio resta online {mesi} mesi. Se l’oggetto è venduto, trovato o regalato prima, avvisaci e lo togliamo.",
                                                  f"Jedes Inserat bleibt {mesi} Monate online. Ist der Gegenstand vorher verkauft, gefunden oder verschenkt, melden Sie es uns und wir entfernen es.",
                                                  f"Each listing stays online for {mesi} months. If the item is sold, found or given away sooner, let us know and we will remove it.")),
            (tr("Costo", "Kosten", "Cost"), tr("Gratuito", "Gratis", "Free")),
            (tr("Trattative", "Abwicklung", "Deals"), tr("Si accordano direttamente le persone interessate: la sezione pubblica gli annunci ma non partecipa alla vendita e non risponde del materiale.",
                                                         "Die Interessierten einigen sich direkt: Die Sektion veröffentlicht die Inserate, ist aber nicht am Verkauf beteiligt und haftet nicht für das Material.",
                                                         "The people concerned deal directly with each other: the section publishes the listings but takes no part in the sale and is not liable for the gear."))]
    titolo = tr("Mercatino", "Marktplatz", "Gear market")
    body = page_hero([servizi_crumb(), (titolo, None)], titolo, tr(
                         "Attrezzatura di montagna tra soci e appassionati: vendo, cerco, regalo. Dai una seconda vita al materiale che non usi più.",
                         "Bergausrüstung unter Mitgliedern und Bergbegeisterten: verkaufen, suchen, verschenken. Die Inserate erscheinen so, wie sie geschrieben wurden, meist auf Italienisch.",
                         "Mountain gear between members and enthusiasts: for sale, wanted, free. Listings appear as they were written, mostly in Italian."),
                     f'<div class="actions hero-actions">{bottone}</div>') + f"""

<section class="section" aria-label="{tr("Annunci", "Inserate", "Listings")}">
<div class="container">
{elenco}
</div>
</section>

<section class="section--surface" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">{tr("Come funziona", "So funktioniert’s", "How it works")}</h2>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav(SERVIZI_MENU(), L("mercatino.html"))}"""
    return sezione_page("mercatino.html", titolo + " | CAS Ticino", tr(
        "Il mercatino del CAS Ticino: annunci di attrezzatura di montagna tra privati, da vendere, cercare o regalare.",
        "Der Marktplatz der SAC-Sektion Ticino: Inserate für Bergausrüstung unter Privaten, zum Verkaufen, Suchen oder Verschenken.",
        "The SAC Ticino Section’s gear market: listings of mountain gear between private people, for sale, wanted or free."), body)


# ------------------------------------------------------------------ versioni tradotte (de/, en/)
# Solo La Sezione, le capanne e Adesione sono tradotte; news, attività, media e PDF restano in italiano.
# I testi sono scritti con i percorsi dalla radice del sito; i link alle pagine tradotte passano da L() (de/…, en/…).
# Home, Introduzione, Sede e Adesione hanno un testo proprio per lingua in TRADOTTE; le altre pagine della sezione
# usano le stesse funzioni dell'italiano (comitato(), storia()…), con tr() e i dizionari *_DE / *_EN.

TRADOTTE = {
    "de": dict(
        # home
        home_title="CAS Ticino | Schweizer Alpen-Club, Sektion Ticino",
        home_desc="Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter. Seit über hundert Jahren das Zuhause des Tessiner Alpinismus.",
        hero_h="In die Berge<br>mit <span class=\"accent\">uns</span>.",
        hero_lead="Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter.",
        diventa="Mitglied werden",
        hero_alt="Skitourengeher im Aufstieg zu einem verschneiten Dorf",
        cifre="Die Sektion in Zahlen",
        sezione="Die Sektion",
        capanne_h="Sechs Hütten, ein Tessin",
        capanne_lead="Immer offen, bewartet, wenn die Hüttenwarte da sind. Melden Sie sich vor dem Aufbruch beim Hüttenwart, um Anwesenheit und Verhältnisse am Berg zu prüfen.",
        accesso="Zugang ab",
        cta_h="Kommen Sie mit.",
        cta_p="Günstigere Preise in den SAC-Hütten der ganzen Schweiz, Kurse, Touren und eine Gemeinschaft, die die Berge so liebt wie Sie.",
        # introduzione
        intro_crumb="Über uns", intro_h="Die Sektion",
        intro_lead="Am 11. April 1886 in Bellinzona gegründet, zählt die Sektion Ticino des Schweizer Alpen-Clubs fast 3000 Mitglieder und bietet ein vielfältiges Programm für jedes Alter: von den Jüngsten bis zu den Senioren.",
        intro_alt="Eine Gruppe Bergsteiger unterwegs auf einem Gletscher",
        stat_intro=["am 11. April in Bellinzona gegründet", "Mitglieder, von den Jüngsten bis zu den Senioren", "Hütten im Besitz der Sektion", "Ressorts neben dem Vorstand"],
        cosa_h="In den Bergen,<br>zu jeder Jahreszeit",
        alt_cresta="Bergsteiger auf einem Felsgrat",
        discipline_h="Disziplinen", discipline_p="Wandern, Bergsteigen, Klettern, Skitouren, Schneeschuhwandern und Eisklettern.",
        inizia_h="Für Einsteiger", inizia_p="Einführungskurse in Bergsteigen, Skitouren, Schneeschuhwandern und Klettern im Gelände.",
        vedi_corsi="Zu den Kursen",
        alt_montebar="Die Capanna Monte Bar",
        capanne_h3="Hütten", capanne_p="Die Sektion besitzt sechs Hütten: {huts}.", e="und",
        oltre_h="Mehr als Sport", oltre_p="Sie koordiniert die Bergrettung im Sottoceneri, setzt sich für den Schutz der alpinen Umwelt ein und fördert die Bergkultur.",
        come_h="So funktioniert es",
        come_p="Ein <a href=\"de/comitato.html\">Vorstand</a> koordiniert die verschiedenen Aktivitäten, unterstützt von fünf <a href=\"de/organizzazione.html\">Ressorts</a> und der Freiwilligenarbeit der Mitglieder.",
        alt_racchette="Verschneiter Grat über einem Nebelmeer",
        com_h="Kommunikation", com_p="Tourenprogramm, Website, ein halbjährliches Bulletin und das Jahrbuch, das vom Leben der Sektion erzählt (auf Italienisch).",
        doc_h="Statuten, Vision und Strategie, Organigramm",
        doc_p="Die massgebenden Dokumente der Sektion, als PDF auf Italienisch. Weitere finden Sie auf der Seite <a href=\"documenti.html\">Dokumente</a>.",
        statuto="Statuten", visione="Vision und Strategie", organigramma="Organigramm",
        intro_title="Die Sektion | CAS Ticino",
        intro_desc="Die Sektion Ticino des Schweizer Alpen-Clubs: 1886 gegründet, fast 3000 Mitglieder, sechs Hütten, Kurse, Touren und Aktivitäten für jedes Alter.",
        # sede
        sede_rows=[
            ("Postadresse", "Schweizer Alpen-Club<br>Sektion Ticino<br>Postfach 112<br>6998 Monteggio 2"),
            ("E-Mail", '<a href="mailto:info@casticino.ch">info@casticino.ch</a>'),
            ("Sitz", "Gebäude Canvetto Luganese, Molino Nuovo (Lugano)<br>2. Stock, auf der Galerie"),
            ("Bibliothek", 'Führer und Karten zum Nachschlagen, Bücher zum Ausleihen; Bücher und T-Shirts zu kaufen. Für einen Besuch schreiben Sie dem Sekretariat: <a href="mailto:info@casticino.ch">info@casticino.ch</a>.'),
            ("Bankverbindung", f'Banca Stato, Lugano<br><span class="num">IBAN {IBAN}</span>'),
        ],
        sede_crumb="Sitz und Kontakt",
        sede_lead="Der Sitz der Sektion befindet sich im Gebäude Canvetto Luganese in Molino Nuovo, mit Büro und Sitzungszimmer im zweiten Stock auf der Galerie.",
        sede_h="Der Canvetto Luganese",
        sede_p="Hier treffen sich der Vorstand und die Ressorts, hier finden die Informationsabende der Kurse und verschiedene kulturelle Anlässe statt: Bilder von Touren, Reisen und Expeditionen der Mitglieder, Abende mit Fachleuten für Wetter, Lawinen und Erste Hilfe.",
        scrivi="Der Sektion schreiben",
        sede_title="Sitz und Kontakt | CAS Ticino",
        sede_desc="Sitz des CAS Ticino im Canvetto Luganese (Molino Nuovo), Postadresse, E-Mail, Bibliothek und Bankverbindung.",
        # adesione
        prezzi=[("Einzel", "Einzelmitglied", "105", "30"),
                ("Familie", "Eltern und Kinder bis 17 Jahre", "179", "50"),
                ("Jugend", "Bis 22 Jahre", "50", "30")],
        tassa="+ CHF {fee} beim ersten Beitritt",
        vantaggi=[("Hütten", "Bis 50 % Rabatt in den Hütten der ganzen Schweiz und in einigen europäischen Ländern"),
                  ("Tourenportal", "Kostenloser Zugang zu Karten und Routen im SAC-Tourenportal"),
                  ("Ausbildung", "Vergünstigungen bei den Kursen"),
                  ("Publikationen", "Die Zeitschrift «Die Alpen», das Bulletin der Sektion und Rabatte auf SAC-Publikationen"),
                  ("Klettern", "Freier Eintritt in die Kletterhalle San Paolo"),
                  ("Digitaler Ausweis", 'Der Mitgliederausweis ist auch in der App SAC-CAS (<a href="https://apps.apple.com/ch/app/sac-cas/id1592646841" rel="noopener">App Store</a>, <a href="https://play.google.com/store/apps/details?id=ch.sac_cas" rel="noopener">Google Play</a>): Anmeldung mit dem SAC-Konto, funktioniert auch offline, der QR-Code gilt in den Hütten')],
        join="https://portal.sac-cas.ch/de/groups/6783/self_registration",
        ade_crumb="Mitgliedschaft", ade_h="Mitglied werden",
        ade_lead="Treten Sie der Tessiner Sektion des Schweizer Alpen-Clubs bei: Touren, Kurse, Hütten und eine Gemeinschaft, die die Berge liebt.",
        iscriviti="Auf der SAC-Website beitreten",
        ade_alt="Bergsee zwischen Felsen, im Hintergrund die Berge",
        quote_h="Jahresbeiträge",
        doppia="Sie sind schon Mitglied einer anderen SAC-Sektion? Sie können eine Doppelmitgliedschaft beantragen und zahlen nur den Beitrag der Sektion Ticino.",
        vantaggi_h="Ihre Vorteile",
        ade_title="Mitglied werden | CAS Ticino",
        ade_desc="Werden Sie Mitglied der Sektion Ticino des Schweizer Alpen-Clubs: Jahresbeiträge für Einzelne, Familien und Jugendliche, und die Vorteile für Mitglieder.",
    ),
    "en": dict(
        home_title="CAS Ticino | Swiss Alpine Club, Ticino Section",
        home_desc="Six huts from the Cristallina Pass to the Denti della Vecchia, courses run by professionals and a trip programme for all ages. For more than a century, the home of mountaineering in Ticino.",
        hero_h="Into the mountains<br>with <span class=\"accent\">us</span>.",
        hero_lead="Six huts from the Cristallina Pass to the Denti della Vecchia, courses run by professionals and a trip programme for all ages.",
        diventa="Become a member",
        hero_alt="Ski tourers climbing towards a snow-covered village",
        cifre="The section in numbers",
        sezione="The Section",
        capanne_h="Six huts, one Ticino",
        capanne_lead="Always open, staffed when the hut keepers are there. Check with the hut keeper before you set out, to make sure they are there and to ask about conditions in the mountains.",
        accesso="Access from",
        cta_h="Come with us.",
        cta_p="Lower rates in SAC huts all over Switzerland, courses, trips and a community that loves the mountains as much as you do.",
        intro_crumb="About us", intro_h="The section",
        intro_lead="Founded in Bellinzona on 11 April 1886, the Ticino Section of the Swiss Alpine Club has almost 3000 members and offers a varied programme for all ages: from the youngest to seniors.",
        intro_alt="A group of climbers walking on a glacier",
        stat_intro=["founded in Bellinzona on 11 April", "members, from the youngest to seniors", "huts owned by the section", "departments alongside the committee"],
        cosa_h="In the mountains,<br>in every season",
        alt_cresta="Climbers on a rocky ridge",
        discipline_h="Disciplines", discipline_p="Hiking, mountaineering, climbing, ski touring, snowshoeing and ice climbing.",
        inizia_h="For beginners", inizia_p="Introductory courses in mountaineering, ski touring, snowshoeing and outdoor climbing.",
        vedi_corsi="See the courses",
        alt_montebar="Capanna Monte Bar",
        capanne_h3="Huts", capanne_p="The section owns six huts: {huts}.", e="and",
        oltre_h="Beyond sport", oltre_p="It coordinates mountain rescue in the Sottoceneri, works to protect the alpine environment and promotes mountain culture.",
        come_h="How it works",
        come_p="A <a href=\"en/comitato.html\">committee</a> coordinates the various activities, supported by five <a href=\"en/organizzazione.html\">departments</a> and the volunteer work of the members.",
        alt_racchette="Snowy ridge above a sea of clouds",
        com_h="Communication", com_p="Trip programme, website, a half-yearly bulletin and the yearbook that tells the story of the section (in Italian).",
        doc_h="Statutes, vision and strategy, organisation chart",
        doc_p="The section’s key documents, as PDFs in Italian. You will find more on the <a href=\"documenti.html\">Documents</a> page.",
        statuto="Statutes", visione="Vision and strategy", organigramma="Organisation chart",
        intro_title="The section | CAS Ticino",
        intro_desc="The Ticino Section of the Swiss Alpine Club: founded in 1886, almost 3000 members, six huts, courses, trips and activities for all ages.",
        sede_rows=[
            ("Postal address", "Swiss Alpine Club<br>Ticino Section<br>PO Box 112<br>6998 Monteggio 2"),
            ("E-mail", '<a href="mailto:info@casticino.ch">info@casticino.ch</a>'),
            ("Office", "Canvetto Luganese building, Molino Nuovo (Lugano)<br>2nd floor, on the gallery"),
            ("Library", 'Guidebooks and maps to consult, books to borrow; books and T-shirts for sale. To visit, write to the secretariat: <a href="mailto:info@casticino.ch">info@casticino.ch</a>.'),
            ("Bank details", f'Banca Stato, Lugano<br><span class="num">IBAN {IBAN}</span>'),
        ],
        sede_crumb="Office and contacts",
        sede_lead="The section’s office is in the Canvetto Luganese building in Molino Nuovo, with an office and meeting room on the second floor, on the gallery.",
        sede_h="The Canvetto Luganese",
        sede_p="This is where the committee and the departments meet, and where course information evenings and various cultural events take place: talks on members’ trips, travels and expeditions, and evenings with experts on weather, avalanches and first aid.",
        scrivi="Write to the section",
        sede_title="Office and contacts | CAS Ticino",
        sede_desc="The CAS Ticino office at the Canvetto Luganese (Molino Nuovo), postal address, e-mail, library and bank details.",
        prezzi=[("Individual", "Individual member", "105", "30"),
                ("Family", "Parents and children up to 17", "179", "50"),
                ("Youth", "Up to 22", "50", "30")],
        tassa="+ CHF {fee} when you first join",
        vantaggi=[("Huts", "Up to 50% off in huts all over Switzerland and in some European countries"),
                  ("Tour portal", "Free access to maps and routes on the SAC tour portal"),
                  ("Training", "Reduced prices on courses"),
                  ("Publications", "The SAC magazine “Die Alpen”, the section bulletin and discounts on SAC publications"),
                  ("Climbing", "Free entry to the San Paolo climbing gym"),
                  ("Digital card", 'Your membership card is also in the SAC-CAS app (<a href="https://apps.apple.com/ch/app/sac-cas/id1592646841" rel="noopener">App Store</a>, <a href="https://play.google.com/store/apps/details?id=ch.sac_cas" rel="noopener">Google Play</a>): log in with your SAC account; it works offline and the QR code is accepted in the huts')],
        join="https://portal.sac-cas.ch/it/groups/6783/self_registration",
        ade_crumb="Membership", ade_h="Become a member",
        ade_lead="Join the Ticino Section of the Swiss Alpine Club: trips, courses, huts and a community that loves the mountains.",
        iscriviti="Join on the SAC website",
        ade_alt="Mountain lake among rocks, with mountains behind",
        quote_h="Annual fees",
        doppia="Already a member of another SAC section? You can apply for dual membership and pay only the Ticino Section fee.",
        vantaggi_h="Your benefits",
        ade_title="Become a member | CAS Ticino",
        ade_desc="Become a member of the Ticino Section of the Swiss Alpine Club: annual fees for individuals, families and young people, and the benefits for members.",
    ),
}


def tx_tradotte():
    return TRADOTTE[LINGUA["lang"]]


def introduzione_tradotta():
    tx = tx_tradotte()
    lang = LINGUA["lang"]
    huts = (f'<a href="{lang}/campotencia.html">Campo Tencia</a>, <a href="{lang}/cristallina.html">Cristallina</a>, <a href="{lang}/adula.html">Adula</a>, '
            f'<a href="{lang}/motterascio.html">Motterascio (Michela)</a>, <a href="{lang}/montebar.html">Monte Bar</a> {tx["e"]} <a href="{lang}/baitadelluca.html">Baita del Luca</a>')
    stats = "\n".join(f'<div class="stat"><strong>{n}</strong><span>{num(x)}</span></div>'
                      for n, x in zip(("1886", "3000", "6", "5"), tx["stat_intro"]))
    body = page_hero([(tx["sezione"], f"{lang}/introduzione.html"), (tx["intro_crumb"], None)], tx["intro_h"], tx["intro_lead"]) + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", tx['intro_alt'], mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
{credito()}
</figure>

<section class="section--accent" aria-label="{tx['cifre']}">
<div class="container">
<div class="stats" data-reveal>
{stats}
</div>
</div>
</section>

<section class="section" aria-labelledby="cosa-h">
<div class="container">
<div class="section-head">
<h2 id="cosa-h" class="h2">{tx['cosa_h']}</h2>
</div>
<div class="pillars" data-reveal>
<article class="pillar pillar--photo pillar--wide">
{img("paesaggi/cresta-lugano-2000", tx['alt_cresta'], 2000, 580)}
<h3>{tx['discipline_h']}</h3>
<p>{tx['discipline_p']}</p>
</article>
<article class="pillar pillar--accent">
<h3>{tx['inizia_h']}</h3>
<p>{tx['inizia_p']}</p>
<a class="link" href="corsi.html">{tx['vedi_corsi']}</a>
</article>
<article class="pillar pillar--photo">
{img("capanne/montebar-3x2", tx['alt_montebar'], 663, 442)}
<h3>{tx['capanne_h3']}</h3>
<p>{tx['capanne_p'].format(huts=huts)}</p>
</article>
<article class="pillar">
<h3>{tx['oltre_h']}</h3>
<p>{tx['oltre_p']}</p>
</article>
<article class="pillar">
<h3>{tx['come_h']}</h3>
<p>{tx['come_p']}</p>
</article>
<article class="pillar pillar--photo pillar--wide-md">
{img("corsi/racchette-4x5", tx['alt_racchette'], 800, 1000)}
<h3>{tx['com_h']}</h3>
<p>{tx['com_p']}</p>
</article>
<article class="pillar pillar--dark pillar--wide">
<h3>{tx['doc_h']}</h3>
<p>{tx['doc_p']}</p>
<div class="actions"><a class="btn btn--primary" href="{DOC}statuto-visione/statuto-2025.pdf">{tx['statuto']} <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/visione-strategia-2025.pdf">{tx['visione']}</a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/organigramma-2025.pdf">{tx['organigramma']}</a></div>
</article>
</div>
</div>
</section>

{subnav(tx["sezione"], f"{lang}/introduzione.html")}"""
    return sezione_page("introduzione.html", tx["intro_title"], tx["intro_desc"], body, og="paesaggi/gruppo-ghiacciaio-2000")


def sede_tradotta():
    tx = tx_tradotte()
    lang = LINGUA["lang"]
    body = page_hero([(tx["sezione"], f"{lang}/introduzione.html"), (tx["sede_crumb"], None)], tx["sede_crumb"], tx["sede_lead"]) + f"""

<section class="section" aria-labelledby="sede-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="sede-h" class="h2">{tx['sede_h']}</h2>
<p>{tx['sede_p']}</p>
<div><a class="btn btn--primary" href="mailto:info@casticino.ch">{tx['scrivi']} <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
{facts(tx['sede_rows'])}
</div>
</div>
</section>

{rubrica()}

{subnav(tx["sezione"], f"{lang}/sede.html")}"""
    return sezione_page("sede.html", tx["sede_title"], tx["sede_desc"], body)


def adesione_tradotta():
    tx = tx_tradotte()
    cards = "\n".join(f"""<article class="price">
<h3 class="h3">{t}</h3>
<p>{who}</p>
<div class="amount"><small>CHF</small>{amt}</div>
<p class="small">{tx['tassa'].format(fee=fee)}</p>
</article>""" for t, who, amt, fee in tx["prezzi"])
    join = tx["join"]
    body = page_hero([(tx["ade_crumb"], None)], tx["ade_h"], tx["ade_lead"],
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{join}">{tx["iscriviti"]} <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<figure class="band">
{pic("paesaggi/laghetto-alpino", tx['ade_alt'], mobile="paesaggi/laghetto-alpino-4x3", w=2000, h=1126, lazy=False)}
{credito()}
</figure>

<section class="section" aria-labelledby="quote-h">
<div class="container">
<div class="section-head"><h2 id="quote-h" class="h2">{tx['quote_h']}</h2></div>
<div class="prices" data-reveal>
{cards}
</div>
<p class="note">{tx['doppia']}</p>
</div>
</section>

<section class="section--surface" aria-labelledby="vantaggi-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="vantaggi-h" class="h2">{tx['vantaggi_h']}</h2>
<div><a class="btn btn--primary" href="{join}">{tx['iscriviti']} <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(tx['vantaggi'])}
</div>
</div>
</section>"""
    return sezione_page("adesione.html", tx["ade_title"], tx["ade_desc"], body, og="paesaggi/laghetto-alpino-2000")


# ------------------------------------------------------------------ ricerca

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


def prima_di_partire():
    """Riquadro «Prima di partire» (Partecipare, Corsi, Programma gite): bollettino valanghe, meteo, pianificazione,
    cartina e numeri d'emergenza. Solo link: nessun servizio esterno viene caricato nella pagina."""
    lang = LINGUA["lang"]
    voci = [
        (tr("Bollettino valanghe", "Lawinenbulletin", "Avalanche bulletin"),
         tr("SLF, la situazione del manto nevoso in tutta la Svizzera", "SLF, die Schneedecke in der ganzen Schweiz", "SLF, the snowpack across Switzerland"),
         {"it": "https://www.slf.ch/it/bollettino-valanghe-e-situazione-nivologica/", "de": "https://www.slf.ch/de/lawinenbulletin-und-schneesituation/",
          "en": "https://www.slf.ch/en/avalanche-bulletin-and-snow-situation/"}[lang]),
        (tr("Meteo", "Wetter", "Weather"), tr("MeteoSvizzera, previsioni e allerte", "MeteoSchweiz, Prognosen und Warnungen", "MeteoSwiss, forecasts and warnings"),
         {"it": "https://www.meteosvizzera.admin.ch/", "de": "https://www.meteoschweiz.admin.ch/", "en": "https://www.meteoswiss.admin.ch/"}[lang]),
        ("White Risk", tr("Pianificare le gite invernali e imparare a valutare il pericolo valanghe",
                          "Wintertouren planen und die Lawinengefahr beurteilen lernen", "Plan winter tours and learn to judge avalanche danger"),
         f"https://whiterisk.ch/{lang}"),
        (tr("Cartina", "Karte", "Map"), tr("swisstopo, carte nazionali, pendenze e itinerari", "swisstopo, Landeskarten, Hangneigung und Routen",
                                            "swisstopo, national maps, slope angles and routes"), f"https://map.geo.admin.ch/?lang={lang}"),
    ]
    links = "\n".join(f'<a href="{u}" rel="noopener"><span><strong>{t_}</strong> <span class="partenza-nota">{nota}</span></span>'
                       f'<span class="tag">{u.split("/")[2].removeprefix("www.")}</span></a>' for t_, nota, u in voci)
    numeri = [("1414", tr("Rega, soccorso aereo", "Rega, Luftrettung", "Rega, air rescue")),
              ("144", tr("Ambulanza", "Sanitätsnotruf", "Ambulance")),
              ("112", tr("Numero d’emergenza europeo", "Europäische Notrufnummer", "European emergency number"))]
    numeri = "\n".join(f'<a href="tel:{n}"><strong class="num">{n}</strong><span>{x}</span></a>' for n, x in numeri)
    return f"""<section class="section" id="prima-di-partire" aria-labelledby="partire-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="partire-h" class="h2">{tr("Prima di partire", "Vor dem Aufbruch", "Before you set off")}</h2>
<p>{tr("Controlla meteo e bollettino valanghe la sera prima e la mattina stessa, e scegli la gita in base alle condizioni, non solo alla meta.",
       "Prüfen Sie Wetter und Lawinenbulletin am Vorabend und am Morgen selbst, und wählen Sie die Tour nach den Verhältnissen, nicht nur nach dem Ziel.",
       "Check the weather and the avalanche bulletin the evening before and on the morning itself, and choose the trip by the conditions, not just the destination.")}</p>
</div>
<div class="stack" data-reveal>
<div class="linklist">
{links}
</div>
<div class="emergenza">
<h3 class="label">{tr("In caso di emergenza", "Im Notfall", "In an emergency")}</h3>
<div class="emergenza-numeri">
{numeri}
</div>
<p class="small">{tr("Con l’app della Rega l’allarme trasmette anche la tua posizione.", "Mit der Rega-App übermittelt der Alarm auch Ihren Standort.",
                     "With the Rega app, the alarm also sends your location.")} <a href="{tr("https://www.rega.ch/it/", "https://www.rega.ch/", "https://www.rega.ch/en/")}" rel="noopener">{tr("App Rega", "Rega-App", "Rega app")}</a></p>
</div>
</div>
</div>
</section>"""


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


REGOLAMENTO_GITE = DOC + "statuto-visione/regolamento-gite-2026.pdf"


def partecipare():
    """Le regole per chi partecipa alle gite, in breve, dal regolamento gite (docs/statuto-visione/regolamento-gite-*.pdf):
    quando cambia il regolamento, aggiornare anche questo testo (nelle tre lingue)."""
    nomi = {"it": {}, "de": DOCS_DE, "en": DOCS_EN}[LINGUA["lang"]]
    scale = ", ".join(f'<a href="{h}">{nomi.get(l, l).lower() if LINGUA["lang"] != "de" else nomi.get(l, l)}</a>' for l, h in DOCS[1][1])
    sezioni = [
        blocco("prima-h", tr("Prima di iscriverti", "Vor der Anmeldung", "Before you register"),
               tr("Le gite sono aperte a tutti, anche a chi non è socio. Scegli quelle adatte a te.",
                  "Die Touren stehen allen offen, auch Nichtmitgliedern. Wählen Sie diejenigen, die zu Ihnen passen.",
                  "Trips are open to everyone, members or not. Choose the ones that suit you."),
               tr(f"""<p>Per ogni gita il programma indica le esigenze tecniche e di condizione fisica, l’itinerario in breve, l’equipaggiamento necessario e il numero massimo di partecipanti. Le difficoltà seguono le scale del CAS: {scale}.</p>
<ul>
<li>Devi avere la preparazione tecnica e fisica richiesta dalla gita.</li>
<li>Alcune gite chiedono una gita di preparazione o un corso; il capogita può chiederti le tue gite recenti.</li>
<li>Le attività del gruppo giovani hanno limiti d’età.</li>
<li>Per qualsiasi dubbio scrivi al capogita, dalla pagina della gita.</li>
</ul>""", f"""<p>Für jede Tour nennt das Programm die technischen und konditionellen Anforderungen, die Route in Kürze, die nötige Ausrüstung und die maximale Teilnehmerzahl. Die Schwierigkeiten folgen den Skalen des SAC (PDF, italienisch): {scale}.</p>
<ul>
<li>Sie müssen die technische und körperliche Vorbereitung mitbringen, die die Tour verlangt.</li>
<li>Einige Touren setzen eine Vorbereitungstour oder einen Kurs voraus; die Tourenleitung kann nach Ihren letzten Touren fragen.</li>
<li>Die Aktivitäten der Jugendgruppe haben Altersgrenzen.</li>
<li>Bei Fragen schreiben Sie der Tourenleitung, über die Seite der Tour.</li>
</ul>""", f"""<p>For each trip the programme gives the technical and fitness requirements, a short description of the route, the equipment needed and the maximum number of participants. Difficulty follows the SAC scales (PDF, in Italian): {scale}.</p>
<ul>
<li>You must have the technical and physical preparation the trip requires.</li>
<li>Some trips require a preparatory trip or a course; the trip leader may ask about your recent trips.</li>
<li>Youth group activities have age limits.</li>
<li>If in doubt, write to the trip leader from the trip’s page.</li>
</ul>""")),
        blocco("iscrizione-h", tr("Iscrizione e conferma", "Anmeldung und Bestätigung", "Registration and confirmation"),
               tr("Ci si iscrive su Droptour, nei termini indicati per ogni gita.", "Angemeldet wird auf Droptour, innerhalb der Fristen jeder Tour.", "You register on Droptour, within the deadlines given for each trip."),
               tr("""<ul>
<li>I posti vengono assegnati in ordine d’iscrizione, con la precedenza ai soci della sezione e poi ai soci di altre associazioni alpinistiche con cui vale la reciprocità.</li>
<li>Al più tardi 20 giorni prima della gita il capogita conferma l’iscrizione su Droptour: <strong>sei iscritto solo quando ricevi la conferma per e-mail</strong>.</li>
<li>Nella settimana prima della gita il capogita manda i dettagli ai partecipanti.</li>
<li>Se non puoi più partecipare, avvisa subito i capigita: il posto passa a chi è in lista d’attesa.</li>
</ul>""", """<ul>
<li>Die Plätze werden nach Anmeldeeingang vergeben, mit Vorrang für Mitglieder der Sektion und danach für Mitglieder anderer Bergsportvereine mit Gegenrecht.</li>
<li>Spätestens 20 Tage vor der Tour bestätigt die Tourenleitung die Anmeldung auf Droptour: <strong>Angemeldet sind Sie erst, wenn Sie die Bestätigung per E-Mail erhalten</strong>.</li>
<li>In der Woche vor der Tour schickt die Tourenleitung die Einzelheiten an die Teilnehmenden.</li>
<li>Wenn Sie nicht mehr teilnehmen können, melden Sie es sofort der Tourenleitung: Der Platz geht an jemanden auf der Warteliste.</li>
</ul>""", """<ul>
<li>Places are allocated in order of registration, with priority for section members and then for members of other mountaineering clubs with reciprocal agreements.</li>
<li>No later than 20 days before the trip the leader confirms your registration on Droptour: <strong>you are registered only once you receive the confirmation e-mail</strong>.</li>
<li>In the week before the trip the leader sends the details to the participants.</li>
<li>If you can no longer take part, tell the trip leaders straight away: the place goes to someone on the waiting list.</li>
</ul>""")),
        blocco("gita-h", tr("Durante la gita", "Während der Tour", "During the trip"),
               tr("Il capogita, di regola affiancato da un co-capogita, organizza e conduce la gita.",
                  "Die Tourenleitung, in der Regel mit einer Co-Leitung, organisiert und führt die Tour.",
                  "The trip leader, usually with a co-leader, organises and leads the trip."),
               tr("""<ul>
<li>La gita si fa se ci sono almeno tre partecipanti, capigita esclusi.</li>
<li>Di regola si parte anche con un tempo non ideale; con condizioni pessime o un rischio evidente il capogita può cambiare meta, rinviare o annullare, anche a gita in corso.</li>
<li>Si seguono le indicazioni dei capigita. Chi non le segue, o non è all’altezza della gita, può esserne escluso; il rientro in sicurezza resta comunque garantito.</li>
<li>Chi si separa dal gruppo di sua iniziativa lo fa a proprio rischio e deve dirlo chiaramente al capogita.</li>
<li>I trasporti li organizzano i capigita: quando si può, mezzi pubblici o auto in comune.</li>
<li>Ognuno porta il proprio materiale tecnico; quello che manca si può <a href="noleggio.html">noleggiare dalla sezione</a>.</li>
</ul>""", """<ul>
<li>Die Tour findet statt, wenn mindestens drei Personen teilnehmen, Leitende nicht mitgezählt.</li>
<li>In der Regel wird auch bei nicht idealem Wetter gestartet; bei sehr schlechten Verhältnissen oder offensichtlicher Gefahr kann die Tourenleitung das Ziel ändern, die Tour verschieben oder absagen, auch unterwegs.</li>
<li>Den Anweisungen der Tourenleitung ist zu folgen. Wer das nicht tut oder der Tour nicht gewachsen ist, kann ausgeschlossen werden; eine sichere Rückkehr bleibt gewährleistet.</li>
<li>Wer sich aus eigenem Entschluss von der Gruppe trennt, tut das auf eigene Gefahr und muss es der Tourenleitung klar mitteilen.</li>
<li>Die Anreise organisiert die Tourenleitung: wenn möglich mit öffentlichen Verkehrsmitteln oder in Fahrgemeinschaften.</li>
<li>Alle bringen ihr eigenes technisches Material mit; was fehlt, kann man <a href="noleggio.html">bei der Sektion mieten</a>.</li>
</ul>""", """<ul>
<li>A trip goes ahead with at least three participants, not counting the leaders.</li>
<li>As a rule trips start even in less than ideal weather; in very bad conditions or with an obvious risk the leader may change the objective, postpone or cancel, even during the trip.</li>
<li>Follow the leaders’ instructions. Anyone who does not, or who is not up to the trip, may be excluded; a safe return is still ensured.</li>
<li>Anyone who leaves the group on their own initiative does so at their own risk and must tell the leader clearly.</li>
<li>The leaders organise transport: public transport or shared cars wherever possible.</li>
<li>Everyone brings their own technical gear; anything missing can be <a href="noleggio.html">hired from the section</a>.</li>
</ul>""")),
        blocco("rischi-h", tr("Rischi e assicurazione", "Risiken und Versicherung", "Risks and insurance"),
               tr("Nessuna attività in montagna è priva di rischi: si partecipa a proprio rischio e pericolo.",
                  "Keine Aktivität in den Bergen ist ohne Risiko: Die Teilnahme erfolgt auf eigene Gefahr.",
                  "No mountain activity is free of risk: you take part at your own risk."),
               tr("""<p>Iscrivendoti dichiari di conoscere i pericoli, di avere capacità adatte alla gita, di saper usare il tuo materiale e di esserti informato sul percorso.</p>
<p><strong>La sezione non ha assicurazioni per le sue attività.</strong> Ogni partecipante deve avere una propria copertura: infortuni, responsabilità civile, protezione giuridica e spese di soccorso e recupero. Salvo i casi previsti dalla legge, la sezione e i capigita non rispondono di infortuni o danni.</p>""",
                  """<p>Mit der Anmeldung erklären Sie, die Gefahren zu kennen, über die für die Tour nötigen Fähigkeiten zu verfügen, mit Ihrem Material umgehen zu können und sich über die Route informiert zu haben.</p>
<p><strong>Die Sektion hat für ihre Aktivitäten keine Versicherungen abgeschlossen.</strong> Alle Teilnehmenden brauchen einen eigenen Versicherungsschutz: Unfall, Haftpflicht, Rechtsschutz sowie Rettungs- und Bergungskosten. Ausser in den gesetzlich vorgesehenen Fällen haften die Sektion und die Tourenleitenden nicht für Unfälle oder Schäden.</p>""",
                  """<p>By registering you declare that you are aware of the dangers, have the skills the trip requires, know how to use your gear and have found out about the route.</p>
<p><strong>The section has no insurance for its activities.</strong> Every participant needs their own cover: accident, third-party liability, legal protection, and rescue and recovery costs. Except where the law provides otherwise, the section and the trip leaders are not liable for accidents or damage.</p>""")),
        blocco("costi-h", tr("Costi", "Kosten", "Costs"),
               tr("I partecipanti si dividono i costi della gita; i capigita sono volontari.",
                  "Die Teilnehmenden teilen sich die Kosten der Tour; die Tourenleitenden sind ehrenamtlich.",
                  "Participants share the costs of the trip; the trip leaders are volunteers."),
               tr("""<ul>
<li>In auto privata ogni partecipante versa 10 centesimi al chilometro, divisi tra chi mette a disposizione l’auto.</li>
<li>Se c’è una guida o un altro professionista della montagna, il suo compenso è diviso tra i partecipanti.</li>
<li>Il capogita può chiedere un acconto.</li>
<li>Se la gita è annullata non ci sono rimborsi: le spese di annullamento della capanna sono divise tra i partecipanti, gli acconti restituiti, tranne quanto trattenuto da terzi.</li>
<li>Se rinunci e nessuno in lista d’attesa prende il tuo posto, il capogita può chiederti i costi già sostenuti, per esempio la caparra della capanna.</li>
</ul>""", """<ul>
<li>Bei Fahrten mit Privatautos zahlen alle Teilnehmenden 10 Rappen pro Kilometer, die unter den Fahrzeughaltern aufgeteilt werden.</li>
<li>Ist ein Bergführer oder eine andere Bergsportfachperson dabei, wird das Honorar unter den Teilnehmenden aufgeteilt.</li>
<li>Die Tourenleitung kann eine Anzahlung verlangen.</li>
<li>Wird die Tour abgesagt, gibt es keine Rückerstattung: Annullierungskosten der Hütte werden unter den Teilnehmenden aufgeteilt, Anzahlungen zurückerstattet, ausser was Dritte einbehalten.</li>
<li>Wenn Sie absagen und niemand von der Warteliste Ihren Platz übernimmt, kann die Tourenleitung die bereits entstandenen Kosten verlangen, etwa die Anzahlung für die Hütte.</li>
</ul>""", """<ul>
<li>When travelling by private car, each participant pays 10 centimes per kilometre, shared among those who provide a car.</li>
<li>If a mountain guide or other mountain professional takes part, their fee is shared among the participants.</li>
<li>The leader may ask for a deposit.</li>
<li>If the trip is cancelled there are no refunds: hut cancellation fees are shared among the participants and deposits returned, except for amounts kept by third parties.</li>
<li>If you withdraw and nobody on the waiting list takes your place, the leader may ask you to pay costs already incurred, such as the hut deposit.</li>
</ul>""")),
        blocco("dati-h", tr("Dati e foto", "Daten und Fotos", "Data and photos"),
               tr("Con l’iscrizione accetti alcune regole sui tuoi dati.", "Mit der Anmeldung akzeptieren Sie einige Regeln zu Ihren Daten.", "By registering you accept a few rules about your data."),
               tr("""<p>I tuoi dati servono ai capigita e alla sezione per organizzare la gita e per la sicurezza; la lista dei partecipanti può essere data agli altri partecipanti. Le foto di gruppo e personali scattate in gita possono comparire su annuario, Informazione, sito e social della sezione: se non vuoi, dillo al capogita. Più dettagli nella pagina sulla <a href="privacy.html">protezione dei dati</a>.</p>""",
                  """<p>Ihre Daten dienen der Tourenleitung und der Sektion zur Organisation der Tour und zur Sicherheit; die Teilnehmerliste kann an die anderen Teilnehmenden weitergegeben werden. Gruppen- und Einzelfotos von der Tour können im Jahrbuch, in «Informazione», auf der Website und in den sozialen Medien der Sektion erscheinen: Wenn Sie das nicht möchten, sagen Sie es der Tourenleitung. Mehr dazu auf der Seite <a href="privacy.html">Datenschutz</a>.</p>""",
                  """<p>Your data is used by the leaders and the section to organise the trip and for safety; the list of participants may be given to the other participants. Group and individual photos taken on the trip may appear in the yearbook, «Informazione», the website and the section’s social media: if you would rather they didn’t, tell the trip leader. More on the <a href="privacy.html">privacy</a> page.</p>""")),
    ]
    titolo = tr("Partecipare alle gite", "An Touren teilnehmen", "Taking part in trips")
    regolamento = tr("Regolamento gite (PDF)", "Tourenreglement (PDF, italienisch)", "Trip regulations (PDF, in Italian)")
    body = page_hero([att_crumb(), (titolo, None)], titolo, tr(
                         "Le regole principali per chi partecipa alle gite e ai corsi della sezione, soci e non soci, in breve. Il testo completo è nel regolamento gite.",
                         "Die wichtigsten Regeln für alle, die an Touren und Kursen der Sektion teilnehmen, Mitglieder und Nichtmitglieder, kurz gefasst. Der vollständige Text steht im Tourenreglement (italienisch).",
                         "The main rules for anyone taking part in the section’s trips and courses, members and non-members, in brief. The full text is in the trip regulations (in Italian)."),
                     extra=f"""<div class="actions"><a class="btn btn--primary" href="{GITE}">{t("gite")} <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--secondary" href="{REGOLAMENTO_GITE}">{regolamento}</a></div>""") + "\n\n" + "\n\n".join(sezioni) + f"""

{prima_di_partire()}

<section class="section" aria-label="{tr("Regolamento gite", "Tourenreglement", "Trip regulations")}">
<div class="container">
<div class="callout">
<p>{tr("<strong>Questa pagina riassume il regolamento gite</strong> approvato dal comitato il 31 marzo 2026. Vale per tutte le gite della sezione, compresi i gruppi Senior e giovani; per i corsi alcune regole possono cambiare.",
       "<strong>Diese Seite fasst das Tourenreglement zusammen</strong>, das der Vorstand am 31. März 2026 genehmigt hat. Es gilt für alle Touren der Sektion, auch für die Senioren- und die Jugendgruppe; für Kurse können einzelne Regeln abweichen. Massgebend ist der italienische Text.",
       "<strong>This page summarises the trip regulations</strong> approved by the committee on 31 March 2026. They apply to all the section’s trips, including the seniors and youth groups; some rules may differ for courses. The Italian text is binding.")}</p>
<div class="actions"><a class="btn btn--secondary" href="{REGOLAMENTO_GITE}">{regolamento}</a><a class="btn btn--secondary" href="documenti.html">{tr("Altri documenti", "Weitere Dokumente", "More documents")}</a></div>
</div>
</div>
</section>

{subnav(ATT_MENU(), L("partecipare.html"))}"""
    return sezione_page("partecipare.html", titolo + " | CAS Ticino", tr(
        "Come partecipare alle gite del CAS Ticino: iscrizione e conferma su Droptour, requisiti, svolgimento, assicurazione, costi e foto, in breve dal regolamento gite.",
        "So nehmen Sie an den Touren der SAC-Sektion Ticino teil: Anmeldung und Bestätigung auf Droptour, Voraussetzungen, Ablauf, Versicherung, Kosten und Fotos, kurz aus dem Tourenreglement.",
        "How to take part in SAC Ticino Section trips: registration and confirmation on Droptour, requirements, conduct, insurance, costs and photos, in brief from the trip regulations."),
        body, og="paesaggi/gruppo-ghiacciaio-2000")


def volontariato():
    def mail(m, testo=None):
        return f'<a class="link" href="mailto:{m}">{testo or tr("Scrivi a", "Schreiben Sie an", "Write to")} {m}</a>'

    titolo = tr("Mettiti in gioco", "Mithelfen", "Get involved")
    body = page_hero([sez_crumb(), (titolo, None)], titolo, tr(
                         "La sezione vive del volontariato: capigita, monitori, aiuti in capanna, chi scrive e chi fotografa. Non serve essere esperti, basta un po’ di tempo e voglia di montagna.",
                         "Die Sektion lebt von der Freiwilligenarbeit: Tourenleitende, Jugendleitende, Helferinnen und Helfer in den Hütten, wer schreibt und wer fotografiert. Man muss kein Profi sein, es braucht nur etwas Zeit und Lust auf Berge.",
                         "The section runs on volunteers: trip leaders, instructors, helpers in the huts, writers and photographers. You don’t need to be an expert, just some time and a love of the mountains.")) + f"""

<section class="section" aria-labelledby="ruoli-h">
<div class="container">
<div class="section-head">
<h2 id="ruoli-h" class="h2">{tr("Dove c’è bisogno", "Wo es Hilfe braucht", "Where help is needed")}</h2>
</div>
<div class="pillars" data-reveal>
<article class="pillar pillar--wide">
<h3>{tr("Api operaie in capanna", "Fleissige Bienen in den Hütten", "Busy bees in the huts")}</h3>
<p>{tr("Aiuti i guardiani ad aprire e chiudere la stagione e nei lavori di manutenzione delle capanne, e passi qualche bella serata in quota.",
       "Sie helfen den Hüttenwarten beim Öffnen und Schliessen der Saison und bei Unterhaltsarbeiten in den Hütten und verbringen schöne Abende in der Höhe.",
       "Help the hut keepers open and close the season and with maintenance work in the huts, and spend some fine evenings up high.")}</p>
<a class="link" href="#capanne-h">{tr("Come dare una mano", "So helfen Sie mit", "How to help")}</a>
</article>
<article class="pillar pillar--accent">
<h3>{tr("Capogita", "Tourenleitung", "Trip leader")}</h3>
<p>{tr("Si comincia affiancando un capogita, o nei corsi base come aiuto-capogita; con i corsi avanzati e la formazione del CAS si diventa capogita.",
       "Man beginnt an der Seite einer Tourenleitung oder als Hilfsleitung in den Grundkursen; mit Fortgeschrittenenkursen und der SAC-Ausbildung wird man Tourenleiterin oder Tourenleiter.",
       "You start alongside a trip leader, or as an assistant leader on the basic courses; with advanced courses and SAC training you become a trip leader.")}</p>
{mail(MAIL_DICASTERI["Dicastero sport di montagna"])}
</article>
<article class="pillar">
<h3>{tr("Monitore G+S", "J+S-Leitung", "Youth+Sport instructor")}</h3>
<p>{tr("Accompagni ragazze e ragazzi in falesia, nei campi e in montagna. La sezione promuove la formazione di monitori Gioventù+Sport.",
       "Sie begleiten Mädchen und Jungen in den Klettergarten, in Lager und in die Berge. Die Sektion fördert die Ausbildung von Jugend+Sport-Leitenden.",
       "Take girls and boys climbing, to camps and into the mountains. The section supports Youth+Sport instructor training.")}</p>
{mail(MAIL_DICASTERI["Dicastero giovani"])}
</article>
<article class="pillar">
<h3>{tr("Gite Senior", "Seniorentouren", "Seniors’ trips")}</h3>
<p>{tr("Il gruppo Senior cerca sempre nuovi capigita per gite di un giorno, fine settimana e vacanze in montagna.",
       "Die Seniorengruppe sucht immer neue Tourenleitende für Tagestouren, Wochenenden und Bergferien.",
       "The seniors group is always looking for new trip leaders for day trips, weekends and mountain holidays.")}</p>
{mail(MAIL_DICASTERI["Dicastero senior"])}
</article>
<article class="pillar pillar--dark">
<h3>{tr("Comunicazione ed eventi", "Kommunikation und Anlässe", "Communication and events")}</h3>
<p>{tr("Testi, foto e resoconti per il sito, i social, l’annuario e Informazione; serate ed eventi sulla cultura della montagna.",
       "Texte, Fotos und Berichte für Website, soziale Medien, Jahrbuch und «Informazione»; Abende und Anlässe zur Bergkultur.",
       "Texts, photos and reports for the website, social media, the yearbook and «Informazione»; evenings and events on mountain culture.")}</p>
{mail(MAIL_DICASTERI["Dicastero comunicazione"])}
</article>
</div>
</div>
</section>

""" + blocco("capanne-h", tr("Lavori in capanna", "Arbeiten in den Hütten", "Work in the huts"),
             tr("Le sei capanne della sezione si tengono in ordine anche grazie ai soci volontari, insieme ai guardiani e al dicastero infrastruttura.",
                "Die sechs Hütten der Sektion werden auch dank freiwilliger Mitglieder in Schuss gehalten, zusammen mit den Hüttenwarten und dem Ressort Infrastruktur.",
                "The section’s six huts are kept in shape partly thanks to volunteer members, together with the hut keepers and the infrastructure department."),
             tr("""<p>Ogni anno servono mani per lavori di ogni genere, per una giornata o per un fine settimana:</p>
<ul>
<li>apertura e chiusura della stagione: pulizie, coperte e materassi, messa in sicurezza per l’inverno;</li>
<li>manutenzione e piccole riparazioni: falegnameria, pittura, impianti, serramenti;</li>
<li>pulizia delle fosse biologiche e degli impianti di depurazione;</li>
<li>legna, trasporti di materiale e sgombero dei dintorni;</li>
<li>lavori più grandi e cantieri, quando una capanna viene rinnovata.</li>
</ul>
<p>Non serve essere artigiani: basta la voglia di fare. Chi ha un mestiere (falegname, idraulico, elettricista, muratore…) è particolarmente prezioso. I lavori si organizzano con il guardiano e il dicastero infrastruttura, che ti dice dove e quando c’è bisogno.</p>""",
                """<p>Jedes Jahr braucht es Hände für Arbeiten aller Art, für einen Tag oder ein Wochenende:</p>
<ul>
<li>Saisoneröffnung und -schluss: Putzen, Decken und Matratzen, Wintersicherung;</li>
<li>Unterhalt und kleine Reparaturen: Schreinerarbeiten, Malen, Installationen, Fenster und Türen;</li>
<li>Reinigung der Klärgruben und Abwasseranlagen;</li>
<li>Holz, Materialtransporte und Aufräumen rund um die Hütte;</li>
<li>grössere Arbeiten und Baustellen, wenn eine Hütte erneuert wird.</li>
</ul>
<p>Handwerkliches Können ist keine Voraussetzung, es braucht nur Tatkraft. Wer einen Beruf hat (Schreiner, Sanitär, Elektriker, Maurer…), ist besonders wertvoll. Die Einsätze werden mit dem Hüttenwart und dem Ressort Infrastruktur organisiert, das Ihnen sagt, wo und wann Hilfe nötig ist.</p>""",
                """<p>Every year hands are needed for all kinds of jobs, for a day or a weekend:</p>
<ul>
<li>opening and closing the season: cleaning, blankets and mattresses, making the hut safe for winter;</li>
<li>maintenance and small repairs: carpentry, painting, installations, windows and doors;</li>
<li>cleaning the septic tanks and wastewater systems;</li>
<li>firewood, carrying materials and clearing up around the hut;</li>
<li>bigger jobs and building work when a hut is renovated.</li>
</ul>
<p>You don’t need to be a tradesperson, just willing. Anyone with a trade (carpenter, plumber, electrician, bricklayer…) is especially valuable. The work is organised with the hut keeper and the infrastructure department, who will tell you where and when help is needed.</p>""")
             + f'\n<p>{mail(MAIL_DICASTERI["Dicastero infrastruttura"])}</p>') + "\n\n" + blocco(
        "capogita-h", tr("Diventare capogita", "Tourenleiter werden", "Becoming a trip leader"),
        tr("Il percorso per chi vuole guidare le gite della sezione.", "Der Weg für alle, die Touren der Sektion leiten möchten.", "The path for those who want to lead the section’s trips."),
        tr("""<ol>
<li><strong>Partecipa</strong> alle gite e ai <a href="corsi.html">corsi</a> della sezione, per fare esperienza.</li>
<li><strong>Fatti avanti come aiuto-capogita</strong>: può esserlo ogni socio che vuole dare una mano o che segue, o vuole seguire, la formazione da capogita.</li>
<li><strong>Formati</strong>: i corsi avanzati di alpinismo, sci alpinismo e arrampicata della sezione preparano a fare da capocordata e ai corsi capogita del CAS centrale o monitore Gioventù+Sport.</li>
<li><strong>Guida le tue gite</strong>, con il sostegno del dicastero sport di montagna, e tieniti aggiornato con i corsi di perfezionamento.</li>
</ol>
<p>Le attività della sezione sono volontarie; ai capigita vengono rimborsate le spese vive. Conosci già <a href="capigita.html">i nostri capigita</a>?</p>""",
           """<ol>
<li><strong>Machen Sie mit</strong> bei Touren und <a href="corsi.html">Kursen</a> der Sektion, um Erfahrung zu sammeln.</li>
<li><strong>Melden Sie sich als Hilfsleitung</strong>: Das kann jedes Mitglied, das mithelfen möchte oder die Tourenleiterausbildung macht oder machen will.</li>
<li><strong>Bilden Sie sich aus</strong>: Die Fortgeschrittenenkurse der Sektion in Hochtouren, Skitouren und Klettern bereiten auf die Rolle als Seilschaftsführer und auf die Tourenleiterkurse des SAC oder die Jugend+Sport-Leiterkurse vor.</li>
<li><strong>Leiten Sie Ihre eigenen Touren</strong>, mit der Unterstützung des Ressorts Bergsport, und bleiben Sie mit Fortbildungskursen auf dem Laufenden.</li>
</ol>
<p>Die Aktivitäten der Sektion sind ehrenamtlich; den Tourenleitenden werden die Auslagen vergütet. Kennen Sie schon <a href="capigita.html">unsere Tourenleitenden</a>?</p>""",
           """<ol>
<li><strong>Take part</strong> in the section’s trips and <a href="corsi.html">courses</a> to gain experience.</li>
<li><strong>Step forward as assistant leader</strong>: any member can, whether to lend a hand or because they are following, or want to follow, trip leader training.</li>
<li><strong>Train</strong>: the section’s advanced courses in mountaineering, ski touring and climbing prepare you to lead a rope and for the SAC trip leader or Youth+Sport instructor courses.</li>
<li><strong>Lead your own trips</strong>, with the support of the mountain sports department, and keep up to date with refresher courses.</li>
</ol>
<p>The section’s activities are voluntary; trip leaders are reimbursed for out-of-pocket expenses. Have you met <a href="capigita.html">our trip leaders</a>?</p>""")) + f"""

{subnav(SEZ_MENU(), L("volontariato.html"))}"""
    return sezione_page("volontariato.html", titolo + " | CAS Ticino", tr(
        "Volontariato nel CAS Ticino: api operaie in capanna, capigita e aiuto-capigita, monitori G+S, capigita Senior, comunicazione ed eventi. Come cominciare.",
        "Freiwilligenarbeit in der SAC-Sektion Ticino: Arbeiten in den Hütten, Tourenleitung und Hilfsleitung, J+S-Leitende, Seniorentouren, Kommunikation und Anlässe. So fangen Sie an.",
        "Volunteering with the SAC Ticino Section: work in the huts, trip leaders and assistant leaders, Youth+Sport instructors, seniors’ trips, communication and events. How to start."),
        body, og="paesaggi/salita-prato-2000")


# ------------------------------------------------------------------ protezione dei dati (privacy.html, de/, en/)
# Testo per lingua: titolo, descrizione, sommario e corpo (HTML, percorsi dalla radice). Tenere allineate le tre versioni
# quando il sito cambia (nuovi servizi esterni, cookie, moduli…) e aggiornare PRIVACY_AGGIORNATA.

PRIVACY_AGGIORNATA = {"it": "ottobre 2026", "de": "Oktober 2026", "en": "October 2026"}

PRIVACY = {
    "it": dict(
        title="Protezione dei dati | CAS Ticino", h1="Protezione dei dati",
        desc="Informativa sulla protezione dei dati del sito del CAS Ticino: quali dati si trattano, cookie, servizi esterni e i tuoi diritti.",
        lead="Il sito del CAS Ticino non usa cookie né strumenti di statistica. Qui trovi quali dati vengono comunque trattati quando lo visiti o ci scrivi, da chi e perché.",
        corpo="""<h2>Chi è responsabile</h2>
<p>Club Alpino Svizzero, Sezione Ticino<br>Casella postale 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>Ci atteniamo alla legge federale sulla protezione dei dati (LPD).</p>

<h2>Visita del sito</h2>
<p>Il sito è ospitato da GitHub Pages (GitHub Inc., USA). Come ogni server web, GitHub registra per ogni visita l’indirizzo IP, la data e l’ora, la pagina richiesta e il tipo di browser, per far funzionare il servizio e per la sicurezza. La sezione non riceve questi dati. GitHub aderisce al Data Privacy Framework Svizzera–USA; i dettagli sono nella <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">dichiarazione sulla privacy di GitHub</a> (in inglese).</p>

<h2>Cookie e memoria del browser</h2>
<p>Il sito non imposta cookie e non usa strumenti di statistica, pubblicità o profilazione. I caratteri tipografici sono caricati dal sito stesso. Il programma gite tiene per 10 minuti l’elenco delle gite nella memoria della scheda del browser (sessionStorage), per aprire più in fretta il dettaglio di una gita: non contiene dati personali e si cancella chiudendo la scheda. Se chiudi l’avviso in cima alle pagine, il browser ricorda solo quale avviso hai chiuso (localStorage), per non mostrartelo di nuovo: resta sul tuo dispositivo e non viene inviato a nessuno. Per aprire il sito più in fretta e anche senza rete (per esempio se lo aggiungi alla schermata Home), il browser tiene in memoria alcune pagine, immagini e file del sito (service worker e cache): restano sul tuo dispositivo e si cancellano con i dati del sito nelle impostazioni del browser.</p>

<h2>Programma gite e foto</h2>
<p>Il programma gite e le foto delle uscite vengono caricati da Droptour (ssl.dropnet.ch, in Svizzera), il servizio con cui la sezione gestisce gite e iscrizioni: aprendo queste pagine il tuo browser si collega a Droptour, che riceve il tuo indirizzo IP. L’iscrizione alle gite avviene su Droptour; i dati che inserisci lì servono a organizzare la gita e sono visibili ai capigita.</p>

<h2>Facebook</h2>
<p>Nelle pagine delle capanne i post da Facebook vengono caricati solo se clicchi «Mostra i post». Prima di quel clic a Facebook non arriva nulla; dopo, Meta Platforms riceve dati sulla tua visita (tra cui l’indirizzo IP) e può impostare cookie, secondo la sua <a href="https://www.facebook.com/privacy/policy/" rel="noopener">informativa sulla privacy</a>. I link a Instagram, Facebook, hut-reservation.org e ad altri siti sono semplici link: i tuoi dati li tratta il sito che apri.</p>

<h2>Contatti e annunci</h2>
<p>Se ci scrivi per e-mail usiamo il tuo messaggio solo per rispondere e per dare seguito alla richiesta (per esempio inoltrandolo al custode di una capanna o al responsabile di un corso). Gli annunci del Mercatino vengono pubblicati con il nome e il contatto che indichi tu e restano online fino alla scadenza; puoi chiederne la rimozione in ogni momento.</p>

<h2 id="notifiche">Notifiche</h2>
<p>Se attivi le notifiche (in fondo alle pagine), il browser chiede il tuo permesso e crea un indirizzo di notifica anonimo: non contiene nome, e-mail o numero di telefono. Lo salviamo con la lingua della pagina in un piccolo servizio della sezione su Cloudflare Workers (Cloudflare Inc., USA; dati salvati in Europa), solo per inviarti le notizie importanti della sezione. Le notifiche passano dal servizio del tuo browser o telefono (Google, Apple, Mozilla o Microsoft). Con «Disattiva le notifiche», o togliendo il permesso nelle impostazioni, l’indirizzo viene cancellato; quelli non più validi li cancelliamo da soli.</p>
<h2 id="noleggio">Noleggio materiale</h2>
<p>Il modulo del noleggio invia nome, e-mail, telefono, note, date e materiale scelto a un piccolo servizio della sezione su Cloudflare Workers (Cloudflare Inc., USA; dati salvati in Europa). Li vede solo il responsabile del noleggio, che li usa per confermare la richiesta e per il ritiro e la riconsegna. Le e-mail di ricevuta e di conferma partono tramite Brevo (Francia). Le richieste vengono cancellate 12 mesi dopo la fine del noleggio. Per proteggere il modulo dai programmi automatici, quando inizi a compilarlo viene caricato Cloudflare Turnstile, che riceve l’indirizzo IP e alcune informazioni tecniche sul browser, secondo l’<a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">informativa sulla privacy di Cloudflare</a> (in inglese). Cloudflare aderisce al Data Privacy Framework Svizzera–USA.</p>

<h2>Persone sul sito</h2>
<p>Nomi, foto e presentazioni dei membri del comitato, dei dicasteri e dei capigita sono pubblicati con il loro consenso. Nelle news e nei resoconti delle gite possono comparire foto di partecipanti. Se vuoi che una tua foto o il tuo nome venga tolto, scrivici.</p>

<h2>Soci</h2>
<p>L’adesione e i dati dei soci sono gestiti con il Club Alpino Svizzero (portal.sac-cas.ch), secondo la sua <a href="https://www.sac-cas.ch/it/datenschutz/" rel="noopener">informativa sulla protezione dei dati</a>.</p>

<h2>I tuoi diritti</h2>
<p>Puoi chiedere quali dati abbiamo su di te, farli correggere o cancellare e opporti al loro uso, scrivendo a <a href="mailto:info@casticino.ch">info@casticino.ch</a>. Puoi anche rivolgerti all’<a href="https://www.edoeb.admin.ch/it" rel="noopener">Incaricato federale della protezione dei dati e della trasparenza (IFPDT)</a>.</p>"""),
    "de": dict(
        title="Datenschutz | CAS Ticino", h1="Datenschutz",
        desc="Datenschutzerklärung der Website der SAC-Sektion Ticino: welche Daten bearbeitet werden, Cookies, externe Dienste und Ihre Rechte.",
        lead="Die Website der Sektion Ticino verwendet weder Cookies noch Statistik-Werkzeuge. Hier steht, welche Daten trotzdem bearbeitet werden, wenn Sie sie besuchen oder uns schreiben, von wem und weshalb.",
        corpo="""<h2>Verantwortlich</h2>
<p>Schweizer Alpen-Club SAC, Sektion Ticino<br>Postfach 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>Wir halten uns an das Bundesgesetz über den Datenschutz (DSG).</p>

<h2>Besuch der Website</h2>
<p>Die Website wird von GitHub Pages (GitHub Inc., USA) betrieben. Wie jeder Webserver speichert GitHub bei jedem Besuch die IP-Adresse, Datum und Uhrzeit, die aufgerufene Seite und den Browsertyp, für den Betrieb und die Sicherheit des Dienstes. Die Sektion erhält diese Daten nicht. GitHub ist dem Swiss-U.S. Data Privacy Framework beigetreten; Einzelheiten in der <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>

<h2>Cookies und Browserspeicher</h2>
<p>Die Website setzt keine Cookies und verwendet keine Werkzeuge für Statistik, Werbung oder Profiling. Die Schriften werden von der Website selbst geladen. Das Tourenprogramm speichert die Tourenliste 10 Minuten lang im Speicher des Browser-Tabs (sessionStorage), damit die Einzelheiten einer Tour schneller erscheinen: Sie enthält keine Personendaten und wird beim Schliessen des Tabs gelöscht. Wenn Sie den Hinweis oben auf den Seiten schliessen, merkt sich der Browser nur, welchen Hinweis Sie geschlossen haben (localStorage), damit er nicht wieder erscheint: Die Angabe bleibt auf Ihrem Gerät und wird an niemanden gesendet. Damit die Website schneller und auch ohne Netz erscheint (zum Beispiel, wenn Sie sie zum Home-Bildschirm hinzufügen), speichert der Browser einige Seiten, Bilder und Dateien der Website (Service Worker und Cache): Sie bleiben auf Ihrem Gerät und werden mit den Website-Daten in den Browser-Einstellungen gelöscht.</p>

<h2>Tourenprogramm und Fotos</h2>
<p>Das Tourenprogramm und die Tourenfotos werden von Droptour geladen (ssl.dropnet.ch, Schweiz), dem Dienst, mit dem die Sektion Touren und Anmeldungen verwaltet: Beim Öffnen dieser Seiten verbindet sich Ihr Browser mit Droptour, das Ihre IP-Adresse erhält. Die Anmeldung zu den Touren erfolgt auf Droptour; die dort eingegebenen Daten dienen der Organisation der Tour und sind für die Tourenleitenden sichtbar.</p>

<h2>Facebook</h2>
<p>Auf den Hüttenseiten werden die Facebook-Beiträge erst geladen, wenn Sie auf «Beiträge anzeigen» klicken. Vorher geht nichts an Facebook; danach erhält Meta Platforms Daten über Ihren Besuch (darunter die IP-Adresse) und kann Cookies setzen, gemäss seiner <a href="https://www.facebook.com/privacy/policy/" rel="noopener">Datenschutzrichtlinie</a>. Links zu Instagram, Facebook, hut-reservation.org und anderen Websites sind einfache Links: Ihre Daten bearbeitet dann die Website, die Sie öffnen.</p>

<h2>Kontakt und Inserate</h2>
<p>Wenn Sie uns per E-Mail schreiben, verwenden wir Ihre Nachricht nur, um zu antworten und Ihr Anliegen zu bearbeiten (zum Beispiel durch Weiterleitung an das Hüttenteam oder an die Kursleitung). Inserate auf dem Mercatino werden mit dem Namen und dem Kontakt veröffentlicht, die Sie angeben, und bleiben bis zum Ablaufdatum online; Sie können jederzeit die Entfernung verlangen.</p>

<h2 id="notifiche">Mitteilungen</h2>
<p>Wenn Sie Mitteilungen einschalten (unten auf den Seiten), fragt der Browser nach Ihrer Erlaubnis und erstellt eine anonyme Mitteilungsadresse: Sie enthält weder Name noch E-Mail noch Telefonnummer. Wir speichern sie mit der Sprache der Seite in einem kleinen Dienst der Sektion auf Cloudflare Workers (Cloudflare Inc., USA; Daten in Europa gespeichert), nur um Ihnen wichtige Neuigkeiten der Sektion zu senden. Die Mitteilungen laufen über den Dienst Ihres Browsers oder Telefons (Google, Apple, Mozilla oder Microsoft). Mit «Mitteilungen ausschalten» oder wenn Sie die Erlaubnis in den Einstellungen entziehen, wird die Adresse gelöscht; ungültig gewordene Adressen löschen wir selbst.</p>
<h2 id="noleggio">Materialvermietung</h2>
<p>Das Formular der Materialvermietung sendet Name, E-Mail, Telefon, Bemerkungen, Daten und das gewählte Material an einen kleinen Dienst der Sektion auf Cloudflare Workers (Cloudflare Inc., USA; Daten in Europa gespeichert). Sie sind nur für die Materialverantwortlichen sichtbar, die sie für die Bestätigung der Anfrage sowie für Abholung und Rückgabe verwenden. Die Empfangs- und Bestätigungs-E-Mails werden über Brevo (Frankreich) verschickt. Die Anfragen werden 12 Monate nach Ende der Miete gelöscht. Zum Schutz des Formulars vor automatisierten Programmen wird Cloudflare Turnstile geladen, sobald Sie mit dem Ausfüllen beginnen; Cloudflare erhält dabei die IP-Adresse und einige technische Angaben zum Browser, gemäss der <a href="https://www.cloudflare.com/de-de/privacypolicy/" rel="noopener">Datenschutzrichtlinie von Cloudflare</a>. Cloudflare ist dem Swiss-U.S. Data Privacy Framework beigetreten.</p>

<h2>Personen auf der Website</h2>
<p>Namen, Fotos und Vorstellungen der Mitglieder von Vorstand und Ressorts sowie der Tourenleitenden werden mit ihrem Einverständnis veröffentlicht. In News und Tourenberichten können Fotos von Teilnehmenden erscheinen. Wenn ein Foto von Ihnen oder Ihr Name entfernt werden soll, schreiben Sie uns.</p>

<h2>Mitglieder</h2>
<p>Mitgliedschaft und Mitgliederdaten werden mit dem Schweizer Alpen-Club verwaltet (portal.sac-cas.ch), gemäss dessen <a href="https://www.sac-cas.ch/de/meta/datenschutz/" rel="noopener">Datenschutzerklärung</a>.</p>

<h2>Ihre Rechte</h2>
<p>Sie können Auskunft über Ihre Daten verlangen, sie berichtigen oder löschen lassen und der Bearbeitung widersprechen: Schreiben Sie an <a href="mailto:info@casticino.ch">info@casticino.ch</a>. Sie können sich auch an den <a href="https://www.edoeb.admin.ch/de" rel="noopener">Eidgenössischen Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB)</a> wenden.</p>"""),
    "en": dict(
        title="Privacy policy | CAS Ticino", h1="Privacy policy",
        desc="Privacy policy of the website of the Ticino Section of the Swiss Alpine Club: what data is processed, cookies, external services and your rights.",
        lead="The Ticino Section’s website uses no cookies and no analytics tools. This page explains what data is nevertheless processed when you visit it or write to us, by whom and why.",
        corpo="""<h2>Who is responsible</h2>
<p>Swiss Alpine Club SAC, Ticino Section<br>PO Box 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>We comply with the Swiss Federal Act on Data Protection (FADP).</p>

<h2>Visiting the website</h2>
<p>The website is hosted by GitHub Pages (GitHub Inc., USA). Like any web server, GitHub logs the IP address, date and time, page requested and browser type of each visit, to run the service and for security. The Section does not receive this data. GitHub participates in the Swiss-U.S. Data Privacy Framework; details are in <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub’s privacy statement</a>.</p>

<h2>Cookies and browser storage</h2>
<p>The website sets no cookies and uses no analytics, advertising or profiling tools. Fonts are served by the website itself. The trip programme keeps the list of trips for 10 minutes in the browser tab’s storage (sessionStorage), so that a trip’s details open faster: it contains no personal data and is deleted when you close the tab. If you close the notice at the top of the pages, your browser only remembers which notice you closed (localStorage), so as not to show it again: this stays on your device and is not sent to anyone. To open the site faster and also without a connection (for example if you add it to your home screen), your browser keeps some of the site’s pages, images and files in its storage (service worker and cache): they stay on your device and are deleted with the site data in your browser settings.</p>

<h2>Trip programme and photos</h2>
<p>The trip programme and the trip photos are loaded from Droptour (ssl.dropnet.ch, Switzerland), the service the Section uses to manage trips and registrations: when you open these pages, your browser connects to Droptour, which receives your IP address. Registration for trips takes place on Droptour; the data you enter there is used to organise the trip and is visible to the trip leaders.</p>

<h2>Facebook</h2>
<p>On the hut pages, posts from Facebook are only loaded if you click «Show posts». Before that click nothing is sent to Facebook; afterwards Meta Platforms receives data about your visit (including your IP address) and may set cookies, under its <a href="https://www.facebook.com/privacy/policy/" rel="noopener">privacy policy</a>. Links to Instagram, Facebook, hut-reservation.org and other websites are plain links: your data is then processed by the website you open.</p>

<h2>Contacts and listings</h2>
<p>If you e-mail us, we use your message only to reply and to deal with your request (for example by forwarding it to a hut keeper or to a course leader). Mercatino listings are published with the name and contact details you give us and stay online until they expire; you can ask for removal at any time.</p>

<h2 id="notifiche">Notifications</h2>
<p>If you turn on notifications (at the bottom of the pages), your browser asks for your permission and creates an anonymous notification address: it contains no name, e-mail or phone number. We store it, with the language of the page, in a small service run by the Section on Cloudflare Workers (Cloudflare Inc., USA; data stored in Europe), only to send you important news from the Section. Notifications pass through your browser’s or phone’s service (Google, Apple, Mozilla or Microsoft). With «Turn off notifications», or by withdrawing permission in your settings, the address is deleted; addresses that are no longer valid are deleted automatically.</p>
<h2 id="noleggio">Equipment hire</h2>
<p>The equipment hire form sends your name, e-mail, phone number, notes, dates and the equipment chosen to a small service run by the Section on Cloudflare Workers (Cloudflare Inc., USA; data stored in Europe). Only the equipment manager sees it, and uses it to confirm the request and for pick-up and return. Receipt and confirmation e-mails are sent through Brevo (France). Requests are deleted 12 months after the end of the hire. To protect the form from automated programs, Cloudflare Turnstile is loaded when you start filling it in; Cloudflare receives your IP address and some technical information about your browser, under <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">Cloudflare’s privacy policy</a>. Cloudflare participates in the Swiss-U.S. Data Privacy Framework.</p>

<h2>People on the website</h2>
<p>Names, photos and introductions of the members of the committee, the departments and the trip leaders are published with their consent. Photos of participants may appear in the news and trip reports. If you would like a photo of you or your name removed, write to us.</p>

<h2>Members</h2>
<p>Membership and members’ data are managed with the Swiss Alpine Club (portal.sac-cas.ch), under its <a href="https://www.sac-cas.ch/en/meta/data-protection/" rel="noopener">privacy policy</a>.</p>

<h2>Your rights</h2>
<p>You can ask what data we hold about you, have it corrected or deleted, and object to its use, by writing to <a href="mailto:info@casticino.ch">info@casticino.ch</a>. You can also contact the <a href="https://www.edoeb.admin.ch/en" rel="noopener">Federal Data Protection and Information Commissioner (FDPIC)</a>.</p>"""),
}


def privacy():
    tx = PRIVACY[LINGUA["lang"]]
    agg = tr("Ultimo aggiornamento", "Letzte Änderung", "Last updated") + ": " + PRIVACY_AGGIORNATA[LINGUA["lang"]]
    body = page_hero([(tx["h1"], None)], tx["h1"], tx["lead"]) + f"""

<section class="section section--tight" aria-label="{tx['h1']}">
<div class="container article article--noimg">
<div class="prose">
{tx["corpo"]}
<p class="small">{agg}</p>
</div>
</div>
</section>"""
    return sezione_page("privacy.html", tx["title"], tx["desc"], body)


def offline_pagina():
    """Pagina mostrata dal service worker (sw.js, pwa.py) quando non c'è rete e la pagina chiesta non è salvata:
    le pagine che il telefono ha sempre (home, capanne, Partecipare, Soccorso) e i numeri d'emergenza."""
    huts = {"it": HUTS, "de": HUTS_DE, "en": HUTS_EN}[LINGUA["lang"]]
    links = [(tr("Home", "Startseite", "Home"), L("index.html"))]
    links += [(f'{tc("capanna")} {h[1]}' if h[0] != "baitadelluca.html" else h[1], L(h[0])) for h in huts]
    links += [(tr("Prima di partire", "Vor dem Aufbruch", "Before you set off"), L("partecipare.html") + "#prima-di-partire"),
              (tr("Soccorso", "Bergrettung", "Mountain rescue"), L("soccorso.html"))]
    lista = "\n".join(f'<a href="{h}"><span>{x}</span></a>' for x, h in links)
    numeri = [("1414", tr("Rega, soccorso aereo", "Rega, Luftrettung", "Rega, air rescue")),
              ("144", tr("Ambulanza", "Sanitätsnotruf", "Ambulance")),
              ("112", tr("Numero d’emergenza europeo", "Europäische Notrufnummer", "European emergency number"))]
    numeri = "\n".join(f'<a href="tel:{n}"><strong class="num">{n}</strong><span>{x}</span></a>' for n, x in numeri)
    titolo = tr("Sei offline", "Sie sind offline", "You are offline")
    body = page_hero([(titolo, None)], titolo, tr(
        "Senza connessione questa pagina non si può aprire. Restano consultabili le pagine già visitate e queste, salvate sul telefono.",
        "Ohne Verbindung lässt sich diese Seite nicht öffnen. Abrufbar bleiben die schon besuchten Seiten und diese, auf dem Telefon gespeichert.",
        "This page cannot be opened without a connection. Pages you have already visited are still available, and so are these, saved on your phone.")) + f"""

<section class="section section--tight" aria-label="{tr("Pagine salvate", "Gespeicherte Seiten", "Saved pages")}">
<div class="container detail">
<div class="linklist">
{lista}
</div>
<div class="emergenza">
<h2 class="label">{tr("In caso di emergenza", "Im Notfall", "In an emergency")}</h2>
<div class="emergenza-numeri">
{numeri}
</div>
</div>
</div>
</section>"""
    nome = L("offline.html")
    html = page(nome, f"{titolo} | CAS Ticino", titolo, body)
    return pubblica(nome, html.replace("<head>\n", '<head>\n<meta name="robots" content="noindex">\n', 1))


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
    """Genera una pagina con la lingua impostata a `lang` (de, en)."""
    def genera():
        LINGUA["lang"] = lang
        try:
            return localizza(fn(), lang)
        finally:
            LINGUA["lang"] = "it"
    return genera


# Versioni tradotte (de/, en/): tutte le pagine tranne la ricerca. Restano in italiano i contenuti scritti da altri
# (news, annunci del mercatino, gite e resoconti di Droptour) e i PDF; nelle pagine tradotte sono marcati lang="it".
for _lang, _contenuti in (("de", CONTENUTI_DE), ("en", CONTENUTI_EN)):
    _pagine = {"index.html": home, "introduzione.html": introduzione_tradotta, "comitato.html": comitato,
               "organizzazione.html": organizzazione, "capigita.html": capigita, "sede.html": sede_tradotta,
               "storia.html": storia, "link.html": link, "adesione.html": adesione_tradotta,
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
    it = name[3:] if name[:3] in ("de/", "en/") else name
    lingue = [lang for lang in ("de", "en") if it in PAGINE_LINGUA[lang]]
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
    for _lang in ("it", "de", "en"):
        scrivi("manifest.webmanifest" if _lang == "it" else f"manifest-{_lang}.webmanifest", pwa.manifest(_lang))
    _essenziali = ["index.html", "partecipare.html", "soccorso.html"] + list(HUT_PAGES)
    _statici = ([asset(f) for f in ("assets/site.css", "assets/site.js", "assets/gite.js", "assets/cerca.js", "assets/foto.js", "assets/noleggio.js")]
                + [f"assets/fonts/{f}" for f in sorted(os.listdir(os.path.join(ROOT, "assets", "fonts"))) if f.endswith(".woff2")]
                + ["assets/logo-cas.webp", "assets/logo-cas-stemma.webp"] + [i["src"] for i in pwa.ICONE] + ["assets/icone/apple-touch-icon.png", pwa.BADGE]
                + ["offline.html", "de/offline.html", "en/offline.html"])
    scrivi("sw.js", pwa.service_worker(_statici, {"it": _essenziali, "de": [f"de/{p}" for p in _essenziali],
                                                   "en": [f"en/{p}" for p in _essenziali]}))
    scrivi("robots.txt", f"User-agent: *\nDisallow: /admin/\n\nSitemap: {SITO}sitemap.xml\n")
    with open(os.path.join(ROOT, "data", "cerca.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(indice_ricerca(pagine), f, ensure_ascii=False, separators=(",", ":"))
    print("scritto data/cerca.json")
    if not only or "cerca.html" in only:
        scrivi("cerca.html", metadati("cerca.html", cerca_pagina()))  # dopo l'indice: il link porta l'impronta di cerca.json
