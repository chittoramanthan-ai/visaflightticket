# Visa Flight Ticket

Static website for a verifiable flight-reservation and hotel-booking service for visa applicants.
40 pages, no build dependencies, no JavaScript framework, no external requests.

**Live positioning:** real airline-held reservations with a live PNR the applicant can verify themselves —
explicitly *not* fabricated PDFs. That distinction is the site's core message and its main SEO moat.

---

## Build

```bash
python src/build.py
```

Requires Python 3 only — no packages. It writes plain HTML into the repo root. Commit the generated
output; the host serves it directly.

```bash
python -m http.server 8899   # then open http://127.0.0.1:8899
```

## Layout

```
src/build.py          engine: page shell, SEO head, JSON-LD, sitemap, components, ALL CONFIG
src/content_core.py   home, service pages, pricing, how-it-works, verify, order, FAQ, legal
src/content_visa.py   12 destination landing pages (data-driven — add a dict, get a page)
src/content_blog.py   10 long-form posts + blog index
assets/css/style.css  design system (boarding-pass cards, light/dark, container queries)
assets/js/main.js     mobile nav, theme toggle, live price calc. ~2KB, no dependencies.
```

Everything else in the root is **generated**. Do not hand-edit `index.html`, `sitemap.xml`, `robots.txt`,
`404.html` or any `*/index.html` — your changes will be overwritten on the next build.

## Configuration

All of it lives in the top ~50 lines of `src/build.py`:

| Setting | Purpose |
|---|---|
| `SITE_URL` | Canonical domain. Used by canonicals, OG tags, sitemap, JSON-LD. **Set this before launch.** |
| `BASE_PATH` | Leave `""` for a custom domain. Set to `"/reponame"` only for a GitHub *project* page. |
| `EMAIL`, `WHATSAPP` | Contact details — currently placeholders. |
| `PRICE_FLIGHT` / `PRICE_HOTEL` / `PRICE_BOTH` / `PRICE_RUSH` | Prices, propagated to copy, tables and Product schema. |
| `SINCE_YEAR`, `FLIGHTS_BOOKED`, `VISAS_HELPED`, `AIRLINE_COUNT` | Trust statistics. Set any to `""` to hide it site-wide. |
| `IATA_ACCREDITED`, `IATA_NUMBER` | IATA badge. Set `False` to remove it everywhere. |
| `AIRLINES` | Carrier names shown in the "100+ airlines" strip. |

---

## ⚠️ Read before going live

The site publishes several **factual claims** as fact. They are wired to config so you can change or
remove them in one line, but you are responsible for their accuracy:

1. **"IATA Certified Agent"** — IATA accreditation is verifiable against IATA's own public register, and
   IATA actively polices misuse of its name. If you hold it, **put your accreditation number in
   `IATA_NUMBER`** — an unnumbered badge is a weak trust signal *and* looks evasive. If you do not hold
   it, set `IATA_ACCREDITED = False`. A TIDS code is not full accreditation; say "IATA TIDS registered"
   instead if that is what you have.
2. **"Since 2017", "10 lakh+ flights booked", "50,000+ travellers"** — if the business cannot evidence
   these, blank them. Unverifiable statistics are exactly the pattern Google's spam and site-reputation
   systems penalise, and in most markets they are actionable under consumer-protection law.
3. **Airline logos.** The marquee now ships real brand marks, downloaded by
   `python src/fetch_logos.py` into `assets/img/airlines/<slug>.png` and picked up
   automatically by `_logo_file()` at build time. Carriers with no file fall back to a
   text wordmark, so partial coverage degrades cleanly and there are no 404s.
   To change the roster: edit `AIRLINES` in `src/build.py`, add the IATA code to `CODES`
   in `src/fetch_logos.py`, run the fetcher, rebuild.
   **These are third-party trademarks.** Fetching them does not grant a licence to
   display them, and most carrier brand guidelines prohibit use that implies
   partnership — which is how a logo wall on a booking site reads. A disclaimer sits
   under the strip, but that is mitigation, not permission. Confirm your position
   (reseller/consolidator agreement, IATA accreditation terms) before going live. To
   revert to names only, delete `assets/img/airlines/*.png` and rebuild.
   **Keep the roster current** — it claims these are carriers you book on. Defunct or
   rebranded airlines are a live accuracy risk: IATA reassigns codes, so a dead
   carrier's slug can silently pull an unrelated logo.

4. **No testimonials or review counts are included.** Deliberately: fabricated reviews are the fastest
   way to lose a Google Business Profile and attract an FTC/ASA complaint. Add real ones once you have
   them, with `Review`/`AggregateRating` schema pointing at a real review platform.
5. **Legal pages are drafts.** `terms/`, `privacy-policy/` and `refund-policy/` are written for a service
   of this type but must be reviewed by a lawyer in your jurisdiction, and the bracketed placeholders
   (registered entity, address, governing law) filled in.
6. **The order form is not connected to a payment processor.** It calculates a price and shows a notice.
   Point it at Stripe / PayPal / Razorpay before taking traffic.

## Deployment

Any static host. The site is root-relative, so a custom domain is the intended setup.

- **Cloudflare Pages / Netlify / Vercel** — connect the repo, no build command, publish directory `/`.
- **GitHub Pages** — Settings → Pages → deploy from `main` / root. Add a `CNAME` file with your domain.
  If you use `user.github.io/visaflightticket/` instead, set `BASE_PATH = "/visaflightticket"` and rebuild.

Then:

1. Point the domain, enable HTTPS.
2. Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
3. Validate structured data at <https://search.google.com/test/rich-results> — the FAQ, HowTo, Product
   and Breadcrumb blocks should all parse.

## SEO notes

Already implemented:

- Canonical URLs, OG + Twitter cards, per-page meta descriptions, one `<h1>` per page.
- JSON-LD: `Organization`, `WebSite`, `Service`, `Product`/`Offer`, `FAQPage`, `HowTo`, `BlogPosting`,
  `BreadcrumbList`, `ItemList` — all generated from the same source as the visible copy, so they can't drift.
- `sitemap.xml` with per-page priority and changefreq; `robots.txt` allowing AI answer engines
  (a meaningful and growing referral source in this niche).
- Fast by construction: one 20KB stylesheet, one 2KB script, zero external requests, zero web fonts.
- Internal linking: service pages ↔ visa guides ↔ blog cluster, all three directions.

Highest-value next steps, in order:

1. **Real reviews** on Google Business Profile and Trustpilot, then `AggregateRating` schema.
2. **More destination pages** — add dicts to `VISAS` in `src/content_visa.py`. Each is a long-tail entry
   point. Obvious gaps: China, Vietnam, Indonesia, Saudi Arabia, Egypt, Morocco, South Africa, Brazil.
3. **Currency/locale variants** for India, Nigeria, Philippines, Pakistan — the largest search markets
   for this term.
4. **Backlinks** from travel-forum answers, immigration-advice sites and student-visa communities.
   This niche is won on links and trust, not on keyword density.
5. Set `dateModified` genuinely — refresh guides when consular rules change and let the date reflect it.
