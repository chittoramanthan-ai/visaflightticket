import re
from urllib.parse import quote
# -*- coding: utf-8 -*-
"""Travel insurance and eSIM: the two things people buy right after the visa."""

from build import (asset, ICON, BRAND, EMAIL, DELIVERY, SITE_URL, TODAY,
                   PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH, PRICE_ESIM, PRICE_INSURE, PRICE_CONSULT, PRICE_CONSULT_ONLY, PRICE_FILING,
                   CURRENCY_CODE, SHOW_USD, usd, money, add_page, url, abs_url,
                   faq_block, faq_schema, crumbs, cta_band, ticket, doodles,
                   WHATSAPP)
import content_core


# Insurance is quoted, not priced on the site, so every "Get a quote" goes
# straight to a chat with the enquiry already written. The message is defined
# once here so the hero button and the three plan cards cannot drift apart.
INSURE_WA = ("https://wa.me/" + re.sub(r"[^0-9]", "", WHATSAPP) +
             "?text=" + quote("I want to buy travel insurance for my trip"))


CONSULT_WA = ("https://wa.me/" + re.sub(r"[^0-9]", "", WHATSAPP) +
              "?text=" + quote("I need help with my visa application"))


def consult_wa(plan=None, price=None):
    """WhatsApp link for a specific plan.

    All three plan buttons used to open the same generic message, so the first
    thing every conversation needed was working out which one had been tapped.
    The plan name and price ride along in the prefilled text instead.
    """
    if not plan:
        return CONSULT_WA
    msg = "Hi, I want the %s plan" % plan
    if price is not None:
        msg += " (%s)" % money(price)
    msg += " for my visa application."
    return ("https://wa.me/" + re.sub(r"[^0-9]", "", WHATSAPP) + "?text=" + quote(msg))

ESIM_WA = ("https://wa.me/" + re.sub(r"[^0-9]", "", WHATSAPP) +
           "?text=" + quote("I want to buy a travel eSIM for my trip"))


def build():
    insurance()
    esim()
    consultation()


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
         "<p>You have to. The embassy wants the certificate with the application. Buy a policy that starts on your intended departure date, and most insurers will refund or reissue if the visa is refused. Check that specific clause before paying.</p>"),
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
      <p class="eyebrow">Visa-compliant cover</p>
      <h1>Travel insurance for your visa application</h1>
      <p class="lede">Schengen embassies want &euro;30,000 of medical cover, valid across the whole area, for
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
    <h2>What an embassy is checking</h2>
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
      <p class="lede">Quoted per traveller once we know your dates, ages and destination.</p>
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
""" % (c_html, INSURE_WA, url("visa/schengen-visa-flight-reservation"),
       content_core.TRUSTLINE,
       ticket("Schengen compliant", "&euro;30,000 medical and repatriation, valid across all 29 states.",
              None,
              ["&euro;30,000 medical cover", "Repatriation and evacuation",
               "Certificate in euros, visa ready", "Dates matched to your itinerary"],
              "Get a quote", INSURE_WA, code="SCHENGEN"),
       ticket("Worldwide", "For trips outside Europe, where cover is sensible rather than mandatory.",
              None,
              ["Higher medical limit", "Baggage and delay cover",
               "Emergency evacuation", "Any destination"],
              "Get a quote", INSURE_WA, code="GLOBAL", featured=True, badge="Most bought"),
       ticket("Insurance + flight + hotel", "The whole visa file in one order, with dates that agree.",
              None,
              ["Flight reservation with live PNR", "Hotel booking for every night",
               "Schengen-compliant insurance", "All three cross-checked"],
              "Order the pack", INSURE_WA, code="FULLPACK"),
       faq_block(faqs, "Travel insurance questions"),
       cta_band("One order, one set of dates",
                "Insurance that matches the itinerary, because we issued the itinerary."))

    product = {
        # Service, not Product. Google's Product snippets require one of
        # offers/review/aggregateRating, and none is available honestly:
        # neither page publishes a price (insurance is quote-based), and
        # inventing reviews is fraud. Service carries no such requirement
        # and is the accurate type anyway - we arrange these, we do not
        # stock them. Matches the consultation page, which is already Service.
        "@type": "Service",
        "name": "Travel insurance for visa applications",
        "serviceType": "Travel insurance arrangement",
        "description": "Schengen-compliant travel medical insurance with EUR 30,000 cover, arranged through licensed insurers and matched to the applicant's flight dates.",
        "provider": {"@id": SITE_URL + "/#organization"},
        "areaServed": "IN",
        "url": abs_url("travel-insurance-for-visa"),
    }
    add_page(slug, "Travel Insurance for Visa | Schengen &euro;30,000 Medical Cover",
             "Travel insurance that satisfies a Schengen visa file: %s30,000 medical cover, repatriation, valid across all 29 states, dates matched to your flight reservation." % "&euro;",
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
      <p class="eyebrow">Data that works on landing</p>
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
""" % (c_html, ESIM_WA, content_core.trustline("esim"),
       ICON["shield"], ICON["clock"], ICON["wallet"], ICON["refresh"],
       ticket("Single country", "One destination, one price. The cheapest way if you are not moving around.",
              None,
              ["1GB to 20GB options", "7 to 30 days",
               "Instant QR delivery", "Top up in the app"],
              "Choose a pack", ESIM_WA, code="LOCAL"),
       ticket("Regional", "One eSIM across a whole region. Europe, Southeast Asia, the Gulf.",
              None,
              ["Works across the region", "No swapping at borders",
               "Ideal for multi-country visas", "Top up in the app"],
              "Choose a pack", ESIM_WA, code="REGION", featured=True, badge="Most bought"),
       ticket("Global", "For long or multi-stop trips across continents.",
              None,
              ["120+ countries", "One install, one balance",
               "Good for open-jaw itineraries", "Top up in the app"],
              "Choose a pack", ESIM_WA, code="GLOBAL"),
       doodles("globe", "map", "compass", "camera"),
       faq_block(faqs, "eSIM questions"),
       cta_band("Sorted before you take off",
                "Install on wifi at home, land with data already working."))

    product = {
        # Service, not Product: see the insurance page above.
        "@type": "Service",
        "name": "Travel eSIM data packs",
        "serviceType": "Travel eSIM provisioning",
        "description": "Prepaid travel eSIM data packs for single countries, regions or worldwide, delivered by QR code and installed before departure.",
        "provider": {"@id": SITE_URL + "/#organization"},
        "areaServed": "IN",
        "url": abs_url("travel-esim"),
    }
    add_page(slug, "Travel eSIM for Indians | Data Packs That Keep Your Number",
             "Travel eSIM data packs for Indian travellers. Keep your Indian number for OTPs and UPI, get local data the moment you land. Single country, regional and global packs.",
             body, schema=[c_schema, product, faq_schema(faqs)],
             priority="0.8", changefreq="weekly")


# --------------------------------------------------------------------------
def _file_card():
    """Artwork for the consultation hero.

    The boarding pass belongs on pages that sell a flight document. Here the
    product is a read of your application, so the card shows a file being
    checked off instead: it says what you get rather than what we also sell.
    """
    # Ordered the way the file is actually built, and carried through to
    # lodging so the card covers all three plans rather than stopping where
    # the middle one does. A muted tick means the line is yours, not ours -
    # bank statements come from your bank, and the embassy fee is your money.
    rows = [
        ("Itinerary", "Planned to the day", True),
        ("Flight reservation", "Live PNR", True),
        ("Hotel booking", "Dates matched", True),
        ("Cover letter", "Written for your case", True),
        ("Bank statements", "You provide, we advise", False),
        ("Application form", "Completed for you", True),
        ("Appointment", "Booked and timed", True),
        ("Embassy fee", "Paid by you, at cost", False),
    ]
    items = ""
    for label, state, ours in rows:
        items += (
            '<li class="fcard__row"><span class="fcard__tick%s">%s</span>'
            '<span class="fcard__lbl">%s</span><span class="fcard__st">%s</span></li>'
            % ("" if ours else " fcard__tick--muted", ICON["check"], label, state))
    return """
<div class="fcard" role="img" aria-label="A visa application file with every document and step checked off, from itinerary to appointment">
  <div class="fcard__top"><span>Application file</span><span>Ready to lodge</span></div>
  <ul class="fcard__list">%s</ul>
  <div class="fcard__foot">%s Every date agrees, across every document in the file</div>
</div>""" % (items, ICON["shield"])


# --------------------------------------------------------------------------
def consultation():
    """Advisory service page.

    The financial-documents card is worded very deliberately. "Help with bank
    statements" reads two ways, and one of those ways is producing them. Every
    other page on this site rests on not fabricating anything, so this one
    says plainly what the help is: reading the checklist, judging whether what
    you already hold is enough, and explaining what an officer looks for.
    There is an explicit "what we will not do" section for the same reason. An
    advisory service is exactly where that line gets tested.
    """
    slug = "visa-consultation"
    c_html, c_schema = crumbs([("Visa consultation", None)])

    faqs = [
        ("What does a consultation actually cover?",
         "<p>We read the embassy's own checklist for your case, look at what you have, and tell you what is missing, what is weak and what will be read the wrong way. Then we help you assemble the parts we can legitimately produce: the flight reservation, the hotel booking and the cover letter.</p>"),
        ("Can you write my cover letter?",
         "<p>Yes. You tell us the purpose of the trip, who is funding it and what ties you to home, and we turn that into a letter an officer can read in thirty seconds. What we will not do is invent a reason for travel or a sponsor who does not exist.</p>"),
        ("Do you prepare bank statements?",
         "<p>No, and nobody honest does. Statements come from your bank. What we do is tell you how many months to show, what an officer is looking for in them, how to explain a large recent deposit, and whether the balance you hold is likely to read as sufficient for the trip you have described.</p>"),
        ("Will this guarantee my visa?",
         "<p>No. Anyone promising that is lying to you. The decision belongs to the embassy. What a well-assembled file removes is the avoidable reasons to refuse it, which is the only part anyone can influence.</p>"),
        ("How much does it cost?",
         "<p>It depends on the country and how much of the file you want help with, so we quote after a short conversation rather than publishing a number that would be wrong for most people.</p>"),
        ("Can you book my appointment slot?",
         "<p>On the first two plans we tell you which portal to use, what the slot situation looks like and how to time your documents around it. On <strong>Flights + hotels + filing</strong> we book the appointment and lodge the application for you. The embassy fee is always paid by you, at cost.</p>"),
    ]

    body = """
<section>
  <div class="wrap">
    %s
    <div class="hero__grid" style="align-items:flex-start">
      <div>
        <p class="eyebrow">Visa consultation &middot; from %s%s</p>
        <h1>Get your visa approved, on time</h1>
        <p class="lede">Most refusals are not close calls. They are avoidable ones: a missing document, a
        letter answering the wrong question, dates that do not agree with each other. We go through your
        file before an embassy does, and tell you what an officer is going to see.</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--wa btn--lg" href="%s">%s Talk on WhatsApp</a>
          <a class="btn btn--ghost btn--lg" href="%s">Browse visa guides</a>
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
      <h2>Three ways to work with us</h2>
      <p class="lede">Advice on its own, the flights and hotels included, or the whole
      application completed and lodged for you.</p>
    </div>
    <div class="grid g3">%s%s%s</div>
    <p class="center" style="margin-top:1.4rem;color:var(--ink-2);font-size:.93rem">
      Per application, not per traveller. Additional travellers on the same file are included.</p>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <div class="creed creed--tight">
      <p class="eyebrow">50+ countries travelled</p>
      <h2>The team building your file are travellers themselves</h2>
      <p class="creed__lead">The people at %s who put your application together have travelled to
      <strong>more than 50 countries</strong> between them. They are not agents who have never
      stepped outside the office, working down a checklist on a screen.</p>
      <p>They have filled in these forms for their own trips, been asked for the same documents at the
      same counters, and had their own files picked apart. That is the difference between advice that
      repeats the embassy website back at you and advice from someone who has actually stood in the
      queue.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>What we help with</h2>
      <p class="lede">The whole file, not only the parts we sell.</p>
    </div>
    <div class="grid g3">
      <div class="card"><div class="card__ico">%s</div><h3>Itinerary planning</h3>
        <p>A day-by-day plan that agrees with your flights, your hotels and the length of stay you have
        declared. Embassies check those three against each other, and they often do not match.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Cover letter</h3>
        <p>Written around your real purpose of travel, who is funding it and what brings you home. One
        page, in the order an officer actually reads it.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Financial documents, explained</h3>
        <p>How many months to show, what balance reads as sufficient for your trip, and how to explain a
        large recent deposit. Your bank issues the statements. We tell you how they will be read.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Flight reservation</h3>
        <p>A real airline booking with a live PNR, dated around your appointment. This part we issue
        ourselves.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Hotel booking</h3>
        <p>A confirmed booking covering every night you have declared, with the dates reconciled against
        the flights so the two cannot contradict each other.</p></div>
      <div class="card"><div class="card__ico">%s</div><h3>Checklist review</h3>
        <p>We read the embassy's own list for your case and tell you what is missing, what is weak and
        what is likely to be queried, before you submit rather than after.</p></div>
    </div>
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>What we will not do</h2>
    <p>An advisory service is exactly where this line gets tested, so we will be blunt about it.</p>
    <ul>
      <li><strong>We do not produce bank statements, payslips or tax documents.</strong> Those come from
      your bank, your employer and the tax authority. Anyone offering to make them is offering you a
      deception finding instead of a visa.</li>
      <li><strong>We do not invent a purpose of travel</strong>, a sponsor, an employer or a relationship.
      The cover letter is built around your circumstances as they actually are.</li>
    </ul>
    <p style="margin-top:1.4rem"><strong>What we will do is improve your chances.</strong> A file with
    nothing missing, nothing contradicting itself and every claim backed by evidence is far more likely to
    be approved than the one most applicants hand over. Refusals overwhelmingly come from avoidable
    mistakes, and removing those is the part anyone can actually influence. That is the work.</p>
    <div class="note">
      <strong>Why this matters more than it sounds</strong>
      A refusal is a setback. A finding that you submitted something false is a different category of
      problem, and it follows you into every application you make afterwards. Everything we help with is
      designed to survive being checked, because the alternative is not worth what it saves.
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2>How it works</h2>
    <ol class="vsteps">
      <li class="vstep"><span class="vstep__n">1</span><div><h3>Tell us the country and the date</h3><p>Which visa, when you are applying, and whether you already hold an appointment.</p></div></li>
      <li class="vstep"><span class="vstep__n">2</span><div><h3>Send what you have so far</h3><p>Whatever is assembled. Nothing needs to be finished for us to look at it.</p></div></li>
      <li class="vstep"><span class="vstep__n">3</span><div><h3>We come back with a list</h3><p>What is missing, what is weak, and what we can produce for you, with a price for the parts you want us to handle.</p></div></li>
      <li class="vstep"><span class="vstep__n">4</span><div><h3>We build the documents we issue</h3><p>Flight reservation, hotel booking and cover letter, with the dates reconciled across all three.</p></div></li>
      <li class="vstep"><span class="vstep__n">5</span><div><h3>You submit with everything agreeing</h3><p>Which is the whole point. Most queries come from two documents in one file disagreeing with each other.</p></div></li>
    </ol>
  </div>
</section>


<section>
  <div class="wrap">
    <div class="center" style="margin-bottom:2.2rem">
      <h2>Countries we help with</h2>
      <p class="lede">Every guide is written for an Indian passport. Open one for the
      requirements, the fees and the mistakes that get files returned.</p>
    </div>
    %s
    <div class="center" style="margin-top:2rem">
      <a class="btn btn--ghost" href="%s">See all visa guides</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2>How we compare with a full-service visa platform</h2>
    <p>Platforms like Atlys file the whole application for you. We do something narrower and
    much cheaper: we produce the documents an application needs and tell you how to assemble
    the rest. Which is right depends on what you actually want, so here is the honest version
    rather than a table rigged in our favour.</p>
    <div class="tbl-wrap">
    <table>
      <thead><tr><th>&nbsp;</th><th>Full-service platform</th><th>%s</th></tr></thead>
      <tbody>
        <tr><td><b>What you are buying</b></td>
            <td>The whole application, filed for you</td>
            <td>The documents and advice, or the full application if you want it</td></tr>
        <tr><td><b>Who submits it</b></td>
            <td>They do, on your behalf</td>
            <td>You do on the first two plans, we do on Flights + hotels + filing</td></tr>
        <tr><td><b>Embassy fee</b></td>
            <td>Bundled into a single price</td>
            <td>You pay it directly, at cost, with nothing added</td></tr>
        <tr><td><b>Flight reservation</b></td>
            <td>Part of the package</td>
            <td><b>%s</b> on its own, real PNR, no package needed</td></tr>
        <tr><td><b>Hotel booking</b></td>
            <td>Part of the package</td>
            <td><b>%s</b> on its own</td></tr>
        <tr><td><b>Advice without documents</b></td>
            <td>Not normally sold separately</td>
            <td><b>%s</b></td></tr>
        <tr><td><b>Best when</b></td>
            <td>You want someone else to handle all of it</td>
            <td>You are filing it yourself and need documents that hold up</td></tr>
      </tbody>
    </table>
    </div>
    <div class="note">
      <strong>When a full-service platform is the better choice</strong>
      If you would rather hand the whole application to someone else and pay one bundled price,
      use one. We are not going to pretend otherwise. Come to us when you are filing it yourself
      and need a reservation an officer can actually look up.
    </div>
  </div>
</section>
<section>
  <div class="wrap wrap--narrow">%s</div>
</section>

%s
""" % (c_html,
       money(PRICE_CONSULT_ONLY),
       ('<span class="usd-alt">%s</span>' % usd(PRICE_CONSULT_ONLY)) if SHOW_USD else "",
       CONSULT_WA, ICON["whatsapp"], url("visa"),
       content_core.trustline("advice"), _file_card(),
       ticket("Consultation only",
              "We read your file and tell you exactly what to fix. You assemble the documents.",
              PRICE_CONSULT_ONLY,
              ["Checklist review against your embassy",
               "Cover letter written for your case",
               "Itinerary planned around your dates",
               "Guidance on what your finances need to show"],
              "Talk on WhatsApp", consult_wa("Consultation only", PRICE_CONSULT_ONLY), code="ADVICE",
              price_note="per application"),
       ticket("Consultation + flights + hotels",
              "Everything above, plus the flight reservation and hotel booking, with every date reconciled.",
              PRICE_CONSULT,
              ["Everything in consultation only",
               "Flight reservation with a live PNR",
               "Hotel booking for every night declared",
               "Dates cross-checked across all three",
               "One pack, ready to upload"],
              "Talk on WhatsApp", consult_wa("Consultation + flights + hotels", PRICE_CONSULT), code="FULLFILE",
              price_note="per application"),
       ticket("Flights + hotels + filing",
              "Everything above, and we complete the forms and lodge the application for you.",
              PRICE_FILING,
              ["Everything in consultation + flights + hotels",
               "Application forms completed for you",
               "Appointment booked around your dates",
               "Application lodged on your behalf",
               "Embassy fee paid by you, at cost"],
              "Talk on WhatsApp", consult_wa("Flights + hotels + filing", PRICE_FILING), code="FILING",
              price_note="per application", featured=True, badge="Best value"),
       BRAND,
       ICON["globe"], ICON["doc"], ICON["wallet"], ICON["plane"], ICON["shield"], ICON["check"],
       _country_tiles(), url("visa"), BRAND,
       money(PRICE_FLIGHT), money(PRICE_HOTEL), money(PRICE_CONSULT_ONLY),
       faq_block(faqs, "Consultation questions"),
       cta_band("Send us your file and we will read it",
                "Tell us the country and where you have got to. We come back with what is missing and what it costs.",
                primary=("Talk on WhatsApp", CONSULT_WA),
                secondary=("See visa guides", "visa")))

    service = {
        "@type": "Service",
        "name": "Visa application consultation",
        "serviceType": "Visa documentation advisory",
        "provider": {"@id": SITE_URL + "/#organization"},
        "description": "Advisory help assembling a visa application file: itinerary planning, cover letter, guidance on financial documents, flight reservations and hotel bookings, and a review against the embassy's own checklist.",
        "areaServed": "IN",
        "url": abs_url(slug),
    }
    add_page(slug, "Visa Consultation | Cover Letter and Document Help",
             "Help assembling a visa application: itinerary planning, cover letter, guidance on what your bank statements need to show, flight reservations and hotel bookings, and a review against the embassy checklist.",
             body, schema=[c_schema, service, faq_schema(faqs)],
             priority="0.8", changefreq="monthly")


# --------------------------------------------------------------------------
def _country_tiles(limit=15):
    """Country tiles for the consultation page.

    Two deliberate omissions from the layout this copies.

    No photography: 38 licensed country photos is a purchase, and the site's
    standing rule is that nothing loads from another host. The gradient is
    derived from the slug, so a country always gets the same colour. Moving to
    real photos later is a background-image on .ccard, with no markup change.

    No VALID column, which the reference design does have. status_note mixes
    stay durations with processing times - Schengen's "15 to 45 days" is how
    long a decision takes, not how long you may stay - so deriving a stay
    length from it would print wrong visa information on a site whose whole
    value is being checkable. TYPE and FEE are curated per country and safe.
    """
    import hashlib
    import content_visa
    from build import slugify

    TYPE = {"visa_free": "VISA FREE", "voa": "ON ARRIVAL",
            "evisa": "E-VISA", "visa_required": "VISA NEEDED"}
    out = []
    for v in content_visa.VISAS[:limit]:
        hue = int(hashlib.md5(v["slug"].encode("utf-8")).hexdigest()[:4], 16) % 360
        fee = re.sub(r"<[^>]+>", "", (v.get("fees") or [("", "-", "")])[0][1])
        out.append(
            '<a class="ccard" style="--h:DEG1;--h2:DEG2" href="HREF">'
            '<img class="ccard__img" src="IMG" alt="" loading="lazy"'
            ' decoding="async" width="440" height="560">'
            '<span class="ccard__name">NAME</span>'
            '<span class="ccard__strip">'
            '<span><b class="ccard__k">Type</b><span class="ccard__v">KIND</span></span>'
            '</span></a>'
            .replace("DEG1", str(hue))
            .replace("DEG2", str((hue + 26) % 360))
            .replace("HREF", url("visa/" + v["slug"]))
            .replace("IMG", asset("assets/img/countries/%s.jpg" % slugify(v["short"]), bust=True))
            .replace("NAME", v["short"].upper())
            .replace("KIND", TYPE.get(v["status"], "VISA"))
            )
    return '<div class="cgrid">' + "".join(out) + "</div>"
