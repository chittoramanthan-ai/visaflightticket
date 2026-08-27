# -*- coding: utf-8 -*-
"""
One-off helper: download airline marks into assets/img/airlines/.

    python src/fetch_logos.py

Deliberately NOT part of build.py -- builds stay offline and deterministic.
Run this once, commit the files, and every later build picks them up via
_logo_file() in build.py. Carriers that fail to download simply keep their
text wordmark in the marquee, so partial coverage degrades cleanly.

Note on rights: these are third-party trademarks fetched from a public CDN.
Downloading them does not grant you a licence to display them. Confirm your
own position before shipping to production -- see README.
"""

import os
import sys
import time

try:
    from urllib.request import urlopen, Request
except ImportError:                                   # pragma: no cover
    from urllib2 import urlopen, Request              # type: ignore

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import AIRLINES, slugify, ROOT             # noqa: E402

SIZE = 128
SRC = "https://images.kiwi.com/airlines/%d/%%s.png" % SIZE
OUT = os.path.join(ROOT, "assets", "img", "airlines")

# Airline name -> IATA designator. Marketing names differ from the register,
# so this cannot be derived; it has to be a table.
CODES = {
    "Batik Air Malaysia": "OD",
    "Malaysia Airlines": "MH",
    "Pegasus Airlines": "PC",
    "IndiGo": "6E",
    "Turkish Airlines": "TK",
    "Etihad Airways": "EY",
    "FlyBaghdad": "IF",
    "Air India": "AI",
    "Oman Air": "WY",
    "Air Sial": "PF",
    "Emirates": "EK",
    "British Airways": "BA",
    "Virgin Atlantic": "VS",
    "Qatar Airways": "QR",
    "SalamAir": "OV",
    "Iran Air": "IR",
    "China Southern": "CZ",
    "Saudia": "SV",
    "Thai Airways": "TG",
    "Air China": "CA",
    "Pakistan International Airlines": "PK",
    "flydubai": "FZ",
    "American Airlines": "AA",
    "flynas": "XY",
    "Air Arabia": "G9",
    "Jazeera Airways": "J9",
    "SriLankan Airlines": "UL",
    "Gulf Air": "GF",
    "Fly Jinnah": "9P",
    "Singapore Airlines": "SQ",
    "Kam Air": "RQ",
    "Kuwait Airways": "KU",
    "airblue": "PA",
    "Mahan Air": "W5",
    "Air Mauritius": "MK",
    "SereneAir": "ER",
    "Cham Wings Airlines": "6Q",
    "Taban Airlines": "HH",
    "SpiceJet": "SG",
    "Iraqi Airways": "IA",
    "Uzbekistan Airways": "HY",
    "Lufthansa": "LH",
}

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fetch(code):
    req = Request(SRC % code, headers={"User-Agent": "Mozilla/5.0 (logo-fetch)"})
    data = urlopen(req, timeout=15).read()
    if not data.startswith(PNG_MAGIC):
        raise ValueError("not a PNG (%d bytes)" % len(data))
    if len(data) < 300:
        raise ValueError("suspiciously small (%d bytes)" % len(data))
    return data


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    got, missed = [], []

    for name in AIRLINES:
        code = CODES.get(name, "")
        dest = os.path.join(OUT, slugify(name) + ".png")
        if not code:
            missed.append((name, "no IATA code"))
            continue
        if os.path.exists(dest):
            got.append(name)
            continue
        try:
            data = fetch(code)
        except Exception as exc:
            missed.append((name, str(exc)[:48]))
            continue
        with open(dest, "wb") as fh:
            fh.write(data)
        got.append(name)
        time.sleep(0.12)                      # be polite to the CDN

    print("Downloaded/present: %d of %d" % (len(got), len(AIRLINES)))
    if missed:
        print("Kept as wordmarks:")
        for name, why in missed:
            print("   %-34s %s" % (name, why))
    print("\nRun `python src/build.py` to pick them up.")


if __name__ == "__main__":
    main()
