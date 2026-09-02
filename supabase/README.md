# Backend setup: Supabase + Razorpay + email

> ## Start here
> The payment path is **not live yet**, and until it is, every order fails:
> `create-order` writes a `passengers` column that does not exist until the
> migration below is applied.
>
> 1. Paste **`migrations/APPLY_ME.sql`** into the SQL editor and run it. It is
>    0002 and 0003 combined, idempotent, and ends with a SELECT that should
>    return 5 rows.
> 2. Run **`bash supabase/deploy.sh`** from the repo root for the rest. It
>    checks you are on the right project before it touches anything, then walks
>    through secrets and the three function deploys in the right order.
>
> The sections below are the reference for what those two steps do.

The site stays static. Supabase Edge Functions are the only server, so hosting
does not change.

**Flow:** customer submits the form → `create-order` prices it, saves a `pending`
row and opens a Razorpay order → Razorpay Checkout takes the payment → Razorpay
calls `razorpay-webhook` server-to-server → the row flips to `paid` and you get
an email → the customer lands on `/order/thank-you/?ref=VFT-001234`.

Until `SUPABASE_URL` is set the form falls back to an offline notice, so the site
is never broken while you are setting this up.

---

## 1. Supabase project

```bash
npm i -g supabase
supabase login
supabase link --project-ref <your-project-ref>
supabase db push                       # applies migrations/0001_orders.sql
```

Or paste `migrations/0001_orders.sql` into the SQL editor.

## 2. Choose how you take money

Two modes. `PAYMENT_MODE` picks; `auto` (the default) uses UPI if `UPI_VPA` is
set and no Razorpay key is.

### Direct UPI, zero fees

Customer scans a QR or taps into their UPI app, pays your VPA, then types the
reference back. You check your bank feed and mark it paid.

```bash
supabase secrets set PAYMENT_MODE=upi   UPI_VPA=yourname@okhdfcbank   UPI_PAYEE_NAME="Visa Flight Ticket"
```

Costs nothing per transaction. Costs you a look at your bank feed per order.
Fine at ten orders a day, painful at a hundred.

**Nothing a customer types marks an order paid.** A submitted reference sets
`awaiting_verification` and emails you. Match it against real money before you
issue anything: a UTR box on a web page is a claim, not a payment, and someone
will eventually type a made-up number. The unique index on `utr` stops the same
reference being reused across two orders, but it cannot tell you the money
arrived. Only your bank can.

### Razorpay, automated

~2% + GST, about Rs11.80 on a Rs499 order. Note that UPI's statutory zero MDR
does not help here: MDR is the bank's cut, and Razorpay's 2% is its own
platform fee, charged on UPI as well as cards. New merchants get 90 days at 0%.

Worth it once reconciling by hand costs more of your time than the fee does.

## 3. Secrets

Never in this repo. Set them on the functions:

```bash
supabase secrets set \
  RAZORPAY_KEY_ID=rzp_live_xxxxxxxx \
  RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx \
  RAZORPAY_WEBHOOK_SECRET=whatever-you-set-in-razorpay \
  RESEND_API_KEY=re_xxxxxxxx \
  NOTIFY_EMAIL=you@yourdomain.com \
  NOTIFY_FROM=orders@visaflighttickets.com \
  ALLOWED_ORIGINS=https://visaflighttickets.com,https://www.visaflighttickets.com \
  IP_SALT=$(openssl rand -hex 16)
```

`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are injected automatically.

## 4. Deploy the functions

```bash
supabase functions deploy create-order
supabase functions deploy confirm-upi
supabase functions deploy razorpay-webhook --no-verify-jwt
```

`--no-verify-jwt` on the webhook only. Razorpay does not send a Supabase JWT;
the request is authenticated by its HMAC signature instead, which the function
verifies before touching anything.

## 5. Razorpay webhook (skip if you are on UPI)

Dashboard → Settings → Webhooks → Add:

- **URL** `https://<project-ref>.supabase.co/functions/v1/razorpay-webhook`
- **Secret** the same string you set as `RAZORPAY_WEBHOOK_SECRET`
- **Events** `payment.captured`, `payment.failed`, `order.paid`

## 6. Email

[Resend](https://resend.com) free tier is 3,000/month. Verify your sending
domain, then set `RESEND_API_KEY` and `NOTIFY_EMAIL`. Without a verified domain,
mail lands in spam. `NOTIFY_EMAIL` accepts a comma-separated list.

## 7. Point the site at it

In `src/build.py`:

```python
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi..."
```

Then `python src/build.py`. Both values are public by design: the anon key is an
identifier, not a secret, and RLS denies it every table.

## 8. Test before going live

Razorpay test mode, card `4111 1111 1111 1111`, any future expiry, any CVV.

1. Submit the form → a `pending` row appears with a `VFT-` reference.
2. Pay → the webhook fires → status becomes `paid` → email arrives.
3. **Close the browser mid-payment.** The webhook should still mark it paid.
   This is the case a client-side-only integration gets wrong.

---

## Security notes

Four things here are deliberate, and worth not undoing:

**Pricing is server-side.** `create-order` computes the amount from its own
table and ignores anything the browser sends. If the client supplied the amount,
anyone could open devtools and buy a ₹499 ticket for ₹1.

**RLS is on with no policies for `anon`.** The browser cannot read or write
`orders` at all. Every write goes through a function using the service-role key,
which never leaves the server. The one exception is `order_status_lookup`, a
`security definer` function that returns a single row only to someone who
already knows both the reference *and* the email, and never exposes the amount
or provider ids.

**Only the webhook marks an order paid.** Not the browser callback. A customer
who closes the tab after paying still gets fulfilled, and a customer who fakes
the callback gets nothing. The webhook also re-checks the amount against what
was priced, and is safe to run twice because Razorpay retries.

**Signature verification is constant-time.** `safeEqual` compares the full
string rather than bailing on the first mismatched byte.

### Prices live in two places

`P_FLIGHT`, `P_HOTEL` and `BUNDLE_SAVING` in `create-order/index.ts` must match
`PRICE_*` in `src/build.py`. They are deliberately not shared: the server must
not trust anything the site publishes. Change one, change the other, and re-run
the test flow.

**Flights are priced per leg.** One way is one leg, a return is two, multi-city
is one per flight:

```
flight = P_FLIGHT x legs x travellers
hotel  = P_HOTEL x travellers
both   = (P_FLIGHT x legs + P_HOTEL - BUNDLE_SAVING) x travellers
```

The server derives `legs` from the itinerary it was sent, not from a leg count
the browser supplies, for the same reason it does not accept a total: otherwise
a return could be submitted priced as a one way.

## Useful queries

```sql
-- today's paid orders, newest first
select ref, service, travellers, amount_minor/100 as rupees, email, created_at
from orders where status = 'paid' and created_at > now() - interval '1 day'
order by created_at desc;

-- mark one delivered once you have sent the PDF
update orders set status = 'delivered', delivered_at = now(), pnr = 'K7QX2M'
where ref = 'VFT-001234';

-- abandoned checkouts worth chasing
select ref, email, created_at from orders
where status = 'pending' and created_at < now() - interval '1 hour';
```
