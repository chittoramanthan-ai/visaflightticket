# -*- coding: utf-8 -*-
"""Visa / destination landing pages - the long-tail SEO engine."""

from build import (ICON, BRAND, DELIVERY, SITE_URL, TODAY,
                   PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH,
                   money, add_page, url, abs_url, faq_block, faq_schema,
                   crumbs, cta_band, pricing_tickets,
                   stat_bar, trust_cards, airline_strip)
import content_core


# --------------------------------------------------------------------------
# Data. Each entry drives one landing page.
#   slug, nav label, H1 subject, route example, and the country-specific facts.
# --------------------------------------------------------------------------
VISAS = [
    dict(
        slug="schengen-visa-flight-reservation",
        label="Schengen visa",
        short="Schengen",
        h1="Flight reservation for a Schengen visa",
        title="Flight Reservation for Schengen Visa | Verifiable PNR %s" % money(PRICE_FLIGHT),
        desc="Get a verifiable flight reservation for your Schengen visa application. Live PNR, return itinerary, hotel bookings for every night. %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "CDG"),
        blurb="All 29 Schengen states run the same visa code, so the document requirements barely differ between "
              "France, Germany, Italy, Spain and the rest. Every one of them wants a round-trip itinerary and "
              "accommodation covering the full stay.",
        requirements=[
            "A <strong>return or onward itinerary</strong> showing entry to and exit from the Schengen Area. One-way is refused almost automatically.",
            "<strong>Accommodation for every night</strong> of the stay. Hotel bookings, or an invitation letter if you are staying with a host.",
            "<strong>Travel medical insurance</strong> with at least &euro;30,000 coverage, valid across the whole area for the exact dates on your itinerary.",
            "Dates that <strong>fall inside your insurance validity</strong> and inside the 90-days-in-180 rule.",
            "Entry through the country you are applying to, or a clear main-destination justification if not.",
        ],
        official="The European Commission's own visa guidance advises applicants not to purchase non-refundable "
                 "tickets before a decision, and VFS Global centres across the network accept unpaid reservations "
                 "with a valid booking reference.",
        traps=[
            ("Applying to the wrong consulate", "You apply to the country of your <em>main destination</em>. Where you spend the most nights. If nights are equal, apply to your country of first entry. Your flight reservation should make that obvious at a glance."),
            ("Gaps in accommodation", "A multi-city trip with one hotel booking is the classic error. Every night needs cover, and officers count."),
            ("Insurance that expires before the return flight", "Buy insurance after your itinerary is fixed, not before, and match the dates exactly."),
            ("Booking too far ahead", "A reservation for travel eight months out with a 48-hour hold window will have lapsed by the time your file is opened. Apply within the sensible window, typically 15 days to 6 months before travel."),
        ],
        faqs=[
            ("Does the Schengen consulate accept an unpaid flight reservation?",
             "<p>Yes. The requirement is for a flight <em>reservation</em> or itinerary, not proof of purchase. EU guidance explicitly warns applicants against buying non-refundable tickets before a visa decision, and consulates and VFS centres process unpaid reservations with valid booking references every day.</p>"),
            ("Do I need to show a return flight?",
             "<p>Yes. A Schengen tourist visa is issued on the basis that you will leave, so the itinerary must show both entry and exit. An onward flight out of the Schengen Area counts as an exit. It does not have to return you home.</p>"),
            ("Do I need a hotel booking for all 15 days?",
             "<p>Every night must be accounted for. Hotels, apartments, or an invitation letter from a host with proof of their address. Our <a href=\"%s\">flight and hotel bundle</a> issues one accommodation booking per city so there are no gaps.</p>" % url("flight-and-hotel-package")),
            ("Which country should I apply to for a multi-country trip?",
             "<p>The country where you will spend the most nights. If it is a genuine tie, apply where you first enter the area. Keep the flight reservation consistent with whichever you choose.</p>"),
            ("How far in advance can I apply?",
             "<p>Up to six months before travel, and at least 15 days before. Most people apply four to eight weeks out, which is also when a flight reservation makes most sense.</p>"),
        ],
    ),
    dict(
        slug="us-visa-flight-itinerary",
        label="US visa (B1/B2)",
        short="United States",
        h1="Flight itinerary for a US B1/B2 visa",
        title="Flight Itinerary for US Visa | B1/B2 Dummy Ticket %s" % money(PRICE_FLIGHT),
        desc="Flight itinerary for your US B1/B2 visa interview. Verifiable reservation with a live PNR, no ticket purchase before approval. %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("BOM", "JFK"),
        blurb="The US is the one major destination that explicitly tells you <em>not</em> to buy a ticket before your "
              "interview. Consular officers care far more about your ties to home than about your itinerary, but "
              "an itinerary still helps you answer the questions you will actually be asked.",
        requirements=[
            "The DS-160 asks for <strong>intended arrival date and address in the US</strong>. Your itinerary and hotel booking supply both.",
            "A <strong>plausible, specific plan</strong>: officers probe vague answers about where you are going and for how long.",
            "Evidence you will <strong>return home</strong>: employment, family, property, studies. This carries more weight than any document.",
            "Consistency between the DS-160, your itinerary and what you say at the counter.",
        ],
        official="The US Department of State advises applicants not to make final travel plans or buy non-refundable "
                 "tickets until they have a visa in hand. An itinerary is used to answer the DS-160 rather than as a "
                 "mandatory attachment.",
        traps=[
            ("Treating the itinerary as the case", "It is not. The B1/B2 decision turns on Section 214(b). Whether you have overcome the presumption of immigrant intent. Bring your ties."),
            ("DS-160 dates that contradict the itinerary", "The officer has your DS-160 on screen. If it says 12 March and your itinerary says 20 March, expect a question you did not need."),
            ("A trip too long to be plausible", "A six-week holiday on two weeks of annual leave invites scrutiny."),
            ("Buying the ticket first", "Interview slots move and administrative processing happens. This is exactly the scenario a reservation exists to protect you from."),
        ],
        faqs=[
            ("Is a flight itinerary required for a US visa interview?",
             "<p>It is not a mandatory attachment. But the DS-160 asks for your intended arrival date and US address, and officers frequently ask about your plans. Having a concrete itinerary makes those answers specific rather than vague.</p>"),
            ("Should I buy the ticket before the interview?",
             "<p>No. The Department of State says so directly. Interview outcomes and administrative processing timelines are unpredictable, and a non-refundable fare is a real loss.</p>"),
            ("Will a reservation improve my chances?",
             "<p>Not on its own. A B1/B2 refusal is almost always about ties to your home country, not paperwork. The itinerary helps you present a coherent, specific plan. Nothing more, and no service can honestly claim otherwise.</p>"),
            ("What about a hotel booking?",
             "<p>Useful for the DS-160 US address field and for answering &ldquo;where will you stay?&rdquo;. %s on its own, or %s bundled with the flight itinerary.</p>" % (money(PRICE_HOTEL), money(PRICE_BOTH))),
        ],
    ),
    dict(
        slug="uk-visa-flight-reservation",
        label="UK visa",
        short="United Kingdom",
        h1="Flight reservation for a UK visitor visa",
        title="Flight Reservation for UK Visa | Standard Visitor %s" % money(PRICE_FLIGHT),
        desc="Flight reservation for a UK Standard Visitor visa. Verifiable PNR, return itinerary, hotel bookings. %s per traveller, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "LHR"),
        blurb="UKVI does not publish a mandatory flight-booking requirement for the Standard Visitor visa. What it does "
              "require is that you satisfy the caseworker you will leave at the end of your visit, and a dated "
              "return itinerary is one of the cleanest ways to show that.",
        requirements=[
            "Evidence you will <strong>leave the UK</strong> at the end of your visit. A return or onward booking is the simplest form.",
            "A <strong>travel plan and accommodation</strong> for the visit, uploaded with the online application.",
            "Proof you can <strong>fund the trip</strong> without working. Bank statements covering the stay.",
            "Consistency with what you entered in the online form and any sponsor letter.",
        ],
        official="UKVI guidance emphasises that you should not book travel until your visa is decided, and caseworkers "
                 "assess intention to leave rather than requiring a purchased ticket.",
        traps=[
            ("Buying tickets before the decision", "UK processing times swing widely. Guidance explicitly advises against booking travel before you have the decision."),
            ("A return date after your visa expires", "Check that the return leg falls inside the six-month visitor allowance."),
            ("Unexplained sponsor arrangements", "If someone else is paying, say so, with their letter and their bank statements. Do not leave the caseworker to infer it."),
            ("Documents in the wrong format", "UKVI wants uploads as clean PDFs. A phone photo of a screen reads as careless."),
        ],
        faqs=[
            ("Do I need a flight booking for a UK visitor visa?",
             "<p>It is not a listed mandatory document, but you must satisfy the caseworker that you will leave. A dated return reservation, with accommodation and funds, is the standard way applicants demonstrate that.</p>"),
            ("Should I buy the ticket first?",
             "<p>No. UKVI itself advises against booking travel before a decision. Use a reservation for the application and buy the fare once the visa is granted.</p>"),
            ("How long can I stay?",
             "<p>A Standard Visitor visa normally permits up to six months per visit. Your return leg should fall well inside that window.</p>"),
            ("Do I need a hotel booking too?",
             "<p>You need to show where you will stay. A hotel booking works; so does a letter from the friend or relative hosting you, with their address details.</p>"),
        ],
    ),
    dict(
        slug="canada-visa-flight-itinerary",
        label="Canada visa",
        short="Canada",
        h1="Flight itinerary for a Canada visitor visa",
        title="Flight Itinerary for Canada Visa | TRV Reservation %s" % money(PRICE_FLIGHT),
        desc="Flight itinerary for a Canadian visitor visa (TRV). Verifiable reservation with live PNR, no purchase before approval. %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "YYZ"),
        blurb="IRCC is explicit: do not buy your ticket until the visa is issued. Processing times for a Temporary "
              "Resident Visa are among the least predictable of any major destination, which makes an unpaid "
              "reservation the obviously sensible choice.",
        requirements=[
            "A <strong>travel plan</strong> with intended dates. Supplied through the application form and supporting documents.",
            "Proof of <strong>funds</strong> for the trip and of <strong>ties</strong> to your home country.",
            "A <strong>purpose of travel letter</strong> that matches your itinerary dates.",
            "An invitation letter if you are visiting family or friends, matching your accommodation plan.",
        ],
        official="IRCC advises applicants not to book non-refundable travel until the visa has been issued, and "
                 "accepts a travel plan or reservation as supporting evidence of intended travel.",
        traps=[
            ("Booking flights before approval", "TRV processing can run many weeks. IRCC says plainly: do not buy tickets first."),
            ("Itinerary that contradicts the purpose letter", "If your letter says a two-week family visit, the itinerary should not show five weeks."),
            ("Missing the biometrics window", "Biometrics can add weeks. Build that into the dates on your reservation."),
            ("Single-entry assumptions", "Most TRVs are issued multiple-entry, but do not assume. Check before planning side trips to the US."),
        ],
        faqs=[
            ("Do I need a flight booking for a Canadian visitor visa?",
             "<p>Not as a mandatory document, but a travel plan with dates is expected and a reservation is the usual way to evidence it. IRCC specifically advises against buying tickets before approval.</p>"),
            ("How long should the reservation be valid?",
             "<p>Long enough to be live when an officer opens your file. Because Canadian processing is slow and variable, most applicants submit a reservation and then buy the real fare after approval.</p>"),
            ("Do I need a hotel booking?",
             "<p>If you are staying in hotels, yes. It supports your stated plan. If you are staying with family, an invitation letter with their address serves the same purpose.</p>"),
        ],
    ),
    dict(
        slug="dubai-uae-visa-flight-ticket",
        label="Dubai / UAE visa",
        short="UAE",
        h1="Flight ticket for a Dubai or UAE tourist visa",
        title="Flight Ticket for Dubai Visa | UAE Reservation %s" % money(PRICE_FLIGHT),
        desc="Flight reservation and hotel booking for a Dubai or UAE tourist visa. Verifiable PNR, confirmed accommodation, delivered in %s from %s." % (DELIVERY, money(PRICE_FLIGHT)),
        route=("BOM", "DXB"),
        blurb="UAE tourist visas are typically arranged through an airline, hotel or licensed agent as sponsor. The "
              "documentation is lighter than a Schengen file, but the return-flight and accommodation requirements "
              "are enforced hard. At the visa stage and again at the immigration counter.",
        requirements=[
            "A <strong>confirmed return or onward flight</strong>. This is checked on arrival, not only at application.",
            "<strong>Hotel booking</strong> for the stay, or the address and details of your host.",
            "Passport valid for at least <strong>six months</strong> from entry.",
            "Sponsor details, where the visa is issued through an airline or hotel.",
        ],
        official="UAE immigration and airline sponsors require evidence of onward travel and accommodation; "
                 "immigration officers at DXB and AUH routinely ask to see a return booking.",
        traps=[
            ("Arriving on a one-way ticket", "One of the most reliable ways to be pulled aside at UAE immigration. Carry an onward booking even on a visa-on-arrival nationality."),
            ("Overstaying the visa period", "UAE overstay fines accrue daily and are collected at departure. Match your return flight to the visa validity, not to your hopes."),
            ("Hotel booking in someone else's name", "The accommodation booking should name the traveller."),
            ("Passport under six months validity", "Refused at check-in, before you get anywhere near immigration."),
        ],
        faqs=[
            ("Do I need a return ticket for Dubai?",
             "<p>Yes in practice. UAE immigration and airline check-in staff both look for evidence of onward travel, and this is enforced consistently. A verifiable onward reservation satisfies it.</p>"),
            ("Is a hotel booking required for a UAE tourist visa?",
             "<p>You need to show where you are staying. A hotel booking or a host's address. Sponsors and immigration both ask.</p>"),
            ("How quickly can I get the documents?",
             "<p>Within %s. UAE trips are often booked at short notice, so priority handling is available if you are travelling the same day.</p>" % DELIVERY),
        ],
    ),
    dict(
        slug="australia-visa-flight-reservation",
        label="Australia visa",
        short="Australia",
        h1="Flight reservation for an Australian visitor visa",
        title="Flight Reservation for Australia Visa | Subclass 600 %s" % money(PRICE_FLIGHT),
        desc="Flight reservation for an Australian visitor visa (subclass 600). Verifiable PNR, no ticket purchase before grant. %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "SYD"),
        blurb="Australia's Department of Home Affairs assesses whether you are a genuine temporary entrant. Travel "
              "plans support that; buying tickets before the grant undermines your own position if the visa is "
              "delayed, which subclass 600 applications routinely are.",
        requirements=[
            "Evidence of a <strong>genuine temporary visit</strong>: a dated plan showing arrival and departure.",
            "<strong>Sufficient funds</strong> for the visit without working.",
            "<strong>Health and character</strong> requirements, which may add a medical appointment to your timeline.",
            "An invitation or sponsorship letter where relevant, consistent with your itinerary.",
        ],
        official="Home Affairs advises against making non-refundable travel arrangements before a visa is granted, "
                 "and accepts a travel plan as supporting evidence.",
        traps=[
            ("Booking before the grant", "Subclass 600 processing varies from days to months. Home Affairs advises waiting."),
            ("Stated purpose not matching the dates", "A three-week 'family wedding visit' with a three-month itinerary raises the genuine-temporary-entrant question."),
            ("Ignoring health checks", "If a medical is requested, it can add weeks. Leave room in your dates."),
            ("Assuming multiple entry", "Check the grant notice before planning a side trip to New Zealand."),
        ],
        faqs=[
            ("Is a flight booking required for an Australian visitor visa?",
             "<p>Not mandatory, but a clear travel plan supports the genuine-temporary-entrant assessment. Home Affairs advises against buying non-refundable travel before the grant.</p>"),
            ("Can I use a reservation for a subclass 600 application?",
             "<p>Yes. Submit a verifiable reservation showing your intended dates, and buy the fare once the visa is granted.</p>"),
        ],
    ),
    dict(
        slug="japan-visa-flight-itinerary",
        label="Japan visa",
        short="Japan",
        h1="Flight itinerary for a Japan tourist visa",
        title="Flight Itinerary for Japan Visa | Daily Schedule + PNR %s" % money(PRICE_FLIGHT),
        desc="Flight itinerary and hotel bookings for a Japan tourist visa, matched to the required daily schedule of stay. %s per traveller, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "NRT"),
        blurb="Japan is unusually specific: the application asks for a <strong>daily schedule of stay</strong> listing "
              "where you are each day, with contact details. Your flight and hotel documents have to line up with "
              "that schedule exactly, which is where most applications come unstuck.",
        requirements=[
            "A <strong>Schedule of Stay</strong> form covering every day from arrival to departure.",
            "<strong>Flight itinerary</strong> with confirmed arrival and departure dates matching day 1 and the final day.",
            "<strong>Hotel bookings</strong> whose check-in and check-out dates match the schedule, city by city.",
            "Bank statements, usually for the last six months.",
        ],
        official="Japanese embassies and consulates require a schedule of stay and supporting travel documents; "
                 "applications are typically lodged through an accredited travel agency.",
        traps=[
            ("Schedule that does not match the bookings", "The single most common Japan rejection. If the schedule says Kyoto on day 4, there must be a Kyoto booking for that night."),
            ("Missing internal moves", "Tokyo to Osaka on day 5 should appear in the schedule, not just in your head."),
            ("Applying too early", "Japanese visas are usually issued with a three-month entry window. Applying six months out wastes it."),
            ("Assuming you can apply direct", "In many countries you must apply through an accredited agency, not at the consulate counter."),
        ],
        faqs=[
            ("Does Japan require a confirmed flight booking?",
             "<p>You must submit a flight itinerary with your dates. A verifiable reservation meets the requirement; Japanese missions do not require proof of payment.</p>"),
            ("How detailed must the schedule of stay be?",
             "<p>Day by day: the date, the city, the accommodation name and its phone number. Your hotel bookings should back up every line of it.</p>"),
            ("Can you match hotel bookings to a multi-city schedule?",
             "<p>Yes. Give us the city order and nights in each, and we issue one booking per city so your schedule reconciles cleanly. That is the <a href=\"%s\">bundle</a>.</p>" % url("flight-and-hotel-package")),
        ],
    ),
    dict(
        slug="turkey-visa-flight-ticket",
        label="Turkey visa",
        short="Turkey",
        h1="Flight ticket for a Turkey visa",
        title="Flight Ticket for Turkey Visa | e-Visa Reservation %s" % money(PRICE_FLIGHT),
        desc="Flight reservation and hotel booking for a Turkey e-visa or sticker visa. Verifiable PNR, delivered in %s from %s." % (DELIVERY, money(PRICE_FLIGHT)),
        route=("DEL", "IST"),
        blurb="Turkey's e-visa is quick for eligible nationalities, but the checks happen at the airport instead of "
              "at a consulate: airline staff and Turkish immigration both ask for onward travel and accommodation.",
        requirements=[
            "A <strong>return or onward flight booking</strong>: checked at check-in and on arrival.",
            "<strong>Hotel booking</strong> or host address for the duration of the stay.",
            "Passport valid at least <strong>150 days</strong> from entry for most e-visa nationalities.",
            "Proof of funds, occasionally requested at the border.",
        ],
        official="Turkish immigration authorities require evidence of accommodation and onward travel for visitors; "
                 "airlines enforce this at check-in under carrier-liability rules.",
        traps=[
            ("Assuming the e-visa is the whole story", "It gets you to the counter. Onward travel and accommodation get you through it."),
            ("The 150-day passport rule", "Stricter than the usual six months and frequently missed."),
            ("Sticker-visa nationalities applying for an e-visa", "Check your nationality against the official e-visa list before assuming eligibility."),
        ],
        faqs=[
            ("Do I need a return ticket for Turkey?",
             "<p>Yes in practice. Airlines check onward travel at check-in, and Turkish immigration may ask on arrival. A verifiable onward booking covers both.</p>"),
            ("Is a hotel booking needed for a Turkish e-visa?",
             "<p>The online form does not always demand one, but immigration can ask where you are staying. Carrying a confirmed booking removes the risk.</p>"),
        ],
    ),
    dict(
        slug="thailand-visa-flight-ticket",
        label="Thailand visa",
        short="Thailand",
        h1="Flight ticket and onward travel proof for Thailand",
        title="Flight Ticket for Thailand | Onward Travel Proof %s" % money(PRICE_FLIGHT),
        desc="Proof of onward travel for Thailand, plus hotel bookings for a Thai visa or visa exemption entry. Verifiable PNR from %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "BKK"),
        blurb="Thailand enforces proof of onward travel more consistently than almost anywhere else, and the "
              "enforcement happens at the check-in desk in your departure city. Before you have any chance to "
              "explain your plans to a Thai official.",
        requirements=[
            "<strong>Proof of onward travel</strong> within your permitted stay. 30, 60 or 90 days depending on entry type.",
            "<strong>Accommodation details</strong> for the arrival card and for immigration questions.",
            "Proof of funds. Officially 10,000 THB per person, occasionally spot-checked.",
            "For a tourist visa applied for in advance, the itinerary and accommodation in the application pack.",
        ],
        official="Thai immigration requires visitors to hold evidence of onward travel within the permitted period, "
                 "and airlines enforce it at check-in because carriers are liable for returning refused passengers.",
        traps=[
            ("Flying in one-way on a visa exemption", "Denied boarding is common on this route. It is an airline decision, not an immigration one."),
            ("Onward flight after the permitted stay ends", "A 45-day onward booking on a 30-day exemption defeats the purpose."),
            ("Land-border onward bookings", "Bus and train tickets to Malaysia or Laos are usually accepted, but airline staff read flight bookings faster."),
        ],
        faqs=[
            ("Do I really need proof of onward travel for Thailand?",
             "<p>Yes, and it is enforced at check-in in your departure city. Airlines are financially liable if you are refused entry, so they check before boarding.</p>"),
            ("Does a bus or train ticket count?",
             "<p>Usually, provided it crosses an international border within your permitted stay. A flight booking is what airline systems display most readily.</p>"),
            ("How long does the onward booking need to be valid?",
             "<p>Only until you have boarded and cleared immigration. That is why buying a full fare for this is poor value.</p>"),
        ],
    ),
    dict(
        slug="south-korea-visa-flight-itinerary",
        label="South Korea visa",
        short="South Korea",
        h1="Flight itinerary for a South Korea tourist visa",
        title="Flight Itinerary for Korea Visa | C-3 Reservation %s" % money(PRICE_FLIGHT),
        desc="Flight itinerary and hotel bookings for a South Korean C-3 tourist visa or K-ETA entry. Verifiable PNR from %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "ICN"),
        blurb="Korean consulates want a documented plan: a round-trip itinerary, accommodation for the stay, and "
              "financial evidence. K-ETA travellers face a lighter process but the same onward-travel checks at the "
              "airport.",
        requirements=[
            "A <strong>round-trip itinerary</strong> with fixed dates.",
            "<strong>Accommodation bookings</strong> covering the visit, or an invitation from a host in Korea.",
            "<strong>Bank statements</strong>, typically for the last three to six months.",
            "Employment or study evidence supporting your return.",
        ],
        official="Korean diplomatic missions require a detailed travel plan with supporting reservations for C-3 "
                 "tourist visa applications.",
        traps=[
            ("K-ETA confusion", "Check whether your nationality needs a visa or a K-ETA before preparing a full file. The lists change."),
            ("Thin financial evidence", "Korean consulates weigh finances heavily. Statements should show a stable balance, not a sudden deposit."),
            ("Itinerary longer than the C-3 allowance", "Usually 90 days maximum. Keep the return leg inside it."),
        ],
        faqs=[
            ("Does Korea require a confirmed flight booking?",
             "<p>A round-trip itinerary is expected with the application. A verifiable reservation satisfies it; payment proof is not required.</p>"),
            ("Do I need hotel bookings for the whole stay?",
             "<p>Accommodation should cover the visit. An invitation letter from a host works instead if you are staying privately.</p>"),
        ],
    ),
    dict(
        slug="singapore-visa-flight-ticket",
        label="Singapore visa",
        short="Singapore",
        h1="Flight ticket and onward travel proof for Singapore",
        title="Flight Ticket for Singapore Visa | Onward Proof %s" % money(PRICE_FLIGHT),
        desc="Flight reservation and hotel booking for a Singapore visa or visa-free entry, plus proof of onward travel. From %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("DEL", "SIN"),
        blurb="Singapore's ICA is efficient and unsentimental. Onward travel and accommodation are part of the SG "
              "Arrival Card, and officers at Changi do ask, particularly of travellers on one-way tickets.",
        requirements=[
            "A <strong>confirmed onward or return booking</strong> within the permitted stay.",
            "<strong>Accommodation address</strong> for the SG Arrival Card, submitted within three days before arrival.",
            "Passport valid for at least <strong>six months</strong>.",
            "Sufficient funds for the visit.",
        ],
        official="Singapore's Immigration and Checkpoints Authority requires visitors to hold onward travel and "
                 "accommodation details, both declared on the SG Arrival Card.",
        traps=[
            ("Leaving the arrival card too late", "It must be submitted within three days before arrival, and it asks for your accommodation."),
            ("One-way entry", "Expect questions at Changi, and possibly at check-in before you leave."),
            ("Assuming the visa-free period is generous", "Length of stay is granted at the officer's discretion. 30 days is not automatic for every nationality."),
        ],
        faqs=[
            ("Do I need proof of onward travel for Singapore?",
             "<p>Yes. It is declared on the SG Arrival Card and checked at immigration, and airlines frequently verify it at check-in.</p>"),
            ("Do I need a hotel booking?",
             "<p>You must declare where you are staying. A confirmed booking with an address is the cleanest way to answer.</p>"),
        ],
    ),
    dict(
        slug="new-zealand-visa-flight-ticket",
        label="New Zealand visa",
        short="New Zealand",
        h1="Flight ticket and onward travel proof for New Zealand",
        title="Flight Ticket for New Zealand Visa | Onward Proof %s" % money(PRICE_FLIGHT),
        desc="Onward travel proof and hotel bookings for a New Zealand visitor visa or NZeTA entry. Verifiable reservation from %s, delivered in %s." % (money(PRICE_FLIGHT), DELIVERY),
        route=("SYD", "AKL"),
        blurb="New Zealand requires visitors to hold onward tickets or evidence of sufficient funds to buy them. In "
              "practice, airline staff on inbound routes ask for the onward booking, because the alternative is "
              "producing bank statements at a check-in desk.",
        requirements=[
            "<strong>Onward travel</strong> to a country you have the right to enter, within your permitted stay.",
            "Evidence of <strong>funds</strong>: commonly NZ$1,000 per month of stay, or NZ$400 if accommodation is prepaid.",
            "<strong>NZeTA</strong> for visa-waiver nationalities, requested before travel.",
            "Accommodation details for the arrival card.",
        ],
        official="Immigration New Zealand requires visitors to hold an onward ticket or show funds sufficient to "
                 "purchase one, alongside evidence of accommodation.",
        traps=[
            ("Relying on the 'sufficient funds' alternative", "Legally valid, practically awkward at a check-in desk. Carry the onward booking instead."),
            ("Forgetting the NZeTA", "It must be requested before you fly and can take up to 72 hours."),
            ("Onward flight beyond the permitted stay", "Match it to the period you will actually be granted."),
        ],
        faqs=[
            ("Does New Zealand require an onward ticket?",
             "<p>You must hold an onward ticket or show funds sufficient to buy one. A verifiable onward booking is far quicker to present at check-in than bank statements.</p>"),
            ("Is prepaid accommodation useful?",
             "<p>Yes. It lowers the funds threshold from around NZ$1,000 to NZ$400 per month of stay.</p>"),
        ],
    ),
]


# --------------------------------------------------------------------------
def link_list():
    return [(v["label"], v["slug"]) for v in VISAS]


def build():
    _index()
    for v in VISAS:
        _page(v)


def _index():
    c_html, c_schema = crumbs([("Visa guides", None)])
    cards = ""
    for v in VISAS:
        cards += """
<a class="card card--link post-card" href="%s">
  <span class="tagline">%s</span>
  <h3>%s</h3>
  <p>%s</p>
  <span class="more">Read the requirements &rarr;</span>
</a>""" % (url("visa/" + v["slug"]), v["short"], v["h1"],
           _strip(v["blurb"])[:145].rsplit(" ", 1)[0] + "&hellip;")

    body = """
<section>
  <div class="wrap">
    %s
    <div class="center" style="margin-bottom:2.6rem">
      <h1>Visa guides by destination</h1>
      <p class="lede">What each consulate actually asks for, which rules are enforced at the airport rather than the
      counter, and the mistakes that get files returned. Written for people filing this month.</p>
    </div>
    <h2 class="sr">All destination guides</h2>
    <div class="grid g3">%s</div>
  </div>
</section>
%s""" % (c_html, cards, cta_band())

    itemlist = {
        "@type": "ItemList",
        "name": "Visa document guides by destination",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": v["h1"], "url": abs_url("visa/" + v["slug"])}
            for i, v in enumerate(VISAS, 1)
        ],
    }
    add_page("visa", "Visa Guides | Flight & Hotel Document Requirements by Country",
             "Flight reservation and hotel booking requirements for Schengen, US, UK, Canada, UAE, Japan, Australia and more. What each consulate accepts, and the traps that get files returned.",
             body, schema=[c_schema, itemlist], priority="0.8", changefreq="weekly")


def _strip(html):
    import re
    return re.sub(r"<[^>]+>", "", html)


def _page(v):
    c_html, c_schema = crumbs([("Visa guides", "visa"), (v["label"], None)])
    dep, arr = v["route"]

    reqs = "".join("<li>%s</li>" % r for r in v["requirements"])
    traps = ""
    for t, d in v["traps"]:
        traps += '<div class="card"><h3>%s</h3><p>%s</p></div>' % (t, d)

    others = "".join('<li><a href="%s">%s</a></li>' % (url("visa/" + o["slug"]), o["label"])
                     for o in VISAS if o["slug"] != v["slug"])

    pass_art = content_core.BOARDING_PASS.replace(">DEL<", ">%s<" % dep).replace(">CDG<", ">%s<" % arr)

    body = """
<section>
  <div class="wrap">
    %s
    <div class="hero__grid" style="align-items:flex-start">
      <div>
        <p class="eyebrow">%s &middot; from %s per traveller</p>
        <h1>%s</h1>
        <p class="lede">%s</p>
        <div class="btn-row" style="margin-top:1.6rem">
          <a class="btn btn--primary btn--lg" href="%s">Order flight reservation at %s</a>
          <a class="btn btn--ghost btn--lg" href="%s">Flight + hotel at %s</a>
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
    <h2>What the application actually requires</h2>
    <ul>%s</ul>
    <div class="note">
      <strong>On unpaid reservations</strong>
      %s
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Four ways this application goes wrong</h2>
    <p class="lede">None of these are exotic. All of them are avoidable in the ten minutes before you submit.</p>
    <div class="grid g2" style="margin-top:1.8rem">%s</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem">
      <h2>Documents for your %s application</h2>
      <p class="lede">Delivered in %s, verifiable before you submit.</p>
    </div>
    %s
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    %s
  </div>
</section>

<section class="band tight">
  <div class="wrap">
    <h2>Other destinations</h2>
    <ul class="pills" style="margin-top:1.2rem">%s</ul>
    <p style="margin-top:1.4rem;font-size:.94rem">Background reading:
      <a href="%s">what a dummy ticket actually is</a> &middot;
      <a href="%s">is it legal?</a> &middot;
      <a href="%s">how to verify a PNR</a></p>
  </div>
</section>

%s
""" % (c_html, v["short"], money(PRICE_FLIGHT), v["h1"], v["blurb"],
       url("order"), money(PRICE_FLIGHT), url("flight-and-hotel-package"), money(PRICE_BOTH),
       content_core.TRUSTLINE, pass_art, stat_bar(),
       trust_cards(heading=None),
       reqs, v["official"], traps,
       v["short"], DELIVERY, pricing_tickets(),
       faq_block(v["faqs"], "%s visa: flight and hotel questions" % v["short"]),
       others,
       url("blog/what-is-a-dummy-ticket"), url("blog/is-a-dummy-ticket-legal"), url("verify-pnr"),
       cta_band("Documents for your %s application" % v["short"],
                "Verifiable flight reservation from %s, or the flight + hotel pack for %s." % (money(PRICE_FLIGHT), money(PRICE_BOTH))))

    webpage = {
        "@type": "WebPage",
        "@id": abs_url("visa/" + v["slug"]) + "#webpage",
        "url": abs_url("visa/" + v["slug"]),
        "name": v["h1"],
        "description": v["desc"],
        "isPartOf": {"@id": SITE_URL + "/#website"},
        "about": {"@type": "Thing", "name": v["label"]},
        "datePublished": TODAY,
        "dateModified": TODAY,
    }

    add_page("visa/" + v["slug"], v["title"], v["desc"], body,
             schema=[c_schema, webpage, faq_schema(v["faqs"])],
             priority="0.8", changefreq="monthly")
