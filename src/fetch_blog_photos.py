# -*- coding: utf-8 -*-
"""
One-off helper: download one illustrating photo per blog post into
assets/img/blog/.

    set PEXELS_API_KEY=...        (Windows)
    export PEXELS_API_KEY=...     (bash)
    python src/fetch_blog_photos.py

Deliberately NOT part of build.py, matching fetch_logos.py and
fetch_country_photos.py: builds stay offline and deterministic.

Two crops per post, because the article column is about 720px and most of
this traffic is on a phone. Both are lazy-loaded and sit below the first
section, so neither is ever the LCP element - which is the whole reason a
blog image can be free where a hero image is not.

Note on rights: Pexels grants free commercial use, modification allowed,
attribution optional. Photographer and source are recorded per image in
assets/img/blog/credits.json regardless, so provenance can be answered later.
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
from build import ROOT                                # noqa: E402
import content_blog                                   # noqa: E402

OUT = os.path.join(ROOT, "assets", "img", "blog")
API = "https://api.pexels.com/v1/search?query=%s&per_page=3&orientation=landscape"
CROP = "?cs=tinysrgb&fit=crop&w=800&h=360"
CROP_SM = "?cs=tinysrgb&fit=crop&w=480&h=216"

# A post is about a process, not a place, so the subject has to be chosen by
# hand. "dummy ticket" returns nothing useful; what illustrates it is the
# counter where the document gets checked.
SUBJECT = {
    "what-is-a-dummy-ticket": "airline check in counter airport",
    "is-a-dummy-ticket-legal": "passport and documents on desk",
    # A departure board is dense small text, which JPEG encodes terribly:
    # the first pick came back at 600 KB for an 800x360 crop.
    "flight-reservation-vs-confirmed-ticket": "airplane wing window clouds",
    "proof-of-onward-travel-explained": "airport boarding gate queue",
    "how-long-is-a-flight-reservation-valid": "airport clock terminal",
    "do-embassies-verify-flight-bookings": "office computer screen work desk",
    "hotel-booking-for-visa-application": "hotel reception lobby desk",
    "visa-application-document-checklist": "paperwork documents folder desk",
    "common-visa-rejection-reasons": "person reading documents worried desk",
    "how-to-choose-a-dummy-ticket-service": "laptop travel planning desk",
    "schengen-visa-appointment-flight-reservation": "european city street travel",
    "do-embassies-call-the-airline": "telephone handset office desk",
    "dummy-ticket-vs-refundable-ticket": "wallet money travel budget",
    "thailand-new-rules-for-indian-travellers": "bangkok thailand temple travel",
}


def subject(slug):
    return SUBJECT.get(slug, "travel documents desk")


def fetch(url, key):
    return urlopen(Request(url, headers={"Authorization": key,
                                         "User-Agent": "visaflighttickets/1.0"}),
                   timeout=30)


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

    ok = skipped = failed = 0
    for post in content_blog.POSTS:
        slug = post["slug"]
        if all(os.path.exists(os.path.join(OUT, slug + x + ".jpg"))
               for x in ("", "-sm")):
            skipped += 1
            continue
        try:
            raw = fetch(API % quote(subject(slug)), key).read()
            hits = json.loads(raw.decode("utf-8")).get("photos") or []
            if not hits:
                print("  no result   %s" % slug)
                failed += 1
                continue
            photo = hits[0]
            total = 0
            for suffix, crop in (("", CROP), ("-sm", CROP_SM)):
                d = urlopen(Request(photo["src"]["original"] + crop,
                                    headers={"User-Agent": "visaflighttickets/1.0"}),
                            timeout=30).read()
                with open(os.path.join(OUT, slug + suffix + ".jpg"), "wb") as fh:
                    fh.write(d)
                total += len(d)
            credits[slug] = {
                "query": subject(slug),
                "photographer": photo.get("photographer", ""),
                "photographer_url": photo.get("photographer_url", ""),
                "source": photo.get("url", ""),
                "licence": "Pexels License - free commercial use",
            }
            who = photo.get("photographer", "?")
            try:
                print("  ok  %-46s %5.0f KB  by %s" % (slug, total / 1024.0, who))
            except UnicodeEncodeError:
                print("  ok  %-46s %5.0f KB  by %s"
                      % (slug, total / 1024.0, who.encode("ascii", "replace").decode()))
            ok += 1
            time.sleep(0.6)
        except Exception as exc:                       # noqa: BLE001
            print("  FAIL %-45s %s" % (slug, exc))
            failed += 1

    with io.open(credits_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(credits, fh, indent=1, sort_keys=True, ensure_ascii=False)
        fh.write(u"\n")

    print("\n%d downloaded, %d already present, %d failed" % (ok, skipped, failed))
    print("Photos in %s" % OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
