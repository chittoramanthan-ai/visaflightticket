# -*- coding: utf-8 -*-
"""
Second wave of blog posts, appended to content_blog.POSTS.

Kept in its own module because content_blog.py was already close to a
thousand lines. Same dict shape, same builder, no special handling: see
content_blog._post() for the fields consumed.

These three target queries where the searcher has a decision to make and
nobody has written a straight answer:

  1. schengen-visa-appointment-flight-reservation
       "flight reservation for Schengen visa appointment" -- high intent,
       and the appointment-vs-application distinction trips people up.
  2. do-embassies-call-the-airline
       "will the embassy call the airline" -- pure anxiety query, and the
       honest answer happens to be our whole differentiator.
  3. dummy-ticket-vs-refundable-ticket
       "refundable ticket for visa" -- the comparison a careful applicant
       actually runs, and the one where the arithmetic favours us.
"""

from build import DELIVERY, PRICE_FLIGHT, PRICE_BOTH, money


POSTS_EXTRA = [

# ==========================================================================
dict(
    slug="schengen-visa-appointment-flight-reservation",
    cat="Practical",
    title="Do You Need a Flight Reservation for the Schengen Appointment, or Only for the Application?",
    meta_title="Flight Reservation for a Schengen Visa Appointment",
    desc="VFS and consulate appointments have different document rules from the application itself. When a flight reservation is needed to book the slot, when it is needed on the day, and how to time the booking so it is still valid.",
    read=8,
    lede="You cannot book the appointment without the documents, and you do not want to buy the documents "
         "before you have the appointment. Almost everyone applying for a Schengen visa hits this loop, and "
         "almost every forum answer to it is wrong in one direction or the other. Here is how the timing "
         "actually works.",
    sections=[
        ("The two moments people confuse", """
<p>There are two separate points where a Schengen application touches a flight reservation, and they have different
rules:</p>
<ol>
  <li><strong>Booking the appointment slot.</strong> Done online through VFS Global, TLScontact, BLS or the consulate's
  own portal, sometimes weeks in advance.</li>
  <li><strong>The appointment itself.</strong> You physically hand over a document folder and give biometrics.</li>
</ol>
<p>The confusion comes from people describing both as &ldquo;the appointment&rdquo;. The document you need, and when you
need it, is different for each.</p>"""),

        ("Booking the slot: usually no reservation needed", """
<p>For most Schengen consulates, booking the appointment slot requires your passport number, personal details and a
travel-date range. Not a flight reservation.</p>
<p>This matters more than it sounds. Appointment slots at busy consulates are the genuine bottleneck. In peak season
the wait for a slot can exceed the wait for a decision. If you believe you need a flight reservation before you can
even book a slot, you delay the one step that is actually scarce.</p>
<div class="note">
  <strong>Book the slot first</strong>
  The slot is the scarce resource. The documents are not. Secure the date, then prepare the folder against that
  date. Doing it the other way round is how people end up with a reservation that expires before they are seen.
</div>"""),

        ("The appointment itself: yes, bring it", """
<p>On the day, the checklist applies in full, and every Schengen consulate's checklist includes evidence of transport.
The standard wording is some variant of <em>&ldquo;round-trip flight reservation or other proof of intended
transport&rdquo;</em>. What is being asked for is a reservation, not a purchased ticket.</p>
<p>The European Commission's visa handbook is explicit that applicants should not be required to hold a paid ticket
before a decision. Consulates follow this because the alternative is applicants losing airfare on refusals. A
reservation with a live PNR satisfies the requirement.</p>
<p>Two details on the day that cause avoidable problems:</p>
<ul>
  <li><strong>Print it.</strong> Many centres will not accept a document shown on a phone screen. Bring paper.</li>
  <li><strong>Match the dates exactly.</strong> The dates on the reservation must agree with the dates on your
  application form and your travel insurance. A one-day discrepancy between the three is a common reason for a file
  being handed back at the counter.</li>
</ul>"""),

        ("Timing it so the reservation is still valid", """
<p>A held reservation does not last forever. Airline hold periods typically run from 24 hours to about 14 days
depending on carrier and fare class. If you order a reservation three weeks before your appointment, it can lapse
before anyone looks at it.</p>
<p>The sequence that works:</p>
<div class="tbl-wrap">
<table>
  <thead><tr><th>When</th><th>Do this</th></tr></thead>
  <tbody>
    <tr><td>As early as possible</td><td>Book the appointment slot. No flight document needed.</td></tr>
    <tr><td>2 to 4 weeks before</td><td>Assemble everything slow: insurance, bank statements, employment letter, accommodation.</td></tr>
    <tr><td>3 to 5 days before</td><td>Order the flight reservation and hotel booking. Delivered in {DELIVERY}.</td></tr>
    <tr><td>The day before</td><td>Verify the PNR yourself on the airline's site. Print everything.</td></tr>
  </tbody>
</table>
</div>
<p>Ordering a few days out is not cutting it fine. It is the point at which the document is freshest for the person
who will actually read it.</p>"""),

        ("What the consulate does with it", """
<p>Very little, usually. The reservation is a completeness check: does this applicant have a coherent itinerary that
matches the dates and the accommodation they have declared?</p>
<p>Where it stops being a formality is when something else in the file has already raised a question. A first-time
traveller, a thin bank statement, a sponsor with an unclear relationship. In those files a reviewer may look
harder, and a reservation that cannot be verified turns a soft doubt into a documented finding.</p>
<p>This is the entire argument for a real booking over a generated PDF. Not that anyone checks routinely. That the
files where somebody does check are exactly the files that could not afford it.</p>"""),

        ("Consulate-by-consulate quirks worth knowing", """
<p>The Schengen rules are common, but the centres implementing them are not identical:</p>
<ul>
  <li><strong>France and Germany</strong> tend to be strict on date consistency across the form, insurance and
  reservation. Reconcile all three before you go.</li>
  <li><strong>Italy and Spain</strong> more often ask for the accommodation booking to cover every night of the stay,
  not just the first.</li>
  <li><strong>The Netherlands</strong> asks for the reservation to show the applicant's name as printed in the
  passport, which catches people whose given names are abbreviated.</li>
  <li><strong>Switzerland</strong> is among the more likely to ask a follow-up question about an itinerary that does
  not match the stated purpose of travel.</li>
</ul>
<p>None of these are secrets. They are all on the respective checklists. They are simply on page four, where nobody
reads.</p>"""),
    ],
    faqs=[
        ("Do I need a flight reservation to book the VFS appointment slot?",
         "<p>In almost all cases no. Booking a slot needs your passport details and an intended travel window. The flight reservation belongs in the document folder you bring on the day.</p>"),
        ("Can I buy a real ticket instead?",
         "<p>You can, and it is never rejected. It is simply an expensive way to satisfy a requirement that a reservation satisfies, and the money is at risk if the visa is refused.</p>"),
        ("What if my reservation expires before the appointment?",
         "<p>Order a fresh one. That is why we suggest ordering three to five days out. A lapsed PNR that will not verify is worse than no reservation, because it looks like a document that was once real and is not any more.</p>"),
        ("Does the reservation have to be return?",
         "<p>For a Schengen visitor visa, yes. The checklist asks for round-trip transport, and a one-way itinerary invites the question of how you intend to leave.</p>"),
        ("Do the flight and hotel dates have to match exactly?",
         "<p>They have to be coherent. Arriving on the 4th with a hotel booked from the 6th is the kind of gap that gets a file queried. Book them together and the dates are reconciled for you.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="do-embassies-call-the-airline",
    cat="Legality",
    title="Will the Embassy Actually Call the Airline to Check Your Booking?",
    meta_title="Do Embassies Verify Flight Bookings by Calling the Airline?",
    desc="What consulate verification of a flight reservation really looks like, who does it, how often, and why the answer to how often is the wrong question to be asking.",
    read=7,
    lede="This is the question everyone actually wants answered before they order anything, and the honest "
         "answer has two halves. Routine phone calls to airlines are rare. And that fact should not change "
         "your decision at all. Here is why.",
    sections=[
        ("What verification actually looks like", """
<p>Nobody picks up a phone. The mental image of a consular officer calling an airline switchboard is not how any of
this works.</p>
<p>What exists instead:</p>
<ul>
  <li><strong>The airline's own site.</strong> Every major carrier has a manage-booking page that takes a PNR and a
  surname. It is public, instant, and anyone can use it, including you.</li>
  <li><strong>GDS lookup.</strong> Consulates with travel-sector relationships, and airlines at check-in, can query
  Amadeus, Sabre or Travelport directly. A reservation either exists in the system or it does not.</li>
  <li><strong>The eyeball test.</strong> Far more common than either. A reviewer who has read ten thousand
  itineraries recognises a template that does not match how the airline in question formats its documents.</li>
</ul>
<p>That third one is the real filter, and it is the one people underestimate. You do not need to be checked to be
caught. You need to be looked at.</p>"""),

        ("How often it happens", """
<p>Honestly: not often, as a proportion of applications. Most files are complete, unremarkable and processed without
anyone testing a single document.</p>
<p>But the rate is not uniform, and treating it as an average is the mistake. Verification concentrates on:</p>
<ul>
  <li>First-time applicants with no travel history</li>
  <li>Applications from countries with elevated refusal or overstay rates</li>
  <li>Files where something else already looks inconsistent</li>
  <li>Anything where the itinerary does not match the stated purpose of travel</li>
  <li>Airlines or routes a particular consulate has seen forged before</li>
</ul>
<p>If you are in one of those groups, and most first-time applicants are, your personal probability is nothing like
the headline average.</p>"""),

        ("Why the frequency is the wrong question", """
<p>People ask &ldquo;how likely is it that they check?&rdquo; because they are trying to work out whether they can get
away with something. That framing hides the actual asymmetry.</p>
<div class="tbl-wrap">
<table>
  <thead><tr><th></th><th>Real reservation</th><th>Generated PDF</th></tr></thead>
  <tbody>
    <tr><td>Nobody checks</td><td>Visa proceeds</td><td>Visa proceeds</td></tr>
    <tr><td>Somebody checks</td><td>Visa proceeds</td><td>Deception finding</td></tr>
    <tr><td>Cost to you</td><td>{PRICE}</td><td>Usually similar</td></tr>
  </tbody>
</table>
</div>
<p>The upside is identical. The downside is not remotely. And the price difference between the two, in this market,
is almost nothing, because a held reservation costs the provider very little to create.</p>
<p>You are not buying a better chance of approval. You are buying the removal of one specific way the application can
fail catastrophically.</p>"""),

        ("What a deception finding actually costs", """
<p>A refusal is a disappointment. A deception finding is a different category of problem, and it is worth being
precise about why.</p>
<ul>
  <li><strong>It follows you.</strong> UK immigration rules provide for a re-entry ban of up to ten years where
  deception is established. Other systems have equivalents.</li>
  <li><strong>It is disclosable.</strong> Visa forms for most countries ask whether you have ever been refused, and
  many ask specifically about false representations. Answering no is a second deception.</li>
  <li><strong>It is not appealable in the usual way.</strong> You are not arguing about the strength of your ties any
  more. You are arguing about your honesty, which is a much harder position.</li>
</ul>
<p>Against that, the difference in price between a real reservation and a fabricated one is roughly the cost of a
meal.</p>"""),

        ("Check it yourself before you submit", """
<p>The simplest way to know where you stand: verify your own PNR. It takes two minutes and requires no special access.</p>
<ol>
  <li>Go to the operating airline's website, not a booking site.</li>
  <li>Find &ldquo;Manage booking&rdquo;, &ldquo;My trips&rdquo; or equivalent.</li>
  <li>Enter the six-character booking reference and the surname exactly as printed.</li>
  <li>The itinerary should load, showing your flights.</li>
</ol>
<p>If it loads for you, it loads for anyone who tries. If it does not, you have learned that before a consulate did,
which is the entire point of doing it.</p>
<p>Any provider who cannot give you a reference that does this is not selling you a booking, whatever the PDF looks
like.</p>"""),
    ],
    faqs=[
        ("Has an embassy ever actually called an airline?",
         "<p>Yes, though it is far less common than online or GDS verification, which achieve the same thing in seconds. The method matters less than the fact that a real booking survives all of them.</p>"),
        ("Can the airline tell the reservation was never paid for?",
         "<p>Yes, and it is not a problem. Booked-but-unticketed is a completely normal state, and consulates ask for reservations precisely because they do not want you paying before a decision.</p>"),
        ("Will the airline cancel my reservation if the embassy looks at it?",
         "<p>No. A lookup is a read. What ends a reservation is the hold period expiring, which is why timing the order close to your appointment matters.</p>"),
        ("If checks are rare, why not use a cheap generated PDF?",
         "<p>Because the payoff is asymmetric. Identical outcome if nobody checks, and a deception finding that can follow you for a decade if somebody does, for a price difference of a few hundred rupees.</p>"),
        ("Do airlines report suspected fake bookings?",
         "<p>Airlines and consulates share information about document fraud patterns, and a carrier that repeatedly sees forged versions of its own itineraries has an obvious interest in flagging it.</p>"),
    ],
),

# ==========================================================================
dict(
    slug="dummy-ticket-vs-refundable-ticket",
    cat="Practical",
    title="Refundable Ticket or Flight Reservation? Running the Actual Numbers",
    meta_title="Dummy Ticket vs Refundable Ticket for a Visa: Cost Comparison",
    desc="Buying a refundable fare and cancelling it after the visa decision is legitimate but expensive. What it really costs once change fees, fare differences and refund delays are counted, against a held reservation.",
    read=8,
    lede="Buying a fully refundable ticket and cancelling it once the visa comes through is completely "
         "legitimate. It is also, for most people, the most expensive way to solve this problem. The gap is "
         "not the one most people assume, and it is not mainly about the fee.",
    sections=[
        ("The three options, honestly stated", """
<p>There are exactly three ways to put a credible itinerary in front of a consulate:</p>
<ol>
  <li><strong>Buy a normal ticket.</strong> Cheapest headline fare, zero flexibility. If the visa is refused you lose
  most or all of it.</li>
  <li><strong>Buy a refundable fare.</strong> Fully legitimate, fully verifiable, refundable on refusal. Refundable
  fares are a different, more expensive fare class.</li>
  <li><strong>Hold a reservation.</strong> A real booking with a live PNR that nobody has paid for. Verifiable the
  same way. Expires rather than needing cancellation.</li>
</ol>
<p>All three are legal. This article is only about which one costs least for the same result.</p>"""),

        ("What a refundable fare actually costs", """
<p>The sticker price is the smallest part of the story. On a typical Delhi to Europe route, a refundable economy fare
runs meaningfully above the cheapest non-refundable equivalent. Fare classes vary constantly, so treat the shape of
this rather than the specific numbers as the point:</p>
<div class="tbl-wrap">
<table>
  <thead><tr><th>Cost</th><th>Refundable fare</th><th>Held reservation</th></tr></thead>
  <tbody>
    <tr><td>Paid up front</td><td>Full fare, often a large multiple of the cheapest fare</td><td>{PRICE}</td></tr>
    <tr><td>Capital tied up</td><td>Weeks, sometimes months</td><td>None</td></tr>
    <tr><td>Refund processing</td><td>Commonly 30 to 90 days after cancellation</td><td>Not applicable</td></tr>
    <tr><td>Amount not returned</td><td>Cancellation and service fees, sometimes the difference between fare classes</td><td>Not applicable</td></tr>
    <tr><td>If you forget to cancel</td><td>You have bought a flight you are not taking</td><td>It simply lapses</td></tr>
  </tbody>
</table>
</div>
<p>The line that hurts most people is not the fee. It is the capital. Paying a full international fare and waiting
two months to get it back is a real cost even when every rupee eventually comes home, and it lands at exactly the
moment you are also paying visa fees, insurance and biometrics.</p>"""),

        ("When a refundable ticket is genuinely the better choice", """
<p>It is not always the wrong answer. Buy the refundable fare when:</p>
<ul>
  <li><strong>Your dates are fixed and the flight is filling up.</strong> A held reservation does not protect a seat
  beyond its hold period. If you need that specific flight, buy it.</li>
  <li><strong>You are applying for a long-stay or settlement visa</strong> where processing runs for months and no
  hold period will span it.</li>
  <li><strong>Your employer is paying</strong> and the capital cost is not yours.</li>
  <li><strong>You have been refused before on document grounds</strong> and want the file to be beyond any argument.</li>
</ul>
<p>Outside those cases, you are paying a significant premium for a document that is treated identically to one costing
a few hundred rupees.</p>"""),

        ("The trap in the middle: non-refundable bought early", """
<p>The genuinely bad option is the one most first-time applicants pick without thinking: buy the cheap
non-refundable fare, because it is cheap, and hope the visa comes through.</p>
<p>Schengen refusal rates for Indian applicants have run in the region of one in six in recent years, and vary a lot
by consulate. On those odds, buying a non-refundable international fare before a decision is a straightforwardly bad
bet, and it is the single most expensive mistake in this whole process.</p>
<div class="note">
  <strong>The rule that covers every case</strong>
  Do not pay for a flight you cannot use until you hold a decision that lets you use it. Every consulate that asks
  for a reservation rather than a ticket is telling you the same thing.
</div>"""),

        ("Side by side", """
<div class="tbl-wrap">
<table>
  <thead><tr><th></th><th>Non-refundable</th><th>Refundable</th><th>Held reservation</th></tr></thead>
  <tbody>
    <tr><td>Accepted by consulates</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
    <tr><td>Verifiable PNR</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
    <tr><td>Cost before decision</td><td>Full fare</td><td>Higher fare</td><td>{PRICE}</td></tr>
    <tr><td>Loss if refused</td><td>Most of the fare</td><td>Fees and delay</td><td>Nothing</td></tr>
    <tr><td>Seat guaranteed</td><td>Yes</td><td>Yes</td><td>No</td></tr>
    <tr><td>Admin after the decision</td><td>None</td><td>You must remember to cancel</td><td>None</td></tr>
  </tbody>
</table>
</div>
<p>One row favours the paid fares: the seat. If that row is the one that matters for your trip, buy the ticket. If it
is not, you are paying a large premium for a document the consulate treats the same way.</p>"""),

        ("The sequence that costs least", """
<ol>
  <li>Apply with a held reservation, and a hotel booking if the checklist asks for accommodation.</li>
  <li>Wait for the decision. Do not buy anything.</li>
  <li>Once approved, book the flight you actually want, at whatever fare is best on the day.</li>
</ol>
<p>Booking after approval usually beats the refundable fare even after any last-minute price rise, because you were
never holding a refundable fare class in the first place. And you are choosing from every flight available, not
locked to the one you guessed at weeks earlier.</p>"""),
    ],
    faqs=[
        ("Is buying a refundable ticket and cancelling it legal?",
         "<p>Entirely. You bought a ticket under its published terms and cancelled under those same terms. Nobody has been misled at any point.</p>"),
        ("How long do airline refunds actually take?",
         "<p>Commonly 30 to 90 days to reach the original payment method, depending on carrier and how you paid. Plan on the longer end.</p>"),
        ("Can I use a 24-hour free cancellation window instead?",
         "<p>Only if your appointment falls inside it, which is rarely how the timing works. Cancel before the window closes and the booking stops verifying; leave it and you have bought the ticket.</p>"),
        ("Does a consulate treat a paid ticket more favourably?",
         "<p>No. Checklists ask for evidence of intended transport. A reservation with a live PNR meets that, and several immigration authorities actively advise against buying before a decision.</p>"),
        ("What if my visa is approved and the flight is now more expensive?",
         "<p>Possible, and usually still cheaper than the refundable fare premium plus the money you had tied up for two months. If a specific flight genuinely matters, that is the case for buying it.</p>"),
        ("Can I get a reservation held for longer than the airline's window?",
         "<p>Not indefinitely. Hold periods are set by the carrier. For long processing times the practical answer is to reissue closer to the date, at half price, rather than hold something that will lapse.</p>"),
    ],
),

]


def _fill():
    """Prices and the delivery window live in build.py, so the tables above
    take them at import time. Hardcoding either would leave a number that goes
    stale the next time the price changes and nobody greps the blog."""
    subs = (("{PRICE}", money(PRICE_FLIGHT)),
            ("{BUNDLE}", money(PRICE_BOTH)),
            ("{DELIVERY}", DELIVERY))
    for p in POSTS_EXTRA:
        out = []
        for h, html in p["sections"]:
            for token, value in subs:
                html = html.replace(token, value)
            out.append((h, html))
        p["sections"] = out


_fill()
