// Astro version — save as: src/pages/api/webinar-register.ts
//
// Posts the registration to a GoHighLevel inbound webhook from the server,
// because GHL's endpoints don't send CORS headers and a browser fetch would
// silently fail while still showing the visitor a success message.

import type { APIRoute } from 'astro';

export const prerender = false;

const REQUIRED = ['firstName', 'lastName', 'email', 'phone', 'city', 'state'];

export const POST: APIRoute = async ({ request }) => {
  const json = (body: unknown, status: number) =>
    new Response(JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' }
    });

  let data: Record<string, string>;
  try {
    data = await request.json();
  } catch {
    return json({ error: 'Malformed request body.' }, 400);
  }

  // Honeypot. Bots fill hidden fields; people don't. Return 200 so the bot
  // thinks it worked and doesn't retry.
  if (data.company) return json({ ok: true }, 200);

  const missing = REQUIRED.filter((f) => !data[f]?.trim());
  if (missing.length) {
    return json({ error: `Missing required fields: ${missing.join(', ')}` }, 400);
  }

  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(data.email)) {
    return json({ error: 'That email address doesn\u2019t look right.' }, 400);
  }

  const webhook = import.meta.env.GHL_WEBINAR_WEBHOOK_URL;
  if (!webhook) {
    console.error('GHL_WEBINAR_WEBHOOK_URL is not set');
    return json({ error: 'Registration is temporarily unavailable.' }, 503);
  }

  const payload = {
    first_name: data.firstName.trim(),
    last_name: data.lastName.trim(),
    email: data.email.trim().toLowerCase(),
    phone: data.phone.trim(),
    city: data.city.trim(),
    state: data.state.trim(),
    flips_completed: data.flipsCompleted ?? '',
    webinar_goal: data.goal ?? '',
    source: data.source ?? 'webinar',
    page: data.page ?? '',
    submitted_at: new Date().toISOString()
  };

  try {
    const res = await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      console.error('GHL webhook rejected the registration', res.status, await res.text());
      return json({ error: 'Registration failed upstream.' }, 502);
    }
  } catch (err) {
    console.error('GHL webhook unreachable', err);
    return json({ error: 'Registration failed upstream.' }, 502);
  }

  return json({ ok: true }, 200);
};
