"""Prototipo del nuovo design: home e Campo Tencia."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from shared import head, nav, footer, pic, img, GITE

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

<section class="section" id="sezione" aria-label="La sezione in cifre">
<div class="container">
<div class="stats" data-reveal>
<div class="stat"><strong>1886</strong><span>anno di fondazione</span></div>
<div class="stat"><strong>≈3000</strong><span>soci</span></div>
<div class="stat"><strong>6</strong><span>rifugi, 362 posti letto</span></div>
<div class="stat"><strong>5</strong><span>discipline insegnate nei corsi</span></div>
</div>
</div>
</section>

<section class="section" id="storia" aria-labelledby="storia-h">
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

<section class="section--surface" id="news" aria-labelledby="news-h">
<div class="container news">
<div class="split-intro">
<h2 id="news-h" class="h2">Dalla sezione</h2>
<div class="links"><a class="link" href="News.html">Tutte le news</a><a class="link" href="Foto.html">Galleria foto</a></div>
</div>
<div class="news-list" data-reveal>
<article class="news-item">
<div class="news-date"><strong class="num">15</strong><span>ott 2026</span></div>
<div class="news-body"><span class="label">Serata, ingresso gratuito</span><h3 class="h3">(S)legati</h3><p>L’incredibile storia degli alpinisti Joe Simpson e Simon Yates.</p><a class="link" href="News.html">Dettagli</a></div>
</article>
<article class="news-item">
<div class="news-date"><strong>FTL</strong><span>Locarno</span></div>
<div class="news-body"><span class="label">Festival</span><h3 class="h3">Film Trail Locarno</h3><p>Cinema, avventura, conversazioni.</p><a class="link" href="News.html">Dettagli</a></div>
</article>
<article class="news-item">
<div class="news-date"><strong class="news-word">Avviso</strong><span>Produttore</span></div>
<div class="news-body"><span class="label">Sicurezza materiale</span><h3 class="h3">Richiamo rinvii Simond Alpinism / Vertika</h3><p>Verifica se i tuoi quickdraws rientrano nel richiamo del produttore.</p><a class="link" href="News.html">Dettagli</a></div>
</article>
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


def campotencia():
    others = [h for h in HUTS if h[0] != "CampoTencia.html"]
    mini = "\n".join(f"""<a class="mini-hut" href="{f}"><figure>{img(im, f'Capanna {n}', w, h)}</figure><strong>{n}</strong><span>{q} m</span></a>"""
                     for f, n, q, v, st, t, posti, acc, im, (w, h), big in others)
    html = head("Capanna Campo Tencia | CAS Ticino",
                "Capanna Campo Tencia, 2140 m, in Val Piumogna (Leventina): 80 posti letto, custodita da metà giugno a metà ottobre. Contatti e prenotazioni.",
                '<meta property="og:image" content="assets/img/capanna-campotencia-2000.webp">\n')
    html += "\n<body>\n" + nav("CampoTencia.html") + f"""
<main id="contenuto">

<section class="page-hero" aria-labelledby="page-h">
<div class="container">
<nav class="crumbs" aria-label="Percorso"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="index.html#capanne">Le capanne</a><span aria-hidden="true">/</span><span aria-current="page">Campo Tencia</span></nav>
<h1 id="page-h" class="display fit">Campo Tencia</h1>
<p class="lead">Val Piumogna, Leventina</p>
<div class="keyfacts">
<dl>
<div><dt>Altitudine</dt><dd class="num">2140 m</dd></div>
<div><dt>Posti letto</dt><dd class="num">80</dd></div>
<div><dt>Custodia</dt><dd>metà giu, metà ott</dd></div>
</dl>
<a class="btn btn--primary" href="mailto:campotencia@casticino.ch">Prenota <span class="arrow" aria-hidden="true">→</span></a>
</div>
</div>
</section>

<figure class="band">
{pic("capanna-campotencia", "La Capanna Campo Tencia al tramonto, sopra la Val Piumogna", mobile="capanna-campotencia-4x3", w=2000, h=658, lazy=False)}
</figure>

<section class="section" aria-labelledby="capanna-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="capanna-h" class="h2">La capanna</h2>
<p>Adagiata su un terrazzo che domina l’alta Val Piumogna, è la base ideale per escursioni, traversate verso altre capanne e salite come quella al Pizzo Campo Tencia, che con i suoi 3071 m è la cima più alta interamente in territorio ticinese.</p>
</div>
<div class="factgroups" data-reveal>
<div class="factgroup">
<h3 class="h3">Soggiorno</h3>
<dl class="facts">
<dt>Apertura</dt><dd>Tutto l’anno</dd>
<dt>Custodia</dt><dd>Da metà giugno a metà ottobre; d’inverno su richiesta</dd>
<dt>Posti letto</dt><dd>80</dd>
<dt>Pasti</dt><dd>Cucina calda, pasti serviti tutto il giorno dal guardiano</dd>
<dt>Bibite</dt><dd>Disponibili anche in assenza del guardiano</dd>
</dl>
</div>
<div class="factgroup">
<h3 class="h3">Arrivare</h3>
<dl class="facts">
<dt>Accesso estivo</dt><dd>Da Dalpe 2h30; da Rodi via Tremorgio e Leit 3h30</dd>
<dt>Cartina</dt><dd>CNS 1272 Campo Tencia, coordinate <span class="num">699.430 / 144.480</span></dd>
</dl>
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
<dl class="facts">
<dt>Guardiani</dt><dd>Valeria Grandi e Paco Porcu</dd>
<dt>Telefono capanna</dt><dd><a class="num" href="tel:+41918671544">+41 91 867 15 44</a></dd>
<dt>Cellulare</dt><dd><a class="num" href="tel:+41766934994">+41 76 693 49 94</a></dd>
<dt>E-mail</dt><dd><a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a></dd>
</dl>
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
</section>

</main>
""" + footer()
    return html


for name, fn in (("index.html", home), ("CampoTencia.html", campotencia)):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as f:
        f.write(fn())
    print("scritto", name)
