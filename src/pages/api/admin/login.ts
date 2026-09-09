export const prerender = false;
import type { APIRoute } from "astro";
import { makeToken, cookieHeader, passwordMatches } from "../../../lib/auth";

export const POST: APIRoute = async ({ request }) => {
  const body = (await request.json().catch(() => null)) as { password?: string } | null;
  const supplied = typeof body?.password === "string" ? body.password : "";

  // deliberate delay so the endpoint isn't a fast password oracle
  await new Promise((r) => setTimeout(r, 400));

  if (!supplied || !passwordMatches(supplied)) {
    return new Response(JSON.stringify({ error: "Wrong password" }), {
      status: 401,
      headers: { "Content-Type": "application/json" },
    });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: {
      "Content-Type": "application/json",
      "Set-Cookie": cookieHeader(await makeToken()),
    },
  });
};
