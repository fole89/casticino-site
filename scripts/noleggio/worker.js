// Richieste di noleggio materiale (noleggio.html e de/, en/): Cloudflare Worker con database D1.
// La pagina chiede qui la disponibilità per le date scelte e invia le richieste; il responsabile le gestisce
// su /admin (protetto da password). I dati personali restano solo qui, mai nel repository.
// Istruzioni per attivarlo: LEGGIMI.md nella stessa cartella; tabella del database: schema.sql.
//
// Variabili (wrangler.toml › [vars]):
//   ALLOWED_ORIGINS  indirizzi del sito che possono usare il servizio, separati da virgola
//   INVENTARIO_URL   data/noleggio-inventario.json pubblicato (quantità, taglie, set, prezzi)
//   SITO_URL         indirizzo del sito (per i link nelle e-mail)
//   MAIL_GESTORE     chi riceve le nuove richieste
//   MAIL_MITTENTE    mittente delle e-mail (verificato su Brevo)
// Segreti (npx wrangler secret put …):
//   ADMIN_PASSWORD   password di /admin
//   BREVO_API_KEY    chiave API di Brevo per le e-mail (senza: niente e-mail, le richieste si salvano lo stesso)
//   TURNSTILE_SECRET chiave segreta di Cloudflare Turnstile (protezione dai programmi automatici)
// Limite (wrangler.toml › [[ratelimits]]):
//   LIMITE_ADMIN     richieste a /admin per indirizzo IP al minuto (contro i tentativi di indovinare la password)

const ATTIVI = ["attesa", "confermata", "ritirata"];   // stati che occupano il materiale
const MAX_GIORNI = 30;       // durata massima di un noleggio
const MAX_ANTICIPO = 365;    // quanto in là si può prenotare (giorni)
const CONSERVA_MESI = 12;    // le richieste si cancellano 12 mesi dopo la fine del noleggio
const STATI = {
  attesa: "Da confermare", confermata: "Confermata", ritirata: "Ritirata",
  riconsegnata: "Riconsegnata", rifiutata: "Rifiutata", annullata: "Annullata",
};
// azione → [stati di partenza, nuovo stato, e-mail al socio]
const AZIONI = {
  conferma: [["attesa"], "confermata", "confermata"],
  rifiuta: [["attesa"], "rifiutata", "rifiutata"],
  ritira: [["confermata"], "ritirata", null],
  riconsegna: [["ritirata"], "riconsegnata", null],
  annulla: [["attesa", "confermata"], "annullata", "annullata"],
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    try {
      if (url.pathname === "/admin" || url.pathname.startsWith("/admin/")) return await admin(request, env, ctx, url);
      if (request.method === "OPTIONS") return cors(request, env, new Response(null, { status: 204 }));
      if (url.pathname === "/disponibilita" && request.method === "GET") return cors(request, env, await disponibilita(env, url));
      if (url.pathname === "/richiesta" && request.method === "POST") return cors(request, env, await richiesta(request, env, ctx));
      return new Response("Noleggio materiale CAS Ticino.", { status: 404 });
    } catch (e) {
      console.log("errore", e && e.stack || e);
      return cors(request, env, json({ errore: "interno" }, 500));
    }
  },

  // ogni notte: via le richieste finite da più di CONSERVA_MESI mesi
  async scheduled(event, env) {
    await env.DB.prepare("DELETE FROM richieste WHERE al < date('now', ?)").bind(`-${CONSERVA_MESI} months`).run();
  },
};

// ------------------------------------------------------------------ inventario

let cacheInv = null;

// articoli per id: { id, nome, de, en, prezzo, gruppo, taglie: {taglia: n} | null, quantita, set: [id] | null }
async function inventario(env) {
  if (cacheInv && Date.now() - cacheInv.quando < 5 * 60 * 1000) return cacheInv.articoli;
  // in cache solo le risposte riuscite: un errore (es. file non ancora pubblicato) non deve restare per 5 minuti
  const r = await fetch(env.INVENTARIO_URL, { cf: { cacheTtlByStatus: { "200-299": 300, "300-599": 0 } } });
  if (!r.ok) throw new Error(`inventario: ${r.status}`);
  const dati = await r.json();
  const articoli = {};
  for (const g of dati.gruppi || []) {
    for (const a of g.articoli || []) {
      articoli[a.id] = { ...a, gruppo: g.gruppo, taglie: a.taglie || null, set: a.set || null, quantita: Number(a.quantita) || 0 };
    }
  }
  cacheInv = { quando: Date.now(), articoli };
  return articoli;
}

// pezzi a magazzino: "casco" → 6, "imbracatura:M" → 3 (i set non hanno pezzi propri)
function totali(inv) {
  const t = {};
  for (const a of Object.values(inv)) {
    if (a.set) continue;
    if (a.taglie) for (const [tg, n] of Object.entries(a.taglie)) t[`${a.id}:${tg}`] = Number(n) || 0;
    else t[a.id] = a.quantita;
  }
  return t;
}

// pezzi usati da una riga della richiesta
function pezziRiga(inv, riga) {
  const a = inv[riga.articolo];
  if (a.set) return Object.fromEntries(a.set.map((id) => [id, riga.quantita]));
  return { [a.taglie ? `${a.id}:${riga.taglia}` : a.id]: riga.quantita };
}

// per ogni pezzo, il massimo già occupato in un giorno del periodo
async function occupati(env, dal, al) {
  const { results } = await env.DB.prepare(
    `SELECT dal, al, pezzi FROM richieste WHERE stato IN (${ATTIVI.map(() => "?").join(",")}) AND dal <= ? AND al >= ?`
  ).bind(...ATTIVI, al, dal).all();
  const giorni = elencoGiorni(dal, al);
  const perGiorno = giorni.map(() => ({}));
  for (const r of results) {
    const pezzi = JSON.parse(r.pezzi);
    giorni.forEach((g, i) => {
      if (g < r.dal || g > r.al) return;
      for (const [k, n] of Object.entries(pezzi)) perGiorno[i][k] = (perGiorno[i][k] || 0) + n;
    });
  }
  const max = {};
  for (const giorno of perGiorno) for (const [k, n] of Object.entries(giorno)) max[k] = Math.max(max[k] || 0, n);
  return max;
}

// disponibilità per articolo (e per taglia): chiave → [a magazzino, liberi]
async function calcolaLiberi(env, dal, al) {
  const inv = await inventario(env);
  const tot = totali(inv);
  const occ = await occupati(env, dal, al);
  const pezzi = {};
  for (const [k, n] of Object.entries(tot)) pezzi[k] = [n, Math.max(0, n - (occ[k] || 0))];
  const disp = { ...pezzi };
  for (const a of Object.values(inv)) {
    if (!a.set) continue;
    const parti = a.set.map((id) => pezzi[id] || [0, 0]);
    disp[a.id] = [Math.min(...parti.map((p) => p[0])), Math.min(...parti.map((p) => p[1]))];
  }
  return { inv, disp, pezzi };
}

// ------------------------------------------------------------------ servizio pubblico

async function disponibilita(env, url) {
  const periodo = controllaDate(url.searchParams.get("dal"), url.searchParams.get("al"));
  if (periodo.errore) return json(periodo, 400);
  const { disp } = await calcolaLiberi(env, periodo.dal, periodo.al);
  return json({ dal: periodo.dal, al: periodo.al, giorni: periodo.giorni, disponibili: disp });
}

async function richiesta(request, env, ctx) {
  let d;
  try { d = await request.json(); } catch { return json({ errore: "dati" }, 400); }
  const periodo = controllaDate(d.dal, d.al);
  if (periodo.errore) return json(periodo, 400);

  const nome = testo(d.nome, 100), email = testo(d.email, 200).toLowerCase(), telefono = testo(d.telefono, 40);
  const note = testo(d.note, 2000, true), lingua = ["it", "de", "en"].includes(d.lingua) ? d.lingua : "it";
  if (nome.length < 3 || /https?:|www\.|[@/<>]/i.test(nome)) return json({ errore: "nome" }, 400);
  if (!/^[a-z0-9._%+'-]+@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$/.test(email)) return json({ errore: "email" }, 400);
  if (!/^[+0-9 ()./-]{7,40}$/.test(telefono)) return json({ errore: "telefono" }, 400);

  if (!(await turnstile(env, d.token, request))) return json({ errore: "verifica" }, 403);

  const { inv, disp, pezzi: liberiPezzi } = await calcolaLiberi(env, periodo.dal, periodo.al);
  const righe = [];
  for (const r of Array.isArray(d.righe) ? d.righe.slice(0, 40) : []) {
    const a = inv[r && r.articolo], q = Number(r && r.quantita);
    if (!a || !Number.isInteger(q) || q < 1) return json({ errore: "materiale" }, 400);   // il massimo lo dà la disponibilità
    const taglia = a.taglie ? String(r.taglia || "") : null;
    if (a.taglie && !(taglia in a.taglie)) return json({ errore: "materiale" }, 400);
    if (righe.some((x) => x.articolo === a.id && x.taglia === taglia)) return json({ errore: "materiale" }, 400);
    righe.push({ articolo: a.id, taglia, quantita: q, nome: a.nome, de: a.de, en: a.en, prezzo: Number(a.prezzo) || 0 });
  }
  if (!righe.length) return json({ errore: "materiale" }, 400);

  // tutti i pezzi chiesti (un set usa anche i pezzi singoli) devono essere liberi
  const pezzi = {};
  for (const r of righe) for (const [k, n] of Object.entries(pezziRiga(inv, r))) pezzi[k] = (pezzi[k] || 0) + n;
  const esauriti = righe.filter((r) => {
    const own = pezziRiga(inv, r);
    return Object.keys(own).some((k) => pezzi[k] > (liberiPezzi[k] || [0, 0])[1]);
  }).map((r) => (r.taglia ? `${r.articolo}:${r.taglia}` : r.articolo));
  if (esauriti.length) return json({ errore: "esaurito", articoli: esauriti, disponibili: disp }, 409);

  const totale = righe.reduce((s, r) => s + r.prezzo * r.quantita, 0) * periodo.giorni;
  const ora = new Date().toISOString();
  const res = await env.DB.prepare(
    `INSERT INTO richieste (creata, aggiornata, dal, al, stato, nome, email, telefono, note, lingua, righe, pezzi, totale)
     VALUES (?, ?, ?, ?, 'attesa', ?, ?, ?, ?, ?, ?, ?, ?)`
  ).bind(ora, ora, periodo.dal, periodo.al, nome, email, telefono, note, lingua,
    JSON.stringify(righe), JSON.stringify(pezzi), totale).run();
  const r = { id: res.meta.last_row_id, dal: periodo.dal, al: periodo.al, nome, email, telefono, note, lingua, righe, totale };

  ctx.waitUntil(Promise.all([
    mail(env, env.MAIL_GESTORE, "Responsabile noleggio", `Noleggio: nuova richiesta n. ${r.id} di ${nome}`,
      mailGestore(r, `${new URL(request.url).origin}/admin`), email),
    mail(env, email, nome, TESTI[lingua].oggetto("ricevuta"), mailSocio(env, r, "ricevuta", ""), env.MAIL_GESTORE),
  ]));
  return json({ ok: true, numero: r.id, totale });
}

async function turnstile(env, token, request) {
  if (!env.TURNSTILE_SECRET || typeof token !== "string" || !token) return false;
  const corpo = new FormData();
  corpo.append("secret", env.TURNSTILE_SECRET);
  corpo.append("response", token);
  const ip = request.headers.get("CF-Connecting-IP");
  if (ip) corpo.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: corpo });
  return r.ok && (await r.json()).success === true;
}

// ------------------------------------------------------------------ e-mail (Brevo)

async function mail(env, a, nome, oggetto, corpo, rispondiA) {
  if (!env.BREVO_API_KEY || !env.MAIL_MITTENTE || !a) return;
  const r = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: { "api-key": env.BREVO_API_KEY, "content-type": "application/json", accept: "application/json" },
    body: JSON.stringify({
      sender: { name: "CAS Ticino – Noleggio materiale", email: env.MAIL_MITTENTE },
      to: [{ email: a, name: nome }],
      ...(rispondiA ? { replyTo: { email: rispondiA } } : {}),
      subject: oggetto,
      textContent: corpo,
    }),
  });
  if (!r.ok) console.log("e-mail non inviata", r.status, await r.text());
}

const TESTI = {
  it: {
    oggetto: (tipo) => ({ ricevuta: "Richiesta di noleggio ricevuta", confermata: "Noleggio confermato",
      rifiutata: "Noleggio: richiesta non accolta", annullata: "Noleggio annullato" })[tipo],
    saluto: (nome) => `Ciao ${nome},`,
    apertura: {
      ricevuta: "abbiamo ricevuto la tua richiesta di noleggio. Ti scriviamo appena l’abbiamo controllata: la richiesta vale solo con la nostra conferma.",
      confermata: "la tua richiesta di noleggio è confermata.",
      rifiutata: "purtroppo non possiamo accogliere la tua richiesta di noleggio.",
      annullata: "il tuo noleggio è stato annullato.",
    },
    messaggio: "Messaggio del responsabile",
    periodo: (dal, al, g) => `Dal ${dal} al ${al} (${g} ${g === 1 ? "giorno" : "giorni"})`,
    totale: (t) => `Totale indicativo: Fr. ${t}.–, da pagare alla riconsegna in contanti o con TWINT.`,
    luogo: "Ritiro e riconsegna al magazzino di Manno.",
    rispondi: "Per domande rispondi a questa e-mail.",
    firma: "CAS Ticino, noleggio materiale",
  },
  de: {
    oggetto: (tipo) => ({ ricevuta: "Mietanfrage erhalten", confermata: "Miete bestätigt",
      rifiutata: "Miete: Anfrage nicht möglich", annullata: "Miete storniert" })[tipo],
    saluto: (nome) => `Hallo ${nome}`,
    apertura: {
      ricevuta: "Wir haben Ihre Mietanfrage erhalten. Wir melden uns, sobald wir sie geprüft haben: Die Anfrage gilt erst mit unserer Bestätigung.",
      confermata: "Ihre Mietanfrage ist bestätigt.",
      rifiutata: "Leider können wir Ihre Mietanfrage nicht annehmen.",
      annullata: "Ihre Miete wurde storniert.",
    },
    messaggio: "Nachricht der Materialvermietung",
    periodo: (dal, al, g) => `Vom ${dal} bis ${al} (${g} ${g === 1 ? "Tag" : "Tage"})`,
    totale: (t) => `Total ungefähr: Fr. ${t}.–, zu bezahlen bei der Rückgabe, bar oder mit TWINT.`,
    luogo: "Abholung und Rückgabe im Lager in Manno.",
    rispondi: "Für Fragen antworten Sie auf diese E-Mail.",
    firma: "SAC Sektion Ticino, Materialvermietung",
  },
  en: {
    oggetto: (tipo) => ({ ricevuta: "Hire request received", confermata: "Hire confirmed",
      rifiutata: "Hire: request declined", annullata: "Hire cancelled" })[tipo],
    saluto: (nome) => `Hello ${nome},`,
    apertura: {
      ricevuta: "we have received your hire request. We will write to you as soon as we have checked it: the request only stands once we confirm it.",
      confermata: "your hire request is confirmed.",
      rifiutata: "unfortunately we cannot accept your hire request.",
      annullata: "your hire has been cancelled.",
    },
    messaggio: "Message from the equipment manager",
    periodo: (dal, al, g) => `From ${dal} to ${al} (${g} ${g === 1 ? "day" : "days"})`,
    totale: (t) => `Approximate total: CHF ${t}, payable on return in cash or by TWINT.`,
    luogo: "Pick-up and return at the store in Manno.",
    rispondi: "If you have any questions, reply to this e-mail.",
    firma: "SAC Ticino Section, equipment hire",
  },
};

function elencoRighe(r, lingua) {
  return r.righe.map((x) => `${x.quantita} × ${(lingua !== "it" && x[lingua]) || x.nome}${x.taglia ? ` (${x.taglia})` : ""}`).join("\n");
}

function mailSocio(env, r, tipo, messaggio) {
  const T = TESTI[r.lingua] || TESTI.it;
  const g = elencoGiorni(r.dal, r.al).length;
  return [
    T.saluto(r.nome), "", T.apertura[tipo], "",
    ...(messaggio ? [`${T.messaggio}:`, messaggio, ""] : []),
    T.periodo(dataCh(r.dal), dataCh(r.al), g), "", elencoRighe(r, r.lingua), "",
    ...(tipo === "ricevuta" || tipo === "confermata" ? [T.totale(r.totale), T.luogo, ""] : []),
    T.rispondi, "", T.firma, env.SITO_URL ? `${env.SITO_URL}${r.lingua === "it" ? "" : r.lingua + "/"}noleggio.html` : "",
  ].join("\n");
}

function mailGestore(r, indirizzoAdmin) {
  const g = elencoGiorni(r.dal, r.al).length;
  return [
    `Nuova richiesta di noleggio n. ${r.id}`, "",
    `Dal ${dataCh(r.dal)} al ${dataCh(r.al)} (${g} ${g === 1 ? "giorno" : "giorni"})`, "",
    elencoRighe(r, "it"), "", `Totale indicativo: Fr. ${r.totale}.–`, "",
    `${r.nome}`, r.email, r.telefono, ...(r.note ? ["", "Note:", r.note] : []), "",
    "Rispondendo a questa e-mail scrivi direttamente a chi ha fatto la richiesta.",
    `Per confermarla o rifiutarla: ${indirizzoAdmin}`,
  ].join("\n");
}

// ------------------------------------------------------------------ gestione (/admin)

async function admin(request, env, ctx, url) {
  // prima della password: chi supera il limite non può provarne altre, giuste o sbagliate
  if (env.LIMITE_ADMIN) {
    const { success } = await env.LIMITE_ADMIN.limit({ key: request.headers.get("CF-Connecting-IP") || "?" });
    if (!success) return new Response("Troppi tentativi: riprova tra un minuto.", { status: 429, headers: { "Retry-After": "60", ...SICUREZZA } });
  }
  if (!(await autorizzato(request, env))) {
    return new Response("Accesso riservato al responsabile del noleggio.", {
      status: 401, headers: { "WWW-Authenticate": 'Basic realm="Noleggio CAS Ticino", charset="UTF-8"', ...SICUREZZA },
    });
  }
  if (url.pathname === "/admin" || url.pathname === "/admin/") {
    return new Response(PAGINA_ADMIN, { headers: { "content-type": "text/html; charset=utf-8", ...SICUREZZA } });
  }
  // le chiamate di /admin arrivano solo dalla pagina stessa (intestazione propria: un altro sito non può aggiungerla)
  if (request.headers.get("X-Noleggio") !== "1") return json({ errore: "origine" }, 403);

  if (url.pathname === "/admin/api/richieste" && request.method === "GET") {
    const vista = url.searchParams.get("vista") || "attesa";
    const filtri = { attesa: ["attesa"], corso: ["confermata", "ritirata"], concluse: ["riconsegnata", "rifiutata", "annullata"] };
    const stati = filtri[vista] || Object.keys(STATI);
    const ordine = vista === "concluse" || vista === "tutte" ? "dal DESC" : "dal ASC";
    const { results } = await env.DB.prepare(
      `SELECT * FROM richieste WHERE stato IN (${stati.map(() => "?").join(",")}) ORDER BY ${ordine}, id LIMIT 300`
    ).bind(...stati).all();
    const conti = await env.DB.prepare("SELECT stato, COUNT(*) AS n FROM richieste GROUP BY stato").all();
    return json({
      richieste: results.map((r) => ({ ...r, righe: JSON.parse(r.righe), pezzi: undefined, stato_nome: STATI[r.stato] })),
      conti: Object.fromEntries(conti.results.map((c) => [c.stato, c.n])),
    });
  }

  const m = url.pathname.match(/^\/admin\/api\/richieste\/(\d+)$/);
  if (m && request.method === "POST") {
    let d;
    try { d = await request.json(); } catch { return json({ errore: "dati" }, 400); }
    const r = await env.DB.prepare("SELECT * FROM richieste WHERE id = ?").bind(Number(m[1])).first();
    if (!r) return json({ errore: "non trovata" }, 404);
    const messaggio = testo(d.messaggio, 2000, true);

    if (d.azione === "elimina") {
      if (ATTIVI.includes(r.stato)) return json({ errore: "Prima annulla o chiudi la richiesta." }, 409);
      await env.DB.prepare("DELETE FROM richieste WHERE id = ?").bind(r.id).run();
      return json({ ok: true });
    }
    const azione = AZIONI[d.azione];
    if (!azione) return json({ errore: "azione" }, 400);
    const [da, nuovo, tipoMail] = azione;
    if (!da.includes(r.stato)) return json({ errore: `La richiesta è «${STATI[r.stato]}».` }, 409);
    const nota = messaggio ? `${r.nota_gestore ? r.nota_gestore + "\n" : ""}${dataCh(oggi())} ${STATI[nuovo]}: ${messaggio}` : r.nota_gestore;
    await env.DB.prepare("UPDATE richieste SET stato = ?, aggiornata = ?, nota_gestore = ? WHERE id = ?")
      .bind(nuovo, new Date().toISOString(), nota, r.id).run();
    if (tipoMail) {
      const piena = { ...r, righe: JSON.parse(r.righe) };
      ctx.waitUntil(mail(env, r.email, r.nome, (TESTI[r.lingua] || TESTI.it).oggetto(tipoMail),
        mailSocio(env, piena, tipoMail, messaggio), env.MAIL_GESTORE));
    }
    return json({ ok: true, stato: nuovo });
  }
  return json({ errore: "non trovato" }, 404);
}

async function autorizzato(request, env) {
  const h = request.headers.get("Authorization") || "";
  if (!env.ADMIN_PASSWORD || !h.startsWith("Basic ")) return false;
  let chiaro;
  try { chiaro = new TextDecoder().decode(Uint8Array.from(atob(h.slice(6)), (c) => c.charCodeAt(0))); } catch { return false; }
  const password = chiaro.slice(chiaro.indexOf(":") + 1);
  // confronto a tempo costante sulle impronte (stessa lunghezza)
  const [a, b] = await Promise.all([password, env.ADMIN_PASSWORD].map((s) =>
    crypto.subtle.digest("SHA-256", new TextEncoder().encode(s))));
  return crypto.subtle.timingSafeEqual(a, b);
}

const SICUREZZA = {
  "Cache-Control": "no-store",
  "X-Robots-Tag": "noindex",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "no-referrer",
  "Content-Security-Policy": "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'",
};

// ------------------------------------------------------------------ utilità

function json(dati, status = 200) {
  return new Response(JSON.stringify(dati), { status, headers: { "content-type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });
}

function cors(request, env, risposta) {
  const origine = request.headers.get("Origin");
  const ammessi = (env.ALLOWED_ORIGINS || "").split(",").map((s) => s.trim()).filter(Boolean);
  const r = new Response(risposta.body, risposta);
  if (origine && ammessi.includes(origine)) {
    r.headers.set("Access-Control-Allow-Origin", origine);
    r.headers.set("Access-Control-Allow-Methods", "GET, POST");
    r.headers.set("Access-Control-Allow-Headers", "Content-Type");
    r.headers.set("Vary", "Origin");
  }
  return r;
}

function testo(v, max, aCapo = false) {
  let s = typeof v === "string" ? v : "";
  s = aCapo ? s.replace(/\r\n?/g, "\n").replace(/[^\S\n]+/g, " ") : s.replace(/\s+/g, " ");
  return s.trim().slice(0, max);
}

// oggi in Svizzera, AAAA-MM-GG
function oggi() {
  return new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Zurich" }).format(new Date());
}

function piuGiorni(data, n) {
  const d = new Date(`${data}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function elencoGiorni(dal, al) {
  const out = [];
  for (let g = dal; g <= al && out.length <= MAX_GIORNI + 1; g = piuGiorni(g, 1)) out.push(g);
  return out;
}

function controllaDate(dal, al) {
  const ok = (s) => typeof s === "string" && /^\d{4}-\d{2}-\d{2}$/.test(s) && piuGiorni(s, 0) === s;
  if (!ok(dal) || !ok(al)) return { errore: "date" };
  if (al < dal) return { errore: "ordine" };
  if (dal <= oggi()) return { errore: "passato" };
  if (dal > piuGiorni(oggi(), MAX_ANTICIPO)) return { errore: "lontano" };
  const giorni = elencoGiorni(dal, al).length;
  if (giorni > MAX_GIORNI) return { errore: "durata", max: MAX_GIORNI };
  return { dal, al, giorni };
}

function dataCh(s) {
  const [a, m, g] = s.split("-");
  return `${g}.${m}.${a}`;
}

// ------------------------------------------------------------------ pagina di gestione

const PAGINA_ADMIN = `<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Noleggio materiale · gestione</title>
<style>
:root{--bg:#fff;--surface:#F0F2F0;--ink:#121816;--muted:#5B6661;--line:rgba(18,24,22,.14);--accent:#EF1C24;--ok:#2F7A4A;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
header{position:sticky;top:0;z-index:1;background:var(--bg);border-bottom:1px solid var(--line);padding:14px 16px}
h1{margin:0 0 10px;font-size:20px;letter-spacing:-.02em}
.viste{display:flex;flex-wrap:wrap;gap:8px}
button{font:inherit;font-weight:600;min-height:40px;padding:0 14px;border:1.5px solid rgba(18,24,22,.32);background:transparent;color:var(--ink);cursor:pointer}
button:hover{border-color:var(--ink)}
button[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:#fff}
button.primario{background:var(--accent);border-color:var(--accent);color:#fff}
button.ok{background:var(--ok);border-color:var(--ok);color:#fff}
button:disabled{opacity:.5;cursor:default}
main{max-width:960px;margin:0 auto;padding:16px}
.richiesta{border:1px solid var(--line);padding:16px;margin-bottom:16px;display:grid;gap:10px}
.testa{display:flex;flex-wrap:wrap;justify-content:space-between;gap:6px 16px;align-items:baseline}
.testa strong{font-size:18px}
.stato{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:2px 8px;background:var(--surface)}
.stato.attesa{background:var(--accent);color:#fff}
.stato.confermata,.stato.ritirata{background:var(--ok);color:#fff}
ul{margin:0;padding-left:20px}
.muted{color:var(--muted);font-size:14px}
.note{white-space:pre-line;background:var(--surface);padding:8px 10px}
textarea{width:100%;min-height:60px;font:inherit;padding:8px;border:1.5px solid rgba(18,24,22,.32)}
.azioni{display:flex;flex-wrap:wrap;gap:8px}
a{color:inherit}
.vuoto{color:var(--muted);padding:24px 0}
</style>
</head>
<body>
<header>
<h1>Noleggio materiale · richieste</h1>
<div class="viste" role="group" aria-label="Mostra">
<button data-vista="attesa">Da confermare</button>
<button data-vista="corso">Confermate e fuori</button>
<button data-vista="concluse">Concluse</button>
<button data-vista="tutte">Tutte</button>
</div>
</header>
<main id="elenco" aria-live="polite"></main>
<script>
(function () {
  var vista = "attesa", elenco = document.getElementById("elenco");
  var AZIONI = {
    attesa: [["conferma", "Conferma", "ok"], ["rifiuta", "Rifiuta", "primario"]],
    confermata: [["ritira", "Ritirata", "ok"], ["annulla", "Annulla", ""]],
    ritirata: [["riconsegna", "Riconsegnata", "ok"]],
    riconsegnata: [["elimina", "Elimina", ""]], rifiutata: [["elimina", "Elimina", ""]], annullata: [["elimina", "Elimina", ""]]
  };
  var MAIL = { conferma: 1, rifiuta: 1, annulla: 1 };
  function el(tag, attr, figli) {
    var e = document.createElement(tag);
    for (var k in attr || {}) { if (k === "text") e.textContent = attr[k]; else e.setAttribute(k, attr[k]); }
    (figli || []).forEach(function (f) { if (f) e.appendChild(f); });
    return e;
  }
  function data(s) { var p = s.split("-"); return p[2] + "." + p[1] + "." + p[0]; }
  function giorni(dal, al) { return Math.round((Date.parse(al) - Date.parse(dal)) / 864e5) + 1; }
  function api(percorso, opzioni) {
    opzioni = opzioni || {};
    opzioni.headers = { "X-Noleggio": "1", "Content-Type": "application/json" };
    return fetch(percorso, opzioni).then(function (r) {
      return r.json().then(function (d) { if (!r.ok) throw new Error(d.errore || r.status); return d; });
    });
  }
  function scheda(r) {
    var g = giorni(r.dal, r.al);
    var msg = el("textarea", { "aria-label": "Messaggio per " + r.nome, placeholder: "Messaggio per il socio (facoltativo: va nell’e-mail di conferma, rifiuto o annullamento), per esempio l’orario di ritiro" });
    var bottoni = (AZIONI[r.stato] || []).map(function (a) {
      var b = el("button", { type: "button", "class": a[2], text: a[1] + (MAIL[a[0]] ? " e invia e-mail" : "") });
      b.addEventListener("click", function () {
        if (a[0] === "elimina" && !confirm("Eliminare la richiesta n. " + r.id + "? Non si può annullare.")) return;
        if (a[0] === "rifiuta" && !msg.value.trim() && !confirm("Rifiutare senza messaggio?")) return;
        b.disabled = true;
        api("/admin/api/richieste/" + r.id, { method: "POST", body: JSON.stringify({ azione: a[0], messaggio: msg.value }) })
          .then(carica).catch(function (e) { alert(e.message); b.disabled = false; });
      });
      return b;
    });
    return el("article", { "class": "richiesta" }, [
      el("div", { "class": "testa" }, [
        el("strong", { text: "n. " + r.id + " · " + data(r.dal) + (r.al !== r.dal ? " – " + data(r.al) : "") + " (" + g + (g === 1 ? " giorno)" : " giorni)") }),
        el("span", { "class": "stato " + r.stato, text: r.stato_nome })
      ]),
      el("ul", {}, r.righe.map(function (x) { return el("li", { text: x.quantita + " × " + x.nome + (x.taglia ? " (" + x.taglia + ")" : "") }); })),
      el("div", { text: "Totale indicativo: Fr. " + r.totale + ".–" }),
      el("div", {}, [
        el("strong", { text: r.nome }), document.createTextNode(" · "),
        el("a", { href: "mailto:" + r.email, text: r.email }), document.createTextNode(" · "),
        el("a", { href: "tel:" + r.telefono.replace(/[^+0-9]/g, ""), text: r.telefono })
      ]),
      r.note ? el("div", { "class": "note", text: r.note }) : null,
      r.nota_gestore ? el("div", { "class": "note muted", text: r.nota_gestore }) : null,
      el("div", { "class": "muted", text: "Ricevuta il " + new Date(r.creata).toLocaleString("it-CH") + " · lingua " + r.lingua }),
      r.stato === "attesa" || r.stato === "confermata" ? msg : null,
      el("div", { "class": "azioni" }, bottoni)
    ]);
  }
  function carica() {
    document.querySelectorAll("[data-vista]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.vista === vista); });
    api("/admin/api/richieste?vista=" + vista).then(function (d) {
      var c = d.conti;
      document.querySelector('[data-vista="attesa"]').textContent = "Da confermare (" + (c.attesa || 0) + ")";
      document.querySelector('[data-vista="corso"]').textContent = "Confermate e fuori (" + ((c.confermata || 0) + (c.ritirata || 0)) + ")";
      elenco.replaceChildren.apply(elenco, d.richieste.length ? d.richieste.map(scheda) : [el("p", { "class": "vuoto", text: "Nessuna richiesta." })]);
    }).catch(function (e) { elenco.replaceChildren(el("p", { "class": "vuoto", text: "Errore: " + e.message })); });
  }
  document.querySelectorAll("[data-vista]").forEach(function (b) {
    b.addEventListener("click", function () { vista = b.dataset.vista; carica(); });
  });
  carica();
})();
</script>
</body>
</html>`;
