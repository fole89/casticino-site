-- Database D1 del noleggio materiale (worker.js). Una riga per richiesta.
-- Crearlo una volta: npx wrangler d1 execute casticino-noleggio --remote --file=schema.sql
CREATE TABLE IF NOT EXISTS richieste (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creata TEXT NOT NULL,              -- data e ora ISO della richiesta
  aggiornata TEXT NOT NULL,
  dal TEXT NOT NULL,                 -- primo giorno di noleggio, AAAA-MM-GG
  al TEXT NOT NULL,                  -- ultimo giorno (compreso)
  stato TEXT NOT NULL,               -- attesa, confermata, ritirata, riconsegnata, rifiutata, annullata
  nome TEXT NOT NULL,
  email TEXT NOT NULL,
  telefono TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  lingua TEXT NOT NULL DEFAULT 'it', -- lingua delle e-mail al socio
  righe TEXT NOT NULL,               -- JSON: [{articolo, taglia, quantita, nome, de, en, prezzo}] come al momento della richiesta
  pezzi TEXT NOT NULL,               -- JSON: pezzi occupati {"casco": 2, "imbracatura:M": 1, "arva": 1, …} (i set sono già scomposti)
  totale INTEGER NOT NULL,           -- franchi, indicativo
  nota_gestore TEXT                  -- messaggi del responsabile, con data
);
CREATE INDEX IF NOT EXISTS richieste_periodo ON richieste (stato, dal, al);
