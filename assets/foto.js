// CAS Ticino — pagina Foto: legge data/foto.json e mostra le ultime gite
(function () {
  var root = document.getElementById('albums');
  var more = document.getElementById('load-more');
  if (!root) return;
  var PAGE = 5, shown = 0, albums = [];
  var fmt = new Intl.DateTimeFormat('it-CH', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' });

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'style') n.style.cssText = attrs[k];
      else if (k === 'text') n.textContent = attrs[k];
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
  var NAVBTN = 'position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border:0;background:rgba(239,237,230,0.92);color:#15201B;cursor:pointer;display:flex;align-items:center;justify-content:center';

  function render(a) {
    var n = a.photos.length, idx = 0, open = false;
    var long = (a.text || '').length > 320;
    var date = a.date ? fmt.format(new Date(a.date + 'T12:00:00')).replace(/\./g, '').toUpperCase() : '';
    var place = a.place ? a.place.toUpperCase() + ' · ' : '';

    var text = el('p', { class: 'serif', style: 'margin:0;font-size:18px;line-height:1.6;white-space:pre-line;max-width:520px' });
    var toggle = long ? el('button', { type: 'button', class: 'card-link', style: 'background:none;border:0;border-bottom:2px solid #15201B;padding:0;color:#15201B;cursor:pointer' }) : null;
    function setText() {
      text.textContent = long && !open ? a.text.slice(0, a.text.lastIndexOf(' ', 300)) + '…' : (a.text || '');
      if (toggle) toggle.textContent = open ? 'Riduci' : 'Leggi tutto';
    }
    if (toggle) toggle.addEventListener('click', function () { open = !open; setText(); });
    setText();

    var left = el('div', { style: 'flex:1 1 360px;display:flex;flex-direction:column;gap:16px' }, [
      el('div', { class: 'mono', style: 'font-size:13px;letter-spacing:0.14em;color:var(--accent)', text: date }),
      el('h2', { class: 'disp', style: 'margin:0;font-size:60px', text: a.title }),
      el('div', { class: 'mono', style: 'font-size:13px;letter-spacing:0.1em;opacity:0.75', text: place + n + ' FOTO' }),
      a.text ? text : null,
      toggle ? el('div', null, [toggle]) : null,
      a.link ? el('div', null, [el('a', { class: 'card-link', href: a.link, style: 'color:#15201B', text: 'Dettagli della gita ↗' })]) : null
    ]);

    var img = el('img', { class: 'f-photo', alt: '', decoding: 'async' });
    var counter = el('span', { class: 'mono', style: 'position:absolute;right:12px;bottom:12px;background:#15201B;color:#EFEDE6;font-size:12px;padding:4px 8px' });
    var thumbs = [];
    function show(k) {
      idx = (k + n) % n;
      img.src = a.photos[idx].large;
      img.alt = a.title + ' — foto ' + (idx + 1) + ' di ' + n;
      counter.textContent = (idx + 1) + ' / ' + n;
      thumbs.forEach(function (t, i) { t.classList.toggle('sel', i === idx); t.setAttribute('aria-current', i === idx ? 'true' : 'false'); });
    }
    var frame = el('div', { style: 'position:relative;aspect-ratio:3/2;background:#2A332E' }, [
      img,
      n > 1 ? el('button', { type: 'button', 'aria-label': 'Foto precedente', style: NAVBTN + ';left:12px', onclick: function () { show(idx - 1); } }, [arrow(-1)]) : null,
      n > 1 ? el('button', { type: 'button', 'aria-label': 'Foto successiva', style: NAVBTN + ';right:12px', onclick: function () { show(idx + 1); } }, [arrow(1)]) : null,
      counter
    ]);
    var grid = el('div', { style: 'display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:8px' });
    a.photos.forEach(function (p, k) {
      var b = el('button', { type: 'button', class: 'th tone' + (k % 6), 'aria-label': 'Mostra foto ' + (k + 1), onclick: function () { show(k); } },
        [el('img', { src: p.thumb, alt: '', loading: 'lazy', decoding: 'async' })]);
      thumbs.push(b); grid.appendChild(b);
    });
    var right = el('div', { style: 'flex:1.5 1 560px;display:flex;flex-direction:column;gap:12px' }, [frame, grid]);
    show(0);
    return el('article', { style: 'display:flex;gap:48px;padding:48px 0 56px;border-top:2px solid #15201B;flex-wrap:wrap' }, [left, right]);
  }

  function next() {
    albums.slice(shown, shown + PAGE).forEach(function (a) { root.appendChild(render(a)); });
    shown += PAGE;
    if (more) more.hidden = shown >= albums.length;
  }

  fetch('data/foto.json', { cache: 'no-cache' })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (data) {
      albums = (data.albums || []).filter(function (a) { return a.photos && a.photos.length; });
      root.textContent = '';
      if (!albums.length) { root.appendChild(el('p', { class: 'serif', style: 'padding:48px 0;font-size:18px', text: 'Nessuna foto pubblicata di recente.' })); return; }
      next();
    })
    .catch(function () {
      root.textContent = '';
      root.appendChild(el('p', { class: 'serif', style: 'padding:48px 0;font-size:18px', text: 'Le foto non sono disponibili al momento. Puoi consultarle sul portale Droptour.' }));
    });
  if (more) more.addEventListener('click', next);
})();
