"""Home (index.html, una funzione per tutte le lingue) e testi tradotti di home e Chi siamo (TRADOTTE)."""
from comune import *
from pagine_capanne import HUTS
from pagine_media import NEWS, news_card
from pagine_attivita import prossime_gite


def banda_adesione(titolo, testo, bottone, href):
    """Home: banda «Diventa socio», bassa, con titolo e testo a sinistra e bottone a destra."""
    return f"""<section class="cta-band" id="adesione" aria-labelledby="adesione-h">
{pic("paesaggi/tramonto-larici", "", mobile="paesaggi/tramonto-larici-4x3", w=2000, h=1126)}
<div class="container">
<div class="cta-text">
<h2 id="adesione-h" class="h2">{titolo}</h2>
<p>{testo}</p>
</div>
<a class="btn btn--light" href="{href}">{bottone} <span class="arrow" aria-hidden="true">→</span></a>
</div>
</section>"""


def home():
    lang = LINGUA["lang"]
    tx = TRADOTTE.get(lang, {})
    nome = L("index.html")
    prossime = prossime_gite()
    if lang == "it":
        huts = schede_capanne(HUTS)
    else:
        huts = schede_capanne({"de": HUTS_DE, "en": HUTS_EN}[lang], tx["accesso"], f"{lang}/")
    n_annunci = len(mercatino_util.attivi())
    mercatino_conta = {0: "", 1: tr(" Un annuncio online.", " Ein Inserat online.", " One listing online.")}.get(
        n_annunci, tr(f" {n_annunci} annunci online.", f" {n_annunci} Inserate online.", f" {n_annunci} listings online."))
    corso_alt = {"it": "Cordata su una cresta di neve", "de": "Seilschaft auf einem Schneegrat", "en": "Rope team on a snow ridge"}[lang]

    html = head(tx.get("home_title", "CAS Ticino | Club Alpino Svizzero, Sezione Ticino"),
                tx.get("home_desc", "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età. Da oltre un secolo, la casa dell’alpinismo ticinese."),
                '<meta property="og:image" content="assets/img/paesaggi/sciatori-villaggio-2000.webp">\n<link rel="preload" as="image" href="assets/img/paesaggi/sciatori-villaggio-2000.webp" imagesrcset="assets/img/paesaggi/sciatori-villaggio-1000.webp 1000w, assets/img/paesaggi/sciatori-villaggio-2000.webp 2000w" imagesizes="100vw" media="(min-width: 701px)">\n')
    html += "\n<body>\n" + nav(nome) + f"""
<main id="contenuto">

<section class="hero" aria-labelledby="hero-h">
<div class="container">
<h1 id="hero-h" class="display">{tx.get("hero_h", 'In montagna<br>con <span class="accent">noi</span>.')}</h1>
<div class="hero-foot">
<div class="hero-testo">
<p class="lead">{tx.get("hero_lead", "Sei rifugi dal Passo Cristallina ai Denti della Vecchia, corsi tenuti da professionisti, un programma di gite per ogni età.")}</p>
{social()}
</div>
<div class="actions">
<a class="btn btn--primary" href="adesione.html">{tx.get("diventa", "Diventa socio")} <span class="arrow" aria-hidden="true">→</span></a>
<a class="btn btn--secondary" href="news.html">{tr("Ultime notizie", "Neuigkeiten", "Latest news")}</a>
</div>
</div>
</div>
<figure class="band">
{pic("paesaggi/sciatori-villaggio", tx.get("hero_alt", "Scialpinisti in salita verso un villaggio innevato"), mobile="paesaggi/sciatori-villaggio-4x3", w=2000, h=901, lazy=False, cls="pos-low")}
{credito()}
</figure>
</section>

<section class="section fascia-home" id="attivita" aria-labelledby="attivita-h">
<div class="container">
<div class="section-head">
<h2 id="attivita-h" class="h2">{tr("Fuori con la sezione", "Unterwegs mit der Sektion", "Out with the section")}</h2>
<p class="lead">{tr("Gite per tutti i livelli, un gruppo per ogni età e corsi per imparare a muoversi in montagna in sicurezza.",
                    "Touren für jedes Niveau, eine Gruppe für jedes Alter und Kurse, um sich sicher in den Bergen zu bewegen.",
                    "Trips for every level, a group for every age and courses to learn to move safely in the mountains.")}</p>
</div>
<div class="bento" id="gruppi">
<article class="tile tile--wide-top" data-reveal>
{img("attivita/gite-2x1", tr("Gruppo in vetta con vista sulle Alpi innevate", "Gruppe auf dem Gipfel mit Blick auf die verschneiten Alpen", "Group on a summit overlooking the snowy Alps"), 1400, 700)}
<div class="tile-body">
<h3 class="h2">{tr("Gite, escursioni e uscite della sezione", "Touren, Wanderungen und Ausflüge der Sektion", "The section’s trips, hikes and outings")}</h3>
<p>{tr("Escursionismo, alpinismo, sci alpinismo, racchette e arrampicata: il calendario completo con iscrizioni online.",
       "Wandern, Hochtouren, Skitouren, Schneeschuhtouren und Klettern: das ganze Programm mit Online-Anmeldung.",
       "Hiking, mountaineering, ski touring, snowshoeing and climbing: the full calendar with online registration.")}</p>
<div class="actions"><a class="btn btn--primary" href="{GITE}">{t("gite")}</a><a class="btn btn--ghost-light" href="foto.html">{tr("Foto e resoconti", "Fotos und Berichte", "Photos and reports")}</a></div>
</div>
</article>
<article class="tile tile--tall" data-reveal>
{img("attivita/giovani-3x4", tr("Giovane arrampicatore su una parete dei Denti della Vecchia", "Junger Kletterer an einer Wand der Denti della Vecchia", "Young climber on a face of the Denti della Vecchia"), 800, 1066)}
<div class="tile-body">
<span class="label">{tr("Gruppo giovani, dagli anni ’60", "Jugendgruppe, seit den 1960er-Jahren", "Youth group, since the 1960s")}</span>
<h3 class="h2">{tr("Giovani", "Jugend", "Youth")}</h3>
<p>{tr("Arrampicata, escursioni e settimane in montagna con monitori della sezione.", "Klettern, Wanderungen und Bergwochen mit Leitenden der Sektion.", "Climbing, hikes and mountain weeks with the section’s instructors.")}</p>
<div class="links"><a class="link" href="giovani.html">{tr("Gruppo giovani", "Jugendgruppe", "Youth group")}</a><a class="link" href="organizzazione.html#giovani">{tr("Organizzazione", "Organisation", "Organisation")}<span class="visually-hidden"> {tr("del gruppo giovani", "der Jugendgruppe", "of the youth group")}</span></a></div>
</div>
</article>
<article class="tile tile--bottom-1" data-reveal>
{img("attivita/senior-2x1", tr("Escursionisti su un sentiero di cresta", "Wandernde auf einem Gratweg", "Hikers on a ridge path"), 1000, 500)}
<div class="tile-body">
<span class="label">{tr("Gruppo senior, dal 1940", "Seniorengruppe, seit 1940", "Seniors group, since 1940")}</span>
<h3 class="h2">{tr("Senior", "Senioren", "Seniors")}</h3>
<p>{tr("Uscite settimanali con capigita esperti, al ritmo giusto e in buona compagnia, dalla Capriasca alle Alpi.",
       "Wöchentliche Touren mit erfahrenen Tourenleitenden, im richtigen Tempo und in guter Gesellschaft, von der Capriasca bis in die Alpen.",
       "Weekly outings with experienced trip leaders, at the right pace and in good company, from the Capriasca to the Alps.")}</p>
<div class="links"><a class="link" href="senior.html">{tr("Gruppo senior", "Seniorengruppe", "Seniors group")}</a><a class="link" href="organizzazione.html#senior">{tr("Organizzazione", "Organisation", "Organisation")}<span class="visually-hidden"> {tr("del gruppo senior", "der Seniorengruppe", "of the seniors group")}</span></a></div>
</div>
</article>
<article class="tile tile--bottom-2" id="corsi" data-reveal>
{img("corsi/alpinismo-4x5", corso_alt, 594, 742)}
<div class="tile-body">
<h3 class="h2">{tr("Corsi", "Kurse", "Courses")}</h3>
<p>{tr("Alpinismo, sci alpinismo, arrampicata, freeride e racchette: per imparare a muoversi in montagna in sicurezza.",
       "Hochtouren, Skitouren, Klettern, Freeride und Schneeschuhtouren: um zu lernen, sich sicher in den Bergen zu bewegen.",
       "Mountaineering, ski touring, climbing, freeride and snowshoeing: to learn to move safely in the mountains.")}</p>
<div class="links"><a class="link" href="corsi.html">{tr("Tutti i corsi", "Alle Kurse", "All courses")}</a><a class="link" href="partecipare.html">{tr("Partecipare alle gite", "An Touren teilnehmen", "Taking part in trips")}</a></div>
</div>
</article>
</div>
{f"""<div class="prossime" data-reveal>
<div class="section-row">
<h3 class="h3">{tr("Prossime gite", "Nächste Touren", "Upcoming trips")}</h3>
<a class="link" href="{GITE}">{tr("Tutto il programma", "Ganzes Programm", "Full programme")}</a>
</div>
<div class="scorri scorri--gite">
<div class="scorri-traccia">
{prossime}
</div>
</div>
</div>""" if prossime else ""}
</div>
</section>

<section class="section--surface fascia-home" id="capanne" aria-labelledby="capanne-h">
<div class="container">
<div class="section-head">
<h2 id="capanne-h" class="h2">{tx.get("capanne_h", "Sei capanne, un solo Ticino")}</h2>
<p class="lead">{tx.get("capanne_lead", "Sempre aperte, custodite quando i guardiani sono presenti. Prima di partire, contatta il guardiano per verificare presenza e condizioni della montagna.")}</p>
</div>
<div class="huts">
{huts}
</div>
<div class="callout callout--accent">
<p>{tr("<strong>Cerchiamo «api operaie».</strong> I volontari aiutano i guardiani ad aprire, chiudere e mantenere le capanne, e passano qualche bella serata in quota.",
       "<strong>Wir suchen «fleissige Bienen».</strong> Freiwillige helfen den Hüttenwarten beim Öffnen, Schliessen und Unterhalten der Hütten und verbringen schöne Abende in der Höhe.",
       "<strong>We are looking for «busy bees».</strong> Volunteers help the hut keepers open, close and maintain the huts, and spend some fine evenings up high.")}</p>
<a class="btn btn--light" href="volontariato.html">{tr("Voglio aiutare", "Ich helfe mit", "I want to help")} <span class="arrow" aria-hidden="true">→</span></a>
</div>
</div>
</section>

<section class="section fascia-home" id="servizi" aria-labelledby="servizi-h">
<div class="container">
<div class="section-head">
<h2 id="servizi-h" class="h2">{SERVIZI_MENU()}</h2>
<p class="lead">{tr("Materiale a noleggio per le tue uscite e un mercatino dell’attrezzatura tra soci.",
                    "Material zur Miete für Ihre Touren und ein Marktplatz für Ausrüstung unter Mitgliedern.",
                    "Equipment for hire for your outings and a gear market between members.")}</p>
</div>
<div class="pillars pillars--servizi" data-reveal>
<article class="pillar pillar--dark pillar--wide">
<h3>{tr("Noleggio materiale", "Materialvermietung", "Equipment hire")}</h3>
<p>{tr("Ramponi, piccozze, imbragature, set ARVA con sonda e pala e molto altro, a pochi franchi al giorno: per le gite della sezione e per le uscite private.",
       "Steigeisen, Pickel, Klettergurte, LVS-Sets mit Sonde und Schaufel und vieles mehr, für wenige Franken pro Tag: für die Touren der Sektion und für private Unternehmungen.",
       "Crampons, ice axes, harnesses, transceiver sets with probe and shovel and much more, for a few francs a day: for section trips and private outings.")}</p>
<a class="link" href="noleggio.html">{tr("Richiedi il materiale", "Material anfragen", "Request equipment")}</a>
</article>
<article class="pillar pillar--accent">
<h3>{tr("Mercatino", "Marktplatz", "Gear market")}</h3>
<p>{tr("Attrezzatura di montagna tra privati: vendo, cerco, regalo.", "Bergausrüstung unter Privaten: verkaufen, suchen, verschenken.", "Mountain gear between private people: for sale, wanted, free.")}{mercatino_conta}</p>
<a class="link" href="mercatino.html">{tr("Vedi gli annunci", "Zu den Inseraten", "See the listings")}</a>
</article>
</div>
</div>
</section>

<section class="section--surface fascia-home" id="news" aria-labelledby="news-h">
<div class="container">
<div class="section-row">
<h2 id="news-h" class="h2">News</h2>
<a class="link" href="news.html">{tr("Tutte le news", "Alle News", "All news")}</a>
</div>
<div class="scorri scorri--news" data-reveal>
<div class="scorri-traccia">
{chr(10).join(news_card(n) for n in NEWS[:8])}
</div>
</div>
</div>
</section>

{banda_adesione(tx.get("cta_h", "Sali con noi."), tx.get("cta_p", "Tariffe ridotte nelle capanne CAS di tutta la Svizzera, corsi, gite e una comunità che ama la montagna quanto te."), tx.get("diventa", "Diventa socio"), "adesione.html")}

</main>
""" + footer()
    return pubblica(nome, html)


# ------------------------------------------------------------------ versioni tradotte (de/, en/)
# Solo La Sezione, le capanne e Adesione sono tradotte; news, attività, media e PDF restano in italiano.
# I testi sono scritti con i percorsi dalla radice del sito; i link alle pagine tradotte passano da L() (de/…, en/…).
# Home, Introduzione, Sede e Adesione hanno un testo proprio per lingua in TRADOTTE; le altre pagine della sezione
# usano le stesse funzioni dell'italiano (comitato(), storia()…), con tr() e i dizionari *_DE / *_EN.

TRADOTTE = {
    "de": dict(
        # home
        home_title="CAS Ticino | Schweizer Alpen-Club, Sektion Ticino",
        home_desc="Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter. Seit über hundert Jahren das Zuhause des Tessiner Alpinismus.",
        hero_h="In die Berge<br>mit <span class=\"accent\">uns</span>.",
        hero_lead="Sechs Hütten vom Cristallinapass bis zu den Denti della Vecchia, Kurse mit Profis und ein Tourenprogramm für jedes Alter.",
        diventa="Mitglied werden",
        hero_alt="Skitourengeher im Aufstieg zu einem verschneiten Dorf",
        cifre="Die Sektion in Zahlen",
        sezione="Die Sektion",
        capanne_h="Sechs Hütten, ein Tessin",
        capanne_lead="Immer offen, bewartet, wenn die Hüttenwarte da sind. Melden Sie sich vor dem Aufbruch beim Hüttenwart, um Anwesenheit und Verhältnisse am Berg zu prüfen.",
        accesso="Zugang ab",
        cta_h="Kommen Sie mit.",
        cta_p="Günstigere Preise in den SAC-Hütten der ganzen Schweiz, Kurse, Touren und eine Gemeinschaft, die die Berge so liebt wie Sie.",
        # introduzione
        intro_crumb="Über uns", intro_h="Die Sektion",
        intro_lead="Am 11. April 1886 in Bellinzona gegründet, zählt die Sektion Ticino des Schweizer Alpen-Clubs fast 3000 Mitglieder und bietet ein vielfältiges Programm für jedes Alter: von den Jüngsten bis zu den Senioren.",
        intro_alt="Eine Gruppe Bergsteiger unterwegs auf einem Gletscher",
        stat_intro=["am 11. April in Bellinzona gegründet", "Mitglieder, von den Jüngsten bis zu den Senioren", "Hütten im Besitz der Sektion", "Ressorts neben dem Vorstand"],
        cosa_h="In den Bergen,<br>zu jeder Jahreszeit",
        alt_cresta="Bergsteiger auf einem Felsgrat",
        discipline_h="Disziplinen", discipline_p="Wandern, Bergsteigen, Klettern, Skitouren, Schneeschuhwandern und Eisklettern.",
        inizia_h="Für Einsteiger", inizia_p="Einführungskurse in Bergsteigen, Skitouren, Schneeschuhwandern und Klettern im Gelände.",
        vedi_corsi="Zu den Kursen",
        alt_montebar="Die Capanna Monte Bar",
        capanne_h3="Hütten", capanne_p="Die Sektion besitzt sechs Hütten: {huts}.", e="und",
        oltre_h="Mehr als Sport", oltre_p="Sie koordiniert die Bergrettung im Sottoceneri, setzt sich für den Schutz der alpinen Umwelt ein und fördert die Bergkultur.",
        come_h="So funktioniert es",
        come_p="Ein <a href=\"de/comitato.html\">Vorstand</a> koordiniert die verschiedenen Aktivitäten, unterstützt von fünf <a href=\"de/organizzazione.html\">Ressorts</a> und der Freiwilligenarbeit der Mitglieder.",
        alt_racchette="Verschneiter Grat über einem Nebelmeer",
        com_h="Kommunikation", com_p="Tourenprogramm, Website, ein halbjährliches Bulletin und das Jahrbuch, das vom Leben der Sektion erzählt (auf Italienisch).",
        doc_h="Statuten, Vision und Strategie, Organigramm",
        doc_p="Die massgebenden Dokumente der Sektion, als PDF auf Italienisch. Weitere finden Sie auf der Seite <a href=\"documenti.html\">Dokumente</a>.",
        statuto="Statuten", visione="Vision und Strategie", organigramma="Organigramm",
        intro_title="Die Sektion | CAS Ticino",
        intro_desc="Die Sektion Ticino des Schweizer Alpen-Clubs: 1886 gegründet, fast 3000 Mitglieder, sechs Hütten, Kurse, Touren und Aktivitäten für jedes Alter.",
    ),
    "en": dict(
        home_title="CAS Ticino | Swiss Alpine Club, Ticino Section",
        home_desc="Six huts from the Cristallina Pass to the Denti della Vecchia, courses run by professionals and a trip programme for all ages. For more than a century, the home of mountaineering in Ticino.",
        hero_h="Into the mountains<br>with <span class=\"accent\">us</span>.",
        hero_lead="Six huts from the Cristallina Pass to the Denti della Vecchia, courses run by professionals and a trip programme for all ages.",
        diventa="Become a member",
        hero_alt="Ski tourers climbing towards a snow-covered village",
        cifre="The section in numbers",
        sezione="The Section",
        capanne_h="Six huts, one Ticino",
        capanne_lead="Always open, staffed when the hut keepers are there. Check with the hut keeper before you set out, to make sure they are there and to ask about conditions in the mountains.",
        accesso="Access from",
        cta_h="Come with us.",
        cta_p="Lower rates in SAC huts all over Switzerland, courses, trips and a community that loves the mountains as much as you do.",
        intro_crumb="About us", intro_h="The section",
        intro_lead="Founded in Bellinzona on 11 April 1886, the Ticino Section of the Swiss Alpine Club has almost 3000 members and offers a varied programme for all ages: from the youngest to seniors.",
        intro_alt="A group of climbers walking on a glacier",
        stat_intro=["founded in Bellinzona on 11 April", "members, from the youngest to seniors", "huts owned by the section", "departments alongside the committee"],
        cosa_h="In the mountains,<br>in every season",
        alt_cresta="Climbers on a rocky ridge",
        discipline_h="Disciplines", discipline_p="Hiking, mountaineering, climbing, ski touring, snowshoeing and ice climbing.",
        inizia_h="For beginners", inizia_p="Introductory courses in mountaineering, ski touring, snowshoeing and outdoor climbing.",
        vedi_corsi="See the courses",
        alt_montebar="Capanna Monte Bar",
        capanne_h3="Huts", capanne_p="The section owns six huts: {huts}.", e="and",
        oltre_h="Beyond sport", oltre_p="It coordinates mountain rescue in the Sottoceneri, works to protect the alpine environment and promotes mountain culture.",
        come_h="How it works",
        come_p="A <a href=\"en/comitato.html\">committee</a> coordinates the various activities, supported by five <a href=\"en/organizzazione.html\">departments</a> and the volunteer work of the members.",
        alt_racchette="Snowy ridge above a sea of clouds",
        com_h="Communication", com_p="Trip programme, website, a half-yearly bulletin and the yearbook that tells the story of the section (in Italian).",
        doc_h="Statutes, vision and strategy, organisation chart",
        doc_p="The section’s key documents, as PDFs in Italian. You will find more on the <a href=\"documenti.html\">Documents</a> page.",
        statuto="Statutes", visione="Vision and strategy", organigramma="Organisation chart",
        intro_title="The section | CAS Ticino",
        intro_desc="The Ticino Section of the Swiss Alpine Club: founded in 1886, almost 3000 members, six huts, courses, trips and activities for all ages.",
    ),
}


def tx_tradotte():
    return TRADOTTE[LINGUA["lang"]]
