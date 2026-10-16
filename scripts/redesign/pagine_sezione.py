"""La Sezione: Chi siamo, Comitato, Organizzazione, Capigita, Soccorso, Sede e contatti, Storia, Mettiti in gioco."""
from html import escape as html_escape
from storia_oggetti import oggetto
from comune import *
from pagine_capanne import HUT_PAGES
from pagine_servizi import MERCATINO_MAIL, NOLEGGIO_MAIL
from pagine_home import tx_tradotte


def introduzione():
    huts = ('<a href="campotencia.html">Campo Tencia</a>, <a href="cristallina.html">Cristallina</a>, <a href="adula.html">Adula</a>, '
            '<a href="motterascio.html">Motterascio (Michela)</a>, <a href="montebar.html">Monte Bar</a> e <a href="baitadelluca.html">Baita del Luca</a>')
    body = page_hero([("La Sezione", "introduzione.html"), ("Chi siamo", None)], "La sezione",
                     "Fondata a Bellinzona l’11 aprile 1886, la Sezione Ticino del Club Alpino Svizzero conta quasi 3000 soci e propone un’attività varia, pensata per tutte le età: dai più giovani ai seniori.") + f"""

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
{img("paesaggi/sciatori-villaggio-2000", "Scialpinisti in salita verso un villaggio innevato", 2000, 901)}
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
    d = testi("soccorso")
    emergenza = [("Rega", f'<a class="num" href="tel:1414">1414</a> <span class="small">{tr("dall’estero", "aus dem Ausland", "from abroad")} <a class="num" href="tel:+41333333333">+41 333 333 333</a></span>'),
                 (tr("Ambulanza", "Sanität", "Ambulance"), '<a class="num" href="tel:144">144</a>'),
                 (tr("Emergenza europeo", "Europäischer Notruf", "European emergency number"), '<a class="num" href="tel:112">112</a>')]
    titolo = tr("Soccorso", "Bergrettung", "Mountain rescue")
    body = page_hero([sez_crumb(), (titolo, None)], titolo, testo_campo(d, "introduzione"),
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
<p>{testo_campo(d, "colonna")}</p>
</div>
<div class="prose" data-reveal>
{testo_md(d, "colonna_testo")}
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
    d = testi("sede")
    titolo = testo_campo(d, "titolo")
    rows = [(testo_campo(r, "etichetta"), testo_campo(r, "testo")) for r in d["righe"]]
    rows.append((tr("Coordinate bancarie", "Bankverbindung", "Bank details"), f'Banca Stato, Lugano<br><span class="num">IBAN {IBAN}</span>'))
    body = page_hero([sez_crumb(), (titolo, None)], titolo, testo_campo(d, "introduzione")) + f"""

<section class="section" aria-labelledby="sede-h">
<div class="container">
<div class="contact" data-reveal>
<div class="contact-intro">
<h2 id="sede-h" class="h2">{testo_campo(d, "sottotitolo")}</h2>
<p>{testo_campo(d, "testo")}</p>
<div><a class="btn btn--primary" href="mailto:info@casticino.ch">{tr("Scrivi alla sezione", "Der Sektion schreiben", "Write to the section")} <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
{facts(rows)}
</div>
</div>
</section>

{rubrica()}

{subnav(SEZ_MENU(), L("sede.html"))}"""
    return sezione_page("sede.html", f'{testo_campo(d, "titolo", semplice=True)} | CAS Ticino',
                        tr("Sede del CAS Ticino al Canvetto Luganese (Molino Nuovo), recapito postale, e-mail, biblioteca e coordinate bancarie.",
                           "Sitz des CAS Ticino im Canvetto Luganese (Molino Nuovo), Postadresse, E-Mail, Bibliothek und Bankverbindung.",
                           "The CAS Ticino office at the Canvetto Luganese (Molino Nuovo), postal address, e-mail, library and bank details."),
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
        body = page_hero([("Die Sektion", "de/introduzione.html"), ("Geschichte", None)], "Seit 1886 zu Fuss unterwegs.",
                         "Mehr als ein Jahrhundert Besteigungen, Hütten, Rettung und Bergkultur: die Geschichte der Sektion in Etappen.")
    elif en():
        body = page_hero([("The Section", "en/introduzione.html"), ("History", None)], "Since 1886, on foot.",
                         "More than a century of climbs, huts, rescue and mountain culture: the history of the section in milestones.")
    else:
        body = page_hero([("La Sezione", "introduzione.html"), ("Storia", None)], "Dal 1886, a piedi.",
                         "Più di un secolo di salite, rifugi, soccorso e cultura alpina: la storia della sezione in tappe.")
    body += f"""

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


def introduzione_tradotta():
    tx = tx_tradotte()
    lang = LINGUA["lang"]
    huts = (f'<a href="{lang}/campotencia.html">Campo Tencia</a>, <a href="{lang}/cristallina.html">Cristallina</a>, <a href="{lang}/adula.html">Adula</a>, '
            f'<a href="{lang}/motterascio.html">Motterascio (Michela)</a>, <a href="{lang}/montebar.html">Monte Bar</a> {tx["e"]} <a href="{lang}/baitadelluca.html">Baita del Luca</a>')
    stats = "\n".join(f'<div class="stat"><strong>{n}</strong><span>{num(x)}</span></div>'
                      for n, x in zip(("1886", "3000", "6", "5"), tx["stat_intro"]))
    body = page_hero([(tx["sezione"], f"{lang}/introduzione.html"), (tx["intro_crumb"], None)], tx["intro_h"], tx["intro_lead"]) + f"""

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
{img("paesaggi/sciatori-villaggio-2000", tx['alt_cresta'], 2000, 901)}
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


def volontariato():
    def mail(m, testo=None):
        return f'<a class="link" href="mailto:{m}">{testo or tr("Scrivi a", "Schreiben Sie an", "Write to")} {m}</a>'

    titolo = tr("Mettiti in gioco", "Mithelfen", "Get involved")
    body = page_hero([sez_crumb(), (titolo, None)], titolo, testo_campo(testi("introduzioni")["volontariato"], "introduzione")) + f"""

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
    body = body.replace('<section class="section"', '<section class="section section--fitta"')   # pagina lunga: meno spazio tra le sezioni
    return sezione_page("volontariato.html", titolo + " | CAS Ticino", tr(
        "Volontariato nel CAS Ticino: api operaie in capanna, capigita e aiuto-capigita, monitori G+S, capigita Senior, comunicazione ed eventi. Come cominciare.",
        "Freiwilligenarbeit in der SAC-Sektion Ticino: Arbeiten in den Hütten, Tourenleitung und Hilfsleitung, J+S-Leitende, Seniorentouren, Kommunikation und Anlässe. So fangen Sie an.",
        "Volunteering with the SAC Ticino Section: work in the huts, trip leaders and assistant leaders, Youth+Sport instructors, seniors’ trips, communication and events. How to start."),
        body, og="paesaggi/salita-prato-2000")
