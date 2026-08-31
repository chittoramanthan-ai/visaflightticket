# -*- coding: utf-8 -*-
"""Travel insurance and eSIM: the two things people buy right after the visa."""

from build import (ICON, BRAND, EMAIL, DELIVERY, SITE_URL, TODAY,
                   PRICE_FLIGHT, PRICE_BOTH, PRICE_ESIM, PRICE_INSURE,
                   CURRENCY_CODE, money, add_page, url, abs_url,
                   faq_block, faq_schema, crumbs, cta_band, ticket, doodles)
import content_core


def build():
    insurance()
    esim()


# --------------------------------------------------------------------------
def insurance():
    slug = "travel-insurance-for-visa"
    c_html, c_schema = crumbs([("Travel insurance for visa", None)])

    faqs = [
        ("Is travel insurance mandatory for a Schengen visa?",
         "<p>Yes, and it is one of the few Schengen requirements with a hard number attached: medical cover of at least &euro;30,000, valid in every Schengen state, for the exact dates on your itinerary. A file without it is refused on the spot.</p>"),
        ("Which other countries require it?",
         "<p>Cuba, Turkey for some nationalities, Oman, Qatar for certain visa types, and Saudi Arabia, where it is bundled into the visa fee. Beyond the mandatory list, most travellers buy it anyway because a hospital bill abroad is the one risk that can genuinely ruin you.</p>"),
        ("What cover do I actually need?",
         "<p>For a Schengen file, &euro;30,000 medical and repatriation is the floor. In practice, look for medical evacuation, a sensible baggage limit, and trip cancellation if you have paid for anything non-refundable.</p>"),
        ("Can I buy it before my visa is approved?",
         "<p>You have to. The consulate wants the certificate with the application. Buy a policy that starts on your intended departure date, and most insurers will refund or reissue if the visa is refused. Check that specific clause before paying.</p>"),
        ("Do you underwrite the policy?",
         "<p>No. We are not an insurer. We arrange cover through licensed insurance partners, and the policy is a contract between you and that insurer. The certificate comes from them, on their paper.</p>"),
        ("How fast do I get the certificate?",
         "<p>Within %s, the same as everything else we issue, and formatted for a visa file rather than as a wall of policy wording.</p>" % DELIVERY),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">From %s per traveller</p>
      <h1>Travel insurance for your visa application</h1>
      <p class="lede">Schengen consulates want &euro;30,000 of medical cover, valid across the whole area, for
      the exact dates on your itinerary. Get the number or the dates wrong and the file comes back. We issue a
      certificate that matches your flight reservation, because we already have your dates.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Get a quote</a>
        <a class="btn btn--ghost btn--lg" href="%s">See the Schengen rules</a>
      </div>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2>What a consulate is checking</h2>
    <p>Not the brand, not the premium. Four things, and all four are mechanical:</p>
    <ol>
      <li><strong>&euro;30,000 minimum medical cover</strong>, stated in euros on the certificate. A policy in
      rupees with no euro figure gets queried even when the cover is adequate.</li>
      <li><strong>Valid in all Schengen states</strong>, not just the country you applied to.</li>
      <li><strong>Repatriation and emergency evacuation</strong> included and named.</li>
      <li><strong>Dates covering your whole trip</strong>, ideally with a day either side. Insurance that expires
      the morning of your return flight is the classic avoidable error.</li>
    </ol>
    <div class="note note--warn">
      <strong>Buy it after your dates are fixed</strong>
      Not before. Insurance bought around approximate dates and a flight reservation issued later almost never
      line up, and a mismatch between the two is exactly what an officer notices.
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>Cover that fits a visa file</h2>
      <p class="lede">Priced per traveller for the length of the trip.</p>
    </div>
    <div class="grid g3">%s%s%s</div>
    <p class="center" style="margin-top:1.6rem;color:var(--ink-3);font-size:.9rem">
      Policies are underwritten by licensed insurers. We arrange the cover; the contract is between you and them.</p>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, money(PRICE_INSURE), url("order"), url("visa/schengen-visa-flight-reservation"),
       content_core.TRUSTLINE,
       ticket("Schengen compliant", "&euro;30,000 medical and repatriation, valid across all 29 states.",
              PRICE_INSURE,
              ["&euro;30,000 medical cover", "Repatriation and evacuation",
               "Certificate in euros, visa ready", "Dates matched to your itinerary"],
              "Get a quote", "order", code="SCHENGEN"),
       ticket("Worldwide", "For trips outside Europe, where cover is sensible rather than mandatory.",
              PRICE_INSURE + 300,
              ["Higher medical limit", "Baggage and delay cover",
               "Emergency evacuation", "Any destination"],
              "Get a quote", "order", code="GLOBAL", featured=True, badge="Most bought"),
       ticket("Insurance + flight + hotel", "The whole visa file in one order, with dates that agree.",
              PRICE_BOTH + PRICE_INSURE,
              ["Flight reservation with live PNR", "Hotel booking for every night",
               "Schengen-compliant insurance", "All three cross-checked"],
              "Order the pack", "order", code="FULLPACK"),
       faq_block(faqs, "Travel insurance questions"),
       cta_band("One order, one set of dates",
                "Insurance that matches the itinerary, because we issued the itinerary."))

    product = {
        "@type": "Product",
        "name": "Travel insurance for visa applications",
        "description": "Schengen-compliant travel medical insurance with EUR 30,000 cover, arranged through licensed insurers and matched to the applicant's flight dates.",
        "brand": {"@id": SITE_URL + "/#organization"},
        "offers": {"@type": "Offer", "price": str(PRICE_INSURE), "priceCurrency": CURRENCY_CODE,
                   "availability": "https://schema.org/InStock", "url": abs_url("order")},
    }
    add_page(slug, "Travel Insurance for Visa | Schengen &euro;30,000 Cover from %s" % money(PRICE_INSURE),
             "Travel insurance that satisfies a Schengen visa file: %s30,000 medical cover, repatriation, valid across all 29 states, dates matched to your flight reservation. From %s." % ("&euro;", money(PRICE_INSURE)),
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.9", changefreq="weekly")


# --------------------------------------------------------------------------
def esim():
    slug = "travel-esim"
    c_html, c_schema = crumbs([("Travel eSIM", None)])

    faqs = [
        ("Will an eSIM work on my phone?",
         "<p>If it is an iPhone XS or newer, a recent Pixel, or most Samsung flagships from the S20 on, yes. Dial *#06# and if you see an EID number alongside the IMEI, your phone supports eSIM. Phones bought in some markets are carrier locked, which blocks it.</p>"),
        ("Do I keep my Indian number?",
         "<p>Yes. That is the point of an eSIM over a physical SIM. Your Indian number stays active for calls, OTPs and UPI, and the eSIM carries data. Turn off roaming on the Indian line so it does not quietly bill you.</p>"),
        ("Will I still get bank OTPs?",
         "<p>Yes, as long as the Indian line is active and roaming is enabled for SMS. This is the thing people get wrong: they disable the Indian line entirely, then cannot authorise a payment. Leave it on for SMS, off for data.</p>"),
        ("When should I install it?",
         "<p>Before you fly, on wifi. Installation needs a connection, and doing it after landing means finding airport wifi first, which is exactly when you least want to.</p>"),
        ("What if I run out of data?",
         "<p>Top up in the app. No queue, no passport photocopy, no shop that only takes cash.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="wrap--narrow" style="padding:0;margin:0">
      <p class="eyebrow">From %s</p>
      <h1>Travel eSIM, working before you land</h1>
      <p class="lede">Keep your Indian number for OTPs and UPI, and get local data the moment the plane doors
      open. No SIM counter, no passport photocopy, no hunting for a shop that takes cards.</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn--primary btn--lg" href="%s">Get a data pack</a>
        <a class="btn btn--ghost btn--lg" href="#compat">Check my phone</a>
      </div>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.2rem"><h2>Why bother with an eSIM</h2></div>
    <div class="grid g4">
      <div class="card"><div class="card__ico">%s</div><h3>Your number survives</h3>
        <p>Indian line stays live for OTPs, UPI and calls from home. Data runs on the eSIM.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Working on landing</h3>
        <p>Installed before you fly, active when you switch off flight mode. No queue at arrivals.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>No roaming shock</h3>
        <p>Indian roaming can run into thousands a day. A regional pack costs less than one airport coffee.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Top up anywhere</h3>
        <p>Run low mid-trip and you add data in the app, not in a shop that shuts at six.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>Data packs</h2>
      <p class="lede">Regional packs cover a whole trip; single-country packs are cheaper if you are staying put.</p>
    </div>
    <div class="grid g3">%s%s%s</div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2 id="compat">Does your phone take an eSIM?</h2>
    <p>Dial <code>*#06#</code> on the handset. If an <strong>EID</strong> appears alongside the IMEI, your phone takes an eSIM. Most iPhones from the XS on, recent Pixels and Samsung flagships do; budget Android handsets mostly do not, and a physical local SIM is the answer there.</p>
    <div class="note">
      <strong>Leave the Indian line switched on</strong>
      Data off, roaming for SMS on. Kill the line entirely and your bank OTP has nowhere to arrive, which people
      discover at the exact moment they are trying to pay for something.
    </div>
    %s
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html, money(PRICE_ESIM), url("order"), content_core.TRUSTLINE,
       ICON["shield"], ICON["clock"], ICON["wallet"], ICON["refresh"],
       ticket("Single country", "One destination, one price. The cheapest way if you are not moving around.",
              PRICE_ESIM,
              ["1GB to 20GB options", "7 to 30 days",
               "Instant QR delivery", "Top up in the app"],
              "Choose a pack", "order", code="LOCAL"),
       ticket("Regional", "One eSIM across a whole region. Europe, Southeast Asia, the Gulf.",
              PRICE_ESIM + 400,
              ["Works across the region", "No swapping at borders",
               "Ideal for multi-country visas", "Top up in the app"],
              "Choose a pack", "order", code="REGION", featured=True, badge="Most bought"),
       ticket("Global", "For long or multi-stop trips across continents.",
              PRICE_ESIM + 1100,
              ["120+ countries", "One install, one balance",
               "Good for open-jaw itineraries", "Top up in the app"],
              "Choose a pack", "order", code="GLOBAL"),
       doodles("globe", "map", "compass", "camera"),
       faq_block(faqs, "eSIM questions"),
       cta_band("Sorted before you take off",
                "Install on wifi at home, land with data already working."))

    product = {
        "@type": "Product",
        "name": "Travel eSIM data packs",
        "description": "Prepaid travel eSIM data packs for single countries, regions or worldwide, delivered by QR code and installed before departure.",
        "brand": {"@id": SITE_URL + "/#organization"},
        "offers": {"@type": "Offer", "price": str(PRICE_ESIM), "priceCurrency": CURRENCY_CODE,
                   "availability": "https://schema.org/InStock", "url": abs_url("order")},
    }
    add_page(slug, "Travel eSIM for Indians | Data Packs from %s, Keep Your Number" % money(PRICE_ESIM),
             "Travel eSIM data packs from %s. Keep your Indian number for OTPs and UPI, get local data the moment you land. Single country, regional and global packs." % money(PRICE_ESIM),
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.8", changefreq="weekly")
