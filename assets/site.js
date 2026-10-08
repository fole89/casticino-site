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

// CAS Ticino - capanne, «In questa pagina» (.salti): la barra resta appiccicata sotto il menu. Qui si segna quando è
// ferma (.is-fisso: linea e ombra), si allarga lo spazio lasciato sopra i titoli raggiunti con un link (scroll-padding)
// e si evidenzia il pulsante della sezione in cui ci si trova; sul telefono la riga scorre fino a mostrarlo.
(function () {
  var barra = document.querySelector('.salti');
  if (!barra) return;
  var riga = barra.querySelector('.subnav-links');
  var voci = Array.prototype.map.call(riga.querySelectorAll('a[href^="#"]'), function (a) {
    return { a: a, sez: document.getElementById(a.getAttribute('href').slice(1)) };
  }).filter(function (v) { return v.sez; });
  var root = document.documentElement;
  function alto() { return parseFloat(getComputedStyle(barra).top) || 0; }
  function spazio() { root.style.scrollPaddingTop = (alto() + barra.offsetHeight + 16) + 'px'; }
  spazio();
  addEventListener('resize', spazio);

  var attiva = null, inCoda = false;
  function aggiorna() {
    inCoda = false;
    var limite = alto() + barra.offsetHeight + 40, nuova = null;
    barra.classList.toggle('is-fisso', barra.getBoundingClientRect().top <= alto() + 0.5 && scrollY > 0);
    voci.forEach(function (v) { if (v.sez.getBoundingClientRect().top <= limite) nuova = v; });
    // in fondo alla pagina l'ultima sezione può non arrivare mai in cima: vale lei
    if (voci.length && innerHeight + scrollY >= root.scrollHeight - 2 && voci[voci.length - 1].sez.getBoundingClientRect().top < innerHeight) nuova = voci[voci.length - 1];
    if (nuova === attiva) return;
    if (attiva) attiva.a.removeAttribute('aria-current');
    attiva = nuova;
    if (!attiva) return;
    attiva.a.setAttribute('aria-current', 'location');
    var r = attiva.a.getBoundingClientRect(), c = riga.getBoundingClientRect();
    if (riga.scrollWidth > riga.clientWidth && (r.left < c.left || r.right > c.right)) {
      var ridotto = matchMedia('(prefers-reduced-motion: reduce)').matches;
      riga.scrollTo({ left: riga.scrollLeft + r.left - c.left - 20, behavior: ridotto ? 'auto' : 'smooth' });
    }
  }
  addEventListener('scroll', function () {
    if (!inCoda) { inCoda = true; requestAnimationFrame(aggiorna); }
  }, { passive: true });
  aggiorna();
})();

// CAS Ticino - Storia, le tappe (.tappe): la corda si riempie di rosso fino a poco sopra metà schermo (--avanza), i nodi
// che ha raggiunto diventano rossi (.passata) e il rampone e la piccozza ([data-moto]) girano e oscillano con lo
// scorrimento (--p da 0 a 1 mentre attraversano lo schermo). Con movimento ridotto gli oggetti restano fermi;
// senza JavaScript la corda è grigia e i disegni sono già tracciati.
(function () {
  var tappe = document.querySelector('.tappe');
  if (!tappe) return;
  var nodi = Array.prototype.slice.call(tappe.querySelectorAll('.tappa-nodo'));
  var moti = matchMedia('(prefers-reduced-motion: reduce)').matches ? [] : Array.prototype.slice.call(tappe.querySelectorAll('[data-moto], .tappa-figura--oggetto'));
  function tra(x) { return Math.max(0, Math.min(1, x)); }
  var inCoda = false;
  function aggiorna() {
    inCoda = false;
    var vh = innerHeight, soglia = vh * 0.55, r = tappe.getBoundingClientRect();
    tappe.style.setProperty('--avanza', tra((soglia - r.top) / r.height).toFixed(4));
    nodi.forEach(function (n) {
      var b = n.getBoundingClientRect();
      n.parentNode.classList.toggle('passata', b.top + b.height / 2 <= soglia);
    });
    moti.forEach(function (m) {
      var b = m.getBoundingClientRect();
      if (b.bottom < -200 || b.top > vh + 200) return;
      var p = tra((vh - b.top) / (vh + b.height));
      m.style.setProperty('--p', p.toFixed(4));
      m.style.setProperty('--z', (1 - Math.abs(p - 0.5) * 2).toFixed(4));
    });
  }
  function chiedi() { if (!inCoda) { inCoda = true; requestAnimationFrame(aggiorna); } }
  addEventListener('scroll', chiedi, { passive: true });
  addEventListener('resize', chiedi);
  aggiorna();
})();

// CAS Ticino - home, prossime gite, mercatino e avvisi delle capanne: le pagine possono contenere gite già passate
// (data-fine), annunci o avvisi scaduti (data-scade); si tolgono qui, prima che la fila che scorre (sotto) duplichi le schede.
(function () {
  var d = new Date();
  var oggi = d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  Array.prototype.forEach.call(document.querySelectorAll('.prossima[data-fine], .annuncio[data-scade], .avviso-capanna-sez[data-scade]'), function (el) {
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


// CAS Ticino - foto a schermo intero (Foto e resoconti, gallerie delle capanne): CASschermo.apri(foto, k, opzioni)
// con foto = [{src, alt}], opzioni {titolo, lang, cambia(k)}. Un solo <dialog class="schermo"> per pagina (Esc e focus li
// gestisce il browser): si chiude con ×, con un clic sulla foto o sullo sfondo; frecce, tastiera e dito cambiano foto.
// Le miniature delle gallerie (.gallery a) lo aprono invece della pagina con l'immagine (che resta senza JavaScript
// e con Ctrl/⌘ + clic). Stili in site.css, blocco «schermo».
(function () {
  var TX = {
    it: { chiudi: 'Chiudi', prec: 'Foto precedente', succ: 'Foto successiva', foto: 'Foto ingrandita' },
    de: { chiudi: 'Schliessen', prec: 'Vorheriges Foto', succ: 'Nächstes Foto', foto: 'Vergrössertes Foto' },
    en: { chiudi: 'Close', prec: 'Previous photo', succ: 'Next photo', foto: 'Enlarged photo' }
  }[(document.documentElement.lang || 'it').slice(0, 2)] || null;
  if (!TX || !window.HTMLDialogElement) return;
  var s = null;

  function nodo(tag, cls, attr) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    Object.keys(attr || {}).forEach(function (k) { n.setAttribute(k, attr[k]); });
    return n;
  }
  function freccia(dir) {
    var ns = 'http://www.w3.org/2000/svg', svg = document.createElementNS(ns, 'svg'), p = document.createElementNS(ns, 'path');
    svg.setAttribute('width', '18'); svg.setAttribute('height', '18'); svg.setAttribute('viewBox', '0 0 16 16'); svg.setAttribute('aria-hidden', 'true');
    p.setAttribute('d', dir < 0 ? 'M10 3 5 8l5 5' : 'M6 3l5 5-5 5');
    p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '2'); p.setAttribute('fill', 'none');
    svg.appendChild(p);
    return svg;
  }

  function crea() {
    var d = nodo('dialog', 'schermo', { 'aria-label': TX.foto });
    var img = nodo('img', '', { alt: '', decoding: 'async' });
    var titolo = nodo('p', 'schermo-titolo'), conta = nodo('span', 'schermo-conta');
    var chiudi = nodo('button', 'schermo-chiudi', { type: 'button', 'aria-label': TX.chiudi });
    chiudi.textContent = '×';
    var prec = nodo('button', 'schermo-nav schermo-nav--prec', { type: 'button', 'aria-label': TX.prec });
    var succ = nodo('button', 'schermo-nav schermo-nav--succ', { type: 'button', 'aria-label': TX.succ });
    prec.appendChild(freccia(-1)); succ.appendChild(freccia(1));
    var barra = nodo('div', 'schermo-barra');
    barra.appendChild(titolo); barra.appendChild(conta);
    [img, barra, prec, succ, chiudi].forEach(function (x) { d.appendChild(x); });
    document.body.appendChild(d);
    s = { d: d, img: img, titolo: titolo, conta: conta, prec: prec, succ: succ };
    var vai = function (passo) { mostra(s.k + passo); };
    chiudi.addEventListener('click', function () { d.close(); });
    prec.addEventListener('click', function (e) { e.stopPropagation(); vai(-1); });
    succ.addEventListener('click', function (e) { e.stopPropagation(); vai(1); });
    d.addEventListener('click', function (e) { if (e.target === d || e.target === img) d.close(); });
    d.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); vai(-1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); vai(1); }
    });
    var x0 = null;  // scorrimento col dito: a sinistra la foto dopo, a destra quella prima
    d.addEventListener('pointerdown', function (e) { x0 = e.pointerType === 'mouse' ? null : e.clientX; });
    d.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0;
      x0 = null;
      if (Math.abs(dx) > 50) vai(dx < 0 ? 1 : -1);
    });
    d.addEventListener('close', function () {
      document.documentElement.classList.remove('schermo-aperto');
      if (s.torna && s.torna.focus) s.torna.focus();
    });
  }

  function mostra(j) {
    var n = s.foto.length;
    s.k = (j + n) % n;
    s.img.src = s.foto[s.k].src;
    s.img.alt = s.foto[s.k].alt || '';
    s.titolo.textContent = s.opz.titolo || s.foto[s.k].alt || '';
    if (s.opz.lang) s.titolo.setAttribute('lang', s.opz.lang); else s.titolo.removeAttribute('lang');
    s.conta.textContent = n > 1 ? (s.k + 1) + ' / ' + n : '';
    s.prec.hidden = s.succ.hidden = n < 2;
    if (s.opz.cambia) s.opz.cambia(s.k);
  }

  window.CASschermo = {
    apri: function (foto, k, opz) {
      if (!s) crea();
      s.foto = foto; s.opz = opz || {}; s.torna = document.activeElement;
      mostra(k || 0);
      document.documentElement.classList.add('schermo-aperto');
      s.d.showModal();
    }
  };

  // gallerie delle capanne: la miniatura apre la foto grande qui, con le altre della stessa galleria
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.gallery a[href]');
    if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
    e.preventDefault();
    var voci = Array.prototype.slice.call(a.closest('.gallery').querySelectorAll('a[href]'));
    var foto = voci.map(function (x) { var im = x.querySelector('img'); return { src: x.href, alt: im ? im.alt : '' }; });
    window.CASschermo.apri(foto, voci.indexOf(a));
  });
})();
