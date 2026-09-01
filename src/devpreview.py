# -*- coding: utf-8 -*-
"""
Local-only preview of the payment flow.

    python src/devpreview.py      ->  _dev/upi-preview.html

The real /order/ page cannot show the payment step until the Supabase
functions are deployed: create-order fails, and the customer never reaches
the UPI panel. This takes the real built order page and injects a stub that
answers create-order and confirm-upi locally, so the actual payment UI can be
seen and clicked through with no backend at all.

It reads order/index.html rather than reimplementing it, so it cannot drift
from the real page. Rerun it after any rebuild.

NEVER DEPLOY _dev/. It is blocked in .htaccess and _headers, ignored by git,
and the page paints a banner saying so. The stub answers with a fake reference
and would happily tell a real customer their order was created.
"""

import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "order", "index.html")
OUT_DIR = os.path.join(ROOT, "_dev")
OUT = os.path.join(OUT_DIR, "upi-preview.html")

# A stubbed create-order response. Shaped exactly like the real one so the
# preview exercises the real showUpi() path rather than a lookalike.
STUB = r"""
<script>
/* ---------------------------------------------------------------------------
   LOCAL PREVIEW STUB. Intercepts the two Edge Function calls and answers them
   from here. Nothing leaves the machine and no order is created anywhere.
   --------------------------------------------------------------------------- */
(function () {
  var VPA   = 'yourbusiness@okhdfcbank';   // pretend merchant VPA
  var PAYEE = 'Visa Flight Ticket';
  var realFetch = window.fetch;

  function refFor() {
    return 'VFT-' + String(Math.floor(Math.random() * 900000) + 100000);
  }

  window.fetch = function (url, opts) {
    var u = String(url);

    if (u.indexOf('/create-order') > -1) {
      var body = {};
      try { body = JSON.parse((opts && opts.body) || '{}'); } catch (e) {}

      // Mirror the server's pricing so the preview shows a real total.
      // Kept in sync by hand with create-order/index.ts and src/build.py.
      var F = 499, H = 399, SAVING = 99;
      var pax = Math.max(1, (body.passengers || []).length || 1);
      var legs = 1;
      if (body.trip === 'round' || (body.return_date && body.return_date !== body.depart_date)) legs = 2;
      if (body.trip === 'multi') legs = Math.min(1 + ((body.legs || []).length), 5);
      var unit = body.service === 'hotel' ? H
               : body.service === 'both'  ? F * legs + H - SAVING
               : F * legs;
      var minor = unit * pax * 100;
      var rupees = (minor / 100).toFixed(2);
      var ref = refFor();

      console.log('[preview] create-order stubbed:', {
        service: body.service, trip: body.trip, legs: legs,
        travellers: pax, amount: rupees
      });

      return Promise.resolve(new Response(JSON.stringify({
        ref: ref, amount_minor: minor, currency: 'INR',
        payment_configured: true, method: 'upi',
        upi: {
          uri: 'upi://pay?pa=' + encodeURIComponent(VPA) +
               '&pn=' + encodeURIComponent(PAYEE) +
               '&am=' + rupees + '&cu=INR&tn=' + encodeURIComponent(ref),
          vpa: VPA, payee: PAYEE, amount: rupees
        }
      }), { status: 200, headers: { 'content-type': 'application/json' } }));
    }

    if (u.indexOf('/confirm-upi') > -1) {
      console.log('[preview] confirm-upi stubbed, redirecting to thank-you');
      return Promise.resolve(new Response(JSON.stringify({ ok: true }),
        { status: 200, headers: { 'content-type': 'application/json' } }));
    }

    return realFetch.apply(this, arguments);
  };
})();
</script>
"""

BANNER = """
<div style="position:sticky;top:0;z-index:9999;background:#7a1620;color:#fff;
            padding:10px 16px;font:600 14px/1.4 system-ui,sans-serif;text-align:center">
  LOCAL PREVIEW &middot; the backend is stubbed in the browser &middot;
  no order is created and no money moves &middot; never deploy /_dev/
</div>
"""


def main():
    if not os.path.exists(SRC):
        raise SystemExit("order/index.html not found. Run python src/build.py first.")

    html = io.open(SRC, encoding="utf-8").read()

    # The stub has to be installed before checkout.js runs. Those scripts are
    # deferred, and a plain inline script executes before any deferred one, so
    # anywhere in <head> is early enough.
    if "</head>" not in html:
        raise SystemExit("could not find </head> in order/index.html")
    html = html.replace("</head>", STUB + "</head>", 1)
    html = html.replace("<body>", "<body>" + BANNER, 1)

    # Assets are root-relative, so they resolve from /_dev/ unchanged. Only the
    # canonical needs neutralising so this can never be indexed if it escapes.
    html = re.sub(r'<link rel="canonical"[^>]*>', '', html)
    html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)

    if not os.path.isdir(OUT_DIR):
        os.makedirs(OUT_DIR)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(html)
    print("wrote %s (%.1f KB)" % (os.path.relpath(OUT, ROOT), len(html) / 1024.0))
    print("open http://127.0.0.1:8899/_dev/upi-preview.html")


if __name__ == "__main__":
    main()
