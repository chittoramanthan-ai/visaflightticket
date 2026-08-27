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
    var PRICES = { flight: 9, hotel: 7, both: 14 };
    var out = document.getElementById('price-out');
    var lineOut = document.getElementById('price-line');

    function recalc() {
      var svc = (form.querySelector('input[name="service"]:checked') || {}).value || 'flight';
      var pax = parseInt(form.querySelector('#travellers').value, 10) || 1;
      var rush = form.querySelector('#rush') && form.querySelector('#rush').checked ? 5 : 0;
      var total = PRICES[svc] * pax + rush;
      if (out) out.textContent = '$' + total;
      if (lineOut) {
        lineOut.textContent = '$' + PRICES[svc] + ' x ' + pax +
          ' traveller' + (pax > 1 ? 's' : '') + (rush ? ' + $5 priority' : '');
      }
    }
    form.addEventListener('change', recalc);
    form.addEventListener('input', recalc);
    recalc();

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('order-msg');
      if (msg) {
        msg.hidden = false;
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
    var PRICES = { flight: 9, hotel: 7, both: 14 };
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

    function render() {
      var hotel = service === 'hotel';
      // hotel needs a city and a stay, not a route and a trip type
      tripBox.hidden = hotel;
      fromWrap.hidden = hotel;
      toLabel.textContent = hotel ? 'City' : 'To';
      toInput.placeholder = hotel ? 'Paris' : 'Paris (CDG)';
      depLabel.textContent = hotel ? 'Check-in' : 'Departure';
      retLabel.textContent = hotel ? 'Check-out' : 'Return';
      retWrap.hidden = !hotel && tripValue() === 'oneway';
      submit.innerHTML = LABELS[service] + ' — $' + PRICES[service];
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

  // --- current year in footer ---------------------------------------------
  var y = document.querySelectorAll('.js-year');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
})();
