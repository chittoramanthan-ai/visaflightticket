# -*- coding: utf-8 -*-
"""Blog: the topical-authority cluster that feeds the money pages."""

from build import (BRAND, SITE_URL, TODAY, DELIVERY, EMAIL,
                   PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH, SINCE_YEAR,
                   money, add_page, url, abs_url, faq_block, faq_schema,
                   crumbs, cta_band, slugify)

AUTHOR = "The %s editorial team" % BRAND


# --------------------------------------------------------------------------
# Posts. sections = [(H2 heading, html), ...] -> TOC + anchors are generated.
# --------------------------------------------------------------------------
POSTS = [

# ==========================================================================
dict(
    slug="what-is-a-dummy-ticket",
    cat="Fundamentals",
    title="What Is a Dummy Ticket for a Visa? A Plain-English Guide",
    meta_title="What Is a Dummy Ticket for a Visa? Meaning, Legality, Cost",
    desc="A dummy ticket is a real airline reservation held without payment, carrying a live PNR. What it is, why embassies ask for one, what it costs and how to tell a genuine one from a forgery.",
    read=7,
    lede="Somebody on a forum told you to get a dummy ticket. Somebody else said dummy tickets get you "
         "banned. Both of them are talking about different things and neither said so. Here is the actual "
         "distinction, in about four minutes.",
    sections=[
        ("The definition, precisely", """
<p>A dummy ticket is a <strong>real airline booking that nobody has paid for yet</strong>. The airline blocks the seat for a defined period and issues a booking reference. A
six-character alphanumeric code known as a PNR (Passenger Name Record), such as <code>K7QX2M</code>.</p>
<p>The document you receive shows everything a paid ticket shows:</p>
<ul>
  <li>Passenger name, surname first, as it appears in the passport</li>
  <li>Airline and flight number for each leg</li>
  <li>Departure and arrival airports, dates and local times</li>
  <li>The booking reference</li>
</ul>
<p>What it does not show is a ticket number, because no fare has been paid. In airline systems the record exists in a
<em>booked</em> state rather than a <em>ticketed</em> state. That distinction is invisible to almost everyone except
airline staff, and entirely acceptable to consulates, who ask for reservations precisely because they do not want
applicants buying fares before a decision.</p>"""),

        ("Why the name is misleading", """
<p>The word &ldquo;dummy&rdquo; entered the vocabulary through travel agents describing a booking that would never be
ticketed. It stuck, and it has been doing damage ever since, because it implies the document is fake.</p>
<p>Consulates and airlines use completely different words for the same thing:</p>
<ul>
  <li><strong>Flight reservation</strong>: the term on most Schengen checklists</li>
  <li><strong>Flight itinerary</strong>: common on US and Canadian documentation</li>
  <li><strong>Provisional booking</strong> or <strong>booking confirmation</strong>: airline language</li>
  <li><strong>Proof of onward travel</strong>: when the purpose is boarding rather than a visa</li>
</ul>
<p>All four describe the same artefact. If a form asks for any of them, an unpaid reservation with a live PNR is what
is wanted.</p>"""),

        ("Why embassies ask for a reservation instead of a ticket", """
<p>There is a catch-22 sitting at the heart of every visa application. The consulate wants evidence you have planned a specific
trip. But buying an international fare before approval means risking tens of thousands of rupees on an
application that may be refused.</p>
<p>Consulates resolved this years ago by asking for reservations. The European Commission's own visa guidance advises
applicants <em>not</em> to purchase non-refundable tickets before a decision is issued. UKVI, IRCC and the US State
Department all give substantially the same advice.</p>
<p>So the unpaid reservation is not a workaround anyone is tolerating. It is the outcome the system was designed to
produce.</p>"""),

        ("Dummy ticket vs fake ticket. The only distinction that matters", """
<p>Two documents can look identical sitting side by side on a desk and be worlds apart legally.</p>
<div class="tbl-wrap">
<table>
<thead><tr><th>&nbsp;</th><th>Genuine reservation</th><th>Fabricated document</th></tr></thead>
<tbody>
<tr><td><b>Exists in an airline system</b></td><td class="yes">Yes</td><td class="no">No</td></tr>
<tr><td><b>PNR resolves on the airline site</b></td><td class="yes">Yes</td><td class="no">No</td></tr>
<tr><td><b>How it is made</b></td><td>A booking is created</td><td>A PDF is designed</td></tr>
<tr><td><b>If an officer checks</b></td><td class="yes">Itinerary appears</td><td class="no">Nothing, or someone else's trip</td></tr>
<tr><td><b>Consequence</b></td><td class="yes">Normal processing</td><td class="no">Refusal, and usually a multi-year ban</td></tr>
</tbody>
</table>
</div>
<p>A fraud finding on a visa record is not a bad afternoon. Under US law it can trigger a permanent inadmissibility
finding; Schengen states share refusal data across the whole area; UKVI applies a ban that commonly runs ten years for
deception. All of that, to avoid spending the price of a takeaway.</p>
<div class="note note--warn"><strong>The test takes two minutes</strong>
Open the operating airline's &ldquo;manage booking&rdquo; page, enter the PNR and the surname. If your own itinerary comes
back, the document is real. If it does not, no amount of good design on the PDF will save you.
<a href="%s">Full verification walkthrough &rarr;</a></div>""" % url("verify-pnr")),

        ("What one should cost", """
<p>Between about &#8377;300 and &#8377;3,000, depending on the provider. Anything materially above that is usually a semi-refundable
ticket rather than a reservation; anything free is usually generated rather than booked.</p>
<p>Our own pricing sits at <strong>%s for a flight reservation</strong>, %s for a hotel booking and %s for both,
per traveller. The reason it can be that cheap is straightforward: no fare is ever purchased, so there is no fare to
recover. You are paying for the booking to be created, held, documented and checked.</p>""" % (money(PRICE_FLIGHT), money(PRICE_HOTEL), money(PRICE_BOTH))),

        ("How long it stays live", """
<p>The hold is the airline's decision, not the seller's. In practice they run from
<strong>48 hours to about 14 days</strong>, varying by carrier, route, fare class and how far ahead you are travelling.
High-demand routes hold for less time.</p>
<p>This worries people more than it should. Consular officers check a PNR when they open your file, which is usually
within days of submission, not months later. And by the time a decision is issued, you will normally have bought
a real ticket anyway. The practical rule is to time the reservation so it is live on your submission date, and to use
a provider who will reissue free if your appointment moves.</p>"""),

        ("When you need one", """
<ul>
  <li><strong>Tourist visa applications</strong>: Schengen, UK, US B1/B2, Canada, Australia, Japan, Korea and most e-visa portals.</li>
  <li><strong>Proof of onward travel</strong>: airlines refuse boarding on one-way tickets to many countries.</li>
  <li><strong>Visa extensions</strong>: frequently require a departure booking before the current permission expires.</li>
  <li><strong>Student and work permits</strong>: provisional travel plans aligned to a course or contract start.</li>
  <li><strong>Travel insurance quotes</strong>: Schengen insurance must cover exact travel dates.</li>
</ul>"""),
    ],
    faqs=[
        ("Is a dummy ticket legal?", "<p>Holding an unpaid airline reservation is a normal commercial transaction that travel agents perform constantly. What is illegal is submitting a fabricated document. The legality question is really a question about where your document came from. <a href=\"%s\">Covered in detail here</a>.</p>" % url("blog/is-a-dummy-ticket-legal")),
        ("Can I make one myself?", "<p>Some airlines offer a 24&ndash;72 hour hold on their own website, free or for a small fee. If your route is served by one of them and your appointment is imminent, that works. It falls down on longer windows, multi-city itineraries, and routes where no carrier offers holds.</p>"),
        ("Will the embassy know it is unpaid?", "<p>Yes, and it does not matter. A reservation shows a booking status rather than a ticket number, and consulates ask for reservations for exactly this reason.</p>"),
        ("Does a dummy ticket guarantee my visa?", "<p>No. It satisfies one line on a checklist. Decisions turn on finances, ties to your home country and immigration history.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="is-a-dummy-ticket-legal",
    cat="Legality",
    title="Is a Dummy Ticket Legal for a Visa Application?",
    meta_title="Is a Dummy Ticket Legal? Visa Rules, Risks and Red Flags",
    desc="Unpaid flight reservations are legal and expected by consulates. Fabricated itineraries are document fraud. Where the line sits, what happens if you cross it, and how to stay on the right side.",
    read=8,
    lede="Short version: an unpaid reservation is legal everywhere, a made-up PDF is fraud everywhere, and "
         "the two look identical when they land in your inbox. The useful version is knowing which one you "
         "just bought.",
    sections=[
        ("What is legal", """
<p>Holding a seat without paying for it is a routine commercial transaction. Airlines built the functionality
deliberately, travel agencies use it thousands of times a day, and consulates rely on it.</p>
<p>Consider what the authorities themselves publish:</p>
<ul>
  <li><strong>European Commission</strong>: Schengen visa guidance lists a flight itinerary among required documents
  and advises applicants not to buy non-refundable tickets before a decision.</li>
  <li><strong>US Department of State</strong>: tells applicants not to make final travel plans or buy non-refundable
  tickets until they hold a visa.</li>
  <li><strong>UKVI</strong>: advises against booking travel before a decision is made.</li>
  <li><strong>IRCC (Canada)</strong>: advises against buying tickets until the visa is issued.</li>
</ul>
<p>Every one of those bodies is telling you to submit a plan rather than a purchase. An unpaid reservation with a
valid PNR is exactly that.</p>"""),

        ("What is not legal", """
<p>Document fraud. Specifically:</p>
<ul>
  <li>A PDF designed to resemble an itinerary with no booking behind it.</li>
  <li>A recycled or invented PNR that belongs to someone else, or to nothing at all.</li>
  <li>An itinerary edited after issue. Changing a date or a name in a PDF editor.</li>
  <li>A screenshot altered to show a booking that was never made.</li>
</ul>
<p>The offence is not &ldquo;not paying for a flight&rdquo;. It is presenting a document to a public authority that
misrepresents a fact. That is the definition of deception in essentially every immigration system.</p>"""),

        ("What happens if you are caught", """
<p>Not a stern letter. Consulates put deception in a completely different box from a weak application:</p>
<div class="tbl-wrap">
<table>
<thead><tr><th>Destination</th><th>Typical consequence of a deception finding</th></tr></thead>
<tbody>
<tr><td><b>Schengen area</b></td><td>Refusal recorded in the shared visa information system. Visible to all 29 member states on any future application</td></tr>
<tr><td><b>United Kingdom</b></td><td>Refusal plus a re-entry ban, commonly ten years for deception</td></tr>
<tr><td><b>United States</b></td><td>Potential permanent inadmissibility for misrepresentation of a material fact</td></tr>
<tr><td><b>Canada</b></td><td>Misrepresentation finding, typically a five-year bar</td></tr>
<tr><td><b>Australia</b></td><td>Refusal and possible exclusion period under the PIC 4020 provisions</td></tr>
</tbody>
</table>
</div>
<p>These are life-shaping outcomes attached to a document that costs less than lunch when bought properly.</p>"""),

        ("Do consulates actually check?", """
<p>Sometimes, and increasingly. Verification is trivially easy: the PNR lookup is a public web form, and
several consulates and visa application centres now check as routine on files that raise any other question.</p>
<p>The strategic point is that you cannot predict which files get checked. Since a genuine reservation costs roughly
the same as a fake one, the expected-value calculation is not close.</p>
<p>The same logic applies at check-in desks. Airline ground staff verify onward bookings far more often than they used
to, because carrier-liability fines land on the airline.</p>"""),

        ("How to tell a legitimate provider from a risky one", """
<p>Six things to look for, roughly in order of how much they tell you:</p>
<ol>
  <li><strong>Can you verify the PNR yourself?</strong> A legitimate provider tells you how, and expects you to.
  This is the only test that cannot be faked.</li>
  <li><strong>Do they explain the hold period honestly?</strong> &ldquo;Valid for 2 weeks, depending on airline&rdquo; is
  candid. &ldquo;Valid until your visa is approved&rdquo; is not a thing airlines offer.</li>
  <li><strong>Do they promise visa approval?</strong> Nobody can. Treat any guarantee as a warning.</li>
  <li><strong>Is the pricing plausible?</strong> Free is a red flag. Creating a real booking costs the provider
  something. So is &#8377;15,000, which suggests you are buying a refundable fare.</li>
  <li><strong>Do they publish a refund policy for unverifiable bookings?</strong> A provider confident in their
  bookings will commit to this in writing.</li>
  <li><strong>Do they ask for your passport scan?</strong> They do not need it. Names and dates of birth make a
  booking; anything more is unnecessary data collection.</li>
</ol>"""),

        ("The safe way to use one", """
<ul>
  <li>Order from a provider who issues real bookings and says how to verify them.</li>
  <li><strong>Verify the PNR yourself</strong> before submitting anything.</li>
  <li>Give names exactly as printed in the passport. No nicknames, no reordering.</li>
  <li>Time the reservation so it is live on your submission date.</li>
  <li>Never edit the document you receive. If something is wrong, ask for a reissue.</li>
  <li>Buy the real ticket once the visa is granted.</li>
</ul>
<p>Follow those six and you are doing exactly what the consulate expects.</p>"""),
    ],
    faqs=[
        ("Can I be banned for using a dummy ticket?", "<p>Not for a genuine unpaid reservation. That is what consulates ask for. For a fabricated document, yes: deception findings carry multi-year and sometimes permanent bans.</p>"),
        ("Do embassies verify flight bookings?", "<p>Some do routinely, others spot-check. Since verification is free and instant for them, assume yours will be checked.</p>"),
        ("Is it legal to buy a dummy ticket from an agency?", "<p>Yes, provided the agency creates a real reservation. You are buying a booking service, which is what travel agents sell.</p>"),
        ("What if my reservation expires before the decision?", "<p>That is normal and not a problem. Officers check the PNR when they open your file. If yours lapses before then and the file is queried, a reissue solves it.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="flight-reservation-vs-confirmed-ticket",
    cat="Fundamentals",
    title="Flight Reservation vs Confirmed Ticket vs Dummy Ticket",
    meta_title="Flight Reservation vs Confirmed Ticket: What Visas Need",
    desc="Reservation, confirmed ticket, e-ticket, dummy ticket and itinerary explained side by side. What each one is, what it costs, and which one your visa application actually needs.",
    read=6,
    lede="Reservation. Itinerary. Dummy ticket. Confirmed ticket. E-ticket. Five words, roughly two actual "
         "things, and a consulate checklist that uses whichever one it feels like. Let us sort that out.",
    sections=[
        ("The five terms", """
<div class="tbl-wrap">
<table>
<thead><tr><th>Term</th><th>What it is</th><th>Paid?</th><th>Has a PNR?</th><th>Ticket number?</th></tr></thead>
<tbody>
<tr><td><b>Flight reservation</b></td><td>A held booking in an airline system</td><td class="no">No</td><td class="yes">Yes</td><td class="no">No</td></tr>
<tr><td><b>Dummy ticket</b></td><td>Slang for the same thing</td><td class="no">No</td><td class="yes">Yes</td><td class="no">No</td></tr>
<tr><td><b>Itinerary</b></td><td>The document describing either</td><td>n/a</td><td class="yes">Usually</td><td>Depends</td></tr>
<tr><td><b>Confirmed / e-ticket</b></td><td>A purchased, ticketed fare</td><td class="yes">Yes</td><td class="yes">Yes</td><td class="yes">Yes</td></tr>
<tr><td><b>Fabricated PDF</b></td><td>A designed document with nothing behind it</td><td class="no">No</td><td class="no">Fake</td><td class="no">Fake</td></tr>
</tbody>
</table>
</div>
<p>Rows one and two are the same product. Row four is what you buy after approval. Row five is what gets people
banned.</p>"""),

        ("The technical difference: booked vs ticketed", """
<p>Inside an airline's system a passenger record moves through states. When a booking is created the record is
<strong>booked</strong>: the seat is held, the PNR exists, the passenger name is attached. When payment clears, the
record becomes <strong>ticketed</strong> and acquires a 13-digit ticket number.</p>
<p>A reservation stops at booked. Everything on it is real; it simply has not progressed to the payment stage. That is
why the PNR resolves normally on the airline's website, and why a consular officer can confirm the itinerary exists.</p>"""),

        ("Which one does a visa application need?", """
<p>Almost always the reservation. Consular checklists ask for a &ldquo;flight reservation&rdquo;, a &ldquo;flight
itinerary&rdquo; or &ldquo;proof of intended travel&rdquo;. Wording chosen deliberately to avoid requiring a purchase.</p>
<p>Narrow exceptions exist:</p>
<ul>
  <li><strong>Some employment and student visas</strong> ask for confirmed travel once the permit is approved, but
  that comes after the decision, not before.</li>
  <li><strong>Some visa-on-arrival and e-visa systems</strong> ask for a confirmed onward ticket, checked at the border
  rather than in advance.</li>
  <li><strong>A handful of consulates</strong> ask for confirmed tickets for specific categories. If yours does, it
  says so on the checklist, and if it does not say so, it does not.</li>
</ul>"""),

        ("Cost, side by side", """
<div class="tbl-wrap">
<table>
<thead><tr><th>Option</th><th>Typical cost</th><th>Money at risk on refusal</th><th>Time to obtain</th></tr></thead>
<tbody>
<tr><td><b>Reservation from a service</b></td><td>%s&ndash;&#8377;3,000</td><td class="yes">Nothing</td><td>%s</td></tr>
<tr><td><b>Airline hold, where offered</b></td><td>&#8377;0&ndash;&#8377;2,000</td><td class="yes">Nothing</td><td>Minutes</td></tr>
<tr><td><b>Fully refundable fare</b></td><td>&#8377;50,000&ndash;&#8377;2,00,000</td><td>Tied up 1&ndash;4 weeks</td><td>Minutes</td></tr>
<tr><td><b>Standard economy fare</b></td><td>&#8377;35,000&ndash;&#8377;1,50,000</td><td class="no">Most of it</td><td>Minutes</td></tr>
</tbody>
</table>
</div>
<p>The refundable fare deserves a note. It works, but it locks up real money for the length of consular processing,
refunds typically take 7&ndash;30 days to reach the card, and some &ldquo;refundable&rdquo; fares carry cancellation fees larger
than the entire cost of a reservation.</p>""" % (money(PRICE_FLIGHT), DELIVERY)),

        ("Reading your own document", """
<p>Look for these fields to work out what you are holding:</p>
<ul>
  <li><strong>Booking reference / PNR / record locator</strong>: six characters. Present on both reservations and tickets.</li>
  <li><strong>Ticket number</strong>: 13 digits, starting with the airline's three-digit code (e.g. <code>176-</code>
  for Cathay). <em>Present only on a purchased ticket.</em></li>
  <li><strong>Status</strong>: <code>HK</code> or &ldquo;Confirmed&rdquo; means the seat is held; that appears on both.</li>
  <li><strong>Fare / total</strong>: a reservation usually shows no amount paid.</li>
</ul>
<p>No ticket number means you are holding a reservation. For a visa application, that is normally the correct
document.</p>"""),
    ],
    faqs=[
        ("Is a flight reservation the same as a dummy ticket?", "<p>Yes. &lsquo;Dummy ticket&rsquo; is informal industry slang; &lsquo;flight reservation&rsquo; is the term consulates use for the same unpaid booking.</p>"),
        ("Can I use a screenshot of an airline search?", "<p>No. A search result is a price quote, not a booking. There is no passenger name and no PNR. Officers can tell instantly.</p>"),
        ("Do I need a confirmed ticket for a Schengen visa?", "<p>No. Schengen consulates ask for a reservation and EU guidance advises against buying tickets first. See the <a href=\"%s\">Schengen guide</a>.</p>" % url("visa/schengen-visa-flight-reservation")),
    ],
),

# ==========================================================================
dict(
    slug="proof-of-onward-travel-explained",
    cat="Travel rules",
    title="Proof of Onward Travel: Who Asks, Why, and What Counts",
    meta_title="Proof of Onward Travel: Rules, Countries and What Counts",
    desc="Why airlines refuse boarding on one-way tickets, which countries enforce onward travel requirements, what documents are accepted, and the cheapest legitimate way to satisfy the rule.",
    read=7,
    lede="You have a visa. You have a hotel. You get to the check-in desk and a very polite person asks "
         "how you plan to leave the country, and suddenly your holiday is a negotiation. Here is why that "
         "happens, and why it is the airline asking rather than the country you are flying to.",
    sections=[
        ("Why the airline cares more than the border does", """
<p>Under carrier-liability rules operated by most countries, an airline that carries a passenger who is subsequently
refused entry must fly them out again at its own cost, and frequently pays a fine on top. Those costs land on the
airline, not on the government.</p>
<p>Airlines therefore push the check forward to the departure gate. The agent scanning your passport in Delhi or
London is protecting their employer's balance sheet, not enforcing the destination's immigration law.</p>
<p>The practical consequence catches people out: <strong>you can be denied boarding by an airline even when
immigration at the other end would have admitted you without comment.</strong> The airline is making a risk decision,
and it is entitled to.</p>"""),

        ("Which countries enforce it", """
<p>Enforcement is inconsistent by design. It depends on the airline, the route, the agent and sometimes your
nationality. Commonly reported as strict:</p>
<div class="tbl-wrap">
<table>
<thead><tr><th>Region</th><th>Frequently enforced</th></tr></thead>
<tbody>
<tr><td><b>Southeast Asia</b></td><td>Thailand, Indonesia, Philippines, Singapore, Vietnam</td></tr>
<tr><td><b>Americas</b></td><td>United States, Costa Rica, Panama, Peru, Colombia, Brazil</td></tr>
<tr><td><b>Oceania</b></td><td>New Zealand, Australia, Fiji</td></tr>
<tr><td><b>Europe</b></td><td>United Kingdom, Schengen area on visa-free entry</td></tr>
<tr><td><b>Middle East</b></td><td>UAE, Turkey, Qatar</td></tr>
<tr><td><b>Caribbean</b></td><td>Most island nations</td></tr>
</tbody>
</table>
</div>
<p>Treat this as indicative rather than definitive. The rule is enforced unpredictably, which is precisely why
carrying the document is worth the small cost.</p>"""),

        ("What counts as proof", """
<p>Generally accepted:</p>
<ul>
  <li><strong>A flight booking out of the country</strong> within your permitted stay. What airline systems display
  most readily, so it is the least friction.</li>
  <li><strong>An international bus or train ticket</strong>: usually accepted for land borders, though agents are
  less familiar with the formats.</li>
  <li><strong>A ferry booking</strong> on island routes.</li>
</ul>
<p>Generally not accepted:</p>
<ul>
  <li>A search result or price screenshot with no passenger name.</li>
  <li>A domestic flight within the destination country.</li>
  <li>An onward flight dated after your permitted stay expires.</li>
  <li>&ldquo;I will buy one when I am there.&rdquo;</li>
</ul>"""),

        ("The options, and what each really costs", """
<ol>
  <li><strong>Buy a real onward ticket.</strong> Fine if you genuinely need the flight. Expensive if you do not.</li>
  <li><strong>Buy a cheap regional flight.</strong> On some routes a &#8377;3,500 hop to a neighbouring country works and you
  simply do not board it. Only viable where such a route exists.</li>
  <li><strong>Buy a refundable fare and cancel after arrival.</strong> Works, ties up tens of thousands of rupees, and
  the refund takes weeks.</li>
  <li><strong>Use a held reservation.</strong> A real booking with a live PNR, valid long enough to get you through
  check-in and immigration. %s, delivered in %s.</li>
</ol>
<p>The fourth option is not a trick. It matches the document to the purpose: the airline needs to see that you have a
plan to leave, and you need that visible at the moment you board. Once you have cleared immigration, the document has
done its job.</p>""" % (money(PRICE_FLIGHT), DELIVERY)),

        ("Making it work at the desk", """
<ul>
  <li><strong>Have it on your phone and printed.</strong> Airport wifi fails at the worst moments.</li>
  <li><strong>Check the dates against the permitted stay.</strong> A 45-day onward booking on a 30-day exemption is
  worse than useless. It demonstrates an intention to overstay.</li>
  <li><strong>Know your own itinerary.</strong> Being able to answer &ldquo;when are you leaving and to where?&rdquo;
  instantly ends most conversations.</li>
  <li><strong>Verify the PNR before you go to the airport.</strong> Agents increasingly look references up.</li>
</ul>"""),
    ],
    faqs=[
        ("Can I be denied boarding without proof of onward travel?", "<p>Yes. It is one of the most common reasons for denied boarding on one-way tickets, and it is the airline's decision, not the destination government's.</p>"),
        ("Does a bus ticket count?", "<p>Usually, if it crosses an international border within your permitted stay. Flight bookings are read fastest by airline staff.</p>"),
        ("How long must the onward booking be valid?", "<p>Only until you have boarded and cleared immigration, which is why an expensive refundable fare is poor value for this purpose.</p>"),
        ("Is this the same as a visa requirement?", "<p>No. Some countries do require it for a visa, but the check you are most likely to face happens at check-in, under airline liability rules.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="how-long-is-a-flight-reservation-valid",
    cat="Practical",
    title="How Long Is a Flight Reservation Valid?",
    meta_title="How Long Is a Flight Reservation Valid? Hold Times Explained",
    desc="Airline hold periods run from 48 hours to about 14 days. Why they vary, what happens when a reservation expires mid-application, and how to time yours around a consular appointment.",
    read=6,
    lede="Everyone asks this. Almost everyone is worried about the wrong half of it. Yes, the booking "
         "expires. No, that is usually not the problem you think it is.",
    sections=[
        ("The typical range", """
<p><strong>48 hours to roughly 14 days.</strong> Within that range, the hold period depends on:</p>
<ul>
  <li><strong>The airline.</strong> Full-service carriers generally hold longer than low-cost ones, which frequently
  do not offer holds at all.</li>
  <li><strong>The route.</strong> High-demand routes get shorter holds because seats are scarce.</li>
  <li><strong>How far ahead you are travelling.</strong> Departures months out often permit longer holds.</li>
  <li><strong>Fare class.</strong> Restricted promotional fares are usually not held at all.</li>
</ul>
<p>A booking made three months before travel on a moderately busy route commonly holds for about a week. That is the
realistic planning assumption.</p>"""),

        ("Why nobody can promise 30 days", """
<p>The hold is the airline's decision, not the provider's. Any service advertising &ldquo;valid for 30 days&rdquo; or
&ldquo;valid until your visa is approved&rdquo; is describing something airlines do not sell.</p>
<p>Longer validity generally means one of three things: a genuinely refundable ticket has been purchased (in which
case the price reflects it), the booking will be silently rebooked when it lapses, or the document is not backed by a
booking at all.</p>"""),

        ("What actually happens when it expires", """
<p>The airline releases the seat and the PNR stops resolving. The PDF in your inbox does not change, but the
lookup behind it now returns nothing.</p>
<p>Here is the part that calms most people down: <strong>consular officers check the PNR when they open your file,
which is usually within a few days of submission.</strong> They do not re-check weeks later. If your reservation
lapses after the officer has already looked, nothing has gone wrong.</p>
<p>The risk case is narrow: a file that sits untouched for weeks and is then queried. Even then the fix is a free
reissue, not a new application.</p>"""),

        ("Timing it around your appointment", """
<div class="tbl-wrap">
<table>
<thead><tr><th>Your situation</th><th>When to order</th></tr></thead>
<tbody>
<tr><td><b>Appointment already booked</b></td><td>1&ndash;2 days before the appointment</td></tr>
<tr><td><b>Online upload with no appointment</b></td><td>The day you intend to upload</td></tr>
<tr><td><b>Postal or drop-box submission</b></td><td>The day you post it, allowing for transit</td></tr>
<tr><td><b>Proof of onward travel at check-in</b></td><td>1&ndash;2 days before you fly</td></tr>
<tr><td><b>Insurance quote needing fixed dates</b></td><td>Any time. The dates matter, not the live booking</td></tr>
</tbody>
</table>
</div>
<p>The general rule: order so that the reservation is <em>live on the day the document is first seen by someone</em>.
Ordering three weeks early does not help and can hurt.</p>"""),

        ("If your appointment moves", """
<p>Appointments get rescheduled constantly. Slot availability, biometrics, document requests. Any provider worth
using will reissue the reservation for the new date without charge. Ours does; if yours does not, that tells you
something about the underlying booking.</p>
<div class="note note--ok"><strong>Our policy</strong>
One free reissue per order, for a name correction or a date change. Email us with the order reference and the new
date. If the airline releases a booking earlier than expected, that reissue is on us and does not count against your
free change.</div>"""),
    ],
    faqs=[
        ("What happens if my reservation expires before the decision?", "<p>Usually nothing. Officers check the PNR when they open the file, typically within days of submission. A lapse after that point has no effect.</p>"),
        ("Can I extend a flight reservation?", "<p>Not extend, but it can be reissued, which creates a fresh booking with a new hold period. One reissue is included with every order.</p>"),
        ("Do longer hold periods cost more?", "<p>Not from us. Hold length is set by the airline and the route, not sold as an upgrade.</p>"),
        ("How far ahead should I order?", "<p>One to two days before the document will first be seen. Earlier does not help.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="do-embassies-verify-flight-bookings",
    cat="Legality",
    title="Do Embassies Actually Verify Flight Bookings?",
    meta_title="Do Embassies Verify Flight Bookings? What Officers Check",
    desc="How consular officers check a flight reservation, which missions verify routinely, what a failed check looks like on your record, and how to make sure yours passes.",
    read=6,
    lede="The honest answer is: sometimes, and more often than they used to. The more useful answer is "
         "that the check takes an officer about fifteen seconds, costs them nothing, and you cannot "
         "predict which files get it.",
    sections=[
        ("How the check works", """
<p>There is no secret consular database. An officer does exactly what you can do from your sofa: opens the operating airline's
&ldquo;manage booking&rdquo; page, types the six-character PNR and the surname, and reads what comes back.</p>
<p>Three outcomes:</p>
<ul>
  <li><strong>The itinerary appears</strong>, matching the document. The check passes.</li>
  <li><strong>Nothing is found.</strong> Either the booking never existed, or it has been released. Both invite a
  question, but only one is fraud.</li>
  <li><strong>A different itinerary appears.</strong> The PNR belongs to somebody else. The worst outcome, and a
  clear indicator of a recycled or fabricated reference.</li>
</ul>
<p>Larger visa application centres also work with the agency channels that issued the booking, which makes
verification even faster.</p>"""),

        ("Who checks, and when", """
<p>Verification concentrates around risk. A file is more likely to be checked when:</p>
<ul>
  <li>The applicant is a first-time traveller with a thin passport history.</li>
  <li>Financial documents look inconsistent with the stated trip.</li>
  <li>The itinerary is implausible. A six-week holiday on two weeks of leave.</li>
  <li>The document has formatting oddities: wrong fonts, missing agency details, a PNR in the wrong format.</li>
  <li>The mission has recently seen a cluster of fabricated documents from a particular market.</li>
</ul>
<p>That last point matters more than applicants realise. Verification rates are not constant. They spike when a
mission finds a batch of forgeries, and everyone applying that month gets checked.</p>"""),

        ("What a failed check does to your record", """
<p>A missing booking is not automatically treated as fraud. An officer who finds nothing may simply request an
updated itinerary, particularly if your file is otherwise strong.</p>
<p>A <em>fabricated</em> document is different. Once an officer concludes you intended to deceive, the finding is
recorded, and it follows you:</p>
<ul>
  <li>Schengen refusals are visible to all member states on future applications.</li>
  <li>UK deception findings commonly attract a ten-year ban.</li>
  <li>US misrepresentation can create permanent inadmissibility.</li>
  <li>Canadian misrepresentation typically carries a five-year bar.</li>
</ul>
<p>You will also be asked, on every future application to almost anywhere, whether you have previously been refused a
visa. Answering that honestly is a permanent handicap; answering it dishonestly compounds the original problem.</p>"""),

        ("Making sure yours passes", """
<ol>
  <li><strong>Verify it yourself first.</strong> Non-negotiable, and it takes two minutes.
  <a href="%s">Here is how</a>.</li>
  <li><strong>Check the operating carrier</strong> on codeshares. The booking lives with the airline that flies
  the aircraft, not the one on the flight number.</li>
  <li><strong>Match the name exactly</strong> to the passport, surname first.</li>
  <li><strong>Submit while the booking is live.</strong> Order one to two days before your appointment.</li>
  <li><strong>Never edit the PDF.</strong> An altered document contradicts the booking behind it, which converts
  a valid reservation into evidence of tampering.</li>
</ol>""" % url("verify-pnr")),
    ],
    faqs=[
        ("Can an embassy tell my ticket is unpaid?", "<p>Yes. A reservation shows a booking status with no ticket number. This is expected. Consulates ask for reservations precisely so applicants do not buy fares first.</p>"),
        ("Will an expired reservation be treated as fraud?", "<p>Not normally. An expired booking is a lapsed real booking, not a fabricated one. An officer may ask for an updated itinerary.</p>"),
        ("Do visa application centres verify bookings?", "<p>VFS, TLScontact and similar centres check documents for completeness and increasingly verify references before passing the file to the consulate.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="hotel-booking-for-visa-application",
    cat="Practical",
    title="Hotel Booking for a Visa Application: What Consulates Check",
    meta_title="Hotel Booking for Visa Application: Rules and Common Errors",
    desc="Why consulates ask for accommodation proof, what a valid hotel booking must show, how to cover multi-city trips without gaps, and when an invitation letter replaces a booking entirely.",
    read=6,
    lede="Accommodation proof is the document people throw together at eleven at night, the evening before "
         "the appointment. It is also the one that fails on the most boring, most avoidable grounds. "
         "Nobody is judging your taste in hotels. They are counting nights.",
    sections=[
        ("Why it is asked for", """
<p>Two reasons, and neither of them is curiosity about your choice of hotel.</p>
<p>First, <strong>it corroborates your itinerary</strong>. Anyone can claim a two-week trip to Italy. A booking for
fourteen nights in Rome and Florence, with dates matching the flights, makes the claim concrete.</p>
<p>Second, <strong>it demonstrates you have somewhere to be</strong>. Consulates are assessing whether you have
planned a temporary visit. An applicant with no accommodation plan looks like someone whose plans do not end.</p>"""),

        ("The four mechanical checks", """
<ol>
  <li><strong>Full coverage.</strong> Every night between arrival and departure must be accounted for. One uncovered
  night invites the obvious question.</li>
  <li><strong>Name match.</strong> The lead guest must be the applicant, spelled as in the passport.</li>
  <li><strong>A real property, with contact details.</strong> Address and phone number that resolve to an actual
  business.</li>
  <li><strong>Date consistency with the flights.</strong> Check-in should not precede arrival; check-out should not
  follow departure.</li>
</ol>
<p>None of this is subjective, which is exactly why it is worth ten minutes of checking before you submit.</p>"""),

        ("Multi-city trips: where files fail", """
<p>The single most common accommodation error is a multi-city itinerary with a single-city booking.</p>
<p>If your plan is Paris (3 nights) &rarr; Amsterdam (4 nights) &rarr; Berlin (3 nights), you need three bookings
covering ten nights with no gaps and no overlaps. A ten-night Paris booking contradicts your own itinerary and
signals that the plan was assembled to satisfy a checklist rather than to describe a trip.</p>
<p>Japan makes this explicit by requiring a day-by-day schedule of stay. Schengen missions do not ask for the same
format, but they perform the same arithmetic.</p>"""),

        ("When you do not need a hotel booking", """
<p>If you are staying with family or friends, you need an <strong>invitation letter</strong> instead, typically with:</p>
<ul>
  <li>The host's full name, address and contact details</li>
  <li>Their status in the country. Citizen, resident, valid permit</li>
  <li>Your relationship to them</li>
  <li>The dates you will stay</li>
  <li>A statement of who is covering costs</li>
</ul>
<p>Some countries formalise this: Germany's <em>Verpflichtungserklärung</em>, the Netherlands' proof of sponsorship
form, Italy's <em>dichiarazione di ospitalità</em>. Check whether yours requires the official form.</p>
<div class="note"><strong>Do not submit both, inconsistently</strong>
An invitation letter for the full stay plus a hotel booking for part of it, with no explanation, reads as confusion at
best. Pick the arrangement that is true and document it cleanly.</div>"""),

        ("Should you pay for accommodation before approval?", """
<p>Not usually. The same logic that applies to flights applies here: a refusal should not cost you a non-refundable
booking.</p>
<p>The standard approach is a confirmed booking under a free-cancellation policy. Real, referenced, and
cancellable at no cost. That is what we issue for %s, or %s bundled with a flight reservation with the dates
reconciled automatically.</p>""" % (money(PRICE_HOTEL), money(PRICE_BOTH))),
    ],
    faqs=[
        ("Do I need a hotel booking for every night?", "<p>Yes for Schengen and most tourist visas. Gaps get noticed because officers count nights.</p>"),
        ("Can I book on a travel site and cancel later?", "<p>Yes, if the rate is genuinely free-cancellation and you are honest about it. The booking must be real and live when your file is reviewed.</p>"),
        ("What if I am staying with family?", "<p>Submit an invitation letter with the host's details instead of a hotel booking. Some countries require an official sponsorship form.</p>"),
        ("Does the booking need to be paid?", "<p>No. Consulates need to see accommodation arranged, not paid for.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="visa-application-document-checklist",
    cat="Practical",
    title="The Visa Application Document Checklist That Actually Works",
    meta_title="Visa Application Document Checklist: Complete 2026 Guide",
    desc="A universal document checklist for tourist visa applications: what every consulate wants, how the documents must agree with each other, and the order to prepare them in.",
    read=8,
    lede="Every consulate publishes its own list, and underneath the variation almost all of them are the "
         "same eight things. The part nobody writes down is that your file is not eight documents. It is "
         "one story told eight times, and the officer is checking whether the tellings agree.",
    sections=[
        ("The eight components", """
<ol>
  <li><strong>Application form</strong>: completed online or on paper, signed.</li>
  <li><strong>Passport</strong>: usually valid six months beyond your return, with blank pages.</li>
  <li><strong>Photographs</strong>: to the mission's exact specification. Rejections here are common and entirely
  avoidable.</li>
  <li><strong>Flight itinerary</strong>: a reservation showing entry and exit dates.</li>
  <li><strong>Accommodation proof</strong>: hotel bookings, or an invitation letter.</li>
  <li><strong>Financial evidence</strong>: bank statements, usually three to six months.</li>
  <li><strong>Ties to your home country</strong>: employment letter, business registration, property, enrolment.</li>
  <li><strong>Travel insurance</strong>: mandatory for Schengen (&euro;30,000 minimum), optional elsewhere.</li>
</ol>"""),

        ("The principle nobody writes down: consistency", """
<p>Read your own file the way an officer will: not as eight documents, but as one story told eight times. They are
checking whether the tellings agree.</p>
<p>Contradictions that sink otherwise strong applications:</p>
<ul>
  <li>Flight arrival on the 12th, hotel check-in on the 10th.</li>
  <li>An employment letter granting two weeks' leave against a four-week itinerary.</li>
  <li>Insurance expiring the day before the return flight.</li>
  <li>A bank balance that cannot fund the trip described.</li>
  <li>An application form listing a hotel that no booking supports.</li>
</ul>
<p>Every one of those is a ten-minute fix before submission and an unrecoverable problem after it.</p>"""),

        ("The order to prepare them in", """
<p>Sequence matters, because later documents depend on earlier ones.</p>
<div class="tbl-wrap">
<table>
<thead><tr><th>#</th><th>Step</th><th>Why here</th></tr></thead>
<tbody>
<tr><td>1</td><td>Fix your dates</td><td>Everything else derives from them</td></tr>
<tr><td>2</td><td>Book the appointment</td><td>Slots drive your whole timeline</td></tr>
<tr><td>3</td><td>Gather financials</td><td>Statements need lead time from the bank</td></tr>
<tr><td>4</td><td>Get the employment / ties letter</td><td>Employers are slow; ask early</td></tr>
<tr><td>5</td><td>Arrange accommodation</td><td>Must match the dates from step 1</td></tr>
<tr><td>6</td><td>Buy insurance</td><td>Must cover the exact travel dates</td></tr>
<tr><td>7</td><td>Order the flight reservation</td><td><strong>Last</strong>: so it is live at submission</td></tr>
<tr><td>8</td><td>Cross-check everything</td><td>The step people skip</td></tr>
</tbody>
</table>
</div>
<p>The flight reservation goes last deliberately. It has the shortest shelf life of anything in the file, <a href="%s">typically 48 hours to 14 days</a>, so ordering it first wastes the hold window.</p>""" % url("blog/how-long-is-a-flight-reservation-valid")),

        ("The final cross-check", """
<p>Ten minutes, before anything is submitted. Read the file as an officer would:</p>
<ul>
  <li>Is your name spelled identically on every document, in passport order?</li>
  <li>Do the flight dates match the hotel dates, the insurance dates and the form?</li>
  <li>Does the leave granted cover the trip described?</li>
  <li>Do the funds plausibly cover the itinerary?</li>
  <li>Does the PNR verify? <a href="%s">Check it</a>.</li>
  <li>Is every page legible, right way up, and a real PDF rather than a photo of a screen?</li>
</ul>
<div class="note note--ok"><strong>The single highest-value habit</strong>
Read your own file front to back as though you were looking for reasons to refuse it. Almost everyone finds at least
one contradiction on the first pass.</div>""" % url("verify-pnr")),
    ],
    faqs=[
        ("What is the most common reason for refusal?", "<p>Insufficient evidence of ties to the home country, followed by inconsistent or insufficient financial documentation. Missing travel documents are usually a request for more information rather than a refusal.</p>"),
        ("How many months of bank statements?", "<p>Three to six is the usual range. Officers look for a stable balance rather than a large deposit that appeared last week.</p>"),
        ("When should I order the flight reservation?", "<p>Last, one to two days before submission, so the hold is live when the file is reviewed.</p>"),
        ("Do I need insurance before applying?", "<p>For Schengen, yes: &euro;30,000 minimum covering the exact travel dates. Buy it after your itinerary is fixed.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="common-visa-rejection-reasons",
    cat="Practical",
    title="Why Tourist Visas Get Refused, and What Fixes It",
    meta_title="Common Visa Rejection Reasons and How to Avoid Them",
    desc="The refusal reasons consulates actually cite, ranked: weak ties, thin finances, inconsistent documents and travel-document errors. What each one means and how to address it.",
    read=8,
    lede="Refusal letters are short, formulaic and maddeningly vague, which leaves you guessing at what "
         "went wrong. The underlying reasons are actually pretty consistent across missions, and most of "
         "them are fixable before you apply rather than after.",
    sections=[
        ("1. Insufficient ties to your home country", """
<p>The biggest category by a mile, and the one people put the least work into.</p>
<p>The officer is answering one question: <em>will this person go home?</em> The presumption in most systems, and explicitly so in US law, is that you will not, and it is your job to rebut it.</p>
<p><strong>What helps:</strong> an employment letter stating role, tenure, salary and approved leave dates; property
documents; business registration and tax filings if self-employed; enrolment records; evidence of dependants
remaining behind; a history of previous travel with timely returns.</p>
<p><strong>What does not help:</strong> asserting that you intend to return. Everyone asserts that.</p>"""),

        ("2. Financial evidence that does not hold up", """
<p>It is rarely just &ldquo;not enough money&rdquo;. Officers look at the <em>shape</em> of the account.</p>
<ul>
  <li>A large deposit shortly before applying, with no explanation, reads as borrowed funds.</li>
  <li>A balance that cannot support the itinerary described.</li>
  <li>Statements that are unstamped, unsigned or clearly assembled from screenshots.</li>
  <li>A sponsor mentioned nowhere in the paperwork.</li>
</ul>
<p><strong>Fix:</strong> plan three to six months ahead so the statements show a stable balance. If someone is
sponsoring you, document it properly. Their letter, their statements, proof of the relationship.</p>"""),

        ("3. Documents that contradict each other", """
<p>The most avoidable category on this list, and the reason ten minutes of cross-checking beats adding another
document to the pile.</p>
<p>Flight dates against hotel dates. Leave granted against trip length. Insurance validity against return date. Form
answers against supporting documents. Each contradiction on its own might be an oversight; two or three together read
as a file assembled to pass rather than to describe a real trip.</p>
<p>Ten minutes with a <a href="%s">checklist</a> resolves nearly all of it.</p>""" % url("blog/visa-application-document-checklist")),

        ("4. Travel documents that fail verification", """
<p>Rarer than the others. Far worse when it happens.</p>
<p>A missing or expired booking usually produces a request for an updated itinerary. A <em>fabricated</em> one
produces a deception finding, which carries multi-year bans and, in the US, potentially permanent inadmissibility.</p>
<p><strong>Fix:</strong> use a real reservation and <a href="%s">verify the PNR yourself</a> before submitting. It is
the cheapest risk reduction available anywhere in the process.</p>""" % url("verify-pnr")),

        ("5. An itinerary that does not add up", """
<p>Officers read thousands of these. They develop a nose for a trip that does not quite add up.</p>
<ul>
  <li>A six-week holiday on two weeks of annual leave.</li>
  <li>Eight countries in ten days.</li>
  <li>A trip costing several times your monthly income with no sponsor.</li>
  <li>A first-ever international trip to the hardest destination to get, alone, in low season.</li>
</ul>
<p><strong>Fix:</strong> apply for the trip you are actually taking. A modest, coherent, well-documented plan beats an
ambitious one every time.</p>"""),

        ("6. Administrative errors", """
<p>Boring, and entirely preventable: photographs to the wrong specification, an unsigned form, a passport with
under six months validity or no blank pages, a missing appointment confirmation, the wrong fee.</p>
<p><strong>Fix:</strong> read the mission's own checklist, not a blog and not a forum, in the week before you
submit. It is the authoritative source and it changes.</p>"""),

        ("If you are refused", """
<ol>
  <li><strong>Read the stated ground carefully.</strong> Schengen refusals use numbered codes; match yours to the
  specific deficiency.</li>
  <li><strong>Do not immediately reapply with the same file.</strong> A second refusal on identical evidence weakens
  you further.</li>
  <li><strong>Fix the cited ground.</strong> Weak ties means better ties evidence, not a nicer itinerary.</li>
  <li><strong>Consider appealing</strong> where the process exists and the refusal looks like an error of fact.</li>
  <li><strong>Declare it honestly</strong> on future applications. Undeclared refusals get discovered, and turn a
  refusal into a deception finding.</li>
</ol>"""),
    ],
    faqs=[
        ("Can I reapply immediately after a refusal?", "<p>Usually yes, but reapplying with unchanged evidence generally produces the same result. Address the stated ground first.</p>"),
        ("Does one refusal ruin future applications?", "<p>No. A refusal on evidentiary grounds is recoverable. A deception finding is a different and far more serious matter.</p>"),
        ("Do I have to declare previous refusals?", "<p>Yes, always, on every application that asks. Non-disclosure is treated as deception, which is worse than the original refusal.</p>"),
        ("Will a better flight itinerary fix a refusal?", "<p>Only if the itinerary was the cited problem. If the ground was weak ties or finances, the itinerary is not the issue.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="how-to-choose-a-dummy-ticket-service",
    cat="Legality",
    title="How to Choose a Dummy Ticket Service (and Spot a Bad One)",
    meta_title="How to Choose a Dummy Ticket Service: 8 Checks Before Paying",
    desc="Eight checks to run before paying any flight reservation service, the claims that indicate a fabricated document, and why the cheapest option is not the risky one.",
    read=7,
    lede="This market is unregulated, the sites all look the same, and the difference between a fine "
         "provider and one that gets you a ten-year ban is invisible from the homepage. It is not "
         "invisible from eight specific questions, though.",
    sections=[
        ("1. Can you verify the PNR yourself?", """
<p>This is the only test that cannot be faked, which makes it the only one that finally matters.</p>
<p>A legitimate provider tells you how to check, names the airline's manage-booking page, and expects you to use it.
A provider that discourages verification. &ldquo;only the embassy can check this&rdquo;, &ldquo;checking may cancel your
booking&rdquo;. Is telling you something important. Neither statement is true. PNR lookups are public and
read-only.</p>"""),

        ("2. Is the validity claim honest?", """
<p>Hold periods are set by airlines. Honest ranges look like &ldquo;48 hours to 14 days, depending on the airline and
route&rdquo;.</p>
<p>Claims that should stop you: &ldquo;valid 30 days guaranteed&rdquo;, &ldquo;valid until your visa is approved&rdquo;,
&ldquo;never expires&rdquo;. Airlines do not sell those terms. Something else is going on.</p>"""),

        ("3. Do they promise visa approval?", """
<p>No document supplier can influence a visa decision, and any that claims to is either lying or misunderstands the
process. &ldquo;100% visa success rate&rdquo; is a marketing fiction attached to a document that satisfies one line of a
checklist.</p>"""),

        ("4. Is the price plausible?", """
<div class="tbl-wrap">
<table>
<thead><tr><th>Price</th><th>What it usually means</th></tr></thead>
<tbody>
<tr><td><b>Free</b></td><td>Generated document, or a lead magnet for something else. Creating a real booking has a cost.</td></tr>
<tr><td><b>&#8377;300&ndash;&#8377;3,000</b></td><td>The normal range for a genuine held reservation</td></tr>
<tr><td><b>&#8377;8,000&ndash;&#8377;25,000</b></td><td>Usually a semi-refundable ticket, or heavy margin</td></tr>
<tr><td><b>&#8377;35,000+</b></td><td>You are buying a refundable fare, not a reservation</td></tr>
</tbody>
</table>
</div>
<p>Note that cheap is not the risk signal here. A real booking genuinely costs the provider very little, because no
fare is paid. Free is the signal.</p>"""),

        ("5. Is there a written refund policy?", """
<p>Specifically for a booking that fails to verify. A provider confident in their bookings will commit to that in
writing. A vague &ldquo;no refunds&rdquo; policy on a document whose entire value is its verifiability tells you they
expect failures.</p>"""),

        ("6. How much personal data do they ask for?", """
<p>A booking needs names and dates of birth. It does not need passport scans, passport numbers, visa application
copies or ID photographs.</p>
<p>Providers who collect all of that are either careless about data minimisation or collecting it for reasons
unconnected to your booking. Neither is reassuring in an industry serving people at their most document-anxious.</p>"""),

        ("7. Are they contactable?", """
<p>A working email that answers, a real support channel, and ideally a company identity. If your document has a
problem two hours before an appointment, a contact form that goes nowhere is worthless.</p>
<p>Be sceptical of stock-photo teams and testimonials with no verifiable source, but note the inverse too: a
provider who leaves a section of their About page visibly unfinished rather than filling it with invented detail is
telling you something good.</p>"""),

        ("8. What do they say about legality?", """
<p>A provider that explains the distinction between a real unpaid reservation and a fabricated document understands
its own product and expects you to. A provider that avoids the topic, or insists everything is &ldquo;100%% legal&rdquo;
without saying <em>why</em>, is hoping you do not ask.</p>
<div class="note"><strong>Our own answers, for comparison</strong>
Verify at the airline's own site. We tell you how. Hold periods 48 hours to 14 days, airline-dependent. No approval
guarantees, ever. %s per traveller. Full refund if a reference does not verify. Names and dates of birth only, no
passport scans. Email answered by people. And the legality distinction is
<a href="%s">set out in full here</a>.</div>""" % (money(PRICE_FLIGHT), url("blog/is-a-dummy-ticket-legal"))),
    ],
    faqs=[
        ("Are free dummy ticket generators safe?", "<p>Generally no. Creating a real airline booking costs the provider something, so a free tool is usually producing a document rather than a booking. That is the category that causes deception findings.</p>"),
        ("Is a cheap reservation lower quality?", "<p>Not necessarily. Because no fare is paid, the underlying cost is genuinely low. Judge on verifiability and refund terms, not price.</p>"),
        ("Should I give a service my passport scan?", "<p>No. A booking needs your name and date of birth. Anything more is unnecessary data collection.</p>"),
    ],
),
]


# --------------------------------------------------------------------------
def build():
    _index()
    for i, p in enumerate(POSTS):
        _post(p, i)


def _index():
    c_html, c_schema = crumbs([("Blog", None)])
    cards = ""
    for p in POSTS:
        cards += """
<a class="card card--link post-card" href="%s">
  <span class="tagline">%s &middot; %d min read</span>
  <h3>%s</h3>
  <p>%s</p>
  <span class="more">Read the guide &rarr;</span>
</a>""" % (url("blog/" + p["slug"]), p["cat"], p["read"], p["title"], p["desc"][:135].rsplit(" ", 1)[0] + "&hellip;")

    body = """
<section>
  <div class="wrap">
    %s
    <div class="center" style="margin-bottom:2.6rem">
      <h1>Visa travel documents, explained properly</h1>
      <p class="lede">No hype, no guaranteed-approval nonsense. What consulates ask for, why they ask for it, and
      where applications go wrong. Written by people who prepare these documents every day.</p>
    </div>
    <h2 class="sr">All articles</h2>
    <div class="grid g3">%s</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Looking for your destination?</h2>
    <p class="lede">Country-specific requirements, hold periods and refusal traps.</p>
    <p style="margin-top:1.4rem"><a class="btn btn--primary" href="%s">Browse visa guides</a></p>
  </div>
</section>
%s""" % (c_html, cards, url("visa"), cta_band())

    blog_schema = {
        "@type": "Blog",
        "@id": abs_url("blog") + "#blog",
        "url": abs_url("blog"),
        "name": "%s blog" % BRAND,
        "description": "Guides to flight reservations, hotel bookings and visa documentation.",
        "publisher": {"@id": SITE_URL + "/#organization"},
        "blogPost": [{"@type": "BlogPosting", "headline": p["title"],
                      "url": abs_url("blog/" + p["slug"])} for p in POSTS],
    }
    add_page("blog", "Blog | Visa Flight Reservation & Travel Document Guides",
             "Guides to dummy tickets, flight reservations, hotel bookings, PNR verification and visa documentation. Written without the marketing gloss.",
             body, schema=[c_schema, blog_schema], priority="0.8", changefreq="weekly")


def _post(p, index):
    slug = "blog/" + p["slug"]
    c_html, c_schema = crumbs([("Blog", "blog"), (p["title"], None)])

    toc, sections = "", ""
    for h, html in p["sections"]:
        anchor = slugify(__import__("re").sub(r"<[^>]+>", "", h))[:60]
        toc += '<li><a href="#%s">%s</a></li>' % (anchor, h)
        sections += '<h2 id="%s">%s</h2>%s' % (anchor, h, html)

    # related: next two posts, wrapping
    rel = ""
    for j in (1, 2):
        o = POSTS[(index + j) % len(POSTS)]
        rel += """
<a class="card card--link post-card" href="%s">
  <span class="tagline">%s</span><h3>%s</h3>
  <span class="more">Read &rarr;</span></a>""" % (url("blog/" + o["slug"]), o["cat"], o["title"])

    body = """
<section>
  <div class="wrap">
    %s
    <div class="article">
      <p class="eyebrow">%s</p>
      <h1>%s</h1>
      <p class="meta"><span>%d min read</span><span>Updated %s</span><span>%s</span></p>
      <p class="lede">%s</p>
      <nav class="toc" aria-label="Contents"><b>On this page</b><ol>%s</ol></nav>
      %s
      <hr>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Keep reading</h2>
    <div class="grid g2" style="margin-top:1.4rem">%s</div>
  </div>
</section>

%s""" % (c_html, p["cat"], p["title"], p["read"], TODAY, AUTHOR, p["lede"], toc, sections,
         faq_block(p["faqs"], "Questions people ask about this", level="h2"),
         rel, cta_band())

    article = {
        "@type": "BlogPosting",
        "@id": abs_url(slug) + "#article",
        "headline": p["meta_title"],
        "alternativeHeadline": p["title"],
        "description": p["desc"],
        "url": abs_url(slug),
        "datePublished": TODAY,
        "dateModified": TODAY,
        "inLanguage": "en",
        "articleSection": p["cat"],
        "wordCount": len(__import__("re").sub(r"<[^>]+>", " ", "".join(h for _, h in p["sections"])).split()),
        "author": {"@type": "Organization", "name": BRAND, "url": SITE_URL + "/"},
        "publisher": {"@id": SITE_URL + "/#organization"},
        "isPartOf": {"@id": abs_url("blog") + "#blog"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": abs_url(slug)},
        "image": SITE_URL + "/assets/img/og-default.png",
    }

    add_page(slug, p["meta_title"] + " | " + BRAND, p["desc"], body,
             schema=[c_schema, article, faq_schema(p["faqs"])],
             og_type="article", og_title=p["title"],
             priority="0.7", changefreq="monthly")
