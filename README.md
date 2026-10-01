# casticino.ch

Sito della Sezione Ticino del Club Alpino Svizzero, pubblicato con GitHub Pages sul dominio **casticino.ch**.

Sito statico in HTML, CSS e JavaScript semplici, senza framework né passaggi di build. Ogni pagina è un file `.html` nella cartella principale.

```
index.html, Comitato.html, …   pagine del sito
assets/site.js                  menu mobile
assets/foto.js                  pagina Foto: legge data/foto.json
assets/logo-cas.webp            stemma
data/foto.json                  ultime gite con foto (generato in automatico)
data/foto-overrides.json        correzioni manuali a titoli e testi delle gite
scripts/update_foto.py          legge le cartelle foto via FTP e scrive data/foto.json
.github/workflows/update-foto.yml   esegue lo script ogni giorno
CNAME                           dominio personalizzato (casticino.ch)
.nojekyll                       pubblica i file così come sono
```

---

## 1. Creare il repository e attivare Pages

1. Crea su GitHub un repository, per esempio `cas-ticino/casticino-site`, e carica tutti questi file sul ramo `main`.
2. Vai in **Settings › Pages**.
3. In **Build and deployment** scegli **Source: Deploy from a branch**, poi **Branch: `main` / `(root)`**, e salva.
4. In **Custom domain** dovrebbe comparire `casticino.ch`, letto dal file `CNAME`. Se manca, scrivilo e salva.

Dopo un paio di minuti il sito è raggiungibile su `https://<utente>.github.io/casticino-site/`. Collegando il DNS (punto 2) sarà anche su casticino.ch.

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
| CNAME | `www`           | `<utente-o-organizzazione>.github.io` |

Prima di cambiarli, verifica questi indirizzi sulla guida ufficiale di GitHub: *Managing a custom domain for your GitHub Pages site*.

**Non toccare:**
- i record **MX** e TXT della posta (info@casticino.ch & co.);
- i sottodomini esistenti, come `capannacristallina.casticino.ch`, `campotencia.casticino.ch` e gli altri siti delle capanne.

Quando il DNS si è propagato (da qualche minuto fino a 48 ore), torna in **Settings › Pages** e attiva **Enforce HTTPS**.

Consigliato: in **Settings (dell'account o dell'organizzazione) › Pages › Verified domains** verifica casticino.ch, così nessun altro può usarlo su GitHub.

## 3. Foto automatiche da Droptour

Lo script `scripts/update_foto.py` fa questo:

1. si collega via FTP alla cartella delle foto delle gite;
2. elenca le cartelle dell'anno in corso e di quello precedente (`AAAA-MM-GG-titolo---luogo`) e prende le più recenti, di default 15;
3. per ciascuna legge `thumbnails/` e costruisce gli indirizzi pubblici di miniatura e foto grande (`mysize/`), con lo stesso nome del file;
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
python3 -m http.server 8000      # poi apri http://localhost:8000/Foto.html
```

La pagina Foto va aperta tramite un server, anche quello locale qui sopra. Aperta con doppio clic, il browser blocca la lettura di `foto.json`.

### Titoli e testi

- **Di default** titolo e luogo vengono dal nome della cartella: `valsolda-bassa-500-m---italia` diventa «Valsolda Bassa 500 m», «Italia». Le sigle dei cantoni (`ur`, `ti`, …) diventano maiuscole.
- **Per correggere** un titolo o aggiungere il racconto della gita, modifica `data/foto-overrides.json`. Usa come chiave il nome della cartella e come campi `title`, `place`, `text`, `link`. Le correzioni vincono sempre.
- **Da fare:** collegare l'API XML di Droptour nella funzione `fetch_droptour()` dello script, così titoli e testi arrivano da soli.

> **Nota:** il `data/foto.json` incluso è un esempio con tre gite e una sola foto ciascuna. Il primo avvio del workflow lo sostituisce con i dati veri.

## 4. Da completare prima di andare online

- I PDF in **Documenti**, **Corsi** e **Noleggio** puntano ancora a `casticino.ch/wp-content/…`. Quando il dominio passa a GitHub quei link smettono di funzionare: copia i PDF in una cartella `docs/` del repository e aggiorna i link.
- Segnaposto da riempire: foto delle capanne e della sede, foto profilo di comitato e dicasteri, Statuto, Visione e strategia, Organigramma, Annuario, alcuni PDF dei corsi, l'ispettore della Capanna Motterascio.
- La pagina **News** è statica: per aggiungere una notizia si modifica `News.html` (e il blocco «Dalla sezione» in `index.html`).
