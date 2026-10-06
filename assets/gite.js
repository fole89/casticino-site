// CAS Ticino - programma gite (gite.html) e dettaglio di una gita (gita.html?id=<numero Droptour>).
// gite.html: legge le gite in tempo reale dall'interfaccia pubblica di Droptour (#gite[data-api]) e le ridisegna con
// lo stesso markup di gita_html() in scripts/redesign/pages.py: tenerli allineati. Se Droptour non risponde usa la
// copia di data/gite.json (#gite[data-copia]); senza JavaScript resta l'elenco generato. Filtri per gruppo e tipo,
// anche da indirizzo: gite.html?gruppo=Giovani&tipo=COR
// gita.html: intestazione e stato dall'elenco, testi (percorso, ritrovo, costi…) dalla scheda Droptour (getItem),
// ridotti a testo semplice; finché Droptour non risponde si mostra la scheda salvata in data/gite.json. L'iscrizione resta su Droptour (pulsante «Iscriviti su Droptour»).
// Dei capigita si prende solo il nome: l'interfaccia contiene anche dati che il sito non deve mostrare.
// Le stesse pagine esistono in de/ e en/: i testi della pagina vengono da TESTI (lingua di <html lang>), le gite
// (titoli, tipi, dettagli della scheda Droptour) restano in italiano. Testi allineati con gita_html() in pages.py.
(function () {
  var box = document.getElementById('gite');
  var dett = document.getElementById('gita');
  if (!box && !dett) return;
  var filtri = document.getElementById('gite-filtri');
  var stato = document.getElementById('gite-stato');
  var TESTI = {
    it: {
      giorni: ['dom', 'lun', 'mar', 'mer', 'gio', 'ven', 'sab'],
      giorniLunghi: ['domenica', 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato'],
      mesi: ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'],
      mesiBrevi: ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'],
      impegno: { A: 'poco impegnativo', B: 'abbastanza impegnativo', C: 'impegnativo', D: 'molto impegnativo' },
      gruppi: {},
      breve: function (g, m) { return g + ' ' + m; },
      lungo: function (gs, g, m, a) { return gs + ' ' + g + ' ' + m + ' ' + a; },
      fino: function (g, m) { return 'fino ' + ([1, 8, 11].indexOf(g) !== -1 ? 'all’' : 'al ') + g + ' ' + m; },
      annullata: 'Annullata', completa: 'Completa', senza: 'Senza iscrizione online', dal: 'Iscrizioni dal ',
      chiuse: 'Iscrizioni chiuse', aperte: 'Iscrizioni aperte', impegnoT: 'Impegno', difficolta: 'Difficoltà',
      capogita: 'Capogita', capigita: 'Capigita', iscritti: ' iscritti', iscrizione: 'Iscrizione',
      dettagli: 'Dettagli', dettagliIscr: 'Dettagli e iscrizione', tuttiGruppi: 'Tutti i gruppi', tuttiTipi: 'Tutti i tipi',
      gita: ' gita', gite: ' gite', titolo: ' | Programma gite | CAS Ticino', perTutti: 'Per tutti', data: 'Data',
      iscrittiT: 'Iscritti', onlineDal: 'Online', dalT: ' da ', alT: ' a ', soloDalT: ' da ', soloAlT: ' fino a ', laGita: 'La gita',
      caricamento: 'Caricamento dei dettagli da Droptour…',
      nonDisp: 'I dettagli della gita non sono disponibili in questo momento: li trovi su Droptour.',
      iscriviti: 'Iscriviti su Droptour', apri: 'Apri su Droptour', programma: 'Programma gite', cerca: 'Cerca su Droptour',
      nonTrovata: 'Gita non trovata', nonTrovataTesto: 'La gita non è (più) nel programma: forse è già passata, oppure il link non è corretto.'
    },
    de: {
      giorni: ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'],
      giorniLunghi: ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'],
      mesi: ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
      mesiBrevi: ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sept.', 'Okt.', 'Nov.', 'Dez.'],
      impegno: { A: 'wenig anspruchsvoll', B: 'ziemlich anspruchsvoll', C: 'anspruchsvoll', D: 'sehr anspruchsvoll' },
      gruppi: { Tutti: 'Alle', Attivi: 'Aktive', Giovani: 'Jugend', Seniori: 'Senioren', Soccorso: 'Bergrettung', Monitori: 'Leitende' },
      breve: function (g, m) { return g + '. ' + m; },
      lungo: function (gs, g, m, a) { return gs + ', ' + g + '. ' + m + ' ' + a; },
      fino: function (g, m) { return 'bis ' + g + '. ' + m; },
      annullata: 'Abgesagt', completa: 'Ausgebucht', senza: 'Ohne Online-Anmeldung', dal: 'Anmeldung ab ',
      chiuse: 'Anmeldung geschlossen', aperte: 'Anmeldung offen', impegnoT: 'Kondition', difficolta: 'Technik',
      capogita: 'Leitung', capigita: 'Leitung', iscritti: ' Angemeldete', iscrizione: 'Anmeldung',
      dettagli: 'Details', dettagliIscr: 'Details und Anmeldung', tuttiGruppi: 'Alle Gruppen', tuttiTipi: 'Alle Arten',
      gita: ' Tour', gite: ' Touren', titolo: ' | Tourenprogramm | CAS Ticino', perTutti: 'Für alle', data: 'Datum',
      iscrittiT: 'Angemeldet', onlineDal: 'Online', dalT: ' von ', alT: ' bis ', soloDalT: ' ab ', soloAlT: ' bis ', laGita: 'Die Tour (italienisch)',
      caricamento: 'Details werden von Droptour geladen…',
      nonDisp: 'Die Details der Tour sind im Moment nicht verfügbar: Sie finden sie auf Droptour.',
      iscriviti: 'Auf Droptour anmelden', apri: 'Auf Droptour öffnen', programma: 'Tourenprogramm', cerca: 'Auf Droptour suchen',
      nonTrovata: 'Tour nicht gefunden', nonTrovataTesto: 'Die Tour ist nicht (mehr) im Programm: Vielleicht ist sie schon vorbei, oder der Link stimmt nicht.'
    },
    en: {
      giorni: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      giorniLunghi: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      mesi: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      mesiBrevi: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      impegno: { A: 'easy', B: 'fairly demanding', C: 'demanding', D: 'very demanding' },
      gruppi: { Tutti: 'All', Attivi: 'Active members', Giovani: 'Youth', Seniori: 'Seniors', Soccorso: 'Mountain rescue', Monitori: 'Instructors' },
      breve: function (g, m) { return g + ' ' + m; },
      lungo: function (gs, g, m, a) { return gs + ' ' + g + ' ' + m + ' ' + a; },
      fino: function (g, m) { return 'to ' + g + ' ' + m; },
      annullata: 'Cancelled', completa: 'Full', senza: 'No online registration', dal: 'Registration from ',
      chiuse: 'Registration closed', aperte: 'Registration open', impegnoT: 'Fitness', difficolta: 'Difficulty',
      capogita: 'Leader', capigita: 'Leaders', iscritti: ' registered', iscrizione: 'Registration',
      dettagli: 'Details', dettagliIscr: 'Details and registration', tuttiGruppi: 'All groups', tuttiTipi: 'All types',
      gita: ' trip', gite: ' trips', titolo: ' | Trip programme | CAS Ticino', perTutti: 'For everyone', data: 'Date',
      iscrittiT: 'Registered', onlineDal: 'Online', dalT: ' from ', alT: ' to ', soloDalT: ' from ', soloAlT: ' until ', laGita: 'The trip (in Italian)',
      caricamento: 'Loading the details from Droptour…',
      nonDisp: 'The trip details are not available at the moment: you can find them on Droptour.',
      iscriviti: 'Register on Droptour', apri: 'Open on Droptour', programma: 'Trip programme', cerca: 'Search on Droptour',
      nonTrovata: 'Trip not found', nonTrovataTesto: 'The trip is not (or no longer) in the programme: it may be over, or the link is not correct.'
    }
  };
  var LINGUA = (document.documentElement.lang || 'it').slice(0, 2);
  var TX = TESTI[LINGUA] || TESTI.it;
  // tipi di gita (category di Droptour, sempre in italiano): tradotti dal codice; un codice nuovo resta in italiano.
  // Tenere allineato con TIPI_GITA_L in pages.py
  var TIPI = {
    de: { ALP: 'Hochtour', ARR: 'Klettern', COR: 'Ausbildungskurs', CUL: 'Kultur', ESC: 'Wandern', EVE: 'Anlass', FER: 'Klettersteig',
          MTB: 'Mountainbike', RAC: 'Schneeschuhtour', SA: 'Skitour', SOC: 'Bergrettung' },
    en: { ALP: 'Mountaineering', ARR: 'Climbing', COR: 'Training course', CUL: 'Culture', ESC: 'Hiking', EVE: 'Event', FER: 'Via ferrata',
          MTB: 'Mountain biking', RAC: 'Snowshoeing', SA: 'Ski touring', SOC: 'Mountain rescue' }
  }[LINGUA] || {};
  function nomeTipo(g) { return TIPI[g.sigla] || g.tipo; }
  var GIORNI = TX.giorni, MESI = TX.mesi, MESI_BREVI = TX.mesiBrevi, IMPEGNO = TX.impegno;
  function nomeGruppo(x) { return TX.gruppi[x] || x; }
  var STATO = { '3': 'completa', '2': 'annullata' };
  var ORDINE_GRUPPI = ['Attivi', 'Giovani', 'Seniori', 'Soccorso', 'Monitori'];
  var scelta = { gruppi: '', tipo: '' };
  var gite = [];

  function esc(t) {
    return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; });
  }
  function testo(v) {
    // documento separato e inerte: niente immagini o script dal testo di Droptour
    var d = new DOMParser().parseFromString(String(v || '').replace(/<[^>]+>/g, ' '), 'text/html');
    return d.body.textContent.replace(/\s+/g, ' ').trim();
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

  function breve(iso) { var d = giorno(iso); return TX.breve(d.getDate(), MESI_BREVI[d.getMonth()]); }
  function statoGita(g, o) {
    if (g.stato === 'annullata') return ['annullata', TX.annullata];
    if (g.stato === 'completa') return ['completa', TX.completa];
    if (!g.iscrizione) return ['', TX.senza];
    if (g.iscrizione_dal && o < g.iscrizione_dal) return ['', TX.dal + breve(g.iscrizione_dal)];
    if (g.iscrizione_al && o > g.iscrizione_al) return ['', TX.chiuse];
    return ['aperte', TX.aperte];
  }

  function gitaHtml(g, o) {
    var d1 = giorno(g.dal), gg = String(d1.getDate()), sotto = GIORNI[d1.getDay()];
    if (g.al && g.al !== g.dal) {
      var d2 = giorno(g.al);
      if (d2.getMonth() === d1.getMonth()) { gg += '–' + d2.getDate(); sotto += '–' + GIORNI[d2.getDay()]; }
      else sotto += ', ' + TX.fino(d2.getDate(), MESI_BREVI[d2.getMonth()]);
    }
    var st = statoGita(g, o), classe = st[0];
    var gruppi = g.gruppi.filter(function (x) { return x !== 'Tutti'; }).map(nomeGruppo);
    if (!gruppi.length) gruppi = [nomeGruppo('Tutti')];
    var tipo = [esc(nomeTipo(g)), esc(gruppi.join(', '))].filter(function (x, i, a) { return x && a.indexOf(x) === i; }).join(' · ');
    var meta = '';
    if (g.cond) meta += '<span title="' + (IMPEGNO[g.cond] || '') + '">' + TX.impegnoT + ' ' + esc(g.cond) + '</span>';
    if (g.tecn) meta += '<span>' + TX.difficolta + ' ' + esc(g.tecn) + '</span>';
    if (g.capigita.length) meta += '<span>' + (g.capigita.length > 1 ? TX.capigita : TX.capogita) + ': ' + esc(g.capigita.join(', ')) + '</span>';
    var posti = g.posti ? g.iscritti + '/' + g.posti + TX.iscritti : g.iscritti ? g.iscritti + TX.iscritti : '';
    var modalita = g.modalita && classe !== 'annullata'
      ? '<span class="gita-nota">' + TX.iscrizione + (LINGUA === 'it' && g.modalita.indexOf('tramite') === 0 ? ' ' : ': ') + esc(g.modalita) + '</span>' : '';
    return '<article class="gita' + (classe === 'annullata' ? ' gita--annullata' : '') + '" id="gita-' + esc(g.id) + '" data-fine="' + esc(g.al || g.dal) + '" data-gruppi="' + esc(g.gruppi.join(' ')) + '" data-tipo="' + esc(g.sigla) + '">' +
      '<p class="gita-data"><span class="gita-giorno num">' + gg + '</span><span class="gita-sotto">' + sotto + '</span></p>' +
      '<div class="gita-corpo"><p class="gita-tipo">' + tipo + '</p>' +
      '<h3 class="gita-titolo"><a href="gita.html?id=' + esc(g.id) + '"' + (LINGUA === 'it' ? '' : ' lang="it"') + '>' + esc(g.titolo) + '</a></h3>' +
      (meta ? '<p class="gita-meta">' + meta + '</p>' : '') + '</div>' +
      '<div class="gita-stato"><span class="stato' + (classe ? ' stato--' + classe : '') + '">' + st[1] + '</span>' +
      (posti ? '<span class="gita-posti num">' + posti + '</span>' : '') + modalita +
      '<a class="link gita-link" href="gita.html?id=' + esc(g.id) + '">' + (classe === 'annullata' || !g.iscrizione ? TX.dettagli : TX.dettagliIscr) +
        '<span class="visually-hidden">: <span' + (LINGUA === 'it' ? '' : ' lang="it"') + '>' + esc(g.titolo) + '</span></span></a></div></article>';
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

  // bottoni (schermo largo) e menu a tendina (telefono) con le stesse voci
  function pulsanti(campo, voci, tutti) {
    var bar = filtri.querySelector('.filtro[data-campo="' + campo + '"]');
    bar.innerHTML = '<button type="button" data-valore="" aria-pressed="' + (!scelta[campo]) + '">' + tutti + '</button>' +
      voci.map(function (v) {
        return '<button type="button" data-valore="' + esc(v[0]) + '" aria-pressed="' + (scelta[campo] === v[0]) + '">' + esc(v[1]) +
          ' <span class="num">' + v[2] + '</span></button>';
      }).join('');
    var sel = filtri.querySelector('select[data-campo="' + campo + '"]');
    sel.innerHTML = '<option value="">' + tutti + '</option>' +
      voci.map(function (v) { return '<option value="' + esc(v[0]) + '">' + esc(v[1]) + ' (' + v[2] + ')</option>'; }).join('');
    sel.value = scelta[campo];
  }

  function scegli(campo, valore) {
    scelta[campo] = valore;
    Array.prototype.forEach.call(filtri.querySelectorAll('.filtro[data-campo="' + campo + '"] button'), function (x) {
      x.setAttribute('aria-pressed', x.dataset.valore === valore ? 'true' : 'false');
    });
    filtri.querySelector('select[data-campo="' + campo + '"]').value = valore;
    applica();
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
      if (g.sigla) tipi[g.sigla] = nomeTipo(g) || g.sigla;
    });
    var nomiGruppi = Object.keys(gruppi).sort(function (a, b) {
      var ia = ORDINE_GRUPPI.indexOf(a), ib = ORDINE_GRUPPI.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib) || a.localeCompare(b);
    });
    if (scelta.gruppi && !gruppi[scelta.gruppi]) scelta.gruppi = '';
    if (scelta.tipo && !tipi[scelta.tipo]) scelta.tipo = '';
    pulsanti('gruppi', nomiGruppi.map(function (x) {
      return [x, nomeGruppo(x), future.filter(function (g) { return corrisponde(g, 'gruppi', x); }).length];
    }), TX.tuttiGruppi);
    pulsanti('tipo', Object.keys(tipi).sort(function (a, b) { return tipi[a].localeCompare(tipi[b]); }).map(function (x) {
      return [x, tipi[x], future.filter(function (g) { return corrisponde(g, 'tipo', x); }).length];
    }), TX.tuttiTipi);
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
    var attivi = [scelta.gruppi && nomeGruppo(scelta.gruppi), scelta.tipo && filtri.querySelector('.filtro[data-campo="tipo"] [aria-pressed="true"]').firstChild.textContent.trim()].filter(Boolean);
    stato.textContent = attivi.length ? n + (n === 1 ? TX.gita : TX.gite) + ': ' + attivi.join(', ') : '';
    var q = [];
    if (scelta.gruppi) q.push('gruppo=' + encodeURIComponent(scelta.gruppi));
    if (scelta.tipo) q.push('tipo=' + encodeURIComponent(scelta.tipo));
    try { history.replaceState(null, '', location.pathname + (q.length ? '?' + q.join('&') : '') + location.hash); } catch (e) {}
  }

  // ------------------------------------------------------------------ dettaglio (gita.html)
  var ETICHETTE_FUORI = ['Data', 'Gruppo', 'Tipo di attività', 'Tipo/Aggiunta', 'Iscrizione'];  // già nell'intestazione
  function lungo(iso, senzaAnno) {
    var d = giorno(iso), t = TX.lungo(TX.giorniLunghi[d.getDay()], d.getDate(), MESI[d.getMonth()], d.getFullYear());
    return senzaAnno ? t.slice(0, -(' ' + d.getFullYear()).length) : t;
  }

  // periodo d'iscrizione: «Online da domenica 1 novembre a mercoledì 2 dicembre 2026» (anno una volta sola se è lo stesso)
  function periodoIscrizione(dal, al) {
    if (dal && al) return TX.onlineDal + TX.dalT + lungo(dal, dal.slice(0, 4) === al.slice(0, 4)) + TX.alT + lungo(al);
    if (dal) return TX.onlineDal + TX.soloDalT + lungo(dal);
    if (al) return TX.onlineDal + TX.soloAlT + lungo(al);
    return TX.onlineDal;
  }

  function conLink(t) {  // testo già sicuro (esc) con gli indirizzi web resi cliccabili
    return t.replace(/\b(https?:\/\/[^\s<]+[^\s<.,;:)])/g, '<a href="$1" rel="noopener">$1</a>')
      .replace(/(^|[\s(])(www\.[^\s<]+[^\s<.,;:)])/g, '$1<a href="https://$2" rel="noopener">$2</a>');
  }

  // link della scheda da tenere (file allegati come i PDF, pagine esterne); quelli interni all'interfaccia Droptour
  // (scheda del capogita, scala delle esigenze) restano solo testo
  function linkBuono(a) {
    try {
      var u = new URL(a.getAttribute('href') || '', 'https://ssl.dropnet.ch/');
      return /^https?:$/.test(u.protocol) && u.pathname.indexOf('/api/') === -1 ? u.href : '';
    } catch (e) { return ''; }
  }

  function righeScheda(html) {  // [etichetta, HTML sicuro] dalla tabella #droptours-detail della scheda Droptour
    var doc = new DOMParser().parseFromString(html, 'text/html'), out = [];
    Array.prototype.forEach.call(doc.querySelectorAll('#droptours-detail tr'), function (tr) {
      var td = tr.querySelectorAll('td');
      if (td.length < 2) return;
      var et = td[0].textContent.replace(/\s+/g, ' ').trim().replace(/:$/, '');
      if (!et || /^Capogita/.test(et) || ETICHETTE_FUORI.indexOf(et) !== -1) return;
      var link = [];
      var t = Array.prototype.slice.call(td, 1).map(function (c) {
        Array.prototype.forEach.call(c.querySelectorAll('img, script, style'), function (x) { x.remove(); });
        // i link buoni diventano segnaposto (\u0001n\u0002), rimessi come <a> dopo aver ridotto il resto a testo
        Array.prototype.forEach.call(c.querySelectorAll('a[href]'), function (x) {
          var href = linkBuono(x), nome = x.textContent.replace(/\s+/g, ' ').trim().replace(/\.pdf$/i, '');  // «Gita 44 Castagnata.pdf» → «Gita 44 Castagnata»
          if (!href || !nome) return;
          link.push('<a href="' + esc(href) + '" rel="noopener">' + esc(nome) + '</a>');
          x.replaceWith('\u0001' + (link.length - 1) + '\u0002');
        });
        // gli a capo del sorgente sono solo spazi: contano solo i <br>
        var h = c.innerHTML.replace(/[\r\n]+/g, ' ').replace(/<br\s*\/?>/gi, '\n');
        return new DOMParser().parseFromString(h, 'text/html').body.textContent;
      }).join('\n').split('\n').map(function (r) { return r.replace(/[ \t ]+/g, ' ').trim(); })
        .filter(function (r) { return !/^(Cond|Tecn)\.$/.test(r); })  // esigenza senza valore
        .join('\n').replace(/\n{3,}/g, '\n\n').trim();
      if (!t) return;
      t = t.split(/(\u0001\d+\u0002)/).map(function (pezzo) {
        var m = /^\u0001(\d+)\u0002$/.exec(pezzo);
        return m ? link[+m[1]] : conLink(esc(pezzo));
      }).join('');
      out.push([et, t]);
    });
    return out;
  }

  function mostraGita(g, righe) {
    var o = oggi(), st = statoGita(g, o), classe = st[0];
    var gruppi = g.gruppi.filter(function (x) { return x !== 'Tutti'; }).map(nomeGruppo);
    document.title = g.titolo + TX.titolo;
    document.getElementById('page-h').textContent = g.titolo;
    if (LINGUA !== 'it') document.getElementById('page-h').lang = 'it';
    document.querySelector('.page-hero .lead').textContent = [nomeTipo(g), gruppi.length ? gruppi.join(', ') : TX.perTutti].filter(Boolean).join(' · ');
    var crumb = document.querySelector('.crumbs [aria-current]');
    if (crumb) crumb.textContent = g.titolo;
    window.dispatchEvent(new Event('resize'));  // site.js riadatta il titolo lungo

    var quando = lungo(g.dal) + (g.al && g.al !== g.dal ? ' – ' + lungo(g.al) : '');
    var iscr = !g.iscrizione ? TX.senza
      : periodoIscrizione(g.iscrizione_dal, g.iscrizione_al);
    // a sinistra, nel riquadro «in breve»: data, capogita, iscritti (con barra dei posti) e iscrizione
    var chiave = [[TX.data, '<span class="gita-quando">' + esc(quando) + '</span>']];
    if (g.capigita.length) chiave.push([g.capigita.length > 1 ? TX.capigita : TX.capogita, esc(g.capigita.join(', '))]);
    if (g.posti || g.iscritti) {
      var pieno = g.posti ? Math.min(100, Math.round(g.iscritti / g.posti * 100)) : 0;
      chiave.push([TX.iscrittiT, '<span class="num">' + g.iscritti + (g.posti ? ' / ' + g.posti : '') + '</span>' +
        (g.posti ? '<span class="gita-barra" aria-hidden="true"><span style="width:' + pieno + '%"></span></span>' : '')]);
    }
    chiave.push([TX.iscrizione, esc(iscr)]);
    document.getElementById('gita-chiave').innerHTML = chiave.map(function (f) { return '<div><dt>' + f[0] + '</dt><dd>' + f[1] + '</dd></div>'; }).join('');

    // a destra: il resto della scheda Droptour
    var fatti = (righe || []).map(function (r) { return [esc(r[0]), '<span class="gita-testo">' + r[1] + '</span>']; });
    document.getElementById('gita-dati').innerHTML =
      (fatti.length ? '<h2 class="h3 gita-dati-h">' + TX.laGita + '</h2><dl class="facts"' + (LINGUA === 'it' ? '' : ' lang="it"') + '>' +
        fatti.map(function (f) { return '<dt>' + f[0] + '</dt><dd>' + f[1] + '</dd>'; }).join('') + '</dl>' : '') +
      (righe === undefined ? '<p class="small gita-avviso">' + TX.caricamento + '</p>'
        : righe ? '' : '<p class="small gita-avviso">' + TX.nonDisp + '</p>');

    document.getElementById('gita-stato').innerHTML = '<span class="stato' + (classe ? ' stato--' + classe : '') + '">' + st[1] + '</span>';
    // iscrizioni aperte: direttamente al modulo d'iscrizione di Droptour (tourFID = numero della gita)
    var modulo = dett.dataset.droptour + '?page=anmeldung&tourFID=' + encodeURIComponent(g.id);
    document.getElementById('gita-azioni').innerHTML = classe === 'aperte'
      ? '<a class="btn btn--primary" href="' + esc(modulo) + '">' + TX.iscriviti + ' <span class="arrow" aria-hidden="true">→</span></a>'
      : '<a class="btn btn--secondary" href="' + esc(g.link) + '">' + TX.apri + '</a>';
    document.querySelector('.gita-riepilogo').hidden = false;
  }

  function nonTrovata(id) {
    document.getElementById('page-h').textContent = TX.nonTrovata;
    document.querySelector('.page-hero .lead').textContent = TX.nonTrovataTesto;
    var link = dett.dataset.droptour + '?page=detail&touren_nummer=' + encodeURIComponent(id);
    document.getElementById('gita-azioni').innerHTML = '<a class="btn btn--primary" href="gite.html">' + TX.programma + '</a>' +
      (id ? '<a class="btn btn--secondary" href="' + esc(link) + '">' + TX.cerca + '</a>' : '');
    document.getElementById('gita-chiave').innerHTML = '';
    document.getElementById('gita-stato').innerHTML = '';
    document.getElementById('gita-dati').innerHTML = '';
    document.querySelector('.gita-riepilogo').hidden = false;
  }

  // gite già lette in tempo reale nella pagina del programma (sessionStorage, 10 minuti): il dettaglio parte subito
  var MEMO = 'casticino-gite';
  function ricorda(lista) { try { sessionStorage.setItem(MEMO, JSON.stringify({ t: Date.now(), gite: lista })); } catch (e) {} }
  function ricordate() {
    try { var m = JSON.parse(sessionStorage.getItem(MEMO)); return m && Date.now() - m.t < 600000 ? m.gite : null; } catch (e) { return null; }
  }

  function dettaglio() {
    var id = new URLSearchParams(location.search).get('id') || '';
    if (!/^\d+$/.test(id)) { nonTrovata(''); return; }
    // si mostra subito la gita dalla fonte più rapida (memoria, poi copia locale), poi si aggiorna: la scheda Droptour
    // (di solito ~0,5 s, a volte molto di più) sostituisce quella della copia locale (data/gite.json, «scheda», scritta
    // ogni mattina da scripts/update_gite.py), l'elenco in tempo reale (~1,5 s) aggiorna stato e iscritti.
    // Se dopo ATTESA ms la scheda non è arrivata e non c'è copia, si smette di dire «Caricamento…».
    var ATTESA = 8000;
    var g = null, righe, copia, finito = { vive: false, copia: false };
    function trova(lista) { return (lista || []).filter(function (x) { return x.id === id; })[0] || null; }
    function aggiorna(nuova) { if (nuova) g = nuova; if (g) mostraGita(g, righe !== undefined ? righe : copia); }
    function forseNonTrovata() { if (!g && finito.vive && finito.copia) nonTrovata(id); }

    aggiorna(trova(ricordate()));
    fetch(dett.dataset.copia).then(function (r) { return r.json(); })
      .then(function (d) {
        var c = trova(d.gite);
        if (c && c.scheda && c.scheda.length) copia = c.scheda;
        if (copia && righe === null) righe = copia;  // Droptour ha già rinunciato: meglio la copia che niente
        aggiorna(g ? null : c);
      })
      .catch(function () {})
      .then(function () { finito.copia = true; forseNonTrovata(); });
    fetch(dett.dataset.api)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) { var lista = daXml(new DOMParser().parseFromString(t, 'text/xml')); ricorda(lista); aggiorna(trova(lista)); })
      .catch(function () {})
      .then(function () { finito.vive = true; forseNonTrovata(); });
    fetch(dett.dataset.dettaglio + id)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(righeScheda)
      .catch(function () { return null; })
      .then(function (x) { if (x || righe === undefined) righe = x || copia || null; aggiorna(); });
    setTimeout(function () { if (righe === undefined) { righe = copia || null; aggiorna(); } }, ATTESA);
  }

  if (box) {
    // l'elenco nella pagina è di quando è stata generata (ogni mattina): le gite già passate si tolgono subito
    var o0 = oggi();
    Array.prototype.forEach.call(box.querySelectorAll('.gita[data-fine]'), function (el) { if (el.dataset.fine < o0) el.remove(); });
    Array.prototype.forEach.call(box.querySelectorAll('.gite-mese'), function (m) { if (!m.querySelector('.gita')) m.remove(); });

    filtri.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-valore]');
      if (b) scegli(b.parentNode.dataset.campo, b.dataset.valore);
    });
    filtri.addEventListener('change', function (e) {
      if (e.target.matches('select[data-campo]')) scegli(e.target.dataset.campo, e.target.value);
    });

    // i filtri compaiono subito dalla fonte più rapida (memoria della sessione, poi copia locale) e si aggiornano
    // quando arrivano le gite in tempo reale da Droptour
    var vive = false, evidenziata = false;
    function pronto(lista, nuove) {
      gite = lista;
      if (nuove) disegna();
      costruisciFiltri();
      applica();
      if (location.hash && !evidenziata) {
        var t = document.getElementById(location.hash.slice(1));
        if (t) { evidenziata = true; t.classList.add('gita--evidenza'); t.scrollIntoView(); }
      }
    }

    var p = new URLSearchParams(location.search);
    scelta.gruppi = p.get('gruppo') || '';
    scelta.tipo = p.get('tipo') || '';

    var memo = ricordate();
    if (memo && memo.length) pronto(memo, true);
    else {
      // l'elenco generato viene dalla stessa copia: basta costruire i filtri (se Droptour non risponde si resta così)
      fetch(box.dataset.copia).then(function (r) { return r.json(); })
        .then(function (d) { if (!vive) pronto(d.gite || [], false); })
        .catch(function () {});
    }
    fetch(box.dataset.api)
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
      .then(function (t) {
        var lista = daXml(new DOMParser().parseFromString(t, 'text/xml'));
        if (!lista.length) throw new Error('vuoto');
        vive = true;
        ricorda(lista);
        pronto(lista, true);
      })
      .catch(function () {});
  } else {
    dettaglio();
  }
})();
