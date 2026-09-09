export const prerender = false;

import type { APIRoute } from "astro";

// api/book-waitlist.js
//
// Book waitlist capture. Same pattern as deal-analysis.js.
//
// Required env var: GHL_BOOK_WAITLIST_WEBHOOK_URL

const MAX_LENGTH = 500;

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });

export const POST: APIRoute = async ({ request }) => {
  const webhook = import.meta.env.GHL_BOOK_WAITLIST_WEBHOOK_URL ?? process.env.GHL_BOOK_WAITLIST_WEBHOOK_URL;
    if (!webhook) {
    console.error("GHL_BOOK_WAITLIST_WEBHOOK_URL is not set");
    return json({ error: "Form is not configured" }, 500);
  }

  const body = (await request.json().catch(() => null)) as Record<string, string> | null;
  if (!body) return json({ error: "Invalid request" }, 400);

  if (clean(body.company)) return json({ ok: true }, 200);

  const fullName = clean(body.name);
  const email = clean(body.email);

  if (!fullName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ error: "Name and a valid email are required" }, 400);
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
      return json({ error: "Could not submit right now" }, 502);
    }
  } catch (error) {
    console.error("GHL waitlist webhook unreachable", error);
    return json({ error: "Could not submit right now" }, 502);
  }

  return json({ ok: true }, 200);
};

export const GET: APIRoute = () => json({ error: "Method not allowed" }, 405);
