// CAS Ticino - pagina Cerca: cerca nel sito leggendo data/cerca.json (generato da scripts/redesign/pages.py)
(function () {
  var form = document.getElementById('cerca-form');
  var input = document.getElementById('cerca-q');
  var out = document.getElementById('cerca-risultati');
  var stato = document.getElementById('cerca-stato');
  if (!form || !input || !out) return;
  var indice = null, timer = null, MAX = 60;

  function norm(s) {
    return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  }
  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  // evidenzia i termini nel testo originale usando le posizioni trovate nel testo normalizzato
  // (la normalizzazione toglie solo gli accenti, quindi le posizioni coincidono carattere per carattere)
  function evidenzia(testo, termini) {
    var n = norm(testo), segni = [];
    termini.forEach(function (t) {
      var i = n.indexOf(t);
      while (i !== -1) { segni.push([i, i + t.length]); i = n.indexOf(t, i + t.length); }
    });
    if (!segni.length) return esc(testo);
    segni.sort(function (a, b) { return a[0] - b[0]; });
    var html = '', pos = 0;
    segni.forEach(function (s) {
      if (s[0] < pos) return;
      html += esc(testo.slice(pos, s[0])) + '<mark>' + esc(testo.slice(s[0], s[1])) + '</mark>';
      pos = s[1];
    });
    return html + esc(testo.slice(pos));
  }
  function estratto(testo, termini) {
    var n = norm(testo), i = -1;
    termini.forEach(function (t) { var k = n.indexOf(t); if (k !== -1 && (i === -1 || k < i)) i = k; });
    if (i === -1) return testo.slice(0, 180) + (testo.length > 180 ? '…' : '');
    var da = Math.max(0, i - 70), a = Math.min(testo.length, i + 130);
    if (da > 0) da = testo.indexOf(' ', da) + 1 || da;
    return (da > 0 ? '…' : '') + testo.slice(da, a) + (a < testo.length ? '…' : '');
  }

  function cerca(q) {
    var termini = norm(q).split(/[^a-z0-9]+/).filter(function (t) { return t.length > 1; });
    if (!termini.length) { out.textContent = ''; stato.textContent = ''; return; }
    var trovati = [];
    indice.forEach(function (e) {
      var punti = 0;
      for (var k = 0; k < termini.length; k++) {
        var t = termini[k], inTitolo = e._t.indexOf(t), inTesto = e._x.indexOf(t);
        if (inTitolo === -1 && inTesto === -1) return;  // tutti i termini devono esserci
        if (inTitolo !== -1) punti += (inTitolo === 0 || e._t.charAt(inTitolo - 1) === ' ') ? 12 : 8;
        if (inTesto !== -1) punti += Math.min(5, e._x.split(t).length - 1);
      }
      var frase = termini.join(' ');
      if (e._t === frase) punti += 20;                 // titolo identico alla ricerca
      else if (e._t.indexOf(frase) === 0) punti += 6;  // titolo che comincia con la ricerca
      trovati.push({ e: e, p: punti });
    });
    trovati.sort(function (a, b) { return b.p - a.p || (b.e.d || '').localeCompare(a.e.d || ''); });
    stato.textContent = trovati.length ? (trovati.length === 1 ? '1 risultato' : trovati.length + ' risultati') + ' per «' + q.trim() + '»'
                                       : 'Nessun risultato per «' + q.trim() + '». Prova con parole diverse o più brevi.';
    out.innerHTML = trovati.slice(0, MAX).map(function (r) {
      var e = r.e;
      return '<li class="cerca-item"><a href="' + esc(e.u) + '">' +
        '<span class="cerca-meta"><span class="cerca-tipo">' + esc(e.k) + '</span>' + (e.dt ? '<span>' + esc(e.dt) + '</span>' : '') + '</span>' +
        '<strong>' + evidenzia(e.t, termini) + '</strong>' +
        (e.x ? '<span class="cerca-estratto">' + evidenzia(estratto(e.x, termini), termini) + '</span>' : '') +
        '</a></li>';
    }).join('');
  }

  function aggiorna() {
    var q = input.value;
    var url = new URL(location.href);
    if (q.trim()) url.searchParams.set('q', q); else url.searchParams.delete('q');
    history.replaceState(null, '', url);
    if (indice) cerca(q);
  }

  form.addEventListener('submit', function (ev) { ev.preventDefault(); aggiorna(); });
  input.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(aggiorna, 150); });
  input.value = new URLSearchParams(location.search).get('q') || '';

  stato.textContent = 'Caricamento…';
  fetch(form.getAttribute('data-indice'))
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (dati) {
      indice = dati.voci.map(function (e) { e._t = norm(e.t); e._x = norm(e.x); return e; });
      stato.textContent = '';
      if (input.value.trim()) cerca(input.value);
    })
    .catch(function () { stato.textContent = 'La ricerca non è disponibile al momento.'; });
})();
