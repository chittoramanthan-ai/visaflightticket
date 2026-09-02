// =============================================================================
// POST /functions/v1/confirm-upi   { ref, utr }
//
// The customer says they have paid and quotes their UPI reference. This does
// NOT mark the order paid -- nothing a customer types can do that. It moves the
// order to awaiting_verification and emails you to go and check your statement.
//
// That manual step is the whole trade: direct UPI costs you nothing per order,
// and costs you a look at your bank feed instead.
// =============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const ALLOWED_ORIGINS = (Deno.env.get("ALLOWED_ORIGINS") ??
  "https://visaflighttickets.com,https://www.visaflighttickets.com,http://127.0.0.1:8899,http://localhost:8899")
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

const json = (b: unknown, s: number, o: string | null) =>
  new Response(JSON.stringify(b), {
    status: s, headers: { "content-type": "application/json", ...cors(o) },
  });

async function notify(order: Record<string, unknown>) {
  const apiKey = Deno.env.get("RESEND_API_KEY");
  const to = Deno.env.get("NOTIFY_EMAIL");
  if (!apiKey || !to) return;

  const money = `₹${(Number(order.amount_minor) / 100).toFixed(0)}`;
  const row = (k: string, v: unknown) =>
    v ? `<tr><td style="padding:4px 14px 4px 0;color:#667">${k}</td><td style="padding:4px 0"><b>${v}</b></td></tr>` : "";

  const html = `
    <div style="font-family:system-ui,Segoe UI,Arial,sans-serif;font-size:15px;color:#14181b">
      <h2 style="margin:0 0 4px">${order.ref} says paid by UPI</h2>
      <p style="margin:0 0 6px;color:#667">${money} claimed. <b>Not verified.</b></p>
      <p style="margin:0 0 18px;padding:10px 14px;background:#fff7e6;border-left:3px solid #b8860d">
        Check <b>${order.utr}</b> against your bank feed for ${money} before you issue anything.
        A reference typed into a form is a claim, not a payment.
      </p>
      <table style="border-collapse:collapse">
        ${row("UPI reference", order.utr)}
        ${row("Amount claimed", money)}
        ${row("Service", order.service)}
        ${row("Travellers", order.travellers)}
        ${row("Route", [order.origin, order.destination].filter(Boolean).join(" to "))}
        ${row("Depart", order.depart_date)}
        ${row("Return", order.return_date)}
        ${row("Passenger", `${order.surname}, ${order.given_name}`)}
        ${row("Email", order.email)}
        ${row("Phone", order.phone)}
      </table>
      ${order.notes ? `<p style="margin:18px 0 0"><b>Notes</b><br>${String(order.notes).replace(/</g, "&lt;")}</p>` : ""}
      <p style="margin:22px 0 0;font-size:13px;color:#667">Once the money is in your account:<br>
        <code>update orders set status='paid', verified_at=now() where ref='${order.ref}';</code></p>
    </div>`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${apiKey}`, "content-type": "application/json" },
    body: JSON.stringify({
      from: `Visa Flight Tickets <${Deno.env.get("NOTIFY_FROM") ?? "orders@visaflighttickets.com"}>`,
      to: to.split(",").map((s) => s.trim()),
      reply_to: String(order.email ?? ""),
      subject: `[VERIFY] ${order.ref} claims UPI payment of ${money}`,
      html,
    }),
  });
  if (!res.ok) console.error("resend failed", res.status, await res.text());
}

Deno.serve(async (req) => {
  const origin = req.headers.get("origin");
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
  if (req.method !== "POST") return json({ error: "method_not_allowed" }, 405, origin);

  let body: Record<string, unknown>;
  try { body = await req.json(); } catch { return json({ error: "bad_json" }, 400, origin); }

  const ref = String(body.ref ?? "").trim().toUpperCase().slice(0, 20);
  const utr = String(body.utr ?? "").trim().replace(/\s+/g, "").slice(0, 40);

  if (!/^VFT-\d{6}$/.test(ref)) return json({ error: "bad_ref" }, 400, origin);
  // UPI references are 12 digits; some banks emit alphanumerics, so stay loose
  // but insist on something that could plausibly be one.
  if (!/^[A-Za-z0-9]{8,24}$/.test(utr)) return json({ error: "bad_utr" }, 400, origin);

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } },
  );

  const { data: order } = await supabase
    .from("orders").select("*").eq("ref", ref).maybeSingle();

  if (!order) return json({ error: "unknown_ref" }, 404, origin);

  if (order.status === "paid" || order.status === "delivered") {
    return json({ ok: true, status: order.status, already: true }, 200, origin);
  }
  if (order.utr) {
    return json({ ok: true, status: order.status, already: true }, 200, origin);
  }

  const { error: upErr } = await supabase.from("orders").update({
    status: "awaiting_verification",
    utr,
    utr_submitted_at: new Date().toISOString(),
    provider: "upi",
  }).eq("id", order.id);

  if (upErr) {
    // The unique index means a reference already claimed elsewhere is rejected,
    // which is exactly what should happen to a recycled screenshot.
    if (String(upErr.code) === "23505") return json({ error: "utr_already_used" }, 409, origin);
    console.error("utr update failed", upErr);
    return json({ error: "could_not_record" }, 500, origin);
  }

  try {
    await notify({ ...order, utr });
  } catch (e) {
    console.error("notify threw", e);
  }

  return json({ ok: true, status: "awaiting_verification" }, 200, origin);
});
