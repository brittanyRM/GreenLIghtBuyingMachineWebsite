/* Session cookie signed with ADMIN_SECRET. No database, no third-party
   login — one shared password that Brian and Gina use. */
const COOKIE = "glbm_admin";
const MAX_AGE = 60 * 60 * 12; // 12 hours

const enc = new TextEncoder();

function env(name: string): string {
  const v = import.meta.env[name] ?? process.env[name];
  if (!v) throw new Error(`${name} is not set`);
  return String(v);
}

async function key() {
  return crypto.subtle.importKey(
    "raw",
    enc.encode(env("ADMIN_SECRET")),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign", "verify"],
  );
}

const b64 = (buf: ArrayBuffer) =>
  btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/=+$/, "");

export async function makeToken(): Promise<string> {
  const expires = Date.now() + MAX_AGE * 1000;
  const payload = String(expires);
  const sig = await crypto.subtle.sign("HMAC", await key(), enc.encode(payload));
  return `${payload}.${b64(sig)}`;
}

export async function verifyToken(token?: string | null): Promise<boolean> {
  if (!token) return false;
  const [payload, sig] = token.split(".");
  if (!payload || !sig) return false;
  if (Number(payload) < Date.now()) return false;
  const expected = b64(await crypto.subtle.sign("HMAC", await key(), enc.encode(payload)));
  // constant-time-ish compare
  if (expected.length !== sig.length) return false;
  let diff = 0;
  for (let i = 0; i < expected.length; i++) diff |= expected.charCodeAt(i) ^ sig.charCodeAt(i);
  return diff === 0;
}

export function cookieHeader(token: string, maxAge = MAX_AGE): string {
  return `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${maxAge}`;
}

export const COOKIE_NAME = COOKIE;

export function passwordMatches(supplied: string): boolean {
  const actual = env("ADMIN_PASSWORD");
  if (supplied.length !== actual.length) return false;
  let diff = 0;
  for (let i = 0; i < actual.length; i++) diff |= actual.charCodeAt(i) ^ supplied.charCodeAt(i);
  return diff === 0;
}
