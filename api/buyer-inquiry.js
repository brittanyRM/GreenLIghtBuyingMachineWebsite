// api/buyer-inquiry.js
//
// Buyer list qualification. Forwards to a GoHighLevel inbound webhook
// server-side, same reasoning as the other handlers: GHL webhook
// endpoints don't return CORS headers, and the URL is unauthenticated
// so it must stay out of the client.
//
// Required env var: GHL_BUYER_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED = ["name", "email", "funding", "timeline"];

function clean(value) {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const webhook = process.env.GHL_BUYER_WEBHOOK_URL;
  if (!webhook) {
    console.error("GHL_BUYER_WEBHOOK_URL is not set");
    return res.status(500).json({ error: "Form is not configured" });
  }

  const body = typeof req.body === "string" ? safeParse(req.body) : req.body || {};
  if (!body) return res.status(400).json({ error: "Invalid request" });

  if (clean(body.company)) return res.status(200).json({ ok: true });

  const missing = REQUIRED.filter((field) => !clean(body[field]));
  if (missing.length) {
    return res.status(400).json({ error: `Missing required fields: ${missing.join(", ")}` });
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: "Enter a valid email address" });
  }

  const fullName = clean(body.name);
  const [firstName, ...rest] = fullName.split(/\s+/);

  const funding = clean(body.funding);
  const timeline = clean(body.timeline);

  // Rough triage so the workflow can branch without re-deriving it.
  // Anything not clearly ready goes to nurture rather than to a call.
  const readyFunding = ["Cash", "Conventional or DSCR financing", "1031 exchange", "Partnership or fund"];
  const readyTimeline = ["Ready now", "Next 3 months"];
  const buyerTier =
    readyFunding.includes(funding) && readyTimeline.includes(timeline)
      ? "core"
      : funding === "Still figuring it out" || timeline === "Just researching"
        ? "nurture"
        : "review";

  const payload = {
    first_name: firstName,
    last_name: rest.join(" "),
    full_name: fullName,
    email,
    phone: clean(body.phone),
    buyer_funding: funding,
    buyer_timeline: timeline,
    buyer_portfolio: clean(body.portfolio),
    buyer_criteria: clean(body.notes),
    buyer_tier: buyerTier,
    source: clean(body.source) || "buyer list",
    page: clean(body.page),
    submitted_at: new Date().toISOString(),
  };

  try {
    const upstream = await fetch(webhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(10000),
    });

    if (!upstream.ok) {
      const detail = await upstream.text().catch(() => "");
      console.error("GHL buyer webhook rejected submission", upstream.status, detail);
      return res.status(502).json({ error: "Could not submit right now" });
    }
  } catch (error) {
    console.error("GHL buyer webhook unreachable", error);
    return res.status(502).json({ error: "Could not submit right now" });
  }

  return res.status(200).json({ ok: true });
}

function safeParse(text) {
  try {
    return JSON.parse(text);
  } catch {
    return null;
  }
}
