// =============================================================================
// POST /functions/v1/create-order
//
// Takes the order form payload, prices it HERE (never from the browser),
// writes a pending row, opens a Razorpay order, and returns just enough for
// Checkout to run: the reference, the amount, and the provider order id.
// =============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

// --- prices, in minor units (paise). The single source of truth. ------------
// Must match PRICE_* in src/build.py. If you change one, change both.
const PRICE = { flight: 49900, hotel: 39900, both: 79900 } as const;
const PRIORITY_FEE = 19900;
const MAX_TRAVELLERS = 12;

// "razorpay" | "upi" | "none".  upi = customer pays your VPA directly, you
// verify by hand. Costs nothing per transaction; costs you reconciliation time.
const PAYMENT_MODE = (Deno.env.get("PAYMENT_MODE") ?? "auto").toLowerCase();
const UPI_VPA = Deno.env.get("UPI_VPA") ?? "";
const UPI_NAME = Deno.env.get("UPI_PAYEE_NAME") ?? "Visa Flight Ticket";

const ALLOWED_ORIGINS = (Deno.env.get("ALLOWED_ORIGINS") ??
  "https://visaflightticket.com,https://www.visaflightticket.com,http://127.0.0.1:8899,http://localhost:8899")
  .split(",").map((s) => s.trim());

function cors(origin: string | null) {
  const ok = origin && ALLOWED_ORIGINS.includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin! : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Headers": "content-type, authorization, apikey",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Vary": "Origin",
  };
}

const json = (body: unknown, status: number, origin: string | null) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...cors(origin) },
  });

const str = (v: unknown, max = 200) =>
  typeof v === "string" ? v.trim().slice(0, max) : "";

const isEmail = (v: string) => /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v);
const isDate = (v: string) => /^\d{4}-\d{2}-\d{2}$/.test(v);

async function sha256Hex(input: string) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(input));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return json({ error: "bad_json" }, 400, origin);
  }

  // --- validate ------------------------------------------------------------
  const service = str(body.service, 10);
  if (!(service in PRICE)) return json({ error: "bad_service" }, 400, origin);

  const trip = ["oneway", "round", "multi"].includes(str(body.trip, 10))
    ? str(body.trip, 10) : "oneway";

  // Passengers drive the count, and the count drives the price. Derive it from
  // the array we were given rather than trusting a separate number field: if
  // those two could disagree, someone could send five names and pay for one.
  const rawPax = Array.isArray(body.passengers) ? body.passengers : [];
  const passengers = rawPax
    .slice(0, MAX_TRAVELLERS)
    .map((p: Record<string, unknown>) => ({
      surname: str(p?.surname, 80),
      given_name: str(p?.given_name, 80),
      dob: isDate(str(p?.dob, 10)) ? str(p?.dob, 10) : null,
    }))
    .filter((p) => p.surname || p.given_name);

  const travellers = Math.min(
    Math.max(passengers.length || parseInt(String(body.travellers ?? 1), 10) || 1, 1),
    MAX_TRAVELLERS,
  );
  const priority = body.priority === true;

  const surname = passengers[0]?.surname || str(body.surname, 80);
  const given = passengers[0]?.given_name || str(body.given_name, 80);
  const email = str(body.email, 160).toLowerCase();
  if (!surname || !given) return json({ error: "name_required" }, 400, origin);
  if (!isEmail(email)) return json({ error: "bad_email" }, 400, origin);

  const depart = str(body.depart_date, 10);
  const ret = str(body.return_date, 10);
  if (depart && !isDate(depart)) return json({ error: "bad_depart" }, 400, origin);
  if (ret && !isDate(ret)) return json({ error: "bad_return" }, 400, origin);
  if (depart && ret && ret < depart) return json({ error: "return_before_depart" }, 400, origin);

  let legs: unknown[] = [];
  if (Array.isArray(body.legs)) legs = body.legs.slice(0, 4);

  // --- price it ourselves --------------------------------------------------
  const amount_minor =
    PRICE[service as keyof typeof PRICE] * travellers + (priority ? PRIORITY_FEE : 0);

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } },
  );

  const ipHash = await sha256Hex(
    (req.headers.get("x-forwarded-for") ?? "") + (Deno.env.get("IP_SALT") ?? "vft"),
  );

  const { data: order, error } = await supabase
    .from("orders")
    .insert({
      service, trip, travellers, priority,
      origin: str(body.origin, 120),
      destination: str(body.destination, 120),
      depart_date: depart || null,
      return_date: ret || null,
      legs,
      visa_type: str(body.visa_type, 120),
      surname, given_name: given,
      passengers,
      dob: isDate(str(body.dob, 10)) ? str(body.dob, 10) : null,
      email,
      phone: str(body.phone, 40),
      notes: str(body.notes, 2000),
      currency: "INR",
      amount_minor,
      status: "pending",
      provider: "razorpay",
      user_agent: str(req.headers.get("user-agent") ?? "", 300),
      ip_hash: ipHash,
    })
    .select("id, ref, amount_minor, currency")
    .single();

  if (error || !order) {
    console.error("insert failed", error);
    return json({ error: "could_not_create_order" }, 500, origin);
  }

  // --- direct UPI: no gateway, no percentage ------------------------------
  const wantUpi = PAYMENT_MODE === "upi" ||
    (PAYMENT_MODE === "auto" && UPI_VPA && !Deno.env.get("RAZORPAY_KEY_ID"));

  if (wantUpi && UPI_VPA) {
    const rupees = (amount_minor / 100).toFixed(2);
    // NPCI deep link. tn carries the reference so it lands in your statement.
    const uri = "upi://pay?pa=" + encodeURIComponent(UPI_VPA) +
      "&pn=" + encodeURIComponent(UPI_NAME) +
      "&am=" + rupees + "&cu=INR" +
      "&tn=" + encodeURIComponent(order.ref);
    await supabase.from("orders").update({ provider: "upi" }).eq("id", order.id);
    return json({
      ref: order.ref, amount_minor, currency: "INR",
      payment_configured: true, method: "upi",
      upi: { uri, vpa: UPI_VPA, payee: UPI_NAME, amount: rupees },
    }, 200, origin);
  }

  // --- open the Razorpay order --------------------------------------------
  const keyId = Deno.env.get("RAZORPAY_KEY_ID");
  const keySecret = Deno.env.get("RAZORPAY_KEY_SECRET");
  if (!keyId || !keySecret) {
    // Payments not configured yet: the order still exists and you still get
    // the email, so the site is usable while keys are being sorted out.
    return json({
      ref: order.ref, amount_minor, currency: "INR", payment_configured: false,
    }, 200, origin);
  }

  const rp = await fetch("https://api.razorpay.com/v1/orders", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: "Basic " + btoa(`${keyId}:${keySecret}`),
    },
    body: JSON.stringify({
      amount: amount_minor,
      currency: "INR",
      receipt: order.ref,
      notes: { ref: order.ref, service, travellers: String(travellers) },
    }),
  });

  if (!rp.ok) {
    console.error("razorpay order failed", rp.status, await rp.text());
    await supabase.from("orders").update({ status: "failed" }).eq("id", order.id);
    return json({ error: "payment_init_failed" }, 502, origin);
  }

  const rpOrder = await rp.json();
  await supabase.from("orders")
    .update({ provider_order_id: rpOrder.id })
    .eq("id", order.id);

  return json({
    ref: order.ref,
    amount_minor,
    currency: "INR",
    payment_configured: true,
    method: "razorpay",
    key_id: keyId,                 // publishable, safe in the browser
    provider_order_id: rpOrder.id,
  }, 200, origin);
});
