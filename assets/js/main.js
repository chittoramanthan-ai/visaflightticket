/* Visa Flight Tickets - minimal progressive enhancement (no dependencies) */
(function () {
  'use strict';

  // --- analytics event layer ----------------------------------------------
  // One call site for the whole site, so switching provider in src/build.py
  // never means re-instrumenting anything. Silent when no provider is
  // configured, which is the default.
  //
  // It swallows its own errors on purpose: an ad blocker eating the analytics
  // script must not be able to take the order form down with it.
  function track(name, props) {
    try {
      if (window.plausible) {
        window.plausible(name, props ? { props: props } : undefined);
      } else if (window.gtag) {
        window.gtag('event', name, props || {});
      }
    } catch (e) { /* never worth an exception */ }
  }
  // The head ships a stub that queues calls, because checkout.js runs before
  // this file does and the thank-you page reports its conversion from there.
  // Replay whatever it caught, then take over.
  var queued = window.vftTrack && window.vftTrack.q;
  window.vftTrack = track;
  if (queued) {
    for (var qi = 0; qi < queued.length; qi++) {
      track(queued[qi][0], queued[qi][1]);
    }
  }

  // Anything with data-track="event_name" reports itself when clicked. Extra
  // data-track-* attributes ride along as properties, so a CTA can say which
  // page it was on without a per-page listener.
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-track]') : null;
    if (!el) return;
    var props = {};
    for (var i = 0; i < el.attributes.length; i++) {
      var a = el.attributes[i];
      if (a.name.indexOf('data-track-') === 0) {
        props[a.name.slice(11).replace(/-/g, '_')] = a.value;
      }
    }
    props.page = location.pathname;
    track(el.getAttribute('data-track'), props);
  }, true);

  // --- hero headline typing effect ----------------------------------------
  // The heading already contains its real text, so this only ever animates
  // over something that is correct without it: search engines index the
  // markup, a JS failure leaves the headline intact, and assistive tech reads
  // the whole string because aria-label carries it throughout.
  //
  // Every character is laid out from the start and merely made visible in
  // turn. Typing by appending text instead makes a half-finished word wrap to
  // the next line and then jump back as it completes, so the whole headline
  // shuffles up and down while it types. Reserving the final layout up front
  // is the only way to get a genuinely still block.
  (function () {
    var h = document.querySelector('h1[data-type]');
    if (!h) return;

    var reduce = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce) return;                       // leave it exactly as rendered

    var text = h.textContent.trim();
    if (!text || text.length > 120) return;   // long headings look silly typed

    h.setAttribute('aria-label', text);
    h.classList.add('is-typing');

    // Build the character spans. Line breaking still happens at the spaces in
    // the text, exactly as it did before, because inline elements do not
    // themselves create break opportunities.
    var frag = document.createDocumentFragment();
    var spans = [];
    for (var i = 0; i < text.length; i++) {
      var c = document.createElement('span');
      c.className = 'tc';
      c.textContent = text.charAt(i);
      frag.appendChild(c);
      spans.push(c);
    }
    h.textContent = '';
    h.setAttribute('aria-hidden', 'false');
    h.appendChild(frag);

    var n = 0, prev = null;
    function tick() {
      if (prev) prev.classList.remove('tc--cur');
      var el = spans[n];
      el.classList.add('tc--on', 'tc--cur');
      prev = el;
      n++;
      if (n < spans.length) {
        // A beat at the sentence break, so it reads rather than rattles.
        setTimeout(tick, text.charAt(n - 1) === '.' ? 170 : 14);
      } else {
        setTimeout(function () {
          el.classList.remove('tc--cur');
          h.classList.remove('is-typing');
        }, 900);
      }
    }
    setTimeout(tick, 160);
  })();

  // --- mobile nav ---------------------------------------------------------
  var burger = document.querySelector('.burger');
  var nav = document.getElementById('nav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // --- theme toggle (light / dark / system) -------------------------------
  var root = document.documentElement;
  // Light is the default for everyone. The OS dark preference is deliberately
  // NOT honoured -- dark only appears if the visitor asks for it here.
  var saved = null;
  try { saved = localStorage.getItem('vft-theme-v2'); } catch (e) {}
  if (saved === 'dark') root.setAttribute('data-theme', 'dark');

  var toggle = document.querySelector('.theme-btn');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('vft-theme-v2', next); } catch (e) {}
      toggle.setAttribute('aria-label', 'Switch to ' + (next === 'dark' ? 'light' : 'dark') + ' theme');
    });
  }

  // --- order form: live price estimate ------------------------------------
  var form = document.getElementById('order-form');
  if (form) {
    var CURO = form.getAttribute('data-cur') || '';
    var P_FLIGHT = +form.getAttribute('data-p-flight');
    var P_HOTEL = +form.getAttribute('data-p-hotel');
    var BUNDLE_SAVING = +form.getAttribute('data-p-saving');

    // Flights are priced per leg. A return date means a second leg.
    function legCount() {
      var ret = form.querySelector('#return');
      return (ret && ret.value) ? 2 : 1;
    }
    function unitPrice(svc, legs) {
      if (svc === 'hotel') return P_HOTEL;
      if (svc === 'both') return P_FLIGHT * legs + P_HOTEL - BUNDLE_SAVING;
      return P_FLIGHT * legs;
    }
    // ---- currency toggle -------------------------------------------------
    // Rupees are what we charge. USD is a conversion shown for readers who
    // think in dollars, which is why the note under the total keeps saying so
    // rather than letting anyone believe they will be billed in dollars.
    var USD_RATE = parseFloat(form.getAttribute('data-usd-rate')) || 0;
    var curMode = 'INR';
    try { curMode = localStorage.getItem('vft-cur') === 'USD' ? 'USD' : 'INR'; } catch (e) {}

    function fmt(rupees) {
      if (curMode === 'USD' && USD_RATE) {
        var v = rupees / USD_RATE;
        return '$' + (v < 100 ? v.toFixed(1).replace(/\.0$/, '') : Math.round(v));
      }
      return CURO + rupees.toLocaleString('en-IN');
    }

    var curBtns = form.querySelectorAll('[data-cur-set]');
    function paintCur() {
      for (var i = 0; i < curBtns.length; i++) {
        var on = curBtns[i].getAttribute('data-cur-set') === curMode;
        curBtns[i].classList.toggle('is-on', on);
        curBtns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
      }
      // The three service options quote a price too. Leaving them in rupees
      // while the total switched to dollars is the sort of half-applied toggle
      // that makes people distrust the number they are about to pay.
      var opts = form.querySelectorAll('.optprice');
      for (var o = 0; o < opts.length; o++) {
        opts[o].textContent = fmt(parseInt(opts[o].getAttribute('data-inr'), 10));
      }
    }
    for (var ci = 0; ci < curBtns.length; ci++) {
      curBtns[ci].addEventListener('click', function () {
        curMode = this.getAttribute('data-cur-set');
        try { localStorage.setItem('vft-cur', curMode); } catch (e) {}
        paintCur();
        recalc();
      });
    }
    paintCur();

    function recalc() {
      // Resolved every time rather than cached: checkout.js rewrites the
      // button's innerHTML while submitting, which destroys this span. A held
      // reference would then be a detached node and the button would freeze
      // on the last price it happened to show.
      var out = document.getElementById('price-out');
      var lineOut = document.getElementById('price-line');
      var svc = (form.querySelector('input[name="service"]:checked') || {}).value || 'flight';
      var pax = form.querySelectorAll('#pax-list .pax').length || 1;
      var legs = legCount();
      var unit = unitPrice(svc, legs);
      if (out) out.textContent = fmt(unit * pax);
      if (lineOut) {
        var bits = fmt(unit) + ' x ' + pax + ' traveller' + (pax > 1 ? 's' : '');
        if (svc !== 'hotel') {
          bits += legs > 1 ? ' (return, 2 flights)' : ' (one way)';
        }
        // Say plainly which currency is actually charged, so a dollar figure
        // is never mistaken for the billing currency.
        lineOut.textContent = bits;
      }
    }
    window.vftRecalc = recalc;
    form.addEventListener('change', recalc);
    form.addEventListener('input', recalc);
    recalc();

    // ---- repeatable travellers -------------------------------------------
    var paxList = document.getElementById('pax-list');
    var paxAdd = document.getElementById('pax-add');
    var MAX_PAX = 12;

    function paxCount() { return paxList ? paxList.querySelectorAll('.pax').length : 1; }

    function renumberPax() {
      var all = paxList.querySelectorAll('.pax');
      for (var i = 0; i < all.length; i++) {
        all[i].querySelector('.pax__n').textContent = 'Traveller ' + (i + 1);
      }
      if (paxAdd) {
        paxAdd.hidden = all.length >= MAX_PAX;
        paxAdd.textContent = '+ Add another traveller';
      }
      recalc();
    }

    function addPax() {
      if (paxCount() >= MAX_PAX) return;
      var n = paxCount() + 1;
      var el = document.createElement('div');
      el.className = 'pax';
      el.innerHTML =
        '<div class="pax__hd"><span class="pax__n">Traveller ' + n + '</span>' +
        '<button type="button" class="pax__rm">Remove</button></div>' +
        '<div class="row2">' +
          '<div class="field"><label>Surname (as in passport)</label>' +
            '<input type="text" data-pax="surname" autocomplete="off" required></div>' +
          '<div class="field"><label>Given name(s)</label>' +
            '<input type="text" data-pax="given" autocomplete="off" required></div>' +
        '</div>' +
        '<div class="row2">' +
          '<div class="field"><label>Date of birth</label>' +
            '<input type="date" data-pax="dob"></div>' +
          '<div class="field"><label>Passport number</label>' +
            '<input type="text" data-pax="passport" autocomplete="off" maxlength="20"></div>' +
        '</div>' +
        '<div class="row2">' +
          '<div class="field"><label>Passport issue date</label>' +
            '<input type="date" data-pax="passport_issue"></div>' +
          '<div class="field"><label>Passport expiry date</label>' +
            '<input type="date" data-pax="passport_expiry"></div>' +
        '</div>';
      el.querySelector('.pax__rm').addEventListener('click', function () {
        el.parentNode.removeChild(el);
        renumberPax();
      });
      paxList.appendChild(el);
      renumberPax();
      var first = el.querySelector('input');
      if (first) first.focus();
    }

    if (paxAdd) paxAdd.addEventListener('click', addPax);

    // Inline validation: tell people what is wrong next to the field, on
    // submit and then live as they fix it -- not a browser tooltip that
    // vanishes, and not a wall of errors at the top.
    function badge(field, message) {
      var wrap = field.closest('.field');
      if (!wrap) return;
      var err = wrap.querySelector('.field-err');
      if (!err) {
        err = document.createElement('span');
        err.className = 'field-err';
        wrap.appendChild(err);
      }
      err.textContent = message;
      wrap.classList.add('is-bad');
      field.setAttribute('aria-invalid', 'true');
    }
    function clearBadge(field) {
      var wrap = field.closest('.field');
      if (wrap) wrap.classList.remove('is-bad');
      field.removeAttribute('aria-invalid');
    }
    function validate() {
      var bad = null;
      var required = form.querySelectorAll('[required]');
      for (var i = 0; i < required.length; i++) {
        var f = required[i];
        var v = (f.value || '').trim();
        var problem = '';
        if (!v) problem = 'This one is required.';
        else if (f.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v))
          problem = 'That does not look like an email address.';
        if (problem) { badge(f, problem); if (!bad) bad = f; }
        else clearBadge(f);
      }
      return bad;
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = validate();
      if (bad) {
        bad.focus();
        bad.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      // Validation passed. checkout.js takes it from here if a backend is
      // configured; otherwise show the offline notice.
      if (window.VFT_CONFIG && window.VFT_CONFIG.supabaseUrl) {
        form.dispatchEvent(new CustomEvent('vft:submit'));
        return;
      }
      var msg = document.getElementById('order-msg');
      if (msg) {
        msg.className = 'note note--ok';
        msg.innerHTML = '<strong>Almost there</strong><p>No payment backend is configured yet. ' +
          'Set SUPABASE_URL and SUPABASE_ANON_KEY in src/build.py and rebuild, or take this order ' +
          'by email in the meantime.</p>';
        msg.hidden = false;
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
    form.addEventListener('input', function (e) {
      if (e.target.getAttribute('aria-invalid')) {
        if ((e.target.value || '').trim()) clearBadge(e.target);
      }
    });

    // return date is never before departure
    var dep = form.querySelector('#depart');
    var ret = form.querySelector('#return');
    var today = new Date().toISOString().slice(0, 10);
    if (dep) { dep.min = today; }
    if (dep && ret) {
      dep.addEventListener('change', function () {
        ret.min = dep.value || today;
        if (ret.value && ret.value < dep.value) ret.value = dep.value;
      });
      ret.min = today;
    }
  }

  // --- hero booking widget -------------------------------------------------
  var bw = document.getElementById('bw');
  if (bw) {
    var tabs = bw.querySelectorAll('.bw__tab');
    var svcField = document.getElementById('bw-service');
    var tripBox = document.getElementById('bw-trip');
    var fromWrap = document.getElementById('bw-from-wrap');
    var retWrap = document.getElementById('bw-ret-wrap');
    var toLabel = document.getElementById('bw-to-label');
    var depLabel = document.getElementById('bw-dep-label');
    var retLabel = document.getElementById('bw-ret-label');
    var toInput = document.getElementById('bw-to');
    var submit = document.getElementById('bw-submit');
    var BW_USD_RATE = parseFloat(bw.getAttribute('data-usd-rate')) || 0;
    var depInput = document.getElementById('bw-dep');
    var retInput = document.getElementById('bw-ret');
    var fromLabel = document.getElementById('bw-from-label');
    var CUR = bw.getAttribute('data-cur') || '';
    var BW_FLIGHT = +bw.getAttribute('data-p-flight');
    var BW_HOTEL = +bw.getAttribute('data-p-hotel');
    var BW_SAVING = +bw.getAttribute('data-p-saving');

    // one way = 1 leg, return = 2, multi-city = 1 per flight shown
    function bwLegs() {
      var t = tripValue();
      if (t === 'round') return 2;
      if (t === 'multi') return 1 + legCount();
      return 1;
    }
    function bwPrice() {
      var legs = bwLegs();
      if (service === 'hotel') return BW_HOTEL;
      if (service === 'both') return BW_FLIGHT * legs + BW_HOTEL - BW_SAVING;
      return BW_FLIGHT * legs;
    }
    var LABELS = {
      flight: 'Get my dummy ticket',
      hotel: 'Get my hotel booking',
      both: 'Get flight + hotel'
    };
    var service = 'flight';

    function tripValue() {
      var r = bw.querySelector('input[name="trip"]:checked');
      return r ? r.value : 'oneway';
    }

    var legsBox = document.getElementById('bw-legs');
    var addLeg = document.getElementById('bw-addleg');
    var MAX_LEGS = 5;

    function legCount() { return legsBox ? legsBox.querySelectorAll('.bw__leg').length : 0; }

    function buildLeg(n) {
      var d = document.createElement('div');
      d.className = 'bw__leg';
      d.innerHTML =
        '<div class="bw__leghd"><span>Flight ' + (n + 2) + '</span>' +
        '<button type="button" class="bw__rm" aria-label="Remove this flight">Remove</button></div>' +
        '<div class="bw__f"><label>From</label>' +
        '<input type="text" name="leg' + (n + 2) + '_from" data-airport placeholder="Paris (CDG)"></div>' +
        '<div class="bw__f"><label>To</label>' +
        '<input type="text" name="leg' + (n + 2) + '_to" data-airport placeholder="Rome (FCO)"></div>' +
        '<div class="bw__f"><label>Departure</label>' +
        '<input type="date" name="leg' + (n + 2) + '_date" min="' +
        new Date().toISOString().slice(0, 10) + '"></div>';
      d.querySelector('.bw__rm').addEventListener('click', function () {
        d.parentNode.removeChild(d);
        renumber();
        render();
      });
      var ins = d.querySelectorAll('[data-airport]');
      for (var i = 0; i < ins.length; i++) attachAirport(ins[i]);
      return d;
    }

    function renumber() {
      var legs = legsBox.querySelectorAll('.bw__leg');
      for (var i = 0; i < legs.length; i++) {
        legs[i].querySelector('.bw__leghd span').textContent = 'Flight ' + (i + 2);
        var f = legs[i].querySelectorAll('input');
        f[0].name = 'leg' + (i + 2) + '_from';
        f[1].name = 'leg' + (i + 2) + '_to';
        f[2].name = 'leg' + (i + 2) + '_date';
      }
      if (addLeg) addLeg.hidden = legs.length + 1 >= MAX_LEGS;
      // legs are priced, so the button total has to follow the leg count
      render();
    }

    if (addLeg) {
      addLeg.addEventListener('click', function () {
        if (legCount() + 1 >= MAX_LEGS) return;
        legsBox.appendChild(buildLeg(legCount()));
        renumber();
      });
    }

    function render() {
      var hotel = service === 'hotel';
      var multi = !hotel && tripValue() === 'multi';

      // hotel needs a city and a stay, not a route and a trip type
      tripBox.hidden = hotel;
      fromWrap.hidden = hotel;
      toLabel.textContent = hotel ? 'City' : 'To';
      toInput.placeholder = hotel ? 'Paris' : 'Paris (CDG)';
      depLabel.textContent = hotel ? 'Check-in' : 'Departure';
      retLabel.textContent = hotel ? 'Check-out' : 'Return';

      // multi-city has no single return leg -- it has a list of onward flights
      retWrap.hidden = hotel ? false : (tripValue() !== 'round');
      if (legsBox) legsBox.hidden = !multi;
      if (addLeg) addLeg.hidden = !multi || legCount() + 1 >= MAX_LEGS;
      if (multi && legCount() === 0) {
        legsBox.appendChild(buildLeg(0));
        renumber();
      }
      if (fromLabel) fromLabel.textContent = multi ? 'From (flight 1)' : 'From';
      if (depLabel && multi) depLabel.textContent = 'Departure (flight 1)';

      // The server renders a dollar figure into this button; rewriting the
      // label here threw it away, so the hero button showed both currencies
      // and the widget button showed one. Rebuild both parts every time.
      var rupees = bwPrice();
      var alt = '';
      if (BW_USD_RATE) {
        var d = rupees / BW_USD_RATE;
        alt = '<span class="usd-alt">$' +
              (d < 100 ? d.toFixed(1).replace(/\.0$/, '') : Math.round(d)) + '</span>';
      }
      submit.innerHTML = LABELS[service] + ' at ' + CUR + rupees + alt;
    }

    for (var i = 0; i < tabs.length; i++) {
      tabs[i].addEventListener('click', function () {
        for (var j = 0; j < tabs.length; j++) {
          tabs[j].classList.remove('is-on');
          tabs[j].setAttribute('aria-selected', 'false');
        }
        this.classList.add('is-on');
        this.setAttribute('aria-selected', 'true');
        service = this.getAttribute('data-svc');
        svcField.value = service;
        render();
      });
    }
    tripBox.addEventListener('change', render);

    var today = new Date().toISOString().slice(0, 10);
    depInput.min = today;
    retInput.min = today;
    depInput.addEventListener('change', function () {
      retInput.min = depInput.value || today;
      if (retInput.value && retInput.value < depInput.value) retInput.value = depInput.value;
    });
    render();
  }

  // --- order page: prefill from the hero widget's query string -------------
  if (form && window.location.search) {
    var q = new URLSearchParams(window.location.search);
    var svc = q.get('service');
    if (svc) {
      var radio = form.querySelector('input[name="service"][value="' + svc + '"]');
      if (radio) { radio.checked = true; }
    }
    [['from', 'from'], ['to', 'to'], ['depart', 'depart'], ['return', 'return']]
      .forEach(function (pair) {
        var v = q.get(pair[0]);
        var el = form.querySelector('#' + pair[1]);
        if (!v || !el) return;
        // Visa guides link in with a bare IATA code. Expand it to the same
        // "City (CODE)" the autocomplete would have written, so a prefilled
        // field is indistinguishable from one the reader filled themselves.
        if ((pair[0] === 'from' || pair[0] === 'to') && /^[A-Za-z]{3}$/.test(v)) {
          var hit = search(v, 1)[0];
          if (hit && hit.code.toUpperCase() === v.toUpperCase()) v = label(hit);
        }
        el.value = v;
      });
    form.dispatchEvent(new Event('change'));
  }

  // --- airport autocomplete -----------------------------------------------
  // Index is "IATA|Airport|City|Country" rows in window.VFT_AIRPORTS.
  var AIR = null;
  function airports() {
    if (AIR) return AIR;
    AIR = [];
    var raw = window.VFT_AIRPORTS;
    if (!raw) return AIR;
    var rows = raw.split('\n');
    for (var i = 0; i < rows.length; i++) {
      var f = rows[i].split('|');
      if (f.length < 4) continue;
      AIR.push({
        code: f[0], name: f[1], city: f[2], country: f[3],
        hay: (f[0] + ' ' + f[1] + ' ' + f[2] + ' ' + f[3]).toLowerCase()
      });
    }
    return AIR;
  }

  // Ranked so the thing you almost certainly meant is first: exact code,
  // then code prefix, then city, then airport name, then country.
  function search(q, limit) {
    q = q.trim().toLowerCase();
    if (!q) return [];
    var list = airports(), hits = [];
    for (var i = 0; i < list.length; i++) {
      var a = list[i], code = a.code.toLowerCase(), city = a.city.toLowerCase(), rank = -1;
      if (code === q) rank = 0;
      else if (code.indexOf(q) === 0) rank = 1;
      else if (city.indexOf(q) === 0) rank = 2;
      else if (a.name.toLowerCase().indexOf(q) === 0) rank = 3;
      else if (city.indexOf(q) > -1) rank = 4;
      else if (a.hay.indexOf(q) > -1) rank = 5;
      if (rank > -1) hits.push([rank, a]);
    }
    hits.sort(function (x, y) {
      return x[0] - y[0] || x[1].city.localeCompare(y[1].city);
    });
    var out = [];
    for (var j = 0; j < hits.length && out.length < (limit || 8); j++) out.push(hits[j][1]);
    return out;
  }

  function label(a) { return a.city + ' (' + a.code + ')'; }

  function attachAirport(input) {
    if (!input || input.__air) return;
    input.__air = true;
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');

    var box = document.createElement('div');
    box.className = 'ac';
    box.setAttribute('role', 'listbox');
    var wrap = document.createElement('div');
    wrap.className = 'ac-wrap';
    input.parentNode.insertBefore(wrap, input);
    wrap.appendChild(input);
    wrap.appendChild(box);

    var items = [], active = -1;

    function close() {
      box.classList.remove('is-open');
      input.setAttribute('aria-expanded', 'false');
      active = -1;
    }
    function choose(a) {
      input.value = label(a);
      close();
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    function paint(list) {
      items = list;
      if (!list.length) { box.innerHTML = ''; close(); return; }
      var html = '';
      for (var i = 0; i < list.length; i++) {
        var a = list[i];
        html += '<button type="button" class="ac__i" role="option" data-i="' + i + '">' +
          '<span class="ac__code">' + a.code + '</span>' +
          '<span class="ac__txt"><b>' + a.city + '</b>' +
          '<small>' + a.name + ' &middot; ' + a.country + '</small></span></button>';
      }
      box.innerHTML = html;
      box.classList.add('is-open');
      input.setAttribute('aria-expanded', 'true');
      active = -1;
    }
    function highlight(n) {
      var els = box.querySelectorAll('.ac__i');
      for (var i = 0; i < els.length; i++) els[i].classList.toggle('is-on', i === n);
      if (els[n]) els[n].scrollIntoView({ block: 'nearest' });
      active = n;
    }

    input.addEventListener('input', function () { paint(search(input.value, 8)); });
    input.addEventListener('focus', function () {
      if (input.value.trim()) paint(search(input.value, 8));
    });
    input.addEventListener('keydown', function (e) {
      if (!box.classList.contains('is-open')) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); highlight(Math.min(active + 1, items.length - 1)); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); highlight(Math.max(active - 1, 0)); }
      else if (e.key === 'Enter' && active > -1) { e.preventDefault(); choose(items[active]); }
      else if (e.key === 'Escape') { close(); }
    });
    box.addEventListener('mousedown', function (e) {
      var b = e.target.closest ? e.target.closest('.ac__i') : null;
      if (b) { e.preventDefault(); choose(items[+b.getAttribute('data-i')]); }
    });
    document.addEventListener('click', function (e) {
      if (!wrap.contains(e.target)) close();
    });
  }

  var airInputs = document.querySelectorAll('[data-airport]');
  for (var ai = 0; ai < airInputs.length; ai++) attachAirport(airInputs[ai]);

  // --- scroll reveal + counters -------------------------------------------
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  // Must mirror the CSS selector list exactly, hero excluded -- above-the-fold
  // content is never allowed to depend on the observer firing.
  var RV_SEL = [
    'section:not(.hero) > .wrap > *', 'section:not(.hero) .grid > *',
    'section:not(.hero) .steps > *', 'section:not(.hero) .trust-panel > .trust-card',
    'section:not(.hero) .stats .stat', 'section:not(.hero) .mq',
    'section:not(.hero) .tbl-wrap', 'section:not(.hero) .faq',
    'section:not(.hero) .note'
  ].join(', ');

  if (reduce || !('IntersectionObserver' in window)) {
    // No observer, no animation: drop the flag so nothing stays hidden.
    document.documentElement.classList.remove('js-anim');
  } else {
    var nodes = document.querySelectorAll(RV_SEL);
    var vh = window.innerHeight || 800;
    var deferred = [];

    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];

      // Anything already on screen when the page opens is shown at once, with
      // no fade and no stagger. Animating what the reader is already looking
      // at is what made a 200ms page feel like a slow one: the bytes had
      // arrived, the content was simply still invisible.
      if (n.getBoundingClientRect().top < vh * 0.95) {
        n.classList.add('rv-now');
        continue;
      }

      // stagger siblings so a grid cascades instead of popping as one block
      var sibs = n.parentNode.children, idx = 0;
      for (var k = 0; k < sibs.length; k++) if (sibs[k] === n) { idx = k; break; }
      n.style.setProperty('--rvd', Math.min(idx, 6) * 30 + 'ms');
      deferred.push(n);
    }
    nodes = deferred;

    var io = new IntersectionObserver(function (entries) {
      for (var e = 0; e < entries.length; e++) {
        if (entries[e].isIntersecting) {
          entries[e].target.classList.add('rv-in');
          io.unobserve(entries[e].target);
        }
      }
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
    for (var r = 0; r < nodes.length; r++) io.observe(nodes[r]);

    // Safety net: whatever has not been revealed after 4s gets revealed anyway,
    // so a stuck observer can never leave content permanently invisible.
    setTimeout(function () {
      document.documentElement.classList.remove('js-anim');
    }, 4000);

    // Count the stat numbers up when the bar first scrolls into view.
    // Skipped entirely for anyone who has asked their OS for less motion:
    // they keep the real numbers, immediately.
    var noMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var statEls = noMotion ? [] : document.querySelectorAll('.stats .stat b');
    var cio = new IntersectionObserver(function (entries) {
      for (var e = 0; e < entries.length; e++) {
        if (!entries[e].isIntersecting) continue;
        var el = entries[e].target;
        cio.unobserve(el);
        var m = el.textContent.match(/^([^\d]*)([\d,]+)(.*)$/);
        if (!m) continue;
        var target = parseInt(m[2].replace(/,/g, ''), 10);
        // A year is not a quantity -- counting "Since 2017" up from zero
        // reads as a bug, not an animation.
        if (!target || target > 5000000) continue;
        if (target >= 1900 && target <= 2100 && /since/i.test(el.parentNode.textContent)) continue;
        (function (el, pre, post, target) {
          var t0 = null, dur = 1100;
          function step(ts) {
            if (!t0) t0 = ts;
            var p = Math.min((ts - t0) / dur, 1);
            var v = Math.round(target * (1 - Math.pow(1 - p, 3)));
            el.textContent = pre + v.toLocaleString('en-IN') + post;
            if (p < 1) requestAnimationFrame(step);
          }
          // Deliberately NOT zeroed before the first frame. requestAnimationFrame
          // does not run in a background tab, so pre-zeroing left anyone who
          // opened the site in a new tab looking at "0 lakh+" until they
          // focused it. The real number stays until an animation frame that
          // will actually replace it arrives.
          requestAnimationFrame(step);
        })(el, m[1], m[3], target);
      }
    }, { threshold: 0.5 });
    for (var si = 0; si < statEls.length; si++) cio.observe(statEls[si]);
  }


  // --- sticky conversion bar ----------------------------------------------
  // Layout values are measured once (and on resize), so the scroll handler
  // only reads scrollY and toggles a class -- no per-frame layout reads, and
  // therefore no need to defer through requestAnimationFrame.
  var scta = document.getElementById('scta');
  if (scta) {
    var showAt = 0, endAt = Infinity, up = null;

    function measureScta() {
      var hero = document.querySelector('.hero');
      showAt = hero ? hero.offsetTop + hero.offsetHeight - 120
                    : Math.round(window.innerHeight * 0.6);
      endAt = document.documentElement.scrollHeight - window.innerHeight - 40;
    }
    function updateScta() {
      var y = window.pageYOffset || document.documentElement.scrollTop || 0;
      var show = y > showAt && y < endAt;     // hide at the very bottom so the
      if (show === up) return;                // footer CTA is never covered
      up = show;
      scta.classList.toggle('is-up', show);
      document.body.classList.toggle('has-scta', show);
    }
    measureScta();
    updateScta();
    window.addEventListener('scroll', updateScta, { passive: true });
    window.addEventListener('resize', function () { measureScta(); up = null; updateScta(); },
                            { passive: true });
    window.addEventListener('load', function () { measureScta(); up = null; updateScta(); });
  }

  // --- back to top ---------------------------------------------------------
  var totop = document.getElementById('totop');
  if (totop) {
    var tShown = null;
    function updateTop() {
      var show = (window.pageYOffset || document.documentElement.scrollTop || 0) > 700;
      if (show === tShown) return;
      tShown = show;
      totop.classList.toggle('is-on', show);
    }
    updateTop();
    window.addEventListener('scroll', updateTop, { passive: true });
    totop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }

  // --- reading progress on articles ---------------------------------------
  var article = document.querySelector('.article');
  if (article && !reduce) {
    var bar = document.createElement('div');
    bar.className = 'rprog';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'Reading progress');
    bar.setAttribute('aria-valuemin', '0');
    bar.setAttribute('aria-valuemax', '100');
    document.body.appendChild(bar);

    var aTop = 0, aSpan = 1;
    function measureProg() {
      aTop = article.offsetTop;
      aSpan = Math.max(1, article.offsetHeight - window.innerHeight);
    }
    function updateProg() {
      var y = (window.pageYOffset || document.documentElement.scrollTop || 0) - aTop;
      var pct = Math.max(0, Math.min(1, y / aSpan));
      bar.style.width = (pct * 100).toFixed(1) + '%';
      bar.setAttribute('aria-valuenow', Math.round(pct * 100));
    }
    measureProg();
    updateProg();
    window.addEventListener('scroll', updateProg, { passive: true });
    window.addEventListener('resize', function () { measureProg(); updateProg(); },
                            { passive: true });
    window.addEventListener('load', function () { measureProg(); updateProg(); });
  }

  // --- date fields open the picker from anywhere in the box ---------------
  // Native date inputs only respond to the little calendar glyph, which is a
  // tiny target and not obviously the only one that works. Delegated from the
  // document so dynamically added rows (extra travellers, multi-city legs)
  // behave the same without being wired up individually.
  (function () {
    if (!('showPicker' in HTMLInputElement.prototype)) return;   // older Safari, Firefox

    function open(e) {
      var el = e.target;
      if (!el || el.tagName !== 'INPUT') return;
      var t = el.type;
      if (t !== 'date' && t !== 'month' && t !== 'time') return;
      if (el.disabled || el.readOnly) return;
      try {
        el.showPicker();
      } catch (_) {
        // Chrome throws if the picker is already open, which happens when the
        // click landed on the native glyph. Nothing to do, it is open.
      }
    }

    document.addEventListener('click', open);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        var el = e.target;
        if (el && el.tagName === 'INPUT' && el.type === 'date') {
          e.preventDefault();
          open(e);
        }
      }
    });
  })();

  // --- current year in footer ---------------------------------------------
  var y = document.querySelectorAll('.js-year');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
})();
