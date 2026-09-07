// api/book-waitlist.js
//
// Book waitlist capture. Same pattern as deal-analysis.js.
//
// Required env var: GHL_BOOK_WAITLIST_WEBHOOK_URL

const MAX_LENGTH = 500;

function clean(value) {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ error: "Method not allowed" });
  }

  const webhook = process.env.GHL_BOOK_WAITLIST_WEBHOOK_URL;
  if (!webhook) {
    console.error("GHL_BOOK_WAITLIST_WEBHOOK_URL is not set");
    return res.status(500).json({ error: "Form is not configured" });
  }

  const body = typeof req.body === "string" ? safeParse(req.body) : req.body || {};
  if (!body) return res.status(400).json({ error: "Invalid request" });

  if (clean(body.company)) return res.status(200).json({ ok: true });

  const fullName = clean(body.name);
  const email = clean(body.email);

  if (!fullName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return res.status(400).json({ error: "Name and a valid email are required" });
  }

  const [firstName, ...rest] = fullName.split(/\s+/);

  const payload = {
    first_name: firstName,
    last_name: rest.join(" "),
    full_name: fullName,
    email,
    source: clean(body.source) || "book waitlist",
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
      console.error("GHL waitlist webhook rejected submission", upstream.status, detail);
      return res.status(502).json({ error: "Could not submit right now" });
    }
  } catch (error) {
    console.error("GHL waitlist webhook unreachable", error);
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
