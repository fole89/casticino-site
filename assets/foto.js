// CAS Ticino - pagina Foto: legge data/foto.json e mostra le ultime gite (stili in assets/site.css, blocco «foto delle gite»)
(function () {
  var root = document.getElementById('albums');
  var more = document.getElementById('load-more');
  if (!root) return;
  var PAGE = 5, shown = 0, albums = [];
  var fmt = new Intl.DateTimeFormat('it-CH', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') n.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') n.addEventListener(k.slice(2), attrs[k]);
      else n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }
  function arrow(dir) {
    var ns = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(ns, 'svg');
    svg.setAttribute('width', '18'); svg.setAttribute('height', '18'); svg.setAttribute('viewBox', '0 0 16 16'); svg.setAttribute('aria-hidden', 'true');
    var p = document.createElementNS(ns, 'path');
    p.setAttribute('d', dir < 0 ? 'M10 3 5 8l5 5' : 'M6 3l5 5-5 5');
    p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '2'); p.setAttribute('fill', 'none');
    svg.appendChild(p); return svg;
  }
  function status(msg) {
    root.textContent = '';
    root.appendChild(el('p', { class: 'albums-status', text: msg }));
  }

  function render(a) {
    var n = a.photos.length, idx = 0;
    var date = a.date ? fmt.format(new Date(a.date + 'T12:00:00')) : '';
    var meta = (a.place ? a.place + ', ' : '') + n + ' foto';

    // resoconto intero in un riquadro ad altezza massima, scorrevole: il carosello resta vicino al titolo
    var text = a.text ? el('div', { class: 'album-text', tabindex: '0', role: 'region', 'aria-label': 'Resoconto: ' + a.title, text: a.text }) : null;

    var info = el('div', { class: 'album-info' }, [
      date ? el('span', { class: 'album-date', text: date }) : null,
      el('h2', { class: 'h2', text: a.title }),
      el('span', { class: 'small', text: meta }),
      text,
      a.link ? el('a', { class: 'link', href: a.link, text: 'Dettagli della gita' }) : null
    ]);

    var photo = el('img', { alt: '', decoding: 'async' });
    var counter = el('span', { class: 'album-count' });
    var thumbs = [];
    function show(k) {
      idx = (k + n) % n;
      photo.src = a.photos[idx].large;
      photo.alt = a.title + ', foto ' + (idx + 1) + ' di ' + n;
      counter.textContent = (idx + 1) + ' / ' + n;
      thumbs.forEach(function (t, i) { t.classList.toggle('sel', i === idx); t.setAttribute('aria-current', i === idx ? 'true' : 'false'); });
    }
    var frame = el('div', { class: 'album-frame' }, [
      photo,
      n > 1 ? el('button', { type: 'button', class: 'album-nav album-nav--prev', 'aria-label': 'Foto precedente', onclick: function () { show(idx - 1); } }, [arrow(-1)]) : null,
      n > 1 ? el('button', { type: 'button', class: 'album-nav album-nav--next', 'aria-label': 'Foto successiva', onclick: function () { show(idx + 1); } }, [arrow(1)]) : null,
      counter
    ]);
    var grid = el('div', { class: 'album-thumbs' });
    a.photos.forEach(function (p, k) {
      var b = el('button', { type: 'button', 'aria-label': 'Mostra foto ' + (k + 1), onclick: function () { show(k); } },
        [el('img', { src: p.thumb, alt: '', loading: 'lazy', decoding: 'async' })]);
      thumbs.push(b); grid.appendChild(b);
    });
    show(0);
    return el('article', { class: 'album' }, [info, el('div', { class: 'album-viewer' }, [frame, grid])]);
  }

  // sfumatura in fondo al resoconto solo se è più lungo del riquadro; sparisce arrivati alla fine
  function fade(box) {
    function upd() { box.classList.toggle('has-more', box.scrollTop + box.clientHeight < box.scrollHeight - 4); }
    box.addEventListener('scroll', upd, { passive: true });
    upd();
  }

  function next() {
    albums.slice(shown, shown + PAGE).forEach(function (a) {
      var art = render(a);
      root.appendChild(art);
      var box = art.querySelector('.album-text');
      if (box) fade(box);
    });
    shown += PAGE;
    if (more) more.hidden = shown >= albums.length;
  }

  fetch('data/foto.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      albums = (data.albums || []).filter(function (a) { return a.photos && a.photos.length; });
      if (!albums.length) { status('Nessuna foto pubblicata di recente.'); return; }
      root.textContent = '';
      next();
    })
    .catch(function () { status('Le foto non sono disponibili al momento. Puoi consultarle sul portale Droptour.'); });
  if (more) more.addEventListener('click', next);
})();
