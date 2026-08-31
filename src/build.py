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
WHATSAPP = "+918619663455"          # E.164; digits are stripped for the wa.me link
WHATSAPP_DISPLAY = "Chat on WhatsApp"
TWITTER = "@visaflightticket"

# --- currency & pricing ---------------------------------------------------
# CURRENCY drives every price on the site, the JS calculators and the
# priceCurrency in Product/Offer schema. Change these four numbers and the
# whole site follows -- copy, tables, badges and structured data included.
CURRENCY = "₹"          # rupee sign
CURRENCY_CODE = "INR"
PRICE_FLIGHT = 499
PRICE_HOTEL = 399
PRICE_BOTH = 799
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

# --------------------------------------------------------------------------
# BACKEND (Supabase + Razorpay)
# Both values below are PUBLIC by design: the anon key is an identifier, not
# a secret, and RLS denies it every table. Secrets (service-role key,
# Razorpay key_secret, webhook secret, Resend key) live only in the Edge
# Function environment -- never here, never in the repo.
# Leave SUPABASE_URL empty and the order form falls back to its offline
# notice, so the site keeps working before the backend is switched on.
# --------------------------------------------------------------------------
SUPABASE_URL = "https://jijnknqfampnmhyakxzz.supabase.co"
SUPABASE_ANON_KEY = "sb_publishable_IcCbMYgZYZGt6Udh2LRTXQ_I38zJepI"


# Carriers we book on, in marquee order.
# Drop a logo at assets/img/airlines/<slug>.svg (or .png) and the next build
# swaps that carrier's wordmark for the image automatically -- no code change.
# Slug = lowercase name, non-alphanumerics collapsed to "-" (see slugify()).
# Only add files you have written permission to display: most carrier brand
# guidelines forbid use that implies partnership or endorsement.
AIRLINES = [
    "Batik Air Malaysia", "Malaysia Airlines", "Pegasus Airlines", "IndiGo",
    "Turkish Airlines", "Etihad Airways", "FlyBaghdad", "Air India",
    "Oman Air", "Air Sial", "Emirates", "British Airways",
    "Virgin Atlantic", "Qatar Airways", "SalamAir", "Iran Air",
    "China Southern", "Saudia", "Thai Airways", "Air China",
    "Pakistan International Airlines", "flydubai", "American Airlines", "flynas",
    "Air Arabia", "Jazeera Airways", "SriLankan Airlines", "Gulf Air",
    "Fly Jinnah", "Singapore Airlines", "Kam Air", "Kuwait Airways",
    "airblue", "Mahan Air", "Air Mauritius", "SereneAir",
    "Cham Wings Airlines", "Taban Airlines", "SpiceJet", "Iraqi Airways",
    "Uzbekistan Airways", "Lufthansa",
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


_ASSET_V = {}


def asset(path, bust=False):
    """Web path for a local asset. bust=True appends a content hash so a
    rebuilt stylesheet or script is never served from a stale cache."""
    rel = path.lstrip("/")
    out = BASE_PATH + "/" + rel
    if not bust:
        return out
    if rel not in _ASSET_V:
        full = os.path.join(ROOT, *rel.split("/"))
        try:
            with open(full, "rb") as fh:
                import hashlib
                _ASSET_V[rel] = hashlib.md5(fh.read()).hexdigest()[:8]
        except OSError:
            _ASSET_V[rel] = "0"
    return out + "?v=" + _ASSET_V[rel]


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


def money(n):
    """499 -> Rs499, 150000 -> Rs1,50,000 (Indian digit grouping).
    Idempotent: an already-formatted value passes straight through, so
    callers never have to know whether a price was formatted upstream."""
    if isinstance(n, str):
        if n.startswith(CURRENCY):
            return n
        n = n.replace(CURRENCY, "").replace(",", "")
    n = int(n)
    s = str(n)
    if len(s) > 3:                      # 1,50,000 not 150,000
        head, tail = s[:-3], s[-3:]
        head = re.sub(r"(?<=\d)(?=(\d\d)+$)", ",", head)
        s = head + "," + tail
    return CURRENCY + s


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
    "whatsapp": ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
                 '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.46 1.32 4.96L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.13h-.01a8.23 8.23 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.19 8.19 0 0 1-1.26-4.36c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.19 8.19 0 0 1 2.41 5.83c0 4.54-3.7 8.21-8.24 8.21Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.54.06-.25-.13-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.44.13-.15.17-.25.25-.42.08-.16.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.84-.2-.49-.4-.42-.56-.43h-.47c-.16 0-.43.06-.65.31-.22.25-.86.84-.86 2.05s.88 2.38 1 2.54c.13.17 1.74 2.65 4.21 3.72.59.25 1.05.4 1.4.52.59.19 1.13.16 1.55.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.11-.22-.17-.47-.29Z"/></svg>'),
    "headset": _svg('<path d="M4 14v-2a8 8 0 0 1 16 0v2"/><path d="M4 14h2.5a1 1 0 0 1 1 1v4a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1Z"/><path d="M20 14h-2.5a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1H19a1 1 0 0 0 1-1Z"/><path d="M18 20a3 3 0 0 1-3 2.5h-2"/>'),
    "bulb": _svg('<path d="M9.5 17h5M10 21h4"/><path d="M12 2a6.5 6.5 0 0 0-3.8 11.8c.5.4.8 1 .8 1.6v.6h6v-.6c0-.6.3-1.2.8-1.6A6.5 6.5 0 0 0 12 2Z"/>'),
    "cash": _svg('<rect x="2" y="6" width="20" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.6"/><path d="M5.5 12h.01M18.5 12h.01"/>'),
    "handshake": _svg('<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2l-1-1"/><path d="m14 16 1.5 1.5a1.4 1.4 0 0 0 2-2L13 11"/><path d="M8.5 8.5 6 11a1.5 1.5 0 0 0 0 2.1l3 3a1.5 1.5 0 0 0 2.1 0l.9-.9"/><path d="M13 11 9.6 7.6a2 2 0 0 0-2.8 0L4 10.4"/><path d="M14.5 8.5 17 6a2 2 0 0 1 2.8 0L22 8.2"/>'),
    "up": _svg('<path d="m6 15 6-6 6 6"/>'),
    "award": _svg('<circle cx="12" cy="9" r="6"/><path d="m8.2 13.8-1.4 7.4 5.2-2.8 5.2 2.8-1.4-7.4"/>'),
}

LOGO_SVG = (
    '<svg viewBox="0 0 32 32" fill="none" aria-hidden="true">'
    '<rect x="1" y="6" width="30" height="20" rx="4" fill="currentColor" opacity=".1"/>'
    '<rect x="1.6" y="6.6" width="28.8" height="18.8" rx="3.4" stroke="currentColor" stroke-opacity=".28" stroke-width="1.2"/>'
    '<path d="M21 6.5v19" stroke="currentColor" stroke-opacity=".45" stroke-width="1.2" stroke-dasharray="2.4 2.4"/>'
    '<path d="M17.4 20.6 16 14.5l2.6-2.6a1.55 1.55 0 0 0-2.2-2.2l-2.6 2.6-6.1-1.4a.37.37 0 0 0-.36.6l2.36 2.36-1.48 1.48-1.33-.3a.37.37 0 0 0-.37.6l1.06 1.06 1.06 1.06a.37.37 0 0 0 .6-.37l-.3-1.33 1.48-1.48 2.36 2.36a.37.37 0 0 0 .6-.37Z" fill="#193b92"/>'
    '<circle cx="25.6" cy="12.5" r="1.1" fill="currentColor" opacity=".3"/>'
    '<circle cx="25.6" cy="16" r="1.1" fill="currentColor" opacity=".3"/>'
    '<circle cx="25.6" cy="19.5" r="1.1" fill="currentColor" opacity=".3"/>'
    '</svg>'
)


def brand_mark():
    """The company logo. Drop your artwork at assets/img/logo-brand.(svg|png|webp)
    and it is used automatically, at any size; otherwise the drawn ticket mark
    below is the fallback. SVG is strongly preferred: the header renders it at
    30px and a raster will look soft on high-density screens."""
    for ext in ("svg", "png", "webp"):
        rel = "assets/img/logo-brand.%s" % ext
        if os.path.exists(os.path.join(ROOT, rel)):
            return ('<img class="logo__img" src="%s" alt="" width="40" height="40" '
                    'decoding="async">' % asset(rel))
    return LOGO_SVG


# --------------------------------------------------------------------------
# navigation
# --------------------------------------------------------------------------
# Top menu is deliberately short. Every other page stays reachable from the
# footer and from in-page links, so crawl depth is unaffected.
NAV = [
    ("Visa Guides", "visa"),
    ("B2B", "b2b"),
    ("Blog", "blog"),
    ("FAQs", "faq"),
    ("Login", "login"),
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
    <p class="ticket__price">%s<small>%s</small></p>
    <div class="ticket__barcode"></div>
    <span class="ticket__code">%s</span>
  </div>
</article>
</div>""" % (
        " ticket--featured" if featured else "",
        '<span class="tag-best">%s</span>' % badge if badge else "",
        title, desc, lis,
        "primary" if featured else "ghost", url(cta_href), cta_label,
        money(price), price_note, code,
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
  %s
  <h2>%s</h2>
  <p>%s</p>
  <div class="btn-row" style="justify-content:center;margin-top:1.6rem">
    <a class="btn btn--ghost btn--lg" href="%s">%s</a>
    <a class="btn btn--lg" style="border-color:rgba(255,255,255,.55);color:#fff" href="%s">%s</a>
  </div>
</div></div></section>""" % (flight_path(), title, text,
                              url(primary[1]), primary[0], url(secondary[1]), secondary[0])


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
                "Free reissue if your appointment moves"],
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


FEATURES = [
    ("bulb", "Live PNR",
     "Every booking is real and held in an airline system. Verify the reference "
     "on the carrier&rsquo;s own site before you file. Takes two minutes."),
    ("headset", "24&times;7 support",
     "Appointment at six in the morning? Message us at any hour and a person "
     "answers, and we would rather you asked than guessed."),
    ("cash", "Cheapest price",
     "%s per traveller, all inclusive. No fare is ever purchased, so there is "
     "no fare to recover. That is why it can be this cheap."),
    ("handshake", "Money-back guarantee",
     "If a reference does not verify, or we fail to deliver, you get a full "
     "refund. Written down, not implied."),
]


def feature_cards():
    """Numbered feature cards. Sits directly under the hero."""
    out = ""
    for i, (icon, title, body) in enumerate(FEATURES, 1):
        text = body % money(PRICE_FLIGHT) if "%s" in body else body
        out += """
<article class="fc">
  <span class="fc__n" aria-hidden="true">%02d</span>
  <span class="fc__i">%s</span>
  <h3>%s</h3>
  <p>%s</p>
</article>""" % (i, ICON[icon], title, text)
    return ('<h2 class="sr">Why travellers choose %s</h2>'
            '<div class="fc-grid">%s</div>' % (BRAND, out))


def trust_cards(heading="Why travellers trust %s" % BRAND):
    """Three-up trust panel: verifiable PNR, IATA accreditation, money-back."""
    cards = []
    if VISAS_HELPED:
        cards.append((ICON["seal"], "%s successful visa files" % VISAS_HELPED,
                      "Documents supplied for Schengen, US, UK, Canada, UAE and beyond. "
                      "since %s." % SINCE_YEAR if SINCE_YEAR else
                      "Documents supplied for Schengen, US, UK, Canada, UAE and beyond."))
    cards.append((ICON["shield"], "100% verifiable PNR",
                  "Real six-character booking references that resolve on the airline&rsquo;s own "
                  "&lsquo;manage booking&rsquo; page. Check yours before you file."))
    if IATA_ACCREDITED:
        cards.append((ICON["award"], "IATA certified agent",
                      "Bookings are made through accredited channels in live airline reservation "
                      "systems, not generated as PDFs." +
                      (" Accreditation no. %s." % IATA_NUMBER if IATA_NUMBER else "")))
    cards.append((ICON["wallet"], "Money-back guarantee",
                  "If a booking reference does not verify, or we fail to deliver, you get a full "
                  "refund. <a href=\"%s\">Read the policy</a>." % url("refund-policy")))

    inner = "".join('<div class="trust-card">%s<h3>%s</h3><p>%s</p></div>' % c for c in cards)
    if heading:
        head = '<div class="center" style="margin-bottom:2.4rem"><h2>%s</h2></div>' % heading
    else:
        # No visible heading, but the h3s below still need an h2 above them or
        # the document outline jumps h1 -> h3.
        head = '<h2 class="sr">Why travellers trust %s</h2>' % BRAND
    return '%s<div class="trust-panel">%s</div>' % (head, inner)


# Hand-drawn-feeling travel doodles, single stroke, no fills. Used as light
# decoration only, never to carry meaning.
DOODLE = {
 "globe":   '<circle cx="24" cy="24" r="15"/><path d="M9 24h30M24 9c4.5 5 4.5 25 0 30-4.5-5-4.5-25 0-30"/><path d="M24 39v5M18 44h12"/>',
 "passport":'<rect x="12" y="8" width="24" height="32" rx="3"/><circle cx="24" cy="20" r="6"/><path d="M18 20h12M24 14c2.5 3 2.5 9 0 12-2.5-3-2.5-9 0-12"/><path d="M19 31h10"/>',
 "suitcase":'<rect x="8" y="17" width="32" height="22" rx="3"/><path d="M18 17v-4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v4M8 26h32"/>',
 "camera":  '<path d="M7 17h7l3-4h14l3 4h7a2 2 0 0 1 2 2v18a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V19a2 2 0 0 1 2-2z"/><circle cx="24" cy="27" r="7"/>',
 "map":     '<path d="M6 13 18 9v26L6 39zM18 9l12 4v26l-12-4zM30 13l12-4v26l-12 4z"/><path d="M18 9v26M30 13v26"/>',
 "palm":    '<path d="M24 20v20M24 20c-6-6-14-5-17 1 5-3 10-2 13 2M24 20c6-6 14-5 17 1-5-3-10-2-13 2M24 20c-2-8 2-14 8-15-4 4-5 9-4 13M24 20c2-8-2-14-8-15 4 4 5 9 4 13"/><path d="M18 40h12"/>',
 "ticket":  '<path d="M6 16h36v8a4 4 0 0 0 0 8v8H6v-8a4 4 0 0 0 0-8z"/><path d="M28 16v4M28 26v4M28 36v4"/>',
 "compass": '<circle cx="24" cy="24" r="16"/><path d="m30 18-4 10-10 4 4-10z"/>',
 "sunhat":  '<path d="M14 28c-5 1-8 3-8 5 0 3 8 5 18 5s18-2 18-5c0-2-3-4-8-5"/><path d="M14 28c0-9 4-15 10-15s10 6 10 15c-3 1-6 1.4-10 1.4S17 29 14 28z"/>',
 "cloud":   '<path d="M14 32a7 7 0 0 1 0-14 10 10 0 0 1 19-3 8 8 0 0 1 1 17z"/>',
}


def doodles(*names):
    """A light scatter of line-art travel icons. Decorative, aria-hidden."""
    out = ""
    for i, n in enumerate(names):
        out += ('<span class="dood dood--%d"><svg viewBox="0 0 48 48" fill="none" '
                'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
                'stroke-linejoin="round">%s</svg></span>' % (i % 6, DOODLE[n]))
    return '<div class="doods" aria-hidden="true">%s</div>' % out


def flight_path():
    """Dashed route with a pin at the origin and a plane at the far end, the
    way a travel graphic actually looks. Decorative, so aria-hidden."""
    return """
<svg class="fpath" viewBox="0 0 1200 420" fill="none" aria-hidden="true"
     preserveAspectRatio="xMidYMax meet">
  <path class="fpath__line"
        d="M112 330 C 208 438, 344 424, 432 314 C 520 204, 628 176, 740 212
           C 852 248, 938 228, 1068 112"
        stroke="currentColor" stroke-width="3" stroke-linecap="round"
        stroke-dasharray="9 13"/>
  <g class="fpath__pin" transform="translate(112 330)">
    <path d="M0 0c-6.6-8.5-9.7-12.7-9.7-17A9.7 9.7 0 1 1 9.7-17C9.7-12.7 6.6-8.5 0 0z"
          fill="currentColor"/>
    <circle cx="0" cy="-17" r="3.7" class="fpath__hole"/>
  </g>
  <g class="fpath__plane" transform="translate(1068 112) rotate(42)">
    <path d="M0-17 3.6-4.9 21 7.2v4.9L3.6 7.2 3 17l5.4 4.9v2.4L0 21.9l-8.4 2.4v-2.4L-3 17
             l-.6-9.8L-21 12.1V7.2L-3.6-4.9Z" fill="currentColor"/>
  </g>
</svg>"""


def route_divider(from_code="DEL", to_code="CDG"):
    """Boarding-pass rule between sections: a pin, a dashed wave, a plane."""
    return """
<div class="rdiv" aria-hidden="true">
  <span class="rdiv__code">%s</span>
  <svg class="rdiv__svg" viewBox="0 0 320 44" fill="none" preserveAspectRatio="none">
    <path d="M8 30 C 58 6, 104 6, 154 22 C 204 38, 250 38, 306 14"
          stroke="currentColor" stroke-width="2.4" stroke-linecap="round"
          stroke-dasharray="7 10"/>
  </svg>
  <span class="rdiv__code">%s</span>
</div>""" % (from_code, to_code)


def highlights(price=True):
    """The three claims the client wants front and centre."""
    items = [
        ("real", ICON["seal"], "100% Real Ticket", "Booked in a real airline system"),
        ("pnr", ICON["shield"], "Live PNR", "Check it yourself, free"),
    ]
    out = ""
    for kind, icon, title, sub in items:
        out += ('<span class="hl__i hl__i--%s">%s<b>%s</b><small>%s</small></span>'
                % (kind, icon, title, sub))
    if price:
        out += ('<span class="hl__i hl__i--price">%s<b>%s <em>only</em></b>'
                '<small>Per traveller, all in</small></span>'
                % (ICON["wallet"], money(PRICE_FLIGHT)))
    return '<div class="hl">%s</div>' % out


def booking_widget():
    """Hero search widget: service tabs, trip type, route, dates. GETs to /order/."""
    return """
<form class="bw" id="bw" action="%s" method="get" data-cur="%s"
      data-p-flight="%d" data-p-hotel="%d" data-p-both="%d">
  <div class="bw__tabs" role="tablist" aria-label="What do you need?">
    <button type="button" class="bw__tab is-on" data-svc="flight" role="tab" aria-selected="true">Flight</button>
    <button type="button" class="bw__tab" data-svc="hotel" role="tab" aria-selected="false">Hotel</button>
    <button type="button" class="bw__tab" data-svc="both" role="tab" aria-selected="false">Both</button>
  </div>
  <input type="hidden" name="service" id="bw-service" value="flight">

  <div class="bw__trip" id="bw-trip">
    <label><input type="radio" name="trip" value="oneway" checked><span>One way</span></label>
    <label><input type="radio" name="trip" value="round"><span>Round trip</span></label>
    <label><input type="radio" name="trip" value="multi"><span>Multi city</span></label>
  </div>

  <div class="bw__f" id="bw-from-wrap">
    <label for="bw-from" id="bw-from-label">From</label>
    <input id="bw-from" name="from" type="text" placeholder="Delhi (DEL)" data-airport>
  </div>
  <div class="bw__f">
    <label for="bw-to" id="bw-to-label">To</label>
    <input id="bw-to" name="to" type="text" placeholder="Paris (CDG)" data-airport>
  </div>
  <div class="bw__row">
    <div class="bw__f">
      <label for="bw-dep" id="bw-dep-label">Departure</label>
      <input id="bw-dep" name="depart" type="date">
    </div>
    <div class="bw__f" id="bw-ret-wrap" hidden>
      <label for="bw-ret" id="bw-ret-label">Return</label>
      <input id="bw-ret" name="return" type="date">
    </div>
  </div>

  <div id="bw-legs" hidden></div>
  <button type="button" class="bw__add" id="bw-addleg" hidden>+ Add another city</button>

  <button class="btn btn--primary btn--lg btn--block" type="submit" id="bw-submit">
    Get my dummy ticket at %s</button>
  <p class="bw__note">
    <b>%s Live PNR</b><b>%s No airline payment</b><b>%s In %s</b>
  </p>
</form>""" % (url("order"), CURRENCY, PRICE_FLIGHT, PRICE_HOTEL, PRICE_BOTH,
       money(PRICE_FLIGHT), ICON["check"], ICON["check"], ICON["check"], DELIVERY)


# --- simplified public-domain national flags, drawn for a 44x29 field -------
_FLAGS = {
    "EU": ('European Union', '<rect width="44" height="29" fill="#039"/>' + "".join(
        '<circle cx="%.2f" cy="%.2f" r="1.35" fill="#fc0"/>' % (
            22 + 8.6 * __import__("math").sin(__import__("math").radians(i * 30)),
            14.5 - 8.6 * __import__("math").cos(__import__("math").radians(i * 30)))
        for i in range(12))),
    "US": ('United States',
           '<rect width="44" height="29" fill="#fff"/>' +
           "".join('<rect y="%.2f" width="44" height="2.23" fill="#b22234"/>' % (i * 4.46) for i in range(7)) +
           '<rect width="17.6" height="15.6" fill="#3c3b6e"/>' +
           "".join('<circle cx="%.1f" cy="%.1f" r=".8" fill="#fff"/>' % (3 + c * 3.9, 3 + r * 3.6)
                   for r in range(4) for c in range(4))),
    "GB": ('United Kingdom',
           '<rect width="44" height="29" fill="#012169"/>'
           '<path d="M0 0 44 29M44 0 0 29" stroke="#fff" stroke-width="6"/>'
           '<path d="M0 0 44 29M44 0 0 29" stroke="#c8102e" stroke-width="2.4"/>'
           '<path d="M22 0v29M0 14.5h44" stroke="#fff" stroke-width="9.5"/>'
           '<path d="M22 0v29M0 14.5h44" stroke="#c8102e" stroke-width="5.7"/>'),
    "CA": ('Canada',
           '<rect width="44" height="29" fill="#fff"/>'
           '<rect width="11" height="29" fill="#d52b1e"/>'
           '<rect x="33" width="11" height="29" fill="#d52b1e"/>'
           '<path d="M22 7.6l1.7 3.3 3.4-.8-1.2 3.2 2.8 2-3.1 1.3.7 3.4-3.2-1.5-1.1 3.4-1.1-3.4-3.2 1.5.7-3.4-3.1-1.3 2.8-2-1.2-3.2 3.4.8z" fill="#d52b1e"/>'),
    "AU": ('Australia',
           '<rect width="44" height="29" fill="#012169"/>'
           '<path d="M0 0 22 14.5M22 0 0 14.5" stroke="#fff" stroke-width="3"/>'
           '<path d="M11 0v14.5M0 7.25h22" stroke="#fff" stroke-width="4.8"/>'
           '<path d="M11 0v14.5M0 7.25h22" stroke="#c8102e" stroke-width="2.6"/>'
           '<circle cx="11" cy="22" r="1.7" fill="#fff"/>'
           '<circle cx="33" cy="6" r="1.1" fill="#fff"/><circle cx="37.5" cy="12" r="1.1" fill="#fff"/>'
           '<circle cx="30" cy="15" r="1.1" fill="#fff"/><circle cx="34" cy="21" r="1.1" fill="#fff"/>'
           '<circle cx="35.5" cy="16.5" r=".7" fill="#fff"/>'),
}


def _window(code):
    label, flag = _FLAGS[code]
    return """<span class="vv__win" title="%s">
<svg viewBox="0 0 62 84" preserveAspectRatio="xMidYMid slice" role="img" aria-label="%s flag">
  <defs><linearGradient id="sky%s" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#bfe3f7"/><stop offset="1" stop-color="#e9f5fb"/></linearGradient></defs>
  <rect width="62" height="84" fill="url(#sky%s)"/>
  <ellipse cx="16" cy="17" rx="13" ry="5" fill="#fff" opacity=".75"/>
  <ellipse cx="47" cy="70" rx="15" ry="5.5" fill="#fff" opacity=".6"/>
  <g transform="translate(9,27.5)">
    <rect width="44" height="29" rx="2.5" fill="#fff"/>
    <g clip-path="inset(0 round 2.5px)">%s</g>
    <rect width="44" height="29" rx="2.5" fill="none" stroke="rgba(0,0,0,.18)"/>
  </g>
</svg></span>""" % (label, label, code, code, flag)


def visitor_visa_panel():
    wins = "".join(_window(c) for c in ("EU", "US", "GB", "CA", "AU"))
    return """
<div class="vv">
  <p class="vv__k">Schengen &middot; USA &middot; UK &middot; Canada &middot; Australia</p>
  <h2>Get your visitor visa</h2>
  <p>One file, five continents. We supply the flight and hotel proof; you bring the rest.</p>
  <div class="vv__windows">%s</div>
</div>""" % wins


def trust_section(heading="Why travellers trust %s" % BRAND):
    """Full-width card row. No side panel -- the cards carry the section."""
    head = ('<div class="center" style="margin-bottom:2.4rem"><h2>%s</h2>'
            '<p class="lede">Four things that separate a document which passes '
            'from one that raises a question.</p></div>' % heading) if heading else ""
    return """%s%s
<p style="text-align:center;margin:2rem 0 0"><a class="btn btn--primary btn--lg" href="%s">Book now</a></p>""" % (
        head, trust_cards(heading=None), url("order"))


def _logo_file(name):
    """Return the web path of a logo for `name` if one is on disk, else None."""
    slug = slugify(name)
    for ext in ("svg", "png", "webp", "jpg"):
        rel = "assets/img/airlines/%s.%s" % (slug, ext)
        if os.path.exists(os.path.join(ROOT, rel)):
            return asset(rel)
    return None


def _mark(name):
    """A logo tile: brand mark plus name when we have the file, name alone
    otherwise. Carriers without a logo sit in the same row without a gap."""
    src = _logo_file(name)
    if src:
        return ('<span class="mq__item mq__item--logo">'
                '<img src="%s" alt="" width="30" height="30" loading="lazy" decoding="async">'
                '<b>%s</b></span>' % (src, name))
    return '<span class="mq__item"><b>%s</b></span>' % name


def _row(names, variant=""):
    """One marquee lane. Content is duplicated so the -50% keyframe wraps clean."""
    tiles = "".join(_mark(n) for n in names)
    return ('<div class="mq%s"><div class="mq__track">%s%s</div></div>'
            % (variant, tiles, tiles))


def airline_strip(heading=None, rows=3):
    if heading is None:
        heading = "Visa flight bookings with %s trusted airlines" % AIRLINE_COUNT
    per = -(-len(AIRLINES) // rows)          # ceil, so nothing is dropped
    lanes = ""
    for i, variant in zip(range(0, len(AIRLINES), per), ("", " mq--b", " mq--c", " mq--b")):
        lanes += _row(AIRLINES[i:i + per], variant)
    return """
<div class="center" style="margin-bottom:2.2rem"><h2>%s</h2>
<p class="lede">We book on the carrier that actually operates your route, using live availability.</p></div>
%s
<p class="center" style="margin-top:1.4rem;color:var(--ink-3);font-size:.83rem">
Airline names and marks are the trademarks of their respective owners, shown to indicate carriers we book on.
No endorsement, partnership or affiliation is implied.</p>""" % (heading, lanes)


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


def _wa_display():
    """+918619663455 -> +91 86196 63455"""
    d = re.sub(r"[^0-9]", "", WHATSAPP)
    return "+%s %s %s" % (d[:2], d[2:7], d[7:]) if len(d) == 12 else WHATSAPP


def sticky_cta(active):
    """Persistent conversion bar. Appears once the hero scrolls away, so blog
    and guide readers always have a route to the order form -- which they lost
    when the header CTA came out of the nav."""
    if active in ("order", "login"):
        return ""
    return """
<button type="button" class="totop" id="totop" aria-label="Back to top">%s</button>
<div class="scta" id="scta" data-hidden>
  <div class="wrap scta__in">
    <div class="scta__txt">
      <b>Verifiable flight reservation for your visa</b>
      <span>%s Live PNR &middot; delivered in %s &middot; money-back guarantee</span>
    </div>
    <div class="scta__act">
      <span class="scta__price"><em>from</em>%s</span>
      <a class="btn btn--primary" href="%s">Get my ticket</a>
      <a class="btn btn--wa scta__wa" href="https://wa.me/%s" aria-label="Chat on WhatsApp">%s</a>
    </div>
  </div>
</div>""" % (ICON["up"], ICON["check"], DELIVERY, money(PRICE_FLIGHT), url("order"),
             re.sub(r"[^0-9]", "", WHATSAPP), ICON["whatsapp"])


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
      <a class="wa" href="https://wa.me/%s">%s<span>%s</span></a>
    </nav>
  </div>
</header>""" % (url(), BRAND, brand_mark(), ICON["burger"], links,
                re.sub(r"[^0-9]", "", WHATSAPP), ICON["whatsapp"], _wa_display())


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
        references. Built for visa applications, delivered in %s.</p>
        <div style="margin-top:1.1rem">%s</div>
        <div class="btn-row" style="margin-top:1.2rem">
          <a class="btn btn--ghost" href="%s">%s Email us</a>
          <button class="theme-btn" type="button" aria-label="Switch colour theme">%s</button>
        </div>
      </div>
      <div><h2 class="ftr__h">Services</h2><ul>%s</ul></div>
      <div><h2 class="ftr__h">Visa guides</h2><ul>%s<li><a href="%s">All visa guides</a></li></ul></div>
      <div><h2 class="ftr__h">Company</h2><ul>%s</ul></div>
    </div>
    <div class="ftr__bottom">
      <span>&copy; <span class="js-year">%s</span> %s. All rights reserved.</span>
      <span>We are a travel-documentation service. We are not a government body and we do not issue visas.</span>
    </div>
  </div>
</footer>""" % (url(), brand_mark(), DELIVERY, iata_badge("sm"), "mailto:" + EMAIL,
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
{robots}<meta name="theme-color" content="#ffffff">
<meta name="color-scheme" content="light">
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
<script>document.documentElement.className+=" js-anim";window.VFT_CONFIG={{supabaseUrl:"{sb_url}",supabaseAnonKey:"{sb_key}",basePath:"{base}",email:"{sb_mail}",whatsapp:"{sb_wa}",currency:"{sb_cur}"}}</script>
<link rel="preload" as="font" type="font/woff2" href="{fjak}" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{fint}" crossorigin>
<link rel="preload" as="style" href="{css}">
<link rel="stylesheet" href="{css}">
{schema}
</head>
<body>
{header}
{scta}
<main id="main">
{body}
</main>
{footer}
{extra_js}<script src="{js}" defer></script>
</body>
</html>
"""


def add_page(slug, title, description, body, schema=None, og_type="website",
             og_title=None, noindex=False, priority="0.7", changefreq="monthly",
             lastmod=TODAY, extra_js=()):
    """Queue a page for writing. Called by every content module."""
    PAGES.append(dict(
        slug=slug, title=title, description=description, body=body,
        schema=schema or [], og_type=og_type, og_title=og_title or title,
        noindex=noindex, priority=priority, changefreq=changefreq, lastmod=lastmod,
        extra_js=tuple(extra_js),
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
            sb_url=SUPABASE_URL, sb_key=SUPABASE_ANON_KEY, base=BASE_PATH,
            sb_mail=EMAIL, sb_wa='https://wa.me/' + re.sub(r'[^0-9]', '', WHATSAPP),
            sb_cur=CURRENCY,
            fjak=asset("assets/fonts/jakarta-latin.woff2"),
            fint=asset("assets/fonts/inter-latin.woff2"),
            css=asset("assets/css/style.css", bust=True),
            js=asset("assets/js/main.js", bust=True),
            extra_js="".join('<script src="%s" defer></script>' % asset(x, bust=True)
                             for x in p["extra_js"]),
            schema=jsonld(*graph),
            header=header(active),
            scta=sticky_cta(active),
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


def write_airports():
    """Ship the lookup table as one pipe-delimited string -- about half the
    bytes of the equivalent JSON, and parsed just as fast in the browser."""
    import airports
    js = "window.VFT_AIRPORTS=%s;" % json.dumps(airports.payload())
    path = os.path.join(ROOT, "assets", "js", "airports.js")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(js)
    return len(airports.AIRPORTS), len(js)


def write_extras():
    manifest = {
        "name": BRAND, "short_name": "VisaFlightTicket",
        "description": TAGLINE, "start_url": url(), "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#193b92",
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
        manifest=asset("site.webmanifest"),
        sb_url=SUPABASE_URL, sb_key=SUPABASE_ANON_KEY, base=BASE_PATH,
        sb_mail=EMAIL, sb_wa='https://wa.me/' + re.sub(r'[^0-9]', '', WHATSAPP),
        sb_cur=CURRENCY,
        fjak=asset("assets/fonts/jakarta-latin.woff2"),
        fint=asset("assets/fonts/inter-latin.woff2"),
        css=asset("assets/css/style.css", bust=True),
        js=asset("assets/js/main.js", bust=True), extra_js="", schema="",
        header=header(""), scta="", body=body, footer=footer(VISA_LINKS_CACHE))
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
    import content_pages

    global VISA_LINKS_CACHE
    VISA_LINKS_CACHE = content_visa.link_list()

    content_core.build()
    content_pages.build()
    content_visa.build()
    content_blog.build()

    count, size = write_airports()
    print("Airport index: %d airports, %.1f KB" % (count, size / 1024.0))
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
