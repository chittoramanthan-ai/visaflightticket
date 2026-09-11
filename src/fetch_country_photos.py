# -*- coding: utf-8 -*-
"""
One-off helper: download a country photo per visa guide into
assets/img/countries/.

    set PEXELS_API_KEY=...        (Windows)
    export PEXELS_API_KEY=...     (bash)
    python src/fetch_country_photos.py

Deliberately NOT part of build.py, matching fetch_logos.py: builds stay
offline and deterministic. Run this once, commit the files, and the card
layout picks them up.

Note on rights
--------------
Pexels grants free commercial use, with modification allowed and attribution
optional. That is why this fetches from Pexels rather than from any site whose
photos are licensed to that site rather than to you - a competitor's country
images are either their own photography or stock they hold the licence for,
and neither transfers by copying the file.

Attribution is optional under the licence but this still records the
photographer and source URL for every image in assets/img/countries/
credits.json, so the provenance of anything on the site can be answered
later without guesswork.
"""

import io
import json
import os
import sys
import time

try:
    from urllib.request import urlopen, Request
    from urllib.parse import quote
except ImportError:                                   # pragma: no cover
    from urllib2 import urlopen, Request              # type: ignore
    from urllib import quote                          # type: ignore

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import ROOT, slugify                       # noqa: E402
import content_visa                                   # noqa: E402

OUT = os.path.join(ROOT, "assets", "img", "countries")
API = ("https://api.pexels.com/v1/search?query=%s&per_page=3&orientation=%s")
CROP = "?auto=compress&cs=tinysrgb&fit=crop&w=440&h=560"
# Landscape crop of the same photo, for the banner on a visa guide page.
# Reusing the chosen image keeps a country looking the same everywhere.
# Two landscape crops, because one size cannot serve both. The Pexels CDN
# ignores a quality parameter - measured, q=45 and q=62 return identical
# bytes - so width is the only lever. At 1100 wide a banner is 140 KB; at 640
# it is 48 KB. The banner is the LCP element on every visa guide, and most of
# that traffic is on a phone, so the small one is what most visitors fetch.
CROP_WIDE = "?cs=tinysrgb&fit=crop&w=1100&h=340"
CROP_WIDE_SM = "?cs=tinysrgb&fit=crop&w=640&h=200"

# A generic query returns abstract stock as often as a country: "Saudi Arabia
# landmark travel" came back as a canopy against sky, which is recognisable as
# nowhere. Every country gets a specific, identifiable subject instead.
SEARCH = {
    "Schengen": "Paris Eiffel Tower",
    "United States": "New York Manhattan skyline",
    "United Kingdom": "London Tower Bridge",
    "Canada": "Banff Moraine Lake Canada",
    "UAE": "Dubai Burj Khalifa skyline",
    "Australia": "Sydney Opera House harbour",
    "Japan": "Mount Fuji pagoda Japan",
    "Turkey": "Istanbul Hagia Sophia",
    "Thailand": "Bangkok Grand Palace temple",
    "South Korea": "Seoul Gyeongbokgung palace",
    "Singapore": "Marina Bay Sands Singapore",
    "New Zealand": "Milford Sound New Zealand",
    "Malaysia": "Petronas Towers Kuala Lumpur",
    "Indonesia": "Bali temple rice terrace",
    "Vietnam": "Ha Long Bay Vietnam",
    "Philippines": "Palawan El Nido Philippines",
    "Cambodia": "Angkor Wat Cambodia",
    "Sri Lanka": "Sigiriya rock Sri Lanka",
    "Maldives": "Maldives overwater villas lagoon",
    "Nepal": "Kathmandu Boudhanath stupa Nepal",
    "Bhutan": "Tiger's Nest monastery Bhutan",
    "Qatar": "Doha skyline Qatar",
    "Saudi Arabia": "Riyadh skyline Kingdom Centre",
    "Oman": "Sultan Qaboos Grand Mosque Muscat",
    "Bahrain": "Manama skyline Bahrain",
    "Kuwait": "Kuwait Towers Kuwait City",
    "Mauritius": "Le Morne Mauritius beach",
    "Kenya": "Masai Mara safari Kenya",
    "Egypt": "Pyramids of Giza Egypt",
    "Azerbaijan": "Baku Flame Towers Azerbaijan",
    "Hong Kong": "Hong Kong Victoria Harbour skyline",
    "Uzbekistan": "Registan Samarkand Uzbekistan",
    "Kazakhstan": "Astana Bayterek Kazakhstan",
    "Georgia": "Tbilisi old town Georgia",
    "Russia": "Moscow Red Square Saint Basil",
    "South Africa": "Cape Town Table Mountain",
    "Morocco": "Marrakech Koutoubia Morocco",
    "Brazil": "Rio de Janeiro Christ the Redeemer",
    "China": "Great Wall of China",
    "Taiwan": "Taipei 101 skyline Taiwan",
}


# Banner-only overrides. A query that finds a good portrait can still return
# a poor landscape: Malaysia's came back as the Petronas Towers reflected in
# office glass, Oman's as a close-up of arches, Kuwait's and Brazil's with the
# landmark a distant speck. Reviewed one by one and re-aimed here.
SEARCH_WIDE = {
    "Malaysia": "Kuala Lumpur skyline night",
    "Qatar": "Doha Corniche skyline waterfront",
    "Oman": "Mutrah Corniche Muscat harbour",
    "Kuwait": "Kuwait City skyline towers",
    "Brazil": "Rio de Janeiro Sugarloaf Copacabana beach",
    "Uzbekistan": "Registan square Samarkand madrasah",
    # "Great Wall of China" landscape results crop to open sky.
    "China": "Shanghai skyline Pudong bund",
}


def search_term(name, wide=False):
    if wide and name in SEARCH_WIDE:
        return SEARCH_WIDE[name]
    return SEARCH.get(name, "%s landmark travel" % name)


def fetch(url, key):
    req = Request(url, headers={"Authorization": key,
                                "User-Agent": "visaflighttickets/1.0"})
    return urlopen(req, timeout=30)


def main():
    key = os.environ.get("PEXELS_API_KEY", "").strip()
    if not key:
        print("PEXELS_API_KEY is not set.")
        print("Get a free key at https://www.pexels.com/api/ and set it, then")
        print("re-run. Nothing was downloaded.")
        return 1

    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    credits_path = os.path.join(OUT, "credits.json")
    try:
        with io.open(credits_path, encoding="utf-8") as fh:
            credits = json.load(fh)
    except (IOError, OSError, ValueError):
        credits = {}

    names = []
    for v in content_visa.VISAS:
        if v["short"] not in names:
            names.append(v["short"])

    ok = skipped = failed = 0
    for name in names:
        slug = slugify(name)
        dest = os.path.join(OUT, slug + ".jpg")
        if all(os.path.exists(os.path.join(OUT, slug + x + ".jpg"))
               for x in ("", "-wide", "-wide-sm")):
            skipped += 1
            continue
        try:
            # Portrait for the card tile, landscape for the page banner.
            # Same country, different photo, each framed for its own shape.
            raw = fetch(API % (quote(search_term(name)), "portrait"), key).read()
            hits = json.loads(raw.decode("utf-8")).get("photos") or []
            if not hits:
                print("  no result   %s" % name)
                failed += 1
                continue
            photo = hits[0]
            img = urlopen(Request(photo["src"]["original"] + CROP,
                                  headers={"User-Agent": "visaflighttickets/1.0"}),
                          timeout=30).read()
            with open(dest, "wb") as fh:
                fh.write(img)

            raw_w = fetch(API % (quote(search_term(name, wide=True)), "landscape"), key).read()
            hits_w = json.loads(raw_w.decode("utf-8")).get("photos") or hits
            wide_photo = hits_w[0]
            for suffix, crop in (("-wide", CROP_WIDE), ("-wide-sm", CROP_WIDE_SM)):
                path = os.path.join(OUT, slug + suffix + ".jpg")
                w = urlopen(Request(wide_photo["src"]["original"] + crop,
                                    headers={"User-Agent": "visaflighttickets/1.0"}),
                            timeout=30).read()
                with open(path, "wb") as fh:
                    fh.write(w)

            credits[slug] = {
                "country": name,
                "query": search_term(name),
                "banner_query": search_term(name, wide=True),
                "photographer": photo.get("photographer", ""),
                "photographer_url": photo.get("photographer_url", ""),
                "source": photo.get("url", ""),
                "banner_photographer": wide_photo.get("photographer", ""),
                "banner_source": wide_photo.get("url", ""),
                "licence": "Pexels License - free commercial use",
            }
            # A photographer name outside the console codepage used to raise
            # here - after every file was already written - so the run reported
            # a failure that had actually succeeded. Never let logging decide
            # whether the fetch counted.
            who = photo.get("photographer", "?")
            try:
                print("  ok  %-22s %6.0f KB  by %s" % (name, len(img) / 1024.0, who))
            except UnicodeEncodeError:
                print("  ok  %-22s %6.0f KB  by %s" %
                      (name, len(img) / 1024.0, who.encode("ascii", "replace").decode()))
            ok += 1
            time.sleep(0.6)                # stay well inside the rate limit
        except Exception as exc:           # noqa: BLE001 - report and continue
            print("  FAIL %-22s %s" % (name, exc))
            failed += 1

    with io.open(credits_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(credits, fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write(u"\n")

    print("\n%d downloaded, %d already present, %d failed" % (ok, skipped, failed))
    print("Photos in %s" % OUT)
    print("Provenance recorded in %s" % credits_path)
    print("")
    print("These arrive cropped to the card aspect and already compressed,")
    print("so there is no conversion step. Nothing references them until the")
    print("tile layout is restored from da0b7b7.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
