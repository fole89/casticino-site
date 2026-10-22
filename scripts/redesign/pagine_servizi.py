"""Servizi: Link utili (LINKS), Documenti (DOCS), Noleggio materiale e Mercatino."""
from urllib.parse import quote
from comune import *


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
                      ("Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)", "https://lawinen.report/"), ("AINEVA, bollettini valanghe in Italia", "https://bollettini.aineva.it/"),
                      ("Météo-France, meteo e valanghe", "https://meteofrance.com/meteo-montagne")]),
    ("Condizioni e resoconti", [("Hikr", "https://www.hikr.org/"), ("On-ice, nord Italia", "http://www.on-ice.it/"),
                                ("Gipfelbuch, resoconti in Svizzera", "https://www.gipfelbuch.ch/"), ("Camptocamp", "https://www.camptocamp.org/"),
                                ("Montagne in Valle d’Aosta", "https://www.montagneinvalledaosta.com/"), ("MonteRosa4000", "https://www.monterosa4000.it/"),
                                ("ViaFerrata.org", "https://www.viaferrata.org/")]),
    ("Mappe e guide", [("MapPlus", "https://www.mapplus.ch/"), ("swisstopo", "https://www.swisstopo.ch/"),
                       ("Piz Bube, guide e cartine", "https://www.pizbube.ch/"), ("Edizioni CAS (SAC-Verlag)", "https://www.sac-verlag.ch/")]),
    ("Società alpinistiche ticinesi", [("CAS Bellinzona e valli", "https://www.casbellinzona.ch/"), ("CAS Locarno", "https://www.caslocarno.ch/"),
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
            "AINEVA, bollettini valanghe in Italia": "AINEVA, Lawinenbulletins Italien", "Météo-France, meteo e valanghe": "Météo-France, Wetter und Lawinen",
            "On-ice, nord Italia": "On-ice, Norditalien", "Gipfelbuch, resoconti in Svizzera": "Gipfelbuch, Tourenberichte Schweiz",
            "Montagne in Valle d’Aosta": "Berge im Aostatal", "Piz Bube, guide e cartine": "Piz Bube, Führer und Karten",
            "Edizioni CAS (SAC-Verlag)": "SAC-Verlag", "Federazione Alpinistica Ticinese": "Tessiner Bergsteigerverband (FAT)",
            "CAS Centrale": "SAC Zentralverband", "Gioventù+Sport": "Jugend+Sport", "Ufficio cantonale G+S": "Kantonales J+S-Amt",
            "Capanne CAS in Svizzera": "SAC-Hütten in der Schweiz", "Capanneti, rifugi Ticino e Mesolcina": "Capanneti, Hütten im Tessin und Misox",
            "Gruppo Guide Alpine Ticino": "Tessiner Bergführer", "Soccorso Alpino Svizzero": "Alpine Rettung Schweiz",
            "PicAlciot, vie d’arrampicata in Ticino": "PicAlciot, Kletterrouten im Tessin", "Portale DropTour": "DropTour-Portal",
            "Reset password": "Passwort zurücksetzen"}


LINKS_FR = {"Capigita": "Chefs de course", "Meteo e neve": "Météo et neige", "Condizioni e resoconti": "Conditions et récits de courses",
            "Mappe e guide": "Cartes et guides", "Società alpinistiche ticinesi": "Sociétés alpines tessinoises", "Formazione": "Formation",
            "Capanne, guide e soccorso": "Cabanes, guides et secours", "Eventi e altre società": "Événements et autres sociétés",
            "News di montagna": "Actualités de montagne",
            "SLF, bollettini valanghe in Svizzera": "SLF, bulletin d’avalanches en Suisse", "MeteoSvizzera": "MétéoSuisse",
            "Meteoblue, previsioni a 7 giorni": "Meteoblue, prévisions à 7 jours", "Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)": "Bulletin d’avalanches Euregio (Tyrol, Haut-Adige, Trentin)",
            "AINEVA, bollettini valanghe in Italia": "AINEVA, bulletins d’avalanches en Italie", "Météo-France, meteo e valanghe": "Météo-France, météo et avalanches",
            "On-ice, nord Italia": "On-ice, nord de l’Italie", "Gipfelbuch, resoconti in Svizzera": "Gipfelbuch, récits de courses en Suisse",
            "Montagne in Valle d’Aosta": "Montagnes du Val d’Aoste", "Piz Bube, guide e cartine": "Piz Bube, guides et cartes",
            "Edizioni CAS (SAC-Verlag)": "Éditions du CAS (SAC-Verlag)", "Federazione Alpinistica Ticinese": "Fédération alpine tessinoise (FAT)",
            "CAS Centrale": "CAS central", "Gioventù+Sport": "Jeunesse+Sport", "Ufficio cantonale G+S": "Office cantonal J+S",
            "Capanne CAS in Svizzera": "Cabanes du CAS en Suisse", "Capanneti, rifugi Ticino e Mesolcina": "Capanneti, cabanes du Tessin et de la Mesolcina",
            "Gruppo Guide Alpine Ticino": "Guides de montagne du Tessin", "Soccorso Alpino Svizzero": "Secours Alpin Suisse",
            "PicAlciot, vie d’arrampicata in Ticino": "PicAlciot, voies d’escalade au Tessin", "Portale DropTour": "Portail DropTour",
            "Reset password": "Réinitialiser le mot de passe"}


LINKS_EN = {"Capigita": "Trip leaders", "Meteo e neve": "Weather and snow", "Condizioni e resoconti": "Conditions and trip reports",
            "Mappe e guide": "Maps and guidebooks", "Società alpinistiche ticinesi": "Ticino mountaineering clubs", "Formazione": "Training",
            "Capanne, guide e soccorso": "Huts, guides and rescue", "Eventi e altre società": "Events and other clubs",
            "News di montagna": "Mountain news",
            "SLF, bollettini valanghe in Svizzera": "SLF, Swiss avalanche bulletin", "MeteoSvizzera": "MeteoSwiss",
            "Meteoblue, previsioni a 7 giorni": "Meteoblue, 7-day forecast", "Bollettino valanghe Euregio (Tirolo, Alto Adige, Trentino)": "Euregio avalanche bulletin (Tyrol, South Tyrol, Trentino)",
            "AINEVA, bollettini valanghe in Italia": "AINEVA, avalanche bulletins in Italy", "Météo-France, meteo e valanghe": "Météo-France, weather and avalanches",
            "On-ice, nord Italia": "On-ice, northern Italy", "Gipfelbuch, resoconti in Svizzera": "Gipfelbuch, trip reports in Switzerland",
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
    elif fr():
        gruppi = [(LINKS_FR.get(g, g), [(LINKS_FR.get(n, n), u) for n, u in links]) for g, links in LINKS]
        hero = page_hero([("Services", "fr/noleggio.html"), ("Liens utiles", None)], "Liens utiles",
                         "Météo, bulletins d’avalanches, conditions, cartes et les autres sociétés alpines de la région.")
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
    if fr():
        return sezione_page("link.html", "Liens utiles | CAS Ticino",
                            "Liens utiles pour la montagne : météo et bulletins d’avalanches, conditions, cartes, sociétés alpines tessinoises, formation et secours.", body)
    if en():
        return sezione_page("link.html", "Useful links | CAS Ticino",
                            "Useful links for the mountains: weather and avalanche bulletins, conditions, maps, Ticino mountaineering clubs, training and rescue.", body)
    return page("link.html", "Link utili | CAS Ticino",
                "Link utili per la montagna: meteo e bollettini valanghe, condizioni, cartine, società alpinistiche ticinesi, formazione e soccorso.",
                body)
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
DOCS_FR = {"La sezione": "La Section", "Statuto": "Statuts", "Visione e strategia": "Vision et stratégie", "Organigramma": "Organigramme",
           "Regolamento gite": "Règlement des courses", "Scale di difficoltà": "Échelles de difficulté", "Arrampicata sportiva": "Escalade sportive",
           "Alpinismo": "Alpinisme", "Arrampicata artificiale": "Escalade artificielle", "Escursionismo e trekking": "Randonnée et trekking",
           "Racchette": "Raquettes", "Sci alpinismo": "Ski de randonnée", "Vie ferrate": "Vias ferratas", "Promemoria": "Aide-mémoire",
           "Meteo": "Météo", "Orientamento": "Orientation", "Scalata su ghiaccio": "Escalade sur glace", "Tecnica alpina": "Technique alpine",
           "Incidente valanga e ARVA": "Accident d’avalanche et DVA", "Promemoria capigita": "Aide-mémoire des chefs de course",
           "Istruzioni DropTour": "Instructions DropTour", "Pianificazione": "Planification",
           "Formulario pianificazione gite estive": "Formulaire de planification des courses d’été", "Cartine CH 1:25 000": "Cartes nationales 1:25 000",
           "Cartine CH 1:50 000": "Cartes nationales 1:50 000", "Cartine CH 1:50 000 sci": "Cartes de ski 1:50 000",
           "Obiettivi corsi": "Objectifs des cours", "Equipaggiamento": "Équipement", "Arrampicata": "Escalade",
           "Tecnica di sci fuori pista": "Technique de ski hors piste"}
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


def documenti():
    nomi = {"it": {}, "de": DOCS_DE, "fr": DOCS_FR, "en": DOCS_EN}[LINGUA["lang"]]
    gruppi = [(nomi.get(g, g), [(nomi.get(n, n), u) for n, u in docs]) for g, docs in DOCS]
    titolo = tr("Documenti", "Dokumente", "Documents", "Documents")
    body = page_hero([servizi_crumb(), (titolo, None)], titolo, tr(
        "Statuto e documenti della sezione, scale di difficoltà, promemoria tecnici, documenti dei corsi, moduli e cartine da scaricare.",
        "Statuten und Dokumente der Sektion, Schwierigkeitsskalen, technische Merkblätter, Formulare und Karten zum Herunterladen. Die Dokumente sind auf Italienisch.",
        "The section’s statutes and documents, difficulty scales, technical fact sheets, forms and maps to download. The documents are in Italian.",
        "Statuts et documents de la section, échelles de difficulté, aide-mémoire techniques, formulaires et cartes à télécharger. Les documents sont en italien.")) + f"""

<section class="section" aria-label="{tr("Elenco dei documenti", "Liste der Dokumente", "List of documents", "Liste des documents")}">
<div class="container">
{linkgroups(gruppi, "PDF")}
<div class="callout">
<p>{tr("<strong>Annuari e Informazione</strong>, il bollettino della sezione, hanno una pagina propria.",
       "<strong>Jahrbücher und «Informazione»</strong>, das Mitteilungsblatt der Sektion, haben eine eigene Seite (italienisch).",
       "<strong>Yearbooks and «Informazione»</strong>, the section’s bulletin, have their own page (in Italian).",
       "<strong>Les annuaires et « Informazione »</strong>, le bulletin de la section, ont leur propre page (en italien).")}</p>
<div class="actions"><a class="btn btn--secondary" href="annuari.html">{tr("Annuari", "Jahrbücher", "Yearbooks", "Annuaires")}</a><a class="btn btn--secondary" href="informazione.html">Informazione</a></div>
</div>
</div>
</section>

{subnav(SERVIZI_MENU(), L("documenti.html"))}"""
    return sezione_page("documenti.html", tr("Documenti", "Dokumente", "Documents", "Documents") + " | CAS Ticino", tr(
        "Documenti del CAS Ticino da scaricare: scale di difficoltà, promemoria tecnici, promemoria capigita, obiettivi ed equipaggiamento dei corsi, pianificazione e cartine.",
        "Dokumente der SAC-Sektion Ticino zum Herunterladen (italienisch): Statuten, Tourenreglement, Schwierigkeitsskalen, Merkblätter, Formulare und Karten.",
        "Documents of the SAC Ticino Section to download (in Italian): statutes, trip regulations, difficulty scales, fact sheets, forms and maps.",
        "Documents du CAS Ticino à télécharger (en italien) : statuts, règlement des courses, échelles de difficulté, aide-mémoire, formulaires et cartes."), body)

# PDF dei corsi anche nella pagina Documenti (e quindi nella ricerca): un gruppo per tipo di documento
CARTELLE_CORSI = [("Alpinismo", "alpinismo"), ("Sci alpinismo", "sci-alpinismo"), ("Arrampicata", "arrampicata"),
                  ("Tecnica di sci fuori pista", "freeride"), ("Racchette", "racchette")]
for gruppo, file in [("Obiettivi corsi", "obiettivi"), ("Equipaggiamento", "materiale")]:
    DOCS.append((gruppo, [(nome, f"{DOC}corsi/{c}/{file}.pdf") for nome, c in CARTELLE_CORSI
                          if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, file + ".pdf"))]))


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
    """Nome di un gruppo o articolo dell'inventario nella lingua corrente (campi de/fr/en, altrimenti l'italiano)."""
    return (LINGUA["lang"] != "it" and d.get(LINGUA["lang"])) or d[chiave]


def noleggio():
    gruppi = inventario_noleggio()
    mail = f'<a href="mailto:{NOLEGGIO_MAIL}">{NOLEGGIO_MAIL}</a>'
    rows = [(tr("In breve", "Kurz gesagt", "In short", "En bref"), tr(
                "Scegli le date e il materiale nel modulo qui sotto: vedi subito cosa è libero. La conferma alla tua richiesta avverrà tramite e-mail. Si paga in contanti o TWINT alla riconsegna.",
                "Wählen Sie im Formular unten die Daten und das Material: Sie sehen sofort, was frei ist. Die Bestätigung Ihrer Anfrage erhalten Sie per E-Mail. Bezahlt wird bei der Rückgabe, bar oder mit TWINT.",
                "Choose the dates and the equipment in the form below: you see straight away what is free. Your request will be confirmed by e-mail. Payment in cash or by TWINT on return.",
                "Choisissez les dates et le matériel dans le formulaire ci-dessous : vous voyez tout de suite ce qui est libre. Votre demande sera confirmée par e-mail. Paiement en espèces ou par TWINT au retour.")),
            (tr("Richiesta", "Anfrage", "Request", "Demande"), tr("Di preferenza una settimana prima dell’attività", "Wenn möglich eine Woche vor der Aktivität", "Preferably a week before the activity", "De préférence une semaine avant l’activité")),
            (tr("Durata", "Dauer", "Duration", "Durée"), tr(f"Da 1 a {NOLEGGIO_MAX_GIORNI} giorni: il prezzo è per giorno di noleggio",
                                                   f"1 bis {NOLEGGIO_MAX_GIORNI} Tage: Der Preis gilt pro Miettag",
                                                   f"1 to {NOLEGGIO_MAX_GIORNI} days: the price is per day of hire",
                                                   f"De 1 à {NOLEGGIO_MAX_GIORNI} jours : le prix est par jour de location")),
            (tr("Ritiro e riconsegna", "Abholung und Rückgabe", "Pick-up and return", "Retrait et retour"), tr(
                "Al magazzino di Manno, al giorno e all’orario indicato nella conferma", "Im Lager in Manno, an dem Tag und zu der Zeit, die in der Bestätigung stehen",
                "At the store in Manno, on the day and at the time given in the confirmation",
                "Au dépôt de Manno, le jour et à l’heure indiqués dans la confirmation")),
            ("E-mail", mail)]
    # dati del modulo nella lingua della pagina: le quantità le dà il servizio, con la disponibilità per le date scelte
    dati = [{"nome": nome_l(g, "gruppo"), "articoli": [
        {"id": a["id"], "nome": nome_l(a), "prezzo": a["prezzo"], "taglie": list(a["taglie"]) if a.get("taglie") else None,
         "set": a.get("set")}
        for a in g["articoli"]]} for g in gruppi]
    dati = json.dumps(dati, ensure_ascii=False).replace("</", "<\\/")
    titolo = tr("Noleggio materiale", "Materialvermietung", "Equipment hire", "Location de matériel")
    body = page_hero([servizi_crumb(), (titolo, None)], tr("Noleggio", "Materialvermietung", "Equipment hire", "Location de matériel"), testo_campo(testi("introduzioni")["noleggio"], "introduzione"),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="#richiesta">{tr("Richiedi il materiale", "Material anfragen", "Request equipment", "Demander du matériel")} <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<section class="section" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">{tr("Come funziona", "So funktioniert’s", "How it works", "Comment ça marche")}</h2>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

<section class="section--surface" id="richiesta" aria-labelledby="richiesta-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="richiesta-h" class="h2">{tr("Richiesta", "Anfrage", "Request", "Demande")}</h2>
<p>{tr("Scegli le date, poi il materiale tra quello ancora libero. Ti rispondiamo per e-mail.",
       "Wählen Sie die Daten, dann das Material, das noch frei ist. Wir antworten Ihnen per E-Mail.",
       "Choose the dates, then the equipment that is still free. We reply by e-mail.",
       "Choisissez les dates, puis le matériel encore libre. Nous vous répondons par e-mail.")}</p>
</div>
<div>
<p class="nol-alt" id="nol-alt">{tr(f"Per chiedere il materiale scrivi a {mail} indicando le date, gli articoli e le taglie.",
                                    f"Für eine Anfrage schreiben Sie an {mail} mit Daten, Artikeln und Grössen.",
                                    f"To request equipment, write to {mail} with the dates, items and sizes.",
                                    f"Pour demander du matériel, écrivez à {mail} en indiquant les dates, les articles et les tailles.")}</p>
<form class="nol" id="nol" data-api="{NOLEGGIO_API}" data-sitekey="{NOLEGGIO_TURNSTILE}" data-max-giorni="{NOLEGGIO_MAX_GIORNI}" hidden novalidate>
<fieldset>
<legend class="h3">{tr("1. Quando", "1. Wann", "1. When", "1. Quand")}</legend>
<div class="campi">
<label class="campo">{tr("Primo giorno", "Erster Tag", "First day", "Premier jour")}<input type="date" name="dal" required></label>
<label class="campo">{tr("Ultimo giorno", "Letzter Tag", "Last day", "Dernier jour")}<input type="date" name="al" required></label>
</div>
<p class="small" id="nol-giorni" aria-live="polite"></p>
</fieldset>
<fieldset>
<legend class="h3">{tr("2. Materiale", "2. Material", "2. Equipment", "2. Matériel")}</legend>
<div class="nol-articoli" id="nol-articoli" aria-live="polite"><p class="small">{tr("Scegli prima le date: qui compare il materiale libero.", "Wählen Sie zuerst die Daten: Hier erscheint das freie Material.", "Choose the dates first: the free equipment appears here.", "Choisissez d’abord les dates : le matériel libre apparaît ici.")}</p></div>
</fieldset>
<fieldset>
<legend class="h3">{tr("3. I tuoi dati", "3. Ihre Angaben", "3. Your details", "3. Vos coordonnées")}</legend>
<div class="campi">
<label class="campo">{tr("Nome e cognome", "Vor- und Nachname", "Full name", "Nom et prénom")}<input name="nome" autocomplete="name" maxlength="100" required></label>
<label class="campo">{tr("Telefono", "Telefon", "Phone", "Téléphone")}<input type="tel" name="telefono" autocomplete="tel" maxlength="40" required></label>
<label class="campo campo--pieno">E-mail<input type="email" name="email" autocomplete="email" maxlength="200" required></label>
<label class="campo campo--pieno">{tr("Note (facoltative)", "Bemerkungen (freiwillig)", "Notes (optional)", "Remarques (facultatif)")}<textarea name="note" rows="3" maxlength="2000" placeholder="{tr("Per esempio l’attività o una domanda", "Zum Beispiel die Aktivität oder eine Frage", "For example the activity or a question", "Par exemple l’activité ou une question")}"></textarea></label>
</div>
</fieldset>
<div class="nol-invio">
<p class="nol-totale" id="nol-totale" aria-live="polite"></p>
<div class="nol-verifica" id="nol-verifica"></div>
<button class="btn btn--primary" type="submit">{tr("Invia la richiesta", "Anfrage senden", "Send request", "Envoyer la demande")} <span class="arrow" aria-hidden="true">→</span></button>
<p class="small">{tr('I dati servono solo a gestire il noleggio: <a href="privacy.html#noleggio">protezione dei dati</a>.',
                     'Die Angaben dienen nur der Abwicklung der Miete: <a href="privacy.html#noleggio">Datenschutz</a>.',
                     'Your details are used only to handle the hire: <a href="privacy.html#noleggio">privacy policy</a>.',
                     "Vos données servent uniquement à gérer la location : <a href=\"privacy.html#noleggio\">protection des données</a>.")}</p>
</div>
<p class="nol-esito" id="nol-esito" role="status" tabindex="-1"></p>
</form>
<script type="application/json" id="nol-dati">{dati}</script>
</div>
</div>
</section>

{subnav(SERVIZI_MENU(), L("noleggio.html"))}"""
    return sezione_page("noleggio.html", tr("Noleggio", "Materialvermietung", "Equipment hire", "Location de matériel") + " | CAS Ticino", tr(
        "Noleggio materiale del CAS Ticino: alpinismo, sci alpinismo, arrampicata, racchette e altro, con ritiro al magazzino di Manno.",
        "Materialvermietung der SAC-Sektion Ticino: Hochtouren, Skitouren, Klettern, Schneeschuhe und mehr, Abholung im Lager in Manno.",
        "Equipment hire from the SAC Ticino Section: mountaineering, ski touring, climbing, snowshoeing and more, collected from the store in Manno.",
        "Location de matériel du CAS Ticino : alpinisme, ski de randonnée, escalade, raquettes et plus, à retirer au dépôt de Manno."),
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

I attach up to 3 photos.""", "fr": """Type (à vendre / recherché / à donner) :
Titre :
Prix :
Lieu :
Description :

Nom :
Contact à publier (e-mail et/ou téléphone) :

Je joins jusqu’à 3 photos."""}
# tipi d'annuncio nelle altre lingue (il testo degli annunci resta come è stato scritto)
TIPI_L = {"it": {}, "de": {"Vendo": "Verkaufe", "Cerco": "Suche", "Regalo": "Zu verschenken"},
          "fr": {"Vendo": "À vendre", "Cerco": "Recherché", "Regalo": "À donner"},
          "en": {"Vendo": "For sale", "Cerco": "Wanted", "Regalo": "Free"}}


def tipo_l(tipo):
    return TIPI_L[LINGUA["lang"]].get(tipo, tipo)


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
        altre = "".join(f'<a href="{esc(f)}" aria-label="{tr("Foto", "Foto", "Photo", "Photo")} {i + 2} {tr("di", "von", "of", "de")} «{esc(a["title"])}»"><img src="{esc(f)}" alt="" loading="lazy" decoding="async"></a>'
                        for i, f in enumerate(foto[1:]))
        fig = f"""<figure class="annuncio-foto">
<a href="{esc(foto[0])}"><img src="{esc(foto[0])}" alt="{esc(a['title'])}" width="{w}" height="{h}" loading="lazy" decoding="async"></a>
{f'<div class="annuncio-altre">{altre}</div>' if altre else ""}
</figure>"""
    tipo = a.get("tipo") if a.get("tipo") in mercatino_util.TIPI else "Vendo"
    testo = "".join(f"<p>{esc(par).replace(chr(10), '<br>')}</p>" for par in re.split(r"\n\s*\n", (a.get("testo") or "").strip()) if par.strip())
    meta = " · ".join(filter(None, [esc(a.get("luogo") or ""), tr("pubblicato il", "veröffentlicht am", "published on", "publié le") + " " + data_l(a["date"][:10])]))
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
    oggetto = tr("Annuncio per il mercatino", "Inserat für den Marktplatz", "Listing for the gear market", "Annonce pour les petites annonces")
    mailto = f"mailto:{MERCATINO_MAIL}?subject={quote(oggetto)}&body={quote(MERCATINO_MODULO[LINGUA['lang']])}"
    bottone = f'<a class="btn btn--primary" href="{esc(mailto)}">{tr("Pubblica un annuncio", "Inserat aufgeben", "Post a listing", "Publier une annonce")} <span class="arrow" aria-hidden="true">→</span></a>'
    if annunci:
        filtri = "\n".join([f'<button type="button" data-filtro="" aria-pressed="true">{tr("Tutti", "Alle", "All", "Toutes")} <span class="num">{len(annunci)}</span></button>'] +
                           [f'<button type="button" data-filtro="{t.lower()}" aria-pressed="false">{tipo_l(t)} <span class="num">{conta[t]}</span></button>'
                            for t in mercatino_util.TIPI if conta[t]])
        elenco = f"""<div class="filtro" role="group" aria-label="{tr("Filtra per tipo di annuncio", "Nach Art filtern", "Filter by type", "Filtrer par type d’annonce")}" data-filtra="#annunci" data-uno="{tr("annuncio", "Inserat", "listing", "annonce")}" data-molti="{tr("annunci", "Inserate", "listings", "annonces")}" hidden>
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
       "<strong>There are no listings at the moment.</strong> Have some gear you no longer use, or looking for something? Send us your listing.",
       "<strong>Il n’y a pas d’annonces pour le moment.</strong> Vous avez du matériel que vous n’utilisez plus, ou vous cherchez quelque chose ? Envoyez-nous votre annonce.")}</p>
{bottone.replace("btn--primary", "btn--secondary")}
</div>"""
    mail = f'<a href="{esc(mailto)}">{MERCATINO_MAIL}</a>'
    mesi = mercatino_util.GIORNI_DEFAULT // 30
    rows = [(tr("Cosa", "Was", "What", "Quoi"), tr("Materiale e abbigliamento per la montagna, da vendere, cercare o regalare tra privati.",
                                         "Bergausrüstung und -bekleidung, die Private verkaufen, suchen oder verschenken.",
                                         "Mountain gear and clothing to sell, find or give away between private people.",
                                         "Matériel et vêtements de montagne à vendre, chercher ou donner entre particuliers.")),
            (tr("Come", "Wie", "How", "Comment"), tr(f"Scrivi a {mail} con tipo, titolo, prezzo, luogo, descrizione, il contatto da pubblicare e fino a 3 foto: la redazione lo mette online.",
                                        f"Schreiben Sie an {mail} mit Art, Titel, Preis, Ort, Beschreibung, dem zu veröffentlichenden Kontakt und bis zu 3 Fotos: Die Redaktion schaltet das Inserat auf.",
                                        f"Write to {mail} with type, title, price, place, description, the contact to publish and up to 3 photos: the editors put it online.",
                                        f"Écrivez à {mail} avec le type, le titre, le prix, le lieu, la description, le contact à publier et jusqu’à 3 photos : la rédaction la met en ligne.")),
            (tr("Durata", "Dauer", "Duration", "Durée"), tr(f"Ogni annuncio resta online {mesi} mesi. Se l’oggetto è venduto, trovato o regalato prima, avvisaci e lo togliamo.",
                                                  f"Jedes Inserat bleibt {mesi} Monate online. Ist der Gegenstand vorher verkauft, gefunden oder verschenkt, melden Sie es uns und wir entfernen es.",
                                                  f"Each listing stays online for {mesi} months. If the item is sold, found or given away sooner, let us know and we will remove it.",
                                                  f"Chaque annonce reste en ligne {mesi} mois. Si l’objet est vendu, trouvé ou donné avant, prévenez-nous et nous la retirons.")),
            (tr("Costo", "Kosten", "Cost", "Coût"), tr("Gratuito", "Gratis", "Free", "Gratuit")),
            (tr("Trattative", "Abwicklung", "Deals", "Transactions"), tr("Si accordano direttamente le persone interessate: la sezione pubblica gli annunci ma non partecipa alla vendita e non risponde del materiale.",
                                                         "Die Interessierten einigen sich direkt: Die Sektion veröffentlicht die Inserate, ist aber nicht am Verkauf beteiligt und haftet nicht für das Material.",
                                                         "The people concerned deal directly with each other: the section publishes the listings but takes no part in the sale and is not liable for the gear.",
                                                         "Les personnes intéressées s’arrangent directement : la section publie les annonces mais ne participe pas à la vente et ne répond pas du matériel."))]
    titolo = tr("Mercatino", "Marktplatz", "Gear market", "Petites annonces")
    body = page_hero([servizi_crumb(), (titolo, None)], titolo, tr(
                         "Attrezzatura di montagna tra soci e appassionati: vendo, cerco, regalo. Dai una seconda vita al materiale che non usi più.",
                         "Bergausrüstung unter Mitgliedern und Bergbegeisterten: verkaufen, suchen, verschenken. Die Inserate erscheinen so, wie sie geschrieben wurden, meist auf Italienisch.",
                         "Mountain gear between members and enthusiasts: for sale, wanted, free. Listings appear as they were written, mostly in Italian.",
                         "Matériel de montagne entre membres et passionnés : à vendre, recherché, à donner. Les annonces paraissent telles qu’elles ont été écrites, surtout en italien."),
                     f'<div class="actions hero-actions">{bottone}</div>') + f"""

<section class="section" aria-label="{tr("Annunci", "Inserate", "Listings", "Annonces")}">
<div class="container">
{elenco}
</div>
</section>

<section class="section--surface" id="come" aria-labelledby="come-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="come-h" class="h2">{tr("Come funziona", "So funktioniert’s", "How it works", "Comment ça marche")}</h2>
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
        "The SAC Ticino Section’s gear market: listings of mountain gear between private people, for sale, wanted or free.",
        "Les petites annonces du CAS Ticino : du matériel de montagne entre particuliers, à vendre, recherché ou à donner."), body)
