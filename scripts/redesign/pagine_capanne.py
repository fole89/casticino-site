"""Capanne: schede della home (HUTS), dati delle pagine (HUT_PAGES), testi fissi (TC, tc()), pagina della capanna (hut())
e sottopagine (attività, storia, foto). I contenuti sono in capanne.py, capanne_de.py, capanne_en.py e data/testi/capanne/."""
from capanne import CONTENUTI, PRENOTA
from capanne_de import CONTENUTI_DE, HUT_DE
from capanne_en import CONTENUTI_EN, HUT_EN
from shared import avviso, avviso_testo
from comune import *


HUTS = [
    # file, nome, quota, valle, stato, testo, posti, accesso, img 3x2 (w,h), grande
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Custodita giu–ott", "Su un terrazzo sopra la Val Piumogna, base per il Pizzo Campo Tencia: la cima più alta interamente ticinese.", "80 posti", "Dalpe 3h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Custodita estate e inverno", "Sull’omonimo passo, tra Leventina e Valle Maggia. Inaugurata nel 2003, primo rifugio moderno del CAS.", "100 posti", "Ossasco 3h30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Custodita mag–ott", "Il classico rifugio in pietra affacciato sulla Valle di Blenio: storia, accoglienza calorosa e cucina nostrana.", "24 posti", "Compietto 2h40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Custodita giu–ott", "Al margine della riserva della Greina: torbiere, alpeggi e l’arco naturale più grande del Ticino.", "70 posti", "Garzott 2h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "Tutto l’anno", "Il balcone sul Luganese, ricostruito nel 2016: vista dal Monte Rosa ai Denti della Vecchia, standard Bike Hotel.", "42 posti", "Corticiasca 1h30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Su riservazione", "Sopra Sonvico, ai piedi dei Denti della Vecchia. Ideale per famiglie e arrampicata.", "16 posti, autogestita", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]


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
    """CONTENUTI nella lingua corrente, con i testi che la redazione cambia da admin/ («Testi del sito» › Capanne):
    guardiani, tariffe e note per prenotare, in data/testi/capanne/<cartella>.json."""
    c = {"it": CONTENUTI, "de": CONTENUTI_DE, "en": CONTENUTI_EN}[LINGUA["lang"]].get(file)
    if not c or not os.path.exists(os.path.join(ROOT, "data", "testi", "capanne", c["cartella"] + ".json")):
        return c
    d = testi(f"capanne/{c['cartella']}")
    c = dict(c)
    if c.get("team"):
        c["team"] = dict(c["team"], testo=testo_md(d, "guardiani"),
                         persone=[(virgolette(esc(p["nome"])), testo_campo(p, "ruolo"), p["foto"]) for p in d.get("persone", []) if p.get("foto")])
    if d.get("tariffe"):
        c["tariffe"] = [(testo_campo(t, "titolo"), testo_campo(t, "nota"),
                         [(testo_campo(r, "voce"), prezzo_l(r.get("prezzo") or "")) for r in t.get("righe", [])])
                        for t in d["tariffe"]]
    c["prenotare"] = testo_md(d, "prenotare")
    return c


def virgolette(t):
    """«…» italiane e tedesche diventano “…” nelle pagine inglesi."""
    return t.replace("«", "“").replace("»", "”") if en() else t


PREZZI_L = {"incluso": ("inbegriffen", "included"), "gratis": ("gratis", "free")}


def prezzo_l(p):
    """Prezzo scritto in italiano («Fr. 30.–», «gratis»): in inglese CHF, le parole note tradotte."""
    p = p.strip()
    if p.lower() in PREZZI_L:
        return tr(p, *PREZZI_L[p.lower()])
    return esc(re.sub(r"^Fr\.\s*", "CHF ", p) if en() else p)


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
    return salti(voci, tc("salta"))


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
