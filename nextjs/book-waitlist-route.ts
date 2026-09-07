// app/api/book-waitlist/route.ts
//
// Book waitlist capture. Same pattern as the deal-analysis route: the
// GHL webhook URL stays server-side, and the honeypot returns 200 so
// bots don't learn they were filtered.
//
// Env: GHL_BOOK_WAITLIST_WEBHOOK_URL

import { NextResponse } from "next/server";

export const runtime = "edge";

const MAX_LENGTH = 500;

function clean(value: unknown): string {
  return typeof value === "string" ? value.trim().slice(0, MAX_LENGTH) : "";
}

export async function POST(request: Request) {
  const webhook = process.env.GHL_BOOK_WAITLIST_WEBHOOK_URL;

  if (!webhook) {
    console.error("GHL_BOOK_WAITLIST_WEBHOOK_URL is not set");
    return NextResponse.json({ error: "Form is not configured" }, { status: 500 });
  }

  let body: Record<string, string>;
  try {
    body = (await request.json()) as Record<string, string>;
  } catch {
    return NextResponse.json({ error: "Invalid request" }, { status: 400 });
  }

  if (clean(body.company)) {
    return NextResponse.json({ ok: true });
  }

  const email = clean(body.email);
  const fullName = clean(body.name);

  if (!fullName || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return NextResponse.json({ error: "Name and a valid email are required" }, { status: 400 });
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
      signal: AbortSignal.timeout(10_000),
    });

    if (!upstream.ok) {
      const detail = await upstream.text().catch(() => "");
      console.error("GHL waitlist webhook rejected submission", upstream.status, detail);
      return NextResponse.json({ error: "Could not submit right now" }, { status: 502 });
    }
  } catch (error) {
    console.error("GHL waitlist webhook unreachable", error);
    return NextResponse.json({ error: "Could not submit right now" }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}

export async function GET() {
  return NextResponse.json({ error: "Method not allowed" }, { status: 405 });
}
