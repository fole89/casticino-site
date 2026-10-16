"""Adesione, protezione dei dati (privacy.html) e pagina offline del sito installabile."""
from comune import *
from pagine_capanne import HUTS, tc


def adesione():
    d = testi("adesione")
    cards = "\n".join(f"""<article class="price">
<h3 class="h3">{testo_campo(q, "nome")}</h3>
<p>{testo_campo(q, "chi")}</p>
<div class="amount"><small>CHF</small>{esc(q["quota"])}</div>
<p class="small">{tr("+ CHF {} alla prima iscrizione", "+ CHF {} beim ersten Beitritt", "+ CHF {} when you first join", "+ CHF {} à la première inscription").format(esc(q["tassa"]))}</p>
</article>""" for q in d["quote"])
    rows = [(testo_campo(v, "etichetta"), testo_md(v, "testo", in_riga=True)) for v in d["vantaggi"]]
    join = tr("https://portal.sac-cas.ch/it/groups/6783/self_registration", "https://portal.sac-cas.ch/de/groups/6783/self_registration",
              "https://portal.sac-cas.ch/it/groups/6783/self_registration",
              "https://portal.sac-cas.ch/fr/groups/6783/self_registration")
    iscriviti = tr("Iscriviti sul sito del CAS", "Auf der SAC-Website beitreten", "Join on the SAC website", "S’inscrire sur le site du CAS")
    body = page_hero([(tr("Adesione", "Mitgliedschaft", "Membership", "Adhésion"), None)], testo_campo(d, "titolo"), testo_campo(d, "introduzione"),
                     f'<div class="actions hero-actions"><a class="btn btn--primary" href="{join}">{iscriviti} <span class="arrow" aria-hidden="true">→</span></a></div>') + f"""

<figure class="band">
{pic("paesaggi/gruppo-ghiacciaio", tr("Gruppo di alpinisti in cammino su un ghiacciaio", "Eine Gruppe Bergsteiger unterwegs auf einem Gletscher", "A group of mountaineers walking on a glacier", "Un groupe d’alpinistes en marche sur un glacier"),
     mobile="paesaggi/gruppo-ghiacciaio-4x3", w=2000, h=1500, lazy=False, cls="pos-low")}
{credito()}
</figure>

<section class="section" aria-labelledby="quote-h">
<div class="container">
<div class="section-head"><h2 id="quote-h" class="h2">{tr("Quote annuali", "Jahresbeiträge", "Annual fees", "Cotisations annuelles")}</h2></div>
<div class="prices" data-reveal>
{cards}
</div>
<p class="note">{testo_campo(d, "nota")}</p>
</div>
</section>

<section class="section--surface" aria-labelledby="vantaggi-h">
<div class="container detail">
<div class="detail-intro">
<h2 id="vantaggi-h" class="h2">{tr("Cosa ricevi", "Ihre Vorteile", "Your benefits", "Vos avantages")}</h2>
<div><a class="btn btn--primary" href="{join}">{iscriviti} <span class="arrow" aria-hidden="true">→</span></a></div>
</div>
<div data-reveal>
{facts(rows)}
</div>
</div>
</section>"""
    return sezione_page("adesione.html", f'{testo_campo(d, "titolo", semplice=True)} | CAS Ticino',
                        tr("Diventa socio della Sezione Ticino del Club Alpino Svizzero: quote annuali per singoli, famiglie e giovani, e vantaggi per i soci.",
                           "Werden Sie Mitglied der Sektion Ticino des Schweizer Alpen-Clubs: Jahresbeiträge für Einzelne, Familien und Jugendliche, und die Vorteile für Mitglieder.",
                           "Become a member of the Ticino Section of the Swiss Alpine Club: annual fees for individuals, families and young people, and the benefits for members.",
                           "Devenez membre de la Section Ticino du Club Alpin Suisse : cotisations annuelles pour individuels, familles et jeunes, et avantages pour les membres."),
                        body, og="paesaggi/gruppo-ghiacciaio-2000")


# ------------------------------------------------------------------ protezione dei dati (privacy.html, de/, fr/, en/)
# Testo per lingua: titolo, descrizione, sommario e corpo (HTML, percorsi dalla radice). Tenere allineate le quattro versioni
# quando il sito cambia (nuovi servizi esterni, cookie, moduli…) e aggiornare PRIVACY_AGGIORNATA.

PRIVACY_AGGIORNATA = {"it": "ottobre 2026", "de": "Oktober 2026", "fr": "octobre 2026", "en": "October 2026"}

PRIVACY = {
    "it": dict(
        title="Protezione dei dati | CAS Ticino", h1="Protezione dei dati",
        desc="Informativa sulla protezione dei dati del sito del CAS Ticino: quali dati si trattano, cookie, servizi esterni e i tuoi diritti.",
        lead="Il sito del CAS Ticino non usa cookie né strumenti di statistica. Qui trovi quali dati vengono comunque trattati quando lo visiti o ci scrivi, da chi e perché.",
        corpo="""<h2>Chi è responsabile</h2>
<p>Club Alpino Svizzero, Sezione Ticino<br>Casella postale 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>Ci atteniamo alla legge federale sulla protezione dei dati (LPD).</p>

<h2>Visita del sito</h2>
<p>Il sito è ospitato da GitHub Pages (GitHub Inc., USA). Come ogni server web, GitHub registra per ogni visita l’indirizzo IP, la data e l’ora, la pagina richiesta e il tipo di browser, per far funzionare il servizio e per la sicurezza. La sezione non riceve questi dati. GitHub aderisce al Data Privacy Framework Svizzera–USA; i dettagli sono nella <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">dichiarazione sulla privacy di GitHub</a> (in inglese).</p>

<h2>Cookie e memoria del browser</h2>
<p>Il sito non imposta cookie e non usa strumenti di statistica, pubblicità o profilazione. I caratteri tipografici sono caricati dal sito stesso. Il programma gite tiene per 10 minuti l’elenco delle gite nella memoria della scheda del browser (sessionStorage), per aprire più in fretta il dettaglio di una gita: non contiene dati personali e si cancella chiudendo la scheda. Se chiudi l’avviso in cima alle pagine, il browser ricorda solo quale avviso hai chiuso (localStorage), per non mostrartelo di nuovo: resta sul tuo dispositivo e non viene inviato a nessuno. Per aprire il sito più in fretta e anche senza rete (per esempio se lo aggiungi alla schermata Home), il browser tiene in memoria alcune pagine, immagini e file del sito (service worker e cache): restano sul tuo dispositivo e si cancellano con i dati del sito nelle impostazioni del browser.</p>

<h2>Programma gite e foto</h2>
<p>Il programma gite e le foto delle uscite vengono caricati da Droptour (ssl.dropnet.ch, in Svizzera), il servizio con cui la sezione gestisce gite e iscrizioni: aprendo queste pagine il tuo browser si collega a Droptour, che riceve il tuo indirizzo IP. L’iscrizione alle gite avviene su Droptour; i dati che inserisci lì servono a organizzare la gita e sono visibili ai capigita.</p>

<h2>Facebook</h2>
<p>Nelle pagine delle capanne i post da Facebook vengono caricati solo se clicchi «Mostra i post». Prima di quel clic a Facebook non arriva nulla; dopo, Meta Platforms riceve dati sulla tua visita (tra cui l’indirizzo IP) e può impostare cookie, secondo la sua <a href="https://www.facebook.com/privacy/policy/" rel="noopener">informativa sulla privacy</a>. I link a Instagram, Facebook, hut-reservation.org e ad altri siti sono semplici link: i tuoi dati li tratta il sito che apri.</p>

<h2>Contatti e annunci</h2>
<p>Se ci scrivi per e-mail usiamo il tuo messaggio solo per rispondere e per dare seguito alla richiesta (per esempio inoltrandolo al custode di una capanna o al responsabile di un corso). Gli annunci del Mercatino vengono pubblicati con il nome e il contatto che indichi tu e restano online fino alla scadenza; puoi chiederne la rimozione in ogni momento.</p>

<h2 id="notifiche">Notifiche</h2>
<p>Se attivi le notifiche (in fondo alle pagine), il browser chiede il tuo permesso e crea un indirizzo di notifica anonimo: non contiene nome, e-mail o numero di telefono. Lo salviamo con la lingua della pagina in un piccolo servizio della sezione su Cloudflare Workers (Cloudflare Inc., USA; dati salvati in Europa), solo per inviarti le notizie importanti della sezione. Le notifiche passano dal servizio del tuo browser o telefono (Google, Apple, Mozilla o Microsoft). Con «Disattiva le notifiche», o togliendo il permesso nelle impostazioni, l’indirizzo viene cancellato; quelli non più validi li cancelliamo da soli.</p>
<h2 id="noleggio">Noleggio materiale</h2>
<p>Il modulo del noleggio invia nome, e-mail, telefono, note, date e materiale scelto a un piccolo servizio della sezione su Cloudflare Workers (Cloudflare Inc., USA; dati salvati in Europa). Li vede solo il responsabile del noleggio, che li usa per confermare la richiesta e per il ritiro e la riconsegna. Le e-mail di ricevuta e di conferma partono tramite Brevo (Francia). Le richieste vengono cancellate 12 mesi dopo la fine del noleggio. Per proteggere il modulo dai programmi automatici, quando inizi a compilarlo viene caricato Cloudflare Turnstile, che riceve l’indirizzo IP e alcune informazioni tecniche sul browser, secondo l’<a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">informativa sulla privacy di Cloudflare</a> (in inglese). Cloudflare aderisce al Data Privacy Framework Svizzera–USA.</p>

<h2>Persone sul sito</h2>
<p>Nomi, foto e presentazioni dei membri del comitato, dei dicasteri e dei capigita sono pubblicati con il loro consenso. Nelle news e nei resoconti delle gite possono comparire foto di partecipanti. Se vuoi che una tua foto o il tuo nome venga tolto, scrivici.</p>

<h2>Soci</h2>
<p>L’adesione e i dati dei soci sono gestiti con il Club Alpino Svizzero (portal.sac-cas.ch), secondo la sua <a href="https://www.sac-cas.ch/it/datenschutz/" rel="noopener">informativa sulla protezione dei dati</a>.</p>

<h2>I tuoi diritti</h2>
<p>Puoi chiedere quali dati abbiamo su di te, farli correggere o cancellare e opporti al loro uso, scrivendo a <a href="mailto:info@casticino.ch">info@casticino.ch</a>. Puoi anche rivolgerti all’<a href="https://www.edoeb.admin.ch/it" rel="noopener">Incaricato federale della protezione dei dati e della trasparenza (IFPDT)</a>.</p>"""),
    "de": dict(
        title="Datenschutz | CAS Ticino", h1="Datenschutz",
        desc="Datenschutzerklärung der Website der SAC-Sektion Ticino: welche Daten bearbeitet werden, Cookies, externe Dienste und Ihre Rechte.",
        lead="Die Website der Sektion Ticino verwendet weder Cookies noch Statistik-Werkzeuge. Hier steht, welche Daten trotzdem bearbeitet werden, wenn Sie sie besuchen oder uns schreiben, von wem und weshalb.",
        corpo="""<h2>Verantwortlich</h2>
<p>Schweizer Alpen-Club SAC, Sektion Ticino<br>Postfach 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>Wir halten uns an das Bundesgesetz über den Datenschutz (DSG).</p>

<h2>Besuch der Website</h2>
<p>Die Website wird von GitHub Pages (GitHub Inc., USA) betrieben. Wie jeder Webserver speichert GitHub bei jedem Besuch die IP-Adresse, Datum und Uhrzeit, die aufgerufene Seite und den Browsertyp, für den Betrieb und die Sicherheit des Dienstes. Die Sektion erhält diese Daten nicht. GitHub ist dem Swiss-U.S. Data Privacy Framework beigetreten; Einzelheiten in der <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">Datenschutzerklärung von GitHub</a>.</p>

<h2>Cookies und Browserspeicher</h2>
<p>Die Website setzt keine Cookies und verwendet keine Werkzeuge für Statistik, Werbung oder Profiling. Die Schriften werden von der Website selbst geladen. Das Tourenprogramm speichert die Tourenliste 10 Minuten lang im Speicher des Browser-Tabs (sessionStorage), damit die Einzelheiten einer Tour schneller erscheinen: Sie enthält keine Personendaten und wird beim Schliessen des Tabs gelöscht. Wenn Sie den Hinweis oben auf den Seiten schliessen, merkt sich der Browser nur, welchen Hinweis Sie geschlossen haben (localStorage), damit er nicht wieder erscheint: Die Angabe bleibt auf Ihrem Gerät und wird an niemanden gesendet. Damit die Website schneller und auch ohne Netz erscheint (zum Beispiel, wenn Sie sie zum Home-Bildschirm hinzufügen), speichert der Browser einige Seiten, Bilder und Dateien der Website (Service Worker und Cache): Sie bleiben auf Ihrem Gerät und werden mit den Website-Daten in den Browser-Einstellungen gelöscht.</p>

<h2>Tourenprogramm und Fotos</h2>
<p>Das Tourenprogramm und die Tourenfotos werden von Droptour geladen (ssl.dropnet.ch, Schweiz), dem Dienst, mit dem die Sektion Touren und Anmeldungen verwaltet: Beim Öffnen dieser Seiten verbindet sich Ihr Browser mit Droptour, das Ihre IP-Adresse erhält. Die Anmeldung zu den Touren erfolgt auf Droptour; die dort eingegebenen Daten dienen der Organisation der Tour und sind für die Tourenleitenden sichtbar.</p>

<h2>Facebook</h2>
<p>Auf den Hüttenseiten werden die Facebook-Beiträge erst geladen, wenn Sie auf «Beiträge anzeigen» klicken. Vorher geht nichts an Facebook; danach erhält Meta Platforms Daten über Ihren Besuch (darunter die IP-Adresse) und kann Cookies setzen, gemäss seiner <a href="https://www.facebook.com/privacy/policy/" rel="noopener">Datenschutzrichtlinie</a>. Links zu Instagram, Facebook, hut-reservation.org und anderen Websites sind einfache Links: Ihre Daten bearbeitet dann die Website, die Sie öffnen.</p>

<h2>Kontakt und Inserate</h2>
<p>Wenn Sie uns per E-Mail schreiben, verwenden wir Ihre Nachricht nur, um zu antworten und Ihr Anliegen zu bearbeiten (zum Beispiel durch Weiterleitung an das Hüttenteam oder an die Kursleitung). Inserate auf dem Mercatino werden mit dem Namen und dem Kontakt veröffentlicht, die Sie angeben, und bleiben bis zum Ablaufdatum online; Sie können jederzeit die Entfernung verlangen.</p>

<h2 id="notifiche">Mitteilungen</h2>
<p>Wenn Sie Mitteilungen einschalten (unten auf den Seiten), fragt der Browser nach Ihrer Erlaubnis und erstellt eine anonyme Mitteilungsadresse: Sie enthält weder Name noch E-Mail noch Telefonnummer. Wir speichern sie mit der Sprache der Seite in einem kleinen Dienst der Sektion auf Cloudflare Workers (Cloudflare Inc., USA; Daten in Europa gespeichert), nur um Ihnen wichtige Neuigkeiten der Sektion zu senden. Die Mitteilungen laufen über den Dienst Ihres Browsers oder Telefons (Google, Apple, Mozilla oder Microsoft). Mit «Mitteilungen ausschalten» oder wenn Sie die Erlaubnis in den Einstellungen entziehen, wird die Adresse gelöscht; ungültig gewordene Adressen löschen wir selbst.</p>
<h2 id="noleggio">Materialvermietung</h2>
<p>Das Formular der Materialvermietung sendet Name, E-Mail, Telefon, Bemerkungen, Daten und das gewählte Material an einen kleinen Dienst der Sektion auf Cloudflare Workers (Cloudflare Inc., USA; Daten in Europa gespeichert). Sie sind nur für die Materialverantwortlichen sichtbar, die sie für die Bestätigung der Anfrage sowie für Abholung und Rückgabe verwenden. Die Empfangs- und Bestätigungs-E-Mails werden über Brevo (Frankreich) verschickt. Die Anfragen werden 12 Monate nach Ende der Miete gelöscht. Zum Schutz des Formulars vor automatisierten Programmen wird Cloudflare Turnstile geladen, sobald Sie mit dem Ausfüllen beginnen; Cloudflare erhält dabei die IP-Adresse und einige technische Angaben zum Browser, gemäss der <a href="https://www.cloudflare.com/de-de/privacypolicy/" rel="noopener">Datenschutzrichtlinie von Cloudflare</a>. Cloudflare ist dem Swiss-U.S. Data Privacy Framework beigetreten.</p>

<h2>Personen auf der Website</h2>
<p>Namen, Fotos und Vorstellungen der Mitglieder von Vorstand und Ressorts sowie der Tourenleitenden werden mit ihrem Einverständnis veröffentlicht. In News und Tourenberichten können Fotos von Teilnehmenden erscheinen. Wenn ein Foto von Ihnen oder Ihr Name entfernt werden soll, schreiben Sie uns.</p>

<h2>Mitglieder</h2>
<p>Mitgliedschaft und Mitgliederdaten werden mit dem Schweizer Alpen-Club verwaltet (portal.sac-cas.ch), gemäss dessen <a href="https://www.sac-cas.ch/de/meta/datenschutz/" rel="noopener">Datenschutzerklärung</a>.</p>

<h2>Ihre Rechte</h2>
<p>Sie können Auskunft über Ihre Daten verlangen, sie berichtigen oder löschen lassen und der Bearbeitung widersprechen: Schreiben Sie an <a href="mailto:info@casticino.ch">info@casticino.ch</a>. Sie können sich auch an den <a href="https://www.edoeb.admin.ch/de" rel="noopener">Eidgenössischen Datenschutz- und Öffentlichkeitsbeauftragten (EDÖB)</a> wenden.</p>"""),
    "fr": dict(
        title="Protection des données | CAS Ticino", h1="Protection des données",
        desc="Déclaration de protection des données du site du CAS Ticino : quelles données sont traitées, cookies, services externes et vos droits.",
        lead="Le site du CAS Ticino n’utilise ni cookies ni outils de statistique. Vous trouverez ici quelles données sont tout de même traitées quand vous le visitez ou nous écrivez, par qui et pourquoi.",
        corpo="""<h2>Responsable</h2>
<p>Club Alpin Suisse CAS, Section Ticino<br>Case postale 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>Nous respectons la loi fédérale sur la protection des données (LPD).</p>

<h2>Visite du site</h2>
<p>Le site est hébergé par GitHub Pages (GitHub Inc., États-Unis). Comme tout serveur web, GitHub enregistre pour chaque visite l’adresse IP, la date et l’heure, la page demandée et le type de navigateur, pour faire fonctionner le service et pour la sécurité. La section ne reçoit pas ces données. GitHub adhère au Swiss-U.S. Data Privacy Framework ; les détails figurent dans la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">déclaration de confidentialité de GitHub</a> (en anglais).</p>

<h2>Cookies et mémoire du navigateur</h2>
<p>Le site ne place pas de cookies et n’utilise pas d’outils de statistique, de publicité ou de profilage. Les polices de caractères sont chargées depuis le site lui-même. Le programme des courses garde la liste des courses pendant 10 minutes dans la mémoire de l’onglet du navigateur (sessionStorage), pour ouvrir plus vite le détail d’une course : elle ne contient pas de données personnelles et s’efface à la fermeture de l’onglet. Si vous fermez l’avis en haut des pages, le navigateur retient seulement quel avis vous avez fermé (localStorage), pour ne plus vous le montrer : cette information reste sur votre appareil et n’est envoyée à personne. Pour ouvrir le site plus vite et même sans réseau (par exemple si vous l’ajoutez à l’écran d’accueil), le navigateur garde en mémoire certaines pages, images et fichiers du site (service worker et cache) : ils restent sur votre appareil et s’effacent avec les données du site dans les réglages du navigateur.</p>

<h2>Programme des courses et photos</h2>
<p>Le programme des courses et les photos des sorties sont chargés depuis Droptour (ssl.dropnet.ch, en Suisse), le service avec lequel la section gère les courses et les inscriptions : en ouvrant ces pages, votre navigateur se connecte à Droptour, qui reçoit votre adresse IP. L’inscription aux courses se fait sur Droptour ; les données que vous y saisissez servent à organiser la course et sont visibles pour les chefs de course.</p>

<h2>Facebook</h2>
<p>Sur les pages des cabanes, les publications de Facebook ne sont chargées que si vous cliquez sur « Afficher les publications ». Avant ce clic, rien n’est envoyé à Facebook ; ensuite, Meta Platforms reçoit des données sur votre visite (dont l’adresse IP) et peut placer des cookies, selon sa <a href="https://www.facebook.com/privacy/policy/" rel="noopener">politique de confidentialité</a>. Les liens vers Instagram, Facebook, hut-reservation.org et d’autres sites sont de simples liens : vos données sont alors traitées par le site que vous ouvrez.</p>

<h2>Contacts et annonces</h2>
<p>Si vous nous écrivez par e-mail, nous utilisons votre message uniquement pour vous répondre et donner suite à votre demande (par exemple en le transmettant au gardien d’une cabane ou au responsable d’un cours). Les annonces du Mercatino sont publiées avec le nom et le contact que vous indiquez et restent en ligne jusqu’à leur échéance ; vous pouvez demander leur retrait à tout moment.</p>

<h2 id="notifiche">Notifications</h2>
<p>Si vous activez les notifications (en bas des pages), le navigateur vous demande votre autorisation et crée une adresse de notification anonyme : elle ne contient ni nom, ni e-mail, ni numéro de téléphone. Nous l’enregistrons, avec la langue de la page, dans un petit service de la section sur Cloudflare Workers (Cloudflare Inc., États-Unis ; données stockées en Europe), uniquement pour vous envoyer les nouvelles importantes de la section. Les notifications passent par le service de votre navigateur ou de votre téléphone (Google, Apple, Mozilla ou Microsoft). Avec « Désactiver les notifications », ou en retirant l’autorisation dans les réglages, l’adresse est effacée ; celles qui ne sont plus valables sont effacées automatiquement.</p>
<h2 id="noleggio">Location de matériel</h2>
<p>Le formulaire de location envoie le nom, l’e-mail, le téléphone, les remarques, les dates et le matériel choisi à un petit service de la section sur Cloudflare Workers (Cloudflare Inc., États-Unis ; données stockées en Europe). Seul le responsable de la location les voit et les utilise pour confirmer la demande ainsi que pour le retrait et le retour. Les e-mails d’accusé de réception et de confirmation sont envoyés par Brevo (France). Les demandes sont effacées 12 mois après la fin de la location. Pour protéger le formulaire des programmes automatiques, Cloudflare Turnstile est chargé quand vous commencez à le remplir ; Cloudflare reçoit alors l’adresse IP et quelques informations techniques sur le navigateur, selon la <a href="https://www.cloudflare.com/fr-fr/privacypolicy/" rel="noopener">politique de confidentialité de Cloudflare</a>. Cloudflare adhère au Swiss-U.S. Data Privacy Framework.</p>

<h2>Personnes sur le site</h2>
<p>Les noms, photos et présentations des membres du comité, des départements et des chefs de course sont publiés avec leur accord. Des photos de participants peuvent paraître dans les news et les récits de courses. Si vous souhaitez qu’une photo de vous ou votre nom soit retiré, écrivez-nous.</p>

<h2>Membres</h2>
<p>L’adhésion et les données des membres sont gérées avec le Club Alpin Suisse (portal.sac-cas.ch), selon sa <a href="https://www.sac-cas.ch/fr/meta/protection-des-donnees/" rel="noopener">déclaration de protection des données</a>.</p>

<h2>Vos droits</h2>
<p>Vous pouvez demander quelles données nous avons sur vous, les faire corriger ou effacer et vous opposer à leur utilisation, en écrivant à <a href="mailto:info@casticino.ch">info@casticino.ch</a>. Vous pouvez aussi vous adresser au <a href="https://www.edoeb.admin.ch/fr" rel="noopener">Préposé fédéral à la protection des données et à la transparence (PFPDT)</a>.</p>"""),
    "en": dict(
        title="Privacy policy | CAS Ticino", h1="Privacy policy",
        desc="Privacy policy of the website of the Ticino Section of the Swiss Alpine Club: what data is processed, cookies, external services and your rights.",
        lead="The Ticino Section’s website uses no cookies and no analytics tools. This page explains what data is nevertheless processed when you visit it or write to us, by whom and why.",
        corpo="""<h2>Who is responsible</h2>
<p>Swiss Alpine Club SAC, Ticino Section<br>PO Box 112, 6998 Monteggio 2<br><a href="mailto:info@casticino.ch">info@casticino.ch</a></p>
<p>We comply with the Swiss Federal Act on Data Protection (FADP).</p>

<h2>Visiting the website</h2>
<p>The website is hosted by GitHub Pages (GitHub Inc., USA). Like any web server, GitHub logs the IP address, date and time, page requested and browser type of each visit, to run the service and for security. The Section does not receive this data. GitHub participates in the Swiss-U.S. Data Privacy Framework; details are in <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener">GitHub’s privacy statement</a>.</p>

<h2>Cookies and browser storage</h2>
<p>The website sets no cookies and uses no analytics, advertising or profiling tools. Fonts are served by the website itself. The trip programme keeps the list of trips for 10 minutes in the browser tab’s storage (sessionStorage), so that a trip’s details open faster: it contains no personal data and is deleted when you close the tab. If you close the notice at the top of the pages, your browser only remembers which notice you closed (localStorage), so as not to show it again: this stays on your device and is not sent to anyone. To open the site faster and also without a connection (for example if you add it to your home screen), your browser keeps some of the site’s pages, images and files in its storage (service worker and cache): they stay on your device and are deleted with the site data in your browser settings.</p>

<h2>Trip programme and photos</h2>
<p>The trip programme and the trip photos are loaded from Droptour (ssl.dropnet.ch, Switzerland), the service the Section uses to manage trips and registrations: when you open these pages, your browser connects to Droptour, which receives your IP address. Registration for trips takes place on Droptour; the data you enter there is used to organise the trip and is visible to the trip leaders.</p>

<h2>Facebook</h2>
<p>On the hut pages, posts from Facebook are only loaded if you click «Show posts». Before that click nothing is sent to Facebook; afterwards Meta Platforms receives data about your visit (including your IP address) and may set cookies, under its <a href="https://www.facebook.com/privacy/policy/" rel="noopener">privacy policy</a>. Links to Instagram, Facebook, hut-reservation.org and other websites are plain links: your data is then processed by the website you open.</p>

<h2>Contacts and listings</h2>
<p>If you e-mail us, we use your message only to reply and to deal with your request (for example by forwarding it to a hut keeper or to a course leader). Mercatino listings are published with the name and contact details you give us and stay online until they expire; you can ask for removal at any time.</p>

<h2 id="notifiche">Notifications</h2>
<p>If you turn on notifications (at the bottom of the pages), your browser asks for your permission and creates an anonymous notification address: it contains no name, e-mail or phone number. We store it, with the language of the page, in a small service run by the Section on Cloudflare Workers (Cloudflare Inc., USA; data stored in Europe), only to send you important news from the Section. Notifications pass through your browser’s or phone’s service (Google, Apple, Mozilla or Microsoft). With «Turn off notifications», or by withdrawing permission in your settings, the address is deleted; addresses that are no longer valid are deleted automatically.</p>
<h2 id="noleggio">Equipment hire</h2>
<p>The equipment hire form sends your name, e-mail, phone number, notes, dates and the equipment chosen to a small service run by the Section on Cloudflare Workers (Cloudflare Inc., USA; data stored in Europe). Only the equipment manager sees it, and uses it to confirm the request and for pick-up and return. Receipt and confirmation e-mails are sent through Brevo (France). Requests are deleted 12 months after the end of the hire. To protect the form from automated programs, Cloudflare Turnstile is loaded when you start filling it in; Cloudflare receives your IP address and some technical information about your browser, under <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener">Cloudflare’s privacy policy</a>. Cloudflare participates in the Swiss-U.S. Data Privacy Framework.</p>

<h2>People on the website</h2>
<p>Names, photos and introductions of the members of the committee, the departments and the trip leaders are published with their consent. Photos of participants may appear in the news and trip reports. If you would like a photo of you or your name removed, write to us.</p>

<h2>Members</h2>
<p>Membership and members’ data are managed with the Swiss Alpine Club (portal.sac-cas.ch), under its <a href="https://www.sac-cas.ch/en/meta/data-protection/" rel="noopener">privacy policy</a>.</p>

<h2>Your rights</h2>
<p>You can ask what data we hold about you, have it corrected or deleted, and object to its use, by writing to <a href="mailto:info@casticino.ch">info@casticino.ch</a>. You can also contact the <a href="https://www.edoeb.admin.ch/en" rel="noopener">Federal Data Protection and Information Commissioner (FDPIC)</a>.</p>"""),
}


def privacy():
    tx = PRIVACY[LINGUA["lang"]]
    agg = tr("Ultimo aggiornamento", "Letzte Änderung", "Last updated", "Dernière mise à jour") + ": " + PRIVACY_AGGIORNATA[LINGUA["lang"]]
    body = page_hero([(tx["h1"], None)], tx["h1"], tx["lead"]) + f"""

<section class="section section--tight" aria-label="{tr("Testo dell’informativa", "Text der Datenschutzerklärung", "Full policy", "Texte complet")}">
<div class="container article article--noimg">
<div class="prose">
{tx["corpo"]}
<p class="small">{agg}</p>
</div>
</div>
</section>"""
    return sezione_page("privacy.html", tx["title"], tx["desc"], body)


def offline_pagina():
    """Pagina mostrata dal service worker (sw.js, pwa.py) quando non c'è rete e la pagina chiesta non è salvata:
    le pagine che il telefono ha sempre (home, capanne, Partecipare, Soccorso) e i numeri d'emergenza."""
    huts = {"it": HUTS, "de": HUTS_DE, "fr": HUTS_FR, "en": HUTS_EN}[LINGUA["lang"]]
    links = [(tr("Home", "Startseite", "Home", "Accueil"), L("index.html"))]
    links += [(f'{tc("capanna")} {h[1]}' if h[0] != "baitadelluca.html" else h[1], L(h[0])) for h in huts]
    links += [(tr("Prima di partire", "Vor dem Aufbruch", "Before you set off", "Avant de partir"), L("partecipare.html") + "#prima-di-partire"),
              (tr("Soccorso", "Bergrettung", "Mountain rescue", "Secours en montagne"), L("soccorso.html"))]
    lista = "\n".join(f'<a href="{h}"><span>{x}</span></a>' for x, h in links)
    numeri = [("1414", tr("Rega, soccorso aereo", "Rega, Luftrettung", "Rega, air rescue", "Rega, sauvetage aérien")),
              ("144", tr("Ambulanza", "Sanitätsnotruf", "Ambulance", "Ambulance")),
              ("112", tr("Numero d’emergenza europeo", "Europäische Notrufnummer", "European emergency number", "Numéro d’urgence européen"))]
    numeri = "\n".join(f'<a href="tel:{n}"><strong class="num">{n}</strong><span>{x}</span></a>' for n, x in numeri)
    titolo = tr("Sei offline", "Sie sind offline", "You are offline", "Vous êtes hors ligne")
    body = page_hero([(titolo, None)], titolo, tr(
        "Senza connessione questa pagina non si può aprire. Restano consultabili le pagine già visitate e queste, salvate sul telefono.",
        "Ohne Verbindung lässt sich diese Seite nicht öffnen. Abrufbar bleiben die schon besuchten Seiten und diese, auf dem Telefon gespeichert.",
        "This page cannot be opened without a connection. Pages you have already visited are still available, and so are these, saved on your phone.",
        "Sans connexion, cette page ne peut pas s’ouvrir. Les pages déjà visitées restent consultables, ainsi que celles-ci, enregistrées sur votre téléphone.")) + f"""

<section class="section section--tight" aria-label="{tr("Pagine salvate", "Gespeicherte Seiten", "Saved pages", "Pages enregistrées")}">
<div class="container detail">
<div class="linklist">
{lista}
</div>
<div class="emergenza">
<h2 class="label">{tr("In caso di emergenza", "Im Notfall", "In an emergency", "En cas d’urgence")}</h2>
<div class="emergenza-numeri">
{numeri}
</div>
</div>
</div>
</section>"""
    nome = L("offline.html")
    html = page(nome, f"{titolo} | CAS Ticino", titolo, body)
    return pubblica(nome, html.replace("<head>\n", '<head>\n<meta name="robots" content="noindex">\n', 1))
