// Service worker del sito CAS Ticino: generato da scripts/redesign/pwa.py (pages.py), non modificare a mano.
const VERSIONE = "098599758f";
const STATICI = ["assets/site.css?v=bc40339f", "assets/site.js?v=323c5a4f", "assets/gite.js?v=a1574ae8", "assets/cerca.js?v=6de6c786", "assets/foto.js?v=0b48c1c6", "assets/noleggio.js?v=f548c601", "assets/fonts/geist-latin-ext.woff2", "assets/fonts/geist-latin.woff2", "assets/fonts/geist-mono-latin-ext.woff2", "assets/fonts/geist-mono-latin.woff2", "assets/logo-cas.webp", "assets/logo-cas-stemma.webp", "assets/icone/icona-192.png", "assets/icone/icona-512.png", "assets/icone/icona-maskable-512.png", "assets/icone/apple-touch-icon.png", "assets/icone/badge-96.png", "offline.html", "de/offline.html", "en/offline.html"];      // salvati all'installazione: stili, script, caratteri, icone, pagine offline
const ESSENZIALI = {"it": ["index.html", "partecipare.html", "soccorso.html", "campotencia.html", "cristallina.html", "adula.html", "motterascio.html", "montebar.html", "baitadelluca.html"], "de": ["de/index.html", "de/partecipare.html", "de/soccorso.html", "de/campotencia.html", "de/cristallina.html", "de/adula.html", "de/motterascio.html", "de/montebar.html", "de/baitadelluca.html"], "en": ["en/index.html", "en/partecipare.html", "en/soccorso.html", "en/campotencia.html", "en/cristallina.html", "en/adula.html", "en/motterascio.html", "en/montebar.html", "en/baitadelluca.html"]};  // per lingua: pagine da avere anche senza rete
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
