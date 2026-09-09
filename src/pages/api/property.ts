export const prerender = false;

import type { APIRoute } from "astro";

// api/property.js
//
// Property submissions from wholesalers, agents and owners — deal flow
// coming into the machine, not student applications (see apply.js).
//
// Vercel serverless function. Forwards to a GoHighLevel inbound webhook.
//
// This runs server-side on purpose: GHL webhook endpoints don't return
// CORS headers, so posting straight from the browser is blocked or
// unreadable. The webhook URL also stays out of the client bundle —
// anyone holding it can push contacts into the workflow.
//
// Required env var: GHL_PROPERTY_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED = ["name", "email", "address"];

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export const POST: APIRoute = async ({ request }) => {
  const webhook = import.meta.env.GHL_PROPERTY_WEBHOOK_URL ?? process.env.GHL_PROPERTY_WEBHOOK_URL;
    if (!webhook) {
    console.error("GHL_PROPERTY_WEBHOOK_URL is not set");
    return json({ error: "Form is not configured" }, 500);
  }

  // Vercel parses JSON bodies automatically, but be defensive about it.
  const body = (await request.json().catch(() => null)) as Record<string, string> | null;
  if (!body) return json({ error: "Invalid request" }, 400);

  // Honeypot. Real people leave this empty. Return 200 so bots learn nothing.
  if (clean(body.company)) return json({ ok: true }, 200);

  const missing = REQUIRED.filter((field) => !clean(body[field]));
  if (missing.length) {
    return json({ error: `Missing required fields: ${missing.join(", ")}` }, 400);
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: "Enter a valid email address" }, 400);
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
    submitter_role: clean(body.role),
    notes: clean(body.notes),
    referred_by: clean(body.referred_by),
    source: clean(body.source) || "property submission",
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
      return json({ error: "Could not submit right now" }, 502);
    }
  } catch (error) {
    console.error("GHL webhook unreachable", error);
    return json({ error: "Could not submit right now" }, 502);
  }

  return json({ ok: true }, 200);
};

export const GET: APIRoute = () => json({ error: "Method not allowed" }, 405);
