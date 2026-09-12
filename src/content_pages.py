# -*- coding: utf-8 -*-
"""Pages reached from the top menu: bulk orders, special visas, order status."""

import re

from build import (ICON, BRAND, EMAIL, DELIVERY, WHATSAPP,
                   money, add_page, url, faq_block, faq_schema, crumbs, cta_band,
                   asset)
import content_core


WA_DIGITS = re.sub(r"[^0-9]", "", WHATSAPP)


def build():
    bulk_page()
    special_visas_page()
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
        <p>Name and date fixes at half price, however many come back from an embassy in a busy week.</p></div>
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
def special_visas_page():
    """Long-stay routes that are not tourist visas.

    Deliberately priceless. The UAE fee schedule is published per duration and
    changes; Indonesia's depends on the index and the guarantor. Quoting either
    here would date the page within a quarter and invite an argument at the
    counter, so both sections point at the issuing authority instead.
    """
    c_html, c_schema = crumbs([("Special visas", None)])

    # Built outside the format string below, so the percent-encoding in the
    # prefilled message cannot be read as a placeholder.
    wa_uae = ("https://wa.me/" + WA_DIGITS +
              "?text=Hi%2C%20I%20want%20to%20ask%20about%20the%20UAE%20job%20seeker%20visa")
    wa_kitas = ("https://wa.me/" + WA_DIGITS +
                "?text=Hi%2C%20I%20want%20to%20ask%20about%20a%20KITAS%20for%20Indonesia")
    # Every "Get a quote" here goes to WhatsApp rather than the consultation
    # page: there is no price to show yet, so a page of three plans would
    # answer a question the reader did not ask.
    wa_quote = ("https://wa.me/" + WA_DIGITS +
                "?text=Hi%2C%20I%20would%20like%20a%20quote%20for%20a%20special%20visa%20application")

    faqs = [
        ("Do I need a job offer for the UAE job seeker visa?",
         "<p>No, and that is the whole point of it. The UAE grants this one without a host or sponsor in the country. What you do need is the qualification, a bachelor&rsquo;s degree or equivalent, and the financial guarantee the authority asks for.</p>"),
        ("Can I start work on a UAE job seeker visa?",
         "<p>No. It is a visit visa. You can look, interview and negotiate on it, but before you start a job your employer has to move you onto a work permit and a residence visa, which is a separate process with its own cost and timeline.</p>"),
        ("How long does the UAE job seeker visa last?",
         "<p>You choose 30 or 60 days when you apply, and it is issued for one trip. The issuing authority can extend it, as long as your total stay does not run past 180 days.</p>"),
        ("What is the difference between VITAS, ITAS and KITAS?",
         "<p>Three names for three stages of the same journey. VITAS is the limited stay visa you apply for before you travel. ITAS is the limited stay permit you hold once you have arrived. KITAS is the physical card for that permit. Most of the confusion online comes from people using all three interchangeably.</p>"),
        ("Which Indonesian permit works without a local sponsor?",
         "<p>E33G, the remote worker index. It needs an employment contract with a company established outside Indonesia and an annual income of at least US$60,000, but no Indonesian guarantor. Every other common index expects one: an employer, a spouse or an institution.</p>"),
        ("Can I work in Indonesia on the remote worker permit?",
         "<p>Only for your employer abroad. E33G specifically bars you from selling goods or services inside Indonesia and from taking wages from an Indonesian company or person. The income has to come from outside.</p>"),
        ("Do you handle these applications, or just advise on them?",
         "<p>We handle them. Eligibility check, forms, document list, attestation sequencing, the flight and hotel bookings the file needs, and lodging the application itself. You can buy either of these from us outright rather than assembling it yourself.</p>"),
        ("What does it cost?",
         "<p>It depends on the route, the duration and, for Indonesia, the index and the guarantor, so we quote per case rather than publishing a number that would be wrong for most people. Send us your situation on WhatsApp and you will get a figure back.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="center" style="margin-bottom:2.6rem">
      <p class="eyebrow">Special visas</p>
      <h1 data-type>We provide Special visas for UAE &amp; Indonesia</h1>
      <p class="lede">Most visa services stop at the tourist visa. We handle the two that people keep
      asking us for afterwards: the UAE permit that lets you job-hunt on the ground with no employer behind
      you, and the Indonesian permit that turns a few weeks in Bali into a year. We take both of these on
      end to end.</p>
      <div class="btn-row" style="justify-content:center;margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Get a quote</a>
        <a class="btn btn--ghost btn--lg" href="#indonesia-kitas">Jump to KITAS</a>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;align-items:center">%s</div>
  </div>
</section>

<section class="band" id="uae-job-seeker">
  <div class="wrap">
    <img class="vhero" src="%s" srcset="%s 640w, %s 1100w"
         sizes="(max-width:640px) 100vw, 1100px" alt="" width="1100" height="340"
         loading="lazy" decoding="async">
    <h2 style="margin-top:2rem">UAE job seeker visit visa</h2>
    <p class="lede">Come and look for work without an employer behind you. No host, no sponsor, no
    offer letter needed before you fly. It buys you time on the ground rather than the right to start a job,
    and that distinction is the one that catches people out. We apply for this one on your behalf.</p>

    <div class="grid g2" style="margin-top:2.4rem">
      <div class="card">
        <div class="card__ico">%s</div>
        <h3>Who qualifies</h3>
        <p>All of the following, not one of them:</p>
        <ul>
          <li>A <strong>bachelor&rsquo;s degree</strong> or its equivalent.</li>
          <li>Either a profession in <strong>MOHRE skill level 1, 2 or 3</strong>, or a degree from a
              <strong>top-500 world university</strong> awarded in the last two years.</li>
          <li>The <strong>financial guarantee</strong> in force when you apply.</li>
        </ul>
      </div>
      <div class="card">
        <div class="card__ico">%s</div>
        <h3>How long you get</h3>
        <ul>
          <li><strong>30 or 60 days</strong>, chosen at the point you apply.</li>
          <li>Issued for <strong>one trip</strong>, not multiple entries.</li>
          <li>Extendable by the issuing authority, provided the total stay does
              <strong>not exceed 180 days</strong>.</li>
        </ul>
        <p style="font-size:.95rem;color:var(--ink-2)">Apply through ICP smart services, or GDRFA if you are
        going through Dubai.</p>
      </div>
    </div>

    <h3 style="margin-top:2.6rem">What the file needs, and what we put in it</h3>
    <ul>
      <li>Passport valid more than <strong>six months</strong>.</li>
      <li>Colour photograph on a white background.</li>
      <li><strong>Attested</strong> qualification certificate.</li>
    </ul>

    <h3 style="margin-top:2.6rem">Where people come unstuck</h3>
    <div class="grid g2">
      <div class="card"><h3>Treating it as a work permit</h3>
        <p>It is a visit visa. Interviewing is fine. Starting work is not, until your employer has converted
        you onto a work permit and residence visa.</p></div>
      <div class="card"><h3>Leaving attestation until last</h3>
        <p>The degree is no use unattested, and attestation runs through your university, then the MEA in
        India, then the UAE embassy. Start it weeks before you plan to fly.</p></div>
      <div class="card"><h3>Forgetting it is single entry</h3>
        <p>A weekend in Muscat in the middle of your job hunt does not pause the permit. It ends it.</p></div>
      <div class="card"><h3>Expecting a published bank figure</h3>
        <p>There is no fixed number on the portal. The guarantee is assessed, and a balance that has been
        there a while reads better than a deposit made the week before.</p></div>
    </div>

    <p style="margin-top:2rem;font-size:.94rem;color:var(--ink-3)">Source: the
    <a href="https://u.ae/en/information-and-services/visa-and-emirates-id/Types-of-visas/Visit-visa/jobseeker-visit-visa"
       rel="nofollow noopener" target="_blank">official UAE government portal</a>.
    Durations and fees are set by ICP and GDRFA and have been revised more than once, so confirm the
    current options there before you apply rather than relying on any third-party page, including this
    one.</p>

    <div class="btn-row" style="margin-top:1.8rem">
      <a class="btn btn--wa btn--lg" href="%s">%s Start a UAE application</a>
    </div>
  </div>
</section>

<section id="indonesia-kitas">
  <div class="wrap">
    <img class="vhero" src="%s" srcset="%s 640w, %s 1100w"
         sizes="(max-width:640px) 100vw, 1100px" alt="" width="1100" height="340"
         loading="lazy" decoding="async">
    <h2 style="margin-top:2rem">Indonesia: KITAS, the limited stay permit</h2>
    <p class="lede">KITAS is the card. ITAS, <em>Izin Tinggal Terbatas</em>, is the permit it stands for. And
    the thing you actually apply for first is a VITAS, a limited stay visa in the index E series. People use
    all three names for the same journey, which is where most of the confusion online starts.</p>

    <h3 style="margin-top:2.4rem">How it works now</h3>
    <ol>
      <li>Apply online for the limited stay visa before you travel, under the index that matches your reason
          for being there.</li>
      <li>Land. If the application is in order, the electronic permit (e-ITAS) and your re-entry permit are
          issued at the immigration checkpoint.</li>
      <li>Collect the physical KITAS card from an immigration office if you want one.</li>
    </ol>

    <h3 style="margin-top:2.6rem">The indexes people ask about</h3>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Index</th><th>What it covers</th></tr></thead>
        <tbody>
          <tr><td><b>E23</b></td><td>Employment with an Indonesian company</td></tr>
          <tr><td><b>E28A</b></td><td>Investors and directors of a PT PMA</td></tr>
          <tr><td><b>E31A</b></td><td>Family: spouse of an Indonesian citizen</td></tr>
          <tr><td><b>E33F</b></td><td>Older applicants staying on a retirement basis</td></tr>
          <tr><td><b>E33G</b></td><td>Remote work for an employer outside Indonesia</td></tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:1.2rem">Most of these need an Indonesian guarantor behind them: a company, a spouse,
    an institution. <strong>E33G is the exception</strong>, and that is exactly why it is the one remote
    workers ask about.</p>

    <div class="card" style="margin-top:2rem">
      <div class="card__ico">%s</div>
      <h3>E33G, the remote worker index, in detail</h3>
      <ul>
        <li>An employment contract with a company <strong>established outside Indonesia</strong>.</li>
        <li>Annual income of at least <strong>US$60,000</strong>.</li>
        <li>Bank statements for the <strong>last three months</strong> showing at least US$2,000.</li>
        <li>Passport valid at least six months.</li>
        <li>Grants <strong>one year</strong> of stay, and the visa itself has to be used within
            <strong>90 days</strong> of being issued.</li>
        <li><strong>No sponsor or guarantor.</strong></li>
      </ul>
      <p style="font-size:.95rem;color:var(--ink-2)">What it does not allow: selling goods or services inside
      Indonesia, or taking wages from an Indonesian company or person. The money has to come from abroad.</p>
    </div>

    <div class="note note--warn" style="margin-top:2rem">
      <strong>The visa-on-arrival version is not the same thing</strong>
      A limited stay permit issued to someone who arrived on a visa on arrival is capped at 30 days and cannot
      be extended. Applying for the VITAS before you travel is what gets you the year. If you are already in
      Indonesia and reading this, that distinction is probably why.
    </div>

    <h3 style="margin-top:2.6rem">Where people come unstuck</h3>
    <div class="grid g2">
      <div class="card"><h3>Missing the conversion window</h3>
        <p>VITAS holders report to the immigration office and convert within 30 days of arrival. The
        electronic system does much of it automatically now, but the deadline is still the deadline.</p></div>
      <div class="card"><h3>Letting the visa expire unused</h3>
        <p>An issued limited stay visa has a window to be used. Miss it and you are applying again, from the
        start, having already paid.</p></div>
      <div class="card"><h3>Working outside your index</h3>
        <p>The index defines what you may do. Picking up local paid work on a permit that does not cover it is
        the most common way people lose one.</p></div>
      <div class="card"><h3>Assuming a KITAS is permanent</h3>
        <p>It is a <em>limited</em> stay permit, renewed on a cycle. KITAP, the permanent one, is a separate
        thing you arrive at later.</p></div>
    </div>

    <p style="margin-top:2rem;font-size:.94rem;color:var(--ink-3)">Source: the
    <a href="https://www.imigrasi.go.id/" rel="nofollow noopener" target="_blank">Directorate General of
    Immigration</a> and the <a href="https://evisa.imigrasi.go.id/" rel="nofollow noopener"
    target="_blank">official Indonesian e-visa site</a>. Fees depend on the index and the guarantor, so take
    them from there.</p>

    <div class="btn-row" style="margin-top:1.8rem">
      <a class="btn btn--wa btn--lg" href="%s">%s Start a KITAS application</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>We do the whole thing</h2>
      <p class="lede">You do not have to work either of these out on your own. We take the application from
      the eligibility check through to lodging it, and the flights and hotels the file needs come from us
      too, already reconciled against your dates.</p>
    </div>
    <div class="grid g3">
      <div class="card"><div class="card__ico">%s</div><h3>Eligibility checked first</h3>
        <p>We confirm which skill level or index you actually qualify under before you spend a rupee on
        attestation or translation. Sometimes the answer is a different route, and it is cheaper to hear that
        now.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>The file built for you</h3>
        <p>Forms completed, documents listed in the order they are wanted, attestation sequenced so it is not
        the thing that delays you, and the flight and hotel bookings issued with a PNR you can verify.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Lodged and followed through</h3>
        <p>We submit it and stay with it, and you hear from us when something moves instead of refreshing a
        portal and guessing.</p></div>
    </div>
    <p class="center" style="margin-top:2rem">
      <a class="btn btn--primary btn--lg" href="%s">Get a quote for your case</a></p>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
"""

    args = (
        c_html,
        wa_quote,
        content_core.TRUSTLINE,
        # UAE
        asset("assets/img/countries/uae-wide-sm.jpg", bust=True),
        asset("assets/img/countries/uae-wide-sm.jpg", bust=True),
        asset("assets/img/countries/uae-wide.jpg", bust=True),
        ICON["award"], ICON["clock"],
        wa_uae, ICON["whatsapp"],
        # Indonesia
        asset("assets/img/countries/indonesia-wide-sm.jpg", bust=True),
        asset("assets/img/countries/indonesia-wide-sm.jpg", bust=True),
        asset("assets/img/countries/indonesia-wide.jpg", bust=True),
        ICON["globe"],
        wa_kitas, ICON["whatsapp"],
        # where we come in
        ICON["search"], ICON["doc"], ICON["seal"],
        wa_quote,
        faq_block(faqs, "Special visa questions"),
        cta_band("Not sure which route you qualify for?",
                 "Send us what you have. We will tell you which index or skill level fits, quote you for "
                 "handling it, and take it from there.",
                 primary=("Get a quote", wa_quote),
                 secondary=("See all visa guides", "visa")),
    )
    body = body % args

    add_page("special-visas",
             "Special Visas | UAE Job Seeker Visa and Indonesia KITAS",
             "We handle the UAE job seeker visit visa and Indonesia's KITAS limited stay permit end to "
             "end: eligibility check, the full file, the flights and hotels it needs, and lodging it. "
             "Quoted per case.",
             body, schema=[c_schema, faq_schema(faqs)],
             priority="0.8", changefreq="monthly")


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
