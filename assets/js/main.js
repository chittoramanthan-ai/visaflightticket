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
  var saved = null;
  try { saved = localStorage.getItem('vft-theme'); } catch (e) {}
  if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);

  var toggle = document.querySelector('.theme-btn');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var isDark = root.getAttribute('data-theme') === 'dark' ||
        (!root.getAttribute('data-theme') &&
          window.matchMedia('(prefers-color-scheme: dark)').matches);
      var next = isDark ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('vft-theme', next); } catch (e) {}
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

  // --- current year in footer ---------------------------------------------
  var y = document.querySelectorAll('.js-year');
  for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
})();
