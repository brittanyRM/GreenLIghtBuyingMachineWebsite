// api/apply.js
//
// Program applications from operators. Forwards to a GoHighLevel inbound
// webhook server-side (GHL webhook endpoints don't return CORS headers,
// and the URL is unauthenticated so it must stay off the client).
//
// Required env var: GHL_APPLICATION_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED = ["name", "email", "flips", "crew", "financing", "market", "timeline"];

function clean(value) {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const webhook = process.env.GHL_APPLICATION_WEBHOOK_URL;
  if (!webhook) {
    console.error("GHL_APPLICATION_WEBHOOK_URL is not set");
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

  const flips = clean(body.flips);
  const crew = clean(body.crew);
  const timeline = clean(body.timeline);

  // Triage against the stated bar: 10+ flips and a crew they already run.
  // Computed here so the workflow branches on one field instead of three.
  const experienceOk = flips === "10 to 15" || flips === "More than 15";
  const crewOk = crew === "I run my own crew" || crew === "I use the same trades on every job";
  const readyNow = timeline === "Next available cohort" || timeline === "Next 3 months";

  const applicantTier =
    experienceOk && crewOk && readyNow ? "core"
    : experienceOk && crewOk ? "qualified"
    : flips === "Fewer than 5" || crew === "I'd need to build one" ? "below_bar"
    : "review";

  const fullName = clean(body.name);
  const [firstName, ...rest] = fullName.split(/\s+/);

  const payload = {
    first_name: firstName,
    last_name: rest.join(" "),
    full_name: fullName,
    email,
    phone: clean(body.phone),
    completed_flips: flips,
    crew_status: crew,
    financing_method: clean(body.financing),
    market_status: clean(body.market),
    start_timeline: timeline,
    recent_project: clean(body.recent),
    applicant_tier: applicantTier,
    source: clean(body.source) || "program application",
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
      console.error("GHL application webhook rejected submission", upstream.status, detail);
      return res.status(502).json({ error: "Could not submit right now" });
    }
  } catch (error) {
    console.error("GHL application webhook unreachable", error);
    return res.status(502).json({ error: "Could not submit right now" });
  }

  return res.status(200).json({ ok: true });
}

function safeParse(text) {
  try { return JSON.parse(text); } catch { return null; }
}
