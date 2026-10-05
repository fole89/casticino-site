"""Nuovo design: genera tutte le pagine del sito.

Uso: python scripts/redesign/pages.py [Pagina.html ...]  (senza argomenti rigenera tutto)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shared import head, nav, footer, social, pic, img, GITE, GITE_DROPTOUR, page_hero, subnav, asset, in_sottocartella, crumbs

# Programma gite su Droptour già filtrato per gruppo o per tipo di attività (i link dei singoli corsi cambiano ogni anno)
GITE_GIOVANI = GITE + "?gruppo=Giovani"   # gite.html con il filtro già scelto (gite.js)
GITE_SENIORI = GITE + "?gruppo=Seniori"
GITE_CORSI = GITE + "?tipo=COR"
from shared import LINGUA, PAGINE_LINGUA, SITO, de, en, tr, L
from urllib.parse import urljoin, quote
from capanne import CONTENUTI, PRENOTA
from capanne_de import CONTENUTI_DE, HUT_DE, HUTS_DE
from capanne_en import CONTENUTI_EN, HUT_EN, HUTS_EN
import json, re, unicodedata
import news_util
import mercatino_util
from news_util import webp_size
from html import unescape as html_unescape, escape as html_escape

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUTS = [
    # file, nome, quota, valle, stato, testo, posti, accesso, img 3x2 (w,h), grande
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Custodita", "Su un terrazzo sopra la Val Piumogna, base per il Pizzo Campo Tencia: la cima più alta interamente ticinese.", "80 posti", "Dalpe 3h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Custodita", "Sull’omonimo passo, tra Leventina e Valle Maggia. Inaugurata nel 2003, primo rifugio moderno del CAS.", "100 posti", "Ossasco 3h30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Custodita", "Il classico rifugio in pietra affacciato sulla Valle di Blenio: storia, accoglienza calorosa e cucina nostrana.", "24 posti", "Compietto 2h40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Custodita", "Al margine della riserva della Greina: torbiere, alpeggi e l’arco naturale più grande del Ticino.", "70 posti", "Garzott 2h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "Tutto l’anno", "Il balcone sul Luganese, ricostruito nel 2016: vista dal Monte Rosa ai Denti della Vecchia, standard Bike Hotel.", "42 posti", "Corticiasca 1h30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Su riservazione", "Sopra Sonvico, ai piedi dei Denti della Vecchia. Ideale per famiglie e arrampicata.", "16 posti, autogestita", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

def num(t):
    """Cifre in Geist Mono (posti, tempi): «80 posti» → «<span class="num">80</span> posti»."""
    return re.sub(r"\d+(?:[.,:’']\d+)*(?:h\d*)?", lambda m: f'<span class="num">{m.group()}</span>', t)


def schede_capanne(lista, accesso="Accesso da", prefisso=""):
    """Home: le sei capanne in schede compatte (foto, nome, quota, valle, stato, posti e accesso)."""
    return "\n".join(f"""<a class="hut" href="{prefisso}{f}" data-reveal>
<figure>{img(im, f'Capanna {n}', w, h)}</figure>
<div class="hut-head"><h3 class="h3">{n}</h3><span class="hut-alt">{q} m</span></div>
<div class="hut-meta"><span>{v}</span><span class="status">{st}</span></div>
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


def home():
    prossime = prossime_gite()
    huts = schede_capanne(HUTS)

    html = head("CAS Ticino | Club Alpino Svizzero, Sezione Ticino",
                "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età. Da oltre un secolo, la casa dell’alpinismo ticinese.",
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n<link rel="preload" as="image" href="assets/img/paesaggi/sciatori-villaggio-2000.webp" imagesrcset="assets/img/paesaggi/sciatori-villaggio-1000.webp 1000w, assets/img/paesaggi/sciatori-villaggio-2000.webp 2000w" imagesizes="100vw" media="(min-width: 701px)">\n')
    html += "\n<body>\n" + nav("index.html") + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">In montagna<br>con <span class="accent">noi</span>.</h1>
<div class="hero-foot">
<div class="hero-testo">
<p class="lead">Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età.</p>
{social()}
</div>
<div class="actions">
<a class="btn btn--primary" href="adesione.html">Diventa socio <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="news.html">Ultime news</a>
</div>
</div>
</div>
<figure class="band">
{pic("paesaggi/sciatori-villaggio", "Scialpinisti in salita verso un villaggio innevato", mobile="paesaggi/sciatori-villaggio-4x3", w=2000, h=901, lazy=False, cls="pos-low")}
</figure>
</section>

<section class="section section--tight section--stats" id="sezione" aria-label="La sezione in cifre">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>anno di fondazione</span></div>
<div class="stat"><strong>3000</strong><span>soci</span></div>
<div class="stat"><strong>6</strong><span>rifugi, {num("362")} posti letto</span></div>
<div class="stat"><strong>5</strong><span>discipline insegnate nei corsi</span></div>
</div>
</div>
</section>

<section class="section--surface section--tight" id="news" aria-labelledby="news-h">
<div class="container">
<div class="section-row">
<h2 id="news-h" class="h2">News</h2>
<div class="links"><a class="link" href="news.html">Tutte le news</a><a class="link" href="foto.html">Foto e resoconti</a></div>
</div>
<div class="scorri scorri--news" data-reveal>
<div class="scorri-traccia">
{chr(10).join(news_card(n) for n in NEWS[:8])}
</div>
</div>
</div>
</section>

<section class="section" id="attivita" aria-labelledby="attivita-h">
<div class="container">
<div class="section-head">
<h2 id="attivita-h" class="h2">Fuori con la sezione</h2>
<p class="lead">Gite per tutti i livelli, un gruppo per ogni età e corsi per imparare a muoversi in montagna in sicurezza.</p>
</div>
<div class="bento" id="gruppi">
<article class="tile tile--wide-top" data-reveal>
{img("attivita/gite-2x1", "Gruppo in vetta con vista sulle Alpi innevate", 1400, 700)}
<div class="tile-body">
<span class="label">Programma gite 2026</span>
<h3 class="h2">Gite, escursioni e uscite della sezione</h3>
<p>Escursionismo, alpinismo, sci alpinismo, racchette e arrampicata: il calendario completo con iscrizioni online.</p>
<div class="actions"><a class="btn btn--primary" href="{GITE}">Programma gite</a><a class="btn btn--ghost-light" href="foto.html">Foto e resoconti</a></div>
</div>
</article>
<article class="tile tile--tall" data-reveal>
{img("attivita/giovani-3x4", "Giovane arrampicatore su una parete dei Denti della Vecchia", 800, 1066)}
<div class="tile-body">
<span class="label">Gruppo giovani, dagli anni ’60</span>
<h3 class="h2">Giovani</h3>
<p>Arrampicata, escursioni e settimane in montagna con monitori della sezione.</p>
<div class="links"><a class="link" href="giovani.html">Gruppo giovani</a><a class="link" href="organizzazione.html#giovani">Organizzazione</a></div>
</div>
</article>
<article class="tile tile--bottom-1" data-reveal>
{img("attivita/senior-2x1", "Escursionisti su un sentiero di cresta", 1000, 500)}
<div class="tile-body">
<span class="label">Gruppo senior, dal 1940</span>
<h3 class="h2">Senior</h3>
<p>Uscite settimanali con capigita esperti, al ritmo giusto e in buona compagnia, dalla Capriasca alle Alpi.</p>
<div class="links"><a class="link" href="senior.html">Gruppo senior</a><a class="link" href="organizzazione.html#senior">Organizzazione</a></div>
</div>
</article>
<article class="tile tile--bottom-2" id="corsi" data-reveal>
{img("corsi/alpinismo-4x5", "Cordata su una cresta di neve", 594, 742)}
<div class="tile-body">
<span class="label">Tenuti da professionisti</span>
<h3 class="h2">Corsi</h3>
<p>Alpinismo, sci alpinismo, arrampicata, freeride e racchette: per imparare a muoversi in montagna in sicurezza.</p>
<div class="links"><a class="link" href="corsi.html">Tutti i corsi</a><a class="link" href="noleggio.html">Noleggio materiale</a></div>
</div>
</article>
</div>
{f"""<div class="prossime" data-reveal>
<div class="section-row">
<h3 class="h3">Prossime gite</h3>
<a class="link" href="{GITE}">Tutto il programma</a>
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
<h2 id="capanne-h" class="h2">Sei capanne, un solo Ticino</h2>
<p class="lead">Sempre aperte, custodite quando i guardiani sono presenti. Prima di partire, contatta il guardiano per verificare presenza e condizioni della montagna.</p>
</div>
<div class="huts">
{huts}
</div>
<div class="callout callout--accent">
<p><strong>Cerchiamo «api operaie».</strong> I volontari aiutano i guardiani ad aprire, chiudere e mantenere le capanne, e passano qualche bella serata in quota.</p>
<a class="btn btn--light" href="mailto:info@casticino.ch">Voglio aiutare <span class="arrow" aria-hidden="true">→</span></a>
</div>
</div>
</section>

{banda_adesione("Sali con noi.", "Tariffe ridotte nelle capanne CAS di tutta la Svizzera, corsi, gite e una comunità che ama la montagna quanto te.", "Diventa socio", "adesione.html")}

</main>
""" + footer()
    return html


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


def band_img(name, alt, w, h):
    return f'<figure class="band">\n{img(name, alt, w, h, lazy=False)}\n</figure>'


# ------------------------------------------------------------------ capanne

HUT_PAGES = {
    "campotencia.html": dict(
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
        name="Cristallina", where="Passo Cristallina, Valle Bedretto", alt_m="2575", beds="100", custody="da giugno a metà ottobre",
        mail="cristallina@casticino.ch", booking=PRENOTA.format(20), facebook="https://www.facebook.com/capannacristallinacas/",
        description="Capanna Cristallina, 2575 m, sul Passo Cristallina tra Leventina e Valle Maggia: 100 posti letto, custodita da giugno a metà ottobre. Contatti e prenotazioni.",
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


# testi fissi delle pagine capanna
TC = {
    "it": dict(prenota="Prenota", cucina="La cucina", team="Chi vi accoglie", vita="La cucina e i guardiani",
               tariffe="Tariffe e prenotazioni", accessi="Come arrivare", attivita="Attività", sostenitori="Sostenitori",
               storia="Storia", storia_link="La storia della capanna", foto="Foto", tutte_foto="Tutte le foto",
               in_breve="In breve", testo="Testo", itinerari="Itinerari", capanne="Le capanne", sezione_menu="Capanne",
               foto_lead="La capanna, la cucina e i dintorni", tocca="Tocca una foto per vederla grande.",
               foto_desc="Foto della Capanna {n} e dei dintorni.", avviso="Avviso", altitudine="Altitudine",
               posti="Posti letto", custodia="Custodia", apertura="Apertura", la_capanna="La capanna",
               soggiorno="Soggiorno", arrivare="Arrivare", contatti_h="Senti il guardiano prima di partire",
               contatti_p="Verifica sempre la presenza del guardiano e le condizioni della montagna.",
               altre="Le altre capanne", capanna="Capanna", n_foto="foto", accesso_da="Accesso da", pdf="",
               fb_h="Dalla capanna", fb_notizie="Ultime notizie", fb_p="Le ultime notizie della capanna, pubblicate dai guardiani su Facebook.",
               fb_carica="Mostra i post", fb_privacy="I post vengono caricati da Facebook solo dopo il clic: da quel momento Facebook riceve dati sulla tua visita.",
               fb_apri="Apri la pagina Facebook"),
    "de": dict(prenota="Reservieren", cucina="Die Küche", team="Ihre Gastgeber", vita="Küche und Hüttenteam",
               tariffe="Preise und Reservation", accessi="Anreise", attivita="Aktivitäten", sostenitori="Unterstützer",
               storia="Geschichte", storia_link="Die Geschichte der Hütte", foto="Fotos", tutte_foto="Alle Fotos",
               in_breve="Auf einen Blick", testo="Text", itinerari="Routen", capanne="Die Hütten", sezione_menu="Hütten",
               foto_lead="Die Hütte, die Küche und die Umgebung", tocca="Tippen Sie auf ein Foto, um es gross zu sehen.",
               foto_desc="Fotos der Capanna {n} und ihrer Umgebung.", avviso="Hinweis", altitudine="Höhe",
               posti="Schlafplätze", custodia="Bewartet", apertura="Öffnung", la_capanna="Die Hütte",
               soggiorno="Aufenthalt", arrivare="Zugang", contatti_h="Vor dem Aufbruch beim Hüttenwart melden",
               contatti_p="Erkundigen Sie sich immer, ob der Hüttenwart da ist, und informieren Sie sich über die Verhältnisse am Berg.",
               altre="Die anderen Hütten", capanna="Capanna", n_foto="Foto", accesso_da="Zugang ab", pdf=" (italienisch)",
               fb_h="Aus der Hütte", fb_notizie="Aktuelles", fb_p="Die neusten Nachrichten der Hütte, vom Hüttenteam auf Facebook veröffentlicht (meist italienisch).",
               fb_carica="Beiträge anzeigen", fb_privacy="Die Beiträge werden erst nach dem Klick von Facebook geladen: ab dann erhält Facebook Daten über Ihren Besuch.",
               fb_apri="Facebook-Seite öffnen"),
    "en": dict(prenota="Book", cucina="The kitchen", team="Your hosts", vita="Kitchen and hut team",
               tariffe="Rates and booking", accessi="Getting there", attivita="Activities", sostenitori="Supporters",
               storia="History", storia_link="The history of the hut", foto="Photos", tutte_foto="All photos",
               in_breve="At a glance", testo="Text", itinerari="Routes", capanne="The huts", sezione_menu="Huts",
               foto_lead="The hut, the kitchen and the surroundings", tocca="Tap a photo to see it full size.",
               foto_desc="Photos of Capanna {n} and its surroundings.", avviso="Notice", altitudine="Altitude",
               posti="Beds", custodia="Staffed", apertura="Opening", la_capanna="The hut",
               soggiorno="Your stay", arrivare="Getting there", contatti_h="Check with the hut keeper before you set out",
               contatti_p="Always check that the hut keeper is there and find out about conditions in the mountains.",
               altre="The other huts", capanna="Capanna", n_foto="photo", accesso_da="Access from", pdf=" (in Italian)",
               fb_h="From the hut", fb_notizie="Latest news", fb_p="The hut’s latest news, posted by the hut team on Facebook (mostly in Italian).",
               fb_carica="Show posts", fb_privacy="Posts are only loaded from Facebook after you click: from then on Facebook receives data about your visit.",
               fb_apri="Open the Facebook page"),
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
        cucina = f"""<div class="hut-cuisine">
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
{foto}
<div class="prose">
{t["testo"]}
</div>
{persone}
</div>"""
        out.append(f"""<section class="section" aria-label="{tc('vita')}">
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
<div class="container detail">
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
<div class="detail hut-activities">
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
    if c.get("sostenitori"):
        loghi = "\n".join(f'<li>{cimg(c, "sostenitori/" + f, nome)}</li>' for nome, f in c["sostenitori"]["loghi"])
        out.append(f"""<section class="section" aria-labelledby="sostenitori-h">
<div class="container">
<div class="section-head">
<h2 id="sostenitori-h" class="h2">{tc('sostenitori')}</h2>
<p>{c["sostenitori"]["testo"]}</p>
</div>
<ul class="logos">
{loghi}
</ul>
</div>
</section>""")
    if c.get("storia"):
        st = c["storia"]
        out.append(f"""<section class="section" aria-labelledby="storia-h">
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
        out.append(f"""<section class="section" aria-labelledby="foto-h">
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
<a class="link" href="{d['facebook']}" rel="noopener">{tc('fb_apri')} <span class="arrow" aria-hidden="true">→</span></a>
</div>
<div class="fb-feed" data-fb="{d['facebook']}" data-lang="{tr('it_IT', 'de_DE', 'en_GB')}" data-titolo="Facebook {d['name']}">
<button type="button" class="btn btn--secondary">{tc('fb_carica')}</button>
<p class="small">{tc('fb_privacy')}</p>
</div>
</div>
</div>
</section>
"""


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
    avviso = f"""

<section class="section section--tight" aria-label="{tc('avviso')}">
<div class="container">
<div class="callout">
<p>{c["avviso"]}</p>
{prenota(d, "btn btn--secondary")}
</div>
</div>
</section>""" if c and c.get("avviso") else ""
    testo = f'\n<div class="prose">\n{c["capanna"]}\n</div>' if c and c.get("capanna") else ""
    body = page_hero([(tc("capanne"), L("index.html#capanne")), (d["name"], None)], d["name"], d["where"], extra) + f"""

{band}{avviso}

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
{facts(d['reach'])}
</div>
</div>
</div>
</section>

{hut_extra(file) if c else ""}
{facebook(d)}

<section class="section" aria-labelledby="contatti-h">
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

<section class="section" aria-labelledby="altre-h">
<div class="container">
<div class="section-head"><h2 id="altre-h" class="h3">{tc('altre')}</h2></div>
<div class="mini-huts">
{mini}
</div>
</div>
</section>"""
    prefix = tc("capanna") + " " if file != "baitadelluca.html" else ""
    nome = L(file)
    return pubblica(nome, page(nome, f"{prefix}{d['name']} | CAS Ticino", d["description"], body, og=og))


# ------------------------------------------------------------------ la sezione

def introduzione():
    huts = ('<a href="campotencia.html">Campo Tencia</a>, <a href="cristallina.html">Cristallina</a>, <a href="adula.html">Adula</a>, '
            '<a href="motterascio.html">Motterascio (Michela)</a>, <a href="montebar.html">Monte Bar</a> e <a href="baitadelluca.html">Baita del Luca</a>')
    body = page_hero([("La Sezione", "index.html#sezione"), ("Introduzione", None)], "La sezione",
                     "Fondata a Bellinzona l’11 aprile 1886, la Sezione Ticino del Club Alpino Svizzero conta quasi 3000 soci e propone un’attività varia, pensata per tutte le età: dai più giovani ai seniori.") + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", "Gruppo di alpinisti in cammino su un ghiacciaio", mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
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
    ("Sport di montagna", "Geoffroy Jolly", None),
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
    "Responsabile comunicazione": "Verantwortlicher Kommunikation", "Redazione annuario": "Redaktion Jahrbuch", "Eventi": "Anlässe",
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
    "Responsabile comunicazione": "Head of communication", "Redazione annuario": "Yearbook editor", "Eventi": "Events",
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
        body = page_hero([("La Sezione", "index.html#sezione"), ("Comitato", None)], "Il comitato",
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
     [("Dario Lanfranconi", "Responsabile comunicazione"),
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
            foto = f"assets/img/persone/{CARTELLE_DICASTERI[title]}/{slug_nome(name)}.webp"
            ph = (f'<img src="{foto}" alt="{tr("Ritratto di", "Porträt von", "Portrait of")} {name}" width="60" height="60" loading="lazy" decoding="async">'
                  if os.path.exists(os.path.join(ROOT, foto)) else f'<span aria-hidden="true">{initials(name)}</span>')
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
        body = page_hero([("La Sezione", "index.html#sezione"), ("Organizzazione", None)], "Organizzazione",
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
    "it": dict(titolo="Capigita", sezione="La Sezione", sezione_href="index.html#sezione", ritratto="Ritratto di", chi="Chi è",
               dal="Capogita dal", tutti="Tutti", filtra="Filtra per ruolo", elenco="Elenco dei capigita",
               uno="capogita", molti="capigita",
               lead="Le gite della sezione sono preparate e guidate da soci volontari, formati nei corsi del CAS: {n} capigita attivi, ognuno con le sue discipline.",
               box="<strong>Per i capigita.</strong> Le gite si pubblicano sul portale Droptour; il promemoria raccoglie compiti e procedure del capogita.",
               portale="Portale Droptour", promemoria="Promemoria capigita (PDF)",
               desc="I {n} capigita del CAS Ticino che preparano e guidano le gite della sezione: estive e invernali, arrampicata, escursionismo e seniori."),
    "de": dict(titolo="Tourenleitende", sezione="Die Sektion", sezione_href="de/introduzione.html", ritratto="Porträt von", chi="Wer ist",
               dal="Tourenleitung seit", tutti="Alle", filtra="Nach Rolle filtern", elenco="Liste der Tourenleitenden",
               uno="Tourenleitende", molti="Tourenleitende",
               lead="Die Touren der Sektion werden von ehrenamtlichen Mitgliedern vorbereitet und geleitet, ausgebildet in den Kursen des SAC: {n} aktive Tourenleitende, alle mit ihren eigenen Disziplinen.",
               box="<strong>Für Tourenleitende.</strong> Die Touren werden im Droptour-Portal veröffentlicht; das Merkblatt fasst Aufgaben und Abläufe der Tourenleitung zusammen.",
               portale="Droptour-Portal", promemoria="Merkblatt Tourenleitung (PDF, italienisch)",
               desc="Die {n} Tourenleitenden des SAC Ticino, die die Touren der Sektion vorbereiten und leiten: Sommer- und Wintertouren, Klettern, Wandern und Senioren."),
    "en": dict(titolo="Trip leaders", sezione="The Section", sezione_href="en/introduzione.html", ritratto="Portrait of", chi="Who is",
               dal="Trip leader since", tutti="All", filtra="Filter by role", elenco="List of trip leaders",
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
    schede = []
    for p in persone:
        foto = foto_persona(p["nome"], "capigita")
        ph = (f'<img src="{foto}" alt="{tx["ritratto"]} {p["nome"]}" width="60" height="60" loading="lazy" decoding="async">'
              if foto else f'<span aria-hidden="true">{initials(p["nome"])}</span>')
        ruoli = " · ".join(nomi[r] for r in p["ruoli"])
        dal = f'<span>{tx["dal"]} <span class="num">{p["dal"]}</span></span>' if p.get("dal") else ""
        corpo = f'<div class="member-body"><strong>{p["nome"]}</strong><span>{ruoli}</span>{dal}</div>'
        bio = info.get(p["nome"])
        if bio:
            id_bio = "bio-" + slug_nome(p["nome"])
            lang = "" if LINGUA["lang"] == "it" else ' lang="it"'
            schede.append(f'<div class="member member--bio" data-ruoli="{" ".join(p["ruoli"])}">'
                          f'<button type="button" class="bio-toggle" aria-expanded="false" aria-controls="{id_bio}" aria-label="{tx["chi"]} {p["nome"]}">'
                          f'<span class="member-photo">{ph}</span><span class="bio-segno" aria-hidden="true"></span></button>'
                          f'{corpo}<p class="bio" id="{id_bio}"{lang}>{html_escape(bio)}</p></div>')
        else:
            schede.append(f'<div class="member" data-ruoli="{" ".join(p["ruoli"])}"><div class="member-photo">{ph}</div>{corpo}</div>')
    conta = {k: sum(k in p["ruoli"] for p in persone) for k, _ in RUOLI_CAPIGITA}
    filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">{tx["tutti"]} <span class="num">{len(persone)}</span></button>'] +
                       [f'<button type="button" data-filtro="{k}" aria-pressed="false">{nomi[k]} <span class="num">{conta[k]}</span></button>'
                        for k, _ in RUOLI_CAPIGITA if conta[k]])
    n = len(persone)
    body = page_hero([(tx["sezione"], tx["sezione_href"]), (tx["titolo"], None)], tx["titolo"], tx["lead"].format(n=n)) + f"""

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
    emergenza = [("Rega", '<a class="num" href="tel:1414">1414</a> <span class="small">dall’estero <a class="num" href="tel:+41333333333">+41 333 333 333</a></span>'),
                 ("Ambulanza", '<a class="num" href="tel:144">144</a>'),
                 ("Emergenza europeo", '<a class="num" href="tel:112">112</a>')]
    body = page_hero([("Attività", "index.html#attivita"), ("Soccorso", None)], "Soccorso",
                     "La sezione coordina il soccorso alpino nel Sottoceneri, con volontari formati che intervengono in montagna insieme al Soccorso Alpino Svizzero e alla Rega.",
                     figure=img("attivita/soccorso-4x5", "Soccorritori con casco e imbragatura recuperano una persona in barella in una gola rocciosa", 525, 657, lazy=False)) + f"""

<section class="section" aria-labelledby="emergenza-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="emergenza-h" class="h2">In caso di emergenza</h2>
<p>Chiama subito: indica chi sei, dove ti trovi, cosa è successo e quante persone sono coinvolte. Resta raggiungibile al telefono.</p>
</div>
{facts(emergenza)}
</div>
</div>
</section>

<section class="section" aria-labelledby="colonna-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="colonna-h" class="h2">La colonna<br>di soccorso</h2>
<p>Dal 1918, quando nacquero le prime stazioni di soccorso alpino a Faido, Airolo e Olivone, la sezione è parte del soccorso in montagna in Ticino.</p>
</div>
<div class="prose" data-reveal>
<p>Qui troverai presto le informazioni sulla colonna di soccorso della sezione: chi la compone, come è organizzata, la formazione dei soccorritori e come entrare a farne parte.</p>
<p class="small">Pagina in preparazione. Foto: Soccorso Alpino Svizzero / Urs Nett.</p>
<div class="actions"><a class="btn btn--secondary" href="https://www.alpinerettung.ch" rel="noopener">Soccorso Alpino Svizzero</a><a class="btn btn--secondary" href="https://www.rega.ch" rel="noopener">Rega</a></div>
</div>
</div>
</section>

{subnav("Attività", "soccorso.html")}"""
    return page("soccorso.html", "Soccorso | CAS Ticino",
                "Il soccorso alpino del CAS Ticino nel Sottoceneri: numeri d’emergenza (Rega 1414, 144, 112) e la colonna di soccorso della sezione.",
                body)


def sede():
    rows = [
        ("Recapito postale", "Club Alpino Svizzero<br>Sezione Ticino<br>Casella postale 112<br>6998 Monteggio 2"),
        ("E-mail", '<a href="mailto:info@casticino.ch">info@casticino.ch</a>'),
        ("Sede", "Stabile Canvetto Luganese, Molino Nuovo (Lugano)<br>2° piano, in balconata"),
        ("Biblioteca", 'Guide e cartine da consultare, libri in prestito; in vendita libri e magliette. Per visitarla scrivi al segretariato: <a href="mailto:info@casticino.ch">info@casticino.ch</a>.'),
        ("Coordinate bancarie", 'Banca Stato, Lugano<br><span class="num">IBAN CH09 0076 4128 9526 1200 6</span>'),
    ]
    body = page_hero([("La Sezione", "index.html#sezione"), ("Sede e recapiti", None)], "Sede e recapiti",
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

{subnav("La Sezione", "sede.html")}"""
    return page("sede.html", "Sede e recapiti | CAS Ticino",
                "Sede del CAS Ticino al Canvetto Luganese (Molino Nuovo), recapito postale, e-mail, biblioteca e coordinate bancarie.",
                body)


STORIA = [
    ("1886", "L’11 aprile, alla Birraria Gambrinus di Bellinzona, nasce il Club Alpino Ticinese, nell’anno del centenario della prima salita al Monte Bianco. Primo presidente è l’avvocato Curzio Curti. Lo scopo: visitare, studiare e far conoscere le montagne del Cantone e delle regioni vicine."),
    ("1887", "Il 20 marzo il club si unisce al Club Alpino Svizzero come sezione ticinese; Lugano ne diventa la sede."),
    ("1911", "A Lanzo d’Intelvi viene inaugurato il vessillo sezionale."),
    ("1913", "Nasce la sezione di Lugano del Club Alpino Femminile Svizzero, presieduta da Adelina Rossi-Baragiola."),
    ("1918", "Si costituiscono le stazioni di soccorso alpino di Faido, Airolo e Olivone. La formazione delle guide spetta alla sezione, la nomina al Consiglio di Stato."),
    ("Anni ’30", "Cresce l’arrampicata su roccia: Emilio Comici, il numero uno dell’alpinismo italiano, viene invitato ai Denti della Vecchia. Nel 1932 Tita Calvi, don Giugni e Aldo Balmelli aprono la Nord-Est del Piz Prevat; Bruno Primi «Stüva» diventa guida e firma grandi classiche, dal Civetta al Cervino."),
    ("1936", "Prima presenza di soci nell’Himalaya centrale, seguita da Lapponia (1959), Huascarán (1977) e Pumori (1978)."),
    ("1940", "Nasce il gruppo Seniori."),
    ("Anni ’60", "Nasce il gruppo giovanile OG ed entra in servizio la colonna di soccorso del Sottoceneri. Nel 1963 l’alpinista Aldo Fontana porta nuovi stimoli; nel 1964 nasce il Gruppo Scoiattoli."),
    ("1980", "Le sezioni maschile e femminile si fondono."),
    ("1982", "Prima edizione della «settimana mini» per i più piccoli."),
    ("2003", "Inaugurata la nuova Capanna Cristallina, progettata da Baserga e Mozzetti."),
    ("2016", "Conclusa la ricostruzione della Capanna Monte Bar."),
]


STORIA_DE = [
    ("1886", "Am 11. April wird in der Birraria Gambrinus in Bellinzona der Club Alpino Ticinese gegründet, im Jahr des hundertjährigen Jubiläums der Erstbesteigung des Mont Blanc. Erster Präsident ist Rechtsanwalt Curzio Curti. Das Ziel: die Berge des Kantons und der Nachbarregionen besuchen, erforschen und bekannt machen."),
    ("1887", "Am 20. März schliesst sich der Club als Tessiner Sektion dem Schweizer Alpen-Club an; Sitz ist Lugano."),
    ("1911", "In Lanzo d’Intelvi wird die Sektionsfahne eingeweiht."),
    ("1913", "Die Sektion Lugano des Schweizerischen Frauen-Alpen-Clubs wird gegründet, unter dem Vorsitz von Adelina Rossi-Baragiola."),
    ("1918", "Die Rettungsstationen von Faido, Airolo und Olivone entstehen. Die Ausbildung der Bergführer liegt bei der Sektion, die Ernennung beim Staatsrat."),
    ("1930er-Jahre", "Das Felsklettern gewinnt an Bedeutung: Emilio Comici, die Nummer eins des italienischen Alpinismus, wird an die Denti della Vecchia eingeladen. 1932 eröffnen Tita Calvi, Don Giugni und Aldo Balmelli die Nordostwand des Piz Prevat; Bruno Primi «Stüva» wird Bergführer und begeht grosse Klassiker, von der Civetta bis zum Matterhorn."),
    ("1936", "Erste Mitglieder im zentralen Himalaya, später folgen Lappland (1959), Huascarán (1977) und Pumori (1978)."),
    ("1940", "Die Seniorengruppe wird gegründet."),
    ("1960er-Jahre", "Die Jugendorganisation JO entsteht, und die Rettungskolonne Sottoceneri nimmt ihren Dienst auf. 1963 bringt der Bergsteiger Aldo Fontana neue Impulse; 1964 entsteht die Gruppo Scoiattoli."),
    ("1980", "Die Männer- und die Frauensektion schliessen sich zusammen."),
    ("1982", "Erste Ausgabe der «Mini-Woche» für die Kleinsten."),
    ("2003", "Die neue Capanna Cristallina von Baserga und Mozzetti wird eingeweiht."),
    ("2016", "Der Neubau der Capanna Monte Bar ist abgeschlossen."),
]


STORIA_EN = [
    ("1886", "On 11 April, at the Birraria Gambrinus in Bellinzona, the Club Alpino Ticinese is founded, in the centenary year of the first ascent of Mont Blanc. Its first president is the lawyer Curzio Curti. Its aim: to visit, study and make known the mountains of the canton and the neighbouring regions."),
    ("1887", "On 20 March the club joins the Swiss Alpine Club as its Ticino section, based in Lugano."),
    ("1911", "The section banner is inaugurated in Lanzo d’Intelvi."),
    ("1913", "The Lugano section of the Swiss Women’s Alpine Club is founded, chaired by Adelina Rossi-Baragiola."),
    ("1918", "Mountain rescue stations are set up in Faido, Airolo and Olivone. Training the guides is the section’s task; appointing them is up to the cantonal government."),
    ("1930s", "Rock climbing grows: Emilio Comici, the leading Italian alpinist of the day, is invited to the Denti della Vecchia. In 1932 Tita Calvi, Don Giugni and Aldo Balmelli open the north-east face of Piz Prevat; Bruno Primi “Stüva” becomes a guide and climbs great classics, from the Civetta to the Matterhorn."),
    ("1936", "First members in the central Himalaya, followed by Lapland (1959), Huascarán (1977) and Pumori (1978)."),
    ("1940", "The Seniors group is founded."),
    ("1960s", "The OG youth group is founded and the Sottoceneri rescue team goes into service. In 1963 the climber Aldo Fontana brings new energy; in 1964 the Gruppo Scoiattoli is founded."),
    ("1980", "The men’s and women’s sections merge."),
    ("1982", "First edition of the “mini week” for the youngest children."),
    ("2003", "The new Capanna Cristallina, designed by Baserga and Mozzetti, is inaugurated."),
    ("2016", "The rebuilding of Capanna Monte Bar is completed."),
]


def storia():
    tl = "\n".join(f'<li><span class="year">{y}</span><span>{t}</span></li>' for y, t in tr(STORIA, STORIA_DE, STORIA_EN))
    if de():
        body = page_hero([("Die Sektion", "de/introduzione.html"), ("Geschichte", None)], "Seit 1886<br>zu Fuss unterwegs.",
                         "Mehr als ein Jahrhundert Besteigungen, Hütten, Rettung und Bergkultur: die Geschichte der Sektion in Etappen.")
    elif en():
        body = page_hero([("The Section", "en/introduzione.html"), ("History", None)], "Since 1886,<br>on foot.",
                         "More than a century of climbs, huts, rescue and mountain culture: the history of the section in milestones.")
    else:
        body = page_hero([("La Sezione", "index.html#sezione"), ("Storia", None)], "Dal 1886,<br>a piedi.",
                         "Più di un secolo di salite, rifugi, soccorso e cultura alpina: la storia della sezione in tappe.")
    body += f"""

<figure class="band">
{pic("paesaggi/capanna-tencia", tr("La Capanna Campo Tencia all’alba, con la bandiera svizzera e le montagne in controluce", "Die Campo-Tencia-Hütte bei Sonnenaufgang, mit Schweizer Fahne und Bergen im Gegenlicht", "Campo Tencia hut at sunrise, with the Swiss flag and backlit mountains"), mobile="paesaggi/capanna-tencia-4x3", w=2000, h=658, lazy=False)}
</figure>

<section class="section" aria-labelledby="tappe-h">
<div class="container split">
<div class="split-intro">
<h2 id="tappe-h" class="h2">{tr("Le tappe", "Die Etappen", "Milestones")}</h2>
<p class="lead">{tr("Accanto all’attività sul terreno, la sezione ha sempre organizzato proiezioni, conferenze e dibattiti, e documentato la propria vita in numerose pubblicazioni e negli annuari.", "Neben den Touren hat die Sektion immer Vorführungen, Vorträge und Diskussionen organisiert und ihr Leben in zahlreichen Publikationen und in den Jahrbüchern festgehalten.", "Alongside its activity in the mountains, the section has always organised slide shows, talks and debates, and recorded its life in many publications and in its yearbooks.")}</p>
</div>
<ol class="timeline" data-reveal>
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
        hero = page_hero([("Die Sektion", "de/introduzione.html"), ("Nützliche Links", None)], "Nützliche Links",
                         "Wetter, Lawinenbulletins, Verhältnisse, Karten und die anderen Bergsteigervereine der Region.")
    elif en():
        gruppi = [(LINKS_EN.get(g, g), [(LINKS_EN.get(n, n), u) for n, u in links]) for g, links in LINKS]
        hero = page_hero([("The Section", "en/introduzione.html"), ("Useful links", None)], "Useful links",
                         "Weather, avalanche bulletins, conditions, maps and the other mountaineering clubs in the region.")
    else:
        gruppi = LINKS
        hero = page_hero([("La Sezione", "index.html#sezione"), ("Link utili", None)], "Link utili",
                         "Meteo, bollettini valanghe, condizioni, cartine e le altre realtà alpinistiche del territorio.")
    body = hero + f"""

<section class="section" aria-label="Link">
<div class="container">
{linkgroups(gruppi, "↗")}
</div>
</section>

{subnav(tr("La Sezione", "Die Sektion", "The Section"), L("link.html"))}"""
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


def documenti():
    body = page_hero([("Media", "foto.html"), ("Documenti", None)], "Documenti",
                     "Statuto e documenti della sezione, scale di difficoltà, promemoria tecnici, documenti dei corsi, moduli e cartine da scaricare.") + f"""

<section class="section" aria-label="Documenti">
<div class="container">
{linkgroups(DOCS, "PDF")}
<div class="callout">
<p><strong>Annuari e Informazione</strong>, il bollettino della sezione, hanno una pagina propria.</p>
<div class="actions"><a class="btn btn--secondary" href="annuari.html">Annuari</a><a class="btn btn--secondary" href="informazione.html">Informazione</a></div>
</div>
</div>
</section>

{subnav("Media", "documenti.html")}"""
    return page("documenti.html", "Documenti | CAS Ticino",
                "Documenti del CAS Ticino da scaricare: scale di difficoltà, promemoria tecnici, promemoria capigita, obiettivi ed equipaggiamento dei corsi, pianificazione e cartine.",
                body)


# ------------------------------------------------------------------ news, foto, adesione

def carica_news():
    """Le news di data/news/*.json (vedi news_util.py) pronte per le pagine: testo in HTML, foto con le dimensioni, estratto."""
    out, presi = [], set()
    for n in news_util.leggi_tutte():
        corpo = news_util.md_html(n["testo"]) if (n.get("testo") or "").strip() else n.get("html", "")
        corpo = "\n".join(x for x in (corpo, news_util.allegati_html(n.get("allegati"))) if x)
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


def news_meta(n):
    cat = f'<span>{esc(n["category"])}</span>' if n["category"] else ""
    return f'<p class="news-meta"><time datetime="{n["date"]}">{data_it(n["date"])}</time>{cat}</p>'


def news_card(n, feature=False):
    """Scheda di una notizia: foto (o blocco rosso con la data se manca), data, titolo, estratto."""
    if n["image"]:
        im = n["image"]
        fig = f'<figure><img src="{im["src"]}" alt="" width="{im["w"]}" height="{im["h"]}" loading="lazy" decoding="async"></figure>'
    else:
        y, m, d = n["date"].split("-")
        fig = f'<figure class="news-noimg" aria-hidden="true"><strong>{int(d)}</strong><span>{MESI[int(m) - 1]} {y}</span></figure>'
    cls = "news-card news-card--feature" if feature else "news-card"
    tag = "h2" if feature else "h3"
    return f"""<a class="{cls}" href="{n['file']}">
{fig}
<div class="news-card-body">
{news_meta(n)}
<{tag}>{esc(n['title'])}</{tag}>
<p>{esc(n['excerpt'])}</p>
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
    gruppi = "\n".join(f"""<section class="news-year" id="anno-{y}" aria-labelledby="anno-{y}-h">
<h2 id="anno-{y}-h" class="news-year-h">{y}</h2>
<div class="news-grid">
{chr(10).join(news_card(n) for n in items)}
</div>
</section>""" for y, items in anni)
    body = page_hero([("News", None)], "News", "Serate, eventi, corsi e avvisi della sezione: tutte le notizie, dalla più recente.", social()) + f"""

<section class="section" aria-label="Ultima notizia">
<div class="container">
{news_card(NEWS[0], feature=True)}
</div>
</section>

<section class="section section--tight" aria-label="Archivio delle notizie">
<div class="container">
<nav class="subnav news-years" aria-label="Anni">
<h2 class="label">Archivio</h2>
<div class="subnav-links">
{salti}
</div>
</nav>
{gruppi}
</div>
</section>"""
    return page("news.html", "News | CAS Ticino",
                "Le notizie della Sezione Ticino del Club Alpino Svizzero: serate, eventi, corsi, avvisi di sicurezza e vita delle capanne.",
                body, og=og_name(NEWS[0]), section="News")


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
    prev = (f'<a class="article-prev" href="{meno_recente["file"]}"><span class="label">Notizia precedente</span><strong>{esc(meno_recente["title"])}</strong></a>'
            if meno_recente else "<span></span>")
    nxt = (f'<a class="article-next" href="{piu_recente["file"]}"><span class="label">Notizia successiva</span><strong>{esc(piu_recente["title"])}</strong></a>'
           if piu_recente else "<span></span>")
    altre = [x for x in NEWS[max(0, i - 2):i + 4] if x is not n][:3]
    body = f"""<section class="page-hero article-hero" aria-labelledby="page-h">
<div class="container">
{crumbs(("News", "news.html"), (esc(n["title"]), None))}
{news_meta(n)}
<h1 id="page-h" class="article-title">{esc(n["title"])}</h1>
</div>
</section>

<section class="section section--tight" aria-label="Testo">
<div class="container article{'' if fig else ' article--noimg'}">
{fig}
<div class="prose">
{corpo}
</div>
</div>
</section>

<section class="section section--tight" aria-labelledby="altre-h">
<div class="container">
<nav class="article-pager" aria-label="Notizia precedente e successiva">{prev}{nxt}</nav>
<div class="section-row">
<h2 id="altre-h" class="h3">Altre notizie</h2>
<a class="link" href="news.html">Tutte le news</a>
</div>
<div class="news-grid">
{chr(10).join(news_card(x) for x in altre)}
</div>
</div>
</section>"""
    su = "../" * n["file"].count("/")  # news/<anno>/… : due livelli sotto la radice
    return in_sottocartella(page(n["file"], f"{esc(n['title'])} | CAS Ticino", esc(n["excerpt"][:155]), body,
                                 og=og_name(n), section="News"), su=su)


# ------------------------------------------------------------------ programma gite (copia da Droptour)
# data/gite.json lo scrive scripts/update_gite.py; nella pagina assets/gite.js rilegge le gite in tempo reale
# dall'interfaccia pubblica di Droptour e le ridisegna con lo stesso markup di gita_html() (tenerli allineati).
GITE_ICS = "webcal://ssl.dropnet.ch/casticino/dropnetapps/tours/index.php?page=ics&amp;type=&amp;group=&amp;eventtype="
GITE_DETTAGLIO = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItem&language=it&item_id="
GITE_API = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItems&limit=500&language=it"
GIORNI_BREVI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
MESI_BREVI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
IMPEGNO = {"A": "poco impegnativo", "B": "abbastanza impegnativo", "C": "impegnativo", "D": "molto impegnativo"}


def gite_dati():
    try:
        return json.load(open(os.path.join(ROOT, "data", "gite.json"), encoding="utf-8")).get("gite", [])
    except OSError:
        return []


def gita_stato(g, oggi):
    """(classe, testo) dello stato delle iscrizioni, calcolato come in gite.js."""
    if g["stato"] == "annullata":
        return "annullata", "Annullata"
    if g["stato"] == "completa":
        return "completa", "Completa"
    if not g["iscrizione"]:
        return "", "Senza iscrizione online"
    if g["iscrizione_dal"] and oggi < g["iscrizione_dal"]:
        return "", f"Iscrizioni dal {data_breve(g['iscrizione_dal'])}"
    if g["iscrizione_al"] and oggi > g["iscrizione_al"]:
        return "", "Iscrizioni chiuse"
    return "aperte", "Iscrizioni aperte"


def fino_al(giorno):
    """«fino al 3», ma «fino all'1», «all'8», «all'11»."""
    return f"fino all’{giorno}" if giorno in (1, 8, 11) else f"fino al {giorno}"


def data_breve(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MESI_BREVI[m - 1]}"


def gita_html(g, oggi):
    import datetime
    d1 = datetime.date.fromisoformat(g["dal"])
    giorno, sotto = str(d1.day), GIORNI_BREVI[d1.weekday()]
    if g["al"] and g["al"] != g["dal"]:
        d2 = datetime.date.fromisoformat(g["al"])
        if d2.month == d1.month:
            giorno, sotto = f"{d1.day}–{d2.day}", f"{sotto}–{GIORNI_BREVI[d2.weekday()]}"
        else:
            sotto += f", {fino_al(d2.day)} {MESI_BREVI[d2.month - 1]}"
    classe, stato = gita_stato(g, oggi)
    gruppi = [x for x in g["gruppi"] if x != "Tutti"] or ["Tutti"]
    tipo = " · ".join(dict.fromkeys(filter(None, [esc(g["tipo"]), esc(", ".join(gruppi))])))
    meta = []
    if g["cond"]:
        meta.append(f'<span title="{IMPEGNO.get(g["cond"], "")}">Impegno {esc(g["cond"])}</span>')
    if g["tecn"]:
        meta.append(f'<span>Difficoltà {esc(g["tecn"])}</span>')
    if g["capigita"]:
        meta.append(f'<span>{"Capigita" if len(g["capigita"]) > 1 else "Capogita"}: {esc(", ".join(g["capigita"]))}</span>')
    posti = (f'{g["iscritti"]}/{g["posti"]} iscritti' if g["posti"] else f'{g["iscritti"]} iscritti' if g["iscritti"] else "")
    modalita = (f'<span class="gita-nota">Iscrizione{"" if g["modalita"].startswith("tramite") else ":"} {esc(g["modalita"])}</span>'
                if g["modalita"] and classe != "annullata" else "")
    return f"""<article class="gita{' gita--annullata' if classe == 'annullata' else ''}" id="gita-{g['id']}" data-fine="{g['al'] or g['dal']}" data-gruppi="{esc(' '.join(g['gruppi']))}" data-tipo="{esc(g['sigla'])}">
<p class="gita-data"><span class="gita-giorno num">{giorno}</span><span class="gita-sotto">{sotto}</span></p>
<div class="gita-corpo">
<p class="gita-tipo">{tipo}</p>
<h3 class="gita-titolo"><a href="gita.html?id={g['id']}">{esc(g['titolo'])}</a></h3>
{f'<p class="gita-meta">{"".join(meta)}</p>' if meta else ""}
</div>
<div class="gita-stato">
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
{f'<span class="gita-posti num">{posti}</span>' if posti else ""}{modalita}
<a class="link gita-link" href="gita.html?id={g['id']}">{"Dettagli" if classe == "annullata" or not g["iscrizione"] else "Dettagli e iscrizione"}</a>
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
            out.append(f'<section class="gite-mese" aria-labelledby="mese-{m}">\n<h2 id="mese-{m}" class="h3">{MESI[mm - 1].capitalize()} {y}</h2>\n<div class="gite-righe">')
            mese = m
        out.append(gita_html(g, oggi))
    if mese:
        out.append("</div>\n</section>")
    return "\n".join(out)



def prossime_gite(n=10):
    """Le prossime gite per la home, in una fila che scorre: senza annullate e senza le serate della colonna di soccorso.
    La pagina può restare indietro di un giorno (si rigenera ogni mattina), quindi site.js toglie quelle già passate (data-fine)."""
    import datetime
    oggi = datetime.date.today().isoformat()
    scelte = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi and g["stato"] != "annullata"
              and "colonna di soccorso" not in g["titolo"].lower()][:n]
    schede = []
    for g in scelte:
        d = datetime.date.fromisoformat(g["dal"])
        quando = f"{GIORNI_BREVI[d.weekday()]} {MESI[d.month - 1]}"
        if g["al"] and g["al"] != g["dal"]:
            d2 = datetime.date.fromisoformat(g["al"])
            quando += f", {fino_al(d2.day)}" + ("" if d2.month == d.month else f" {MESI_BREVI[d2.month - 1]}")
        classe, stato = gita_stato(g, oggi)
        gruppi = [x for x in g["gruppi"] if x != "Tutti"] or ["Tutti"]
        tipo = " · ".join(dict.fromkeys(filter(None, [esc(g["tipo"]), esc(", ".join(gruppi))])))
        schede.append(f"""<a class="prossima" href="gita.html?id={g['id']}" data-fine="{g['al'] or g['dal']}">
<p class="prossima-data"><span class="prossima-giorno num">{d.day}</span><span>{quando}</span></p>
<p class="gita-tipo">{tipo}</p>
<h3 class="prossima-titolo">{esc(g['titolo'])}</h3>
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
</a>""")
    return "\n".join(schede)


def gite():
    import datetime
    oggi = datetime.date.today().isoformat()
    lista = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi]
    body = page_hero([("Attività", "index.html#attivita"), ("Programma gite", None)], "Programma gite",
                     "Gite, corsi ed eventi della sezione, aggiornati in tempo reale dal portale Droptour, dove ci si iscrive.") + f"""

<section class="section" aria-label="Elenco delle gite">
<div class="container">
<div class="gite-filtri" id="gite-filtri" hidden>
<div class="filtro" role="group" aria-label="Filtra per gruppo" data-campo="gruppi"></div>
<div class="filtro" role="group" aria-label="Filtra per tipo" data-campo="tipo"></div>
<div class="filtri-tendina">
<label><span class="label">Gruppo</span><select data-campo="gruppi"></select></label>
<label><span class="label">Tipo</span><select data-campo="tipo"></select></label>
</div>
</div>
<p class="small filtro-stato" id="gite-stato" aria-live="polite"></p>
<div class="gite" id="gite" data-api="{GITE_API}" data-copia="{asset('data/gite.json')}">
{gite_lista(lista, oggi) if lista else '<p>Il programma non è disponibile in questo momento: lo trovi su <a href="' + GITE_DROPTOUR + '">Droptour</a>.</p>'}
</div>
<div class="callout">
<p>Le iscrizioni, l’accesso per soci e capigita e i dettagli di ogni gita sono sul portale Droptour. Per le domande su una gita scrivi al capogita, dalla pagina della gita.</p>
<div class="actions"><a class="btn btn--secondary" href="{GITE_DROPTOUR}" rel="noopener">Programma completo su Droptour</a><a class="btn btn--secondary" href="{GITE_ICS}">Calendario (iCal)</a><a class="btn btn--secondary" href="documenti.html">Scale di difficoltà</a></div>
</div>
</div>
</section>

{subnav("Attività", "gite.html")}"""
    return page("gite.html", "Programma gite | CAS Ticino",
                "Il programma delle gite, dei corsi e degli eventi della Sezione Ticino del Club Alpino Svizzero, con le iscrizioni su Droptour.",
                body, og="attivita/gite-2x1", section="Attività", scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n')


def gita_pagina():
    """Dettaglio di una gita: gita.html?id=<numero Droptour>, riempita da gite.js (dati in tempo reale da Droptour)."""
    body = page_hero([("Attività", "index.html#attivita"), ("Programma gite", "gite.html"), ("Gita", None)], "Gita",
                     "Caricamento della gita…").replace('class="display fit"', 'class="display display--gita fit"') + f"""

<section class="section" aria-label="Dettagli della gita">
<div class="container detail gita-dettaglio" id="gita" data-api="{GITE_API}" data-dettaglio="{GITE_DETTAGLIO}"
 data-droptour="{GITE_DROPTOUR}" data-copia="{asset('data/gite.json')}">
<aside class="gita-riepilogo" aria-label="La gita in breve" hidden>
<p id="gita-stato"></p>
<dl class="gita-chiave" id="gita-chiave"></dl>
<div class="actions" id="gita-azioni"></div>
</aside>
<div id="gita-dati"><noscript><p>Per vedere la gita serve JavaScript: la trovi nel <a href="{GITE_DROPTOUR}">programma su Droptour</a>.</p></noscript></div>
</div>
</section>

{subnav("Attività", "gita.html")}"""
    return page("gita.html", "Gita | CAS Ticino", "Dettagli di una gita della Sezione Ticino del CAS, con l’iscrizione su Droptour.",
                body, og="attivita/gite-2x1", section="Attività", scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n')


def foto():
    body = page_hero([("Media", "foto.html"), ("Foto e resoconti", None)], "Foto e resoconti", "Le foto e i resoconti delle ultime gite della sezione, pubblicati dai capigita sul portale Droptour.") + f"""

<section class="section" aria-label="Ultime gite">
<div class="container">
<div id="albums" aria-live="polite"><p class="albums-status">Caricamento delle foto…</p></div>
<div class="albums-more">
<button type="button" class="btn btn--secondary" id="load-more" hidden>Carica altre gite</button>
</div>
</div>
</section>

{subnav("Media", "foto.html")}"""
    return page("foto.html", "Foto e resoconti delle gite | CAS Ticino",
                "Le foto delle ultime gite della Sezione Ticino del Club Alpino Svizzero, con i resoconti dei capigita.",
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
<figure><img src="{x['cover']}" alt="Copertina: {titolo}" width="{x['w']}" height="{x['h']}" loading="lazy" decoding="async"></figure>
<strong>{titolo}</strong>
<span class="small">PDF {x['mb']}MB</span>
</a>"""


def pub_feature(x, titolo, testo):
    return f"""<div class="pub-feature" data-reveal>
<figure><img src="{x['cover']}" alt="Copertina: {titolo}" width="{x['w']}" height="{x['h']}"></figure>
<div class="pub-feature-body">
<span class="label">Ultimo numero</span>
<h2 class="h2">{titolo}</h2>
<p>{testo}</p>
<a class="btn btn--primary" href="{x['pdf']}">Leggi il PDF <span class="arrow" aria-hidden="true">→</span></a>
<span class="small">PDF {x['mb']}MB</span>
</div>
</div>"""


def annuari():
    items = pubblicazioni("annuari", "annuario")
    ultimo, altri = items[0], items[1:]
    body = page_hero([("Media", "foto.html"), ("Annuari", None)], "Annuari",
                     "L’annuario racconta la vita della sezione: un volume per ogni anno, da sfogliare in PDF.") + f"""

<section class="section" aria-label="Annuari">
<div class="container">
{pub_feature(ultimo, f"Annuario {ultimo['anno']}", "L’ultimo annuario pubblicato dalla sezione.")}
<div class="section-row"><h2 class="h3">Annate precedenti</h2></div>
<div class="pubs" data-reveal>
{chr(10).join(pub_card(x, f"Annuario {x['anno']}") for x in altri)}
</div>
</div>
</section>

{subnav("Media", "annuari.html")}"""
    return page("annuari.html", "Annuari | CAS Ticino",
                "Gli annuari della Sezione Ticino del Club Alpino Svizzero da scaricare in PDF.",
                body, og=ultimo["cover"][len("assets/img/"):-len(".webp")])


def informazione():
    items = pubblicazioni("informazione", "informazione")
    ultimo, altri = items[0], items[1:]
    griglia = (f"""<div class="section-row"><h2 class="h3">Numeri precedenti</h2></div>
<div class="pubs" data-reveal>
{chr(10).join(pub_card(x, f"Informazione, {x['quando']}") for x in altri)}
</div>""" if altri else "")
    body = page_hero([("Media", "foto.html"), ("Informazione", None)], "Informazione",
                     "Il bollettino ufficiale della sezione: notizie, attività e appuntamenti, da sfogliare in PDF.") + f"""

<section class="section" aria-label="Numeri di Informazione">
<div class="container">
{pub_feature(ultimo, f"Informazione, {ultimo['quando']}", "Il numero più recente del bollettino ufficiale della Sezione Ticino.")}
{griglia}
</div>
</section>

{subnav("Media", "informazione.html")}"""
    return page("informazione.html", "Informazione | CAS Ticino",
                "Informazione, il bollettino ufficiale della Sezione Ticino del Club Alpino Svizzero, da scaricare in PDF.",
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
            ("Arrampicata", "Accesso gratuito alla palestra di arrampicata San Paolo")]
    join = "https://portal.sac-cas.ch/it/groups/6783/self_registration"
    body = page_hero([("Adesione", None)], "Diventa socio",
                     "Entra nella sezione ticinese del Club Alpino Svizzero: gite, corsi, capanne e una comunità che ama la montagna.",
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{join}">Iscriviti sul sito del CAS <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<figure class="band">
{pic("paesaggi/laghetto-alpino", "Laghetto alpino tra le rocce, con le montagne sullo sfondo", mobile="paesaggi/laghetto-alpino-4x3", w=2000, h=1126, lazy=False)}
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
    groups = [("2-10", "Giovanissimi e famiglie", "Arrampicata in famiglia: i bambini imparano a muoversi in corda, gli adulti ad assicurare."),
              ("9-14", "Spider", "Arrampicata, nevai, lettura della carta e scoperta della natura, tra gioco, divertimento e spirito di gruppo."),
              ("13-17", "Junior", "D’inverno sci alpinismo e splitboard, d’estate creste e arrampicata: prima il divertimento e la sicurezza, poi l’autonomia."),
              ("16-25", "OG", "Sci alpinismo impegnativo, cascate di ghiaccio e arrampicata tecnica in tutto l’arco alpino. Chi vuole può formarsi come monitore.")]
    cards = "\n".join(f"""<article class="group">
<div class="age">{a}<span>anni</span></div>
<h3 class="h3">{t}</h3>
<p>{p}</p>
</article>""" for a, t, p in groups)
    rows = [("Iscrizione", "Su Droptour, almeno due settimane prima per le singole attività, oppure dal coordinatore per iscrizioni a blocchi."),
            ("Requisiti", 'Serve essere soci del CAS Ticino, tranne per le uscite di prova. <a href="adesione.html">Diventa socio</a>'),
            ("Costi", "Coprono vitto e alloggio a mezza pensione, guida e trasporto in furgone. Dai 21 ai 25 anni si aggiungono CHF 30 al giorno, perché non ci sono contributi G+S."),
            ("Inclusione", "Ragazze e ragazzi con disabilità fisica o psichica sono i benvenuti: contatta il coordinatore per trovare insieme la soluzione giusta."),
            ("Coordinatore", 'Diego Romelli, <a class="num" href="tel:+393485731549">+39 348 573 1549</a>'),
            ("Cassiere", 'Nicola Martinoni, <a class="num" href="tel:+41794391691">+41 79 439 16 91</a>'),
            ("Spider", "Giosiana Codoni")]
    body = page_hero([("Attività", "index.html#attivita"), ("Giovani", None)], "Giovani",
                     "Uscite di un giorno, fine settimana e campi di più giorni: alpinismo, arrampicata, sci alpinismo e molto altro, con monitori formati e guide alpine.",
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{GITE_GIOVANI}">Programma giovani <span class="arrow" aria-hidden="true">→</span></a></div>',
                     figure=img("attivita/giovani-3x4", "Giovane arrampicatore su una parete dei Denti della Vecchia", 800, 1066, lazy=False)) + f"""

<section class="section" aria-labelledby="fasce-h">
<div class="container">
<div class="section-head"><h2 id="fasce-h" class="h2">Quattro fasce d’età</h2></div>
<div class="groups" data-reveal>
{cards}
</div>
</div>
</section>

<section class="section--surface" aria-labelledby="iscr-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="iscr-h" class="h2">Iscrizioni<br>e costi</h2>
<div><a class="link" href="{GITE_GIOVANI}">Programma giovani</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "giovani.html")}"""
    return page("giovani.html", "Giovani | CAS Ticino",
                "Il gruppo giovani del CAS Ticino: arrampicata, sci alpinismo, campi e uscite per ragazze e ragazzi dai 2 ai 25 anni, con monitori e guide alpine.",
                body, og="attivita/giovani-3x4")


def senior():
    rows = [("Chi può partecipare", 'Dai 60 anni, con l’affiliazione al CAS Ticino. Non c’è una tassa aggiuntiva, e tutti i soci della sezione possono partecipare alle attività. <a href="adesione.html">Diventa socio</a>'),
            ("Come aderire", 'Scrivi a <a href="mailto:senior@casticino.ch">senior@casticino.ch</a> con nome, data di nascita, numero di socio CAS, indirizzo, telefono ed e-mail.'),
            ("Uscite", "Di norma il giovedì. Il calendario aggiornato è sul programma gite online."),
            ("Pranzi", 'Il secondo e il quarto mercoledì del mese al Bistrot Vecchio Torchio di Viganello. Iscrizioni entro il lunedì presso Hanni Vanossi (<a class="num" href="tel:+41763973390">+41 76 397 33 90</a>) o direttamente al ristorante (<a class="num" href="tel:+41919721010">+41 91 972 10 10</a>).'),
            ("Capigita", "Il dicastero cerca sempre nuovi capigita.")]
    body = page_hero([("Attività", "index.html#attivita"), ("Senior", None)], "Senior",
                     "Un gruppo di non più giovani con la passione per la montagna: la bellezza della natura, i piaceri della tavola e la nostra storia.") + f"""

{band_img("attivita/senior-2x1", "Escursionisti del gruppo senior su un sentiero di cresta", 1000, 500)}

<section class="section" aria-labelledby="gruppo-h">
<div class="container detail">
<div class="detail-intro split-intro">
<span class="label">Il gruppo, dal 1940</span>
<h2 id="gruppo-h" class="h2">Ogni giovedì<br>in cammino</h2>
<p>Escursioni, gite di più giorni, mountain bike e racchette, con percorsi adatti a diversi livelli di allenamento.</p>
<div><a class="btn btn--primary" href="{GITE_SENIORI}">Programma senior <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "senior.html")}"""
    return page("senior.html", "Senior | CAS Ticino",
                "Il gruppo senior del CAS Ticino, dal 1940: escursioni il giovedì, gite di più giorni, mountain bike e racchette per soci dai 60 anni.",
                body, og="attivita/senior-2x1")


CORSO_SLUG = {"Alpinismo": "alpinismo", "Sci alpinismo": "scialpinismo", "Arrampicata": "arrampicata",
              "Tecnica di sci fuori pista": "fuoripista", "Freeride": "fuoripista", "Racchette": "racchette"}

def pdf_corso(cartella, file, testo):
    """Link a un PDF del corso in docs/corsi/<cartella>/."""
    return f'<a href="{DOC}corsi/{cartella}/{file}.pdf">{testo} (PDF)</a>'


def schede_corso(c, struttura, requisiti, partecipanti, materiale, programma):
    """Le cinque righe di ogni corso: struttura, materiale e programma rimandano ai PDF in docs/corsi/<c>/
    (il link al programma compare solo quando c'è il PDF dell'anno)."""
    prog = programma
    if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, "programma-2027.pdf")):
        prog += " " + pdf_corso(c, "programma-2027", "Programma 2027")
    return [("Struttura", f'{struttura} {pdf_corso(c, "obiettivi", "Obiettivi del corso")}'),
            ("Requisiti", requisiti),
            ("Partecipanti", partecipanti),
            ("Materiale", f'{materiale} {pdf_corso(c, "materiale", "Lista del materiale")}'),
            ("Programma", prog)]


CORSI = [
    ("Estate", "Alpinismo", "corsi/alpinismo-4x5", (594, 742), "Cordata su una cresta di neve",
     "Il ponte tra escursionismo e alpinismo: legarsi correttamente su ghiacciaio e in cresta, tecniche di assicurazione, uso della corda in arrampicata e dei diversi attrezzi di progressione. Teoria e pratica, con lettura della carta, pianificazione, primo soccorso e salite in vetta su roccia e ghiaccio.",
     GITE_CORSI,
     schede_corso("alpinismo",
                  "Sette giorni in tre uscite: tre giorni alla Capanna Piansecco, in Valle Bedretto, per nodi, corda, ramponi e piccozza; un fine settimana tra il granito del Furka e il ghiacciaio del Rodano; uno al Passo del Susten, con una gita alpinistica finale. Alla fine si partecipa da secondi di cordata a gite fino al grado PD+/III.",
                  "Discreta condizione fisica: 4-5 ore di cammino con uno zaino di circa 10 kg, a 350-400 m di dislivello all’ora. Esperienza escursionistica, nessuna vertigine, età minima 16 anni (con il consenso dei genitori).",
                  "Iscrizioni online dal 1° dicembre 2026. Numero di posti limitato per ragioni di sicurezza (in definizione); precedenza in ordine d’iscrizione e ai soci CAS, poi lista d’attesa. L’iscrizione è definitiva con il pagamento della quota. Serata di presentazione e uscite obbligatorie, con qualsiasi tempo.",
                  "L’equipaggiamento personale spetta al partecipante; il materiale tecnico lo presta il CAS a chi non ce l’ha. Alla serata di presentazione si vede cosa serve: meglio aspettarla prima di comprare.",
                  'Serata di presentazione il 12 marzo 2027 a Bellinzona; uscite il 28-30 maggio, il 12-13 giugno e il 3-4 luglio 2027. CHF 700 per i soci, 800 per i non soci, 450 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing escluse.')),
    ("Inverno", "Sci alpinismo", "corsi/scialpinismo-4x5", (582, 728), "Sci alpinisti in salita su un pendio innevato",
     "Per muoversi in sicurezza e in autonomia nelle gite della sezione: salita con le pelli su pendii ripidi, discesa fuori pista, uso del materiale di sicurezza, valutazione del pericolo valanghe e pianificazione.",
     GITE_CORSI,
     schede_corso("sci-alpinismo",
                  "Sette giorni: una giornata introduttiva ad Airolo per verificare forma e tecnica, una serata di teoria su neve, ARTVA e autosoccorso, poi tre fine settimana alla Capanna Piansecco, all’Hotel Tiefenbach sul Furka e alla Camona da Maighels, con istruzione e gite fino a 800-1200 m di dislivello.",
                  "Sciare bene su piste nere e reggere una gita di 1200 m di dislivello con uno zaino di 5 kg in al massimo 4 ore. Età minima 16 anni. Aperto anche agli snowboarder con splitboard. Chi dopo la giornata introduttiva non risulta idoneo riceve l’80% della quota.",
                  'Al massimo 30. Iscrizioni dal 1° ottobre al 1° dicembre 2026, o fino a esaurimento dei posti; la quota va versata entro il 10 dicembre. Uscite obbligatorie, con qualsiasi tempo; assenze e ritiri non danno diritto a rimborsi.',
                  "Attrezzatura completa da sci alpinismo. ARTVA, pala e sonda prestati su richiesta, compresi nella quota.",
                  'Presentazione il 3 dicembre 2026 (anche via Teams); giornata introduttiva il 9 gennaio, teoria il 12 gennaio, uscite il 16-17 gennaio, il 20-21 febbraio e il 6-7 marzo 2027. CHF 650 per i soci, 750 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (circa CHF 100) escluse.')),
    ("Primavera", "Arrampicata", "corsi/arrampicata-4x5", (594, 742), "Cordata su una parete di roccia accanto a un ghiacciaio",
     "Per principianti che vogliono avvicinarsi all’arrampicata in ambiente e per chi vuole consolidare la tecnica: sicurezza, manovre di corda, progressione su vie di più tiri. Dopo le basi, sempre più autonomia sotto la supervisione di un istruttore di arrampicata.",
     GITE_CORSI,
     schede_corso("arrampicata",
                  "Sette giorni in tre fine settimana: prime arrampicate in falesia in Piemonte, vie di più tiri nel Locarnese, gite di applicazione nelle Alpi centrali; tra maggio e giugno, a volte, serate di arrampicata e ripasso dei nodi. Alla fine si arrampica in autonomia in falesia e su vie di più tiri: da secondi fino al 5a, da primi fino al 4b, con discesa in corda doppia.",
                  "Nessun prerequisito tecnico: il corso è pensato per chi comincia. Età minima 16 anni.",
                  "Al massimo 26, in ordine d’iscrizione. All’iscrizione si versa un anticipo di CHF 300; l’iscrizione è definitiva con il saldo alla serata di presentazione. Serata e uscite obbligatorie, con qualsiasi tempo; le assenze vanno annunciate al capocorso entro il martedì prima.",
                  "Il CAS presta il materiale tecnico a chi non ce l’ha; alla serata di presentazione si vede cosa serve.",
                  'Presentazione il 12 aprile 2027 alle 20:00 alla Scuola professionale di Trevano; uscite il 1-2 maggio, il 15-17 maggio e il 12-13 giugno 2027. CHF 600 per i soci, 650 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (CHF 40) escluse.')),
    ("Inverno", "Tecnica di sci fuori pista", "corsi/freeride-4x5", (594, 742), "Sciatori in discesa su un ghiacciaio",
     "Per chi fatica a scendere su pendii non preparati: trucchi e consigli per affrontare la neve fuori dalle piste battute. Adatto ai soci che vogliono migliorare, a chi si avvicina allo sci alpinismo e agli sciatori esperti in cerca di strategie per le condizioni difficili.",
     GITE_CORSI,
     schede_corso("freeride",
                  "Quattro giorni per affinare la tecnica su diversi tipi di neve e di terreno, leggere il pendio e scegliere la tattica giusta per il gruppo, applicare le misure di riduzione del rischio e consolidare il soccorso in valanga.",
                  "Le basi dello sci alpinismo (salire con le pelli, autosoccorso in valanga) e una discreta tecnica di sci fuori pista.",
                  'Numero di posti e condizioni d’iscrizione in definizione.',
                  "Attrezzatura completa da fuori pista e sci alpinismo, con ARTVA, pala e sonda.",
                  'Programma 2027 in definizione: date e costi seguono.')),
    ("Inverno", "Racchette", "corsi/racchette-4x5", (800, 1000), "Cresta innevata sopra un mare di nuvole",
     "Introduzione all’escursionismo con le racchette, tra teoria e pratica: riconoscere i segnali di pericolo, valutare il rischio valanghe e il terreno, pianificare con gli strumenti disponibili, ricerca dei sepolti e primo soccorso.",
     GITE_CORSI,
     schede_corso("racchette",
                  "Sei giorni: una serata di nivologia, una giornata sulla sicurezza con ARTVA, pala e sonda, poi due fine settimana in capanna, alla Capanna Piansecco e alla Capanna Maighels, tra tecnica di progressione, metodo 3x3, orientamento e dinamiche di gruppo. Alla fine si sale e si scende in sicurezza su terreni semplici, segnati e non.",
                  "Discreta condizione fisica: escursioni di 4-5 ore con 500-700 m di dislivello. Età minima 16 anni.",
                  "Al massimo 20, in ordine d’iscrizione. L’iscrizione è definitiva con il pagamento della quota alla serata introduttiva. Serata e uscite obbligatorie, con qualsiasi tempo; la meta può cambiare secondo le condizioni.",
                  "L’equipaggiamento personale viene controllato il primo giorno. ARTVA, pala e sonda prestati a chi ne ha bisogno.",
                  'Serata introduttiva martedì 15 dicembre 2026 nel Luganese; nivologia il 12 gennaio 2027 a Mezzovico, sicurezza il 16 gennaio ad Airolo, uscite il 23-24 gennaio e il 13-14 febbraio 2027. CHF 650 per i soci, 700 per i non soci, 375 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni, trasferte comprese.')),
]

# PDF dei corsi anche nella pagina Documenti (e quindi nella ricerca): un gruppo per tipo di documento
CARTELLE_CORSI = [("Alpinismo", "alpinismo"), ("Sci alpinismo", "sci-alpinismo"), ("Arrampicata", "arrampicata"),
                  ("Tecnica di sci fuori pista", "freeride"), ("Racchette", "racchette")]
for gruppo, file in [("Obiettivi corsi", "obiettivi"), ("Equipaggiamento", "materiale")]:
    DOCS.append((gruppo, [(nome, f"{DOC}corsi/{c}/{file}.pdf") for nome, c in CARTELLE_CORSI
                          if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, file + ".pdf"))]))


def corsi():
    rows = "\n".join(f"""<article class="course-row course-row--corso" id="corso-{CORSO_SLUG[title]}" aria-labelledby="corso-{CORSO_SLUG[title]}-h" data-reveal>
<figure>{img(im, alt, w, h)}</figure>
<div class="course-text">
<span class="label">{season}</span>
<h2 id="corso-{CORSO_SLUG[title]}-h" class="h2">{title}</h2>
<p>{text}</p>
<a class="btn btn--primary" href="{href}">Iscriviti <span class="arrow" aria-hidden="true">→</span></a>
</div>
{facts(fs)}
</article>""" for i, (season, title, im, (w, h), alt, text, href, fs) in enumerate(CORSI, 1))
    body = page_hero([("Attività", "index.html#attivita"), ("Corsi", None)], "Corsi",
                     "Corsi nei fine settimana, diretti da professionisti della montagna con monitori esperti: le basi per partecipare in sicurezza alle attività della sezione. Il programma dell’anno successivo esce entro novembre.") + f"""

<figure class="band">
{pic("paesaggi/salita-prato", "Un gruppo sale in fila su un sentiero tra prati fioriti, sotto il cielo azzurro", mobile="paesaggi/salita-prato-4x3", w=2000, h=1125, lazy=False)}
</figure>

<section class="section" aria-label="Corsi base">
<div class="container">
{rows}
</div>
</section>

<section class="section" aria-labelledby="avanzati-h">
<div class="container">
<div class="callout">
<p><strong id="avanzati-h">Verso capogita e monitore G+S.</strong> Per chi vuole approfondire o prepararsi ai corsi capogita CAS e monitore Gioventù+Sport, la sezione propone corsi avanzati di alpinismo, sci alpinismo e arrampicata, di regola ad anni alterni, e serate di formazione teorica con specialisti.</p>
</div>
</div>
</section>

{subnav("Attività", "corsi.html")}"""
    return page("corsi.html", "Corsi | CAS Ticino",
                "Corsi del CAS Ticino diretti da professionisti: sci alpinismo, racchette, tecnica di sci fuori pista, arrampicata e alpinismo.",
                body, og="corsi/scialpinismo-4x5")


MATERIALE = [  # prezzo giornaliero in franchi
    ("Alpinismo e arrampicata", [
        ("Ramponi", 5), ("Piccozza", 5), ("Imbracatura (S, M, L, XL)", 5), ("Casco", 5), ("Pedule", 5),
        ("Moschettone a ghiera", 3), ("Discensore e moschettone", 5), ("Jul e moschettone", 5),
        ("Cordino prussik", 1), ("Cordino 3–5 m", 1), ("Longe", 2), ("Set di rinvii", 5)]),
    ("Scialpinismo", [
        ("Set ARVA, sonda e pala", 10), ("ARVA", 5), ("Sonda", 5), ("Pala", 5),
        ("Slittino di pronto soccorso", 5), ("Pelli di riserva", 5)]),
    ("Altro", [
        ("Bussola", 5), ("Occhiali da sole", 5), ("Kit ferrata", 10), ("Crash pad", 10)]),
]


def noleggio():
    tabelle = []
    for gruppo, articoli in MATERIALE:
        righe = "\n".join(f'<tr><th scope="row">{nome}</th><td>Fr. {prezzo}.–</td></tr>' for nome, prezzo in articoli)
        tabelle.append(f"""<div class="rate">
<h3 class="h3">{gruppo}</h3>
<table class="listino">
<thead><tr><th scope="col">Articolo</th><th scope="col">Al giorno</th></tr></thead>
<tbody>
{righe}
</tbody>
</table>
</div>""")
    # la lista lunga a sinistra, le altre impilate a destra
    tabelle = tabelle[0] + '\n<div class="listini-col">\n' + "\n".join(tabelle[1:]) + "\n</div>"
    rows = [("Come funziona", 'Scrivi a <a href="mailto:noleggio@casticino.ch">noleggio@casticino.ch</a>. Con la conferma ricevi le istruzioni per il ritiro. Si paga in contanti o TWINT alla riconsegna.'),
            ("Richiesta", "Una settimana prima dell’attività"),
            ("Ritiro", 'A partire dal mercoledì alle <span class="num">19:00</span>'),
            ("Riconsegna", "Entro il martedì sera successivo"),
            ("Magazzino", "Manno"),
            ("E-mail", '<a href="mailto:noleggio@casticino.ch">noleggio@casticino.ch</a>')]
    body = page_hero([("Attività", "index.html#attivita"), ("Noleggio", None)], "Noleggio",
                     "Materiale in affitto per le attività della sezione e per le uscite private: alpinismo, cascate di ghiaccio, scialpinismo, arrampicata, racchette, escursionismo e bouldering.",
                     '<div class="actions hero-actions"><a class="btn btn--primary" href="#come">Come noleggiare <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<section class="section--surface section--tight" id="listino" aria-labelledby="listino-h">
<div class="container">
<div class="section-row">
<h2 id="listino-h" class="h2">Listino</h2>
<p class="small">Prezzi per giorno di noleggio, in franchi.</p>
</div>
<div class="listini" data-reveal>
{tabelle}
</div>
</div>
</section>

<section class="section" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">Come funziona</h2>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "noleggio.html")}"""
    return page("noleggio.html", "Noleggio | CAS Ticino",
                "Noleggio materiale del CAS Ticino: alpinismo, sci alpinismo, arrampicata, racchette e altro, con ritiro al magazzino di Manno.",
                body)


# ------------------------------------------------------------------ mercatino
# Annunci di materiale tra privati, inseriti dalla redazione (admin/, raccolta «Mercatino») da data/mercatino/*.json:
# campi e scadenza in mercatino_util.py. La pagina si rigenera ogni mattina (update-gite.yml): gli scaduti escono da soli.

MERCATINO_MAIL = "mercatino@casticino.ch"
MERCATINO_MODULO = """Tipo (vendo / cerco / regalo):
Titolo:
Prezzo:
Luogo:
Descrizione:

Nome:
Contatto da pubblicare (e-mail e/o telefono):

Allego fino a 3 foto."""


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


def annuncio_html(a):
    nome = os.path.splitext(os.path.basename(a["percorso"]))[0]
    foto = [f for f in a.get("foto") or [] if f and os.path.exists(os.path.join(ROOT, f))][:3]
    fig = ""
    if foto:
        w, h = webp_size(os.path.join(ROOT, foto[0])) if foto[0].endswith(".webp") else (1200, 900)
        altre = "".join(f'<a href="{esc(f)}" aria-label="Foto {i + 2} di «{esc(a["title"])}»"><img src="{esc(f)}" alt="" loading="lazy" decoding="async"></a>'
                        for i, f in enumerate(foto[1:]))
        fig = f"""<figure class="annuncio-foto">
<a href="{esc(foto[0])}"><img src="{esc(foto[0])}" alt="{esc(a['title'])}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>
{f'<div class="annuncio-altre">{altre}</div>' if altre else ""}
</figure>"""
    tipo = a.get("tipo") if a.get("tipo") in mercatino_util.TIPI else "Vendo"
    testo = "".join(f"<p>{esc(par).replace(chr(10), '<br>')}</p>" for par in re.split(r"\n\s*\n", (a.get("testo") or "").strip()) if par.strip())
    meta = " · ".join(filter(None, [esc(a.get("luogo") or ""), f'pubblicato il {data_it(a["date"][:10])}']))
    contatto = "".join(filter(None, [esc(a["nome"]) + (": " if a.get("contatto") else "") if a.get("nome") else "",
                                     contatto_html(a["contatto"]) if a.get("contatto") else ""]))
    return f"""<article class="annuncio" id="{nome}" data-ruoli="{tipo.lower()}" data-scade="{mercatino_util.scadenza(a)}">
{fig}
<div class="annuncio-corpo">
<p class="annuncio-tipo annuncio-tipo--{tipo.lower()}">{tipo}</p>
<h3 class="annuncio-titolo">{esc(a['title'])}</h3>
{f'<p class="annuncio-prezzo">{esc(a["prezzo"])}</p>' if a.get("prezzo") else ""}
{f'<div class="annuncio-testo">{testo}</div>' if testo else ""}
<p class="small">{meta}</p>
{f'<p class="annuncio-contatto">{contatto}</p>' if contatto else ""}
</div>
</article>"""


def mercatino():
    annunci = mercatino_util.attivi()
    conta = {t: sum(1 for a in annunci if (a.get("tipo") if a.get("tipo") in mercatino_util.TIPI else "Vendo") == t) for t in mercatino_util.TIPI}
    mailto = f"mailto:{MERCATINO_MAIL}?subject={quote('Annuncio per il mercatino')}&body={quote(MERCATINO_MODULO)}"
    bottone = f'<a class="btn btn--primary" href="{esc(mailto)}">Pubblica un annuncio <span class="arrow" aria-hidden="true">→</span></a>'
    if annunci:
        filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">Tutti <span class="num">{len(annunci)}</span></button>'] +
                           [f'<button type="button" data-filtro="{t.lower()}" aria-pressed="false">{t} <span class="num">{conta[t]}</span></button>'
                            for t in mercatino_util.TIPI if conta[t]])
        elenco = f"""<div class="filtro" role="group" aria-label="Filtra per tipo di annuncio" data-filtra="#annunci" data-uno="annuncio" data-molti="annunci" hidden>
{filtri}
</div>
<p class="small filtro-stato" id="filtro-stato" aria-live="polite"></p>
<div class="annunci" id="annunci">
{chr(10).join(annuncio_html(a) for a in annunci)}
</div>"""
    else:
        elenco = f"""<div class="callout">
<p><strong>Al momento non ci sono annunci.</strong> Hai dell’attrezzatura che non usi più, o cerchi qualcosa? Mandaci il tuo annuncio.</p>
{bottone.replace("btn--primary", "btn--secondary")}
</div>"""
    rows = [("Cosa", "Materiale e abbigliamento per la montagna, da vendere, cercare o regalare tra privati."),
            ("Come", f'Scrivi a <a href="{esc(mailto)}">{MERCATINO_MAIL}</a> con tipo, titolo, prezzo, luogo, descrizione, il contatto da pubblicare e fino a 3 foto: la redazione lo mette online.'),
            ("Durata", f"Ogni annuncio resta online {mercatino_util.GIORNI_DEFAULT // 30} mesi. Se l’oggetto è venduto, trovato o regalato prima, avvisaci e lo togliamo."),
            ("Costo", "Gratuito"),
            ("Trattative", "Si accordano direttamente le persone interessate: la sezione pubblica gli annunci ma non partecipa alla vendita e non risponde del materiale.")]
    body = page_hero([("Attività", "index.html#attivita"), ("Mercatino", None)], "Mercatino",
                     "Attrezzatura di montagna tra soci e appassionati: vendo, cerco, regalo. Dai una seconda vita al materiale che non usi più.",
                     f'<div class="actions hero-actions">{bottone}</div>') + f"""

<section class="section" aria-label="Annunci">
<div class="container">
{elenco}
</div>
</section>

<section class="section--surface" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">Come funziona</h2>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "mercatino.html")}"""
    return page("mercatino.html", "Mercatino | CAS Ticino",
                "Il mercatino del CAS Ticino: annunci di attrezzatura di montagna tra privati, da vendere, cercare o regalare.",
                body)


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
        diventa="Mitglied werden", le_capanne="Die Hütten",
        hero_alt="Skitourengeher im Aufstieg zu einem verschneiten Dorf",
        cifre="Die Sektion in Zahlen",
        stat_home=["Gründungsjahr", "Mitglieder", "Hütten, 362 Schlafplätze", "Disziplinen in den Kursen"],
        sez_h="Seit 1886<br>zu Fuss unterwegs.",
        sez_lead="Gegründet in der Birraria Gambrinus in Bellinzona, im Jubiläumsjahr der Erstbesteigung des Mont Blanc, um die Berge des Kantons «zu besuchen, zu erforschen und bekannt zu machen».",
        sezione="Die Sektion", storia="Geschichte",
        solo_it="<strong>Vieles gibt es nur auf Italienisch.</strong> Tourenprogramm, News, Kurse, Jugend- und Seniorengruppen, Fotos und Dokumente der Sektion sind nur auf Italienisch verfügbar.",
        gite="Tourenprogramm", corsi="Kurse",
        capanne_h="Sechs Hütten, ein Tessin",
        capanne_lead="Immer offen, bewartet, wenn die Hüttenwarte da sind. Melden Sie sich vor dem Aufbruch beim Hüttenwart, um Anwesenheit und Verhältnisse am Berg zu prüfen.",
        accesso="Zugang ab",
        cta_h="Kommen Sie mit.",
        cta_p="Günstigere Preise in den SAC-Hütten der ganzen Schweiz, Kurse, Touren und eine Gemeinschaft, die die Berge so liebt wie Sie.",
        # introduzione
        intro_crumb="Einführung", intro_h="Die Sektion",
        intro_lead="Am 11. April 1886 in Bellinzona gegründet, zählt die Sektion Ticino des Schweizer Alpen-Clubs fast 3000 Mitglieder und bietet ein vielfältiges Programm für jedes Alter: von den Jüngsten bis zu den Senioren.",
        intro_alt="Eine Gruppe Bergsteiger unterwegs auf einem Gletscher",
        stat_intro=["am 11. April in Bellinzona gegründet", "Mitglieder, von den Jüngsten bis zu den Senioren", "Hütten im Besitz der Sektion", "Ressorts neben dem Vorstand"],
        cosa_h="In den Bergen,<br>zu jeder Jahreszeit",
        alt_cresta="Bergsteiger auf einem Felsgrat",
        discipline_h="Disziplinen", discipline_p="Wandern, Bergsteigen, Klettern, Skitouren, Schneeschuhwandern und Eisklettern.",
        inizia_h="Für Einsteiger", inizia_p="Einführungskurse in Bergsteigen, Skitouren, Schneeschuhwandern und Klettern im Gelände (auf Italienisch).",
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
            ("Bankverbindung", 'Banca Stato, Lugano<br><span class="num">IBAN CH09 0076 4128 9526 1200 6</span>'),
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
                  ("Klettern", "Freier Eintritt in die Kletterhalle San Paolo")],
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
        diventa="Become a member", le_capanne="The huts",
        hero_alt="Ski tourers climbing towards a snow-covered village",
        cifre="The section in numbers",
        stat_home=["year founded", "members", "huts, 362 beds", "disciplines taught in courses"],
        sez_h="Since 1886,<br>on foot.",
        sez_lead="Founded at the Birraria Gambrinus in Bellinzona, in the centenary year of the first ascent of Mont Blanc, to “visit, study and make known” the mountains of the canton.",
        sezione="The Section", storia="History",
        solo_it="<strong>Much is only in Italian.</strong> The trip programme, news, courses, youth and seniors groups, photos and documents of the section are only available in Italian.",
        gite="Trip programme", corsi="Courses",
        capanne_h="Six huts, one Ticino",
        capanne_lead="Always open, staffed when the hut keepers are there. Check with the hut keeper before you set out, to make sure they are there and to ask about conditions in the mountains.",
        accesso="Access from",
        cta_h="Come with us.",
        cta_p="Lower rates in SAC huts all over Switzerland, courses, trips and a community that loves the mountains as much as you do.",
        intro_crumb="Introduction", intro_h="The section",
        intro_lead="Founded in Bellinzona on 11 April 1886, the Ticino Section of the Swiss Alpine Club has almost 3000 members and offers a varied programme for all ages: from the youngest to seniors.",
        intro_alt="A group of climbers walking on a glacier",
        stat_intro=["founded in Bellinzona on 11 April", "members, from the youngest to seniors", "huts owned by the section", "departments alongside the committee"],
        cosa_h="In the mountains,<br>in every season",
        alt_cresta="Climbers on a rocky ridge",
        discipline_h="Disciplines", discipline_p="Hiking, mountaineering, climbing, ski touring, snowshoeing and ice climbing.",
        inizia_h="For beginners", inizia_p="Introductory courses in mountaineering, ski touring, snowshoeing and outdoor climbing (in Italian).",
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
            ("Bank details", 'Banca Stato, Lugano<br><span class="num">IBAN CH09 0076 4128 9526 1200 6</span>'),
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
                  ("Climbing", "Free entry to the San Paolo climbing gym")],
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


def home_tradotta():
    tx = tx_tradotte()
    lang = LINGUA["lang"]
    huts = schede_capanne({"de": HUTS_DE, "en": HUTS_EN}[lang], tx['accesso'], f"{lang}/")
    stats = "\n".join(f'<div class="stat"><strong>{n}</strong><span>{num(x)}</span></div>'
                      for n, x in zip(("1886", "3000", "6", "5"), tx["stat_home"]))
    html = head(tx["home_title"], tx["home_desc"],
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n')
    html += "\n<body>\n" + nav(f"{lang}/index.html") + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">{tx['hero_h']}</h1>
<div class="hero-foot">
<p class="lead">{tx['hero_lead']}</p>
<div class="actions">
<a class="btn btn--primary" href="{lang}/adesione.html">{tx['diventa']} <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="#capanne">{tx['le_capanne']}</a>
</div>
</div>
</div>
<figure class="band">
{pic("paesaggi/sciatori-villaggio", tx['hero_alt'], mobile="paesaggi/sciatori-villaggio-4x3", w=2000, h=901, lazy=False, cls="pos-low")}
</figure>
</section>

<section class="section section--tight section--stats" id="sezione" aria-label="{tx['cifre']}">
<div class="container">
<div class="stats" data-reveal>
{stats}
</div>
</div>
</section>

<section class="section section--tight section--after-stats" aria-labelledby="sektion-h">
<div class="container split">
<div class="split-intro">
<h2 id="sektion-h" class="h2">{tx['sez_h']}</h2>
<p class="lead">{tx['sez_lead']}</p>
<div class="links"><a class="link" href="{lang}/introduzione.html">{tx['sezione']}</a><a class="link" href="{lang}/storia.html">{tx['storia']}</a></div>
</div>
<div class="callout" data-reveal>
<p>{tx['solo_it']}</p>
<div class="links"><a class="link" href="{GITE}">{tx['gite']}</a><a class="link" href="news.html">News</a><a class="link" href="corsi.html">{tx['corsi']}</a></div>
</div>
</div>
</section>

<section class="section" id="capanne" aria-labelledby="capanne-h">
<div class="container">
<div class="section-head">
<h2 id="capanne-h" class="h2">{tx['capanne_h']}</h2>
<p class="lead">{tx['capanne_lead']}</p>
</div>
<div class="huts">
{huts}
</div>
</div>
</section>

{banda_adesione(tx['cta_h'], tx['cta_p'], tx['diventa'], f"{lang}/adesione.html")}

</main>
""" + footer()
    return pubblica(f"{lang}/index.html", html)


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
FUORI_INDICE = {"gita.html", "news.html", "cerca.html"}  # elenchi che ripetono il contenuto di altre pagine


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
            voci.append({"t": a["title"], "u": a.get("link") or "foto.html", "k": "Foto e resoconto gita", "d": a.get("date", ""),
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


PAGES = {
    "index.html": home,
    "introduzione.html": introduzione, "comitato.html": comitato, "organizzazione.html": organizzazione,
    "sede.html": sede, "storia.html": storia, "link.html": link, "documenti.html": documenti,
    "news.html": news, "gite.html": gite, "gita.html": gita_pagina, "foto.html": foto, "annuari.html": annuari, "informazione.html": informazione,
    "adesione.html": adesione,
    "giovani.html": giovani, "senior.html": senior, "corsi.html": corsi, "noleggio.html": noleggio, "mercatino.html": mercatino,
    "soccorso.html": soccorso, "capigita.html": capigita,
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
            return fn()
        finally:
            LINGUA["lang"] = "it"
    return genera


# Versioni tradotte (de/, en/): La Sezione, le capanne con le loro sotto-pagine e Adesione.
for _lang, _contenuti in (("de", CONTENUTI_DE), ("en", CONTENUTI_EN)):
    _pagine = {"index.html": home_tradotta, "introduzione.html": introduzione_tradotta, "comitato.html": comitato,
               "organizzazione.html": organizzazione, "capigita.html": capigita, "sede.html": sede_tradotta,
               "storia.html": storia, "link.html": link, "adesione.html": adesione_tradotta}
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
    scrivi("sitemap.xml", sitemap([p for p in pagine if p != "gita.html"] + ["cerca.html"]))  # gita.html vale solo con ?id=
    scrivi("robots.txt", f"User-agent: *\nDisallow: /admin/\n\nSitemap: {SITO}sitemap.xml\n")
    with open(os.path.join(ROOT, "data", "cerca.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(indice_ricerca(pagine), f, ensure_ascii=False, separators=(",", ":"))
    print("scritto data/cerca.json")
    if not only or "cerca.html" in only:
        scrivi("cerca.html", metadati("cerca.html", cerca_pagina()))  # dopo l'indice: il link porta l'impronta di cerca.json
