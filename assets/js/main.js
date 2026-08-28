/* Visa Flight Ticket - minimal progressive enhancement (no dependencies) */
(function () {
  'use strict';

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
    var PRICES = {
      flight: +form.getAttribute('data-p-flight'),
      hotel: +form.getAttribute('data-p-hotel'),
      both: +form.getAttribute('data-p-both')
    };
    var RUSH = +form.getAttribute('data-p-rush');
    var out = document.getElementById('price-out');
    var lineOut = document.getElementById('price-line');

    function recalc() {
      var svc = (form.querySelector('input[name="service"]:checked') || {}).value || 'flight';
      var pax = parseInt(form.querySelector('#travellers').value, 10) || 1;
      var rush = form.querySelector('#rush') && form.querySelector('#rush').checked ? RUSH : 0;
      var total = PRICES[svc] * pax + rush;
      if (out) out.textContent = CURO + total;
      if (lineOut) {
        lineOut.textContent = CURO + PRICES[svc] + ' x ' + pax +
          ' traveller' + (pax > 1 ? 's' : '') +
          (rush ? ' + ' + CURO + RUSH + ' priority' : '');
      }
    }
    form.addEventListener('change', recalc);
    form.addEventListener('input', recalc);
    recalc();

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
    var depInput = document.getElementById('bw-dep');
    var retInput = document.getElementById('bw-ret');
    var fromLabel = document.getElementById('bw-from-label');
    var CUR = bw.getAttribute('data-cur') || '';
    var PRICES = {
      flight: +bw.getAttribute('data-p-flight'),
      hotel: +bw.getAttribute('data-p-hotel'),
      both: +bw.getAttribute('data-p-both')
    };
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

      submit.innerHTML = LABELS[service] + ' at ' + CUR + PRICES[service];
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
        if (v && el) el.value = v;
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
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      // stagger siblings so a grid cascades instead of popping as one block
      var sibs = n.parentNode.children, idx = 0;
      for (var k = 0; k < sibs.length; k++) if (sibs[k] === n) { idx = k; break; }
      n.style.setProperty('--rvd', Math.min(idx, 6) * 55 + 'ms');
    }

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

    // count the stat numbers up when the bar first scrolls into view
    var statEls = document.querySelectorAll('.stats .stat b');
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
          el.textContent = pre + '0' + post;
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

  // --- current year in footer ---------------------------------------------
  var y = document.querySelectorAll('.js-year');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
})();
