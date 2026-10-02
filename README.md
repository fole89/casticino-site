# casticino.ch

Sito della Sezione Ticino del Club Alpino Svizzero, pubblicato con GitHub Pages sul dominio **casticino.ch**.

Sito statico in HTML, CSS e JavaScript semplici, senza framework né passaggi di build. Ogni pagina è un file `.html` nella cartella principale.

```
index.html, comitato.html, …   pagine del sito (generate, non modificarle a mano)
scripts/redesign/               genera le pagine: python scripts/redesign/pages.py
assets/site.css                 stile di tutto il sito
assets/site.js                  menu, comparsa allo scorrimento, menu mobile
assets/foto.js                  pagina Foto: legge data/foto.json
assets/logo-cas.webp            stemma
assets/img/<tema>/              foto del sito in WebP: paesaggi, capanne, attivita, corsi, news, pubblicazioni
assets/img/originali/           foto originali ad alta risoluzione (non pubblicate, escluse da git)
assets/img/persone/<gruppo>/    foto profilo (WebP 240×280) di comitato e dicasteri, nome-cognome.webp
assets/sponsor/                 loghi degli sponsor nel footer (originali/ = file ricevuti)
data/foto.json                  ultime gite con foto (generato in automatico)
docs/<tema>/                    PDF della sezione per tema (scale-difficolta, promemoria, cartine, moduli, corsi, noleggio,
                                annuari, informazione, statuto-visione, news);
                                nomi in minuscolo con trattini, i link sono in scripts/redesign/pages.py
data/foto-overrides.json        correzioni manuali a titoli e testi delle gite
data/cerca.json                 indice della pagina Cerca (generato da scripts/redesign/pages.py)
scripts/update_foto.py          legge le cartelle foto via FTP e scrive data/foto.json
.github/workflows/update-foto.yml   esegue lo script ogni giorno
.nojekyll                       pubblica i file così come sono
```

---

## 1. Creare il repository e attivare Pages

1. Crea su GitHub un repository, per esempio `cas-ticino/casticino-site`, e carica tutti questi file sul ramo `main`.
2. Vai in **Settings › Pages**.
3. In **Build and deployment** scegli **Source: Deploy from a branch**, poi **Branch: `main` / `(root)`**, e salva.
Dopo un paio di minuti il sito è raggiungibile su `https://fole89.github.io/casticino-site/` (repository attuale: `fole89/casticino-site`).

> **Dominio personalizzato tolto per ora.** Finché il DNS di casticino.ch punta al vecchio sito, la repo non contiene il file `CNAME`: altrimenti l'indirizzo github.io rimanderebbe a casticino.ch, cioè al vecchio sito, e non si potrebbe vedere la versione nuova. Il dominio si rimette al punto 2.

## 2. Collegare il dominio casticino.ch

Nel pannello di chi gestisce il DNS di casticino.ch **cambia solo i record del sito**:

| Tipo  | Nome            | Valore                          |
|-------|-----------------|---------------------------------|
| A     | `@` (casticino.ch) | `185.199.108.153`            |
| A     | `@`             | `185.199.109.153`               |
| A     | `@`             | `185.199.110.153`               |
| A     | `@`             | `185.199.111.153`               |
| AAAA  | `@`             | `2606:50c0:8000::153`           |
| AAAA  | `@`             | `2606:50c0:8001::153`           |
| AAAA  | `@`             | `2606:50c0:8002::153`           |
| AAAA  | `@`             | `2606:50c0:8003::153`           |
| CNAME | `www`           | `fole89.github.io`              |

Prima di cambiarli, verifica questi indirizzi sulla guida ufficiale di GitHub: *Managing a custom domain for your GitHub Pages site*.

Note sul CNAME:
- il valore è solo il nome utente GitHub, **senza** `/casticino-site`;
- il dominio principale (`casticino.ch`, senza www) non può avere un CNAME: per quello servono i record A e AAAA qui sopra;
- alcuni pannelli DNS vogliono il punto finale (`fole89.github.io.`), altri lo aggiungono da soli;
- se il repository passa a un account o un'organizzazione della sezione, il valore diventa `<nome-organizzazione>.github.io`.

**Non toccare:**
- i record **MX** e TXT della posta (info@casticino.ch & co.);
- i sottodomini esistenti, come `capannacristallina.casticino.ch`, `campotencia.casticino.ch` e gli altri siti delle capanne.

Al momento del cambio DNS rimetti il dominio: crea nella cartella principale il file `CNAME` con dentro solo `casticino.ch` e fai push. In alternativa scrivi `casticino.ch` in **Settings › Pages › Custom domain**: GitHub crea il file da solo.

Quando il DNS si è propagato (da qualche minuto fino a 48 ore), torna in **Settings › Pages** e attiva **Enforce HTTPS**.

Consigliato: in **Settings (dell'account o dell'organizzazione) › Pages › Verified domains** verifica casticino.ch, così nessun altro può usarlo su GitHub.

## 3. Foto automatiche da Droptour

Lo script `scripts/update_foto.py` fa questo:

1. si collega via FTP alla cartella delle foto delle gite;
2. elenca le cartelle dell'anno in corso e di quello precedente (`AAAA-MM-GG-titolo---luogo`) e prende le più recenti, di default 15;
3. per ciascuna legge i nomi delle foto direttamente nella cartella della gita (via FTP non ci sono sottocartelle) e costruisce gli indirizzi pubblici di miniatura (`thumbnails/`) e foto grande (`mysize/`), con lo stesso nome del file;
4. scrive `data/foto.json`, solo se qualcosa è cambiato.

Le immagini **non vengono copiate**: restano su ssl.dropnet.ch e il sito le carica da lì.

### Configurazione (una volta sola)

In **Settings › Secrets and variables › Actions**:

**Secrets** (riservati):
- `FTP_HOST`: server FTP
- `FTP_USER`: utente (meglio un utente in **sola lettura**)
- `FTP_PASSWORD`

**Variables** (facoltative, servono solo se i valori di default non vanno bene):
- `FTP_BASE`: percorso FTP della cartella delle gite. Default: `/casticino/dropbox/photo/gite`. **Controllalo**: dipende da dove ti fa entrare l'FTP dopo il login.
- `PUBLIC_BASE`: l'indirizzo web che corrisponde a `FTP_BASE`. Default: `https://ssl.dropnet.ch/casticino/dropbox/photo/gite`
- `FTP_TLS`: `1` per FTPS (default), `0` per FTP semplice
- `MAX_ALBUMS`: quante gite mostrare (default `15`)

Poi vai in **Actions › Aggiorna foto da Droptour › Run workflow** per il primo avvio. In seguito il workflow gira da solo ogni mattina.

### Prova in locale

```bash
FTP_HOST=… FTP_USER=… FTP_PASSWORD=… python3 scripts/update_foto.py
python3 -m http.server 8000      # poi apri http://localhost:8000/foto.html
```

La pagina Foto va aperta tramite un server, anche quello locale qui sopra. Aperta con doppio clic, il browser blocca la lettura di `foto.json`.

### Titoli e testi

- **Di default** titolo, luogo, resoconto e link alla scheda della gita arrivano dalla galleria pubblica di Droptour (`https://ssl.dropnet.ch/casticino/gite/index.php?page=galery_overview`, senza login). L'abbinamento con la cartella delle foto avviene tramite l'indirizzo delle foto. Basta quindi scrivere il resoconto su Droptour: il giorno dopo compare sul sito.
- **Se la galleria non è raggiungibile** titolo e luogo vengono dal nome della cartella: `valsolda-bassa-500-m---italia` diventa «Valsolda Bassa 500 m», «Italia». Le sigle dei cantoni (`ur`, `ti`, …) diventano maiuscole.
- **Per correggere** un titolo o un testo solo sul sito, modifica `data/foto-overrides.json`. Usa come chiave il nome della cartella e come campi `title`, `place`, `text`, `link`. Le correzioni vincono sempre, anche su Droptour, quindi usale solo quando serve davvero.

## 4. Da completare prima di andare online

- Segnaposto da riempire: foto della sede, foto profilo dei dicasteri e di due membri del comitato (Geoffroy Jolly, Flavia Spinelli: oggi mostrano le iniziali), alcuni PDF dei corsi, l'ispettore della Capanna Motterascio.
- **News**: le notizie sono in `data/news.json` (importate una volta dal vecchio sito con `scripts/import_news.py`). Per aggiungerne una si inserisce una voce in cima al file e si rigenerano le pagine: compare in `news.html`, nella sua pagina `news/<anno>/<AAAA-MM-GG>-<titolo-breve>.html` e, se è tra le ultime 3, in home.
- **Annuari e Informazione**: si mette il PDF in `docs/annuari/annuario-<anno>.pdf` o `docs/informazione/informazione-<anno>-<mese>.pdf`, si lancia `python scripts/copertine.py` (crea la copertina) e si rigenerano le pagine.
