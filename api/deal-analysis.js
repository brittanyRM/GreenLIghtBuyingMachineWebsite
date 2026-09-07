// api/deal-analysis.js
//
// Vercel serverless function. Forwards website form submissions to a
// GoHighLevel inbound webhook.
//
// This runs server-side on purpose: GHL webhook endpoints don't return
// CORS headers, so posting straight from the browser is blocked or
// unreadable. The webhook URL also stays out of the client bundle —
// anyone holding it can push contacts into the workflow.
//
// Required env var: GHL_DEAL_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED = ["name", "email", "address"];

function clean(value) {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const webhook = process.env.GHL_DEAL_WEBHOOK_URL;
  if (!webhook) {
    console.error("GHL_DEAL_WEBHOOK_URL is not set");
    return res.status(500).json({ error: "Form is not configured" });
  }

  // Vercel parses JSON bodies automatically, but be defensive about it.
  const body = typeof req.body === "string" ? safeParse(req.body) : req.body || {};
  if (!body) return res.status(400).json({ error: "Invalid request" });

  // Honeypot. Real people leave this empty. Return 200 so bots learn nothing.
  if (clean(body.company)) return res.status(200).json({ ok: true });

  const missing = REQUIRED.filter((field) => !clean(body[field]));
  if (missing.length) {
    return res.status(400).json({ error: `Missing required fields: ${missing.join(", ")}` });
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: "Enter a valid email address" });
  }

  // Split the name so GHL maps first/last cleanly instead of dumping
  // everything into a single field.
  const fullName = clean(body.name);
  const [firstName, ...rest] = fullName.split(/\s+/);

  const payload = {
    first_name: firstName,
    last_name: rest.join(" "),
    full_name: fullName,
    email,
    phone: clean(body.phone),
    property_address: clean(body.address),
    asking_price: clean(body.price),
    property_specs: clean(body.specs),
    completed_renovations: clean(body.experience),
    notes: clean(body.notes),
    source: clean(body.source) || "website",
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
      console.error("GHL webhook rejected submission", upstream.status, detail);
      return res.status(502).json({ error: "Could not submit right now" });
    }
  } catch (error) {
    console.error("GHL webhook unreachable", error);
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
