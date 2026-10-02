# Area di redazione delle news

L’area di redazione è su **https://fole89.github.io/casticino-site/admin/** (dopo il cambio di dominio: `https://casticino.ch/admin/`).
Si entra con un account GitHub che ha accesso in scrittura al repository `fole89/casticino-site`.

Come funziona: l’area di redazione (Decap CMS, configurazione in `admin/config.yml`) salva ogni news come file
`data/news/<data>-<titolo>.json` direttamente nel repository. Il workflow `.github/workflows/news.yml` parte da solo,
converte le foto (`scripts/prepara_news.py`), rigenera il sito (`scripts/redesign/pages.py`) e lo pubblica:
la news è online in uno o due minuti.

## Attivazione (una volta sola)

Per il login serve un piccolo servizio che custodisce la chiave segreta di GitHub: è `worker.js` in questa cartella,
da pubblicare gratis su Cloudflare Workers.

### 1. Il servizio su Cloudflare
1. Crea un account gratuito su <https://dash.cloudflare.com/sign-up>.
2. **Workers & Pages › Create › Create Worker**, nome `casticino-cms-auth`, **Deploy**.
3. **Edit code**: sostituisci tutto il codice con il contenuto di `worker.js`, poi **Deploy**.
4. Annota l’indirizzo del Worker, del tipo `https://casticino-cms-auth.<tuo-account>.workers.dev`.

### 2. L’applicazione su GitHub
1. GitHub › **Settings › Developer settings › OAuth Apps › New OAuth App**:
   - Application name: `CAS Ticino, redazione news`
   - Homepage URL: `https://fole89.github.io/casticino-site/`
   - Authorization callback URL: `https://casticino-cms-auth.<tuo-account>.workers.dev/callback`
2. **Register application**, poi **Generate a new client secret**. Annota *Client ID* e *Client secret*.

### 3. Collegare le due cose
1. Nel Worker su Cloudflare: **Settings › Variables and Secrets › Add**:
   - `GITHUB_CLIENT_ID` = il Client ID (tipo *Text*)
   - `GITHUB_CLIENT_SECRET` = il Client secret (tipo *Secret*)
   - `ALLOWED_ORIGINS` = `https://fole89.github.io,https://casticino.ch` (tipo *Text*)
   - **Deploy**.
2. In `admin/config.yml` sostituisci in `base_url` l’indirizzo provvisorio con quello del Worker, poi commit e push.

### 4. I redattori
Repository su GitHub › **Settings › Collaborators › Add people**: aggiungi l’account GitHub di ogni redattore
con ruolo **Write**. Ognuno riceve un invito via e-mail da accettare.

### Dopo il cambio di dominio (casticino.ch)
- In `admin/config.yml` aggiorna `site_url` e `display_url`.
- Nell’applicazione OAuth di GitHub aggiorna la *Homepage URL* (il callback resta quello del Worker).
- `ALLOWED_ORIGINS` contiene già `https://casticino.ch`.

## Guida per chi scrive le news

1. Vai su `…/admin/` e clicca **Accedi con GitHub** (la prima volta GitHub chiede di autorizzare l’applicazione).
2. **News › + news**.
3. Compila:
   - **Titolo** e **Data** (l’ora serve solo a mettere in ordine le news dello stesso giorno); il titolo breve e in minuscolo normale, senza parole TUTTE MAIUSCOLE;
   - **Foto principale** (JPG o PNG, anche grande: viene ridimensionata) e la sua **descrizione**;
   - **Riassunto** (facoltativo: due righe per la scheda in home; se vuoto si usa l’inizio del testo);
   - **Testo**, con grassetto, corsivo, link, titoletti, elenchi; con **+** si inserisce una foto nel testo;
   - **Allegati PDF**: titolo del link e file.
4. A destra c’è l’**anteprima** con l’aspetto del sito (l’icona a occhio la mostra o la nasconde).
5. Per pubblicare: **Pubblica › Pubblica ora**. Finché non lo fai, la news non è salvata né pubblicata.
6. Dopo uno o due minuti la news è online: in home, nella pagina News e nella ricerca.

Per correggere una news la si apre dalla lista, si modifica e si ripubblica. **Cancella voce** la toglie dal sito.
Le news importate dal vecchio sito hanno il testo nel campo «Testo HTML»: si possono correggere lì.
