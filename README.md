# Green Light Buying Machine

Astro site with a built-in admin editor. Brian and Gina sign in at `/admin`
with a password, edit the words, and hit publish. No GitHub account, no
third-party login, nothing to install.

```
src/
├── content/
│   ├── settings/site.json     contact details, footer, nav buttons
│   └── pages/*.json           one file per page — all the words live here
├── layouts/Base.astro         nav, footer, analytics, shared scripts
├── components/
│   ├── Blocks.astro           renders content blocks into markup
│   └── Form.astro             all four intake forms
├── lib/
│   ├── auth.ts                signed session cookie
│   └── github.ts              commits content on the editor's behalf
├── pages/
│   ├── [...slug].astro        builds every page from src/content/pages
│   ├── admin.astro            the editor
│   ├── funnel.astro           paid-traffic funnel (bespoke, two-step form)
│   ├── webinar.astro          live webinar registration, countdown, .ics download
│   └── api/
│       ├── admin/*.ts         login, logout, read and save content
│       └── *.ts               four handlers → GoHighLevel webhooks
├── scripts/                   lightbox, form submission, two-step funnel form
└── styles/global.css          the whole design system
```

## How the editor works

Sign in at `/admin` → pick a page from the list → edit the fields → **Publish
changes**. Behind the scenes the server commits the updated JSON to GitHub
using a token that only it can see, Vercel notices the commit and rebuilds,
and the change is live in about a minute.

Editors never touch git. They also can't break the layout: they're editing
text inside a fixed set of section types, not markup.

What they can edit: every heading, paragraph, list item, FAQ answer, number,
button label, and the site-wide contact details and footer.

## Setup

Six environment variables in Vercel → Settings → Environment Variables:

| Variable | What it is |
|---|---|
| `ADMIN_PASSWORD` | The password they type in. Make it long. |
| `ADMIN_SECRET` | Any long random string; signs the login cookie. Changing it signs everyone out. |
| `GITHUB_REPO` | `owner/repo` — where content is committed |
| `GITHUB_TOKEN` | Fine-grained PAT, **Contents: Read and write**, scoped to that one repo |
| `GITHUB_BRANCH` | Optional, defaults to `main` |
| `GHL_*_WEBHOOK_URL` | The five GoHighLevel inbound webhooks |

Generate the token at GitHub → Settings → Developer settings → Personal access
tokens → Fine-grained. Give it access to this repository only, and only the
Contents permission. It never reaches the browser.

## Security notes

- The session cookie is HMAC-signed, HttpOnly, Secure, and expires after 12 hours.
- Password and signature comparisons are constant-time; the login endpoint is
  deliberately slowed so it can't be used as a fast oracle.
- `/admin` is `noindex`, but it is not secret — the password is what protects it.
  Use a long one, and change `ADMIN_SECRET` if you ever suspect a leak.
- The GitHub token is scoped to one repo and one permission. If it leaks, the
  worst case is content edits, which are all revertible commits.

## Adding a section type

Three places, in this order:

1. `src/content.config.ts` — add it to the `block` union so content validates
2. `src/components/Blocks.astro` — add the markup
3. `src/pages/admin.astro` — add a friendly name to `BLOCK_NAMES`

If the first two disagree the build fails loudly, which is the intent.

## Local development

```bash
npm install
cp .env.example .env      # fill it in
npm run dev               # http://localhost:4321
npm run build
```

`astro preview` doesn't work with the Vercel adapter — use `npm run dev`.

## Forms

Five forms post JSON to `/api/*`, which validate and forward to GoHighLevel.
They run server-side because GHL webhook endpoints don't return CORS headers
and the URLs are unauthenticated — they must never reach the browser.

Full GHL workflow spec, tags and email copy: see `ghl-build.md`.

The pre-qualification form deliberately collects no SSN, income, assets or
documents. Those belong in the lender's own secure intake.
