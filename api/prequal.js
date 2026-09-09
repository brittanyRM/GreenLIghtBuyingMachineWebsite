// api/prequal.js
//
// Buyer pre-qualification enquiries, routed to Rachelle via a GoHighLevel
// inbound webhook. Runs server-side because GHL webhook endpoints don't
// return CORS headers and the URL is unauthenticated.
//
// Deliberately does NOT collect SSN, income, assets or documents. Those
// belong in the lender's own secure intake, not on a marketing site.
//
// Required env var: GHL_PREQUAL_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED = ["name", "email", "phone", "state", "funding", "timeline", "prequal_status"];

function clean(value) {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const webhook = process.env.GHL_PREQUAL_WEBHOOK_URL;
  if (!webhook) {
    console.error("GHL_PREQUAL_WEBHOOK_URL is not set");
    return res.status(500).json({ error: "Form is not configured" });
  }

  const body = typeof req.body === "string" ? safeParse(req.body) : req.body || {};
  if (!body) return res.status(400).json({ error: "Invalid request" });

  if (clean(body.company)) return res.status(200).json({ ok: true });

  const missing = REQUIRED.filter((f) => !clean(body[f]));
  if (missing.length) {
    return res.status(400).json({ error: `Missing required fields: ${missing.join(", ")}` });
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: "Enter a valid email address" });
  }

  const funding = clean(body.funding);
  const timeline = clean(body.timeline);
  const status = clean(body.prequal_status);

  // Triage so the workflow branches on one field. Someone already
  // pre-qualified and moving soon goes straight onto the buyer registry;
  // everyone else starts with Rachelle.
  const fundingReady = funding !== "Not sure yet";
  const soon = timeline === "Ready now" || timeline === "Next 3 months";
  const alreadyQualified = status.startsWith("Yes");

  const buyerTier =
    alreadyQualified && soon ? "registry_ready"
    : fundingReady && soon ? "send_to_lender"
    : timeline === "Just researching" ? "nurture"
    : "review";

  const fullName = clean(body.name);
  const [firstName, ...rest] = fullName.split(/\s+/);

  const payload = {
    first_name: firstName,
    last_name: rest.join(" "),
    full_name: fullName,
    email,
    phone: clean(body.phone),
    buyer_state: clean(body.state),
    buyer_funding: funding,
    buyer_timeline: timeline,
    buyer_price_range: clean(body.price_range),
    prequal_status: status,
    buyer_notes: clean(body.notes),
    buyer_tier: buyerTier,
    source: clean(body.source) || "lender pre-qualification",
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
      console.error("GHL prequal webhook rejected submission", upstream.status, detail);
      return res.status(502).json({ error: "Could not submit right now" });
    }
  } catch (error) {
    console.error("GHL prequal webhook unreachable", error);
    return res.status(502).json({ error: "Could not submit right now" });
  }

  return res.status(200).json({ ok: true });
}

function safeParse(text) {
  try { return JSON.parse(text); } catch { return null; }
}
