# -*- coding: utf-8 -*-
"""
The next 18 destinations, taking the guide set to the 30 countries Indians
actually travel to most.

Every entry carries a `status` so the page and the index can say plainly
whether an Indian passport needs a visa at all:

    visa_free      walk up to immigration, nothing to apply for
    voa            visa issued on arrival
    evisa          apply online before you fly
    visa_required  full application, appointment, the works

Visa policy moves. Several entries below are explicitly time-limited
(Malaysia's waiver, for one), so each page links the issuing authority and
carries a checked-on date rather than pretending the position is permanent.
"""

from build import DELIVERY, PRICE_FLIGHT, PRICE_BOTH, money, url

EXTRA = [
# ============================================================ Southeast Asia
dict(
    slug="malaysia-visa-for-indians",
    official_src=('Immigration Department of Malaysia', 'https://www.imi.gov.my/'),
    label="Malaysia", short="Malaysia",
    status="visa_free", status_note="30 days, waiver currently runs to December 2026",
    h1="Malaysia for Indian passport holders",
    title="Malaysia Visa Free for Indians 2026 | Rules, MDAC, Onward Ticket",
    desc="Malaysia is visa free for Indians for 30 days. What you still need: the MDAC arrival card, proof of onward travel and accommodation. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "KUL"),
    blurb="Malaysia waived visas for Indian passport holders and has kept extending it. Thirty days, no "
          "application, no fee. What has not gone away is the paperwork at the airport: the digital arrival "
          "card, an onward ticket and somewhere to stay.",
    requirements=[
        "<strong>MDAC (Malaysia Digital Arrival Card)</strong> submitted within three days before you land. Free, online, and genuinely mandatory.",
        "<strong>Onward or return ticket</strong> within 30 days. Checked at the gate in India as often as at Malaysian immigration.",
        "<strong>Accommodation details</strong> for the arrival card and for the officer.",
        "Passport valid at least <strong>six months</strong> with blank pages.",
    ],
    official="Immigration Department of Malaysia operates the visa waiver for Indian nationals and the MDAC requirement.",
    traps=[
        ("Skipping the MDAC", "Visa free does not mean form free. No MDAC and you are filling it in on airport wifi with a queue behind you."),
        ("Assuming the waiver is permanent", "It has been extended repeatedly, never made permanent. Check the date before you book."),
        ("Flying in one way", "The waiver does not remove the onward-travel requirement, and airline staff enforce it in India."),
    ],
    steps=[
        ("Check the waiver still covers your travel dates", "It runs to December 2026 as things stand. Extensions have come late each time."),
        ("Submit the MDAC", "Within three days before arrival, on the official Immigration Department site. It is free."),
        ("Sort onward travel", "A dated ticket out within 30 days. This is the one people get stopped for."),
        ("Book somewhere to stay", "The arrival card asks for the address."),
        ("Carry proof of funds", "Rarely asked for, occasionally decisive at the counter."),
    ],
    fees=[("Visa", "Free", "No visa needed for stays up to 30 days"),
          ("MDAC arrival card", "Free", "Official site only. Look-alike sites charge for it"),
          ("Overstay penalty", "From RM 100 per day", "Plus possible blacklisting")],
    tips=[
        "Grab and Touch 'n Go cover almost everything. Set up Touch 'n Go eWallet before you land, it works for trains, tolls and half the hawker stalls.",
        "KLIA to KL Sentral on the KLIA Ekspres is 28 minutes; the bus is a third of the price and takes an hour. Neither needs booking ahead.",
        "Langkawi is duty free, which is why chocolate and alcohol are startlingly cheap there and nowhere else in Malaysia.",
        "Vegetarian food is easy in KL and Penang: look for the word 'banana leaf' and any Indian-Muslim mamak stall, most of which run 24 hours.",
    ],
    faqs=[
        ("Do Indians need a visa for Malaysia?", "<p>No, not for stays up to 30 days under the current waiver, which runs to December 2026. You do still need to submit the free MDAC arrival card before you land.</p>"),
        ("Do I need a return ticket for Malaysia?", "<p>Yes. The visa waiver does not remove the onward-travel requirement, and airline staff in India check it before boarding.</p>"),
        ("What is the MDAC and is it really required?", "<p>The Malaysia Digital Arrival Card, submitted within three days before arrival. It is free, it takes two minutes, and immigration does ask for it.</p>"),
    ]),

dict(
    slug="indonesia-bali-visa-for-indians",
    official_src=('Indonesian Directorate General of Immigration', 'https://evisa.imigrasi.go.id/'),
    label="Indonesia / Bali", short="Indonesia",
    status="voa", status_note="Visa on arrival, 30 days, extendable once",
    h1="Bali and Indonesia visa on arrival for Indians",
    title="Bali Visa on Arrival for Indians 2026 | Cost and e-VOA",
    desc="Indians get a 30-day visa on arrival for Indonesia at IDR 500,000, extendable once. Onward ticket required. Verifiable reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "DPS"),
    blurb="Indonesia gives Indian passport holders a visa on arrival, and you can now buy it online beforehand "
          "as an e-VOA to skip one queue. Thirty days, extendable once by another thirty.",
    requirements=[
        "<strong>Visa on arrival fee</strong>, payable at the airport or online in advance as an e-VOA.",
        "<strong>Onward or return ticket</strong> within 30 days. Enforced at check-in.",
        "Passport valid <strong>six months</strong> from arrival with two blank pages.",
        "<strong>All Indonesia Customs Declaration</strong>, submitted online in the two days before arrival.",
    ],
    official="Indonesian Directorate General of Immigration issues the visa on arrival and the e-VOA.",
    traps=[
        ("Landing without an onward ticket", "The most common reason Indians are stopped at Denpasar. Immigration does check."),
        ("Passport under six months", "Refused at check-in in India, before Indonesia is involved."),
        ("Assuming you can extend twice", "One extension, thirty more days. After that you leave or you pay daily."),
    ],
    steps=[
        ("Buy the e-VOA online, or pay on arrival", "Online is the same price and saves a queue at a busy airport."),
        ("File the customs declaration", "Online, within two days before you land. You get a QR code to show."),
        ("Have your onward ticket ready", "Within 30 days of arrival."),
        ("Clear immigration", "e-VOA holders use the automatic gates at Denpasar and Jakarta."),
        ("Extend once if you need to", "Online or at an immigration office, before the first 30 days run out."),
    ],
    fees=[("Visa on arrival / e-VOA", "IDR 500,000", "Roughly Rs2,700. Same price either way"),
          ("Extension", "IDR 500,000", "One extension of 30 days"),
          ("Overstay", "IDR 1,000,000 per day", "Charged per day, no discretion")],
    tips=[
        "Bali is bigger than it looks and the traffic is worse than it looks. Canggu to Ubud is 25km and can take two hours. Do not plan two areas in one day.",
        "Withdraw from bank ATMs inside branches. Standalone machines in tourist strips have the worst rates and the most skimmers.",
        "Nyepi, the day of silence, shuts the entire island including the airport for 24 hours. Check the date before booking March travel.",
        "Book a car with a driver for full days rather than per trip. It works out cheaper than three Grabs and the driver waits while you eat.",
    ],
    faqs=[
        ("Do Indians need a visa for Bali?", "<p>You need a visa on arrival, which is issued to Indian passport holders at the airport for IDR 500,000, or bought online in advance as an e-VOA at the same price. Thirty days, extendable once.</p>"),
        ("Is a return ticket required for Indonesia?", "<p>Yes, and it is the single most common reason Indian travellers are pulled aside at Denpasar. Carry a dated onward booking within 30 days.</p>"),
        ("Can I extend my Bali visa?", "<p>Once, for another 30 days, applied for before the first 30 expire. After that you must leave.</p>"),
    ]),

dict(
    slug="vietnam-evisa-for-indians",
    official_src=('Vietnam Immigration Department', 'https://evisa.gov.vn/'),
    label="Vietnam", short="Vietnam",
    status="evisa", status_note="e-visa, 90 days, single or multiple entry",
    h1="Vietnam e-visa for Indian passport holders",
    title="Vietnam e-Visa for Indians 2026 | Cost and Documents",
    desc="Vietnam's e-visa gives Indians up to 90 days, single or multiple entry, for USD 25 to 50. Applied for online in about three working days. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "SGN"),
    blurb="Vietnam runs one of the easier e-visa systems in the region. Ninety days, single or multiple entry, "
          "applied for entirely online, usually decided in about three working days.",
    requirements=[
        "<strong>Passport scan</strong> of the data page and a <strong>passport photo</strong> on a white background.",
        "<strong>Entry and exit points</strong> declared on the form. You must enter through the one you named.",
        "Passport valid <strong>six months</strong> from entry.",
        "Accommodation address for the first night.",
    ],
    official="Vietnam Immigration Department issues the e-visa through the official government portal.",
    traps=[
        ("Applying on a copycat site", "Search results are full of agents charging four times the government fee for the same form."),
        ("Naming the wrong entry point", "You have to arrive through the port you declared. Changing it means a new application."),
        ("Photo rejected", "Plain white background, no glasses, no smile. This is the usual reason for a rejection."),
    ],
    steps=[
        ("Apply on the official portal", "evisa.gov.vn. Everything else is a reseller."),
        ("Upload the photo and passport page", "White background, no filters, the whole data page in one frame."),
        ("Declare your entry and exit points", "Get this right, you are held to it."),
        ("Pay the fee", "Non-refundable, even if the application is refused."),
        ("Wait about three working days", "Then download and print the e-visa. Carry it on paper."),
    ],
    fees=[("e-visa, single entry", "USD 25", "About Rs2,200"),
          ("e-visa, multiple entry", "USD 50", "Up to 90 days"),
          ("Agent markup", "USD 20 to 80", "Avoidable. Use the official site")],
    tips=[
        "Grab is everywhere and much cheaper than a taxi from the airport. Book from inside the terminal, not from the touts outside.",
        "Vietnamese notes have a lot of zeroes and 500,000 looks a lot like 20,000. Sort your wallet by colour on day one.",
        "The north and south have opposite seasons. Hanoi in January is cold and grey; Saigon is dry and hot. Do not pack for one and visit both.",
        "Book the Reunification Express sleeper a week ahead in peak season. Soft sleeper, four berths, and far more pleasant than the internal flight.",
    ],
    faqs=[
        ("How long does the Vietnam e-visa take?", "<p>About three working days for most applications. Allow a week in peak season, and apply at least two weeks before you fly.</p>"),
        ("How much is the Vietnam e-visa for Indians?", "<p>USD 25 single entry, USD 50 multiple entry, paid to the government portal. Agent sites charge substantially more for the identical application.</p>"),
        ("Do I need a return ticket for Vietnam?", "<p>Airline staff check it at the gate, and immigration can ask. Carry a dated onward booking within your 90 days.</p>"),
    ]),

dict(
    slug="philippines-visa-for-indians",
    official_src=('Philippine Bureau of Immigration', 'https://immigration.gov.ph/'),
    label="Philippines", short="Philippines",
    status="evisa", status_note="e-visa, or visa free for 14 days with a valid US, UK, Schengen, Japan, Australia or Canada visa",
    h1="Philippines visa for Indian passport holders",
    title="Philippines Visa for Indians 2026 | e-Visa, 14-Day Visa Free Rule",
    desc="Indians can enter the Philippines visa free for 14 days holding a valid US, UK, Schengen, Japan, Australian or Canadian visa, or apply for an e-visa. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "MNL"),
    blurb="The Philippines has a rule worth knowing: if you already hold a valid visa for the US, UK, Schengen, "
          "Japan, Australia or Canada, you can enter visa free for 14 days. Everyone else applies for an e-visa.",
    requirements=[
        "Either a valid <strong>US, UK, Schengen, Japanese, Australian or Canadian visa</strong> for the 14-day waiver, or an approved e-visa.",
        "<strong>Return or onward ticket</strong>, checked strictly.",
        "Passport valid <strong>six months</strong> beyond your stay.",
        "<strong>eTravel registration</strong> submitted within 72 hours before arrival.",
    ],
    official="Philippine Bureau of Immigration operates the visa waiver and the eTravel system.",
    traps=[
        ("Assuming the waiver covers a longer trip", "Fourteen days, not thirty. Extensions must be applied for locally."),
        ("An expired third-country visa", "The US or Schengen visa must be valid on the day you arrive, not merely issued at some point."),
        ("Missing eTravel", "Separate from the visa and mandatory for everyone."),
    ],
    steps=[
        ("Check whether the 14-day waiver applies to you", "Valid US, UK, Schengen, Japan, Australia or Canada visa in the passport."),
        ("If not, apply for the e-visa", "Through the official Bureau of Immigration channel or your nearest consulate."),
        ("Register on eTravel", "Within 72 hours before arrival. Free."),
        ("Have onward travel ready", "Within your permitted stay. Enforced firmly here."),
        ("Extend locally if you need longer", "At a Bureau of Immigration office, straightforward but not free."),
    ],
    fees=[("e-visa", "About USD 30 to 40", "Varies by consulate"),
          ("14-day waiver", "Free", "With a qualifying third-country visa"),
          ("eTravel", "Free", "Mandatory for everyone")],
    tips=[
        "Domestic flights are how you get between islands and they are cheap, but the baggage allowance is small and strictly weighed. Pay for extra kilos online, not at the counter.",
        "Typhoon season runs June to November and mostly hits the east. It rarely cancels a holiday, but it does move ferries.",
        "Carry cash outside Manila and Cebu. Card acceptance drops off fast once you leave the cities.",
        "Book a hotel near the airport terminal you are flying out of. Manila's terminals are far apart and the traffic between them is genuinely punishing.",
    ],
    faqs=[
        ("Can Indians enter the Philippines without a visa?", "<p>Yes, for 14 days, if you hold a valid visa for the US, UK, Schengen area, Japan, Australia or Canada. It must be valid on the day you arrive. Otherwise you need an e-visa.</p>"),
        ("What is eTravel?", "<p>A free arrival registration everyone must complete within 72 hours before landing. It is separate from your visa.</p>"),
        ("Is a return ticket required?", "<p>Yes, and the Philippines enforces it firmly. Airlines are fined for boarding passengers without one.</p>"),
    ]),

dict(
    slug="cambodia-visa-for-indians",
    official_src=('Cambodia Ministry of Foreign Affairs', 'https://www.evisa.gov.kh/'),
    label="Cambodia", short="Cambodia",
    status="evisa", status_note="e-visa or visa on arrival, 30 days",
    h1="Cambodia visa for Indian passport holders",
    title="Cambodia Visa for Indians 2026 | e-Visa Cost, Visa on Arrival",
    desc="Cambodia gives Indians a 30-day tourist visa on arrival or online for about USD 36. Simple, quick, and onward travel is checked. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "REP"),
    blurb="Cambodia is one of the simpler ones. A 30-day tourist visa, available on arrival at the airport or "
          "online three days ahead, and nobody makes it complicated.",
    requirements=[
        "<strong>Passport photo</strong> for the on-arrival counter, or uploaded for the e-visa.",
        "Passport valid <strong>six months</strong> with a blank page.",
        "<strong>Onward ticket</strong> within 30 days.",
        "Cash in USD for the on-arrival fee. Cambodia runs on dollars.",
    ],
    official="Ministry of Foreign Affairs of Cambodia issues the tourist e-visa.",
    traps=[
        ("Using a look-alike e-visa site", "Several charge triple. The official domain ends in gov.kh."),
        ("Arriving without USD cash", "The visa-on-arrival counter wants dollars and gives poor change."),
        ("Overstaying by a few days", "Ten dollars a day, collected at the airport, in cash."),
    ],
    steps=[
        ("Decide between e-visa and on arrival", "The e-visa saves a queue at Siem Reap and Phnom Penh."),
        ("Apply at evisa.gov.kh if online", "Three working days is typical."),
        ("Bring a passport photo and USD cash if on arrival", "Both, or you will be sent to a side desk."),
        ("Have onward travel ready", "Within 30 days."),
        ("Keep the departure card", "You hand it back on the way out."),
    ],
    fees=[("Tourist e-visa", "USD 36", "Includes a USD 6 processing fee"),
          ("Visa on arrival", "USD 30", "Plus a photo, cash only"),
          ("Overstay", "USD 10 per day", "Collected at departure")],
    tips=[
        "Angkor tickets are sold only at the official ticket centre, not at the temples. Buy after 5pm and the ticket is valid from the next day, with that evening's sunset thrown in free.",
        "US dollars are the working currency. Riel appears only as change under a dollar. Bring clean, untorn notes, damaged ones get refused.",
        "Tuk-tuk drivers will offer a full-day Angkor circuit for about USD 20. That is the going rate and worth it over hiring per trip.",
        "Siem Reap to Phnom Penh is six hours by road. The flight is 45 minutes and often costs less than the bus if booked ahead.",
    ],
    faqs=[
        ("How much is a Cambodia visa for Indians?", "<p>USD 36 for the tourist e-visa including processing, or USD 30 in cash at the airport plus a passport photo. Thirty days either way.</p>"),
        ("Is Cambodia visa free for Indians?", "<p>No. You need a visa, but it is one of the easiest to get, either online in three days or on arrival at the airport.</p>"),
        ("Which is better, e-visa or visa on arrival?", "<p>The e-visa if you want to skip a queue and have three days to spare. On arrival if you are deciding late.</p>"),
    ]),

# ==================================================================== South Asia
dict(
    slug="sri-lanka-visa-for-indians",
    official_src=('Sri Lanka Department of Immigration', 'https://www.eta.gov.lk/'),
    label="Sri Lanka", short="Sri Lanka",
    status="visa_free", status_note="Visa free for 30 days, free ETA registration still required",
    h1="Sri Lanka for Indian passport holders",
    title="Sri Lanka Visa Free for Indians 2026 | ETA, Rules, Return Ticket",
    desc="Sri Lanka is visa free for Indians for 30 days, with a free ETA registration before travel. Onward ticket and funds checked. Reservations from %s." % money(PRICE_FLIGHT),
    route=("MAA", "CMB"),
    blurb="Sri Lanka scrapped visa fees for Indian visitors and kept the free ETA registration. Thirty days, "
          "nothing to pay, but you do still have to register before you fly.",
    requirements=[
        "<strong>Free ETA</strong> obtained online before travel. Free does not mean optional.",
        "<strong>Return or onward ticket</strong> within 30 days.",
        "Passport valid <strong>six months</strong> from arrival.",
        "Proof of sufficient funds, occasionally requested.",
    ],
    official="Sri Lanka Department of Immigration and Emigration operates the free ETA scheme for Indian nationals.",
    traps=[
        ("Paying for the ETA", "It is free for Indians. Agent sites charge anyway and many travellers pay without checking."),
        ("Arriving without the ETA", "Registration is still required even though the fee is waived."),
        ("Assuming the waiver is permanent", "It has been extended in blocks. Check before you book."),
    ],
    steps=[
        ("Apply for the free ETA online", "On the official Department of Immigration site. It costs nothing."),
        ("Print the approval", "Or save it offline. Colombo airport wifi is not something to rely on."),
        ("Have your return ticket", "Within 30 days."),
        ("Carry some funds evidence", "Card statements are enough when asked."),
        ("Keep the ETA with your passport", "You may be asked again on departure."),
    ],
    fees=[("Visa", "Free", "Fee waived for Indian nationals"),
          ("ETA registration", "Free", "Official site only"),
          ("Extension", "About USD 100", "Applied for in Colombo")],
    tips=[
        "The Kandy to Ella train is the point of going, not a way to get somewhere. Book reserved second class about a month ahead and sit on the right leaving Kandy.",
        "Tuk-tuks in Colombo have meters and drivers will avoid using them. PickMe is the local app and settles the argument.",
        "The island has two monsoons on opposite coasts. When the west is washed out the east is perfect, so a bad forecast rarely means a bad trip.",
        "Take off shoes and hats at temples and cover your shoulders. Photographs with your back to a Buddha statue genuinely cause offence and have led to arrests.",
    ],
    faqs=[
        ("Is Sri Lanka visa free for Indians?", "<p>Yes, for stays up to 30 days. You still need to register for the free ETA online before you travel.</p>"),
        ("Do I have to pay for the Sri Lanka ETA?", "<p>No. It is free for Indian passport holders on the official site. Third-party sites charge a fee for the same free registration.</p>"),
        ("Do I need a return ticket?", "<p>Yes, within your 30 days. It is checked at the gate in India.</p>"),
    ]),

dict(
    slug="maldives-visa-for-indians",
    official_src=('Maldives Immigration', 'https://imuga.immigration.gov.mv/'),
    label="Maldives", short="Maldives",
    status="visa_free", status_note="Free visa on arrival, 30 days",
    h1="Maldives for Indian passport holders",
    title="Maldives Visa for Indians 2026 | Free 30-Day Visa on Arrival",
    desc="The Maldives issues Indians a free 30-day visa on arrival. You need confirmed accommodation, an onward ticket and Traveller Declaration. Reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "MLE"),
    blurb="The Maldives gives every arriving tourist a free 30-day visa on arrival, Indians included. There is "
          "nothing to apply for. What they do check is where you are staying and how you are leaving.",
    requirements=[
        "<strong>Confirmed accommodation</strong> for your whole stay. Checked properly here, not glanced at.",
        "<strong>Onward or return ticket</strong> within 30 days.",
        "<strong>Traveller Declaration</strong> submitted within 96 hours before arrival and again before departure.",
        "Passport valid <strong>one month</strong> beyond your stay, and sufficient funds.",
    ],
    official="Maldives Immigration issues the free visa on arrival and operates the IMUGA Traveller Declaration.",
    traps=[
        ("No confirmed hotel booking", "Maldives immigration is stricter about this than most. A resort or guesthouse booking for the full stay."),
        ("Forgetting the Traveller Declaration", "Needed both ways, within 96 hours of each journey."),
        ("Assuming resort transfers are included", "A seaplane transfer can cost more than the flight from India. Check before booking."),
    ],
    steps=[
        ("Book accommodation for every night", "Immigration will ask, and a booking for part of the stay causes trouble."),
        ("Submit the Traveller Declaration", "Within 96 hours before you fly, on IMUGA."),
        ("Have your return ticket", "Within 30 days."),
        ("Arrive and collect the free visa", "Stamped at the counter, no fee."),
        ("Submit the declaration again before leaving", "People forget this half."),
    ],
    fees=[("Visa on arrival", "Free", "30 days, all nationalities"),
          ("Traveller Declaration", "Free", "Required in both directions"),
          ("Green tax", "USD 6 to 12 per night", "Usually billed by the resort")],
    tips=[
        "Local islands cost a fraction of resort islands and are reached by public ferry for a few dollars. Ferries do not run on Fridays.",
        "Alcohol is not available on local islands, only on resorts and liveaboards. Bringing it in is confiscation at the airport, no exceptions.",
        "Book the seaplane transfer through the resort, not separately. Seaplanes only fly in daylight, so a late arrival into Male means an unplanned airport hotel.",
        "Bikinis are fine on resort islands and on marked bikini beaches only. On local islands, cover shoulders and knees away from those beaches.",
    ],
    faqs=[
        ("Do Indians need a visa for the Maldives?", "<p>No. A free 30-day visa is issued on arrival to all visitors including Indian passport holders. You need confirmed accommodation and an onward ticket.</p>"),
        ("What is the Traveller Declaration?", "<p>A free online form, submitted within 96 hours before arrival and again before departure. It is mandatory both ways.</p>"),
        ("Do I need a hotel booking?", "<p>Yes, for the whole stay, and Maldives immigration checks it more carefully than most places do.</p>"),
    ]),

dict(
    slug="nepal-visa-for-indians",
    official_src=('Nepal Department of Immigration', 'https://www.immigration.gov.np/'),
    label="Nepal", short="Nepal",
    status="visa_free", status_note="No visa, no passport needed. Voter ID or Aadhaar works",
    h1="Nepal for Indian passport holders",
    title="Nepal Travel for Indians 2026 | No Visa, ID Rules, What to Carry",
    desc="Indians need no visa for Nepal and can enter on a voter ID or Aadhaar. What to carry, what changes if you fly, and the rules that catch people out.",
    route=("DEL", "KTM"),
    blurb="Nepal is the easiest border an Indian passport opens, and you do not even need the passport. Indians "
          "travel visa free with no time limit, on nothing more than photo ID.",
    requirements=[
        "<strong>Photo ID</strong>: voter ID card, or a passport. Aadhaar is accepted at land borders but a passport is safer by air.",
        "No visa, <strong>no time limit</strong>, and no fee.",
        "For minors, a birth certificate or school ID with a parent.",
        "Indian rupee notes above Rs100 are <strong>not legal tender</strong> in Nepal.",
    ],
    official="Nepal Department of Immigration exempts Indian nationals from visa requirements under the bilateral treaty.",
    traps=[
        ("Carrying only Rs500 and Rs2000 notes", "Notes above Rs100 cannot legally be used or exchanged in Nepal. Carry small denominations or cards."),
        ("Flying with only Aadhaar", "Fine at a land border, unreliable at the airport. Take a passport or voter ID if you are flying."),
        ("Assuming trekking needs nothing", "Most treks need a TIMS card and a national park permit, bought in Kathmandu or Pokhara."),
    ],
    steps=[
        ("Carry acceptable photo ID", "Passport or voter ID. Aadhaar for land crossings."),
        ("Change money sensibly", "Small Indian notes, or withdraw Nepali rupees on arrival."),
        ("Buy trekking permits in the city", "TIMS and park permits, before you reach the trailhead."),
        ("Register with your insurer if trekking high", "Helicopter evacuation is the one genuinely expensive risk here."),
        ("Keep ID on you", "Checkpoints on trekking routes ask for it."),
    ],
    fees=[("Visa", "Free", "Indians are visa exempt without time limit"),
          ("TIMS trekking card", "About NPR 2,000", "Required for most trekking routes"),
          ("National park permit", "NPR 3,000", "Per park, per entry")],
    tips=[
        "Fly to Kathmandu on the left side of the aircraft coming from Delhi for the Himalayan range. On the way back, sit right.",
        "Load-shedding has largely gone but water is still rationed in Kathmandu. Hotels store it, so a shower at 6am is more reliable than at 9pm.",
        "Domestic flights to Lukla and Pokhara are weather dependent and cancel routinely. Build two spare days into any trek, not one.",
        "Altitude sickness does not care how fit you are. Above 3,000m, climb no more than 500m of sleeping altitude per day and take the rest day.",
    ],
    faqs=[
        ("Do Indians need a visa for Nepal?", "<p>No. Indian nationals travel to Nepal visa free with no time limit, under the bilateral treaty. You do not even need a passport for land crossings.</p>"),
        ("What ID do Indians need for Nepal?", "<p>A passport or voter ID card. Aadhaar is accepted at land borders but is unreliable if you are flying, so carry a passport or voter ID for air travel.</p>"),
        ("Can I use Indian rupees in Nepal?", "<p>Notes of Rs100 and below only. Rs500 and Rs2000 notes are not legal tender in Nepal and cannot be exchanged.</p>"),
    ]),

dict(
    slug="bhutan-permit-for-indians",
    official_src=('Department of Immigration, Bhutan', 'https://www.immi.gov.bt/'),
    label="Bhutan", short="Bhutan",
    status="visa_free", status_note="No visa, but a permit and a daily levy apply",
    h1="Bhutan permit for Indian passport holders",
    title="Bhutan for Indians 2026 | Permit, SDF Daily Fee, Entry Rules",
    desc="Indians need no visa for Bhutan but do need an entry permit and pay a daily Sustainable Development Fee of Rs1,200. How the permit works and what it costs.",
    route=("DEL", "PBH"),
    blurb="Bhutan is visa free for Indians but not fee free. You need an entry permit, and you pay a daily "
          "Sustainable Development Fee for every night you stay. Indians pay a fraction of what everyone else does.",
    requirements=[
        "<strong>Entry permit</strong>, applied for online before travel or at Phuentsholing by land.",
        "<strong>Passport or voter ID</strong>. Aadhaar is not accepted.",
        "<strong>Sustainable Development Fee</strong> of Rs1,200 per adult per night.",
        "Hotel bookings in <strong>government-registered</strong> properties only.",
    ],
    official="Department of Immigration, Royal Government of Bhutan issues permits and collects the SDF.",
    traps=[
        ("Turning up with Aadhaar", "Not accepted for Bhutan. Passport or voter ID only."),
        ("Budgeting for the flight but not the SDF", "Rs1,200 per person per night adds up faster than the hotel does."),
        ("Booking an unregistered hotel", "Permits are issued against registered properties. An unregistered booking will not support one."),
    ],
    steps=[
        ("Apply for the entry permit online", "Through the official immigration portal, before you travel."),
        ("Book registered accommodation", "The permit is tied to it."),
        ("Pay the SDF", "Rs1,200 per adult per night, half for children 6 to 12, nothing under 6."),
        ("Carry passport or voter ID", "Aadhaar will not get you in."),
        ("Get a separate permit to go beyond Thimphu and Paro", "Arranged in Thimphu, takes a morning."),
    ],
    fees=[("Visa", "Free", "Indians are visa exempt"),
          ("Sustainable Development Fee", "Rs1,200 per night", "Per adult. Rs600 for children 6 to 12"),
          ("Entry permit", "Free", "But required, and tied to registered hotels")],
    tips=[
        "Fly in on the left for Everest and Kanchenjunga. Paro's approach is famously steep and only a handful of pilots are certified for it, which is why flights only operate in daylight.",
        "The Tiger's Nest hike is three hours up and genuinely steep. Start at 7am, before the tour groups and the heat.",
        "Indian rupees are accepted everywhere at par with the ngultrum, but again, Rs100 notes and below.",
        "There is no smoking anywhere in public and tobacco import is heavily restricted. Do not bring cartons as gifts.",
    ],
    faqs=[
        ("Do Indians need a visa for Bhutan?", "<p>No visa, but you do need an entry permit and you pay a Sustainable Development Fee of Rs1,200 per adult per night.</p>"),
        ("Is Aadhaar accepted for Bhutan?", "<p>No. Indian travellers need a passport or a voter ID card. Aadhaar is not accepted for entry.</p>"),
        ("How much does Bhutan cost per day?", "<p>The SDF alone is Rs1,200 per adult per night, before accommodation, food and transport. Budget accordingly.</p>"),
    ]),

# ======================================================================== Gulf
dict(
    slug="qatar-visa-for-indians",
    official_src=('Qatar Ministry of Interior', 'https://portal.moi.gov.qa/'),
    label="Qatar", short="Qatar",
    status="voa", status_note="Free visa on arrival, 30 days, conditions apply",
    h1="Qatar visa on arrival for Indian passport holders",
    title="Qatar Visa for Indians 2026 | Free Visa on Arrival, Conditions",
    desc="Indians get a free 30-day visa on arrival in Qatar with a confirmed hotel booking and return ticket, or holding a valid US, UK or Schengen visa. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "DOH"),
    blurb="Qatar gives Indian passport holders a free visa on arrival, but it comes with conditions that are "
          "actually checked: a confirmed hotel booking, a return ticket, and either sufficient funds or a "
          "valid US, UK or Schengen visa.",
    requirements=[
        "<strong>Confirmed hotel booking</strong> or a valid US, UK or Schengen visa or residence permit.",
        "<strong>Return ticket</strong> within 30 days.",
        "Passport valid <strong>six months</strong>.",
        "Funds of about <strong>QAR 5,000</strong> or an international card, occasionally verified.",
    ],
    official="Qatar Ministry of Interior operates the visa waiver for Indian nationals.",
    traps=[
        ("Arriving without a hotel booking", "This is the condition people get caught by. Staying with friends still means you need a booking or a qualifying visa."),
        ("A hotel booking that does not cover the stay", "It should cover the nights you have declared."),
        ("Assuming a transit stop counts", "Hamad transit is separate from entering the country."),
    ],
    steps=[
        ("Check which route you qualify under", "Hotel booking, or a valid US, UK or Schengen visa."),
        ("Book a confirmed hotel for the stay", "The condition most commonly missed."),
        ("Have a return ticket within 30 days", "Checked at the gate and on arrival."),
        ("Carry funds evidence or a card", "QAR 5,000 equivalent is the guideline."),
        ("Collect the free waiver at immigration", "Nothing to pay, nothing to apply for in advance."),
    ],
    fees=[("Visa on arrival", "Free", "30 days, conditions apply"),
          ("Extension", "About QAR 500", "Applied for locally"),
          ("Hayya card for events", "Varies", "Only for specific events")],
    tips=[
        "Qatar Airways gives free or cheap stopover hotels on long layovers. Ask at booking, it is not offered automatically.",
        "Souq Waqif comes alive after 8pm and is dead in the afternoon. Plan around the heat, not the clock.",
        "The metro is spotless, air conditioned and costs almost nothing. Gold Club carriages are worth the small extra in summer.",
        "Alcohol is served in hotel bars only, and is expensive. Buying it to take away requires a permit residents hold.",
    ],
    faqs=[
        ("Is Qatar visa free for Indians?", "<p>Effectively yes. A free 30-day visa waiver is issued on arrival, provided you have a confirmed hotel booking and a return ticket, or hold a valid US, UK or Schengen visa.</p>"),
        ("Do I need a hotel booking for Qatar?", "<p>Yes, unless you hold a valid US, UK or Schengen visa or residence permit. It is the condition most travellers overlook.</p>"),
        ("How long can Indians stay in Qatar?", "<p>Thirty days on the waiver, extendable once locally for a fee.</p>"),
    ]),

dict(
    slug="saudi-arabia-visa-for-indians",
    official_src=('Visit Saudi official visa portal', 'https://visa.visitsaudi.com/'),
    label="Saudi Arabia", short="Saudi Arabia",
    status="evisa", status_note="e-visa, one year multiple entry, 90 days per visit",
    h1="Saudi Arabia tourist e-visa for Indians",
    title="Saudi Arabia Visa for Indians 2026 | e-Visa Cost, Umrah, Rules",
    desc="Saudi Arabia's tourist e-visa gives Indians a year of multiple entry, 90 days per visit, for about SAR 535 including insurance. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "RUH"),
    blurb="Saudi Arabia opened up to tourism properly and the e-visa is now straightforward: a year of multiple "
          "entry, ninety days a visit, applied for online in minutes. It also covers Umrah, which used to need "
          "a separate route.",
    requirements=[
        "<strong>Passport valid six months</strong> and a digital photo.",
        "<strong>Medical insurance</strong>, bundled into the visa fee automatically.",
        "<strong>Return ticket</strong> and accommodation details.",
        "Women under 25 travelling alone may be asked for additional detail, though the guardian rule no longer applies to tourists.",
    ],
    official="Saudi Ministry of Tourism issues the tourist e-visa through the official Visit Saudi portal.",
    traps=[
        ("Using an agent site", "The official portal is visa.visitsaudi.com. Agents charge several times the fee."),
        ("Assuming the e-visa covers Hajj", "It covers Umrah and tourism. Hajj is a separate, quota-controlled process."),
        ("Ignoring dress codes", "Not a visa issue, but modest dress is enforced in public and for women covering shoulders and knees is expected."),
    ],
    steps=[
        ("Apply on the official Visit Saudi portal", "Ten minutes, and usually approved within 24 hours."),
        ("Pay the fee including insurance", "The insurance is compulsory and bundled."),
        ("Print the visa", "Carry it with your passport."),
        ("Have accommodation and a return ticket", "Both are asked for."),
        ("Register for Umrah separately if relevant", "Through the Nusuk app, which is free."),
    ],
    fees=[("Tourist e-visa", "About SAR 535", "Roughly Rs12,000, including compulsory insurance"),
          ("Visa on arrival", "Same fee", "For holders of valid US, UK or Schengen visas"),
          ("Overstay", "SAR 100 per day", "Plus possible ban")],
    tips=[
        "AlUla is the reason to go beyond the cities and it is a two-hour flight from Riyadh, not a day trip. Book Hegra tickets before you arrive, they sell out.",
        "Everything shuts for about 30 minutes at each of the five prayer times, including restaurants mid-meal. Check prayer timings and plan around them.",
        "Careem works better than Uber inside Saudi. Both are far cheaper than airport taxis.",
        "Riyadh in summer is 45 degrees and genuinely dangerous in the middle of the day. Visit between November and March if you have the choice.",
    ],
    faqs=[
        ("How much is the Saudi e-visa for Indians?", "<p>About SAR 535, roughly Rs12,000, which includes the compulsory medical insurance. It gives a year of multiple entry with 90 days per visit.</p>"),
        ("Can I do Umrah on a tourist visa?", "<p>Yes. The tourist e-visa covers Umrah. Hajj is separate and quota controlled.</p>"),
        ("Can Indian women travel to Saudi alone?", "<p>Yes. The guardian requirement does not apply to tourists. Modest dress is expected in public.</p>"),
    ]),

dict(
    slug="oman-visa-for-indians",
    official_src=('Royal Oman Police eVisa', 'https://evisa.rop.gov.om/'),
    label="Oman", short="Oman",
    status="evisa", status_note="e-visa, or visa free for 14 days holding a valid US, UK, Schengen, Canada, Australia or Japan visa",
    h1="Oman visa for Indian passport holders",
    title="Oman Visa for Indians 2026 | e-Visa, 14-Day Visa Free Rule",
    desc="Indians can enter Oman visa free for 14 days holding a valid US, UK, Schengen, Canadian, Australian or Japanese visa, or apply for an e-visa. Reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "MCT"),
    blurb="Oman has a rule worth checking before you pay for anything: if you already hold a valid visa for the "
          "US, UK, Schengen, Canada, Australia or Japan, and have used it at least once, you enter free for 14 days.",
    requirements=[
        "A <strong>valid and previously used</strong> US, UK, Schengen, Canadian, Australian or Japanese visa for the waiver, or an e-visa.",
        "<strong>Return ticket</strong> and confirmed accommodation.",
        "Passport valid <strong>six months</strong>.",
        "<strong>Medical insurance</strong> valid for the stay.",
    ],
    official="Royal Oman Police operates the e-visa system and the third-country visa waiver.",
    traps=[
        ("An unused third-country visa", "The qualifying visa must have been used to enter that country at least once. Issued but never used does not count."),
        ("Assuming the waiver is 30 days", "Fourteen days on the waiver. The e-visa gives longer."),
        ("No insurance", "Required, and occasionally checked at the counter."),
    ],
    steps=[
        ("Check whether the 14-day waiver applies", "Valid and previously used US, UK, Schengen, Canada, Australia or Japan visa."),
        ("If not, apply for the e-visa", "On the Royal Oman Police portal, evisa.rop.gov.om."),
        ("Buy travel insurance", "Required for the stay."),
        ("Have accommodation and a return ticket", "Both asked for at immigration."),
        ("Print everything", "Muscat immigration prefers paper."),
    ],
    fees=[("e-visa, 10 days", "OMR 5", "About Rs1,100"),
          ("e-visa, 30 days", "OMR 20", "About Rs4,500"),
          ("14-day waiver", "Free", "With a qualifying used third-country visa")],
    tips=[
        "Oman is a driving country. Roads are excellent and empty, and a hire car opens up wadis and forts that no tour reaches. An Indian licence plus an international permit works.",
        "Wadi Shab needs a short swim to reach the cave, so bring a dry bag. Sandals with grip beat flip flops on the walk in.",
        "Turtle nesting at Ras al Jinz runs year round but peaks June to September. It is booked through the reserve, not on the beach.",
        "Fridays start late. Shops and souqs open in the afternoon, so plan the morning around a drive or a beach.",
    ],
    faqs=[
        ("Is Oman visa free for Indians?", "<p>For 14 days, if you hold a valid US, UK, Schengen, Canadian, Australian or Japanese visa that you have already used at least once. Otherwise you need an e-visa.</p>"),
        ("How much is the Oman e-visa?", "<p>OMR 5 for 10 days, OMR 20 for 30 days, applied for on the Royal Oman Police portal.</p>"),
        ("Do I need insurance for Oman?", "<p>Yes, valid travel medical insurance for the stay. It is part of the entry requirements.</p>"),
    ]),

dict(
    slug="bahrain-visa-for-indians",
    official_src=('Kingdom of Bahrain eVisa', 'https://www.evisa.gov.bh/'),
    label="Bahrain", short="Bahrain",
    status="evisa", status_note="e-visa or visa on arrival, 14 days to 3 months",
    h1="Bahrain visa for Indian passport holders",
    title="Bahrain Visa for Indians 2026 | e-Visa, Visa on Arrival Cost",
    desc="Indians can get a Bahrain visa on arrival or apply for an e-visa, from 14 days to three months. Requirements, fees and what is checked. Reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "BAH"),
    blurb="Bahrain offers Indians both a visa on arrival and an e-visa, with durations from two weeks to three "
          "months. The e-visa is cheaper and removes any doubt at the counter.",
    requirements=[
        "<strong>Return ticket</strong> and confirmed accommodation.",
        "Passport valid <strong>six months</strong>.",
        "<strong>Funds evidence</strong>, around BHD 200 or a card.",
        "Holders of valid US, UK, Schengen or GCC residence get easier terms.",
    ],
    official="Kingdom of Bahrain eVisa portal, operated by the Nationality, Passports and Residence Affairs.",
    traps=[
        ("Paying more on arrival", "The visa on arrival costs more than the same e-visa applied for in advance."),
        ("No confirmed hotel", "Asked for at the counter, particularly if you have no GCC or Western visa."),
        ("Overstaying", "BHD 15 per day, and it is collected."),
    ],
    steps=[
        ("Apply for the e-visa online", "evisa.gov.bh, the official portal."),
        ("Or take the visa on arrival", "More expensive, but available."),
        ("Book accommodation", "Required for both routes."),
        ("Have a return ticket", "Within your permitted stay."),
        ("Carry funds evidence", "BHD 200 equivalent or an international card."),
    ],
    fees=[("e-visa, 14 days", "BHD 9", "About Rs2,100"),
          ("e-visa, 3 months", "BHD 16", "Multiple entry available"),
          ("Visa on arrival", "BHD 5 to 25", "Costs more than applying ahead")],
    tips=[
        "Bahrain is small enough to drive end to end in an hour. Hiring a car for two days covers everything worth seeing.",
        "The Formula One weekend in spring triples hotel prices and fills every flight. Either come for it or avoid the dates entirely.",
        "Alcohol is legally available in hotels and licensed restaurants, which is why weekends bring a lot of Saudi visitors over the causeway. Book restaurants on Thursday and Friday nights.",
        "Qal'at al-Bahrain is best late afternoon, when the light is good and the heat has dropped.",
    ],
    faqs=[
        ("Do Indians need a visa for Bahrain?", "<p>Yes, but it is easy. Apply for an e-visa online from BHD 9, or take a visa on arrival for more. Durations run from 14 days to three months.</p>"),
        ("Is the e-visa cheaper than visa on arrival?", "<p>Yes, noticeably. Applying in advance also removes any argument at the counter.</p>"),
        ("What documents do I need?", "<p>Passport valid six months, a return ticket, confirmed accommodation and evidence of funds.</p>"),
    ]),

dict(
    slug="kuwait-visa-for-indians",
    official_src=('Kuwait Ministry of Interior', 'https://www.moi.gov.kw/'),
    label="Kuwait", short="Kuwait",
    status="visa_required", status_note="Visa required, e-visa suspended for many categories",
    h1="Kuwait visa for Indian passport holders",
    title="Kuwait Visa for Indians 2026 | Requirements, Sponsor, Documents",
    desc="Kuwait requires Indians to hold a visa, usually sponsored by a host, employer or hotel. What is required and how the process works. Reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "KWI"),
    blurb="Kuwait is the strictest of the Gulf states for Indian tourists. There is no straightforward tourist "
          "e-visa route at present, and most visas are sponsored by a family member, employer or hotel.",
    requirements=[
        "A <strong>sponsor</strong>: a family member resident in Kuwait, an employer, or a hotel booking through an approved agent.",
        "Passport valid <strong>six months</strong>.",
        "<strong>Return ticket</strong> and confirmed accommodation.",
        "Supporting documents from the sponsor, including their civil ID.",
    ],
    official="Kuwait Ministry of Interior handles visa issuance and sponsorship requirements.",
    traps=[
        ("Assuming the e-visa is open", "Availability for Indian nationals has been restricted and reinstated more than once. Check current status before planning."),
        ("A sponsor without the right status", "The sponsor's residency category matters and not all can sponsor visitors."),
        ("Booking flights before the visa", "This is one where the visa genuinely should come first."),
    ],
    steps=[
        ("Confirm the current position", "Kuwait has opened and closed routes for Indian nationals more than once."),
        ("Arrange a sponsor", "Family, employer, or a hotel through an approved agency."),
        ("Gather the sponsor's documents", "Civil ID, salary certificate, and their invitation."),
        ("Submit the application", "Through the sponsor or the embassy."),
        ("Only then book travel", "Use a reservation until the visa is in hand."),
    ],
    fees=[("Visit visa", "About KWD 3", "Government fee; agent charges are extra"),
          ("Agent or sponsor fees", "Varies widely", "Often the larger cost"),
          ("Overstay", "KWD 2 per day", "Plus possible ban")],
    tips=[
        "Summer in Kuwait regularly passes 50 degrees. Between June and August, life happens indoors and after dark.",
        "Alcohol is completely prohibited, including in hotels. Do not pack any, and be careful with anything containing it.",
        "Friday is the quiet day. Malls open late, government offices are closed, and traffic is pleasant for once.",
        "The Avenues is one of the largest malls in the world and is genuinely a day out in summer, not merely shopping.",
    ],
    faqs=[
        ("Can Indians get a visa on arrival in Kuwait?", "<p>Not generally. Most Indian visitors need a sponsored visa arranged before travel, through family, an employer or a hotel via an approved agency.</p>"),
        ("Is there a Kuwait e-visa for Indians?", "<p>Availability has been restricted and reinstated more than once. Check the current position with the embassy before making plans.</p>"),
        ("Should I book flights first?", "<p>No. Kuwait is one where the visa genuinely comes first. Use a reservation for the application and buy the fare afterwards.</p>"),
    ]),

# ====================================================================== Africa
dict(
    slug="mauritius-visa-for-indians",
    official_src=('Mauritius Passport and Immigration Office', 'https://passport.govmu.org/'),
    label="Mauritius", short="Mauritius",
    status="visa_free", status_note="Visa free on arrival, 90 days",
    h1="Mauritius for Indian passport holders",
    title="Mauritius Visa Free for Indians 2026 | 90 Days, Entry Rules",
    desc="Mauritius is visa free for Indians for up to 90 days. You need accommodation, an onward ticket and funds. Verifiable reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "MRU"),
    blurb="Mauritius gives Indian passport holders 90 days visa free on arrival, one of the most generous "
          "allowances anywhere. The conditions are the usual ones and they are checked at the counter.",
    requirements=[
        "<strong>Confirmed accommodation</strong> for the stay.",
        "<strong>Return or onward ticket</strong> within 90 days.",
        "<strong>Funds</strong> of about USD 100 per day of stay.",
        "Passport valid for the duration of the stay, and an All-in-One travel form submitted online.",
    ],
    official="Mauritius Passport and Immigration Office grants visa-free entry to Indian nationals for 90 days.",
    traps=[
        ("Thin funds evidence", "The USD 100 per day guideline is applied more literally here than in most places."),
        ("No accommodation booking", "Asked for on arrival, especially if you are staying privately."),
        ("Missing the online travel form", "Required before departure."),
    ],
    steps=[
        ("Submit the All-in-One travel form", "Online, before you fly."),
        ("Book accommodation for the stay", "Or have the host's details ready."),
        ("Have a return ticket within 90 days", "Checked at the gate."),
        ("Carry funds evidence", "About USD 100 per day, card statements are fine."),
        ("Collect the free stamp on arrival", "Nothing to pay."),
    ],
    fees=[("Visa", "Free", "90 days for Indian nationals"),
          ("All-in-One travel form", "Free", "Mandatory before departure"),
          ("Extension", "About MUR 1,000", "Applied for locally")],
    tips=[
        "The south and east are wilder and cheaper than the north-west. Grand Baie is where the crowds are.",
        "A hire car is worth it. The island is small, the roads are good, and buses stop early in the evening.",
        "Cyclone season is January to March. Resorts stay open but sea excursions get cancelled at short notice.",
        "There is a large Indian-origin population and Bhojpuri is widely spoken, so Hindi will often get you further than English outside hotels.",
    ],
    faqs=[
        ("Is Mauritius visa free for Indians?", "<p>Yes, for up to 90 days. No visa to apply for, but you need accommodation, an onward ticket and funds of around USD 100 per day.</p>"),
        ("How much money do I need for Mauritius?", "<p>The guideline is about USD 100 per day of stay, and Mauritius applies it more literally than most. Card statements are accepted.</p>"),
        ("Do I need to fill anything in before flying?", "<p>Yes, the All-in-One travel form, submitted online before departure. It is free.</p>"),
    ]),

dict(
    slug="kenya-eta-for-indians",
    official_src=('Republic of Kenya eTA', 'https://www.etakenya.go.ke/'),
    label="Kenya", short="Kenya",
    status="evisa", status_note="Electronic Travel Authorisation, visa requirement abolished",
    h1="Kenya eTA for Indian passport holders",
    title="Kenya eTA for Indians 2026 | Cost, Processing Time, Safari Tips",
    desc="Kenya abolished visas and replaced them with an Electronic Travel Authorisation for about USD 30, approved in around three days. Reservations from %s." % money(PRICE_FLIGHT),
    route=("BOM", "NBO"),
    blurb="Kenya abolished visas altogether and replaced them with an Electronic Travel Authorisation. It is not "
          "quite visa free, since you still apply and pay, but it is quicker and there is no embassy involved.",
    requirements=[
        "<strong>eTA</strong> approved before travel. Everyone needs one, including children.",
        "<strong>Return ticket</strong> and accommodation details.",
        "Passport valid <strong>six months</strong>.",
        "<strong>Yellow fever certificate</strong> if arriving from a country with risk, which includes parts of India.",
    ],
    official="Republic of Kenya electronic Travel Authorisation, issued through the official eTA portal.",
    traps=[
        ("Leaving the eTA too late", "Three days is typical but it can take longer. Apply at least a week ahead."),
        ("Yellow fever certificate", "Check whether your departure route triggers the requirement. It is refused-boarding territory."),
        ("Unofficial eTA sites", "Plenty of them, all charging more than the government fee."),
    ],
    steps=[
        ("Apply on the official eTA portal", "etakenya.go.ke. Anything else is a reseller."),
        ("Upload passport, photo and your itinerary", "Accommodation and return flight details are asked for."),
        ("Pay about USD 30", "Non-refundable."),
        ("Wait around three days", "Apply a week ahead to be safe."),
        ("Carry the printed approval and yellow fever card", "Both get checked."),
    ],
    fees=[("eTA", "About USD 30", "Roughly Rs2,700, plus a small processing charge"),
          ("Park fees", "USD 60 to 200 per day", "Masai Mara is the expensive one"),
          ("Yellow fever vaccination", "About Rs1,500", "In India, at an authorised centre")],
    tips=[
        "The Great Migration crosses the Mara roughly July to October, but the herds do not read calendars. Book a camp that can move you between conservancies.",
        "Conservancies bordering the Mara allow off-road driving and night drives that the national reserve does not. Often better wildlife, fewer vehicles.",
        "Domestic bush flights have a 15kg soft-bag limit, strictly enforced. Leave the hard suitcase in Nairobi.",
        "M-Pesa runs the country. Get a local SIM at the airport and load it, it works where cards do not.",
    ],
    faqs=[
        ("Does Kenya still require a visa for Indians?", "<p>No. Kenya abolished visas and replaced them with an Electronic Travel Authorisation, which costs about USD 30 and is usually approved in three days.</p>"),
        ("Do I need a yellow fever certificate for Kenya?", "<p>If you are arriving from a country with transmission risk, which includes parts of India, yes. Check your route, because it is a refused-boarding issue.</p>"),
        ("How long does the Kenya eTA take?", "<p>About three days typically. Apply at least a week before you travel.</p>"),
    ]),

dict(
    slug="egypt-visa-for-indians",
    official_src=('Egypt e-Visa Portal', 'https://visa2egypt.gov.eg/'),
    label="Egypt", short="Egypt",
    status="evisa", status_note="e-visa, or visa on arrival holding a valid US, UK, Schengen or Japan visa",
    h1="Egypt visa for Indian passport holders",
    title="Egypt Visa for Indians 2026 | e-Visa Cost, Visa on Arrival Rules",
    desc="Indians need a visa for Egypt: an e-visa for about USD 25, or a visa on arrival if you hold a valid US, UK, Schengen or Japanese visa. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "CAI"),
    blurb="Egypt requires a visa from Indian passport holders, but there is a useful shortcut: hold a valid and "
          "used US, UK, Schengen or Japanese visa and you can get one on arrival instead.",
    requirements=[
        "<strong>e-visa</strong> applied for online, or a qualifying third-country visa for the on-arrival route.",
        "Passport valid <strong>six months</strong>.",
        "<strong>Return ticket</strong> and hotel bookings.",
        "Proof of funds, occasionally requested.",
    ],
    official="Egypt e-Visa Portal, operated by the Ministry of Interior.",
    traps=[
        ("Copycat e-visa sites", "The official one is visa2egypt.gov.eg. The rest add a markup."),
        ("Assuming Sinai-only entry covers the whole country", "The free Sinai permit covers Sharm and Dahab only, not Cairo or Luxor."),
        ("Single entry when you need two", "A Nile cruise that dips into Jordan or Israel and returns needs multiple entry."),
    ],
    steps=[
        ("Apply on the official e-visa portal", "About a week before travel; approval is usually a few days."),
        ("Or check whether you qualify on arrival", "Valid, used US, UK, Schengen or Japan visa."),
        ("Book hotels and a return ticket", "Both asked for."),
        ("Print the visa approval", "Carry it on paper."),
        ("Keep the entry stamp safe", "You need it on the way out."),
    ],
    fees=[("e-visa, single entry", "About USD 25", "Roughly Rs2,200"),
          ("e-visa, multiple entry", "About USD 60", ""),
          ("Visa on arrival", "USD 25", "Only with a qualifying third-country visa")],
    tips=[
        "Buy Giza tickets online in advance and go at opening, 8am. By ten it is hot, crowded and the touts have warmed up.",
        "Nile cruises between Luxor and Aswan run four or five nights. The three-night version skips Edfu and Kom Ombo, which are the good ones.",
        "Agree taxi fares before getting in, or use Uber in Cairo, which works well and removes the negotiation entirely.",
        "Small notes for tipping are essential and genuinely expected. Change a larger note at the hotel on day one.",
    ],
    faqs=[
        ("How much is an Egypt visa for Indians?", "<p>About USD 25 for a single-entry e-visa, USD 60 for multiple entry. A visa on arrival at the same price is available if you hold a valid US, UK, Schengen or Japanese visa.</p>"),
        ("Can Indians get an Egypt visa on arrival?", "<p>Only holding a valid and previously used US, UK, Schengen or Japanese visa. Otherwise apply for the e-visa online.</p>"),
        ("Does the Sinai permit cover Cairo?", "<p>No. The free Sinai-only permit covers Sharm el-Sheikh and Dahab. For Cairo or Luxor you need a full visa.</p>"),
    ]),

# ================================================================ Eurasia / HK
dict(
    slug="azerbaijan-visa-for-indians",
    official_src=('ASAN Visa portal', 'https://evisa.gov.az/'),
    label="Azerbaijan", short="Azerbaijan",
    status="evisa", status_note="ASAN e-visa, 30 days single entry",
    h1="Azerbaijan e-visa for Indian passport holders",
    title="Azerbaijan Visa for Indians 2026 | ASAN e-Visa Cost",
    desc="Azerbaijan's ASAN e-visa gives Indians 30 days for about USD 26, issued in three working days. Requirements and what to know. Reservations from %s." % money(PRICE_FLIGHT),
    route=("DEL", "GYD"),
    blurb="Baku became a favourite short-haul European-feeling break for Indian travellers, helped by a genuinely "
          "simple e-visa: thirty days, three working days, entirely online.",
    requirements=[
        "<strong>ASAN e-visa</strong> applied for online.",
        "Passport valid <strong>three months</strong> beyond the stay.",
        "<strong>Return ticket</strong> and accommodation details.",
        "No Nagorno-Karabakh entry stamps in the passport.",
    ],
    official="Republic of Azerbaijan ASAN Visa portal.",
    traps=[
        ("Applying through an agent", "evisa.gov.az is the official site and costs a fraction of what agents charge."),
        ("Urgent processing you do not need", "The three-hour option costs far more. Three working days is usually plenty."),
        ("Armenian border stamps", "Entry via Armenia or an Artsakh stamp will cause problems."),
    ],
    steps=[
        ("Apply on evisa.gov.az", "The official ASAN portal."),
        ("Choose standard processing", "Three working days, much cheaper than urgent."),
        ("Pay by card", "About USD 26 including the service fee."),
        ("Print the e-visa", "Carry it on paper with your passport."),
        ("Have accommodation and a return ticket", "Asked for at the counter."),
    ],
    fees=[("ASAN e-visa, standard", "About USD 26", "Three working days"),
          ("Urgent processing", "About USD 60", "Three hours, rarely necessary"),
          ("Extension", "Not generally available", "Leave and re-enter instead")],
    tips=[
        "Baku is compact and walkable but the Old City is cobbled and steep. Comfortable shoes matter more than you would expect.",
        "The Gobustan petroglyphs and mud volcanoes make a good half day, and the mud volcano road needs a proper vehicle, not a city taxi.",
        "There are direct flights from Delhi and Mumbai but the cheapest fares often route through Baku on Azerbaijan Airlines with a free stopover option.",
        "Indian restaurants are plentiful and good in Baku, which makes it an easy destination for a group with vegetarians in it.",
    ],
    faqs=[
        ("How much is the Azerbaijan e-visa for Indians?", "<p>About USD 26 for standard three-working-day processing on the official ASAN portal. Urgent processing costs roughly double and is rarely needed.</p>"),
        ("How long does it take?", "<p>Three working days on standard. Apply a week or two before you travel.</p>"),
        ("Is Azerbaijan visa free for Indians?", "<p>No, but the e-visa is quick, online and inexpensive.</p>"),
    ]),

dict(
    slug="hong-kong-visa-for-indians",
    official_src=('Hong Kong Immigration Department', 'https://www.immd.gov.hk/'),
    label="Hong Kong", short="Hong Kong",
    status="visa_free", status_note="Visa free for 14 days, but pre-arrival registration is compulsory",
    h1="Hong Kong for Indian passport holders",
    title="Hong Kong Visa Free for Indians 2026 | Pre-Arrival Registration",
    desc="Hong Kong is visa free for Indians for 14 days, but you must complete free Pre-Arrival Registration first. Without it you will be denied boarding.",
    route=("DEL", "HKG"),
    blurb="Hong Kong is visa free for Indian passport holders for 14 days, with one catch that catches a lot of "
          "people: you must complete Pre-Arrival Registration online first, and airlines will not board you without it.",
    requirements=[
        "<strong>Pre-Arrival Registration</strong>, completed online and free. Valid six months, multiple visits.",
        "<strong>Onward ticket</strong> within 14 days.",
        "Passport valid <strong>one month</strong> beyond your stay.",
        "Sufficient funds for the visit.",
    ],
    official="Hong Kong Immigration Department operates the Pre-Arrival Registration scheme for Indian nationals.",
    traps=[
        ("No Pre-Arrival Registration", "Airlines deny boarding. It is free and takes minutes, but it is not optional."),
        ("Assuming PAR is a visa", "It permits you to travel, not to enter. Immigration still decides at the counter."),
        ("Confusing Hong Kong with mainland China", "Completely separate entry rules. A China visa does not cover Hong Kong and vice versa."),
    ],
    steps=[
        ("Complete Pre-Arrival Registration", "Free, online, and valid for six months of visits."),
        ("Print or save the notification slip", "You need it at check-in."),
        ("Have an onward ticket within 14 days", "Checked at boarding."),
        ("Carry accommodation details", "Immigration asks."),
        ("Re-register after six months", "PAR expires; the free registration does not last forever."),
    ],
    fees=[("Visa", "Free", "14 days visa free for Indian nationals"),
          ("Pre-Arrival Registration", "Free", "Compulsory, valid six months"),
          ("Extension", "HKD 230", "Applied for locally, rarely granted for tourists")],
    tips=[
        "Get an Octopus card at the airport. It works on the MTR, buses, ferries, 7-Eleven and most cheap restaurants.",
        "The Star Ferry costs almost nothing and gives the same harbour view as the paid cruises. Go at dusk, upper deck.",
        "Hiking is the underrated part of Hong Kong. Dragon's Back is 90 minutes from Central and finishes at a beach.",
        "Vegetarian food is harder than you would expect. Learn to say it clearly, or head for the Buddhist restaurants in Causeway Bay.",
    ],
    faqs=[
        ("Is Hong Kong visa free for Indians?", "<p>Yes, for 14 days, but only after you complete free Pre-Arrival Registration online. Airlines will refuse boarding without it.</p>"),
        ("What is Pre-Arrival Registration?", "<p>A free online registration for Indian nationals, valid six months and multiple visits. It is compulsory and separate from a visa.</p>"),
        ("Does a China visa cover Hong Kong?", "<p>No. Hong Kong has completely separate entry rules. A mainland China visa does not admit you to Hong Kong.</p>"),
    ]),

# =================================================================== Central Asia
dict(
    slug="uzbekistan-visa-for-indians",
    official_src=('e-Visa portal, Republic of Uzbekistan', 'https://e-visa.gov.uz/'),
    label="Uzbekistan", short="Uzbekistan",
    status="visa_free", status_note="Visa free for short tourist stays",
    h1="Uzbekistan visa rules for Indian passport holders",
    title="Uzbekistan for Indians 2026 | Visa Free Entry and Rules",
    desc="Uzbekistan is visa free for Indian passport holders on short tourist stays. What immigration and airlines actually ask for, what the e-visa is still useful for, and the mistakes that get people stopped at check-in.",
    route=("DEL", "TAS"),
    blurb="Uzbekistan opened up to Indian travellers, and short tourist visits no longer need a visa applied "
          "for in advance. That removes the paperwork. It does not remove the questions at check-in, which is "
          "where most people actually get stopped.",
    requirements=[
        "<strong>Passport valid six months</strong> beyond your arrival date, with blank pages.",
        "<strong>Proof of onward or return travel.</strong> Airlines ask for this at check-in on a one-way booking, visa free or not.",
        "<strong>Accommodation details</strong> for the stay. Registration with your hotel is part of how the country tracks visitors.",
        "<strong>Funds for the trip</strong>, occasionally asked about at the border rather than proved on paper.",
    ],
    official="The Republic of Uzbekistan publishes current entry rules and the e-visa system on its official portal. Check it before you fly, because entry arrangements between the two countries have changed recently and news articles go stale faster than government pages.",
    traps=[
        ("Assuming visa free means no documents",
         "Two different things. You skip the visa application. You still face an airline agent who wants to see how you are leaving the country, and an immigration officer who may ask where you are staying."),
        ("Not registering your stay",
         "Uzbekistan expects visitors to be registered where they sleep. Hotels do it automatically. Stay privately or in an unregistered rental and it becomes your problem, sometimes at the airport on the way out."),
        ("Booking a one-way flight",
         "The single most common reason to be denied boarding to a visa free country. The airline is liable for flying you if you are refused entry, so it asks first."),
        ("Relying on a news headline for the rules",
         "Entry arrangements changed recently, and duration limits are exactly the detail that gets reported imprecisely. Read the official portal, not a listicle."),
    ],
    steps=[
        ("Check the current rule on the official portal",
         "Confirm the visa free allowance and how long it runs for your passport. This has changed recently, so anything written more than a few months ago may be wrong."),
        ("Confirm your passport has six months left",
         "Counted from arrival, not from booking. This catches people whose passport is fine today and short by the time they fly."),
        ("Book accommodation for the whole stay",
         "It also handles your registration, which is the part travellers forget."),
        ("Sort proof of onward travel",
         "Whether or not you need a visa, the airline needs to see you leaving. A held reservation with a live PNR satisfies this."),
        ("Keep it all on your phone and on paper",
         "Tashkent immigration is straightforward. Airline check-in desks in India are where the questions happen."),
    ],
    fees=[("Tourist visa", "Not required", "Short tourist stays are visa free for Indian passport holders"),
          ("e-Visa", "Around USD 20", "Only if your trip falls outside the visa free arrangement"),
          ("Registration", "Free", "Handled by your hotel, but it must happen")],
    tips=[
        "Tashkent to Samarkand on the Afrosiyob high speed train takes a bit over two hours and costs a fraction of a flight. Book it online in advance, because it sells out and it is the single best way to move between the big three cities.",
        "Carry cash. Card acceptance is improving in Tashkent and thin everywhere else, and som notes come in large denominations that confuse first timers.",
        "Registan in Samarkand is worth doing twice, once at opening and once after dark when it is lit. The light in between is flat and the photographs are disappointing.",
        "Uzbek plov is a lunch dish, not a dinner one. The good places sell out by early afternoon and close.",
        "October and April are the two months worth planning around. July heat in the desert cities is genuinely punishing.",
    ],
    faqs=[
        ("Is Uzbekistan visa free for Indians?",
         "<p>Yes, for short tourist stays. Check the current allowance on the official Uzbek portal before you book, because this arrangement changed recently and the exact duration is the detail most often reported wrongly.</p>"),
        ("Do I still need a return ticket if no visa is required?",
         "<p>Yes, in practice. Visa free governs whether the country lets you in. It has no effect on whether an airline lets you board, and airlines ask one-way travellers for proof of onward travel because they carry the cost if you are refused entry.</p>"),
        ("What is the e-visa for, if it is visa free?",
         "<p>Longer stays, or purposes outside tourism. If your trip fits the visa free arrangement you do not need it.</p>"),
        ("Do I need to register where I stay?",
         "<p>Yes. Hotels do it for you as a matter of course. If you are staying privately or in an unregistered rental, it becomes your responsibility, and it is sometimes checked on departure.</p>"),
        ("How long is the flight from India?",
         "<p>Delhi to Tashkent is a little over three hours direct, which makes it one of the shortest genuinely foreign trips available from north India.</p>"),
    ]),
]
