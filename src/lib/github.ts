/* Commits content changes to GitHub using a single repo token held on the
   server. Editors never see GitHub — they sign in with the site password
   and this does the committing on their behalf. Vercel redeploys on push. */

function env(name: string): string {
  const v = import.meta.env[name] ?? process.env[name];
  if (!v) throw new Error(`${name} is not set`);
  return String(v);
}

const api = () => `https://api.github.com/repos/${env("GITHUB_REPO")}`;

const headers = () => ({
  Authorization: `Bearer ${env("GITHUB_TOKEN")}`,
  Accept: "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28",
  "Content-Type": "application/json",
});

const branch = () => import.meta.env.GITHUB_BRANCH ?? process.env.GITHUB_BRANCH ?? "main";

export async function readFile(path: string): Promise<{ json: any; sha: string }> {
  const res = await fetch(`${api()}/contents/${path}?ref=${branch()}`, { headers: headers() });
  if (!res.ok) throw new Error(`GitHub read failed (${res.status})`);
  const data = await res.json();
  const text = new TextDecoder().decode(
    Uint8Array.from(atob(data.content.replace(/\n/g, "")), (c) => c.charCodeAt(0)),
  );
  return { json: JSON.parse(text), sha: data.sha };
}

export async function writeFile(path: string, json: unknown, message: string): Promise<void> {
  // re-read for the current sha so concurrent edits fail loudly rather than clobber
  const current = await readFile(path).catch(() => null);
  const body = JSON.stringify(
    {
      message,
      branch: branch(),
      sha: current?.sha,
      content: btoa(
        String.fromCharCode(...new TextEncoder().encode(JSON.stringify(json, null, 2) + "\n")),
      ),
    },
  );
  const res = await fetch(`${api()}/contents/${path}`, {
    method: "PUT",
    headers: headers(),
    body,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(`GitHub write failed (${res.status}) ${detail.slice(0, 200)}`);
  }
}

export async function listPages(): Promise<string[]> {
  const res = await fetch(`${api()}/contents/src/content/pages?ref=${branch()}`, {
    headers: headers(),
  });
  if (!res.ok) throw new Error(`GitHub list failed (${res.status})`);
  const data = await res.json();
  return data
    .filter((f: any) => f.name.endsWith(".json"))
    .map((f: any) => f.name.replace(/\.json$/, ""))
    .sort();
}
