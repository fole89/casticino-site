// CAS Ticino - pagina Foto (foto.html, de/foto.html, en/foto.html): legge data/foto.json (#albums[data-json]) e mostra
// le ultime gite (stili in assets/site.css, blocco «foto delle gite»)
(function () {
  var root = document.getElementById('albums');
  var more = document.getElementById('load-more');
  if (!root) return;
  var PAGE = 5, shown = 0, albums = [];
  // testi nella lingua della pagina (<html lang>); titoli e resoconti delle gite restano in italiano
  var LINGUA = (document.documentElement.lang || 'it').slice(0, 2);
  var TX = {
    it: { foto: 'foto', di: 'di', resoconto: 'Resoconto: ', dettagli: 'Dettagli della gita', prec: 'Foto precedente', succ: 'Foto successiva',
          mostra: 'Mostra foto ', nessuna: 'Nessuna foto pubblicata di recente.', errore: 'Le foto non sono disponibili al momento. Puoi consultarle sul portale Droptour.' },
    de: { foto: 'Fotos', di: 'von', resoconto: 'Bericht: ', dettagli: 'Details der Tour', prec: 'Vorheriges Foto', succ: 'Nächstes Foto',
          mostra: 'Foto anzeigen: ', nessuna: 'In letzter Zeit wurden keine Fotos veröffentlicht.', errore: 'Die Fotos sind im Moment nicht verfügbar. Sie finden sie auf dem Portal Droptour.' },
    en: { foto: 'photos', di: 'of', resoconto: 'Report: ', dettagli: 'Trip details', prec: 'Previous photo', succ: 'Next photo',
          mostra: 'Show photo ', nessuna: 'No photos published recently.', errore: 'The photos are not available at the moment. You can find them on the Droptour portal.' }
  }[LINGUA] || null;
  if (!TX) { LINGUA = 'it'; TX = { foto: 'foto', di: 'di', resoconto: 'Resoconto: ', dettagli: 'Dettagli della gita', prec: 'Foto precedente', succ: 'Foto successiva', mostra: 'Mostra foto ', nessuna: 'Nessuna foto pubblicata di recente.', errore: 'Le foto non sono disponibili al momento. Puoi consultarle sul portale Droptour.' }; }
  var IT = LINGUA === 'it' ? {} : { lang: 'it' };  // attributo per i testi in italiano
  var fmt = new Intl.DateTimeFormat({ it: 'it-CH', de: 'de-CH', en: 'en-GB' }[LINGUA], { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
  function conIt(attrs) { Object.keys(IT).forEach(function (k) { attrs[k] = IT[k]; }); return attrs; }

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
    var meta = (a.place ? a.place + ', ' : '') + n + ' ' + TX.foto;

    // resoconto intero in un riquadro ad altezza massima, scorrevole: il carosello resta vicino al titolo
    var text = a.text ? el('div', conIt({ class: 'album-text', tabindex: '0', role: 'region', 'aria-label': TX.resoconto + a.title, text: a.text })) : null;

    var info = el('div', { class: 'album-info' }, [
      date ? el('span', { class: 'album-date', text: date }) : null,
      el('h2', conIt({ class: 'h2', text: a.title })),
      el('span', { class: 'small', text: meta }),
      text,
      a.link ? el('a', { class: 'link', href: a.link, text: TX.dettagli }) : null
    ]);

    var photo = el('img', { alt: '', decoding: 'async' });
    photo.addEventListener('load', function () { photo.classList.remove('cambia'); });
    photo.addEventListener('error', function () { photo.classList.remove('cambia'); });
    var counter = el('span', { class: 'album-count' });
    var thumbs = [];
    function show(k) {
      idx = (k + n) % n;
      if (photo.getAttribute('src')) photo.classList.add('cambia');  // dissolvenza breve tra una foto e l'altra (CSS)
      photo.src = a.photos[idx].large;
      photo.alt = a.title + ', ' + (idx + 1) + ' ' + TX.di + ' ' + n;
      counter.textContent = (idx + 1) + ' / ' + n;
      thumbs.forEach(function (t, i) { t.classList.toggle('sel', i === idx); t.setAttribute('aria-current', i === idx ? 'true' : 'false'); });
    }
    var frame = el('div', { class: 'album-frame' }, [
      photo,
      n > 1 ? el('button', { type: 'button', class: 'album-nav album-nav--prev', 'aria-label': TX.prec, onclick: function () { show(idx - 1); } }, [arrow(-1)]) : null,
      n > 1 ? el('button', { type: 'button', class: 'album-nav album-nav--next', 'aria-label': TX.succ, onclick: function () { show(idx + 1); } }, [arrow(1)]) : null,
      counter
    ]);
    var grid = el('div', { class: 'album-thumbs' });
    a.photos.forEach(function (p, k) {
      var b = el('button', { type: 'button', 'aria-label': TX.mostra + (k + 1), onclick: function () { show(k); } },
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

  fetch(root.dataset.json || 'data/foto.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      albums = (data.albums || []).filter(function (a) { return a.photos && a.photos.length; });
      if (!albums.length) { status(TX.nessuna); return; }
      root.textContent = '';
      next();
    })
    .catch(function () { status(TX.errore); });
  if (more) more.addEventListener('click', next);
})();
