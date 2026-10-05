// CAS Ticino - modulo del noleggio materiale (noleggio.html, de/, en/): con le date scelte chiede al servizio
// (form#nol[data-api], scripts/noleggio/worker.js) quanto materiale è libero, poi invia la richiesta.
// Articoli e nomi nella lingua della pagina in #nol-dati (da data/noleggio-inventario.json, scritti da pages.py).
// Cloudflare Turnstile si carica solo quando si inizia a compilare il modulo. Stili in site.css, blocco «noleggio».
(function () {
  var form = document.getElementById('nol');
  var datiEl = document.getElementById('nol-dati');
  if (!form || !datiEl || !window.fetch) return;
  var API = form.dataset.api.replace(/\/?$/, '/');
  var MAX_GIORNI = Number(form.dataset.maxGiorni) || 30;
  var gruppi = JSON.parse(datiEl.textContent);
  var LINGUA = (document.documentElement.lang || 'it').slice(0, 2);
  var TX = {
    it: {
      giorni: function (n) { return n === 1 ? '1 giorno' : n + ' giorni'; },
      carico: 'Controllo cosa è libero…', liberi: function (n) { return n === 1 ? '1 libero' : n + ' liberi'; },
      esaurito: 'occupato', taglia: 'Taglia', giorno: 'al giorno', quantita: 'Quantità', nessuno: 'Per queste date non c’è materiale libero.',
      totale: function (t, g) { return 'Totale indicativo: Fr. ' + t + '.– per ' + g + ', da pagare alla riconsegna.'; },
      scegli: 'Scegli almeno un articolo.',
      ok: function (m) { return 'Richiesta inviata. Ti abbiamo mandato una ricevuta a ' + m + ': controlliamo la disponibilità e ti scriviamo la conferma.'; },
      nuova: 'Nuova richiesta',
      errori: {
        date: 'Indica il primo e l’ultimo giorno.', ordine: 'L’ultimo giorno viene prima del primo.',
        passato: 'Si può chiedere il materiale a partire da domani.', lontano: 'Si può prenotare al massimo un anno prima.',
        durata: 'Il noleggio può durare al massimo ' + MAX_GIORNI + ' giorni.',
        nome: 'Scrivi nome e cognome.', email: 'Controlla l’indirizzo e-mail.', telefono: 'Controlla il numero di telefono.',
        materiale: 'Scegli almeno un articolo.', verifica: 'Conferma il controllo «non sono un robot» qui sopra e riprova.',
        esaurito: 'Nel frattempo qualcuno ha prenotato una parte del materiale: controlla le quantità e riprova.',
        rete: 'Il servizio non risponde.'
      },
      alt: function (m) { return ' Riprova più tardi o scrivi a ' + m + '.'; }
    },
    de: {
      giorni: function (n) { return n === 1 ? '1 Tag' : n + ' Tage'; },
      carico: 'Freies Material wird geprüft…', liberi: function (n) { return n + ' frei'; },
      esaurito: 'besetzt', taglia: 'Grösse', giorno: 'pro Tag', quantita: 'Anzahl', nessuno: 'Für diese Daten ist kein Material frei.',
      totale: function (t, g) { return 'Total ungefähr: Fr. ' + t + '.– für ' + g + ', zu bezahlen bei der Rückgabe.'; },
      scegli: 'Wählen Sie mindestens einen Artikel.',
      ok: function (m) { return 'Anfrage gesendet. Wir haben Ihnen eine Empfangsbestätigung an ' + m + ' geschickt: Wir prüfen die Verfügbarkeit und senden Ihnen die Bestätigung.'; },
      nuova: 'Neue Anfrage',
      errori: {
        date: 'Geben Sie den ersten und den letzten Tag an.', ordine: 'Der letzte Tag liegt vor dem ersten.',
        passato: 'Material kann ab morgen angefragt werden.', lontano: 'Reservationen sind höchstens ein Jahr im Voraus möglich.',
        durata: 'Die Miete dauert höchstens ' + MAX_GIORNI + ' Tage.',
        nome: 'Geben Sie Vor- und Nachnamen an.', email: 'Prüfen Sie die E-Mail-Adresse.', telefono: 'Prüfen Sie die Telefonnummer.',
        materiale: 'Wählen Sie mindestens einen Artikel.', verifica: 'Bestätigen Sie oben die Prüfung «Ich bin kein Roboter» und versuchen Sie es nochmals.',
        esaurito: 'Inzwischen wurde ein Teil des Materials reserviert: Prüfen Sie die Anzahl und versuchen Sie es nochmals.',
        rete: 'Der Dienst antwortet nicht.'
      },
      alt: function (m) { return ' Versuchen Sie es später nochmals oder schreiben Sie an ' + m + '.'; }
    },
    en: {
      giorni: function (n) { return n === 1 ? '1 day' : n + ' days'; },
      carico: 'Checking what is free…', liberi: function (n) { return n + ' free'; },
      esaurito: 'taken', taglia: 'Size', giorno: 'per day', quantita: 'Quantity', nessuno: 'No equipment is free for these dates.',
      totale: function (t, g) { return 'Approximate total: CHF ' + t + ' for ' + g + ', payable on return.'; },
      scegli: 'Choose at least one item.',
      ok: function (m) { return 'Request sent. We have e-mailed a receipt to ' + m + ': we will check availability and send you the confirmation.'; },
      nuova: 'New request',
      errori: {
        date: 'Enter the first and the last day.', ordine: 'The last day is before the first.',
        passato: 'Equipment can be requested from tomorrow.', lontano: 'Bookings can be made at most one year ahead.',
        durata: 'A hire can last at most ' + MAX_GIORNI + ' days.',
        nome: 'Enter your full name.', email: 'Check the e-mail address.', telefono: 'Check the phone number.',
        materiale: 'Choose at least one item.', verifica: 'Complete the «I am not a robot» check above and try again.',
        esaurito: 'Meanwhile part of the equipment has been booked: check the quantities and try again.',
        rete: 'The service is not responding.'
      },
      alt: function (m) { return ' Try again later or write to ' + m + '.'; }
    }
  };
  if (!TX[LINGUA]) LINGUA = 'it';
  var T = TX[LINGUA];
  var alt = document.getElementById('nol-alt');
  var mailLink = alt && alt.querySelector('a[href^="mailto:"]');
  var MAIL = mailLink ? mailLink.textContent : '';
  var elArticoli = document.getElementById('nol-articoli');
  var elGiorni = document.getElementById('nol-giorni');
  var elTotale = document.getElementById('nol-totale');
  var elEsito = document.getElementById('nol-esito');
  var dal = form.elements.dal, al = form.elements.al;
  var scelte = {};        // "casco" / "imbracatura:M" → quantità scelta
  var disponibili = null; // dal servizio: chiave → [a magazzino, liberi]
  var giorni = 0, token = '', widget = null;

  alt.hidden = true;
  form.hidden = false;

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') n.textContent = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return n;
  }

  // date in AAAA-MM-GG, nel fuso del browser
  function iso(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function piu(s, n) { var p = s.split('-'); return iso(new Date(+p[0], p[1] - 1, +p[2] + n)); }
  function conta(a, b) { var x = a.split('-'), y = b.split('-'); return Math.round((Date.UTC(y[0], y[1] - 1, y[2]) - Date.UTC(x[0], x[1] - 1, x[2])) / 864e5) + 1; }
  var domani = piu(iso(new Date()), 1);
  dal.min = domani; dal.max = piu(domani, 364);
  al.min = domani;

  function messaggio(testo, errore) {
    elEsito.textContent = testo;
    elEsito.classList.toggle('is-errore', !!errore);
  }

  // ------------------------------------------------------------ date e disponibilità
  var attesa = 0;
  function dateCambiate() {
    if (dal.value) { al.min = dal.value; al.max = piu(dal.value, MAX_GIORNI - 1); if (!al.value || al.value < dal.value) al.value = dal.value; }
    if (!dal.value || !al.value) return;
    if (al.value < dal.value) { elGiorni.textContent = T.errori.ordine; return; }
    giorni = conta(dal.value, al.value);
    if (giorni > MAX_GIORNI) { elGiorni.textContent = T.errori.durata; return; }
    elGiorni.textContent = T.giorni(giorni);
    caricaDisponibili();
  }

  function caricaDisponibili() {
    var n = ++attesa;
    elArticoli.setAttribute('aria-busy', 'true');
    if (!disponibili) elArticoli.replaceChildren(el('p', { 'class': 'small', text: T.carico }));
    fetch(API + 'disponibilita?dal=' + dal.value + '&al=' + al.value)
      .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw d; return d; }); })
      .then(function (d) { if (n === attesa) { disponibili = d.disponibili; disegna(); } })
      .catch(function (e) {
        if (n !== attesa) return;
        var err = e && e.errore && T.errori[e.errore];
        elArticoli.replaceChildren(el('p', { 'class': 'nol-avviso', text: err || T.errori.rete + T.alt(MAIL) }));
        disponibili = null; totale();
      })
      .then(function () { if (n === attesa) elArticoli.removeAttribute('aria-busy'); });
  }

  function riga(chiave, etichetta, nomeCompleto, sotto) {
    var d = disponibili[chiave] || [0, 0];
    if (!d[0]) { delete scelte[chiave]; return null; }   // non a magazzino
    var liberi = d[1], max = liberi;
    if ((scelte[chiave] || 0) > max) scelte[chiave] = max;
    var sel = el('select', { 'aria-label': T.quantita + ': ' + nomeCompleto, 'data-chiave': chiave });
    for (var i = 0; i <= max; i++) sel.appendChild(el('option', { value: i, text: String(i) }));
    sel.value = scelte[chiave] || 0;
    if (!max) sel.disabled = true;
    return el('div', { 'class': 'nol-riga' + (sotto ? ' nol-riga--taglia' : '') + (max ? '' : ' is-occupato') }, [
      el('span', { 'class': 'nol-nome' }, etichetta),
      el('span', { 'class': 'nol-liberi' }, [liberi ? T.liberi(liberi) : T.esaurito]),
      sel
    ]);
  }

  function disegna() {
    var blocchi = [];
    gruppi.forEach(function (g) {
      var righe = [];
      g.articoli.forEach(function (a) {
        var prezzo = el('span', { 'class': 'nol-prezzo' }, ['Fr. ' + a.prezzo + '.– ' + T.giorno]);
        if (!a.taglie) {
          var r = riga(a.id, [a.nome, prezzo], a.nome);
          if (r) righe.push(r);
          return;
        }
        var sotto = a.taglie.map(function (t) {
          return riga(a.id + ':' + t, [T.taglia + ' ' + t], a.nome + ', ' + T.taglia.toLowerCase() + ' ' + t, true);
        }).filter(Boolean);
        if (sotto.length) righe.push(el('div', { 'class': 'nol-gruppo-taglie' }, [el('p', { 'class': 'nol-nome' }, [a.nome, prezzo])].concat(sotto)));
      });
      if (righe.length) blocchi.push(el('div', { 'class': 'nol-gruppo' }, [el('h4', { 'class': 'nol-gruppo-titolo', text: g.nome })].concat(righe)));
    });
    elArticoli.replaceChildren.apply(elArticoli, blocchi.length ? blocchi : [el('p', { 'class': 'nol-avviso', text: T.nessuno })]);
    totale();
  }

  function prezzoDi(chiave) {
    var id = chiave.split(':')[0], p = 0;
    gruppi.forEach(function (g) { g.articoli.forEach(function (a) { if (a.id === id) p = a.prezzo; }); });
    return p;
  }

  function totale() {
    var t = 0, n = 0;
    Object.keys(scelte).forEach(function (k) { if (scelte[k]) { t += prezzoDi(k) * scelte[k]; n += scelte[k]; } });
    elTotale.textContent = n && disponibili ? T.totale(t * giorni, T.giorni(giorni)) : '';
  }

  elArticoli.addEventListener('change', function (e) {
    var k = e.target.getAttribute('data-chiave');
    if (!k) return;
    scelte[k] = Number(e.target.value);
    if (!scelte[k]) delete scelte[k];
    totale();
  });
  dal.addEventListener('change', dateCambiate);
  al.addEventListener('change', dateCambiate);

  // ------------------------------------------------------------ verifica anti-robot (Cloudflare Turnstile)
  var turnstileCaricato = false;
  function caricaTurnstile() {
    if (turnstileCaricato) return;
    turnstileCaricato = true;
    window.nolTurnstile = function () {
      widget = window.turnstile.render('#nol-verifica', {
        sitekey: form.dataset.sitekey, language: LINGUA, theme: 'light',
        callback: function (t) { token = t; },
        'expired-callback': function () { token = ''; },
        'error-callback': function () { token = ''; }
      });
    };
    var s = document.createElement('script');
    s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit&onload=nolTurnstile';
    s.async = true;
    document.head.appendChild(s);
  }
  form.addEventListener('focusin', caricaTurnstile);
  form.addEventListener('pointerdown', caricaTurnstile);

  // ------------------------------------------------------------ invio
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var f = form.elements;
    var righe = Object.keys(scelte).filter(function (k) { return scelte[k] > 0; }).map(function (k) {
      var p = k.split(':');
      return { articolo: p[0], taglia: p.length > 1 ? p.slice(1).join(':') : null, quantita: scelte[k] };
    });
    var errore = !f.dal.value || !f.al.value ? 'date'
      : !righe.length ? 'materiale'
      : f.nome.value.trim().length < 3 ? 'nome'
      : !f.telefono.checkValidity() || f.telefono.value.replace(/\D/g, '').length < 7 ? 'telefono'
      : !f.email.value || !f.email.checkValidity() ? 'email'
      : !token ? 'verifica' : '';
    if (errore) {
      messaggio(T.errori[errore], true);
      var campo = { date: f.dal, nome: f.nome, telefono: f.telefono, email: f.email }[errore];
      if (campo) campo.focus(); else elEsito.focus();
      return;
    }
    var bottone = form.querySelector('button[type="submit"]');
    bottone.disabled = true;
    messaggio('…');
    fetch(API + 'richiesta', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dal: f.dal.value, al: f.al.value, righe: righe, nome: f.nome.value, email: f.email.value,
        telefono: f.telefono.value, note: f.note.value, lingua: LINGUA, token: token
      })
    })
      .then(function (r) { return r.json().then(function (d) { if (!r.ok) throw d; return d; }); })
      .then(function () { fatto(f.email.value); })
      .catch(function (d) {
        bottone.disabled = false;
        if (window.turnstile && widget !== null) { window.turnstile.reset(widget); token = ''; }
        if (d && d.errore === 'esaurito' && d.disponibili) { disponibili = d.disponibili; disegna(); }
        var err = d && d.errore && T.errori[d.errore];
        messaggio(err || T.errori.rete + T.alt(MAIL), true);
        elEsito.focus();
      });
  });

  function fatto(mail) {
    var nuova = el('button', { 'class': 'btn btn--secondary', type: 'button', text: T.nuova });
    var box = el('div', { 'class': 'nol-fatto', tabindex: '-1', role: 'status' }, [el('p', { text: T.ok(mail) }), nuova]);
    nuova.addEventListener('click', function () { location.reload(); });
    form.hidden = true;
    form.parentNode.insertBefore(box, form);
    box.focus();
  }
})();
