-- Database D1 delle notifiche (worker.js). Una riga per telefono o browser iscritto.
-- Crearlo una volta: npx wrangler d1 execute casticino-notifiche --remote --file=schema.sql
CREATE TABLE IF NOT EXISTS iscrizioni (
  endpoint TEXT PRIMARY KEY,   -- indirizzo di notifica creato dal browser (anonimo: nessun nome né e-mail)
  p256dh TEXT NOT NULL,        -- chiave pubblica del browser per cifrare i messaggi
  auth TEXT NOT NULL,          -- segreto del browser per cifrare i messaggi
  lingua TEXT NOT NULL DEFAULT 'it',
  creata TEXT NOT NULL         -- data e ora ISO dell'iscrizione
);
