"""Nuovo design: genera tutte le pagine del sito.

Uso: python scripts/redesign/pages.py [Pagina.html ...]  (senza argomenti rigenera tutto)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shared import head, nav, footer, pic, img, GITE, page_hero, subnav, asset, in_sottocartella, crumbs

# Programma gite su Droptour già filtrato per gruppo o per tipo di attività (i link dei singoli corsi cambiano ogni anno)
GITE_FILTRO = GITE + "?page=touren&amp;year=&amp;typ=&amp;gruppe={gruppe}&amp;anlasstyp={tipo}&amp;selected_anf_tech=&amp;selected_anf_kond=&amp;zusatz=&amp;search="
GITE_GIOVANI = GITE_FILTRO.format(gruppe="Giovani", tipo="")
GITE_SENIORI = GITE_FILTRO.format(gruppe="Seniori", tipo="")
GITE_CORSI = GITE_FILTRO.format(gruppe="", tipo="Corso")
from shared import LINGUA, PAGINE_DE, de, L
from capanne import CONTENUTI, PRENOTA
from capanne_de import CONTENUTI_DE, HUT_DE, HUTS_DE
import json, re, unicodedata
import news_util
from news_util import webp_size
from html import unescape as html_unescape

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUTS = [
    # file, nome, quota, valle, stato, testo, posti, accesso, img 3x2 (w,h), grande
    ("CampoTencia.html", "Campo Tencia", "2140", "Val Piumogna", "Custodita", "Su un terrazzo sopra la Val Piumogna, base per il Pizzo Campo Tencia: la cima più alta interamente ticinese.", "80 posti", "Dalpe 3h", "capanne/campotencia-3x2", (987, 658), True),
    ("Cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Custodita", "Sull’omonimo passo, tra Leventina e Valle Maggia. Inaugurata nel 2003, primo rifugio moderno del CAS.", "100 posti", "Ossasco 3h30", "capanne/cristallina-3x2", (837, 558), True),
    ("Adula.html", "Adula", "2012", "Val Carassino", "Custodita", "Il classico rifugio in pietra affacciato sulla Valle di Blenio: storia, accoglienza calorosa e cucina nostrana.", "24 posti", "Compietto 2h40", "capanne/adula-3x2", (1000, 667), False),
    ("Motterascio.html", "Motterascio", "2172", "Greina", "Custodita", "Al margine della riserva della Greina: torbiere, alpeggi e l’arco naturale più grande del Ticino.", "70 posti", "Garzott 2h", "capanne/motterascio-3x2", (974, 649), False),
    ("MonteBar.html", "Monte Bar", "1620", "Alta Capriasca", "Tutto l’anno", "Il balcone sul Luganese, ricostruito nel 2016: vista dal Monte Rosa ai Denti della Vecchia, standard Bike Hotel.", "42 posti", "Corticiasca 1h30", "capanne/montebar-3x2", (663, 442), False),
    ("BaitaDelLuca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Su riservazione", "Sopra Sonvico, ai piedi dei Denti della Vecchia. Punto di ritrovo dei giovani, ideale per famiglie e arrampicata.", "16 posti, autogestita", "Rosone 30 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

COURSES = [
    ("Estate", "Alpinismo", "Progressione su neve e roccia per escursionisti che vogliono salire più in alto.", "corsi/alpinismo-4x5", (594, 742), "Cordata su una cresta di neve"),
    ("Inverno", "Sci alpinismo", "Salita e discesa fuori pista, nivologia, prevenzione valanghe, ricerca ARTVA.", "corsi/scialpinismo-4x5", (582, 728), "Sci alpinisti in salita su un pendio innevato"),
    ("Primavera", "Arrampicata", "Vie a uno o più tiri: assicurazione, gestione della sosta, corda doppia.", "corsi/arrampicata-4x5", (594, 742), "Cordata su una parete di roccia accanto a un ghiacciaio"),
    ("Inverno", "Freeride", "Tecnica di sci fuori pista per chi vuole scendere con più sicurezza.", "corsi/freeride-4x5", (594, 742), "Sciatori in discesa su un ghiacciaio"),
    ("Inverno", "Racchette", "Muoversi sulla neve in sicurezza: meteo, orientamento, primi soccorsi.", "corsi/racchette-4x5", (800, 1000), "Cresta innevata sopra un mare di nuvole"),
]

TIMELINE = [
    ("1886", "Nasce il Club Alpino Ticinese; primo presidente l’avv. Curzio Curti."),
    ("1887", "Adesione al Club Alpino Svizzero come sezione ticinese, con sede a Lugano."),
    ("1913", "Nasce la sezione di Lugano del Club Alpino Femminile Svizzero."),
    ("1918", "Prime stazioni di soccorso alpino a Faido, Airolo e Olivone."),
    ("1940", "Costituzione del gruppo Seniori."),
    ("1980", "Le sezioni maschile e femminile si fondono."),
    ("2003", "Inaugurata la nuova Capanna Cristallina."),
    ("2016", "Conclusa la ricostruzione della Capanna Monte Bar."),
]


def home():
    huts = "\n".join(f"""<a class="hut{' hut--big' if big else ''}" href="{f}" data-reveal>
<figure>{img(im, f'Capanna {n}', w, h)}</figure>
<div class="hut-head"><h3 class="h3">{n}</h3><span class="hut-alt">{q} m</span></div>
<div class="hut-meta"><span>{v}</span><span class="status">{st}</span></div>
<p>{t}</p>
<div class="hut-meta"><span>{posti}</span><span>Accesso da {acc}</span></div>
</a>""" for f, n, q, v, st, t, posti, acc, im, (w, h), big in HUTS)
    courses = "\n".join(f"""<a class="course" href="Corsi.html#corso-{CORSO_SLUG[title]}">
<figure>{img(im, alt, w, h)}</figure>
<span class="label">{season}</span>
<h3 class="h3">{title}</h3>
<p>{text}</p>
</a>""" for season, title, text, im, (w, h), alt in COURSES)
    timeline = "\n".join(f'<li><span class="year">{y}</span><span>{t}</span></li>' for y, t in TIMELINE)

    html = head("CAS Ticino | Club Alpino Svizzero, Sezione Ticino",
                "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età. Da oltre un secolo, la casa dell’alpinismo ticinese.",
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n<link rel="preload" as="image" href="assets/img/paesaggi/sciatori-villaggio-2000.webp" imagesrcset="assets/img/paesaggi/sciatori-villaggio-1000.webp 1000w, assets/img/paesaggi/sciatori-villaggio-2000.webp 2000w" imagesizes="100vw" media="(min-width: 701px)">\n')
    html += "\n<body>\n" + nav("index.html") + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">In montagna<br>con <span class="accent">noi</span>.</h1>
<div class="hero-foot">
<p class="lead">Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età.</p>
<div class="actions">
<a class="btn btn--primary" href="Adesione.html">Diventa socio <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="#capanne">Le capanne</a>
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
<div class="stat"><strong>≈3000</strong><span>soci</span></div>
<div class="stat"><strong>6</strong><span>rifugi, 362 posti letto</span></div>
<div class="stat"><strong>5</strong><span>discipline insegnate nei corsi</span></div>
</div>
</div>
</section>

<section class="section section--tight section--after-stats" id="storia" aria-labelledby="storia-h">
<div class="container split">
<div class="split-intro">
<h2 id="storia-h" class="h2">Dal 1886,<br>a piedi.</h2>
<p class="lead">Fondato alla Birraria Gambrinus di Bellinzona nell’anno del centenario della prima salita al Monte Bianco, per «visitare, studiare e far conoscere» le montagne del Cantone.</p>
<div><a class="link" href="Storia.html">Leggi la storia completa</a></div>
</div>
<ol class="timeline timeline--compact" data-reveal>
{timeline}
</ol>
</div>
</section>

<section class="section--surface section--tight" id="news" aria-labelledby="news-h">
<div class="container">
<div class="section-row">
<h2 id="news-h" class="h2">Dalla sezione</h2>
<div class="links"><a class="link" href="News.html">Tutte le news</a><a class="link" href="Foto.html">Foto e resoconti</a></div>
</div>
<div class="news-grid" data-reveal>
{chr(10).join(news_card(n) for n in NEWS[:3])}
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
<div class="actions"><a class="btn btn--primary" href="{GITE}">Programma gite</a><a class="btn btn--ghost-light" href="Foto.html">Foto e resoconti</a></div>
</div>
</article>
<article class="tile tile--tall" data-reveal>
{img("attivita/giovani-3x4", "Giovane arrampicatore su una parete dei Denti della Vecchia", 800, 1066)}
<div class="tile-body">
<span class="label">Gruppo giovani, dagli anni ’60</span>
<h3 class="h2">Giovani</h3>
<p>Arrampicata, escursioni e settimane in montagna con monitori della sezione. Il ritrovo è la Baita del Luca, ai piedi dei Denti della Vecchia.</p>
<div class="links"><a class="link" href="Giovani.html">Gruppo giovani</a><a class="link" href="Organizzazione.html#giovani">Organizzazione</a></div>
</div>
</article>
<article class="tile tile--wide-bottom" data-reveal>
{img("attivita/senior-2x1", "Escursionisti su un sentiero di cresta", 1000, 500)}
<div class="tile-body">
<span class="label">Gruppo senior, dal 1940</span>
<h3 class="h2">Senior</h3>
<p>Uscite settimanali con capigita esperti, al ritmo giusto e in buona compagnia, dalla Capriasca alle Alpi.</p>
<div class="links"><a class="link" href="Senior.html">Gruppo senior</a><a class="link" href="Organizzazione.html#senior">Organizzazione</a></div>
</div>
</article>
</div>
</div>
</section>

<section class="section" id="corsi" aria-labelledby="corsi-h">
<div class="container">
<div class="section-head">
<h2 id="corsi-h" class="h2">Impara la montagna</h2>
<p class="lead">Corsi nel fine settimana, diretti da professionisti con monitori esperti. Il programma del nuovo anno esce entro novembre.</p>
</div>
<div class="rail" tabindex="0" aria-label="Corsi">
{courses}
</div>
<div class="rail-foot">
<p class="small">Corsi avanzati per futuri capigita CAS e monitori G+S.</p>
<a class="link" href="Noleggio.html">Noleggio</a>
</div>
</div>
</section>

<section class="section" id="capanne" aria-labelledby="capanne-h">
<div class="container">
<div class="section-head">
<h2 id="capanne-h" class="h2">Sei capanne, un solo Ticino</h2>
<p class="lead">Sempre aperte, custodite quando i guardiani sono presenti. Prima di partire, contatta il guardiano per verificare presenza e condizioni della montagna.</p>
</div>
<div class="huts">
{huts}
</div>
<div class="callout">
<p><strong>Cerchiamo «api operaie».</strong> I volontari aiutano i guardiani ad aprire, chiudere e mantenere le capanne, e passano qualche bella serata in quota.</p>
<a class="btn btn--secondary" href="mailto:info@casticino.ch">Voglio aiutare</a>
</div>
</div>
</section>

{media_section()}

<section class="cta-band" id="adesione" aria-labelledby="adesione-h">
{pic("paesaggi/tramonto-larici", "", mobile="paesaggi/tramonto-larici-4x3", w=2000, h=1126)}
<div class="container">
<h2 id="adesione-h" class="h2">Sali con noi.</h2>
<p>Tariffe ridotte nelle capanne CAS di tutta la Svizzera, corsi, gite e una comunità che ama la montagna quanto te.</p>
<a class="btn btn--light" href="Adesione.html">Diventa socio <span class="arrow" aria-hidden="true">→</span></a>
</div>
</section>

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
    "CampoTencia.html": dict(
        name="Campo Tencia", where="Val Piumogna, Leventina", alt_m="2140", beds="80", custody="da metà giugno a metà ottobre",
        mail="campotencia@casticino.ch", booking=PRENOTA.format(36), facebook="https://www.facebook.com/61559861696010",
        description="Capanna Campo Tencia, 2140 m, in Val Piumogna (Leventina): 80 posti letto, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
        band=("capanne/campotencia", "La Capanna Campo Tencia al tramonto, sopra la Val Piumogna", 658),
        intro="Adagiata su un terrazzo che domina l’alta Val Piumogna, è la base ideale per escursioni, traversate verso altre capanne e salite come quella al Pizzo Campo Tencia, che con i suoi 3071 m è la cima più alta interamente in territorio ticinese.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da metà giugno a metà ottobre; d’inverno in marzo e aprile, su riservazione"),
              ("Posti letto", "80"),
              ("Pasti", "Cucina calda, pasti serviti tutto il giorno dal guardiano"),
              ("Locale invernale", "Sempre aperto, con bibite e legna")],
        reach=[("Accesso estivo", "Da Dalpe 3h; dal Lago Tremorgio (funivia da Rodi) 3h30; da Fusio per il Passo Campolungo 6h"),
               ("Accesso invernale", "Da Dalpe 3h, con gli sci per la Val Piumogna"),
               ("Cartina", 'CNS 1272 Campo Tencia, coordinate <span class="num">699.430 / 144.480</span>')],
        contact=[("Guardiani", "Valeria Grandi e Paco Porcu"),
                 ("Telefono capanna", '<a class="num" href="tel:+41918671544">+41 (0) 91 867 15 44</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41767212572">+41 (0) 76 721 25 72</a>'),
                 ("E-mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "Cristallina.html": dict(
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
                 ("Telefono", '<a class="num" href="tel:+41918692330">+41 (0) 91 869 23 30</a>'),
                 ("E-mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "Adula.html": dict(
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
                 ("Telefono capanna", '<a class="num" href="tel:+41918721532">+41 (0) 91 872 15 32</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41795352112">+41 (0) 79 535 21 12</a>'),
                 ("E-mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "Motterascio.html": dict(
        name="Motterascio", where="Alpe Motterascio, Greina, Blenio", alt_m="2172", beds="70", custody="da metà giugno a metà ottobre",
        mail="motterascio@casticino.ch", booking=PRENOTA.format(221), facebook="https://www.facebook.com/michelamotterascio",
        description="Capanna Motterascio, 2172 m, al margine della Greina (Blenio): 70 posti letto, aperta tutto l’anno, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
        band=("capanne/motterascio", "La Capanna Motterascio sull’altopiano della Greina", 649),
        intro="Capanna nuova, al margine di una riserva naturale straordinaria: la Greina, con le sue paludi, torbiere, alpeggi e una flora incontaminata. Punto di partenza per itinerari interessanti, tra cui spicca l’arco della Greina, il più grande arco naturale del Canton Ticino.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da metà giugno a metà ottobre (nel 2026 dal 13 giugno al 10 ottobre); d’inverno il locale invernale da 10 posti, su riservazione"),
              ("Posti letto", "70"),
              ("Pasti", "Pasti caldi preparati dai guardiani tutto il giorno"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Dall’Alpe Garzott (Lago di Luzzone) 2h; dalla diga del Luzzone 3h30; da Pian Geirètt 3h30; da Ghirone per la Val Camadra 6h"),
               ("Accesso invernale", "Da Ghirone per la Val Camadra e il Passo della Greina, 5-6h, solo con neve assestata"),
               ("Cartina", 'CNS 1233 Greina, coordinate <span class="num">720.075 / 161.425</span>')],
        contact=[("Guardiano", "Fabio Merzaghi"),
                 ("Prenotazioni", '<a class="num" href="tel:+41918721622">+41 (0) 91 872 16 22</a> (da metà giugno a metà ottobre)'),
                 ("Cellulare", '<a class="num" href="tel:+41797276905">+41 (0) 79 727 69 05</a>'),
                 ("E-mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "MonteBar.html": dict(
        name="Monte Bar", where="Alta Capriasca, Luganese", alt_m="1620", beds="42", custody="tutto l’anno",
        mail="montebar@casticino.ch", booking=PRENOTA.format(168), facebook="https://www.facebook.com/CapannaMonteBarCAS/",
        description="Capanna Monte Bar, 1620 m, in Alta Capriasca: 42 posti letto in camere da 2, 4 e 6, custodita tutto l’anno, standard Bike Hotel. Contatti e prenotazioni.",
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
                 ("Telefono", '<a class="num" href="tel:+41919663322">+41 (0) 91 966 33 22</a>'),
                 ("E-mail", '<a href="mailto:montebar@casticino.ch">montebar@casticino.ch</a>')]),
    "BaitaDelLuca.html": dict(
        name="Baita del Luca", where="Cioascio, Sonvico", alt_m="1070", beds="16", custody="su riservazione",
        mail="baitaluca@casticino.ch",
        description="Baita del Luca, 1070 m, sopra Sonvico ai piedi dei Denti della Vecchia: 16 posti letto, autogestita, solo su riservazione. Ritrovo del gruppo giovani.",
        img=("capanne/baitadelluca-3x2", "La Baita del Luca su un pendio erboso sopra Sonvico", 1000, 667),
        intro="Su un ampio pendio erboso sopra Sonvico, ai piedi dei Denti della Vecchia: base ideale per escursioni, anche in famiglia, e arrampicate in un paesaggio unico. È il punto di ritrovo del <a href=\"Giovani.html\">gruppo giovani</a>.",
        stay=[("Apertura", "Chiusa; accessibile solo previa riservazione"),
              ("Posti letto", "16"),
              ("Pasti", "Possibilità di cucinare"),
              ("Bibite", "Disponibili anche in assenza del guardiano"),
              ("Prenotazioni", "Il codice d’accesso viene dato dopo il versamento anticipato")],
        reach=[("Accesso estivo", "Da Rosone 30 min; da Lovarescia (sopra Sonvico) 60 min; da Car e da Luss (Villa Luganese) 60 min"),
               ("Cartina", 'CNS 1333 Tesserete, coordinate <span class="num">722.980 / 102.600</span>')],
        contact=[("Responsabile", "Priska Deluigi, 6960 Odogno"),
                 ("Cellulare", '<a class="num" href="tel:+41792033084">+41 (0) 79 203 30 84</a>'),
                 ("E-mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Prenotazioni", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}


# testi fissi delle pagine capanna
TC = {
    "it": dict(prenota="Prenota", cucina="La cucina", team="Chi vi accoglie", vita="La cucina e i guardiani",
               tariffe="Tariffe e prenotazioni", accessi="Come arrivare", attivita="Attività", sostenitori="Sostenitori",
               storia="Storia", storia_link="La storia della capanna", foto="Foto", tutte_foto="Tutte le foto",
               in_breve="In breve", testo="Testo", itinerari="Itinerari", capanne="Le capanne", sezione_menu="Le Capanne",
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
}


def tc(chiave):
    return TC[LINGUA["lang"]][chiave]


def capanna(file):
    """Dati di HUT_PAGES nella lingua corrente (in tedesco i testi vengono da capanne_de.HUT_DE)."""
    d = dict(HUT_PAGES[file])
    if de():
        d.update(HUT_DE[file])
    return d


def contenuti(file):
    return (CONTENUTI_DE if de() else CONTENUTI).get(file)


def pubblica(nome, html):
    """Pagina in una sottocartella (de/, capanne/…): i percorsi relativi salgono dei livelli giusti."""
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
    """In tedesco i PDF (tutti in italiano) dentro i testi lo dicono, come quelli in link_capanna()."""
    if not de():
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
<div class="fb-feed" data-fb="{d['facebook']}" data-lang="{'de_DE' if de() else 'it_IT'}" data-titolo="Facebook {d['name']}">
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
    others = [h for h in (HUTS_DE if de() else HUTS) if h[0] != file]
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
    custody_dt = tc("apertura") if file == "BaitaDelLuca.html" else tc("custodia")
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
    prefix = tc("capanna") + " " if file != "BaitaDelLuca.html" else ""
    nome = L(file)
    return pubblica(nome, page(nome, f"{prefix}{d['name']} | CAS Ticino", d["description"], body, og=og))


# ------------------------------------------------------------------ la sezione

def introduzione():
    huts = ('<a href="CampoTencia.html">Campo Tencia</a>, <a href="Cristallina.html">Cristallina</a>, <a href="Adula.html">Adula</a>, '
            '<a href="Motterascio.html">Motterascio (Michela)</a>, <a href="MonteBar.html">Monte Bar</a> e <a href="BaitaDelLuca.html">Baita del Luca</a>')
    body = page_hero([("La Sezione", "index.html#sezione"), ("Introduzione", None)], "La sezione",
                     "Fondata a Bellinzona l’11 aprile 1886, la Sezione Ticino del Club Alpino Svizzero conta quasi 3000 soci e propone un’attività varia, pensata per tutte le età: dai più giovani ai seniori.") + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", "Gruppo di alpinisti in cammino su un ghiacciaio", mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
</figure>

<section class="section--accent" aria-label="La sezione in cifre">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>fondata a Bellinzona l’11 aprile</span></div>
<div class="stat"><strong>≈3000</strong><span>soci, dai più giovani ai seniori</span></div>
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
<a class="link" href="Corsi.html">Vedi i corsi</a>
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
<p>Un <a href="Comitato.html">comitato</a> coordina le diverse attività, affiancato da cinque <a href="Organizzazione.html">dicasteri</a> e dal lavoro volontario dei soci.</p>
</article>
<article class="pillar pillar--photo pillar--wide-md">
{img("corsi/racchette-4x5", "Cresta innevata sopra un mare di nuvole", 800, 1000)}
<h3>Comunicazione</h3>
<p>Programma delle attività, sito web, un periodico semestrale e l’annuario che racconta la vita della sezione.</p>
</article>
<article class="pillar pillar--dark pillar--wide">
<h3>Statuto, visione e strategia, organigramma</h3>
<p>I documenti di riferimento della sezione, in PDF. Gli altri sono nella pagina <a href="Documenti.html">Documenti</a>.</p>
<div class="actions"><a class="btn btn--primary" href="{DOC}statuto-visione/statuto-2025.pdf">Statuto <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/visione-strategia-2025.pdf">Visione e strategia</a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/organigramma-2025.pdf">Organigramma</a></div>
</article>
</div>
</div>
</section>

{subnav("La Sezione", "Introduzione.html")}"""
    return page("Introduzione.html", "La sezione | CAS Ticino",
                "La Sezione Ticino del Club Alpino Svizzero: fondata nel 1886, quasi 3000 soci, sei capanne, corsi, gite e attività per tutte le età.",
                body, og="paesaggi/gruppo-ghiacciaio-2000")


COMITATO = [
    ("Presidente", "Giovanni Galli", "giovanni.galli1@gmail.com", "giovanni-galli"),
    ("Capanne e vicepresidente", "Richard Knupfer", "richard@knupferarredamenti.ch", "richard-knupfer"),
    ("Segretaria", "Melanie Becchi", "melanie.becchi@gmail.com", "melanie-becchi"),
    ("Consigliere giuridico", "Costantino Castelli", "castelli@csnlaw.com", "costantino-castelli"),
    ("Finanze e sponsoring", "Claudio Roncoroni", "roncoroni.claudio@hotmail.com", "claudio-roncoroni"),
    ("Coordinazione gruppi", "Nadir Caduff", "nadir.caduff@bluewin.ch", "nadir-caduff"),
    ("Sport di montagna", "Geoffroy Jolly", "Geo155@gmail.com", None),
    ("Comunicazione", "Flavia Spinelli", "flavia.spinelli@bluewin.ch", None),
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
    "Responsabile amministrativo palestra Cornaredo": "Administration Kletterhalle Cornaredo", "Responsabile magazzino": "Verantwortlicher Materiallager",
    "Amministratrice sito web": "Administratorin Website", "Membro": "Mitglied", "Coordinatore e comunicazione": "Koordinator und Kommunikation",
    "Coach": "Coach", "Cassiere": "Kassier", "Segretariato, giovanissimi e Spider": "Sekretariat, Jüngste und Spider",
    "Attività del mercoledì sera e arrampicata": "Mittwochabend und Klettern", "Attività estive": "Sommeraktivitäten",
    "Attività invernali": "Winteraktivitäten", "Coordinatore gite": "Tourenkoordinator", "Informatica": "Informatik",
    "Responsabile comunicazione": "Verantwortlicher Kommunikation", "Redazione annuario": "Redaktion Jahrbuch", "Eventi": "Anlässe",
    "Grafica": "Grafik", "Responsabile ambiente": "Verantwortliche Umwelt",
}


def ruolo(r):
    """Ruolo nella lingua corrente (gli ispettori delle capanne in tedesco sono «Hüttenchef»)."""
    if not de():
        return r
    if r.startswith("Ispettore "):
        return "Hüttenchef " + r[len("Ispettore "):].replace(" e ", " und ")
    return RUOLI_DE.get(r, r)


def sezione_page(file, title, description, body, **kw):
    """Pagina della sezione nella lingua corrente (in tedesco: de/<file>)."""
    nome = L(file)
    return pubblica(nome, page(nome, title, description, body, **kw))


def comitato():
    people = []
    ritratto = "Porträt von" if de() else "Ritratto di"
    for role, name, mail, photo in COMITATO:
        role = ruolo(role)
        ph = (f'<img src="assets/img/persone/comitato/{photo}.webp" alt="{ritratto} {name}" width="96" height="96" loading="lazy">'
              if photo else f'<span aria-hidden="true">{initials(name)}</span>')
        people.append(f"""<article class="person">
<div class="person-photo">{ph}</div>
<div class="person-body">
<span class="role">{role}</span>
<h2>{name}</h2>
<a href="mailto:{mail}">{mail}</a>
</div>
</article>""")
    if de():
        body = page_hero([("Die Sektion", "de/Introduzione.html"), ("Vorstand", None)], "Der Vorstand",
                         "Acht Personen, jede mit einem klaren Aufgabenbereich, führen die Sektion zusammen mit den <a href=\"de/Organizzazione.html\">Ressorts</a> und den Freiwilligen.")
    else:
        body = page_hero([("La Sezione", "index.html#sezione"), ("Comitato", None)], "Il comitato",
                         "Otto persone, ognuna con un ambito preciso, che guidano la sezione insieme ai <a href=\"Organizzazione.html\">dicasteri</a> e ai volontari.")
    body += f"""

<section class="section" aria-label="{"Mitglieder des Vorstands" if de() else "Membri del comitato"}">
<div class="container">
<div class="people" data-reveal>
{chr(10).join(people)}
</div>
</div>
</section>

{subnav("Die Sektion" if de() else "La Sezione", L("Comitato.html"))}"""
    if de():
        return sezione_page("Comitato.html", "Vorstand | CAS Ticino",
                            "Der Vorstand der Sektion Ticino des Schweizer Alpen-Clubs: Präsident, Vizepräsident, Sekretärin und Verantwortliche, mit Kontakten.", body)
    return page("Comitato.html", "Comitato | CAS Ticino",
                "Il comitato della Sezione Ticino del Club Alpino Svizzero: presidente, vicepresidente, segretaria e responsabili, con i recapiti.",
                body)


DICASTERI = [
    ("Dicastero infrastruttura",
     "Si occupa delle infrastrutture della sezione: capanne e sentieri. Affianca il comitato su tutte le questioni e i progetti legati ai rifugi. Tramite gli ispettori segue l’operato dei guardiani, coordina la manutenzione ordinaria e straordinaria, cura gli aspetti amministrativi e contrattuali con i guardiani e sviluppa la promozione delle capanne.",
     [("Richard Knupfer", "Responsabile capanne", "richard@knupferarredamenti.ch"),
      ("Ulisse Conrengia", "Responsabile sentieri", None),
      ("Stefano Olgiati", "Responsabile sentieri", None),
      ("Edgardo Bulloni", "Responsabile tecnico capanne", "e_bulloni@bluewin.ch"),
      (None, "Ispettore Capanna Michela Motterascio", None),
      ("Edy Galli", "Ispettore Capanna Campo Tencia", "tgmgalli@yahoo.it"),
      ("Fabio Savoldelli", "Ispettore Capanna Adula", "fabio.savoldelli@bmsuisse.ch"),
      ("Marzio Pagani", "Ispettore Capanna Cristallina e Baita del Luca", "ma.pa@bluewin.ch"),
      ("Francesco Mattinelli", "Ispettore Capanna Cristallina", "f.mattinelli70@gmail.com"),
      ("Erico Fogliada", "Ispettore Capanna Monte Bar", "ericofo@bluewin.ch"),
      ("Mauro Scalmanini", "Ispettore Capanna Monte Bar", "mascate@bluewin.ch"),
      ("Roberto Grassi", "Ispettore Capanna Monte Bar", "roby.grassi@live.com")]),
    ("Dicastero sport di montagna",
     "Oltre a comporre il programma annuale delle gite, aggiorna e prepara materiale formativo, consiglia e sostiene i capigita promuovendone la formazione continua e gestisce il materiale tecnico della sezione.",
     [("Geoffroy Jolly", "Coordinatore e responsabile attività", "Geo155@gmail.com"),
      ("Enrico Zamboni", "Responsabile formazione", "zamboni.e.89@gmail.com"),
      ("David Stracquadanio", "Responsabile amministrativo palestra Cornaredo", "d.stracqua@bluewin.ch"),
      ("Michele Foletti", "Responsabile magazzino", "fole89@gmail.com"),
      ("Valeria Demarta", "Amministratrice sito web", "valeria.demarta@gmail.com"),
      ("Sara Della Frera", "Membro", "sara.dellafrera@gmail.com"),
      ("Thomas Arn", "Membro", "thomas.arn@ticino.com"),
      ("Alessandro Docimo", "Membro", "alessandro.docimo@outlook.com")]),
    ("Dicastero giovani",
     "Organizza campi settimanali e attività di arrampicata per ragazze e ragazzi dai 10 ai 22 anni e promuove la formazione di monitori Gioventù+Sport.",
     [("Diego Romelli", "Coordinatore e comunicazione", "diego.romelli15@gmail.com"),
      ("Claudio Petrini", "Coach", "claudio@petrininet.ch"),
      ("Nicola Martinoni", "Cassiere", "nicola.martinoni@bluewin.ch"),
      ("Giosiana Codoni", "Segretariato, giovanissimi e Spider", "giosiana.codoni@bluewin.ch"),
      ("Deborah Acierno", "Attività del mercoledì sera e arrampicata", "debo.ooacierno@gmail.com"),
      ("Kilian Knupfer", "Attività estive", "kilian.knupfer@gmail.com"),
      ("Jacopo Soldini", "Attività invernali", "soldini.jacopo@gmail.com")]),
    ("Dicastero senior",
     "Coordina il programma annuale del gruppo Senior: gite di un giorno, fine settimana e vacanze di più giorni. È sempre alla ricerca di nuovi capigita.",
     [("Luca Salzborn", "Presidente", "lsalzborn@gmail.com"),
      ("Cati Eisenhut", "Segretaria", "segretariato.seniori@casticino.ch"),
      ("Christoph Rudolf von Rohr", "Cassiere", "vonrohr55@gmail.com"),
      ("Fausto Cattalini", "Coordinatore gite", "laca2@bluewin.ch"),
      ("Fabrizio Gastori", "Informatica", "biciog@bluewin.ch"),
      ("Walter Baumgartner", "Membro", "Walterbaumgartner51@gmail.com")]),
    ("Dicastero comunicazione",
     "Cura il periodico semestrale, l’annuario, il sito e i canali social. Organizza, anche con altri partner, eventi e iniziative che promuovono la cultura della montagna.",
     [("Dario Lanfranconi", "Responsabile comunicazione", "dario.lanfranconi@gmail.com"),
      ("Alessandro Romelli", "Redazione annuario", "alessandro.romelli@outlook.com"),
      ("Katia Papa", "Eventi", "katiapa@bluewin.ch"),
      ("Roberto Grizzi", "Grafica", "bodesign@bluewin.ch"),
      ("Zita Sartori", "Responsabile ambiente", "zita.sartori@gmail.com"),
      ("Maria Jannuzzi", "Membro", "maria.jannuzzi@rsi.ch"),
      ("Tiziano Allevi", "Membro", "tiziano.allevi@bluewin.ch")]),
]


DICASTERI_DE = {
    "Dicastero infrastruttura": ("Ressort Infrastruktur",
        "Kümmert sich um die Infrastruktur der Sektion: Hütten und Wanderwege. Unterstützt den Vorstand in allen Fragen und Projekten rund um die Hütten. Über die Hüttenchefs begleitet es die Arbeit der Hüttenwarte, koordiniert den laufenden und ausserordentlichen Unterhalt, betreut die administrativen und vertraglichen Fragen mit den Hüttenwarten und fördert die Hütten."),
    "Dicastero sport di montagna": ("Ressort Bergsport",
        "Stellt das jährliche Tourenprogramm zusammen, aktualisiert und erstellt Ausbildungsunterlagen, berät und unterstützt die Tourenleiter in ihrer Weiterbildung und verwaltet das technische Material der Sektion."),
    "Dicastero giovani": ("Ressort Jugend",
        "Organisiert Lagerwochen und Kletteraktivitäten für Mädchen und Jungen von 10 bis 22 Jahren und fördert die Ausbildung von Leitern Jugend+Sport."),
    "Dicastero senior": ("Ressort Senioren",
        "Koordiniert das Jahresprogramm der Seniorengruppe: Tagestouren, Wochenenden und mehrtägige Ferien. Ist immer auf der Suche nach neuen Tourenleitern."),
    "Dicastero comunicazione": ("Ressort Kommunikation",
        "Betreut das halbjährliche Bulletin, das Jahrbuch, die Website und die sozialen Medien. Organisiert, auch mit Partnern, Anlässe und Initiativen zur Bergkultur."),
}

CARTELLE_DICASTERI = {"Dicastero infrastruttura": "infrastruttura", "Dicastero sport di montagna": "sport-di-montagna",
                      "Dicastero giovani": "giovani", "Dicastero senior": "senior", "Dicastero comunicazione": "comunicazione"}


def slug_nome(nome):
    t = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def organizzazione():
    depts = []
    for i, (title, text, members) in enumerate(DICASTERI, 1):
        ms = []
        for name, role, mail in members:
            role = ruolo(role)
            if name is None:
                ms.append(f'<div class="member member--tbd"><div class="member-photo" aria-hidden="true"><span>?</span></div>'
                          f'<div class="member-body"><strong>{"Noch offen" if de() else "Da definire"}</strong><span>{role}</span></div></div>')
                continue
            foto = f"assets/img/persone/{CARTELLE_DICASTERI[title]}/{slug_nome(name)}.webp"
            ph = (f'<img src="{foto}" alt="{"Porträt von" if de() else "Ritratto di"} {name}" width="60" height="60" loading="lazy" decoding="async">'
                  if os.path.exists(os.path.join(ROOT, foto)) else f'<span aria-hidden="true">{initials(name)}</span>')
            m = f'<a href="mailto:{mail}">{mail}</a>' if mail else ""
            ms.append(f'<div class="member"><div class="member-photo">{ph}</div>'
                      f'<div class="member-body"><strong>{name}</strong><span>{role}</span>{m}</div></div>')
        titolo, testo = DICASTERI_DE[title] if de() else (title, text)
        depts.append(f"""<article class="dept" id="{CARTELLE_DICASTERI[title]}" aria-labelledby="d{i}-h" data-reveal>
<div class="dept-intro">
<span class="dept-count">{len(members)} {"Mitglieder" if de() else "membri"}</span>
<h2 id="d{i}-h" class="h2">{titolo}</h2>
<p>{testo}</p>
</div>
<div class="members">
{chr(10).join(ms)}
</div>
</article>""")
    if de():
        body = page_hero([("Die Sektion", "de/Introduzione.html"), ("Organisation", None)], "Organisation",
                         'Der <a href="de/Comitato.html">Vorstand</a> stützt sich auf fünf Ressorts, die je für einen Bereich des Sektionslebens verantwortlich sind.')
    else:
        body = page_hero([("La Sezione", "index.html#sezione"), ("Organizzazione", None)], "Organizzazione",
                         'Il <a href="Comitato.html">comitato</a> si appoggia a cinque dicasteri, ognuno responsabile di un ambito della vita della sezione.')
    body += f"""

<section class="section" aria-label="{"Ressorts" if de() else "Dicasteri"}">
<div class="container">
{chr(10).join(depts)}
</div>
</section>

{subnav("Die Sektion" if de() else "La Sezione", L("Organizzazione.html"))}"""
    if de():
        return sezione_page("Organizzazione.html", "Organisation | CAS Ticino",
                            "Die fünf Ressorts der Sektion Ticino des SAC (Infrastruktur, Bergsport, Jugend, Senioren, Kommunikation) mit ihren Mitgliedern und Kontakten.", body)
    return page("Organizzazione.html", "Organizzazione | CAS Ticino",
                "I cinque dicasteri della Sezione Ticino del CAS (infrastruttura, sport di montagna, giovani, senior, comunicazione) con i loro membri e recapiti.",
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

{subnav("La Sezione", "Sede.html")}"""
    return page("Sede.html", "Sede e recapiti | CAS Ticino",
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


def storia():
    tl = "\n".join(f'<li><span class="year">{y}</span><span>{t}</span></li>' for y, t in (STORIA_DE if de() else STORIA))
    if de():
        body = page_hero([("Die Sektion", "de/Introduzione.html"), ("Geschichte", None)], "Seit 1886<br>zu Fuss unterwegs.",
                         "Mehr als ein Jahrhundert Besteigungen, Hütten, Rettung und Bergkultur: die Geschichte der Sektion in Etappen.")
    else:
        body = page_hero([("La Sezione", "index.html#sezione"), ("Storia", None)], "Dal 1886,<br>a piedi.",
                         "Più di un secolo di salite, rifugi, soccorso e cultura alpina: la storia della sezione in tappe.")
    body += f"""

<figure class="band">
{pic("paesaggi/seraccata", "Gletscherbruch unter blauem Himmel" if de() else "Seraccata di un ghiacciaio sotto il cielo azzurro", mobile="paesaggi/seraccata-4x3", w=2000, h=1125, lazy=False)}
</figure>

<section class="section" aria-labelledby="tappe-h">
<div class="container split">
<div class="split-intro">
<h2 id="tappe-h" class="h2">{"Die Etappen" if de() else "Le tappe"}</h2>
<p class="lead">{"Neben den Touren hat die Sektion immer Vorführungen, Vorträge und Diskussionen organisiert und ihr Leben in zahlreichen Publikationen und in den Jahrbüchern festgehalten." if de() else "Accanto all’attività sul terreno, la sezione ha sempre organizzato proiezioni, conferenze e dibattiti, e documentato la propria vita in numerose pubblicazioni e negli annuari."}</p>
</div>
<ol class="timeline" data-reveal>
{tl}
</ol>
</div>
</section>

{subnav("Die Sektion" if de() else "La Sezione", L("Storia.html"))}"""
    if de():
        return sezione_page("Storia.html", "Geschichte | CAS Ticino",
                            "Die Geschichte der Sektion Ticino des Schweizer Alpen-Clubs seit 1886: Gründung, Bergrettung, Expeditionen, Jugend- und Seniorengruppen, Hütten.", body)
    return page("Storia.html", "Storia | CAS Ticino",
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
    ("Meteo e neve", [("SLF, bollettini valanghe in Svizzera", "http://www.slf.ch/"), ("MeteoSvizzera", "http://www.meteosvizzera.ch/"),
                      ("Meteoblue, previsioni a 7 giorni", "http://www.meteoblue.com/"), ("MeteoCentrale", "http://www.meteocentrale.ch/it/"),
                      ("Bollettino valanghe Tirolo", "http://lawine.tirol.gv.at/"), ("Servizio valanghe italiano (CAI-SVI)", "http://www.cai-svi.it/j15/"),
                      ("Météo-France, meteo e valanghe", "http://france.meteofrance.com/france/accueil/")]),
    ("Condizioni e resoconti", [("Bergtour", "http://www.bergtour.ch/"), ("Hikr", "http://www.hikr.org/"), ("On-ice, nord Italia", "http://www.on-ice.it/"),
                                ("OHM Chamonix, Monte Bianco", "http://www.ohm-chamonix.com/"), ("Camptocamp", "http://www.camptocamp.org/"),
                                ("Montagne in Valle d’Aosta", "http://www.montagneinvalledaosta.com/"), ("MonteRosa4000", "http://www.monterosa4000.it/"),
                                ("ViaFerrata.org", "http://www.viaferrata.org/")]),
    ("Mappe e guide", [("MapPlus", "http://www.mapplus.ch/"), ("swisstopo", "http://www.swisstopo.ch/"),
                       ("Piz Bube, guide e cartine", "http://www.pizbube.ch/"), ("Edizioni CAS (SAC-Verlag)", "http://www.sac-verlag.ch/")]),
    ("Società alpinistiche ticinesi", [("CAS Bellinzona e valli", "http://www.casbellinzona.ch/"), ("CAS Locarno", "http://www.cas-locarno.ch/"),
                                       ("Federazione Alpinistica Ticinese", "http://www.fat-ti.ch/"), ("Società Escursionistica Verzaschese", "http://www.verzasca.com/sev"),
                                       ("Gruppo Scoiattoli Denti della Vecchia", "http://www.scoiattoli.ch/")]),
    ("Formazione", [("CAS Centrale", "http://www.sac-cas.ch/"), ("Gioventù+Sport", "http://www.jugendundsport.ch/"),
                    ("Ufficio cantonale G+S", "http://www4.ti.ch/decs/sa/ugs/")]),
    ("Capanne, guide e soccorso", [("Capanne CAS in Svizzera", "http://www.sac-cas.ch/huetten.html"), ("Capanneti, rifugi Ticino e Mesolcina", "http://www.capanneti.ch/"),
                                   ("Gruppo Guide Alpine Ticino", "http://www.guidealpineticino.ch/"), ("Soccorso Alpino Svizzero", "http://www.alpinerettung.ch/")]),
    ("Eventi e altre società", [("Tris Rotondo", "http://www.trisrotondo.ch/"), ("Skyrace Lodrino Lavertezzo", "http://www.lodrino-lavertezzo.ch/"),
                                ("Sci Club Lodrino-Prosito", "http://www.sclp.ch/"), ("PicAlciot, vie d’arrampicata in Ticino", "http://www.picalciot.ch/")]),
    ("News di montagna", [("PlanetMountain", "http://www.planetmountain.com/"), ("Montagna.tv", "http://www.montagna.tv/")]),
]


LINKS_DE = {"Capigita": "Tourenleiter", "Meteo e neve": "Wetter und Schnee", "Condizioni e resoconti": "Verhältnisse und Tourenberichte",
            "Mappe e guide": "Karten und Führer", "Società alpinistiche ticinesi": "Tessiner Bergsteigervereine", "Formazione": "Ausbildung",
            "Capanne, guide e soccorso": "Hütten, Bergführer und Rettung", "Eventi e altre società": "Anlässe und andere Vereine",
            "News di montagna": "Bergnews",
            "SLF, bollettini valanghe in Svizzera": "SLF, Lawinenbulletin Schweiz", "MeteoSvizzera": "MeteoSchweiz",
            "Meteoblue, previsioni a 7 giorni": "Meteoblue, 7-Tage-Prognose", "Bollettino valanghe Tirolo": "Lawinenwarndienst Tirol",
            "Servizio valanghe italiano (CAI-SVI)": "Italienischer Lawinendienst (CAI-SVI)", "Météo-France, meteo e valanghe": "Météo-France, Wetter und Lawinen",
            "On-ice, nord Italia": "On-ice, Norditalien", "OHM Chamonix, Monte Bianco": "OHM Chamonix, Mont Blanc",
            "Montagne in Valle d’Aosta": "Berge im Aostatal", "Piz Bube, guide e cartine": "Piz Bube, Führer und Karten",
            "Edizioni CAS (SAC-Verlag)": "SAC-Verlag", "Federazione Alpinistica Ticinese": "Tessiner Bergsteigerverband (FAT)",
            "CAS Centrale": "SAC Zentralverband", "Gioventù+Sport": "Jugend+Sport", "Ufficio cantonale G+S": "Kantonales J+S-Amt",
            "Capanne CAS in Svizzera": "SAC-Hütten in der Schweiz", "Capanneti, rifugi Ticino e Mesolcina": "Capanneti, Hütten im Tessin und Misox",
            "Gruppo Guide Alpine Ticino": "Tessiner Bergführer", "Soccorso Alpino Svizzero": "Alpine Rettung Schweiz",
            "PicAlciot, vie d’arrampicata in Ticino": "PicAlciot, Kletterrouten im Tessin", "Portale DropTour": "DropTour-Portal",
            "Reset password": "Passwort zurücksetzen"}


def link():
    if de():
        gruppi = [(LINKS_DE.get(g, g), [(LINKS_DE.get(n, n), u) for n, u in links]) for g, links in LINKS]
        hero = page_hero([("Die Sektion", "de/Introduzione.html"), ("Nützliche Links", None)], "Nützliche Links",
                         "Wetter, Lawinenbulletins, Verhältnisse, Karten und die anderen Bergsteigervereine der Region.")
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

{subnav("Die Sektion" if de() else "La Sezione", L("Link.html"))}"""
    if de():
        return sezione_page("Link.html", "Nützliche Links | CAS Ticino",
                            "Nützliche Links für die Berge: Wetter und Lawinenbulletins, Verhältnisse, Karten, Tessiner Bergsteigervereine, Ausbildung und Rettung.", body)
    return page("Link.html", "Link utili | CAS Ticino",
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
    body = page_hero([("Media", "index.html#media"), ("Documenti", None)], "Documenti",
                     "Statuto e documenti della sezione, scale di difficoltà, promemoria tecnici, documenti dei corsi, moduli e cartine da scaricare.") + f"""

<section class="section" aria-label="Documenti">
<div class="container">
{linkgroups(DOCS, "PDF")}
<div class="callout">
<p><strong>Annuari e Informazione</strong>, il bollettino della sezione, hanno una pagina propria.</p>
<div class="actions"><a class="btn btn--secondary" href="Annuari.html">Annuari</a><a class="btn btn--secondary" href="Informazione.html">Informazione</a></div>
</div>
</div>
</section>

{subnav("Media", "Documenti.html")}"""
    return page("Documenti.html", "Documenti | CAS Ticino",
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
    body = page_hero([("News", None)], "News", "Serate, eventi, corsi e avvisi della sezione: tutte le notizie, dalla più recente.") + f"""

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
    return page("News.html", "News | CAS Ticino",
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
{crumbs(("News", "News.html"), (esc(n["title"]), None))}
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
<a class="link" href="News.html">Tutte le news</a>
</div>
<div class="news-grid">
{chr(10).join(news_card(x) for x in altre)}
</div>
</div>
</section>"""
    su = "../" * n["file"].count("/")  # news/<anno>/… : due livelli sotto la radice
    return in_sottocartella(page(n["file"], f"{esc(n['title'])} | CAS Ticino", esc(n["excerpt"][:155]), body,
                                 og=og_name(n), section="News"), su=su)


def foto():
    body = page_hero([("Media", "index.html#media"), ("Foto e resoconti", None)], "Foto e resoconti", "Le foto e i resoconti delle ultime gite della sezione, pubblicati dai capigita sul portale Droptour.") + f"""

<section class="section" aria-label="Ultime gite">
<div class="container">
<div id="albums" aria-live="polite"><p class="albums-status">Caricamento delle foto…</p></div>
<div class="albums-more">
<button type="button" class="btn btn--secondary" id="load-more" hidden>Carica altre gite</button>
</div>
</div>
</section>

{subnav("Media", "index.html#media")}"""
    return page("Foto.html", "Foto e resoconti delle gite | CAS Ticino",
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
                    "pdf": f"docs/{cartella}/{nome}", "mb": f"{mb:.1f}".replace(".", ","),
                    "cover": f"assets/img/pubblicazioni/{base}.webp", "w": w, "h": h})
    return sorted(out, key=lambda x: x["ordine"], reverse=True)


def pub_card(x, titolo):
    return f"""<a class="pub" href="{x['pdf']}">
<figure><img src="{x['cover']}" alt="Copertina: {titolo}" width="{x['w']}" height="{x['h']}" loading="lazy" decoding="async"></figure>
<strong>{titolo}</strong>
<span class="small">PDF, {x['mb']} MB</span>
</a>"""


def pub_feature(x, titolo, testo):
    return f"""<div class="pub-feature" data-reveal>
<figure><img src="{x['cover']}" alt="Copertina: {titolo}" width="{x['w']}" height="{x['h']}"></figure>
<div class="pub-feature-body">
<span class="label">Ultimo numero</span>
<h2 class="h2">{titolo}</h2>
<p>{testo}</p>
<a class="btn btn--primary" href="{x['pdf']}">Leggi il PDF <span class="arrow" aria-hidden="true">→</span></a>
<span class="small">PDF, {x['mb']} MB</span>
</div>
</div>"""


def media_section():
    """Home: un riquadro per ciascuna pagina di Media, con l'ultima foto, le ultime copertine e i documenti."""
    foto = json.load(open(os.path.join(ROOT, "data", "foto.json"), encoding="utf-8")).get("albums", [])
    foto = next((a for a in foto if a.get("photos")), None)
    ann = pubblicazioni("annuari", "annuario")[0]
    inf = pubblicazioni("informazione", "informazione")[0]
    n_doc = sum(len(g[1]) for g in DOCS)
    foto_fig = (f'<figure><img src="{foto["photos"][0]["large"]}" alt="" loading="lazy" decoding="async"></figure>'
                if foto else f'<figure>{img("attivita/gite-2x1", "", 1400, 700)}</figure>')
    foto_txt = f"Ultima gita: {esc(foto['title'])}" if foto else "Le foto e i resoconti delle gite della sezione"
    return f"""<section class="section" id="media" aria-labelledby="media-h">
<div class="container">
<div class="section-row">
<h2 id="media-h" class="h2">Media</h2>
</div>
<div class="media-grid" data-reveal>
<a class="media-card" href="Foto.html">
{foto_fig}
<div class="media-card-body"><h3>Foto e resoconti</h3><p>{foto_txt}</p></div>
</a>
<a class="media-card media-card--cover" href="Annuari.html">
<figure><img src="{ann['cover']}" alt="" width="{ann['w']}" height="{ann['h']}" loading="lazy" decoding="async"></figure>
<div class="media-card-body"><h3>Annuari</h3><p>Annuario {ann['anno']} e annate precedenti</p></div>
</a>
<a class="media-card media-card--cover" href="Informazione.html">
<figure><img src="{inf['cover']}" alt="" width="{inf['w']}" height="{inf['h']}" loading="lazy" decoding="async"></figure>
<div class="media-card-body"><h3>Informazione</h3><p>Il bollettino, numero di {inf['quando']}</p></div>
</a>
<a class="media-card media-card--docs" href="Documenti.html">
<figure aria-hidden="true"><strong>{n_doc}</strong><span>PDF da scaricare</span></figure>
<div class="media-card-body"><h3>Documenti</h3><p>Statuto, scale di difficoltà, promemoria, cartine</p></div>
</a>
</div>
</div>
</section>"""


def annuari():
    items = pubblicazioni("annuari", "annuario")
    ultimo, altri = items[0], items[1:]
    body = page_hero([("Media", "index.html#media"), ("Annuari", None)], "Annuari",
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

{subnav("Media", "Annuari.html")}"""
    return page("Annuari.html", "Annuari | CAS Ticino",
                "Gli annuari della Sezione Ticino del Club Alpino Svizzero da scaricare in PDF.",
                body, og=ultimo["cover"][len("assets/img/"):-len(".webp")])


def informazione():
    items = pubblicazioni("informazione", "informazione")
    ultimo, altri = items[0], items[1:]
    griglia = (f"""<div class="section-row"><h2 class="h3">Numeri precedenti</h2></div>
<div class="pubs" data-reveal>
{chr(10).join(pub_card(x, f"Informazione, {x['quando']}") for x in altri)}
</div>""" if altri else "")
    body = page_hero([("Media", "index.html#media"), ("Informazione", None)], "Informazione",
                     "Il bollettino ufficiale della sezione: notizie, attività e appuntamenti, da sfogliare in PDF.") + f"""

<section class="section" aria-label="Numeri di Informazione">
<div class="container">
{pub_feature(ultimo, f"Informazione, {ultimo['quando']}", "Il numero più recente del bollettino ufficiale della Sezione Ticino.")}
{griglia}
</div>
</section>

{subnav("Media", "Informazione.html")}"""
    return page("Informazione.html", "Informazione | CAS Ticino",
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
    join = "https://www.sac-cas.ch/it/affiliazione/diventasocio/?section=5100"
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
    return page("Adesione.html", "Diventa socio | CAS Ticino",
                "Diventa socio della Sezione Ticino del Club Alpino Svizzero: quote annuali per singoli, famiglie e giovani, e vantaggi per i soci.",
                body, og="paesaggi/laghetto-alpino-2000")


# ------------------------------------------------------------------ attività

def giovani():
    groups = [("2-10", "Giovanissimi e famiglie", "Arrampicata in famiglia: i bambini imparano a muoversi in corda, gli adulti ad assicurare."),
              ("9-14", "Spider", "Arrampicata, nevai, lettura della carta e scoperta della natura, tra gioco, divertimento e spirito di gruppo."),
              ("13-17", "Junior", "D’inverno sci alpinismo e splitboard, d’estate creste e arrampicata: prima il divertimento e la sicurezza, poi l’autonomia."),
              ("16-22", "OG", "Sci alpinismo impegnativo, cascate di ghiaccio e arrampicata tecnica in tutto l’arco alpino. Chi vuole può formarsi come monitore.")]
    cards = "\n".join(f"""<article class="group">
<div class="age">{a}<span>anni</span></div>
<h3 class="h3">{t}</h3>
<p>{p}</p>
</article>""" for a, t, p in groups)
    rows = [("Iscrizione", "Su Droptour, almeno due settimane prima per le singole attività, oppure dal coordinatore per iscrizioni a blocchi."),
            ("Requisiti", 'Serve essere soci del CAS Ticino, tranne per le uscite di prova. <a href="Adesione.html">Diventa socio</a>'),
            ("Costi", "Coprono vitto e alloggio a mezza pensione, guida e trasporto in furgone. Dai 20 ai 25 anni si aggiungono CHF 30 al giorno, perché non ci sono contributi G+S."),
            ("Inclusione", "Ragazze e ragazzi con disabilità fisica o psichica sono i benvenuti: contatta il coordinatore per trovare insieme la soluzione giusta."),
            ("Coordinatore", 'Diego Romelli, <a class="num" href="tel:+393485731549">+39 348 573 1549</a>'),
            ("Cassiere", 'Nicola Martinoni, <a class="num" href="tel:+41794391691">+41 (0) 79 439 16 91</a>'),
            ("Spider", "Giosiana Codoni"),
            ("Ritrovo", '<a href="BaitaDelLuca.html">Baita del Luca</a>, ai piedi dei Denti della Vecchia')]
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
<div><a class="link" href="{GITE_GIOVANI}">Programma giovani su Droptour</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "Giovani.html")}"""
    return page("Giovani.html", "Giovani | CAS Ticino",
                "Il gruppo giovani del CAS Ticino: arrampicata, sci alpinismo, campi e uscite per ragazze e ragazzi dai 2 ai 22 anni, con monitori e guide alpine.",
                body, og="attivita/giovani-3x4")


def senior():
    rows = [("Chi può partecipare", 'Dai 60 anni, con l’affiliazione al CAS Ticino. Non c’è una tassa aggiuntiva, e tutti i soci della sezione possono partecipare alle attività. <a href="Adesione.html">Diventa socio</a>'),
            ("Come aderire", 'Scrivi a <a href="mailto:segretariato.seniori@casticino.ch">segretariato.seniori@casticino.ch</a> con nome, data di nascita, numero di socio CAS, indirizzo, telefono ed e-mail.'),
            ("Uscite", "Di norma il giovedì. Il calendario aggiornato è sul programma gite online."),
            ("Pranzi", 'Il secondo e il quarto mercoledì del mese al Bistrot Vecchio Torchio di Viganello. Iscrizioni entro il lunedì presso Hanni Vanossi (<a class="num" href="tel:+41763973390">+41 (0) 76 397 33 90</a>) o direttamente al ristorante (<a class="num" href="tel:+41919721010">+41 (0) 91 972 10 10</a>).'),
            ("Capigita", 'Il dicastero cerca sempre nuovi capigita. <a href="Documenti.html">Promemoria capigita</a>')]
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

{subnav("Attività", "Senior.html")}"""
    return page("Senior.html", "Senior | CAS Ticino",
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
                  'Serata di presentazione il 12 marzo 2027 a Bellinzona; uscite il 28-30 maggio, il 12-13 giugno e il 3-4 luglio 2027. CHF 700 per i soci, 800 per i non soci, 450 per i giovani G+S e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing escluse.')),
    ("Inverno", "Sci alpinismo", "corsi/scialpinismo-4x5", (582, 728), "Sci alpinisti in salita su un pendio innevato",
     "Per muoversi in sicurezza e in autonomia nelle gite della sezione: salita con le pelli su pendii ripidi, discesa fuori pista, uso del materiale di sicurezza, valutazione del pericolo valanghe e pianificazione.",
     GITE_CORSI,
     schede_corso("sci-alpinismo",
                  "Sette giorni: una giornata introduttiva ad Airolo per verificare forma e tecnica, una serata di teoria su neve, ARTVA e autosoccorso, poi tre fine settimana alla Capanna Piansecco, all’Hotel Tiefenbach sul Furka e alla Camona da Maighels, con istruzione e gite fino a 800-1200 m di dislivello.",
                  "Sciare bene su piste nere e reggere una gita di 1200 m di dislivello con uno zaino di 5 kg in al massimo 4 ore. Età minima 16 anni. Aperto anche agli snowboarder con splitboard. Chi dopo la giornata introduttiva non risulta idoneo riceve l’80% della quota.",
                  'Al massimo 30. Iscrizioni dal 1° ottobre al 1° dicembre 2026, o fino a esaurimento dei posti; la quota va versata entro il 10 dicembre. Uscite obbligatorie, con qualsiasi tempo; assenze e ritiri non danno diritto a rimborsi.',
                  "Attrezzatura completa da sci alpinismo. ARTVA, pala e sonda prestati su richiesta, compresi nella quota.",
                  'Presentazione il 3 dicembre 2026 (anche via Teams); giornata introduttiva il 9 gennaio, teoria il 12 gennaio, uscite il 16-17 gennaio, il 20-21 febbraio e il 6-7 marzo 2027. CHF 650 per i soci, 750 per i non soci, 400 per i giovani G+S fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (circa CHF 100) escluse.')),
    ("Primavera", "Arrampicata", "corsi/arrampicata-4x5", (594, 742), "Cordata su una parete di roccia accanto a un ghiacciaio",
     "Per principianti che vogliono avvicinarsi all’arrampicata in ambiente e per chi vuole consolidare la tecnica: sicurezza, manovre di corda, progressione su vie di più tiri. Dopo le basi, sempre più autonomia sotto la supervisione di un istruttore di arrampicata.",
     GITE_CORSI,
     schede_corso("arrampicata",
                  "Sette giorni in tre fine settimana: prime arrampicate in falesia in Piemonte, vie di più tiri nel Locarnese, gite di applicazione nelle Alpi centrali; tra maggio e giugno, a volte, serate di arrampicata e ripasso dei nodi. Alla fine si arrampica in autonomia in falesia e su vie di più tiri: da secondi fino al 5a, da primi fino al 4b, con discesa in corda doppia.",
                  "Nessun prerequisito tecnico: il corso è pensato per chi comincia. Età minima 16 anni.",
                  "Al massimo 26, in ordine d’iscrizione. All’iscrizione si versa un anticipo di CHF 300; l’iscrizione è definitiva con il saldo alla serata di presentazione. Serata e uscite obbligatorie, con qualsiasi tempo; le assenze vanno annunciate al capocorso entro il martedì prima.",
                  "Il CAS presta il materiale tecnico a chi non ce l’ha; alla serata di presentazione si vede cosa serve.",
                  'Presentazione il 12 aprile 2027 alle 20:00 alla Scuola professionale di Trevano; uscite il 1-2 maggio, il 15-17 maggio e il 12-13 giugno 2027. CHF 600 per i soci, 650 per i non soci, 400 per i giovani dai 16 ai 20 anni; trasferte in car sharing (CHF 40) escluse.')),
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
                  'Serata introduttiva martedì 15 dicembre 2026 nel Luganese; nivologia il 12 gennaio 2027 a Mezzovico, sicurezza il 16 gennaio ad Airolo, uscite il 23-24 gennaio e il 13-14 febbraio 2027. CHF 650 per i soci, 700 per i non soci, 375 per i giovani OG dai 16 ai 20 anni, trasferte comprese.')),
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
{pic("paesaggi/traccia-ghiacciaio", "Traccia di sci su un ghiacciaio, sotto una cima innevata", mobile="paesaggi/traccia-ghiacciaio-4x3", w=2000, h=901, lazy=False)}
</figure>

<section class="section" aria-label="Corsi base">
<div class="container">
{rows}
</div>
</section>

<section class="section" aria-labelledby="avanzati-h">
<div class="container">
<div class="callout">
<p><strong id="avanzati-h">Verso capogita e monitore G+S.</strong> Per chi vuole approfondire o prepararsi ai corsi capogita CAS e monitore Gioventù+Sport, la sezione propone corsi avanzati nelle tre discipline e serate di formazione teorica con specialisti.</p>
</div>
</div>
</section>

{subnav("Attività", "Corsi.html")}"""
    return page("Corsi.html", "Corsi | CAS Ticino",
                "Corsi del CAS Ticino diretti da professionisti: sci alpinismo, racchette, tecnica di sci fuori pista, arrampicata e alpinismo.",
                body, og="corsi/scialpinismo-4x5")


def noleggio():
    rows = [("Come funziona", "Compila il formulario con i dati dell’attività e il materiale che ti serve. Con la conferma ricevi il codice d’accesso e le istruzioni per il ritiro. Si paga in contanti alla riconsegna."),
            ("Richiesta", "Una settimana prima dell’attività"),
            ("Ritiro", 'Dal mercoledì alle <span class="num">19:00</span>'),
            ("Riconsegna", "Entro il martedì sera"),
            ("Magazzino", "Manno"),
            ("Responsabile", 'Michele Foletti, <a class="num" href="tel:+41792416955">+41 (0) 79 241 69 55</a> (anche WhatsApp), <a href="mailto:fole89@gmail.com">fole89@gmail.com</a>')]
    body = page_hero([("Attività", "index.html#attivita"), ("Noleggio", None)], "Noleggio",
                     "Materiale in affitto per le attività della sezione e per le uscite private.") + f"""

<section class="section" aria-labelledby="cosa-h">
<div class="container detail">
<div class="detail-intro split-intro">
<h2 id="cosa-h" class="h2">Dall’arrampicata<br>al bouldering</h2>
<p>Alpinismo, mountain bike, cascate di ghiaccio, sci alpinismo, arrampicata, racchette, escursionismo e bouldering. L’elenco completo con i prezzi giornalieri è nella lista del magazzino.</p>
<div><a class="btn btn--primary" href="{DOC}noleggio/lista-materiale.pdf">Lista materiale (PDF) <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "Noleggio.html")}"""
    return page("Noleggio.html", "Noleggio | CAS Ticino",
                "Noleggio materiale del CAS Ticino: alpinismo, sci alpinismo, arrampicata, racchette e altro, con ritiro al magazzino di Manno.",
                body)


# ------------------------------------------------------------------ versione tedesca (de/)
# Solo La Sezione, le capanne e Adesione sono tradotte; news, attività, media e PDF restano in italiano.
# I testi sono scritti con i percorsi dalla radice del sito: i link alle pagine tedesche hanno de/ davanti.

def home_de():
    huts = "\n".join(f"""<a class="hut{' hut--big' if big else ''}" href="de/{f}" data-reveal>
<figure>{img(im, f'Capanna {n}', w, h)}</figure>
<div class="hut-head"><h3 class="h3">{n}</h3><span class="hut-alt">{q} m</span></div>
<div class="hut-meta"><span>{v}</span><span class="status">{st}</span></div>
<p>{t}</p>
<div class="hut-meta"><span>{posti}</span><span>Zugang ab {acc}</span></div>
</a>""" for f, n, q, v, st, t, posti, acc, im, (w, h), big in HUTS_DE)
    html = head("CAS Ticino | Schweizer Alpen-Club, Sektion Ticino",
                "Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter. Seit über hundert Jahren das Zuhause des Tessiner Alpinismus.",
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n')
    html += "\n<body>\n" + nav("de/index.html") + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">In die Berge<br>mit <span class="accent">uns</span>.</h1>
<div class="hero-foot">
<p class="lead">Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter.</p>
<div class="actions">
<a class="btn btn--primary" href="de/Adesione.html">Mitglied werden <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="#capanne">Die Hütten</a>
</div>
</div>
</div>
<figure class="band">
{pic("paesaggi/sciatori-villaggio", "Skitourengeher im Aufstieg zu einem verschneiten Dorf", mobile="paesaggi/sciatori-villaggio-4x3", w=2000, h=901, lazy=False, cls="pos-low")}
</figure>
</section>

<section class="section section--tight section--stats" id="sezione" aria-label="Die Sektion in Zahlen">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>Gründungsjahr</span></div>
<div class="stat"><strong>≈3000</strong><span>Mitglieder</span></div>
<div class="stat"><strong>6</strong><span>Hütten, 362 Schlafplätze</span></div>
<div class="stat"><strong>5</strong><span>Disziplinen in den Kursen</span></div>
</div>
</div>
</section>

<section class="section section--tight section--after-stats" aria-labelledby="sektion-h">
<div class="container split">
<div class="split-intro">
<h2 id="sektion-h" class="h2">Seit 1886<br>zu Fuss unterwegs.</h2>
<p class="lead">Gegründet in der Birraria Gambrinus in Bellinzona, im Jubiläumsjahr der Erstbesteigung des Mont Blanc, um die Berge des Kantons «zu besuchen, zu erforschen und bekannt zu machen».</p>
<div class="links"><a class="link" href="de/Introduzione.html">Die Sektion</a><a class="link" href="de/Storia.html">Geschichte</a></div>
</div>
<div class="callout" data-reveal>
<p><strong>Vieles gibt es nur auf Italienisch.</strong> Tourenprogramm, News, Kurse, Jugend- und Seniorengruppen, Fotos und Dokumente der Sektion sind nur auf Italienisch verfügbar.</p>
<div class="links"><a class="link" href="{GITE}">Tourenprogramm</a><a class="link" href="News.html">News</a><a class="link" href="Corsi.html">Kurse</a></div>
</div>
</div>
</section>

<section class="section" id="capanne" aria-labelledby="capanne-h">
<div class="container">
<div class="section-head">
<h2 id="capanne-h" class="h2">Sechs Hütten, ein Tessin</h2>
<p class="lead">Immer offen, bewartet, wenn die Hüttenwarte da sind. Melden Sie sich vor dem Aufbruch beim Hüttenwart, um Anwesenheit und Verhältnisse am Berg zu prüfen.</p>
</div>
<div class="huts">
{huts}
</div>
</div>
</section>

<section class="cta-band" id="adesione" aria-labelledby="adesione-h">
{pic("paesaggi/tramonto-larici", "", mobile="paesaggi/tramonto-larici-4x3", w=2000, h=1126)}
<div class="container">
<h2 id="adesione-h" class="h2">Kommen Sie mit.</h2>
<p>Günstigere Preise in den SAC-Hütten der ganzen Schweiz, Kurse, Touren und eine Gemeinschaft, die die Berge so liebt wie Sie.</p>
<a class="btn btn--light" href="de/Adesione.html">Mitglied werden <span class="arrow" aria-hidden="true">→</span></a>
</div>
</section>

</main>
""" + footer()
    return pubblica("de/index.html", html)


def introduzione_de():
    huts = ('<a href="de/CampoTencia.html">Campo Tencia</a>, <a href="de/Cristallina.html">Cristallina</a>, <a href="de/Adula.html">Adula</a>, '
            '<a href="de/Motterascio.html">Motterascio (Michela)</a>, <a href="de/MonteBar.html">Monte Bar</a> und <a href="de/BaitaDelLuca.html">Baita del Luca</a>')
    body = page_hero([("Die Sektion", "de/Introduzione.html"), ("Einführung", None)], "Die Sektion",
                     "Am 11. April 1886 in Bellinzona gegründet, zählt die Sektion Ticino des Schweizer Alpen-Clubs fast 3000 Mitglieder und bietet ein vielfältiges Programm für jedes Alter: von den Jüngsten bis zu den Senioren.") + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", "Eine Gruppe Bergsteiger unterwegs auf einem Gletscher", mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
</figure>

<section class="section--accent" aria-label="Die Sektion in Zahlen">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>am 11. April in Bellinzona gegründet</span></div>
<div class="stat"><strong>≈3000</strong><span>Mitglieder, von den Jüngsten bis zu den Senioren</span></div>
<div class="stat"><strong>6</strong><span>Hütten im Besitz der Sektion</span></div>
<div class="stat"><strong>5</strong><span>Ressorts neben dem Vorstand</span></div>
</div>
</div>
</section>

<section class="section" aria-labelledby="cosa-h">
<div class="container">
<div class="section-head">
<h2 id="cosa-h" class="h2">In den Bergen,<br>zu jeder Jahreszeit</h2>
</div>
<div class="pillars" data-reveal>
<article class="pillar pillar--photo pillar--wide">
{img("paesaggi/cresta-lugano-2000", "Bergsteiger auf einem Felsgrat", 2000, 580)}
<h3>Disziplinen</h3>
<p>Wandern, Bergsteigen, Klettern, Skitouren, Schneeschuhwandern und Eisklettern.</p>
</article>
<article class="pillar pillar--accent">
<h3>Für Einsteiger</h3>
<p>Einführungskurse in Bergsteigen, Skitouren, Schneeschuhwandern und Klettern im Gelände (auf Italienisch).</p>
<a class="link" href="Corsi.html">Zu den Kursen</a>
</article>
<article class="pillar pillar--photo">
{img("capanne/montebar-3x2", "Die Capanna Monte Bar", 663, 442)}
<h3>Hütten</h3>
<p>Die Sektion besitzt sechs Hütten: {huts}.</p>
</article>
<article class="pillar">
<h3>Mehr als Sport</h3>
<p>Sie koordiniert die Bergrettung im Sottoceneri, setzt sich für den Schutz der alpinen Umwelt ein und fördert die Bergkultur.</p>
</article>
<article class="pillar">
<h3>So funktioniert es</h3>
<p>Ein <a href="de/Comitato.html">Vorstand</a> koordiniert die verschiedenen Aktivitäten, unterstützt von fünf <a href="de/Organizzazione.html">Ressorts</a> und der Freiwilligenarbeit der Mitglieder.</p>
</article>
<article class="pillar pillar--photo pillar--wide-md">
{img("corsi/racchette-4x5", "Verschneiter Grat über einem Nebelmeer", 800, 1000)}
<h3>Kommunikation</h3>
<p>Tourenprogramm, Website, ein halbjährliches Bulletin und das Jahrbuch, das vom Leben der Sektion erzählt (auf Italienisch).</p>
</article>
<article class="pillar pillar--dark pillar--wide">
<h3>Statuten, Vision und Strategie, Organigramm</h3>
<p>Die massgebenden Dokumente der Sektion, als PDF auf Italienisch. Weitere finden Sie auf der Seite <a href="Documenti.html">Dokumente</a>.</p>
<div class="actions"><a class="btn btn--primary" href="{DOC}statuto-visione/statuto-2025.pdf">Statuten <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/visione-strategia-2025.pdf">Vision und Strategie</a><a class="btn btn--ghost-dark" href="{DOC}statuto-visione/organigramma-2025.pdf">Organigramm</a></div>
</article>
</div>
</div>
</section>

{subnav("Die Sektion", "de/Introduzione.html")}"""
    return sezione_page("Introduzione.html", "Die Sektion | CAS Ticino",
                        "Die Sektion Ticino des Schweizer Alpen-Clubs: 1886 gegründet, fast 3000 Mitglieder, sechs Hütten, Kurse, Touren und Aktivitäten für jedes Alter.",
                        body, og="paesaggi/gruppo-ghiacciaio-2000")


def sede_de():
    rows = [
        ("Postadresse", "Schweizer Alpen-Club<br>Sektion Ticino<br>Postfach 112<br>6998 Monteggio 2"),
        ("E-Mail", '<a href="mailto:info@casticino.ch">info@casticino.ch</a>'),
        ("Sitz", "Gebäude Canvetto Luganese, Molino Nuovo (Lugano)<br>2. Stock, auf der Galerie"),
        ("Bibliothek", 'Führer und Karten zum Nachschlagen, Bücher zum Ausleihen; Bücher und T-Shirts zu kaufen. Für einen Besuch schreiben Sie dem Sekretariat: <a href="mailto:info@casticino.ch">info@casticino.ch</a>.'),
        ("Bankverbindung", 'Banca Stato, Lugano<br><span class="num">IBAN CH09 0076 4128 9526 1200 6</span>'),
    ]
    body = page_hero([("Die Sektion", "de/Introduzione.html"), ("Sitz und Kontakt", None)], "Sitz und Kontakt",
                     "Der Sitz der Sektion befindet sich im Gebäude Canvetto Luganese in Molino Nuovo, mit Büro und Sitzungszimmer im zweiten Stock auf der Galerie.") + f"""

<section class="section" aria-labelledby="sede-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="sede-h" class="h2">Der Canvetto Luganese</h2>
<p>Hier treffen sich der Vorstand und die Ressorts, hier finden die Informationsabende der Kurse und verschiedene kulturelle Anlässe statt: Bilder von Touren, Reisen und Expeditionen der Mitglieder, Abende mit Fachleuten für Wetter, Lawinen und Erste Hilfe.</p>
<div><a class="btn btn--primary" href="mailto:info@casticino.ch">Der Sektion schreiben <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
{facts(rows)}
</div>
</div>
</section>

{subnav("Die Sektion", "de/Sede.html")}"""
    return sezione_page("Sede.html", "Sitz und Kontakt | CAS Ticino",
                        "Sitz des CAS Ticino im Canvetto Luganese (Molino Nuovo), Postadresse, E-Mail, Bibliothek und Bankverbindung.", body)


def adesione_de():
    prices = [("Einzel", "Einzelmitglied", "105", "30"),
              ("Familie", "Eltern und Kinder bis 17 Jahre", "179", "50"),
              ("Jugend", "Bis 22 Jahre", "50", "30")]
    cards = "\n".join(f"""<article class="price">
<h3 class="h3">{t}</h3>
<p>{who}</p>
<div class="amount"><small>CHF</small>{amt}</div>
<p class="small">+ CHF {fee} beim ersten Beitritt</p>
</article>""" for t, who, amt, fee in prices)
    rows = [("Hütten", "Bis 50 % Rabatt in den Hütten der ganzen Schweiz und in einigen europäischen Ländern"),
            ("Tourenportal", "Kostenloser Zugang zu Karten und Routen im SAC-Tourenportal"),
            ("Ausbildung", "Vergünstigungen bei den Kursen"),
            ("Publikationen", "Die Zeitschrift «Die Alpen», das Bulletin der Sektion und Rabatte auf SAC-Publikationen"),
            ("Klettern", "Freier Eintritt in die Kletterhalle San Paolo")]
    join = "https://www.sac-cas.ch/de/mitgliedschaft/mitglied-werden/?section=5100"
    body = page_hero([("Mitgliedschaft", None)], "Mitglied werden",
                     "Treten Sie der Tessiner Sektion des Schweizer Alpen-Clubs bei: Touren, Kurse, Hütten und eine Gemeinschaft, die die Berge liebt.",
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{join}">Auf der SAC-Website beitreten <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<figure class="band">
{pic("paesaggi/laghetto-alpino", "Bergsee zwischen Felsen, im Hintergrund die Berge", mobile="paesaggi/laghetto-alpino-4x3", w=2000, h=1126, lazy=False)}
</figure>

<section class="section" aria-labelledby="quote-h">
<div class="container">
<div class="section-head"><h2 id="quote-h" class="h2">Jahresbeiträge</h2></div>
<div class="prices" data-reveal>
{cards}
</div>
<p class="note">Sie sind schon Mitglied einer anderen SAC-Sektion? Sie können eine Doppelmitgliedschaft beantragen und zahlen nur den Beitrag der Sektion Ticino.</p>
</div>
</section>

<section class="section--surface" aria-labelledby="vantaggi-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="vantaggi-h" class="h2">Ihre Vorteile</h2>
<div><a class="btn btn--primary" href="{join}">Auf der SAC-Website beitreten <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>"""
    return sezione_page("Adesione.html", "Mitglied werden | CAS Ticino",
                        "Werden Sie Mitglied der Sektion Ticino des Schweizer Alpen-Clubs: Jahresbeiträge für Einzelne, Familien und Jugendliche, und die Vorteile für Mitglieder.",
                        body, og="paesaggi/laghetto-alpino-2000")


# ------------------------------------------------------------------ ricerca

TIPI = {"news/": "Notizia", "capanne/": "Capanna", "CampoTencia.html": "Capanna", "Cristallina.html": "Capanna", "Adula.html": "Capanna",
        "Motterascio.html": "Capanna", "MonteBar.html": "Capanna", "BaitaDelLuca.html": "Capanna"}
FUORI_INDICE = {"News.html", "Cerca.html"}  # elenchi che ripetono il contenuto di altre pagine


def solo_testo(frammento):
    t = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", frammento, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html_unescape(t).replace("→", " ")).strip()


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
    voci = [voce_pagina(f, h) for f, h in pagine.items() if f not in FUORI_INDICE and not f.startswith("de/")]
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
            voci.append({"t": a["title"], "u": a.get("link") or "Foto.html", "k": "Foto e resoconto gita", "d": a.get("date", ""),
                         "dt": data_it(a["date"]) if a.get("date") else "", "x": " ".join(filter(None, [a.get("place"), a.get("text")]))[:3000]})
    return {"voci": voci}


def cerca_pagina():
    body = page_hero([("Cerca", None)], "Cerca", "Cerca tra pagine, notizie, capanne, documenti, annuari e foto delle gite.",
                     f"""<form class="cerca-form" id="cerca-form" role="search" action="Cerca.html" data-indice="{asset("data/cerca.json")}">
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
    return page("Cerca.html", "Cerca | CAS Ticino", "Cerca nel sito della Sezione Ticino del Club Alpino Svizzero.",
                body, scripts=f'<script src="{asset("assets/cerca.js")}" defer></script>\n')


PAGES = {
    "index.html": home,
    "Introduzione.html": introduzione, "Comitato.html": comitato, "Organizzazione.html": organizzazione,
    "Sede.html": sede, "Storia.html": storia, "Link.html": link, "Documenti.html": documenti,
    "News.html": news, "Foto.html": foto, "Annuari.html": annuari, "Informazione.html": informazione,
    "Adesione.html": adesione,
    "Giovani.html": giovani, "Senior.html": senior, "Corsi.html": corsi, "Noleggio.html": noleggio,
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


def in_tedesco(fn):
    """Genera una pagina con la lingua impostata a tedesco."""
    def genera():
        LINGUA["lang"] = "de"
        try:
            return fn()
        finally:
            LINGUA["lang"] = "it"
    return genera


PAGES_DE = {"index.html": home_de, "Introduzione.html": introduzione_de, "Comitato.html": comitato,
            "Organizzazione.html": organizzazione, "Sede.html": sede_de, "Storia.html": storia, "Link.html": link,
            "Adesione.html": adesione_de}
for _f in HUT_PAGES:
    PAGES_DE[_f] = (lambda f: lambda: hut(f))(_f)
for _f, _c in CONTENUTI_DE.items():
    for _p in _c["pagine"] + ([_c["storia"]] if _c.get("storia") else []):
        PAGES_DE[f"capanne/{_c['cartella']}/{_p['file']}.html"] = (lambda f, p: lambda: hut_page(f, p))(_f, _p)
    if _c.get("foto"):
        PAGES_DE[f"capanne/{_c['cartella']}/foto.html"] = (lambda f: lambda: hut_foto(f))(_f)
PAGINE_DE.update(PAGES_DE)  # per il selettore di lingua e per i link L()
for _f, _fn in PAGES_DE.items():
    PAGES["de/" + _f] = in_tedesco(_fn)

def scrivi(name, contenuto):
    os.makedirs(os.path.dirname(os.path.join(ROOT, name)), exist_ok=True)
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(contenuto)
    print("scritto", name)


if __name__ == "__main__":
    only = sys.argv[1:]
    # tutte le pagine vengono generate comunque: servono per l'indice della ricerca
    pagine = {name: fn() for name, fn in PAGES.items()}
    for name, contenuto in pagine.items():
        if not only or name in only:
            scrivi(name, contenuto)
    with open(os.path.join(ROOT, "data", "cerca.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(indice_ricerca(pagine), f, ensure_ascii=False, separators=(",", ":"))
    print("scritto data/cerca.json")
    if not only or "Cerca.html" in only:
        scrivi("Cerca.html", cerca_pagina())  # dopo l'indice: il link porta l'impronta di cerca.json
