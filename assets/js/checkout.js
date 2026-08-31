/* Visa Flight Ticket - checkout
   Loaded only on /order/ and /login/. Talks to Supabase Edge Functions.
   No secret ever lives here: the amount is priced server-side and the only
   Razorpay key that reaches this file is the publishable key_id, returned
   by create-order at request time. */
(function () {
  'use strict';

  var CFG = window.VFT_CONFIG || {};
  var FN = (CFG.supabaseUrl || '').replace(/\/$/, '') + '/functions/v1/';

  function post(path, payload) {
    return fetch(FN + path, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        // anon key is a public identifier, not a secret; RLS blocks everything
        'authorization': 'Bearer ' + (CFG.supabaseAnonKey || ''),
        'apikey': CFG.supabaseAnonKey || ''
      },
      body: JSON.stringify(payload)
    }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (b) {
        if (!r.ok) {
          var e = new Error(b.error || ('http_' + r.status));
          e.status = r.status;
          throw e;
        }
        return b;
      });
    });
  }

  function loadScript(src) {
    return new Promise(function (res, rej) {
      var s = document.createElement('script');
      s.src = src; s.onload = res; s.onerror = function () { rej(new Error('script_failed')); };
      document.head.appendChild(s);
    });
  }

  var MESSAGES = {
    bad_email: 'That email address does not look right.',
    name_required: 'We need the traveller name as printed in the passport.',
    return_before_depart: 'The return date is before the departure date.',
    payment_init_failed: 'The payment provider did not respond. Nothing has been charged.',
    could_not_create_order: 'We could not save the order. Please try again.',
    network: 'Could not reach our server. Check your connection and try again.'
  };

  // ---------------------------------------------------------------- order --
  var form = document.getElementById('order-form');
  if (form && CFG.supabaseUrl) {
    var btn = document.getElementById('order-submit');
    var msg = document.getElementById('order-msg');
    var busy = false;

    function say(kind, html) {
      if (!msg) return;
      msg.className = 'note note--' + (kind === 'ok' ? 'ok' : 'warn');
      msg.innerHTML = html;
      msg.hidden = false;
      msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    function setBusy(on, label) {
      busy = on;
      if (!btn) return;
      btn.disabled = on;
      btn.setAttribute('aria-busy', on ? 'true' : 'false');
      if (on) { btn.dataset.label = btn.dataset.label || btn.innerHTML; btn.innerHTML = label; }
      else if (btn.dataset.label) {
        btn.innerHTML = btn.dataset.label;
        // the restored markup carries a stale total, so repaint it
        if (window.vftRecalc) window.vftRecalc();
      }
    }

    function payload() {
      var v = function (id) { var e = form.querySelector('#' + id); return e ? e.value.trim() : ''; };
      var legs = [];
      form.querySelectorAll('.bw__leg').forEach(function (leg) {
        var i = leg.querySelectorAll('input');
        if (i[0] && i[0].value) legs.push({ from: i[0].value, to: i[1] ? i[1].value : '', date: i[2] ? i[2].value : '' });
      });
      var pax = [];
      form.querySelectorAll('#pax-list .pax').forEach(function (row, i) {
        if (i === 0) {
          pax.push({ surname: v('surname'), given_name: v('given'), dob: v('dob') });
          return;
        }
        var get = function (k) {
          var e = row.querySelector('[data-pax="' + k + '"]');
          return e ? e.value.trim() : '';
        };
        if (get('surname') || get('given')) {
          pax.push({ surname: get('surname'), given_name: get('given'), dob: get('dob') });
        }
      });
      var svcEl = form.querySelector('input[name="service"]:checked');
      var tripEl = form.querySelector('input[name="trip"]:checked');
      return {
        service: svcEl ? svcEl.value : 'flight',
        trip: tripEl ? tripEl.value : 'oneway',
        travellers: pax.length || 1,
        passengers: pax,
        origin: v('from'), destination: v('to'),
        depart_date: v('depart'), return_date: v('return'),
        legs: legs,
        visa_type: v('visa'),
        surname: v('surname'), given_name: v('given'),
        dob: v('dob'), email: v('email'), phone: v('phone'),
        notes: v('notes')
      };
    }

    function mailtoFallback() {
      var p = payload();
      var lines = [
        'Service: ' + p.service,
        'Travellers: ' + p.travellers,
        'Trip: ' + p.trip,
        'From: ' + p.origin,
        'To: ' + p.destination,
        'Depart: ' + p.depart_date,
        'Return: ' + p.return_date,
        'Passenger: ' + p.surname + ', ' + p.given_name,
        'Date of birth: ' + p.dob,
        'Email: ' + p.email,
        'Phone: ' + p.phone,
        'Visa: ' + p.visa_type,
        'Notes: ' + p.notes
      ].filter(function (l) { return !/: $/.test(l); });
      return 'mailto:' + (CFG.email || '') +
        '?subject=' + encodeURIComponent('Order request') +
        '&body=' + encodeURIComponent(lines.join(String.fromCharCode(10)));
    }

    // ------------------------------------------------------------ UPI ----
    function showUpi(res) {
      var u = res.upi;
      var isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
      say('ok',
        '<strong>Order ' + res.ref + ' created. Now pay ' + CFG.currency + u.amount + '</strong>' +
        '<div class="upi">' +
          '<div class="upi__qr" id="upi-qr"></div>' +
          '<div class="upi__side">' +
            (isMobile
              ? '<a class="btn btn--primary btn--block" href="' + u.uri + '">Open my UPI app</a>'
              : '<p class="upi__scan">Scan with any UPI app, or pay to the ID below.</p>') +
            '<dl class="upi__kv">' +
              '<dt>UPI ID</dt><dd><code id="upi-vpa">' + u.vpa + '</code>' +
                '<button type="button" class="upi__copy" data-copy="' + u.vpa + '">Copy</button></dd>' +
              '<dt>Amount</dt><dd><b>' + CFG.currency + u.amount + '</b></dd>' +
              '<dt>Reference</dt><dd><code>' + res.ref + '</code>' +
                '<button type="button" class="upi__copy" data-copy="' + res.ref + '">Copy</button></dd>' +
            '</dl>' +
            '<p class="upi__note">Put the reference in the payment note so we can match it.</p>' +
          '</div>' +
        '</div>' +
        '<div class="upi__confirm">' +
          '<label for="utr">Paid? Enter the UPI reference number from your app</label>' +
          '<div class="upi__row">' +
            '<input id="utr" type="text" inputmode="numeric" autocomplete="off" ' +
              'placeholder="12-digit reference" maxlength="24">' +
            '<button type="button" class="btn btn--primary" id="utr-go">Confirm</button>' +
          '</div>' +
          '<span class="hint">Your app calls it UTR, transaction ID or reference number. ' +
          'We check it against our account before issuing.</span>' +
          '<p class="field-err" id="utr-err"></p>' +
        '</div>');

      try { drawQR(document.getElementById('upi-qr'), u.uri); }
      catch (e) { document.getElementById('upi-qr').style.display = 'none'; }

      msg.querySelectorAll('.upi__copy').forEach(function (b) {
        b.addEventListener('click', function () {
          navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function () {
            var t = b.textContent; b.textContent = 'Copied';
            setTimeout(function () { b.textContent = t; }, 1400);
          });
        });
      });

      var go = document.getElementById('utr-go');
      go.addEventListener('click', function () {
        var utr = (document.getElementById('utr').value || '').replace(/\s+/g, '');
        var err = document.getElementById('utr-err');
        if (!/^[A-Za-z0-9]{8,24}$/.test(utr)) {
          err.textContent = 'That does not look like a reference number. Check your UPI app.';
          err.style.display = 'block';
          return;
        }
        err.style.display = 'none';
        go.disabled = true; go.textContent = 'Checking...';
        post('confirm-upi', { ref: res.ref, utr: utr }).then(function () {
          window.location.href = (CFG.basePath || '') + '/order/thank-you/?ref=' +
            encodeURIComponent(res.ref) + '&upi=1';
        }).catch(function (e) {
          go.disabled = false; go.textContent = 'Confirm';
          err.textContent = e.message === 'utr_already_used'
            ? 'That reference is already recorded against another order.'
            : 'Could not record that. Try again, or email us the reference.';
          err.style.display = 'block';
        });
      });
    }

    form.addEventListener('vft:submit', function () {
      if (busy) return;
      setBusy(true, 'Creating your order&hellip;');

      post('create-order', payload()).then(function (res) {
        if (res.method === 'upi') { setBusy(false); return showUpi(res); }
        if (!res.payment_configured) {
          say('ok',
            '<strong>Order ' + res.ref + ' saved</strong>' +
            '<p>Payments are not switched on yet, so nothing has been charged. We have your details ' +
            'and will email you at the address above. Quote <b>' + res.ref + '</b> if you get in touch.</p>');
          setBusy(false);
          return;
        }
        return loadScript('https://checkout.razorpay.com/v1/checkout.js').then(function () {
          setBusy(false);
          var rz = new window.Razorpay({
            key: res.key_id,
            order_id: res.provider_order_id,
            amount: res.amount_minor,
            currency: res.currency,
            name: 'Visa Flight Ticket',
            description: 'Order ' + res.ref,
            prefill: {
              name: payload().given_name + ' ' + payload().surname,
              email: payload().email,
              contact: payload().phone
            },
            theme: { color: '#193b92' },
            handler: function () {
              // The webhook is what actually marks this paid. This only moves
              // the customer along, so a closed browser cannot lose an order.
              window.location.href = (CFG.basePath || '') + '/order/thank-you/?ref=' +
                encodeURIComponent(res.ref);
            },
            modal: {
              ondismiss: function () {
                say('warn',
                  '<strong>Payment cancelled</strong>' +
                  '<p>Order <b>' + res.ref + '</b> is saved but unpaid. Reload and try again, or email us ' +
                  'the reference and we will send a payment link.</p>');
              }
            }
          });
          rz.on('payment.failed', function (e) {
            say('warn', '<strong>Payment failed</strong><p>' +
              ((e && e.error && e.error.description) || 'Your bank declined it.') +
              ' Nothing has been charged. Order <b>' + res.ref + '</b> is saved.</p>');
          });
          rz.open();
        });
      }).catch(function (err) {
        setBusy(false);
        // A missing or sleeping backend must not cost you the order. Hand the
        // customer a pre-filled email so the enquiry still reaches you.
        var down = err.status === 404 || err.status === 503 || !err.status;
        if (down) {
          say('warn',
            '<strong>Our order system is not reachable right now</strong>' +
            '<p>Nothing has been charged. Send us the details instead and we will ' +
            'take it from there, usually within the hour.</p>' +
            '<p><a class="btn btn--primary" href="' + mailtoFallback() + '">Email my order</a>' +
            ' <a class="btn btn--wa" href="' + (CFG.whatsapp || '#') + '">WhatsApp us</a></p>');
          return;
        }
        say('warn', '<strong>Something went wrong</strong><p>' +
          (MESSAGES[err.message] || MESSAGES.network) + '</p>');
      });
    });
  }

  // --------------------------------------------------------------- status --
  var statusForm = document.getElementById('status-form');
  if (statusForm && CFG.supabaseUrl) {
    statusForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var out = document.getElementById('status-msg');
      var ref = (document.getElementById('ref') || {}).value || '';
      var email = (document.getElementById('stat-email') || {}).value || '';
      if (!ref.trim() || !email.trim()) return;

      out.className = 'note';
      out.innerHTML = '<p>Checking&hellip;</p>';
      out.hidden = false;

      fetch((CFG.supabaseUrl || '').replace(/\/$/, '') + '/rest/v1/rpc/order_status_lookup', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'apikey': CFG.supabaseAnonKey || '',
          'authorization': 'Bearer ' + (CFG.supabaseAnonKey || '')
        },
        body: JSON.stringify({ p_ref: ref, p_email: email })
      }).then(function (r) { return r.json(); }).then(function (rows) {
        var o = Array.isArray(rows) ? rows[0] : null;
        if (!o) {
          out.className = 'note note--warn';
          out.innerHTML = '<strong>No match</strong><p>Check the reference and that the email is the one ' +
            'you ordered with. Still stuck? Email us and we will find it.</p>';
          return;
        }
        var LABEL = {
          pending: 'Received, awaiting payment',
          paid: 'Paid. We are working on it now',
          processing: 'Being issued',
          delivered: 'Delivered to your inbox',
          refunded: 'Refunded',
          failed: 'Payment did not go through'
        };
        out.className = 'note note--ok';
        out.innerHTML = '<strong>' + o.ref + ' &middot; ' + (LABEL[o.status] || o.status) + '</strong>' +
          '<p>Ordered ' + new Date(o.created_at).toLocaleString() +
          (o.delivered_at ? '. Delivered ' + new Date(o.delivered_at).toLocaleString() : '') + '.</p>';
      }).catch(function () {
        out.className = 'note note--warn';
        out.innerHTML = '<strong>Could not check right now</strong><p>Please try again shortly.</p>';
      });
    });
  }

  // ------------------------------------------------------------ thank you --
  var refOut = document.getElementById('ty-ref');
  if (refOut) {
    var q = new URLSearchParams(window.location.search).get('ref');
    if (q) refOut.textContent = q;
    else refOut.closest('[data-ref-wrap]').hidden = true;
  }
})();
