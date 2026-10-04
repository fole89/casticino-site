// CAS Ticino - programma gite (gite.html) e dettaglio di una gita (gita.html?id=<numero Droptour>).
// gite.html: legge le gite in tempo reale dall'interfaccia pubblica di Droptour (#gite[data-api]) e le ridisegna con
// lo stesso markup di gita_html() in scripts/redesign/pages.py: tenerli allineati. Se Droptour non risponde usa la
// copia di data/gite.json (#gite[data-copia]); senza JavaScript resta l'elenco generato. Filtri per gruppo e tipo,
// anche da indirizzo: gite.html?gruppo=Giovani&tipo=COR
// gita.html: intestazione e stato dall'elenco, testi (percorso, ritrovo, costi…) dalla scheda Droptour (getItem),
// ridotti a testo semplice. L'iscrizione resta su Droptour (pulsante «Iscriviti su Droptour»).
// Dei capigita si prende solo il nome: l'interfaccia contiene anche dati che il sito non deve mostrare.
(function () {
  var box = document.getElementById('gite');
  var dett = document.getElementById('gita');
  if (!box && !dett) return;
  var filtri = document.getElementById('gite-filtri');
  var stato = document.getElementById('gite-stato');
  var GIORNI = ['dom', 'lun', 'mar', 'mer', 'gio', 'ven', 'sab'];
  var MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
  var MESI_BREVI = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
  var IMPEGNO = { A: 'poco impegnativo', B: 'abbastanza impegnativo', C: 'impegnativo', D: 'molto impegnativo' };
  var STATO = { '3': 'completa', '2': 'annullata' };
  var ORDINE_GRUPPI = ['Attivi', 'Giovani', 'Seniori', 'Soccorso', 'Monitori'];
  var scelta = { gruppi: '', tipo: '' };
  var gite = [];

  function esc(t) {
    return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function testo(v) {
    var d = document.createElement('div');
    d.innerHTML = String(v || '').replace(/<[^>]+>/g, ' ');
    return d.textContent.replace(/\s+/g, ' ').trim();
  }
  function data(v) { return v && v.indexOf('0000') !== 0 ? v : ''; }
  function giorno(iso) { var p = iso.split('-'); return new Date(+p[0], p[1] - 1, +p[2]); }
  function oggi() {
    var d = new Date();
    return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2);
  }

  // stessa forma di data/gite.json (scripts/update_gite.py)
  function daXml(xml) {
    var items = xml.getElementsByTagName('item'), out = [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      if (it.getAttribute('type') !== 'tour') continue;
      var a = function (n) { return it.getAttribute(n) || ''; };
      var capi = [], ad = it.getElementsByTagName('address');
      for (var j = 0; j < ad.length; j++) {
        if ((ad[j].getAttribute('type') || '').indexOf('tour_guide') === 0) {
          var nome = testo((ad[j].getAttribute('fname') || '') + ' ' + (ad[j].getAttribute('lname') || ''));
          if (nome) capi.push(nome);
        }
      }
      if (!capi.length && a('author')) capi.push(testo(a('author')));
      out.push({
        id: a('id'), titolo: testo(a('name')), link: a('link'), dal: data(a('date_start')), al: data(a('date_end')),
        tipo: testo(a('category_description')), sigla: a('category'), gruppi: a('group').split('|').filter(Boolean),
        capigita: capi, cond: a('requirements_kond'), tecn: a('requirements_techn'), descrizione: testo(a('description')),
        iscrizione: a('register_type') !== '0', iscrizione_dal: data(a('register_start_date')), iscrizione_al: data(a('register_end_date')),
        modalita: testo(a('register_formalities')), iscritti: parseInt(a('participants_nr'), 10) || 0,
        posti: parseInt(a('participants_max'), 10) || 0, stato: STATO[a('tour_status')] || ''
      });
    }
    return out.sort(function (x, y) { return (x.dal + x.titolo).localeCompare(y.dal + y.titolo); });
  }

  function breve(iso) { var d = giorno(iso); return d.getDate() + ' ' + MESI_BREVI[d.getMonth()]; }
  function statoGita(g, o) {
    if (g.stato === 'annullata') return ['annullata', 'Annullata'];
    if (g.stato === 'completa') return ['completa', 'Completa'];
    if (!g.iscrizione) return ['', 'Senza iscrizione online'];
    if (g.iscrizione_dal && o < g.iscrizione_dal) return ['', 'Iscrizioni dal ' + breve(g.iscrizione_dal)];
    if (g.iscrizione_al && o > g.iscrizione_al) return ['', 'Iscrizioni chiuse'];
    return ['aperte', 'Iscrizioni aperte'];
  }

  function gitaHtml(g, o) {
    var d1 = giorno(g.dal), gg = String(d1.getDate()), sotto = GIORNI[d1.getDay()];
    if (g.al && g.al !== g.dal) {
      var d2 = giorno(g.al);
      if (d2.getMonth() === d1.getMonth()) { gg += '–' + d2.getDate(); sotto += '–' + GIORNI[d2.getDay()]; }
      else sotto += ', fino al ' + d2.getDate() + ' ' + MESI_BREVI[d2.getMonth()];
    }
    var st = statoGita(g, o), classe = st[0];
    var gruppi = g.gruppi.filter(function (x) { return x !== 'Tutti'; });
    if (!gruppi.length) gruppi = ['Tutti'];
    var tipo = [esc(g.tipo), esc(gruppi.join(', '))].filter(function (x, i, a) { return x && a.indexOf(x) === i; }).join(' · ');
    var meta = '';
    if (g.cond) meta += '<span title="' + (IMPEGNO[g.cond] || '') + '">Impegno ' + esc(g.cond) + '</span>';
    if (g.tecn) meta += '<span>Difficoltà ' + esc(g.tecn) + '</span>';
    if (g.capigita.length) meta += '<span>' + (g.capigita.length > 1 ? 'Capigita' : 'Capogita') + ': ' + esc(g.capigita.join(', ')) + '</span>';
    var posti = g.posti ? g.iscritti + '/' + g.posti + ' iscritti' : g.iscritti ? g.iscritti + ' iscritti' : '';
    var modalita = g.modalita && classe !== 'annullata'
      ? '<span class="gita-nota">Iscrizione' + (g.modalita.indexOf('tramite') === 0 ? ' ' : ': ') + esc(g.modalita) + '</span>' : '';
    return '<article class="gita' + (classe === 'annullata' ? ' gita--annullata' : '') + '" id="gita-' + esc(g.id) + '" data-gruppi="' + esc(g.gruppi.join(' ')) + '" data-tipo="' + esc(g.sigla) + '">' +
      '<p class="gita-data"><span class="gita-giorno num">' + gg + '</span><span class="gita-sotto">' + sotto + '</span></p>' +
      '<div class="gita-corpo"><p class="gita-tipo">' + tipo + '</p>' +
      '<h3 class="gita-titolo"><a href="gita.html?id=' + esc(g.id) + '">' + esc(g.titolo) + '</a></h3>' +
      (meta ? '<p class="gita-meta">' + meta + '</p>' : '') + '</div>' +
      '<div class="gita-stato"><span class="stato' + (classe ? ' stato--' + classe : '') + '">' + st[1] + '</span>' +
      (posti ? '<span class="gita-posti num">' + posti + '</span>' : '') + modalita +
      '<a class="link gita-link" href="gita.html?id=' + esc(g.id) + '">' + (classe === 'annullata' || !g.iscrizione ? 'Dettagli' : 'Dettagli e iscrizione') + '</a></div></article>';
  }

  function disegna() {
    var o = oggi(), html = '', mese = '';
    gite.filter(function (g) { return (g.al || g.dal) >= o; }).forEach(function (g) {
      var m = g.dal.slice(0, 7);
      if (m !== mese) {
        if (mese) html += '</div></section>';
        html += '<section class="gite-mese" aria-labelledby="mese-' + m + '"><h2 id="mese-' + m + '" class="h3">' +
          MESI[+m.slice(5) - 1].replace(/^./, function (c) { return c.toUpperCase(); }) + ' ' + m.slice(0, 4) + '</h2><div class="gite-righe">';
        mese = m;
      }
      html += gitaHtml(g, o);
    });
    if (mese) html += '</div></section>';
    if (html) box.innerHTML = html;
  }

  function pulsanti(campo, voci, tutti) {
    var bar = filtri.querySelector('[data-campo="' + campo + '"]');
    bar.innerHTML = '<button type="button" data-valore="" aria-pressed="' + (!scelta[campo]) + '">' + tutti + '</button>' +
      voci.map(function (v) {
        return '<button type="button" data-valore="' + esc(v[0]) + '" aria-pressed="' + (scelta[campo] === v[0]) + '">' + esc(v[1]) +
          ' <span class="num">' + v[2] + '</span></button>';
      }).join('');
  }

  function corrisponde(g, campo, v) {
    if (!v) return true;
    if (campo === 'tipo') return g.sigla === v;
    return g.gruppi.indexOf(v) !== -1 || g.gruppi.indexOf('Tutti') !== -1;
  }

  function costruisciFiltri() {
    var o = oggi(), future = gite.filter(function (g) { return (g.al || g.dal) >= o; });
    var gruppi = {}, tipi = {};
    future.forEach(function (g) {
      g.gruppi.forEach(function (x) { if (x !== 'Tutti') gruppi[x] = 1; });
      if (g.sigla) tipi[g.sigla] = g.tipo || g.sigla;
    });
    var nomiGruppi = Object.keys(gruppi).sort(function (a, b) {
      var ia = ORDINE_GRUPPI.indexOf(a), ib = ORDINE_GRUPPI.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib) || a.localeCompare(b);
    });
    if (scelta.gruppi && !gruppi[scelta.gruppi]) scelta.gruppi = '';
    if (scelta.tipo && !tipi[scelta.tipo]) scelta.tipo = '';
    pulsanti('gruppi', nomiGruppi.map(function (x) {
      return [x, x, future.filter(function (g) { return corrisponde(g, 'gruppi', x); }).length];
    }), 'Tutti i gruppi');
    pulsanti('tipo', Object.keys(tipi).sort(function (a, b) { return tipi[a].localeCompare(tipi[b]); }).map(function (x) {
      return [x, tipi[x], future.filter(function (g) { return corrisponde(g, 'tipo', x); }).length];
    }), 'Tutti i tipi');
    filtri.hidden = false;
  }

  function applica() {
    var perId = {}, n = 0;
    gite.forEach(function (g) { perId['gita-' + g.id] = g; });
    Array.prototype.forEach.call(box.querySelectorAll('.gita'), function (el) {
      var g = perId[el.id], ok = g && corrisponde(g, 'gruppi', scelta.gruppi) && corrisponde(g, 'tipo', scelta.tipo);
      el.hidden = !ok;
      if (ok) n++;
    });
    Array.prototype.forEach.call(box.querySelectorAll('.gite-mese'), function (m) {
      m.hidden = !m.querySelector('.gita:not([hidden])');
    });
    var attivi = [scelta.gruppi, scelta.tipo && filtri.querySelector('[data-campo="tipo"] [aria-pressed="true"]').firstChild.textContent.trim()].filter(Boolean);
    stato.textContent = attivi.length ? n + (n === 1 ? ' gita' : ' gite') + ': ' + attivi.join(', ') : '';
    var q = [];
    if (scelta.gruppi) q.push('gruppo=' + encodeURIComponent(scelta.gruppi));
    if (scelta.tipo) q.push('tipo=' + encodeURIComponent(scelta.tipo));
    try { history.replaceState(null, '', location.pathname + (q.length ? '?' + q.join('&') : '') + location.hash); } catch (e) {}
  }

  // ------------------------------------------------------------------ dettaglio (gita.html)
  var ETICHETTE_FUORI = ['Data', 'Gruppo', 'Tipo di attività', 'Tipo/Aggiunta', 'Iscrizione'];  // già nell'intestazione
  var GIORNI_LUNGHI = ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'];

  function lungo(iso) { var d = giorno(iso); return GIORNI_LUNGHI[d.getDay()] + ' ' + d.getDate() + ' ' + MESI[d.getMonth()] + ' ' + d.getFullYear(); }

  function conLink(t) {  // testo già sicuro (esc) con gli indirizzi web resi cliccabili
    return t.replace(/\b(https?:\/\/[^\s<]+[^\s<.,;:)])/g, '<a href="$1" rel="noopener">$1</a>')
      .replace(/(^|[\s(])(www\.[^\s<]+[^\s<.,;:)])/g, '$1<a href="https://$2" rel="noopener">$2</a>');
  }

  function righeScheda(html) {  // [etichetta, testo] dalla tabella #droptours-detail della scheda Droptour
    var doc = new DOMParser().parseFromString(html, 'text/html'), out = [];
    Array.prototype.forEach.call(doc.querySelectorAll('#droptours-detail tr'), function (tr) {
      var td = tr.querySelectorAll('td');
      if (td.length < 2) return;
      var et = td[0].textContent.replace(/\s+/g, ' ').trim().replace(/:$/, '');
      if (!et || /^Capogita/.test(et) || ETICHETTE_FUORI.indexOf(et) !== -1) return;
      var t = Array.prototype.slice.call(td, 1).map(function (c) {
        Array.prototype.forEach.call(c.querySelectorAll('img, script, style'), function (x) { x.remove(); });
        // gli a capo del sorgente sono solo spazi: contano solo i <br>
        var h = c.innerHTML.replace(/[\r\n]+/g, ' ').replace(/<br\s*\/?>/gi, '\n');
        return new DOMParser().parseFromString(h, 'text/html').body.textContent;
      }).join('\n').split('\n').map(function (r) { return r.replace(/[ \t ]+/g, ' ').trim(); })
        .filter(function (r) { return !/^(Cond|Tecn)\.$/.test(r); })  // esigenza senza valore
        .join('\n').replace(/\n{3,}/g, '\n\n').trim();
      if (t) out.push([et, t]);
    });
    return out;
  }

  function mostraGita(g, righe) {
    var o = oggi(), st = statoGita(g, o), classe = st[0];
    var gruppi = g.gruppi.filter(function (x) { return x !== 'Tutti'; });
    document.title = g.titolo + ' | Programma gite | CAS Ticino';
    document.getElementById('page-h').textContent = g.titolo;
    document.querySelector('.page-hero .lead').textContent = [g.tipo, gruppi.length ? gruppi.join(', ') : 'Per tutti'].filter(Boolean).join(' · ');
    var crumb = document.querySelector('.crumbs [aria-current]');
    if (crumb) crumb.textContent = g.titolo;
    window.dispatchEvent(new Event('resize'));  // site.js riadatta il titolo lungo

    var quando = lungo(g.dal) + (g.al && g.al !== g.dal ? ' – ' + lungo(g.al) : '');
    var iscr = !g.iscrizione ? 'Senza iscrizione online'
      : 'Online su Droptour' + (g.iscrizione_dal ? ' dal ' + lungo(g.iscrizione_dal) : '') + (g.iscrizione_al ? ' al ' + lungo(g.iscrizione_al) : '');
    var fatti = [['Data', esc(quando)]];
    if (g.capigita.length) fatti.push([g.capigita.length > 1 ? 'Capigita' : 'Capogita', esc(g.capigita.join(', '))]);
    fatti.push(['Iscrizione', esc(iscr)]);
    if (g.posti || g.iscritti) fatti.push(['Iscritti', '<span class="num">' + g.iscritti + (g.posti ? ' / ' + g.posti : '') + '</span>']);
    (righe || []).forEach(function (r) { fatti.push([esc(r[0]), '<span class="gita-testo">' + conLink(esc(r[1])) + '</span>']); });
    document.getElementById('gita-dati').innerHTML = '<dl class="facts">' +
      fatti.map(function (f) { return '<dt>' + f[0] + '</dt><dd>' + f[1] + '</dd>'; }).join('') + '</dl>' +
      (righe ? '' : '<p class="small gita-avviso">I dettagli della gita non sono disponibili in questo momento: li trovi su Droptour.</p>');

    document.getElementById('gita-stato').innerHTML = '<span class="stato' + (classe ? ' stato--' + classe : '') + '">' + st[1] + '</span>';
    var az = classe === 'aperte'
      ? '<a class="btn btn--primary" href="' + esc(g.link) + '">Iscriviti su Droptour <span class="arrow" aria-hidden="true">→</span></a>'
      : '<a class="btn btn--secondary" href="' + esc(g.link) + '">Apri su Droptour</a>';
    document.getElementById('gita-azioni').innerHTML = az + '<a class="btn btn--secondary" href="gite.html">Programma gite</a>';
  }

  function nonTrovata(id) {
    document.getElementById('page-h').textContent = 'Gita non trovata';
    document.querySelector('.page-hero .lead').textContent = 'La gita non è (più) nel programma: forse è già passata, oppure il link non è corretto.';
    var link = dett.dataset.droptour + '?page=detail&touren_nummer=' + encodeURIComponent(id);
    document.getElementById('gita-azioni').innerHTML = '<a class="btn btn--primary" href="gite.html">Programma gite</a>' +
      (id ? '<a class="btn btn--secondary" href="' + esc(link) + '">Cerca su Droptour</a>' : '');
    document.getElementById('gita-dati').innerHTML = '';
  }

  function dettaglio() {
    var id = new URLSearchParams(location.search).get('id') || '';
    if (!/^\d+$/.test(id)) { nonTrovata(''); return; }
    var elenco = fetch(dett.dataset.api)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) { return daXml(new DOMParser().parseFromString(t, 'text/xml')); })
      .catch(function () { return fetch(dett.dataset.copia).then(function (r) { return r.json(); }).then(function (d) { return d.gite || []; }); });
    var scheda = fetch(dett.dataset.dettaglio + id)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(righeScheda)
      .catch(function () { return null; });
    Promise.all([elenco, scheda]).then(function (x) {
      var g = (x[0] || []).filter(function (g) { return g.id === id; })[0];
      if (g) mostraGita(g, x[1]); else nonTrovata(id);
    }).catch(function () { nonTrovata(id); });
  }

  if (box) {
    filtri.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-valore]');
      if (!b) return;
      var campo = b.parentNode.dataset.campo;
      scelta[campo] = b.dataset.valore;
      Array.prototype.forEach.call(b.parentNode.querySelectorAll('button'), function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      applica();
    });

    function pronto(lista, vive) {
      gite = lista;
      if (vive) disegna();
      costruisciFiltri();
      applica();
      if (location.hash) {
        var t = document.getElementById(location.hash.slice(1));
        if (t) { t.classList.add('gita--evidenza'); t.scrollIntoView(); }
      }
    }

    var p = new URLSearchParams(location.search);
    scelta.gruppi = p.get('gruppo') || '';
    scelta.tipo = p.get('tipo') || '';

    fetch(box.dataset.api)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) {
        var lista = daXml(new DOMParser().parseFromString(t, 'text/xml'));
        if (!lista.length) throw new Error('vuoto');
        pronto(lista, true);
      })
      .catch(function () {
        // Droptour non risponde: si resta all'elenco generato e si prendono i dati per i filtri dalla copia
        fetch(box.dataset.copia).then(function (r) { return r.json(); })
          .then(function (d) { pronto(d.gite || [], false); })
          .catch(function () {});
      });
  } else {
    dettaglio();
  }
})();
