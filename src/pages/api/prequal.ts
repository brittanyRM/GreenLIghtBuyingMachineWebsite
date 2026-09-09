export const prerender = false;

import type { APIRoute } from "astro";

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

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export const POST: APIRoute = async ({ request }) => {
  const webhook = import.meta.env.GHL_PREQUAL_WEBHOOK_URL ?? process.env.GHL_PREQUAL_WEBHOOK_URL;
    if (!webhook) {
    console.error("GHL_PREQUAL_WEBHOOK_URL is not set");
    return json({ error: "Form is not configured" }, 500);
  }

  const body = (await request.json().catch(() => null)) as Record<string, string> | null;
  if (!body) return json({ error: "Invalid request" }, 400);

  if (clean(body.company)) return json({ ok: true }, 200);

  const missing = REQUIRED.filter((f) => !clean(body[f]));
  if (missing.length) {
    return json({ error: `Missing required fields: ${missing.join(", ")}` }, 400);
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: "Enter a valid email address" }, 400);
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
      return json({ error: "Could not submit right now" }, 502);
    }
  } catch (error) {
    console.error("GHL prequal webhook unreachable", error);
    return json({ error: "Could not submit right now" }, 502);
  }

  return json({ ok: true }, 200);
};

export const GET: APIRoute = () => json({ error: "Method not allowed" }, 405);
