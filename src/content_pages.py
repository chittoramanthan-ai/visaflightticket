# -*- coding: utf-8 -*-
"""Pages reached from the top menu: bulk orders and order status."""

import re

from build import (ICON, BRAND, EMAIL, DELIVERY, WHATSAPP,
                   money, add_page, url, faq_block, faq_schema, crumbs, cta_band)
import content_core


WA_DIGITS = re.sub(r"[^0-9]", "", WHATSAPP)


def build():
    bulk_page()
    login_page()


# --------------------------------------------------------------------------
def bulk_page():
    c_html, c_schema = crumbs([("Bulk Orders", None)])

    faqs = [
        ("What counts as a bulk order?",
         "<p>Either around twenty files a month on an ongoing basis, or a single batch of ten travellers or more at once. Below that our standard per-traveller price is already lower than most trade rates, so an account has nothing left to save you.</p>"),
        ("How do I send a bulk order?",
         "<p>Three ways, and you can mix them: a shared inbox with a fixed template, a spreadsheet upload for batches, or an HTTP endpoint if you want your own system to place orders directly.</p>"),
        ("Is there a minimum order or a lock-in?",
         "<p>Neither. No minimum commitment, no prepaid credit to burn down, no monthly fee. A quiet month costs you nothing.</p>"),
        ("Can travellers in one batch have different routes?",
         "<p>Yes. A batch is only a list, and every row carries its own route, dates and service. Pricing stays per traveller and per leg, so a batch of one-way files costs less than a batch of returns.</p>"),
        ("Can documents be issued unbranded?",
         "<p>They already are. Nothing we issue carries our branding. The itinerary reads as a standard agency document. Bulk accounts can carry your own agency details on it instead.</p>"),
        ("How does billing work?",
         "<p>One consolidated invoice per month with a per-file breakdown, on 14- or 30-day terms depending on volume. You are not buying credit up front.</p>"),
        ("What turnaround can we promise our clients?",
         "<p>The same %s as retail, and a batch does not queue behind itself. For same-day appointment volume we can agree a tighter window in writing.</p>" % DELIVERY),
        ("Who is this for?",
         "<p>Travel agencies, immigration consultants and visa-filing services, university international offices, relocation and mobility teams, and employers who sponsor visas at volume.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="hero__grid" style="align-items:flex-start">
      <div>
        <p class="eyebrow">Bulk orders</p>
        <h1>Bulk orders: visa travel documents at volume</h1>
        <p class="lede">If you file visa applications for other people, as an agency, a consultancy, a
        university or an employer, you should not be paying retail and you should not be re-keying the same
        traveller details into a form twenty times a week. Send the batch once and get one pack back.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--primary btn--lg" href="mailto:%s?subject=Bulk%%20order%%20enquiry">Request bulk pricing</a>
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
      <h2>What ordering in bulk changes</h2>
      <p class="lede">Same documents, same verifiable PNRs. Less friction, lower unit cost.</p>
    </div>
    <div class="grid g3">
      <div class="card"><div class="card__ico">%s</div><h3>Bulk pricing</h3>
        <p>Rates step down with monthly volume. We quote against your actual file count, not the bracket you
        nearly reach.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>One batch, one upload</h3>
        <p>Send twenty travellers in a single spreadsheet instead of twenty forms. You get back one pack, named
        per traveller.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Monthly invoicing</h3>
        <p>One consolidated invoice on 14- or 30-day terms, itemised per file so you can bill your own clients
        straight from it.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Your branding, or none</h3>
        <p>Documents carry no branding of ours by default. Bulk accounts can carry your own agency details
        instead.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Corrections without quibble</h3>
        <p>Name and date fixes at half price, however many come back from a consulate in a busy week.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>A named contact</h3>
        <p>One person who knows your account and answers directly, not a shared inbox and a ticket
        number.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>Three ways to send a bulk order</h2>
    <p>Pick whichever matches how you already work. None of them asks you to change your process much.</p>
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

    <h3 style="margin-top:2.6rem">What a batch file needs</h3>
    <p>One row per traveller, with these columns. Anything missing comes back to you as a single query rather
    than six separate ones.</p>
    <ul>
      <li>Surname and given names, spelled exactly as they appear in the passport</li>
      <li>Date of birth</li>
      <li>Service: flight reservation, hotel booking, or both</li>
      <li>Route and travel dates, one way or return</li>
      <li>The visa being applied for, so we date the booking to suit the appointment</li>
    </ul>

    <div class="note">
      <strong>One thing volume does not change</strong>
      Every reservation is still a real airline booking with a PNR your client can verify. If a buyer wants
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
       faq_block(faqs, "Bulk order questions"),
       cta_band("Tell us your monthly volume",
                "We come back with a rate, a submission method and a named contact, usually the same day.",
                primary=("Email the bulk desk", "contact"),
                secondary=("See retail pricing", "pricing")))

    add_page("bulk-orders", "Bulk Orders | Volume Pricing for Visa Agencies",
             "Bulk flight reservations and hotel bookings for travel agencies, immigration consultants, universities and employers: volume pricing, batch upload, monthly invoicing and a named contact.",
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
        <p style="font-size:.95rem;color:var(--ink-2)">Delivery is normally within %s. Check spam first. PDFs
        from an unfamiliar sender get filtered more often than you would expect.</p></div>
      <div class="card"><h3>Need a correction?</h3>
        <p style="font-size:.95rem;color:var(--ink-2)">A reissue costs half the original price. Send your
        reference and the exact corrected spelling to <a href="mailto:%s">%s</a>.</p></div>
    </div>

    <p class="center" style="margin-top:2rem;color:var(--ink-3);font-size:.93rem">
      Want to check the booking itself rather than the order? You do not need us for that. You can
      <a href="%s">verify the PNR on the airline&rsquo;s own site</a>.</p>
  </div>
</section>
""" % (c_html, EMAIL, EMAIL, DELIVERY, EMAIL, EMAIL, url("verify-pnr"))

    # noindex: a status lookup has no search value and would read as thin content
    add_page("login", "Check Your Order Status | " + BRAND,
             "Track a flight reservation or hotel booking order using your reference number.",
             body, schema=[c_schema], noindex=True, priority="0.2",
             extra_js=("assets/js/checkout.js",))
