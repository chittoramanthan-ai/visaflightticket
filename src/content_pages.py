# -*- coding: utf-8 -*-
"""Pages reached from the top menu: B2B and order status."""

import re

from build import (ICON, BRAND, EMAIL, DELIVERY, WHATSAPP,
                   money, add_page, url, faq_block, faq_schema, crumbs, cta_band)
import content_core


WA_DIGITS = re.sub(r"[^0-9]", "", WHATSAPP)


def build():
    b2b_page()
    login_page()


# --------------------------------------------------------------------------
def b2b_page():
    c_html, c_schema = crumbs([("B2B", None)])

    faqs = [
        ("What volume qualifies for trade pricing?",
         "<p>Roughly twenty files a month and up. Below that our standard per-traveller price is already lower than most trade rates, so there is nothing for an account to save you.</p>"),
        ("How are partner orders submitted?",
         "<p>Three ways, and you can mix them: a shared inbox with a fixed template, a spreadsheet upload for batches, or an HTTP endpoint if you want your own system to place orders directly.</p>"),
        ("Can documents be issued unbranded?",
         "<p>They already are. Nothing we issue carries our branding. The itinerary reads as a standard agency document. Partner accounts can carry your agency details on it instead.</p>"),
        ("How does billing work?",
         "<p>One consolidated invoice per month with a per-file breakdown, on 14- or 30-day terms depending on volume. No prepaid credit to burn down, no minimum commitment.</p>"),
        ("What turnaround can we promise our clients?",
         "<p>The same %s as retail. For same-day appointment volume we can agree a tighter window in writing.</p>" % DELIVERY),
        ("Who is this for?",
         "<p>Travel agencies, immigration consultants and visa-filing services, university international offices, relocation and mobility teams, and employers who sponsor visas at volume.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="hero__grid" style="align-items:flex-start">
      <div>
        <p class="eyebrow">Partner accounts</p>
        <h1>B2B: visa travel documents at volume</h1>
        <p class="lede">If you file visa applications for other people. As an agency, a consultancy, a
        university or an employer. You should not be paying retail, and you should not be re-keying the same
        traveller details into a form twenty times a week.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--primary btn--lg" href="mailto:%s?subject=B2B%%20account%%20enquiry">Request trade pricing</a>
          <a class="btn btn--wa btn--lg" href="https://wa.me/%s">%s Talk on WhatsApp</a>
        </div>
        %s
      </div>
      <div>%s</div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>What a partner account changes</h2>
      <p class="lede">Same documents, same verifiable PNRs. Less friction, lower unit cost.</p>
    </div>
    <div class="grid g3">
      <div class="card"><div class="card__ico">%s</div><h3>Tiered pricing</h3>
        <p>Rates step down with monthly volume. We quote against your actual file count, not the bracket you
        nearly reach.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Batch submission</h3>
        <p>Send twenty travellers in one spreadsheet instead of twenty forms. You get back one pack, named per
        traveller.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Monthly invoicing</h3>
        <p>One consolidated invoice on 14- or 30-day terms, itemised per file so you can bill your own clients
        from it.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Your branding, or none</h3>
        <p>Documents carry no branding of ours by default. Partner accounts can carry your agency details
        instead.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Corrections without quibble</h3>
        <p>Name and date fixes at half price, and free when the fault is ours, however many come back from a
        consulate in a busy week.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>A named contact</h3>
        <p>One person who knows your account and answers directly, not a shared inbox and a ticket
        number.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>How partners integrate</h2>
    <p>Pick whichever matches how you already work. None of them ask you to change your process much.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Method</th><th>Good for</th><th>Setup time</th></tr></thead>
        <tbody>
          <tr><td><b>Email template</b></td><td>Ad-hoc files, small teams</td><td>Immediate</td></tr>
          <tr><td><b>Spreadsheet batch</b></td><td>Groups, student intakes, corporate cohorts</td><td>Same day</td></tr>
          <tr><td><b>HTTP endpoint</b></td><td>Agencies running their own booking system</td><td>A few days</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note">
      <strong>One thing volume does not change</strong>
      Every reservation is still a real airline booking with a PNR your client can verify. If a partner wants
      documents that skip that step, we are not the right supplier, and any supplier who agrees is handing
      your clients a fraud finding with your name attached to it.
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, EMAIL, WA_DIGITS, ICON["whatsapp"], content_core.TRUSTLINE, content_core.BOARDING_PASS,
       ICON["wallet"], ICON["doc"], ICON["refresh"], ICON["shield"], ICON["clock"], ICON["users"],
       faq_block(faqs, "B2B questions"),
       cta_band("Tell us your monthly volume",
                "We come back with a rate, a submission method and a named contact, usually the same day.",
                primary=("Email the B2B team", "contact"),
                secondary=("See retail pricing", "pricing")))

    add_page("b2b", "B2B | Trade Pricing for Agencies & Visa Consultants",
             "Partner accounts for travel agencies, immigration consultants, universities and employers: tiered pricing, batch submission, monthly invoicing and a named contact.",
             body, schema=[c_schema, faq_schema(faqs)],
             priority="0.7", changefreq="monthly")


# --------------------------------------------------------------------------
def login_page():
    c_html, c_schema = crumbs([("Order status", None)])

    body = """
<section>
  <div class="wrap wrap--narrow">
    %s
    <div class="center" style="margin-bottom:2.2rem">
      <p class="eyebrow">Check status</p>
      <h1>Track your order</h1>
      <p class="lede">Enter the reference from your confirmation email to see where your documents are.</p>
    </div>

    <form class="form" id="status-form" novalidate>
      <div class="field">
        <label for="ref">Order reference</label>
        <input id="ref" name="ref" type="text" placeholder="VFT-000000" autocomplete="off" required>
        <span class="hint">In the subject line of your confirmation email.</span>
      </div>
      <div class="field">
        <label for="stat-email">Email used on the order</label>
        <input id="stat-email" name="email" type="email" autocomplete="email" required>
      </div>
      <button class="btn btn--primary btn--lg btn--block" type="submit">Check status</button>

      <div class="note note--ok" id="status-msg" hidden>
        <strong>Not connected yet</strong>
        <p>This build has no order database behind it. Point this form at your backend when you have one. Until
        then, email <a href="mailto:%s">%s</a> with your reference and we will reply with the status.</p>
      </div>
    </form>

    <h2 class="sr">Common questions about an order</h2>
    <div class="grid g2" style="margin-top:2.2rem">
      <div class="card"><h3>Nothing arrived?</h3>
        <p style="font-size:.95rem;color:var(--ink-2)">Delivery is normally within %s. Check spam first.         PDFs from an unfamiliar sender get filtered more often than you would expect.</p></div>
      <div class="card"><h3>Need a correction?</h3>
        <p style="font-size:.95rem;color:var(--ink-2)">A reissue costs half the original price, and nothing if
        the error was ours. Send your reference and the exact corrected spelling to <a href="mailto:%s">%s</a>.</p></div>
    </div>

    <p class="center" style="margin-top:2rem;color:var(--ink-3);font-size:.93rem">
      Want to check the booking itself rather than the order? You do not need us for that.       <a href="%s">verify the PNR on the airline&rsquo;s own site</a>.</p>
  </div>
</section>
""" % (c_html, EMAIL, EMAIL, DELIVERY, EMAIL, EMAIL, url("verify-pnr"))

    # noindex: a status lookup has no search value and would read as thin content
    add_page("login", "Check Your Order Status | " + BRAND,
             "Track a flight reservation or hotel booking order using your reference number.",
             body, schema=[c_schema], noindex=True, priority="0.2",
             extra_js=("assets/js/checkout.js",))
