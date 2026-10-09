# Noleggio materiale: richieste online

Il modulo nella pagina **Noleggio** (`noleggio.html`, anche in `de/` ed `en/`) mostra il materiale libero per le date
scelte e invia la richiesta. Dietro c’è un piccolo servizio su Cloudflare Workers (`worker.js` in questa cartella)
con un database D1 gratuito: salva le richieste, calcola la disponibilità giorno per giorno, manda le e-mail e offre
la pagina di gestione **/admin**, protetta da password. I dati personali stanno solo lì, mai nel repository.

## Come funziona

- **Inventario**: `data/noleggio-inventario.json`. Ci sono le quantità per articolo, le taglie (solo imbracature e pedule),
  i set e i prezzi. Lo leggono la pagina (modulo) e il servizio, che lo scarica dal sito pubblicato
  (con al massimo 5 minuti di ritardo). Dopo una modifica: `python scripts/redesign/pages.py noleggio.html de/noleggio.html en/noleggio.html`,
  poi commit e push.
- **Disponibilità**: per ogni giorno del periodo si sommano i pezzi delle richieste *da confermare*, *confermate* e
  *ritirate*. È libero il minimo su tutti i giorni. Un set (es. ARVA, sonda e pala) usa i pezzi singoli: si può
  noleggiare se tutti i suoi pezzi sono liberi, e chi noleggia il set li occupa.
- **Richiesta**: da domani fino a un anno avanti, durata 1–30 giorni. Il socio riceve subito una ricevuta, che dice che
  la richiesta vale solo con la conferma. Il responsabile riceve un’e-mail con tutti i dati: rispondendo a quell’e-mail
  si scrive direttamente al socio.
- **Gestione** su `https://casticino-noleggio.<account>.workers.dev/admin`:
  - *Da confermare* → **Conferma** o **Rifiuta**: il socio riceve un’e-mail con l’eventuale messaggio (ad esempio
    l’orario di ritiro).
  - *Confermata* → **Ritirata** quando il materiale esce, oppure **Annulla**, con un’e-mail al socio.
  - *Ritirata* → **Riconsegnata**: da quel momento il materiale torna libero.
  - Una richiesta lasciata *Da confermare* per più di una settimana scade da sola (di notte): diventa *Scaduta*, il
    materiale torna libero e il socio riceve un’e-mail che lo invita a mandarne una nuova.
  - Le richieste rifiutate, annullate, scadute o riconsegnate si possono eliminare. Comunque il servizio le cancella da solo
    12 mesi dopo la fine del noleggio (lo dice l’informativa sulla privacy).

## Attivazione (una volta sola)

Serve Node.js. Tutti i comandi `npx wrangler …` si lanciano **da questa cartella** (`scripts/noleggio`, dove c’è
`wrangler.toml`). Lanciati dalla radice del sito, wrangler propone di pubblicare tutto il sito come Worker statico: va interrotto con Ctrl+C.

### 1. Il servizio e il database
```bash
cd scripts/noleggio
npx wrangler login                                          # apre il browser: accesso all'account Cloudflare (lo stesso del login del CMS)
npx wrangler d1 create casticino-noleggio --location weur   # database in Europa occidentale
```
Copia il `database_id` stampato in `wrangler.toml` (al posto di `DA-COMPILARE`), poi:
```bash
npx wrangler d1 execute casticino-noleggio --remote --file=schema.sql
npx wrangler deploy
```
L’indirizzo del Worker è del tipo `https://casticino-noleggio.fole89.workers.dev`. Se è diverso, aggiornalo in
`NOLEGGIO_API` in `scripts/redesign/pages.py`.

### 2. La password della gestione
```bash
npx wrangler secret put ADMIN_PASSWORD
```
Scegli una password lunga (almeno 16 caratteri): è l’unica protezione di /admin. Il browser la chiede alla prima
apertura di /admin; il nome utente non conta. Contro i tentativi di indovinarla, /admin accetta al massimo
30 richieste al minuto per indirizzo IP (`[[ratelimits]]` in `wrangler.toml`, attivo con `npx wrangler deploy`):
chi lo supera riceve «Troppi tentativi» per un minuto.

### 3. La protezione dai programmi automatici (Turnstile)
1. Cloudflare › **Turnstile › Add widget**: nome `Noleggio CAS Ticino`, domini `fole89.github.io`, `casticino.ch`
   e `localhost`, modalità *Managed*.
2. Copia la **Site Key** in `NOLEGGIO_TURNSTILE` in `scripts/redesign/pages.py`.
3. Salva la **Secret Key** nel servizio:
   ```bash
   npx wrangler secret put TURNSTILE_SECRET
   ```

Senza `TURNSTILE_SECRET` il servizio rifiuta tutte le richieste.

### 4. Le e-mail (Brevo)
1. Crea un account gratuito su <https://www.brevo.com> (300 e-mail al giorno).
2. **Senders, Domains & Dedicated IPs › Senders › Add a sender**: `fole89@gmail.com`, poi conferma il codice che arriva
   per e-mail.
3. **SMTP & API › API Keys › Generate a new API key**, poi:
   ```bash
   npx wrangler secret put BREVO_API_KEY
   ```

Senza `BREVO_API_KEY` le richieste si salvano lo stesso, ma non parte nessuna e-mail.

### 5. Pubblicare la pagina
```bash
python scripts/redesign/pages.py
```
Poi commit e push dalla radice del repository.

## Quando `noleggio@casticino.ch` sarà attiva
- In `wrangler.toml`: `MAIL_GESTORE` e `MAIL_MITTENTE` = `noleggio@casticino.ch`, poi `npx wrangler deploy`.
- Su Brevo aggiungi il mittente, o meglio il dominio `casticino.ch`. Il dominio va verificato con alcuni record DNS
  nuovi (DKIM): vanno **aggiunti** senza toccare i record MX/TXT che ci sono già.
- Sul sito `NOLEGGIO_MAIL` in `scripts/redesign/pages.py` è già `noleggio@casticino.ch`: non serve cambiarlo.

## Dopo il cambio di dominio (casticino.ch)
In `wrangler.toml` cambia `INVENTARIO_URL` in `https://casticino.ch/…`, poi `npx wrangler deploy`.
`ALLOWED_ORIGINS` contiene già `https://casticino.ch`.

## Prova in locale
Crea `scripts/noleggio/.dev.vars` (ignorato da git) con le chiavi di prova di Turnstile, che accettano sempre:
```
ADMIN_PASSWORD=prova
TURNSTILE_SECRET=1x0000000000000000000000000000000AA
ALLOWED_ORIGINS=http://localhost:8000
INVENTARIO_URL=http://localhost:8000/data/noleggio-inventario.json
```
Poi:
```bash
npx wrangler d1 execute casticino-noleggio --local --file=schema.sql
npx wrangler dev                                  # servizio su http://localhost:8787 (gestione: /admin)
python -m http.server 8000                        # dalla radice del repository, in un altro terminale
```
Nella pagina locale il modulo usa ancora `NOLEGGIO_API`. Per provarlo con il servizio locale, cambia per un momento
`data-api` in `noleggio.html` con `http://localhost:8787/` (senza rigenerare la pagina).
