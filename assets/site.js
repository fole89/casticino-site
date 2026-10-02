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
