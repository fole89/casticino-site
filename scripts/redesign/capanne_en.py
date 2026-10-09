"""Versione inglese delle pagine capanna: stessa struttura di capanne.py (CONTENUTI) e dei dati di pages.py (HUT_PAGES, HUTS).

Le pagine inglesi si generano in en/ (en/campotencia.html, en/capanne/<cartella>/<pagina>.html).
I link ad altre pagine tradotte si scrivono già con en/ davanti (es. "en/motterascio.html"); quelli a pagine solo in
italiano (news, attività, PDF) restano senza. Immagini, gallerie e PDF sono gli stessi della versione italiana.
Inglese britannico; i nomi propri delle capanne restano in italiano («Capanna Cristallina»).
Traduzione da far rileggere a chi parla inglese."""
from capanne import PRENOTA  # noqa: F401  (stesso formato del link di prenotazione)

CT_DOC = "docs/capanne/campotencia/"

# testi di HUT_PAGES (pages.py) in inglese: sostituiscono quelli italiani, il resto (quota, foto, contatti…) resta uguale
HUT_EN = {
    "campotencia.html": dict(
        where="Val Piumogna, Leventina", custody="mid-June to mid-October",
        description="Capanna Campo Tencia, 2140 m, in Val Piumogna (Leventina): 80 beds, staffed from mid-June to mid-October. Contacts and booking.",
        intro="Set on a terrace high above the upper Val Piumogna, it is the ideal base for hikes, traverses to other huts and climbs such as Pizzo Campo Tencia, which at 3072 m is the highest peak lying entirely in Ticino.",
        stay=[("Opening", "All year round"),
              ("Staffed", "Mid-June to mid-October; not staffed in winter, but booking is required; for large groups the hut can be opened by arrangement with the keepers"),
              ("Beds", "80"),
              ("Meals", "Hot food, served all day by the hut keeper"),
              ("Winter room", "Always open, with drinks and firewood")],
        reach=[("Summer access", "From Dalpe 3 h; from Lago Tremorgio (cable car from Rodi) 3 h 30; from Fusio over the Passo Campolungo 6 h"),
               ("Winter access", "From Dalpe 3 h, on skis up Val Piumogna"),
               ("Map", 'Swiss map 1272 Campo Tencia, coordinates <span class="num">699.430 / 144.480</span>')],
        contact=[("Hut keepers", "Valeria Grandi and Paco Porcu"),
                 ("Hut phone", '<a class="num" href="tel:+41918671544">+41 91 867 15 44</a>'),
                 ("Mobile", '<a class="num" href="tel:+41767212572">+41 76 721 25 72</a>'),
                 ("E-mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "cristallina.html": dict(
        where="Passo Cristallina, Valle Bedretto", custody="June to mid-October; in winter at weekends and on public holidays",
        description="Capanna Cristallina, 2575 m, on the pass between Leventina and Valle Maggia: 100 beds, staffed from June to mid-October and at winter weekends and holidays. Contacts and booking.",
        intro="Designed by the architects Baserga and Mozzetti and opened in 2003, it is the first modern hut built by the Swiss Alpine Club. It stands on the pass, at a strategic point between Leventina and Valle Maggia: a panoramic stage on the traverses to Robiei, the Naret, Campo Tencia and San Giacomo. The Cristallina lakes circuit, over one or two days, is also suitable for families; in an hour you can reach the Cristallina and the Cima di Lago. In winter, reached mainly from the north, it opens up superb slopes towards Valle Bedretto, Robiei and Val Formazza.",
        stay=[("Opening", "Always open and accessible"),
              ("Staffed", "June to mid-October; in winter, from December to the end of April, in good conditions, at weekends, on public holidays and for groups"),
              ("Beds", "100"),
              ("Meals", "Prepared all day by the hut keeper"),
              ("Drinks", "Also available when the hut keeper is away")],
        reach=[("Summer access", "From Ossasco 3 h 30; from Robiei 3 h; from Lago del Narèt 2 h 30; from Passo San Giacomo 4 h"),
               ("Winter access", "From Ossasco 3 h; from All’Acqua 4 h"),
               ("Map", 'Swiss map 1251 Bedretto, coordinates <span class="num">683.550 / 147.300</span>')],
        contact=[("Hut keeper", "Emanuele Vellati"),
                 ("Phone", '<a class="num" href="tel:+41918692330">+41 91 869 23 30</a>'),
                 ("E-mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "adula.html": dict(
        where="Upper Val Carassino, Val Soi, Blenio", custody="end of May to mid-October",
        description="Capanna Adula, 2012 m, between Val Carassino and Val Soi (Blenio): 24 beds, open all year, staffed from the end of May to mid-October. Contacts and booking.",
        intro="The “Bassa”, as it has always been known, has the charm of the huts of old: built of stone, a common room full of history, dormitories where thousands of climbers have slept, a warm welcome and local cooking. From this balcony above Valle di Blenio you set off for the summit of the Adula (Rheinwaldhorn) or, on easy paths, for other huts; the wild routes of Val Carassino offer adventurous hiking. For the less ambitious: a walk in the valley, a good lunch and a nap in the sun.",
        stay=[("Opening", "All year round"),
              ("Staffed", "End of May to mid-October"),
              ("Beds", "24"),
              ("Meals", "Prepared by the hut keeper; self-catering only in winter or by arrangement with the hut keeper"),
              ("Drinks", "Also available when the hut keeper is away")],
        reach=[("Summer access", "From Compietto through Val Carassino 2 h 40 (by mountain bike about 1 h); from Dangio through Val Soi 3 h; from Cusiè (Val Malvaglia) over the Passo del Laghetto 5 h"),
               ("Winter access", "From Dangio 3 h 30; from Ghirone 5 h"),
               ("Map", 'Swiss map 1253 Olivone, coordinates <span class="num">719.510 / 150.950</span>')],
        contact=[("Hut keeper", "Raffaele “Lele” Demaldi"),
                 ("Hut phone", '<a class="num" href="tel:+41918721532">+41 91 872 15 32</a>'),
                 ("Mobile", '<a class="num" href="tel:+41795352112">+41 79 535 21 12</a>'),
                 ("E-mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "motterascio.html": dict(
        where="Alpe Motterascio, Greina, Blenio", custody="mid-June to mid-October",
        description="Capanna Motterascio, 2172 m, on the edge of the Greina (Blenio): 70 beds, open all year, staffed from mid-June to mid-October. Contacts and booking.",
        intro="Inaugurated in 1967 and enlarged in 1980, 1990 and 2006, the hut stands on the edge of an extraordinary nature reserve: the Greina, with its marshes, peat bogs, alpine pastures and unspoilt flora. The starting point for fascinating routes, above all to the Greina arch, the largest natural rock arch in Ticino.",
        stay=[("Opening", "All year round"),
              ("Staffed", "Mid-June to mid-October (in 2026 from 13 June to 10 October); in winter the winter room with 10 places, on booking"),
              ("Beds", "70"),
              ("Meals", "Hot meals, prepared all day by the hut keepers"),
              ("Drinks", "Also available when the hut keeper is away")],
        reach=[("Summer access", "From Alpe Garzott (Lago di Luzzone) 2 h; from the Luzzone dam 3 h 30; from Pian Geirètt 3 h 30; from Ghirone through Val Camadra 6 h"),
               ("Winter access", "From Ghirone through Val Camadra and over the Greina Pass, 5-6 h, only with settled snow"),
               ("Map", 'Swiss map 1233 Greina, coordinates <span class="num">720.075 / 161.425</span>')],
        contact=[("Hut keeper", "Fabio Merzaghi"),
                 ("Booking", '<a class="num" href="tel:+41918721622">+41 91 872 16 22</a> (mid-June to mid-October)'),
                 ("Mobile", '<a class="num" href="tel:+41797276905">+41 79 727 69 05</a>'),
                 ("E-mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "montebar.html": dict(
        where="Alta Capriasca, Lugano region", custody="all year round",
        description="Capanna Monte Bar, 1602 m, in the Alta Capriasca: 42 beds in rooms with 2, 4 and 6 beds, staffed all year round, Bike Hotel standard. Contacts and booking.",
        intro="On an exceptionally beautiful rounded summit, with a 180-degree view from the Denti della Vecchia to the Tamaro and, to the west, the Valais four-thousanders from the Mischabel to Monte Rosa. Rebuilt in autumn 2016: rooms with 2, 4 and 6 beds, toilets on each floor, a dining room for about 80 people, a meeting room for 20, a large terrace and a closed room with e-bike charging points and a small workshop, to Bike Hotel standard.",
        stay=[("Opening", "All year round; on request also for events, dinners and lunches"),
              ("Staffed", "Every day from May to early November; in winter from Friday noon to Sunday noon, on public holidays and during school holidays"),
              ("Beds", "42, in rooms with 2, 4 and 6 beds"),
              ("Meals", "Regional cooking with local produce; special menus on booking"),
              ("Without hut keepers", "The hut is closed; only a small entrance room stays open for emergencies")],
        reach=[("Summer access", "From Corticiasca 1 h 30; from Bidogno 2 h; from Isone through Val Serdena and over Piandanazzo 3 h; from Gola di Lago 2 h 30"),
               ("Mountain bike", "Forest road Bidogno-Rompiago, descending to Scareglia or Signôra; Piandanazzo-Al Matro-Serdena-Isone; Piandanazzo-Alpe Pietra Rossa-San Lucio-Bogno"),
               ("Winter access", "From Corticiasca and from Gola di Lago"),
               ("Map", 'Swiss map 1333 Tesserete, coordinates <span class="num">721.800 / 106.610</span>')],
        contact=[("Hut keepers", "James Mauri and Serge Santese"),
                 ("Phone", '<a class="num" href="tel:+41919663322">+41 91 966 33 22</a>'),
                 ("E-mail", '<a href="mailto:montebar@casticino.ch">montebar@casticino.ch</a>')]),
    "baitadelluca.html": dict(
        where="Cioascio, Sonvico", custody="on booking",
        description="Baita del Luca, 1070 m, above Sonvico at the foot of the Denti della Vecchia: 16 beds, self-catering, on booking only.",
        intro="On a broad grassy slope above Sonvico, at the foot of the Denti della Vecchia: the ideal starting point for hikes, also with the family, and for climbing in a unique landscape.",
        stay=[("Opening", "All year, only on booking"),
              ("Beds", "16"),
              ("Meals", "Self-catering, kitchen available"),
              ("Drinks", "Available in limited quantities"),
              ("Booking", "You receive the access code after paying in advance")],
        reach=[("Access", "From Rosone 45 min; from Lovarescia (above Sonvico) 60 min; from Car and Luss (Villa Luganese) 60 min"),
               ("Map", 'Swiss map 1333 Tesserete, coordinates <span class="num">722.980 / 102.600</span>')],
        contact=[("Manager", "Priska Deluigi, 6960 Odogno"),
                 ("Mobile", '<a class="num" href="tel:+41792033084">+41 79 203 30 84</a>'),
                 ("E-mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Booking", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}

# schede della home inglese e delle «altre capanne»: stessi campi di HUTS in pages.py
HUTS_EN = [
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Staffed Jun–Oct", "On a terrace above Val Piumogna, the base for Pizzo Campo Tencia, the highest peak lying entirely in Ticino.", "80 beds", "Dalpe 3 h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Staffed summer and winter", "On the pass of the same name between Leventina and Valle Maggia. Opened in 2003, the first modern SAC hut.", "100 beds", "Ossasco 3 h 30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Staffed May–Oct", "The classic stone hut high above Valle di Blenio: history, a warm welcome and local cooking.", "24 beds", "Compietto 2 h 40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Staffed Jun–Oct", "On the edge of the protected Greina plateau: peat bogs, alpine pastures and the largest natural rock arch in Ticino.", "70 beds", "Garzott 2 h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "All year", "The balcony above Lugano, rebuilt in 2016: views from Monte Rosa to the Denti della Vecchia, Bike Hotel standard.", "42 beds", "Corticiasca 1 h 30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "On booking", "Above Sonvico, at the foot of the Denti della Vecchia. Ideal for families and climbing.", "16 beds, self-catering", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

CONTENUTI_EN = {
    "campotencia.html": dict(
        cartella="campotencia",
        capanna="""<p>The first hut in the mountains of Ticino was built in 1912 at the foot of the peak of the same name, on the Leventina side, in the upper Val Piumogna. It is a base camp for families, hikers and climbers: nature walks, Lago Morghirolo close by, the climbing crags and the great routes of the Campo Tencia group, with the classic traverse of the Cresta dei Corni.</p>
<p>The present building, designed by the section’s architect Oscar Hofmann and inaugurated in 1977, has three floors: on the ground floor the entrance, boot room, toilets and cellar; on the first floor a bright common room with 70 places and the kitchen; on the second about 70 beds in 7 dormitories, some with 4 to 8 places, ideal for families.</p>
<p>The beds have duvets; <strong>a sleeping-bag liner is compulsory</strong>. The hut has kept its 1980s character: no single rooms with bathroom and no hairdryers!</p>""",
        cucina="""<p>A simple, honest menu with a local flavour, though not only from Ticino: cold platters of cured meats and cheeses from the region, soups, fresh gnocchi and polenta with various accompaniments, depending on the season and what is available.</p>
<p>For overnight guests we cook specialities from the area, with a menu that changes with the occasion, inspired by the mountains and beyond.</p>
<p>Vegetarians, vegans and guests with special diets are welcome: please let us know in good time, so that we can look after everyone.</p>""",
        team=dict(img=("guardiani", "Valeria and Paco, hut keepers of Capanna Campo Tencia")),
        accessi=f"""<p>In summer the hut is easy to reach on foot, on family-friendly paths; in winter on skis from Dalpe up Val Piumogna.</p>
<p><strong>To Dalpe:</strong> from the north or south on the A2, exit Rodi-Quinto; by public transport to Rodi and from there by <a href="https://www.postauto.ch/en" rel="noopener">PostBus</a>.</p>
<ul>
<li>From Dalpe (1192 m): 3 h.</li>
<li>From Lago Tremorgio (1849 m), top station of the cable car from Rodi: 3 h 30.</li>
<li>From Fusio (Val Lavizzara) over the Passo Campolungo (2318 m): 6 h.</li>
<li>In winter from Dalpe: 3 h.</li>
</ul>
<p>Maps: Swiss map 1:25,000 sheet 1272 Campo Tencia; 1:50,000 sheet 266 S Valle Leventina. Routes on <a href="https://map.schweizmobil.ch/?lang=en&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2699408&amp;N=1146376" rel="noopener">SwitzerlandMobility</a>.</p>
<p><a class="file-link" href="{CT_DOC}aet-pieghevole-tremorgio.pdf">Rodi-Tremorgio cable car: timetable and prices</a></p>""",
        attivita="""<p>Not just Campo Tencia! Val Piumogna is ideal for experiencing the mountains in all their variety and at any age: the federal game reserve, the alpine pastures, the geological trail on the Campolungo, the kyanite of the Forno and the mountain lakes, refreshing even on the hottest days.</p>
<p>The massif offers many routes: the classic Cresta dei Corni, ascents such as Pizzo Campo Tencia, traverses to the Leìt, Sponda, Barone and Garzonera huts. The hut lies halfway along the <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, the 100 km route from the Nufenen Pass to Lago Maggiore. The crags near the hut are ideal for courses with children and beginners; in winter there are demanding ski tours and icefalls.</p>""",
        storia=dict(
            file="storia", titolo="History of the hut",
            lead="Since 1912 the first hut in the mountains of Ticino: enlarged, destroyed by fire and rebuilt more beautiful than before.",
            img=("inaugurazione-1912", "Postcard of the hut’s inauguration on 10 August 1912, with climbers in front of the stone hut"),
            corpo="""<p>The hut was built in 1912 at the foot of the peak of the same name, on the Leventina side, in the upper Val Piumogna. The name Campo Tencia was invented in 1858: it was given to the highest mountain lying entirely in Ticino (3072 m) when the famous Dufour map was drawn. It combines the names of two alpine pastures belonging to the Patriziato di Prato, Campo and Tencia, in the upper Val Lavizzara on the Valle Maggia side.</p>
<p>The hut was inaugurated on 11 August 1912 (10 August according to some archive sources). In 1932 Patocchi, as ever the driving force, presented plans for an extension, and in the summer of 1933 the new east wing was built.</p>
<figure><img src="assets/img/capanne/campotencia/costruzione.webp" alt="Men at work in front of the old stone hut, historical photograph" width="1200" height="832" loading="lazy" decoding="async"></figure>
<p>Forty years later further work followed to strengthen and improve it. On 22 August 1975 a serious fire destroyed the work of many years.</p>
<p>Work began at once, and the hut was rebuilt bigger, more beautiful and more practical. Its construction was a first in Switzerland, thanks to the architect Oscar Hofmann: no longer the angular image of the classic mountain hut, but a new, light and elegant appearance, with a load-bearing structure in steel, clad and insulated for altitude. The new inauguration took place on 25 September 1977.</p>
<figure><img src="assets/img/capanne/campotencia/capanna-storica.webp" alt="The old stone hut in the snow, historical photograph" width="1200" height="782" loading="lazy" decoding="async"></figure>
<p>In 2008 the north wing added a new professional kitchen. On 11 August 2012 the hut celebrated its centenary. In 2022 a water turbine was installed for the power supply, the photovoltaic system was extended and the waste-water treatment renewed.</p>"""),
        pagine=[
            dict(file="escursioni-facili", titolo="Easy hikes",
                 lead="On white-red-white paths, among alpine pastures, mountain lakes and the Campo Tencia federal game reserve.",
                 img=("lago-morghirolo-fiori", "Cotton grass in flower on the shore of Lago Morghirolo"),
                 corpo="""<p>Between Leìt and Tencia the hikes lead through a precious natural landscape: the Campo Tencia federal game reserve, the geotourism trail on the Campolungo, the alpine pastures and many mountain lakes for a swim or a picnic.</p>""",
                 itinerari=[
                     dict(titolo="Lago Morghirolo", img=("lago-morghirolo", "Lago Morghirolo below the peaks of the Campo Tencia group"),
                          testo="After a break at the hut, why not walk up to the beautiful mountain lake for a refreshing swim?",
                          dati=[("Length", "1.4 km"), ("Ascent", "+250 m"), ("Time", "1 h there and back"), ("Difficulty", "T2")],
                          link=[("Route description", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                     dict(titolo="Nature trail", img=("torrente-piumogna", "The Piumogna stream among the meadows of the valley"),
                          testo="A circular walk starting and finishing in Piumogna, via Capanna Campo Tencia and Alpe Morghirolo, with information boards on nature. You can add Lago Morghirolo (about 1 h more, there and back) or have lunch at the hut and close the loop in the afternoon via Alpe Morghirolo.",
                          dati=[("Length", "12 km"), ("Ascent", "+1300 m"), ("Time", "4-5 h"), ("Difficulty", "T3")],
                          link=[("Online map", "https://s.geo.admin.ch/151dbckh2v17"),
                                ("Route description", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                 ]),
            dict(file="giro-piumogna", titolo="Piumogna circuit",
                 lead="A circular route from Dalpe via the Leìt and Campo Tencia huts, through a protected area rich in flowers.",
                 img=("lago-leit", "The mountain lake below the peaks of the Campo Tencia group"),
                 corpo="""<p>A fantastic route through an area especially rich in flowers, recognised and protected nationally for its geology: alpine columbines, gentians, anemones, black vanilla orchids, alpenroses, mountain buttercups and Haller’s primroses.</p>
<p>From Dalpe you climb through the splendid Boscobello woods to the Passo Vanitt and, on a fine panoramic path, to Capanna Leìt. Along the lake you pass at the foot of Pizzo Prèvat, a peak popular with climbers and also known as the “little Matterhorn”. After the Passo Leìt and the Bocchetta Lei di Cima you can see the peaks of the Campo Tencia group, the highest of which (3072 m) is the highest lying entirely in Ticino. On the descent you pass Lago Morghirolo, from where Capanna Campo Tencia is half an hour away. The way back follows Val Piumogna, with its lovely stream and several alpine pastures.</p>
<figure><img src="assets/img/capanne/campotencia/pascoli-piumogna.webp" alt="Pastures with a cairn and a white-red-white waymark" width="1200" height="659" loading="lazy" decoding="async"></figure>
<h2>There and back from Dalpe</h2>
<p>From Dalpe (reached by PostBus from Rodi-Fiesso or Airolo) follow the path to Boscobello, pass Alpe Cadonighino and cross the Passo Vanitt (2138 m). You reach Capanna Leìt and its lake (2260 m) and continue towards Capanna Campo Tencia: after the Passo Leìt (2431 m) and the Bocchetta Lei di Cima (2481 m) you reach the huts of Lei di Cima (2400 m). The new path leads to Lago Morghirolo (2264 m) and, in half an hour, to Capanna Campo Tencia (2140 m) high above Val Piumogna. On the descent follow the valley path to the huts of Piumogna, then the road towards Boscobello; shortly after the Polpiano bridge a path on the right leads down to Dalpe.</p>
<p>You can also start in Rodi-Fiesso, take the cable car to Lago Tremorgio and follow the path to Capanna Leìt, or do the circuit in the opposite direction. <strong>Note:</strong> the stage is long; a night at the hut is a good idea.</p>
<figure><img src="assets/img/capanne/campotencia/cascina-piumogna.webp" alt="An alpine hut among larches in Val Piumogna, with snowy peaks behind" width="1200" height="900" loading="lazy" decoding="async"></figure>""",
                 dati=[("Length", "19 km"), ("Ascent", "+1330 / −1330 m"), ("Time", "8 h"), ("Difficulty", "T2"),
                       ("Highlights", "Boscobello, Capanna Leìt, Pizzo Prèvat, Lago Leìt, the huts of Lei di Cima, the Campo Tencia group, Lago Morghirolo, the Croslina and Geira pastures")],
                 link=[("Online map of the route", "https://map.schweizmobil.ch/?lang=en&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2700579&amp;N=1146079&amp;trackId=4267446")]),
            dict(file="escursionismo-alpino", titolo="Alpine hiking",
                 lead="Off the beaten track: the summits of Campo Tencia, Forno and Campolungo, from T4.",
                 img=("segnavia-alpino", "White-blue-white waymark on a boulder, with the peaks behind"),
                 corpo="""<p>Hiking difficulty is graded on the T scale in six levels, from T1 (hiking) to T6 (difficult alpine hiking). Around Campo Tencia there are many options: the ascents of Pizzo Campo Tencia, Pizzo Forno or the Campolungo. The routes are only partly waymarked and a good sense of direction is needed; there may be objective dangers and, in early summer, leftover snow: set off well prepared.</p>
<p><a href="https://www.sac-cas.ch/en/training-and-safety/" rel="noopener">Training and safety: SAC advice</a></p>""",
                 itinerari=[
                     dict(titolo="Pizzo Campo Tencia (3072 m) and Pizzo Croslina (3012 m)", img=("croce-campo-tencia", "The summit cross of Pizzo Campo Tencia"),
                          testo="The highest mountain lying entirely in Ticino owes its name to its reddish, iron-rich rock: “tencie”, meaning dirty, in dialect. In the centre of the canton, it offers a panoramic view; from the summit you can descend into Val Lavizzara or join the Via Alta Vallemaggia. The route is mostly waymarked; in some places watch out for stonefall, especially when others are about. In early summer there is snow in the hollow below the Bocchetta di Croslina. From the col (2864 m) you can traverse north to the ridge leading to Pizzo Croslina: exposed sections, take care especially on the descent.",
                          dati=[("Length", "3 km"), ("Ascent", "+940 m"), ("Time", "3 h for Pizzo Campo Tencia, 4 h including Pizzo Croslina"),
                                ("Difficulty", "T4+ Pizzo Campo Tencia, T6 including Pizzo Croslina"), ("Equipment", "Good mountain boots")],
                          link=[("Detailed description", "capanne/campotencia/tencia-croslina.html"),
                                ("Route description", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")]),
                     dict(titolo="Pizzo Forno (2907 m)", img=("pizzo-forno", "Pizzo Forno and Pizzo Laghetto with the last snowfields"),
                          testo="Stage 5 of the Via Idra follows the Senda del Ghiacciaio to the Passo del Ghiacciaione, from where you can climb Pizzo Forno before descending to the Rifugio Alpe Sponda. The north side stays snowy for a long time: good boots and microspikes are strongly recommended.",
                          dati=[("Length", "4.5 km"), ("Ascent", "+767 m"), ("Time", "3 h"), ("Difficulty", "T4")],
                          link=[("Via Idra, stage 5", "https://www.viaidra.ch/tappa05"), ("Route description", CT_DOC + "d-pizzo-forno-2907-m.pdf")]),
                     dict(titolo="Pizzo Campolungo (2714 m)", img=("pizzo-campolungo", "Pizzo Campolungo and the ridges towards Pizzo Prèvat"),
                          testo="From the summit the view opens onto the Leìt, Tremorgio and Morghirolo lakes and onto Pizzo Prèvat, the “Matterhorn of Ticino”. The ascent is not waymarked and crosses steep meadows and scree in the hollow below Alpe Lei di Cima: not difficult, but a good sense of direction is needed.",
                          dati=[("Length", "3 km"), ("Ascent", "+690 m"), ("Time", "2 h 30"), ("Difficulty", "T4")],
                          link=[("Online map", "https://s.geo.admin.ch/epntrruz341r"), ("Route description", CT_DOC + "c-pizzo-campolungo-2714-m.pdf")]),
                     dict(titolo="Campolungo circuit", img=("giro-campolungo", "A turquoise mountain lake among the ridges of the Campolungo"),
                          testo="A wild hike, an alternative link between Capanna Leìt and Campo Tencia via the Valle Maggia side. Rough terrain in places, poor mobile reception and, in early summer, snow on the steep shady slopes.",
                          dati=[("Length", "8 km"), ("Ascent", "+1268 / −1166 m"), ("Time", "6 h from hut to hut, 7-8 h for the whole circuit"),
                                ("Difficulty", "T4-T5, partly protected with ropes"), ("Best time", "July to the end of September"),
                                ("Equipment", "Good mountain boots, helmet and possibly a via ferrata set"),
                                ("Highlights", "Lago Morghirolo, Corte di Zaria, the Cantùn dal Prèvat lakes, Pizzo del Prèvat")],
                          link=[("Route description", CT_DOC + "a-giro-del-campolungo.pdf")]),
                 ]),
            dict(file="cresta-dei-corni", titolo="Cresta dei Corni",
                 lead="Neither hiking nor mountaineering: the airy ridge traverse from the Passo Morghirolo to Campo Tencia.",
                 img=("capanna-cresta-dei-corni", "Capanna Campo Tencia below the Cresta dei Corni"),
                 corpo="""<p>No longer hiking, but not quite mountaineering either: “scrambling” is the word that best describes the Cresta dei Corni on Campo Tencia. The route leads from the Passo Morghirolo over Pizzo Canà, the Tre Corni and Pizzo Croslina to the summit of Campo Tencia: an airy path with breathtaking views over Leventina and Val Lavizzara, devised and equipped by Franco Demarchi, “Dema”, hut keeper for 28 years.</p>
<p>It is a high-alpine, exposed ridge route with pillars and rock steps up to 25 m, well protected and waymarked; in early summer there may be snow. <strong>There are no escape routes: good fitness, a head for heights and stable weather are essential. Plan your time carefully and keep plenty in reserve.</strong></p>
<h2>Route</h2>
<p>From the hut, follow traces of path up to the col at 2560 m. From the saddle you stay mostly on the crest, with easy climbing, partly protected, alternating with walking sections. From Pizzo Croslina descend carefully to the col of the same name, from where, if you still have the energy, you can climb Pizzo Campo Tencia. Descent by the normal route in about 1 h 30.</p>""",
                 dati=[("Length", "8 km"), ("Ascent", "+1350 / −1190 m"), ("Time", "8 h from hut to hut"),
                       ("Difficulty", "T6, F+ (PD), sections of grade III"), ("Equipment", "Harness, via ferrata set, helmet, possibly a 30 m rope for belaying")],
                 link=[("Route online", "https://s.geo.admin.ch/r94n5ne4qz11"), ("Overview of the Cresta dei Corni", CT_DOC + "prospetto-tre-corni.pdf")],
                 foto="cresta-dei-corni"),
            dict(file="tencia-croslina", titolo="Pizzo Campo Tencia and Pizzo Croslina",
                 lead="The highest pyramid of rock and ice in Ticino and the giant that towers over the hut.",
                 img=("croslina-tencia", "The summits of Pizzo Croslina and Pizzo Campo Tencia with snow"),
                 corpo="""<p>Pizzo Campo Tencia (3072 m) is an extraordinary pyramid of rock and ice with a wide panoramic view. Pizzo Croslina (3012 m) rises like a giant above the hut; seen from the east, however, it is an elegant pyramid.</p>
<p>The north side of this stretch of the main ridge is typical: after the pyramid of the Croslina, three summits follow regularly towards the south-east, separated by barely marked saddles: Pizzo Campo Tencia (3072 m), the middle summit Tenca (3035 m, unnamed on the national map) and Pizzo Penca (3038 m).</p>
<h2>Route</h2>
<p>From the hut head south following the white-blue-white waymarks to a waterfall. On the left a wide chimney leads to the ledge that crosses the whole face: a well waymarked, exposed path climbs south-east to an easy rib. Heading south-west you reach the hollow of the Laghetto, at the foot of the remains of the Ghiacciaio Grande di Croslina. Continue along the small ridge between the two Croslina glaciers to about 2800 m, then south-west, descending slightly onto the glacier, to the Bocchetta di Croslina (2864 m), always following the white-blue-white waymarks. Along the crest you reach the summit cross.</p>
<p>From the summit you can traverse to Capanna Soveltra in Valle Maggia, heading south-east on the white-blue-white waymarks.</p>
<p><strong>Pizzo Croslina:</strong> from the Bocchetta di Croslina head north-west following the blue dots to a ledge to the right of the obvious scree gully. Partly exposed ascent with rock sections of grade II.</p>
<p>For both summits the descent is by the ascent route.</p>""",
                 dati=[("Length", "3 km"), ("Ascent", "+940 m"), ("Time", "3 h for Pizzo Campo Tencia, 4 h including Pizzo Croslina"),
                       ("Difficulty", "T4+ Pizzo Campo Tencia, T6 including Pizzo Croslina"),
                       ("Highlights", "The hollow of the Laghetto, the Ghiacciaio Grande di Croslina, the summit cross of Campo Tencia, the edelweiss on the Croslina")],
                 link=[("Route description", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")],
                 foto="tencia-croslina"),
            dict(file="arrampicata", titolo="Climbing",
                 lead="Crags a few minutes from the hut, from grade III to 6b: ideal for learning.",
                 img=("giardino-arrampicata", "A climber on a slab near the hut"),
                 corpo=f"""<p>An ideal area for teaching children and beginners to climb: around the hut several crags have been equipped, from grade III up to a few 6b pitches for the more demanding.</p>
<p>The Angolo sector by the lake is equipped specifically for rock training: single-pitch routes, abseil stations, free-hanging abseils and a short, easy multi-pitch route for practice. A few minutes from the hut, in the Cascata sector, you can practise rope work on easy, parallel multi-pitch routes, and the Kape boulder has a few single-pitch routes.</p>
<p><a href="https://s.geo.admin.ch/na49wcdjtms7" rel="noopener">The sectors on the map</a></p>
<p><a class="file-link" href="{CT_DOC}volantino-arrampicata-campo-tencia.pdf">Crag leaflet</a></p>
<table>
<thead><tr><th>Sector</th><th>Routes</th><th>Length</th><th>Grade</th><th>Notes</th></tr></thead>
<tbody>
<tr><td>Cascata</td><td>4</td><td>60 m</td><td>3-4</td><td>multi-pitch, parallel</td></tr>
<tr><td>Kape</td><td>7</td><td>10 m</td><td>5-6c</td><td>single pitch</td></tr>
<tr><td>Tutto o niente</td><td>10</td><td>20 m</td><td>3-5a</td><td>single pitch</td></tr>
<tr><td>Disperato</td><td>6</td><td>10 m</td><td>4-5a</td><td></td></tr>
<tr><td>Onapart</td><td>3</td><td>30 m</td><td>5a-6b</td><td></td></tr>
<tr><td>Pulce di roccia</td><td>5</td><td>20 m</td><td>3-4</td><td>easy slabs</td></tr>
<tr><td>Angolo</td><td>8</td><td>20 m</td><td>4-5a</td><td>training area</td></tr>
<tr><td>Piode</td><td>3</td><td>25 m</td><td>4-5a</td><td></td></tr>
<tr><td>Pitela</td><td>6</td><td>10-80 m</td><td>3-5a</td><td></td></tr>
<tr><td>Cresta rossa</td><td></td><td>500 m</td><td>2-4</td><td>alpine route</td></tr>
<tr><td>Lago</td><td>1</td><td>75 m</td><td>5a</td><td></td></tr>
</tbody>
</table>
<figure><img src="assets/img/capanne/campotencia/settori-arrampicata.webp" alt="Map of the climbing sectors around the hut and Lago Morghirolo" width="1088" height="766" loading="lazy" decoding="async"></figure>""",
                 foto="arrampicata"),
            dict(file="inverno", titolo="In winter",
                 lead="Demanding ski tours away from the well-known destinations, and icefalls up to 200 metres.",
                 img=("scialpinismo", "Ski tourers descending a wide snow slope, against the light"),
                 corpo="""<h2>Ski touring</h2>
<p>In winter the Campo Tencia area stays away from the well-known destinations. The technical, rough terrain calls for good snow conditions and solid skills in ski touring and navigation. In spring you find the conditions for very rewarding tours: Pizzo Campo Tencia, Pizzo Forno and Pizzo Campolungo. The hut is not staffed, but booking is required; for large groups it can be opened by arrangement with the keepers.</p>
<h2>Icefalls</h2>
<p>In the hollow of the Buco di Cumasna, at 2000 metres, mighty icefalls up to 200 metres long and of varying difficulty form from the start of winter. On the right is the best known, the “Giovannelli”, in the gully used in winter to get past the rock step on the way to or from the summit of Pizzo Campo Tencia.</p>""",
                 foto="inverno"),
        ],
        sostenitori=dict(
            testo="Many thanks to the partners who support the hut.",
            loghi=[("Switzerland Tourism", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/"),
                   ("Ticino Tourism", "sostenitori/ticino-turismo", "https://www.ticino.ch/en/"),
                   ("Bellinzona e Valli Tourism", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/en/")]),
        foto=[("The hut", "capanna"), ("The kitchen", "cucina"), ("The surroundings", "dintorni")],
    ),

    "cristallina.html": dict(
        cartella="cristallina",
        capanna="""<p>The first modern hut of the Swiss Alpine Club stands at 2575 m on the Cristallina Pass, in an area that invites you to explore in summer and winter alike. In summer it is a base for the surrounding peaks and for traverses into Valle Maggia, Val Formazza and the Gotthard area; in winter the snowy surroundings offer superb descents and combinations of summits.</p>
<p>It has 100 beds in bunks with duvets, in 6 rooms of 4, 9 of 8 and 2 dormitories of 12, a panoramic dining room with terrace, indoor toilets with hot water, a shower, a drying room and a boot room with hut slippers. A sleeping-bag liner is compulsory. Good Swisscom reception at the hut.</p>""",
        cucina="""<p>During the day, simple dishes for everyone: gnocchi, ravioli, savoury tarts, cured meats, desserts and much more, all made at the hut with local Swiss produce. For half board the menus change with the day of the week, with vegetarians in mind too. Plus a good choice of wines and spirits.</p>
<p><strong>Important:</strong> let us know in good time if you are vegetarian or vegan or have allergies or intolerances: we will gladly prepare a suitable menu.</p>
<p>Rooms are allocated according to when bookings arrive and the size of the group; rooms cannot be booked exclusively. When the hut is staffed, half board is compulsory.</p>
<p>Dogs are welcome, but not in the bedrooms or common rooms: please let us know before you arrive.</p>""",
        team=dict(titolo="The hut keeper", img=("guardiano", "Emanuele Vellati, hut keeper of Capanna Cristallina, in the snow with the Basodino behind")),
        accessi="""<p>In summer the hut is a few hours’ walk away, mostly on family-friendly paths; in winter on skis from Valle Bedretto, from Robiei or from Val Formazza.</p>
<ul>
<li>From Ossasco: 3 h 30.</li>
<li>From Passo San Giacomo: 4 h.</li>
<li>From Robiei: 3 h.</li>
<li>From Lago del Narèt: 2 h 30.</li>
<li>From Airolo Pesciüm: 5 h.</li>
<li>From Capanna Poncione di Braga: 4 h.</li>
<li>In winter: from Ossasco 3 h, from All’Acqua 4 h.</li>
</ul>
<p><strong>By car from the north:</strong> A2 to Airolo, then towards the Nufenen Pass and Valle Bedretto. <strong>From the south:</strong> A2 to Bellinzona, then Locarno and Valle Maggia: Val Bavona for Robiei, with the <a href="https://www.robiei.ch/" rel="noopener">San Carlo-Robiei cable car</a> (in summer), or Val Lavizzara for the Narèt.</p>
<p><strong>By public transport:</strong> S10 train to Airolo, then bus into Valle Bedretto. Taxi from Airolo: Marchetti Taxi <a class="num" href="tel:+41918733035">+41 91 873 30 35</a>, Gotthard Taxi <a class="num" href="tel:+41787901055">+41 78 790 10 55</a>.</p>
<p><strong>Traverses to other huts:</strong> <a href="https://www.corno-gries.ch/" rel="noopener">Corno Gries</a> (2338 m) 5 h; <a href="https://www.capanna-basodino.ch/" rel="noopener">Basodino</a> (2200 m) 2 h; <a href="https://www.utoelocarno.ch/" rel="noopener">Poncione di Braga</a> (1870 m) 4 h; <a href="https://www.satritom.ch/garzonera/" rel="noopener">Garzonera</a> (2000 m) 5 h, T5; <a href="https://www.rifugiomarialuisa.it/" rel="noopener">Rifugio Maria Luisa</a> (Italy, 2393 m) 5 h.</p>
<p>Maps: Swiss map 1:25,000 sheet 1251 Val Bedretto; ski touring map 265 S Nufenenpass.</p>""",
        attivita="""<p>The Cristallina Pass is a natural link between the Gotthard massif and Valle Maggia, in the middle of a network of routes and huts: the <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, the Via Cristallina and the Via Alta della Vallemaggia all pass this way. In winter it is a ski touring paradise, with reliable snow even in poor years.</p>
<p>The geology tells the story of how the Alps were formed: marble from marine sediments next to igneous rock, incredible folds. The wildlife is rich: the ibex colony towards the Cima di Lago, chamois, eagles, kestrels. And everywhere traces of human work: alpine pastures, military installations and large hydroelectric plants.</p>""",
        pagine=[
            dict(file="proposte-gite", titolo="Suggested trips", foto="proposte-gite",
                 lead="Five moderate routes, from the Cima di Lago to the Via Idra, using the hut as a base or a stage.",
                 img=("pizzo-cristallina", "View from the summit of Pizzo Cristallina over mountain lakes and peaks"),
                 corpo="""<p>If you want to discover the wonderful Cristallina area, with its mountain lakes and high-mountain wildlife, here are moderate routes, not too long, that start at the hut or use it as a stage.</p>""",
                 itinerari=[
                     dict(titolo="Cima di Lago (2832 m)", img=("cima-di-lago", "An ibex on the slope of the Cima di Lago, with the route marked in red"),
                          testo="A summit with a superb view, ideal for sure-footed children too: you are likely to meet ibex.",
                          dati=[("Length", "4 km"), ("Ascent", "+300 m"), ("Time", "1 h"), ("Difficulty", "T4")],
                          link=[("Route description", "docs/capanne/cristallina/a-cima-di-lago-2832-msm.pdf")]),
                     dict(titolo="Pizzo Cristallina (2912 m)", img=("pizzo-cristallina", "View from the summit of Pizzo Cristallina over mountain lakes and peaks"),
                          testo="The main summit, surrounded by a string of mountain lakes; on the top still stands the Rifugio Camosci, the last witness of wartime in the area. On the final slope watch out for stonefall when others are about; enter the bivouac only with great care, there is a risk of falling.",
                          dati=[("Length", "11 km from Ossasco"), ("Ascent", "+1100 m from Ossasco"), ("Time", "2 h from the hut, 6 h from Ossasco"), ("Difficulty", "T4")],
                          link=[("Route description", "docs/capanne/cristallina/b-cristallina-2912.pdf")]),
                     dict(titolo="Cristallina circuit", img=("giro-cristallina", "The Robiei reservoir and its dam, below the mountains"),
                          testo="A classic, easy circuit on a white-red-white path around the summit of the Cristallina. Also possible as a day trip from Robiei or from the Narèt pass, with lunch at the hut.",
                          dati=[("Length", "14 km"), ("Ascent", "+980 m"), ("Time", "5 h 30"), ("Difficulty", "T3")],
                          link=[("Route description", "docs/capanne/cristallina/c-giro-del-cristallina.pdf")]),
                     dict(titolo="Sentiero Cristallina 59, towards Robiei", img=("percorso-59", "Mountain lakes in a rocky basin on the Sentiero Cristallina"),
                          testo="The Sentiero Cristallina number 59 is a classic three-day traverse from Bignasco in Valle Maggia to Airolo.",
                          dati=[("Length", "42 km, in three stages"), ("Ascent", "+2800 / −2100 m"), ("Time", "3 days"), ("Difficulty", "T3")],
                          link=[("Route description", "docs/capanne/cristallina/d-percorso-59-cristallina.pdf")]),
                     dict(titolo="Nufenen Pass-Cristallina-Airolo", img=("nufenen-airolo", "Hikers on a grassy, rocky ridge"),
                          testo="The first stage of the Via Idra, from the Nufenen Pass to Airolo with a night at the hut. The highlight is the climb through the Canale del Becco, protected with ropes and steps: best done in ascent; watch out for stonefall and snow at the start of the season.",
                          dati=[("Length", "27 km"), ("Ascent", "+1600 / −2450 m"), ("Time", "10 h, over two days (5 + 5)"),
                                ("Difficulty", "T4 on the first day (T6 in the Canale del Becco), T3 on the second")],
                          link=[("Route description", "docs/capanne/cristallina/e-passo-nufenen-airolo.pdf")]),
                 ]),
            dict(file="inverno", titolo="In winter", foto="inverno",
                 lead="Summits and powder descents: several runs in a day around the hut.",
                 img=("discesa-polvere", "Ski tourers climbing a wide, shady snow slope"),
                 corpo="""<p>The Cristallina area is excellent for powder descents. Many routes around the hut can be combined, with two or more descents in a day, which often ends on the shady slopes on the right-hand side of Valle Bedretto.</p>
<ul>
<li>Up through Val Torta and down through <strong>Val Cassinello</strong> from the Bassa di Folcra or from the <strong>Passo Gararesch</strong>, a variant (routes 521 h and 521 i).</li>
<li>Up through Val Torta for the classic <strong>Cristallina circuit</strong>, with lunch at the hut and a descent through Val Piana or Val Cavagnolo.</li>
<li>The summit of the <strong>Cristallina</strong> and a descent via the “Diavolezzina”, possibly climbing back up to the Bassa di Folcra (521 h) or the Passo Gararesch (521 i).</li>
<li><strong>Cima di Lago</strong> as an afternoon tour, from Val Torta or from Val Cavagnoli.</li>
<li>The wild, varied <strong>circuit of the cols</strong>: on the first day All’Acqua, San Giacomo, Passo Grandinagia, Bocchetta di Valleggia, Passo di Cima di Lago and the hut (<a href="https://s.geo.admin.ch/7e3436c217" rel="noopener">map</a>); on the second Cima di Lago, Sfunadau, Cristallina and Passo Gararesch.</li>
<li><strong>Poncione di Braga, Basodino, Marchhorn:</strong> summits on long traverses.</li>
</ul>"""),
            dict(file="curiosita", titolo="Did you know?",
                 lead="Military occupation, the birth of the Alps and great hydroelectric plants: background to the Cristallina area.",
                 img=("rocce-piegate", "Rocks bent by the folding of the Alps in a green hollow"),
                 corpo="""<p>The traces of the formation of the Alps are plain to see: the forces that folded up the chain brought marine sediments to the surface, and within a few metres you find rocks of quite different composition and origin. This also shapes the flora, which depends on the ground beneath. The wildlife is typically alpine: you can easily meet the ibex of the colony, over a hundred animals with no fear of people. People have changed the area too, with border guarding in wartime and the great hydroelectric installations.</p>
<p>The full texts are only available in Italian.</p>""",
                 itinerari=[
                     dict(titolo="The history of the military occupation", img=("rifugio-camosci", "The old military stone hut on the summit, in the snow"),
                          testo="The building of the road through Val Formazza to the Passo San Giacomo between 1926 and 1929 worried Switzerland and led to the fortification of the area.",
                          link=[("Full text", "docs/capanne/cristallina/a-la-storia-delloccupazione-militare-1.pdf")]),
                     dict(titolo="The traces of mountain building", img=("rocce-piegate", "Rocks bent by the folding of the Alps in a green hollow"),
                          testo="The Cristallina landscape was shaped by alpine mountain building, a process that lasted about 25 million years.",
                          link=[("Full text", "docs/capanne/cristallina/b-le-tracce-dellorogenesi-1.pdf")]),
                     dict(titolo="Naret-Robiei hydroelectric power", img=("schema-idroelettrico", "Diagram of the linked reservoirs between Gries, Robiei and Lago Maggiore"),
                          testo="The Robiei-Narèt area is rich in interconnected reservoirs that make the best possible use of the water for clean electricity.",
                          link=[("Full text", "docs/capanne/cristallina/c-ldroelettrico-naret-robiei-1.pdf")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Many thanks to the partners who support the hut.",
            loghi=[("Switzerland Tourism", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/"),
                   ("Ticino Tourism", "sostenitori/ticino-turismo", "https://www.ticino.ch/en/"),
                   ("Bellinzona e Valli Tourism", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/en/")]),
        foto=[("The hut", "capanna"), ("The kitchen", "cucina"), ("The surroundings", "dintorni")],
    ),

    "adula.html": dict(
        cartella="adula",
        capanna="""<p>The “Bassa”, as it has always been known, was inaugurated in 1924 and has kept all the features of the original building in stone and wood: a common room full of history, dormitories where thousands of climbers have slept, a warm welcome and local cooking that fills both stomach and soul.</p>
<p>It has 24 beds in four small dormitories of 4, 5 and 7 places, also suitable for families, and two double rooms at extra cost; two cosy dining rooms with 20 places, indoor toilets, a shower, solar power for the lighting and a kitchen running on wood and gas. The beds have duvets; a sleeping-bag liner is compulsory. Moderate mobile reception at the hut.</p>
<p>The winter room is always open, with drinks and firewood.</p>""",
        cucina="""<p>The panoramic terrace invites you to eat outdoors. Every day we cook with produce from the region: Ticino dishes, cheeses and formaggini, pasta with sauce, soup, minestrone and our rösti in various versions, and always several cakes.</p>
<p>For overnight guests there are dishes and specialities with seasonal produce in the evening, and a generous breakfast gives you strength for new adventures.</p>
<p><strong>Important:</strong> let us know in good time if you are vegetarian or vegan or have allergies or intolerances.</p>
<p>Dogs are welcome, but not in the bedrooms: there is a place for them outside. Please let us know about your dog in advance.</p>""",
        team=dict(img=("guardiani", "The hut keeper and two helpers in front of the entrance of the stone hut")),
        accessi="""<p><strong>In summer</strong> the hut is easy to reach on the flat mule track through Val Carassino from Compietto. The valley is about 6 km long and passes two alpine pastures, Alpe Bolla and Alpe Bresciana, where an excellent cheese is made, which you can also enjoy at the hut. The stream close by makes the path ideal for families on hot days; by mountain bike about an hour is enough.</p>
<p><strong>In winter</strong> you climb on skis from Dangio through Val Soi, or from Ghirone via the Luzzone and Val Carassino, with safe snow and preferably in spring.</p>
<ul>
<li>From Compietto (car park) through Val Carassino: 2 h 40, by mountain bike about 1 h.</li>
<li>From Dangio (bus stop) through Val Soi: 3 h.</li>
<li>From Cusiè in Val Malvaglia (car park) over the Passo del Laghetto: 5 h.</li>
<li>From the Läntahütte over the Bocchetta di Fornee.</li>
<li>In winter: from Ghirone 5 h, from Dangio 3 h 30.</li>
</ul>
<p><strong>By car:</strong> A2 to Biasca, then towards the Lukmanier Pass to Campo Blenio and Ghirone; up to the Luzzone dam, across the dam and on to Alpe di Compietto. Or leave the car in Ghirone and take the <a href="https://www.autolinee.ch/greina" rel="noopener">alpine bus</a>.</p>
<p><strong>By public transport:</strong> S10 train to Biasca, bus 131 to Ghirone, then the alpine bus to the Luzzone dam. Taxi Riviera (Biasca): <a class="num" href="tel:+41918624848">+41 91 862 48 48</a>.</p>
<p><strong>Traverses to other huts:</strong> <a href="en/motterascio.html">Motterascio</a> 5 h; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 3 h 30; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 1 h; <a href="https://quarnei.ch/" rel="noopener">Quarnei</a> 3 h.</p>
<p>Maps: Swiss map 1:25,000 sheet 1253 Olivone; ski touring map 256 S.</p>""",
        attivita="""<p>At the Adula there is a touch of the old days in the air: hospitality and good food, with a glass of wine, invite you to lie back in the grass against an extraordinary backdrop. From here you set off on exciting routes, old crossings and airy ridges.</p>
<p>An ideal place for children: splendid flowers in early summer, chamois and ibex, marmots, cows to stroke and a stream to bathe in. You sleep in a historic hut with old-time charm and climb the Adula (Rheinwaldhorn), the goal of many people from Ticino, with its glacier, which sadly will soon be only a memory.</p>""",
        pagine=[
            dict(file="cima-adula", titolo="The summit of the Adula", foto="cima-adula",
                 lead="On the roof of Ticino: the ascent of the Adula (Rheinwaldhorn, 3402 m) by the Via Malvaglia, descending over the Bresciana glacier.",
                 img=("cordata-vetta", "A roped party on the snowy summit"),
                 corpo="""<p>The ascent of the Adula is the goal of many hikers and climbers from Ticino. The summit is fairly easy to reach in winter and in summer; because of the shrinking glacier and hot summers, it is better to go before the snow has melted completely and exposed the glacier.</p>
<p>For those with basic alpine experience, we recommend the circuit via the lake of Cadabi, climbing by the ridge of the Via Malvaglia. Near the summit the rock left by the glacier is loose: take care. On the descent you can go over the Bresciana glacier, watching out for crevasses, as far as the path back to Capanna UTOE.</p>""",
                 dati=[("Length", "8 km"), ("Ascent", "+1400 m"), ("Time", "4-5 h up, 2-3 h down"),
                       ("Difficulty", "F+ (PD), protected sections on the ridge of the Via Malvaglia"), ("Highlights", "The lake of Cadabi, the Bresciana glacier, the view from the summit")],
                 link=[("Online map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721078&amp;N=1150644&amp;trackId=5023916")]),
            dict(file="proposte-gite", titolo="Suggested trips",
                 lead="Five traverses to other huts, from the high route in Val Carassino to the Via Crio.",
                 img=("via-alta-carassino", "A hiker on a rocky ridge above Val Carassino"),
                 corpo="""<p>If you have several days, these hiking and mountain routes reveal little-known corners of Val Carassino. They are not circuits: they link the hut with other huts. The high route in Val Carassino can be walked in both directions and avoids going along the valley floor twice if you start or finish at the Luzzone; the Cassimoi-Cassinello traverse is a superb ridge walk; the Bocchetta di Fornee opens the way to Vals; the crossing to Quarnei is a popular classic, also for families with children.</p>""",
                 itinerari=[
                     dict(titolo="High route in Val Carassino", img=("via-alta-carassino", "A hiker on a rocky ridge above Val Carassino"),
                          testo="From Compietto to the hut, high up via Sgiu, La Colma, Pinadee and Bresciana.",
                          dati=[("Length", "7.5 km"), ("Ascent", "+1050 m"), ("Time", "5 h"), ("Difficulty", "T5")],
                          link=[("Route description", "docs/capanne/adula/a-via-alta-della-val-carassino.pdf")]),
                     dict(titolo="Ledges and summits of Val Carassino", img=("cengie-carassino", "Grassy slopes and ledges below snowy peaks"),
                          testo="Pizzo Amianto and its ancient landslide, the sheep ledges, chamois, ibex and the eagle.",
                          dati=[("Length", "11.5 km"), ("Ascent", "+1000 m"), ("Time", "5 h"), ("Difficulty", "T5")],
                          link=[("Route description", "docs/capanne/adula/b-cengie-e-vette-della-val-carassino.pdf")]),
                     dict(titolo="To the Läntahütte over the Bocchetta di Fornee", img=("lago-fornee", "A mountain lake among glacier-polished rocks"),
                          testo="The traces of the retreating glacier, rocks and ibex, towards Vals.",
                          dati=[("Length", "8.7 km"), ("Ascent", "+1000 m"), ("Time", "5 h 30"), ("Difficulty", "T5")],
                          link=[("Route description", "docs/capanne/adula/c-alla-capanna-lanta-dalla-btta-di-fornee.pdf")]),
                     dict(titolo="Easy crossing to Quarnei", img=("laghetto-cadabi", "The lake of Cadabi in a rocky basin"),
                          testo="The Bresciana glacier and its decline, the lateral moraines, the roches moutonnées, the lake of Cadabi and the Quarnei plain.",
                          dati=[("Length", "4 km"), ("Ascent", "+700 m"), ("Time", "3 h 30"), ("Difficulty", "T3")],
                          link=[("Route description", "docs/capanne/adula/d-facile-traversata-a-quarnei.pdf")]),
                     dict(titolo="Via Crio, stage 6: from Pizzo Cassimoi to the Luzzone", img=("via-crio", "A hiker on a protected section among reddish rocks"),
                          testo="Three three-thousanders on one of the most demanding stages of the <a href=\"https://www.viacrio.ch/\" rel=\"noopener\">Via Crio</a>.",
                          dati=[("Length", "15.9 km"), ("Ascent", "+1540 / −1950 m"), ("Time", "8 h"), ("Difficulty", "T6, demanding traverse")],
                          link=[("Route description", "docs/capanne/adula/e-scaradra-luzzone-passando-dalla-bocchetta-di-fornee.pdf"),
                                ("Overview of the Via Crio", "docs/capanne/adula/via-alta-crio-prospetto-2024.pdf"),
                                ("GPX track", "https://www.viacrio.ch/s/006-CRIO-GPX-Adla-UTOE-Scaradra-MV.gpx")]),
                 ]),
            dict(file="inverno", titolo="Winter and spring", foto="inverno",
                 lead="Lonely summits for experienced ski tourers and snow gullies for early-season mountaineering.",
                 img=("pendio-innevato", "Ski tracks on a wide snow slope"),
                 corpo="""<h2>The Adula in winter</h2>
<p>In winter the Ticino side of the Adula stays remote: avalanches come down the slopes of the Carassina, and the climb from Val Soi needs settled snow in its final part. When spring comes to the valley, the massif offers fine, technical hut-to-hut traverses between the <strong>Läntahütte</strong>, <strong>Zapporthütte</strong>, <strong>Adula</strong> and <strong>Quarnei</strong>: on the Adula circuit and its variants you climb at least one summit over 3000 m every day.</p>
<ul>
<li><strong>Adula (Rheinwaldhorn, 3402 m) via the Vadrecc di Bresciana:</strong> ascent by the summer route (324 a); in good conditions you ski straight down the glacier to about 2500 m and, with a short climb back over the moraine, reach the slope above Capanna UTOE (324 c). F+ (PD).</li>
<li><strong>Grauhorn (3258 m):</strong> too loose in summer, reachable in spring by route 323, on foot up the slope to the ridge at 3100 m. AD.</li>
<li><strong>Piz Jut (3128 m):</strong> over the Bocchetta di Fornee (2885 m, route 320), then on the Graubünden side to the summit; descent to the Läntahütte through the Forneitobel (309). AD.</li>
<li><strong>Cima di Pinadee (2486 m):</strong> above Val Carassina, with no great difficulty in a good hour from Alpe di Bresciana. F+ (PD).</li>
</ul>
<h2>Mountaineering in spring</h2>
<p>The summits from the Torrone di Nav to the Passo Cadabi are suffering from the melting of the glaciers: ascents that were once safe even in summer are now loose scree slopes prone to stonefall. They are best tackled while there is still enough snow above 2500 m, carefully judging the overnight freeze.</p>
<p>In these conditions the snow gullies up to 50°, with crampons and ice axe, are well worth it:</p>
<ul>
<li>the west couloir of the <strong>Cima dal Laghetto</strong> from Val Soi to point 2582 m, F;</li>
<li>the Adula by the <strong>Damstädten</strong> couloir (left), south-west face to point 3205 m, F+ (PD);</li>
<li>the Adula by the <strong>Ezio e Maria</strong> couloir (right), south-west face to point 3205 m, PD+.</li>
</ul>
<p>For the <strong>Grauhorn</strong> (scree slope to about 3180 m), as well as for the <strong>Cima di Fornee</strong>, <strong>Piz Jut</strong> and <strong>Punta dello Stambecco</strong> from Fornee, setting off early in the season is also safer and easier.</p>""",
                 link=[("Ski touring routes on the map", "https://map.geo.admin.ch/?lang=en&amp;topic=wildruhezonen&amp;bgLayer=ch.swisstopo.pixelkarte-farbe&amp;layers=ch.bafu.wrz-jagdbanngebiete_select,ch.bafu.wrz-wildruhezonen_portal,ch.swisstopo-karto.skitouren&amp;layers_visibility=true,false,true&amp;catalogNodes=1308&amp;E=2721748.94&amp;N=1152606.59&amp;zoom=6&amp;layers_opacity=1,1,0.8")]),
            dict(file="curiosita", titolo="Did you know?",
                 lead="Two huts and the political struggles of a hundred years ago, ancient seasonal migrations and the riches of Val Carassino.",
                 img=("vetta-tramonto", "A summit in the evening light above shady valleys"),
                 corpo="""<p>At first sight Val Carassino seems long and monotonous, but at the huts the view opens onto the Adula, Val Soi and Valle di Blenio. If you look closely you discover the valley’s botanical riches and the wildlife on its slopes.</p>
<p>The people of the valley have used the area since the early Middle Ages: alpine farming lives on today, and its produce is much appreciated. The summit and the two huts also recall the political struggles of more than a hundred years ago, when “proletarian” climbing groups and the UTOE grew out of civic and workers’ movements, a Ticino peculiarity in the history of Swiss mountaineering.</p>
<p>The full texts are only available in Italian.</p>""",
                 itinerari=[
                     dict(titolo="Why two huts? A short history", img=("vetta-tramonto", "A summit in the evening light above shady valleys"),
                          testo="The greatest dream that the spirited president Remo Patocchi wanted to make come true…",
                          link=[("Full text", "docs/capanne/adula/a-perche-due-capanne-cenni-di-storia.pdf")]),
                     dict(titolo="Stories of ancient seasonal migrations", img=("dipinto-alpe", "Painting of an alpine pasture with a stone hut below the peaks"),
                          testo="A thousand years ago a very warm period had a great influence on the whole of the Alps…",
                          link=[("Full text", "docs/capanne/adula/c-storie-di-antiche-transumanze.pdf")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Many thanks to the partners who support the hut.",
            loghi=[("Switzerland Tourism", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/"),
                   ("Ticino Tourism", "sostenitori/ticino-turismo", "https://www.ticino.ch/en/"),
                   ("Bellinzona e Valli Tourism", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/en/")]),
        foto=[("The hut", "capanna"), ("The surroundings", "dintorni")],
        foto_lead="The hut and the surroundings",
    ),

    "motterascio.html": dict(
        cartella="motterascio",
        capanna="""<p>In the middle of a network of paths between some of the most beautiful places in southern Switzerland, Capanna Michela Motterascio stands at 2172 m on Alpe Motterascio, on the southern edge of the Greina plateau, in harmony with wood, copper and stone. Below the peaks of Piz Terri, Pizzo Coroi, Piz Vial, Gaglianera and Piz Valdraus you spend days full of walks, silence and rest. You don’t need to be an experienced climber: curiosity, enthusiasm and a little energy are enough.</p>
<p>The hut is spacious: 70 beds with duvets, a panoramic dining room with 55 places and a wall of windows onto the Alps, a “romantic” common room with 20 places, separate indoor toilets for women and men, a shower when the spring water is sufficient, a drying room and hut slippers at the entrance, for the little ones too. The water is drinkable spring water; electricity comes from photovoltaics, with a generator as back-up. A sleeping-bag liner is compulsory and can also be hired. No mobile reception.</p>
<p><strong>Winter room:</strong> 10 beds with duvets, drinks, firewood and the basics (salt, sugar, instant coffee). Please bring your own food; water is not guaranteed (fountain on the terrace, if not frozen), and there is no winter toilet. Booking is compulsory, online; the confirmation contains all the information.</p>""",
        cucina="""<p>At lunchtime the sunny terrace and the lovely common room invite you to simple regional dishes, hot and cold, with a breathtaking view, plus the buffet of homemade cakes. Dinner is at 7 pm, depending on what is available and the cook’s inspiration; then a generous breakfast for the next day. Cooking is done mainly on the wood stove and with gas.</p>
<p><strong>Important:</strong> let us know in good time if you are vegetarian or vegan or have allergies or intolerances.</p>
<p>For children there are games, books, paper and coloured pencils; along the path, with a bit of luck, you will see marmots. Dogs are welcome but may not enter the hut: for the night the sheltered, dry woodshed is ready with a blanket and bowls. Please let us know in advance.</p>
<p>In summer the goods cableway helps with supplies, but the helicopter remains essential: please take your rubbish back down to the valley.</p>""",
        team=dict(titolo="The hut keeper", img=("fabio", "Fabio Merzaghi in the kitchen with freshly baked cakes")),
        accessi="""<p>In summer the hut is easy to reach on foot, mostly on family-friendly paths. In winter you climb on skis through Val Camadra and over the Greina Pass (5-6 h), only with settled snow and once the side slopes have discharged.</p>
<ul>
<li>From Lago di Luzzone, Alpe Garzott: 2 h.</li>
<li>From Lago di Luzzone, dam: 3 h 30.</li>
<li>From Ghirone via Lago di Luzzone: 4 h 30; through Val Camadra: 6 h.</li>
<li>From Pian Geirètt: 3 h 30.</li>
<li>From Vrin: 5 h; from Vals: 7-8 h.</li>
</ul>
<p><strong>By public transport:</strong> train and bus to Ghirone, Aquilesco; then the Autolinee Bleniesi <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a> to Lago di Luzzone or Pian Geirètt, daily in July and August, at weekends only in September.</p>
<p><strong>By car:</strong> A2 to Biasca, then towards the Lukmanier Pass to Campo Blenio and Ghirone; up to the Luzzone dam and along the lake to Alpe Garzott. Free parking in Ghirone-Aquilesco and at the dam (with toilets; Ristorante Luzzone from April to October); at Alpe Garzott, where you can buy excellent cheese, there are only a few spaces: arrive early or share cars.</p>
<p><strong>Taxi:</strong> Poglia Mirko (Olivone) <a class="num" href="tel:+41794440712">+41 79 444 07 12</a>; <a href="https://www.taxiriviera.ch/" rel="noopener">Taxi Riviera</a> (Biasca) <a class="num" href="tel:+41794136868">+41 79 413 68 68</a>.</p>
<p><strong>Traverses to other huts:</strong> <a href="https://www.terrihuette.ch/" rel="noopener">Terri</a> 2 h 30; <a href="https://www.satlucomagno.ch/wordpress/capanna-scaletta/" rel="noopener">Scaletta</a> 2 h; <a href="https://www.capannabovarina.ch/" rel="noopener">Bovarina</a> 5 h; <a href="en/adula.html">Adula CAS</a> 5 h; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 6 h; <a href="https://www.medelserhuette.ch/" rel="noopener">Medelser Hütte</a> 6 h; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 7 h; <a href="https://www.rifugioscaradra.ch/" rel="noopener">Rifugio Scaradra</a> 3 h. Routes on <a href="https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=10&amp;E=2720474&amp;N=1161992&amp;layers=Wanderland%2CStation%2CAccomodation" rel="noopener">SwitzerlandMobility</a>.</p>
<p>Maps: Swiss map 1:25,000 sheet 1233 Greina; ski touring map 256 S.</p>""",
        attivita="""<p>The Greina is a unique high plateau between Ticino and Graubünden, almost 6 km long and over 2200 m high: a protected alpine tundra in the Federal Inventory of Landscapes of National Importance. It is unspoilt: the only signs of people are the Crap la Crusch and the Crap pass, where an iron cross recalls that the Greina was already a route and pastureland in Roman times and in the Middle Ages.</p>
<p>Countless springs rise here, forming meanders, oxbows and marshes on the continental divide: the Brenno della Greina flows to the Mediterranean, the Rein da Sumvitg to the North Sea. It is the queen of contrasts, between the white of the glaciers, the black of the schists and the green of the tundra, with the rock arch about forty metres long, the peat bogs, the small rock towers and the sinkholes. <strong>To really feel its magic, stay two days or more.</strong></p>""",
        pagine=[
            dict(file="giro-greina", titolo="Greina circuit", foto="giro-greina",
                 lead="The Greina in a day: from the Luzzone to the hut, over the Greina Pass and down to the Scaletta, with the Bus alpin.",
                 img=("piano-greina", "The Greina plain with the stream among meadows and mountains"),
                 corpo="""<p>Ghirone, Lago di Luzzone, Capanna Michela Motterascio, Crap la Crusch, Greina Pass, Capanna Scaletta, Pian Geirètt, Ghirone: for those who have only one day, the circuit can be done in summer in 6-7 hours’ walking, thanks to the <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a>.</p>
<p>From the stop follow the unsurfaced road along <strong>Lago di Luzzone</strong>. At Alpe Garzott a well waymarked path enters the “fjord”, a narrow gorge; the path was improved in 2017 with the support of the Patriziato di Aquila. After a modern bridge you climb among open larches to the Monti di Rafüsc (1691 m) and over steep grassy slopes to the Trachee plain (1947 m). Over an old wooden footbridge across the Ri di Motterascio and a last climb in zigzags you reach the <strong>hut</strong> (2172 m, about 3 h).</p>
<p>Carry on to <strong>Alpe Motterascio</strong>: climb a metal staircase (with dogs, go round it on the right on the cows’ path) and cross the pasture between streams and boggy ground to the wide saddle of the <strong>Crap la Crusch</strong> (2268 m, about 1 h), with a fantastic view over the Plaun la Greina.</p>
<p>Always on the white-red-white path, climb to the <strong>Greina Pass</strong> (2355 m), along the sources of the Rhine, which flows into the North Sea, and continue to <strong>Capanna Scaletta</strong> (2205 m, 2 h), looking down on the meanders of the Brenno, which by contrast flows into the Mediterranean. If you want to see the <strong>Greina arch</strong>, take a short detour along the meanders; from the arch a white-blue-white path leads to the Scaletta, only for experienced hikers and without ice or snow; otherwise return to the white-red-white path (1 h). From the Scaletta the descent to <strong>Pian Geirètt</strong> is steep but short (1 h), and the Bus alpin takes you back to Ghirone.</p>
<p>The circuit also works in the opposite direction, recommended for families because the climb from Pian Geirètt is less tiring than the one from the Luzzone.</p>""",
                 dati=[("Length", "17 km"), ("Ascent", "+700 m"), ("Time", "6 h"), ("Difficulty", "T2"),
                       ("Highlights", "Alpe Garzott, Alpe Motterascio, Crap la Crusch, the watershed, the sources of the Rhine and the Brenno, small rock towers, meanders, the Greina arch")],
                 link=[("Online map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=7.09&amp;E=2717383&amp;N=1160737&amp;trackId=4244704")]),
            dict(file="proposte-gite", titolo="Suggested trips",
                 lead="Six trips from the hut: Crap la Crusch, Piz Terri, the Greina arch, Plaun la Greina and the Via Crio.",
                 img=("crap-la-crusch", "The great boulder of the Crap la Crusch with its cross, on the Greina plain"),
                 corpo="""<p>If you have several days, these routes let you experience the magic of the Greina to the full. Almost all of them start and finish at the hut.</p>""",
                 itinerari=[
                     dict(titolo="Crap la Crusch", img=("crap-la-crusch", "The great boulder of the Crap la Crusch with its cross, on the Greina plain"),
                          testo="An easy walk to the heart of the Greina, via Alpe Motterascio and the Ri di Motterascio.",
                          dati=[("Length", "6 km"), ("Ascent", "+180 m"), ("Time", "2 h"), ("Difficulty", "T2")],
                          link=[("Route description", "docs/capanne/motterascio/a-crap-la-crusch.pdf")]),
                     dict(titolo="Piz Terri", img=("piz-terri", "The pyramid of Piz Terri in the sunlight"),
                          testo="Val Güida, Piz Terri, the Laghet la Greina, Val Canal and the Crap la Crusch.",
                          dati=[("Length", "11 km"), ("Ascent", "+1100 m"), ("Time", "6 h"), ("Difficulty", "T3-T4")],
                          link=[("Route description", "docs/capanne/motterascio/b-piz-terri.pdf")]),
                     dict(titolo="Pizzo Coroi and Capanna Scaletta", img=("arco-greina", "The natural rock arch of the Greina"),
                          testo="Pizzo Coroi, the Greina arch, the meanders, the small rock towers and the sources of the Brenno and the Rhine.",
                          dati=[("Length", "15 km"), ("Ascent", "+900 m"), ("Time", "6 h"), ("Difficulty", "T3")],
                          link=[("Route description", "docs/capanne/motterascio/c-pizzo-coroi-capanna-scaletta.pdf")]),
                     dict(titolo="Plaun la Greina and the Terrihütte", img=("plaun-la-greina", "View from above of the valleys and ridges around the Greina"),
                          testo="The sources of the Rhine, the meanders, the peat bogs, the parallel terraces, the grassy hummocks and the Muot la Greina.",
                          dati=[("Length", "13 km"), ("Ascent", "+400 m"), ("Time", "4 h"), ("Difficulty", "T2")],
                          link=[("Route description", "docs/capanne/motterascio/d-plaun-la-greina-capanna-terri.pdf")]),
                     dict(titolo="Val Larciolo", img=("val-larciolo", "Huts of Alpe Larciolo among golden autumn larches"),
                          testo="A lonely, wild variant off the waymarked paths, reaching the hut from above when coming from the Luzzone, via Alpe Coroi, Alpe Larciolo and Alpe Garzott.",
                          dati=[("Length", "7 km"), ("Ascent", "+250 m"), ("Time", "2 h"), ("Difficulty", "T2-T3")],
                          link=[("Route description", "docs/capanne/motterascio/e-val-larciolo.pdf")]),
                     dict(titolo="Via Crio, stages 7 and 8", img=("via-crio", "A hiker on a protected section among reddish rocks"),
                          testo="Two stages of the Via Crio pass by the hut.",
                          link=[("Stage 7", "https://www.viacrio.ch/tappa7"), ("Stage 8", "https://www.viacrio.ch/tappa8"),
                                ("Overview of the Via Crio", "docs/capanne/motterascio/prospettocrio.pdf"),
                                ("Elevation profile of the Via Crio", "docs/capanne/motterascio/altimetria-totale.pdf")]),
                 ]),
            dict(file="trekking-greina-alta", titolo="Greina Alta trek", foto="trekking-greina-alta",
                 lead="From Curaglia to Vals in four stages: three SAC huts, three cultures, three languages.",
                 img=("escursionisti-greina", "Hikers on a meadow heading towards the mountains"),
                 corpo="""<p>Camona da Medel, Capanna Michela Motterascio, Läntahütte: the Greina Alta trek, for intermediate to experienced hikers, leads from Curaglia to Vals, with a common denominator, the number 3. It crosses a region with 3 SAC huts, 3 cultures, 3 languages and 3 mighty peaks. If you walk the whole trek, you can ask any of the three huts for a package booking.</p>
<ul>
<li><strong>Day 1:</strong> (Disentis) Curaglia (1332 m), Val Platta, Alp Sura (1982 m), Camona da Medel (2524 m). 3 h 30, T3.</li>
<li><strong>Day 2:</strong> Camona da Medel, Fuorcla Sura da Lavaz (2703 m), Greina Pass (2355 m), Crap la Crusch (2268 m), Capanna Michela Motterascio (2172 m). 6 h, T4.</li>
<li><strong>Day 3:</strong> Capanna Michela Motterascio, Lago di Luzzone, Larecc (1633 m), Val Scaradra, Passo Soreda (2759 m), Läntatal, Läntahütte (2090 m). 7 h, T3.</li>
<li><strong>Day 4:</strong> Läntahütte, Furggelti (2712 m), Zervreilasee (1862 m), Zervreila (Vals). 5 h, T3.</li>
</ul>""",
                 dati=[("Length", "45 km"), ("Ascent", "+4200 m"), ("Time", "6-7 h a day"), ("Difficulty", "T3-T4"),
                       ("Best time", "Mid-July to early October"),
                       ("Highlights", "Val Platta, Fuorcla Sura da Lavaz, the Greina, Lago di Luzzone, Val Scaradra, Läntatal, Zervreilasee")],
                 link=[("The trek’s website", "https://greinaalta.ch/"),
                       ("Online map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=17.65&amp;E=2718864&amp;N=1162797&amp;layers=Wanderland&amp;trackId=4230099")]),
        ],
        sostenitori=dict(
            testo="Many thanks to the partners who support the hut.",
            loghi=[("Switzerland Tourism", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/"),
                   ("Ticino Tourism", "sostenitori/ticino-turismo", "https://www.ticino.ch/en/"),
                   ("Bellinzona e Valli Tourism", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/en/"),
                   ("Blenio Turismo", "sostenitori/blenio-turismo", "https://www.vallediblenio.ch/"),
                   ("Patriziato Generale di Aquila, Torre e Lottigna", "sostenitori/patriziato-aquila-torre", "https://comuneblenio.ch/Aquila")]),
        foto=[("The hut", "capanna"), ("The kitchen", "cucina"), ("The surroundings", "dintorni")],
    ),

    "montebar.html": dict(
        cartella="montebar",
        capanna="""<p>The new hut owned by CAS Ticino was inaugurated in 2016, exactly 80 years after the first building. The “Barlume” project by the architects Oliviero Piffaretti and Carlo Romano (Atelier PeR, Mendrisio), chosen from thirty entries, is a simple, cubic building in larch wood around the fireplace: a lantern in the landscape, in dialogue with the huts on the surrounding summits.</p>
<p>The dining room, the heart of the hut, has windows on all sides and up to 60 places; the terrace can be reached from the dining room and from the kitchen. On the upper floors are rooms with 2, 4 and 6 beds in bunks, with toilets on each floor; there is a workshop room for meetings, courses and schools. In the basement are the washrooms, the room open to hikers when the hut is closed and the bike room with battery charging points and a small workshop, to Bike Hotel standard.</p>
<p>Easy to reach on a dense network of hiking and mountain bike trails, with surprising nature, history and scenery, it is the ideal destination for families and schools, or for a night at the hut after a convivial dinner.</p>""",
        cucina="""<p>We cook fresh, seasonal produce from the region with passion, with Ticino cooking as our benchmark. Lunch is served from 11.30 am to 3 pm; in the afternoon there is always a soup, cold platters and cakes. Dinner is at 7 pm: in the evening please book. On request we also prepare menus for special occasions.</p>
<ul>
<li>Homemade cakes, minestrone with vegetables and pulses, Ticino polenta.</li>
<li>Cheeses from the nearby alpine pastures and Ticino cured meats.</li>
<li>Barbecue on the terrace in summer, game in autumn, cheese fondue in winter.</li>
</ul>
<p>Breakfast from 7.45 am (from 8 am in winter). Dogs are not allowed in the hut; minors are welcome when accompanied by an adult. From 10 pm please be considerate of those sleeping.</p>""",
        team=dict(titolo="The hut keepers", img=("gestori", "James Mauri and Serge Santese on the pastures in front of the hut")),
        accessi="""<p>On foot or by mountain bike the hut is easy to reach, mostly on family-friendly paths. In winter too you can get up on skis or snowshoes, but remember that conditions in the mountains can be different from those in the valley. Parking in the valley is limited: public transport is better.</p>
<ul>
<li>From Corticiasca: 1 h 30.</li>
<li>From Bidogno: 2 h.</li>
<li>From Isone through Val Serdena and over Piandanazzo: 3 h.</li>
<li>From Gola di Lago: 2 h 30.</li>
<li>From Scareglia or Signôra: 3 h 30.</li>
</ul>
<p>Routes on <a href="https://schweizmobil.ch/en/map?bgLayer=pk&amp;layers=wanderland%2Cveloland&amp;season=summer&amp;highlightPointCoordinates=2721818-1106610&amp;E=2721449&amp;N=1106526&amp;resolution=4.51" rel="noopener">SwitzerlandMobility</a>. Map: Swiss map 1:25,000 sheet 1333 Tesserete.</p>
<p><strong>Safety:</strong> in winter ice and snow make even easy sections tricky, and there is avalanche danger on steep slopes and in gullies. In summer suckler cows with calves graze here: keep your distance and keep dogs on a lead. Cyclists, please be considerate of hikers. Leave no rubbish behind and light no fires outdoors: Monte Bar was hit by devastating fires in the past.</p>""",
        attivita="""<p>The area offers countless options for mountain biking, on tarmac, unsurfaced roads and singletrails, with panoramic loops for much of the year: national routes 66, 358 and 359 are described by <a href="https://www.luganoregion.com/en/things-to-do/sport-and-nature/bike" rel="noopener">Lugano Region</a>. From the hut you can also cross the Passo San Lucio into Val Cavargna or head north into Val Serdena and to Rivera.</p>
<p>The chain stretching from Gola di Lago to the 2115 m Gazzirola is criss-crossed by easy paths. The hut is the goal and a stage of the Lugano Trekking and of national route 52; from here you can reach the Camoghè and Val Morobbia. Autumn and spring are the ideal seasons.</p>""",
        pagine=[
            dict(file="escursioni", titolo="Themed walks",
                 lead="Seven easy paths through history, nature and landscape: from the ski carriers to the wildlife.",
                 img=("escursionista-cresta", "A hiker on a grassy ridge path, with the lakes behind"),
                 corpo="""<p>Seven themed paths to discover little-known corners, often with surprising encounters and discoveries. All of them are easy (T2).</p>""",
                 itinerari=[
                     dict(titolo="The ski carriers’ path", img=("portatrici-sci", "Historical photograph of women carrying skis up through the snow"),
                          testo="It recalls the “Sherpa women” who carried the skis of the well-to-do people of Lugano, who came to Bidogno by PostBus, from the church square of San Barnaba up to the hut.",
                          dati=[("Length", "4 km"), ("Ascent", "+800 m"), ("Time", "2 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2721402&amp;N=1105567&amp;trackId=4074166"),
                                ("Route description", "docs/capanne/montebar/il-sentiero-delle-portatrici-di-sci.pdf")]),
                     dict(titolo="The Barchi path", img=("barchi", "Old stone byres on the pastures below Monte Bar"),
                          testo="From Corticiasca to the terrace of the Barchi, the typical buildings of Val Colla where the cattle stayed in spring and autumn, and which gave Monte Bar its name.",
                          dati=[("Length", "4 km"), ("Ascent", "+600 m"), ("Time", "2 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721927&amp;N=1105895&amp;trackId=4073878"),
                                ("Route description", "docs/capanne/montebar/barchi.pdf")]),
                     dict(titolo="The panoramic path", img=("tramonto-pascoli", "Pastures in the evening light, the valleys in the haze"),
                          testo="From Roveredo, where the composer Ernest Bloch lived from 1930 to 1939, up to the mayens, oases of peace.",
                          dati=[("Length", "6 km"), ("Ascent", "+900 m"), ("Time", "3 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2720510&amp;N=1105400&amp;trackId=4073853"),
                                ("Route description", "docs/capanne/montebar/panoramico.pdf")]),
                     dict(titolo="The glacier path", img=("tramonto-luganese", "The hut on the snowy slope in the evening light, with the lights of Lugano"),
                          testo="Near Gola di Lago, bogs, pools, carnivorous plants and roches moutonnées bear witness to a tongue of the Ticino glacier during the last ice age.",
                          dati=[("Length", "7 km"), ("Ascent", "+700 m"), ("Time", "3 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2719894&amp;N=1106340&amp;trackId=4074157"),
                                ("Route description", "docs/capanne/montebar/ghiacciai.pdf")]),
                     dict(titolo="The vegetation path", img=("genziane", "Purple gentians in the grass"),
                          testo="It leads through every vegetation zone, from the Insubrian chestnuts to the arctic-alpine zone on the ridge of the Cima di Moncucco.",
                          dati=[("Length", "7 km"), ("Ascent", "+800 m"), ("Time", "4 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722942&amp;N=1106858&amp;trackId=4074169"),
                                ("Route description", "docs/capanne/montebar/vegetazione.pdf")]),
                     dict(titolo="The reforestation path", img=("piantagioni", "The hut on the golden pastures of Monte Bar"),
                          testo="An easy, shady path through a protection forest planted at the end of the 19th century to safeguard the water balance in the Cassarate valley.",
                          dati=[("Length", "7 km"), ("Ascent", "+800 m"), ("Time", "4 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722222&amp;N=1106106&amp;trackId=4074163"),
                                ("Route description", "docs/capanne/montebar/piantagioni.pdf")]),
                     dict(titolo="The wildlife path", img=("cervo", "A stag bellowing on a grassy slope"),
                          testo="An easy path through the wild forest, with surprising encounters: roe deer, red deer, squirrels and wild boar.",
                          dati=[("Length", "7 km"), ("Ascent", "+200 m"), ("Time", "3 h"), ("Difficulty", "T2")],
                          link=[("Map of the route", "https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722748&amp;N=1107781&amp;trackId=4074167"),
                                ("Route description", "docs/capanne/montebar/selvaggina.pdf")]),
                 ]),
            dict(file="mountain-bike", titolo="Mountain biking",
                 lead="Panoramic loops on tarmac, unsurfaced roads and singletrails, with a bike room and charging points at the hut.",
                 img=("mountain-bike", "Two mountain bikers on the pastures, with Lake Lugano behind"),
                 corpo="""<p>The Monte Bar area offers countless options for mountain biking: tarmac, unsurfaced roads and singletrails alternate on panoramic loops that can be ridden for much of the year. The main routes, especially national routes 66, 358 and 359, are described on the <a href="https://www.luganoregion.com/en/things-to-do/sport-and-nature/bike" rel="noopener">Lugano Region</a> website.</p>
<p>From the hut you can also cross the Passo San Lucio into Val Cavargna or head north into Val Serdena and to Rivera.</p>
<p>The hut meets the Bike Hotel standard: a closed bike room, battery charging points and a small workshop. We ask all cyclists to be considerate of hikers.</p>"""),
            dict(file="curiosita", titolo="Did you know?",
                 lead="The origin of the name, the lost forests, the “Sherpa women” and the cup-marked stones of Monte Bar.",
                 img=("valle-colla", "View over the valleys and the Lugano area from the slopes of Monte Bar"),
                 itinerari=[
                     dict(titolo="The origin of the name", img=("valle-colla", "View over the valleys and the Lugano area from the slopes of Monte Bar"),
                          testo="Over the last two million years the area has risen in three phases, forming three terraces: that of the villages, that of the “Barchi” and that of the alpine pastures. The Barchi, typical of Val Colla and Capriasca, were byres with a hayloft near the village, not lived in: the women climbed up twice a day to milk, and the milk was made into cheese and butter at home. From “barc” comes the name Monte Bar."),
                     dict(titolo="The lost forest", img=("bosco-nebbia", "Forests and pastures rising out of a sea of fog"),
                          testo="Monte Bar was once wooded. After the uprisings in Milan in 1848, Austria expelled Ticino emigrants from Lombardy and closed the borders: the seasonal workers who came home made the famine worse, and large areas of forest were cleared or burnt for more fields and pastures. The mountain became bare; after the severe floods of 1896 the slopes were reforested on a large scale against erosion, as you can still see today."),
                     dict(titolo="A journey through nature", img=("ellebori", "Christmas roses in flower against the light"),
                          testo="In the last ice age the ice stayed below 1200 m: the ice-free summits were a real Noah’s ark for plants and animals, and between Caval Drossa and the Gazzirola you find species older than the ice ages, next to arctic plants driven this far by the cold. In a small area you go from chestnuts through beech and conifer forest to lichens, mosses and alpine flora on the summits."),
                     dict(titolo="The “Sherpa women” of Ticino", img=("portatrici-storica", "Historical photograph of carriers in a line on a snow slope"),
                          testo="When the first hut was built in 1936, the women of Bidogno carried the building materials up to the site in baskets on their backs; afterwards they carried the skis of the people of Lugano from the church square to the hut, for 50 centimes a pair. They also carried up young trees for reforestation, gathered leaves and ferns as bedding for the byres and, in the First World War, took food to the soldiers as far as the Camoghè."),
                     dict(titolo="Cup-marked stones and rock carvings", img=("masso-coppellare", "A man looking at the marks on a cup-marked stone in the woods"),
                          testo="On Monte Bar many rocks bear carved marks: cups, grooves, crosses, footprints, stone circles. Perhaps boundary markers, places of sun worship or pilgrimage, or hollows for rainwater and burning oil. Worth seeing are the boundary stone between Bidogno and Corticiasca, the rock of Gola di Lago, the “Motarell de la Stria” in Roveredo, the “Gigante” and “Ul pé del Crist” in Lelgio, the “Balena bianca” in Caslasc, the boulders of Pian di Sotto and the Madonna stone of Borisio."),
                 ]),
        ],
        storia=dict(
            file="storia", titolo="History of the hut", foto="storia",
            lead="From the first ski school in Ticino in 1935, via the hut of 1936, to the new “Barlume” hut of 2016.",
            img=("capanna-1936", "Historical photograph of the first stone hut with skiers in the snow"),
            corpo="""<p>After the experience on the Monti di Condra, in 1935 the CAS was given the alpine hut of Alpe Musgatina as winter quarters for the first ski school in the canton of Ticino, with the instructors Tita Calvi and Aldo Balmelli.</p>
<p>It was such a success that in 1936, for the fiftieth anniversary of the Ticino Section, a hut was built on Monte Bar; the building site gave work to the valley’s many seasonal emigrants. The hut quickly became the destination of many groups of skiers: on Sundays there were up to 300 people on the slopes. The Sci Club Lugano took over the winter management, and the Monte Bar giant slalom was a great success. In summer the hut was a base camp for the surrounding summits.</p>
<p>In 2013 the section decided to build a new hut: the 1936 hut, improved in 1993, by then had serious problems with logistics, safety and supplies. The aim was a modern, practical and ecological building with the character of a classic mountain hut. The project was developed with the municipality of Capriasca (Areaviva project) and various local partners, to enhance the whole region.</p>
<p>The 2014 competition, with thirty entries, was won by “Barlume” by the architects Oliviero Piffaretti and Carlo Romano (Atelier PeR, Mendrisio): a simple, cubic wooden building around the fireplace as a symbol of meeting. The mountain remains the defining element, and the hut is a lantern in the landscape. Inaugurated in 2016, 80 years after the first hut, at 1602 m on the south-facing pastures, it is perhaps the finest terrace over Lugano, the Prealps, the Apennines with Monviso, Monte Rosa and the Ticino Alps, with unforgettable sunsets.</p>
<p><a href="https://www.simonemengani.ch/nuovo-servizio-fotografico-capanna-monte-bar/" rel="noopener">Photos of the construction by Simone Mengani</a></p>"""),
        sostenitori=dict(
            testo="The new hut was made possible by these supporters and more than 300 friends, public and private, who contributed to building it. Thank you very much!",
            loghi=[("Republic and Canton of Ticino", "cantone-ticino"), ("Swisslos", "swisslos"), ("City of Lugano", "citta-di-lugano"),
                   ("Municipality of Capriasca", "comune-di-capriasca"), ("Banca Raiffeisen del Cassarate", "raiffeisen"), ("BancaStato", "bancastato"),
                   ("Cornèr Banca", "corner-banca"), ("EFG", "efg"), ("Lugano Turismo", "lugano-turismo"), ("Revifida", "revifida"),
                   ("Ernst Göhner Stiftung", "ernst-gohner-stiftung"), ("Lambertini, Ernst & Partners", "lambertini-ernst-partners"),
                   ("Blue Planet", "blue-planet"), ("The North Face and VF", "the-north-face-vf"), ("Ente regionale per lo sviluppo del Luganese", "ersl")]),
        foto=[("The hut", "capanna"), ("The kitchen", "cucina"), ("The surroundings", "dintorni")],
    ),

    "baitadelluca.html": dict(
        cartella="baitadelluca",
        capanna_titolo="The baita",
        capanna="""<p>The baita has 16 beds in two rooms of 4 and 12 places, a common room with a gas kitchen and fireplace, hot water and a shower; the light comes from solar panels. Crockery and pans are provided, and drinks are available in limited quantities. Moderate reception, no Wi-Fi and no telephone.</p>
<p>It is not staffed: the door is locked and you receive the code from the manager. Quick and easy to reach, it is also used for courses, training days or simply for a dinner together.</p>""",
        accessi="""<ul>
<li>From Rosone (bus): 45 min, +270 m, T2 (<a href="https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2722290&amp;N=1102884&amp;layers=Wanderland%2CStation&amp;trackId=5273099" rel="noopener">route</a>).</li>
<li>From Sonvico (bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721523&amp;N=1102174&amp;layers=Wanderland%2CStation&amp;trackId=5273106" rel="noopener">route</a>).</li>
<li>From Villa Luganese (bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=en&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721748&amp;N=1101916&amp;layers=Wanderland%2CStation&amp;trackId=5273108" rel="noopener">route</a>).</li>
</ul>
<p>Map: Swiss map 1:25,000 sheet 1333 Tesserete.</p>""",
        pagine=[
            dict(file="attivita", titolo="Hiking and climbing",
                 lead="Hikes to the surrounding summits and huts, over 200 routes on the limestone of the Denti della Vecchia and the Lugano Bike 66.",
                 img=("sentiero-denti", "A hiker on the path below the rock towers of the Denti della Vecchia"),
                 itinerari=[
                     dict(titolo="Hiking", img=("sentiero-denti", "A hiker on the path below the rock towers of the Denti della Vecchia"),
                          testo="From the baita to Alpe Bolla 3 h, to Villa Luganese 3 h, to the summit of the Fojorina 4 h; from Brè to the baita 4-5 h; from the baita to Capanna San Lucio 4 h and to <a href=\"en/montebar.html\">Capanna Monte Bar</a> 6 h, or 9 h over the summits of the Fojorina and the Gazzirola.",
                          link=[("From the archive, 1997: Prealpi ticinesi 5, from the Passo San Jorio to Monte Generoso", "docs/capanne/baitadelluca/baita-del-luca-prealpi-ticinesi-5-passo-s-jorio-generoso.pdf")]),
                     dict(titolo="Climbing", img=("arrampicata-denti", "Climbers on the limestone slabs of the Denti della Vecchia"),
                          testo="The Denti della Vecchia are a climbing paradise with over 200 routes on limestone. The Gruppo Scoiattoli guidebook is online at <a href=\"https://scoiattoli.ch/\" rel=\"noopener\">scoiattoli.ch</a>; a printed copy is also kept at the baita for reference.",
                          link=[("Denti della Vecchia climbing guide (Gruppo Scoiattoli)", "https://scoiattoli.ch/wp-content/uploads/2020/06/GUIDA-DENTI-DELLA-VECCHIA-.pdf"),
                                ("Denti della Vecchia: new routes 2023", "docs/capanne/baitadelluca/denti-news-2023.pdf"),
                                ("Denti della Vecchia: Nirvana 2023", "docs/capanne/baitadelluca/denti-nirvana-news-2023.pdf"),
                                ("Denti della Vecchia: Paléo 2023", "docs/capanne/baitadelluca/denti-paleo-news-2023.pdf")]),
                     dict(titolo="Mountain biking", img=("mountain-bike", "A mountain biker on a forest trail"),
                          testo="Several routes cross the surrounding area, and the baita is very close to the Lugano Bike 66 route.",
                          link=[("Mountain biking on Lugano Region", "https://www.luganoregion.com/en/things-to-do/sport-and-nature/bike")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Many thanks to the partners who support the baita.",
            loghi=[("Switzerland Tourism", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/"),
                   ("Ticino Tourism", "sostenitori/ticino-turismo", "https://www.ticino.ch/en/"),
                   ("Lugano Region", "sostenitori/lugano-region", "https://www.luganoregion.com/en")]),
        foto=[("The baita", "capanna"), ("The surroundings", "dintorni")],
        foto_lead="The baita and the surroundings",
    ),
}
