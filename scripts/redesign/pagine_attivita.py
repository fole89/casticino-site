"""Attività: programma gite (copia da Droptour, gite.html e gita.html), Giovani, Senior, Corsi (CORSI), Partecipare
e il riquadro «Prima di partire»."""
from shared import GITE_DROPTOUR
from comune import *
from pagine_servizi import DOCS, DOCS_DE, DOCS_EN, DOCS_FR


# ------------------------------------------------------------------ programma gite (copia da Droptour)
# data/gite.json lo scrive scripts/update_gite.py; nella pagina assets/gite.js rilegge le gite in tempo reale
# dall'interfaccia pubblica di Droptour e le ridisegna con lo stesso markup di gita_html() (tenerli allineati).
GITE_ICS = "webcal://ssl.dropnet.ch/casticino/dropnetapps/tours/index.php?page=ics&amp;type=&amp;group=&amp;eventtype="
GITE_DETTAGLIO = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItem&language=it&item_id="
GITE_API = "https://ssl.dropnet.ch/casticino/dropnetapps/tours/api/?action=command&command=getItems&limit=500&language=it"
GIORNI_BREVI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
MESI_BREVI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
IMPEGNO = {"A": "poco impegnativo", "B": "abbastanza impegnativo", "C": "impegnativo", "D": "molto impegnativo"}
# Programma gite anche in de/, fr/ e en/: si traducono solo i testi della pagina; titoli, tipi e dettagli delle gite
# (da Droptour) restano in italiano. Gli stessi testi sono in assets/gite.js (TESTI): tenerli allineati.
GIORNI_BREVI_L = {"it": GIORNI_BREVI, "de": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
                  "fr": ["lun", "mar", "mer", "jeu", "ven", "sam", "dim"],
                  "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
MESI_BREVI_L = {"it": MESI_BREVI, "de": ["Jan.", "Feb.", "März", "Apr.", "Mai", "Juni", "Juli", "Aug.", "Sept.", "Okt.", "Nov.", "Dez."],
                "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
                "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
IMPEGNO_L = {"it": IMPEGNO, "de": {"A": "wenig anspruchsvoll", "B": "ziemlich anspruchsvoll", "C": "anspruchsvoll", "D": "sehr anspruchsvoll"},
             "fr": {"A": "peu exigeant", "B": "assez exigeant", "C": "exigeant", "D": "très exigeant"},
             "en": {"A": "easy", "B": "fairly demanding", "C": "demanding", "D": "very demanding"}}
GRUPPI_L = {"de": {"Tutti": "Alle", "Attivi": "Aktive", "Giovani": "Jugend", "Seniori": "Senioren", "Soccorso": "Bergrettung", "Monitori": "Leitende"},
            "fr": {"Tutti": "Tous", "Attivi": "Membres actifs", "Giovani": "Jeunesse", "Seniori": "Seniors", "Soccorso": "Secours en montagne", "Monitori": "Moniteurs"},
            "en": {"Tutti": "All", "Attivi": "Active members", "Giovani": "Youth", "Seniori": "Seniors", "Soccorso": "Mountain rescue", "Monitori": "Instructors"}}


# tipi di gita (category di Droptour, sempre in italiano) per codice; un codice nuovo resta in italiano.
# Tenere allineato con TIPI in assets/gite.js
TIPI_GITA_L = {"de": {"ALP": "Hochtour", "ARR": "Klettern", "COR": "Ausbildungskurs", "CUL": "Kultur", "ESC": "Wandern", "EVE": "Anlass",
                      "FER": "Klettersteig", "MTB": "Mountainbike", "RAC": "Schneeschuhtour", "SA": "Skitour", "SOC": "Bergrettung"},
               "fr": {"ALP": "Alpinisme", "ARR": "Escalade", "COR": "Cours de formation", "CUL": "Culture", "ESC": "Randonnée", "EVE": "Événement",
                      "FER": "Via ferrata", "MTB": "VTT", "RAC": "Raquettes", "SA": "Ski de randonnée", "SOC": "Secours en montagne"},
               "en": {"ALP": "Mountaineering", "ARR": "Climbing", "COR": "Training course", "CUL": "Culture", "ESC": "Hiking", "EVE": "Event",
                      "FER": "Via ferrata", "MTB": "Mountain biking", "RAC": "Snowshoeing", "SA": "Ski touring", "SOC": "Mountain rescue"}}


def nome_tipo(g):
    return TIPI_GITA_L.get(LINGUA["lang"], {}).get(g.get("sigla"), g["tipo"])


def nome_gruppo(x):
    return GRUPPI_L.get(LINGUA["lang"], {}).get(x, x)


def gite_dati():
    try:
        return json.load(open(os.path.join(ROOT, "data", "gite.json"), encoding="utf-8")).get("gite", [])
    except OSError:
        return []


def gita_stato(g, oggi):
    """(classe, testo) dello stato delle iscrizioni, calcolato come in gite.js."""
    if g["stato"] == "annullata":
        return "annullata", tr("Annullata", "Abgesagt", "Cancelled", "Annulée")
    if g["stato"] == "completa":
        return "completa", tr("Completa", "Ausgebucht", "Full", "Complète")
    if not g["iscrizione"]:
        return "", tr("Senza iscrizione online", "Ohne Online-Anmeldung", "No online registration", "Sans inscription en ligne")
    if g["iscrizione_dal"] and oggi < g["iscrizione_dal"]:
        b = data_breve(g["iscrizione_dal"])
        return "", tr(f"Iscrizioni dal {b}", f"Anmeldung ab {b}", f"Registration from {b}", f"Inscriptions dès le {b}")
    if g["iscrizione_al"] and oggi > g["iscrizione_al"]:
        return "", tr("Iscrizioni chiuse", "Anmeldung geschlossen", "Registration closed", "Inscriptions fermées")
    return "aperte", tr("Iscrizioni aperte", "Anmeldung offen", "Registration open", "Inscriptions ouvertes")


def fino_al(giorno):
    """«fino al 3», ma «fino all'1», «all'8», «all'11»."""
    return f"fino all’{giorno}" if giorno in (1, 8, 11) else f"fino al {giorno}"


def data_breve(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    mb = MESI_BREVI_L[LINGUA["lang"]][m - 1]
    return tr(f"{d} {mb}", f"{d}. {mb}", f"{d} {mb}", f"{d} {mb}")


def fino_data(d2):
    """Ultimo giorno di una gita che finisce il mese dopo: «fino all’1 nov», «bis 1. Nov.», «to 1 Nov»."""
    mb = MESI_BREVI_L[LINGUA["lang"]][d2.month - 1]
    return tr(f"{fino_al(d2.day)} {mb}", f"bis {d2.day}. {mb}", f"to {d2.day} {mb}", f"jusqu’au {d2.day} {mb}")


def gita_html(g, oggi):
    import datetime
    gb = GIORNI_BREVI_L[LINGUA["lang"]]
    d1 = datetime.date.fromisoformat(g["dal"])
    giorno, sotto = str(d1.day), gb[d1.weekday()]
    if g["al"] and g["al"] != g["dal"]:
        d2 = datetime.date.fromisoformat(g["al"])
        if d2.month == d1.month:
            giorno, sotto = f"{d1.day}–{d2.day}", f"{sotto}–{gb[d2.weekday()]}"
        else:
            sotto += f", {fino_data(d2)}"
    classe, stato = gita_stato(g, oggi)
    gruppi = [nome_gruppo(x) for x in g["gruppi"] if x != "Tutti"] or [nome_gruppo("Tutti")]
    tipo = " · ".join(dict.fromkeys(filter(None, [esc(nome_tipo(g)), esc(", ".join(gruppi))])))
    meta = []
    if g["cond"]:
        meta.append(f'<span title="{IMPEGNO_L[LINGUA["lang"]].get(g["cond"], "")}">{tr("Impegno", "Kondition", "Fitness", "Condition")} {esc(g["cond"])}</span>')
    if g["tecn"]:
        meta.append(f'<span>{tr("Difficoltà", "Technik", "Difficulty", "Difficulté")} {esc(g["tecn"])}</span>')
    if g["capigita"]:
        piu = len(g["capigita"]) > 1
        meta.append(f'<span>{tr("Capigita" if piu else "Capogita", "Leitung", "Leaders" if piu else "Leader", "Chefs de course" if piu else "Chef de course")}: {esc(", ".join(g["capigita"]))}</span>')
    iscritti = tr("iscritti", "Angemeldete", "registered", "inscrits")
    posti = (f'{g["iscritti"]}/{g["posti"]} {iscritti}' if g["posti"] else f'{g["iscritti"]} {iscritti}' if g["iscritti"] else "")
    modalita = (f'<span class="gita-nota">{tr("Iscrizione" + ("" if g["modalita"].startswith("tramite") else ":"), "Anmeldung:", "Registration:", "Inscription :")} {esc(g["modalita"])}</span>'
                if g["modalita"] and classe != "annullata" else "")
    dettagli = (tr("Dettagli", "Details", "Details", "Détails") if classe == "annullata" or not g["iscrizione"]
                else tr("Dettagli e iscrizione", "Details und Anmeldung", "Details and registration", "Détails et inscription"))
    link = L("gita.html") + f"?id={g['id']}"
    return f"""<article class="gita{' gita--annullata' if classe == 'annullata' else ''}" id="gita-{g['id']}" data-fine="{g['al'] or g['dal']}" data-gruppi="{esc(' '.join(g['gruppi']))}" data-tipo="{esc(g['sigla'])}">
<p class="gita-data"><span class="gita-giorno num">{giorno}</span><span class="gita-sotto">{sotto}</span></p>
<div class="gita-corpo">
<p class="gita-tipo">{tipo}</p>
<h3 class="gita-titolo"><a href="{link}"{'' if LINGUA["lang"] == "it" else ' lang="it"'}>{esc(g['titolo'])}</a></h3>
{f'<p class="gita-meta">{"".join(meta)}</p>' if meta else ""}
</div>
<div class="gita-stato">
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
{f'<span class="gita-posti num">{posti}</span>' if posti else ""}{modalita}
<a class="link gita-link" href="{link}">{dettagli}<span class="visually-hidden">: <span{'' if LINGUA["lang"] == "it" else ' lang="it"'}>{esc(g['titolo'])}</span></span></a>
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
            out.append(f'<section class="gite-mese" aria-labelledby="mese-{m}">\n<h2 id="mese-{m}" class="h3">{MESI_L[LINGUA["lang"]][mm - 1].capitalize()} {y}</h2>\n<div class="gite-righe">')
            mese = m
        out.append(gita_html(g, oggi))
    if mese:
        out.append("</div>\n</section>")
    return "\n".join(out)


def prossime_gite(n=10):
    """Le prossime gite per la home, in una fila che scorre: senza annullate e senza le serate della colonna di soccorso.
    La pagina può restare indietro di un giorno (si rigenera ogni mattina), quindi site.js toglie quelle già passate (data-fine)."""
    import datetime
    lang = LINGUA["lang"]
    oggi = datetime.date.today().isoformat()
    scelte = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi and g["stato"] != "annullata"
              and "colonna di soccorso" not in g["titolo"].lower()][:n]
    schede = []
    for g in scelte:
        d = datetime.date.fromisoformat(g["dal"])
        quando = f"{GIORNI_BREVI_L[lang][d.weekday()]} {MESI_L[lang][d.month - 1]}"
        if g["al"] and g["al"] != g["dal"]:
            d2 = datetime.date.fromisoformat(g["al"])
            quando += ", " + (fino_data(d2) if d2.month != d.month else tr(fino_al(d2.day), f"bis {d2.day}.", f"to {d2.day}", f"jusqu’au {d2.day}"))
        classe, stato = gita_stato(g, oggi)
        gruppi = [nome_gruppo(x) for x in g["gruppi"] if x != "Tutti"] or [nome_gruppo("Tutti")]
        tipo = " · ".join(dict.fromkeys(filter(None, [esc(nome_tipo(g)), esc(", ".join(gruppi))])))
        schede.append(f"""<a class="prossima" href="gita.html?id={g['id']}" data-fine="{g['al'] or g['dal']}">
<p class="prossima-data"><span class="prossima-giorno num">{d.day}</span><span>{quando}</span></p>
<p class="gita-tipo">{tipo}</p>
<h3 class="prossima-titolo"{in_it()}>{esc(g['titolo'])}</h3>
<span class="stato{' stato--' + classe if classe else ''}">{stato}</span>
</a>""")
    return "\n".join(schede)


def gite():
    import datetime
    oggi = datetime.date.today().isoformat()
    lista = [g for g in gite_dati() if (g["al"] or g["dal"]) >= oggi]
    it = LINGUA["lang"] == "it"
    nome = L("gite.html")
    su = "" if it else "../"  # data-copia non passa da pubblica()
    titolo = tr("Programma gite", "Tourenprogramm", "Trip programme", "Programme des courses")
    trail = [("Attività", "index.html#attivita"), (titolo, None)] if it else [(titolo, None)]
    body = page_hero(trail, titolo, tr(
        "Gite, corsi ed eventi della sezione, aggiornati in tempo reale dal portale Droptour, dove ci si iscrive.",
        "Touren, Kurse und Anlässe der Sektion, laufend aktualisiert aus dem Portal Droptour, wo man sich anmeldet. Titel und Beschreibungen der Touren sind auf Italienisch.",
        "Trips, courses and events of the section, updated live from the Droptour portal, where you register. Trip titles and descriptions are in Italian.",
        "Courses, cours et événements de la section, mis à jour en temps réel depuis le portail Droptour, où l’on s’inscrit. Les titres et descriptions des courses sont en italien.")) + f"""

<section class="section" aria-label="{tr("Elenco delle gite", "Liste der Touren", "List of trips", "Liste des courses")}">
<div class="container">
<div class="gite-filtri" id="gite-filtri" hidden>
<div class="filtro" role="group" aria-label="{tr("Filtra per gruppo", "Nach Gruppe filtern", "Filter by group", "Filtrer par groupe")}" data-campo="gruppi"></div>
<div class="filtro" role="group" aria-label="{tr("Filtra per tipo", "Nach Art filtern", "Filter by type", "Filtrer par type")}" data-campo="tipo"></div>
<div class="filtri-tendina">
<label><span class="label">{tr("Gruppo", "Gruppe", "Group", "Groupe")}</span><select data-campo="gruppi"></select></label>
<label><span class="label">{tr("Tipo", "Art", "Type", "Type")}</span><select data-campo="tipo"></select></label>
</div>
</div>
<p class="small filtro-stato" id="gite-stato" aria-live="polite"></p>
<div class="gite" id="gite" data-api="{GITE_API}" data-copia="{su}{asset('data/gite.json')}">
{gite_lista(lista, oggi) if lista else '<p>' + tr("Il programma non è disponibile in questo momento: lo trovi su", "Das Programm ist im Moment nicht verfügbar: Sie finden es auf", "The programme is not available at the moment: you can find it on", "Le programme n’est pas disponible pour le moment : vous le trouverez sur") + ' <a href="' + GITE_DROPTOUR + '">Droptour</a>.</p>'}
</div>
<div class="callout">
<p>{tr("Le iscrizioni, l’accesso per soci e capigita e i dettagli di ogni gita sono sul portale Droptour. Per le domande su una gita scrivi al capogita, dalla pagina della gita.",
       "Anmeldungen, Zugang für Mitglieder und Tourenleitende und alle Details zu jeder Tour finden Sie auf dem Portal Droptour (italienisch). Fragen zu einer Tour richten Sie an die Tourenleitung, über die Seite der Tour.",
       "Registration, access for members and trip leaders and the details of every trip are on the Droptour portal (in Italian). For questions about a trip, write to the trip leader from the trip’s page.",
       "Les inscriptions, l’accès pour les membres et les chefs de course et les détails de chaque course sont sur le portail Droptour (en italien). Pour toute question sur une course, écrivez au chef de course depuis la page de la course.")}</p>
<div class="actions"><a class="btn btn--secondary" href="{GITE_DROPTOUR}" rel="noopener">{tr("Programma completo su Droptour", "Ganzes Programm auf Droptour", "Full programme on Droptour", "Programme complet sur Droptour")}</a><a class="btn btn--secondary" href="{GITE_ICS}">{tr("Calendario (iCal)", "Kalender (iCal)", "Calendar (iCal)", "Calendrier (iCal)")}</a>{'<a class="btn btn--secondary" href="partecipare.html">Come partecipare</a>' if it else ""}<a class="btn btn--secondary" href="documenti.html">{tr("Scale di difficoltà", "Schwierigkeitsskalen (italienisch)", "Difficulty scales (in Italian)", "Échelles de difficulté (en italien)")}</a></div>
</div>
</div>
</section>

{prima_di_partire()}
{subnav("Attività", "gite.html") if it else ""}"""
    return pubblica(nome, page(nome, f"{titolo} | CAS Ticino", tr(
        "Il programma delle gite, dei corsi e degli eventi della Sezione Ticino del Club Alpino Svizzero, con le iscrizioni su Droptour.",
        "Das Programm der Touren, Kurse und Anlässe der Sektion Ticino des Schweizer Alpen-Clubs, mit Anmeldung auf Droptour.",
        "The programme of trips, courses and events of the Ticino Section of the Swiss Alpine Club, with registration on Droptour.",
        "Le programme des courses, des cours et des événements de la Section Ticino du Club Alpin Suisse, avec inscription sur Droptour."),
        body, og="attivita/gite-2x1", section="Attività" if it else None, scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n'))


def gita_pagina():
    """Dettaglio di una gita: gita.html?id=<numero Droptour>, riempita da gite.js (dati in tempo reale da Droptour)."""
    it = LINGUA["lang"] == "it"
    nome = L("gita.html")
    su = "" if it else "../"
    programma = tr("Programma gite", "Tourenprogramm", "Trip programme", "Programme des courses")
    gita = tr("Gita", "Tour", "Trip", "Course")
    trail = ([("Attività", "index.html#attivita")] if it else []) + [(programma, L("gite.html")), (gita, None)]
    body = page_hero(trail, gita, tr("Caricamento della gita…", "Tour wird geladen…", "Loading the trip…", "Chargement de la course…")
                     ).replace('class="display fit"', 'class="display display--gita fit"') + f"""

<section class="section" aria-label="{tr("Dettagli della gita", "Details der Tour", "Trip details", "Détails de la course")}">
<div class="container detail gita-dettaglio" id="gita" data-api="{GITE_API}" data-dettaglio="{GITE_DETTAGLIO}"
 data-droptour="{GITE_DROPTOUR}" data-copia="{su}{asset('data/gite.json')}" data-programma="{L('gite.html')}">
<aside class="gita-riepilogo" aria-label="{tr("La gita in breve", "Die Tour in Kürze", "The trip at a glance", "La course en bref")}" hidden>
<p id="gita-stato"></p>
<dl class="gita-chiave" id="gita-chiave"></dl>
<div class="actions" id="gita-azioni"></div>
</aside>
<div id="gita-dati"><noscript><p>{tr("Per vedere la gita serve JavaScript: la trovi nel", "Um die Tour zu sehen, braucht es JavaScript; Sie finden sie im", "JavaScript is needed to see the trip; you can find it in the", "JavaScript est nécessaire pour afficher la course ; vous la trouverez dans le")} <a href="{GITE_DROPTOUR}">{tr("programma su Droptour", "Programm auf Droptour", "programme on Droptour", "programme sur Droptour")}</a>.</p></noscript></div>
</div>
</section>
{subnav("Attività", "gita.html") if it else ""}"""
    return pubblica(nome, page(nome, f"{gita} | CAS Ticino", tr(
        "Dettagli di una gita della Sezione Ticino del CAS, con l’iscrizione su Droptour.",
        "Details einer Tour der Sektion Ticino des SAC, mit Anmeldung auf Droptour.",
        "Details of a trip of the Ticino Section of the SAC, with registration on Droptour.",
        "Détails d’une course de la Section Ticino du CAS, avec inscription sur Droptour."),
        body, og="attivita/gite-2x1", section="Attività" if it else None, scripts=f'<script src="{asset("assets/gite.js")}" defer></script>\n'))


# ------------------------------------------------------------------ giovani, senior, corsi

def giovani():
    groups = [("2-10", tr("Giovanissimi e famiglie", "Die Jüngsten und Familien", "Youngest and families", "Plus jeunes et familles"),
               tr("Arrampicata in famiglia: i bambini imparano a muoversi in corda, gli adulti ad assicurare.",
                  "Klettern mit der Familie: Die Kinder lernen, sich am Seil zu bewegen, die Erwachsenen das Sichern.",
                  "Family climbing: children learn to move on the rope, adults learn to belay.",
                  "Escalade en famille : les enfants apprennent à évoluer encordés, les adultes à assurer.")),
              ("9-14", "Spider", tr("Arrampicata, nevai, lettura della carta e scoperta della natura, tra gioco, divertimento e spirito di gruppo.",
                                    "Klettern, Schneefelder, Kartenlesen und Naturentdeckung, mit Spiel, Spass und Teamgeist.",
                                    "Climbing, snowfields, map reading and discovering nature, with games, fun and team spirit.",
                                    "Escalade, névés, lecture de carte et découverte de la nature, entre jeu, plaisir et esprit d’équipe.")),
              ("13-17", "Junior", tr("D’inverno sci alpinismo e splitboard, d’estate creste e arrampicata: prima il divertimento e la sicurezza, poi l’autonomia.",
                                     "Im Winter Skitouren und Splitboard, im Sommer Grate und Klettern: zuerst Spass und Sicherheit, dann Selbständigkeit.",
                                     "Ski touring and splitboarding in winter, ridges and climbing in summer: fun and safety first, then independence.",
                                     "En hiver ski de randonnée et splitboard, en été arêtes et escalade : d’abord le plaisir et la sécurité, ensuite l’autonomie.")),
              ("16-25", "OG", tr("Sci alpinismo impegnativo, cascate di ghiaccio e arrampicata tecnica in tutto l’arco alpino. Chi vuole può formarsi come monitore.",
                                 "Anspruchsvolle Skitouren, Eisfälle und technisches Klettern im ganzen Alpenbogen. Wer will, kann sich zur Leiterin oder zum Leiter ausbilden.",
                                 "Demanding ski touring, ice falls and technical climbing across the Alps. Those who wish can train as instructors.",
                                 "Ski de randonnée exigeant, cascades de glace et escalade technique dans tout l’arc alpin. Qui le souhaite peut se former comme moniteur."))]
    anni = tr("anni", "Jahre", "years", "ans")
    cards = "\n".join(f"""<article class="group">
<div class="age">{a}<span>{anni}</span></div>
<h3 class="h3">{t_}</h3>
<p>{p}</p>
</article>""" for a, t_, p in groups)
    rows = [(tr("Iscrizione", "Anmeldung", "Registration", "Inscription"), tr(
                "Su Droptour, almeno due settimane prima per le singole attività, oppure dal coordinatore per iscrizioni a blocchi.",
                "Auf Droptour, mindestens zwei Wochen im Voraus für einzelne Aktivitäten, oder beim Koordinator für Blockanmeldungen.",
                "On Droptour, at least two weeks in advance for single activities, or through the coordinator for block registrations.",
                "Sur Droptour, au moins deux semaines avant pour les activités isolées, ou auprès du coordinateur pour les inscriptions en bloc.")),
            (tr("Requisiti", "Voraussetzungen", "Requirements", "Conditions"), tr(
                'Serve essere soci del CAS Ticino, tranne per le uscite di prova. <a href="adesione.html">Diventa socio</a>',
                'Mitgliedschaft bei der SAC-Sektion Ticino, ausser für Schnuppertouren. <a href="adesione.html">Mitglied werden</a>',
                'Membership of the SAC Ticino Section, except for trial outings. <a href="adesione.html">Become a member</a>',
                "Il faut être membre du CAS Ticino, sauf pour les sorties d’essai. <a href=\"adesione.html\">Devenir membre</a>")),
            (tr("Costi", "Kosten", "Costs", "Coûts"), tr(
                "Coprono vitto e alloggio a mezza pensione, guida e trasporto in furgone. Dai 21 ai 25 anni si aggiungono CHF 30 al giorno, perché non ci sono contributi G+S.",
                "Sie decken Unterkunft mit Halbpension, Bergführer und Transport im Kleinbus. Von 21 bis 25 Jahren kommen CHF 30 pro Tag dazu, weil es keine J+S-Beiträge gibt.",
                "They cover half-board food and lodging, guide and minibus transport. From 21 to 25, CHF 30 a day is added, as there are no Youth+Sport contributions.",
                "Ils couvrent la demi-pension, le guide et le transport en minibus. De 21 à 25 ans, CHF 30 par jour s’ajoutent, car il n’y a pas de contributions J+S.")),
            (tr("Inclusione", "Inklusion", "Inclusion", "Inclusion"), tr(
                "Ragazze e ragazzi con disabilità fisica o psichica sono i benvenuti: contatta il coordinatore per trovare insieme la soluzione giusta.",
                "Mädchen und Jungen mit körperlicher oder psychischer Beeinträchtigung sind willkommen: Kontaktieren Sie den Koordinator, um gemeinsam die richtige Lösung zu finden.",
                "Girls and boys with physical or mental disabilities are welcome: contact the coordinator to find the right solution together.",
                "Les filles et garçons avec un handicap physique ou psychique sont les bienvenus : contactez le coordinateur pour trouver ensemble la bonne solution.")),
            (tr("Coordinatore", "Koordinator", "Coordinator", "Coordinateur"), 'Diego Romelli, <a class="num" href="tel:+393485731549">+39 348 573 1549</a>'),
            (tr("Cassiere", "Kassier", "Treasurer", "Caissier"), 'Nicola Martinoni, <a class="num" href="tel:+41794391691">+41 79 439 16 91</a>'),
            ("Spider", "Giosiana Codoni")]
    titolo = tr("Giovani", "Jugend", "Youth", "Jeunesse")
    programma = tr("Programma giovani", "Jugendprogramm", "Youth programme", "Programme jeunesse")
    body = page_hero([att_crumb(), (titolo, None)], titolo, testo_campo(testi("introduzioni")["giovani"], "introduzione"),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{GITE_GIOVANI}">{programma} <span class="arrow" aria-hidden="true">→</span></a></div>',
                     figure=img("attivita/giovani-3x4", tr("Giovane arrampicatore su una parete dei Denti della Vecchia", "Junger Kletterer an einer Wand der Denti della Vecchia", "Young climber on a face of the Denti della Vecchia", "Jeune grimpeur sur une paroi des Denti della Vecchia"), 800, 1066, lazy=False)
                     .replace("<img ", '<img class="orizzontale alto" ', 1)) + f"""

<section class="section" aria-labelledby="fasce-h">
<div class="container">
<div class="section-head"><h2 id="fasce-h" class="h2">{tr("Quattro fasce d’età", "Vier Altersgruppen", "Four age groups", "Quatre tranches d’âge")}</h2></div>
<div class="groups" data-reveal>
{cards}
</div>
</div>
</section>

<section class="section--surface" aria-labelledby="iscr-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="iscr-h" class="h2">{tr("Iscrizioni<br>e costi", "Anmeldung<br>und Kosten", "Registration<br>and costs", "Inscriptions<br>et coûts")}</h2>
<div><a class="link" href="{GITE_GIOVANI}">{programma}</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav(ATT_MENU(), L("giovani.html"))}"""
    return sezione_page("giovani.html", titolo + " | CAS Ticino", tr(
        "Il gruppo giovani del CAS Ticino: arrampicata, sci alpinismo, campi e uscite per ragazze e ragazzi dai 2 ai 25 anni, con monitori e guide alpine.",
        "Die Jugendgruppe der SAC-Sektion Ticino: Klettern, Skitouren, Lager und Touren für Mädchen und Jungen von 2 bis 25 Jahren, mit Leitenden und Bergführern.",
        "The SAC Ticino Section’s youth group: climbing, ski touring, camps and outings for girls and boys aged 2 to 25, with instructors and mountain guides.",
        "Le groupe jeunesse du CAS Ticino : escalade, ski de randonnée, camps et sorties pour filles et garçons de 2 à 25 ans, avec moniteurs et guides de montagne."),
        body, og="attivita/giovani-3x4")


def senior():
    mail = '<a href="mailto:senior@casticino.ch">senior@casticino.ch</a>'
    tel = ('<a class="num" href="tel:+41763973390">+41 76 397 33 90</a>', '<a class="num" href="tel:+41919721010">+41 91 972 10 10</a>')
    rows = [(tr("Chi può partecipare", "Wer mitmachen kann", "Who can join", "Qui peut participer"), tr(
                'Dai 60 anni, con l’affiliazione al CAS Ticino. Non c’è una tassa aggiuntiva, e tutti i soci della sezione possono partecipare alle attività. <a href="adesione.html">Diventa socio</a>',
                'Ab 60 Jahren, mit Mitgliedschaft bei der SAC-Sektion Ticino. Es gibt keinen Zusatzbeitrag, und alle Mitglieder der Sektion können an den Aktivitäten teilnehmen. <a href="adesione.html">Mitglied werden</a>',
                'From age 60, with membership of the SAC Ticino Section. There is no extra fee, and all the section’s members can take part in the activities. <a href="adesione.html">Become a member</a>',
                "Dès 60 ans, avec l’affiliation au CAS Ticino. Il n’y a pas de cotisation supplémentaire, et tous les membres de la section peuvent participer aux activités. <a href=\"adesione.html\">Devenir membre</a>")),
            (tr("Come aderire", "Beitritt", "How to join", "Comment adhérer"), tr(
                f"Scrivi a {mail} con nome, data di nascita, numero di socio CAS, indirizzo, telefono ed e-mail.",
                f"Schreiben Sie an {mail} mit Name, Geburtsdatum, SAC-Mitgliedernummer, Adresse, Telefon und E-Mail.",
                f"Write to {mail} with your name, date of birth, SAC membership number, address, phone and e-mail.",
                f"Écrivez à {mail} avec votre nom, date de naissance, numéro de membre CAS, adresse, téléphone et e-mail.")),
            (tr("Uscite", "Touren", "Outings", "Sorties"), tr(
                "Di norma il giovedì. Il calendario aggiornato è sul programma gite online.",
                "In der Regel am Donnerstag. Der aktuelle Kalender steht im Online-Tourenprogramm.",
                "Usually on Thursdays. The up-to-date calendar is in the online trip programme.",
                "En principe le jeudi. Le calendrier à jour se trouve dans le programme des courses en ligne.")),
            (tr("Pranzi", "Mittagessen", "Lunches", "Repas"), tr(
                f"Il secondo e il quarto mercoledì del mese al Bistrot Vecchio Torchio di Viganello. Iscrizioni entro il lunedì presso Hanni Vanossi ({tel[0]}) o direttamente al ristorante ({tel[1]}).",
                f"Am zweiten und vierten Mittwoch im Monat im Bistrot Vecchio Torchio in Viganello. Anmeldung bis Montag bei Hanni Vanossi ({tel[0]}) oder direkt im Restaurant ({tel[1]}).",
                f"On the second and fourth Wednesday of the month at the Bistrot Vecchio Torchio in Viganello. Book by Monday with Hanni Vanossi ({tel[0]}) or directly with the restaurant ({tel[1]}).",
                f"Le deuxième et le quatrième mercredi du mois au Bistrot Vecchio Torchio de Viganello. Inscriptions jusqu’au lundi auprès de Hanni Vanossi ({tel[0]}) ou directement au restaurant ({tel[1]}).")),
            (tr("Capigita", "Tourenleitende", "Trip leaders", "Chefs de course"), tr(
                "Il dicastero cerca sempre nuovi capigita.", "Das Ressort sucht immer neue Tourenleitende.", "The department is always looking for new trip leaders.", "Le département cherche toujours de nouveaux chefs de course."))]
    titolo = tr("Senior", "Senioren", "Seniors", "Seniors")
    programma = tr("Programma senior", "Seniorenprogramm", "Seniors’ programme", "Programme seniors")
    # come Giovani: foto a lato del titolo (taglio 4:3 di senior-2x1, il gruppo sta a sinistra)
    body = page_hero([att_crumb(), (titolo, None)], titolo, testo_campo(testi("introduzioni")["senior"], "introduzione"),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{GITE_SENIORI}">{programma} <span class="arrow" aria-hidden="true">→</span></a></div>',
                     figure=img("attivita/senior-4x3", tr("Escursionisti del gruppo senior su un sentiero di cresta", "Wandernde der Seniorengruppe auf einem Gratweg", "Hikers from the seniors group on a ridge path", "Randonneurs du groupe seniors sur un sentier de crête"), 667, 500, lazy=False)
                     .replace("<img ", '<img class="orizzontale" ', 1)) + f"""

<section class="section" aria-labelledby="gruppo-h">
<div class="container detail">
<div class="detail-intro split-intro">
<span class="label">{tr("Il gruppo, dal 1940", "Die Gruppe, seit 1940", "The group, since 1940", "Le groupe, depuis 1940")}</span>
<h2 id="gruppo-h" class="h2">{tr("Ogni giovedì<br>in cammino", "Jeden Donnerstag<br>unterwegs", "On the trail<br>every Thursday", "Chaque jeudi<br>en chemin")}</h2>
<p>{tr("Escursioni, gite di più giorni, mountain bike e racchette, con percorsi adatti a diversi livelli di allenamento.",
       "Wanderungen, mehrtägige Touren, Mountainbike und Schneeschuhe, auf Routen für verschiedene Trainingsstände.",
       "Hikes, trips of several days, mountain biking and snowshoeing, on routes suited to different levels of fitness.",
       "Randonnées, courses de plusieurs jours, VTT et raquettes, avec des itinéraires adaptés à différents niveaux d’entraînement.")}</p>
<div><a class="link" href="{GITE_SENIORI}">{programma}</a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>

{subnav(ATT_MENU(), L("senior.html"))}"""
    return sezione_page("senior.html", titolo + " | CAS Ticino", tr(
        "Il gruppo senior del CAS Ticino, dal 1940: escursioni il giovedì, gite di più giorni, mountain bike e racchette per soci dai 60 anni.",
        "Die Seniorengruppe der SAC-Sektion Ticino, seit 1940: Wanderungen am Donnerstag, mehrtägige Touren, Mountainbike und Schneeschuhe für Mitglieder ab 60.",
        "The SAC Ticino Section’s seniors group, since 1940: Thursday hikes, trips of several days, mountain biking and snowshoeing for members aged 60 and over.",
        "Le groupe seniors du CAS Ticino, depuis 1940 : randonnées le jeudi, courses de plusieurs jours, VTT et raquettes pour les membres dès 60 ans."),
        body, og="attivita/senior-2x1")


CORSO_SLUG = {"Alpinismo": "alpinismo", "Sci alpinismo": "scialpinismo", "Arrampicata": "arrampicata",
              "Tecnica di sci fuori pista": "fuoripista", "Freeride": "fuoripista", "Racchette": "racchette"}

def pdf_corso(cartella, file, testo):
    """Link a un PDF del corso in docs/corsi/<cartella>/ (in italiano)."""
    return f'<a href="{DOC}corsi/{cartella}/{file}.pdf">{testo} ({tr("PDF", "PDF, italienisch", "PDF, in Italian", "PDF, en italien")})</a>'


def schede_corso(c, x):
    """Le cinque righe di ogni corso: struttura, materiale e programma rimandano ai PDF in docs/corsi/<c>/
    (il link al programma compare solo quando c'è il PDF dell'anno)."""
    prog = x["programma"]
    if os.path.exists(os.path.join(ROOT, "docs", "corsi", c, "programma-2027.pdf")):
        prog += " " + pdf_corso(c, "programma-2027", tr("Programma 2027", "Programm 2027", "Programme 2027", "Programme 2027"))
    return [(tr("Struttura", "Aufbau", "Structure", "Structure"), f'{x["struttura"]} {pdf_corso(c, "obiettivi", tr("Obiettivi del corso", "Kursziele", "Course objectives", "Objectifs du cours"))}'),
            (tr("Requisiti", "Voraussetzungen", "Requirements", "Conditions"), x["requisiti"]),
            (tr("Partecipanti", "Teilnehmende", "Participants", "Participants"), x["partecipanti"]),
            (tr("Materiale", "Material", "Equipment", "Matériel"), f'{x["materiale"]} {pdf_corso(c, "materiale", tr("Lista del materiale", "Materialliste", "Equipment list", "Liste du matériel"))}'),
            (tr("Programma", "Programm", "Programme", "Programme"), prog)]


CORSI = [
    dict(stagione="Estate", titolo="Alpinismo", cartella="alpinismo", img="corsi/alpinismo-4x5", dim=(594, 742), alt="Cordata su una cresta di neve",
         testo="Il ponte tra escursionismo e alpinismo: legarsi correttamente su ghiacciaio e in cresta, tecniche di assicurazione, uso della corda in arrampicata e dei diversi attrezzi di progressione. Teoria e pratica, con lettura della carta, pianificazione, primo soccorso e salite in vetta su roccia e ghiaccio.",
         struttura="Sette giorni in tre uscite: tre giorni alla Capanna Piansecco, in Valle Bedretto, per nodi, corda, ramponi e piccozza; un fine settimana tra il granito del Furka e il ghiacciaio del Rodano; uno al Passo del Susten, con una gita alpinistica finale. Alla fine si partecipa da secondi di cordata a gite fino al grado PD+/III.",
         requisiti="Discreta condizione fisica: 4-5 ore di cammino con uno zaino di circa 10 kg, a 350-400 m di dislivello all’ora. Esperienza escursionistica, nessuna vertigine, età minima 16 anni (con il consenso dei genitori).",
         partecipanti="Iscrizioni online dal 1° dicembre 2026. Numero di posti limitato per ragioni di sicurezza (in definizione); precedenza in ordine d’iscrizione e ai soci CAS, poi lista d’attesa. L’iscrizione è definitiva con il pagamento della quota. Serata di presentazione e uscite obbligatorie, con qualsiasi tempo.",
         materiale="L’equipaggiamento personale spetta al partecipante; il materiale tecnico lo presta il CAS a chi non ce l’ha. Alla serata di presentazione si vede cosa serve: meglio aspettarla prima di comprare.",
         programma="Serata di presentazione il 12 marzo 2027 a Bellinzona; uscite il 28-30 maggio, il 12-13 giugno e il 3-4 luglio 2027. CHF 700 per i soci, 800 per i non soci, 450 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing escluse.",
         de=dict(titolo="Hochtouren", alt="Seilschaft auf einem Schneegrat",
                 testo="Die Brücke zwischen Wandern und Hochtouren: sich auf Gletscher und Grat richtig anseilen, Sicherungstechniken, Seilhandhabung beim Klettern und der Gebrauch der verschiedenen Geräte. Theorie und Praxis, mit Kartenlesen, Planung, Erster Hilfe und Gipfelbesteigungen auf Fels und Eis.",
                 struttura="Sieben Tage in drei Blöcken: drei Tage in der Capanna Piansecco im Bedrettotal für Knoten, Seil, Steigeisen und Pickel; ein Wochenende zwischen dem Granit der Furka und dem Rhonegletscher; eines am Sustenpass, mit einer abschliessenden Hochtour. Danach nimmt man als Seilzweite oder Seilzweiter an Touren bis zum Grad ZS+/III teil.",
                 requisiti="Gute Kondition: 4–5 Stunden Gehzeit mit einem Rucksack von etwa 10 kg, bei 350–400 Höhenmetern pro Stunde. Wandererfahrung, schwindelfrei, Mindestalter 16 Jahre (mit Einverständnis der Eltern).",
                 partecipanti="Online-Anmeldung ab 1. Dezember 2026. Aus Sicherheitsgründen beschränkte Platzzahl (noch offen); Vorrang nach Anmeldeeingang und für SAC-Mitglieder, danach Warteliste. Die Anmeldung ist mit der Bezahlung definitiv. Informationsabend und Kurstage obligatorisch, bei jedem Wetter.",
                 materiale="Die persönliche Ausrüstung bringen die Teilnehmenden selbst mit; technisches Material leiht der SAC allen, die keines haben. Am Informationsabend sieht man, was es braucht: Am besten erst danach einkaufen.",
                 programma="Informationsabend am 12. März 2027 in Bellinzona; Kurstage 28.–30. Mai, 12.–13. Juni und 3.–4. Juli 2027. CHF 700 für Mitglieder, 800 für Nichtmitglieder, 450 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften nicht inbegriffen."),
         fr=dict(titolo="Alpinisme", alt="Cordée sur une arête de neige",
                 testo="Le pont entre randonnée et alpinisme : s’encorder correctement sur glacier et en arête, techniques d’assurage, usage de la corde en escalade et des différents outils de progression. Théorie et pratique, avec lecture de carte, planification, premiers secours et ascensions de sommets sur rocher et glace.",
                 struttura="Sept jours en trois sorties : trois jours à la Capanna Piansecco, dans le Val Bedretto, pour les nœuds, la corde, les crampons et le piolet ; un week-end entre le granit de la Furka et le glacier du Rhône ; un autre au col du Susten, avec une course d’alpinisme finale. À la fin, on participe comme second de cordée à des courses jusqu’au degré PD+/III.",
                 requisiti="Bonne condition physique : 4-5 heures de marche avec un sac d’environ 10 kg, à 350-400 m de dénivelé à l’heure. Expérience de la randonnée, pas de vertige, âge minimum 16 ans (avec l’accord des parents).",
                 partecipanti="Inscriptions en ligne dès le 1er décembre 2026. Nombre de places limité pour des raisons de sécurité (à définir) ; priorité dans l’ordre d’inscription et aux membres du CAS, puis liste d’attente. L’inscription est définitive avec le paiement de la finance. Soirée de présentation et sorties obligatoires, par tous les temps.",
                 materiale="L’équipement personnel est à la charge du participant ; le CAS prête le matériel technique à qui n’en a pas. La soirée de présentation montre ce qu’il faut : mieux vaut l’attendre avant d’acheter.",
                 programma="Soirée de présentation le 12 mars 2027 à Bellinzona ; sorties les 28-30 mai, 12-13 juin et 3-4 juillet 2027. CHF 700 pour les membres, 800 pour les non-membres, 450 pour les jeunes OJ jusqu’à 20 ans et les membres étudiants de 21 à 25 ans ; déplacements en covoiturage non compris."),
         en=dict(titolo="Mountaineering", alt="Rope team on a snow ridge",
                 testo="The bridge between hiking and mountaineering: roping up correctly on glaciers and ridges, belaying techniques, rope work when climbing and the use of the various tools. Theory and practice, with map reading, planning, first aid and summit climbs on rock and ice.",
                 struttura="Seven days in three sessions: three days at Capanna Piansecco in Valle Bedretto for knots, rope, crampons and ice axe; a weekend between the Furka granite and the Rhone glacier; one at the Susten Pass, with a final mountaineering tour. Afterwards you can take part as a second on the rope in tours up to grade PD+/III.",
                 requisiti="Reasonable fitness: 4–5 hours’ walking with a pack of about 10 kg, at 350–400 m of ascent per hour. Hiking experience, no fear of heights, minimum age 16 (with parental consent).",
                 partecipanti="Online registration from 1 December 2026. Places limited for safety reasons (number to be confirmed); priority in order of registration and to SAC members, then a waiting list. Registration is final once the fee is paid. The presentation evening and outings are compulsory, whatever the weather.",
                 materiale="Personal equipment is the participant’s responsibility; the SAC lends technical gear to those who don’t have it. The presentation evening covers what you need: best wait for it before buying.",
                 programma="Presentation evening on 12 March 2027 in Bellinzona; outings on 28–30 May, 12–13 June and 3–4 July 2027. CHF 700 for members, 800 for non-members, 450 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel not included.")),
    dict(stagione="Inverno", titolo="Sci alpinismo", cartella="sci-alpinismo", img="corsi/scialpinismo-4x5", dim=(582, 728), alt="Sci alpinisti in salita su un pendio innevato",
         testo="Per muoversi in sicurezza e in autonomia nelle gite della sezione: salita con le pelli su pendii ripidi, discesa fuori pista, uso del materiale di sicurezza, valutazione del pericolo valanghe e pianificazione.",
         struttura="Sette giorni: una giornata introduttiva ad Airolo per verificare forma e tecnica, una serata di teoria su neve, ARTVA e autosoccorso, poi tre fine settimana alla Capanna Piansecco, all’Hotel Tiefenbach sul Furka e alla Camona da Maighels, con istruzione e gite fino a 800-1200 m di dislivello.",
         requisiti="Sciare bene su piste nere e reggere una gita di 1200 m di dislivello con uno zaino di 5 kg in al massimo 4 ore. Età minima 16 anni. Aperto anche agli snowboarder con splitboard. Chi dopo la giornata introduttiva non risulta idoneo riceve l’80% della quota.",
         partecipanti="Al massimo 30. Iscrizioni dal 1° ottobre al 1° dicembre 2026, o fino a esaurimento dei posti; la quota va versata entro il 10 dicembre. Uscite obbligatorie, con qualsiasi tempo; assenze e ritiri non danno diritto a rimborsi.",
         materiale="Attrezzatura completa da sci alpinismo. ARTVA, pala e sonda prestati su richiesta, compresi nella quota.",
         programma="Presentazione il 3 dicembre 2026 (anche via Teams); giornata introduttiva il 9 gennaio, teoria il 12 gennaio, uscite il 16-17 gennaio, il 20-21 febbraio e il 6-7 marzo 2027. CHF 650 per i soci, 750 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (circa CHF 100) escluse.",
         de=dict(titolo="Skitouren", alt="Skitourengeher im Aufstieg an einem verschneiten Hang",
                 testo="Um sich auf den Touren der Sektion sicher und selbständig zu bewegen: Aufstieg mit Fellen an steilen Hängen, Abfahrt abseits der Piste, Umgang mit dem Sicherheitsmaterial, Beurteilung der Lawinengefahr und Planung.",
                 struttura="Sieben Tage: ein Einführungstag in Airolo, um Form und Technik zu prüfen, ein Theorieabend über Schnee, LVS und Kameradenrettung, dann drei Wochenenden in der Capanna Piansecco, im Hotel Tiefenbach an der Furka und in der Camona da Maighels, mit Ausbildung und Touren bis 800–1200 Höhenmeter.",
                 requisiti="Sicheres Skifahren auf schwarzen Pisten und eine Tour von 1200 Höhenmetern mit 5 kg Rucksack in höchstens 4 Stunden. Mindestalter 16 Jahre. Auch für Snowboarder mit Splitboard offen. Wer sich nach dem Einführungstag als nicht geeignet erweist, erhält 80 % des Kursgelds zurück.",
                 partecipanti="Höchstens 30. Anmeldung vom 1. Oktober bis 1. Dezember 2026 oder bis die Plätze vergeben sind; das Kursgeld ist bis 10. Dezember zu bezahlen. Kurstage obligatorisch, bei jedem Wetter; Abwesenheiten und Rückzüge geben kein Recht auf Rückerstattung.",
                 materiale="Vollständige Skitourenausrüstung. LVS, Schaufel und Sonde auf Anfrage leihweise, im Kursgeld inbegriffen.",
                 programma="Präsentation am 3. Dezember 2026 (auch über Teams); Einführungstag am 9. Januar, Theorie am 12. Januar, Kurstage 16.–17. Januar, 20.–21. Februar und 6.–7. März 2027. CHF 650 für Mitglieder, 750 für Nichtmitglieder, 400 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften (etwa CHF 100) nicht inbegriffen."),
         fr=dict(titolo="Ski de randonnée", alt="Des skieurs de randonnée montant une pente enneigée",
                 testo="Pour se déplacer en sécurité et en autonomie lors des courses de la section : montée avec les peaux sur des pentes raides, descente hors piste, usage du matériel de sécurité, évaluation du danger d’avalanche et planification.",
                 struttura="Sept jours : une journée d’introduction à Airolo pour vérifier la forme et la technique, une soirée de théorie sur la neige, le DVA et le sauvetage par les camarades, puis trois week-ends à la Capanna Piansecco, à l’Hôtel Tiefenbach à la Furka et à la Camona da Maighels, avec instruction et courses jusqu’à 800-1200 m de dénivelé.",
                 requisiti="Bien skier sur les pistes noires et tenir une course de 1200 m de dénivelé avec un sac de 5 kg en 4 heures au maximum. Âge minimum 16 ans. Ouvert aussi aux snowboardeurs avec splitboard. Qui n’est pas jugé apte après la journée d’introduction récupère 80 % de la finance.",
                 partecipanti="30 au maximum. Inscriptions du 1er octobre au 1er décembre 2026, ou jusqu’à épuisement des places ; la finance est à verser avant le 10 décembre. Sorties obligatoires, par tous les temps ; absences et retraits ne donnent pas droit à un remboursement.",
                 materiale="Équipement complet de ski de randonnée. DVA, pelle et sonde prêtés sur demande, compris dans la finance.",
                 programma="Présentation le 3 décembre 2026 (aussi par Teams) ; journée d’introduction le 9 janvier, théorie le 12 janvier, sorties les 16-17 janvier, 20-21 février et 6-7 mars 2027. CHF 650 pour les membres, 750 pour les non-membres, 400 pour les jeunes OJ jusqu’à 20 ans et les membres étudiants de 21 à 25 ans ; déplacements en covoiturage (environ CHF 100) non compris."),
         en=dict(titolo="Ski touring", alt="Ski tourers climbing a snowy slope",
                 testo="To move safely and independently on the section’s trips: skinning up steep slopes, off-piste descents, use of safety equipment, avalanche risk assessment and planning.",
                 struttura="Seven days: an introductory day in Airolo to check fitness and technique, a theory evening on snow, transceivers and companion rescue, then three weekends at Capanna Piansecco, Hotel Tiefenbach on the Furka and Camona da Maighels, with instruction and tours of up to 800–1200 m of ascent.",
                 requisiti="Ski well on black runs and manage a 1200 m tour with a 5 kg pack in at most 4 hours. Minimum age 16. Also open to snowboarders with a splitboard. Anyone found unsuitable after the introductory day gets 80% of the fee back.",
                 partecipanti="Maximum 30. Registration from 1 October to 1 December 2026, or until places run out; the fee is due by 10 December. Outings are compulsory, whatever the weather; absences and withdrawals give no right to a refund.",
                 materiale="Full ski touring equipment. Transceiver, shovel and probe lent on request, included in the fee.",
                 programma="Presentation on 3 December 2026 (also via Teams); introductory day on 9 January, theory on 12 January, outings on 16–17 January, 20–21 February and 6–7 March 2027. CHF 650 for members, 750 for non-members, 400 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel (about CHF 100) not included.")),
    dict(stagione="Primavera", titolo="Arrampicata", cartella="arrampicata", img="corsi/arrampicata-4x5", dim=(594, 742), alt="Cordata su una parete di roccia accanto a un ghiacciaio",
         testo="Per principianti che vogliono avvicinarsi all’arrampicata in ambiente e per chi vuole consolidare la tecnica: sicurezza, manovre di corda, progressione su vie di più tiri. Dopo le basi, sempre più autonomia sotto la supervisione di un istruttore di arrampicata.",
         struttura="Sette giorni in tre fine settimana: prime arrampicate in falesia in Piemonte, vie di più tiri nel Locarnese, gite di applicazione nelle Alpi centrali; tra maggio e giugno, a volte, serate di arrampicata e ripasso dei nodi. Alla fine si arrampica in autonomia in falesia e su vie di più tiri: da secondi fino al 5a, da primi fino al 4b, con discesa in corda doppia.",
         requisiti="Nessun prerequisito tecnico: il corso è pensato per chi comincia. Età minima 16 anni.",
         partecipanti="Al massimo 26, in ordine d’iscrizione. All’iscrizione si versa un anticipo di CHF 300; l’iscrizione è definitiva con il saldo alla serata di presentazione. Serata e uscite obbligatorie, con qualsiasi tempo; le assenze vanno annunciate al capocorso entro il martedì prima.",
         materiale="Il CAS presta il materiale tecnico a chi non ce l’ha; alla serata di presentazione si vede cosa serve.",
         programma="Presentazione il 12 aprile 2027 alle 20:00 alla Scuola professionale di Trevano; uscite il 1-2 maggio, il 15-17 maggio e il 12-13 giugno 2027. CHF 600 per i soci, 650 per i non soci, 400 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni; trasferte in car sharing (CHF 40) escluse.",
         de=dict(titolo="Klettern", alt="Seilschaft an einer Felswand neben einem Gletscher",
                 testo="Für Einsteigerinnen und Einsteiger, die das Klettern draussen kennenlernen möchten, und für alle, die ihre Technik festigen wollen: Sicherheit, Seilmanöver, Mehrseillängenrouten. Nach den Grundlagen immer mehr Selbständigkeit unter Aufsicht eines Kletterlehrers.",
                 struttura="Sieben Tage an drei Wochenenden: erste Klettereien im Klettergarten im Piemont, Mehrseillängenrouten im Locarnese, Anwendungstouren in den Zentralalpen; zwischen Mai und Juni manchmal Kletterabende und Knotenrepetition. Am Ende klettert man selbständig im Klettergarten und in Mehrseillängenrouten: im Nachstieg bis 5a, im Vorstieg bis 4b, mit Abseilen.",
                 requisiti="Keine technischen Voraussetzungen: Der Kurs ist für Einsteiger gedacht. Mindestalter 16 Jahre.",
                 partecipanti="Höchstens 26, nach Anmeldeeingang. Bei der Anmeldung ist eine Anzahlung von CHF 300 zu leisten; definitiv ist die Anmeldung mit der Restzahlung am Informationsabend. Abend und Kurstage obligatorisch, bei jedem Wetter; Abwesenheiten sind dem Kursleiter bis zum Dienstag davor zu melden.",
                 materiale="Der SAC leiht technisches Material allen, die keines haben; am Informationsabend sieht man, was es braucht.",
                 programma="Präsentation am 12. April 2027 um 20:00 Uhr in der Berufsschule Trevano; Kurstage 1.–2. Mai, 15.–17. Mai und 12.–13. Juni 2027. CHF 600 für Mitglieder, 650 für Nichtmitglieder, 400 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren; Fahrten in Fahrgemeinschaften (CHF 40) nicht inbegriffen."),
         fr=dict(titolo="Escalade", alt="Cordée sur une paroi rocheuse à côté d’un glacier",
                 testo="Pour les débutants qui veulent découvrir l’escalade en extérieur et pour qui veut consolider sa technique : sécurité, manœuvres de corde, progression dans des voies de plusieurs longueurs. Après les bases, toujours plus d’autonomie sous la supervision d’un moniteur d’escalade.",
                 struttura="Sept jours en trois week-ends : premières escalades en falaise dans le Piémont, voies de plusieurs longueurs dans la région de Locarno, courses d’application dans les Alpes centrales ; entre mai et juin, parfois, des soirées d’escalade et de révision des nœuds. À la fin, on grimpe en autonomie en falaise et dans des voies de plusieurs longueurs : en second jusqu’au 5a, en tête jusqu’au 4b, avec descente en rappel.",
                 requisiti="Aucun prérequis technique : le cours est pensé pour les débutants. Âge minimum 16 ans.",
                 partecipanti="26 au maximum, dans l’ordre d’inscription. À l’inscription, un acompte de CHF 300 est demandé ; l’inscription est définitive avec le solde versé à la soirée de présentation. Soirée et sorties obligatoires, par tous les temps ; les absences sont à annoncer au chef de cours au plus tard le mardi précédent.",
                 materiale="Le CAS prête le matériel technique à qui n’en a pas ; la soirée de présentation montre ce qu’il faut.",
                 programma="Présentation le 12 avril 2027 à 20 h à l’École professionnelle de Trevano ; sorties les 1er-2 mai, 15-17 mai et 12-13 juin 2027. CHF 600 pour les membres, 650 pour les non-membres, 400 pour les jeunes OJ jusqu’à 20 ans et les membres étudiants de 21 à 25 ans ; déplacements en covoiturage (CHF 40) non compris."),
         en=dict(titolo="Climbing", alt="Rope team on a rock face next to a glacier",
                 testo="For beginners who want to get into outdoor climbing and for those who want to consolidate their technique: safety, rope work, multi-pitch routes. After the basics, more and more independence under the supervision of a climbing instructor.",
                 struttura="Seven days over three weekends: first climbs at a crag in Piedmont, multi-pitch routes around Locarno, applied trips in the Central Alps; between May and June, sometimes, climbing evenings and knot practice. By the end you climb independently at crags and on multi-pitch routes: seconding up to 5a, leading up to 4b, with abseiling.",
                 requisiti="No technical prerequisites: the course is designed for beginners. Minimum age 16.",
                 partecipanti="Maximum 26, in order of registration. A deposit of CHF 300 is due on registration; registration is final with the balance paid at the presentation evening. The evening and outings are compulsory, whatever the weather; absences must be reported to the course leader by the Tuesday before.",
                 materiale="The SAC lends technical gear to those who don’t have it; the presentation evening covers what you need.",
                 programma="Presentation on 12 April 2027 at 20:00 at the Trevano vocational school; outings on 1–2 May, 15–17 May and 12–13 June 2027. CHF 600 for members, 650 for non-members, 400 for OG youth up to 20 and student members aged 21 to 25; car-sharing travel (CHF 40) not included.")),
    dict(stagione="Inverno", titolo="Tecnica di sci fuori pista", cartella="freeride", img="corsi/freeride-4x5", dim=(594, 742), alt="Sciatori in discesa su un ghiacciaio",
         testo="Per chi fatica a scendere su pendii non preparati: trucchi e consigli per affrontare la neve fuori dalle piste battute. Adatto ai soci che vogliono migliorare, a chi si avvicina allo sci alpinismo e agli sciatori esperti in cerca di strategie per le condizioni difficili.",
         struttura="Quattro giorni per affinare la tecnica su diversi tipi di neve e di terreno, leggere il pendio e scegliere la tattica giusta per il gruppo, applicare le misure di riduzione del rischio e consolidare il soccorso in valanga.",
         requisiti="Le basi dello sci alpinismo (salire con le pelli, autosoccorso in valanga) e una discreta tecnica di sci fuori pista.",
         partecipanti="Numero di posti e condizioni d’iscrizione in definizione.",
         materiale="Attrezzatura completa da fuori pista e sci alpinismo, con ARTVA, pala e sonda.",
         programma="Programma 2027 in definizione: date e costi seguono.",
         de=dict(titolo="Off-Piste-Skitechnik", alt="Skifahrer in der Abfahrt auf einem Gletscher",
                 testo="Für alle, die sich an unpräparierten Hängen schwertun: Tricks und Tipps für den Schnee abseits der Pisten. Für Mitglieder, die sich verbessern wollen, für Einsteiger ins Skitourengehen und für erfahrene Skifahrer, die Strategien für schwierige Verhältnisse suchen.",
                 struttura="Vier Tage, um die Technik in verschiedenen Schnee- und Geländearten zu verfeinern, den Hang zu lesen und die richtige Taktik für die Gruppe zu wählen, Massnahmen zur Risikominderung anzuwenden und die Lawinenrettung zu festigen.",
                 requisiti="Die Grundlagen des Skitourengehens (Aufstieg mit Fellen, Kameradenrettung) und eine ordentliche Technik abseits der Piste.",
                 partecipanti="Platzzahl und Anmeldebedingungen noch offen.",
                 materiale="Vollständige Freeride- und Skitourenausrüstung mit LVS, Schaufel und Sonde.",
                 programma="Programm 2027 in Vorbereitung: Daten und Kosten folgen."),
         fr=dict(titolo="Technique de ski hors piste", alt="Des skieurs descendant un glacier",
                 testo="Pour qui peine à descendre des pentes non préparées : trucs et conseils pour affronter la neige hors des pistes damées. Pour les membres qui veulent progresser, pour qui débute en ski de randonnée et pour les skieurs expérimentés en quête de stratégies pour les conditions difficiles.",
                 struttura="Quatre jours pour affiner la technique sur différents types de neige et de terrain, lire la pente et choisir la bonne tactique pour le groupe, appliquer les mesures de réduction du risque et consolider le sauvetage en avalanche.",
                 requisiti="Les bases du ski de randonnée (monter avec les peaux, sauvetage par les camarades) et une bonne technique de ski hors piste.",
                 partecipanti="Nombre de places et conditions d’inscription à définir.",
                 materiale="Équipement complet de hors-piste et de ski de randonnée, avec DVA, pelle et sonde.",
                 programma="Programme 2027 en préparation : dates et coûts suivront."),
         en=dict(titolo="Off-piste ski technique", alt="Skiers descending a glacier",
                 testo="For those who struggle on ungroomed slopes: tips and tricks for snow away from the pistes. For members who want to improve, for newcomers to ski touring and for experienced skiers looking for strategies for difficult conditions.",
                 struttura="Four days to refine technique on different kinds of snow and terrain, read the slope and choose the right tactics for the group, apply risk-reduction measures and consolidate avalanche rescue.",
                 requisiti="The basics of ski touring (skinning, avalanche companion rescue) and a reasonable off-piste technique.",
                 partecipanti="Number of places and registration conditions to be confirmed.",
                 materiale="Full off-piste and ski touring equipment, with transceiver, shovel and probe.",
                 programma="2027 programme in preparation: dates and costs to follow.")),
    dict(stagione="Inverno", titolo="Racchette", cartella="racchette", img="corsi/racchette-4x5", dim=(800, 1000), alt="Cresta innevata sopra un mare di nuvole",
         testo="Introduzione all’escursionismo con le racchette, tra teoria e pratica: riconoscere i segnali di pericolo, valutare il rischio valanghe e il terreno, pianificare con gli strumenti disponibili, ricerca dei sepolti e primo soccorso.",
         struttura="Sei giorni: una serata di nivologia, una giornata sulla sicurezza con ARTVA, pala e sonda, poi due fine settimana in capanna, alla Capanna Piansecco e alla Capanna Maighels, tra tecnica di progressione, metodo 3x3, orientamento e dinamiche di gruppo. Alla fine si sale e si scende in sicurezza su terreni semplici, segnati e non.",
         requisiti="Discreta condizione fisica: escursioni di 4-5 ore con 500-700 m di dislivello. Età minima 16 anni.",
         partecipanti="Al massimo 20, in ordine d’iscrizione. L’iscrizione è definitiva con il pagamento della quota alla serata introduttiva. Serata e uscite obbligatorie, con qualsiasi tempo; la meta può cambiare secondo le condizioni.",
         materiale="L’equipaggiamento personale viene controllato il primo giorno. ARTVA, pala e sonda prestati a chi ne ha bisogno.",
         programma="Serata introduttiva martedì 15 dicembre 2026 nel Luganese; nivologia il 12 gennaio 2027 a Mezzovico, sicurezza il 16 gennaio ad Airolo, uscite il 23-24 gennaio e il 13-14 febbraio 2027. CHF 650 per i soci, 700 per i non soci, 375 per i giovani OG fino a 20 anni e gli studenti soci dai 21 ai 25 anni, trasferte comprese.",
         de=dict(titolo="Schneeschuhtouren", alt="Verschneiter Grat über einem Nebelmeer",
                 testo="Einführung ins Schneeschuhwandern, in Theorie und Praxis: Gefahrenzeichen erkennen, Lawinenrisiko und Gelände beurteilen, mit den verfügbaren Hilfsmitteln planen, Verschüttetensuche und Erste Hilfe.",
                 struttura="Sechs Tage: ein Abend Schnee- und Lawinenkunde, ein Sicherheitstag mit LVS, Schaufel und Sonde, dann zwei Wochenenden in der Capanna Piansecco und der Capanna Maighels, mit Gehtechnik, 3x3-Methode, Orientierung und Gruppendynamik. Am Ende steigt man sicher auf und ab in einfachem Gelände, markiert und unmarkiert.",
                 requisiti="Gute Kondition: Touren von 4–5 Stunden mit 500–700 Höhenmetern. Mindestalter 16 Jahre.",
                 partecipanti="Höchstens 20, nach Anmeldeeingang. Definitiv ist die Anmeldung mit der Bezahlung am Einführungsabend. Abend und Kurstage obligatorisch, bei jedem Wetter; das Ziel kann je nach Verhältnissen ändern.",
                 materiale="Die persönliche Ausrüstung wird am ersten Tag kontrolliert. LVS, Schaufel und Sonde werden bei Bedarf ausgeliehen.",
                 programma="Einführungsabend am Dienstag, 15. Dezember 2026, im Luganese; Schnee- und Lawinenkunde am 12. Januar 2027 in Mezzovico, Sicherheitstag am 16. Januar in Airolo, Kurstage 23.–24. Januar und 13.–14. Februar 2027. CHF 650 für Mitglieder, 700 für Nichtmitglieder, 375 für JO-Jugendliche bis 20 Jahre und studierende Mitglieder von 21 bis 25 Jahren, Fahrten inbegriffen."),
         fr=dict(titolo="Raquettes", alt="Arête enneigée au-dessus d’une mer de brouillard",
                 testo="Introduction à la randonnée à raquettes, entre théorie et pratique : reconnaître les signaux de danger, évaluer le risque d’avalanche et le terrain, planifier avec les outils disponibles, recherche de victimes ensevelies et premiers secours.",
                 struttura="Six jours : une soirée de nivologie, une journée sur la sécurité avec DVA, pelle et sonde, puis deux week-ends en cabane, à la Capanna Piansecco et à la Capanna Maighels, entre technique de progression, méthode 3x3, orientation et dynamique de groupe. À la fin, on monte et on descend en sécurité sur des terrains simples, balisés ou non.",
                 requisiti="Bonne condition physique : randonnées de 4-5 heures avec 500-700 m de dénivelé. Âge minimum 16 ans.",
                 partecipanti="20 au maximum, dans l’ordre d’inscription. L’inscription est définitive avec le paiement de la finance à la soirée d’introduction. Soirée et sorties obligatoires, par tous les temps ; le but peut changer selon les conditions.",
                 materiale="L’équipement personnel est contrôlé le premier jour. DVA, pelle et sonde prêtés à qui en a besoin.",
                 programma="Soirée d’introduction le mardi 15 décembre 2026 dans la région de Lugano ; nivologie le 12 janvier 2027 à Mezzovico, sécurité le 16 janvier à Airolo, sorties les 23-24 janvier et 13-14 février 2027. CHF 650 pour les membres, 700 pour les non-membres, 375 pour les jeunes OJ jusqu’à 20 ans et les membres étudiants de 21 à 25 ans, déplacements compris."),
         en=dict(titolo="Snowshoeing", alt="Snowy ridge above a sea of clouds",
                 testo="An introduction to snowshoeing, in theory and practice: recognising danger signs, assessing avalanche risk and terrain, planning with the tools available, searching for buried people and first aid.",
                 struttura="Six days: an evening on snow science, a safety day with transceiver, shovel and probe, then two weekends at Capanna Piansecco and Capanna Maighels, covering walking technique, the 3x3 method, navigation and group dynamics. By the end you can go up and down safely on easy terrain, marked and unmarked.",
                 requisiti="Reasonable fitness: outings of 4–5 hours with 500–700 m of ascent. Minimum age 16.",
                 partecipanti="Maximum 20, in order of registration. Registration is final once the fee is paid at the introductory evening. The evening and outings are compulsory, whatever the weather; the destination may change according to conditions.",
                 materiale="Personal equipment is checked on the first day. Transceiver, shovel and probe lent to those who need them.",
                 programma="Introductory evening on Tuesday 15 December 2026 in the Lugano area; snow science on 12 January 2027 in Mezzovico, safety day on 16 January in Airolo, outings on 23–24 January and 13–14 February 2027. CHF 650 for members, 700 for non-members, 375 for OG youth up to 20 and student members aged 21 to 25, travel included.")),
]


def corsi():
    lang = LINGUA["lang"]
    stagioni = {"Estate": tr("Estate", "Sommer", "Summer", "Été"), "Inverno": tr("Inverno", "Winter", "Winter", "Hiver"), "Primavera": tr("Primavera", "Frühling", "Spring", "Printemps")}
    articoli, voci = [], []
    for c in CORSI:
        x = c if lang == "it" else {**c, **c[lang]}
        voci.append((f"corso-{CORSO_SLUG[c['titolo']]}", x["titolo"]))
        articoli.append(f"""<article class="course-row course-row--corso" id="corso-{CORSO_SLUG[c['titolo']]}" aria-labelledby="corso-{CORSO_SLUG[c['titolo']]}-h" data-reveal>
<figure>{img(c['img'], x['alt'], *c['dim'])}</figure>
<div class="course-text">
<span class="label">{stagioni[c['stagione']]}</span>
<h2 id="corso-{CORSO_SLUG[c['titolo']]}-h" class="h2">{x['titolo']}</h2>
<p>{x['testo']}</p>
<a class="btn btn--primary" href="{GITE_CORSI}">{tr("Iscriviti", "Anmelden", "Register", "S’inscrire")} <span class="arrow" aria-hidden="true">→</span></a>
</div>
{facts(schede_corso(c['cartella'], x))}
</article>""")
    titolo = tr("Corsi", "Kurse", "Courses", "Cours")
    body = page_hero([att_crumb(), (titolo, None)], titolo, testo_campo(testi("introduzioni")["corsi"], "introduzione")) + f"""

{salti(voci, tr("Vai al corso", "Zum Kurs", "Go to course", "Aller au cours"))}

<section class="section" aria-label="{tr("Corsi base", "Grundkurse", "Basic courses", "Cours de base")}">
<div class="container">
{chr(10).join(articoli)}
</div>
</section>

<section class="section" aria-labelledby="avanzati-h">
<div class="container">
<div class="callout">
<p>{tr("<strong id=\"avanzati-h\">Verso capogita e monitore G+S.</strong> Per chi vuole approfondire o prepararsi ai corsi capogita CAS e monitore Gioventù+Sport, la sezione propone corsi avanzati di alpinismo, sci alpinismo e arrampicata, di regola ad anni alterni, e serate di formazione teorica con specialisti.",
       "<strong id=\"avanzati-h\">Auf dem Weg zur Tourenleitung und J+S-Leitung.</strong> Wer sich vertiefen oder auf die Tourenleiterkurse des SAC und die Jugend+Sport-Leiterkurse vorbereiten will, findet bei der Sektion Fortgeschrittenenkurse in Hochtouren, Skitouren und Klettern, in der Regel alle zwei Jahre, und Theorieabende mit Fachleuten.",
       "<strong id=\"avanzati-h\">Towards trip leader and Youth+Sport instructor.</strong> For those who want to go further or prepare for the SAC trip leader and Youth+Sport instructor courses, the section offers advanced courses in mountaineering, ski touring and climbing, usually every other year, and theory evenings with specialists.",
       "<strong id=\"avanzati-h\">Vers chef de course et moniteur J+S.</strong> Pour qui veut approfondir ou se préparer aux cours de chef de course du CAS et de moniteur Jeunesse+Sport, la section propose des cours avancés d’alpinisme, de ski de randonnée et d’escalade, en principe une année sur deux, et des soirées de formation théorique avec des spécialistes.")}</p>
</div>
</div>
</section>

{prima_di_partire()}

{subnav(ATT_MENU(), L("corsi.html"))}"""
    return sezione_page("corsi.html", titolo + " | CAS Ticino", tr(
        "Corsi del CAS Ticino diretti da professionisti: sci alpinismo, racchette, tecnica di sci fuori pista, arrampicata e alpinismo.",
        "Kurse der SAC-Sektion Ticino mit Bergprofis: Skitouren, Schneeschuhtouren, Off-Piste-Skitechnik, Klettern und Hochtouren.",
        "Courses of the SAC Ticino Section led by professionals: ski touring, snowshoeing, off-piste ski technique, climbing and mountaineering.",
        "Cours du CAS Ticino dirigés par des professionnels : ski de randonnée, raquettes, technique de ski hors piste, escalade et alpinisme."),
        body, og="corsi/scialpinismo-4x5")


def prima_di_partire():
    """Riquadro «Prima di partire» (Partecipare, Corsi, Programma gite): bollettino valanghe, meteo, pianificazione,
    cartina e numeri d'emergenza. Solo link: nessun servizio esterno viene caricato nella pagina."""
    lang = LINGUA["lang"]
    voci = [
        (tr("Bollettino valanghe", "Lawinenbulletin", "Avalanche bulletin", "Bulletin d’avalanches"),
         tr("SLF, la situazione del manto nevoso in tutta la Svizzera", "SLF, die Schneedecke in der ganzen Schweiz", "SLF, the snowpack across Switzerland", "SLF, l’état du manteau neigeux dans toute la Suisse"),
         {"it": "https://www.slf.ch/it/bollettino-valanghe-e-situazione-nivologica/", "de": "https://www.slf.ch/de/lawinenbulletin-und-schneesituation/",
          "fr": "https://www.slf.ch/fr/bulletin-davalanches-et-situation-nivologique/",
          "en": "https://www.slf.ch/en/avalanche-bulletin-and-snow-situation/"}[lang]),
        (tr("Meteo", "Wetter", "Weather", "Météo"), tr("MeteoSvizzera, previsioni e allerte", "MeteoSchweiz, Prognosen und Warnungen", "MeteoSwiss, forecasts and warnings", "MétéoSuisse, prévisions et alertes"),
         {"it": "https://www.meteosvizzera.admin.ch/", "de": "https://www.meteoschweiz.admin.ch/", "fr": "https://www.meteosuisse.admin.ch/",
          "en": "https://www.meteoswiss.admin.ch/"}[lang]),
        ("White Risk", tr("Pianificare le gite invernali e imparare a valutare il pericolo valanghe",
                          "Wintertouren planen und die Lawinengefahr beurteilen lernen", "Plan winter tours and learn to judge avalanche danger",
                                                                                         "Planifier les courses d’hiver et apprendre à évaluer le danger d’avalanche"),
         f"https://whiterisk.ch/{lang}"),
        (tr("Cartina", "Karte", "Map", "Carte"), tr("swisstopo, carte nazionali, pendenze e itinerari", "swisstopo, Landeskarten, Hangneigung und Routen",
                                            "swisstopo, national maps, slope angles and routes",
                                            "swisstopo, cartes nationales, inclinaison des pentes et itinéraires"), f"https://map.geo.admin.ch/?lang={lang}"),
    ]
    links = "\n".join(f'<a href="{u}" rel="noopener"><span><strong>{t_}</strong> <span class="partenza-nota">{nota}</span></span>'
                       f'<span class="tag">{u.split("/")[2].removeprefix("www.")}</span></a>' for t_, nota, u in voci)
    numeri = [("1414", tr("Rega, soccorso aereo", "Rega, Luftrettung", "Rega, air rescue", "Rega, sauvetage aérien")),
              ("144", tr("Ambulanza", "Sanitätsnotruf", "Ambulance", "Ambulance")),
              ("112", tr("Numero d’emergenza europeo", "Europäische Notrufnummer", "European emergency number", "Numéro d’urgence européen"))]
    numeri = "\n".join(f'<a href="tel:{n}"><strong class="num">{n}</strong><span>{x}</span></a>' for n, x in numeri)
    return f"""<section class="section" id="prima-di-partire" aria-labelledby="partire-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="partire-h" class="h2">{tr("Prima di partire", "Vor dem Aufbruch", "Before you set off", "Avant de partir")}</h2>
<p>{tr("Controlla meteo e bollettino valanghe la sera prima e la mattina stessa, e scegli la gita in base alle condizioni, non solo alla meta.",
       "Prüfen Sie Wetter und Lawinenbulletin am Vorabend und am Morgen selbst, und wählen Sie die Tour nach den Verhältnissen, nicht nur nach dem Ziel.",
       "Check the weather and the avalanche bulletin the evening before and on the morning itself, and choose the trip by the conditions, not just the destination.",
       "Consultez la météo et le bulletin d’avalanches la veille et le matin même, et choisissez la course selon les conditions, pas seulement selon le but.")}</p>
</div>
<div class="stack" data-reveal>
<div class="linklist">
{links}
</div>
<div class="emergenza">
<h3 class="label">{tr("In caso di emergenza", "Im Notfall", "In an emergency", "En cas d’urgence")}</h3>
<div class="emergenza-numeri">
{numeri}
</div>
<p class="small">{tr("Con l’app della Rega l’allarme trasmette anche la tua posizione.", "Mit der Rega-App übermittelt der Alarm auch Ihren Standort.",
                     "With the Rega app, the alarm also sends your location.",
                     "Avec l’app de la Rega, l’alarme transmet aussi votre position.")} <a href="{tr("https://www.rega.ch/it/", "https://www.rega.ch/", "https://www.rega.ch/en/", "https://www.rega.ch/fr/")}" rel="noopener">{tr("App Rega", "Rega-App", "Rega app", "App Rega")}</a></p>
</div>
</div>
</div>
</section>"""


REGOLAMENTO_GITE = DOC + "statuto-visione/regolamento-gite-2026.pdf"


def partecipare():
    """Le regole per chi partecipa alle gite, in breve, dal regolamento gite (docs/statuto-visione/regolamento-gite-*.pdf):
    quando cambia il regolamento, aggiornare anche questo testo (nelle quattro lingue)."""
    nomi = {"it": {}, "de": DOCS_DE, "fr": DOCS_FR, "en": DOCS_EN}[LINGUA["lang"]]
    scale = ", ".join(f'<a href="{h}">{nomi.get(l, l).lower() if LINGUA["lang"] != "de" else nomi.get(l, l)}</a>' for l, h in DOCS[1][1])
    sezioni = [
        blocco("prima-h", tr("Prima di iscriverti", "Vor der Anmeldung", "Before you register", "Avant de vous inscrire"),
               tr("Le gite sono aperte a tutti, anche a chi non è socio. Scegli quelle adatte a te.",
                  "Die Touren stehen allen offen, auch Nichtmitgliedern. Wählen Sie diejenigen, die zu Ihnen passen.",
                  "Trips are open to everyone, members or not. Choose the ones that suit you.",
                  "Les courses sont ouvertes à tous, membres ou non. Choisissez celles qui vous conviennent."),
               tr(f"""<p>Per ogni gita il programma indica le esigenze tecniche e di condizione fisica, l’itinerario in breve, l’equipaggiamento necessario e il numero massimo di partecipanti. Le difficoltà seguono le scale del CAS: {scale}.</p>
<ul>
<li>Devi avere la preparazione tecnica e fisica richiesta dalla gita.</li>
<li>Alcune gite chiedono una gita di preparazione o un corso; il capogita può chiederti le tue gite recenti.</li>
<li>Le attività del gruppo giovani hanno limiti d’età.</li>
<li>Per qualsiasi dubbio scrivi al capogita, dalla pagina della gita.</li>
</ul>""", f"""<p>Für jede Tour nennt das Programm die technischen und konditionellen Anforderungen, die Route in Kürze, die nötige Ausrüstung und die maximale Teilnehmerzahl. Die Schwierigkeiten folgen den Skalen des SAC (PDF, italienisch): {scale}.</p>
<ul>
<li>Sie müssen die technische und körperliche Vorbereitung mitbringen, die die Tour verlangt.</li>
<li>Einige Touren setzen eine Vorbereitungstour oder einen Kurs voraus; die Tourenleitung kann nach Ihren letzten Touren fragen.</li>
<li>Die Aktivitäten der Jugendgruppe haben Altersgrenzen.</li>
<li>Bei Fragen schreiben Sie der Tourenleitung, über die Seite der Tour.</li>
</ul>""", f"""<p>For each trip the programme gives the technical and fitness requirements, a short description of the route, the equipment needed and the maximum number of participants. Difficulty follows the SAC scales (PDF, in Italian): {scale}.</p>
<ul>
<li>You must have the technical and physical preparation the trip requires.</li>
<li>Some trips require a preparatory trip or a course; the trip leader may ask about your recent trips.</li>
<li>Youth group activities have age limits.</li>
<li>If in doubt, write to the trip leader from the trip’s page.</li>
</ul>""",
          f"""<p>Pour chaque course, le programme indique les exigences techniques et de condition physique, l’itinéraire en bref, l’équipement nécessaire et le nombre maximum de participants. Les difficultés suivent les échelles du CAS (PDF, en italien) : {scale}.</p>
<ul>
<li>Vous devez avoir la préparation technique et physique demandée par la course.</li>
<li>Certaines courses demandent une course de préparation ou un cours ; le chef de course peut vous demander vos courses récentes.</li>
<li>Les activités du groupe jeunesse ont des limites d’âge.</li>
<li>En cas de doute, écrivez au chef de course depuis la page de la course.</li>
</ul>""")),
        blocco("iscrizione-h", tr("Iscrizione e conferma", "Anmeldung und Bestätigung", "Registration and confirmation", "Inscription et confirmation"),
               tr("Ci si iscrive su Droptour, nei termini indicati per ogni gita.", "Angemeldet wird auf Droptour, innerhalb der Fristen jeder Tour.", "You register on Droptour, within the deadlines given for each trip.", "On s’inscrit sur Droptour, dans les délais indiqués pour chaque course."),
               tr("""<ul>
<li>I posti vengono assegnati in ordine d’iscrizione, con la precedenza ai soci della sezione e poi ai soci di altre associazioni alpinistiche con cui vale la reciprocità.</li>
<li>Al più tardi 20 giorni prima della gita il capogita conferma l’iscrizione su Droptour: <strong>sei iscritto solo quando ricevi la conferma per e-mail</strong>.</li>
<li>Nella settimana prima della gita il capogita manda i dettagli ai partecipanti.</li>
<li>Se non puoi più partecipare, avvisa subito i capigita: il posto passa a chi è in lista d’attesa.</li>
</ul>""", """<ul>
<li>Die Plätze werden nach Anmeldeeingang vergeben, mit Vorrang für Mitglieder der Sektion und danach für Mitglieder anderer Bergsportvereine mit Gegenrecht.</li>
<li>Spätestens 20 Tage vor der Tour bestätigt die Tourenleitung die Anmeldung auf Droptour: <strong>Angemeldet sind Sie erst, wenn Sie die Bestätigung per E-Mail erhalten</strong>.</li>
<li>In der Woche vor der Tour schickt die Tourenleitung die Einzelheiten an die Teilnehmenden.</li>
<li>Wenn Sie nicht mehr teilnehmen können, melden Sie es sofort der Tourenleitung: Der Platz geht an jemanden auf der Warteliste.</li>
</ul>""", """<ul>
<li>Places are allocated in order of registration, with priority for section members and then for members of other mountaineering clubs with reciprocal agreements.</li>
<li>No later than 20 days before the trip the leader confirms your registration on Droptour: <strong>you are registered only once you receive the confirmation e-mail</strong>.</li>
<li>In the week before the trip the leader sends the details to the participants.</li>
<li>If you can no longer take part, tell the trip leaders straight away: the place goes to someone on the waiting list.</li>
</ul>""",
          """<ul>
<li>Les places sont attribuées dans l’ordre d’inscription, avec la priorité aux membres de la section, puis aux membres d’autres associations alpines avec qui la réciprocité s’applique.</li>
<li>Au plus tard 20 jours avant la course, le chef de course confirme l’inscription sur Droptour : <strong>vous n’êtes inscrit qu’une fois la confirmation reçue par e-mail</strong>.</li>
<li>Dans la semaine précédant la course, le chef de course envoie les détails aux participants.</li>
<li>Si vous ne pouvez plus participer, prévenez tout de suite les chefs de course : la place passe à quelqu’un sur la liste d’attente.</li>
</ul>""")),
        blocco("gita-h", tr("Durante la gita", "Während der Tour", "During the trip", "Pendant la course"),
               tr("Il capogita, di regola affiancato da un co-capogita, organizza e conduce la gita.",
                  "Die Tourenleitung, in der Regel mit einer Co-Leitung, organisiert und führt die Tour.",
                  "The trip leader, usually with a co-leader, organises and leads the trip.",
                  "Le chef de course, en principe secondé par un co-chef de course, organise et conduit la course."),
               tr("""<ul>
<li>La gita si fa se ci sono almeno tre partecipanti, capigita esclusi.</li>
<li>Di regola si parte anche con un tempo non ideale; con condizioni pessime o un rischio evidente il capogita può cambiare meta, rinviare o annullare, anche a gita in corso.</li>
<li>Si seguono le indicazioni dei capigita. Chi non le segue, o non è all’altezza della gita, può esserne escluso; il rientro in sicurezza resta comunque garantito.</li>
<li>Chi si separa dal gruppo di sua iniziativa lo fa a proprio rischio e deve dirlo chiaramente al capogita.</li>
<li>I trasporti li organizzano i capigita: quando si può, mezzi pubblici o auto in comune.</li>
<li>Ognuno porta il proprio materiale tecnico; quello che manca si può <a href="noleggio.html">noleggiare dalla sezione</a>.</li>
</ul>""", """<ul>
<li>Die Tour findet statt, wenn mindestens drei Personen teilnehmen, Leitende nicht mitgezählt.</li>
<li>In der Regel wird auch bei nicht idealem Wetter gestartet; bei sehr schlechten Verhältnissen oder offensichtlicher Gefahr kann die Tourenleitung das Ziel ändern, die Tour verschieben oder absagen, auch unterwegs.</li>
<li>Den Anweisungen der Tourenleitung ist zu folgen. Wer das nicht tut oder der Tour nicht gewachsen ist, kann ausgeschlossen werden; eine sichere Rückkehr bleibt gewährleistet.</li>
<li>Wer sich aus eigenem Entschluss von der Gruppe trennt, tut das auf eigene Gefahr und muss es der Tourenleitung klar mitteilen.</li>
<li>Die Anreise organisiert die Tourenleitung: wenn möglich mit öffentlichen Verkehrsmitteln oder in Fahrgemeinschaften.</li>
<li>Alle bringen ihr eigenes technisches Material mit; was fehlt, kann man <a href="noleggio.html">bei der Sektion mieten</a>.</li>
</ul>""", """<ul>
<li>A trip goes ahead with at least three participants, not counting the leaders.</li>
<li>As a rule trips start even in less than ideal weather; in very bad conditions or with an obvious risk the leader may change the objective, postpone or cancel, even during the trip.</li>
<li>Follow the leaders’ instructions. Anyone who does not, or who is not up to the trip, may be excluded; a safe return is still ensured.</li>
<li>Anyone who leaves the group on their own initiative does so at their own risk and must tell the leader clearly.</li>
<li>The leaders organise transport: public transport or shared cars wherever possible.</li>
<li>Everyone brings their own technical gear; anything missing can be <a href="noleggio.html">hired from the section</a>.</li>
</ul>""",
          """<ul>
<li>La course a lieu s’il y a au moins trois participants, chefs de course non compris.</li>
<li>En règle générale, on part même par un temps peu idéal ; en cas de conditions très mauvaises ou de risque évident, le chef de course peut changer de but, reporter ou annuler, même pendant la course.</li>
<li>On suit les indications des chefs de course. Qui ne les suit pas, ou n’est pas à la hauteur de la course, peut en être exclu ; le retour en sécurité reste dans tous les cas assuré.</li>
<li>Qui se sépare du groupe de sa propre initiative le fait à ses risques et doit le dire clairement au chef de course.</li>
<li>Les chefs de course organisent les transports : quand c’est possible, transports publics ou voitures partagées.</li>
<li>Chacun apporte son matériel technique ; ce qui manque peut être <a href="noleggio.html">loué à la section</a>.</li>
</ul>""")),
        blocco("rischi-h", tr("Rischi e assicurazione", "Risiken und Versicherung", "Risks and insurance", "Risques et assurance"),
               tr("Nessuna attività in montagna è priva di rischi: si partecipa a proprio rischio e pericolo.",
                  "Keine Aktivität in den Bergen ist ohne Risiko: Die Teilnahme erfolgt auf eigene Gefahr.",
                  "No mountain activity is free of risk: you take part at your own risk.",
                  "Aucune activité en montagne n’est sans risque : on participe à ses propres risques et périls."),
               tr("""<p>Iscrivendoti dichiari di conoscere i pericoli, di avere capacità adatte alla gita, di saper usare il tuo materiale e di esserti informato sul percorso.</p>
<p><strong>La sezione non ha assicurazioni per le sue attività.</strong> Ogni partecipante deve avere una propria copertura: infortuni, responsabilità civile, protezione giuridica e spese di soccorso e recupero. Salvo i casi previsti dalla legge, la sezione e i capigita non rispondono di infortuni o danni.</p>""",
                  """<p>Mit der Anmeldung erklären Sie, die Gefahren zu kennen, über die für die Tour nötigen Fähigkeiten zu verfügen, mit Ihrem Material umgehen zu können und sich über die Route informiert zu haben.</p>
<p><strong>Die Sektion hat für ihre Aktivitäten keine Versicherungen abgeschlossen.</strong> Alle Teilnehmenden brauchen einen eigenen Versicherungsschutz: Unfall, Haftpflicht, Rechtsschutz sowie Rettungs- und Bergungskosten. Ausser in den gesetzlich vorgesehenen Fällen haften die Sektion und die Tourenleitenden nicht für Unfälle oder Schäden.</p>""",
                  """<p>By registering you declare that you are aware of the dangers, have the skills the trip requires, know how to use your gear and have found out about the route.</p>
<p><strong>The section has no insurance for its activities.</strong> Every participant needs their own cover: accident, third-party liability, legal protection, and rescue and recovery costs. Except where the law provides otherwise, the section and the trip leaders are not liable for accidents or damage.</p>""",
                  """<p>En vous inscrivant, vous déclarez connaître les dangers, avoir les capacités adaptées à la course, savoir utiliser votre matériel et vous être renseigné sur l’itinéraire.</p>
<p><strong>La section n’a pas d’assurance pour ses activités.</strong> Chaque participant doit avoir sa propre couverture : accidents, responsabilité civile, protection juridique et frais de sauvetage et de récupération. Sauf dans les cas prévus par la loi, la section et les chefs de course ne répondent pas des accidents ou des dommages.</p>""")),
        blocco("costi-h", tr("Costi", "Kosten", "Costs", "Coûts"),
               tr("I partecipanti si dividono i costi della gita; i capigita sono volontari.",
                  "Die Teilnehmenden teilen sich die Kosten der Tour; die Tourenleitenden sind ehrenamtlich.",
                  "Participants share the costs of the trip; the trip leaders are volunteers.",
                  "Les participants se partagent les coûts de la course ; les chefs de course sont bénévoles."),
               tr("""<ul>
<li>In auto privata ogni partecipante versa 10 centesimi al chilometro, divisi tra chi mette a disposizione l’auto.</li>
<li>Se c’è una guida o un altro professionista della montagna, il suo compenso è diviso tra i partecipanti.</li>
<li>Il capogita può chiedere un acconto.</li>
<li>Se la gita è annullata non ci sono rimborsi: le spese di annullamento della capanna sono divise tra i partecipanti, gli acconti restituiti, tranne quanto trattenuto da terzi.</li>
<li>Se rinunci e nessuno in lista d’attesa prende il tuo posto, il capogita può chiederti i costi già sostenuti, per esempio la caparra della capanna.</li>
</ul>""", """<ul>
<li>Bei Fahrten mit Privatautos zahlen alle Teilnehmenden 10 Rappen pro Kilometer, die unter den Fahrzeughaltern aufgeteilt werden.</li>
<li>Ist ein Bergführer oder eine andere Bergsportfachperson dabei, wird das Honorar unter den Teilnehmenden aufgeteilt.</li>
<li>Die Tourenleitung kann eine Anzahlung verlangen.</li>
<li>Wird die Tour abgesagt, gibt es keine Rückerstattung: Annullierungskosten der Hütte werden unter den Teilnehmenden aufgeteilt, Anzahlungen zurückerstattet, ausser was Dritte einbehalten.</li>
<li>Wenn Sie absagen und niemand von der Warteliste Ihren Platz übernimmt, kann die Tourenleitung die bereits entstandenen Kosten verlangen, etwa die Anzahlung für die Hütte.</li>
</ul>""", """<ul>
<li>When travelling by private car, each participant pays 10 centimes per kilometre, shared among those who provide a car.</li>
<li>If a mountain guide or other mountain professional takes part, their fee is shared among the participants.</li>
<li>The leader may ask for a deposit.</li>
<li>If the trip is cancelled there are no refunds: hut cancellation fees are shared among the participants and deposits returned, except for amounts kept by third parties.</li>
<li>If you withdraw and nobody on the waiting list takes your place, the leader may ask you to pay costs already incurred, such as the hut deposit.</li>
</ul>""",
          """<ul>
<li>En voiture privée, chaque participant verse 10 centimes par kilomètre, répartis entre ceux qui mettent leur voiture à disposition.</li>
<li>S’il y a un guide ou un autre professionnel de la montagne, ses honoraires sont répartis entre les participants.</li>
<li>Le chef de course peut demander un acompte.</li>
<li>Si la course est annulée, il n’y a pas de remboursement : les frais d’annulation de la cabane sont répartis entre les participants, les acomptes rendus, sauf les montants retenus par des tiers.</li>
<li>Si vous renoncez et que personne sur la liste d’attente ne prend votre place, le chef de course peut vous demander les frais déjà engagés, par exemple les arrhes de la cabane.</li>
</ul>""")),
        blocco("dati-h", tr("Dati e foto", "Daten und Fotos", "Data and photos", "Données et photos"),
               tr("Con l’iscrizione accetti alcune regole sui tuoi dati.", "Mit der Anmeldung akzeptieren Sie einige Regeln zu Ihren Daten.", "By registering you accept a few rules about your data.", "En vous inscrivant, vous acceptez quelques règles sur vos données."),
               tr("""<p>I tuoi dati servono ai capigita e alla sezione per organizzare la gita e per la sicurezza; la lista dei partecipanti può essere data agli altri partecipanti. Le foto di gruppo e personali scattate in gita possono comparire su annuario, Informazione, sito e social della sezione: se non vuoi, dillo al capogita. Più dettagli nella pagina sulla <a href="privacy.html">protezione dei dati</a>.</p>""",
                  """<p>Ihre Daten dienen der Tourenleitung und der Sektion zur Organisation der Tour und zur Sicherheit; die Teilnehmerliste kann an die anderen Teilnehmenden weitergegeben werden. Gruppen- und Einzelfotos von der Tour können im Jahrbuch, in «Informazione», auf der Website und in den sozialen Medien der Sektion erscheinen: Wenn Sie das nicht möchten, sagen Sie es der Tourenleitung. Mehr dazu auf der Seite <a href="privacy.html">Datenschutz</a>.</p>""",
                  """<p>Your data is used by the leaders and the section to organise the trip and for safety; the list of participants may be given to the other participants. Group and individual photos taken on the trip may appear in the yearbook, «Informazione», the website and the section’s social media: if you would rather they didn’t, tell the trip leader. More on the <a href="privacy.html">privacy</a> page.</p>""",
                  """<p>Vos données servent aux chefs de course et à la section pour organiser la course et pour la sécurité ; la liste des participants peut être remise aux autres participants. Les photos de groupe et individuelles prises pendant la course peuvent paraître dans l’annuaire, « Informazione », le site et les réseaux sociaux de la section : si vous ne le souhaitez pas, dites-le au chef de course. Plus de détails sur la page <a href="privacy.html">protection des données</a>.</p>""")),
    ]
    titolo = tr("Partecipare alle gite", "An Touren teilnehmen", "Taking part in trips", "Participer aux courses")
    regolamento = tr("Regolamento gite (PDF)", "Tourenreglement (PDF, italienisch)", "Trip regulations (PDF, in Italian)", "Règlement des courses (PDF, en italien)")
    body = page_hero([att_crumb(), (titolo, None)], titolo, testo_campo(testi("introduzioni")["partecipare"], "introduzione"),
                     extra=f"""<div class="actions"><a class="btn btn--primary" href="{GITE}">{t("gite")} <span class="arrow" aria-hidden="true">→</span></a><a class="btn btn--secondary" href="{REGOLAMENTO_GITE}">{regolamento}</a></div>""") + "\n\n" + "\n\n".join(sezioni) + f"""

{prima_di_partire()}

<section class="section" aria-label="{tr("Regolamento gite", "Tourenreglement", "Trip regulations", "Règlement des courses")}">
<div class="container">
<div class="callout">
<p>{tr("<strong>Questa pagina riassume il regolamento gite</strong> approvato dal comitato il 31 marzo 2026. Vale per tutte le gite della sezione, compresi i gruppi Senior e giovani; per i corsi alcune regole possono cambiare.",
       "<strong>Diese Seite fasst das Tourenreglement zusammen</strong>, das der Vorstand am 31. März 2026 genehmigt hat. Es gilt für alle Touren der Sektion, auch für die Senioren- und die Jugendgruppe; für Kurse können einzelne Regeln abweichen. Massgebend ist der italienische Text.",
       "<strong>This page summarises the trip regulations</strong> approved by the committee on 31 March 2026. They apply to all the section’s trips, including the seniors and youth groups; some rules may differ for courses. The Italian text is binding.",
       "<strong>Cette page résume le règlement des courses</strong> approuvé par le comité le 31 mars 2026. Il s’applique à toutes les courses de la section, y compris les groupes Seniors et jeunesse ; pour les cours, certaines règles peuvent changer. Le texte italien fait foi.")}</p>
<div class="actions"><a class="btn btn--secondary" href="{REGOLAMENTO_GITE}">{regolamento}</a><a class="btn btn--secondary" href="documenti.html">{tr("Altri documenti", "Weitere Dokumente", "More documents", "Autres documents")}</a></div>
</div>
</div>
</section>

{subnav(ATT_MENU(), L("partecipare.html"))}"""
    body = body.replace('<section class="section"', '<section class="section section--fitta"')   # pagina lunga: meno spazio tra le sezioni
    return sezione_page("partecipare.html", titolo + " | CAS Ticino", tr(
        "Come partecipare alle gite del CAS Ticino: iscrizione e conferma su Droptour, requisiti, svolgimento, assicurazione, costi e foto, in breve dal regolamento gite.",
        "So nehmen Sie an den Touren der SAC-Sektion Ticino teil: Anmeldung und Bestätigung auf Droptour, Voraussetzungen, Ablauf, Versicherung, Kosten und Fotos, kurz aus dem Tourenreglement.",
        "How to take part in SAC Ticino Section trips: registration and confirmation on Droptour, requirements, conduct, insurance, costs and photos, in brief from the trip regulations.",
        "Comment participer aux courses du CAS Ticino : inscription et confirmation sur Droptour, conditions, déroulement, assurance, coûts et photos, en bref d’après le règlement des courses."),
        body, og="paesaggi/gruppo-ghiacciaio-2000")
