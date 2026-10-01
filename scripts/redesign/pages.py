"""Nuovo design: genera tutte le pagine del sito.

Uso: python scripts/redesign/pages.py [Pagina.html ...]  (senza argomenti rigenera tutto)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shared import head, nav, footer, pic, img, GITE, page_hero, subnav, asset, in_sottocartella, crumbs
import json, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HUTS = [
    # file, nome, quota, valle, stato, testo, posti, accesso, img 3x2 (w,h), grande
    ("CampoTencia.html", "Campo Tencia", "2140", "Val Piumogna", "Custodita", "Su un terrazzo sopra la Val Piumogna, base per il Pizzo Campo Tencia: la cima più alta interamente ticinese.", "80 posti", "Dalpe 2h30", "capanna-campotencia-3x2", (987, 658), True),
    ("Cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Custodita", "Sull’omonimo passo, tra Leventina e Valle Maggia. Inaugurata nel 2003, primo rifugio moderno del CAS.", "120 posti", "Ossasco 3h45", "capanna-cristallina-3x2", (837, 558), True),
    ("Adula.html", "Adula", "2012", "Val Carassino", "Custodita", "Il classico rifugio in pietra affacciato sulla Valle di Blenio: storia, accoglienza calorosa e cucina nostrana.", "34 posti", "Compietto 2h", "capanna-adula-3x2", (1000, 667), False),
    ("Motterascio.html", "Motterascio", "2172", "Greina", "Custodita", "Al margine della riserva della Greina: torbiere, alpeggi e l’arco naturale più grande del Ticino.", "70 posti", "Luzzone 1h30", "capanna-motterascio-3x2", (974, 649), False),
    ("MonteBar.html", "Monte Bar", "1620", "Alta Capriasca", "Tutto l’anno", "Il balcone sul Luganese, ricostruito nel 2016: vista dal Monte Rosa ai Denti della Vecchia, standard Bike Hotel.", "42 posti", "Corticiasca 1h30", "capanna-montebar-3x2", (663, 442), False),
    ("BaitaDelLuca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Su riservazione", "Sopra Sonvico, ai piedi dei Denti della Vecchia. Punto di ritrovo dei giovani, ideale per famiglie e arrampicata.", "16 posti, autogestita", "Rosone 30 min", "capanna-baitadelluca-3x2", (1000, 667), False),
]

COURSES = [
    ("Inverno", "Sci alpinismo", "Salita e discesa fuori pista, nivologia, prevenzione valanghe, ricerca ARTVA.", "corso-scialpinismo-4x5", (582, 728), "Sci alpinisti in salita su un pendio innevato"),
    ("Inverno", "Racchette", "Muoversi sulla neve in sicurezza: meteo, orientamento, primi soccorsi.", "corso-racchette-4x5", (800, 1000), "Cresta innevata sopra un mare di nuvole"),
    ("Inverno", "Freeride", "Tecnica di sci fuori pista per chi vuole scendere con più sicurezza.", "corso-freeride-4x5", (594, 742), "Sciatori in discesa su un ghiacciaio"),
    ("Primavera", "Arrampicata", "Vie a uno o più tiri: assicurazione, gestione della sosta, corda doppia.", "corso-arrampicata-4x5", (594, 742), "Cordata su una parete di roccia accanto a un ghiacciaio"),
    ("Estate", "Alpinismo", "Progressione su neve e roccia per escursionisti che vogliono salire più in alto.", "corso-alpinismo-4x5", (594, 742), "Cordata su una cresta di neve"),
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
    courses = "\n".join(f"""<a class="course" href="Corsi.html">
<figure>{img(im, alt, w, h)}</figure>
<span class="label">{season}</span>
<h3 class="h3">{title}</h3>
<p>{text}</p>
</a>""" for season, title, text, im, (w, h), alt in COURSES)
    timeline = "\n".join(f'<li><span class="year">{y}</span><span>{t}</span></li>' for y, t in TIMELINE)

    html = head("CAS Ticino | Club Alpino Svizzero, Sezione Ticino",
                "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età. Da oltre un secolo, la casa dell’alpinismo ticinese.",
                '<meta property="og:image" content="assets/img/hero-ticino-2000.webp">\n<link rel="preload" as="image" href="assets/img/hero-ticino-2000.webp" imagesrcset="assets/img/hero-ticino-1000.webp 1000w, assets/img/hero-ticino-2000.webp 2000w" imagesizes="100vw" media="(min-width: 701px)">\n')
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
{pic("hero-ticino", "Alpinisti su una cresta rocciosa sopra il Lago di Lugano", mobile="hero-ticino-4x3", w=2000, h=580, lazy=False)}
</figure>
</section>

<section class="section section--tight" id="sezione" aria-label="La sezione in cifre">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>anno di fondazione</span></div>
<div class="stat"><strong>≈3000</strong><span>soci</span></div>
<div class="stat"><strong>6</strong><span>rifugi, 362 posti letto</span></div>
<div class="stat"><strong>5</strong><span>discipline insegnate nei corsi</span></div>
</div>
</div>
</section>

<section class="section section--tight" id="storia" aria-labelledby="storia-h">
<div class="container split">
<div class="split-intro">
<h2 id="storia-h" class="h2">Dal 1886,<br>a piedi.</h2>
<p class="lead">Fondato alla Birraria Gambrinus di Bellinzona nell’anno del centenario della prima salita al Monte Bianco, per «visitare, studiare e far conoscere» le montagne del Cantone.</p>
<div><a class="link" href="Storia.html">Leggi la storia completa</a></div>
</div>
<ol class="timeline" data-reveal>
{timeline}
</ol>
</div>
</section>

<section class="section--surface section--tight" id="news" aria-labelledby="news-h">
<div class="container">
<div class="section-row">
<h2 id="news-h" class="h2">Dalla sezione</h2>
<div class="links"><a class="link" href="News.html">Tutte le news</a><a class="link" href="Foto.html">Galleria foto</a></div>
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
{img("attivita-gite-2x1", "Gruppo in vetta con vista sulle Alpi innevate", 1400, 700)}
<div class="tile-body">
<span class="label">Programma gite 2026</span>
<h3 class="h2">Gite, escursioni e uscite della sezione</h3>
<p>Escursionismo, alpinismo, sci alpinismo, racchette e arrampicata: il calendario completo con iscrizioni online.</p>
<div class="actions"><a class="btn btn--primary" href="{GITE}">Programma gite</a><a class="btn btn--ghost-light" href="Foto.html">Galleria foto</a></div>
</div>
</article>
<article class="tile tile--tall" data-reveal>
{img("attivita-giovani-3x4", "Giovane arrampicatore su una parete dei Denti della Vecchia", 800, 1066)}
<div class="tile-body">
<span class="label">Gruppo giovani, dagli anni ’60</span>
<h3 class="h2">Giovani</h3>
<p>Arrampicata, escursioni e settimane in montagna con monitori della sezione. Il ritrovo è la Baita del Luca, ai piedi dei Denti della Vecchia.</p>
<div class="links"><a class="link" href="Giovani.html">Gruppo giovani</a><a class="link" href="Organizzazione.html">Organizzazione</a></div>
</div>
</article>
<article class="tile tile--wide-bottom" data-reveal>
{img("attivita-senior-2x1", "Escursionisti su un sentiero di cresta", 1000, 500)}
<div class="tile-body">
<span class="label">Gruppo senior, dal 1940</span>
<h3 class="h2">Senior</h3>
<p>Uscite settimanali con capigita esperti, al ritmo giusto e in buona compagnia, dalla Capriasca alle Alpi.</p>
<div class="links"><a class="link" href="Senior.html">Gruppo senior</a><a class="link" href="Documenti.html">Promemoria capigita</a></div>
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
<a class="link" href="Noleggio.html">Noleggio materiale</a>
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

<section class="cta-band" id="adesione" aria-labelledby="adesione-h">
{pic("adesione", "", mobile="adesione-4x3", w=2000, h=602)}
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

def page(file, title, description, body, og="hero-ticino-2000", section=None, scripts=""):
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
        name="Campo Tencia", where="Val Piumogna, Leventina", alt_m="2140", beds="80", custody="metà giu, metà ott",
        mail="campotencia@casticino.ch",
        description="Capanna Campo Tencia, 2140 m, in Val Piumogna (Leventina): 80 posti letto, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
        band=("capanna-campotencia", "La Capanna Campo Tencia al tramonto, sopra la Val Piumogna", 658),
        intro="Adagiata su un terrazzo che domina l’alta Val Piumogna, è la base ideale per escursioni, traversate verso altre capanne e salite come quella al Pizzo Campo Tencia, che con i suoi 3071 m è la cima più alta interamente in territorio ticinese.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da metà giugno a metà ottobre; d’inverno su richiesta"),
              ("Posti letto", "80"),
              ("Pasti", "Cucina calda, pasti serviti tutto il giorno dal guardiano"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Da Dalpe 2h30; da Rodi via Tremorgio e Leit 3h30"),
               ("Cartina", 'CNS 1272 Campo Tencia, coordinate <span class="num">699.430 / 144.480</span>')],
        contact=[("Guardiani", "Valeria Grandi e Paco Porcu"),
                 ("Telefono capanna", '<a class="num" href="tel:+41918671544">+41 91 867 15 44</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41766934994">+41 76 693 49 94</a>'),
                 ("E-mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "Cristallina.html": dict(
        name="Cristallina", where="Passo Cristallina, Valle Bedretto", alt_m="2575", beds="120", custody="fine giu, ott",
        mail="cristallina@casticino.ch",
        description="Capanna Cristallina, 2575 m, sul Passo Cristallina tra Leventina e Valle Maggia: 120 posti letto, custodita da fine giugno a ottobre. Contatti e prenotazioni.",
        band=("capanna-cristallina", "La Capanna Cristallina sul passo, tra Leventina e Valle Maggia", 558),
        intro="Progettata dagli architetti Baserga e Mozzetti e inaugurata nel 2003, è il primo rifugio moderno costruito dal Club Alpino Svizzero. Sorge sul passo, in un punto strategico tra Leventina e Valle Maggia: tappa panoramica sulle traversate verso Robiei, il Naret, il Campo Tencia e il San Giacomo. Il giro dei laghi del Cristallina, di uno o due giorni, è adatto anche alle famiglie; in un’ora si raggiungono il Cristallina e la Cima di Lago. D’inverno, raggiungibile soprattutto da nord, apre pendii splendidi verso la Valle Bedretto, Robiei e la Val Formazza.",
        stay=[("Apertura", "Da giugno a ottobre; d’inverno saltuariamente o su richiesta"),
              ("Custodia", "Da fine giugno a ottobre; inverno su prenotazione"),
              ("Posti letto", "120"),
              ("Pasti", "Preparati dal guardiano tutto il giorno"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Da Ossasco 3h45; da Robiei 2h30; dalla diga del Naret 2h30; dalla Capanna Basodino 3h"),
               ("Accesso invernale", "Da Ossasco 4h; cartine sci CNS 266S e 256S"),
               ("Cartina", 'CNS 1251 Bedretto, coordinate <span class="num">683.550 / 147.300</span>')],
        contact=[("Guardiano", "Emanuele Vellati"),
                 ("Telefono", '<a class="num" href="tel:+41918692330">+41 91 869 23 30</a>'),
                 ("E-mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "Adula.html": dict(
        name="Adula", where="Alta Val Carassino, Val Soi, Blenio", alt_m="2012", beds="34", custody="fine giu, fine set",
        mail="adula@casticino.ch",
        description="Capanna Adula, 2012 m, tra Val Carassino e Val Soi (Blenio): 34 posti letto, aperta tutto l’anno, custodita da fine giugno a fine settembre. Contatti e prenotazioni.",
        img=("capanna-adula-3x2", "La Capanna Adula, rifugio in pietra affacciato sulla Valle di Blenio", 1000, 667),
        intro="La «Bassa», come la si chiama da sempre, ha il fascino del rifugio d’altri tempi: costruzione in pietra, un soggiorno che trasuda storia, dormitori che hanno visto passare migliaia di alpinisti, accoglienza calorosa e cucina nostrana. Da questo balcone sulla Valle di Blenio si parte per la cima dell’Adula o, su comodi sentieri, verso altre capanne; i selvaggi itinerari della Val Carassino offrono un escursionismo avventuroso. Per i meno ambiziosi: una passeggiata in valle, un buon pranzo e un pisolino al sole.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Da fine giugno a fine settembre"),
              ("Posti letto", "34"),
              ("Pasti", "Pasti preparati dal guardiano; cucina autonoma solo d’inverno o d’accordo con il guardiano"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Da Dangio per la Val Soi 3h; dalla diga del Luzzone per la Val Carassino 3h; da Compietto 2h (40 min in MTB)"),
               ("Accesso invernale", "Da Dangio 5h; da Ghirone 5h"),
               ("Cartina", 'CNS 1253 Olivone, coordinate <span class="num">719.510 / 150.950</span>')],
        contact=[("Guardiano", "Raffaele «Lele» Demaldi"),
                 ("Telefono capanna", '<a class="num" href="tel:+41918721532">+41 91 872 15 32</a>'),
                 ("Cellulare", '<a class="num" href="tel:+41795352112">+41 79 535 21 12</a>'),
                 ("E-mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "Motterascio.html": dict(
        name="Motterascio", where="Alpe Motterascio, Greina, Blenio", alt_m="2172", beds="70", custody="10 giu, 15 ott",
        mail="motterascio@casticino.ch",
        description="Capanna Motterascio, 2172 m, al margine della Greina (Blenio): 70 posti letto, aperta tutto l’anno, custodita dal 10 giugno al 15 ottobre. Contatti e prenotazioni.",
        band=("capanna-motterascio", "La Capanna Motterascio sull’altopiano della Greina", 649),
        intro="Capanna nuova, al margine di una riserva naturale straordinaria: la Greina, con le sue paludi, torbiere, alpeggi e una flora incontaminata. Punto di partenza per itinerari interessanti, tra cui spicca l’arco della Greina, il più grande arco naturale del Canton Ticino.",
        stay=[("Apertura", "Tutto l’anno"),
              ("Custodia", "Dal 10 giugno al 15 ottobre; d’inverno nel periodo pasquale o su richiesta"),
              ("Posti letto", "70"),
              ("Pasti", "Pasti caldi preparati dai guardiani tutto il giorno"),
              ("Bibite", "Disponibili anche in assenza del guardiano")],
        reach=[("Accesso estivo", "Dal Lago di Luzzone (Garzott) 1h30; da Ghirone per la Val Camadra 5h"),
               ("Accesso invernale", "Da Ghirone solo passando dalla Capanna Scaletta-Greina, 5-6h"),
               ("Cartina", 'CNS 1233 Greina, coordinate <span class="num">720.075 / 161.425</span>')],
        contact=[("Guardiano", "Fabio Merzaghi"),
                 ("Prenotazioni", '<a class="num" href="tel:+41918721622">+41 91 872 16 22</a> (dal 10 giugno al 15 ottobre)'),
                 ("Cellulare", '<a class="num" href="tel:+41797276905">+41 79 727 69 05</a>'),
                 ("E-mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "MonteBar.html": dict(
        name="Monte Bar", where="Alta Capriasca, Luganese", alt_m="1620", beds="42", custody="tutto l’anno",
        mail="montebar@casticino.ch",
        description="Capanna Monte Bar, 1620 m, in Alta Capriasca: 42 posti letto in camere da 2, 4 e 6, custodita tutto l’anno, standard Bike Hotel. Contatti e prenotazioni.",
        band=("capanna-montebar", "La Capanna Monte Bar con vista sul Luganese", 442),
        intro="Su un poggio di eccezionale bellezza, con una vista a 180 gradi dai Denti della Vecchia al Tamaro e, a ovest, sui 4000 vallesani dal Mischabel al Monte Rosa. Ricostruita nell’autunno 2016: camere da 2, 4 e 6 posti, servizi ai piani, refettorio per circa 80 persone, saletta riunioni per 20, ampia terrazza e un locale chiuso con caricatori per e-bike e piccola officina, secondo lo standard Bike Hotel.",
        stay=[("Apertura", "In presenza dei custodi e su riservazione; apre anche per eventi, cene e pranzi fuori stagione"),
              ("Custodia", "Da aprile a ottobre sempre; da novembre a marzo dal giovedì alla domenica"),
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
    "BaitaDelLuca.html": dict(
        name="Baita del Luca", where="Cioascio, Sonvico", alt_m="1070", beds="16", custody="su riservazione",
        mail="baitaluca@casticino.ch",
        description="Baita del Luca, 1070 m, sopra Sonvico ai piedi dei Denti della Vecchia: 16 posti letto, autogestita, solo su riservazione. Ritrovo del gruppo giovani.",
        img=("capanna-baitadelluca-3x2", "La Baita del Luca su un pendio erboso sopra Sonvico", 1000, 667),
        intro="Su un ampio pendio erboso sopra Sonvico, ai piedi dei Denti della Vecchia: base ideale per escursioni, anche in famiglia, e arrampicate in un paesaggio unico. È il punto di ritrovo del <a href=\"Giovani.html\">gruppo giovani</a>.",
        stay=[("Apertura", "Chiusa; accessibile solo previa riservazione"),
              ("Posti letto", "16"),
              ("Pasti", "Possibilità di cucinare"),
              ("Bibite", "Disponibili anche in assenza del guardiano"),
              ("Prenotazioni", "Il codice d’accesso viene dato dopo il versamento anticipato")],
        reach=[("Accesso estivo", "Da Rosone 30 min; da Lovarescia (sopra Sonvico) 60 min; da Car e da Luss (Villa Luganese) 60 min"),
               ("Cartina", 'CNS 1333 Tesserete, coordinate <span class="num">722.980 / 102.600</span>')],
        contact=[("Responsabile", "Priska Deluigi, 6960 Odogno"),
                 ("Cellulare", '<a class="num" href="tel:+41792033084">079 203 30 84</a>'),
                 ("E-mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Prenotazioni", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}


def hut(file):
    d = HUT_PAGES[file]
    others = [h for h in HUTS if h[0] != file]
    mini = "\n".join(f"""<a class="mini-hut" href="{f}"><figure>{img(im, f'Capanna {n}', w, h)}</figure><strong>{n}</strong><span>{q} m</span></a>"""
                     for f, n, q, v, st, t, posti, acc, im, (w, h), big in others)
    if "band" in d:
        base, alt, h = d["band"]
        band = f'<figure class="band">\n{pic(base, alt, mobile=base + "-4x3", w=2000, h=h, lazy=False)}\n</figure>'
        og = base + "-2000"
    else:
        name, alt, w, h = d["img"]
        band = band_img(name, alt, w, h)
        og = name
    custody_dt = "Custodia" if d["custody"] != "su riservazione" else "Apertura"
    extra = f"""<div class="keyfacts">
<dl>
<div><dt>Altitudine</dt><dd class="num">{d['alt_m']} m</dd></div>
<div><dt>Posti letto</dt><dd class="num">{d['beds']}</dd></div>
<div><dt>{custody_dt}</dt><dd>{d['custody']}</dd></div>
</dl>
<a class="btn btn--primary" href="mailto:{d['mail']}">Prenota <span class="arrow" aria-hidden="true">→</span></a>
</div>"""
    body = page_hero([("Le capanne", "index.html#capanne"), (d["name"], None)], d["name"], d["where"], extra) + f"""

{band}

<section class="section" aria-labelledby="capanna-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="capanna-h" class="h2">La capanna</h2>
<p>{d['intro']}</p>
</div>
<div class="factgroups" data-reveal>
<div class="factgroup">
<h3 class="h3">Soggiorno</h3>
{facts(d['stay'])}
</div>
<div class="factgroup">
<h3 class="h3">Arrivare</h3>
{facts(d['reach'])}
</div>
</div>
</div>
</section>

<section class="section" aria-labelledby="contatti-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="contatti-h" class="h2">Senti il guardiano prima di partire</h2>
<p>Verifica sempre la presenza del guardiano e le condizioni della montagna.</p>
</div>
{facts(d['contact'])}
</div>
</div>
</section>

<section class="section" aria-labelledby="altre-h">
<div class="container">
<div class="section-head"><h2 id="altre-h" class="h3">Le altre capanne</h2></div>
<div class="mini-huts">
{mini}
</div>
</div>
</section>"""
    prefix = "Capanna " if file != "BaitaDelLuca.html" else ""
    return page(file, f"{prefix}{d['name']} | CAS Ticino", d["description"], body, og=og)


# ------------------------------------------------------------------ la sezione

def introduzione():
    huts = ('<a href="CampoTencia.html">Campo Tencia</a>, <a href="Cristallina.html">Cristallina</a>, <a href="Adula.html">Adula</a>, '
            '<a href="Motterascio.html">Motterascio (Michela)</a>, <a href="MonteBar.html">Monte Bar</a> e <a href="BaitaDelLuca.html">Baita del Luca</a>')
    body = page_hero([("La Sezione", "index.html#sezione"), ("Introduzione", None)], "La sezione",
                     "Fondata a Bellinzona l’11 aprile 1886, la Sezione Ticino del Club Alpino Svizzero conta quasi 3000 soci e propone un’attività varia, pensata per tutte le età: dai più giovani ai seniori.") + f"""

{band_img("attivita-gite-2x1", "Gruppo della sezione in vetta, con vista sulle Alpi innevate", 1400, 700)}

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
{img("hero-ticino-2000", "Alpinisti su una cresta rocciosa", 2000, 580)}
<h3>Discipline</h3>
<p>Escursionismo, alpinismo, arrampicata, sci alpinismo, racchette e cascate di ghiaccio.</p>
</article>
<article class="pillar pillar--accent">
<h3>Per chi inizia</h3>
<p>Corsi di introduzione ad alpinismo, sci alpinismo, racchette e arrampicata in ambiente.</p>
<a class="link" href="Corsi.html">Vedi i corsi</a>
</article>
<article class="pillar pillar--photo">
{img("capanna-montebar-3x2", "La Capanna Monte Bar", 663, 442)}
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
{img("corso-racchette-4x5", "Cresta innevata sopra un mare di nuvole", 800, 1000)}
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
                body, og="attivita-gite-2x1")


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


def comitato():
    people = []
    for role, name, mail, photo in COMITATO:
        ph = (f'<img src="assets/comitato/{photo}.webp" alt="Ritratto di {name}" width="96" height="112" loading="lazy">'
              if photo else f'<span aria-hidden="true">{initials(name)}</span>')
        people.append(f"""<article class="person">
<div class="person-photo">{ph}</div>
<div class="person-body">
<span class="role">{role}</span>
<h2>{name}</h2>
<a href="mailto:{mail}">{mail}</a>
</div>
</article>""")
    body = page_hero([("La Sezione", "index.html#sezione"), ("Comitato", None)], "Il comitato",
                     "Otto persone, ognuna con un ambito preciso, che guidano la sezione insieme ai <a href=\"Organizzazione.html\">dicasteri</a> e ai volontari.") + f"""

<section class="section" aria-label="Membri del comitato">
<div class="container">
<div class="people" data-reveal>
{chr(10).join(people)}
</div>
</div>
</section>

{subnav("La Sezione", "Comitato.html")}"""
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


def organizzazione():
    depts = []
    for i, (title, text, members) in enumerate(DICASTERI, 1):
        ms = []
        for name, role, mail in members:
            if name is None:
                ms.append(f'<div class="member member--tbd"><strong>Da definire</strong><span>{role}</span></div>')
            else:
                m = f'<a href="mailto:{mail}">{mail}</a>' if mail else ""
                ms.append(f'<div class="member"><strong>{name}</strong><span>{role}</span>{m}</div>')
        depts.append(f"""<article class="dept" aria-labelledby="d{i}-h" data-reveal>
<div class="dept-intro">
<span class="dept-count">{len(members)} membri</span>
<h2 id="d{i}-h" class="h2">{title}</h2>
<p>{text}</p>
</div>
<div class="members">
{chr(10).join(ms)}
</div>
</article>""")
    body = page_hero([("La Sezione", "index.html#sezione"), ("Organizzazione", None)], "Organizzazione",
                     'Il <a href="Comitato.html">comitato</a> si appoggia a cinque dicasteri, ognuno responsabile di un ambito della vita della sezione.') + f"""

<section class="section" aria-label="Dicasteri">
<div class="container">
{chr(10).join(depts)}
</div>
</section>

{subnav("La Sezione", "Organizzazione.html")}"""
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


def storia():
    tl = "\n".join(f'<li><span class="year">{y}</span><span>{t}</span></li>' for y, t in STORIA)
    body = page_hero([("La Sezione", "index.html#sezione"), ("Storia", None)], "Dal 1886,<br>a piedi.",
                     "Più di un secolo di salite, rifugi, soccorso e cultura alpina: la storia della sezione in tappe.") + f"""

<section class="section" aria-labelledby="tappe-h">
<div class="container split">
<div class="split-intro">
<h2 id="tappe-h" class="h2">Le tappe</h2>
<p class="lead">Accanto all’attività sul terreno, la sezione ha sempre organizzato proiezioni, conferenze e dibattiti, e documentato la propria vita in numerose pubblicazioni e negli annuari.</p>
</div>
<ol class="timeline" data-reveal>
{tl}
</ol>
</div>
</section>

{subnav("La Sezione", "Storia.html")}"""
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


def link():
    body = page_hero([("La Sezione", "index.html#sezione"), ("Link utili", None)], "Link utili",
                     "Meteo, bollettini valanghe, condizioni, cartine e le altre realtà alpinistiche del territorio.") + f"""

<section class="section" aria-label="Link">
<div class="container">
{linkgroups(LINKS, "↗")}
</div>
</section>

{subnav("La Sezione", "Link.html")}"""
    return page("Link.html", "Link utili | CAS Ticino",
                "Link utili per la montagna: meteo e bollettini valanghe, condizioni, cartine, società alpinistiche ticinesi, formazione e soccorso.",
                body)


DOC = "docs/"  # PDF della sezione, in sottocartelle per tema (nomi in minuscolo, con trattini)
DOCS = [
    ("La sezione", [("Statuto", DOC + "statuto-visione/statuto-2025.pdf"),
                    ("Visione e strategia", DOC + "statuto-visione/visione-strategia-2025.pdf"),
                    ("Organigramma", DOC + "statuto-visione/organigramma-2025.pdf")]),
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
                    ("Promemoria capigita", DOC + "promemoria/capigita.pdf")]),
    ("Materiale e pianificazione", [("Lista noleggio materiale", DOC + "noleggio/lista-materiale.pdf"),
                                    ("Formulario pianificazione gite estive", DOC + "moduli/pianificazione-gite-estive.pdf"),
                                    ("Cartine CH 1:25 000", DOC + "cartine/carte-nazionali-25000.pdf"),
                                    ("Cartine CH 1:50 000", DOC + "cartine/carte-nazionali-50000.pdf"),
                                    ("Cartine CH 1:50 000 sci", DOC + "cartine/carte-nazionali-50000-sci.pdf")]),
]


def documenti():
    body = page_hero([("Media", "Foto.html"), ("Documenti", None)], "Documenti",
                     "Statuto e documenti della sezione, scale di difficoltà, promemoria tecnici, moduli e cartine da scaricare.") + f"""

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
                "Documenti del CAS Ticino da scaricare: scale di difficoltà, promemoria tecnici, promemoria capigita, lista del materiale e cartine.",
                body)


# ------------------------------------------------------------------ news, foto, adesione

NEWS = json.load(open(os.path.join(ROOT, "data", "news.json"), encoding="utf-8"))["news"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto",
        "settembre", "ottobre", "novembre", "dicembre"]


def data_it(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{d} {MESI[m - 1]} {y}"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def og_name(n):
    """Nome dell'immagine per og:image (page() aggiunge assets/img/ e .webp)."""
    return n["image"]["src"][len("assets/img/"):-len(".webp")] if n["image"] else "hero-ticino-2000"


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
                body, og=og_name(NEWS[0]))


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
    return in_sottocartella(page(n["file"], f"{esc(n['title'])} | CAS Ticino", esc(n["excerpt"][:155]), body,
                                 og=og_name(n), section="News"))


def foto():
    body = page_hero([("Media", "Foto.html"), ("Foto", None)], "Foto", "Gli scatti delle ultime gite della sezione, pubblicati dai capigita sul portale Droptour.") + f"""

<section class="section" aria-label="Ultime gite">
<div class="container">
<div class="albums-head">
<p class="small">Ultime gite pubblicate, dal portale Droptour</p>
<a class="link" href="{GITE}?page=galery_overview">Archivio completo su Droptour</a>
</div>
<div id="albums" aria-live="polite"><p class="albums-status">Caricamento delle foto…</p></div>
<div class="albums-more">
<button type="button" class="btn btn--secondary" id="load-more" hidden>Carica altre gite</button>
</div>
</div>
</section>

{subnav("Media", "Foto.html")}"""
    return page("Foto.html", "Foto delle gite | CAS Ticino",
                "Le foto delle ultime gite della Sezione Ticino del Club Alpino Svizzero, con i resoconti dei capigita.",
                body, og="attivita-gite-2x1", scripts=f'<script src="{asset("assets/foto.js")}" defer></script>\n')


def webp_size(path):
    """Larghezza e altezza di un file WebP, leggendo l'intestazione (senza librerie esterne)."""
    with open(path, "rb") as f:
        d = f.read(30)
    kind = d[12:16]
    if kind == b"VP8 ":
        return int.from_bytes(d[26:28], "little") & 0x3FFF, int.from_bytes(d[28:30], "little") & 0x3FFF
    if kind == b"VP8L":
        v = int.from_bytes(d[21:25], "little")
        return (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
    return int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1


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


def annuari():
    items = pubblicazioni("annuari", "annuario")
    ultimo, altri = items[0], items[1:]
    body = page_hero([("Media", "Foto.html"), ("Annuari", None)], "Annuari",
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
    body = page_hero([("Media", "Foto.html"), ("Informazione", None)], "Informazione",
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
{pic("adesione", "Alpinisti in cammino su un crinale", mobile="adesione-4x3", w=2000, h=602, lazy=False)}
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
                body, og="adesione-2000")


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
            ("Cassiere", 'Nicola Martinoni, <a class="num" href="tel:+41794391691">+41 79 439 16 91</a>'),
            ("Spider", "Giosiana Codoni"),
            ("Ritrovo", '<a href="BaitaDelLuca.html">Baita del Luca</a>, ai piedi dei Denti della Vecchia')]
    body = page_hero([("Attività", "index.html#attivita"), ("Giovani", None)], "Giovani",
                     "Uscite di un giorno, fine settimana e campi di più giorni: alpinismo, arrampicata, sci alpinismo e molto altro, con monitori formati e guide alpine.",
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{GITE}">Programma giovani <span class="arrow" aria-hidden="true">→</span></a></div>',
                     figure=img("attivita-giovani-3x4", "Giovane arrampicatore su una parete dei Denti della Vecchia", 800, 1066, lazy=False)) + f"""

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
<div><a class="link" href="{GITE}">Programma giovani su Droptour</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "Giovani.html")}"""
    return page("Giovani.html", "Giovani | CAS Ticino",
                "Il gruppo giovani del CAS Ticino: arrampicata, sci alpinismo, campi e uscite per ragazze e ragazzi dai 2 ai 22 anni, con monitori e guide alpine.",
                body, og="attivita-giovani-3x4")


def senior():
    rows = [("Chi può partecipare", 'Dai 60 anni, con l’affiliazione al CAS Ticino. Non c’è una tassa aggiuntiva, e tutti i soci della sezione possono partecipare alle attività. <a href="Adesione.html">Diventa socio</a>'),
            ("Come aderire", 'Scrivi a <a href="mailto:segretariato.seniori@casticino.ch">segretariato.seniori@casticino.ch</a> con nome, data di nascita, numero di socio CAS, indirizzo, telefono ed e-mail.'),
            ("Uscite", "Di norma il giovedì. Il calendario aggiornato è sul programma gite online."),
            ("Pranzi", 'Il secondo e il quarto mercoledì del mese al Bistrot Vecchio Torchio di Viganello. Iscrizioni entro il lunedì presso Hanni Vanossi (<a class="num" href="tel:+41763973390">076 397 33 90</a>) o direttamente al ristorante (<a class="num" href="tel:+41919721010">091 972 10 10</a>).'),
            ("Capigita", 'Il dicastero cerca sempre nuovi capigita. <a href="Documenti.html">Promemoria capigita</a>')]
    body = page_hero([("Attività", "index.html#attivita"), ("Senior", None)], "Senior",
                     "Un gruppo di non più giovani con la passione per la montagna: la bellezza della natura, i piaceri della tavola e la nostra storia.") + f"""

{band_img("attivita-senior-2x1", "Escursionisti del gruppo senior su un sentiero di cresta", 1000, 500)}

<section class="section" aria-labelledby="gruppo-h">
<div class="container detail">
<div class="detail-intro split-intro">
<span class="label">Il gruppo, dal 1940</span>
<h2 id="gruppo-h" class="h2">Ogni giovedì<br>in cammino</h2>
<p>Escursioni, gite di più giorni, mountain bike e racchette, con percorsi adatti a diversi livelli di allenamento.</p>
<div><a class="btn btn--primary" href="{GITE}">Programma senior <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav("Attività", "Senior.html")}"""
    return page("Senior.html", "Senior | CAS Ticino",
                "Il gruppo senior del CAS Ticino, dal 1940: escursioni il giovedì, gite di più giorni, mountain bike e racchette per soci dai 60 anni.",
                body, og="attivita-senior-2x1")


CORSI = [
    ("Inverno", "Sci alpinismo", "corso-scialpinismo-4x5", (582, 728), "Sci alpinisti in salita su un pendio innevato",
     "Per muoversi in sicurezza e in autonomia nelle gite della sezione: salita con le pelli su pendii ripidi, discesa fuori pista, uso del materiale di sicurezza, valutazione del pericolo valanghe e pianificazione.",
     GITE + "?page=detail&amp;touren_nummer=2096",
     [("Struttura", "Tre fine settimana più una giornata di prova per valutare forma e tecnica. Sabato istruzione, domenica applicazione con salita in vetta."),
      ("Requisiti", "Sciare bene su piste nere e reggere 4-5 ore di salita con 1200 m di dislivello. Età minima 16 anni; presenza obbligatoria a tutte le uscite."),
      ("Partecipanti", "Al massimo 30, con precedenza ai principianti e in ordine d’iscrizione. ARTVA, pala e sonda prestati gratuitamente su richiesta."),
      ("Programma", f'<a href="{DOC}corsi/sci-alpinismo-base-2027.pdf">Programma 2027 (PDF)</a>')]),
    ("Inverno", "Racchette", "corso-racchette-4x5", (800, 1000), "Cresta innevata sopra un mare di nuvole",
     "Introduzione all’escursionismo con le racchette, tra teoria e pratica: riconoscere i segnali di pericolo, valutare il rischio valanghe e il terreno, pianificare con gli strumenti disponibili, ricerca dei sepolti e primo soccorso.",
     GITE,
     [("Struttura", "Sei giornate: una serata di teoria sulla nivologia, una giornata dedicata alla sicurezza e due fine settimana di pratica."),
      ("Materiale", 'Obiettivi del corso, lista del materiale, regolamento gite e programma 2027 in PDF. <span class="small">In preparazione.</span>')]),
    ("Inverno", "Tecnica di sci fuori pista", "corso-freeride-4x5", (594, 742), "Sciatori in discesa su un ghiacciaio",
     "Per chi fatica a scendere su pendii non preparati: trucchi e consigli per affrontare la neve fuori dalle piste battute. Adatto ai soci che vogliono migliorare, a chi si avvicina allo sci alpinismo e agli sciatori esperti in cerca di strategie per le condizioni difficili.",
     GITE + "?page=detail&amp;touren_nummer=2167",
     [("Date", "Seguono informazioni."),
      ("Materiale", 'Attrezzatura da fuori pista completa; lista dettagliata nella scheda del corso. <span class="small">PDF in preparazione.</span>')]),
    ("Primavera", "Arrampicata", "corso-arrampicata-4x5", (594, 742), "Cordata su una parete di roccia accanto a un ghiacciaio",
     "Per principianti che vogliono avvicinarsi all’arrampicata in ambiente e per chi vuole consolidare la tecnica: sicurezza, manovre di corda, progressione su vie di più tiri. Dopo le basi, sempre più autonomia sotto la supervisione di un istruttore di arrampicata.",
     GITE,
     [("Obiettivo", "Praticare in sicurezza e in autonomia l’arrampicata sportiva su vie di uno o più tiri."),
      ("Materiale", 'Programma, lista del materiale e regolamento gite in PDF. <span class="small">In preparazione.</span>')]),
    ("Estate", "Alpinismo", "corso-alpinismo-4x5", (594, 742), "Cordata su una cresta di neve",
     "Il ponte tra escursionismo e alpinismo: legarsi correttamente su ghiacciaio e in cresta, tecniche di assicurazione, uso della corda in arrampicata e dei diversi attrezzi di progressione. Teoria e pratica, con lettura della carta, pianificazione, primo soccorso e salite in vetta su roccia e ghiaccio.",
     GITE,
     [("Struttura", "Tre uscite: la prima di solito in una capanna della sezione, le altre due vicino a un ghiacciaio adatto all’istruzione su roccia e ghiaccio. Nell’ultima si applicano le tecniche sotto la supervisione degli istruttori."),
      ("Programma", 'Programma 2027, obiettivi, lista del materiale e regolamento gite in PDF. <span class="small">In preparazione.</span>')]),
]


def corsi():
    rows = "\n".join(f"""<article class="course-row" id="corso-{i}" aria-labelledby="corso-{i}-h" data-reveal>
<figure>{img(im, alt, w, h)}</figure>
<div class="course-text">
<span class="label">{season}</span>
<h2 id="corso-{i}-h" class="h2">{title}</h2>
<p>{text}</p>
<a class="btn btn--primary" href="{href}">Iscriviti <span class="arrow" aria-hidden="true">→</span></a>
</div>
{facts(fs)}
</article>""" for i, (season, title, im, (w, h), alt, text, href, fs) in enumerate(CORSI, 1))
    body = page_hero([("Attività", "index.html#attivita"), ("Corsi", None)], "Corsi",
                     "Corsi nei fine settimana, diretti da professionisti della montagna con monitori esperti: le basi per partecipare in sicurezza alle attività della sezione. Il programma dell’anno successivo esce entro novembre.") + f"""

<section class="section" aria-label="Corsi base">
<div class="container">
{rows}
</div>
</section>

<section class="section" aria-labelledby="avanzati-h">
<div class="container">
<div class="callout">
<p><strong id="avanzati-h">Verso capogita e monitore G+S.</strong> Per chi vuole approfondire o prepararsi ai corsi capogita CAS e monitore Gioventù+Sport, la sezione propone corsi avanzati nelle tre discipline e serate di formazione teorica con specialisti.</p>
<a class="btn btn--secondary" href="Noleggio.html">Noleggio materiale</a>
</div>
</div>
</section>

{subnav("Attività", "Corsi.html")}"""
    return page("Corsi.html", "Corsi | CAS Ticino",
                "Corsi del CAS Ticino diretti da professionisti: sci alpinismo, racchette, tecnica di sci fuori pista, arrampicata e alpinismo.",
                body, og="corso-scialpinismo-4x5")


def noleggio():
    rows = [("Come funziona", "Compila il formulario con i dati dell’attività e il materiale che ti serve. Con la conferma ricevi il codice d’accesso e le istruzioni per il ritiro. Si paga in contanti alla riconsegna."),
            ("Richiesta", "Una settimana prima dell’attività"),
            ("Ritiro", 'Dal mercoledì alle <span class="num">19:00</span>'),
            ("Riconsegna", "Entro il martedì sera"),
            ("Magazzino", "Manno"),
            ("Responsabile", 'Michele Foletti, <a class="num" href="tel:+41792416955">079 241 69 55</a> (anche WhatsApp), <a href="mailto:fole89@gmail.com">fole89@gmail.com</a>')]
    body = page_hero([("Attività", "index.html#attivita"), ("Noleggio materiale", None)], "Noleggio<br>materiale",
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
    return page("Noleggio.html", "Noleggio materiale | CAS Ticino",
                "Noleggio materiale del CAS Ticino: alpinismo, sci alpinismo, arrampicata, racchette e altro, con ritiro al magazzino di Manno.",
                body)


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
for _i, _n in enumerate(NEWS):
    PAGES[_n["file"]] = (lambda i: lambda: news_article(i))(_i)

if __name__ == "__main__":
    only = sys.argv[1:]
    for name, fn in PAGES.items():
        if only and name not in only:
            continue
        os.makedirs(os.path.dirname(os.path.join(ROOT, name)), exist_ok=True)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(fn())
        print("scritto", name)
