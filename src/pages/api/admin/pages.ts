export const prerender = false;
import type { APIRoute } from "astro";
import { verifyToken, COOKIE_NAME } from "../../../lib/auth";
import { readFile, writeFile, listPages } from "../../../lib/github";

const json = (payload: unknown, status = 200) =>
  new Response(JSON.stringify(payload), {
    status,
    headers: { "Content-Type": "application/json" },
  });

async function guard(cookies: any) {
  return verifyToken(cookies.get(COOKIE_NAME)?.value);
}

export const GET: APIRoute = async ({ cookies, url }) => {
  if (!(await guard(cookies))) return json({ error: "Not signed in" }, 401);

  const slug = url.searchParams.get("slug");
  try {
    if (!slug) {
      const pages = await listPages();
      return json({ pages });
    }
    if (!/^[a-z0-9-]+$/.test(slug)) return json({ error: "Bad slug" }, 400);
    const path =
      slug === "site"
        ? "src/content/settings/site.json"
        : `src/content/pages/${slug}.json`;
    const { json: data } = await readFile(path);
    return json({ slug, data });
  } catch (error: any) {
    console.error("admin read failed", error);
    return json({ error: error.message ?? "Read failed" }, 502);
  }
};

export const PUT: APIRoute = async ({ cookies, request }) => {
  if (!(await guard(cookies))) return json({ error: "Not signed in" }, 401);

  const body = (await request.json().catch(() => null)) as
    | { slug?: string; data?: unknown }
    | null;
  const slug = body?.slug;
  if (!slug || !/^[a-z0-9-]+$/.test(slug) || !body?.data) {
    return json({ error: "Bad request" }, 400);
  }

  const path =
    slug === "site" ? "src/content/settings/site.json" : `src/content/pages/${slug}.json`;

  try {
    await writeFile(path, body.data, `Content: update ${slug} via admin`);
    return json({ ok: true });
  } catch (error: any) {
    console.error("admin write failed", error);
    return json({ error: error.message ?? "Save failed" }, 502);
  }
};
