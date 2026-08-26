# -*- coding: utf-8 -*-
"""
Static site generator for visaflightticket.com

Run:  python src/build.py
Emits plain HTML into the repo root so the site can be served by GitHub Pages,
Netlify, Vercel, Cloudflare Pages or any static host with zero build step.
"""

import json
import os
import re
import shutil
from datetime import date

# --------------------------------------------------------------------------
# CONFIG  -- change these three lines when the real domain / contacts are live
# --------------------------------------------------------------------------
SITE_URL = "https://visaflightticket.com"
BASE_PATH = ""            # set to "/reponame" only if hosting on a GitHub *project* page
BRAND = "Visa Flight Ticket"
TAGLINE = "Verifiable flight reservations & hotel bookings for visa applications"

EMAIL = "support@visaflightticket.com"
WHATSAPP = "+10000000000"           # TODO: replace with the real WhatsApp number
WHATSAPP_DISPLAY = "Chat on WhatsApp"
TWITTER = "@visaflightticket"

PRICE_FLIGHT = 9
PRICE_HOTEL = 7
PRICE_BOTH = 14
PRICE_RUSH = 5
DELIVERY = "30-60 minutes"

# --------------------------------------------------------------------------
# TRUST / CREDENTIALS
# Every value below is published as a factual claim on the live site.
# Only fill these in with figures you can substantiate if challenged --
# IATA accreditation in particular is verifiable against IATA's own register,
# and unverifiable stats are a Google trust-signal and consumer-law liability.
# Set any value to "" (empty string) to hide that claim site-wide.
# --------------------------------------------------------------------------
SINCE_YEAR = "2017"          # "" hides the "Since ..." claim
FLIGHTS_BOOKED = "10 lakh+"  # "" hides the flights-booked stat
VISAS_HELPED = "50,000+"     # "" hides the successful-visas stat
IATA_ACCREDITED = True       # False removes the IATA badge everywhere
IATA_NUMBER = ""             # your IATA / TIDS code, e.g. "96-1 2345 6" - shown on the badge
AIRLINE_COUNT = "100+"

# Carriers we book on. Names only -- drop logo SVGs into assets/img/airlines/
# and extend airline_strip() if you have licence to display the marks.
AIRLINES = [
    "Emirates", "Qatar Airways", "Turkish Airlines", "Lufthansa", "Air France",
    "KLM", "British Airways", "SWISS", "LOT Polish Airlines", "Vietnam Airlines",
    "Japan Airlines", "American Airlines", "AirAsia", "Singapore Airlines",
    "Etihad Airways", "Air India", "IndiGo", "Thai Airways", "Cathay Pacific", "ANA",
]

TODAY = date.today().isoformat()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = []          # populated by add_page(); consumed by the sitemap writer


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def url(path=""):
    """Root-relative URL for an internal path."""
    path = path.strip("/")
    if not path:
        return BASE_PATH + "/"
    return BASE_PATH + "/" + path + "/"


def asset(path):
    return BASE_PATH + "/" + path.lstrip("/")


def abs_url(path=""):
    return SITE_URL + url(path)


def _prune(obj):
    """Drop None values so optional schema fields disappear cleanly."""
    if isinstance(obj, dict):
        return {k: _prune(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [_prune(v) for v in obj if v is not None]
    return obj


def jsonld(*objects):
    graph = [_prune(o) for o in objects if o]
    if not graph:
        return ""
    data = {"@context": "https://schema.org", "@graph": graph}
    dumped = json.dumps(data, ensure_ascii=False, indent=None, separators=(",", ":"))
    dumped = dumped.replace("</", "<\\/")
    return '<script type="application/ld+json">%s</script>' % dumped


def slugify(text):
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")


# --------------------------------------------------------------------------
# inline icons
# --------------------------------------------------------------------------
def _svg(body, extra=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (extra, body))


ICON = {
    "plane": _svg('<path d="M17.8 19.2 16 11l3.5-3.5a2.1 2.1 0 0 0-3-3L13 8 4.8 6.2a.5.5 0 0 0-.5.8l3.2 3.2-2 2-1.8-.4a.5.5 0 0 0-.5.8L5 14.5l1.9 1.8a.5.5 0 0 0 .8-.5l-.4-1.8 2-2 3.2 3.2a.5.5 0 0 0 .8-.5Z"/>'),
    "bed": _svg('<path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 17h20"/><circle cx="7" cy="12" r="2"/>'),
    "shield": _svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>'),
    "clock": _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "check": _svg('<path d="M20 6 9 17l-5-5"/>'),
    "search": _svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
    "globe": _svg('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18Z"/>'),
    "wallet": _svg('<path d="M3 7a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M16 12h3"/>'),
    "doc": _svg('<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h4"/>'),
    "refresh": _svg('<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 4v5h-5"/>'),
    "mail": _svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    "chat": _svg('<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12Z"/>'),
    "sun": _svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    "burger": _svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "users": _svg('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/>'),
    "lock": _svg('<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>'),
    "seal": _svg('<path d="m12 2 2.4 1.8 3-.2.9 2.9 2.4 1.8-1.1 2.8 1.1 2.8-2.4 1.8-.9 2.9-3-.2L12 20l-2.4-1.8-3 .2-.9-2.9L3.3 13.7 4.4 11 3.3 8.2l2.4-1.8.9-2.9 3 .2Z"/><path d="m9 11.5 2 2 4-4"/>'),
    "award": _svg('<circle cx="12" cy="9" r="6"/><path d="m8.2 13.8-1.4 7.4 5.2-2.8 5.2 2.8-1.4-7.4"/>'),
}

LOGO_SVG = (
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">'
    '<rect x="1" y="6" width="30" height="20" rx="4" fill="currentColor" opacity=".1"/>'
    '<rect x="1.6" y="6.6" width="28.8" height="18.8" rx="3.4" stroke="currentColor" stroke-opacity=".28" stroke-width="1.2"/>'
    '<path d="M21 6.5v19" stroke="currentColor" stroke-opacity=".45" stroke-width="1.2" stroke-dasharray="2.4 2.4"/>'
    '<path d="M17.4 20.6 16 14.5l2.6-2.6a1.55 1.55 0 0 0-2.2-2.2l-2.6 2.6-6.1-1.4a.37.37 0 0 0-.36.6l2.36 2.36-1.48 1.48-1.33-.3a.37.37 0 0 0-.37.6l1.06 1.06 1.06 1.06a.37.37 0 0 0 .6-.37l-.3-1.33 1.48-1.48 2.36 2.36a.37.37 0 0 0 .6-.37Z" fill="#b4531f"/>'
    '<circle cx="25.6" cy="12.5" r="1.1" fill="currentColor" opacity=".3"/>'
    '<circle cx="25.6" cy="16" r="1.1" fill="currentColor" opacity=".3"/>'
    '<circle cx="25.6" cy="19.5" r="1.1" fill="currentColor" opacity=".3"/>'
    '</svg>'
)


# --------------------------------------------------------------------------
# navigation
# --------------------------------------------------------------------------
NAV = [
    ("Flight Ticket", "flight-reservation-for-visa"),
    ("Hotel Booking", "hotel-booking-for-visa"),
    ("Flight + Hotel", "flight-and-hotel-package"),
    ("Pricing", "pricing"),
    ("How It Works", "how-it-works"),
    ("Visa Guides", "visa"),
    ("Blog", "blog"),
]

FOOTER_SERVICES = [
    ("Flight reservation for visa", "flight-reservation-for-visa"),
    ("Hotel booking for visa", "hotel-booking-for-visa"),
    ("Flight + hotel package", "flight-and-hotel-package"),
    ("Proof of onward travel", "proof-of-onward-travel"),
    ("Pricing", "pricing"),
    ("Verify a PNR", "verify-pnr"),
]

FOOTER_COMPANY = [
    ("How it works", "how-it-works"),
    ("About us", "about"),
    ("Contact", "contact"),
    ("FAQ", "faq"),
    ("Blog", "blog"),
    ("Terms of service", "terms"),
    ("Privacy policy", "privacy-policy"),
    ("Refund policy", "refund-policy"),
]


# --------------------------------------------------------------------------
# reusable components
# --------------------------------------------------------------------------
def ticket(title, desc, price, features, cta_label, cta_href,
           code="ECONOMY", featured=False, badge=None, price_note="per traveller"):
    lis = "".join("<li>%s</li>" % f for f in features)
    return """
<div class="ticket-slot">
<article class="ticket%s">%s
  <div class="ticket__main">
    <h3>%s</h3>
    <p class="ticket__desc">%s</p>
    <ul class="ticket__list">%s</ul>
    <a class="btn btn--%s btn--block" href="%s">%s</a>
  </div>
  <div class="ticket__stub">
    <p class="ticket__price">$%s<small>%s</small></p>
    <div class="ticket__barcode"></div>
    <span class="ticket__code">%s</span>
  </div>
</article>
</div>""" % (
        " ticket--featured" if featured else "",
        '<span class="tag-best">%s</span>' % badge if badge else "",
        title, desc, lis,
        "primary" if featured else "ghost", url(cta_href), cta_label,
        price, price_note, code,
    )


def faq_block(items, heading="Frequently asked questions", intro=None, level="h2"):
    """items = list of (question, answer_html). Renders HTML; schema built separately."""
    rows = ""
    for q, a in items:
        rows += ('<details><summary>%s</summary><div class="faq__a">%s</div></details>'
                 % (q, a))
    head = "<%s>%s</%s>" % (level, heading, level) if heading else ""
    lede = '<p class="lede">%s</p>' % intro if intro else ""
    return '%s%s<div class="faq">%s</div>' % (head, lede, rows)


def faq_schema(items):
    return {
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question",
            "name": re.sub(r"<[^>]+>", "", q),
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", a)).strip()},
        } for q, a in items],
    }


def crumbs(trail):
    """trail = list of (label, slug|None). Returns (html, schema)."""
    parts, items = [], []
    parts.append('<a href="%s">Home</a>' % url())
    items.append({"@type": "ListItem", "position": 1, "name": "Home", "item": abs_url()})
    for i, (label, slug) in enumerate(trail, start=2):
        parts.append("&rsaquo;")
        if slug:
            parts.append('<a href="%s">%s</a>' % (url(slug), label))
            items.append({"@type": "ListItem", "position": i, "name": label, "item": abs_url(slug)})
        else:
            parts.append("<span>%s</span>" % label)
            items.append({"@type": "ListItem", "position": i, "name": label})
    html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " ".join(parts)
    return html, {"@type": "BreadcrumbList", "itemListElement": items}


def cta_band(title="Ready to complete your visa file?",
             text="Get a verifiable flight reservation with a live PNR in %s. No airline payment, no risk if your visa is refused." % DELIVERY,
             primary=("Order your ticket", "order"),
             secondary=("See pricing", "pricing")):
    return """
<section class="tight"><div class="wrap"><div class="cta">
  <h2>%s</h2>
  <p>%s</p>
  <div class="btn-row" style="justify-content:center;margin-top:1.6rem">
    <a class="btn btn--ghost btn--lg" href="%s">%s</a>
    <a class="btn btn--lg" style="border-color:rgba(255,255,255,.55);color:#fff" href="%s">%s</a>
  </div>
</div></div></section>""" % (title, text, url(primary[1]), primary[0], url(secondary[1]), secondary[0])


def pricing_tickets(featured="both"):
    return """<div class="grid g3">%s%s%s</div>""" % (
        ticket("Flight Reservation", "A real, airline-held itinerary with a live PNR you can verify yourself.",
               PRICE_FLIGHT,
               ["Live PNR, verifiable on the airline site",
                "One-way, return or multi-city",
                "Delivered as an embassy-ready PDF",
                "Free name or date correction once"],
               "Order flight ticket", "order", code="FLIGHT", featured=(featured == "flight")),
        ticket("Hotel Booking", "A confirmed accommodation booking in your name for the exact dates of your stay.",
               PRICE_HOTEL,
               ["Confirmed booking with a reference number",
                "Matches your flight dates automatically",
                "Any city, any length of stay",
                "Free date correction once"],
               "Order hotel booking", "order", code="HOTEL", featured=(featured == "hotel")),
        ticket("Flight + Hotel", "The complete travel-proof bundle most consulates ask for. Best value.",
               PRICE_BOTH,
               ["Everything in both plans above",
                "Dates cross-checked for consistency",
                "One PDF pack, ready to upload",
                "Priority support until your appointment"],
               "Order the bundle", "order", code="BUNDLE",
               featured=(featured == "both"), badge="Most popular"),
    )


def iata_badge(size="md"):
    """IATA accreditation badge. Renders nothing when IATA_ACCREDITED is False."""
    if not IATA_ACCREDITED:
        return ""
    num = ('<span class="badge__num">IATA %s</span>' % IATA_NUMBER) if IATA_NUMBER else ""
    return """<span class="badge badge--%s">%s<span class="badge__txt"><b>IATA Certified Agent</b>%s</span></span>""" % (
        size, ICON["seal"], num)


def stat_bar():
    """The 'Since 2017 / 10 lakh flights' credibility strip."""
    cells = []
    if SINCE_YEAR:
        cells.append(("Since " + SINCE_YEAR, "Issuing travel documents for visa applicants"))
    if FLIGHTS_BOOKED:
        cells.append((FLIGHTS_BOOKED, "Flight bookings made"))
    if VISAS_HELPED:
        cells.append((VISAS_HELPED, "Travellers helped with visa files"))
    cells.append((AIRLINE_COUNT if AIRLINE_COUNT else "Global", "Airlines we book on"))
    if not cells:
        return ""
    inner = "".join('<div class="stat"><b>%s</b><span>%s</span></div>' % (a, b) for a, b in cells)
    return '<div class="stats">%s</div>' % inner


def trust_cards(heading="Why travellers trust %s" % BRAND):
    """Three-up trust panel: verifiable PNR, IATA accreditation, money-back."""
    cards = []
    if VISAS_HELPED:
        cards.append((ICON["seal"], "%s successful visa files" % VISAS_HELPED,
                      "Documents supplied for Schengen, US, UK, Canada, UAE and beyond &mdash; "
                      "since %s." % SINCE_YEAR if SINCE_YEAR else
                      "Documents supplied for Schengen, US, UK, Canada, UAE and beyond."))
    cards.append((ICON["shield"], "100% verifiable PNR",
                  "Real six-character booking references that resolve on the airline&rsquo;s own "
                  "&lsquo;manage booking&rsquo; page. Check yours before you file."))
    if IATA_ACCREDITED:
        cards.append((ICON["award"], "IATA certified agent",
                      "Bookings are made through accredited channels in live airline reservation "
                      "systems &mdash; not generated as PDFs." +
                      (" Accreditation no. %s." % IATA_NUMBER if IATA_NUMBER else "")))
    cards.append((ICON["wallet"], "Money-back guarantee",
                  "If a booking reference does not verify, or we fail to deliver, you get a full "
                  "refund. <a href=\"%s\">Read the policy</a>." % url("refund-policy")))

    inner = "".join('<div class="trust-card">%s<h3>%s</h3><p>%s</p></div>' % c for c in cards)
    head = '<div class="center" style="margin-bottom:2.4rem"><h2>%s</h2></div>' % heading if heading else ""
    return '%s<div class="trust-panel">%s</div>' % (head, inner)


def airline_strip(heading=None):
    if heading is None:
        heading = "Visa flight bookings with %s trusted airlines" % AIRLINE_COUNT
    marks = "".join('<span class="mark">%s</span>' % a for a in AIRLINES)
    return """
<div class="center"><h2>%s</h2>
<p class="lede">We book on the carrier that actually operates your route, using live availability.</p></div>
<div class="marks" role="list" aria-label="Airlines we book on">%s</div>
<p class="center" style="margin-top:1rem;color:var(--ink-3);font-size:.85rem">
Airline names are the trademarks of their respective owners and are shown to indicate carriers we book on.
No endorsement or partnership is implied.</p>""" % (heading, marks)


# --------------------------------------------------------------------------
# page shell
# --------------------------------------------------------------------------
ORG_SCHEMA = {
    "@type": "Organization",
    "@id": SITE_URL + "/#organization",
    "name": BRAND,
    "url": SITE_URL + "/",
    "description": TAGLINE,
    "email": EMAIL,
    "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/img/logo.png", "width": 512, "height": 512},
    "foundingDate": SINCE_YEAR if SINCE_YEAR else None,
    "hasCredential": ([{
        "@type": "EducationalOccupationalCredential",
        "credentialCategory": "IATA accreditation",
        "recognizedBy": {"@type": "Organization", "name": "International Air Transport Association"},
    }] if IATA_ACCREDITED else None),
    "sameAs": [],
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "customer support",
        "email": EMAIL,
        "availableLanguage": ["English"],
        "areaServed": "Worldwide",
    }],
}

WEBSITE_SCHEMA = {
    "@type": "WebSite",
    "@id": SITE_URL + "/#website",
    "url": SITE_URL + "/",
    "name": BRAND,
    "description": TAGLINE,
    "publisher": {"@id": SITE_URL + "/#organization"},
    "inLanguage": "en",
}


def header(active):
    links = ""
    for label, slug in NAV:
        cur = ' aria-current="page"' if slug == active else ""
        links += '<a href="%s"%s>%s</a>' % (url(slug), cur, label)
    return """
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap hdr__in">
    <a class="logo" href="%s" aria-label="%s home">%s<span>Visa<b>Flight</b>Ticket</span></a>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav">%s</button>
    <nav class="nav" id="nav" aria-label="Main">
      %s
      <a class="btn btn--primary" href="%s">Order now</a>
    </nav>
  </div>
</header>""" % (url(), BRAND, LOGO_SVG, ICON["burger"], links, url("order"))


def footer(visa_links):
    services = "".join('<li><a href="%s">%s</a></li>' % (url(s), l) for l, s in FOOTER_SERVICES)
    company = "".join('<li><a href="%s">%s</a></li>' % (url(s), l) for l, s in FOOTER_COMPANY)
    visas = "".join('<li><a href="%s">%s</a></li>' % (url("visa/" + s), l) for l, s in visa_links[:8])
    return """
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__grid">
      <div>
        <a class="logo" href="%s">%s<span>Visa<b>Flight</b>Ticket</span></a>
        <p class="ftr__note">Real, airline-held flight reservations and confirmed hotel bookings with verifiable
        references &mdash; built for visa applications, delivered in %s.</p>
        <div style="margin-top:1.1rem">%s</div>
        <div class="btn-row" style="margin-top:1.2rem">
          <a class="btn btn--ghost" href="%s">%s Email us</a>
          <button class="theme-btn" type="button" aria-label="Switch colour theme">%s</button>
        </div>
      </div>
      <div><h4>Services</h4><ul>%s</ul></div>
      <div><h4>Visa guides</h4><ul>%s<li><a href="%s">All visa guides</a></li></ul></div>
      <div><h4>Company</h4><ul>%s</ul></div>
    </div>
    <div class="ftr__bottom">
      <span>&copy; <span class="js-year">%s</span> %s. All rights reserved.</span>
      <span>We are a travel-documentation service. We are not a government body and we do not issue visas.</span>
    </div>
  </div>
</footer>""" % (url(), LOGO_SVG, DELIVERY, iata_badge("sm"), "mailto:" + EMAIL,
                ICON["mail"], ICON["sun"],
                services, visas, url("visa"), company, date.today().year, BRAND)


PAGE_TPL = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
{robots}<meta name="theme-color" content="#b4531f" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#17120d" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{brand}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/og-default.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="{twitter}">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{site}/assets/img/og-default.png">
<link rel="icon" href="{fav}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{apple}">
<link rel="manifest" href="{manifest}">
<link rel="preload" as="style" href="{css}">
<link rel="stylesheet" href="{css}">
{schema}
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
<script src="{js}" defer></script>
</body>
</html>
"""


def add_page(slug, title, description, body, schema=None, og_type="website",
             og_title=None, noindex=False, priority="0.7", changefreq="monthly",
             lastmod=TODAY):
    """Queue a page for writing. Called by every content module."""
    PAGES.append(dict(
        slug=slug, title=title, description=description, body=body,
        schema=schema or [], og_type=og_type, og_title=og_title or title,
        noindex=noindex, priority=priority, changefreq=changefreq, lastmod=lastmod,
    ))


def write_pages(visa_links):
    for p in PAGES:
        active = p["slug"].split("/")[0]
        graph = list(p["schema"])
        if p["slug"] == "":
            graph = [ORG_SCHEMA, WEBSITE_SCHEMA] + graph
        html = PAGE_TPL.format(
            title=p["title"],
            description=p["description"].replace('"', "&quot;"),
            canonical=abs_url(p["slug"]),
            robots='<meta name="robots" content="noindex,follow">\n' if p["noindex"]
                   else '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">\n',
            og_type=p["og_type"],
            og_title=p["og_title"].replace('"', "&quot;"),
            brand=BRAND,
            site=SITE_URL,
            twitter=TWITTER,
            fav=asset("assets/img/favicon.svg"),
            apple=asset("assets/img/apple-touch-icon.png"),
            manifest=asset("site.webmanifest"),
            css=asset("assets/css/style.css"),
            js=asset("assets/js/main.js"),
            schema=jsonld(*graph),
            header=header(active),
            body=p["body"],
            footer=footer(visa_links),
        )
        out_dir = ROOT if p["slug"] == "" else os.path.join(ROOT, *p["slug"].split("/"))
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(html)
    return len(PAGES)


def write_sitemap():
    rows = []
    for p in sorted(PAGES, key=lambda x: (-float(x["priority"]), x["slug"])):
        if p["noindex"]:
            continue
        rows.append(
            "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>"
            % (abs_url(p["slug"]), p["lastmod"], p["changefreq"], p["priority"]))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)

    robots = """User-agent: *
Allow: /
Disallow: /order/thank-you/

# AI answer engines are a growing referral source for this niche - let them in.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: %s/sitemap.xml
""" % SITE_URL
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots)


def write_extras():
    manifest = {
        "name": BRAND, "short_name": "VisaFlightTicket",
        "description": TAGLINE, "start_url": url(), "display": "standalone",
        "background_color": "#fdfaf5", "theme_color": "#b4531f",
        "icons": [
            {"src": asset("assets/img/favicon.svg"), "sizes": "any", "type": "image/svg+xml"},
            {"src": asset("assets/img/apple-touch-icon.png"), "sizes": "180x180", "type": "image/png"},
        ],
    }
    with open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    # 404 page (GitHub Pages / Netlify pick this up automatically)
    body = """
<section><div class="wrap wrap--narrow center">
  <p class="eyebrow">Error 404</p>
  <h1>This gate has changed</h1>
  <p class="lede">The page you were looking for is not here. Here are the routes people use most.</p>
  <ul class="pills" style="justify-content:center;margin:2rem 0">
    <li><a href="%s">Flight reservation for visa</a></li>
    <li><a href="%s">Hotel booking for visa</a></li>
    <li><a href="%s">Pricing</a></li>
    <li><a href="%s">Visa guides</a></li>
    <li><a href="%s">Blog</a></li>
  </ul>
  <a class="btn btn--primary btn--lg" href="%s">Back to home</a>
</div></section>""" % (url("flight-reservation-for-visa"), url("hotel-booking-for-visa"),
                       url("pricing"), url("visa"), url("blog"), url())
    html = PAGE_TPL.format(
        title="Page not found | " + BRAND, description="The page you requested could not be found.",
        canonical=abs_url("404"), robots='<meta name="robots" content="noindex,follow">\n',
        og_type="website", og_title="Page not found", brand=BRAND, site=SITE_URL, twitter=TWITTER,
        fav=asset("assets/img/favicon.svg"), apple=asset("assets/img/apple-touch-icon.png"),
        manifest=asset("site.webmanifest"), css=asset("assets/css/style.css"),
        js=asset("assets/js/main.js"), schema="", header=header(""), body=body,
        footer=footer(VISA_LINKS_CACHE))
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(html)


VISA_LINKS_CACHE = []


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    import content_core
    import content_visa
    import content_blog

    global VISA_LINKS_CACHE
    VISA_LINKS_CACHE = content_visa.link_list()

    content_core.build()
    content_visa.build()
    content_blog.build()

    n = write_pages(VISA_LINKS_CACHE)
    write_sitemap()
    write_extras()
    print("Built %d pages -> %s" % (n, ROOT))
    for p in sorted(PAGES, key=lambda x: x["slug"]):
        print("   /%s" % p["slug"])


if __name__ == "__main__":
    # Re-enter through the real module name so the content modules and this
    # file share one copy of PAGES (running as __main__ would create two).
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build as _build
    _build.main()
