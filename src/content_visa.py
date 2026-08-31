# -*- coding: utf-8 -*-
"""Visa / destination landing pages - the long-tail SEO engine."""

import re

from build import (ICON, BRAND, DELIVERY, SITE_URL, TODAY, doodles,
                   PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH,
                   money, add_page, url, abs_url, faq_block, faq_schema,
                   crumbs, cta_band, pricing_tickets,
                   stat_bar, trust_cards, airline_strip)
import content_core
from visa_extra import EXTRA


# --------------------------------------------------------------------------
# Data. Each entry drives one landing page.
#   slug, nav label, H1 subject, route example, and the country-specific facts.
# --------------------------------------------------------------------------
VISAS = [
    dict(
        slug="schengen-visa-flight-reservation",
        status='visa_required',
        status_note='Full application, biometrics, 15 to 45 days',
        tips=['Apply to the country you sleep the most nights in, not the one you land in. Officers check this and it is the commonest reason a Schengen file is rejected outright.',
 'Book appointment slots the moment they open. Delhi and Mumbai summer slots vanish within hours and agents hoard them.',
 'Carry printouts of everything even after uploading. VFS staff routinely ask for paper.',
 'Your first Schengen visa is usually issued for exactly your travel dates. Later ones get longer validity, so build a history with a short trip first.'],
        official_src=('European Commission visa policy', 'https://home-affairs.ec.europa.eu/policies/schengen-borders-and-visa/visa-policy_en'),
        fees=[('Adult applicant', '&euro;90', 'Up from &euro;80 in June 2026'),
 ('Child aged 6 to 11', '&euro;45', ''),
 ('Child under 6', 'Free', ''),
 ('VFS or TLScontact service fee', '&euro;20 to &euro;40 equivalent', 'Charged on top, varies by country and centre'),
 ('Travel medical insurance', 'From about &euro;20', '&euro;30,000 minimum cover is mandatory')],
        steps=[('Work out which consulate is yours', 'Whichever country you sleep the most nights in. Equal split? Apply where you land first. Get this wrong and the file bounces before anyone reads it.'),
 ('Book the appointment early',
  'Slots in Delhi, Mumbai and Bengaluru vanish weeks out over summer. Book the slot first and gather papers second. Almost everyone does it the other way round and regrets it.'),
 ('Fill in the application form', 'Online for most missions, printed and signed for the rest. Names exactly as the passport prints them, surname first.'),
 ('Get the documents together', 'Passport, photos to spec, bank statements, employment letter, insurance, accommodation for every night, and the flight itinerary.'),
 ('Order the flight reservation last', 'A day or two before the appointment, so the PNR is live when the officer opens your file rather than lapsed.'),
 ('Attend and give biometrics', 'Fingerprints and a photo, valid for 59 months. If you gave them recently for another Schengen visa you may be able to skip this.'),
 ('Wait', '15 calendar days is the norm. It stretches to 45 in peak season or if your file goes for consultation. Do not buy the fare yet.')],
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
        status='visa_required',
        status_note='DS-160, interview, 214(b) test',
        tips=['Interview slots move. Check the portal daily for the first week after paying, cancellations open up constantly.',
 'Answer in short sentences and stop. Officers decide in under three minutes and volunteering extra detail rarely helps.',
 'Take documents but do not push them across the counter. They will ask if they want them.',
 'A refusal under 214(b) is not a ban. You can reapply immediately, but only reapply once something material about your situation has changed.'],
        official_src=('US Department of State', 'https://travel.state.gov/content/travel/en/us-visas/tourism-visit/visitor.html'),
        fees=[('MRV application fee, B1/B2', 'US$185', 'Non-refundable, paid before you can book an interview'),
 ('Visa Integrity Fee', 'US$250', 'Signed into law in 2025; confirm whether it applies to your appointment date'),
 ('Issuance or reciprocity fee', 'Varies', 'Depends on nationality; many applicants pay nothing')],
        steps=[('Complete the DS-160', 'The long one. It asks for your intended arrival date and US address, which is exactly where an itinerary and hotel booking earn their keep. Save the confirmation barcode.'),
 ('Pay the MRV fee', 'Keep the receipt number safe. No receipt, no interview slot.'),
 ('Book two appointments', 'Biometrics at the visa application centre, then the consular interview. In India these are separate visits on separate days.'),
 ('Prepare for the questions you will actually get', 'Nobody is going to admire your itinerary. They will ask what you do, who is paying, and why you will come back. Short, true answers.'),
 ('Order the flight itinerary', "A day or two before the interview, matching the DS-160 dates exactly. A contradiction on the officer's screen is a question you did not need to invite."),
 ('Attend the interview', 'Usually over in under three minutes. Take the DS-160 confirmation, appointment letter, passport and your supporting file.'),
 ('Wait for the passport', 'Most decisions are given at the counter, then the passport is couriered back. Administrative processing can add weeks and no reason is given.')],
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
        status='visa_required',
        status_note='Online application, biometrics, about 3 weeks',
        tips=['Upload proper PDFs, not phone photos. Caseworkers see thousands and a bad scan reads as a weak application.',
 'The priority service is worth it if your dates are tight, but it only speeds the decision, not the biometrics appointment.',
 'A refused UK visa must be declared on every future application anywhere, so do not submit a thin file to test the water.',
 'Bank statements should be stamped by the bank. Downloaded PDFs without a stamp get queried.'],
        official_src=('GOV.UK Standard Visitor', 'https://www.gov.uk/standard-visitor'),
        fees=[('Standard Visitor, up to 6 months', '&pound;135', 'Rose from &pound;127 in April 2026'),
 ('Long-term, 2 years', '&pound;475', ''),
 ('Long-term, 5 years', '&pound;848', ''),
 ('Long-term, 10 years', '&pound;1,059', ''),
 ('Priority service', 'From &pound;500', 'Optional, cuts the decision to about 5 working days')],
        steps=[('Apply on GOV.UK', 'The official form is free to fill in. Plenty of agent sites charge you to type the same answers into the same form.'),
 ('Pay and book biometrics', 'You will be sent to a VFS or TLScontact centre for fingerprints and a photo.'),
 ('Upload clean evidence', 'Proper PDFs. A phone photo of a bank statement lying on a kitchen table reads as careless, and caseworkers see thousands of them.'),
 ('Show you will leave', 'This is the whole test. Job, business, studies, family, property, and a dated return booking.'),
 ('Order the flight reservation', 'Just before you submit, so it is live when the caseworker opens the file.'),
 ('Attend the appointment', 'Passport and the printed confirmation.'),
 ('Wait about three weeks', 'On standard service. Do not book the fare until the decision lands. UKVI advises this itself.')],
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
        status='visa_required',
        status_note='Online application, biometrics, weeks to months',
        tips=['Biometrics are valid for ten years and reused across applications, so the second Canadian visa is faster than the first.',
 'Processing times published by IRCC are averages, not promises. Apply three months out if you have fixed dates.',
 'A strong purpose-of-travel letter does more work here than in most applications. Be specific about who, where and why.',
 'If you hold a valid US visa you may qualify for eTA rather than a full TRV on some routes. Check before applying.'],
        official_src=('IRCC visitor visa', 'https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/visitor-visa.html'),
        fees=[('Visitor visa, TRV', 'CAD$100', 'Single or multiple entry, same price'),
 ('Biometrics', 'CAD$85', 'CAD$170 cap for a family applying together'),
 ('Medical exam', 'CAD$100 to CAD$300', 'Only when requested, usually for longer stays')],
        steps=[('Create an IRCC secure account', 'Everything runs through the online portal.'),
 ('Answer the eligibility questions', 'The portal builds your personal document checklist from your answers, so the checklist is only as correct as they are.'),
 ('Upload the documents', 'Purpose of travel letter, funds, ties, and the travel plan. The letter and the itinerary have to agree on dates.'),
 ('Pay and give biometrics', 'Book the collection appointment promptly. This is the step where timelines quietly slip.'),
 ('Order the flight itinerary late', 'Canadian processing is unpredictable and a hold window is short, so there is nothing to gain by ordering early.'),
 ('Watch the portal', 'Weeks to months depending on your country. IRCC may ask for more documents and the clock does not stop while you find them.'),
 ('Send the passport for stamping', 'Once approved you post the passport in. Only now is it sensible to buy the fare.')],
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
        status='evisa',
        status_note='e-visa via airline, hotel or agent, 30 to 60 days',
        tips=['Emirates and flydubai sponsor visas for their own passengers, often cheaper than a standalone agent.',
 'Nol card for the metro, bought at any station. Dubai taxis are fine but the Red Line beats traffic to the airport.',
 'Ramadan changes everything: shorter hours, no eating in public during daylight, but spectacular nights. Check the dates.',
 'Overstay fines accrue daily and are collected at the airport before you fly. There is no appeal at the counter.'],
        official_src=('UAE government portal', 'https://u.ae/en/information-and-services/visa-and-emirates-id'),
        fees=[('30-day tourist visa', 'About AED 350', 'Varies by sponsor; airlines and hotels price differently'),
 ('60-day tourist visa', 'About AED 650', ''),
 ('Extension', 'About AED 600', 'Per 30 days, applied for before the current one expires'),
 ('Overstay fine', 'AED 50 per day', 'Collected at departure. There is no negotiating it')],
        steps=[('Check whether you need one at all', 'A long list of nationalities gets a visa on arrival. Check before you pay anybody.'),
 ('Pick a sponsor', 'An airline, a hotel, or a licensed agent. Emirates and flydubai sponsor visas for their own passengers.'),
 ('Send a passport scan and photo', 'Passport valid at least six months, photo to spec on a white background.'),
 ('Wait two to four working days', 'Quicker than most places. The e-visa arrives by email.'),
 ('Have onward travel ready', 'Checked at check-in and again at immigration. This one is enforced properly, not occasionally.'),
 ('Carry accommodation details', "Hotel booking or the host's address. You will be asked at the counter."),
 ('Watch the expiry date', 'Fines accrue daily and are collected before they let you fly out.')],
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
             "<p>Within %s. UAE trips are often booked at short notice, so tell us if you are travelling the same day.</p>" % DELIVERY),
        ],
    ),
    dict(
        slug="australia-visa-flight-reservation",
        status='visa_required',
        status_note='Subclass 600, online, weeks to months',
        tips=['Domestic distances are enormous. Sydney to Perth is five hours flying, further than Delhi to Dubai.',
 'Declare all food, plant and wood items on the incoming card. Biosecurity fines are immediate and steep, and declaring costs nothing.',
 'The subclass 600 often grants multiple entry over 12 months. Read the grant notice, it is worth more than people realise.',
 'If your passport qualifies for an ETA, use it. Twenty dollars against two hundred and fifty.'],
        official_src=('Department of Home Affairs', 'https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/visitor-600'),
        fees=[('Visitor visa, subclass 600', 'From AUD$250', 'Increased in July 2026'),
 ('ETA, subclass 601', 'AUD$20', 'Eligible passports only, applied for in the app'),
 ('eVisitor, subclass 651', 'Free', 'Most EU passports'),
 ('Health examination', 'AUD$300 to AUD$500', 'Only when requested')],
        steps=[('Check whether an ETA covers you', 'If your passport qualifies, it costs twenty dollars and takes minutes. Do not pay for a subclass 600 you do not need.'),
 ('Create an ImmiAccount', 'The subclass 600 is lodged online.'),
 ('Prove genuine temporary entry', 'This is the test that decides it. Funds, ties, a coherent plan, and a reason to come home.'),
 ('Upload the documents', 'Bank statements, employment or study evidence, an invitation letter if you have one, and the travel plan.'),
 ('Order the flight reservation', 'Home Affairs advises against booking real travel before the grant, which is precisely what a reservation is for.'),
 ('Do health checks if asked', 'This can add weeks. Leave slack in your dates.'),
 ('Read the grant notice properly', 'Check entries allowed and stay period before planning a side trip to New Zealand.')],
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
        status='visa_required',
        status_note='Via accredited agency, about 5 working days',
        tips=['Buy the JR Pass before you arrive if you are covering long distances; it must be bought outside Japan for the best price.',
 'Get a Suica or Pasmo card at the airport for local trains, buses and konbini. Cash is still king in small restaurants.',
 'Cherry blossom dates move by a week or two each year and hotels price accordingly. Book flexible if you are chasing them.',
 'Vegetarian is genuinely hard: dashi fish stock is in almost everything. Learn the phrase, or use Happy Cow.'],
        official_src=('Ministry of Foreign Affairs of Japan', 'https://www.mofa.go.jp/j_info/visit/visa/index.html'),
        fees=[('Single-entry visa', 'Revised in 2026', 'Japan raised visa fees during 2026. Confirm the current figure with your own mission before paying'),
 ('Multiple-entry visa', 'Revised in 2026', 'As above'),
 ('Agency handling fee', 'Varies', 'Many countries require you to apply through an accredited agency, which charges its own fee on top')],
        steps=[('Check whether you need a visa', 'Plenty of passports are exempt for 90 days.'),
 ('Find your accredited agency', 'In India and several other countries you cannot walk up to the consulate. Applications go through accredited travel agencies.'),
 ('Build the Schedule of Stay', 'Day by day: date, city, hotel name, hotel phone number. This is the document Japan genuinely cares about and the one people get wrong.'),
 ('Make the bookings match the schedule', 'Kyoto on day four means a Kyoto booking for that night. Officers do the arithmetic, every time.'),
 ('Prepare financial evidence', 'Usually six months of bank statements plus employment proof.'),
 ('Order flights and hotels together', 'So the dates reconcile with the schedule without you fixing anything by hand afterwards.'),
 ('Submit and wait about a week', 'Often five working days once the agency lodges it. Visas usually carry a three-month entry window, so applying six months early wastes it.')],
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
        status='evisa',
        status_note='e-visa online, minutes to hours',
        tips=['Istanbul has two airports far apart. Check whether you are flying into IST or SAW before booking a hotel.',
 'The Istanbul Card works on trams, ferries, buses and the metro, and the Bosphorus ferry is the best value sightseeing anywhere.',
 'Cappadocia balloons are cancelled often for wind. Give yourself three mornings there, not one.',
 'Bargaining is expected in the Grand Bazaar and nowhere else. Fixed prices in ordinary shops are fixed.'],
        official_src=('Republic of Turkiye e-Visa', 'https://www.evisa.gov.tr/en/'),
        fees=[('e-Visa', 'US$20 to US$60', 'Depends on nationality. Some passports pay nothing'), ('Sticker visa at a consulate', 'Varies', 'For nationalities not eligible for the e-Visa')],
        steps=[('Check e-Visa eligibility on evisa.gov.tr', 'That is the official site. Look-alike sites charge a markup for the identical thing.'),
 ('Check passport validity', 'Turkey wants at least 150 days from entry for most e-Visa nationalities. Stricter than the usual six months, and regularly missed.'),
 ('Apply online', 'Ten minutes. The visa lands by email, often within the hour.'),
 ('Print it', 'Do not stake your holiday on airport wifi and a phone at five in the morning.'),
 ('Have onward travel ready', 'Airline staff check this at check-in in your departure city, before Turkey gets any say in it.'),
 ('Carry accommodation details', 'Immigration can and does ask where you are staying.'),
 ('Keep the e-Visa with the passport', 'You will be asked for it again on the way out.')],
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
        status='visa_free',
        status_note='60 days visa free for Indians',
        tips=['Thailand made visa-free entry for Indians permanent at 60 days. You still need proof of onward travel, and airlines check it in India.',
 'Grab and Bolt work in Bangkok and are cheaper than metered taxis from the airport, which often refuse the meter.',
 'The BTS and MRT do not accept notes at some machines. Keep coins or buy a Rabbit card.',
 'Songkran in mid-April shuts the country for a week of water fights. Either plan for it or avoid it entirely.'],
        official_src=('Thai e-Visa portal', 'https://www.thaievisa.go.th/'),
        fees=[('Tourist visa, single entry', 'About THB 2,000', 'Roughly US$55, varies a little by embassy'),
 ('Visa exemption', 'Free', 'Most Western passports, 30 or 60 days depending on nationality'),
 ('Extension at an immigration office', 'THB 1,900', 'One extension, typically 30 days')],
        steps=[('Check whether you need a visa at all', 'Many nationalities enter free under the exemption scheme. Do not buy something you do not need.'),
 ('If you do need one, use the official e-Visa portal', 'thaievisa.go.th. Agent sites charge a fee to type the same form for you.'),
 ('Sort proof of onward travel first', 'This is where Thailand catches people, and it happens at the check-in desk in your home city, not in Bangkok.'),
 ('Check the onward date against your permitted stay', 'A 45-day onward flight on a 30-day exemption defeats the point, and staff do notice.'),
 ('Have funds evidence to hand', '10,000 THB per person officially. Spot-checked rather than always checked.'),
 ('Fill in the arrival card', 'It wants your accommodation address.'),
 ('Extend locally if you stay longer', '1,900 THB at an immigration office. Straightforward.')],
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
        status='visa_required',
        status_note='C-3 visa, or K-ETA for waiver nationals',
        tips=['T-money card from any convenience store covers subway, bus and taxis nationwide.',
 'Korean immigration weighs bank statements heavily. A steady balance across six months beats a large recent deposit.',
 'Naver Map and KakaoMap work; Google Maps barely does in Korea because of mapping restrictions.',
 'Most museums close Mondays and many palaces close Tuesdays. Check before building an itinerary around them.'],
        official_src=('Korea Visa Portal', 'https://www.visa.go.kr/'),
        fees=[('C-3 short-term visit, single entry', 'US$40', ''), ('C-3 multiple entry', 'US$90', ''), ('K-ETA', 'KRW 10,000', 'Visa-waiver nationalities, applied for before travel')],
        steps=[('Work out whether you need a visa or a K-ETA', 'Two different lists, and they change. Check before preparing anything else.'),
 ('Apply through the Korea Visa Portal or your consulate', 'Some missions insist on an accredited agency.'),
 ('Get the financial evidence right', 'Korean consulates weigh this heavily. A steady balance across months beats a large deposit that appeared last week.'),
 ('Prepare accommodation and itinerary', 'Round trip with fixed dates, and somewhere to stay for the whole visit.'),
 ('Order the flight itinerary near submission', 'Not weeks ahead.'),
 ('Submit and wait a week or two', 'Usually quick, but it varies by mission and season.'),
 ('Or apply for the K-ETA', 'At least 72 hours before departure, on the official site only.')],
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
        status='visa_required',
        status_note='e-visa via authorised agent, SG Arrival Card for all',
        tips=['The SG Arrival Card is separate from the visa and required for everyone, submitted within three days of arrival.',
 'Changi is worth arriving early for. Jewel, the canopy park and the free cinema are all landside.',
 'Chewing gum import is genuinely restricted and littering fines are enforced. This is not a myth.',
 'Hawker centres are the good food and cost a fraction of restaurants. Look for the queue of locals, not the sign.'],
        official_src=('ICA Singapore', 'https://www.ica.gov.sg/enter-transit-depart/entering-singapore'),
        fees=[('Entry visa', 'SGD$30', 'Only for nationalities that require one'),
 ('SG Arrival Card', 'Free', 'Mandatory for everyone, submitted online'),
 ('Agent processing fee', 'SGD$30 to SGD$50', 'If you lodge through an authorised agent')],
        steps=[('Check whether your passport needs a visa', 'Most do not. The Arrival Card, however, applies to everyone.'),
 ('If you need one, go through an authorised agent or sponsor', 'Singapore does not take direct applications from most individuals.'),
 ('Submit the SG Arrival Card', 'Within three days before you land. It asks for your accommodation address.'),
 ('Have onward travel ready', 'Declared on the Arrival Card and checked at Changi.'),
 ('Check passport validity', 'Six months minimum. No exceptions are made.'),
 ('Carry funds evidence', 'Rarely asked for. Occasionally decisive.'),
 ('Expect a stay length, not a guarantee', "How long you get is at the officer's discretion. Thirty days is common, not promised.")],
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
        status='visa_required',
        status_note='Visitor visa, or NZeTA for waiver nationals',
        tips=['The NZeTA takes up to 72 hours, so request it before you book anything non-refundable.',
 'Biosecurity is the strictest anywhere. Boots, tents and anything with soil on it must be declared and will be inspected.',
 'Distances look small and take twice as long as the map suggests. South Island roads are winding and beautiful and slow.',
 'The International Visitor Levy is charged on top of the NZeTA and catches people out at the payment screen.'],
        official_src=('Immigration New Zealand', 'https://www.immigration.govt.nz/new-zealand-visas/visas/visa/visitor-visa'),
        fees=[('Visitor visa', 'NZD$341', 'For nationalities that require a visa'),
 ('NZeTA', 'NZD$17 to NZD$23', 'Visa-waiver nationalities. Cheaper in the app than on the website'),
 ('International Visitor Levy', 'NZD$100', 'Charged alongside the NZeTA or visa')],
        steps=[('Work out which route applies', 'Visa-waiver passports need an NZeTA, not a visa. Everyone else applies for a visitor visa.'),
 ('Request the NZeTA early', 'It can take up to 72 hours. Use the app, it is cheaper than the website.'),
 ('Budget for the levy', 'NZD$100 on top, and it catches people out.'),
 ('Prove funds, or prepay accommodation', 'NZD$1,000 per month of stay, or NZD$400 if accommodation is already paid for. Prepaying lowers the bar.'),
 ('Sort onward travel', 'You must hold an onward ticket or show you could buy one. A booking is far quicker to produce at a check-in desk than a pile of bank statements.'),
 ('Apply online and upload evidence', 'Through the Immigration New Zealand portal.'),
 ('Wait for the decision, then buy the fare', 'In that order.')],
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

VISAS += EXTRA


# --------------------------------------------------------------------------
def link_list():
    """(label, slug, status) so the footer can lead with visa-free ones."""
    return [(v["label"], v["slug"], v["status"]) for v in VISAS]


def build():
    _index()
    for v in VISAS:
        _page(v)


STATUS = {
    "visa_free":     ("Visa free", "vf", "No visa to apply for"),
    "voa":           ("Visa on arrival", "voa", "Issued when you land"),
    "evisa":         ("e-Visa", "ev", "Apply online before you fly"),
    "visa_required": ("Visa required", "vr", "Full application before travel"),
}


def _badge(v, big=False):
    label, cls, _ = STATUS[v["status"]]
    return ('<span class="vstat vstat--%s%s">%s<b>%s</b>%s</span>'
            % (cls, " vstat--lg" if big else "",
               ICON["check"] if v["status"] == "visa_free" else "",
               label, ('<small>%s</small>' % v["status_note"]) if big else ""))


def _tips_html(v):
    items = "".join('<li>%s</li>' % t for t in v["tips"])
    return ('<div class="tips"><h2>Worth knowing before you go</h2>'
            '<ul class="tips__list">%s</ul></div>' % items)


def _index():
    c_html, c_schema = crumbs([("Visa guides", None)])

    ORDER = [("visa_free", "Visa free for Indians",
              "Nothing to apply for. Turn up with the right paperwork and you are in."),
             ("voa", "Visa on arrival",
              "Issued at the airport, but only if you meet the conditions."),
             ("evisa", "e-Visa, applied for online",
              "No embassy visit. Usually decided in a few days."),
             ("visa_required", "Full visa application",
              "Appointment, documents, and a wait. Plan these first.")]

    groups = ""
    for status, heading, blurb in ORDER:
        rows = [v for v in VISAS if v["status"] == status]
        if not rows:
            continue
        cards = ""
        for v in sorted(rows, key=lambda x: x["short"]):
            cards += """
<a class="card card--link vcard" href="%s">
  <div class="vcard__hd"><span class="vcard__c">%s</span>%s</div>
  <p>%s</p>
  <span class="more">Requirements and fees &rarr;</span>
</a>""" % (url("visa/" + v["slug"]), v["short"], _badge(v),
           _strip(v["blurb"])[:118].rsplit(" ", 1)[0] + "&hellip;")
        groups += """
<section class="%s">
  <div class="wrap">
    <div class="center" style="margin-bottom:2rem">
      <h2>%s</h2><p class="lede">%s</p>
    </div>
    <div class="grid g3">%s</div>
  </div>
</section>""" % ("band" if status in ("voa", "visa_required") else "", heading, blurb, cards)

    free = sum(1 for v in VISAS if v["status"] in ("visa_free", "voa"))
    body = """
<section class="tight">
  <div class="wrap">
    %s
    <div class="center">
      <h1>Visa guides for Indian travellers</h1>
      <p class="lede">%d destinations, sorted by what your passport actually needs. %d of them let an Indian
      passport in without applying for anything in advance. For the rest: the steps, the fees and the traps.</p>
      %s
    </div>
  </div>
</section>
%s
%s""" % (c_html, len(VISAS), free,
         doodles("globe", "passport", "map", "suitcase", "compass", "palm"),
         groups, cta_band())

    itemlist = {
        "@type": "ItemList",
        "name": "Visa guides for Indian passport holders",
        "numberOfItems": len(VISAS),
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": v["h1"], "url": abs_url("visa/" + v["slug"])}
            for i, v in enumerate(VISAS, 1)
        ],
    }
    add_page("visa", "Visa Guides for Indians | %d Countries, Fees & Rules 2026" % len(VISAS),
             "Visa requirements for Indian passport holders across %d destinations. Which are visa free, "
             "which need an e-visa, what each costs, and the step-by-step process." % len(VISAS),
             body, schema=[c_schema, itemlist], priority="0.9", changefreq="weekly")


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
        %s
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

<section>
  <div class="wrap wrap--narrow">
    <h2 id="how-to-apply">How to apply, step by step</h2>
    <p class="lede">The order matters more than people expect. Do these out of sequence and you end up
    with a lapsed booking or an appointment you cannot fill.</p>
    %s
  </div>
</section>

<section class="band">
  <div class="wrap wrap--narrow">
    <h2 id="fees">What it costs</h2>
    %s
  </div>
</section>

<section>
  <div class="wrap wrap--narrow">
    <h2>What the application actually requires</h2>
    <ul>%s</ul>
    <div class="note">
      <strong>On unpaid reservations</strong>
      %s
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Four ways this application goes wrong</h2>
    <p class="lede">None of these are exotic. Every one of them is fixable in the ten minutes before you hit submit.</p>
    <div class="grid g2" style="margin-top:1.8rem">%s</div>
  </div>
</section>

<section>
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

<section class="band">
  <div class="wrap wrap--narrow">
    %s
  </div>
</section>

<section class="tight">
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
""" % (c_html, v["short"], money(PRICE_FLIGHT), _badge(v, big=True), v["h1"], v["blurb"],
       url("order"), money(PRICE_FLIGHT), url("flight-and-hotel-package"), money(PRICE_BOTH),
       content_core.TRUSTLINE, pass_art, stat_bar(),
       trust_cards(heading=None),
       _steps_html(v), _fees_html(v),
       reqs, v["official"], traps,
       v["short"], DELIVERY, pricing_tickets(),
       faq_block(v["faqs"], "%s: your questions" % v["short"]),
       _tips_html(v),
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
             schema=[c_schema, webpage, _howto_schema(v), faq_schema(v["faqs"])],
             priority="0.8", changefreq="monthly")


def _steps_html(v):
    rows = ""
    for i, (title, detail) in enumerate(v["steps"], 1):
        rows += ("""
<li class="vstep">
  <span class="vstep__n">%d</span>
  <div><h3>%s</h3><p>%s</p></div>
</li>""" % (i, title, detail))
    return '<ol class="vsteps">%s</ol>' % rows


def _fees_html(v):
    label, href = v["official_src"]
    rows = ""
    for item, amount, note in v["fees"]:
        rows += ("<tr><td><b>%s</b>%s</td><td class=\"vfee\">%s</td></tr>"
                 % (item, ("<small>%s</small>" % note) if note else "", amount))
    return """
<div class="tbl-wrap">
  <table class="fees">
    <thead><tr><th>What you pay</th><th>How much</th></tr></thead>
    <tbody>%s</tbody>
  </table>
</div>
<p class="fee-note">Checked %s. Government fees move, sometimes with a month&rsquo;s notice and sometimes
with none. Treat this as a planning figure and confirm the number you will actually be charged at
<a href="%s" rel="nofollow noopener" target="_blank">%s</a> before you pay.</p>""" % (rows, TODAY, href, label)


def _howto_schema(v):
    return {
        "@type": "HowTo",
        "name": "How to apply for a %s" % v["label"].lower(),
        "description": "Step by step: the order to do things in when applying for a %s." % v["label"].lower(),
        "step": [{"@type": "HowToStep", "position": i, "name": t,
                  "text": re.sub(r"<[^>]+>", "", d)}
                 for i, (t, d) in enumerate(v["steps"], 1)],
    }
