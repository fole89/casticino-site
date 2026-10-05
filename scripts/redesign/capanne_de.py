"""Versione tedesca delle pagine capanna: stessa struttura di capanne.py (CONTENUTI) e dei dati di pages.py (HUT_PAGES, HUTS).

Le pagine tedesche si generano in de/ (de/campotencia.html, de/capanne/<cartella>/<pagina>.html).
I link ad altre pagine tradotte si scrivono già con de/ davanti (es. "de/motterascio.html"); quelli a pagine solo in
italiano (news, attività, PDF) restano senza. Immagini, gallerie e PDF sono gli stessi della versione italiana.
Traduzione da far rileggere a chi parla tedesco."""
from capanne import PRENOTA  # noqa: F401  (stesso formato del link di prenotazione)

CT_DOC = "docs/capanne/campotencia/"

# testi di HUT_PAGES (pages.py) in tedesco: sostituiscono quelli italiani, il resto (quota, foto, contatti…) resta uguale
HUT_DE = {
    "campotencia.html": dict(
        where="Val Piumogna, Leventina", custody="Mitte Juni bis Mitte Oktober",
        description="Capanna Campo Tencia, 2140 m, im Val Piumogna (Leventina): 80 Schlafplätze, bewartet von Mitte Juni bis Mitte Oktober. Kontakt und Reservation.",
        intro="Auf einer Terrasse hoch über dem Val Piumogna gelegen, ist sie der ideale Ausgangspunkt für Wanderungen, Übergänge zu anderen Hütten und Besteigungen wie die des Pizzo Campo Tencia, mit 3072 m der höchste Gipfel, der ganz auf Tessiner Boden liegt.",
        stay=[("Öffnung", "Ganzjährig"),
              ("Bewartet", "Mitte Juni bis Mitte Oktober; im Winter nicht bewartet, die Reservation ist aber obligatorisch; für grosse Gruppen kann die Hütte nach Absprache mit den Hüttenwarten geöffnet werden"),
              ("Schlafplätze", "80"),
              ("Verpflegung", "Warme Küche, den ganzen Tag vom Hüttenwart serviert"),
              ("Winterraum", "Immer offen, mit Getränken und Brennholz")],
        reach=[("Sommerzugang", "Ab Dalpe 3 h; ab Lago Tremorgio (Seilbahn ab Rodi) 3 h 30; ab Fusio über den Passo Campolungo 6 h"),
               ("Winterzugang", "Ab Dalpe 3 h, mit Ski durch das Val Piumogna"),
               ("Karte", 'LK 1272 Campo Tencia, Koordinaten <span class="num">699.430 / 144.480</span>')],
        contact=[("Hüttenwarte", "Valeria Grandi und Paco Porcu"),
                 ("Telefon Hütte", '<a class="num" href="tel:+41918671544">+41 91 867 15 44</a>'),
                 ("Mobile", '<a class="num" href="tel:+41767212572">+41 76 721 25 72</a>'),
                 ("E-Mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "cristallina.html": dict(
        where="Passo Cristallina, Valle Bedretto", custody="Juni bis Mitte Oktober; im Winter an Wochenenden und Feiertagen",
        description="Capanna Cristallina, 2575 m, auf dem Cristallinapass zwischen Leventina und Maggiatal: 100 Schlafplätze, bewartet von Juni bis Mitte Oktober und im Winter an Wochenenden und Feiertagen. Kontakt und Reservation.",
        intro="Von den Architekten Baserga und Mozzetti entworfen und 2003 eröffnet, ist sie die erste moderne Hütte des Schweizer Alpen-Clubs. Sie steht auf dem Pass, an einer strategischen Stelle zwischen Leventina und Maggiatal: aussichtsreiche Etappe auf den Übergängen nach Robiei, zum Naret, zum Campo Tencia und zum San Giacomo. Die Seenrunde am Cristallina, an einem oder zwei Tagen, eignet sich auch für Familien; in einer Stunde erreicht man den Cristallina und die Cima di Lago. Im Winter, vor allem von Norden her erreichbar, öffnen sich herrliche Hänge ins Bedrettotal, nach Robiei und ins Val Formazza.",
        stay=[("Öffnung", "Immer offen und zugänglich"),
              ("Bewartet", "Juni bis Mitte Oktober; im Winter, von Dezember bis Ende April, bei guten Verhältnissen, an Wochenenden, Feiertagen und für Gruppen"),
              ("Schlafplätze", "100"),
              ("Verpflegung", "Den ganzen Tag vom Hüttenwart zubereitet"),
              ("Getränke", "Auch ohne Hüttenwart erhältlich")],
        reach=[("Sommerzugang", "Ab Ossasco 3 h 30; ab Robiei 3 h; ab Lago del Narèt 2 h 30; ab Passo San Giacomo 4 h"),
               ("Winterzugang", "Ab Ossasco 3 h; ab All’Acqua 4 h"),
               ("Karte", 'LK 1251 Bedretto, Koordinaten <span class="num">683.550 / 147.300</span>')],
        contact=[("Hüttenwart", "Emanuele Vellati"),
                 ("Telefon", '<a class="num" href="tel:+41918692330">+41 91 869 23 30</a>'),
                 ("E-Mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "adula.html": dict(
        where="Oberes Val Carassino, Val Soi, Blenio", custody="Ende Mai bis Mitte Oktober",
        description="Capanna Adula, 2012 m, zwischen Val Carassino und Val Soi (Blenio): 24 Schlafplätze, ganzjährig offen, bewartet von Ende Mai bis Mitte Oktober. Kontakt und Reservation.",
        intro="Die «Bassa», wie sie seit jeher heisst, hat den Charme der Hütte von früher: Steinbau, eine Stube voller Geschichte, Schlafräume, in denen Tausende von Bergsteigern übernachtet haben, herzlicher Empfang und einheimische Küche. Von diesem Balkon über dem Bleniotal startet man zum Gipfel des Rheinwaldhorns (Adula) oder auf bequemen Wegen zu anderen Hütten; die wilden Routen im Val Carassino bieten abenteuerliches Wandern. Für weniger Ehrgeizige: ein Spaziergang im Tal, ein gutes Mittagessen und ein Nickerchen in der Sonne.",
        stay=[("Öffnung", "Ganzjährig"),
              ("Bewartet", "Ende Mai bis Mitte Oktober"),
              ("Schlafplätze", "24"),
              ("Verpflegung", "Vom Hüttenwart zubereitet; selber kochen nur im Winter oder nach Absprache mit dem Hüttenwart"),
              ("Getränke", "Auch ohne Hüttenwart erhältlich")],
        reach=[("Sommerzugang", "Ab Compietto durch das Val Carassino 2 h 40 (mit dem Mountainbike etwa 1 h); ab Dangio durch das Val Soi 3 h; ab Cusiè (Val Malvaglia) über den Passo del Laghetto 5 h"),
               ("Winterzugang", "Ab Dangio 3 h 30; ab Ghirone 5 h"),
               ("Karte", 'LK 1253 Olivone, Koordinaten <span class="num">719.510 / 150.950</span>')],
        contact=[("Hüttenwart", "Raffaele «Lele» Demaldi"),
                 ("Telefon Hütte", '<a class="num" href="tel:+41918721532">+41 91 872 15 32</a>'),
                 ("Mobile", '<a class="num" href="tel:+41795352112">+41 79 535 21 12</a>'),
                 ("E-Mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "motterascio.html": dict(
        where="Alpe Motterascio, Greina, Blenio", custody="Mitte Juni bis Mitte Oktober",
        description="Capanna Motterascio, 2172 m, am Rand der Greina (Blenio): 70 Schlafplätze, ganzjährig offen, bewartet von Mitte Juni bis Mitte Oktober. Kontakt und Reservation.",
        intro="1967 eingeweiht und 1980, 1990 und 2006 erweitert, steht sie am Rand eines aussergewöhnlichen Naturschutzgebiets: die Greina, mit ihren Sümpfen, Mooren, Alpweiden und einer unberührten Flora. Ausgangspunkt für spannende Routen, allen voran zum Greina-Bogen, dem grössten Felsbogen im Tessin.",
        stay=[("Öffnung", "Ganzjährig"),
              ("Bewartet", "Mitte Juni bis Mitte Oktober (2026 vom 13. Juni bis 10. Oktober); im Winter der Winterraum mit 10 Plätzen, auf Reservation"),
              ("Schlafplätze", "70"),
              ("Verpflegung", "Warme Mahlzeiten, den ganzen Tag von den Hüttenwarten zubereitet"),
              ("Getränke", "Auch ohne Hüttenwart erhältlich")],
        reach=[("Sommerzugang", "Ab Alpe Garzott (Lago di Luzzone) 2 h; ab Staumauer Luzzone 3 h 30; ab Pian Geirètt 3 h 30; ab Ghirone durch das Val Camadra 6 h"),
               ("Winterzugang", "Ab Ghirone durch das Val Camadra und über den Greinapass, 5-6 h, nur bei gesetztem Schnee"),
               ("Karte", 'LK 1233 Greina, Koordinaten <span class="num">720.075 / 161.425</span>')],
        contact=[("Hüttenwart", "Fabio Merzaghi"),
                 ("Reservation", '<a class="num" href="tel:+41918721622">+41 91 872 16 22</a> (Mitte Juni bis Mitte Oktober)'),
                 ("Mobile", '<a class="num" href="tel:+41797276905">+41 79 727 69 05</a>'),
                 ("E-Mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "montebar.html": dict(
        where="Alta Capriasca, Region Lugano", custody="ganzjährig",
        description="Capanna Monte Bar, 1602 m, in der Alta Capriasca: 42 Schlafplätze in Zimmern mit 2, 4 und 6 Betten, ganzjährig bewartet, Bike-Hotel-Standard. Kontakt und Reservation.",
        intro="Auf einer aussergewöhnlich schönen Kuppe, mit 180-Grad-Blick von den Denti della Vecchia bis zum Tamaro und im Westen auf die Walliser Viertausender von den Mischabel bis zum Monte Rosa. Im Herbst 2016 neu gebaut: Zimmer mit 2, 4 und 6 Betten, Toiletten auf den Etagen, Speisesaal für rund 80 Personen, Sitzungszimmer für 20, grosse Terrasse und ein geschlossener Raum mit E-Bike-Ladestationen und kleiner Werkstatt nach Bike-Hotel-Standard.",
        stay=[("Öffnung", "Ganzjährig; auf Anfrage auch für Anlässe, Abend- und Mittagessen"),
              ("Bewartet", "Von Mai bis Anfang November täglich; im Winter von Freitagmittag bis Sonntagmittag, an Feiertagen und in den Schulferien"),
              ("Schlafplätze", "42, in Zimmern mit 2, 4 und 6 Betten"),
              ("Verpflegung", "Regionale Küche mit Produkten aus der Gegend; besondere Menüs auf Reservation"),
              ("Ohne Hüttenwarte", "Die Hütte ist geschlossen; offen bleibt nur ein kleiner Vorraum für Notfälle")],
        reach=[("Sommerzugang", "Ab Corticiasca 1 h 30; ab Bidogno 2 h; ab Isone durch das Val Serdena und über Piandanazzo 3 h; ab Gola di Lago 2 h 30"),
               ("Mountainbike", "Forststrasse Bidogno-Rompiago mit Abfahrt nach Scareglia oder Signôra; Piandanazzo-Al Matro-Serdena-Isone; Piandanazzo-Alpe Pietra Rossa-San Lucio-Bogno"),
               ("Winterzugang", "Ab Corticiasca und ab Gola di Lago"),
               ("Karte", 'LK 1333 Tesserete, Koordinaten <span class="num">721.800 / 106.610</span>')],
        contact=[("Hüttenwarte", "James Mauri und Serge Santese"),
                 ("Telefon", '<a class="num" href="tel:+41919663322">+41 91 966 33 22</a>'),
                 ("E-Mail", '<a href="mailto:montebar@casticino.ch">montebar@casticino.ch</a>')]),
    "baitadelluca.html": dict(
        where="Cioascio, Sonvico", custody="auf Reservation",
        description="Baita del Luca, 1070 m, oberhalb von Sonvico am Fuss der Denti della Vecchia: 16 Schlafplätze, Selbstversorgerhütte, nur auf Reservation.",
        intro="Auf einem weiten Grashang oberhalb von Sonvico, am Fuss der Denti della Vecchia: idealer Ausgangspunkt für Wanderungen, auch mit der Familie, und zum Klettern in einer einzigartigen Landschaft.",
        stay=[("Öffnung", "Ganzjährig, nur nach Reservation"),
              ("Schlafplätze", "16"),
              ("Verpflegung", "Selbstversorgung, Küche vorhanden"),
              ("Getränke", "In beschränkter Menge erhältlich"),
              ("Reservation", "Den Zugangscode erhalten Sie nach der Vorauszahlung")],
        reach=[("Zugang", "Ab Rosone 45 min; ab Lovarescia (oberhalb von Sonvico) 60 min; ab Car und Luss (Villa Luganese) 60 min"),
               ("Karte", 'LK 1333 Tesserete, Koordinaten <span class="num">722.980 / 102.600</span>')],
        contact=[("Verantwortliche", "Priska Deluigi, 6960 Odogno"),
                 ("Mobile", '<a class="num" href="tel:+41792033084">+41 79 203 30 84</a>'),
                 ("E-Mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Reservation", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}

# schede della home tedesca e delle «altre capanne»: stessi campi di HUTS in pages.py
HUTS_DE = [
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Bewartet Juni–Okt.", "Auf einer Terrasse über dem Val Piumogna, Ausgangspunkt für den Pizzo Campo Tencia, den höchsten ganz im Tessin gelegenen Gipfel.", "80 Plätze", "Dalpe 3 h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Valle Bedretto", "Bewartet Sommer und Winter", "Auf dem gleichnamigen Pass zwischen Leventina und Maggiatal. 2003 eröffnet, die erste moderne SAC-Hütte.", "100 Plätze", "Ossasco 3 h 30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Bewartet Mai–Okt.", "Die klassische Steinhütte hoch über dem Bleniotal: Geschichte, herzlicher Empfang und einheimische Küche.", "24 Plätze", "Compietto 2 h 40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Bewartet Juni–Okt.", "Am Rand der geschützten Greina-Ebene: Moore, Alpweiden und der grösste natürliche Felsbogen im Tessin.", "70 Plätze", "Garzott 2 h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "Ganzjährig", "Der Balkon über Lugano, 2016 neu gebaut: Blick vom Monte Rosa bis zu den Denti della Vecchia, Bike-Hotel-Standard.", "42 Plätze", "Corticiasca 1 h 30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Auf Reservation", "Oberhalb von Sonvico, am Fuss der Denti della Vecchia. Ideal für Familien und zum Klettern.", "16 Plätze, Selbstversorger", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

CONTENUTI_DE = {
    "campotencia.html": dict(
        cartella="campotencia",
        capanna="""<p>Die erste Hütte der Tessiner Berge wurde 1912 am Fuss des gleichnamigen Gipfels gebaut, auf der Leventiner Seite im oberen Val Piumogna. Sie ist ein Basislager für Familien, Wanderer und Bergsteiger: Naturwanderungen, der Lago Morghirolo ganz in der Nähe, die Klettergärten und die grossen Touren der Campo-Tencia-Gruppe mit der klassischen Überschreitung der Cresta dei Corni.</p>
<p>Das heutige Gebäude, entworfen vom Sektionsarchitekten Oscar Hofmann und 1977 eingeweiht, hat drei Stockwerke: im Erdgeschoss Eingang, Schuhraum, Toiletten und Keller; im ersten Stock eine helle Stube mit 70 Plätzen und die Küche; im zweiten rund 70 Schlafplätze in 7 Lagern, einige mit 4 bis 8 Plätzen, ideal für Familien.</p>
<p>Die Betten haben Duvets; <strong>der Hüttenschlafsack ist obligatorisch</strong>. Die Hütte hat den Charakter der 1980er-Jahre bewahrt: keine Einzelzimmer mit Bad und keine Föhns!</p>""",
        cucina="""<p>Ein einfaches, ehrliches Angebot mit einheimischer, aber nicht nur tessinischer Prägung: kalte Teller mit Wurst und Käse aus der Region, Suppen, frische Gnocchi und Polenta mit verschiedenen Beilagen, je nach Saison und Angebot.</p>
<p>Für Übernachtungsgäste kochen wir Spezialitäten aus der Gegend, mit einem Menü, das je nach Anlass wechselt, inspiriert von den Bergen und mehr.</p>
<p>Vegetarier, Veganer und Gäste mit besonderer Ernährung sind willkommen: Bitte melden Sie sich frühzeitig, damit wir alle zufriedenstellen können.</p>""",
        team=dict(img=("guardiani", "Valeria und Paco, Hüttenwarte der Capanna Campo Tencia"),
                  testo="""<p>Wir sehen uns als fröhliche, positive Menschen voller Energie, mit viel Lust anzupacken. Früher führten wir eine Osteria mit Unterkunft; seit 2024 sind wir die Hüttenwarte der Capanna Campo Tencia.</p>
<p>Wir sind viel gereist und haben wunderbare Orte entdeckt, aber auch gemerkt, wie schön es ist, in unsere Berge zurückzukehren: Hier fühlen wir uns zu Hause. Nach vielen Jahren in der Hotellerie hat uns der Ruf der Berge höher hinaufgeführt, um diesen Traum zu verwirklichen.</p>
<p>Während der Saison helfen uns Freunde und Freiwillige. Wir freuen uns darauf, Sie in der Hütte zu begrüssen!</p>
<p><strong>Valeria und Paco</strong></p>"""),
        tariffe=[
            ("Mitglieder SAC/FAT und Gegenrechtsvereine", "Übernachtung mit Halbpension (Abendessen und Frühstück)",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 45.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 58.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 75.–"), ("Bergführer IFMGA", "Fr. 50.–")]),
            ("Nichtmitglieder", "Übernachtung mit Halbpension (Abendessen und Frühstück)",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 50.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 63.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 85.–")]),
            ("Familien und Gruppen", "Familienrabatt unter der Woche (Sonntag-Donnerstag) und Angebot für Jugendgruppen: Schulen, Pfadi, J+S-Kurse (Montag-Donnerstag)",
             [("Familien: Rabatt pro Kind unter 15 Jahren", "Fr. 5.–"), ("Gruppen: Kinder unter 15 Jahren", "Fr. 40.–"),
              ("Gruppen: Jugendliche von 15 bis 18 Jahren", "Fr. 45.–")]),
            ("Extras", "Aus hygienischen Gründen ist der Hüttenschlafsack obligatorisch",
             [("Lunch", "Fr. 12.–"), ("Tagestee (1 l)", "Fr. 4.–"), ("Dusche (pro Person)", "Fr. 5.–"),
              ("Einweg-Hüttenschlafsack", "Fr. 7.–")]),
        ],
        prenotare=f"""<ul>
<li><strong>Reservation obligatorisch</strong>, online mit der Schaltfläche «Reservieren».</li>
<li>Kostenlose Annullierung bis 18 Uhr <strong>zwei Tage vor</strong> dem reservierten Datum.</li>
<li>Keine Reservationen oder Anfragen über soziale Medien: Rufen Sie uns bitte an.</li>
</ul>
<p><a class="file-link" href="{CT_DOC}disposizioni-per-gli-ospiti.pdf">Hinweise für die Gäste</a></p>
<p><a class="file-link" href="{CT_DOC}2020-cgc-capanne-cas-it.pdf">Allgemeine Geschäftsbedingungen der SAC-Hütten</a></p>""",
        accessi=f"""<p>Im Sommer erreicht man die Hütte bequem zu Fuss, auf familienfreundlichen Wegen; im Winter mit Ski ab Dalpe durch das Val Piumogna.</p>
<p><strong>Nach Dalpe:</strong> von Norden oder Süden auf der A2, Ausfahrt Rodi-Quinto; mit dem öffentlichen Verkehr bis Rodi und von dort mit dem <a href="https://www.postauto.ch/de" rel="noopener">Postauto</a>.</p>
<ul>
<li>Ab Dalpe (1192 m): 3 h.</li>
<li>Ab Lago Tremorgio (1849 m), Bergstation der Seilbahn ab Rodi: 3 h 30.</li>
<li>Ab Fusio (Val Lavizzara) über den Passo Campolungo (2318 m): 6 h.</li>
<li>Im Winter ab Dalpe: 3 h.</li>
</ul>
<p>Karten: LK 1:25’000 Blatt 1272 Campo Tencia; LK 1:50’000 Blatt 266 S Valle Leventina. Routen auf <a href="https://map.schweizmobil.ch/?lang=de&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2699408&amp;N=1146376" rel="noopener">SchweizMobil</a>.</p>
<p><a class="file-link" href="{CT_DOC}aet-pieghevole-tremorgio.pdf">Seilbahn Rodi-Tremorgio: Fahrplan und Preise</a></p>""",
        attivita="""<p>Nicht nur der Campo Tencia! Das Val Piumogna ist ideal, um die Berge in allen Facetten und in jedem Alter zu erleben: das eidgenössische Jagdbanngebiet, die Alpen, der geologische Weg am Campolungo, der Disthen am Forno und die Bergseen, die auch an heissen Tagen erfrischen.</p>
<p>Das Massiv bietet zahlreiche Routen: die klassische Cresta dei Corni, Besteigungen wie die des Pizzo Campo Tencia, Übergänge zu den Hütten Leìt, Sponda, Barone und Garzonera. Die Hütte liegt auf halber Strecke der <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, der 100 km langen Route vom Nufenenpass zum Lago Maggiore. Die Klettergärten bei der Hütte sind ideal für Kurse mit Kindern und Anfängern; im Winter gibt es anspruchsvolle Skitouren und Eisfälle.</p>""",
        storia=dict(
            file="storia", titolo="Geschichte der Hütte",
            lead="Seit 1912 die erste Hütte der Tessiner Berge: erweitert, von einem Brand zerstört und schöner wieder aufgebaut.",
            img=("inaugurazione-1912", "Postkarte von der Einweihung der Hütte am 10. August 1912, mit Bergsteigern vor der Steinhütte"),
            corpo="""<p>Die Hütte wurde 1912 am Fuss des gleichnamigen Gipfels gebaut, auf der Leventiner Seite im oberen Val Piumogna. Der Name Campo Tencia ist eine Erfindung von 1858: Er bezeichnete den höchsten ganz auf Tessiner Boden gelegenen Berg (3072 m), als die berühmte Dufourkarte gezeichnet wurde. Er verbindet die Namen zweier Alpen des Patriziato di Prato, Campo und Tencia, im oberen Val Lavizzara auf der Seite des Maggiatals.</p>
<p>Am 11. August 1912 (nach einigen Archivquellen am 10. August) wurde die Hütte eingeweiht. 1932 legte Patocchi, wie immer die treibende Kraft, das Projekt für eine Erweiterung vor, und im Sommer 1933 wurde der neue Ostflügel gebaut.</p>
<figure><img src="assets/img/capanne/campotencia/costruzione.webp" alt="Männer bei der Arbeit vor der alten Steinhütte, historische Aufnahme" width="1200" height="832" loading="lazy" decoding="async"></figure>
<p>Vierzig Jahre später folgten weitere Arbeiten zur Verstärkung und Verbesserung. Am 22. August 1975 zerstörte ein schwerer Brand das Werk vieler Jahre.</p>
<p>Sofort machte man sich an den Wiederaufbau, und die Hütte entstand grösser, schöner und zweckmässiger neu. Ihre Bauweise war schweizweit eine Neuheit, das Verdienst des Architekten Oscar Hofmann: nicht mehr das kantige Bild der klassischen Berghütte, sondern ein neuartiges, leichtes und elegantes Aussehen, mit einem Tragwerk aus verkleidetem und für die Höhe isoliertem Stahl. Die neue Einweihung fand am 25. September 1977 statt.</p>
<figure><img src="assets/img/capanne/campotencia/capanna-storica.webp" alt="Die alte Steinhütte im Schnee, historische Aufnahme" width="1200" height="782" loading="lazy" decoding="async"></figure>
<p>2008 kam mit dem Nordflügel eine neue Profiküche dazu. Am 11. August 2012 wurde das 100-Jahr-Jubiläum gefeiert. 2022 sorgte eine Wasserturbine für die Stromversorgung, die Photovoltaikanlage wurde erweitert und die Abwasserreinigung erneuert.</p>"""),
        pagine=[
            dict(file="escursioni-facili", titolo="Leichte Wanderungen",
                 lead="Auf weiss-rot-weissen Wegen, zwischen Alpen, Bergseen und dem eidgenössischen Jagdbanngebiet Campo Tencia.",
                 img=("lago-morghirolo-fiori", "Blühendes Wollgras am Ufer des Lago Morghirolo"),
                 corpo="""<p>Zwischen Leìt und Tencia führen die Wanderungen durch eine wertvolle Naturlandschaft: das eidgenössische Jagdbanngebiet Campo Tencia, den geotouristischen Weg am Campolungo, die Alpen und viele Bergseen für ein Bad oder ein Picknick.</p>""",
                 itinerari=[
                     dict(titolo="Lago Morghirolo", img=("lago-morghirolo", "Der Lago Morghirolo unter den Gipfeln der Campo-Tencia-Gruppe"),
                          testo="Warum nach einer Rast in der Hütte nicht zum wunderschönen Bergsee wandern und ein erfrischendes Bad nehmen?",
                          dati=[("Länge", "1,4 km"), ("Höhendifferenz", "+250 m"), ("Zeit", "1 h hin und zurück"), ("Schwierigkeit", "T2")],
                          link=[("Routenbeschreibung", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                     dict(titolo="Lehrpfad", img=("torrente-piumogna", "Der Bach Piumogna zwischen den Wiesen des Tals"),
                          testo="Rundweg mit Start und Ziel in Piumogna, über die Capanna Campo Tencia und die Alpe Morghirolo, mit Infotafeln zur Natur. Man kann den Lago Morghirolo anhängen (etwa 1 h mehr, hin und zurück) oder in der Hütte zu Mittag essen und die Runde am Nachmittag über die Alpe Morghirolo schliessen.",
                          dati=[("Länge", "12 km"), ("Höhendifferenz", "+1300 m"), ("Zeit", "4-5 h"), ("Schwierigkeit", "T3")],
                          link=[("Online-Karte", "https://s.geo.admin.ch/151dbckh2v17"),
                                ("Routenbeschreibung", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                 ]),
            dict(file="giro-piumogna", titolo="Piumogna-Runde",
                 lead="Eine Rundtour ab Dalpe über die Hütten Leìt und Campo Tencia, in einem geschützten, blumenreichen Gebiet.",
                 img=("lago-leit", "Der Bergsee unter den Gipfeln der Campo-Tencia-Gruppe"),
                 corpo="""<p>Eine fantastische Route in einem besonders blumenreichen Gebiet, das wegen seiner Geologie national anerkannt und geschützt ist: Alpenakelei, Enziane, Anemonen, Männertreu, Alpenrosen, Berg-Hahnenfuss und Hallers Schlüsselblumen.</p>
<p>Von Dalpe steigt man durch den herrlichen Boscobello zum Passo Vanitt und auf einem schönen Panoramaweg zur Capanna Leìt. Dem See entlang geht es am Fuss des Pizzo Prèvat vorbei, eines bei Kletterern beliebten Gipfels, auch «Cervinetto» genannt. Nach dem Passo Leìt und der Bocchetta Lei di Cima sieht man die Gipfel der Campo-Tencia-Gruppe, deren höchster (3072 m) der höchste ganz im Tessin gelegene ist. Im Abstieg kommt man am Lago Morghirolo vorbei, von wo man in einer halben Stunde die Capanna Campo Tencia erreicht. Der Rückweg folgt dem Val Piumogna mit seinem schönen Bach und mehreren Alpen.</p>
<figure><img src="assets/img/capanne/campotencia/pascoli-piumogna.webp" alt="Weiden mit einem Steinmann und weiss-rot-weisser Markierung" width="1200" height="659" loading="lazy" decoding="async"></figure>
<h2>Hin und zurück ab Dalpe</h2>
<p>Ab Dalpe (mit dem Postauto ab Rodi-Fiesso oder Airolo erreichbar) folgt man dem Weg nach Boscobello, kommt an der Alpe Cadonighino vorbei und überschreitet den Passo Vanitt (2138 m). Man erreicht die Capanna Leìt und den See (2260 m) und geht weiter Richtung Capanna Campo Tencia: Nach dem Passo Leìt (2431 m) und der Bocchetta Lei di Cima (2481 m) erreicht man die Hütten von Lei di Cima (2400 m). Der neue Weg führt zum Lago Morghirolo (2264 m) und in einer halben Stunde zur Capanna Campo Tencia (2140 m) hoch über dem Val Piumogna. Im Abstieg folgt man dem Talweg bis zu den Hütten von Piumogna, dann der Strasse Richtung Boscobello; kurz nach der Brücke von Polpiano führt rechts ein Weg hinunter nach Dalpe.</p>
<p>Man kann auch in Rodi-Fiesso starten, mit der Seilbahn zum Lago Tremorgio fahren und dem Weg zur Capanna Leìt folgen, oder die Runde in umgekehrter Richtung gehen. <strong>Achtung:</strong> Die Etappe ist lang, eine Übernachtung in der Hütte ist eine gute Idee.</p>
<figure><img src="assets/img/capanne/campotencia/cascina-piumogna.webp" alt="Eine Alphütte zwischen Lärchen im Val Piumogna, im Hintergrund verschneite Gipfel" width="1200" height="900" loading="lazy" decoding="async"></figure>""",
                 dati=[("Länge", "19 km"), ("Höhendifferenz", "+1330 / −1330 m"), ("Zeit", "8 h"), ("Schwierigkeit", "T2"),
                       ("Sehenswert", "Boscobello, Capanna Leìt, Pizzo Prèvat, Lago Leìt, Hütten von Lei di Cima, Campo-Tencia-Gruppe, Lago Morghirolo, Alpen Croslina und Geira")],
                 link=[("Online-Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2700579&amp;N=1146079&amp;trackId=4267446")]),
            dict(file="escursionismo-alpino", titolo="Alpinwandern",
                 lead="Abseits der Wege: die Gipfel von Campo Tencia, Forno und Campolungo, ab T4.",
                 img=("segnavia-alpino", "Weiss-blau-weisse Markierung auf einem Felsblock, im Hintergrund die Gipfel"),
                 corpo="""<p>Die Schwierigkeiten beim Wandern sind nach der T-Skala in sechs Stufen eingeteilt, von T1 (Wandern) bis T6 (schwieriges Alpinwandern). Rund um den Campo Tencia gibt es viele Möglichkeiten: die Besteigungen des Pizzo Campo Tencia, des Pizzo Forno oder des Campolungo. Die Routen sind nur teilweise markiert, Orientierungssinn ist nötig; es kann objektive Gefahren und im Frühsommer Schneereste geben: Gehen Sie gut vorbereitet los.</p>
<p><a href="https://www.sac-cas.ch/de/ausbildung-und-sicherheit/sicher-unterwegs/sicher-unterwegs-beim-berg-und-alpinwandern/" rel="noopener">Sicher unterwegs beim Alpinwandern: die Tipps des SAC</a></p>""",
                 itinerari=[
                     dict(titolo="Pizzo Campo Tencia (3072 m) und Pizzo Croslina (3012 m)", img=("croce-campo-tencia", "Das Gipfelkreuz des Pizzo Campo Tencia"),
                          testo="Der höchste ganz im Tessin gelegene Berg verdankt seinen Namen dem rötlichen, eisenhaltigen Gestein: «tencie», also schmutzig, im Dialekt. In der Mitte des Kantons bietet er eine Rundsicht; vom Gipfel kann man ins Val Lavizzara absteigen oder die Via Alta Vallemaggia erreichen. Die Route ist grösstenteils markiert; an einigen Stellen Vorsicht vor Steinschlag, besonders wenn andere unterwegs sind. Im Frühsommer liegt Schnee in der Mulde vor der Bocchetta di Croslina. Von der Scharte (2864 m) kann man nach Norden zum Grat queren, der auf den Pizzo Croslina führt: ausgesetzte Stellen, Vorsicht vor allem im Abstieg.",
                          dati=[("Länge", "3 km"), ("Höhendifferenz", "+940 m"), ("Zeit", "3 h für den Pizzo Campo Tencia, 4 h mit dem Pizzo Croslina"),
                                ("Schwierigkeit", "T4+ Pizzo Campo Tencia, T6 mit dem Pizzo Croslina"), ("Ausrüstung", "Gute Bergschuhe")],
                          link=[("Ausführliche Beschreibung", "capanne/campotencia/tencia-croslina.html"),
                                ("Routenbeschreibung", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")]),
                     dict(titolo="Pizzo Forno (2907 m)", img=("pizzo-forno", "Pizzo Forno und Pizzo Laghetto mit den letzten Schneefeldern"),
                          testo="Die 5. Etappe der Via Idra folgt der Senda del Ghiacciaio bis zum Passo del Ghiacciaione, von wo man den Pizzo Forno besteigen kann, bevor man zum Rifugio Alpe Sponda absteigt. Die Nordseite bleibt lange verschneit: Gute Schuhe und Grödel sind sehr empfohlen.",
                          dati=[("Länge", "4,5 km"), ("Höhendifferenz", "+767 m"), ("Zeit", "3 h"), ("Schwierigkeit", "T4")],
                          link=[("Via Idra, Etappe 5", "https://www.viaidra.ch/tappa05"), ("Routenbeschreibung", CT_DOC + "d-pizzo-forno-2907-m.pdf")]),
                     dict(titolo="Pizzo Campolungo (2714 m)", img=("pizzo-campolungo", "Der Pizzo Campolungo und die Grate zum Pizzo Prèvat"),
                          testo="Vom Gipfel öffnet sich der Blick auf die Seen Leìt, Tremorgio und Morghirolo und auf den Pizzo Prèvat, das «Tessiner Matterhorn». Der Aufstieg ist nicht markiert und führt über steile Wiesen und Geröll in der Mulde vor der Alpe Lei di Cima: nicht schwierig, aber Orientierungssinn ist nötig.",
                          dati=[("Länge", "3 km"), ("Höhendifferenz", "+690 m"), ("Zeit", "2 h 30"), ("Schwierigkeit", "T4")],
                          link=[("Online-Karte", "https://s.geo.admin.ch/epntrruz341r"), ("Routenbeschreibung", CT_DOC + "c-pizzo-campolungo-2714-m.pdf")]),
                     dict(titolo="Campolungo-Runde", img=("giro-campolungo", "Ein türkisfarbener Bergsee zwischen den Graten des Campolungo"),
                          testo="Eine wilde Wanderung, alternative Verbindung zwischen der Capanna Leìt und der Campo Tencia über die Seite des Maggiatals. Teilweise unwegsames Gelände, schlechter Handyempfang und im Frühsommer Schnee an den steilen Schattenhängen.",
                          dati=[("Länge", "8 km"), ("Höhendifferenz", "+1268 / −1166 m"), ("Zeit", "6 h von Hütte zu Hütte, 7-8 h die ganze Runde"),
                                ("Schwierigkeit", "T4-T5, teilweise mit Seilen gesichert"), ("Beste Zeit", "Juli bis Ende September"),
                                ("Ausrüstung", "Gute Bergschuhe, Helm und eventuell Klettersteigset"),
                                ("Sehenswert", "Lago Morghirolo, Corte di Zaria, Seen Cantùn dal Prèvat, Pizzo del Prèvat")],
                          link=[("Routenbeschreibung", CT_DOC + "a-giro-del-campolungo.pdf")]),
                 ]),
            dict(file="cresta-dei-corni", titolo="Cresta dei Corni",
                 lead="Weder Wandern noch Bergsteigen: die luftige Gratüberschreitung vom Passo Morghirolo auf den Campo Tencia.",
                 img=("capanna-cresta-dei-corni", "Die Capanna Campo Tencia unter der Cresta dei Corni"),
                 corpo="""<p>Nicht mehr Wandern, aber auch nicht Bergsteigen: Das englische Wort «Scrambling» beschreibt die Cresta dei Corni am Campo Tencia am besten. Die Route führt vom Passo Morghirolo über den Pizzo Canà, die Tre Corni und den Pizzo Croslina auf den Gipfel des Campo Tencia: ein luftiger Weg mit atemberaubendem Blick auf die Leventina und das Val Lavizzara, erdacht und eingerichtet von Franco Demarchi, «Dema», 28 Jahre lang Hüttenwart.</p>
<p>Es ist eine hochalpine, ausgesetzte Gratroute mit Pfeilern und Felsstufen bis 25 m, gut gesichert und markiert; im Frühsommer kann Schnee liegen. <strong>Es gibt keine Fluchtwege: Gute Kondition, Schwindelfreiheit und stabiles Wetter sind nötig. Planen Sie die Zeit sorgfältig und behalten Sie genügend Reserve.</strong></p>
<h2>Route</h2>
<p>Von der Hütte steigt man auf Wegspuren zur Scharte auf 2560 m. Ab dem Sattel bleibt man meist auf der Gratschneide, mit leichter, teils gesicherter Kletterei im Wechsel mit Gehgelände. Vom Pizzo Croslina steigt man vorsichtig zur gleichnamigen Scharte ab, von wo man, wenn die Kräfte reichen, noch den Pizzo Campo Tencia besteigen kann. Abstieg über die Normalroute in etwa 1 h 30.</p>""",
                 dati=[("Länge", "8 km"), ("Höhendifferenz", "+1350 / −1190 m"), ("Zeit", "8 h von Hütte zu Hütte"),
                       ("Schwierigkeit", "T6, WS, Stellen im III. Grad"), ("Ausrüstung", "Klettergurt, Klettersteigset, Helm, eventuell ein 30-m-Seil zum Sichern")],
                 link=[("Route online", "https://s.geo.admin.ch/r94n5ne4qz11"), ("Übersicht der Cresta dei Corni", CT_DOC + "prospetto-tre-corni.pdf")],
                 foto="cresta-dei-corni"),
            dict(file="tencia-croslina", titolo="Pizzo Campo Tencia und Pizzo Croslina",
                 lead="Die höchste Pyramide aus Fels und Eis im Tessin und der Koloss, der über der Hütte thront.",
                 img=("croslina-tencia", "Die Gipfel von Pizzo Croslina und Pizzo Campo Tencia mit Schnee"),
                 corpo="""<p>Der Pizzo Campo Tencia (3072 m) ist eine aussergewöhnliche Pyramide aus Fels und Eis mit weiter Rundsicht. Der Pizzo Croslina (3012 m) erhebt sich wie ein Koloss über der Hütte; von Osten gesehen ist er dagegen eine elegante Pyramide.</p>
<p>Typisch ist die Nordseite dieses Abschnitts des Hauptkamms: Nach der Pyramide des Croslina folgen gegen Südosten regelmässig drei Gipfel, getrennt durch kaum angedeutete Sättel: der Pizzo Campo Tencia (3072 m), der mittlere Gipfel Tenca (3035 m, ohne Namen auf der Landeskarte) und der Pizzo Penca (3038 m).</p>
<h2>Route</h2>
<p>Von der Hütte geht man nach Süden den weiss-blau-weissen Markierungen nach bis zu einem Wasserfall. Links führt ein breiter Kamin zum Band, das die ganze Wand quert: Ein gut markierter, ausgesetzter Weg steigt nach Südosten zu einer leichten Rippe. Gegen Südwesten erreicht man die Mulde des Laghetto, am Fuss der Reste des Ghiacciaio Grande di Croslina. Weiter geht es über den kleinen Grat zwischen den beiden Croslina-Gletschern bis etwa 2800 m, dann nach Südwesten, leicht auf den Gletscher absteigend, zur Bocchetta di Croslina (2864 m), immer den weiss-blau-weissen Markierungen nach. Auf der Gratschneide erreicht man das Gipfelkreuz.</p>
<p>Vom Gipfel kann man zur Capanna Soveltra im Maggiatal queren, gegen Südosten auf den weiss-blau-weissen Markierungen.</p>
<p><strong>Pizzo Croslina:</strong> Von der Bocchetta di Croslina geht man nach Nordwesten den blauen Punkten nach bis zu einem Band rechts der deutlichen Geröllrinne. Teilweise ausgesetzter Aufstieg mit Felsstellen im II. Grad.</p>
<p>Für beide Gipfel erfolgt der Abstieg über die Aufstiegsroute.</p>""",
                 dati=[("Länge", "3 km"), ("Höhendifferenz", "+940 m"), ("Zeit", "3 h für den Pizzo Campo Tencia, 4 h mit dem Pizzo Croslina"),
                       ("Schwierigkeit", "T4+ Pizzo Campo Tencia, T6 mit dem Pizzo Croslina"),
                       ("Sehenswert", "Mulde des Laghetto, Ghiacciaio Grande di Croslina, das Gipfelkreuz des Campo Tencia, die Edelweiss am Croslina")],
                 link=[("Routenbeschreibung", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")],
                 foto="tencia-croslina"),
            dict(file="arrampicata", titolo="Klettern",
                 lead="Klettergärten wenige Minuten von der Hütte, vom III. Grad bis 6b: ideal zum Lernen.",
                 img=("giardino-arrampicata", "Kletterer an einer Felsplatte bei der Hütte"),
                 corpo=f"""<p>Eine ideale Gegend, um Kindern und Anfängern das Klettern beizubringen: Rund um die Hütte wurden mehrere Klettergärten eingerichtet, vom III. Grad bis zu einigen Seillängen im 6b für Anspruchsvolle.</p>
<p>Der Sektor Angolo beim See ist eigens für die Felsausbildung eingerichtet: Einseillängenrouten, Abseilstellen, Abseilen im freien Hang und eine kleine, leichte Mehrseillängenroute zum Üben. Wenige Minuten von der Hütte entfernt kann man im Sektor Cascata die Manöver auf leichten, parallelen Mehrseillängenrouten trainieren, und am Block Kape gibt es einige Einseillängenrouten.</p>
<p><a href="https://s.geo.admin.ch/na49wcdjtms7" rel="noopener">Die Sektoren auf der Karte</a></p>
<p><a class="file-link" href="{CT_DOC}volantino-arrampicata-campo-tencia.pdf">Flyer der Klettergärten</a></p>
<table>
<thead><tr><th>Sektor</th><th>Routen</th><th>Länge</th><th>Grad</th><th>Hinweise</th></tr></thead>
<tbody>
<tr><td>Cascata</td><td>4</td><td>60 m</td><td>3-4</td><td>Mehrseillängen, parallel</td></tr>
<tr><td>Kape</td><td>7</td><td>10 m</td><td>5-6c</td><td>Einseillängen</td></tr>
<tr><td>Tutto o niente</td><td>10</td><td>20 m</td><td>3-5a</td><td>Einseillängen</td></tr>
<tr><td>Disperato</td><td>6</td><td>10 m</td><td>4-5a</td><td></td></tr>
<tr><td>Onapart</td><td>3</td><td>30 m</td><td>5a-6b</td><td></td></tr>
<tr><td>Pulce di roccia</td><td>5</td><td>20 m</td><td>3-4</td><td>leichte Platten</td></tr>
<tr><td>Angolo</td><td>8</td><td>20 m</td><td>4-5a</td><td>Ausbildungsgelände</td></tr>
<tr><td>Piode</td><td>3</td><td>25 m</td><td>4-5a</td><td></td></tr>
<tr><td>Pitela</td><td>6</td><td>10-80 m</td><td>3-5a</td><td></td></tr>
<tr><td>Cresta rossa</td><td></td><td>500 m</td><td>2-4</td><td>alpine Route</td></tr>
<tr><td>Lago</td><td>1</td><td>75 m</td><td>5a</td><td></td></tr>
</tbody>
</table>
<figure><img src="assets/img/capanne/campotencia/settori-arrampicata.webp" alt="Karte der Klettersektoren rund um die Hütte und den Lago Morghirolo" width="1088" height="766" loading="lazy" decoding="async"></figure>""",
                 foto="arrampicata"),
            dict(file="inverno", titolo="Im Winter",
                 lead="Anspruchsvolle Skitouren abseits der bekannten Ziele und Eisfälle bis 200 Meter.",
                 img=("scialpinismo", "Skitourengeher in der Abfahrt auf einem weiten Schneehang, im Gegenlicht"),
                 corpo="""<h2>Skitouren</h2>
<p>Im Winter bleibt das Gebiet des Campo Tencia abseits der bekannten Ziele. Das technische, unwegsame Gelände verlangt gute Schneeverhältnisse und sicheres Können im Skitourengehen und in der Orientierung. Im Frühling findet man die Verhältnisse für sehr lohnende Touren: Pizzo Campo Tencia, Pizzo Forno und Pizzo Campolungo. Die Hütte ist nicht bewartet, die Reservation ist aber obligatorisch; für grosse Gruppen kann sie nach Absprache mit den Hüttenwarten geöffnet werden.</p>
<h2>Eisfälle</h2>
<p>In der Mulde des Buco di Cumasna auf 2000 Metern bilden sich ab Winterbeginn mächtige Eisfälle bis 200 Meter Länge und in verschiedenen Schwierigkeiten. Rechts liegt der bekannteste, die «Giovannelli», in der Rinne, über die man im Winter die Felsstufe zum oder vom Gipfel des Pizzo Campo Tencia überwindet.</p>""",
                 foto="inverno"),
        ],
        foto=[("Die Hütte", "capanna"), ("Die Küche", "cucina"), ("Die Umgebung", "dintorni")],
    ),

    "cristallina.html": dict(
        cartella="cristallina",
        capanna="""<p>Die erste moderne Hütte des Schweizer Alpen-Clubs steht auf 2575 m auf dem Cristallinapass, in einem Gebiet, das im Sommer wie im Winter zum Wandern einlädt. Im Sommer ist sie Stützpunkt für die umliegenden Gipfel und für Übergänge ins Maggiatal, ins Val Formazza und ins Gotthardgebiet; im Winter bietet die schneereiche Gegend herrliche Abfahrten und Gipfelkombinationen.</p>
<p>Sie hat 100 Schlafplätze in Kojen mit Duvets, in 6 Zimmern mit 4, 9 mit 8 und 2 Lagern mit 12 Plätzen, einen Panorama-Speisesaal mit Terrasse, Toiletten mit warmem Wasser im Haus, Dusche, Trocknungsraum und einen Schuhraum mit Hüttenschuhen. Der Hüttenschlafsack ist obligatorisch. Guter Swisscom-Empfang bei der Hütte.</p>""",
        cucina="""<p>Tagsüber einfache Gerichte für alle: Gnocchi, Ravioli, Wähen, Wurstwaren, Desserts und vieles mehr, alles in der Hütte mit lokalen Schweizer Produkten zubereitet. Für die Halbpension wechseln die Menüs je nach Wochentag, auch mit Blick auf Vegetarier. Dazu eine gute Auswahl an Weinen und Bränden.</p>
<p><strong>Wichtig:</strong> Teilen Sie uns rechtzeitig mit, wenn Sie vegetarisch oder vegan essen oder Allergien und Unverträglichkeiten haben: Wir bereiten Ihnen gerne ein passendes Menü zu.</p>
<p>Die Zimmer werden nach Eingang der Reservation und Grösse der Gruppe zugeteilt; Zimmer können nicht exklusiv reserviert werden. Wenn die Hütte bewartet ist, ist die Halbpension obligatorisch.</p>
<p>Hunde sind willkommen, aber nicht in den Zimmern und Aufenthaltsräumen: Bitte melden Sie sie vor der Ankunft an.</p>""",
        team=dict(titolo="Der Hüttenwart", img=("guardiano", "Emanuele Vellati, Hüttenwart der Capanna Cristallina, im Schnee mit dem Basodino im Hintergrund"),
                  testo="""<p>Emanuele Vellati führt die Hütte seit dem Winter 2018. Elektriker und Koch von Beruf, leitet er sie mit grosser Sorgfalt und Hingabe, wie die gepflegte Infrastruktur und die ausgezeichnete Küche zeigen. In jungen Jahren begeisterter Bergsteiger, lebt er die Berge heute jeden Tag, als Kern seiner Arbeit.</p>
<p>Im Sommer und im Winter unterstützen ihn viele Helferinnen und Helfer, Freunde und Freiwillige des CAS Ticino, die sich über ein kleines Dankeschön immer freuen. Und dann ist da noch Jack, der friedlichste und neugierigste Bewohner der Hütte, der Neuschnee fast mehr liebt als wir.</p>
<p><strong>Emanuele</strong></p>""",
                  persone=[("Jack", "Der Hüttenhund, liebt Neuschnee", "jack")]),
        tariffe=[
            ("Mitglieder SAC/FAT und Gegenrechtsvereine", "Übernachtung mit Halbpension (Abendessen und Frühstück), MWST und Kurtaxe inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 50.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 70.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 83.–"), ("Bergführer", "Fr. 55.–")]),
            ("Nichtmitglieder", "Übernachtung mit Halbpension (Abendessen und Frühstück), MWST und Kurtaxe inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 55.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 77.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 95.–")]),
            ("Familien und Gruppen", "Familienrabatt unter der Woche (Sonntag-Donnerstag) und Angebot für Jugendgruppen: Schulen, Pfadi, J+S-Kurse (Montag-Donnerstag)",
             [("Familien: Rabatt pro Kind unter 15 Jahren", "Fr. 5.–"), ("Gruppen: Kinder bis 14 Jahre", "Fr. 40.–"),
              ("Gruppen: Jugendliche von 15 bis 18 Jahren", "Fr. 50.–")]),
            ("Extras", "Aus hygienischen Gründen ist der Hüttenschlafsack obligatorisch",
             [("Lunch", "Fr. 12.–"), ("Tee in der Thermosflasche, mit dem Lunch", "inbegriffen"), ("Dusche (pro Person)", "Fr. 5.–"),
              ("Einweg-Hüttenschlafsack", "Fr. 7.–")]),
        ],
        prenotare="""<ul>
<li><strong>Nur Barzahlung in Schweizer Franken</strong>, keine Euro.</li>
<li>Reservation online mit der Schaltfläche «Reservieren»: Allergien, Unverträglichkeiten und Vegetarier bitte im entsprechenden Feld angeben.</li>
<li>Annullieren Sie bis <strong>zwei Tage vor der Ankunft</strong>, wenn nötig auch per Telefon oder E-Mail; es gilt das No-Show-Reglement.</li>
</ul>
<p><a class="file-link" href="docs/capanne/cristallina/disposizioni-per-gli-ospiti-1.pdf">Hinweise für die Gäste</a></p>
<p><a class="file-link" href="docs/capanne/cristallina/2020-condizioni-generali-it.pdf">Allgemeine Geschäftsbedingungen der SAC-Hütten</a></p>""",
        accessi="""<p>Im Sommer erreicht man die Hütte in einigen Stunden zu Fuss, meist auf familienfreundlichen Wegen; im Winter mit Ski aus dem Bedrettotal, von Robiei oder aus dem Val Formazza.</p>
<ul>
<li>Ab Ossasco: 3 h 30.</li>
<li>Ab Passo San Giacomo: 4 h.</li>
<li>Ab Robiei: 3 h.</li>
<li>Ab Lago del Narèt: 2 h 30.</li>
<li>Ab Airolo Pesciüm: 5 h.</li>
<li>Ab Capanna Poncione di Braga: 4 h.</li>
<li>Im Winter: ab Ossasco 3 h, ab All’Acqua 4 h.</li>
</ul>
<p><strong>Mit dem Auto von Norden:</strong> A2 bis Airolo, dann Richtung Nufenenpass und Bedrettotal. <strong>Von Süden:</strong> A2 bis Bellinzona, dann Locarno und Maggiatal: Val Bavona für Robiei, mit der <a href="https://www.robiei.ch/" rel="noopener">Seilbahn San Carlo-Robiei</a> (im Sommer), oder Val Lavizzara für den Narèt.</p>
<p><strong>Mit dem öffentlichen Verkehr:</strong> Zug S10 bis Airolo, dann Bus ins Bedrettotal. Taxi ab Airolo: Marchetti Taxi <a class="num" href="tel:+41918733035">+41 91 873 30 35</a>, Gotthard Taxi <a class="num" href="tel:+41787901055">+41 78 790 10 55</a>.</p>
<p><strong>Übergänge zu anderen Hütten:</strong> <a href="https://www.corno-gries.ch/?lang=de" rel="noopener">Corno Gries</a> (2338 m) 5 h; <a href="https://www.capanna-basodino.ch/" rel="noopener">Basodino</a> (2200 m) 2 h; <a href="https://www.utoelocarno.ch/" rel="noopener">Poncione di Braga</a> (1870 m) 4 h; <a href="https://www.satritom.ch/garzonera/" rel="noopener">Garzonera</a> (2000 m) 5 h, T5; <a href="https://www.rifugiomarialuisa.it/" rel="noopener">Rifugio Maria Luisa</a> (Italien, 2393 m) 5 h.</p>
<p>Karten: LK 1:25’000 Blatt 1251 Val Bedretto; Skitourenkarte 265 S Nufenenpass.</p>""",
        attivita="""<p>Der Cristallinapass ist eine natürliche Verbindung zwischen dem Gotthardmassiv und dem Maggiatal, mitten in einem Netz von Routen und Hütten: Die <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, die Via Cristallina und die Via Alta della Vallemaggia führen hier vorbei. Im Winter ist er ein Skitourenparadies, mit sicherem Schnee auch in schlechten Jahren.</p>
<p>Die Geologie erzählt von der Entstehung der Alpen: Marmor aus Meeresablagerungen neben magmatischem Gestein, unglaubliche Faltungen. Die Tierwelt ist reich: die Steinbockkolonie Richtung Cima di Lago, Gämsen, Adler, Turmfalke. Und überall Spuren menschlicher Arbeit: Alpen, Militäranlagen und grosse Wasserkraftwerke.</p>""",
        pagine=[
            dict(file="proposte-gite", titolo="Tourenvorschläge", foto="proposte-gite",
                 lead="Fünf mittelschwere Routen, von der Cima di Lago bis zur Via Idra, mit der Hütte als Stützpunkt oder Etappe.",
                 img=("pizzo-cristallina", "Blick vom Gipfel des Pizzo Cristallina auf Bergseen und Gipfel"),
                 corpo="""<p>Wer die wunderbare Gegend am Cristallina mit ihren Bergseen und der Tierwelt des Hochgebirges entdecken möchte, findet hier mittelschwere, nicht zu lange Routen, die bei der Hütte beginnen oder sie als Etappe nutzen.</p>""",
                 itinerari=[
                     dict(titolo="Cima di Lago (2832 m)", img=("cima-di-lago", "Ein Steinbock am Hang der Cima di Lago, die Route rot eingezeichnet"),
                          testo="Gipfel mit herrlicher Aussicht, auch für trittsichere Kinder ideal: Steinbockbegegnungen sind wahrscheinlich.",
                          dati=[("Länge", "4 km"), ("Höhendifferenz", "+300 m"), ("Zeit", "1 h"), ("Schwierigkeit", "T4")],
                          link=[("Routenbeschreibung", "docs/capanne/cristallina/a-cima-di-lago-2832-msm.pdf")]),
                     dict(titolo="Pizzo Cristallina (2912 m)", img=("pizzo-cristallina", "Blick vom Gipfel des Pizzo Cristallina auf Bergseen und Gipfel"),
                          testo="Der Hauptgipfel inmitten einer Reihe von Bergseen; auf dem Gipfel steht noch das Rifugio Camosci, letzter Zeuge der Kriegszeit in der Gegend. Im letzten Hang auf Steinschlag achten, wenn andere unterwegs sind; das Biwak nur mit grosser Vorsicht betreten, Absturzgefahr.",
                          dati=[("Länge", "11 km ab Ossasco"), ("Höhendifferenz", "+1100 m ab Ossasco"), ("Zeit", "2 h ab der Hütte, 6 h ab Ossasco"), ("Schwierigkeit", "T4")],
                          link=[("Routenbeschreibung", "docs/capanne/cristallina/b-cristallina-2912.pdf")]),
                     dict(titolo="Cristallina-Runde", img=("giro-cristallina", "Der Stausee von Robiei mit der Mauer, unter den Bergen"),
                          testo="Klassische, leichte Runde auf weiss-rot-weissem Weg rund um den Gipfel des Cristallina. Auch als Tagestour ab Robiei oder vom Narèt-Pass, mit Mittagessen in der Hütte.",
                          dati=[("Länge", "14 km"), ("Höhendifferenz", "+980 m"), ("Zeit", "5 h 30"), ("Schwierigkeit", "T3")],
                          link=[("Routenbeschreibung", "docs/capanne/cristallina/c-giro-del-cristallina.pdf")]),
                     dict(titolo="Sentiero Cristallina 59, Richtung Robiei", img=("percorso-59", "Bergseen in einem felsigen Kessel am Sentiero Cristallina"),
                          testo="Der Sentiero Cristallina Nummer 59 ist eine klassische dreitägige Durchquerung von Bignasco im Maggiatal nach Airolo.",
                          dati=[("Länge", "42 km, in drei Etappen"), ("Höhendifferenz", "+2800 / −2100 m"), ("Zeit", "3 Tage"), ("Schwierigkeit", "T3")],
                          link=[("Routenbeschreibung", "docs/capanne/cristallina/d-percorso-59-cristallina.pdf")]),
                     dict(titolo="Nufenenpass-Cristallina-Airolo", img=("nufenen-airolo", "Wanderer auf einem grasigen, felsigen Grat"),
                          testo="Die erste Etappe der Via Idra, vom Nufenenpass nach Airolo mit Übernachtung in der Hütte. Höhepunkt ist der Aufstieg durch den Canale del Becco, mit Seilen und Tritten gesichert: am besten im Aufstieg begehen, auf Steinschlag und Schnee zu Saisonbeginn achten.",
                          dati=[("Länge", "27 km"), ("Höhendifferenz", "+1600 / −2450 m"), ("Zeit", "10 h, an zwei Tagen (5 + 5)"),
                                ("Schwierigkeit", "T4 am ersten Tag (T6 im Canale del Becco), T3 am zweiten")],
                          link=[("Routenbeschreibung", "docs/capanne/cristallina/e-passo-nufenen-airolo.pdf")]),
                 ]),
            dict(file="inverno", titolo="Im Winter", foto="inverno",
                 lead="Gipfel und Abfahrten im Pulverschnee: mehrere Abfahrten an einem Tag rund um die Hütte.",
                 img=("discesa-polvere", "Skitourengeher im Aufstieg auf einem weiten, schattigen Schneehang"),
                 corpo="""<p>Die Gegend am Cristallina eignet sich hervorragend für Abfahrten im Pulverschnee. Viele Routen rund um die Hütte lassen sich kombinieren, mit zwei oder mehr Abfahrten an einem Tag, der oft an den schattigen Hängen auf der rechten Seite des Bedrettotals endet.</p>
<ul>
<li>Aufstieg durch das Val Torta und Abfahrt durch das <strong>Val Cassinello</strong> von der Bassa di Folcra oder vom <strong>Passo Gararesch</strong>, Variante (Routen 521 h und 521 i).</li>
<li>Aufstieg durch das Val Torta zur klassischen <strong>Cristallina-Runde</strong>, mit Mittagessen in der Hütte und Abfahrt durch das Val Piana oder das Val Cavagnolo.</li>
<li>Gipfel des <strong>Cristallina</strong> und Abfahrt über die «Diavolezzina», eventuell mit Wiederaufstieg zur Bassa di Folcra (521 h) oder zum Passo Gararesch (521 i).</li>
<li><strong>Cima di Lago</strong> als Nachmittagstour, vom Val Torta oder vom Val Cavagnoli her.</li>
<li>Die wilde, abwechslungsreiche <strong>Scharten-Runde</strong>: am ersten Tag All’Acqua, San Giacomo, Passo Grandinagia, Bocchetta di Valleggia, Passo di Cima di Lago und Hütte (<a href="https://s.geo.admin.ch/7e3436c217" rel="noopener">Karte</a>); am zweiten Cima di Lago, Sfunadau, Cristallina und Passo Gararesch.</li>
<li><strong>Poncione di Braga, Basodino, Marchhorn:</strong> Gipfel auf grossen Durchquerungen.</li>
</ul>"""),
            dict(file="curiosita", titolo="Wissenswertes",
                 lead="Militärische Besetzung, Entstehung der Alpen und grosse Wasserkraftwerke: Hintergründe zur Gegend am Cristallina.",
                 img=("rocce-piegate", "Von der Alpenfaltung gebogene Felsen in einer grünen Mulde"),
                 corpo="""<p>Die Spuren der Alpenbildung sind gut sichtbar: Die Kräfte, die die Kette auffalteten, haben Meeresablagerungen an die Oberfläche gebracht, und auf wenigen Metern finden sich Gesteine ganz unterschiedlicher Zusammensetzung und Herkunft. Das prägt auch die Flora, die vom Untergrund abhängt. Die Tierwelt ist typisch alpin: Man begegnet leicht den Steinböcken der Kolonie, über hundert Tiere ohne Scheu vor dem Menschen. Auch der Mensch hat die Gegend verändert, mit der Grenzbewachung in Kriegszeiten und den grossen Wasserkraftanlagen.</p>
<p>Die ausführlichen Texte gibt es nur auf Italienisch.</p>""",
                 itinerari=[
                     dict(titolo="Die Geschichte der militärischen Besetzung", img=("rifugio-camosci", "Die alte militärische Steinhütte auf dem Gipfel, im Schnee"),
                          testo="Der Bau der Strasse durch das Val Formazza bis zum Passo San Giacomo zwischen 1926 und 1929 beunruhigte die Schweiz und führte zur Befestigung der Gegend.",
                          link=[("Ganzer Text", "docs/capanne/cristallina/a-la-storia-delloccupazione-militare-1.pdf")]),
                     dict(titolo="Die Spuren der Gebirgsbildung", img=("rocce-piegate", "Von der Alpenfaltung gebogene Felsen in einer grünen Mulde"),
                          testo="Die Landschaft am Cristallina ist von der alpinen Gebirgsbildung geprägt, einem Prozess, der rund 25 Millionen Jahre dauerte.",
                          link=[("Ganzer Text", "docs/capanne/cristallina/b-le-tracce-dellorogenesi-1.pdf")]),
                     dict(titolo="Die Wasserkraft Naret-Robiei", img=("schema-idroelettrico", "Schema der verbundenen Stauseen zwischen Gries, Robiei und Lago Maggiore"),
                          testo="Das Gebiet Robiei-Narèt ist reich an miteinander verbundenen Stauseen, die das Wasser bestmöglich für sauberen Strom nutzen.",
                          link=[("Ganzer Text", "docs/capanne/cristallina/c-ldroelettrico-naret-robiei-1.pdf")]),
                 ]),
        ],
        foto=[("Die Hütte", "capanna"), ("Die Küche", "cucina"), ("Die Umgebung", "dintorni")],
    ),

    "adula.html": dict(
        cartella="adula",
        capanna="""<p>Die «Bassa», wie sie seit jeher heisst, wurde 1924 eingeweiht und hat alle Merkmale des ursprünglichen Baus aus Stein und Holz bewahrt: eine Stube voller Geschichte, Schlafräume, in denen Tausende von Bergsteigern übernachtet haben, herzlicher Empfang und eine einheimische Küche, die Magen und Seele füllt.</p>
<p>Sie hat 24 Schlafplätze in vier kleinen Lagern mit 4, 5 und 7 Plätzen, auch für Familien geeignet, und zwei Doppelzimmer mit Aufpreis; zwei gemütliche Gaststuben mit 20 Plätzen, Toiletten im Haus, Dusche, Solarstrom für die Beleuchtung und Küche mit Holz und Gas. Die Betten haben Duvets; der Hüttenschlafsack ist obligatorisch. Mässiger Handyempfang bei der Hütte.</p>
<p>Der Winterraum ist immer offen, mit Getränken und Brennholz.</p>""",
        cucina="""<p>Die Panoramaterrasse lädt zum Essen im Freien ein. Jeden Tag kochen wir mit Produkten aus der Region: Tessiner Gerichte, Käse und Formaggini, Pasta mit Sauce, Suppe, Minestrone und unsere Rösti in verschiedenen Varianten, dazu immer mehrere Kuchen.</p>
<p>Für Übernachtungsgäste gibt es abends Gerichte und Spezialitäten mit saisonalen Produkten, und ein reichhaltiges Frühstück gibt Kraft für neue Abenteuer.</p>
<p><strong>Wichtig:</strong> Teilen Sie uns rechtzeitig mit, wenn Sie vegetarisch oder vegan essen oder Allergien und Unverträglichkeiten haben.</p>
<p>Hunde sind willkommen, aber nicht in den Zimmern: Für sie gibt es einen Platz draussen. Bitte melden Sie Ihren Hund vorher an.</p>""",
        team=dict(img=("guardiani", "Der Hüttenwart und zwei Helfer vor dem Eingang der Steinhütte"),
                  testo="""<p>Ich bin Lele, seit 2024 auf der Capanna Adula, zusammen mit meiner Partnerin Mirella. Die Leidenschaft für die Berge und die Erfahrung als Helfer in anderen Hütten jenseits der Alpen haben mich dazu gebracht, meinen Beruf aufzugeben, um mit den Menschen und der Natur zu leben.</p>
<p>Während der Saison helfen uns junge Leute, die Lust auf ein einzigartiges Erlebnis in der Höhe haben. Ein Traum, der wahr geworden ist.</p>""",
                  persone=[("Raffaele «Lele» Demaldi", "Hüttenwart", "lele"), ("Mirella", "Mit Lele in der Hütte", "mirella")]),
        tariffe=[
            ("Mitglieder SAC/FAT und Gegenrechtsvereine", "Übernachtung, Abendessen (Suppe, Salat, Hauptgang, Dessert) und Frühstück, MWST inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 45.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 58.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 75.–")]),
            ("Nichtmitglieder", "Übernachtung, Abendessen (Suppe, Salat, Hauptgang, Dessert) und Frühstück, MWST inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 50.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 63.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 85.–")]),
            ("Familien und Gruppen", "Familienrabatt unter der Woche (Sonntag-Donnerstag) und Preise für Schulen, Pfadi und J+S unter der Woche",
             [("Familien: Rabatt pro Kind unter 15 Jahren", "Fr. 5.–"), ("Gruppen: Kinder von 8 bis 14 Jahren", "Fr. 35.–"),
              ("Gruppen: Jugendliche von 15 bis 21 Jahren", "Fr. 45.–")]),
            ("Extras", "Aus hygienischen Gründen ist der Hüttenschlafsack obligatorisch",
             [("Doppelzimmer (Zuschlag pro Zimmer)", "Fr. 20.–"), ("Marschtee (1 l)", "Fr. 5.–"), ("Dusche (pro Person)", "Fr. 5.–"),
              ("Einweg-Hüttenschlafsack", "Fr. 7.–")]),
        ],
        prenotare="""<ul>
<li>Reservation online mit der Schaltfläche «Reservieren».</li>
<li>Kostenlose Annullierung bis 18 Uhr <strong>zwei Tage vor</strong> dem reservierten Datum.</li>
<li>Bezahlung bar, mit Twint oder Kreditkarte.</li>
<li>Keine Reservationen oder Anfragen über soziale Medien: Rufen Sie uns bitte an.</li>
</ul>
<p><a class="file-link" href="docs/capanne/adula/disposizioni-per-gli-ospiti-1.pdf">Hinweise für die Gäste</a></p>
<p><a class="file-link" href="docs/capanne/adula/2020-cgc-capanne-cas-it.pdf">Allgemeine Geschäftsbedingungen der SAC-Hütten</a></p>
<p><a class="file-link" href="docs/capanne/adula/pagamento-non-custodita-adula.pdf">Aufenthalt im Winter: Merkblatt zur Bezahlung</a></p>""",
        accessi="""<p><strong>Im Sommer</strong> erreicht man die Hütte bequem über den flachen Saumweg durch das Val Carassino ab Compietto. Das Tal ist etwa 6 km lang und führt an zwei Alpen vorbei, der Alpe Bolla und der Alpe Bresciana, wo ein ausgezeichneter Käse entsteht, den man auch in der Hütte geniesst. Der nahe Bach macht den Weg an heissen Tagen ideal für Familien; mit dem Mountainbike genügt etwa eine Stunde.</p>
<p><strong>Im Winter</strong> steigt man mit Ski ab Dangio durch das Val Soi auf, oder ab Ghirone über den Luzzone und das Val Carassino, bei sicherem Schnee und am besten im Frühling.</p>
<ul>
<li>Ab Compietto (Parkplatz) durch das Val Carassino: 2 h 40, mit dem Mountainbike etwa 1 h.</li>
<li>Ab Dangio (Bushaltestelle) durch das Val Soi: 3 h.</li>
<li>Ab Cusiè im Val Malvaglia (Parkplatz) über den Passo del Laghetto: 5 h.</li>
<li>Ab Läntahütte über die Bocchetta di Fornee.</li>
<li>Im Winter: ab Ghirone 5 h, ab Dangio 3 h 30.</li>
</ul>
<p><strong>Mit dem Auto:</strong> A2 bis Biasca, dann Richtung Lukmanier bis Campo Blenio und Ghirone; hinauf zur Staumauer des Luzzone, über die Mauer und weiter bis zur Alpe di Compietto. Oder das Auto in Ghirone lassen und den <a href="https://www.autolinee.ch/greina" rel="noopener">Alpenbus</a> nehmen.</p>
<p><strong>Mit dem öffentlichen Verkehr:</strong> Zug S10 bis Biasca, Bus 131 bis Ghirone, dann Alpenbus zur Staumauer des Luzzone. Taxi Riviera (Biasca): <a class="num" href="tel:+41918624848">+41 91 862 48 48</a>.</p>
<p><strong>Übergänge zu anderen Hütten:</strong> <a href="de/motterascio.html">Motterascio</a> 5 h; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 3 h 30; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 1 h; <a href="https://quarnei.ch/" rel="noopener">Quarnei</a> 3 h.</p>
<p>Karten: LK 1:25’000 Blatt 1253 Olivone; Skitourenkarte 256 S.</p>""",
        attivita="""<p>Auf der Adula liegt ein Hauch von früher in der Luft: Gastfreundschaft und gute Küche, dazu ein Glas Wein, laden ein, sich vor einer aussergewöhnlichen Kulisse ins Gras zu legen. Von hier aus geht es zu spannenden Routen, alten Übergängen und luftigen Graten.</p>
<p>Ein idealer Ort für Kinder: prächtige Blumen im Frühsommer, Gämsen und Steinböcke, Murmeltiere, Kühe zum Streicheln und ein Bach zum Baden. Man schläft in einer historischen Hütte mit dem Charme von früher und steigt auf das Rheinwaldhorn (Adula), Ziel vieler Tessiner, mit seinem Gletscher, der leider bald nur noch Erinnerung sein wird.</p>""",
        pagine=[
            dict(file="cima-adula", titolo="Gipfel der Adula", foto="cima-adula",
                 lead="Auf dem Dach des Tessins: Aufstieg auf das Rheinwaldhorn (Adula, 3402 m) über die Via Malvaglia, Abstieg über den Bresciana-Gletscher.",
                 img=("cordata-vetta", "Eine Seilschaft auf dem verschneiten Gipfel"),
                 corpo="""<p>Der Aufstieg auf das Rheinwaldhorn ist das Ziel vieler Tessiner Wanderer und Bergsteiger. Der Gipfel ist im Winter wie im Sommer recht leicht zu besteigen; wegen des Gletscherschwunds und der heissen Sommer geht man besser, bevor der Schnee ganz geschmolzen ist und den Gletscher freilegt.</p>
<p>Wer alpine Grundkenntnisse hat, dem empfehlen wir die Runde über den See von Cadabi mit Aufstieg über den Grat der Via Malvaglia. In Gipfelnähe ist der vom Gletscher freigegebene Fels brüchig: Vorsicht. Im Abstieg kann man über den Bresciana-Gletscher gehen, auf Spalten achten, bis zur Wegspur, die zur Capanna UTOE zurückführt.</p>""",
                 dati=[("Länge", "8 km"), ("Höhendifferenz", "+1400 m"), ("Zeit", "4-5 h im Aufstieg, 2-3 h im Abstieg"),
                       ("Schwierigkeit", "WS, gesicherte Abschnitte am Grat der Via Malvaglia"), ("Sehenswert", "See von Cadabi, Bresciana-Gletscher, Gipfelpanorama")],
                 link=[("Online-Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721078&amp;N=1150644&amp;trackId=5023916")]),
            dict(file="proposte-gite", titolo="Tourenvorschläge",
                 lead="Fünf Übergänge zu anderen Hütten, von der Höhenroute im Val Carassino bis zur Via Crio.",
                 img=("via-alta-carassino", "Ein Wanderer auf einem felsigen Grat über dem Val Carassino"),
                 corpo="""<p>Wer mehrere Tage Zeit hat, entdeckt mit diesen Wander- und Bergrouten wenig bekannte Winkel des Val Carassino. Es sind keine Rundtouren: Sie verbinden die Hütte mit anderen Hütten. Die Höhenroute im Val Carassino ist in beide Richtungen begehbar und vermeidet, zweimal durch den Talboden zu gehen, wenn man beim Luzzone startet oder ankommt; die Überschreitung Cassimoi-Cassinello ist ein herrlicher Gratweg; die Bocchetta di Fornee öffnet das Tor nach Vals; der Übergang nach Quarnei ist ein beliebter Klassiker, auch für Familien mit Kindern.</p>""",
                 itinerari=[
                     dict(titolo="Höhenroute im Val Carassino", img=("via-alta-carassino", "Ein Wanderer auf einem felsigen Grat über dem Val Carassino"),
                          testo="Von Compietto zur Hütte, in der Höhe über Sgiu, La Colma, Pinadee und Bresciana.",
                          dati=[("Länge", "7,5 km"), ("Höhendifferenz", "+1050 m"), ("Zeit", "5 h"), ("Schwierigkeit", "T5")],
                          link=[("Routenbeschreibung", "docs/capanne/adula/a-via-alta-della-val-carassino.pdf")]),
                     dict(titolo="Bänder und Gipfel im Val Carassino", img=("cengie-carassino", "Grashänge und Bänder unter verschneiten Gipfeln"),
                          testo="Der Pizzo Amianto und sein alter Bergsturz, die Schafbänder, Gämsen, Steinböcke und der Adler.",
                          dati=[("Länge", "11,5 km"), ("Höhendifferenz", "+1000 m"), ("Zeit", "5 h"), ("Schwierigkeit", "T5")],
                          link=[("Routenbeschreibung", "docs/capanne/adula/b-cengie-e-vette-della-val-carassino.pdf")]),
                     dict(titolo="Zur Läntahütte über die Bocchetta di Fornee", img=("lago-fornee", "Ein Bergsee zwischen gletschergeschliffenen Felsen"),
                          testo="Die Spuren des Gletscherrückzugs, Felsen und Steinböcke, Richtung Vals.",
                          dati=[("Länge", "8,7 km"), ("Höhendifferenz", "+1000 m"), ("Zeit", "5 h 30"), ("Schwierigkeit", "T5")],
                          link=[("Routenbeschreibung", "docs/capanne/adula/c-alla-capanna-lanta-dalla-btta-di-fornee.pdf")]),
                     dict(titolo="Leichter Übergang nach Quarnei", img=("laghetto-cadabi", "Der See von Cadabi in einem felsigen Kessel"),
                          testo="Der Bresciana-Gletscher und sein Sterben, die Seitenmoränen, die Rundhöcker, der See von Cadabi und die Ebene von Quarnei.",
                          dati=[("Länge", "4 km"), ("Höhendifferenz", "+700 m"), ("Zeit", "3 h 30"), ("Schwierigkeit", "T3")],
                          link=[("Routenbeschreibung", "docs/capanne/adula/d-facile-traversata-a-quarnei.pdf")]),
                     dict(titolo="Via Crio, Etappe 6: vom Pizzo Cassimoi zum Luzzone", img=("via-crio", "Ein Wanderer an einer gesicherten Stelle zwischen rötlichen Felsen"),
                          testo="Drei Dreitausender auf einer der anspruchsvollsten Etappen der <a href=\"https://www.viacrio.ch/\" rel=\"noopener\">Via Crio</a>.",
                          dati=[("Länge", "15,9 km"), ("Höhendifferenz", "+1540 / −1950 m"), ("Zeit", "8 h"), ("Schwierigkeit", "T6, anspruchsvolle Überschreitung")],
                          link=[("Routenbeschreibung", "docs/capanne/adula/e-scaradra-luzzone-passando-dalla-bocchetta-di-fornee.pdf"),
                                ("Übersicht der Via Crio", "docs/capanne/adula/via-alta-crio-prospetto-2024.pdf"),
                                ("GPX-Track", "https://www.viacrio.ch/s/006-CRIO-GPX-Adla-UTOE-Scaradra-MV.gpx")]),
                 ]),
            dict(file="inverno", titolo="Winter und Frühling", foto="inverno",
                 lead="Einsame Gipfel für erfahrene Skitourengeher und Schneerinnen für das Bergsteigen zu Saisonbeginn.",
                 img=("pendio-innevato", "Skispuren auf einem weiten Schneehang"),
                 corpo="""<h2>Die Adula im Winter</h2>
<p>Im Winter bleibt die Tessiner Seite der Adula abgeschieden: Lawinen gehen an den Hängen der Carassina nieder, und der Aufstieg aus dem Val Soi verlangt im letzten Teil gesetzten Schnee. Wenn im Tal der Frühling kommt, bietet das Massiv schöne, technische Übergänge von Hütte zu Hütte zwischen <strong>Läntahütte</strong>, <strong>Zapporthütte</strong>, <strong>Adula</strong> und <strong>Quarnei</strong>: Mit der Adula-Runde und ihren Varianten besteigt man jeden Tag mindestens einen Gipfel über 3000 m.</p>
<ul>
<li><strong>Rheinwaldhorn (3402 m) über den Vadrecc di Bresciana:</strong> Aufstieg über die Sommerroute (324 a); bei guten Verhältnissen fährt man direkt über den Gletscher bis etwa 2500 m ab und erreicht mit einem kurzen Gegenanstieg über die Moräne den Hang oberhalb der Capanna UTOE (324 c). WS.</li>
<li><strong>Grauhorn (3258 m):</strong> im Sommer zu brüchig, im Frühling über Route 323 erreichbar, zu Fuss über den Hang bis zum Grat auf 3100 m. ZS.</li>
<li><strong>Piz Jut (3128 m):</strong> über die Bocchetta di Fornee (2885 m, Route 320), dann auf der Bündner Seite zum Gipfel; Abfahrt zur Läntahütte durch das Forneitobel (309). ZS.</li>
<li><strong>Cima di Pinadee (2486 m):</strong> über dem Val Carassina, ohne grosse Schwierigkeiten in gut einer Stunde ab der Alpe di Bresciana. WS.</li>
</ul>
<h2>Bergsteigen im Frühling</h2>
<p>Die Gipfel vom Torrone di Nav bis zum Passo Cadabi leiden unter der Gletscherschmelze: Einst auch im Sommer sichere Aufstiege sind heute brüchige, steinschlaggefährdete Geröllhalden. Man geht sie besser an, wenn oberhalb von 2500 m noch genug Schnee liegt, und beurteilt das nächtliche Durchfrieren sorgfältig.</p>
<p>Unter diesen Voraussetzungen lohnen sich die Schneerinnen bis 50° Neigung, mit Steigeisen und Pickel:</p>
<ul>
<li>Westcouloir der <strong>Cima dal Laghetto</strong> aus dem Val Soi bis Punkt 2582 m, L;</li>
<li>Rheinwaldhorn durch das Couloir <strong>Damstädten</strong> (links), Südwestwand bis Punkt 3205 m, WS;</li>
<li>Rheinwaldhorn durch das Couloir <strong>Ezio e Maria</strong> (rechts), Südwestwand bis Punkt 3205 m, WS+.</li>
</ul>
<p>Auch für das <strong>Grauhorn</strong> (Geröllhang bis etwa 3180 m) sowie für <strong>Cima di Fornee</strong>, <strong>Piz Jut</strong> und <strong>Punta dello Stambecco</strong> ab Fornee ist ein Aufbruch zu Saisonbeginn sicherer und bequemer.</p>""",
                 link=[("Skitourenrouten auf der Karte", "https://map.geo.admin.ch/?lang=de&amp;topic=wildruhezonen&amp;bgLayer=ch.swisstopo.pixelkarte-farbe&amp;layers=ch.bafu.wrz-jagdbanngebiete_select,ch.bafu.wrz-wildruhezonen_portal,ch.swisstopo-karto.skitouren&amp;layers_visibility=true,false,true&amp;catalogNodes=1308&amp;E=2721748.94&amp;N=1152606.59&amp;zoom=6&amp;layers_opacity=1,1,0.8")]),
            dict(file="curiosita", titolo="Wissenswertes",
                 lead="Zwei Hütten und die politischen Kämpfe vor hundert Jahren, alte Alpwanderungen und der Reichtum des Val Carassino.",
                 img=("vetta-tramonto", "Ein Gipfel im Abendlicht über schattigen Tälern"),
                 corpo="""<p>Auf den ersten Blick wirkt das Val Carassino lang und eintönig, doch bei den Hütten öffnet sich der Blick auf das Rheinwaldhorn, das Val Soi und das Bleniotal. Wer genau hinsieht, entdeckt den botanischen Reichtum des Tals und die Wildtiere an seinen Hängen.</p>
<p>Seit dem frühen Mittelalter nutzen die Talbewohner die Gegend: Die Alpwirtschaft lebt bis heute weiter, und ihre Produkte sind sehr geschätzt. Der Gipfel und die beiden Hütten erinnern auch an die politischen Kämpfe vor über hundert Jahren, als aus bürgerlichen und Arbeiterbewegungen die «proletarischen» Bergsteigergruppen und die UTOE entstanden, eine Tessiner Besonderheit in der Geschichte des Schweizer Alpinismus.</p>
<p>Die ausführlichen Texte gibt es nur auf Italienisch.</p>""",
                 itinerari=[
                     dict(titolo="Warum zwei Hütten? Zur Geschichte", img=("vetta-tramonto", "Ein Gipfel im Abendlicht über schattigen Tälern"),
                          testo="Der grösste Traum, den der temperamentvolle Präsident Remo Patocchi verwirklichen wollte…",
                          link=[("Ganzer Text", "docs/capanne/adula/a-perche-due-capanne-cenni-di-storia.pdf")]),
                     dict(titolo="Geschichten von alten Alpwanderungen", img=("dipinto-alpe", "Gemälde einer Alp mit Steinhütte unter den Gipfeln"),
                          testo="Vor tausend Jahren hatte eine sehr warme Zeit grossen Einfluss auf die ganzen Alpen…",
                          link=[("Ganzer Text", "docs/capanne/adula/c-storie-di-antiche-transumanze.pdf")]),
                 ]),
        ],
        foto=[("Die Hütte", "capanna"), ("Die Umgebung", "dintorni")],
        foto_lead="Die Hütte und die Umgebung",
    ),

    "motterascio.html": dict(
        cartella="motterascio",
        capanna="""<p>Mitten in einem Netz von Wegen zwischen einigen der schönsten Orte der Südschweiz steht die Capanna Michela Motterascio auf 2172 m auf der Alpe Motterascio, am Südrand der Greina-Hochebene, im Einklang von Holz, Kupfer und Stein. Unter den Gipfeln von Piz Terri, Pizzo Coroi, Piz Vial, Gaglianera und Piz Valdraus verbringt man Tage voller Wanderungen, Stille und Erholung. Man muss kein erfahrener Bergsteiger sein: Neugier, Begeisterung und etwas Energie genügen.</p>
<p>Die Hütte ist geräumig: 70 Schlafplätze mit Duvets, ein Panorama-Speisesaal mit 55 Plätzen und Fensterfront zu den Alpen, eine «romantische» Stube mit 20 Plätzen, getrennte Toiletten für Frauen und Männer im Haus, eine Dusche, wenn das Quellwasser reicht, Trocknungsraum und Hüttenschuhe beim Eingang, auch für die Kleinen. Das Wasser ist trinkbares Quellwasser; der Strom kommt von der Photovoltaik, mit einem Generator als Reserve. Der Hüttenschlafsack ist obligatorisch, auch zum Mieten. Kein Handyempfang.</p>
<p><strong>Winterraum:</strong> 10 Schlafplätze mit Duvets, Getränken, Brennholz und dem Nötigsten (Salz, Zucker, Pulverkaffee). Essen bitte selber mitbringen; Wasser ist nicht garantiert (Brunnen auf der Terrasse, wenn nicht gefroren), und es gibt keine Wintertoilette. Die Reservation ist obligatorisch, online; die Bestätigung enthält alle Informationen.</p>""",
        cucina="""<p>Mittags laden die Sonnenterrasse und die schöne Stube zu einfachen, regionalen Gerichten ein, warm und kalt, mit atemberaubender Aussicht, dazu das Buffet mit hausgemachten Kuchen. Das Abendessen gibt es um 19 Uhr, je nach Angebot und Einfall des Kochs; danach ein reichhaltiges Frühstück für den nächsten Tag. Gekocht wird vor allem auf dem Holzherd und mit Gas.</p>
<p><strong>Wichtig:</strong> Teilen Sie uns rechtzeitig mit, wenn Sie vegetarisch oder vegan essen oder Allergien und Unverträglichkeiten haben.</p>
<p>Für Kinder gibt es Spiele, Bücher, Papier und Farbstifte; am Weg sieht man mit etwas Glück Murmeltiere. Hunde sind willkommen, dürfen aber nicht in die Hütte: Für die Nacht steht der geschützte, trockene Holzschopf mit Decke und Näpfen bereit. Bitte vorher melden.</p>
<p>Im Sommer hilft die Materialseilbahn bei der Versorgung, der Helikopter bleibt aber unverzichtbar: Bitte nehmen Sie Ihre Abfälle wieder mit ins Tal.</p>""",
        team=dict(titolo="Der Hüttenwart", img=("fabio", "Fabio Merzaghi in der Küche mit frisch gebackenen Kuchen"),
                  testo="""<p>Ich heisse Fabio Merzaghi und bin am Fuss des Monte Generoso aufgewachsen, am Ufer des Luganersees. Die Berge sind seit jeher meine Leidenschaft: Im Winter steige ich mit Fellen auf die Gipfel, im Sommer klettere ich.</p>
<p>In einer Hütte zu arbeiten war mein Traum: Im Sommer 2023 habe ich ihn in der <a href="https://www.fornohuette.ch/" rel="noopener">Fornohütte</a> verwirklicht, danach habe ich eine Zeit lang die <a href="https://www.sac-bluemlisalp.ch/de/Baltschiederklause" rel="noopener">Baltschiederklause</a> auf 2783 m im Wallis geführt. Ich habe den Hüttenwartskurs des Schweizer Alpen-Clubs besucht. Als Maschineningenieur habe ich das Büro gegen ein Abenteuer in der Natur getauscht.</p>
<p>Die Hütte setzt auf hochwertige lokale Produkte und nachhaltiges Wirtschaften. Und ohne die Zauberhände unserer treuen Helferinnen und Helfer gäbe es nicht einmal ein Stück Kuchen: herzlichen Dank!</p>
<p><strong>Fabio</strong></p>"""),
        tariffe=[
            ("Mitglieder SAC/FAT und Gegenrechtsvereine", "Saison 2026: Übernachtung, Abendessen (Suppe, Salat, Hauptgang, Dessert) und Frühstücksbuffet, MWST und Kurtaxe inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 50.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 65.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 82.–"), ("Bergführer", "Fr. 52.–")]),
            ("Nichtmitglieder", "Saison 2026: Übernachtung, Abendessen und Frühstücksbuffet, MWST und Kurtaxe inbegriffen",
             [("Kinder bis 7 Jahre", "Fr. 32.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 55.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 72.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 95.–")]),
            ("Familien und Gruppen", "Familienrabatt unter der Woche (Sonntag-Donnerstag) und Preise für Schulen, Pfadi und J+S (Montag-Donnerstag)",
             [("Familien: Rabatt pro Kind unter 15 Jahren", "Fr. 5.–"), ("Gruppen: Kinder von 8 bis 14 Jahren", "Fr. 40.–"),
              ("Gruppen: Jugendliche von 15 bis 18 Jahren", "Fr. 50.–")]),
            ("Extras", "Aus hygienischen Gründen ist der Hüttenschlafsack obligatorisch",
             [("Lunch", "Fr. 10.–"), ("Tee (1 l)", "Fr. 3.–"), ("Dusche (pro Person)", "Fr. 5.–"),
              ("Einweg-Hüttenschlafsack", "Fr. 7.–"), ("Hüttenschlafsack zum Mieten", "Fr. 5.–")]),
        ],
        prenotare="""<ul>
<li>Reservation online mit der Schaltfläche «Reservieren»; für kurzfristige Reservationen bitte anrufen.</li>
<li><strong>Nur Barzahlung</strong>, in Franken oder Euro.</li>
<li>Annullierungen und Änderungen kostenlos bis 18 Uhr zwei Tage vor der Ankunft; bis 18 Uhr am Vortag Fr. 30.– pro Person und Nacht; nicht gemeldetes Nichterscheinen Fr. 50.– pro Person und Nacht.</li>
</ul>
<p><a class="file-link" href="docs/capanne/motterascio/disposizioni-per-gli-ospiti-1.pdf">Hinweise für die Gäste</a></p>
<p><a class="file-link" href="docs/capanne/motterascio/cgc-capanne-cas.pdf">Allgemeine Geschäftsbedingungen der SAC-Hütten</a></p>""",
        accessi="""<p>Im Sommer erreicht man die Hütte bequem zu Fuss, meist auf familienfreundlichen Wegen. Im Winter steigt man mit Ski durch das Val Camadra und über den Greinapass auf (5-6 h), nur bei gesetztem Schnee und wenn die seitlichen Hänge entladen sind.</p>
<ul>
<li>Ab Lago di Luzzone, Alpe Garzott: 2 h.</li>
<li>Ab Lago di Luzzone, Staumauer: 3 h 30.</li>
<li>Ab Ghirone über den Lago di Luzzone: 4 h 30; durch das Val Camadra: 6 h.</li>
<li>Ab Pian Geirètt: 3 h 30.</li>
<li>Ab Vrin: 5 h; ab Vals: 7-8 h.</li>
</ul>
<p><strong>Mit dem öffentlichen Verkehr:</strong> Zug und Bus bis Ghirone, Aquilesco; dann mit dem <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a> der Autolinee Bleniesi bis Lago di Luzzone oder Pian Geirètt, im Juli und August täglich, im September nur an Wochenenden.</p>
<p><strong>Mit dem Auto:</strong> A2 bis Biasca, dann Richtung Lukmanier bis Campo Blenio und Ghirone; hinauf zur Staumauer des Luzzone und dem See entlang bis zur Alpe Garzott. Kostenlose Parkplätze in Ghirone-Aquilesco und bei der Staumauer (mit Toiletten; Ristorante Luzzone von April bis Oktober); auf der Alpe Garzott, wo man ausgezeichneten Käse kaufen kann, gibt es nur wenige Plätze: früh kommen oder Fahrgemeinschaften bilden.</p>
<p><strong>Taxi:</strong> Poglia Mirko (Olivone) <a class="num" href="tel:+41794440712">+41 79 444 07 12</a>; <a href="https://www.taxiriviera.ch/" rel="noopener">Taxi Riviera</a> (Biasca) <a class="num" href="tel:+41794136868">+41 79 413 68 68</a>.</p>
<p><strong>Übergänge zu anderen Hütten:</strong> <a href="https://www.terrihuette.ch/" rel="noopener">Terri</a> 2 h 30; <a href="https://www.satlucomagno.ch/wordpress/capanna-scaletta/" rel="noopener">Scaletta</a> 2 h; <a href="https://www.capannabovarina.ch/" rel="noopener">Bovarina</a> 5 h; <a href="de/adula.html">Adula CAS</a> 5 h; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 6 h; <a href="https://www.medelserhuette.ch/" rel="noopener">Medelser Hütte</a> 6 h; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 7 h; <a href="https://www.rifugioscaradra.ch/" rel="noopener">Rifugio Scaradra</a> 3 h. Routen auf <a href="https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=10&amp;E=2720474&amp;N=1161992&amp;layers=Wanderland%2CStation%2CAccomodation" rel="noopener">SchweizMobil</a>.</p>
<p>Karten: LK 1:25’000 Blatt 1233 Greina; Skitourenkarte 256 S.</p>""",
        attivita="""<p>Die Greina ist eine einzigartige Hochebene zwischen Tessin und Graubünden, fast 6 km lang und über 2200 m hoch: eine geschützte alpine Tundra im Bundesinventar der Landschaften von nationaler Bedeutung. Sie ist unberührt: Die einzigen Spuren des Menschen sind der Crap la Crusch und der Pass Crap, wo ein Eisenkreuz daran erinnert, dass die Greina schon in römischer Zeit und im Mittelalter Durchgangsweg und Weideland war.</p>
<p>Hier entspringen unzählige Quellen, die Mäander, Altwasser und Sümpfe bilden, auf der kontinentalen Wasserscheide: Der Brenno della Greina fliesst zum Mittelmeer, der Rein da Sumvitg zur Nordsee. Sie ist die Königin der Kontraste, zwischen dem Weiss der Gletscher, dem Schwarz der Schiefer und dem Grün der Tundra, mit dem rund vierzig Meter langen Felsbogen, den Mooren, den Felstürmchen und den Dolinen. <strong>Um ihren Zauber wirklich zu erleben, bleiben Sie zwei Tage oder länger.</strong></p>""",
        pagine=[
            dict(file="giro-greina", titolo="Greina-Rundtour", foto="giro-greina",
                 lead="Die Greina an einem Tag: vom Luzzone zur Hütte, über den Greinapass und hinunter zur Scaletta, mit dem Bus alpin.",
                 img=("piano-greina", "Die Greina-Ebene mit dem Bach zwischen Wiesen und Bergen"),
                 corpo="""<p>Ghirone, Lago di Luzzone, Capanna Michela Motterascio, Crap la Crusch, Greinapass, Capanna Scaletta, Pian Geirètt, Ghirone: Für alle, die nur einen Tag haben, ist die Runde dank dem <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a> im Sommer in 6-7 Stunden Gehzeit machbar.</p>
<p>Von der Haltestelle folgt man der Naturstrasse dem <strong>Lago di Luzzone</strong> entlang. Bei der Alpe Garzott betritt man auf einem gut markierten Weg den «Fjord», eine enge Schlucht; der Weg wurde 2017 mit Unterstützung des Patriziato di Aquila ausgebaut. Nach einer modernen Brücke steigt man zwischen lichten Lärchen zu den Monti di Rafüsc (1691 m) und über steile Grashänge zur Ebene von Trachee (1947 m). Über ein altes Holzbrücklein über den Ri di Motterascio und einen letzten Anstieg in Kehren erreicht man die <strong>Hütte</strong> (2172 m, etwa 3 h).</p>
<p>Weiter geht es zur <strong>Alpe Motterascio</strong>: Man überwindet eine Gittertreppe (mit Hunden umgeht man sie rechts auf dem Weg der Kühe) und quert die Alp zwischen Bächen und sumpfigem Boden bis zum breiten Sattel des <strong>Crap la Crusch</strong> (2268 m, etwa 1 h), mit einem fantastischen Blick auf die Plaun la Greina.</p>
<p>Immer auf dem weiss-rot-weissen Weg steigt man zum <strong>Greinapass</strong> (2355 m), den Quellen des Rheins entlang, der in die Nordsee mündet, und geht weiter zur <strong>Capanna Scaletta</strong> (2205 m, 2 h), mit Blick auf die Mäander des Brenno, der dagegen ins Mittelmeer fliesst. Wer den <strong>Greina-Bogen</strong> sehen will, macht einen kleinen Abstecher den Mäandern entlang; vom Bogen führt ein weiss-blau-weisser Weg zur Scaletta, nur für erfahrene Wanderer und ohne Eis und Schnee; sonst kehrt man auf den weiss-rot-weissen Weg zurück (1 h). Von der Scaletta ist der Abstieg nach <strong>Pian Geirètt</strong> steil, aber kurz (1 h), und der Bus alpin bringt einen zurück nach Ghirone.</p>
<p>Die Runde geht auch in umgekehrter Richtung, für Familien empfohlen, weil der Aufstieg ab Pian Geirètt weniger anstrengend ist als der vom Luzzone.</p>""",
                 dati=[("Länge", "17 km"), ("Höhendifferenz", "+700 m"), ("Zeit", "6 h"), ("Schwierigkeit", "T2"),
                       ("Sehenswert", "Alpe Garzott, Alpe Motterascio, Crap la Crusch, die Wasserscheide, die Quellen von Rhein und Brenno, Felstürmchen, Mäander, der Greina-Bogen")],
                 link=[("Online-Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=7.09&amp;E=2717383&amp;N=1160737&amp;trackId=4244704")]),
            dict(file="proposte-gite", titolo="Tourenvorschläge",
                 lead="Sechs Touren ab der Hütte: Crap la Crusch, Piz Terri, Greina-Bogen, Plaun la Greina und Via Crio.",
                 img=("crap-la-crusch", "Der grosse Felsblock des Crap la Crusch mit dem Kreuz, auf der Greina-Ebene"),
                 corpo="""<p>Wer mehrere Tage Zeit hat, kann mit diesen Routen den Zauber der Greina voll erleben. Fast alle beginnen und enden bei der Hütte.</p>""",
                 itinerari=[
                     dict(titolo="Crap la Crusch", img=("crap-la-crusch", "Der grosse Felsblock des Crap la Crusch mit dem Kreuz, auf der Greina-Ebene"),
                          testo="Leichter Spaziergang zum Mittelpunkt der Greina, über die Alpe Motterascio und den Ri di Motterascio.",
                          dati=[("Länge", "6 km"), ("Höhendifferenz", "+180 m"), ("Zeit", "2 h"), ("Schwierigkeit", "T2")],
                          link=[("Routenbeschreibung", "docs/capanne/motterascio/a-crap-la-crusch.pdf")]),
                     dict(titolo="Piz Terri", img=("piz-terri", "Die Pyramide des Piz Terri im Sonnenlicht"),
                          testo="Das Val Güida, der Piz Terri, der Laghet la Greina, das Val Canal und der Crap la Crusch.",
                          dati=[("Länge", "11 km"), ("Höhendifferenz", "+1100 m"), ("Zeit", "6 h"), ("Schwierigkeit", "T3-T4")],
                          link=[("Routenbeschreibung", "docs/capanne/motterascio/b-piz-terri.pdf")]),
                     dict(titolo="Pizzo Coroi und Capanna Scaletta", img=("arco-greina", "Der natürliche Felsbogen der Greina"),
                          testo="Der Pizzo Coroi, der Greina-Bogen, die Mäander, die Felstürmchen und die Quellen von Brenno und Rhein.",
                          dati=[("Länge", "15 km"), ("Höhendifferenz", "+900 m"), ("Zeit", "6 h"), ("Schwierigkeit", "T3")],
                          link=[("Routenbeschreibung", "docs/capanne/motterascio/c-pizzo-coroi-capanna-scaletta.pdf")]),
                     dict(titolo="Plaun la Greina und Terrihütte", img=("plaun-la-greina", "Blick von oben auf die Täler und Grate rund um die Greina"),
                          testo="Die Quellen des Rheins, die Mäander, die Moore, die parallelen Terrassen, die Grashöcker und der Muot la Greina.",
                          dati=[("Länge", "13 km"), ("Höhendifferenz", "+400 m"), ("Zeit", "4 h"), ("Schwierigkeit", "T2")],
                          link=[("Routenbeschreibung", "docs/capanne/motterascio/d-plaun-la-greina-capanna-terri.pdf")]),
                     dict(titolo="Val Larciolo", img=("val-larciolo", "Hütten der Alpe Larciolo zwischen goldenen Herbstlärchen"),
                          testo="Einsame, wilde Variante abseits der markierten Wege, um die Hütte vom Luzzone her von oben zu erreichen, über die Alpe Coroi, die Alpe Larciolo und die Alpe Garzott.",
                          dati=[("Länge", "7 km"), ("Höhendifferenz", "+250 m"), ("Zeit", "2 h"), ("Schwierigkeit", "T2-T3")],
                          link=[("Routenbeschreibung", "docs/capanne/motterascio/e-val-larciolo.pdf")]),
                     dict(titolo="Via Crio, Etappen 7 und 8", img=("via-crio", "Ein Wanderer an einer gesicherten Stelle zwischen rötlichen Felsen"),
                          testo="Zwei Etappen der Via Crio führen an der Hütte vorbei.",
                          link=[("Etappe 7", "https://www.viacrio.ch/tappa7"), ("Etappe 8", "https://www.viacrio.ch/tappa8"),
                                ("Übersicht der Via Crio", "docs/capanne/motterascio/prospettocrio.pdf"),
                                ("Höhenprofil der Via Crio", "docs/capanne/motterascio/altimetria-totale.pdf")]),
                 ]),
            dict(file="trekking-greina-alta", titolo="Trekking Greina Alta", foto="trekking-greina-alta",
                 lead="Von Curaglia nach Vals in vier Etappen: drei SAC-Hütten, drei Kulturen, drei Sprachen.",
                 img=("escursionisti-greina", "Wanderer auf einer Wiese Richtung Berge"),
                 corpo="""<p>Camona da Medel, Capanna Michela Motterascio, Läntahütte: Das Trekking Greina Alta für mittlere bis erfahrene Wanderer führt von Curaglia nach Vals, mit einem gemeinsamen Nenner, der Zahl 3. Es durchquert eine Region mit 3 SAC-Hütten, 3 Kulturen, 3 Sprachen und 3 mächtigen Gipfeln. Wer es ganz geht, kann in einer der drei Hütten eine Pauschalreservation verlangen.</p>
<ul>
<li><strong>Tag 1:</strong> (Disentis) Curaglia (1332 m), Val Platta, Alp Sura (1982 m), Camona da Medel (2524 m). 3 h 30, T3.</li>
<li><strong>Tag 2:</strong> Camona da Medel, Fuorcla Sura da Lavaz (2703 m), Greinapass (2355 m), Crap la Crusch (2268 m), Capanna Michela Motterascio (2172 m). 6 h, T4.</li>
<li><strong>Tag 3:</strong> Capanna Michela Motterascio, Lago di Luzzone, Larecc (1633 m), Val Scaradra, Passo Soreda (2759 m), Läntatal, Läntahütte (2090 m). 7 h, T3.</li>
<li><strong>Tag 4:</strong> Läntahütte, Furggelti (2712 m), Zervreilasee (1862 m), Zervreila (Vals). 5 h, T3.</li>
</ul>""",
                 dati=[("Länge", "45 km"), ("Höhendifferenz", "+4200 m"), ("Zeit", "6-7 h pro Tag"), ("Schwierigkeit", "T3-T4"),
                       ("Beste Zeit", "Mitte Juli bis Anfang Oktober"),
                       ("Sehenswert", "Val Platta, Fuorcla Sura da Lavaz, Greina, Lago di Luzzone, Val Scaradra, Läntatal, Zervreilasee")],
                 link=[("Die Website des Trekkings", "https://greinaalta.ch/"),
                       ("Online-Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=17.65&amp;E=2718864&amp;N=1162797&amp;layers=Wanderland&amp;trackId=4230099")]),
        ],
        foto=[("Die Hütte", "capanna"), ("Die Küche", "cucina"), ("Die Umgebung", "dintorni")],
    ),

    "montebar.html": dict(
        cartella="montebar",
        capanna="""<p>Die neue Hütte im Besitz des CAS Ticino wurde 2016 eingeweiht, genau 80 Jahre nach dem ersten Bau. Das Projekt «Barlume» der Architekten Oliviero Piffaretti und Carlo Romano (Atelier PeR, Mendrisio), unter dreissig ausgewählt, ist ein einfacher, kubischer Baukörper aus Lärchenholz rund um die Feuerstelle: eine Laterne in der Landschaft, im Dialog mit den Hütten auf den Gipfeln ringsum.</p>
<p>Der Speisesaal, das Herz der Hütte, hat Fenster auf allen Seiten und bis zu 60 Plätze; die Terrasse ist vom Speisesaal und von der Küche aus zugänglich. In den oberen Stockwerken liegen Zimmer mit 2, 4 und 6 Betten in Kajütenbetten, mit Toiletten auf der Etage; es gibt einen Workshop-Raum für Sitzungen, Kurse und Schulen. Im Untergeschoss liegen die Sanitärräume, der Raum, der Wanderern offensteht, wenn die Hütte geschlossen ist, und der Veloraum mit Akku-Ladestationen und kleiner Werkstatt nach Bike-Hotel-Standard.</p>
<p>Über ein dichtes Netz von Wander- und Mountainbikewegen leicht erreichbar, mit überraschender Natur, Geschichte und Landschaft, ist sie das ideale Ziel für Familien und Schulen, oder für eine Nacht in der Hütte nach einem geselligen Abendessen.</p>""",
        cucina="""<p>Wir kochen mit Leidenschaft frische, saisonale Produkte aus der Region, mit der Tessiner Küche als Massstab. Mittagessen gibt es von 11.30 bis 15 Uhr; am Nachmittag immer eine Suppe, kalte Teller und Kuchen. Das Abendessen ist um 19 Uhr: Abends bitten wir um Reservation. Auf Anfrage bereiten wir auch Menüs für besondere Anlässe zu.</p>
<ul>
<li>Hausgemachte Kuchen, Minestrone mit Gemüse und Hülsenfrüchten, Tessiner Polenta.</li>
<li>Käse von den nahen Alpen und Tessiner Wurstwaren.</li>
<li>Grill auf der Terrasse im Sommer, Wild im Herbst, Käsefondue im Winter.</li>
</ul>
<p>Frühstück ab 7.45 Uhr (im Winter ab 8 Uhr). Hunde sind in der Hütte nicht erlaubt; Minderjährige sind in Begleitung eines Erwachsenen willkommen. Ab 22 Uhr bitte Rücksicht auf die Schlafenden nehmen.</p>""",
        team=dict(titolo="Die Hüttenwarte", img=("gestori", "James Mauri und Serge Santese auf den Weiden vor der Hütte"),
                  testo="""<p>Seit 2020 führen James Mauri und Serge «Seo» Santese die Hütte, mit Erfahrung in sehr guten Küchen im Tessin und darüber hinaus. Wir freuen uns über das, was wir tun: Hier zu leben ist eine bewusste Wahl und vor allem eine schöne Lebensschule.</p>
<p><strong>James und Seo</strong></p>"""),
        tariffe=[
            ("Mitglieder SAC/FAT und Gegenrechtsvereine", "Übernachtung mit Halbpension",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 40.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 60.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 80.–")]),
            ("Nichtmitglieder", "Übernachtung mit Halbpension",
             [("Kinder bis 7 Jahre", "Fr. 30.–"), ("Kinder von 8 bis 14 Jahren", "Fr. 45.–"), ("Jugendliche von 15 bis 21 Jahren", "Fr. 65.–"),
              ("Erwachsene ab 22 Jahren", "Fr. 95.–")]),
            ("Doppelzimmer", "Mit Doppelbett und frischer Bettwäsche",
             [("Pro Person", "Fr. 120.–"), ("Einzelbelegung", "Fr. 150.–")]),
            ("Familien und Gruppen", "Familien mit 2 Erwachsenen und mindestens 2 Kindern bis 15 Jahre; Jugendgruppen (Schulen, Pfadi, J+S) von Montag bis Donnerstag",
             [("Familien, Freitag-Samstag: Rabatt pro Person", "Fr. 5.–"), ("Familien, Sonntag-Donnerstag: Rabatt pro Person", "Fr. 10.–"),
              ("Gruppen: Kinder bis 15 Jahre", "Fr. 35.–"), ("Gruppen: Jugendliche von 15 bis 18 Jahren", "Fr. 45.–")]),
            ("Extras", "Besondere Menüs für Anlässe nach Absprache mit den Hüttenwarten; Hüttenschlafsack obligatorisch",
             [("Lunch zum Mitnehmen", "Fr. 12.–"), ("Tagestee (1 l)", "Fr. 3.–"), ("Dusche (pro Person)", "Fr. 5.–"),
              ("Hüttenschlafsack", "Fr. 7.–")]),
            ("Workshop-Raum", "Mit Beamer und Tischen für etwa 15 Personen",
             [("Pro Tag, ohne Verpflegung", "Fr. 200.–"), ("Mit Mittag- oder Abendessen", "Fr. 100.–"), ("Mit Halbpension", "gratis")]),
        ],
        prenotare="""<ul>
<li><strong>Sommer</strong> (1. Mai bis 8. November 2026): täglich offen.</li>
<li><strong>Winter</strong> (9. November 2026 bis 30. April 2027): von Freitagmittag bis Sonntagmittag, an Feiertagen und in den Schulferien immer offen; an den übrigen Tagen auf Anfrage. Wenn die Hütte geschlossen ist, sind nur der Eingang mit Toiletten und Getränken zugänglich: <strong>Übernachten ist dann nicht möglich</strong>.</li>
<li>Reservation online mit der Schaltfläche «Reservieren». Annullierungen und Änderungen ohne Gebühr bis 18 Uhr 2 Tage vor der Ankunft für bis zu 9 Personen, 4 Tage vorher ab 10 Personen; danach Fr. 50.– pro Person und Nacht.</li>
<li>Check-in von 16.30 bis 18 Uhr, Check-out um 9 Uhr. Übernachtungsgäste melden sich bei der Ankunft und tragen sich ins Gästebuch ein.</li>
<li>Bezahlung bar, mit EC, Visa oder Twint.</li>
</ul>
<p><a class="file-link" href="docs/capanne/montebar/disposizioni-per-gli-ospiti.pdf">Hinweise für die Gäste</a></p>
<p><a class="file-link" href="docs/capanne/montebar/cgc-capanna-monte-bar-it-2025.pdf">Allgemeine Geschäftsbedingungen der Capanna Monte Bar</a></p>""",
        accessi="""<p>Zu Fuss oder mit dem Mountainbike ist die Hütte ohne grosse Schwierigkeiten erreichbar, meist auf familienfreundlichen Wegen. Auch im Winter kommt man mit Ski oder Schneeschuhen hinauf, aber denken Sie daran, dass die Verhältnisse in den Bergen anders sein können als im Tal. Parkplätze im Tal sind knapp: besser mit dem öffentlichen Verkehr.</p>
<ul>
<li>Ab Corticiasca: 1 h 30.</li>
<li>Ab Bidogno: 2 h.</li>
<li>Ab Isone durch das Val Serdena und über Piandanazzo: 3 h.</li>
<li>Ab Gola di Lago: 2 h 30.</li>
<li>Ab Scareglia oder Signôra: 3 h 30.</li>
</ul>
<p>Routen auf <a href="https://schweizmobil.ch/de/map?bgLayer=pk&amp;layers=wanderland%2Cveloland&amp;season=summer&amp;highlightPointCoordinates=2721818-1106610&amp;E=2721449&amp;N=1106526&amp;resolution=4.51" rel="noopener">SchweizMobil</a>. Karte: LK 1:25’000 Blatt 1333 Tesserete.</p>
<p><strong>Sicherheit:</strong> Im Winter machen Eis und Schnee auch einfache Stellen heikel, und an steilen Hängen und in Rinnen besteht Lawinengefahr. Im Sommer weiden Mutterkühe mit Kälbern: Halten Sie Abstand und nehmen Sie Hunde an die Leine. Velofahrer nehmen bitte Rücksicht auf die Wanderer. Lassen Sie keine Abfälle zurück und machen Sie kein Feuer im Freien: Der Monte Bar wurde früher von verheerenden Bränden getroffen.</p>""",
        attivita="""<p>Die Gegend bietet unzählige Möglichkeiten für das Mountainbike, zwischen Asphalt, Naturstrassen und Singletrails, mit aussichtsreichen Runden während eines grossen Teils des Jahres: Die nationalen Routen 66, 358 und 359 beschreibt <a href="https://www.luganoregion.com/de/erleben/sport-und-natur/fahrraeder" rel="noopener">Lugano Region</a>. Von der Hütte gelangt man auch über den Passo San Lucio ins Val Cavargna oder nach Norden ins Val Serdena und nach Rivera.</p>
<p>Die Kette, die von Gola di Lago bis zum 2115 m hohen Gazzirola reicht, ist von leichten Wegen durchzogen. Die Hütte ist Ziel und Etappe des Lugano Trekking und des nationalen Wegs 52; von hier erreicht man den Camoghè und das Val Morobbia. Herbst und Frühling sind die idealen Jahreszeiten.</p>""",
        pagine=[
            dict(file="escursioni", titolo="Themenwanderungen",
                 lead="Sieben leichte Wege zwischen Geschichte, Natur und Landschaft: von den Skiträgerinnen bis zum Wild.",
                 img=("escursionista-cresta", "Wanderer auf einem grasigen Gratweg, im Hintergrund die Seen"),
                 corpo="""<p>Sieben Themenwege, um wenig bekannte Winkel zu entdecken, mit oft überraschenden Begegnungen und Entdeckungen. Alle sind leicht (T2).</p>""",
                 itinerari=[
                     dict(titolo="Der Weg der Skiträgerinnen", img=("portatrici-sci", "Historische Aufnahme von Frauen, die Ski durch den Schnee hinauftragen"),
                          testo="Er erinnert an die «Sherpa-Frauen», die vom Kirchplatz von San Barnaba die Ski der wohlhabenden Luganesi, die mit dem Postauto nach Bidogno kamen, bis zur Hütte trugen.",
                          dati=[("Länge", "4 km"), ("Höhendifferenz", "+800 m"), ("Zeit", "2 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2721402&amp;N=1105567&amp;trackId=4074166"),
                                ("Routenbeschreibung", "docs/capanne/montebar/il-sentiero-delle-portatrici-di-sci.pdf")]),
                     dict(titolo="Der Weg der Barchi", img=("barchi", "Alte Steinställe auf den Weiden unter dem Monte Bar"),
                          testo="Von Corticiasca zur Terrasse der Barchi, den typischen Bauten des Val Colla, in denen das Vieh im Frühling und im Herbst stand und die dem Monte Bar den Namen gaben.",
                          dati=[("Länge", "4 km"), ("Höhendifferenz", "+600 m"), ("Zeit", "2 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721927&amp;N=1105895&amp;trackId=4073878"),
                                ("Routenbeschreibung", "docs/capanne/montebar/barchi.pdf")]),
                     dict(titolo="Der Panoramaweg", img=("tramonto-pascoli", "Weiden im Abendlicht, die Täler im Dunst"),
                          testo="Von Roveredo, wo der Komponist Ernst Bloch von 1930 bis 1939 lebte, hinauf zu den Maiensässen, Oasen der Ruhe.",
                          dati=[("Länge", "6 km"), ("Höhendifferenz", "+900 m"), ("Zeit", "3 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2720510&amp;N=1105400&amp;trackId=4073853"),
                                ("Routenbeschreibung", "docs/capanne/montebar/panoramico.pdf")]),
                     dict(titolo="Der Gletscherweg", img=("tramonto-luganese", "Die Hütte am verschneiten Hang im Abendlicht, mit den Lichtern von Lugano"),
                          testo="Bei Gola di Lago zeugen Moore, Tümpel, fleischfressende Pflanzen und Rundhöcker von einer Zunge des Tessingletschers während der letzten Eiszeit.",
                          dati=[("Länge", "7 km"), ("Höhendifferenz", "+700 m"), ("Zeit", "3 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2719894&amp;N=1106340&amp;trackId=4074157"),
                                ("Routenbeschreibung", "docs/capanne/montebar/ghiacciai.pdf")]),
                     dict(titolo="Der Vegetationsweg", img=("genziane", "Violette Enziane im Gras"),
                          testo="Er führt durch alle Vegetationsstufen, von den insubrischen Kastanien bis zur arktisch-alpinen Zone auf dem Grat der Cima di Moncucco.",
                          dati=[("Länge", "7 km"), ("Höhendifferenz", "+800 m"), ("Zeit", "4 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722942&amp;N=1106858&amp;trackId=4074169"),
                                ("Routenbeschreibung", "docs/capanne/montebar/vegetazione.pdf")]),
                     dict(titolo="Der Aufforstungsweg", img=("piantagioni", "Die Hütte auf den goldenen Weiden des Monte Bar"),
                          testo="Ein bequemer, schattiger Weg durch einen Schutzwald, der Ende des 19. Jahrhunderts angepflanzt wurde, um den Wasserhaushalt im Tal des Cassarate zu sichern.",
                          dati=[("Länge", "7 km"), ("Höhendifferenz", "+800 m"), ("Zeit", "4 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722222&amp;N=1106106&amp;trackId=4074163"),
                                ("Routenbeschreibung", "docs/capanne/montebar/piantagioni.pdf")]),
                     dict(titolo="Der Wildweg", img=("cervo", "Ein röhrender Hirsch an einem Grashang"),
                          testo="Ein bequemer Weg durch den wilden Wald, mit überraschenden Begegnungen: Rehe, Hirsche, Eichhörnchen und Wildschweine.",
                          dati=[("Länge", "7 km"), ("Höhendifferenz", "+200 m"), ("Zeit", "3 h"), ("Schwierigkeit", "T2")],
                          link=[("Karte der Route", "https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722748&amp;N=1107781&amp;trackId=4074167"),
                                ("Routenbeschreibung", "docs/capanne/montebar/selvaggina.pdf")]),
                 ]),
            dict(file="mountain-bike", titolo="Mountainbike",
                 lead="Aussichtsreiche Runden zwischen Asphalt, Naturstrassen und Singletrails, mit Veloraum und Ladestationen in der Hütte.",
                 img=("mountain-bike", "Zwei Mountainbiker auf den Weiden, im Hintergrund der Luganersee"),
                 corpo="""<p>Die Gegend am Monte Bar bietet unzählige Möglichkeiten für das Mountainbike: Asphalt, Naturstrassen und Singletrails wechseln sich ab, in aussichtsreichen Runden, die man während eines grossen Teils des Jahres fahren kann. Die wichtigsten Routen, besonders die nationalen Routen 66, 358 und 359, beschreibt die Website von <a href="https://www.luganoregion.com/de/erleben/sport-und-natur/fahrraeder" rel="noopener">Lugano Region</a>.</p>
<p>Von der Hütte gelangt man auch über den Passo San Lucio ins Val Cavargna oder nach Norden ins Val Serdena und nach Rivera.</p>
<p>Die Hütte erfüllt den Bike-Hotel-Standard: geschlossener Veloraum, Akku-Ladestationen und kleine Werkstatt. Wir bitten alle Velofahrer um Rücksicht auf die Wanderer.</p>"""),
            dict(file="curiosita", titolo="Wissenswertes",
                 lead="Der Ursprung des Namens, die verlorenen Wälder, die «Sherpa-Frauen» und die Schalensteine des Monte Bar.",
                 img=("valle-colla", "Blick auf die Täler und die Region Lugano von den Hängen des Monte Bar"),
                 itinerari=[
                     dict(titolo="Der Ursprung des Namens", img=("valle-colla", "Blick auf die Täler und die Region Lugano von den Hängen des Monte Bar"),
                          testo="In den letzten zwei Millionen Jahren hat sich die Gegend in drei Phasen gehoben und drei Terrassen gebildet: die der Dörfer, die der «Barchi» und die der Alpen. Die Barchi, typisch für das Val Colla und die Capriasca, waren Ställe mit Heuboden nahe beim Dorf, nicht bewohnt: Die Frauen stiegen zweimal täglich zum Melken hinauf, und aus der Milch wurden zu Hause Käse und Butter. Von «barc» kommt der Name Monte Bar."),
                     dict(titolo="Der verlorene Wald", img=("bosco-nebbia", "Wälder und Weiden, die aus einem Nebelmeer ragen"),
                          testo="Früher war der Monte Bar bewaldet. Nach den Aufständen von Mailand 1848 wies Österreich die Tessiner Auswanderer aus der Lombardei aus und schloss die Grenzen: Die heimgekehrten Saisonarbeiter verschärften die Hungersnot, und für mehr Felder und Weiden wurden weite Waldflächen gerodet oder abgebrannt. Der Berg wurde kahl; nach dem schweren Hochwasser von 1896 wurden die Hänge gegen die Erosion grossflächig aufgeforstet, wie man heute noch sieht."),
                     dict(titolo="Eine Reise durch die Natur", img=("ellebori", "Blühende Christrosen im Gegenlicht"),
                          testo="In der letzten Eiszeit blieb das Eis unter 1200 m: Die eisfreien Gipfel waren eine wahre Arche Noah für Pflanzen und Tiere, und zwischen Caval Drossa und Gazzirola findet man Arten, die älter sind als die Eiszeiten, neben arktischen Pflanzen, die die Kälte bis hierher getrieben hat. Auf kleinem Raum geht man von den Kastanien über Buchen und Nadelwald bis zu Flechten, Moosen und Alpenflora auf den Gipfeln."),
                     dict(titolo="Die Tessiner «Sherpa-Frauen»", img=("portatrici-storica", "Historische Aufnahme von Trägerinnen in einer Reihe an einem Schneehang"),
                          testo="Beim Bau der ersten Hütte 1936 trugen die Frauen von Bidogno das Baumaterial im Tragkorb bis zur Baustelle; danach trugen sie die Ski der Luganesi vom Kirchplatz bis zur Hütte, für 50 Rappen pro Paar. Sie trugen auch junge Bäume zum Aufforsten hinauf, sammelten Laub und Farn als Einstreu für die Ställe und brachten im Ersten Weltkrieg den Soldaten das Essen bis zum Camoghè."),
                     dict(titolo="Schalensteine und Felszeichnungen", img=("masso-coppellare", "Ein Mann betrachtet die Zeichen auf einem Schalenstein im Wald"),
                          testo="Am Monte Bar tragen viele Felsen eingeritzte Zeichen: Schalen, Rinnen, Kreuze, Fussabdrücke, Steinkreise. Vielleicht Grenzzeichen, Orte des Sonnenkults oder der Wallfahrt, oder Vertiefungen für Regenwasser und brennendes Öl. Sehenswert sind der Grenzstein zwischen Bidogno und Corticiasca, der Fels von Gola di Lago, der «Motarell de la Stria» in Roveredo, der «Gigante» und «Ul pé del Crist» in Lelgio, die «Balena bianca» in Caslasc, die Blöcke von Pian di Sotto und der Madonnenstein von Borisio."),
                 ]),
        ],
        storia=dict(
            file="storia", titolo="Geschichte der Hütte", foto="storia",
            lead="Von der ersten Skischule des Tessins 1935 über die Hütte von 1936 bis zur neuen Hütte «Barlume» von 2016.",
            img=("capanna-1936", "Historische Aufnahme der ersten Steinhütte mit Skifahrern im Schnee"),
            corpo="""<p>Nach den Erfahrungen auf den Monti di Condra erhielt der CAS 1935 die Alphütte der Alpe Musgatina als Winterunterkunft für die erste Skischule des Kantons Tessin, mit den Lehrern Tita Calvi und Aldo Balmelli.</p>
<p>Der Erfolg war so gross, dass schon 1936, zum fünfzigjährigen Bestehen der Sektion Ticino, eine Hütte auf dem Monte Bar gebaut wurde; die Baustelle gab den vielen Saisonauswanderern des Tals Arbeit. Die Hütte wurde rasch zum Ziel zahlreicher Skifahrergruppen: Sonntags waren bis zu 300 Leute auf den Pisten. Die Winterverwaltung übernahm der Sci Club Lugano, und der Riesenslalom am Monte Bar war ein grosser Erfolg. Im Sommer war die Hütte Basislager für die Gipfel der Umgebung.</p>
<p>2013 beschloss die Sektion, eine neue Hütte zu bauen: Die Hütte von 1936, 1993 verbessert, hatte inzwischen grosse Probleme bei Logistik, Sicherheit und Versorgung. Gesucht war ein moderner, zweckmässiger und ökologischer Bau mit dem Charakter einer klassischen Berghütte. Das Projekt entstand mit der Gemeinde Capriasca (Projekt Areaviva) und verschiedenen lokalen Partnern, um die ganze Region aufzuwerten.</p>
<p>Den Wettbewerb von 2014 gewann unter dreissig Projekten «Barlume» der Architekten Oliviero Piffaretti und Carlo Romano (Atelier PeR, Mendrisio): ein einfacher, kubischer Holzbau rund um die Feuerstelle als Symbol der Begegnung. Der Berg bleibt das prägende Element, und die Hütte ist eine Laterne in der Landschaft. 2016 eingeweiht, 80 Jahre nach der ersten Hütte, auf 1602 m auf den südseitigen Weiden, ist sie vielleicht die schönste Terrasse über Lugano, den Voralpen, dem Apennin mit dem Monviso, dem Monte Rosa und den Tessiner Alpen, mit unvergesslichen Sonnenuntergängen.</p>
<p><a href="https://www.simonemengani.ch/nuovo-servizio-fotografico-capanna-monte-bar/" rel="noopener">Fotos des Baus von Simone Mengani</a></p>"""),
        sostenitori=dict(
            testo="Die neue Hütte entstand dank diesen Unterstützern und über 300 Freunden, öffentlichen und privaten, die zu ihrem Bau beigetragen haben. Herzlichen Dank!",
            loghi=[("Republik und Kanton Tessin", "cantone-ticino"), ("Swisslos", "swisslos"), ("Stadt Lugano", "citta-di-lugano"),
                   ("Gemeinde Capriasca", "comune-di-capriasca"), ("Banca Raiffeisen del Cassarate", "raiffeisen"), ("BancaStato", "bancastato"),
                   ("Cornèr Banca", "corner-banca"), ("EFG", "efg"), ("Lugano Turismo", "lugano-turismo"), ("Revifida", "revifida"),
                   ("Ernst Göhner Stiftung", "ernst-gohner-stiftung"), ("Lambertini, Ernst & Partners", "lambertini-ernst-partners"),
                   ("Blue Planet", "blue-planet"), ("The North Face und VF", "the-north-face-vf"), ("Ente regionale per lo sviluppo del Luganese", "ersl")]),
        foto=[("Die Hütte", "capanna"), ("Die Küche", "cucina"), ("Die Umgebung", "dintorni")],
    ),

    "baitadelluca.html": dict(
        cartella="baitadelluca",
        capanna_titolo="Die Baita",
        capanna="""<p>Die Baita hat 16 Schlafplätze in zwei Räumen mit 4 und 12 Plätzen, eine Stube mit Gasküche und Cheminée, warmes Wasser und Dusche; das Licht kommt von Solarzellen. Geschirr und Pfannen sind vorhanden, Getränke gibt es in beschränkter Menge. Mässiger Empfang, kein WLAN und kein Telefon.</p>
<p>Sie ist nicht bewartet: Die Tür ist abgeschlossen, den Code erhalten Sie von der Verantwortlichen. Schnell und einfach erreichbar, wird sie auch für Kurse, Ausbildungstage oder einfach für ein gemeinsames Abendessen genutzt.</p>""",
        tariffe=[
            ("Mitglieder SAC/FAT/CAI/DAV", "Übernachtung, Taxen inbegriffen",
             [("Erwachsene ab 22 Jahren", "Fr. 15.–"), ("Jugendliche von 6 bis 21 Jahren, Bergführer-Aspiranten und SAC-Tourenleiter", "Fr. 8.–"),
              ("Kinder bis 5 Jahre", "gratis"), ("Bergführer IFMGA", "gratis")]),
            ("Nichtmitglieder", "Übernachtung, Taxen inbegriffen",
             [("Erwachsene ab 20 Jahren", "Fr. 25.–"), ("Jugendliche von 6 bis 19 Jahren", "Fr. 12.–"), ("Kinder bis 5 Jahre", "gratis")]),
            ("Zuschläge", "Der Hüttenschlafsack ist obligatorisch und in der Baita nicht erhältlich",
             [("Gas zum Kochen (pro Tag)", "Fr. 5.–"), ("Brennholz (pro Tag)", "Fr. 5.–"), ("Dusche (pro Person)", "Fr. 5.–")]),
        ],
        prenotare="""<ul>
<li><strong>Reservation unerlässlich</strong> per E-Mail an <a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>, mit Vorname, Name, Adresse und Handynummer.</li>
<li>Kostenlose Annullierung bis 18 Uhr <strong>zwei Tage vor</strong> dem reservierten Datum.</li>
<li>Den Code zum Schlüssel erhalten Sie von den Verantwortlichen; im Winter wird die Tür auf Anfrage und je nach Wetter geöffnet.</li>
<li>Bringen Sie Hüttenschlafsack und Kissenbezug (55×80) mit.</li>
<li>Bezahlung mit dem QR-Code (im Hüttenbuch) oder mit Twint.</li>
<li>Rauchen ist streng verboten; Hunde sind nur in der Stube erlaubt, nicht im Schlafraum.</li>
<li>Keine Reservationen oder Anfragen über soziale Medien: Rufen Sie bitte an.</li>
</ul>
<p><a class="file-link" href="docs/capanne/baitadelluca/2020-cgc-capanne-cas-it.pdf">Allgemeine Geschäftsbedingungen der SAC-Hütten</a></p>""",
        accessi="""<ul>
<li>Ab Rosone (Bus): 45 min, +270 m, T2 (<a href="https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2722290&amp;N=1102884&amp;layers=Wanderland%2CStation&amp;trackId=5273099" rel="noopener">Route</a>).</li>
<li>Ab Sonvico (Bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721523&amp;N=1102174&amp;layers=Wanderland%2CStation&amp;trackId=5273106" rel="noopener">Route</a>).</li>
<li>Ab Villa Luganese (Bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=de&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721748&amp;N=1101916&amp;layers=Wanderland%2CStation&amp;trackId=5273108" rel="noopener">Route</a>).</li>
</ul>
<p>Karte: LK 1:25’000 Blatt 1333 Tesserete.</p>""",
        pagine=[
            dict(file="attivita", titolo="Wandern und Klettern",
                 lead="Wanderungen zu den Gipfeln und Hütten der Umgebung, über 200 Routen im Kalk der Denti della Vecchia und die Lugano Bike 66.",
                 img=("sentiero-denti", "Ein Wanderer auf dem Weg unter den Felstürmen der Denti della Vecchia"),
                 itinerari=[
                     dict(titolo="Wandern", img=("sentiero-denti", "Ein Wanderer auf dem Weg unter den Felstürmen der Denti della Vecchia"),
                          testo="Von der Baita zur Alpe Bolla 3 h, nach Villa Luganese 3 h, auf den Gipfel der Fojorina 4 h; von Brè zur Baita 4-5 h; von der Baita zur Capanna San Lucio 4 h und zur <a href=\"de/montebar.html\">Capanna Monte Bar</a> 6 h, oder 9 h über die Gipfel von Fojorina und Gazzirola.",
                          link=[("Aus dem Archiv, 1997: Prealpi ticinesi 5, vom Passo San Jorio zum Monte Generoso", "docs/capanne/baitadelluca/baita-del-luca-prealpi-ticinesi-5-passo-s-jorio-generoso.pdf")]),
                     dict(titolo="Klettern", img=("arrampicata-denti", "Kletterer an den Kalkplatten der Denti della Vecchia"),
                          testo="Die Denti della Vecchia sind ein Kletterparadies mit über 200 Routen im Kalk. Der Führer der Gruppo Scoiattoli ist online auf <a href=\"https://scoiattoli.ch/\" rel=\"noopener\">scoiattoli.ch</a>; in der Baita liegt auch die gedruckte Ausgabe zum Nachschlagen.",
                          link=[("Kletterführer Denti della Vecchia (Gruppo Scoiattoli)", "https://scoiattoli.ch/wp-content/uploads/2020/06/GUIDA-DENTI-DELLA-VECCHIA-.pdf"),
                                ("Denti della Vecchia: neue Routen 2023", "docs/capanne/baitadelluca/denti-news-2023.pdf"),
                                ("Denti della Vecchia: Nirvana 2023", "docs/capanne/baitadelluca/denti-nirvana-news-2023.pdf"),
                                ("Denti della Vecchia: Paléo 2023", "docs/capanne/baitadelluca/denti-paleo-news-2023.pdf")]),
                     dict(titolo="Mountainbike", img=("mountain-bike", "Ein Mountainbiker auf einem Waldweg"),
                          testo="Mehrere Routen führen durch die Umgebung, und die Baita liegt ganz in der Nähe der Route Lugano Bike 66.",
                          link=[("Mountainbike auf Lugano Region", "https://www.luganoregion.com/de/erleben/sport-und-natur/fahrraeder")]),
                 ]),
        ],
        foto=[("Die Baita", "capanna"), ("Die Umgebung", "dintorni")],
        foto_lead="Die Baita und die Umgebung",
    ),
}
