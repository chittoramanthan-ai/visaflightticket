# Backend setup: Supabase + Razorpay + email

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

## 2. Secrets

Never in this repo. Set them on the functions:

```bash
supabase secrets set \
  RAZORPAY_KEY_ID=rzp_live_xxxxxxxx \
  RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxx \
  RAZORPAY_WEBHOOK_SECRET=whatever-you-set-in-razorpay \
  RESEND_API_KEY=re_xxxxxxxx \
  NOTIFY_EMAIL=you@yourdomain.com \
  NOTIFY_FROM=orders@visaflightticket.com \
  ALLOWED_ORIGINS=https://visaflightticket.com,https://www.visaflightticket.com \
  IP_SALT=$(openssl rand -hex 16)
```

`SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are injected automatically.

## 3. Deploy the functions

```bash
supabase functions deploy create-order
supabase functions deploy razorpay-webhook --no-verify-jwt
```

`--no-verify-jwt` on the webhook only. Razorpay does not send a Supabase JWT;
the request is authenticated by its HMAC signature instead, which the function
verifies before touching anything.

## 4. Razorpay webhook

Dashboard → Settings → Webhooks → Add:

- **URL** `https://<project-ref>.supabase.co/functions/v1/razorpay-webhook`
- **Secret** the same string you set as `RAZORPAY_WEBHOOK_SECRET`
- **Events** `payment.captured`, `payment.failed`, `order.paid`

## 5. Email

[Resend](https://resend.com) free tier is 3,000/month. Verify your sending
domain, then set `RESEND_API_KEY` and `NOTIFY_EMAIL`. Without a verified domain,
mail lands in spam. `NOTIFY_EMAIL` accepts a comma-separated list.

## 6. Point the site at it

In `src/build.py`:

```python
SUPABASE_URL = "https://xxxxxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOi..."
```

Then `python src/build.py`. Both values are public by design: the anon key is an
identifier, not a secret, and RLS denies it every table.

## 7. Test before going live

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

`PRICE` in `create-order/index.ts` must match `PRICE_*` in `src/build.py`.
They are deliberately not shared: the server must not trust anything the site
publishes. Change one, change the other, and re-run the test flow.

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
