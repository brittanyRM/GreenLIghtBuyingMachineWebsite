// app/api/deal-analysis/route.ts
//
// Forwards website form submissions to a GoHighLevel inbound webhook.
// Runs server-side on purpose: GHL's webhook endpoints don't return CORS
// headers, so a fetch straight from the browser is blocked or unreadable.
//
// Set GHL_DEAL_WEBHOOK_URL in your environment. Never expose it client-side
// (no NEXT_PUBLIC_ prefix) — anyone with the URL can push contacts into
// the workflow.

import { NextResponse } from "next/server";

export const runtime = "edge";

type Payload = Record<string, string>;

const REQUIRED = ["name", "email", "address"] as const;
const MAX_LENGTH = 2000;

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export async function POST(request: Request) {
  const webhook = process.env.GHL_DEAL_WEBHOOK_URL;

  if (!webhook) {
    console.error("GHL_DEAL_WEBHOOK_URL is not set");
    return NextResponse.json({ error: "Form is not configured" }, { status: 500 });
  }

  let body: Payload;
  try {
    body = (await request.json()) as Payload;
  } catch {
    return NextResponse.json({ error: "Invalid request" }, { status: 400 });
  }

  // Honeypot: real people leave this empty. Return 200 so bots don't learn.
  if (clean(body.company)) {
    return NextResponse.json({ ok: true });
  }

  const missing = REQUIRED.filter((field) => !clean(body[field]));
  if (missing.length) {
    return NextResponse.json(
      { error: `Missing required fields: ${missing.join(", ")}` },
      { status: 400 },
    );
  }

  const email = clean(body.email);
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return NextResponse.json({ error: "Enter a valid email address" }, { status: 400 });
  }

  // Split the name so GHL maps first/last cleanly instead of dumping
  // everything into one field.
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
      signal: AbortSignal.timeout(10_000),
    });

    if (!upstream.ok) {
      const detail = await upstream.text().catch(() => "");
      console.error("GHL webhook rejected submission", upstream.status, detail);
      return NextResponse.json({ error: "Could not submit right now" }, { status: 502 });
    }
  } catch (error) {
    console.error("GHL webhook unreachable", error);
    return NextResponse.json({ error: "Could not submit right now" }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}

export async function GET() {
  return NextResponse.json({ error: "Method not allowed" }, { status: 405 });
}
