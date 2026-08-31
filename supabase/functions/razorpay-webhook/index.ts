// =============================================================================
// POST /functions/v1/razorpay-webhook
//
// The only thing that may mark an order paid. Razorpay calls this server to
// server, so it cannot be spoofed by a customer closing the browser at the
// right moment -- and it still fires if they do.
//
// Deploy with --no-verify-jwt (Razorpay does not send a Supabase JWT):
//   supabase functions deploy razorpay-webhook --no-verify-jwt
// =============================================================================
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.4";

const enc = new TextEncoder();

/** Constant-time compare, so we do not leak the signature a byte at a time. */
function safeEqual(a: string, b: string) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function hmacHex(secret: string, payload: string) {
  const key = await crypto.subtle.importKey(
    "raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"],
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(payload));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

async function notify(order: Record<string, unknown>) {
  const apiKey = Deno.env.get("RESEND_API_KEY");
  const to = Deno.env.get("NOTIFY_EMAIL");
  const from = Deno.env.get("NOTIFY_FROM") ?? "orders@visaflightticket.com";
  if (!apiKey || !to) {
    console.log("email not configured, skipping notification");
    return;
  }

  const money = `₹${(Number(order.amount_minor) / 100).toFixed(0)}`;
  const row = (k: string, v: unknown) =>
    v ? `<tr><td style="padding:4px 14px 4px 0;color:#667">${k}</td><td style="padding:4px 0"><b>${v}</b></td></tr>` : "";

  const html = `
    <div style="font-family:system-ui,Segoe UI,Arial,sans-serif;font-size:15px;color:#14181b">
      <h2 style="margin:0 0 4px">New paid order ${order.ref}</h2>
      <p style="margin:0 0 18px;color:#667">${money} received via Razorpay.</p>
      <table style="border-collapse:collapse">
        ${row("Service", order.service)}
        ${row("Travellers", order.travellers)}
        ${row("Route", [order.origin, order.destination].filter(Boolean).join(" to "))}
        ${row("Depart", order.depart_date)}
        ${row("Return", order.return_date)}
        ${row("Trip", order.trip)}
        ${row("Passenger", `${order.surname}, ${order.given_name}`)}
        ${row("Date of birth", order.dob)}
        ${row("Email", order.email)}
        ${row("Phone", order.phone)}
        ${row("Visa", order.visa_type)}
        ${row("Payment id", order.provider_payment_id)}
      </table>
      ${Array.isArray(order.passengers) && order.passengers.length > 1
        ? `<p style="margin:18px 0 6px"><b>All travellers</b></p><ol style="margin:0;padding-left:20px">` +
          (order.passengers as Array<Record<string, string>>).map((p) =>
            `<li>${p.surname}, ${p.given_name}${p.dob ? ` (${p.dob})` : ""}</li>`).join("") + `</ol>`
        : ""}
      ${order.notes ? `<p style="margin:18px 0 0"><b>Notes</b><br>${String(order.notes).replace(/</g, "&lt;")}</p>` : ""}
      ${Array.isArray(order.legs) && order.legs.length
        ? `<p style="margin:14px 0 0"><b>Extra legs</b><br><code>${JSON.stringify(order.legs)}</code></p>` : ""}
    </div>`;

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { authorization: `Bearer ${apiKey}`, "content-type": "application/json" },
    body: JSON.stringify({
      from: `Visa Flight Ticket <${from}>`,
      to: to.split(",").map((s) => s.trim()),
      reply_to: String(order.email ?? ""),
      subject: `New order ${order.ref} - ${money}`,
      html,
    }),
  });
  if (!res.ok) console.error("resend failed", res.status, await res.text());
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("method_not_allowed", { status: 405 });

  const secret = Deno.env.get("RAZORPAY_WEBHOOK_SECRET");
  if (!secret) return new Response("not_configured", { status: 500 });

  const raw = await req.text();                       // verify the exact bytes sent
  const signature = req.headers.get("x-razorpay-signature") ?? "";
  const expected = await hmacHex(secret, raw);
  if (!safeEqual(signature, expected)) {
    console.warn("bad webhook signature");
    return new Response("bad_signature", { status: 401 });
  }

  const event = JSON.parse(raw);
  const kind = event?.event as string | undefined;
  const payment = event?.payload?.payment?.entity;
  if (!payment?.order_id) return new Response("ignored", { status: 200 });

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    { auth: { persistSession: false } },
  );

  const { data: order } = await supabase
    .from("orders").select("*")
    .eq("provider_order_id", payment.order_id).maybeSingle();

  if (!order) {
    console.warn("no order for", payment.order_id);
    return new Response("unknown_order", { status: 200 });
  }

  if (kind === "payment.failed") {
    await supabase.from("orders").update({ status: "failed" }).eq("id", order.id);
    return new Response("ok", { status: 200 });
  }

  if (kind !== "payment.captured" && kind !== "order.paid") {
    return new Response("ignored", { status: 200 });
  }

  // Razorpay retries on any non-2xx, so this has to be safe to run twice.
  if (order.status === "paid" || order.status === "delivered") {
    return new Response("already_processed", { status: 200 });
  }

  // Never trust the amount in the callback over the one we priced.
  if (Number(payment.amount) !== Number(order.amount_minor)) {
    console.error("amount mismatch", payment.amount, order.amount_minor);
    await supabase.from("orders").update({ status: "failed" }).eq("id", order.id);
    return new Response("amount_mismatch", { status: 200 });
  }

  const { data: updated } = await supabase
    .from("orders")
    .update({
      status: "paid",
      provider_payment_id: payment.id,
      paid_at: new Date().toISOString(),
    })
    .eq("id", order.id)
    .select("*")
    .single();

  try {
    await notify(updated ?? order);
  } catch (e) {
    console.error("notify threw", e);   // never fail the webhook over an email
  }

  return new Response("ok", { status: 200 });
});
