"""Versione francese delle pagine capanna: stessa struttura di capanne.py (CONTENUTI) e dei dati di pagine_capanne.py (HUT_PAGES, HUTS).

Le pagine francesi si generano in fr/ (fr/campotencia.html, fr/capanne/<cartella>/<pagina>.html).
I link ad altre pagine tradotte si scrivono già con fr/ davanti (es. "fr/motterascio.html"); quelli a pagine solo in
italiano (news, attività, PDF) restano senza. Immagini, gallerie e PDF sono gli stessi della versione italiana.
Francese di Svizzera; i nomi propri delle capanne restano in italiano («Capanna Cristallina»).
Traduzione da far rileggere a chi parla francese."""
from capanne import PRENOTA  # noqa: F401  (stesso formato del link di prenotazione)

CT_DOC = "docs/capanne/campotencia/"

# testi di HUT_PAGES (pagine_capanne.py) in francese: sostituiscono quelli italiani, il resto (quota, foto, contatti…) resta uguale
HUT_FR = {
    "campotencia.html": dict(
        where="Val Piumogna, Léventine", custody="de mi-juin à mi-octobre",
        description="Capanna Campo Tencia, 2140 m, dans le Val Piumogna (Léventine) : 80 places, gardiennée de mi-juin à mi-octobre. Contacts et réservation.",
        intro="Posée sur une terrasse au-dessus du haut Val Piumogna, c’est la base idéale pour des randonnées, des traversées vers d’autres cabanes et des ascensions comme le Pizzo Campo Tencia qui, avec ses 3072 m, est le plus haut sommet entièrement tessinois.",
        stay=[("Ouverture", "Toute l’année"),
              ("Gardiennage", "De mi-juin à mi-octobre ; en hiver non gardiennée, mais la réservation est obligatoire ; pour les grands groupes, ouverture possible en accord avec les gardiens"),
              ("Places", "80"),
              ("Repas", "Plats chauds, servis toute la journée par les gardiens"),
              ("Local d’hiver", "Toujours ouvert, avec boissons et bois")],
        reach=[("Accès en été", "De Dalpe 3 h ; du lac Tremorgio (téléphérique depuis Rodi) 3 h 30 ; de Fusio par le Passo Campolungo 6 h"),
               ("Accès en hiver", "De Dalpe 3 h, à skis par le Val Piumogna"),
               ("Carte", 'Carte nationale 1272 Campo Tencia, coordonnées <span class="num">699.430 / 144.480</span>')],
        contact=[("Gardiens", "Valeria Grandi et Paco Porcu"),
                 ("Téléphone de la cabane", '<a class="num" href="tel:+41918671544">+41 91 867 15 44</a>'),
                 ("Portable", '<a class="num" href="tel:+41767212572">+41 76 721 25 72</a>'),
                 ("E-mail", '<a href="mailto:campotencia@casticino.ch">campotencia@casticino.ch</a>')]),
    "cristallina.html": dict(
        where="Passo Cristallina, Val Bedretto", custody="de juin à mi-octobre ; en hiver les week-ends et jours fériés",
        description="Capanna Cristallina, 2575 m, sur le col entre la Léventine et le Val Maggia : 100 places, gardiennée de juin à mi-octobre et les week-ends et jours fériés d’hiver. Contacts et réservation.",
        intro="Conçue par les architectes Baserga et Mozzetti et inaugurée en 2003, c’est la première cabane moderne construite par le Club Alpin Suisse. Elle se dresse sur le col, à un point stratégique entre la Léventine et le Val Maggia : une étape panoramique sur les traversées vers Robiei, le Naret, le Campo Tencia et le San Giacomo. Le tour des lacs du Cristallina, en un ou deux jours, convient aussi aux familles ; en une heure on atteint le Cristallina et la Cima di Lago. En hiver, accessible surtout par le nord, elle ouvre sur de superbes pentes vers le Val Bedretto, Robiei et le Val Formazza.",
        stay=[("Ouverture", "Toujours ouverte et accessible"),
              ("Gardiennage", "De juin à mi-octobre ; en hiver, de décembre à fin avril, si les conditions sont bonnes, les week-ends, les jours fériés et pour les groupes"),
              ("Places", "100"),
              ("Repas", "Préparés toute la journée par le gardien"),
              ("Boissons", "Disponibles aussi en l’absence du gardien")],
        reach=[("Accès en été", "D’Ossasco 3 h 30 ; de Robiei 3 h ; du lac du Narèt 2 h 30 ; du Passo San Giacomo 4 h"),
               ("Accès en hiver", "D’Ossasco 3 h ; d’All’Acqua 4 h"),
               ("Carte", 'Carte nationale 1251 Bedretto, coordonnées <span class="num">683.550 / 147.300</span>')],
        contact=[("Gardien", "Emanuele Vellati"),
                 ("Téléphone", '<a class="num" href="tel:+41918692330">+41 91 869 23 30</a>'),
                 ("E-mail", '<a href="mailto:cristallina@casticino.ch">cristallina@casticino.ch</a>')]),
    "adula.html": dict(
        where="Haut Val Carassino, Val Soi, Blenio", custody="de fin mai à mi-octobre",
        description="Capanna Adula, 2012 m, entre le Val Carassino et le Val Soi (Blenio) : 24 places, ouverte toute l’année, gardiennée de fin mai à mi-octobre. Contacts et réservation.",
        intro="La « Bassa », comme on l’a toujours appelée, a le charme des cabanes d’autrefois : construite en pierre, une salle commune chargée d’histoire, des dortoirs où ont dormi des milliers d’alpinistes, un accueil chaleureux et une cuisine du terroir. Depuis ce balcon au-dessus du Val Blenio, on part vers le sommet de l’Adula (Rheinwaldhorn) ou, par des sentiers faciles, vers d’autres cabanes ; les itinéraires sauvages du Val Carassino offrent des randonnées aventureuses. Pour les moins ambitieux : une promenade dans la vallée, un bon repas et une sieste au soleil.",
        stay=[("Ouverture", "Toute l’année"),
              ("Gardiennage", "De fin mai à mi-octobre"),
              ("Places", "24"),
              ("Repas", "Préparés par le gardien ; cuisine autonome seulement en hiver ou en accord avec le gardien"),
              ("Boissons", "Disponibles aussi en l’absence du gardien")],
        reach=[("Accès en été", "De Compietto par le Val Carassino 2 h 40 (à VTT environ 1 h) ; de Dangio par le Val Soi 3 h ; de Cusiè (Val Malvaglia) par le Passo del Laghetto 5 h"),
               ("Accès en hiver", "De Dangio 3 h 30 ; de Ghirone 5 h"),
               ("Carte", 'Carte nationale 1253 Olivone, coordonnées <span class="num">719.510 / 150.950</span>')],
        contact=[("Gardien", "Raffaele « Lele » Demaldi"),
                 ("Téléphone de la cabane", '<a class="num" href="tel:+41918721532">+41 91 872 15 32</a>'),
                 ("Portable", '<a class="num" href="tel:+41795352112">+41 79 535 21 12</a>'),
                 ("E-mail", '<a href="mailto:adula@casticino.ch">adula@casticino.ch</a>')]),
    "motterascio.html": dict(
        where="Alpe Motterascio, Greina, Blenio", custody="de mi-juin à mi-octobre",
        description="Capanna Motterascio, 2172 m, au bord de la Greina (Blenio) : 70 places, ouverte toute l’année, gardiennée de mi-juin à mi-octobre. Contacts et réservation.",
        intro="Inaugurée en 1967 et agrandie en 1980, 1990 et 2006, la cabane se trouve au bord d’une réserve naturelle extraordinaire : la Greina, avec ses marais, ses tourbières, ses alpages et sa flore intacte. Point de départ d’itinéraires fascinants, surtout vers l’arche de la Greina, la plus grande arche rocheuse naturelle du Tessin.",
        stay=[("Ouverture", "Toute l’année"),
              ("Gardiennage", "De mi-juin à mi-octobre (en 2026 du 13 juin au 10 octobre) ; en hiver le local d’hiver de 10 places, sur réservation"),
              ("Places", "70"),
              ("Repas", "Repas chauds, préparés toute la journée par les gardiens"),
              ("Boissons", "Disponibles aussi en l’absence du gardien")],
        reach=[("Accès en été", "De l’Alpe Garzott (lac de Luzzone) 2 h ; du barrage de Luzzone 3 h 30 ; de Pian Geirètt 3 h 30 ; de Ghirone par le Val Camadra 6 h"),
               ("Accès en hiver", "De Ghirone par le Val Camadra et le col de la Greina, 5-6 h, seulement avec une neige stable"),
               ("Carte", 'Carte nationale 1233 Greina, coordonnées <span class="num">720.075 / 161.425</span>')],
        contact=[("Gardien", "Fabio Merzaghi"),
                 ("Réservation", '<a class="num" href="tel:+41918721622">+41 91 872 16 22</a> (de mi-juin à mi-octobre)'),
                 ("Portable", '<a class="num" href="tel:+41797276905">+41 79 727 69 05</a>'),
                 ("E-mail", '<a href="mailto:motterascio@casticino.ch">motterascio@casticino.ch</a>')]),
    "montebar.html": dict(
        where="Alta Capriasca, région de Lugano", custody="toute l’année",
        description="Capanna Monte Bar, 1602 m, dans l’Alta Capriasca : 42 places en chambres de 2, 4 et 6 lits, gardiennée toute l’année, standard Bike Hotel. Contacts et réservation.",
        intro="Sur un sommet arrondi d’une beauté exceptionnelle, avec une vue à 180 degrés des Denti della Vecchia au Tamaro et, à l’ouest, sur les quatre-mille valaisans, des Mischabel au Mont Rose. Reconstruite en automne 2016 : chambres de 2, 4 et 6 lits, toilettes à chaque étage, une salle à manger pour environ 80 personnes, une salle de réunion pour 20, une grande terrasse et un local fermé avec bornes de recharge pour vélos électriques et un petit atelier, au standard Bike Hotel.",
        stay=[("Ouverture", "Toute l’année ; sur demande aussi pour des événements, dîners et repas de midi"),
              ("Gardiennage", "Tous les jours de mai à début novembre ; en hiver du vendredi midi au dimanche midi, les jours fériés et pendant les vacances scolaires"),
              ("Places", "42, en chambres de 2, 4 et 6 lits"),
              ("Repas", "Cuisine régionale avec des produits locaux ; menus spéciaux sur réservation"),
              ("Sans gardiens", "La cabane est fermée ; seul un petit local d’entrée reste ouvert pour les urgences")],
        reach=[("Accès en été", "De Corticiasca 1 h 30 ; de Bidogno 2 h ; d’Isone par le Val Serdena et Piandanazzo 3 h ; de Gola di Lago 2 h 30"),
               ("VTT", "Route forestière Bidogno-Rompiago, descente vers Scareglia ou Signôra ; Piandanazzo-Al Matro-Serdena-Isone ; Piandanazzo-Alpe Pietra Rossa-San Lucio-Bogno"),
               ("Accès en hiver", "De Corticiasca et de Gola di Lago"),
               ("Carte", 'Carte nationale 1333 Tesserete, coordonnées <span class="num">721.800 / 106.610</span>')],
        contact=[("Gardiens", "James Mauri et Serge Santese"),
                 ("Téléphone", '<a class="num" href="tel:+41919663322">+41 91 966 33 22</a>'),
                 ("E-mail", '<a href="mailto:montebar@casticino.ch">montebar@casticino.ch</a>')]),
    "baitadelluca.html": dict(
        where="Cioascio, Sonvico", custody="sur réservation",
        description="Baita del Luca, 1070 m, au-dessus de Sonvico au pied des Denti della Vecchia : 16 places, cuisine autonome, uniquement sur réservation.",
        intro="Sur un large versant herbeux au-dessus de Sonvico, au pied des Denti della Vecchia : le point de départ idéal pour des randonnées, aussi en famille, et pour l’escalade dans un paysage unique.",
        stay=[("Ouverture", "Toute l’année, uniquement sur réservation"),
              ("Places", "16"),
              ("Repas", "Cuisine autonome, cuisine à disposition"),
              ("Boissons", "Disponibles en quantité limitée"),
              ("Réservation", "Le code d’accès est envoyé après le paiement anticipé")],
        reach=[("Accès", "De Rosone 45 min ; de Lovarescia (au-dessus de Sonvico) 60 min ; de Car et Luss (Villa Luganese) 60 min"),
               ("Carte", 'Carte nationale 1333 Tesserete, coordonnées <span class="num">722.980 / 102.600</span>')],
        contact=[("Responsable", "Priska Deluigi, 6960 Odogno"),
                 ("Portable", '<a class="num" href="tel:+41792033084">+41 79 203 30 84</a>'),
                 ("E-mail", '<a href="mailto:pristh@bluewin.ch">pristh@bluewin.ch</a>'),
                 ("Réservation", '<a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>')]),
}

# schede della home francese e delle «altre capanne»: stessi campi di HUTS in pagine_capanne.py
HUTS_FR = [
    ("campotencia.html", "Campo Tencia", "2140", "Val Piumogna", "Gardiennée juin–oct.", "Sur une terrasse au-dessus du Val Piumogna, la base pour le Pizzo Campo Tencia, le plus haut sommet entièrement tessinois.", "80 places", "Dalpe 3 h", "capanne/campotencia-3x2", (987, 658), True),
    ("cristallina.html", "Cristallina", "2575", "Val Bedretto", "Gardiennée été et hiver", "Sur le col du même nom entre la Léventine et le Val Maggia. Inaugurée en 2003, la première cabane moderne du CAS.", "100 places", "Ossasco 3 h 30", "capanne/cristallina-3x2", (837, 558), True),
    ("adula.html", "Adula", "2012", "Val Carassino", "Gardiennée mai–oct.", "La cabane de pierre classique au-dessus du Val Blenio : histoire, accueil chaleureux et cuisine du terroir.", "24 places", "Compietto 2 h 40", "capanne/adula-3x2", (1000, 667), False),
    ("motterascio.html", "Motterascio", "2172", "Greina", "Gardiennée juin–oct.", "Au bord du haut plateau protégé de la Greina : tourbières, alpages et la plus grande arche rocheuse naturelle du Tessin.", "70 places", "Garzott 2 h", "capanne/motterascio-3x2", (974, 649), False),
    ("montebar.html", "Monte Bar", "1602", "Alta Capriasca", "Toute l’année", "Le balcon au-dessus de Lugano, reconstruit en 2016 : vue du Mont Rose aux Denti della Vecchia, standard Bike Hotel.", "42 places", "Corticiasca 1 h 30", "capanne/montebar-3x2", (663, 442), False),
    ("baitadelluca.html", "Baita del Luca", "1070", "Denti della Vecchia", "Sur réservation", "Au-dessus de Sonvico, au pied des Denti della Vecchia. Idéale pour les familles et l’escalade.", "16 places, cuisine autonome", "Rosone 45 min", "capanne/baitadelluca-3x2", (1000, 667), False),
]

CONTENUTI_FR = {
    "campotencia.html": dict(
        cartella="campotencia",
        capanna="""<p>La première cabane des montagnes tessinoises a été construite en 1912 au pied du sommet du même nom, côté Léventine, dans le haut Val Piumogna. C’est un camp de base pour familles, randonneurs et alpinistes : promenades dans la nature, le lac Morghirolo tout proche, les jardins d’escalade et les grandes courses du groupe du Campo Tencia, avec la traversée classique de la Cresta dei Corni.</p>
<p>Le bâtiment actuel, conçu par l’architecte de la section Oscar Hofmann et inauguré en 1977, compte trois niveaux : au rez-de-chaussée l’entrée, le local à chaussures, les toilettes et la cave ; au premier étage une salle commune lumineuse de 70 places et la cuisine ; au deuxième environ 70 places dans 7 dortoirs, certains de 4 à 8 places, idéaux pour les familles.</p>
<p>Les lits ont des duvets ; <strong>le sac à viande est obligatoire</strong>. La cabane a gardé son caractère des années 1980 : pas de chambres individuelles avec salle de bain ni de sèche-cheveux !</p>""",
        cucina="""<p>Un menu simple et sincère au goût local, mais pas seulement tessinois : assiettes froides de charcuterie et de fromages de la région, soupes, gnocchis frais et polenta avec différents accompagnements, selon la saison et les disponibilités.</p>
<p>Pour les hôtes qui passent la nuit, nous cuisinons des spécialités de la région, avec un menu qui change selon l’occasion, inspiré de la montagne et d’ailleurs.</p>
<p>Végétariens, végans et hôtes avec un régime particulier sont les bienvenus : merci de nous prévenir à temps, pour que nous puissions bien accueillir chacun.</p>""",
        team=dict(img=("guardiani", "Valeria et Paco, gardiens de la Capanna Campo Tencia")),
        accessi=f"""<p>En été, la cabane s’atteint facilement à pied, par des sentiers adaptés aux familles ; en hiver à skis depuis Dalpe par le Val Piumogna.</p>
<p><strong>Pour Dalpe :</strong> du nord ou du sud par l’A2, sortie Rodi-Quinto ; en transports publics jusqu’à Rodi, puis en <a href="https://www.postauto.ch/fr" rel="noopener">CarPostal</a>.</p>
<ul>
<li>De Dalpe (1192 m) : 3 h.</li>
<li>Du lac Tremorgio (1849 m), station supérieure du téléphérique depuis Rodi : 3 h 30.</li>
<li>De Fusio (Val Lavizzara) par le Passo Campolungo (2318 m) : 6 h.</li>
<li>En hiver depuis Dalpe : 3 h.</li>
</ul>
<p>Cartes : carte nationale 1:25 000 feuille 1272 Campo Tencia ; 1:50 000 feuille 266 S Valle Leventina. Itinéraires sur <a href="https://map.schweizmobil.ch/?lang=fr&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2699408&amp;N=1146376" rel="noopener">SuisseMobile</a>.</p>
<p><a class="file-link" href="{CT_DOC}aet-pieghevole-tremorgio.pdf">Téléphérique Rodi-Tremorgio : horaires et prix</a></p>""",
        attivita="""<p>Pas seulement le Campo Tencia ! Le Val Piumogna est idéal pour vivre la montagne dans toute sa variété et à tout âge : le district franc fédéral, les alpages, le sentier géologique du Campolungo, la cyanite du Forno et les lacs de montagne, rafraîchissants même les jours les plus chauds.</p>
<p>Le massif offre de nombreuses courses : la classique Cresta dei Corni, des ascensions comme le Pizzo Campo Tencia, des traversées vers les cabanes Leìt, Sponda, Barone et Garzonera. La cabane se trouve à mi-chemin de la <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, l’itinéraire de 100 km du col du Nufenen au lac Majeur. Les jardins d’escalade près de la cabane sont idéaux pour des cours avec des enfants et des débutants ; en hiver, il y a des randonnées à skis exigeantes et des cascades de glace.</p>""",
        storia=dict(
            file="storia", titolo="Histoire de la cabane",
            lead="Depuis 1912, la première cabane des montagnes tessinoises : agrandie, détruite par un incendie et reconstruite plus belle qu’avant.",
            img=("inaugurazione-1912", "Carte postale de l’inauguration de la cabane le 10 août 1912, avec des alpinistes devant la cabane en pierre"),
            corpo="""<p>La cabane a été construite en 1912 au pied du sommet du même nom, côté Léventine, dans le haut Val Piumogna. Le nom Campo Tencia a été inventé en 1858 : on l’a donné à la plus haute montagne entièrement tessinoise (3072 m) lors de l’établissement de la célèbre carte Dufour. Il réunit les noms de deux alpages du Patriziato di Prato, Campo et Tencia, dans le haut Val Lavizzara, côté Val Maggia.</p>
<p>La cabane a été inaugurée le 11 août 1912 (le 10 août selon certaines sources d’archives). En 1932, Patocchi, toujours moteur du projet, présenta les plans d’un agrandissement, et l’été 1933 la nouvelle aile est fut construite.</p>
<figure><img src="assets/img/capanne/campotencia/costruzione.webp" alt="Des hommes au travail devant l’ancienne cabane en pierre, photographie historique" width="1200" height="832" loading="lazy" decoding="async"></figure>
<p>Quarante ans plus tard suivirent d’autres travaux pour la renforcer et l’améliorer. Le 22 août 1975, un grave incendie détruisit le travail de nombreuses années.</p>
<p>Les travaux commencèrent aussitôt, et la cabane fut reconstruite plus grande, plus belle et plus pratique. Sa construction fut une première en Suisse, grâce à l’architecte Oscar Hofmann : non plus l’image anguleuse de la cabane de montagne classique, mais un aspect nouveau, léger et élégant, avec une structure porteuse en acier, revêtue et isolée pour l’altitude. La nouvelle inauguration eut lieu le 25 septembre 1977.</p>
<figure><img src="assets/img/capanne/campotencia/capanna-storica.webp" alt="L’ancienne cabane en pierre dans la neige, photographie historique" width="1200" height="782" loading="lazy" decoding="async"></figure>
<p>En 2008, l’aile nord a accueilli une nouvelle cuisine professionnelle. Le 11 août 2012, la cabane a fêté son centenaire. En 2022, une turbine hydraulique a été installée pour l’alimentation électrique, l’installation photovoltaïque agrandie et l’épuration des eaux usées renouvelée.</p>"""),
        pagine=[
            dict(file="escursioni-facili", titolo="Randonnées faciles",
                 lead="Sur des sentiers blanc-rouge-blanc, entre alpages, lacs de montagne et le district franc fédéral du Campo Tencia.",
                 img=("lago-morghirolo-fiori", "Linaigrettes en fleur au bord du lac Morghirolo"),
                 corpo="""<p>Entre Leìt et Tencia, les randonnées traversent un paysage naturel précieux : le district franc fédéral du Campo Tencia, le sentier géotouristique du Campolungo, les alpages et de nombreux lacs de montagne pour une baignade ou un pique-nique.</p>""",
                 itinerari=[
                     dict(titolo="Lac Morghirolo", img=("lago-morghirolo", "Le lac Morghirolo au pied des sommets du groupe du Campo Tencia"),
                          testo="Après une pause à la cabane, pourquoi ne pas monter jusqu’au beau lac de montagne pour une baignade rafraîchissante ?",
                          dati=[("Longueur", "1,4 km"), ("Montée", "+250 m"), ("Temps", "1 h aller et retour"), ("Difficulté", "T2")],
                          link=[("Description de l’itinéraire", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                     dict(titolo="Sentier didactique", img=("torrente-piumogna", "Le torrent Piumogna dans les prés de la vallée"),
                          testo="Une boucle au départ et à l’arrivée de Piumogna, par la Capanna Campo Tencia et l’Alpe Morghirolo, avec des panneaux sur la nature. On peut y ajouter le lac Morghirolo (environ 1 h de plus, aller et retour) ou manger à la cabane et boucler le tour l’après-midi par l’Alpe Morghirolo.",
                          dati=[("Longueur", "12 km"), ("Montée", "+1300 m"), ("Temps", "4-5 h"), ("Difficulté", "T3")],
                          link=[("Carte en ligne", "https://s.geo.admin.ch/151dbckh2v17"),
                                ("Description de l’itinéraire", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                 ]),
            dict(file="giro-piumogna", titolo="Tour du Piumogna",
                 lead="Une boucle depuis Dalpe par les cabanes Leìt et Campo Tencia, à travers une zone protégée riche en fleurs.",
                 img=("lago-leit", "Le lac de montagne au pied des sommets du groupe du Campo Tencia"),
                 corpo="""<p>Un itinéraire fantastique à travers une région particulièrement riche en fleurs, reconnue et protégée au niveau national pour sa géologie : ancolies des Alpes, gentianes, anémones, nigritelles, rhododendrons, renoncules des montagnes et primevères de Haller.</p>
<p>De Dalpe, on monte par les splendides forêts de Boscobello jusqu’au Passo Vanitt puis, par un beau sentier panoramique, jusqu’à la Capanna Leìt. Le long du lac, on passe au pied du Pizzo Prèvat, un sommet apprécié des grimpeurs, connu aussi comme le « petit Cervin ». Après le Passo Leìt et la Bocchetta Lei di Cima apparaissent les sommets du groupe du Campo Tencia, dont le plus haut (3072 m) est le plus haut entièrement tessinois. À la descente, on passe par le lac Morghirolo, d’où la Capanna Campo Tencia est à une demi-heure. Le retour suit le Val Piumogna, avec son beau torrent et plusieurs alpages.</p>
<figure><img src="assets/img/capanne/campotencia/pascoli-piumogna.webp" alt="Pâturages avec un cairn et un balisage blanc-rouge-blanc" width="1200" height="659" loading="lazy" decoding="async"></figure>
<h2>Aller et retour depuis Dalpe</h2>
<p>De Dalpe (en CarPostal depuis Rodi-Fiesso ou Airolo), suivre le sentier vers Boscobello, passer l’Alpe Cadonighino et franchir le Passo Vanitt (2138 m). On atteint la Capanna Leìt et son lac (2260 m) et on continue vers la Capanna Campo Tencia : après le Passo Leìt (2431 m) et la Bocchetta Lei di Cima (2481 m), on arrive aux chalets de Lei di Cima (2400 m). Le nouveau sentier mène au lac Morghirolo (2264 m) et, en une demi-heure, à la Capanna Campo Tencia (2140 m), au-dessus du Val Piumogna. À la descente, suivre le sentier de la vallée jusqu’aux chalets de Piumogna, puis la route vers Boscobello ; peu après le pont de Polpiano, un sentier à droite descend à Dalpe.</p>
<p>On peut aussi partir de Rodi-Fiesso, prendre le téléphérique jusqu’au lac Tremorgio et suivre le sentier vers la Capanna Leìt, ou faire le tour dans l’autre sens. <strong>Attention :</strong> l’étape est longue ; une nuit à la cabane est conseillée.</p>
<figure><img src="assets/img/capanne/campotencia/cascina-piumogna.webp" alt="Un chalet d’alpage parmi les mélèzes du Val Piumogna, avec des sommets enneigés derrière" width="1200" height="900" loading="lazy" decoding="async"></figure>""",
                 dati=[("Longueur", "19 km"), ("Montée", "+1330 / −1330 m"), ("Temps", "8 h"), ("Difficulté", "T2"),
                       ("Points forts", "Boscobello, Capanna Leìt, Pizzo Prèvat, lac Leìt, les chalets de Lei di Cima, le groupe du Campo Tencia, le lac Morghirolo, les alpages de Croslina et Geira")],
                 link=[("Carte en ligne de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2700579&amp;N=1146079&amp;trackId=4267446")]),
            dict(file="escursionismo-alpino", titolo="Randonnée alpine",
                 lead="Hors des sentiers battus : les sommets du Campo Tencia, du Forno et du Campolungo, dès T4.",
                 img=("segnavia-alpino", "Balisage blanc-bleu-blanc sur un rocher, avec les sommets derrière"),
                 corpo="""<p>La difficulté des randonnées se mesure sur l’échelle T en six niveaux, de T1 (randonnée) à T6 (randonnée alpine difficile). Autour du Campo Tencia, les possibilités sont nombreuses : les ascensions du Pizzo Campo Tencia, du Pizzo Forno ou du Campolungo. Les itinéraires ne sont que partiellement balisés et un bon sens de l’orientation est nécessaire ; il peut y avoir des dangers objectifs et, en début d’été, des restes de neige : partez bien préparés.</p>
<p><a href="https://www.sac-cas.ch/fr/formation-et-securite/" rel="noopener">Formation et sécurité : les conseils du CAS</a></p>""",
                 itinerari=[
                     dict(titolo="Pizzo Campo Tencia (3072 m) et Pizzo Croslina (3012 m)", img=("croce-campo-tencia", "La croix sommitale du Pizzo Campo Tencia"),
                          testo="La plus haute montagne entièrement tessinoise doit son nom à sa roche rougeâtre, riche en fer : « tencie », c’est-à-dire sale, en dialecte. Au centre du canton, elle offre une vue panoramique ; du sommet on peut descendre dans le Val Lavizzara ou rejoindre la Via Alta Vallemaggia. L’itinéraire est en grande partie balisé ; par endroits, attention aux chutes de pierres, surtout s’il y a d’autres personnes. En début d’été, il y a de la neige dans la cuvette sous la Bocchetta di Croslina. Du col (2864 m), on peut traverser vers le nord jusqu’à l’arête qui mène au Pizzo Croslina : passages exposés, prudence surtout à la descente.",
                          dati=[("Longueur", "3 km"), ("Montée", "+940 m"), ("Temps", "3 h pour le Pizzo Campo Tencia, 4 h avec le Pizzo Croslina"),
                                ("Difficulté", "T4+ Pizzo Campo Tencia, T6 avec le Pizzo Croslina"), ("Équipement", "Bonnes chaussures de montagne")],
                          link=[("Description détaillée", "capanne/campotencia/tencia-croslina.html"),
                                ("Description de l’itinéraire", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")]),
                     dict(titolo="Pizzo Forno (2907 m)", img=("pizzo-forno", "Le Pizzo Forno et le Pizzo Laghetto avec les derniers névés"),
                          testo="L’étape 5 de la Via Idra suit la Senda del Ghiacciaio jusqu’au Passo del Ghiacciaione, d’où l’on peut gravir le Pizzo Forno avant de descendre au Rifugio Alpe Sponda. Le versant nord reste longtemps enneigé : de bonnes chaussures et des microcrampons sont vivement conseillés.",
                          dati=[("Longueur", "4,5 km"), ("Montée", "+767 m"), ("Temps", "3 h"), ("Difficulté", "T4")],
                          link=[("Via Idra, étape 5", "https://www.viaidra.ch/tappa05"), ("Description de l’itinéraire", CT_DOC + "d-pizzo-forno-2907-m.pdf")]),
                     dict(titolo="Pizzo Campolungo (2714 m)", img=("pizzo-campolungo", "Le Pizzo Campolungo et les arêtes vers le Pizzo Prèvat"),
                          testo="Du sommet, la vue s’ouvre sur les lacs Leìt, Tremorgio et Morghirolo et sur le Pizzo Prèvat, le « Cervin du Tessin ». La montée n’est pas balisée et traverse des prés raides et des éboulis dans la cuvette sous l’Alpe Lei di Cima : pas difficile, mais un bon sens de l’orientation est nécessaire.",
                          dati=[("Longueur", "3 km"), ("Montée", "+690 m"), ("Temps", "2 h 30"), ("Difficulté", "T4")],
                          link=[("Carte en ligne", "https://s.geo.admin.ch/epntrruz341r"), ("Description de l’itinéraire", CT_DOC + "c-pizzo-campolungo-2714-m.pdf")]),
                     dict(titolo="Tour du Campolungo", img=("giro-campolungo", "Un lac de montagne turquoise entre les arêtes du Campolungo"),
                          testo="Une randonnée sauvage, une liaison alternative entre la Capanna Leìt et le Campo Tencia par le versant du Val Maggia. Terrain par endroits accidenté, faible réseau mobile et, en début d’été, de la neige sur les pentes raides à l’ombre.",
                          dati=[("Longueur", "8 km"), ("Montée", "+1268 / −1166 m"), ("Temps", "6 h de cabane à cabane, 7-8 h pour le tour complet"),
                                ("Difficulté", "T4-T5, en partie équipé de cordes"), ("Meilleure période", "De juillet à fin septembre"),
                                ("Équipement", "Bonnes chaussures de montagne, casque et éventuellement un set de via ferrata"),
                                ("Points forts", "Lac Morghirolo, Corte di Zaria, les lacs du Cantùn dal Prèvat, Pizzo del Prèvat")],
                          link=[("Description de l’itinéraire", CT_DOC + "a-giro-del-campolungo.pdf")]),
                 ]),
            dict(file="cresta-dei-corni", titolo="Cresta dei Corni",
                 lead="Ni randonnée ni alpinisme : la traversée aérienne d’arête du Passo Morghirolo au Campo Tencia.",
                 img=("capanna-cresta-dei-corni", "La Capanna Campo Tencia au pied de la Cresta dei Corni"),
                 corpo="""<p>Plus de la randonnée, mais pas tout à fait de l’alpinisme : « scrambling » est le mot qui décrit le mieux la Cresta dei Corni au Campo Tencia. L’itinéraire mène du Passo Morghirolo par le Pizzo Canà, les Tre Corni et le Pizzo Croslina jusqu’au sommet du Campo Tencia : un parcours aérien avec des vues à couper le souffle sur la Léventine et le Val Lavizzara, imaginé et équipé par Franco Demarchi, « Dema », gardien pendant 28 ans.</p>
<p>C’est un itinéraire d’arête haute-alpin et exposé, avec des piliers et des ressauts rocheux jusqu’à 25 m, bien équipé et balisé ; en début d’été, il peut y avoir de la neige. <strong>Il n’y a pas d’échappatoires : une bonne condition physique, l’absence de vertige et une météo stable sont indispensables. Planifiez bien votre temps et gardez une bonne marge.</strong></p>
<h2>Itinéraire</h2>
<p>De la cabane, suivre des traces de sentier jusqu’au col à 2560 m. Depuis la selle, on reste surtout sur le fil, avec une escalade facile, en partie équipée, alternant avec des passages à pied. Du Pizzo Croslina, descendre prudemment jusqu’au col du même nom, d’où, s’il reste de l’énergie, on peut gravir le Pizzo Campo Tencia. Descente par la voie normale en environ 1 h 30.</p>""",
                 dati=[("Longueur", "8 km"), ("Montée", "+1350 / −1190 m"), ("Temps", "8 h de cabane à cabane"),
                       ("Difficulté", "T6, F+ (PD), passages de III"), ("Équipement", "Baudrier, set de via ferrata, casque, éventuellement une corde de 30 m pour assurer")],
                 link=[("Itinéraire en ligne", "https://s.geo.admin.ch/r94n5ne4qz11"), ("Vue d’ensemble de la Cresta dei Corni", CT_DOC + "prospetto-tre-corni.pdf")],
                 foto="cresta-dei-corni"),
            dict(file="tencia-croslina", titolo="Pizzo Campo Tencia et Pizzo Croslina",
                 lead="La plus haute pyramide de roche et de glace du Tessin et le géant qui domine la cabane.",
                 img=("croslina-tencia", "Les sommets du Pizzo Croslina et du Pizzo Campo Tencia sous la neige"),
                 corpo="""<p>Le Pizzo Campo Tencia (3072 m) est une extraordinaire pyramide de roche et de glace avec une vaste vue panoramique. Le Pizzo Croslina (3012 m) se dresse comme un géant au-dessus de la cabane ; vu de l’est, c’est pourtant une élégante pyramide.</p>
<p>Le versant nord de ce tronçon de la crête principale est typique : après la pyramide du Croslina, trois sommets se suivent régulièrement vers le sud-est, séparés par des selles à peine marquées : le Pizzo Campo Tencia (3072 m), le sommet central Tenca (3035 m, sans nom sur la carte nationale) et le Pizzo Penca (3038 m).</p>
<h2>Itinéraire</h2>
<p>De la cabane, se diriger vers le sud en suivant le balisage blanc-bleu-blanc jusqu’à une cascade. À gauche, une large cheminée mène à la vire qui traverse toute la paroi : un sentier bien balisé et exposé monte vers le sud-est jusqu’à une crête facile. En direction du sud-ouest, on atteint la cuvette du Laghetto, au pied des restes du Ghiacciaio Grande di Croslina. Continuer le long de la petite arête entre les deux glaciers du Croslina jusqu’à environ 2800 m, puis vers le sud-ouest, en descendant un peu sur le glacier, jusqu’à la Bocchetta di Croslina (2864 m), toujours en suivant le balisage blanc-bleu-blanc. Par l’arête, on atteint la croix sommitale.</p>
<p>Du sommet, on peut traverser jusqu’à la Capanna Soveltra dans le Val Maggia, en direction du sud-est sur le balisage blanc-bleu-blanc.</p>
<p><strong>Pizzo Croslina :</strong> de la Bocchetta di Croslina, se diriger vers le nord-ouest en suivant les points bleus jusqu’à une vire à droite du couloir d’éboulis bien visible. Montée en partie exposée, avec des passages rocheux de II.</p>
<p>Pour les deux sommets, la descente se fait par l’itinéraire de montée.</p>""",
                 dati=[("Longueur", "3 km"), ("Montée", "+940 m"), ("Temps", "3 h pour le Pizzo Campo Tencia, 4 h avec le Pizzo Croslina"),
                       ("Difficulté", "T4+ Pizzo Campo Tencia, T6 avec le Pizzo Croslina"),
                       ("Points forts", "La cuvette du Laghetto, le Ghiacciaio Grande di Croslina, la croix sommitale du Campo Tencia, les edelweiss du Croslina")],
                 link=[("Description de l’itinéraire", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")],
                 foto="tencia-croslina"),
            dict(file="arrampicata", titolo="Escalade",
                 lead="Des jardins d’escalade à quelques minutes de la cabane, du III au 6b : idéal pour apprendre.",
                 img=("giardino-arrampicata", "Un grimpeur sur une dalle près de la cabane"),
                 corpo=f"""<p>Une zone idéale pour apprendre l’escalade aux enfants et aux débutants : autour de la cabane, plusieurs secteurs ont été équipés, du III jusqu’à quelques longueurs en 6b pour les plus exigeants.</p>
<p>Le secteur Angolo, près du lac, est équipé spécialement pour l’entraînement sur rocher : voies d’une longueur, relais de rappel, rappels en fil d’araignée et une courte voie facile de plusieurs longueurs pour s’exercer. À quelques minutes de la cabane, dans le secteur Cascata, on peut s’exercer aux manœuvres de corde sur des voies faciles et parallèles de plusieurs longueurs, et le bloc Kape offre quelques voies d’une longueur.</p>
<p><a href="https://s.geo.admin.ch/na49wcdjtms7" rel="noopener">Les secteurs sur la carte</a></p>
<p><a class="file-link" href="{CT_DOC}volantino-arrampicata-campo-tencia.pdf">Dépliant des jardins d’escalade</a></p>
<table>
<thead><tr><th>Secteur</th><th>Voies</th><th>Longueur</th><th>Cotation</th><th>Remarques</th></tr></thead>
<tbody>
<tr><td>Cascata</td><td>4</td><td>60 m</td><td>3-4</td><td>plusieurs longueurs, parallèles</td></tr>
<tr><td>Kape</td><td>7</td><td>10 m</td><td>5-6c</td><td>une longueur</td></tr>
<tr><td>Tutto o niente</td><td>10</td><td>20 m</td><td>3-5a</td><td>une longueur</td></tr>
<tr><td>Disperato</td><td>6</td><td>10 m</td><td>4-5a</td><td></td></tr>
<tr><td>Onapart</td><td>3</td><td>30 m</td><td>5a-6b</td><td></td></tr>
<tr><td>Pulce di roccia</td><td>5</td><td>20 m</td><td>3-4</td><td>dalles faciles</td></tr>
<tr><td>Angolo</td><td>8</td><td>20 m</td><td>4-5a</td><td>zone d’entraînement</td></tr>
<tr><td>Piode</td><td>3</td><td>25 m</td><td>4-5a</td><td></td></tr>
<tr><td>Pitela</td><td>6</td><td>10-80 m</td><td>3-5a</td><td></td></tr>
<tr><td>Cresta rossa</td><td></td><td>500 m</td><td>2-4</td><td>voie alpine</td></tr>
<tr><td>Lago</td><td>1</td><td>75 m</td><td>5a</td><td></td></tr>
</tbody>
</table>
<figure><img src="assets/img/capanne/campotencia/settori-arrampicata.webp" alt="Carte des secteurs d’escalade autour de la cabane et du lac Morghirolo" width="1088" height="766" loading="lazy" decoding="async"></figure>""",
                 foto="arrampicata"),
            dict(file="inverno", titolo="En hiver",
                 lead="Des randonnées à skis exigeantes, loin des destinations connues, et des cascades de glace jusqu’à 200 mètres.",
                 img=("scialpinismo", "Des skieurs de randonnée descendant une large pente de neige, à contre-jour"),
                 corpo="""<h2>Ski de randonnée</h2>
<p>En hiver, la région du Campo Tencia reste à l’écart des destinations connues. Le terrain technique et accidenté demande de bonnes conditions de neige et de solides compétences en ski de randonnée et en orientation. Au printemps, on trouve les conditions pour des courses très gratifiantes : Pizzo Campo Tencia, Pizzo Forno et Pizzo Campolungo. La cabane n’est pas gardiennée, mais la réservation est obligatoire ; pour les grands groupes, elle peut être ouverte en accord avec les gardiens.</p>
<h2>Cascades de glace</h2>
<p>Dans la cuvette du Buco di Cumasna, à 2000 mètres, de puissantes cascades de glace jusqu’à 200 mètres de long et de difficulté variable se forment dès le début de l’hiver. À droite se trouve la plus connue, la « Giovannelli », dans le couloir utilisé en hiver pour franchir le ressaut rocheux en montant au sommet du Pizzo Campo Tencia ou en en redescendant.</p>""",
                 foto="inverno"),
        ],
        sostenitori=dict(
            testo="Un grand merci aux partenaires qui soutiennent la cabane.",
            loghi=[("Suisse Tourisme", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/fr-ch/"),
                   ("Ticino Turismo", "sostenitori/ticino-turismo", "https://www.ticino.ch/fr/"),
                   ("Bellinzona e Valli Turismo", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/")]),
        foto=[("La cabane", "capanna"), ("La cuisine", "cucina"), ("Les environs", "dintorni")],
    ),

    "cristallina.html": dict(
        cartella="cristallina",
        capanna="""<p>La première cabane moderne du Club Alpin Suisse se dresse à 2575 m sur le Passo Cristallina, dans une région qui invite à l’exploration en été comme en hiver. En été, c’est une base pour les sommets alentour et pour les traversées vers le Val Maggia, le Val Formazza et la région du Gothard ; en hiver, les environs enneigés offrent de superbes descentes et des combinaisons de sommets.</p>
<p>Elle compte 100 places en couchettes avec duvets, dans 6 chambres de 4, 9 de 8 et 2 dortoirs de 12, une salle à manger panoramique avec terrasse, des toilettes intérieures avec eau chaude, une douche, un séchoir et un local à chaussures avec pantoufles de cabane. Le sac à viande est obligatoire. Bonne réception Swisscom à la cabane.</p>""",
        cucina="""<p>Pendant la journée, des plats simples pour tous : gnocchis, raviolis, tartes salées, charcuterie, desserts et bien plus, le tout préparé à la cabane avec des produits locaux suisses. Pour la demi-pension, les menus changent selon le jour de la semaine, en pensant aussi aux végétariens. Avec un bon choix de vins et d’eaux-de-vie.</p>
<p><strong>Important :</strong> prévenez-nous à temps si vous êtes végétarien ou végan ou si vous avez des allergies ou des intolérances : nous préparerons volontiers un menu adapté.</p>
<p>Les chambres sont attribuées selon l’ordre d’arrivée des réservations et la taille du groupe ; elles ne peuvent pas être réservées en exclusivité. Quand la cabane est gardiennée, la demi-pension est obligatoire.</p>
<p>Les chiens sont les bienvenus, mais pas dans les chambres ni dans les salles communes : merci de nous prévenir avant votre arrivée.</p>""",
        team=dict(titolo="Le gardien", img=("guardiano", "Emanuele Vellati, gardien de la Capanna Cristallina, dans la neige avec le Basodino derrière")),
        accessi="""<p>En été, la cabane est à quelques heures de marche, surtout par des sentiers adaptés aux familles ; en hiver à skis depuis le Val Bedretto, Robiei ou le Val Formazza.</p>
<ul>
<li>D’Ossasco : 3 h 30.</li>
<li>Du Passo San Giacomo : 4 h.</li>
<li>De Robiei : 3 h.</li>
<li>Du lac du Narèt : 2 h 30.</li>
<li>D’Airolo Pesciüm : 5 h.</li>
<li>De la Capanna Poncione di Braga : 4 h.</li>
<li>En hiver : d’Ossasco 3 h, d’All’Acqua 4 h.</li>
</ul>
<p><strong>En voiture depuis le nord :</strong> A2 jusqu’à Airolo, puis direction col du Nufenen et Val Bedretto. <strong>Depuis le sud :</strong> A2 jusqu’à Bellinzona, puis Locarno et le Val Maggia : Val Bavona pour Robiei, avec le <a href="https://www.robiei.ch/" rel="noopener">téléphérique San Carlo-Robiei</a> (en été), ou Val Lavizzara pour le Narèt.</p>
<p><strong>En transports publics :</strong> train S10 jusqu’à Airolo, puis bus dans le Val Bedretto. Taxi depuis Airolo : Marchetti Taxi <a class="num" href="tel:+41918733035">+41 91 873 30 35</a>, Gotthard Taxi <a class="num" href="tel:+41787901055">+41 78 790 10 55</a>.</p>
<p><strong>Traversées vers d’autres cabanes :</strong> <a href="https://www.corno-gries.ch/" rel="noopener">Corno Gries</a> (2338 m) 5 h ; <a href="https://www.capanna-basodino.ch/" rel="noopener">Basodino</a> (2200 m) 2 h ; <a href="https://www.utoelocarno.ch/" rel="noopener">Poncione di Braga</a> (1870 m) 4 h ; <a href="https://www.satritom.ch/garzonera/" rel="noopener">Garzonera</a> (2000 m) 5 h, T5 ; <a href="https://www.rifugiomarialuisa.it/" rel="noopener">Rifugio Maria Luisa</a> (Italie, 2393 m) 5 h.</p>
<p>Cartes : carte nationale 1:25 000 feuille 1251 Val Bedretto ; carte de ski de randonnée 265 S Nufenenpass.</p>""",
        attivita="""<p>Le Passo Cristallina est un lien naturel entre le massif du Gothard et le Val Maggia, au milieu d’un réseau d’itinéraires et de cabanes : la <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, la Via Cristallina et la Via Alta della Vallemaggia passent toutes par ici. En hiver, c’est un paradis du ski de randonnée, avec un enneigement sûr même les années pauvres en neige.</p>
<p>La géologie raconte la formation des Alpes : du marbre issu de sédiments marins à côté de roches magmatiques, des plis incroyables. La faune est riche : la colonie de bouquetins vers la Cima di Lago, des chamois, des aigles, des faucons crécerelles. Et partout des traces du travail humain : alpages, installations militaires et grandes centrales hydroélectriques.</p>""",
        pagine=[
            dict(file="proposte-gite", titolo="Propositions de courses", foto="proposte-gite",
                 lead="Cinq itinéraires de difficulté moyenne, de la Cima di Lago à la Via Idra, avec la cabane comme base ou comme étape.",
                 img=("pizzo-cristallina", "Vue du sommet du Pizzo Cristallina sur des lacs de montagne et des sommets"),
                 corpo="""<p>Si vous voulez découvrir la merveilleuse région du Cristallina, avec ses lacs de montagne et sa faune de haute montagne, voici des itinéraires de difficulté moyenne, pas trop longs, qui partent de la cabane ou l’utilisent comme étape.</p>""",
                 itinerari=[
                     dict(titolo="Cima di Lago (2832 m)", img=("cima-di-lago", "Un bouquetin sur la pente de la Cima di Lago, avec l’itinéraire en rouge"),
                          testo="Un sommet à la vue superbe, idéal aussi pour des enfants au pied sûr : vous rencontrerez probablement des bouquetins.",
                          dati=[("Longueur", "4 km"), ("Montée", "+300 m"), ("Temps", "1 h"), ("Difficulté", "T4")],
                          link=[("Description de l’itinéraire", "docs/capanne/cristallina/a-cima-di-lago-2832-msm.pdf")]),
                     dict(titolo="Pizzo Cristallina (2912 m)", img=("pizzo-cristallina", "Vue du sommet du Pizzo Cristallina sur des lacs de montagne et des sommets"),
                          testo="Le sommet principal, entouré d’un chapelet de lacs de montagne ; au sommet se dresse encore le Rifugio Camosci, dernier témoin des temps de guerre dans la région. Sur la dernière pente, attention aux chutes de pierres s’il y a d’autres personnes ; n’entrer dans le bivouac qu’avec beaucoup de prudence, il y a un risque de chute.",
                          dati=[("Longueur", "11 km depuis Ossasco"), ("Montée", "+1100 m depuis Ossasco"), ("Temps", "2 h depuis la cabane, 6 h depuis Ossasco"), ("Difficulté", "T4")],
                          link=[("Description de l’itinéraire", "docs/capanne/cristallina/b-cristallina-2912.pdf")]),
                     dict(titolo="Tour du Cristallina", img=("giro-cristallina", "Le lac de retenue de Robiei et son barrage, au pied des montagnes"),
                          testo="Un tour classique et facile, sur un sentier blanc-rouge-blanc, autour du sommet du Cristallina. Possible aussi en excursion d’un jour depuis Robiei ou depuis le col du Narèt, avec repas à la cabane.",
                          dati=[("Longueur", "14 km"), ("Montée", "+980 m"), ("Temps", "5 h 30"), ("Difficulté", "T3")],
                          link=[("Description de l’itinéraire", "docs/capanne/cristallina/c-giro-del-cristallina.pdf")]),
                     dict(titolo="Sentiero Cristallina 59, vers Robiei", img=("percorso-59", "Des lacs de montagne dans un cirque rocheux sur le Sentiero Cristallina"),
                          testo="Le Sentiero Cristallina numéro 59 est une traversée classique de trois jours de Bignasco, dans le Val Maggia, à Airolo.",
                          dati=[("Longueur", "42 km, en trois étapes"), ("Montée", "+2800 / −2100 m"), ("Temps", "3 jours"), ("Difficulté", "T3")],
                          link=[("Description de l’itinéraire", "docs/capanne/cristallina/d-percorso-59-cristallina.pdf")]),
                     dict(titolo="Col du Nufenen-Cristallina-Airolo", img=("nufenen-airolo", "Des randonneurs sur une arête herbeuse et rocheuse"),
                          testo="La première étape de la Via Idra, du col du Nufenen à Airolo avec une nuit à la cabane. Le point fort est la montée par le Canale del Becco, équipé de cordes et de marches : mieux vaut le faire à la montée ; attention aux chutes de pierres et à la neige en début de saison.",
                          dati=[("Longueur", "27 km"), ("Montée", "+1600 / −2450 m"), ("Temps", "10 h, sur deux jours (5 + 5)"),
                                ("Difficulté", "T4 le premier jour (T6 dans le Canale del Becco), T3 le second")],
                          link=[("Description de l’itinéraire", "docs/capanne/cristallina/e-passo-nufenen-airolo.pdf")]),
                 ]),
            dict(file="inverno", titolo="En hiver", foto="inverno",
                 lead="Sommets et descentes en poudreuse : plusieurs descentes dans la journée autour de la cabane.",
                 img=("discesa-polvere", "Des skieurs de randonnée montant une large pente de neige à l’ombre"),
                 corpo="""<p>La région du Cristallina est excellente pour les descentes en poudreuse. De nombreux itinéraires autour de la cabane peuvent se combiner, avec deux descentes ou plus dans la journée, qui se termine souvent sur les pentes à l’ombre du versant droit du Val Bedretto.</p>
<ul>
<li>Montée par le Val Torta et descente par le <strong>Val Cassinello</strong> depuis la Bassa di Folcra ou depuis le <strong>Passo Gararesch</strong>, une variante (itinéraires 521 h et 521 i).</li>
<li>Montée par le Val Torta pour le classique <strong>tour du Cristallina</strong>, avec repas à la cabane et descente par le Val Piana ou le Val Cavagnolo.</li>
<li>Le sommet du <strong>Cristallina</strong> et une descente par la « Diavolezzina », en remontant éventuellement à la Bassa di Folcra (521 h) ou au Passo Gararesch (521 i).</li>
<li>La <strong>Cima di Lago</strong> comme course de l’après-midi, depuis le Val Torta ou le Val Cavagnoli.</li>
<li>Le <strong>tour des cols</strong>, sauvage et varié : le premier jour All’Acqua, San Giacomo, Passo Grandinagia, Bocchetta di Valleggia, Passo di Cima di Lago et la cabane (<a href="https://s.geo.admin.ch/7e3436c217" rel="noopener">carte</a>) ; le second Cima di Lago, Sfunadau, Cristallina et Passo Gararesch.</li>
<li><strong>Poncione di Braga, Basodino, Marchhorn :</strong> des sommets sur de longues traversées.</li>
</ul>"""),
            dict(file="curiosita", titolo="Le saviez-vous ?",
                 lead="Occupation militaire, naissance des Alpes et grandes centrales hydroélectriques : quelques clés sur la région du Cristallina.",
                 img=("rocce-piegate", "Des roches plissées par la formation des Alpes dans une cuvette verte"),
                 corpo="""<p>Les traces de la formation des Alpes sautent aux yeux : les forces qui ont plissé la chaîne ont fait remonter des sédiments marins, et en quelques mètres on trouve des roches de composition et d’origine très différentes. Cela façonne aussi la flore, qui dépend du sol. La faune est typiquement alpine : on rencontre facilement les bouquetins de la colonie, plus d’une centaine d’animaux qui ne craignent pas l’homme. L’homme a lui aussi transformé la région, avec la garde de la frontière en temps de guerre et les grandes installations hydroélectriques.</p>
<p>Les textes complets ne sont disponibles qu’en italien.</p>""",
                 itinerari=[
                     dict(titolo="L’histoire de l’occupation militaire", img=("rifugio-camosci", "L’ancien refuge militaire en pierre au sommet, dans la neige"),
                          testo="La construction de la route du Val Formazza au Passo San Giacomo entre 1926 et 1929 inquiéta la Suisse et conduisit à la fortification de la région.",
                          link=[("Texte complet", "docs/capanne/cristallina/a-la-storia-delloccupazione-militare-1.pdf")]),
                     dict(titolo="Les traces de la formation des montagnes", img=("rocce-piegate", "Des roches plissées par la formation des Alpes dans une cuvette verte"),
                          testo="Le paysage du Cristallina a été façonné par l’orogenèse alpine, un processus qui a duré environ 25 millions d’années.",
                          link=[("Texte complet", "docs/capanne/cristallina/b-le-tracce-dellorogenesi-1.pdf")]),
                     dict(titolo="L’hydroélectricité Naret-Robiei", img=("schema-idroelettrico", "Schéma des lacs de retenue reliés entre Gries, Robiei et le lac Majeur"),
                          testo="La région Robiei-Narèt est riche en lacs de retenue reliés entre eux, qui exploitent au mieux l’eau pour produire une électricité propre.",
                          link=[("Texte complet", "docs/capanne/cristallina/c-ldroelettrico-naret-robiei-1.pdf")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Un grand merci aux partenaires qui soutiennent la cabane.",
            loghi=[("Suisse Tourisme", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/fr-ch/"),
                   ("Ticino Turismo", "sostenitori/ticino-turismo", "https://www.ticino.ch/fr/"),
                   ("Bellinzona e Valli Turismo", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/")]),
        foto=[("La cabane", "capanna"), ("La cuisine", "cucina"), ("Les environs", "dintorni")],
    ),

    "adula.html": dict(
        cartella="adula",
        capanna="""<p>La « Bassa », comme on l’a toujours appelée, a été inaugurée en 1924 et a gardé tous les traits du bâtiment d’origine en pierre et en bois : une salle commune chargée d’histoire, des dortoirs où ont dormi des milliers d’alpinistes, un accueil chaleureux et une cuisine du terroir qui nourrit le corps et l’âme.</p>
<p>Elle compte 24 places dans quatre petits dortoirs de 4, 5 et 7 places, adaptés aussi aux familles, et deux chambres doubles avec supplément ; deux salles à manger chaleureuses de 20 places, des toilettes intérieures, une douche, l’énergie solaire pour l’éclairage et une cuisine au bois et au gaz. Les lits ont des duvets ; le sac à viande est obligatoire. Réception mobile moyenne à la cabane.</p>
<p>Le local d’hiver est toujours ouvert, avec boissons et bois.</p>""",
        cucina="""<p>La terrasse panoramique invite à manger dehors. Chaque jour, nous cuisinons des produits de la région : plats tessinois, fromages et formaggini, pâtes en sauce, soupe, minestrone et notre rösti en plusieurs versions, et toujours plusieurs gâteaux.</p>
<p>Pour les hôtes qui passent la nuit, il y a le soir des plats et des spécialités avec des produits de saison, et un petit-déjeuner copieux donne des forces pour de nouvelles aventures.</p>
<p><strong>Important :</strong> prévenez-nous à temps si vous êtes végétarien ou végan ou si vous avez des allergies ou des intolérances.</p>
<p>Les chiens sont les bienvenus, mais pas dans les chambres : une place les attend dehors. Merci de nous signaler votre chien à l’avance.</p>""",
        team=dict(img=("guardiani", "Le gardien et deux aides devant l’entrée de la cabane en pierre")),
        accessi="""<p><strong>En été</strong>, la cabane s’atteint facilement par le chemin muletier plat du Val Carassino depuis Compietto. La vallée fait environ 6 km et passe par deux alpages, l’Alpe Bolla et l’Alpe Bresciana, où l’on fabrique un excellent fromage, que l’on peut aussi déguster à la cabane. Le torrent tout proche rend le sentier idéal pour les familles par les jours chauds ; à VTT, environ une heure suffit.</p>
<p><strong>En hiver</strong>, on monte à skis depuis Dangio par le Val Soi, ou depuis Ghirone par le Luzzone et le Val Carassino, avec une neige sûre et de préférence au printemps.</p>
<ul>
<li>De Compietto (parking) par le Val Carassino : 2 h 40, à VTT environ 1 h.</li>
<li>De Dangio (arrêt de bus) par le Val Soi : 3 h.</li>
<li>De Cusiè dans le Val Malvaglia (parking) par le Passo del Laghetto : 5 h.</li>
<li>De la Läntahütte par la Bocchetta di Fornee.</li>
<li>En hiver : de Ghirone 5 h, de Dangio 3 h 30.</li>
</ul>
<p><strong>En voiture :</strong> A2 jusqu’à Biasca, puis direction col du Lukmanier jusqu’à Campo Blenio et Ghirone ; monter au barrage du Luzzone, le traverser et continuer jusqu’à l’Alpe di Compietto. Ou laisser la voiture à Ghirone et prendre le <a href="https://www.autolinee.ch/greina" rel="noopener">bus alpin</a>.</p>
<p><strong>En transports publics :</strong> train S10 jusqu’à Biasca, bus 131 jusqu’à Ghirone, puis le bus alpin jusqu’au barrage du Luzzone. Taxi Riviera (Biasca) : <a class="num" href="tel:+41918624848">+41 91 862 48 48</a>.</p>
<p><strong>Traversées vers d’autres cabanes :</strong> <a href="fr/motterascio.html">Motterascio</a> 5 h ; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 3 h 30 ; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 1 h ; <a href="https://quarnei.ch/" rel="noopener">Quarnei</a> 3 h.</p>
<p>Cartes : carte nationale 1:25 000 feuille 1253 Olivone ; carte de ski de randonnée 256 S.</p>""",
        attivita="""<p>À l’Adula flotte un air d’autrefois : l’hospitalité et la bonne cuisine, avec un verre de vin, invitent à s’allonger dans l’herbe face à un décor extraordinaire. D’ici partent des itinéraires passionnants, d’anciens passages et des arêtes aériennes.</p>
<p>Un endroit idéal pour les enfants : de splendides fleurs au début de l’été, chamois et bouquetins, marmottes, vaches à caresser et un torrent pour se baigner. On dort dans une cabane historique au charme d’antan et on gravit l’Adula (Rheinwaldhorn), but de nombreux Tessinois, avec son glacier qui, hélas, ne sera bientôt plus qu’un souvenir.</p>""",
        pagine=[
            dict(file="cima-adula", titolo="Le sommet de l’Adula", foto="cima-adula",
                 lead="Sur le toit du Tessin : l’ascension de l’Adula (Rheinwaldhorn, 3402 m) par la Via Malvaglia, avec descente par le glacier de la Bresciana.",
                 img=("cordata-vetta", "Une cordée sur le sommet enneigé"),
                 corpo="""<p>L’ascension de l’Adula est le but de nombreux randonneurs et alpinistes tessinois. Le sommet est assez facile à atteindre en hiver comme en été ; en raison du recul du glacier et des étés chauds, mieux vaut y aller avant que la neige n’ait complètement fondu et découvert le glacier.</p>
<p>Pour ceux qui ont une expérience alpine de base, nous conseillons le tour par le lac de Cadabi, en montant par l’arête de la Via Malvaglia. Près du sommet, la roche laissée par le glacier est instable : prudence. À la descente, on peut passer par le glacier de la Bresciana, en faisant attention aux crevasses, jusqu’au sentier qui ramène à la Capanna UTOE.</p>""",
                 dati=[("Longueur", "8 km"), ("Montée", "+1400 m"), ("Temps", "4-5 h à la montée, 2-3 h à la descente"),
                       ("Difficulté", "F+ (PD), passages équipés sur l’arête de la Via Malvaglia"), ("Points forts", "Le lac de Cadabi, le glacier de la Bresciana, la vue depuis le sommet")],
                 link=[("Carte en ligne de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721078&amp;N=1150644&amp;trackId=5023916")]),
            dict(file="proposte-gite", titolo="Propositions de courses",
                 lead="Cinq traversées vers d’autres cabanes, de la haute route du Val Carassino à la Via Crio.",
                 img=("via-alta-carassino", "Un randonneur sur une arête rocheuse au-dessus du Val Carassino"),
                 corpo="""<p>Si vous avez plusieurs jours, ces itinéraires de randonnée et de montagne font découvrir des coins peu connus du Val Carassino. Ce ne sont pas des boucles : ils relient la cabane à d’autres cabanes. La haute route du Val Carassino se parcourt dans les deux sens et évite de parcourir deux fois le fond de la vallée si l’on part du Luzzone ou si l’on y arrive ; la traversée Cassimoi-Cassinello est une superbe course d’arête ; la Bocchetta di Fornee ouvre la voie vers Vals ; le passage vers Quarnei est un classique apprécié, aussi pour les familles avec enfants.</p>""",
                 itinerari=[
                     dict(titolo="Haute route du Val Carassino", img=("via-alta-carassino", "Un randonneur sur une arête rocheuse au-dessus du Val Carassino"),
                          testo="De Compietto à la cabane, par les hauteurs, via Sgiu, La Colma, Pinadee et Bresciana.",
                          dati=[("Longueur", "7,5 km"), ("Montée", "+1050 m"), ("Temps", "5 h"), ("Difficulté", "T5")],
                          link=[("Description de l’itinéraire", "docs/capanne/adula/a-via-alta-della-val-carassino.pdf")]),
                     dict(titolo="Vires et sommets du Val Carassino", img=("cengie-carassino", "Pentes herbeuses et vires sous des sommets enneigés"),
                          testo="Le Pizzo Amianto et son ancien éboulement, les vires des moutons, les chamois, les bouquetins et l’aigle.",
                          dati=[("Longueur", "11,5 km"), ("Montée", "+1000 m"), ("Temps", "5 h"), ("Difficulté", "T5")],
                          link=[("Description de l’itinéraire", "docs/capanne/adula/b-cengie-e-vette-della-val-carassino.pdf")]),
                     dict(titolo="Vers la Läntahütte par la Bocchetta di Fornee", img=("lago-fornee", "Un lac de montagne parmi des roches polies par le glacier"),
                          testo="Les traces du glacier en recul, rochers et bouquetins, en direction de Vals.",
                          dati=[("Longueur", "8,7 km"), ("Montée", "+1000 m"), ("Temps", "5 h 30"), ("Difficulté", "T5")],
                          link=[("Description de l’itinéraire", "docs/capanne/adula/c-alla-capanna-lanta-dalla-btta-di-fornee.pdf")]),
                     dict(titolo="Passage facile vers Quarnei", img=("laghetto-cadabi", "Le lac de Cadabi dans un cirque rocheux"),
                          testo="Le glacier de la Bresciana et son recul, les moraines latérales, les roches moutonnées, le lac de Cadabi et la plaine de Quarnei.",
                          dati=[("Longueur", "4 km"), ("Montée", "+700 m"), ("Temps", "3 h 30"), ("Difficulté", "T3")],
                          link=[("Description de l’itinéraire", "docs/capanne/adula/d-facile-traversata-a-quarnei.pdf")]),
                     dict(titolo="Via Crio, étape 6 : du Pizzo Cassimoi au Luzzone", img=("via-crio", "Un randonneur sur un passage équipé parmi des roches rougeâtres"),
                          testo="Trois trois-mille sur l’une des étapes les plus exigeantes de la <a href=\"https://www.viacrio.ch/\" rel=\"noopener\">Via Crio</a>.",
                          dati=[("Longueur", "15,9 km"), ("Montée", "+1540 / −1950 m"), ("Temps", "8 h"), ("Difficulté", "T6, traversée exigeante")],
                          link=[("Description de l’itinéraire", "docs/capanne/adula/e-scaradra-luzzone-passando-dalla-bocchetta-di-fornee.pdf"),
                                ("Vue d’ensemble de la Via Crio", "docs/capanne/adula/via-alta-crio-prospetto-2024.pdf"),
                                ("Trace GPX", "https://www.viacrio.ch/s/006-CRIO-GPX-Adla-UTOE-Scaradra-MV.gpx")]),
                 ]),
            dict(file="inverno", titolo="Hiver et printemps", foto="inverno",
                 lead="Des sommets solitaires pour les skieurs de randonnée expérimentés et des couloirs de neige pour l’alpinisme de début de saison.",
                 img=("pendio-innevato", "Des traces de ski sur une large pente enneigée"),
                 corpo="""<h2>L’Adula en hiver</h2>
<p>En hiver, le versant tessinois de l’Adula reste isolé : des avalanches descendent des pentes de la Carassina, et la montée depuis le Val Soi demande une neige stable dans sa dernière partie. Quand le printemps arrive dans la vallée, le massif offre de belles traversées techniques de cabane en cabane entre la <strong>Läntahütte</strong>, la <strong>Zapporthütte</strong>, l’<strong>Adula</strong> et <strong>Quarnei</strong> : sur le tour de l’Adula et ses variantes, on gravit chaque jour au moins un sommet de plus de 3000 m.</p>
<ul>
<li><strong>Adula (Rheinwaldhorn, 3402 m) par le Vadrecc di Bresciana :</strong> montée par l’itinéraire d’été (324 a) ; dans de bonnes conditions, on descend à skis directement par le glacier jusqu’à environ 2500 m et, avec une courte remontée sur la moraine, on rejoint la pente au-dessus de la Capanna UTOE (324 c). F+ (PD).</li>
<li><strong>Grauhorn (3258 m) :</strong> trop instable en été, accessible au printemps par l’itinéraire 323, à pied sur la pente jusqu’à l’arête à 3100 m. AD.</li>
<li><strong>Piz Jut (3128 m) :</strong> par la Bocchetta di Fornee (2885 m, itinéraire 320), puis côté grison jusqu’au sommet ; descente vers la Läntahütte par le Forneitobel (309). AD.</li>
<li><strong>Cima di Pinadee (2486 m) :</strong> au-dessus du Val Carassina, sans grande difficulté en une bonne heure depuis l’Alpe di Bresciana. F+ (PD).</li>
</ul>
<h2>Alpinisme au printemps</h2>
<p>Les sommets du Torrone di Nav au Passo Cadabi souffrent de la fonte des glaciers : des ascensions autrefois sûres même en été sont aujourd’hui des pentes d’éboulis instables, exposées aux chutes de pierres. Mieux vaut les aborder tant qu’il reste assez de neige au-dessus de 2500 m, en évaluant soigneusement le regel nocturne.</p>
<p>Dans ces conditions, les couloirs de neige jusqu’à 50°, avec crampons et piolet, valent vraiment la peine :</p>
<ul>
<li>le couloir ouest de la <strong>Cima dal Laghetto</strong> depuis le Val Soi jusqu’au point 2582 m, F ;</li>
<li>l’Adula par le couloir <strong>Damstädten</strong> (à gauche), face sud-ouest jusqu’au point 3205 m, F+ (PD) ;</li>
<li>l’Adula par le couloir <strong>Ezio e Maria</strong> (à droite), face sud-ouest jusqu’au point 3205 m, PD+.</li>
</ul>
<p>Pour le <strong>Grauhorn</strong> (pente d’éboulis jusqu’à environ 3180 m), comme pour la <strong>Cima di Fornee</strong>, le <strong>Piz Jut</strong> et la <strong>Punta dello Stambecco</strong> depuis Fornee, partir tôt dans la saison est aussi plus sûr et plus facile.</p>""",
                 link=[("Itinéraires de ski de randonnée sur la carte", "https://map.geo.admin.ch/?lang=fr&amp;topic=wildruhezonen&amp;bgLayer=ch.swisstopo.pixelkarte-farbe&amp;layers=ch.bafu.wrz-jagdbanngebiete_select,ch.bafu.wrz-wildruhezonen_portal,ch.swisstopo-karto.skitouren&amp;layers_visibility=true,false,true&amp;catalogNodes=1308&amp;E=2721748.94&amp;N=1152606.59&amp;zoom=6&amp;layers_opacity=1,1,0.8")]),
            dict(file="curiosita", titolo="Le saviez-vous ?",
                 lead="Deux cabanes et les luttes politiques d’il y a cent ans, d’anciennes transhumances et les richesses du Val Carassino.",
                 img=("vetta-tramonto", "Un sommet dans la lumière du soir au-dessus de vallées dans l’ombre"),
                 corpo="""<p>Au premier regard, le Val Carassino semble long et monotone, mais aux chalets la vue s’ouvre sur l’Adula, le Val Soi et le Val Blenio. En regardant de près, on découvre les richesses botaniques de la vallée et la faune de ses versants.</p>
<p>Les habitants de la vallée exploitent la région depuis le haut Moyen Âge : l’économie alpestre perdure aujourd’hui, et ses produits sont très appréciés. Le sommet et les deux cabanes rappellent aussi les luttes politiques d’il y a plus de cent ans, quand des groupes d’alpinisme « prolétaires » et l’UTOE naquirent de mouvements civiques et ouvriers, une particularité tessinoise dans l’histoire de l’alpinisme suisse.</p>
<p>Les textes complets ne sont disponibles qu’en italien.</p>""",
                 itinerari=[
                     dict(titolo="Pourquoi deux cabanes ? Un peu d’histoire", img=("vetta-tramonto", "Un sommet dans la lumière du soir au-dessus de vallées dans l’ombre"),
                          testo="Le plus grand rêve que le fougueux président Remo Patocchi voulait réaliser…",
                          link=[("Texte complet", "docs/capanne/adula/a-perche-due-capanne-cenni-di-storia.pdf")]),
                     dict(titolo="Histoires d’anciennes transhumances", img=("dipinto-alpe", "Peinture d’un alpage avec un chalet en pierre sous les sommets"),
                          testo="Il y a mille ans, une période très chaude a eu une grande influence sur l’ensemble des Alpes…",
                          link=[("Texte complet", "docs/capanne/adula/c-storie-di-antiche-transumanze.pdf")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Un grand merci aux partenaires qui soutiennent la cabane.",
            loghi=[("Suisse Tourisme", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/fr-ch/"),
                   ("Ticino Turismo", "sostenitori/ticino-turismo", "https://www.ticino.ch/fr/"),
                   ("Bellinzona e Valli Turismo", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/")]),
        foto=[("La cabane", "capanna"), ("Les environs", "dintorni")],
        foto_lead="La cabane et les environs",
    ),

    "motterascio.html": dict(
        cartella="motterascio",
        capanna="""<p>Au milieu d’un réseau de sentiers entre quelques-uns des plus beaux endroits du sud de la Suisse, la Capanna Michela Motterascio se dresse à 2172 m sur l’Alpe Motterascio, en bordure sud du plateau de la Greina, en harmonie avec le bois, le cuivre et la pierre. Au pied du Piz Terri, du Pizzo Coroi, du Piz Vial, de la Gaglianera et du Piz Valdraus, on passe des journées pleines de promenades, de silence et de repos. Pas besoin d’être un alpiniste expérimenté : un peu de curiosité, d’enthousiasme et d’énergie suffisent.</p>
<p>La cabane est spacieuse : 70 places avec duvets, une salle à manger panoramique de 55 places avec une paroi vitrée sur les Alpes, une salle commune « romantique » de 20 places, des toilettes intérieures séparées pour femmes et hommes, une douche quand l’eau de source suffit, un séchoir et des pantoufles de cabane à l’entrée, aussi pour les petits. L’eau est une eau de source potable ; l’électricité vient du photovoltaïque, avec un générateur de secours. Le sac à viande est obligatoire et peut aussi être loué. Pas de réseau mobile.</p>
<p><strong>Local d’hiver :</strong> 10 places avec duvets, boissons, bois et l’essentiel (sel, sucre, café soluble). Apportez votre nourriture ; l’eau n’est pas garantie (fontaine sur la terrasse, si elle n’est pas gelée), et il n’y a pas de toilettes d’hiver. Réservation obligatoire, en ligne ; la confirmation contient toutes les informations.</p>""",
        cucina="""<p>À midi, la terrasse ensoleillée et la belle salle commune invitent à des plats régionaux simples, chauds et froids, avec une vue à couper le souffle, plus le buffet de gâteaux maison. Le souper est à 19 h, selon les disponibilités et l’inspiration du cuisinier ; puis un petit-déjeuner copieux pour le lendemain. On cuisine surtout au fourneau à bois et au gaz.</p>
<p><strong>Important :</strong> prévenez-nous à temps si vous êtes végétarien ou végan ou si vous avez des allergies ou des intolérances.</p>
<p>Pour les enfants, il y a des jeux, des livres, du papier et des crayons de couleur ; le long du sentier, avec un peu de chance, on voit des marmottes. Les chiens sont les bienvenus mais ne peuvent pas entrer dans la cabane : pour la nuit, le bûcher abrité et sec est prêt avec une couverture et des gamelles. Merci de nous prévenir à l’avance.</p>
<p>En été, le téléphérique de service aide pour le ravitaillement, mais l’hélicoptère reste indispensable : merci de redescendre vos déchets dans la vallée.</p>""",
        team=dict(titolo="Le gardien", img=("fabio", "Fabio Merzaghi dans la cuisine avec des gâteaux tout juste sortis du four")),
        accessi="""<p>En été, la cabane s’atteint facilement à pied, surtout par des sentiers adaptés aux familles. En hiver, on monte à skis par le Val Camadra et le col de la Greina (5-6 h), seulement avec une neige stable et quand les pentes latérales se sont déchargées.</p>
<ul>
<li>Du lac de Luzzone, Alpe Garzott : 2 h.</li>
<li>Du lac de Luzzone, barrage : 3 h 30.</li>
<li>De Ghirone par le lac de Luzzone : 4 h 30 ; par le Val Camadra : 6 h.</li>
<li>De Pian Geirètt : 3 h 30.</li>
<li>De Vrin : 5 h ; de Vals : 7-8 h.</li>
</ul>
<p><strong>En transports publics :</strong> train et bus jusqu’à Ghirone, Aquilesco ; puis le <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a> des Autolinee Bleniesi jusqu’au lac de Luzzone ou à Pian Geirètt, tous les jours en juillet et août, seulement le week-end en septembre.</p>
<p><strong>En voiture :</strong> A2 jusqu’à Biasca, puis direction col du Lukmanier jusqu’à Campo Blenio et Ghirone ; monter au barrage du Luzzone et longer le lac jusqu’à l’Alpe Garzott. Parking gratuit à Ghirone-Aquilesco et au barrage (avec toilettes ; Ristorante Luzzone d’avril à octobre) ; à l’Alpe Garzott, où l’on peut acheter un excellent fromage, il n’y a que quelques places : arrivez tôt ou partagez les voitures.</p>
<p><strong>Taxi :</strong> Poglia Mirko (Olivone) <a class="num" href="tel:+41794440712">+41 79 444 07 12</a> ; <a href="https://www.taxiriviera.ch/" rel="noopener">Taxi Riviera</a> (Biasca) <a class="num" href="tel:+41794136868">+41 79 413 68 68</a>.</p>
<p><strong>Traversées vers d’autres cabanes :</strong> <a href="https://www.terrihuette.ch/" rel="noopener">Terri</a> 2 h 30 ; <a href="https://www.satlucomagno.ch/wordpress/capanna-scaletta/" rel="noopener">Scaletta</a> 2 h ; <a href="https://www.capannabovarina.ch/" rel="noopener">Bovarina</a> 5 h ; <a href="fr/adula.html">Adula CAS</a> 5 h ; <a href="https://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 6 h ; <a href="https://www.medelserhuette.ch/" rel="noopener">Medelser Hütte</a> 6 h ; <a href="https://laentahuette.ch/" rel="noopener">Läntahütte</a> 7 h ; <a href="https://www.rifugioscaradra.ch/" rel="noopener">Rifugio Scaradra</a> 3 h. Itinéraires sur <a href="https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=10&amp;E=2720474&amp;N=1161992&amp;layers=Wanderland%2CStation%2CAccomodation" rel="noopener">SuisseMobile</a>.</p>
<p>Cartes : carte nationale 1:25 000 feuille 1233 Greina ; carte de ski de randonnée 256 S.</p>""",
        attivita="""<p>La Greina est un haut plateau unique entre le Tessin et les Grisons, long de près de 6 km et à plus de 2200 m d’altitude : une toundra alpine protégée, inscrite à l’Inventaire fédéral des paysages d’importance nationale. Elle est intacte : les seuls signes de l’homme sont le Crap la Crusch et le col du Crap, où une croix de fer rappelle que la Greina était déjà un passage et un pâturage à l’époque romaine et au Moyen Âge.</p>
<p>D’innombrables sources y jaillissent, formant méandres, bras morts et marais sur la ligne de partage des eaux : le Brenno della Greina coule vers la Méditerranée, le Rein da Sumvitg vers la mer du Nord. C’est la reine des contrastes, entre le blanc des glaciers, le noir des schistes et le vert de la toundra, avec l’arche rocheuse d’une quarantaine de mètres, les tourbières, les petites tours rocheuses et les dolines. <strong>Pour vraiment sentir sa magie, restez deux jours ou plus.</strong></p>""",
        pagine=[
            dict(file="giro-greina", titolo="Tour de la Greina", foto="giro-greina",
                 lead="La Greina en un jour : du Luzzone à la cabane, par le col de la Greina et en descendant vers la Scaletta, avec le Bus alpin.",
                 img=("piano-greina", "La plaine de la Greina avec le torrent entre prés et montagnes"),
                 corpo="""<p>Ghirone, lac de Luzzone, Capanna Michela Motterascio, Crap la Crusch, col de la Greina, Capanna Scaletta, Pian Geirètt, Ghirone : pour qui n’a qu’un jour, le tour peut se faire en été en 6-7 heures de marche, grâce au <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">Bus alpin</a>.</p>
<p>De l’arrêt, suivre la route non goudronnée le long du <strong>lac de Luzzone</strong>. À l’Alpe Garzott, un sentier bien balisé entre dans le « fjord », une gorge étroite ; le sentier a été amélioré en 2017 avec le soutien du Patriziato di Aquila. Après un pont moderne, on monte parmi des mélèzes clairsemés jusqu’aux Monti di Rafüsc (1691 m) et, par des pentes herbeuses raides, jusqu’à la plaine de Trachee (1947 m). Par une ancienne passerelle en bois sur le Ri di Motterascio et une dernière montée en lacets, on atteint la <strong>cabane</strong> (2172 m, environ 3 h).</p>
<p>Continuer jusqu’à l’<strong>Alpe Motterascio</strong> : monter un escalier métallique (avec des chiens, le contourner par la droite sur le chemin des vaches) et traverser le pâturage entre ruisseaux et terrain marécageux jusqu’à la large selle du <strong>Crap la Crusch</strong> (2268 m, environ 1 h), avec une vue fantastique sur la Plaun la Greina.</p>
<p>Toujours sur le sentier blanc-rouge-blanc, monter au <strong>col de la Greina</strong> (2355 m), le long des sources du Rhin, qui se jette dans la mer du Nord, et continuer jusqu’à la <strong>Capanna Scaletta</strong> (2205 m, 2 h), en dominant les méandres du Brenno, qui coule au contraire vers la Méditerranée. Pour voir l’<strong>arche de la Greina</strong>, faire un petit détour le long des méandres ; de l’arche, un sentier blanc-bleu-blanc mène à la Scaletta, seulement pour randonneurs expérimentés et sans glace ni neige ; sinon revenir au sentier blanc-rouge-blanc (1 h). De la Scaletta, la descente vers <strong>Pian Geirètt</strong> est raide mais courte (1 h), et le Bus alpin vous ramène à Ghirone.</p>
<p>Le tour se fait aussi dans l’autre sens, conseillé aux familles car la montée depuis Pian Geirètt est moins fatigante que celle depuis le Luzzone.</p>""",
                 dati=[("Longueur", "17 km"), ("Montée", "+700 m"), ("Temps", "6 h"), ("Difficulté", "T2"),
                       ("Points forts", "Alpe Garzott, Alpe Motterascio, Crap la Crusch, la ligne de partage des eaux, les sources du Rhin et du Brenno, les petites tours rocheuses, les méandres, l’arche de la Greina")],
                 link=[("Carte en ligne de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=7.09&amp;E=2717383&amp;N=1160737&amp;trackId=4244704")]),
            dict(file="proposte-gite", titolo="Propositions de courses",
                 lead="Six courses depuis la cabane : Crap la Crusch, Piz Terri, l’arche de la Greina, la Plaun la Greina et la Via Crio.",
                 img=("crap-la-crusch", "Le grand rocher du Crap la Crusch avec sa croix, sur la plaine de la Greina"),
                 corpo="""<p>Si vous avez plusieurs jours, ces itinéraires permettent de vivre pleinement la magie de la Greina. Presque tous partent de la cabane et y reviennent.</p>""",
                 itinerari=[
                     dict(titolo="Crap la Crusch", img=("crap-la-crusch", "Le grand rocher du Crap la Crusch avec sa croix, sur la plaine de la Greina"),
                          testo="Une promenade facile jusqu’au cœur de la Greina, par l’Alpe Motterascio et le Ri di Motterascio.",
                          dati=[("Longueur", "6 km"), ("Montée", "+180 m"), ("Temps", "2 h"), ("Difficulté", "T2")],
                          link=[("Description de l’itinéraire", "docs/capanne/motterascio/a-crap-la-crusch.pdf")]),
                     dict(titolo="Piz Terri", img=("piz-terri", "La pyramide du Piz Terri au soleil"),
                          testo="Le Val Güida, le Piz Terri, le Laghet la Greina, le Val Canal et le Crap la Crusch.",
                          dati=[("Longueur", "11 km"), ("Montée", "+1100 m"), ("Temps", "6 h"), ("Difficulté", "T3-T4")],
                          link=[("Description de l’itinéraire", "docs/capanne/motterascio/b-piz-terri.pdf")]),
                     dict(titolo="Pizzo Coroi et Capanna Scaletta", img=("arco-greina", "L’arche rocheuse naturelle de la Greina"),
                          testo="Le Pizzo Coroi, l’arche de la Greina, les méandres, les petites tours rocheuses et les sources du Brenno et du Rhin.",
                          dati=[("Longueur", "15 km"), ("Montée", "+900 m"), ("Temps", "6 h"), ("Difficulté", "T3")],
                          link=[("Description de l’itinéraire", "docs/capanne/motterascio/c-pizzo-coroi-capanna-scaletta.pdf")]),
                     dict(titolo="Plaun la Greina et la Terrihütte", img=("plaun-la-greina", "Vue d’en haut des vallées et des arêtes autour de la Greina"),
                          testo="Les sources du Rhin, les méandres, les tourbières, les terrasses parallèles, les buttes herbeuses et le Muot la Greina.",
                          dati=[("Longueur", "13 km"), ("Montée", "+400 m"), ("Temps", "4 h"), ("Difficulté", "T2")],
                          link=[("Description de l’itinéraire", "docs/capanne/motterascio/d-plaun-la-greina-capanna-terri.pdf")]),
                     dict(titolo="Val Larciolo", img=("val-larciolo", "Les chalets de l’Alpe Larciolo parmi les mélèzes dorés de l’automne"),
                          testo="Une variante solitaire et sauvage, hors des sentiers balisés, qui rejoint la cabane par le haut en venant du Luzzone, par l’Alpe Coroi, l’Alpe Larciolo et l’Alpe Garzott.",
                          dati=[("Longueur", "7 km"), ("Montée", "+250 m"), ("Temps", "2 h"), ("Difficulté", "T2-T3")],
                          link=[("Description de l’itinéraire", "docs/capanne/motterascio/e-val-larciolo.pdf")]),
                     dict(titolo="Via Crio, étapes 7 et 8", img=("via-crio", "Un randonneur sur un passage équipé parmi des roches rougeâtres"),
                          testo="Deux étapes de la Via Crio passent par la cabane.",
                          link=[("Étape 7", "https://www.viacrio.ch/tappa7"), ("Étape 8", "https://www.viacrio.ch/tappa8"),
                                ("Vue d’ensemble de la Via Crio", "docs/capanne/motterascio/prospettocrio.pdf"),
                                ("Profil altimétrique de la Via Crio", "docs/capanne/motterascio/altimetria-totale.pdf")]),
                 ]),
            dict(file="trekking-greina-alta", titolo="Trek Greina Alta", foto="trekking-greina-alta",
                 lead="De Curaglia à Vals en quatre étapes : trois cabanes du CAS, trois cultures, trois langues.",
                 img=("escursionisti-greina", "Des randonneurs sur un pré en direction des montagnes"),
                 corpo="""<p>Camona da Medel, Capanna Michela Motterascio, Läntahütte : le trek Greina Alta, pour randonneurs moyens à expérimentés, mène de Curaglia à Vals, avec un dénominateur commun, le chiffre 3. Il traverse une région avec 3 cabanes du CAS, 3 cultures, 3 langues et 3 sommets imposants. Si vous parcourez tout le trek, vous pouvez demander une réservation forfaitaire à l’une des trois cabanes.</p>
<ul>
<li><strong>Jour 1 :</strong> (Disentis) Curaglia (1332 m), Val Platta, Alp Sura (1982 m), Camona da Medel (2524 m). 3 h 30, T3.</li>
<li><strong>Jour 2 :</strong> Camona da Medel, Fuorcla Sura da Lavaz (2703 m), col de la Greina (2355 m), Crap la Crusch (2268 m), Capanna Michela Motterascio (2172 m). 6 h, T4.</li>
<li><strong>Jour 3 :</strong> Capanna Michela Motterascio, lac de Luzzone, Larecc (1633 m), Val Scaradra, Passo Soreda (2759 m), Läntatal, Läntahütte (2090 m). 7 h, T3.</li>
<li><strong>Jour 4 :</strong> Läntahütte, Furggelti (2712 m), Zervreilasee (1862 m), Zervreila (Vals). 5 h, T3.</li>
</ul>""",
                 dati=[("Longueur", "45 km"), ("Montée", "+4200 m"), ("Temps", "6-7 h par jour"), ("Difficulté", "T3-T4"),
                       ("Meilleure période", "De mi-juillet à début octobre"),
                       ("Points forts", "Val Platta, Fuorcla Sura da Lavaz, la Greina, le lac de Luzzone, le Val Scaradra, le Läntatal, le Zervreilasee")],
                 link=[("Le site du trek", "https://greinaalta.ch/"),
                       ("Carte en ligne de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=17.65&amp;E=2718864&amp;N=1162797&amp;layers=Wanderland&amp;trackId=4230099")]),
        ],
        sostenitori=dict(
            testo="Un grand merci aux partenaires qui soutiennent la cabane.",
            loghi=[("Suisse Tourisme", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/fr-ch/"),
                   ("Ticino Turismo", "sostenitori/ticino-turismo", "https://www.ticino.ch/fr/"),
                   ("Bellinzona e Valli Turismo", "sostenitori/bellinzona-e-valli", "https://www.bellinzonaevalli.ch/"),
                   ("Blenio Turismo", "sostenitori/blenio-turismo", "https://www.vallediblenio.ch/"),
                   ("Patriziato Generale di Aquila, Torre e Lottigna", "sostenitori/patriziato-aquila-torre", "https://comuneblenio.ch/Aquila")]),
        foto=[("La cabane", "capanna"), ("La cuisine", "cucina"), ("Les environs", "dintorni")],
    ),

    "montebar.html": dict(
        cartella="montebar",
        capanna="""<p>La nouvelle cabane du CAS Ticino a été inaugurée en 2016, exactement 80 ans après le premier bâtiment. Le projet « Barlume » des architectes Oliviero Piffaretti et Carlo Romano (Atelier PeR, Mendrisio), choisi parmi une trentaine de propositions, est un bâtiment simple et cubique en bois de mélèze autour de la cheminée : une lanterne dans le paysage, en dialogue avec les cabanes des sommets alentour.</p>
<p>La salle à manger, cœur de la cabane, a des fenêtres de tous côtés et jusqu’à 60 places ; la terrasse est accessible depuis la salle à manger et depuis la cuisine. Aux étages se trouvent des chambres de 2, 4 et 6 lits en couchettes, avec toilettes à chaque étage ; une salle d’atelier accueille réunions, cours et écoles. Au sous-sol se trouvent les sanitaires, le local ouvert aux randonneurs quand la cabane est fermée et le local à vélos avec bornes de recharge et un petit atelier, au standard Bike Hotel.</p>
<p>Facile à atteindre par un réseau dense de sentiers de randonnée et de VTT, avec une nature, une histoire et des paysages surprenants, c’est la destination idéale pour les familles et les écoles, ou pour une nuit à la cabane après un souper convivial.</p>""",
        cucina="""<p>Nous cuisinons avec passion des produits frais et de saison de la région, avec la cuisine tessinoise comme référence. Le repas de midi est servi de 11 h 30 à 15 h ; l’après-midi, il y a toujours une soupe, des assiettes froides et des gâteaux. Le souper est à 19 h : le soir, merci de réserver. Sur demande, nous préparons aussi des menus pour des occasions spéciales.</p>
<ul>
<li>Gâteaux maison, minestrone aux légumes et légumineuses, polenta tessinoise.</li>
<li>Fromages des alpages voisins et charcuterie tessinoise.</li>
<li>Grillades sur la terrasse en été, gibier en automne, fondue au fromage en hiver.</li>
</ul>
<p>Petit-déjeuner dès 7 h 45 (dès 8 h en hiver). Les chiens ne sont pas admis dans la cabane ; les mineurs sont les bienvenus accompagnés d’un adulte. À partir de 22 h, merci de respecter ceux qui dorment.</p>""",
        team=dict(titolo="Les gardiens", img=("gestori", "James Mauri et Serge Santese sur les pâturages devant la cabane")),
        accessi="""<p>À pied ou à VTT, la cabane s’atteint facilement, surtout par des sentiers adaptés aux familles. En hiver aussi, on peut monter à skis ou à raquettes, mais n’oubliez pas que les conditions en montagne peuvent être différentes de celles de la vallée. Les places de parc dans la vallée sont limitées : mieux vaut prendre les transports publics.</p>
<ul>
<li>De Corticiasca : 1 h 30.</li>
<li>De Bidogno : 2 h.</li>
<li>D’Isone par le Val Serdena et Piandanazzo : 3 h.</li>
<li>De Gola di Lago : 2 h 30.</li>
<li>De Scareglia ou Signôra : 3 h 30.</li>
</ul>
<p>Itinéraires sur <a href="https://schweizmobil.ch/fr/map?bgLayer=pk&amp;layers=wanderland%2Cveloland&amp;season=summer&amp;highlightPointCoordinates=2721818-1106610&amp;E=2721449&amp;N=1106526&amp;resolution=4.51" rel="noopener">SuisseMobile</a>. Carte : carte nationale 1:25 000 feuille 1333 Tesserete.</p>
<p><strong>Sécurité :</strong> en hiver, la glace et la neige rendent délicats même les passages faciles, et il y a un danger d’avalanche sur les pentes raides et dans les couloirs. En été, des vaches allaitantes avec leurs veaux pâturent ici : gardez vos distances et tenez les chiens en laisse. Cyclistes, merci de respecter les randonneurs. Ne laissez pas de déchets et n’allumez pas de feu en plein air : le Monte Bar a été touché par des incendies dévastateurs par le passé.</p>""",
        attivita="""<p>La région offre d’innombrables possibilités de VTT, sur goudron, routes non goudronnées et singletrails, avec des boucles panoramiques une bonne partie de l’année : les itinéraires nationaux 66, 358 et 359 sont décrits par <a href="https://www.luganoregion.com/fr" rel="noopener">Lugano Region</a>. Depuis la cabane, on peut aussi franchir le Passo San Lucio vers le Val Cavargna ou partir vers le nord dans le Val Serdena et jusqu’à Rivera.</p>
<p>La chaîne qui va de Gola di Lago jusqu’aux 2115 m du Gazzirola est sillonnée de sentiers faciles. La cabane est le but et une étape du Lugano Trekking et de l’itinéraire national 52 ; d’ici on peut rejoindre le Camoghè et le Val Morobbia. L’automne et le printemps sont les saisons idéales.</p>""",
        pagine=[
            dict(file="escursioni", titolo="Sentiers thématiques",
                 lead="Sept sentiers faciles à travers l’histoire, la nature et le paysage : des porteuses de skis à la faune.",
                 img=("escursionista-cresta", "Un randonneur sur un sentier de crête herbeux, avec les lacs derrière"),
                 corpo="""<p>Sept sentiers thématiques pour découvrir des coins peu connus, souvent avec des rencontres et des découvertes surprenantes. Tous sont faciles (T2).</p>""",
                 itinerari=[
                     dict(titolo="Le sentier des porteuses de skis", img=("portatrici-sci", "Photographie historique de femmes portant des skis dans la neige"),
                          testo="Il rappelle les « sherpas » qui portaient les skis des Luganais aisés, arrivés à Bidogno en car postal, de la place de l’église San Barnaba jusqu’à la cabane.",
                          dati=[("Longueur", "4 km"), ("Montée", "+800 m"), ("Temps", "2 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2721402&amp;N=1105567&amp;trackId=4074166"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/il-sentiero-delle-portatrici-di-sci.pdf")]),
                     dict(titolo="Le sentier des Barchi", img=("barchi", "Anciennes étables en pierre sur les pâturages sous le Monte Bar"),
                          testo="De Corticiasca à la terrasse des Barchi, les bâtiments typiques du Val Colla où le bétail séjournait au printemps et en automne, et qui ont donné son nom au Monte Bar.",
                          dati=[("Longueur", "4 km"), ("Montée", "+600 m"), ("Temps", "2 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721927&amp;N=1105895&amp;trackId=4073878"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/barchi.pdf")]),
                     dict(titolo="Le sentier panoramique", img=("tramonto-pascoli", "Des pâturages dans la lumière du soir, les vallées dans la brume"),
                          testo="De Roveredo, où le compositeur Ernest Bloch vécut de 1930 à 1939, jusqu’aux mayens, oasis de paix.",
                          dati=[("Longueur", "6 km"), ("Montée", "+900 m"), ("Temps", "3 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2720510&amp;N=1105400&amp;trackId=4073853"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/panoramico.pdf")]),
                     dict(titolo="Le sentier des glaciers", img=("tramonto-luganese", "La cabane sur la pente enneigée dans la lumière du soir, avec les lumières de Lugano"),
                          testo="Près de Gola di Lago, tourbières, gouilles, plantes carnivores et roches moutonnées témoignent d’une langue du glacier du Tessin lors de la dernière glaciation.",
                          dati=[("Longueur", "7 km"), ("Montée", "+700 m"), ("Temps", "3 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2719894&amp;N=1106340&amp;trackId=4074157"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/ghiacciai.pdf")]),
                     dict(titolo="Le sentier de la végétation", img=("genziane", "Des gentianes violettes dans l’herbe"),
                          testo="Il traverse tous les étages de végétation, des châtaigniers insubriens à l’étage arctico-alpin sur la crête de la Cima di Moncucco.",
                          dati=[("Longueur", "7 km"), ("Montée", "+800 m"), ("Temps", "4 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722942&amp;N=1106858&amp;trackId=4074169"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/vegetazione.pdf")]),
                     dict(titolo="Le sentier du reboisement", img=("piantagioni", "La cabane sur les pâturages dorés du Monte Bar"),
                          testo="Un sentier facile et ombragé à travers une forêt protectrice plantée à la fin du XIXe siècle pour préserver le régime des eaux dans la vallée du Cassarate.",
                          dati=[("Longueur", "7 km"), ("Montée", "+800 m"), ("Temps", "4 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722222&amp;N=1106106&amp;trackId=4074163"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/piantagioni.pdf")]),
                     dict(titolo="Le sentier de la faune", img=("cervo", "Un cerf qui brame sur une pente herbeuse"),
                          testo="Un sentier facile à travers la forêt sauvage, avec des rencontres surprenantes : chevreuils, cerfs, écureuils et sangliers.",
                          dati=[("Longueur", "7 km"), ("Montée", "+200 m"), ("Temps", "3 h"), ("Difficulté", "T2")],
                          link=[("Carte de l’itinéraire", "https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722748&amp;N=1107781&amp;trackId=4074167"),
                                ("Description de l’itinéraire", "docs/capanne/montebar/selvaggina.pdf")]),
                 ]),
            dict(file="mountain-bike", titolo="VTT",
                 lead="Des boucles panoramiques sur goudron, routes non goudronnées et singletrails, avec un local à vélos et des bornes de recharge à la cabane.",
                 img=("mountain-bike", "Deux vététistes sur les pâturages, avec le lac de Lugano derrière"),
                 corpo="""<p>La région du Monte Bar offre d’innombrables possibilités de VTT : goudron, routes non goudronnées et singletrails alternent sur des boucles panoramiques praticables une bonne partie de l’année. Les principaux itinéraires, en particulier les itinéraires nationaux 66, 358 et 359, sont décrits sur le site de <a href="https://www.luganoregion.com/fr" rel="noopener">Lugano Region</a>.</p>
<p>Depuis la cabane, on peut aussi franchir le Passo San Lucio vers le Val Cavargna ou partir vers le nord dans le Val Serdena et jusqu’à Rivera.</p>
<p>La cabane répond au standard Bike Hotel : un local à vélos fermé, des bornes de recharge et un petit atelier. Nous demandons à tous les cyclistes de respecter les randonneurs.</p>"""),
            dict(file="curiosita", titolo="Le saviez-vous ?",
                 lead="L’origine du nom, les forêts disparues, les « sherpas » et les pierres à cupules du Monte Bar.",
                 img=("valle-colla", "Vue sur les vallées et la région de Lugano depuis les pentes du Monte Bar"),
                 itinerari=[
                     dict(titolo="L’origine du nom", img=("valle-colla", "Vue sur les vallées et la région de Lugano depuis les pentes du Monte Bar"),
                          testo="Au cours des deux derniers millions d’années, la région s’est soulevée en trois phases, formant trois terrasses : celle des villages, celle des « Barchi » et celle des alpages. Les Barchi, typiques du Val Colla et de la Capriasca, étaient des étables avec un fenil près du village, non habitées : les femmes y montaient deux fois par jour pour traire, et le lait était transformé en fromage et en beurre à la maison. De « barc » vient le nom du Monte Bar."),
                     dict(titolo="La forêt disparue", img=("bosco-nebbia", "Forêts et pâturages émergeant d’une mer de brouillard"),
                          testo="Le Monte Bar était autrefois boisé. Après les soulèvements de Milan en 1848, l’Autriche expulsa les émigrés tessinois de Lombardie et ferma les frontières : les travailleurs saisonniers rentrés au pays aggravèrent la famine, et de grandes surfaces de forêt furent défrichées ou brûlées pour gagner des champs et des pâturages. La montagne devint nue ; après les graves inondations de 1896, les pentes furent largement reboisées contre l’érosion, comme on le voit encore aujourd’hui."),
                     dict(titolo="Un voyage dans la nature", img=("ellebori", "Des roses de Noël en fleur à contre-jour"),
                          testo="Lors de la dernière glaciation, la glace est restée sous 1200 m : les sommets libres de glace furent une véritable arche de Noé pour les plantes et les animaux, et entre le Caval Drossa et le Gazzirola on trouve des espèces plus anciennes que les glaciations, à côté de plantes arctiques poussées jusqu’ici par le froid. Sur une petite surface, on passe des châtaigniers à la hêtraie et à la forêt de conifères, puis aux lichens, aux mousses et à la flore alpine des sommets."),
                     dict(titolo="Les « sherpas » du Tessin", img=("portatrici-storica", "Photographie historique de porteuses en file sur une pente enneigée"),
                          testo="Quand la première cabane fut construite en 1936, les femmes de Bidogno portèrent les matériaux de construction jusqu’au chantier dans des hottes sur le dos ; ensuite elles portèrent les skis des Luganais de la place de l’église jusqu’à la cabane, pour 50 centimes la paire. Elles montaient aussi de jeunes arbres pour le reboisement, ramassaient feuilles et fougères comme litière pour les étables et, pendant la Première Guerre mondiale, apportaient de la nourriture aux soldats jusqu’au Camoghè."),
                     dict(titolo="Pierres à cupules et gravures rupestres", img=("masso-coppellare", "Un homme observant les signes d’une pierre à cupules dans la forêt"),
                          testo="Sur le Monte Bar, de nombreux rochers portent des signes gravés : cupules, rainures, croix, empreintes de pieds, cercles de pierres. Peut-être des bornes, des lieux de culte du soleil ou de pèlerinage, ou des creux pour l’eau de pluie et l’huile à brûler. À voir : la borne entre Bidogno et Corticiasca, le rocher de Gola di Lago, le « Motarell de la Stria » à Roveredo, le « Gigante » et « Ul pé del Crist » à Lelgio, la « Balena bianca » à Caslasc, les blocs de Pian di Sotto et la pierre de la Madone de Borisio."),
                 ]),
        ],
        storia=dict(
            file="storia", titolo="Histoire de la cabane", foto="storia",
            lead="De la première école de ski du Tessin en 1935, en passant par la cabane de 1936, jusqu’à la nouvelle cabane « Barlume » de 2016.",
            img=("capanna-1936", "Photographie historique de la première cabane en pierre avec des skieurs dans la neige"),
            corpo="""<p>Après l’expérience des Monti di Condra, le CAS obtint en 1935 le chalet de l’Alpe Musgatina comme quartier d’hiver pour la première école de ski du canton du Tessin, avec les moniteurs Tita Calvi et Aldo Balmelli.</p>
<p>Le succès fut tel qu’en 1936, pour le cinquantième anniversaire de la Section Ticino, une cabane fut construite sur le Monte Bar ; le chantier donna du travail aux nombreux émigrés saisonniers de la vallée. La cabane devint vite la destination de nombreux groupes de skieurs : le dimanche, il y avait jusqu’à 300 personnes sur les pistes. Le Sci Club Lugano reprit la gestion hivernale, et le slalom géant du Monte Bar connut un grand succès. En été, la cabane était un camp de base pour les sommets alentour.</p>
<p>En 2013, la section décida de construire une nouvelle cabane : celle de 1936, améliorée en 1993, avait désormais de graves problèmes de logistique, de sécurité et de ravitaillement. Le but était un bâtiment moderne, pratique et écologique, avec le caractère d’une cabane de montagne classique. Le projet a été développé avec la commune de Capriasca (projet Areaviva) et différents partenaires locaux, pour valoriser toute la région.</p>
<p>Le concours de 2014, avec une trentaine de propositions, a été remporté par « Barlume » des architectes Oliviero Piffaretti et Carlo Romano (Atelier PeR, Mendrisio) : un bâtiment simple et cubique en bois autour de la cheminée, symbole de rencontre. La montagne reste l’élément déterminant, et la cabane est une lanterne dans le paysage. Inaugurée en 2016, 80 ans après la première cabane, à 1602 m sur les pâturages exposés au sud, c’est peut-être la plus belle terrasse sur Lugano, les Préalpes, les Apennins avec le Mont Viso, le Mont Rose et les Alpes tessinoises, avec des couchers de soleil inoubliables.</p>
<p><a href="https://www.simonemengani.ch/nuovo-servizio-fotografico-capanna-monte-bar/" rel="noopener">Photos de la construction par Simone Mengani</a></p>"""),
        sostenitori=dict(
            testo="La nouvelle cabane a été rendue possible par ces soutiens et par plus de 300 amis, publics et privés, qui ont contribué à sa construction. Un grand merci !",
            loghi=[("République et Canton du Tessin", "cantone-ticino"), ("Swisslos", "swisslos"), ("Ville de Lugano", "citta-di-lugano"),
                   ("Commune de Capriasca", "comune-di-capriasca"), ("Banca Raiffeisen del Cassarate", "raiffeisen"), ("BancaStato", "bancastato"),
                   ("Cornèr Banca", "corner-banca"), ("EFG", "efg"), ("Lugano Turismo", "lugano-turismo"), ("Revifida", "revifida"),
                   ("Ernst Göhner Stiftung", "ernst-gohner-stiftung"), ("Lambertini, Ernst & Partners", "lambertini-ernst-partners"),
                   ("Blue Planet", "blue-planet"), ("The North Face and VF", "the-north-face-vf"), ("Ente regionale per lo sviluppo del Luganese", "ersl")]),
        foto=[("La cabane", "capanna"), ("La cuisine", "cucina"), ("Les environs", "dintorni")],
    ),

    "baitadelluca.html": dict(
        cartella="baitadelluca",
        capanna_titolo="La baita",
        capanna="""<p>La baita compte 16 places dans deux chambres de 4 et 12 places, une salle commune avec cuisine au gaz et cheminée, eau chaude et douche ; la lumière vient de panneaux solaires. Vaisselle et casseroles sont fournies, et des boissons sont disponibles en quantité limitée. Réception moyenne, pas de Wi-Fi ni de téléphone.</p>
<p>Elle n’est pas gardiennée : la porte est fermée à clé et le code vous est donné par la responsable. Rapide et facile à atteindre, elle sert aussi pour des cours, des journées de formation ou simplement pour un souper entre amis.</p>""",
        accessi="""<ul>
<li>De Rosone (bus) : 45 min, +270 m, T2 (<a href="https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2722290&amp;N=1102884&amp;layers=Wanderland%2CStation&amp;trackId=5273099" rel="noopener">itinéraire</a>).</li>
<li>De Sonvico (bus) : 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721523&amp;N=1102174&amp;layers=Wanderland%2CStation&amp;trackId=5273106" rel="noopener">itinéraire</a>).</li>
<li>De Villa Luganese (bus) : 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=fr&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721748&amp;N=1101916&amp;layers=Wanderland%2CStation&amp;trackId=5273108" rel="noopener">itinéraire</a>).</li>
</ul>
<p>Carte : carte nationale 1:25 000 feuille 1333 Tesserete.</p>""",
        pagine=[
            dict(file="attivita", titolo="Randonnée et escalade",
                 lead="Des randonnées vers les sommets et cabanes alentour, plus de 200 voies sur le calcaire des Denti della Vecchia et le Lugano Bike 66.",
                 img=("sentiero-denti", "Un randonneur sur le sentier au pied des tours rocheuses des Denti della Vecchia"),
                 itinerari=[
                     dict(titolo="Randonnée", img=("sentiero-denti", "Un randonneur sur le sentier au pied des tours rocheuses des Denti della Vecchia"),
                          testo="De la baita à l’Alpe Bolla 3 h, à Villa Luganese 3 h, au sommet de la Fojorina 4 h ; de Brè à la baita 4-5 h ; de la baita à la Capanna San Lucio 4 h et à la <a href=\"fr/montebar.html\">Capanna Monte Bar</a> 6 h, ou 9 h par les sommets de la Fojorina et du Gazzirola.",
                          link=[("Des archives, 1997 : Prealpi ticinesi 5, du Passo San Jorio au Monte Generoso", "docs/capanne/baitadelluca/baita-del-luca-prealpi-ticinesi-5-passo-s-jorio-generoso.pdf")]),
                     dict(titolo="Escalade", img=("arrampicata-denti", "Des grimpeurs sur les dalles calcaires des Denti della Vecchia"),
                          testo="Les Denti della Vecchia sont un paradis de l’escalade avec plus de 200 voies sur calcaire. Le guide du Gruppo Scoiattoli est en ligne sur <a href=\"https://scoiattoli.ch/\" rel=\"noopener\">scoiattoli.ch</a> ; un exemplaire imprimé est aussi consultable à la baita.",
                          link=[("Guide d’escalade des Denti della Vecchia (Gruppo Scoiattoli)", "https://scoiattoli.ch/wp-content/uploads/2020/06/GUIDA-DENTI-DELLA-VECCHIA-.pdf"),
                                ("Denti della Vecchia : nouvelles voies 2023", "docs/capanne/baitadelluca/denti-news-2023.pdf"),
                                ("Denti della Vecchia : Nirvana 2023", "docs/capanne/baitadelluca/denti-nirvana-news-2023.pdf"),
                                ("Denti della Vecchia : Paléo 2023", "docs/capanne/baitadelluca/denti-paleo-news-2023.pdf")]),
                     dict(titolo="VTT", img=("mountain-bike", "Un vététiste sur un sentier forestier"),
                          testo="Plusieurs itinéraires traversent les environs, et la baita est tout près de l’itinéraire Lugano Bike 66.",
                          link=[("Le VTT sur Lugano Region", "https://www.luganoregion.com/fr")]),
                 ]),
        ],
        sostenitori=dict(
            testo="Un grand merci aux partenaires qui soutiennent la baita.",
            loghi=[("Suisse Tourisme", "sostenitori/svizzera-turismo", "https://www.myswitzerland.com/fr-ch/"),
                   ("Ticino Turismo", "sostenitori/ticino-turismo", "https://www.ticino.ch/fr/"),
                   ("Lugano Region", "sostenitori/lugano-region", "https://www.luganoregion.com/fr")]),
        foto=[("La baita", "capanna"), ("Les environs", "dintorni")],
        foto_lead="La baita et les environs",
    ),
}
