export const prerender = false;

import type { APIRoute } from "astro";

// api/apply.js
//
// Program applications from operators. Forwards to a GoHighLevel inbound
// webhook server-side (GHL webhook endpoints don't return CORS headers,
// and the URL is unauthenticated so it must stay off the client).
//
// Required env var: GHL_APPLICATION_WEBHOOK_URL

const MAX_LENGTH = 2000;
const REQUIRED_COMPLETE = ["name", "email", "flips", "crew", "financing", "market", "city", "timeline"];
const REQUIRED_PARTIAL = ["name", "email"];

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export const POST: APIRoute = async ({ request }) => {
  const webhook = import.meta.env.GHL_APPLICATION_WEBHOOK_URL ?? process.env.GHL_APPLICATION_WEBHOOK_URL;
    if (!webhook) {
    console.error("GHL_APPLICATION_WEBHOOK_URL is not set");
    return json({ error: "Form is not configured" }, 500);
  }

  const body = (await request.json().catch(() => null)) as Record<string, string> | null;
  if (!body) return json({ error: "Invalid request" }, 400);

  if (clean(body.company)) return json({ ok: true }, 200);

  // Step 1 of the landing-page form posts on its own so an abandoned
  // application still leaves a reachable lead. Those arrive as partials
  // and can't be held to the full field list.
  const isPartial = clean(body.stage) === "partial";
  const required = isPartial ? REQUIRED_PARTIAL : REQUIRED_COMPLETE;

  const missing = required.filter((f) => !clean(body[f]));
  if (missing.length) {
    return json({ error: `Missing required fields: ${missing.join(", ")}` }, 400);
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: "Enter a valid email address" }, 400);
  }

  // The funnel labels the under-10 options with an information path, e.g.
  // "5 to 9 — send me more info instead". Strip that before scoring.
  const flips = clean(body.flips).split("\u2014")[0].split(" - ")[0].trim();
  const crew = clean(body.crew);
  const timeline = clean(body.timeline);

  // Triage against the stated bar: 10+ flips and a crew they already run.
  // Computed here so the workflow branches on one field instead of three.
  const experienceOk = flips === "10 to 15" || flips === "More than 15";
  const crewOk = crew === "I run my own crew" || crew === "I use the same trades on every job";
  const readyNow = timeline === "Next available cohort" || timeline === "Next 3 months";

  // We work nationwide, so market is routing information rather than a gate.
  const outsideArizona = clean(body.market).startsWith("Outside Arizona");

  // Someone who chose the information path is a nurture lead, not a decline.
  const wantsInfo = clean(body.intent) === "more_info";

  const applicantTier =
    isPartial ? "incomplete"
    : wantsInfo ? "not_yet"
    : experienceOk && crewOk && readyNow ? "core"
    : experienceOk && crewOk ? "qualified"
    : flips === "Fewer than 5" || crew === "I'd need to build one" ? "below_bar"
    : "review";

  const outsideHomeMarket = outsideArizona;

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
    operating_market: clean(body.city),
    outside_home_market: outsideHomeMarket ? "yes" : "no",
    start_timeline: timeline,
    recent_project: clean(body.recent),
    applicant_tier: applicantTier,
    intent: wantsInfo ? "more_info" : "apply",
    stage: isPartial ? "partial" : "complete",
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
      return json({ error: "Could not submit right now" }, 502);
    }
  } catch (error) {
    console.error("GHL application webhook unreachable", error);
    return json({ error: "Could not submit right now" }, 502);
  }

  return json({ ok: true }, 200);
};

export const GET: APIRoute = () => json({ error: "Method not allowed" }, 405);
