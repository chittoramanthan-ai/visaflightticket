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
API = "https://api.pexels.com/v1/search?query=%s&per_page=3&orientation=portrait"
CROP = "?auto=compress&cs=tinysrgb&fit=crop&w=440&h=560"

# A bare country name returns flags, maps and food as often as a skyline.
# Anything not listed here falls back to "<name> landmark travel".
SEARCH = {
    "Schengen": "Paris Eiffel Tower",
    "United States": "New York skyline",
    "United Kingdom": "London Tower Bridge",
    "UAE": "Dubai skyline",
    "South Korea": "Seoul city",
    "New Zealand": "New Zealand mountains landscape",
    "Sri Lanka": "Sigiriya Sri Lanka",
    "Czech Republic": "Prague old town",
}


def search_term(name):
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
        if os.path.exists(dest):
            skipped += 1
            continue
        try:
            raw = fetch(API % quote(search_term(name)), key).read()
            hits = json.loads(raw.decode("utf-8")).get("photos") or []
            if not hits:
                print("  no result   %s" % name)
                failed += 1
                continue
            photo = hits[0]
            # Ask the CDN to crop and compress to the card aspect rather than
            # pulling a full-size original and processing it here. Pillow is not
            # installed and does not need to be: this arrives at roughly 30 KB,
            # already the right shape, so there is no conversion step to forget.
            # 440x560 covers a 220px card at 2x.
            src = photo["src"]["original"] + CROP
            img = urlopen(Request(src, headers={"User-Agent": "visaflighttickets/1.0"}),
                          timeout=30).read()
            with open(dest, "wb") as fh:
                fh.write(img)
            credits[slug] = {
                "country": name,
                "photographer": photo.get("photographer", ""),
                "photographer_url": photo.get("photographer_url", ""),
                "source": photo.get("url", ""),
                "licence": "Pexels License - free commercial use",
            }
            print("  ok  %-22s %6.0f KB  by %s" %
                  (name, len(img) / 1024.0, photo.get("photographer", "?")))
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
