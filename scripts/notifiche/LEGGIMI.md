# Notifiche del sito

Un solo canale: «Notizie importanti della sezione». Chi vuole riceverle tocca «Ricevi le notifiche» in fondo alle
pagine; su iPhone funziona solo con il sito installato sulla schermata Home.

## Come funziona

1. **Iscrizione**: il browser chiede il permesso e crea un indirizzo di notifica anonimo (nessun nome, e-mail o
   telefono). `assets/site.js` lo manda a questo servizio (`worker.js`, Cloudflare Workers + database D1), che lo
   conserva con la lingua della pagina. «Disattiva le notifiche» lo cancella.
2. **Invio**: nell'area di redazione, una news o l'avviso con la casella **«Invia anche come notifica»**. Alla
   pubblicazione il workflow `.github/workflows/news.yml`:
   - prima di pubblicare, `scripts/notifiche.py prepara` trasforma news e avviso con la casella accesa in messaggi,
     spegne la casella e segna «notifica inviata» (così una modifica successiva non la rimanda);
   - dopo la pubblicazione aspetta 90 secondi (che GitHub Pages metta online la pagina) e `scripts/notifiche.py invia`
     manda il messaggio a tutti gli iscritti, firmato con la chiave VAPID della sezione; gli indirizzi non più validi
     (telefono cambiato, app tolta) vengono tolti da qui.
3. Le notifiche partono con priorità alta (`Urgency: high`): con la priorità normale Android le trattiene, a telefono
   bloccato, fino allo sblocco.
4. **Sul telefono** il service worker (`sw.js`, da `scripts/redesign/pwa.py`) mostra la notifica; toccandola si apre
   la pagina.

Testo della notifica: per una news il titolo e il riassunto (in italiano), per l'avviso il suo testo nella lingua
scelta all'iscrizione. Al massimo una o due notifiche a settimana, solo per cose importanti.

## Chiavi

- Chiave pubblica VAPID: `NOTIFICHE_CHIAVE` in `scripts/redesign/shared.py` (sta nelle pagine, non è segreta).
- Segreti su **GitHub › Settings › Secrets and variables › Actions**: `VAPID_PRIVATE` (chiave privata, PEM) e
  `NOTIFICHE_TOKEN` (lo stesso token impostato nel Worker con `npx wrangler secret put NOTIFICHE_TOKEN`).
  Senza questi segreti il workflow pubblica lo stesso, ma non invia nulla (lo scrive nel log).
- Cambiare la coppia di chiavi VAPID rende inutili tutte le iscrizioni: chi le aveva deve riattivare le notifiche.

## Comandi (da questa cartella)

```bash
npx wrangler deploy                                     # pubblica il servizio
npx wrangler d1 execute casticino-notifiche --remote --command "SELECT COUNT(*) FROM iscrizioni"   # quanti iscritti
```

Notifica di prova a tutti gli iscritti: **GitHub › Actions › «Notifica di prova» › Run workflow** (testo a scelta).
Oppure dalla radice del repository, con i due segreti nell'ambiente e `pip install pywebpush`:

```bash
python scripts/notifiche.py prova "Testo della prova"
```

## Messa in funzione (già fatta il 6 ottobre 2026)

```bash
npx wrangler d1 create casticino-notifiche --location weur   # database_id in wrangler.toml
npx wrangler d1 execute casticino-notifiche --remote --file=schema.sql
npx wrangler deploy
npx wrangler secret put NOTIFICHE_TOKEN
```

Al cambio di dominio `ALLOWED_ORIGINS` in `wrangler.toml` contiene già `https://casticino.ch`. Le iscrizioni fatte
su `fole89.github.io` non valgono per `casticino.ch`: dopo il passaggio vanno riattivate.
