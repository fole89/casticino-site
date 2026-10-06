// Notifiche del sito (un solo canale: «Notizie importanti della sezione»): Cloudflare Worker con database D1.
// Qui si conservano solo le iscrizioni (indirizzi di notifica anonimi creati dal browser, con le loro chiavi): l'invio
// lo fa il workflow .github/workflows/news.yml (scripts/notifiche.py), che legge l'elenco e toglie gli indirizzi scaduti.
// Istruzioni: LEGGIMI.md nella stessa cartella; tabella del database: schema.sql.
//
//   POST /iscrizione     {endpoint, keys: {p256dh, auth}, lingua}   dal sito (CORS: ALLOWED_ORIGINS)
//   POST /disiscrizione  {endpoint}                                 dal sito
//   GET  /iscrizioni     elenco per l'invio                         Authorization: Bearer NOTIFICHE_TOKEN
//   POST /rimuovi        {endpoints: [...]} scaduti                 Authorization: Bearer NOTIFICHE_TOKEN
//
// Variabili (wrangler.toml › [vars]): ALLOWED_ORIGINS. Segreto: NOTIFICHE_TOKEN (npx wrangler secret put …).
// Limite (wrangler.toml › [[ratelimits]]): LIMITE, richieste per indirizzo IP al minuto su /iscrizione e /disiscrizione.

const MAX_ISCRIZIONI = 20000;
// servizi di notifica dei browser: Google (Chrome, Edge su Android, Samsung), Apple, Mozilla, Microsoft (Edge su Windows)
const SERVIZI = [/\.googleapis\.com$/, /\.push\.apple\.com$/, /\.push\.services\.mozilla\.com$/, /\.notify\.windows\.com$/];

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    try {
      if (request.method === "OPTIONS") return cors(request, env, new Response(null, { status: 204 }));
      if (url.pathname === "/iscrizione" && request.method === "POST") return cors(request, env, await iscrizione(request, env));
      if (url.pathname === "/disiscrizione" && request.method === "POST") return cors(request, env, await disiscrizione(request, env));
      if (url.pathname === "/iscrizioni" && request.method === "GET") return await elenco(request, env);
      if (url.pathname === "/rimuovi" && request.method === "POST") return await rimuovi(request, env);
      return new Response("Notifiche CAS Ticino.", { status: 404 });
    } catch (e) {
      console.log("errore", e && e.stack || e);
      return cors(request, env, json({ errore: "interno" }, 500));
    }
  },
};

async function troppe(request, env) {
  if (!env.LIMITE) return false;
  const { success } = await env.LIMITE.limit({ key: request.headers.get("CF-Connecting-IP") || "?" });
  return !success;
}

// indirizzo https di un servizio di notifica conosciuto, chiavi della lunghezza giusta
function valida(d) {
  const endpoint = d && typeof d.endpoint === "string" ? d.endpoint : "";
  let host;
  try { const u = new URL(endpoint); if (u.protocol !== "https:") return null; host = u.hostname; } catch { return null; }
  if (endpoint.length > 1000 || !SERVIZI.some((r) => r.test(host))) return null;
  const p256dh = d.keys && d.keys.p256dh, auth = d.keys && d.keys.auth;
  if (lunghezza(p256dh) !== 65 || lunghezza(auth) !== 16) return null;
  return { endpoint, p256dh, auth };
}

// byte di una stringa base64url (-1 se non lo è)
function lunghezza(s) {
  if (typeof s !== "string" || !/^[A-Za-z0-9_-]+={0,2}$/.test(s) || s.length > 200) return -1;
  const b = s.replace(/=+$/, "").replace(/-/g, "+").replace(/_/g, "/");
  try { return atob(b + "=".repeat((4 - (b.length % 4)) % 4)).length; } catch { return -1; }
}

async function iscrizione(request, env) {
  if (await troppe(request, env)) return json({ errore: "troppe" }, 429);
  let d;
  try { d = await request.json(); } catch { return json({ errore: "dati" }, 400); }
  const s = valida(d);
  if (!s) return json({ errore: "dati" }, 400);
  const lingua = ["it", "de", "en"].includes(d.lingua) ? d.lingua : "it";
  const { n } = await env.DB.prepare("SELECT COUNT(*) AS n FROM iscrizioni").first();
  if (n >= MAX_ISCRIZIONI) return json({ errore: "pieno" }, 503);
  await env.DB.prepare(
    `INSERT INTO iscrizioni (endpoint, p256dh, auth, lingua, creata) VALUES (?, ?, ?, ?, ?)
     ON CONFLICT(endpoint) DO UPDATE SET p256dh = excluded.p256dh, auth = excluded.auth, lingua = excluded.lingua`
  ).bind(s.endpoint, s.p256dh, s.auth, lingua, new Date().toISOString()).run();
  return json({ ok: true });
}

async function disiscrizione(request, env) {
  if (await troppe(request, env)) return json({ errore: "troppe" }, 429);
  let d;
  try { d = await request.json(); } catch { return json({ errore: "dati" }, 400); }
  if (!d || typeof d.endpoint !== "string") return json({ errore: "dati" }, 400);
  await env.DB.prepare("DELETE FROM iscrizioni WHERE endpoint = ?").bind(d.endpoint).run();
  return json({ ok: true });
}

async function autorizzato(request, env) {
  const h = request.headers.get("Authorization") || "";
  if (!env.NOTIFICHE_TOKEN || !h.startsWith("Bearer ")) return false;
  const [a, b] = await Promise.all([h.slice(7), env.NOTIFICHE_TOKEN].map((s) =>
    crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))));
  return crypto.subtle.timingSafeEqual(a, b);
}

async function elenco(request, env) {
  if (!(await autorizzato(request, env))) return json({ errore: "accesso" }, 401);
  const { results } = await env.DB.prepare("SELECT endpoint, p256dh, auth, lingua FROM iscrizioni").all();
  return json({ iscrizioni: results });
}

async function rimuovi(request, env) {
  if (!(await autorizzato(request, env))) return json({ errore: "accesso" }, 401);
  let d;
  try { d = await request.json(); } catch { return json({ errore: "dati" }, 400); }
  const lista = Array.isArray(d && d.endpoints) ? d.endpoints.filter((x) => typeof x === "string").slice(0, 5000) : [];
  for (let i = 0; i < lista.length; i += 50) {
    await env.DB.batch(lista.slice(i, i + 50).map((e) => env.DB.prepare("DELETE FROM iscrizioni WHERE endpoint = ?").bind(e)));
  }
  return json({ ok: true, rimossi: lista.length });
}

function json(dati, status = 200) {
  return new Response(JSON.stringify(dati), { status, headers: { "content-type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });
}

function cors(request, env, risposta) {
  const origine = request.headers.get("Origin");
  const ammessi = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const r = new Response(risposta.body, risposta);
  if (origine && ammessi.includes(origine)) {
    r.headers.set("Access-Control-Allow-Origin", origine);
    r.headers.set("Access-Control-Allow-Methods", "POST");
    r.headers.set("Access-Control-Allow-Headers", "Content-Type");
    r.headers.set("Vary", "Origin");
  }
  return r;
}
