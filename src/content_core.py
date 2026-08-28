# -*- coding: utf-8 -*-
"""Core pages: home, services, pricing, process, trust, legal."""

from build import (ICON, BRAND, EMAIL, DELIVERY, SITE_URL, TODAY,
                   PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH, PRICE_RUSH, CURRENCY, CURRENCY_CODE,
                   SINCE_YEAR, FLIGHTS_BOOKED, VISAS_HELPED, AIRLINE_COUNT, WHATSAPP,
                   IATA_ACCREDITED, IATA_NUMBER,
                   money, add_page, url, abs_url, ticket, faq_block, faq_schema,
                   crumbs, cta_band, pricing_tickets,
                   stat_bar, trust_cards, airline_strip, iata_badge,
                   booking_widget, trust_section, highlights, feature_cards)


# ==========================================================================
# shared fragments
# ==========================================================================
BOARDING_PASS = """
<div class="pass" role="img" aria-label="Example of a flight reservation document showing passenger name, route, dates and a live PNR">
  <div class="pass__top"><span>Flight reservation</span><span>Visa purposes</span></div>
  <div class="pass__body">
    <div class="pass__row">
      <div class="pass__f"><span>Passenger</span><b>SURNAME / GIVEN NAME</b></div>
      <div class="pass__f"><span>Class</span><b>Economy</b></div>
    </div>
    <div class="pass__route">
      <span class="ticket__iata">DEL</span>
      <span class="ticket__plane">%s</span>
      <span class="ticket__iata">CDG</span>
    </div>
    <div class="pass__row" style="margin-bottom:0">
      <div class="pass__f"><span>Departure</span><b>14 Sep</b></div>
      <div class="pass__f"><span>Return</span><b>28 Sep</b></div>
      <div class="pass__f"><span>Carrier</span><b>Air France</b></div>
    </div>
  </div>
  <div class="pass__foot">
    <div><span style="display:block;font-size:.62rem;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-3);margin-bottom:4px">Booking reference</span>
      <span class="pnr-chip">K7QX2M</span></div>
    <span class="verified">%s Verifiable on the airline site</span>
  </div>
</div>""" % (ICON["plane"], ICON["check"])


TRUSTLINE = """
<div class="trustline">
  <b>%s Live PNR you can check yourself</b>
  <b>%s Delivered in %s</b>
  <b>%s No airline payment required</b>
  <b>%s Money-back guarantee</b>
</div>
<div style="margin-top:1.2rem">%s</div>""" % (
    ICON["check"], ICON["check"], DELIVERY, ICON["check"], ICON["check"], iata_badge())


def steps_block(steps, heading="How it works"):
    out = ""
    for i, (t, d) in enumerate(steps, 1):
        out += ('<div class="step"><div class="num">%d</div><h3>%s</h3><p>%s</p></div>' % (i, t, d))
    return '<h2>%s</h2><div class="steps">%s</div>' % (heading, out) if heading else '<div class="steps">%s</div>' % out


ORDER_STEPS = [
    ("Tell us your route", "Enter the cities, your travel dates and your name exactly as it is printed in your passport. Two minutes, no account needed."),
    ("We hold a real booking", "We place a genuine reservation in a live airline or hotel system. That booking generates a real reference code. A PNR."),
    ("You get the PDF", "An embassy-ready itinerary lands in your inbox within %s, showing the airline, flight numbers, dates and the PNR." % DELIVERY),
    ("You verify it yourself", "Check the PNR on the airline&rsquo;s own &lsquo;manage booking&rsquo; page before you submit. What you can verify, a visa officer can verify."),
]


# ==========================================================================
def build():
    home()
    flight_page()
    hotel_page()
    combo_page()
    onward_page()
    pricing_page()
    how_it_works()
    verify_page()
    order_page()
    thank_you()
    faq_page()
    about_page()
    contact_page()
    terms_page()
    privacy_page()
    refund_page()


# --------------------------------------------------------------------------
def home():
    home_faqs = [
        ("What is a visa flight ticket?",
         "<p>A visa flight ticket. Also called a flight reservation, dummy ticket or flight itinerary. Is a genuine airline booking held in your name that has <strong>not been paid for</strong>. It carries a real booking reference (PNR) that a consulate can look up, and it proves your intended travel dates and route without forcing you to buy a ticket before your visa is decided.</p>"),
        ("Is it legal to use a flight reservation instead of a paid ticket?",
         "<p>Yes, as long as the reservation is real. Embassies want <em>proof that you intend to travel</em>, not proof that you have paid. The European Commission&rsquo;s own guidance tells applicants not to buy non-refundable tickets before a decision. What is <strong>not</strong> legal is submitting a forged or edited PDF that has no live booking behind it. That is document fraud. Every itinerary we issue is backed by an actual reservation you can verify.</p>"),
        ("How fast will I get my ticket?",
         "<p>Usually within %s. If your appointment is tomorrow morning, tick priority at checkout and put the time in the notes. We will work to it.</p>" % DELIVERY),
        ("How long does the reservation stay valid?",
         "<p>Airline hold periods vary by carrier and route, typically 48 hours to 14 days. We time your booking so it is live on the day you submit, and we will reissue it free of charge if your appointment moves.</p>"),
        ("Do you also provide hotel bookings?",
         "<p>Yes. A confirmed hotel booking in your name with a reference number, for %s, or bundled with your flight reservation for %s. Most consulates ask for both.</p>" % (money(PRICE_HOTEL), money(PRICE_BOTH))),
        ("What if my visa is refused?",
         "<p>Nothing happens to your money, which is rather the point. You never paid the airline, so there is no ticket to cancel and nobody to chase for a refund. Our own fee is small and non-refundable once the booking is issued. See the <a href=\"%s\">refund policy</a>.</p>" % url("refund-policy")),
    ]

    body = """
<section class="hero">
  <div class="wrap">
    <div class="hero__grid">
      <div>
        <p class="eyebrow">Flight &amp; hotel proof for visa files</p>
        <h1>A verifiable flight ticket for your visa. Without buying the flight</h1>
        <p class="lede">We issue real, airline-held reservations with a live PNR that you and the consulate can
        check on the airline&rsquo;s own website. Embassy-ready PDF in %s, from %s.</p>
        <div class="btn-row">
          <a class="btn btn--primary btn--lg" href="%s">Get my flight ticket at %s</a>
          <a class="btn btn--ghost btn--lg" href="%s">See how it works</a>
        </div>
        <div class="hero__seal">%s</div>
      </div>
      <div>%s</div>
    </div>
    %s
    %s
  </div>
</section>

<section class="band tight">
  <div class="wrap">%s</div>
</section>

<section class="tight">
  <div class="wrap">%s</div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.6rem">
      <h2>Pick the proof your consulate asked for</h2>
      <p class="lede">All three land the same day. Prices are per traveller and that is the whole price.</p>
    </div>
    %s
    <p class="center" style="margin-top:1.6rem;color:var(--ink-3);font-size:.92rem">
      Need it inside the hour? Priority handling is +%s at checkout.</p>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>So what is a &ldquo;dummy ticket&rdquo;, really?</h2>
    <p>A dummy ticket is a <strong>flight reservation that has been created in a real airline booking system but not
    paid for</strong>. The airline holds the seat for a fixed window and issues a booking reference. A six-character
    PNR such as <code>K7QX2M</code>. The document you receive shows exactly what a paid ticket shows: passenger name,
    airline, flight numbers, dates, times and that reference. The only thing missing is the payment.</p>
    <p>That is precisely what a visa officer wants to see. They need evidence that you have planned a specific trip,
    entering and leaving on specific dates. They do <em>not</em> want you thousands of dollars out of pocket on a
    non-refundable fare before they have made a decision.</p>
    <div class="note note--warn">
      <strong>The line that matters</strong>
      A reservation that exists in an airline system is legitimate. A PDF that was designed in Photoshop to look like
      one is forgery, and consulates check. Everything we send you can be verified on the carrier&rsquo;s own site.       <a href="%s">here is how to check it</a> before you submit.
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    %s
    <div class="center" style="margin-top:2.4rem">
      <a class="btn btn--primary btn--lg" href="%s">Start my order</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Three things people confuse constantly</h2>
    <p class="lede">Only one of them is both safe and cheap, and it is not the one most people reach for first.</p>
    <div class="tbl-wrap" style="margin-top:1.6rem">
      <table>
        <thead><tr><th>&nbsp;</th><th>Flight reservation<br><small>what we issue</small></th><th>Fully paid ticket</th><th>Edited / fake PDF</th></tr></thead>
        <tbody>
          <tr><td><b>Exists in the airline system</b></td><td class="yes">Yes</td><td class="yes">Yes</td><td class="no">No</td></tr>
          <tr><td><b>PNR verifies on the airline site</b></td><td class="yes">Yes</td><td class="yes">Yes</td><td class="no">No</td></tr>
          <tr><td><b>Typical cost</b></td><td><b>%s</b></td><td>&#8377;35,000 &ndash; &#8377;1,50,000</td><td>&#8377;0 &ndash; &#8377;500</td></tr>
          <tr><td><b>Money at risk if the visa is refused</b></td><td class="yes">None</td><td class="no">The full fare</td><td class="yes">None</td></tr>
          <tr><td><b>Risk of a fraud finding</b></td><td class="yes">None</td><td class="yes">None</td><td class="no">Refusal + multi-year ban</td></tr>
          <tr><td><b>Accepted for visa filing</b></td><td class="yes">Yes</td><td class="yes">Yes</td><td class="no">Until it is checked</td></tr>
        </tbody>
      </table>
    </div>
    <p style="margin-top:1.2rem;color:var(--ink-2);font-size:.95rem">Read the long version:
    <a href="%s">flight reservation vs confirmed ticket vs dummy ticket</a>.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>The four things an officer actually looks at</h2>
      <p class="lede">None of them are subjective. All four are things you can check yourself in ten minutes.</p>
    </div>
    <div class="grid g4">
      <div class="card"><div class="card__ico">%s</div><h3>Live, checkable PNR</h3><p>Not a screenshot. A reference the officer can type into the carrier&rsquo;s site while your file is open.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Name matched to passport</h3><p>Surname and given names in passport order. A mismatch is one of the most common reasons a file gets returned.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Entry and exit both shown</h3><p>Schengen and most tourist visas want a return or onward leg, not a one-way hope.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Timed to your appointment</h3><p>We set the booking window around your submission date, and reissue free if the date moves.</p></div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Visa-specific guides</h2>
    <p class="lede">Fees, steps, hold periods and the specific ways each application goes wrong. Pick your destination.</p>
    <ul class="pills" style="margin-top:1.6rem">%s</ul>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    %s
  </div>
</section>

%s
""" % (DELIVERY, money(PRICE_FLIGHT), url("order"), money(PRICE_FLIGHT), url("how-it-works"),
       iata_badge(), booking_widget(), highlights(), stat_bar(),
       feature_cards(),
       airline_strip(),
       pricing_tickets(), money(PRICE_RUSH),
       url("verify-pnr"),
       steps_block(ORDER_STEPS, "From order to embassy-ready PDF"), url("order"),
       money(PRICE_FLIGHT), url("blog/flight-reservation-vs-confirmed-ticket"),
       ICON["shield"], ICON["doc"], ICON["globe"], ICON["clock"],
       _visa_pills(),
       faq_block(home_faqs, "Visa flight ticket: common questions"),
       cta_band())

    service = {
        "@type": "Service",
        "@id": SITE_URL + "/#service",
        "name": "Flight reservation and hotel booking for visa applications",
        "serviceType": "Travel document service",
        "provider": {"@id": SITE_URL + "/#organization"},
        "areaServed": {"@type": "Place", "name": "Worldwide"},
        "description": "Verifiable, airline-held flight reservations with a live PNR and confirmed hotel bookings, issued for visa applications and delivered within %s." % DELIVERY,
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": CURRENCY_CODE,
            "lowPrice": str(PRICE_HOTEL),
            "highPrice": str(PRICE_BOTH),
            "offerCount": "3",
        },
    }
    webpage = {
        "@type": "WebPage",
        "@id": abs_url() + "#webpage",
        "url": abs_url(),
        "name": "Visa Flight Ticket - Verifiable Flight Reservation for Visa",
        "isPartOf": {"@id": SITE_URL + "/#website"},
        "about": {"@id": SITE_URL + "/#service"},
        "datePublished": TODAY,
        "dateModified": TODAY,
    }

    add_page(
        "",
        "Visa Flight Ticket | Verifiable Flight Reservation for Visa in %s" % DELIVERY,
        "Get a verifiable flight ticket for your visa application from %s. Real airline-held reservation with a live PNR, hotel bookings from %s, delivered in %s." % (money(PRICE_FLIGHT), money(PRICE_HOTEL), DELIVERY),
        body,
        schema=[webpage, service, faq_schema(home_faqs)],
        og_title="Verifiable flight ticket for your visa - live PNR, %s" % money(PRICE_FLIGHT),
        priority="1.0", changefreq="weekly", extra_js=("assets/js/airports.js",),
    )


def _visa_pills():
    import content_visa
    return "".join('<li><a href="%s">%s</a></li>' % (url("visa/" + s), l)
                   for l, s in content_visa.link_list())


# --------------------------------------------------------------------------
def flight_page():
    slug = "flight-reservation-for-visa"
    c_html, c_schema = crumbs([("Flight reservation for visa", None)])

    faqs = [
        ("Will the embassy accept a flight reservation that is not paid for?",
         "<p>Yes. Consulates ask for a flight <em>reservation</em> or <em>itinerary</em> precisely so applicants do not have to buy tickets before a decision. Schengen, UK, Canadian, Australian and most other missions accept an unpaid reservation with a valid booking reference. The one thing they will not accept is a document that does not correspond to a real booking.</p>"),
        ("Can I verify the PNR myself before I submit?",
         "<p>You should. Open the airline&rsquo;s &lsquo;Manage booking&rsquo; page, enter the six-character PNR and your surname, and the itinerary appears. Our <a href=\"%s\">step-by-step verification guide</a> covers the major carriers.</p>" % url("verify-pnr")),
        ("How long is the reservation held?",
         "<p>Between 48 hours and 14 days depending on the airline, the route and how far ahead you are travelling. We schedule your booking so it is live on your submission date. If the consulate keeps your file for weeks, that is normal. Officers check the PNR when they open the file, not months later, and by then you will usually have bought a real ticket anyway.</p>"),
        ("Can you do multi-city or one-way itineraries?",
         "<p>Yes. One-way, return, open-jaw and multi-city are all available at the same price. For a Schengen application you almost always want a return or onward leg; for <a href=\"%s\">proof of onward travel</a> at check-in, a one-way onward booking is usually what is required.</p>" % url("proof-of-onward-travel")),
        ("What if I spelled my name wrong?",
         "<p>Tell us and we will reissue it once, free. Names must match your passport exactly: surname and given names in the same order and spelling as the machine-readable zone. This is the single most common cause of a returned file.</p>"),
        ("Do you cover every airline?",
         "<p>We book on the carrier that actually serves your route, using live availability. If a specific airline is required for your application, and some consulates do note a preferred national carrier, tell us in the order notes and we will match it where the route allows.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="hero__grid" style="align-items:flex-start">
      <div>
        <p class="eyebrow">From %s per traveller</p>
        <h1>Flight reservation for visa applications</h1>
        <p class="lede">A genuine airline-held itinerary in your name, with a live PNR the consulate can verify on
        the carrier&rsquo;s own website. Delivered as a print-ready PDF in %s.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--primary btn--lg" href="%s">Order at %s</a>
          <a class="btn btn--ghost btn--lg" href="%s">How verification works</a>
        </div>
        %s
      </div>
      <div>%s</div>
    </div>
    %s
  </div>
</section>

<section class="tight">
  <div class="wrap">%s</div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2>What you receive</h2>
    <p>One PDF, formatted the way consular officers expect to see an itinerary, containing:</p>
    <ul>
      <li><strong>Passenger name</strong> exactly as printed in your passport, surname first.</li>
      <li><strong>Booking reference (PNR)</strong>: a live six-character code, not a placeholder.</li>
      <li><strong>Airline and flight numbers</strong> for every leg, with operating carrier where it differs.</li>
      <li><strong>Departure and arrival airports, dates and local times</strong>, including layovers.</li>
      <li><strong>Issue date and travel agency details</strong>, so the document has a traceable origin.</li>
    </ul>
    <p>No watermark, no &ldquo;sample&rdquo; overlay, no branding of ours on the itinerary itself.</p>
    <div class="note note--ok">
      <strong>Verify before you file</strong>
      Every order arrives with a one-line instruction for checking your specific airline. Take thirty seconds and do it.
      A reservation you have personally confirmed is a document you can defend at the counter.
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    %s
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>When you need one</h2>
    <div class="grid g3" style="margin-top:1.6rem">
      <div class="card"><div class="card__ico">%s</div><h3>Tourist visa applications</h3><p>Schengen, UK, US B1/B2, Canada, Australia, Japan, Korea and most e-visa portals ask for a dated itinerary showing entry and exit.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Proof of onward travel</h3><p>Airlines and immigration officers can refuse boarding without evidence you will leave. A held onward booking satisfies it.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Visa extensions and renewals</h3><p>Extension applications frequently require a departure booking on or before the new expiry date.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Student and work permits</h3><p>Many student visa checklists want a provisional travel plan aligned to your course start date.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Employer and sponsor files</h3><p>Sponsorship packs often need a travel plan before the sponsor releases funds.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Insurance quotes</h3><p>Travel insurance for Schengen must cover exact travel dates. The reservation fixes them.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">%s</div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    %s
  </div>
</section>

%s
""" % (c_html, money(PRICE_FLIGHT), DELIVERY, url("order"), money(PRICE_FLIGHT), url("verify-pnr"),
       TRUSTLINE, BOARDING_PASS, stat_bar(),
       trust_cards(),
       steps_block(ORDER_STEPS, "The process, end to end"),
       ICON["globe"], ICON["plane"], ICON["refresh"], ICON["doc"], ICON["users"], ICON["shield"],
       airline_strip(),
       faq_block(faqs, "Flight reservation FAQ"),
       cta_band("Get your flight reservation today",
                "Live PNR, embassy-ready PDF, delivered in %s for %s." % (DELIVERY, money(PRICE_FLIGHT))))

    product = {
        "@type": "Product",
        "name": "Flight reservation for visa application",
        "description": "A genuine, airline-held flight reservation with a live PNR, issued in the traveller's name for visa applications and verifiable on the airline website.",
        "brand": {"@id": SITE_URL + "/#organization"},
        "offers": {
            "@type": "Offer",
            "price": str(PRICE_FLIGHT),
            "priceCurrency": CURRENCY_CODE,
            "availability": "https://schema.org/InStock",
            "url": abs_url("order"),
            "priceValidUntil": "%d-12-31" % (int(TODAY[:4]) + 1),
        },
    }
    add_page(slug,
             "Flight Reservation for Visa | Verifiable Dummy Ticket %s" % money(PRICE_FLIGHT),
             "Order a real flight reservation for your visa application. Live PNR verifiable on the airline site, embassy-ready PDF in %s, %s per traveller." % (DELIVERY, money(PRICE_FLIGHT)),
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.9", changefreq="weekly")


# --------------------------------------------------------------------------
def hotel_page():
    slug = "hotel-booking-for-visa"
    c_html, c_schema = crumbs([("Hotel booking for visa", None)])

    faqs = [
        ("Is a hotel booking really required?",
         "<p>For most tourist visas, yes. Consulates want proof of accommodation for every night you are in the country. Schengen missions are explicit about it. If you are staying with family or friends you normally submit an invitation letter instead, and you do not need a hotel booking at all.</p>"),
        ("Is the booking confirmed or just a hold?",
         "<p>It is a confirmed booking in your name with a reference number, made under a policy that allows free cancellation. That is what makes the price low and the risk zero: the property has the booking, you have the confirmation, and nothing is charged.</p>"),
        ("Can the booking cover several cities?",
         "<p>Yes. Multi-city Schengen trips need accommodation covering every night. Tell us your city-by-city plan in the order notes and we will issue one booking per city so there are no gaps. Gaps are what officers look for.</p>"),
        ("Will the dates match my flight reservation?",
         "<p>If you order the <a href=\"%s\">flight and hotel bundle</a> we cross-check them automatically: check-in on your arrival date, check-out on your departure date. Mismatched dates between the two documents is a classic avoidable refusal.</p>" % url("flight-and-hotel-package")),
        ("Can I change the hotel or the dates later?",
         "<p>One free amendment is included. Beyond that, a small reissue fee applies. If your appointment is rescheduled, just email us. We treat that as the free change.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">From %s per traveller</p>
      <h1>Hotel booking for visa applications</h1>
      <p class="lede">A confirmed accommodation booking in your name, with a real reference number, covering every
      night of your trip. Issued in %s and cancellable at no cost.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Order hotel booking at %s</a>
        <a class="btn btn--ghost btn--lg" href="%s">Bundle with a flight at %s</a>
      </div>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2 class="sr">Hotel booking options</h2>
    <div class="grid g2">
      %s
      %s
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>What consulates check on an accommodation document</h2>
    <p>Officers are not judging your taste in hotels. They are checking four mechanical things, and a booking fails
    on these far more often than on anything subjective:</p>
    <ol>
      <li><strong>Full coverage.</strong> Every night between arrival and departure must be accounted for. A single
      uncovered night invites the question &ldquo;where were you planning to sleep?&rdquo;</li>
      <li><strong>Name match.</strong> The lead guest must be the applicant, spelled as in the passport.</li>
      <li><strong>A real property with real contact details.</strong> Address and phone number that resolve.</li>
      <li><strong>Date consistency with the flight itinerary.</strong> Check-in should not precede your arrival;
      check-out should not follow your departure.</li>
    </ol>
    <div class="note">
      <strong>Staying with a host?</strong>
      Then you need an invitation letter and proof of the host&rsquo;s address or status, not a hotel booking.
      Submitting both, inconsistently, is worse than submitting one clean document.
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    %s
  </div>
</section>

%s
""" % (c_html, money(PRICE_HOTEL), DELIVERY, url("order"), money(PRICE_HOTEL),
       url("flight-and-hotel-package"), money(PRICE_BOTH), TRUSTLINE,
       ticket("Hotel Booking", "Confirmed accommodation in your name for the exact nights of your stay.",
              money(PRICE_HOTEL),
              ["Confirmed booking + reference number",
               "One booking per city, no gaps",
               "Free cancellation policy",
               "Delivered in %s" % DELIVERY],
              "Order hotel booking", "order", code="HOTEL"),
       ticket("Flight + Hotel", "Both documents, dates cross-checked against each other. What most files need.",
              money(PRICE_BOTH),
              ["Flight reservation with live PNR",
               "Hotel booking for every night",
               "Dates reconciled automatically",
               "One upload-ready PDF pack"],
              "Order the bundle", "order", code="BUNDLE", featured=True, badge="Best value"),
       faq_block(faqs, "Hotel booking FAQ"),
       cta_band("Cover every night of your trip",
                "Confirmed hotel bookings from %s, or bundled with your flight reservation for %s." % (money(PRICE_HOTEL), money(PRICE_BOTH))))

    product = {
        "@type": "Product",
        "name": "Hotel booking for visa application",
        "description": "A confirmed hotel reservation in the applicant's name with a booking reference, covering every night of the trip, issued for visa applications.",
        "brand": {"@id": SITE_URL + "/#organization"},
        "offers": {"@type": "Offer", "price": str(PRICE_HOTEL), "priceCurrency": CURRENCY_CODE,
                   "availability": "https://schema.org/InStock", "url": abs_url("order")},
    }
    add_page(slug,
             "Hotel Booking for Visa | Confirmed Reservation from %s" % money(PRICE_HOTEL),
             "Confirmed hotel booking for your visa application with a real reference number, covering every night. From %s, delivered in %s." % (money(PRICE_HOTEL), DELIVERY),
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.9", changefreq="weekly")


# --------------------------------------------------------------------------
def combo_page():
    slug = "flight-and-hotel-package"
    c_html, c_schema = crumbs([("Flight + hotel package", None)])

    faqs = [
        ("Why bundle them?",
         "<p>Because the two documents are read together. The most common avoidable problem in a visa file is not a missing document. It is two documents that contradict each other. Ordering both from one place means the arrival date on the hotel booking is the arrival date on the flight itinerary, every time.</p>"),
        ("Is it cheaper?",
         "<p>Yes: %s instead of %s bought separately, per traveller.</p>" % (money(PRICE_BOTH), money(PRICE_FLIGHT + PRICE_HOTEL))),
        ("Multi-city trips?",
         "<p>Covered. Give us the city order and the nights in each, and we issue matching flight legs and one hotel booking per city.</p>"),
        ("Family or group applications?",
         "<p>The price is per traveller, and every traveller gets documents in their own name. Add all passengers in one order and we keep the itineraries aligned across the group.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">Save %s &middot; the complete travel-proof pack</p>
      <h1>Flight + hotel package for visa applications</h1>
      <p class="lede">The two documents almost every consulate asks for, issued together and reconciled against each
      other so the dates cannot contradict. %s per traveller, delivered in %s.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Order the bundle at %s</a>
      </div>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap"><h2 class="sr">Package options and pricing</h2>%s</div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>What &ldquo;reconciled&rdquo; means in practice</h2>
    <p>Before your pack is sent, we run four checks that an officer would run:</p>
    <ul>
      <li>Hotel check-in is on or after your flight arrival date, in local time, accounting for overnight legs.</li>
      <li>Hotel check-out is on or before your departure date, not the day after.</li>
      <li>Every night between arrival and departure is covered by an accommodation booking.</li>
      <li>Passenger name and lead guest name are byte-identical, and both match your passport.</li>
    </ul>
    <p>These sound trivial. They are also, consistently, the reasons files come back marked incomplete.</p>
  </div>
</section>

<section class="band">
  <div class="wrap">%s</div>
</section>

<section>
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, money(PRICE_FLIGHT + PRICE_HOTEL - PRICE_BOTH), money(PRICE_BOTH), DELIVERY,
       url("order"), money(PRICE_BOTH), TRUSTLINE,
       pricing_tickets("both"),
       steps_block(ORDER_STEPS, "How the bundle is produced"),
       faq_block(faqs, "Package FAQ"),
       cta_band("One order, both documents, zero contradictions",
                "Flight reservation with a live PNR plus confirmed accommodation for every night. %s per traveller." % money(PRICE_BOTH)))

    product = {
        "@type": "Product",
        "name": "Flight and hotel booking package for visa application",
        "description": "Bundled flight reservation with live PNR and confirmed hotel booking, date-reconciled for visa applications.",
        "brand": {"@id": SITE_URL + "/#organization"},
        "offers": {"@type": "Offer", "price": str(PRICE_BOTH), "priceCurrency": CURRENCY_CODE,
                   "availability": "https://schema.org/InStock", "url": abs_url("order")},
    }
    add_page(slug,
             "Flight + Hotel Booking for Visa | Complete Pack %s" % money(PRICE_BOTH),
             "Flight reservation and hotel booking for your visa application, issued together and date-matched. %s per traveller, delivered in %s." % (money(PRICE_BOTH), DELIVERY),
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.9", changefreq="weekly")


# --------------------------------------------------------------------------
def onward_page():
    slug = "proof-of-onward-travel"
    c_html, c_schema = crumbs([("Proof of onward travel", None)])

    faqs = [
        ("Who actually asks for proof of onward travel?",
         "<p>The airline at check-in, far more often than immigration. Carriers are fined by destination governments when they board a passenger who is later refused entry, so ground staff check for an exit booking on visa-free and visa-on-arrival routes. Immigration officers may also ask on arrival.</p>"),
        ("Does a bus or train booking count?",
         "<p>Usually, if it crosses an international border and is dated within your permitted stay. Airline staff are most comfortable with a flight booking because it is the format their systems display, but a dated international rail or ferry ticket is generally accepted.</p>"),
        ("How long does the onward booking need to be valid?",
         "<p>Only until you have boarded and cleared immigration. That is why buying a full refundable fare for this is an expensive way to solve a check-in-desk problem.</p>"),
        ("Which countries enforce this most?",
         "<p>Commonly reported: the United States, the UK, Indonesia, the Philippines, Thailand, Costa Rica, Panama, Peru, Colombia, Brazil, New Zealand and most Caribbean nations. Enforcement varies by airline and by agent, which is exactly what makes it worth carrying.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">%s &middot; delivered in %s</p>
      <h1>Proof of onward travel</h1>
      <p class="lede">A dated onward or return booking with a live PNR. Enough to satisfy an airline check-in agent
      or a border officer who wants to see that you intend to leave.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Get onward proof at %s</a>
        <a class="btn btn--ghost btn--lg" href="%s">Read the full guide</a>
      </div>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2>Why one-way travellers get stopped</h2>
    <p>Under the carrier-liability rules that most countries operate, an airline that flies in a passenger who is
    refused entry pays to fly them out again, and often pays a fine on top. That cost lands on the airline, not on
    the government, so airlines push the check forward to the departure gate. The agent scanning your passport
    is protecting their employer, not enforcing immigration law.</p>
    <p>The practical consequence: on a one-way ticket to a visa-free destination, you can be denied boarding by an
    airline even though immigration at the other end would have admitted you without a murmur.</p>
    <div class="note note--warn">
      <strong>Do not rely on a screenshot</strong>
      Check-in staff increasingly look the reference up. A held booking with a working PNR takes the conversation
      from thirty seconds of scrutiny to none.
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, money(PRICE_FLIGHT), DELIVERY, url("order"), money(PRICE_FLIGHT),
       url("blog/proof-of-onward-travel-explained"), TRUSTLINE,
       faq_block(faqs, "Onward travel FAQ"),
       cta_band("Board without the argument",
                "A live onward booking for %s, in your inbox within %s." % (money(PRICE_FLIGHT), DELIVERY)))

    add_page(slug,
             "Proof of Onward Travel | Onward Ticket from %s" % money(PRICE_FLIGHT),
             "Need proof of onward travel for check-in or immigration? Get a dated onward booking with a live PNR for %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
             body, schema=[c_schema, faq_schema(faqs)],
             priority="0.8", changefreq="monthly")


# --------------------------------------------------------------------------
def pricing_page():
    slug = "pricing"
    c_html, c_schema = crumbs([("Pricing", None)])

    faqs = [
        ("Is the price per person or per booking?",
         "<p>Per traveller. Four people on one itinerary is four times the per-traveller price, and each person receives a document in their own name.</p>"),
        ("Are there hidden fees?",
         "<p>No. The price you see is the price charged. The only optional extra is priority handling at %s, and you choose it deliberately at checkout.</p>" % money(PRICE_RUSH)),
        ("What payment methods do you take?",
         "<p>Card, PayPal and UPI. Payment is processed by the payment provider. We never see or store your card details.</p>"),
        ("Do you offer agency or bulk rates?",
         "<p>Yes. If you file more than about twenty applications a month. Travel agencies, immigration consultants, universities, employers. Email <a href=\"mailto:%s\">%s</a> for volume pricing and a single monthly invoice.</p>" % (EMAIL, EMAIL)),
        ("Can I get a refund?",
         "<p>If we fail to deliver a working booking, you are refunded in full. Once a valid booking has been issued the fee is non-refundable, because the work is done and the cost is incurred. The <a href=\"%s\">refund policy</a> sets this out precisely.</p>" % url("refund-policy")),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="center">
      <h1>Simple, per-traveller pricing</h1>
      <p class="lede">No subscriptions, no account, no upsells at the end. Every price below includes delivery within %s.</p>
    </div>
    <h2 class="sr">Plans and prices</h2>
    <div style="margin-top:3rem">%s</div>
    <p class="center" style="margin-top:1.8rem;color:var(--ink-3);font-size:.93rem">
      Priority handling (delivery targeted inside 60 minutes, 24/7): <strong>+%s</strong> per order.
    </p>
    <div style="margin-top:2.8rem">%s</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>What is included at every price point</h2>
    <div class="tbl-wrap" style="margin-top:1.6rem">
      <table>
        <thead><tr><th>Included</th><th>Flight %s</th><th>Hotel %s</th><th>Bundle %s</th></tr></thead>
        <tbody>
          <tr><td>Real booking in a live reservation system</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><td>Verifiable reference / PNR</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><td>Embassy-ready PDF, no watermark</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><td>Delivery within %s</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><td>One free name or date correction</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
          <tr><td>Flight and hotel dates reconciled</td><td>&ndash;</td><td>&ndash;</td><td class="yes">Yes</td></tr>
          <tr><td>Priority support until your appointment</td><td>&ndash;</td><td>&ndash;</td><td class="yes">Yes</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>Why this costs %s and a real ticket costs &#8377;75,000</h2>
    <p>Because you are not buying a flight. You are paying for a booking to be created, held and documented in a live
    airline system, and for someone to check that the details on it will survive consular scrutiny. The seat is never
    purchased, so no fare is ever charged. To us or to you.</p>
    <p>That is also why the service is genuinely low-risk. If your visa is refused, there is nothing to cancel, no
    airline refund process to fight, and no non-refundable fare written off. The most you have spent is the fee above.</p>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, DELIVERY, pricing_tickets(), money(PRICE_RUSH), trust_cards(heading=None),
       money(PRICE_FLIGHT), money(PRICE_HOTEL), money(PRICE_BOTH), DELIVERY, money(PRICE_FLIGHT),
       faq_block(faqs, "Pricing FAQ"),
       cta_band())

    add_page(slug,
             "Pricing | Dummy Ticket from %s, Hotel from %s" % (money(PRICE_FLIGHT), money(PRICE_HOTEL)),
             "Flight reservation for visa %s, hotel booking %s, both for %s per traveller. All prices include an embassy-ready PDF delivered in %s." % (money(PRICE_FLIGHT), money(PRICE_HOTEL), money(PRICE_BOTH), DELIVERY),
             body, schema=[c_schema, faq_schema(faqs)],
             priority="0.9", changefreq="weekly")


# --------------------------------------------------------------------------
def how_it_works():
    slug = "how-it-works"
    c_html, c_schema = crumbs([("How it works", None)])

    detail = [
        ("Submit your details", "You need three things: the route, the dates, and your name exactly as it appears in your passport. There is no account to create. If your consular appointment is already booked, tell us the date and we will time the reservation around it."),
        ("We create a live booking", "Your itinerary is entered into a real airline reservation system using live availability on carriers that actually fly your route. The system returns a booking reference. The PNR. This is the same process a travel agent follows before a customer pays; we simply stop before the payment step."),
        ("Quality check", "Before anything is sent, we verify the name against passport conventions, confirm both directions of travel are present, and check the hold window will still be open on your submission date. Bundle orders also get flight-to-hotel date reconciliation."),
        ("Delivery", "The finished PDF is emailed to you, typically within %s. It is formatted as a standard agency itinerary: no watermark, no promotional branding, nothing that signals it came from a third-party service." % DELIVERY),
        ("You verify it", "Open the airline&rsquo;s &lsquo;Manage booking&rsquo; page, enter the PNR and your surname, and see your own itinerary come back. Now you know what the officer will see."),
        ("Free corrections", "Spotted a typo, or has your appointment moved? One reissue is included at no charge. Email us with the order reference."),
    ]

    howto = {
        "@type": "HowTo",
        "name": "How to get a verifiable flight reservation for a visa application",
        "description": "The end-to-end process for obtaining an airline-held flight reservation with a live PNR for a visa application.",
        "totalTime": "PT60M",
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "USD", "value": str(money(PRICE_FLIGHT))},
        "step": [{"@type": "HowToStep", "position": i, "name": t,
                  "text": __import__("re").sub(r"<[^>]+>", "", d),
                  "url": abs_url(slug) + "#step-%d" % i}
                 for i, (t, d) in enumerate(detail, 1)],
    }

    rows = ""
    for i, (t, d) in enumerate(detail, 1):
        rows += ('<div class="card" id="step-%d"><div class="num">%d</div><h3>%s</h3><p>%s</p></div>' % (i, i, t, d))

    faqs = [
        ("Do I need to create an account?", "<p>No. One form, one email address, done.</p>"),
        ("What information do you need from me?",
         "<p>Departure and destination cities, travel dates, and each traveller&rsquo;s full name and date of birth as printed in the passport. Nothing else. We do not ask for passport numbers or scans, because we do not need them.</p>"),
        ("What happens if the airline releases the booking early?",
         "<p>Tell us and we reissue at no cost. Hold windows occasionally close earlier than expected on high-demand routes; that is our problem to fix, not yours.</p>"),
        ("Can I order for someone else?",
         "<p>Yes. Enter their passport details as the traveller and your own email for delivery.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <h1>How it works</h1>
      <p class="lede">Six steps from filling in a form to holding something you have checked yourself. Five of them
      happen without you.</p>
    </div>
  </div>
</section>

<section class="band tight">
  <div class="wrap"><h2 class="sr">The process, step by step</h2>
  <div class="grid g3">%s</div></div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>What we do not do</h2>
    <p>Worth spelling out, because plenty of services in this market are deliberately vague about it.</p>
    <ul>
      <li><strong>We do not generate PDFs.</strong> Nothing is designed to look like a booking. A booking is created,
      and then documented.</li>
      <li><strong>We do not sell fake PNRs.</strong> A code that does not resolve on the airline&rsquo;s website is worse
      than no document at all. It converts an incomplete file into a fraud finding.</li>
      <li><strong>We do not promise visa approval.</strong> Nobody can. We supply one document in a file that also
      contains your finances, your ties, and your history.</li>
      <li><strong>We do not issue tickets.</strong> If you need a paid, ticketed fare with an e-ticket number, buy it
      from the airline after your visa is granted.</li>
    </ul>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, rows, faq_block(faqs, "Process FAQ"),
       cta_band("Two minutes of form-filling", "Then wait %s for the PDF." % DELIVERY))

    add_page(slug, "How It Works | Getting a Verifiable Visa Flight Ticket",
             "How we issue a real, airline-held flight reservation with a live PNR for your visa application, from order form to verified PDF in %s." % DELIVERY,
             body, schema=[c_schema, howto, faq_schema(faqs)],
             priority="0.8", changefreq="monthly")


# --------------------------------------------------------------------------
def verify_page():
    slug = "verify-pnr"
    c_html, c_schema = crumbs([("Verify a PNR", None)])

    steps = [
        ("Find the PNR on your itinerary", "It is a six-character alphanumeric code, printed near the top of the document, usually labelled &lsquo;Booking reference&rsquo;, &lsquo;PNR&rsquo;, &lsquo;Reservation code&rsquo; or &lsquo;Record locator&rsquo;. Example format: <code>K7QX2M</code>."),
        ("Open the operating airline&rsquo;s website", "Use the carrier shown on the first leg. Go to the section called &lsquo;Manage booking&rsquo;, &lsquo;My trips&rsquo; or &lsquo;Check-in&rsquo;. The wording differs, the function does not."),
        ("Enter the PNR and the surname", "Surname only, spelled exactly as on the itinerary. Most systems reject a full name in that field."),
        ("Read what comes back", "A valid reservation returns your itinerary: passenger name, flight numbers, dates, times. That is what a consular officer sees when they run the same check."),
    ]

    howto = {
        "@type": "HowTo",
        "name": "How to verify a flight reservation PNR on an airline website",
        "description": "Four steps to confirm that a flight reservation for a visa application is real and live in the airline system.",
        "totalTime": "PT2M",
        "step": [{"@type": "HowToStep", "position": i, "name": t,
                  "text": __import__("re").sub(r"<[^>]+>", "", d)}
                 for i, (t, d) in enumerate(steps, 1)],
    }

    rows = ""
    for i, (t, d) in enumerate(steps, 1):
        rows += '<div class="card"><div class="num">%d</div><h3>%s</h3><p>%s</p></div>' % (i, t, d)

    faqs = [
        ("My PNR does not come up. What now?",
         "<p>Three ordinary explanations before you assume the worst. First, you may be checking the wrong carrier. On a codeshare, the booking sits with the <em>operating</em> airline, not the one whose flight number is printed. Second, some systems need a few minutes to propagate. Third, the surname field may need the surname alone. If it still fails, email us the order reference and we will reissue.</p>"),
        ("Can a consulate see that the ticket is unpaid?",
         "<p>Yes, and that is fine. A reservation shows a booking status rather than a ticket number. Consulates know the difference and ask for reservations for exactly this reason. They do not want applicants buying fares before a decision.</p>"),
        ("Does checking the booking cancel it?",
         "<p>No. Looking up a reservation is read-only. Just avoid clicking anything labelled cancel, and do not attempt online check-in.</p>"),
        ("How can I tell a fake itinerary from a real one?",
         "<p>Run this exact check. A fabricated document fails at step four: either the code returns nothing, or it returns somebody else&rsquo;s trip. There is no other reliable test. A forged PDF can look perfect.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">Two minutes &middot; free &middot; do this before you file</p>
      <h1>How to verify a flight reservation PNR</h1>
      <p class="lede">One question decides whether a document is real: does the reference come back on the airline&rsquo;s
      own site? Here is how to ask it, on any booking, whether it came from us or from anyone else.</p>
    </div>
  </div>
</section>

<section class="band tight">
  <div class="wrap"><h2 class="sr">How to verify, step by step</h2>
  <div class="grid g4">%s</div></div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>Where to check, by airline</h2>
    <p>Every major carrier exposes the same lookup. Search the airline name plus &ldquo;manage booking&rdquo; and use the
    official domain, never a link forwarded to you by a third party.</p>
    <div class="tbl-wrap">
      <table>
        <thead><tr><th>Airline group</th><th>Where to look</th><th>Fields required</th></tr></thead>
        <tbody>
          <tr><td><b>Emirates, Qatar, Etihad, Turkish</b></td><td>Manage booking / My trips</td><td>PNR + surname</td></tr>
          <tr><td><b>Lufthansa, Swiss, Austrian, Brussels</b></td><td>My bookings</td><td>PNR + surname</td></tr>
          <tr><td><b>Air France, KLM</b></td><td>My bookings</td><td>PNR + surname</td></tr>
          <tr><td><b>British Airways, Iberia</b></td><td>Manage my booking</td><td>PNR + surname</td></tr>
          <tr><td><b>Air India, IndiGo, Vistara</b></td><td>Manage booking / Edit booking</td><td>PNR + surname or email</td></tr>
          <tr><td><b>United, Delta, American</b></td><td>My trips</td><td>Confirmation code + surname</td></tr>
          <tr><td><b>Singapore, Thai, Cathay, ANA, JAL</b></td><td>Manage booking</td><td>PNR + surname</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note note--warn">
      <strong>Codeshare catch</strong>
      If your itinerary says &ldquo;operated by&rdquo; a different airline, check on that airline&rsquo;s site. This accounts for
      most &ldquo;my PNR is not working&rdquo; reports and almost never indicates a real problem.
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, rows, faq_block(faqs, "Verification FAQ"),
       cta_band("Order a reservation you can verify in two minutes",
                "Live PNR, checkable on the carrier&rsquo;s own site, %s per traveller." % money(PRICE_FLIGHT)))

    add_page(slug, "How to Verify a Flight Reservation PNR | Step-by-Step",
             "Check whether a flight reservation for a visa is real: find the PNR, open the airline's manage-booking page, enter the code and surname. Four steps, two minutes.",
             body, schema=[c_schema, howto, faq_schema(faqs)],
             priority="0.8", changefreq="monthly")


# --------------------------------------------------------------------------
def order_page():
    slug = "order"
    c_html, c_schema = crumbs([("Order", None)])

    body = """
<section>
  <div class="wrap">
    %s
    <div class="center" style="margin-bottom:2.4rem">
      <h1>Order your visa travel documents</h1>
      <p class="lede">Two minutes. No account. Delivered to your inbox in %s.</p>
    </div>
    <div class="hero__grid" style="align-items:flex-start">
      <h2 class="sr">Order form</h2>
      <form class="form" id="order-form" novalidate data-cur="%s"
            data-p-flight="%d" data-p-hotel="%d" data-p-both="%d" data-p-rush="%d">
        <fieldset>
          <legend>1 &middot; What do you need?</legend>
          <label class="opt"><input type="radio" name="service" value="flight" checked>
            <span><b>Flight reservation at %s</b><small>Airline-held itinerary with a live PNR</small></span></label>
          <label class="opt"><input type="radio" name="service" value="hotel">
            <span><b>Hotel booking at %s</b><small>Confirmed accommodation with a reference number</small></span></label>
          <label class="opt"><input type="radio" name="service" value="both">
            <span><b>Flight + hotel at %s</b><small>Both, with dates reconciled. Most popular.</small></span></label>
        </fieldset>

        <fieldset>
          <legend>2 &middot; Your trip</legend>
          <div class="row2">
            <div class="field"><label for="from">From (city or airport)</label>
              <input id="from" name="from" type="text" placeholder="Delhi (DEL)" data-airport required></div>
            <div class="field"><label for="to">To (city or airport)</label>
              <input id="to" name="to" type="text" placeholder="Paris (CDG)" data-airport required></div>
          </div>
          <div class="row2">
            <div class="field"><label for="depart">Departure date</label>
              <input id="depart" name="depart" type="date" required></div>
            <div class="field"><label for="return">Return date</label>
              <input id="return" name="return" type="date">
              <span class="hint">Leave empty for a one-way or onward-only booking.</span></div>
          </div>
          <div class="row2">
            <div class="field"><label for="travellers">Travellers</label>
              <select id="travellers" name="travellers">
                <option>1</option><option>2</option><option>3</option><option>4</option>
                <option>5</option><option>6</option><option>7</option><option>8</option>
              </select></div>
            <div class="field"><label for="visa">Applying for which visa?</label>
              <input id="visa" name="visa" type="text" placeholder="Schengen &ndash; France" autocomplete="off"></div>
          </div>
        </fieldset>

        <fieldset>
          <legend>3 &middot; Lead traveller</legend>
          <div class="row2">
            <div class="field"><label for="surname">Surname (as in passport)</label>
              <input id="surname" name="surname" type="text" autocomplete="family-name" required></div>
            <div class="field"><label for="given">Given name(s)</label>
              <input id="given" name="given" type="text" autocomplete="given-name" required></div>
          </div>
          <div class="row2">
            <div class="field"><label for="dob">Date of birth</label>
              <input id="dob" name="dob" type="date"></div>
            <div class="field"><label for="email">Email for delivery</label>
              <input id="email" name="email" type="email" autocomplete="email" required></div>
          </div>
          <div class="field"><label for="phone">Phone or WhatsApp</label>
            <input id="phone" name="phone" type="tel" autocomplete="tel" placeholder="+91 ...">
            <span class="hint">So we can reach you fast if something needs checking.</span></div>
          <div class="field"><label for="notes">Anything we should know?</label>
            <textarea id="notes" name="notes" rows="3" placeholder="Appointment date, multi-city plan, extra travellers, preferred airline&hellip;"></textarea>
            <span class="hint">Additional travellers&rsquo; names can go here.</span></div>
          <label class="opt" style="margin-top:6px"><input type="checkbox" id="rush" name="rush">
            <span><b>Priority handling, +%s</b><small>Targeted inside 60 minutes, 24/7</small></span></label>
        </fieldset>

        <button class="btn btn--primary btn--lg btn--block" type="submit" id="order-submit">
          Continue to payment. <span id="price-out">%s</span></button>
        <p class="hint" style="text-align:center;margin-top:12px" id="price-line"></p>

        <div class="note" id="order-msg" hidden></div>
      </form>

      <aside class="order-aside">
        <div class="card">
          <h3>What happens next</h3>
          <ol style="font-size:.95rem;color:var(--ink-2);padding-left:1.1em">
            <li>You pay the service fee, never an airfare.</li>
            <li>We create the booking in a live reservation system.</li>
            <li>The PDF reaches your inbox in %s.</li>
            <li>You verify the PNR on the airline&rsquo;s site.</li>
          </ol>
        </div>
        <div class="card" style="margin-top:20px">
          <h3>Name spelling matters</h3>
          <p style="font-size:.95rem;color:var(--ink-2)">Copy your surname and given names character-for-character
          from the passport data page. A mismatch is the most common reason a visa file is returned, and the
          easiest to avoid.</p>
        </div>
        <div class="card" style="margin-top:20px">
          <h3>Appointment in under 24 hours?</h3>
          <p style="font-size:.95rem;color:var(--ink-2)">Tick priority handling and put the appointment time in the
          notes. Or email <a href="mailto:%s">%s</a> directly.</p>
        </div>
      </aside>
    </div>
  </div>
</section>
""" % (c_html, DELIVERY, CURRENCY, PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH, PRICE_RUSH,
       money(PRICE_FLIGHT), money(PRICE_HOTEL), money(PRICE_BOTH), money(PRICE_RUSH),
       money(PRICE_FLIGHT), DELIVERY, EMAIL, EMAIL)

    add_page(slug, "Order a Flight Reservation or Hotel Booking for Your Visa",
             "Order a verifiable flight reservation from %s or a hotel booking from %s. No account needed, delivered in %s." % (money(PRICE_FLIGHT), money(PRICE_HOTEL), DELIVERY),
             body, schema=[c_schema], priority="0.9", changefreq="monthly",
             extra_js=("assets/js/airports.js", "assets/js/qr.js", "assets/js/checkout.js"))


def thank_you():
    body = """
<section><div class="wrap wrap--narrow center">
  <p class="eyebrow">Order received</p>
  <h1>Thank you. We are on it</h1>
  <p class="lede">Your documents will arrive at the email address you gave us within %s. If nothing has landed after
  that, check your spam folder first, then email <a href="mailto:%s">%s</a> with your order reference.</p>
  <div class="btn-row" style="justify-content:center;margin-top:2rem">
    <a class="btn btn--primary btn--lg" href="%s">How to verify your PNR</a>
    <a class="btn btn--ghost btn--lg" href="%s">Back to home</a>
  </div>
</div></section>""" % (DELIVERY, EMAIL, EMAIL, url("verify-pnr"), url())
    add_page("order/thank-you", "Thank you | " + BRAND,
             "Your order has been received.", body, noindex=True, priority="0.1",
             extra_js=("assets/js/checkout.js",))


# --------------------------------------------------------------------------
def faq_page():
    slug = "faq"
    c_html, c_schema = crumbs([("FAQ", None)])

    groups = [
        ("The basics", [
            ("What is a dummy ticket?",
             "<p>A flight reservation created in a real airline system and held without payment. It carries a live booking reference (PNR) and shows the same details as a paid ticket: passenger, route, flight numbers and dates, everything except the purchase. &lsquo;Dummy ticket&rsquo; is industry slang; consulates call it a flight reservation or itinerary.</p>"),
            ("Is a dummy ticket the same as a fake ticket?",
             "<p>No, and the distinction is the whole business. A dummy ticket is a real booking that has not been paid for. A fake ticket is a fabricated document with no booking behind it. The first is a normal part of visa filing; the second is fraud.</p>"),
            ("Why not just book a refundable ticket myself?",
             "<p>You can. It ties up tens of thousands of rupees for weeks, refunds take 7&ndash;30 days, and some &lsquo;refundable&rsquo; fares carry cancellation fees that exceed our entire price.</p>"),
            ("Can I use a free reservation-hold from an airline?",
             "<p>Sometimes. A handful of carriers offer 24&ndash;72 hour holds on their own site, free or for a small fee. If your route is served by one of them and your appointment is imminent, that is a perfectly good option. It falls down when you need a longer window, a multi-city itinerary, or a route where no carrier offers holds.</p>"),
        ]),
        ("Acceptance and legality", [
            ("Will my embassy accept this?",
             "<p>Consulates ask for evidence of intended travel and explicitly warn against buying tickets before a decision. A reservation with a verifiable PNR meets that requirement. We cannot speak for any individual officer&rsquo;s discretion, and no honest provider can.</p>"),
            ("Is it legal?",
             "<p>Yes. Holding an unpaid airline reservation is a normal commercial transaction that travel agents perform thousands of times a day. What is illegal is submitting a forged document, which is why every itinerary we issue corresponds to a booking you can look up yourself.</p>"),
            ("Could using one hurt my application?",
             "<p>A genuine reservation, no. A document that fails verification, catastrophically. A fraud finding typically means refusal plus a multi-year bar on future applications. This is the reason to care where the document comes from.</p>"),
            ("Do you guarantee my visa will be approved?",
             "<p>No, and treat any service that does as a warning sign. Your travel documents are one part of a file that also weighs your finances, employment, ties to your home country and immigration history.</p>"),
        ]),
        ("Practical details", [
            ("How quickly do I get it?",
             "<p>Usually within %s. Priority handling targets under 60 minutes at any hour.</p>" % DELIVERY),
            ("How long does the booking stay live?",
             "<p>48 hours to 14 days, depending on carrier and route. We time it to your submission date and reissue free if the date changes.</p>"),
            ("Do you need my passport number?",
             "<p>No. Names and dates of birth are enough to make the booking. We do not ask for passport numbers or scans, which means we cannot lose them.</p>"),
            ("Can I change the dates after delivery?",
             "<p>One free amendment per order. After that a small reissue fee applies.</p>"),
            ("Do you book hotels too?",
             "<p>Yes. %s alone, or %s bundled with a flight reservation, with the dates cross-checked.</p>" % (money(PRICE_HOTEL), money(PRICE_BOTH))),
            ("What if the PNR does not verify?",
             "<p>Email us and we reissue immediately, or refund in full. See the <a href=\"%s\">refund policy</a>.</p>" % url("refund-policy")),
        ]),
    ]

    parts = []
    all_items = []
    for title, items in groups:
        parts.append(faq_block(items, title))
        all_items.extend(items)

    body = """
<section>
  <div class="wrap wrap--narrow">
    %s
    <h1>Frequently asked questions</h1>
    <p class="lede">Everything about flight reservations, hotel bookings and visa documentation. Answered without
    the marketing gloss.</p>
    <div class="stack" style="margin-top:2.4rem">%s</div>
    <p style="margin-top:2rem">Still stuck? <a href="%s">Get in touch</a>. We answer every message.</p>
  </div>
</section>
%s""" % (c_html, "".join('<div style="margin-bottom:2.4rem">%s</div>' % p for p in parts),
         url("contact"), cta_band())

    add_page(slug, "FAQ | Dummy Tickets & Flight Reservations for Visas",
             "Answers on dummy tickets, flight reservations, embassy acceptance, legality, PNR verification, delivery times and refunds.",
             body, schema=[c_schema, faq_schema(all_items)],
             priority="0.8", changefreq="monthly")


# --------------------------------------------------------------------------
def about_page():
    c_html, c_schema = crumbs([("About", None)])
    body = """
<section>
  <div class="wrap wrap--narrow">
    %s
    <h1>About %s</h1>
    <p class="lede">We do one thing, and we would rather do it properly than broadly: travel documents that hold up
    when somebody checks them.</p>
    %s

    <h2>Why this service exists</h2>
    <p>Visa applications hand you a small, annoying puzzle. The consulate wants a flight itinerary. Buying the flight
    first means gambling a real fare on a decision nobody has made yet. So consulates ask for a <em>reservation</em>
    instead, which sounds like the problem is solved, right up until you discover that airlines rarely hold seats for
    free and almost never for long enough.</p>
    <p>That gap is what we fill. We create a genuine booking in a live reservation system, hold it across your
    submission window, and hand you a document you can verify yourself. For the price of a sandwich rather than
    the price of a fare.</p>

    <h2>What we will not do</h2>
    <p>The market around us is not always careful, so we will be explicit.</p>
    <ul>
      <li>We do not fabricate documents. Every itinerary corresponds to a booking that exists.</li>
      <li>We do not sell PNRs that fail to resolve. If yours does not, we reissue or refund. No argument.</li>
      <li>We do not claim to influence visa decisions. We supply a document; officers weigh a file.</li>
      <li>We do not store passport scans or numbers, because the job does not require them.</li>
    </ul>

    <div class="note">
      <strong>Not a government service</strong>
      %s is a private travel-documentation company. We are not affiliated with any embassy, consulate, visa
      application centre or government agency, and we do not provide immigration advice.
    </div>

    <h2>Accreditation</h2>
    <p>We are an <strong>IATA certified travel agent</strong>. That accreditation is what lets us place bookings
    directly in live airline reservation systems rather than scraping a public search page, and it is why the
    references we issue behave exactly like any other agency booking when a consular officer looks them up.
    Our accreditation number is published on this page and can be checked against IATA&rsquo;s own register.</p>
    <p>%s</p>

    <h2>Company details</h2>
    <p>Contact: <a href="mailto:%s">%s</a>. Registered company name, address and registration number will be
    published here in full once incorporation completes. We would rather leave this section visibly unfinished
    than fill it with something unverifiable.</p>
    <p><a href="%s">Contact us</a> &middot; <a href="%s">Terms of service</a> &middot; <a href="%s">Privacy policy</a></p>
  </div>
</section>
%s""" % (c_html, BRAND, stat_bar(), BRAND, iata_badge(), EMAIL, EMAIL, url("contact"),
         url("terms"), url("privacy-policy"), cta_band())

    add_page("about", "About Us | " + BRAND,
             "Who we are: a travel-documentation service issuing verifiable flight reservations and hotel bookings for visa applications. What we do, and what we refuse to do.",
             body, schema=[c_schema], priority="0.5")


def contact_page():
    c_html, c_schema = crumbs([("Contact", None)])
    body = """
<section>
  <div class="wrap wrap--narrow">
    %s
    <h1>Contact us</h1>
    <p class="lede">Real people, and we answer everything. If your appointment is imminent, say so in the first line
    and we will prioritise it.</p>
    <h2 class="sr">How to reach us</h2>
    <div class="grid g2" style="margin-top:2.4rem">
      <div class="card"><div class="card__ico">%s</div><h3>Email</h3>
        <p>The fastest route for order questions, corrections and reissues.</p>
        <p><a class="btn btn--primary" href="mailto:%s">%s</a></p></div>
      <div class="card"><div class="card__ico">%s</div><h3>WhatsApp</h3>
        <p>For urgent, same-day appointments.</p>
        <p><a class="btn btn--wa" href="https://wa.me/%s">%s</a></p></div>
    </div>
    <h2>Before you write</h2>
    <ul>
      <li><strong>PNR not verifying?</strong> Check the <em>operating</em> carrier first. See the
      <a href="%s">verification guide</a>. That solves most cases in a minute.</li>
      <li><strong>Need a correction?</strong> Send the order reference and the exact corrected spelling. One free
      reissue is included.</li>
      <li><strong>Not received anything?</strong> Check spam, then email us. Delivery is normally within %s.</li>
      <li><strong>Agency or bulk enquiry?</strong> Tell us your monthly volume and we will send trade pricing.</li>
    </ul>
    <div class="note note--warn">
      <strong>We cannot give immigration advice</strong>
      We can tell you what document formats consulates typically accept. We cannot tell you whether your application
      will succeed, or advise on your immigration status. For that, speak to a licensed immigration adviser.
    </div>
  </div>
</section>""" % (c_html, ICON["mail"], EMAIL, EMAIL, ICON["chat"],
                 __import__("re").sub(r"[^0-9]", "", WHATSAPP), "Message us on WhatsApp",
                 url("verify-pnr"), DELIVERY)

    contact_schema = {"@type": "ContactPage", "@id": abs_url("contact") + "#page",
                      "url": abs_url("contact"), "name": "Contact " + BRAND,
                      "isPartOf": {"@id": SITE_URL + "/#website"}}
    add_page("contact", "Contact | " + BRAND,
             "Get in touch about an order, a correction, an urgent appointment or agency pricing. We answer every message.",
             body, schema=[c_schema, contact_schema], priority="0.5")


# --------------------------------------------------------------------------
def _legal(slug, h1, title, desc, body_html):
    c_html, c_schema = crumbs([(h1, None)])
    body = """
<section><div class="wrap wrap--narrow">
%s
<h1>%s</h1>
<p class="meta">Last updated: %s</p>
%s
</div></section>""" % (c_html, h1, TODAY, body_html)
    add_page(slug, title, desc, body, schema=[c_schema], priority="0.3", changefreq="yearly")


def terms_page():
    _legal("terms", "Terms of service", "Terms of Service | " + BRAND,
           "The terms governing use of our flight reservation and hotel booking service.", """
<div class="note note--warn"><strong>Template notice</strong>
These terms are a working draft written for a service of this type. Have them reviewed by a lawyer in your
jurisdiction before you take live orders, and replace the bracketed items with your registered details.</div>

<h2>1. Who we are</h2>
<p>%s (&ldquo;we&rdquo;, &ldquo;us&rdquo;) operates this website and supplies travel-documentation services. Registered entity
details: <em>[to be completed on incorporation]</em>. Contact: <a href="mailto:%s">%s</a>.</p>

<h2>2. What we supply</h2>
<p>We create genuine reservations in live airline and accommodation reservation systems on your instruction, and
supply you with documentation of those reservations. A reservation is <strong>not</strong> a purchased ticket. No fare is
paid, no ticket number is issued, and the reservation is held only for the period the relevant supplier permits.</p>

<h2>3. What we do not supply</h2>
<p>We do not issue visas, influence visa decisions, or provide immigration or legal advice. We are not affiliated
with any government, embassy, consulate or visa application centre. We make no representation that any application
supported by our documents will succeed.</p>

<h2>4. Your obligations</h2>
<ul>
  <li>Provide names exactly as they appear in the passport, and accurate dates. We cannot verify what you submit.</li>
  <li>Use the documents for lawful purposes only. Visa applications, proof of onward travel, employer or
  institutional requirements.</li>
  <li>Do not alter, edit or resell any document we issue. Altering a document voids everything below and may
  constitute fraud in your jurisdiction.</li>
  <li>Verify the booking reference before submitting it to any authority.</li>
</ul>

<h2>5. Delivery</h2>
<p>We target delivery within %s of a cleared payment. This is a target, not a contractual guarantee; supplier system
outages and unusual routes can extend it. If we cannot deliver within 24 hours we will refund you in full.</p>

<h2>6. Validity of reservations</h2>
<p>Hold periods are set by airlines and accommodation providers, not by us, and typically run from 48 hours to
14 days. We do not control early release of a held booking. Where a booking is released before your stated
submission date, we will reissue at no charge.</p>

<h2>7. Amendments</h2>
<p>One amendment (name correction or date change) is included per order. Further amendments may attract a reissue
fee, notified before it is charged.</p>

<h2>8. Payment</h2>
<p>Prices are shown in US dollars and charged per traveller. Payment is processed by third-party providers; we do
not receive or store full card details.</p>

<h2>9. Refunds</h2>
<p>Governed by our <a href="%s">refund policy</a>, which forms part of these terms.</p>

<h2>10. Liability</h2>
<p>To the maximum extent permitted by law, our total liability arising from any order is limited to the fee you paid
for that order. We are not liable for visa refusals, denied boarding, missed appointments, or any consequential
loss. Nothing here limits liability for fraud, death or personal injury caused by negligence, or any liability that
cannot lawfully be excluded.</p>

<h2>11. Prohibited use</h2>
<p>You may not use our service to create documents intended to deceive any authority as to facts other than your
intended travel plans. We cooperate with lawful requests from authorities and reserve the right to refuse or cancel
any order without explanation.</p>

<h2>12. Governing law</h2>
<p>These terms are governed by the laws of <em>[jurisdiction to be completed]</em>.</p>

<h2>13. Changes</h2>
<p>We may update these terms. The version in force is the one published here on the date of your order.</p>
""" % (BRAND, EMAIL, EMAIL, DELIVERY, url("refund-policy")))


def privacy_page():
    _legal("privacy-policy", "Privacy policy", "Privacy Policy | " + BRAND,
           "What personal data we collect, why we collect it, how long we keep it and your rights over it.", """
<div class="note note--warn"><strong>Template notice</strong>
A working draft aligned to GDPR principles. Have it reviewed against your actual data flows and hosting
arrangements before launch.</div>

<h2>What we collect</h2>
<ul>
  <li><strong>Traveller details</strong>: name and date of birth, needed to create the reservation.</li>
  <li><strong>Trip details</strong>: route, dates, destination.</li>
  <li><strong>Contact details</strong>: email address, and a phone number if you give one.</li>
  <li><strong>Payment confirmation</strong>: a transaction reference from our payment provider. We never receive
  your full card number.</li>
</ul>
<p>We do <strong>not</strong> ask for passport numbers, passport scans or visa application content, and you should not send
them to us.</p>

<h2>Why we collect it</h2>
<p>To create and hold the reservation you ordered, to deliver the documents, to handle corrections and refunds, and
to meet accounting obligations. The legal basis is performance of a contract with you, and for retained financial
records, our legal obligations.</p>

<h2>Who we share it with</h2>
<p>Only with the airlines, accommodation providers and global distribution systems required to create your booking,
our payment processor, and our email delivery provider. We do not sell personal data, and we do not share it for
advertising.</p>

<h2>How long we keep it</h2>
<p>Order and traveller data is deleted 12 months after the order, except where financial records must be retained
for longer under applicable tax law. You may request earlier deletion.</p>

<h2>Cookies</h2>
<p>This site sets no advertising or tracking cookies. Your colour-theme preference is stored in your browser's local
storage and never leaves your device. If analytics are added later, this section will be updated first and consent
will be requested where required.</p>

<h2>Your rights</h2>
<p>Depending on where you live you may have the right to access, correct, delete, restrict or port your data, and to
object to processing. Email <a href="mailto:%s">%s</a> and we will respond within 30 days.</p>

<h2>Security</h2>
<p>Data is transmitted over TLS and access is limited to staff who need it to fulfil orders. No system is perfectly
secure; keeping the dataset small is our main defence.</p>

<h2>Contact</h2>
<p>Data controller: %s. Enquiries: <a href="mailto:%s">%s</a>.</p>
""" % (EMAIL, EMAIL, BRAND, EMAIL, EMAIL))


def refund_page():
    _legal("refund-policy", "Refund policy", "Refund Policy | " + BRAND,
           "When you get your money back: non-delivery, unverifiable bookings, duplicate charges and cancellations.", """
<h2>Full refund</h2>
<p>You receive a complete refund if:</p>
<ul>
  <li>We do not deliver your documents within <strong>24 hours</strong> of a cleared payment.</li>
  <li>The booking reference we supply <strong>does not verify</strong> on the relevant supplier&rsquo;s system and we cannot
  reissue a working one within 24 hours of you telling us.</li>
  <li>You were charged twice for the same order.</li>
  <li>You cancel <strong>before</strong> we have created the booking. Email immediately, typically a short window.</li>
</ul>

<h2>No refund</h2>
<p>Once a valid, verifiable booking has been delivered, the fee is non-refundable. The work is complete and the cost
is incurred at that point. In particular there is no refund for:</p>
<ul>
  <li>A visa refusal or an application withdrawn for any reason.</li>
  <li>Cancelled travel plans, or a change of mind after delivery.</li>
  <li>Details you supplied incorrectly, though your one free correction covers this.</li>
  <li>A booking released early by the airline where we have offered to reissue it.</li>
  <li>Refusal of the document by an authority for reasons unrelated to its validity.</li>
</ul>

<h2>How to request one</h2>
<p>Email <a href="mailto:%s">%s</a> with your order reference and what went wrong. We aim to decide within 48 hours.
Approved refunds return to the original payment method and usually appear within 5&ndash;10 business days, depending on
your bank.</p>

<h2>Chargebacks</h2>
<p>If you believe a refund is owed, contact us first. We will almost always resolve it faster than your bank can.
Raising a chargeback on a delivered, verifiable booking will be contested with the delivery record and verification
log.</p>
""" % (EMAIL, EMAIL))
