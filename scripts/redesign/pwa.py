"""Sito installabile (PWA): manifesto per lingua e service worker, scritti da pages.py a ogni rigenerazione.

- manifest.webmanifest (it), manifest-de.webmanifest, manifest-en.webmanifest: nome, icone (assets/icone/), colori,
  pagina iniziale nella lingua; head() in shared.py collega quello della lingua della pagina.
- sw.js nella radice del sito (così vale per tutte le pagine): prima la rete per le pagine (sempre aggiornate quando
  c'è campo, l'ultima versione vista quando non c'è, altrimenti offline.html); dalla memoria stili, script, caratteri
  e icone (hanno l'impronta ?v= nel nome); le foto già viste dalla memoria, al massimo MAX_FOTO; i dati JSON prima
  dalla rete. Mai in memoria: admin/ (redazione), PDF, altri siti (Droptour, noleggio, Facebook, Turnstile).
  Mostra le notifiche (evento push, da scripts/notifiche.py) e al tocco apre la pagina indicata.
  Le pagine essenziali di una lingua (home, capanne, Partecipare con «Prima di partire», Soccorso, offline) si
  salvano quando site.js lo chiede, al massimo una volta al giorno per lingua.
VERSIONE cambia quando cambiano i file in memoria o il codice qui sotto: il browser installa il nuovo service
worker e cancella la memoria vecchia degli statici."""
import hashlib, json

ICONE = [
    {"src": "assets/icone/icona-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
    {"src": "assets/icone/icona-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
    {"src": "assets/icone/icona-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
]
BADGE = "assets/icone/badge-96.png"   # sagoma bianca per la barra di stato di Android (notifiche)

DESCRIZIONE = {
    "it": "Club Alpino Svizzero, Sezione Ticino: gite, corsi, capanne e news.",
    "de": "Schweizer Alpen-Club, Sektion Ticino: Touren, Kurse, Hütten und News.",
    "en": "Swiss Alpine Club, Ticino Section: trips, courses, huts and news.",
}


def manifest(lang):
    return json.dumps({
        "id": "./",
        "name": "CAS Ticino",
        "short_name": "CAS Ticino",
        "description": DESCRIZIONE[lang],
        "lang": lang,
        "start_url": "./" if lang == "it" else f"./{lang}/",
        "scope": "./",
        "display": "standalone",
        "background_color": "#FFFFFF",
        "theme_color": "#FFFFFF",
        "icons": ICONE,
    }, ensure_ascii=False, indent=2) + "\n"


SW = r"""// Service worker del sito CAS Ticino: generato da scripts/redesign/pwa.py (pages.py), non modificare a mano.
const VERSIONE = "__VERSIONE__";
const STATICI = __STATICI__;      // salvati all'installazione: stili, script, caratteri, icone, pagine offline
const ESSENZIALI = __ESSENZIALI__;  // per lingua: pagine da avere anche senza rete
const C_STATICI = "statici-" + VERSIONE, C_PAGINE = "pagine", C_FOTO = "foto";
const MAX_PAGINE = 80, MAX_FOTO = 120;
const BASE = self.registration.scope;

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(C_STATICI)
    .then((c) => c.addAll(STATICI.map((u) => new URL(u, BASE).href)))
    .then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(caches.keys()
    .then((ks) => Promise.all(ks.filter((k) => k.startsWith("statici-") && k !== C_STATICI).map((k) => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// site.js dice la lingua della pagina: si salvano le pagine essenziali di quella lingua
self.addEventListener("message", (e) => {
  const lista = e.data && ESSENZIALI[e.data.lingua];
  if (lista) e.waitUntil(salvaPagine(lista));
});

async function salvaPagine(lista) {
  const c = await caches.open(C_PAGINE);
  await Promise.all(lista.map(async (u) => {
    try {
      const r = await fetch(new URL(u, BASE).href, { cache: "no-cache" });
      if (r.ok) await c.put(new URL(u, BASE).href, r);
    } catch (err) { /* senza rete si riprova la volta dopo */ }
  }));
}

self.addEventListener("fetch", (e) => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || !url.href.startsWith(BASE)) return;      // altri siti: come senza service worker
  const percorso = url.pathname.slice(new URL(BASE).pathname.length);
  if (percorso.startsWith("admin/") || percorso.endsWith(".pdf")) return;
  if (req.mode === "navigate") return e.respondWith(pagina(req, url, percorso));
  if (/\.(css|js|woff2)$/.test(url.pathname) || /^assets\/(icone\/|logo)/.test(percorso)) return e.respondWith(primaMemoria(req, C_STATICI));
  if (/^assets\/img\/.+\.webp$/.test(percorso)) return e.respondWith(primaMemoria(req, C_FOTO, MAX_FOTO));
  if (/^data\/.+\.json$/.test(percorso)) return e.respondWith(primaRete(req));
});

// stessa pagina con o senza .html e senza ?…: una sola copia (site.js toglie .html dalla barra degli indirizzi)
function chiave(url) {
  let p = url.pathname;
  if (p.endsWith("/")) p += "index.html";
  else if (!/\.[a-z0-9]+$/i.test(p)) p += ".html";
  return url.origin + p;
}

async function pagina(req, url, percorso) {
  const c = await caches.open(C_PAGINE);
  try {
    const r = await fetch(req);
    if (r.ok && (r.headers.get("content-type") || "").includes("text/html")) {
      await c.put(chiave(url), r.clone());
      limita(C_PAGINE, MAX_PAGINE);
    }
    return r;
  } catch (err) {
    const salvata = await caches.match(chiave(url));
    if (salvata) return salvata;
    if (/offline\.html$/.test(url.pathname)) return new Response("Offline", { status: 503 });
    const lang = /^(de|en)\//.exec(percorso);
    return Response.redirect(new URL((lang ? lang[1] + "/" : "") + "offline.html", BASE).href, 302);
  }
}

async function primaMemoria(req, nome, max) {
  const salvata = await caches.match(req);
  if (salvata) return salvata;
  const r = await fetch(req);
  if (r.ok) {
    const c = await caches.open(nome);
    await c.put(req, r.clone());
    if (max) limita(nome, max);
  }
  return r;
}

async function primaRete(req) {
  try {
    const r = await fetch(req);
    if (r.ok) (await caches.open(C_PAGINE)).put(req, r.clone());
    return r;
  } catch (err) {
    return (await caches.match(req, { ignoreSearch: true })) || Response.error();
  }
}

// notifiche (scripts/notifiche.py): {titolo, testo, url, tag, lingua}; al tocco si apre la pagina
self.addEventListener("push", (e) => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (err) { d = { testo: e.data ? e.data.text() : "" }; }
  e.waitUntil(self.registration.showNotification(d.titolo || "CAS Ticino", {
    body: d.testo || "", tag: d.tag || undefined, lang: d.lingua || "it",
    icon: new URL("assets/icone/icona-192.png", BASE).href, badge: new URL("assets/icone/badge-96.png", BASE).href,
    data: { url: /^https:\/\//.test(d.url || "") ? d.url : BASE },
  }));
});

self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const url = (e.notification.data && e.notification.data.url) || BASE;
  e.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then((finestre) => {
    for (const f of finestre) if (f.url === url && "focus" in f) return f.focus();
    return clients.openWindow(url);
  }));
});

// tiene al massimo `max` voci: via le più vecchie
async function limita(nome, max) {
  const c = await caches.open(nome), ks = await c.keys();
  for (let i = 0; i < ks.length - max; i++) await c.delete(ks[i]);
}
"""


def service_worker(statici, essenziali):
    corpo = SW.replace("__STATICI__", json.dumps(statici)).replace("__ESSENZIALI__", json.dumps(essenziali))
    versione = hashlib.md5(corpo.encode()).hexdigest()[:10]
    return corpo.replace("__VERSIONE__", versione)
