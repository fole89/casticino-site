"""Contenuti in più delle pagine capanna: tariffe, cucina, guardiani, accessi, attività, storia e foto.

Copiati una volta dai vecchi siti delle capanne (es. campotencia.casticino.ch) e da qui in poi modificati solo qui.
Ogni capanna ha una cartella (es. "campotencia"):
  assets/img/capanne/<cartella>/            immagini dei testi, senza assets/img/ e .webp (es. "lago-morghirolo")
  assets/img/capanne/<cartella>/foto/       gallerie: <gruppo>-<nn>-600.webp e -1200.webp (si mostrano tutte, in ordine)
  docs/capanne/<cartella>/                  PDF (schede degli itinerari, condizioni)
  capanne/<cartella>/<pagina>.html          sottopagine generate da pages.py (attività, storia, foto)
I testi sono HTML; i percorsi sono relativi alla radice del sito (pages.py li sistema nelle sottopagine)."""

PRENOTA = "https://www.hut-reservation.org/reservation/book-hut/{}/wizard"

CT = "capanne/campotencia/"          # sottopagine
CT_IMG = "capanne/campotencia/"      # immagini (dentro assets/img/)
CT_DOC = "docs/capanne/campotencia/"

CONTENUTI = {
    "CampoTencia.html": dict(
        cartella="campotencia",
        avviso="""<strong>Stagione estiva 2026.</strong> La capanna è aperta e custodita fino a metà ottobre circa.
Riservate il soggiorno online; per altre informazioni chiamateci. A presto, Valeria e Paco.""",
        capanna="""<p>La prima capanna delle montagne ticinesi fu costruita nel 1912 ai piedi del pizzo omonimo, sul versante leventinese in alta Val Piumogna. È un campo base per famiglie, escursionisti e alpinisti: escursioni naturalistiche, il Lago Morghirolo a due passi, i giardini d’arrampicata e le grandi ascensioni del gruppo del Campo Tencia, con la classica traversata della Cresta dei Corni.</p>
<p>L’edificio attuale, progettato dall’architetto sezionale Oscar Hofmann e inaugurato nel 1977, è su tre piani: al pianterreno entrata, locale scarpe, servizi e cantina; al primo piano un luminoso soggiorno da 70 posti e la cucina; al secondo circa 70 posti letto in 7 camerate, alcune da 4-8 posti, ideali per le famiglie.</p>
<p>I letti hanno piumoni nordici; <strong>il sacco lenzuolo è obbligatorio</strong>. La capanna mantiene il carattere degli anni ’80: niente camere singole con bagno, né asciugacapelli!</p>""",
        cucina="""<p>Un’offerta semplice e genuina, di impronta nostrana ma non solo ticinese: piatti freddi con salumi e formaggi locali, zuppe, gnocchi freschi e polenta con vari accompagnamenti, secondo la stagione e la disponibilità.</p>
<p>A chi pernotta proponiamo specialità del territorio, con un menu che cambia secondo l’occasione, ispirato dalla montagna e non solo.</p>
<p>Vegetariani, vegani e chi segue diete speciali sono i benvenuti: avvisateci con largo anticipo, così da accontentare tutti.</p>""",
        team=dict(img=("guardiani", "Valeria e Paco, guardiani della Capanna Campo Tencia", 1200, 899),
                  testo="""<p>Ci piace definirci persone solari, positive e piene di energia, con tanta voglia di fare e di metterci in gioco. Prima gestori di un’osteria con alloggio, dal 2024 siamo i guardiani della Capanna Campo Tencia.</p>
<p>Abbiamo viaggiato molto, scoprendo posti meravigliosi, ma accorgendoci anche di quanto è bello tornare sulle nostre montagne: è lì che ci sentiamo a casa. Dopo molte esperienze di lavoro e di gestione alberghiera abbiamo sentito il richiamo della montagna, che ci ha spinto a puntare più in alto e ad aprire questo sogno nel cassetto.</p>
<p>Durante la stagione ci affiancano amici e volontari. Non vediamo l’ora di accogliervi in capanna!</p>
<p><strong>Valeria e Paco</strong></p>"""),
        tariffe=[
            ("Soci CAS/FAT e club con diritto di reciprocità", "Pernottamento con mezza pensione (cena e colazione)",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 45.–"), ("Giovani da 15 a 21 anni", "Fr. 58.–"),
              ("Adulti dai 22 anni", "Fr. 75.–"), ("Guide alpine UIAGM", "Fr. 50.–")]),
            ("Non soci", "Pernottamento con mezza pensione (cena e colazione)",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 50.–"), ("Giovani da 15 a 21 anni", "Fr. 63.–"),
              ("Adulti dai 22 anni", "Fr. 85.–")]),
            ("Famiglie e gruppi", "Sconto infrasettimanale per famiglie (domenica-giovedì) e offerta per gruppi di giovani: scuole, scout, corsi G+S (lunedì-giovedì)",
             [("Famiglie: riduzione per ogni bambino sotto i 15 anni", "Fr. 5.–"), ("Gruppi: bambini sotto i 15 anni", "Fr. 40.–"),
              ("Gruppi: giovani da 15 a 18 anni", "Fr. 45.–")]),
            ("Extra", "Per ragioni igieniche il sacco lenzuolo è obbligatorio",
             [("Lunch", "Fr. 12.–"), ("Tè di giornata (1 l)", "Fr. 4.–"), ("Doccia (a persona)", "Fr. 5.–"),
              ("Sacco lenzuolo monouso", "Fr. 7.–")]),
        ],
        prenotare=f"""<ul>
<li><strong>Riservazione obbligatoria</strong>, online con il pulsante «Prenota».</li>
<li>Disdette senza costi entro le 18.00 di <strong>due giorni prima</strong> della data riservata.</li>
<li>Non si accettano riservazioni o richieste tramite social media: per informazioni chiamateci.</li>
<li>Capanna custodita da metà giugno a metà ottobre; d’inverno in marzo e aprile, su riservazione.</li>
<li>Locale invernale sempre aperto, con bibite e legna a disposizione.</li>
</ul>
<p><a class="file-link" href="{CT_DOC}disposizioni-per-gli-ospiti.pdf">Disposizioni per gli ospiti</a></p>
<p><a class="file-link" href="{CT_DOC}2020-cgc-capanne-cas-it.pdf">Condizioni generali delle capanne CAS</a></p>""",
        accessi=f"""<p>D’estate la capanna si raggiunge facilmente a piedi, con itinerari adatti alle famiglie; d’inverno con gli sci da Dalpe per la Val Piumogna.</p>
<p><strong>Come arrivare a Dalpe:</strong> da nord o da sud con l’autostrada A2, uscita Rodi-Quinto; con i mezzi pubblici fino a Rodi e da lì in <a href="https://www.postauto.ch/it" rel="noopener">autopostale</a>.</p>
<ul>
<li>Da Dalpe (1192 m): 3 h.</li>
<li>Dal Lago Tremorgio (1849 m), arrivo della funivia da Rodi: 3 h 30.</li>
<li>Da Fusio (Val Lavizzara) per il Passo Campolungo (2318 m): 6 h.</li>
<li>D’inverno da Dalpe: 3 h.</li>
</ul>
<p>Cartine: CNS 1:25’000 foglio 1272 Campo Tencia; CNS 1:50’000 foglio 266 S Valle Leventina. Itinerari su <a href="https://map.schweizmobil.ch/?lang=it&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2699408&amp;N=1146376" rel="noopener">SvizzeraMobile</a>.</p>
<p><a class="file-link" href="{CT_DOC}aet-pieghevole-tremorgio.pdf">Funivia Rodi-Tremorgio: orari e tariffe</a></p>""",
        attivita="""<p>Non solo Campo Tencia! La Val Piumogna è un terreno ideale per vivere la montagna a 360 gradi, a tutte le età: la bandita federale di caccia, gli alpeggi, il sentiero geologico del Campolungo, la cianite del Forno e i laghetti che rinfrescano anche nelle giornate più calde.</p>
<p>Il massiccio offre numerosi itinerari: la classica Cresta dei Corni, le ascensioni come quella al Pizzo Campo Tencia, le traversate verso le capanne Leìt, Sponda, Barone e Garzonera. La capanna è a metà della <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, la cavalcata di 100 km dal Passo della Novena al Lago Maggiore. I giardini d’arrampicata vicino alla capanna sono ideali per corsi con bambini e principianti; d’inverno ci sono sci alpinismo impegnativo e cascate di ghiaccio.</p>""",
        storia=dict(
            file="storia", titolo="Storia della capanna",
            lead="Dal 1912 la prima capanna delle montagne ticinesi: ampliata, distrutta da un incendio e ricostruita più bella.",
            img=("inaugurazione-1912", "Cartolina dell’inaugurazione del rifugio il 10 agosto 1912, con un gruppo di alpinisti davanti alla capanna in pietra"),
            corpo=f"""<p>La capanna fu costruita nel 1912 ai piedi del pizzo omonimo, sul versante leventinese, in alta Val Piumogna. Il nome Campo Tencia è un’invenzione toponomastica del 1858: indicava la montagna più alta interamente in territorio ticinese (3071,7 m) quando si disegnava la famosa carta nazionale del generale Dufour. Unisce i nomi di due alpi del Patriziato di Prato, Campo e Tencia, in alta Valle Lavizzara, sul versante valmaggese.</p>
<p>L’11 agosto 1912 l’inaugurazione. Nel 1932 Patocchi, sempre lui l’animatore, presenta il progetto di ampliamento e nell’estate del 1933 si costruisce la nuova ala est.</p>
<figure><img src="assets/img/{CT_IMG}costruzione.webp" alt="Uomini al lavoro davanti alla vecchia capanna in pietra, in una foto d’epoca" width="1200" height="832" loading="lazy" decoding="async"></figure>
<p>Passano quarant’anni e si mette mano ad altre opere di consolidamento e miglioria. Il 22 agosto 1975 un grave incendio distrugge il paziente lavoro di anni.</p>
<p>L’estate seguente la capanna rinasce più grande, più bella, più funzionale. La sua struttura è una novità a livello nazionale, merito dell’architetto Oscar Hofmann: non più l’immagine squadrata delle classiche capanne alpine, ma un aspetto innovativo, agile e aggraziato, con strutture portanti in acciaio rivestito e isolato con materiali adatti alla quota. Nuova inaugurazione il 25 settembre 1977.</p>
<figure><img src="assets/img/{CT_IMG}capanna-storica.webp" alt="La vecchia capanna in pietra nella neve, in una foto d’epoca" width="1200" height="782" loading="lazy" decoding="async"></figure>
<p>Nel 2008 l’ala nord aggiunge una nuova cucina professionale. L’11 agosto 2012 si festeggiano i 100 anni. Nel 2022 una turbina idrica garantisce l’approvvigionamento elettrico, l’impianto fotovoltaico è ampliato e il trattamento delle acque reflue rifatto.</p>"""),
        pagine=[
            dict(file="escursioni-facili", titolo="Escursioni facili",
                 lead="Su sentieri bianco-rossi, tra alpeggi, laghetti e la bandita federale di caccia del Campo Tencia.",
                 img=("lago-morghirolo-fiori", "Prato fiorito di eriofori sulla riva del Lago Morghirolo"),
                 corpo="""<p>Nella zona tra Leìt e Tencia le escursioni attraversano un ambiente naturale di pregio: la bandita federale di caccia del Campo Tencia, il sentiero geoturistico del Campolungo, gli alpeggi e numerosi laghetti per un bagno o un picnic.</p>""",
                 itinerari=[
                     dict(titolo="Lago Morghirolo", img=("lago-morghirolo", "Il Lago Morghirolo sotto le cime del gruppo del Campo Tencia"),
                          testo="Dopo una sosta in capanna, perché non raggiungere il magnifico laghetto per un bagno rinfrescante?",
                          dati=[("Lunghezza", "1,4 km"), ("Dislivello", "+250 m"), ("Tempo", "1 h andata e ritorno"), ("Difficoltà", "T2")],
                          link=[("Scheda dell’itinerario", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                     dict(titolo="Sentiero didattico", img=("torrente-piumogna", "Il torrente Piumogna tra i prati della valle"),
                          testo="Percorso ad anello con partenza e ritorno in Piumogna, passando dalla Capanna Campo Tencia e dall’Alpe Morghirolo, con pannelli didattici naturalistici. Si può aggiungere il Lago Morghirolo (circa 1 h in più, andata e ritorno) o pranzare in capanna e chiudere il giro verso l’Alpe Morghirolo nel pomeriggio.",
                          dati=[("Lunghezza", "12 km"), ("Dislivello", "+1300 m"), ("Tempo", "4-5 h"), ("Difficoltà", "T3")],
                          link=[("Mappa online", "https://s.geo.admin.ch/151dbckh2v17"),
                                ("Scheda dell’itinerario", CT_DOC + "e-lago-morghirolo-e-sentiero-didattico.pdf")]),
                     dict(titolo="Giro Leìt-Piumogna", img=("genziane", "Genziane in fiore sotto una cima rocciosa"),
                          testo="Grande giro ad anello che collega due capanne e due laghetti passando da due passi, in un contesto naturalistico di grande pregio. Attenzione: a inizio estate, nella parte alta a est del Pizzo Lei di Cima, ci sono spesso nevai ripidi e pericolosi.",
                          dati=[("Lunghezza", "18 km"), ("Dislivello", "+1350 / −1350 m"), ("Tempo", "8 h"), ("Difficoltà", "T3")],
                          link=[("Mappa online", "https://s.geo.admin.ch/rzubpn495uo8")]),
                 ]),
            dict(file="giro-piumogna", titolo="Giro della Piumogna",
                 lead="Un anello da Dalpe per le capanne Leìt e Campo Tencia, in una zona protetta ricca di fiori.",
                 img=("lago-leit", "Il laghetto sotto le cime del gruppo del Campo Tencia"),
                 corpo=f"""<p>Un itinerario fantastico in una zona particolarmente ricca di flora, riconosciuta e protetta a livello nazionale per la sua geologia: aquilegia alpina, genziane, anemoni, nigritelle, rododendri, ranuncoli di montagna e primule di Haller.</p>
<p>Da Dalpe, attraverso il magnifico Boscobello, si sale al Passo Vanitt e per un bel sentiero panoramico si raggiunge la Capanna Leìt. Si costeggia il laghetto ai piedi del Pizzo Prèvat, cima cara ai rocciatori detta anche «Cervinetto». Superati il Passo Leìt e la bocchetta Lei di Cima si ammirano le cime del gruppo del Campo Tencia, la più alta interamente in territorio ticinese (3072 m). In discesa si passa dal Lago Morghirolo, da dove in mezz’ora si arriva alla Capanna Campo Tencia. Il rientro segue la Val Piumogna, con il suo bel fiume e diversi alpeggi.</p>
<figure><img src="assets/img/{CT_IMG}pascoli-piumogna.webp" alt="Pascoli con un ometto di pietre e il segnavia bianco-rosso" width="1200" height="659" loading="lazy" decoding="async"></figure>
<h2>Andata e ritorno da Dalpe</h2>
<p>Da Dalpe (raggiungibile in autopostale da Rodi-Fiesso o da Airolo) si segue il sentiero per Boscobello, si passa dall’Alpe Cadonighino e si supera il Passo Vanitt (2138 m). Si raggiungono la Capanna Leìt e il laghetto (2260 m), poi si prosegue verso la Capanna Campo Tencia: superati il Passo Leìt (2431 m) e la bocchetta Lei di Cima (2481 m) si arriva alle cascine Lei di Cima (2400 m). Il nuovo sentiero porta al Lago Morghirolo (2264 m) e in mezz’ora alla Capanna Campo Tencia (2140 m), che domina la Val Piumogna. In discesa si segue il sentiero lungo la valle fino alle cascine di Piumogna, poi la strada verso Boscobello; poco dopo il ponte di Polpiano un sentiero a destra scende a Dalpe.</p>
<p>Si può partire anche da Rodi-Fiesso, salendo con la funivia al Lago Tremorgio e seguendo il sentiero per la Capanna Leìt, o fare il giro al contrario. <strong>Attenzione:</strong> la tappa è lunga, valutate il pernottamento in capanna.</p>
<figure><img src="assets/img/{CT_IMG}cascina-piumogna.webp" alt="Una cascina tra i larici in Val Piumogna, con le cime innevate sullo sfondo" width="1200" height="900" loading="lazy" decoding="async"></figure>""",
                 dati=[("Lunghezza", "19 km"), ("Dislivello", "+1330 / −1330 m"), ("Tempo", "8 h"), ("Difficoltà", "T2"),
                       ("Da vedere", "Boscobello, Capanna Leìt, Pizzo Prèvat, Lago Leìt, cascine Lei di Cima, gruppo del Campo Tencia, Lago Morghirolo, alpeggi di Croslina e Geira")],
                 link=[("Mappa online del percorso", "https://map.schweizmobil.ch/?lang=it&amp;land=wanderland&amp;route=all&amp;bgLayer=pk&amp;layers=Wanderland%2CStation&amp;season=summer&amp;resolution=10&amp;E=2700579&amp;N=1146079&amp;trackId=4267446")]),
            dict(file="escursionismo-alpino", titolo="Escursionismo alpino",
                 lead="Fuori dai sentieri: le cime del Campo Tencia, del Forno e del Campolungo, da T4 in su.",
                 img=("segnavia-alpino", "Segnavia bianco-blu su un masso, con le cime sullo sfondo"),
                 corpo="""<p>Le difficoltà dell’escursionismo sono divise in sei gradi secondo la scala T, da T1 (escursione) a T6 (escursione alpina difficile). Intorno al Campo Tencia ci sono parecchie possibilità: le salite al Pizzo Campo Tencia, al Pizzo Forno o al Campolungo. I percorsi sono segnalati solo in parte e bisogna sapersi orientare; ci possono essere pericoli oggettivi e, a inizio estate, resti di nevai: partite preparati.</p>
<p><a href="https://www.sac-cas.ch/it/formazione-e-sicurezza/sicuri/sicuri-nelle-escursioni-alpine-e-in-montagna/" rel="noopener">Sicuri nelle escursioni alpine: i consigli del CAS</a></p>""",
                 itinerari=[
                     dict(titolo="Pizzo Campo Tencia (3072 m) e Pizzo Croslina (3012 m)", img=("croce-campo-tencia", "La croce di vetta del Pizzo Campo Tencia"),
                          testo="La montagna più alta interamente in territorio ticinese deve il nome alle sue rocce rossastre e ferrose, «tencie», cioè sporche, in dialetto. Al centro del cantone, offre una vista a 360 gradi; dalla cima si può scendere in Valle Lavizzara o raggiungere la Via Alta Vallemaggia. Il percorso è in buona parte marcato; in alcuni punti attenzione alla caduta di sassi, soprattutto se ci sono altre persone. A inizio estate c’è neve nella conca prima della bocchetta di Croslina. Dalla bocchetta (2865 m) si può traversare verso nord fino alla cresta che porta al Pizzo Croslina: passaggi esposti, attenzione soprattutto in discesa.",
                          dati=[("Lunghezza", "3 km"), ("Dislivello", "+940 m"), ("Tempo", "3 h per una cima, 4 h 30 per le due"),
                                ("Difficoltà", "T4 Pizzo Campo Tencia, T6 Pizzo Croslina"), ("Materiale", "Buoni scarponi")],
                          link=[("Descrizione completa", CT + "tencia-croslina.html"),
                                ("Scheda dell’itinerario", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")]),
                     dict(titolo="Pizzo Forno (2907 m)", img=("pizzo-forno", "Il Pizzo Forno e il Pizzo Laghetto con gli ultimi nevai"),
                          testo="La tappa 5 della Via Idra percorre la Senda del Ghiacciaio fino al passo del Ghiacciaione, da dove si può salire al Pizzo Forno prima di scendere al rifugio Alpe Sponda. Il versante nord resta a lungo innevato: buone calzature e ramponcini sono molto raccomandati.",
                          dati=[("Lunghezza", "4,5 km"), ("Dislivello", "+767 m"), ("Tempo", "3 h"), ("Difficoltà", "T4")],
                          link=[("Via Idra, tappa 5", "https://www.viaidra.ch/tappa05"), ("Scheda dell’itinerario", CT_DOC + "d-pizzo-forno-2907-m.pdf")]),
                     dict(titolo="Pizzo Campolungo (2714 m)", img=("pizzo-campolungo", "Il Pizzo Campolungo e le creste verso il Pizzo Prèvat"),
                          testo="Dalla cima la vista si apre sui laghetti Leìt, Tremorgio e Morghirolo e sul Pizzo Prèvat, il «Cervino ticinese». La salita non è segnata e passa su ripidi prati e pietraie, nella conca prima dell’Alpe Lei di Cima: non è difficile, ma bisogna sapersi orientare.",
                          dati=[("Lunghezza", "3 km"), ("Dislivello", "+690 m"), ("Tempo", "2 h 30"), ("Difficoltà", "T4")],
                          link=[("Mappa online", "https://s.geo.admin.ch/epntrruz341r"), ("Scheda dell’itinerario", CT_DOC + "c-pizzo-campolungo-2714-m.pdf")]),
                     dict(titolo="Giro del Campolungo", img=("giro-campolungo", "Un laghetto turchese tra le creste del Campolungo"),
                          testo="Un’escursione selvaggia, collegamento alternativo tra la Capanna Leìt e la Campo Tencia passando dal versante valmaggese. Terreno in parte impervio, cattiva ricezione telefonica e, a inizio estate, neve sui ripidi versanti in ombra.",
                          dati=[("Lunghezza", "8 km"), ("Dislivello", "+1268 / −1166 m"), ("Tempo", "6 h da capanna a capanna, 7-8 h il giro completo"),
                                ("Difficoltà", "T4-T5, in parte attrezzato con cavi"), ("Periodo", "Da luglio a fine settembre"),
                                ("Materiale", "Buoni scarponi, casco ed eventualmente set da ferrata"),
                                ("Da vedere", "Lago Morghirolo, Corte di Zaria, laghetti Cantùn dal Prèvat, Pizzo del Prèvat")],
                          link=[("Scheda dell’itinerario", CT_DOC + "a-giro-del-campolungo.pdf")]),
                 ]),
            dict(file="cresta-dei-corni", titolo="Cresta dei Corni",
                 lead="Né escursionismo né alpinismo: la cavalcata aerea dal Passo Morghirolo alla vetta del Campo Tencia.",
                 img=("capanna-cresta-dei-corni", "La Capanna Campo Tencia sotto la Cresta dei Corni"),
                 corpo="""<p>Non più escursionismo ma nemmeno alpinismo: il vecchio termine inglese «scrambling» descrive bene la Cresta dei Corni al Campo Tencia. L’itinerario porta in vetta al Campo Tencia dal Passo Morghirolo, passando dai pizzi Canà, Tre Corni e Croslina: un percorso aereo con vista mozzafiato su Leventina e Lavizzara, ideato e realizzato da Franco Demarchi, «Dema», per 28 anni custode della capanna.</p>
<p>È una via di cresta d’alta montagna, esposta, con pilastri e paretine di roccia fino a 25 m, ben attrezzata e marcata; a inizio estate ci può essere neve. <strong>Non ci sono vie di fuga: servono buona condizione fisica, assenza di vertigini e tempo stabile. Calcolate bene i tempi e tenete una riserva sufficiente.</strong></p>
<h2>Percorso</h2>
<p>Dalla capanna si sale verso la bocchetta a 2560 m su tracce di sentiero. Dalla sella si resta per lo più sul filo di cresta, con facile arrampicata in parte attrezzata alternata a tratti camminabili. Dal Pizzo Croslina si scende con attenzione all’omonima bocchetta, da dove, se le energie bastano, si può aggiungere la vetta del Pizzo Campo Tencia. Discesa per la via normale in circa 1 h 30.</p>""",
                 dati=[("Lunghezza", "8 km"), ("Dislivello", "+1350 / −1190 m"), ("Tempo", "8 h da capanna a capanna"),
                       ("Difficoltà", "T6, PD, passaggi di III grado"), ("Materiale", "Imbracatura, set da ferrata, casco, eventualmente una corda da 30 m per assicurare")],
                 link=[("Percorso online", "https://s.geo.admin.ch/r94n5ne4qz11"), ("Prospetto della Cresta dei Corni", CT_DOC + "prospetto-tre-corni.pdf")],
                 foto="cresta-dei-corni"),
            dict(file="tencia-croslina", titolo="Pizzo Campo Tencia e Pizzo Croslina",
                 lead="La piramide di pietra e ghiaccio più alta del Ticino e il colosso che sovrasta la capanna.",
                 img=("croslina-tencia", "Le cime del Pizzo Croslina e del Pizzo Campo Tencia con la neve"),
                 corpo="""<p>Il Pizzo Campo Tencia (3072 m) è una straordinaria piramide di pietra e di ghiaccio, con un vasto panorama a 360 gradi. Il Pizzo Croslina (3012 m) si erge come un colosso sopra la capanna; visto da est è invece un’elegante piramide.</p>
<p>Caratteristico è il versante nord di questo tratto della catena principale: dopo la piramide del Croslina emergono verso sud-est, in sequenza regolare, tre cime separate da selle appena accennate: il Pizzo Campo Tencia (3072 m), la cima intermedia detta Tenca (3035 m, senza nome sulla carta nazionale) e il Pizzo Penca (3038 m).</p>
<h2>Percorso</h2>
<p>Dalla capanna si va verso sud seguendo le marcature bianco-blu fino a una cascata. A sinistra un largo camino porta alla cengia che attraversa tutta la parete: un sentiero ben marcato ed esposto sale verso sud-est fino a una facile costa. Piegando a sud-ovest si arriva nella conca del Laghetto, ai piedi di quel che resta del Ghiacciaio Grande di Croslina. Si continua sulla crestina tra i due ghiacciai di Croslina fino a circa 2800 m, poi verso sud-ovest, abbassandosi sul ghiacciaio, alla bocchetta di Croslina (2867 m), sempre sulle marcature bianco-blu. Restando sul filo di cresta si raggiunge la croce di vetta.</p>
<p>Dalla cima si può traversare verso la Capanna Soveltra, in Valle Maggia, scendendo a sud-est sulle marcature bianco-blu-bianco.</p>
<p><strong>Pizzo Croslina:</strong> dalla bocchetta di Croslina si va verso nord-ovest seguendo i punti blu, fino a una cengia sul lato destro dell’evidente canale detritico. Salita in parte esposta, con passaggi su roccia di II grado.</p>
<p>Per entrambe le cime la discesa segue lo stesso itinerario.</p>""",
                 dati=[("Lunghezza", "3 km"), ("Dislivello", "+940 m"), ("Tempo", "3 h per una cima, 4 h per le due"),
                       ("Difficoltà", "T3-T4 Pizzo Campo Tencia, T6 Pizzo Croslina"),
                       ("Da vedere", "Conca del Laghetto, Ghiacciaio Grande di Croslina, la croce di vetta del Campo Tencia, le stelle alpine sul Croslina")],
                 link=[("Scheda dell’itinerario", CT_DOC + "b-pizzo-campo-tencia-3072-m-pizzo-croslina-3012-m.pdf")],
                 foto="tencia-croslina"),
            dict(file="arrampicata", titolo="Arrampicata",
                 lead="Giardini d’arrampicata a pochi minuti dalla capanna, dal III grado al 6b: ideali per imparare.",
                 img=("giardino-arrampicata", "Arrampicatori su una placca di roccia vicino alla capanna"),
                 corpo=f"""<p>Una regione ideale per insegnare l’arrampicata a bambini e principianti: intorno alla capanna sono stati attrezzati diversi giardini d’arrampicata, con difficoltà dal III grado fino a qualche tiro di 6b per i più esigenti.</p>
<p>Il settore Angolo, vicino al lago, è attrezzato apposta per l’istruzione su roccia: monotiri, calate, corda doppia nel vuoto e una piccola via di più tiri, facile e didattica. A pochi minuti dalla capanna il settore Cascata permette di allenare le manovre su facili vie di più tiri parallele, mentre sul masso Kape ci sono alcuni monotiri.</p>
<p><a href="https://s.geo.admin.ch/na49wcdjtms7" rel="noopener">I settori sulla mappa</a></p>
<p><a class="file-link" href="{CT_DOC}volantino-arrampicata-campo-tencia.pdf">Volantino dei giardini d’arrampicata</a></p>
<table>
<thead><tr><th>Settore</th><th>Vie</th><th>Lunghezza</th><th>Grado</th><th>Note</th></tr></thead>
<tbody>
<tr><td>Cascata</td><td>4</td><td>60 m</td><td>3-4</td><td>più tiri, paralleli</td></tr>
<tr><td>Kape</td><td>7</td><td>10 m</td><td>5-6c</td><td>monotiri</td></tr>
<tr><td>Tutto o niente</td><td>10</td><td>20 m</td><td>3-5a</td><td>monotiri</td></tr>
<tr><td>Disperato</td><td>6</td><td>10 m</td><td>4-5a</td><td></td></tr>
<tr><td>Onapart</td><td>3</td><td>30 m</td><td>5a-6b</td><td></td></tr>
<tr><td>Pulce di roccia</td><td>5</td><td>20 m</td><td>3-4</td><td>facili placchette</td></tr>
<tr><td>Angolo</td><td>8</td><td>20 m</td><td>4-5a</td><td>terreno d’istruzione</td></tr>
<tr><td>Piode</td><td>3</td><td>25 m</td><td>4-5a</td><td></td></tr>
<tr><td>Pitela</td><td>6</td><td>10-80 m</td><td>3-5a</td><td></td></tr>
<tr><td>Cresta rossa</td><td></td><td>500 m</td><td>2-4</td><td>via alpina</td></tr>
<tr><td>Lago</td><td>1</td><td>75 m</td><td>5a</td><td></td></tr>
</tbody>
</table>
<figure><img src="assets/img/{CT_IMG}settori-arrampicata.webp" alt="Cartina dei settori d’arrampicata intorno alla capanna e al Lago Morghirolo" width="1088" height="766" loading="lazy" decoding="async"></figure>""",
                 foto="arrampicata"),
            dict(file="inverno", titolo="In inverno",
                 lead="Sci alpinismo impegnativo lontano dalle mete più battute e cascate di ghiaccio fino a 200 metri.",
                 img=("scialpinismo", "Scialpinisti in discesa su un ampio pendio innevato, controsole"),
                 corpo="""<h2>Sci alpinismo</h2>
<p>D’inverno la zona del Campo Tencia resta lontana dalle mete più battute. Il terreno tecnico e impervio richiede buone condizioni di neve e una buona padronanza dello sci alpinismo e dell’orientamento. In primavera si trovano le condizioni per gite di grande soddisfazione: il Pizzo Campo Tencia, il Pizzo Forno e il Pizzo Campolungo. Di norma la capanna non è custodita, ma può essere aperta per gruppi o per più giornate.</p>
<h2>Cascate di ghiaccio</h2>
<p>Nella conca del Buco di Cumasna, a 2000 metri, dall’inizio dell’inverno si formano imponenti cascate di ghiaccio, lunghe fino a 200 metri e di varie difficoltà. Sulla destra c’è la più famosa, la «Giovannelli», lungo il canale che d’inverno permette di superare la barra rocciosa per salire o scendere dalla vetta del Pizzo Campo Tencia.</p>""",
                 foto="inverno"),
        ],
        foto=[("La capanna", "capanna"), ("La cucina", "cucina"), ("I dintorni", "dintorni")],
    ),

    "Cristallina.html": dict(
        cartella="cristallina",
        avviso="""<strong>Stagione estiva a pieno regime.</strong> Tutti i principali collegamenti sono liberi dalla neve e ben percorribili.
Le prenotazioni si fanno online. Vi aspettiamo, Manu.""",
        capanna="""<p>La prima capanna moderna del Club Alpino Svizzero sorge a 2572 m sul Passo Cristallina, in una zona molto bella per l’escursionismo estivo e invernale. D’estate è il punto d’appoggio per le cime vicine e per le traversate verso la Valle Maggia, la Val Formazza e il Gottardo; d’inverno la regione, ricca di neve, offre splendide discese e concatenamenti di vette.</p>
<p>Ha 100 posti letto in cuccette con piumone, in 6 camere da 4, 9 da 8 e 2 dormitori da 12, un refettorio panoramico con terrazza, servizi interni con acqua calda, doccia, locale essiccatoio e locale scarponi con ciabatte per gli ospiti. Il sacco lenzuolo è obbligatorio. Buona ricezione Swisscom vicino alla capanna.</p>
<p>La capanna è sempre aperta e accessibile. È custodita d’estate, da giugno a metà ottobre; d’inverno, da dicembre a fine aprile, il guardiano c’è con buone condizioni, nei fine settimana, durante le feste e per i gruppi che hanno riservato.</p>""",
        cucina="""<p>Durante il giorno ricette semplici alla portata di tutti: gnocchi, ravioli, torte salate, salumi, dolci e tanto altro, tutto fatto in capanna con prodotti locali di origine svizzera. Per la mezza pensione i menu cambiano secondo il giorno della settimana, pensando anche ai vegetariani. Vi aspetta inoltre una buona scelta di vini e distillati.</p>
<p><strong>Importante:</strong> avvisateci in tempo se siete vegetariani o vegani, o se avete allergie o intolleranze: cercheremo di prepararvi un menu adatto.</p>
<p>Le camere si assegnano secondo l’ordine delle riservazioni e la grandezza dei gruppi; non si possono riservare camere a uso esclusivo. Quando la capanna è custodita la mezza pensione è obbligatoria.</p>
<p>I cani sono benvenuti, ma non sono ammessi nelle camere e negli spazi comuni: avvisateci prima dell’arrivo.</p>""",
        team=dict(titolo="Il guardiano", img=("guardiano", "Emanuele Vellati, guardiano della Capanna Cristallina, nella neve con il Basodino sullo sfondo"),
                  testo="""<p>Emanuele Vellati gestisce la capanna dall’inverno 2018. Elettricista e cuoco di formazione, la conduce con grande cura e dedizione, come mostrano le infrastrutture curate e l’ottima cucina. Appassionato alpinista in gioventù, oggi vive la montagna ogni giorno, come essenza del suo lavoro.</p>
<p>D’estate e d’inverno lo affiancano numerosi aiutanti, amici e volontari del CAS Ticino, sempre felici di un piccolo ringraziamento. E poi c’è Jack, il più pacifico e curioso abitante della capanna, che ama la neve fresca quasi più di noi.</p>
<p><strong>Emanuele</strong></p>""",
                  persone=[("Jack", "Il cane della capanna, ama la neve fresca", "jack")]),
        tariffe=[
            ("Soci CAS/FAT e club con diritto di reciprocità", "Pernottamento con mezza pensione (cena e colazione), IVA e tassa di soggiorno incluse",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 50.–"), ("Giovani da 15 a 21 anni", "Fr. 70.–"),
              ("Adulti dai 22 anni", "Fr. 83.–"), ("Guide alpine", "Fr. 55.–")]),
            ("Non soci", "Pernottamento con mezza pensione (cena e colazione), IVA e tassa di soggiorno incluse",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 55.–"), ("Giovani da 15 a 21 anni", "Fr. 77.–"),
              ("Adulti dai 22 anni", "Fr. 95.–")]),
            ("Famiglie e gruppi", "Sconto infrasettimanale per famiglie (domenica-giovedì) e offerta per gruppi di giovani: scuole, scout, corsi G+S (lunedì-giovedì)",
             [("Famiglie: riduzione per ogni bambino sotto i 15 anni", "Fr. 5.–"), ("Gruppi: bambini fino a 14 anni", "Fr. 40.–"),
              ("Gruppi: ragazzi da 15 a 18 anni", "Fr. 50.–")]),
            ("Extra", "Per ragioni igieniche il sacco lenzuolo è obbligatorio",
             [("Lunch", "Fr. 12.–"), ("Tè in thermos per la giornata, con il lunch", "incluso"), ("Doccia (a persona)", "Fr. 5.–"),
              ("Sacco lenzuolo monouso", "Fr. 7.–")]),
        ],
        prenotare="""<ul>
<li><strong>Si accetta solo contante in franchi svizzeri</strong>, niente euro.</li>
<li>Riservazione online con il pulsante «Prenota»: indicate allergie, intolleranze e vegetariani nell’apposita casella.</li>
<li>Annullate la prenotazione entro <strong>due giorni prima dell’arrivo</strong>, se serve anche per telefono o e-mail; vale il regolamento sul mancato arrivo (no-show).</li>
</ul>
<p><a class="file-link" href="docs/capanne/cristallina/disposizioni-per-gli-ospiti-1.pdf">Disposizioni per gli ospiti</a></p>
<p><a class="file-link" href="docs/capanne/cristallina/2020-condizioni-generali-it.pdf">Condizioni generali delle capanne CAS</a></p>""",
        accessi="""<p>D’estate la capanna si raggiunge a piedi in qualche ora di cammino, per lo più su itinerari adatti alle famiglie; d’inverno con gli sci dalla Valle Bedretto, da Robiei o dalla Val Formazza.</p>
<ul>
<li>Da Ossasco: 3 h 30.</li>
<li>Dal Passo San Giacomo: 4 h.</li>
<li>Da Robiei: 3 h.</li>
<li>Dal Lago del Narèt: 2 h 30.</li>
<li>Da Airolo Pesciüm: 5 h.</li>
<li>Dalla Capanna Poncione di Braga: 4 h.</li>
<li>D’inverno: da Ossasco 3 h, da All’Acqua 4 h.</li>
</ul>
<p><strong>In auto da nord:</strong> A2 fino ad Airolo, poi direzione Passo della Novena e Valle Bedretto. <strong>Da sud:</strong> A2 fino a Bellinzona, poi Locarno e Valle Maggia: Val Bavona per Robiei, con la <a href="https://www.robiei.ch/" rel="noopener">funivia San Carlo-Robiei</a> (d’estate), o Val Lavizzara per il Narèt.</p>
<p><strong>Con i mezzi pubblici:</strong> treno S10 fino ad Airolo, poi bus per la Valle Bedretto. Taxi da Airolo: Marchetti Taxi <a class="num" href="tel:+41918733035">+41 (0) 91 873 30 35</a>, Gotthard Taxi <a class="num" href="tel:+41787901055">+41 (0) 78 790 10 55</a>.</p>
<p><strong>Traversate ad altre capanne:</strong> <a href="https://www.corno-gries.ch/?lang=it" rel="noopener">Corno Gries</a> (2338 m) 5 h; <a href="https://www.capanna-basodino.ch/" rel="noopener">Basodino</a> (2200 m) 2 h; <a href="http://www.utoelocarno.ch/" rel="noopener">Poncione di Braga</a> (1870 m) 4 h; <a href="https://www.satritom.ch/garzonera/" rel="noopener">Garzonera</a> (2000 m) 5 h, T5; <a href="https://www.rifugiomarialuisa.it/" rel="noopener">Rifugio Maria Luisa</a> (Italia, 2393 m) 5 h.</p>
<p>Cartine: CNS 1:25’000 foglio 1251 Val Bedretto; carta scialpinistica 265 S Nufenenpass.</p>""",
        attivita="""<p>Il Passo Cristallina è un collegamento naturale tra il massiccio del Gottardo e la Valle Maggia, al centro di una rete di itinerari e rifugi: la <a href="https://www.viaidra.ch/" rel="noopener">Via Idra</a>, la Via Cristallina e la Via Alta della Valle Maggia passano di qui. D’inverno è un paradiso dello sci alpinismo, con neve garantita anche nelle annate peggiori.</p>
<p>La geologia racconta la nascita delle Alpi: marmi di origine marina addossati a rocce magmatiche, pieghe incredibili. La fauna è ricca: la colonia di stambecchi verso la Cima di Lago, camosci, l’aquila, il gheppio. E ovunque le tracce del lavoro dell’uomo: alpeggi, opere militari e grandi impianti idroelettrici.</p>""",
        pagine=[
            dict(file="proposte-gite", titolo="Proposte di gite",
                 foto="proposte-gite",
                 lead="Cinque itinerari di media difficoltà, dalla Cima di Lago alla Via Idra, con la capanna come base o come tappa.",
                 img=("pizzo-cristallina", "Vista dalla vetta del Pizzo Cristallina su laghetti e cime"),
                 corpo="""<p>A chi vuole scoprire la magnifica zona del Cristallina, i laghetti e la fauna dell’alta montagna, proponiamo itinerari di media difficoltà e non troppo lunghi, che partono dalla capanna o la usano come tappa.</p>""",
                 itinerari=[
                     dict(titolo="Cima di Lago (2832 m)", img=("cima-di-lago", "Uno stambecco sul pendio della Cima di Lago, con il percorso segnato in rosso"),
                          testo="Facile vetta con una splendida vista, ideale anche per i bambini: è probabile incontrare gli stambecchi.",
                          dati=[("Lunghezza", "4 km"), ("Dislivello", "+300 m"), ("Tempo", "1 h"), ("Difficoltà", "T4")],
                          link=[("Scheda dell’itinerario", "docs/capanne/cristallina/a-cima-di-lago-2832-msm.pdf")]),
                     dict(titolo="Pizzo Cristallina (2912 m)", img=("pizzo-cristallina", "Vista dalla vetta del Pizzo Cristallina su laghetti e cime"),
                          testo="La cima principale, al centro di una serie di laghetti alpini; in vetta resiste il rifugio Camosci, ultima traccia del periodo bellico. Nel pendio finale attenzione alla caduta di sassi se ci sono altre persone; entrate nel bivacco con molta prudenza, c’è pericolo di caduta.",
                          dati=[("Lunghezza", "11 km"), ("Dislivello", "+1100 m"), ("Tempo", "2 h"), ("Difficoltà", "T4")],
                          link=[("Scheda dell’itinerario", "docs/capanne/cristallina/b-cristallina-2912.pdf")]),
                     dict(titolo="Giro del Cristallina", img=("giro-cristallina", "Il lago artificiale di Robiei con la diga, sotto le montagne"),
                          testo="Classico e facile anello su sentiero bianco-rosso intorno alla vetta del Cristallina. Si fa anche in giornata da Robiei o dal Passo del Narèt, con pranzo in capanna.",
                          dati=[("Lunghezza", "14 km"), ("Dislivello", "+980 m"), ("Tempo", "5 h 30"), ("Difficoltà", "T3")],
                          link=[("Scheda dell’itinerario", "docs/capanne/cristallina/c-giro-del-cristallina.pdf")]),
                     dict(titolo="Sentiero Cristallina 59, verso Robiei", img=("percorso-59", "Laghetti alpini in una conca rocciosa lungo il sentiero Cristallina"),
                          testo="Il sentiero Cristallina numero 59 è una classicissima traversata di tre giorni da Bignasco, in Valle Maggia, ad Airolo.",
                          dati=[("Lunghezza", "42 km, in tre tappe"), ("Dislivello", "+2800 / −2100 m"), ("Tempo", "3 giorni"), ("Difficoltà", "T3")],
                          link=[("Scheda dell’itinerario", "docs/capanne/cristallina/d-percorso-59-cristallina.pdf")]),
                     dict(titolo="Passo della Novena-Cristallina-Airolo", img=("nufenen-airolo", "Escursionisti su una cresta erbosa e rocciosa"),
                          testo="La prima tappa della Via Idra, dal Passo della Novena ad Airolo con notte in capanna. Il punto saliente è la salita del Canale del Becco, attrezzato con funi e scalini: meglio percorrerlo in salita, attenzione alla caduta di sassi e alla neve a inizio stagione.",
                          dati=[("Lunghezza", "27 km"), ("Dislivello", "+1600 / −2450 m"), ("Tempo", "10 h, in due giorni (5 + 5)"),
                                ("Difficoltà", "T4 il primo giorno (T6 il Canale del Becco), T3 il secondo")],
                          link=[("Scheda dell’itinerario", "docs/capanne/cristallina/e-passo-nufenen-airolo.pdf")]),
                 ]),
            dict(file="inverno", titolo="In inverno",
                 foto="inverno",
                 lead="Vette e discese in neve polverosa: più discese in una sola giornata intorno alla capanna.",
                 img=("discesa-polvere", "Scialpinista in salita su un ampio pendio innevato in ombra"),
                 corpo="""<p>La regione del Cristallina si presta a magnifiche discese in neve polverosa. Molti itinerari intorno alla capanna si possono combinare, con due o più discese in una sola giornata, che spesso finisce sui versanti in ombra della sponda destra della Valle Bedretto.</p>
<ul>
<li>Salita dalla Val Torta e discesa della <strong>Val Cassinello</strong> dalla Bassa di Folcra o dal <strong>Passo Gararesch</strong>, variante (itinerari 521 h e 521 i).</li>
<li>Salita dalla Val Torta per il classico <strong>giro del Cristallina</strong>, con pranzo in capanna e discesa dalla Val Piana o dalla Valle Cavagnolo.</li>
<li>Vetta del <strong>Cristallina</strong> e discesa dalla «Diavolezzina», con eventuale risalita alla Bassa di Folcra (521 h) o al Passo Gararesch (521 i).</li>
<li><strong>Cima di Lago</strong> come gita pomeridiana arrivando dalla Val Torta o dalla Val Cavagnoli.</li>
<li>Il selvaggio e vario <strong>giro delle bocchette</strong>: il primo giorno All’Acqua, San Giacomo, Passo Grandinagia, Bocchetta di Valleggia, Passo di Cima di Lago e capanna (<a href="https://s.geo.admin.ch/7e3436c217" rel="noopener">mappa</a>); il secondo Cima di Lago, Sfunadau, Cristallina e Passo Gararesch.</li>
<li><strong>Poncione di Braga, Basodino, Marchhorn:</strong> vette lungo grandi traversate.</li>
</ul>"""),
            dict(file="curiosita", titolo="Curiosità",
                 lead="Occupazione militare, nascita delle Alpi e grandi impianti idroelettrici: approfondimenti sulla zona del Cristallina.",
                 img=("rocce-piegate", "Rocce piegate dall’orogenesi alpina in una conca verde"),
                 corpo="""<p>Le tracce della formazione delle Alpi sono ben visibili: le forze che hanno sollevato la catena hanno portato in superficie i sedimenti marini, e in pochi metri si trovano rocce molto diverse per composizione e origine. Questo influenza anche la flora, legata al tipo di substrato. La fauna è quella tipica delle Alpi: è facile incontrare gli stambecchi della colonia, oltre cento esemplari che non temono l’uomo. Anche l’uomo ha trasformato la zona, con il presidio del confine in tempo di guerra e con le grandi opere idroelettriche.</p>""",
                 itinerari=[
                     dict(titolo="La storia dell’occupazione militare", img=("rifugio-camosci", "Il vecchio rifugio militare in pietra sulla vetta, tra la neve"),
                          testo="La costruzione della strada della Val Formazza fino al Passo San Giacomo, tra il 1926 e il 1929, preoccupò la Svizzera e portò alla fortificazione della zona.",
                          link=[("Leggi tutto", "docs/capanne/cristallina/a-la-storia-delloccupazione-militare-1.pdf")]),
                     dict(titolo="Le tracce dell’orogenesi", img=("rocce-piegate", "Rocce piegate dall’orogenesi alpina in una conca verde"),
                          testo="Il paesaggio del Cristallina è segnato dall’orogenesi alpina, un processo durato circa 25 milioni di anni.",
                          link=[("Leggi tutto", "docs/capanne/cristallina/b-le-tracce-dellorogenesi-1.pdf")]),
                     dict(titolo="L’idroelettrico Naret-Robiei", img=("schema-idroelettrico", "Schema dei bacini idroelettrici collegati tra il Gries, Robiei e il Lago Maggiore"),
                          testo="La zona Robiei-Narèt è ricca di sbarramenti collegati tra loro, che sfruttano al meglio l’acqua per produrre energia elettrica pulita.",
                          link=[("Leggi tutto", "docs/capanne/cristallina/c-ldroelettrico-naret-robiei-1.pdf")]),
                 ]),
        ],
        foto=[("La capanna", "capanna"), ("La cucina", "cucina"), ("I dintorni", "dintorni")],
    ),

    "Adula.html": dict(
        cartella="adula",
        avviso="""<strong>Stagione 2026: la capanna è aperta.</strong> Tutti i sentieri di accesso sono percorribili; gradita la riservazione anche per il pranzo.
Per qualsiasi informazione chiamateci. A presto in quota, Lele, Miri e il team.""",
        capanna="""<p>La «Bassa», come la si chiama da sempre, è stata inaugurata nel 1924 e ha conservato tutte le caratteristiche dell’edificio originale in pietra e legno: un soggiorno che trasuda storia, dormitori che hanno visto passare migliaia di alpinisti, accoglienza calorosa e una cucina nostrana che riempie lo stomaco e lo spirito.</p>
<p>Ha 24 posti letto in quattro piccoli dormitori da 4, 5 e 7 posti, adatti anche alle famiglie, e due stanzette matrimoniali con sovrapprezzo; due refettori accoglienti da 20 posti, servizi interni, doccia, pannelli solari per l’illuminazione e cucina a legna e a gas. I letti hanno piumoni; il sacco lenzuolo è obbligatorio. Ricezione discreta vicino alla capanna.</p>
<p>È aperta tutto l’anno e custodita da fine maggio a metà ottobre; il locale invernale è sempre aperto, con bibite e legna.</p>""",
        cucina="""<p>La terrazza panoramica invita a mangiare all’aperto. Ogni giorno cuciniamo con prodotti locali: piatti ticinesi, formaggi e formaggini, pasta al sugo, zuppa, minestrone e i nostri rösti conditi in vari modi, oltre a diverse torte sempre pronte.</p>
<p>A chi pernotta la cena propone piatti e specialità secondo i prodotti di stagione, e una ricca colazione dà la forza per nuove avventure.</p>
<p><strong>Importante:</strong> avvisateci in tempo se siete vegetariani o vegani, o se avete allergie o intolleranze.</p>
<p>I cani sono benvenuti, ma non nelle camere: per loro c’è una sistemazione all’esterno. Avvisateci prima se portate il vostro cane.</p>""",
        team=dict(img=("guardiani", "Il guardiano e due aiutanti davanti all’entrata della capanna in pietra"),
                  testo="""<p>Sono Lele, alla Capanna Adula dal 2024, insieme alla mia compagna Mirella. La passione per la montagna e l’esperienza come aiuto in altre capanne oltralpe mi hanno portato a lasciare il mio lavoro per vivere a contatto con la gente e la natura.</p>
<p>Durante la stagione ci aiutano giovani che hanno voglia di vivere un’esperienza unica in quota. Un sogno diventato realtà.</p>""",
                  persone=[("Raffaele «Lele» Demaldi", "Guardiano", "lele"), ("Mirella", "In capanna con Lele", "mirella")]),
        tariffe=[
            ("Soci CAS/FAT e club con diritto di reciprocità", "Pernottamento, cena (zuppa, insalata, piatto forte, dessert) e colazione, IVA inclusa",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 45.–"), ("Giovani da 15 a 21 anni", "Fr. 58.–"),
              ("Adulti dai 22 anni", "Fr. 75.–")]),
            ("Non soci", "Pernottamento, cena (zuppa, insalata, piatto forte, dessert) e colazione, IVA inclusa",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 50.–"), ("Giovani da 15 a 21 anni", "Fr. 63.–"),
              ("Adulti dai 22 anni", "Fr. 85.–")]),
            ("Famiglie e gruppi", "Sconto infrasettimanale per famiglie (domenica-giovedì) e prezzi per scuole, scout e G+S in settimana",
             [("Famiglie: riduzione per ogni bambino sotto i 15 anni", "Fr. 5.–"), ("Gruppi: ragazzi da 8 a 14 anni", "Fr. 35.–"),
              ("Gruppi: giovani da 15 a 21 anni", "Fr. 45.–")]),
            ("Extra", "Per ragioni igieniche il sacco lenzuolo è obbligatorio",
             [("Camera matrimoniale (supplemento per camera)", "Fr. 20.–"), ("Tè di marcia (1 l)", "Fr. 5.–"), ("Doccia (a persona)", "Fr. 5.–"),
              ("Sacco lenzuolo monouso", "Fr. 7.–")]),
        ],
        prenotare="""<ul>
<li>Riservazione online con il pulsante «Prenota».</li>
<li>Disdette senza costi entro le 18.00 di <strong>due giorni prima</strong> della data riservata.</li>
<li>Pagamento in contanti, con Twint o carta di credito.</li>
<li>Non si accettano riservazioni o richieste tramite social media: per informazioni chiamateci.</li>
</ul>
<p><a class="file-link" href="docs/capanne/adula/disposizioni-per-gli-ospiti-1.pdf">Disposizioni per gli ospiti</a></p>
<p><a class="file-link" href="docs/capanne/adula/2020-cgc-capanne-cas-it.pdf">Condizioni generali delle capanne CAS</a></p>
<p><a class="file-link" href="docs/capanne/adula/pagamento-non-custodita-adula.pdf">Soggiorno invernale: promemoria per il pagamento</a></p>""",
        accessi="""<p><strong>D’estate</strong> la capanna si raggiunge facilmente dalla mulattiera pianeggiante della Val Carassino, partendo da Compietto. La valle è lunga circa 6 km e tocca due alpeggi, l’Alpe Bolla e l’Alpe Bresciana, dove si produce un ottimo formaggio che si gusta anche in capanna. Il fiume vicino ne fa una passeggiata ideale per le famiglie nelle giornate calde; in mountain bike basta circa un’ora.</p>
<p><strong>D’inverno</strong> si sale con gli sci da Dangio per la Val Soi, oppure da Ghirone per il Luzzone e la Val Carassino, con neve sicura e preferibilmente a inizio primavera.</p>
<ul>
<li>Da Compietto (posteggio) per la Val Carassino: 2 h 40, in mountain bike circa 1 h.</li>
<li>Da Dangio (fermata del bus) per la Val Soi: 3 h.</li>
<li>Da Cusiè in Val Malvaglia (posteggio) per il Passo del Laghetto: 5 h.</li>
<li>Dalla Läntahütte per la Bocchetta di Fornee.</li>
<li>D’inverno: da Ghirone 5 h, da Dangio 3 h 30.</li>
</ul>
<p><strong>In auto:</strong> A2 fino a Biasca, poi direzione Lucomagno fino a Campo Blenio e Ghirone; si sale alla diga del Luzzone, la si attraversa e si arriva all’Alpe di Compietto. Oppure si lascia l’auto a Ghirone e si prende il <a href="http://www.autolinee.ch/greina" rel="noopener">bus alpino</a>.</p>
<p><strong>Con i mezzi pubblici:</strong> treno S10 fino a Biasca, bus 131 fino a Ghirone, poi bus alpino verso la diga del Luzzone. Taxi Riviera (Biasca): <a class="num" href="tel:+41918624848">+41 (0) 91 862 48 48</a>.</p>
<p><strong>Traversate ad altre capanne:</strong> <a href="Motterascio.html">Motterascio</a> 5 h; <a href="http://laentahuette.ch/it/startseite.html" rel="noopener">Läntahütte</a> 3 h 30; <a href="http://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 1 h; <a href="http://quarnei.ch/" rel="noopener">Quarnei</a> 3 h.</p>
<p>Cartine: CNS 1:25’000 foglio 1233 Greina; carta scialpinistica 256 S.</p>""",
        attivita="""<p>All’Adula si respira un profumo antico: l’accoglienza e la buona cucina, con un bicchiere di vino, invitano a sdraiarsi sul prato davanti a uno scenario d’eccezione. Da qui si parte per itinerari entusiasmanti, antichi passaggi e creste aeree.</p>
<p>È il posto giusto per i bambini, che possono vedere fiori stupendi a inizio estate, scovare camosci e stambecchi, sentire le marmotte, accarezzare le mucche e bagnarsi nel fiume. Si dorme in una capanna storica, che conserva il fascino del rifugio d’altri tempi, e si sale sulla vetta dell’Adula, ambizione di tanti ticinesi, con il suo ghiacciaio che purtroppo presto sarà solo un ricordo.</p>""",
        pagine=[
            dict(file="cima-adula", titolo="Cima dell’Adula", foto="cima-adula",
                 lead="Sul tetto del Ticino: la salita all’Adula (3402 m) per la via Malvaglia, con discesa sul ghiacciaio di Bresciana.",
                 img=("cordata-vetta", "Una cordata in vetta tra la neve"),
                 corpo="""<p>La salita all’Adula è l’obiettivo di molti escursionisti e alpinisti ticinesi. La cima si sale piuttosto facilmente d’inverno come d’estate; per il ritiro del ghiacciaio e le estati calde è meglio salire prima che la neve si sciolga del tutto, lasciando il ghiacciaio scoperto.</p>
<p>A chi ha nozioni alpinistiche consigliamo l’anello che passa dal laghetto di Cadabi e risale la cresta della via Malvaglia. Vicino alla vetta la roccia lasciata libera dal ghiacciaio è instabile: attenzione. In discesa si può percorrere il ghiacciaio di Bresciana, attenti ai crepacci, fino alla traccia di sentiero che riporta alla Capanna UTOE.</p>""",
                 dati=[("Lunghezza", "8 km"), ("Dislivello", "+1400 m"), ("Tempo", "4-5 h in salita, 2-3 h in discesa"),
                       ("Difficoltà", "PD, tratti attrezzati sulla cresta della via Malvaglia"), ("Da vedere", "Laghetto di Cadabi, ghiacciaio di Bresciana, panorama dalla vetta")],
                 link=[("Mappa online del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721078&amp;N=1150644&amp;trackId=5023916")]),
            dict(file="proposte-gite", titolo="Proposte di gite",
                 lead="Cinque traversate verso altre capanne, dalla via alta della Val Carassino alla Via Crio.",
                 img=("via-alta-carassino", "Un escursionista su una cresta rocciosa sopra la Val Carassino"),
                 corpo="""<p>A chi ha più giorni a disposizione proponiamo percorsi escursionistici e alpinistici alla scoperta di angoli poco conosciuti della Val Carassino. Non sono anelli: collegano la capanna ad altre capanne. La via alta della Val Carassino si percorre nei due sensi ed evita di passare due volte dal fondovalle se si parte o si rientra dal Luzzone; la traversata Cassimoi-Cassinello è una magnifica cavalcata in cresta; la Bocchetta di Fornee apre le porte verso Vals; la traversata verso Quarnei è un classico, adatto anche alle famiglie con ragazzi.</p>""",
                 itinerari=[
                     dict(titolo="Via alta della Val Carassino", img=("via-alta-carassino", "Un escursionista su una cresta rocciosa sopra la Val Carassino"),
                          testo="Da Compietto alla capanna passando in quota, per Sgiu, La Colma, Pinadee e Bresciana.",
                          dati=[("Lunghezza", "7,5 km"), ("Dislivello", "+1050 m"), ("Tempo", "5 h"), ("Difficoltà", "T5")],
                          link=[("Scheda dell’itinerario", "docs/capanne/adula/a-via-alta-della-val-carassino.pdf")]),
                     dict(titolo="Cengie e vette della Val Carassino", img=("cengie-carassino", "Pendii erbosi e cengie sotto cime con la neve"),
                          testo="Il Pizzo Amianto e la sua antica frana, le cengie delle pecore, camosci, stambecchi e l’aquila.",
                          dati=[("Lunghezza", "11,5 km"), ("Dislivello", "+1000 m"), ("Tempo", "5 h"), ("Difficoltà", "T5")],
                          link=[("Scheda dell’itinerario", "docs/capanne/adula/b-cengie-e-vette-della-val-carassino.pdf")]),
                     dict(titolo="Alla Läntahütte per la Bocchetta di Fornee", img=("lago-fornee", "Un laghetto tra le rocce levigate dai ghiacciai"),
                          testo="I segni del ritiro dei ghiacci, le rocce e gli stambecchi, verso la valle di Vals.",
                          dati=[("Lunghezza", "8,7 km"), ("Dislivello", "+1000 m"), ("Tempo", "5 h 30"), ("Difficoltà", "T5")],
                          link=[("Scheda dell’itinerario", "docs/capanne/adula/c-alla-capanna-lanta-dalla-btta-di-fornee.pdf")]),
                     dict(titolo="Facile traversata a Quarnei", img=("laghetto-cadabi", "Il laghetto di Cadabi in una conca rocciosa"),
                          testo="Il ghiacciaio di Bresciana e la sua agonia, le morene laterali, le rocce montonate, il laghetto di Cadabi e il pianoro di Quarnei.",
                          dati=[("Lunghezza", "4 km"), ("Dislivello", "+700 m"), ("Tempo", "3 h 30"), ("Difficoltà", "T3")],
                          link=[("Scheda dell’itinerario", "docs/capanne/adula/d-facile-traversata-a-quarnei.pdf")]),
                     dict(titolo="Via Crio, tappa 6: dal Pizzo Cassimoi al Luzzone", img=("via-crio", "Un escursionista su un passaggio attrezzato tra rocce rossastre"),
                          testo="Tre tremila in una delle tappe più impegnative della <a href=\"https://www.viacrio.ch/\" rel=\"noopener\">Via Crio</a>.",
                          dati=[("Lunghezza", "15,9 km"), ("Dislivello", "+1540 / −1950 m"), ("Tempo", "8 h"), ("Difficoltà", "T6, traversata impegnativa")],
                          link=[("Scheda dell’itinerario", "docs/capanne/adula/e-scaradra-luzzone-passando-dalla-bocchetta-di-fornee.pdf"),
                                ("Prospetto della Via Crio", "docs/capanne/adula/via-alta-crio-prospetto-2024.pdf"),
                                ("Traccia GPX", "https://www.viacrio.ch/s/006-CRIO-GPX-Adla-UTOE-Scaradra-MV.gpx")]),
                 ]),
            dict(file="inverno", titolo="Inverno e primavera", foto="inverno",
                 lead="Cime solitarie per scialpinisti preparati e canali nevosi per l’alpinismo di inizio stagione.",
                 img=("pendio-innevato", "Tracce di sci su un vasto pendio innevato"),
                 corpo="""<h2>L’Adula in inverno</h2>
<p>D’inverno il versante ticinese dell’Adula resta isolato: le valanghe scendono dai versanti della Carassina e la salita dalla Val Soi richiede neve assestata nella parte finale. Quando in valle arriva la primavera, il massiccio offre belle traversate tecniche da capanna a capanna tra la <strong>Läntahütte</strong>, la <strong>Zapporthütte</strong>, l’<strong>Adula</strong> e <strong>Quarnei</strong>: con il giro dell’Adula e le sue varianti si sale ogni giorno almeno una cima oltre i 3000 m.</p>
<ul>
<li><strong>Adula (3402 m) per il Vadrecc di Bresciana:</strong> si sale per l’itinerario estivo (324 a); con buone condizioni si scende direttamente sul ghiacciaio fino a circa 2500 m e con una breve risalita sulla morena si arriva sopra la Capanna UTOE (324 c). PD.</li>
<li><strong>Grauhorn (3258 m):</strong> troppo instabile d’estate, in primavera si raggiunge con l’itinerario 323, salendo a piedi il pendio fino alla cresta a quota 3100. AD.</li>
<li><strong>Piz Jut (3128 m):</strong> per la Bocchetta di Fornee (2885 m, itinerario 320), poi sul versante grigionese fino in vetta; discesa verso la Läntahütte per il Forneitobel (309). AD.</li>
<li><strong>Cima di Pinadee (2486 m):</strong> si affaccia sulla Val Carassina e si sale senza grandi difficoltà in poco più di un’ora dall’Alpe di Bresciana. PD.</li>
</ul>
<h2>Alpinismo primaverile</h2>
<p>Le cime dal Torrone di Nav al Passo Cadabi subiscono lo scioglimento dei ghiacciai: salite un tempo sicure anche d’estate sono oggi pietraie instabili esposte alla caduta di sassi. Meglio affrontarle quando sopra i 2500 m c’è ancora una buona copertura di neve, valutando con attenzione il rigelo notturno.</p>
<p>Con queste premesse sono interessanti i canali nevosi, fino a 50° di pendenza, da salire con ramponi e piccozza:</p>
<ul>
<li>canalone ovest della <strong>Cima dal Laghetto</strong> dalla Val Soi fino al punto 2582 m, F;</li>
<li>Adula per il canale <strong>Damstädten</strong> (a sinistra), parete sud-ovest fino al punto 3205 m, PD;</li>
<li>Adula per il canale <strong>Ezio e Maria</strong> (a destra), parete sud-ovest fino al punto 3205 m, PD+.</li>
</ul>
<p>Anche per il <strong>Grauhorn</strong> (pendio detritico fino a circa 3180 m) e per la <strong>Cima di Fornee</strong>, il <strong>Piz Jut</strong> e la <strong>Punta dello Stambecco</strong> salendo da Fornee è più sicuro e comodo partire a inizio stagione.</p>""",
                 link=[("Itinerari scialpinistici sulla mappa", "https://map.geo.admin.ch/?lang=it&amp;topic=wildruhezonen&amp;bgLayer=ch.swisstopo.pixelkarte-farbe&amp;layers=ch.bafu.wrz-jagdbanngebiete_select,ch.bafu.wrz-wildruhezonen_portal,ch.swisstopo-karto.skitouren&amp;layers_visibility=true,false,true&amp;catalogNodes=1308&amp;E=2721748.94&amp;N=1152606.59&amp;zoom=6&amp;layers_opacity=1,1,0.8")]),
            dict(file="curiosita", titolo="Curiosità",
                 lead="Due capanne e le lotte politiche di cent’anni fa, le antiche transumanze e la ricchezza della Val Carassino.",
                 img=("vetta-tramonto", "Una cima illuminata dal sole del tramonto sopra valli in ombra"),
                 corpo="""<p>A prima vista la Val Carassino sembra lunga e monotona, ma vicino alle capanne la vista si apre sulla vetta dell’Adula, sulla Val Soi e sulla Valle di Blenio. Un occhio attento coglie la ricchezza botanica della valle e gli animali selvatici sui suoi fianchi.</p>
<p>La zona è sfruttata fin dall’inizio del Medioevo dalle popolazioni del fondovalle: la gestione degli alpeggi continua ancora oggi e i suoi prodotti sono molto apprezzati. La vetta dell’Adula e le due capanne ricordano anche le lotte politiche di oltre cent’anni fa, quando dai movimenti borghesi e operai nacquero i gruppi alpinistici «proletari» e l’UTOE, una particolarità ticinese nella storia dell’alpinismo svizzero.</p>""",
                 itinerari=[
                     dict(titolo="Perché due capanne? Cenni di storia", img=("vetta-tramonto", "Una cima illuminata dal sole del tramonto sopra valli in ombra"),
                          testo="Il sogno che il vulcanico presidente Remo Patocchi avrebbe voluto realizzare…",
                          link=[("Leggi tutto", "docs/capanne/adula/a-perche-due-capanne-cenni-di-storia.pdf")]),
                     dict(titolo="Storie di antiche transumanze", img=("dipinto-alpe", "Dipinto di un alpe con una cascina in pietra sotto le cime"),
                          testo="Mille anni fa un periodo molto caldo ha avuto un grande influsso su tutte le Alpi…",
                          link=[("Leggi tutto", "docs/capanne/adula/c-storie-di-antiche-transumanze.pdf")]),
                 ]),
        ],
        foto=[("La capanna", "capanna"), ("I dintorni", "dintorni")],
        foto_lead="La capanna e i dintorni",
    ),

    "Motterascio.html": dict(
        cartella="motterascio",
        avviso="""<strong>Capanna aperta: vi aspettiamo!</strong> Siamo aperti da sabato 13 giugno a sabato 10 ottobre 2026.
Riservate il soggiorno online; per informazioni scriveteci o chiamateci. A presto, Fabio e Vanessa.""",
        capanna="""<p>Al centro di una costellazione di sentieri tra alcuni dei luoghi più belli della Svizzera meridionale, la Capanna Michela Motterascio sorge a 2172 m sull’Alpe Motterascio, al margine sud dell’altopiano della Greina, in un’armonia di legno, rame e sasso. Sotto i pizzi Terri, Coroi, Vial, Gaglianera e Valdraus si passano giornate tra passeggiate, silenzi e relax. Non serve essere alpinisti esperti: bastano curiosità, passione e un po’ di energia.</p>
<p>La capanna è ampia: 70 posti letto con piumoni, un refettorio panoramico da 55 posti con vetrata sulle Alpi, un refettorio «romantico» da 20, servizi interni separati per donne e uomini, doccia quando l’acqua di sorgente basta, locale essiccatoio e ciabatte all’ingresso, anche per i più piccoli. L’acqua è di sorgente, potabile; l’elettricità viene dal fotovoltaico, con un generatore di riserva. Il sacco lenzuolo è obbligatorio, anche a noleggio. Non c’è ricezione telefonica.</p>
<p><strong>Locale invernale:</strong> aperto quando la capanna non è custodita, da metà ottobre a fine maggio, con 10 posti letto con piumoni, bevande, legna e beni di prima necessità (sale, zucchero, caffè in polvere). Il cibo va portato; l’acqua non è garantita (fontana sulla terrazza, se non è ghiacciata) e non c’è WC invernale. La riservazione è obbligatoria, online; la conferma contiene tutte le informazioni.</p>""",
        cucina="""<p>A pranzo la terrazza al sole e il bel refettorio invitano a gustare piatti semplici e locali, caldi e freddi, con un panorama mozzafiato, e il buffet delle torte fatte in casa. La cena è alle 19.00, con piatti secondo la disponibilità e l’estro dello chef; poi una ricca colazione per ripartire. Si cucina soprattutto con la stufa a legna e i fornelli a gas.</p>
<p><strong>Importante:</strong> avvisateci in tempo se siete vegetariani o vegani, o se avete allergie o intolleranze.</p>
<p>Per i bambini ci sono giochi, libri, carta e matite; lungo il sentiero, con un po’ di fortuna, si vedono le marmotte. I cani sono benvenuti ma non entrano in capanna: per la notte c’è la legnaia, riparata e asciutta, con coperta e ciotole. Avvisateci prima.</p>
<p>D’estate la teleferica aiuta i rifornimenti, ma l’elicottero resta indispensabile: vi chiediamo di riportare a valle i vostri rifiuti.</p>""",
        team=dict(titolo="Il guardiano", img=("fabio", "Fabio Merzaghi in cucina con le torte appena sfornate"),
                  testo="""<p>Mi chiamo Fabio Merzaghi e sono cresciuto ai piedi del Monte Generoso, sulle rive del Lago di Lugano. La montagna è sempre stata la mia passione: d’inverno salgo le vette con le pelli di foca, d’estate arrampico.</p>
<p>Lavorare in un rifugio era il mio sogno: l’ho realizzato nell’estate 2023 alla <a href="https://www.fornohuette.ch/" rel="noopener">Capanna del Forno</a>, e poi gestendo per un periodo la <a href="https://www.sac-bluemlisalp.ch/de/Baltschiederklause" rel="noopener">Baltschiederklause</a>, a 2783 m in Vallese. Ho seguito il corso per guardiani del Club Alpino Svizzero. Ingegnere meccanico di formazione, ho lasciato l’ufficio per un’avventura a contatto con la natura.</p>
<p>La capanna si basa su prodotti locali di qualità e su pratiche sostenibili. E senza le mani magiche dei nostri fedelissimi aiutanti non ci sarebbe nemmeno una fetta di torta: grazie di cuore!</p>
<p><strong>Fabio</strong></p>"""),
        tariffe=[
            ("Soci CAS/FAT e club con diritto di reciprocità", "Stagione 2026: pernottamento, cena (zuppa, insalata, piatto forte, dessert) e buffet di colazione, IVA e tassa di soggiorno incluse",
             [("Bambini fino a 7 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 50.–"), ("Giovani da 15 a 21 anni", "Fr. 65.–"),
              ("Adulti dai 22 anni", "Fr. 82.–"), ("Guide alpine", "Fr. 52.–")]),
            ("Non soci", "Stagione 2026: pernottamento, cena e buffet di colazione, IVA e tassa di soggiorno incluse",
             [("Bambini fino a 7 anni", "Fr. 32.–"), ("Ragazzi da 8 a 14 anni", "Fr. 55.–"), ("Giovani da 15 a 21 anni", "Fr. 72.–"),
              ("Adulti dai 22 anni", "Fr. 95.–")]),
            ("Famiglie e gruppi", "Sconto infrasettimanale per famiglie (domenica-giovedì) e prezzi per scuole, scout e G+S (lunedì-giovedì)",
             [("Famiglie: riduzione per ogni bambino sotto i 15 anni", "Fr. 5.–"), ("Gruppi: ragazzi da 8 a 14 anni", "Fr. 40.–"),
              ("Gruppi: giovani da 15 a 18 anni", "Fr. 50.–")]),
            ("Extra", "Per ragioni igieniche il sacco lenzuolo è obbligatorio",
             [("Lunch", "Fr. 10.–"), ("Tè (1 l)", "Fr. 3.–"), ("Doccia (a persona)", "Fr. 5.–"),
              ("Sacco lenzuolo monouso", "Fr. 7.–"), ("Sacco lenzuolo a noleggio", "Fr. 5.–")]),
        ],
        prenotare="""<ul>
<li>Riservazione online con il pulsante «Prenota»; per l’ultimo momento telefonate.</li>
<li><strong>Pagamento solo in contanti</strong>, in franchi o in euro.</li>
<li>Annullamenti e modifiche gratuiti entro le 18.00 di due giorni prima dell’arrivo; entro le 18.00 del giorno prima Fr. 30.– per persona e notte; mancato arrivo non annunciato Fr. 50.– per persona e notte.</li>
</ul>
<p><a class="file-link" href="docs/capanne/motterascio/disposizioni-per-gli-ospiti-1.pdf">Disposizioni per gli ospiti</a></p>
<p><a class="file-link" href="docs/capanne/motterascio/cgc-capanne-cas.pdf">Condizioni generali delle capanne CAS</a></p>""",
        accessi="""<p>D’estate la capanna si raggiunge facilmente a piedi, per lo più su itinerari adatti alle famiglie. D’inverno si sale con gli sci per la Val Camadra e il Passo della Greina (5-6 h), solo con neve assestata e quando i pendii laterali si sono scaricati.</p>
<ul>
<li>Dal Lago di Luzzone, Alpe Garzott: 2 h.</li>
<li>Dal Lago di Luzzone, diga: 3 h 30.</li>
<li>Da Ghirone per il Lago di Luzzone: 4 h 30; per la Val Camadra: 6 h.</li>
<li>Da Pian Geirètt: 3 h 30.</li>
<li>Da Vrin: 5 h; da Vals: 7-8 h.</li>
</ul>
<p><strong>Con i mezzi pubblici:</strong> treno e bus fino a Ghirone, Aquilesco; poi il <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">bus alpino</a> delle Autolinee Bleniesi fino al Lago di Luzzone o a Pian Geirètt, ogni giorno in luglio e agosto, solo nei fine settimana in settembre.</p>
<p><strong>In auto:</strong> A2 fino a Biasca, poi direzione Lucomagno fino a Campo Blenio e Ghirone; si sale alla diga del Luzzone e si costeggia il lago fino all’Alpe Garzott. Posteggi gratuiti a Ghirone-Aquilesco e alla diga (con servizi igienici; ristorante Luzzone da aprile a ottobre); all’Alpe Garzott, dove si compra un ottimo formaggio, i posti sono pochi: arrivate presto o condividete l’auto.</p>
<p><strong>Taxi:</strong> Poglia Mirko (Olivone) <a class="num" href="tel:+41794440712">+41 (0) 79 444 07 12</a>; <a href="https://www.taxiriviera.ch/" rel="noopener">Taxi Riviera</a> (Biasca) <a class="num" href="tel:+41794136868">+41 (0) 79 413 68 68</a>.</p>
<p><strong>Traversate ad altre capanne:</strong> <a href="https://www.terrihuette.ch/" rel="noopener">Terri</a> 2 h 30; <a href="https://www.satlucomagno.ch/wordpress/capanna-scaletta/" rel="noopener">Scaletta</a> 2 h; <a href="http://www.capannabovarina.ch/" rel="noopener">Bovarina</a> 5 h; <a href="Adula.html">Adula CAS</a> 5 h; <a href="http://adula-utoe.ch/" rel="noopener">Adula UTOE</a> 6 h; <a href="https://www.medelserhuette.ch/" rel="noopener">Medels</a> 6 h; <a href="http://laentahuette.ch/" rel="noopener">Länta</a> 7 h; <a href="https://www.rifugioscaradra.ch/" rel="noopener">Rifugio Scaradra</a> 3 h. Itinerari su <a href="https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=10&amp;E=2720474&amp;N=1161992&amp;layers=Wanderland%2CStation%2CAccomodation" rel="noopener">SvizzeraMobile</a>.</p>
<p>Cartine: CNS 1:25’000 foglio 1233 Greina; carta scialpinistica 256 S.</p>""",
        attivita="""<p>La Greina è un altopiano unico tra Ticino e Grigioni, lungo quasi 6 km a oltre 2200 m: una tundra alpina protetta, iscritta nell’inventario federale dei paesaggi d’importanza nazionale. È intatta: gli unici segni dell’uomo sono il Crap la Crusch e il Pass Crap, dove una croce di ferro ricorda che già in epoca romana e nel Medioevo era via di transito e di pascolo.</p>
<p>Qui nascono innumerevoli sorgenti che formano meandri, lanche e paludi, sullo spartiacque continentale: il Brenno della Greina va verso il Mediterraneo, il Rein da Sumvitg verso il Mare del Nord. È la regina dei contrasti, tra il bianco dei ghiacciai, il nero degli scisti e il verde della tundra, con l’arco naturale di pietra di una quarantina di metri, le torbiere, i pinnacoli e le doline. <strong>Per viverne davvero l’incanto, fermatevi due giorni o più.</strong></p>""",
        pagine=[
            dict(file="giro-greina", titolo="Il giro della Greina", foto="giro-greina",
                 lead="La Greina in un giorno: dal Luzzone alla capanna, al Passo della Greina e giù alla Scaletta, con il bus alpino.",
                 img=("piano-greina", "Il piano della Greina con il torrente tra i prati e le montagne"),
                 corpo="""<p>Ghirone, Lago di Luzzone, Capanna Michela Motterascio, Crap la Crusch, Passo della Greina, Capanna Scaletta, Pian Geirètt, Ghirone: per chi ha una sola giornata, grazie al <a href="https://busalpin.ch/regionen/greina/sommer" rel="noopener">bus alpino</a> d’estate il giro si fa in 6-7 ore di cammino.</p>
<p>Dalla fermata si segue la strada sterrata lungo il <strong>Lago di Luzzone</strong>. Dall’Alpe Garzott si entra nel «fiordo», una stretta gola, su un sentiero ben segnalato, ampliato nel 2017 con il sostegno del Patriziato di Aquila. Passato un ponte moderno si sale tra radi larici ai Monti di Rafüsc (1691 m) e per ripidi pendii erbosi al piano di Trachee (1947 m). Attraversato il Ri di Motterascio su un vecchio ponticello di legno e superato l’ultimo strappo a tornanti si arriva alla <strong>capanna</strong> (2172 m, circa 3 h).</p>
<p>Si prosegue verso l’<strong>Alpe Motterascio</strong>: si supera una scala a grate (con i cani si aggira sul versante destro, seguendo il percorso delle mucche) e si attraversa l’alpe tra corsi d’acqua e terreni paludosi fino alla larga sella del <strong>Crap la Crusch</strong> (2268 m, circa 1 h), con un colpo d’occhio fantastico sul Plaun la Greina.</p>
<p>Sempre sul sentiero bianco-rosso si sale al <strong>Passo della Greina</strong> (2355 m) lungo le sorgenti del Reno, che finirà nel Mare del Nord, e si prosegue verso la <strong>Capanna Scaletta</strong> (2205 m, 2 h), guardando da lontano i meandri del Brenno, che invece sfocia nel Mediterraneo. Chi vuole vedere l’<strong>arco della Greina</strong> fa una piccola deviazione lungo i meandri; dall’arco un sentiero bianco-blu porta alla Scaletta, solo per escursionisti esperti e senza ghiaccio né neve; altrimenti si torna sul sentiero bianco-rosso (1 h). Dalla Scaletta la discesa a <strong>Pian Geirètt</strong> è ripida ma breve (1 h), e il bus alpino riporta a Ghirone.</p>
<p>Il giro si fa anche al contrario, consigliato alle famiglie perché la salita da Pian Geirètt è meno faticosa di quella dal Luzzone.</p>""",
                 dati=[("Lunghezza", "17 km"), ("Dislivello", "+700 m"), ("Tempo", "6 h"), ("Difficoltà", "T2"),
                       ("Da vedere", "Alpe Garzott, Alpe Motterascio, Crap la Crusch, lo spartiacque, le sorgenti del Reno e del Brenno, pinnacoli, meandri, l’arco della Greina")],
                 link=[("Mappa online del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=7.09&amp;E=2717383&amp;N=1160737&amp;trackId=4244704")]),
            dict(file="proposte-gite", titolo="Proposte di gite",
                 lead="Sei gite dalla capanna: il Crap la Crusch, il Piz Terri, l’arco della Greina, il Plaun la Greina e la Via Crio.",
                 img=("crap-la-crusch", "Il grande masso del Crap la Crusch con la croce, sul piano della Greina"),
                 corpo="""<p>A chi ha più giorni a disposizione proponiamo percorsi che fanno vivere appieno l’incanto della Greina. Quasi tutti partono e tornano alla capanna.</p>""",
                 itinerari=[
                     dict(titolo="Crap la Crusch", img=("crap-la-crusch", "Il grande masso del Crap la Crusch con la croce, sul piano della Greina"),
                          testo="Facile passeggiata fino al punto centrale della Greina, per l’Alpe Motterascio e il Ri di Motterascio.",
                          dati=[("Lunghezza", "6 km"), ("Dislivello", "+180 m"), ("Tempo", "2 h"), ("Difficoltà", "T2")],
                          link=[("Scheda dell’itinerario", "docs/capanne/motterascio/a-crap-la-crusch.pdf")]),
                     dict(titolo="Piz Terri", img=("piz-terri", "La piramide del Piz Terri illuminata dal sole"),
                          testo="La Valle di Güida, il Piz Terri, il Laghet la Greina, la Val Canal e il Crap la Crusch.",
                          dati=[("Lunghezza", "11 km"), ("Dislivello", "+1100 m"), ("Tempo", "6 h"), ("Difficoltà", "T3-T4")],
                          link=[("Scheda dell’itinerario", "docs/capanne/motterascio/b-piz-terri.pdf")]),
                     dict(titolo="Pizzo Coroi e Capanna Scaletta", img=("arco-greina", "L’arco naturale di pietra della Greina"),
                          testo="Il Pizzo Coroi, l’arco della Greina, i meandri, i pinnacoli e le sorgenti del Brenno e del Reno.",
                          dati=[("Lunghezza", "15 km"), ("Dislivello", "+900 m"), ("Tempo", "6 h"), ("Difficoltà", "T3")],
                          link=[("Scheda dell’itinerario", "docs/capanne/motterascio/c-pizzo-coroi-capanna-scaletta.pdf")]),
                     dict(titolo="Plaun la Greina e Capanna Terri", img=("plaun-la-greina", "Vista dall’alto sulle valli e le creste intorno alla Greina"),
                          testo="Le sorgenti del Reno, i meandri, le torbiere, i terrazzi paralleli, i cuscinetti erbosi e il Muot la Greina.",
                          dati=[("Lunghezza", "13 km"), ("Dislivello", "+400 m"), ("Tempo", "4 h"), ("Difficoltà", "T2")],
                          link=[("Scheda dell’itinerario", "docs/capanne/motterascio/d-plaun-la-greina-capanna-terri.pdf")]),
                     dict(titolo="Val Larciolo", img=("val-larciolo", "Cascine dell’Alpe Larciolo tra i larici dorati d’autunno"),
                          testo="Variante solitaria e selvaggia, fuori dai sentieri marcati, per arrivare alla capanna dall’alto partendo dal Luzzone, per l’Alpe Coroi, l’Alpe Larciolo e l’Alpe Garzott.",
                          dati=[("Lunghezza", "7 km"), ("Dislivello", "+250 m"), ("Tempo", "2 h"), ("Difficoltà", "T2-T3")],
                          link=[("Scheda dell’itinerario", "docs/capanne/motterascio/e-val-larciolo.pdf")]),
                     dict(titolo="Via Crio, tappe 7 e 8", img=("via-crio", "Un escursionista su un passaggio attrezzato tra rocce rossastre"),
                          testo="Due tappe della Via Crio passano dalla capanna.",
                          link=[("Tappa 7", "https://www.viacrio.ch/tappa7"), ("Tappa 8", "https://www.viacrio.ch/tappa8"),
                                ("Prospetto della Via Crio", "docs/capanne/motterascio/prospettocrio.pdf"),
                                ("Altimetria della Via Crio", "docs/capanne/motterascio/altimetria-totale.pdf")]),
                 ]),
            dict(file="trekking-greina-alta", titolo="Trekking Greina Alta", foto="trekking-greina-alta",
                 lead="Da Curaglia a Vals in quattro tappe: tre capanne del CAS, tre culture, tre lingue.",
                 img=("escursionisti-greina", "Escursionisti su un prato verso le montagne"),
                 corpo="""<p>Camona da Medel, Capanna Michela Motterascio, Läntahütte: il trekking Greina Alta, per escursionisti medi o esperti, va da Curaglia a Vals e ha un denominatore comune, il numero 3. Attraversa una regione con 3 capanne del CAS, 3 culture, 3 lingue e 3 vette imponenti. Chi lo percorre per intero può chiedere una prenotazione forfettaria in una delle tre capanne.</p>
<ul>
<li><strong>Giorno 1:</strong> (Disentis) Curaglia (1332 m), Val Platta, Alp Sura (1982 m), Camona da Medel (2524 m). 3 h 30, T3.</li>
<li><strong>Giorno 2:</strong> Camona da Medel, Fuorcla Sura da Lavaz (2759 m), Passo della Greina (2355 m), Crap la Crusch (2268 m), Capanna Michela Motterascio (2172 m). 6 h, T4.</li>
<li><strong>Giorno 3:</strong> Capanna Michela Motterascio, Lago di Luzzone, Larecc (1633 m), Val Scaradra, Passo Soreda (2759 m), Valle della Länta, Läntahütte (2090 m). 7 h, T3.</li>
<li><strong>Giorno 4:</strong> Läntahütte, Furggelti (2712 m), Lago di Zervreila (1862 m), Zervreila (Vals). 5 h, T3.</li>
</ul>""",
                 dati=[("Lunghezza", "45 km"), ("Dislivello", "+4200 m"), ("Tempo", "6-7 h al giorno"), ("Difficoltà", "T3-T4"),
                       ("Periodo", "Da metà luglio a inizio ottobre"),
                       ("Da vedere", "Val Platta, Fuorcla Sura da Lavaz, Greina, Lago di Luzzone, Val Scaradra, Valle della Länta, Lago di Zervreila")],
                 link=[("Il sito del trekking", "https://greinaalta.ch/it/3-3-3-1-italiano/"),
                       ("Mappa online del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=17.65&amp;E=2718864&amp;N=1162797&amp;layers=Wanderland&amp;trackId=4230099")]),
        ],
        foto=[("La capanna", "capanna"), ("La cucina", "cucina"), ("I dintorni", "dintorni")],
    ),

    "MonteBar.html": dict(
        cartella="montebar",
        avviso="""<strong>Strada chiusa:</strong> per il rifacimento del ponte sul fiume Bello la strada da Bidogno al posteggio Monte Bar («strada da Boris») è chiusa ai veicoli.
La capanna si raggiunge solo da Corticiasca. Aperta tutti i giorni fino all’8 novembre.""",
        capanna="""<p>La nuova capanna, di proprietà del CAS Ticino, è stata inaugurata nel 2016, esattamente 80 anni dopo il primo rifugio. Il progetto «Barlume» degli architetti Oliviero Piffaretti e Carlo Romano (Atelier PeR, Mendrisio), scelto tra trenta, è un volume semplice e cubico in legno di larice che ruota intorno al focolare: una lanterna nel paesaggio, in dialogo con le capanne sulle cime vicine.</p>
<p>Il refettorio, cuore della capanna, ha vetrate su tutti i lati e fino a 60 posti; la terrazza è accessibile dal refettorio e dalla cucina. Ai piani superiori camerette da 2, 4 e 6 posti con letti a castello e servizi al piano; c’è una sala workshop per riunioni, corsi e scuole. Al piano inferiore i servizi, il locale aperto agli escursionisti quando la capanna è chiusa e il deposito biciclette, con ricarica delle batterie e piccola officina secondo gli standard Bike Hotel.</p>
<p>Facile da raggiungere su una ricca rete di sentieri e di percorsi in mountain bike, con aspetti naturalistici, storici e paesaggistici sorprendenti, è la meta ideale per famiglie e scuole, o per una notte in rifugio dopo una cena in compagnia.</p>""",
        cucina="""<p>Cuciniamo con passione i prodotti del territorio, freschi e di stagione, con la cultura gastronomica ticinese come riferimento. Il pranzo è servito dalle 11.30 alle 15.00; nel pomeriggio ci sono sempre una zuppa, piatti freddi e torte. La cena è alle 19.00: la sera è gradita la riservazione. Su richiesta prepariamo anche menu per occasioni speciali.</p>
<ul>
<li>Torte fatte in capanna, minestrone di verdure e legumi, polenta ticinese.</li>
<li>Formaggi degli alpeggi vicini e salumi ticinesi.</li>
<li>Griglia in terrazza d’estate, selvaggina in autunno, fondue al formaggio d’inverno.</li>
</ul>
<p>Colazione dalle 7.45 (d’inverno dalle 8.00). I cani non sono ammessi in capanna; i minorenni sono benvenuti se accompagnati da un adulto. Dopo le 22.00 rispettate chi dorme.</p>""",
        team=dict(titolo="I gestori", img=("gestori", "James Mauri e Serge Santese sui pascoli davanti alla capanna"),
                  testo="""<p>Dal 2020 la capanna è gestita da James Mauri e Serge «Seo» Santese, con esperienze in ottime cucine del cantone e non solo. Siamo felici di fare quello che facciamo: vivere qui è una scelta, e soprattutto una bella scuola di vita.</p>
<p><strong>James e Seo</strong></p>"""),
        tariffe=[
            ("Soci CAS/FAT e club con diritto di reciprocità", "Pernottamento con mezza pensione",
             [("Bambini fino a 8 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 40.–"), ("Giovani da 15 a 21 anni", "Fr. 60.–"),
              ("Adulti dai 22 anni", "Fr. 80.–")]),
            ("Non soci", "Pernottamento con mezza pensione",
             [("Bambini fino a 8 anni", "Fr. 30.–"), ("Ragazzi da 8 a 14 anni", "Fr. 45.–"), ("Giovani da 15 a 21 anni", "Fr. 65.–"),
              ("Adulti dai 22 anni", "Fr. 95.–")]),
            ("Camera doppia", "Con letto matrimoniale e biancheria fresca",
             [("Per persona", "Fr. 120.–"), ("Uso singolo", "Fr. 150.–")]),
            ("Famiglie e gruppi", "Famiglie con 2 adulti e almeno 2 giovani fino a 15 anni; gruppi di giovani (scuole, scout, G+S) da lunedì a giovedì",
             [("Famiglie, venerdì-sabato: riduzione a persona", "Fr. 5.–"), ("Famiglie, domenica-giovedì: riduzione a persona", "Fr. 10.–"),
              ("Gruppi: bambini fino a 15 anni", "Fr. 35.–"), ("Gruppi: giovani da 15 a 18 anni", "Fr. 45.–")]),
            ("Extra", "Menu particolari per eventi da concordare con i gestori; sacco lenzuolo obbligatorio",
             [("Lunch da asporto", "Fr. 12.–"), ("Tè di giornata (1 l)", "Fr. 3.–"), ("Doccia (a persona)", "Fr. 5.–"),
              ("Sacco lenzuolo", "Fr. 7.–")]),
            ("Sala workshop", "Con proiettore e tavoli per circa 15 persone",
             [("Al giorno, senza pasti", "Fr. 200.–"), ("Con pranzo o cena", "Fr. 100.–"), ("Con mezza pensione", "gratis")]),
        ],
        prenotare="""<ul>
<li><strong>Estate</strong> (dal 1° maggio all’8 novembre 2026): aperto tutti i giorni.</li>
<li><strong>Inverno</strong> (dal 9 novembre 2026 al 30 aprile 2027): dal venerdì a pranzo alla domenica a pranzo, sempre aperto nei festivi e nelle vacanze scolastiche; negli altri giorni su richiesta. Quando la capanna è chiusa resta accessibile solo l’entrata con i servizi e le bibite: <strong>non si può pernottare</strong>.</li>
<li>Riservazione online con il pulsante «Prenota». Annullamenti e modifiche senza penale entro le 18.00 di 2 giorni prima dell’arrivo fino a 9 persone, di 4 giorni prima da 10 persone; poi Fr. 50.– per persona e notte.</li>
<li>Check-in dalle 16.30 alle 18.00, check-out alle 9.00. Chi pernotta si annuncia all’arrivo e firma il libro degli ospiti.</li>
<li>Pagamento in contanti, EC, Visa o Twint.</li>
</ul>
<p><a class="file-link" href="docs/capanne/montebar/disposizioni-per-gli-ospiti.pdf">Disposizioni per gli ospiti</a></p>
<p><a class="file-link" href="docs/capanne/montebar/cgc-capanna-monte-bar-it-2025.pdf">Condizioni generali della Capanna Monte Bar</a></p>""",
        accessi="""<p>A piedi o in mountain bike la capanna si raggiunge senza grosse difficoltà, per lo più su itinerari adatti alle famiglie. Anche d’inverno si arriva con gli sci o le racchette, ricordando che in montagna le condizioni possono essere diverse dal fondovalle. I posteggi in valle sono pochi: meglio i mezzi pubblici.</p>
<ul>
<li>Da Corticiasca: 1 h 30.</li>
<li>Da Bidogno: 2 h.</li>
<li>Da Isone per la Val Serdena e Piandanazzo: 3 h.</li>
<li>Da Gola di Lago: 2 h 30.</li>
<li>Da Scareglia o Signôra: 3 h 30.</li>
</ul>
<p>Percorsi su <a href="https://schweizmobil.ch/it/map?bgLayer=pk&amp;layers=wanderland%2Cveloland&amp;season=summer&amp;highlightPointCoordinates=2721818-1106610&amp;E=2721449&amp;N=1106526&amp;resolution=4.51" rel="noopener">SvizzeraMobile</a>. Cartina: CNS 1:25’000 foglio 1333 Tesserete.</p>
<p><strong>Sicurezza:</strong> d’inverno ghiaccio e neve rendono insidiosi anche passaggi banali, e sui pendii ripidi e nei canaloni c’è pericolo di valanghe. D’estate pascolano vacche nutrici con i vitelli: non avvicinatevi e tenete i cani al guinzaglio. Chi va in bicicletta rispetti gli escursionisti. Non abbandonate rifiuti e non accendete fuochi all’aperto: in passato il Monte Bar è stato colpito da incendi catastrofici.</p>""",
        attivita="""<p>La zona offre innumerevoli possibilità per la mountain bike, tra asfalto, sterrati e single trail, con giri ad anello panoramici per buona parte dell’anno: i percorsi nazionali 66, 358 e 359 sono descritti da <a href="https://www.luganoregion.com/it/cosa-fare/sport-e-natura/bicicletta" rel="noopener">Lugano Region</a>. Dalla capanna si arriva anche in Valle Cavargna per il Passo San Lucio, o a nord verso la Val Serdena e Rivera.</p>
<p>La catena che da Gola di Lago culmina nei 2115 m del Gazzirola è solcata da sentieri facili. La capanna è meta e tappa del Lugano Trekking e del sentiero nazionale 52; da qui si raggiunge il Camoghè e la Valle Morobbia. Autunno e primavera sono le stagioni ideali.</p>""",
        pagine=[
            dict(file="escursioni", titolo="Escursioni tematiche",
                 lead="Sette sentieri facili tra storia, natura e paesaggio: dalle portatrici di sci alla selvaggina.",
                 img=("escursionista-cresta", "Escursionista su un sentiero di cresta erboso, con i laghi sullo sfondo"),
                 corpo="""<p>Sette itinerari tematici per scoprire angoli poco conosciuti, con incontri e scoperte spesso sorprendenti. Tutti sono facili (T2).</p>""",
                 itinerari=[
                     dict(titolo="Il sentiero delle portatrici di sci", img=("portatrici-sci", "Foto d’epoca di donne che salgono nella neve portando gli sci"),
                          testo="Fa rivivere il ricordo delle donne «sherpa» che dal sagrato della chiesa di San Barnaba portavano fino alla capanna gli sci dei luganesi benestanti, arrivati in autopostale a Bidogno.",
                          dati=[("Lunghezza", "4 km"), ("Dislivello", "+800 m"), ("Tempo", "2 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2721402&amp;N=1105567&amp;trackId=4074166"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/il-sentiero-delle-portatrici-di-sci.pdf")]),
                     dict(titolo="Il sentiero dei barchi", img=("barchi", "Vecchie stalle in pietra sui pascoli sotto il Monte Bar"),
                          testo="Da Corticiasca al terrazzo dei barchi, le costruzioni tipiche della Val Colla dove il bestiame stava in primavera e in autunno, che hanno dato il nome al Monte Bar.",
                          dati=[("Lunghezza", "4 km"), ("Dislivello", "+600 m"), ("Tempo", "2 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721927&amp;N=1105895&amp;trackId=4073878"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/barchi.pdf")]),
                     dict(titolo="Il sentiero panoramico", img=("tramonto-pascoli", "Pascoli al tramonto con le valli nella foschia"),
                          testo="Da Roveredo, dove il compositore Ernst Bloch visse dal 1930 al 1939, si sale ai monti del maggengo, oasi di pace e tranquillità.",
                          dati=[("Lunghezza", "6 km"), ("Dislivello", "+900 m"), ("Tempo", "3 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2720510&amp;N=1105400&amp;trackId=4073853"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/panoramico.pdf")]),
                     dict(titolo="Il sentiero dei ghiacciai", img=("tramonto-luganese", "La capanna sul pendio innevato al tramonto, con le luci del Luganese"),
                          testo="A Gola di Lago torbiere, stagni, piante carnivore e rocce montonate testimoniano il passaggio di una lingua del ghiacciaio del Ticino durante l’ultima glaciazione.",
                          dati=[("Lunghezza", "7 km"), ("Dislivello", "+700 m"), ("Tempo", "3 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2719894&amp;N=1106340&amp;trackId=4074157"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/ghiacciai.pdf")]),
                     dict(titolo="Il sentiero della vegetazione", img=("genziane", "Genziane viola tra l’erba"),
                          testo="Attraversa tutte le fasce di vegetazione, da quella insubrica dei castagni a quella artico-alpina sul crinale della Cima di Moncucco.",
                          dati=[("Lunghezza", "7 km"), ("Dislivello", "+800 m"), ("Tempo", "4 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722942&amp;N=1106858&amp;trackId=4074169"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/vegetazione.pdf")]),
                     dict(titolo="Il sentiero delle piantagioni", img=("piantagioni", "La capanna sui pascoli dorati del Monte Bar"),
                          testo="Un comodo sentiero all’ombra, in una piantagione protettiva iniziata alla fine dell’Ottocento per salvaguardare l’equilibrio idrogeologico della valle del Cassarate.",
                          dati=[("Lunghezza", "7 km"), ("Dislivello", "+800 m"), ("Tempo", "4 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722222&amp;N=1106106&amp;trackId=4074163"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/piantagioni.pdf")]),
                     dict(titolo="Il sentiero della selvaggina", img=("cervo", "Un cervo che bramisce su un pendio erboso"),
                          testo="Un comodo itinerario nel bosco selvaggio, con incontri a sorpresa: caprioli, cervi, scoiattoli e cinghiali.",
                          dati=[("Lunghezza", "7 km"), ("Dislivello", "+200 m"), ("Tempo", "3 h"), ("Difficoltà", "T2")],
                          link=[("Mappa del percorso", "https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=5&amp;E=2722748&amp;N=1107781&amp;trackId=4074167"),
                                ("Scheda dell’itinerario", "docs/capanne/montebar/selvaggina.pdf")]),
                 ]),
            dict(file="mountain-bike", titolo="Mountain bike",
                 lead="Giri ad anello panoramici tra asfalto, sterrati e single trail, con deposito e ricarica in capanna.",
                 img=("mountain-bike", "Due ciclisti in mountain bike sui pascoli, con il Lago di Lugano sullo sfondo"),
                 corpo="""<p>La zona del Monte Bar offre innumerevoli possibilità per la mountain bike: tratti asfaltati, sterrati e single trail si alternano in giri ad anello panoramici percorribili per buona parte dell’anno. I percorsi principali, in particolare quelli della rete nazionale 66, 358 e 359, sono descritti sul sito di <a href="https://www.luganoregion.com/it/cosa-fare/sport-e-natura/bicicletta" rel="noopener">Lugano Region</a>.</p>
<p>Dalla capanna si raggiunge anche la Valle Cavargna per il Passo San Lucio, oppure si scende a nord verso la Val Serdena e Rivera.</p>
<p>La capanna segue gli standard Bike Hotel: deposito chiuso per le biciclette, ricarica delle batterie e piccola officina. Agli amanti della bicicletta chiediamo rispetto per gli escursionisti sui sentieri.</p>"""),
            dict(file="curiosita", titolo="Curiosità",
                 lead="L’origine del nome, i boschi perduti, le donne «sherpa» e i massi coppellari del Monte Bar.",
                 img=("valle-colla", "Vista sulle valli e sul Luganese dai pendii del Monte Bar"),
                 itinerari=[
                     dict(titolo="L’origine del nome", img=("valle-colla", "Vista sulle valli e sul Luganese dai pendii del Monte Bar"),
                          testo="Negli ultimi due milioni di anni la regione si è sollevata in tre fasi, formando tre terrazzi: dei villaggi, dei «barchi» e degli alpeggi. I barchi, tipici della Val Colla e della Capriasca, erano stalle con fienile vicino al paese, non abitate: le donne ci salivano due volte al giorno a mungere, e il latte diventava formaggio e burro in casa. Da «barc» viene il nome del Monte Bar."),
                     dict(titolo="Il bosco perduto", img=("bosco-nebbia", "Boschi e pascoli che emergono da un mare di nebbia"),
                          testo="Un tempo il Monte Bar era coperto di boschi. Nel 1848, dopo i moti di Milano, l’Austria espulse gli emigranti ticinesi dalla Lombardia e chiuse le frontiere: i lavoratori stagionali rientrati aggravarono la crisi alimentare, e per avere più campi e pascoli vaste aree di bosco furono tagliate o bruciate. La montagna rimase spoglia; dopo la terribile alluvione del 1896 i pendii furono ampiamente rimboschiti contro l’erosione, come si vede ancora oggi."),
                     dict(titolo="Un viaggio tra curiosità naturalistiche", img=("ellebori", "Ellebori in fiore controsole"),
                          testo="Nell’ultima era glaciale il ghiaccio restò sotto i 1200 m: le cime libere furono una vera arca di Noè per piante e animali, e tra Caval Drossa e Gazzirola si trovano specie più antiche delle glaciazioni, accanto a piante artiche spinte fin qui dal freddo. In poco spazio si passa dai castagni ai faggi e alle conifere, fino a licheni, muschi e flora alpina in vetta."),
                     dict(titolo="Le «sherpa» ticinesi", img=("portatrici-storica", "Foto d’epoca di portatrici in fila su un pendio innevato"),
                          testo="Quando nel 1936 si costruì la prima capanna, le donne di Bidogno portavano i materiali nella gerla fino al cantiere; poi continuarono portando gli sci dei luganesi dalla piazza della chiesa fino al rifugio, per 50 centesimi al paio. Salivano anche con gli alberelli per rimboschire, raccoglievano foglie e felci per le stalle e, durante la Prima guerra mondiale, portavano il cibo ai soldati fino al Camoghè."),
                     dict(titolo="Massi coppellari e incisioni", img=("masso-coppellare", "Un uomo esamina le incisioni su un masso coppellare nel bosco"),
                          testo="Sul Monte Bar molte rocce portano segni incisi: coppelle, canali, croci, impronte, cerchi di pietre. Forse confini, luoghi di culto del sole o di pellegrinaggio, o cavità per l’acqua piovana e per l’olio acceso. Da vedere il masso di confine tra Bidogno e Corticiasca, la roccia di Gola di Lago, il «Motarell de la Stria» di Roveredo, il «Gigante» e «Ul pé del Crist» di Lelgio, la «Balena bianca» di Caslasc, i massi di Pian di Sotto e il sasso della Madonna di Borisio."),
                 ]),
        ],
        storia=dict(
            file="storia", titolo="Storia della capanna",
            foto="storia",
            lead="Dalla prima scuola di sci del Ticino nel 1935 al rifugio del 1936, fino alla nuova capanna «Barlume» del 2016.",
            img=("capanna-1936", "Foto d’epoca della prima capanna in pietra con sciatori sulla neve"),
            corpo="""<p>Dopo l’esperienza sui monti di Condra, nel 1935 il CAS ottenne la cascina dell’Alpe Musgatina come rifugio invernale per la prima scuola di sci del Canton Ticino, con gli istruttori Tita Calvi e Aldo Balmelli.</p>
<p>Il successo fu tale che già nel 1936, per il cinquantenario della Sezione Ticino, si costruì una capanna sul Monte Bar; il cantiere diede lavoro ai molti emigranti stagionali della valle. Il rifugio divenne presto la meta di numerosi gruppi di sciatori: la domenica sulle piste si contavano anche più di 300 persone. L’amministrazione invernale fu affidata allo Sci Club Lugano, e lo slalom gigante del Monte Bar ebbe un enorme successo. D’estate la capanna era il campo base per le salite sulle montagne vicine.</p>
<p>Nel 2013 la sezione decise di costruire una nuova capanna: quella del 1936, migliorata nel 1993, aveva ormai grossi problemi di logistica, sicurezza e approvvigionamento. Si cercava una struttura moderna, funzionale ed ecologica, con il carattere di un rifugio alpino classico. Il progetto fu pensato con il Comune di Capriasca (progetto Areaviva) e vari partner locali, per valorizzare tutta la regione.</p>
<p>Il concorso del 2014 fu vinto, tra trenta progetti, da «Barlume» degli architetti Oliviero Piffaretti e Carlo Romano (Atelier PeR, Mendrisio): un edificio semplice, cubico, in legno, intorno al focolare come simbolo di incontro. La montagna resta l’elemento dominante e la capanna è una lanterna nel paesaggio. Inaugurata nel 2016, 80 anni dopo il primo rifugio, a 1600 m sui pascoli rivolti a sud è forse la più bella terrazza sul Luganese, sulle Prealpi, sugli Appennini con il Monviso, sul Monte Rosa e sulle Alpi ticinesi, con tramonti indimenticabili.</p>
<p><a href="http://www.simonemengani.ch/nuovo-servizio-fotografico-capanna-monte-bar/" rel="noopener">Fotografie del progetto di Simone Mengani</a></p>"""),
        sostenitori=dict(
            testo="La nuova capanna è nata grazie a questi sostenitori e agli oltre 300 amici, pubblici e privati, che hanno contribuito alla sua realizzazione. Grazie!",
            loghi=[("Repubblica e Cantone Ticino", "cantone-ticino"), ("Swisslos", "swisslos"), ("Città di Lugano", "citta-di-lugano"),
                   ("Comune di Capriasca", "comune-di-capriasca"), ("Banca Raiffeisen del Cassarate", "raiffeisen"), ("BancaStato", "bancastato"),
                   ("Cornèr Banca", "corner-banca"), ("EFG", "efg"), ("Lugano Turismo", "lugano-turismo"), ("Revifida", "revifida"),
                   ("Ernst Göhner Stiftung", "ernst-gohner-stiftung"), ("Lambertini, Ernst & Partners", "lambertini-ernst-partners"),
                   ("Blue Planet", "blue-planet"), ("The North Face e VF", "the-north-face-vf"), ("Ente regionale per lo sviluppo del Luganese", "ersl")]),
        foto=[("La capanna", "capanna"), ("La cucina", "cucina"), ("I dintorni", "dintorni")],
    ),

    "BaitaDelLuca.html": dict(
        cartella="baitadelluca",
        capanna="""<p>La baita ha 16 posti letto in due camere da 4 e da 12, un refettorio con cucina a gas e camino a legna, acqua calda e doccia; l’illuminazione è a pannelli solari. Piatti e pentole sono a disposizione e le bibite ci sono anche in assenza della responsabile. Ricezione discreta, niente wi-fi e niente telefono.</p>
<p>È aperta tutto l’anno ma non è custodita: la porta è chiusa e il codice per entrare si chiede alla responsabile. Facile e veloce da raggiungere, è usata anche per corsi, giornate di formazione o semplicemente per una cena in compagnia.</p>""",
        tariffe=[
            ("Soci CAS/FAT/CAI/DAV", "Pernottamento, tasse incluse",
             [("Adulti dai 22 anni", "Fr. 15.–"), ("Giovani da 6 a 21 anni, aspiranti guida e capigita CAS", "Fr. 8.–"),
              ("Bambini fino a 5 anni", "gratis"), ("Guide alpine UIAGM", "gratis")]),
            ("Non soci", "Pernottamento, tasse incluse",
             [("Adulti dai 20 anni", "Fr. 25.–"), ("Giovani da 6 a 19 anni", "Fr. 12.–"), ("Bambini fino a 5 anni", "gratis")]),
            ("Supplementi", "Il sacco lenzuolo è obbligatorio e non è disponibile in baita",
             [("Uso del gas per cucinare (al giorno)", "Fr. 5.–"), ("Uso della legna (al giorno)", "Fr. 5.–"), ("Doccia (a persona)", "Fr. 5.–")]),
        ],
        prenotare="""<ul>
<li><strong>Prenotazione indispensabile</strong> via e-mail a <a href="mailto:baitaluca@casticino.ch">baitaluca@casticino.ch</a>, con nome, cognome, indirizzo e numero di cellulare.</li>
<li>Disdette senza costi entro le 18.00 di <strong>due giorni prima</strong> della data riservata.</li>
<li>Il codice per accedere alla chiave lo danno i responsabili; d’inverno la porta si apre su richiesta, secondo il meteo.</li>
<li>Portate sacco lenzuolo e federa del cuscino (55×80).</li>
<li>Pagamento con il codice QR (nel libro della baita) o con Twint.</li>
<li>Divieto assoluto di fumare; i cani sono ammessi solo nel soggiorno, non nel dormitorio.</li>
<li>Non si accettano riservazioni o richieste tramite social media: per informazioni chiamate.</li>
</ul>
<p><a class="file-link" href="docs/capanne/baitadelluca/2020-cgc-capanne-cas-it.pdf">Condizioni generali delle capanne CAS</a></p>""",
        accessi="""<ul>
<li>Da Rosone (bus): 1 h, +270 m, T2 (<a href="https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2722290&amp;N=1102884&amp;layers=Wanderland%2CStation&amp;trackId=5273099" rel="noopener">percorso</a>).</li>
<li>Da Sonvico (bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721523&amp;N=1102174&amp;layers=Wanderland%2CStation&amp;trackId=5273106" rel="noopener">percorso</a>).</li>
<li>Da Villa Luganese (bus): 1 h 45, +500 m, T2 (<a href="https://map.schweizmobil.ch/?lang=it&amp;bgLayer=pk&amp;season=summer&amp;resolution=2&amp;E=2721748&amp;N=1101916&amp;layers=Wanderland%2CStation&amp;trackId=5273108" rel="noopener">percorso</a>).</li>
</ul>
<p>Cartina: CNS 1:25’000 foglio 1333 Tesserete.</p>""",
        pagine=[
            dict(file="attivita", titolo="Escursioni e arrampicata",
                 lead="Escursioni verso le cime e le capanne vicine, più di 200 vie sul calcare dei Denti della Vecchia e la Lugano Bike 66.",
                 img=("sentiero-denti", "Un escursionista sul sentiero sotto le guglie dei Denti della Vecchia"),
                 itinerari=[
                     dict(titolo="Escursioni", img=("sentiero-denti", "Un escursionista sul sentiero sotto le guglie dei Denti della Vecchia"),
                          testo="Dalla baita all’Alpe Bolla 3 h, a Villa Luganese 3 h, alla cima della Fojorina 4 h; da Brè alla baita 4-5 h; dalla baita alla Capanna San Lucio 4 h e alla <a href=\"MonteBar.html\">Capanna Monte Bar</a> 6 h, o 9 h passando dalle cime Fojorina e Gazzirola.",
                          link=[("Dall’archivio, 1997: Prealpi ticinesi 5, dal Passo San Jorio al Monte Generoso", "docs/capanne/baitadelluca/baita-del-luca-prealpi-ticinesi-5-passo-s-jorio-generoso.pdf")]),
                     dict(titolo="Arrampicata", img=("arrampicata-denti", "Arrampicatori sulle placche calcaree dei Denti della Vecchia"),
                          testo="I Denti della Vecchia sono un paradiso per l’arrampicata, con più di 200 vie su calcare. La guida del Gruppo Scoiattoli è online su <a href=\"https://scoiattoli.ch/\" rel=\"noopener\">scoiattoli.ch</a>; in baita c’è anche la versione cartacea da consultare.",
                          link=[("Guida dei Denti della Vecchia (Gruppo Scoiattoli)", "https://scoiattoli.ch/wp-content/uploads/2020/06/GUIDA-DENTI-DELLA-VECCHIA-.pdf"),
                                ("Denti della Vecchia: nuove vie 2023", "docs/capanne/baitadelluca/denti-news-2023.pdf"),
                                ("Denti della Vecchia: Nirvana 2023", "docs/capanne/baitadelluca/denti-nirvana-news-2023.pdf"),
                                ("Denti della Vecchia: Paléo 2023", "docs/capanne/baitadelluca/denti-paleo-news-2023.pdf")]),
                     dict(titolo="Mountain bike", img=("mountain-bike", "Un ciclista in mountain bike su un sentiero nel bosco"),
                          testo="Diversi itinerari passano nei dintorni, e la baita è vicinissima al percorso Lugano Bike 66.",
                          link=[("La mountain bike su Lugano Region", "https://www.luganoregion.com/it/cosa-fare/sport-e-natura/bicicletta")]),
                 ]),
        ],
        foto=[("La baita", "capanna"), ("I dintorni", "dintorni")],
        foto_lead="La baita e i dintorni",
    ),
}
