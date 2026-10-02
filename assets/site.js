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
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
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
  function open() { panel.hidden = false; btn.setAttribute('aria-expanded', 'true'); document.body.style.overflow = 'hidden'; close.focus(); }
  function shut() { panel.hidden = true; btn.setAttribute('aria-expanded', 'false'); document.body.style.overflow = ''; btn.focus(); }
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

// CAS Ticino - filtro per ruolo (pagina Capigita): ogni pulsante [data-filtro] mostra solo gli elementi
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
  });
})();

// CAS Ticino - feste: nella settimana prima di Carnevale, Pasqua, 1° agosto, Halloween e Natale un'icona accanto al logo
// e un effetto leggero sulla foto della home. Solo decorazione (aria-hidden), nessuna pagina in più.
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
  var ICONE = {
    natale: '<svg viewBox="0 0 32 32"><path class="f-rosso" d="M4 24 C8 12 16 4 26 8 L22 12 C16 10 12 16 12 24 Z"/><rect class="f-bianco" x="2" y="22" width="13" height="5" rx="2.5"/><circle class="f-bianco" cx="26" cy="9" r="3.6"/></svg>',
    halloween: '<svg viewBox="0 0 32 32"><path class="f-verde" d="M15 9 C15 5 17 3 20 3 L20 5 C18 5 17 6 17 9 Z"/><ellipse class="f-arancio" cx="16" cy="19" rx="12" ry="10"/><path class="f-scuro" d="M9 16 L12 13 L14 17 Z M23 16 L20 13 L18 17 Z M9 21 Q16 27 23 21 L21 22 L19 21 L16 23 L13 21 L11 22 Z"/></svg>',
    pasqua: '<svg viewBox="0 0 32 32"><ellipse class="f-giallo" cx="16" cy="17" rx="10" ry="13"/><path class="f-rosso" d="M6.4 14 L11 11 L16 14 L21 11 L25.6 14 L25.9 17 L21 14 L16 17 L11 14 L6.1 17 Z"/><circle class="f-blu" cx="12" cy="22" r="1.6"/><circle class="f-blu" cx="16" cy="24" r="1.6"/><circle class="f-blu" cx="20" cy="22" r="1.6"/></svg>',
    carnevale: '<svg viewBox="0 0 32 32"><path class="f-viola" d="M2 12 C8 9 12 10 16 13 C20 10 24 9 30 12 C30 20 26 23 21 23 C18 23 17 20 16 19 C15 20 14 23 11 23 C6 23 2 20 2 12 Z"/><ellipse class="f-bianco" cx="9.5" cy="15.5" rx="3" ry="2"/><ellipse class="f-bianco" cx="22.5" cy="15.5" rx="3" ry="2"/><path class="f-giallo" d="M27 10 C28 5 30 3 31 2 C31 6 30 9 28.5 11 Z"/></svg>',
    agosto: '<svg viewBox="0 0 32 32"><path class="f-scuro" d="M15 0 H17 V5 H15 Z"/><path class="f-rosso" d="M8 7 H24 C26 11 26 21 24 25 H8 C6 21 6 11 8 7 Z"/><path class="f-bianco" d="M14 11 H18 V14 H21 V18 H18 V21 H14 V18 H11 V14 H14 Z"/><path class="f-scuro" d="M9 5 H23 V7 H9 Z M9 25 H23 V27 H9 Z"/></svg>'
  };
  if (!nome || !ICONE[nome]) return;
  document.documentElement.classList.add('festa', 'festa--' + nome);

  var brand = document.querySelector('.site-nav .brand');
  if (brand) {
    var icona = document.createElement('span');
    icona.className = 'festa-icona';
    icona.setAttribute('aria-hidden', 'true');
    icona.innerHTML = ICONE[nome];
    brand.appendChild(icona);
  }

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
