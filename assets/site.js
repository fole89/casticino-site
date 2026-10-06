// CAS Ticino - indirizzo senza .html: GitHub Pages serve corsi.html anche come /corsi, quindi nella barra degli indirizzi
// si toglie l'estensione (e index.html) senza ricaricare. Non in locale: python -m http.server non trova le pagine senza .html.
(function () {
  if (!history.replaceState || location.protocol === 'file:' || /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) return;
  var p = location.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
  if (p !== location.pathname) history.replaceState(history.state, '', p + location.search + location.hash);
})();

// CAS Ticino - menu fisso: classe .scrolled appena la pagina non è più in cima.
// Un elemento sentinella osservato con IntersectionObserver evita di ascoltare ogni evento di scroll.
(function () {
  var nav = document.querySelector('.site-nav nav');
  if (!nav || !('IntersectionObserver' in window)) return;
  var bar = nav.closest('.site-nav') || nav;
  var sentinel = document.createElement('div');
  sentinel.setAttribute('aria-hidden', 'true');
  sentinel.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:24px;pointer-events:none';
  document.body.prepend(sentinel);
  new IntersectionObserver(function (entries) {
    bar.classList.toggle('scrolled', !entries[0].isIntersecting);
  }).observe(sentinel);
})();

// CAS Ticino - comparsa delle sezioni allo scorrimento (solo se il sistema non chiede di ridurre il movimento)
(function () {
  var els = document.querySelectorAll('[data-reveal]');
  if (!els.length) return;
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    Array.prototype.forEach.call(els, function (el) { el.classList.add('is-in'); });
    return;
  }
  // Quello che è già nello schermo resta visibile; solo il resto aspetta lo scorrimento.
  // La classe che nasconde la mette questo script: se non gira (o è una versione vecchia in cache) si vede tutto.
  var h = window.innerHeight;
  Array.prototype.forEach.call(els, function (el) { if (el.getBoundingClientRect().top < h) el.classList.add('is-in'); });
  document.documentElement.classList.add('reveal-on');
  // i blocchi che entrano insieme (schede delle capanne, colonne) compaiono a cascata, 50 ms l'uno dall'altro (al massimo 4)
  var io = new IntersectionObserver(function (entries) {
    var k = 0;
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.style.setProperty('--i', Math.min(k++, 4)); e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  Array.prototype.forEach.call(els, function (el) { if (!el.classList.contains('is-in')) io.observe(el); });
})();

// CAS Ticino - titoloni: se una parola lunga non sta nello schermo, riduce il corpo finché entra
(function () {
  var hs = document.querySelectorAll('.hero-h, .sec-h, .fit');
  if (!hs.length) return;
  function fit() {
    Array.prototype.forEach.call(hs, function (h) {
      if (h.dataset.fs === undefined) h.dataset.fs = h.style.getPropertyValue('font-size');
      h.style.setProperty('font-size', h.dataset.fs);
      if (h.scrollWidth > h.clientWidth + 1) {
        var size = parseFloat(getComputedStyle(h).fontSize) * h.clientWidth / h.scrollWidth;
        h.style.setProperty('font-size', Math.floor(size) + 'px', 'important');
      }
    });
  }
  fit();
  window.addEventListener('resize', fit);
  if (document.fonts) document.fonts.ready.then(fit);
})();

// CAS Ticino - cambio di lingua: la stessa pagina nell'altra lingua tiene i parametri dell'indirizzo
// (gita.html?id=…, gite.html?gruppo=…); prima del menu mobile, che copia questi link.
(function () {
  if (!location.search) return;
  Array.prototype.forEach.call(document.querySelectorAll('.nav-lang'), function (a) {
    if (!/index\.html$/.test(a.getAttribute('href'))) a.href = a.getAttribute('href') + location.search;
  });
})();

// CAS Ticino - menu mobile (costruito a partire dal menu desktop)
(function () {
  var btn = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.site-nav nav');
  if (!btn || !nav) return;

  var panel = document.createElement('div');
  panel.className = 'mnav';
  panel.id = 'mobile-nav';
  panel.hidden = true;
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-modal', 'true');
  panel.setAttribute('aria-label', btn.getAttribute('data-titolo') || 'Menu');

  var top = document.createElement('div');
  top.className = 'mnav-top';
  var brand = nav.querySelector('a').cloneNode(true);
  var close = document.createElement('button');
  close.type = 'button';
  close.className = 'mnav-close';
  close.setAttribute('aria-label', btn.getAttribute('data-chiudi') || 'Chiudi menu');
  close.textContent = '×';
  top.appendChild(brand);
  top.appendChild(close);
  panel.appendChild(top);

  var desktop = nav.querySelector('.hide-sm');
  Array.prototype.forEach.call(desktop.children, function (item) {
    var group = document.createElement('div');
    group.className = 'mnav-group';
    if (item.classList.contains('dd')) {
      var head = item.querySelector('.dd-trigger');
      var a = document.createElement('a');
      a.href = head.getAttribute('href');
      a.textContent = head.textContent.trim();
      group.appendChild(a);
      var sub = document.createElement('div');
      sub.className = 'mnav-sub';
      item.querySelectorAll('.dd-menu a').forEach(function (l) {
        var c = document.createElement('a');
        c.href = l.getAttribute('href');
        c.textContent = l.textContent;
        sub.appendChild(c);
      });
      group.appendChild(sub);
    } else {
      var l = document.createElement('a');
      l.href = item.getAttribute('href');
      l.textContent = item.textContent.trim();
      group.appendChild(l);
    }
    panel.appendChild(group);
  });

  var cta = nav.querySelector('a.btn');
  if (cta) {
    var wrap = document.createElement('div');
    wrap.className = 'mnav-cta';
    wrap.appendChild(cta.cloneNode(true));
    panel.appendChild(wrap);
  }
  // le altre lingue: sugli schermi stretti non stanno nella barra in alto, quindi compaiono qui con il nome intero
  var langs = nav.querySelectorAll('.nav-lang');
  if (langs.length) {
    var lw = document.createElement('div');
    lw.className = 'mnav-langs';
    Array.prototype.forEach.call(langs, function (l) {
      var c = l.cloneNode(false);
      c.className = '';
      c.textContent = l.getAttribute('title') || l.textContent;
      lw.appendChild(c);
    });
    panel.appendChild(lw);
  }
  document.body.appendChild(panel);

  btn.setAttribute('aria-controls', 'mobile-nav');
  btn.setAttribute('aria-expanded', 'false');
  // con il pannello aperto il resto della pagina non è raggiungibile (Tab resta nel menu)
  var fuori = document.querySelectorAll('body > header, body > main, body > footer, body > .skip-link');
  function inerte(si) { Array.prototype.forEach.call(fuori, function (el) { if (si) el.setAttribute('inert', ''); else el.removeAttribute('inert'); }); }
  function open() { panel.hidden = false; inerte(true); btn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; close.focus(); }
  function shut() { panel.hidden = true; inerte(false); btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; btn.focus(); }
  btn.addEventListener('click', open);
  close.addEventListener('click', shut);
  panel.addEventListener('click', function (e) { if (e.target.tagName === 'A') shut(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) shut(); });
})();

// CAS Ticino - post Facebook delle capanne: il riquadro di Facebook si carica solo quando il visitatore lo chiede
// Il pulsante «Ultime notizie» in cima (o un link diretto a #notizie) vale come clic: il riquadro si carica subito.
(function () {
  var carica = [];
  Array.prototype.forEach.call(document.querySelectorAll('.fb-feed[data-fb]'), function (box) {
    var btn = box.querySelector('button');
    if (!btn) return;
    carica.push(function () { if (box.contains(btn)) btn.click(); });
    btn.addEventListener('click', function () {
      var w = Math.min(500, Math.max(180, Math.floor(box.clientWidth)));
      var src = 'https://www.facebook.com/plugins/page.php?tabs=timeline&small_header=true&hide_cover=true' +
        '&adapt_container_width=true&show_facepile=false&width=' + w + '&height=640' +
        '&locale=' + encodeURIComponent(box.dataset.lang || 'it_IT') + '&href=' + encodeURIComponent(box.dataset.fb);
      var f = document.createElement('iframe');
      f.src = src;
      f.title = box.dataset.titolo || 'Facebook';
      f.setAttribute('loading', 'lazy');
      f.setAttribute('allow', 'encrypted-media');
      box.innerHTML = '';
      box.appendChild(f);
    });
  });
  if (!carica.length) return;
  function tutti() { carica.forEach(function (fn) { fn(); }); }
  Array.prototype.forEach.call(document.querySelectorAll('[data-fb-apri]'), function (a) {
    a.addEventListener('click', tutti);
  });
  if (location.hash === '#notizie') tutti();
})();

// CAS Ticino - home, prossime gite, e mercatino: le pagine si rigenerano ogni mattina, quindi possono contenere gite già
// passate (data-fine) o annunci scaduti (data-scade); si tolgono qui, prima che la fila che scorre (sotto) duplichi le schede.
(function () {
  var d = new Date();
  var oggi = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  Array.prototype.forEach.call(document.querySelectorAll('.prossima[data-fine], .annuncio[data-scade]'), function (el) {
    if ((el.dataset.fine || el.dataset.scade) < oggi) el.remove();
  });
})();

// CAS Ticino - filtro per ruolo (pagine Capigita, Mercatino e News): ogni pulsante [data-filtro] mostra solo gli elementi
// [data-ruoli] che contengono quel ruolo; senza JavaScript il filtro resta nascosto e si vede l'elenco completo.
(function () {
  var bar = document.querySelector('.filtro[data-filtra]');
  if (!bar) return;
  var items = document.querySelectorAll(bar.dataset.filtra + ' [data-ruoli]');
  var stato = document.getElementById('filtro-stato');
  bar.hidden = false;
  bar.addEventListener('click', function (e) {
    var b = e.target.closest('button[data-filtro]');
    if (!b) return;
    var f = b.dataset.filtro, n = 0;
    Array.prototype.forEach.call(bar.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    Array.prototype.forEach.call(items, function (it) {
      var ok = !f || (' ' + it.dataset.ruoli + ' ').indexOf(' ' + f + ' ') !== -1;
      it.hidden = !ok;
      if (ok) n++;
    });
    if (stato) stato.textContent = f ? n + ' ' + (n === 1 ? bar.dataset.uno : bar.dataset.molti) + ': ' + b.firstChild.textContent.trim() : '';
    // i gruppi rimasti vuoti (ultima notizia e anni nella pagina News) spariscono, con il loro link nell'elenco degli anni
    Array.prototype.forEach.call(document.querySelectorAll(bar.dataset.filtra + ' [data-filtro-gruppo]'), function (g) {
      g.hidden = !g.querySelector('[data-ruoli]:not([hidden])');
      if (!g.id) return;
      Array.prototype.forEach.call(document.querySelectorAll('a[href="#' + g.id + '"]'), function (a) { a.hidden = g.hidden; });
    });
  });
})();


// CAS Ticino - home, news e prossime gite: la fila (.scorri) scorre da destra a sinistra in loop. Le schede si
// duplicano (le copie nascoste a lettori di schermo e tastiera) e la traccia si sposta di metà: il giro non ha stacchi.
// Si ferma al passaggio del mouse e col focus. Solo con un mouse: sui touch (dove non si può fermare) e con movimento
// ridotto resta da scorrere col dito.
(function () {
  if (!window.matchMedia || window.matchMedia('(prefers-reduced-motion: reduce)').matches
      || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  var PX_AL_SECONDO = 40;
  Array.prototype.forEach.call(document.querySelectorAll('.scorri'), function (box) {
    var traccia = box.querySelector('.scorri-traccia');
    if (!traccia || traccia.children.length < 2 || traccia.scrollWidth <= box.clientWidth) return;
    Array.prototype.slice.call(traccia.children).forEach(function (scheda) {
      var copia = scheda.cloneNode(true);
      copia.setAttribute('aria-hidden', 'true');
      copia.setAttribute('tabindex', '-1');
      Array.prototype.forEach.call(copia.querySelectorAll('a, button'), function (el) { el.setAttribute('tabindex', '-1'); });
      traccia.appendChild(copia);
    });
    box.style.setProperty('--scorri-durata', Math.round(traccia.scrollWidth / 2 / PX_AL_SECONDO) + 's');
    box.classList.add('is-animato');
  });
})();

// CAS Ticino - capigita: la presentazione si apre passando sulla foto (CSS) e, per i touch, toccandola;
// si chiude toccando fuori o con Esc.
(function () {
  var aperti = document.getElementsByClassName('is-open');
  function chiudi(tranne) {
    Array.prototype.slice.call(aperti).forEach(function (m) {
      if (m === tranne || !m.classList.contains('member--bio')) return;
      m.classList.remove('is-open');
      m.querySelector('.bio-toggle').setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.bio-toggle');
    if (!b) { if (!e.target.closest('.bio')) chiudi(); return; }
    var m = b.closest('.member--bio'), aperto = m.classList.toggle('is-open');
    b.setAttribute('aria-expanded', aperto ? 'true' : 'false');
    chiudi(m);
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') chiudi(); });
})();

// CAS Ticino - feste: nella settimana prima di Carnevale, Pasqua, 1° agosto, Halloween e Natale un'icona dopo il titolo
// della home e un effetto leggero sulla sua foto. Solo decorazione (aria-hidden), nessuna pagina in più.
// Per provarle in qualsiasi giorno: ?festa=carnevale | pasqua | agosto | halloween | natale (?festa=no le spegne).
(function () {
  function pasqua(y) { // calcolo gregoriano (Meeus/Jones/Butcher)
    var a = y % 19, b = Math.floor(y / 100), c = y % 100, d = Math.floor(b / 4), e = b % 4,
        f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
        i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
        mese = Math.floor((h + l - 7 * m + 114) / 31), giorno = (h + l - 7 * m + 114) % 31 + 1;
    return new Date(y, mese - 1, giorno);
  }
  function giorni(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function festa(oggi) {
    var y = oggi.getFullYear(), p = pasqua(y), martediGrasso = giorni(p, -47);
    var periodi = [
      ['carnevale', giorni(martediGrasso, -6), martediGrasso],
      ['pasqua', giorni(p, -7), giorni(p, 1)],          // fino a Pasquetta
      ['agosto', new Date(y, 6, 25), new Date(y, 7, 1)],
      ['halloween', new Date(y, 9, 24), new Date(y, 9, 31)],
      ['natale', new Date(y, 11, 18), new Date(y, 11, 26)] // fino a Santo Stefano
    ];
    var t = new Date(y, oggi.getMonth(), oggi.getDate());
    for (var j = 0; j < periodi.length; j++) if (t >= periodi[j][1] && t <= periodi[j][2]) return periodi[j][0];
    return null;
  }

  var scelta = null;
  try { scelta = new URLSearchParams(location.search).get('festa'); } catch (e) {}
  var nome = scelta ? (scelta === 'no' ? null : scelta) : festa(new Date());
  var FESTE = ['carnevale', 'pasqua', 'agosto', 'halloween', 'natale'];
  if (!nome || FESTE.indexOf(nome) === -1) return;
  // icone 3D in assets/img/feste/ (Fluent Emoji, licenza MIT); il percorso parte da quello di site.js, che conosce la profondità della pagina
  var script = document.querySelector('script[src*="assets/site.js"]');
  var radice = script ? script.getAttribute('src').split('assets/site.js')[0] : '';
  function icona(cls) {
    var el = document.createElement('span');
    el.className = cls;
    el.setAttribute('aria-hidden', 'true');
    el.innerHTML = '<img src="' + radice + 'assets/img/feste/' + nome + '.webp" alt="" width="128" height="128" decoding="async">';
    return el;
  }
  document.documentElement.classList.add('festa', 'festa--' + nome);

  // icona dopo il titolo «In montagna con noi.»
  var titolo = document.querySelector('.hero h1');
  if (titolo) titolo.appendChild(icona('festa-icona'));

  // effetto sulla foto della home, solo se il sistema non chiede di ridurre il movimento
  var foto = document.querySelector('.hero .band');
  if (!foto || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var strato = document.createElement('div');
  strato.className = 'festa-strato';
  strato.setAttribute('aria-hidden', 'true');
  var quanti = { natale: 28, carnevale: 26, pasqua: 14, halloween: 3, agosto: 4 }[nome];
  for (var n = 0; n < quanti; n++) {
    var p = document.createElement('i');
    p.style.left = (Math.random() * 96 + 2) + '%';
    if (nome === 'halloween' || nome === 'agosto') p.style.top = (Math.random() * 45 + 8) + '%'; // gli altri cadono dall'alto
    p.style.animationDelay = (-Math.random() * 14).toFixed(2) + 's';
    p.style.animationDuration = (9 + Math.random() * 7).toFixed(2) + 's';
    p.style.setProperty('--s', (0.6 + Math.random() * 0.8).toFixed(2));
    p.className = 'v' + (n % 4);
    strato.appendChild(p);
  }
  foto.appendChild(strato);
})();

// CAS Ticino - avviso in cima alla pagina (shared.avviso_html): chi lo chiude non lo rivede finché il testo non cambia.
// Il browser ricorda solo l'impronta dell'avviso chiuso (localStorage «avviso»); senza memoria si chiude solo per questa pagina.
(function () {
  var box = document.querySelector('.avviso[data-avviso]');
  if (!box) return;
  box.querySelector('.avviso-chiudi').addEventListener('click', function () {
    try { localStorage.setItem('avviso', box.dataset.avviso); } catch (e) {}
    document.documentElement.classList.add('avviso-via');
    var main = document.getElementById('contenuto');
    if (main) { main.setAttribute('tabindex', '-1'); main.focus({ preventScroll: true }); }
  });
})();

// CAS Ticino - sito installabile: registra il service worker (sw.js, generato da scripts/redesign/pwa.py) e gli chiede,
// al massimo una volta al giorno per lingua, di salvare le pagine da avere anche senza rete. In anteprima locale solo
// con ?pwa=1 (poi resta attivo finché non lo si cancella dagli strumenti del browser).
(function () {
  if (!('serviceWorker' in navigator) || location.protocol === 'file:') return;
  var locale = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname);
  if (locale && !/[?&]pwa=1\b/.test(location.search) && !navigator.serviceWorker.controller) return;
  var script = document.querySelector('script[src*="assets/site.js"]');
  var radice = script ? script.getAttribute('src').split('assets/site.js')[0] : '';
  var lingua = (document.documentElement.lang || 'it').slice(0, 2);
  navigator.serviceWorker.register(radice + 'sw.js').then(function () { return navigator.serviceWorker.ready; })
    .then(function (reg) {
      var oggi = new Date().toISOString().slice(0, 10), chiave = 'pwa-salvate-' + lingua;
      try { if (localStorage.getItem(chiave) === oggi) return; localStorage.setItem(chiave, oggi); } catch (e) {}
      if (reg.active) reg.active.postMessage({ lingua: lingua });
    })
    .catch(function () {});
})();

// CAS Ticino - «App sul telefono» nel footer: dove il browser lo permette (Android, computer) il pulsante «Installa»
// apre la sua richiesta d'installazione; su iPhone e iPad, dove non si può, una riga spiega il gesto
// (Condividi › Aggiungi alla schermata Home). Niente se il sito è già aperto come app.
(function () {
  var box = document.querySelector('.app-install');
  if (!box) return;
  var installata = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  if (installata) return;
  var bottone = box.querySelector('.app-installa'), richiesta = null;
  var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (ios) { box.querySelector('.app-ios').hidden = false; box.hidden = false; }
  window.addEventListener('beforeinstallprompt', function (e) {
    if (ios) return;   // su iPhone si installa solo da Condividi
    e.preventDefault();
    richiesta = e;
    bottone.hidden = false;
    box.hidden = false;
  });
  bottone.addEventListener('click', function () {
    if (!richiesta) return;
    richiesta.prompt();
    richiesta.userChoice.then(function (scelta) { if (scelta.outcome === 'accepted') box.hidden = true; });
    richiesta = null;
  });
  window.addEventListener('appinstalled', function () { box.hidden = true; });
})();

// CAS Ticino - «Notifiche» nel footer (un solo canale): dopo il clic il browser chiede il permesso e crea un indirizzo
// di notifica anonimo, salvato nel servizio scripts/notifiche/ (data-api); «Disattiva» lo cancella. Serve il service
// worker (sw.js): in anteprima locale solo con ?pwa=1. Su iPhone le notifiche arrivano solo con il sito installato.
(function () {
  var box = document.querySelector('.notifiche[data-api]');
  if (!box || !('serviceWorker' in navigator)) return;
  var api = box.dataset.api.replace(/\/?$/, '/'), stato = box.querySelector('.notifiche-stato');
  var attiva = box.querySelector('.notifiche-attiva'), disattiva = box.querySelector('.notifiche-disattiva');
  var lingua = (document.documentElement.lang || 'it').slice(0, 2);
  var installata = (window.matchMedia && matchMedia('(display-mode: standalone)').matches) || navigator.standalone === true;
  var ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  if (ios && !installata) { stato.textContent = box.dataset.ios; box.hidden = false; return; }
  if (!('PushManager' in window) || !('Notification' in window)) return;

  function chiave(b64) {  // chiave pubblica VAPID (base64url) nel formato che vuole il browser
    var s = atob(b64.replace(/-/g, '+').replace(/_/g, '/') + '='.repeat((4 - (b64.length % 4)) % 4));
    var out = new Uint8Array(s.length);
    for (var i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
    return out;
  }
  function mostra(iscritto) {
    var bloccate = Notification.permission === 'denied';
    attiva.hidden = iscritto || bloccate;
    disattiva.hidden = !iscritto;
    stato.textContent = iscritto ? box.dataset.attive : bloccate ? box.dataset.bloccate : '';
    box.hidden = false;
  }
  function servizio(percorso, dati) {
    return fetch(api + percorso, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dati) })
      .then(function (r) { if (!r.ok) throw new Error(r.status); });
  }

  navigator.serviceWorker.ready.then(function (reg) {
    reg.pushManager.getSubscription().then(function (s) { mostra(!!s); });
    attiva.addEventListener('click', function () {
      attiva.disabled = true;
      Promise.resolve(Notification.requestPermission()).then(function (permesso) {
        if (permesso !== 'granted') { mostra(false); return; }
        return reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: chiave(box.dataset.chiave) })
          .then(function (s) {
            var j = s.toJSON();
            // se il servizio non risponde si annulla anche l'iscrizione nel browser: niente iscritti «a metà»
            return servizio('iscrizione', { endpoint: j.endpoint, keys: j.keys, lingua: lingua })
              .catch(function (e) { return s.unsubscribe().then(function () { throw e; }); });
          })
          .then(function () { mostra(true); disattiva.focus(); });
      }).catch(function () { mostra(false); stato.textContent = box.dataset.errore; })
        .then(function () { attiva.disabled = false; });
    });
    disattiva.addEventListener('click', function () {
      disattiva.disabled = true;
      reg.pushManager.getSubscription().then(function (s) {
        if (!s) return;
        var endpoint = s.endpoint;
        return s.unsubscribe().then(function () { return servizio('disiscrizione', { endpoint: endpoint }).catch(function () {}); });
      }).then(function () { mostra(false); attiva.focus(); }, function () { stato.textContent = box.dataset.errore; })
        .then(function () { disattiva.disabled = false; });
    });
  });
})();
