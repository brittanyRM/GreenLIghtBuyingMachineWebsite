# Green Light Buying Machine

Static marketing site with two serverless functions that forward form
submissions into GoHighLevel.

```
├── index.html            home
├── how-it-works.html     ten stages, division of labor
├── is-it-for-you.html    fit list and FAQ
├── for-buyers.html       buyer track: lender pre-qual + GHL form embed
├── homes.html            photo and floor plan gallery
├── the-book.html         coming soon + waitlist capture
├── about.html            Brian and Gina (needs real bio)
├── apply.html            deal analysis form
├── api/
│   ├── deal-analysis.js  → GHL_DEAL_WEBHOOK_URL
│   └── book-waitlist.js  → GHL_BOOK_WAITLIST_WEBHOOK_URL
├── images/plans/         5 floor plans, full + thumb
├── images/homes/         17 finished-home photos, full + thumb
├── build.py              regenerates every page — edit here, not in the HTML
├── nextjs/               same handlers as Next.js route files,
│                         if this ever moves into an app
└── ghl-build.md          workflow spec: fields, tags, sequences
```

**Editing pages:** the CSS and the shared nav, footer, and form script are
inlined into every HTML file so each page stands alone (useful for pasting
one into a GHL page). That means the HTML is generated — change `build.py`
and run `python3 build.py`, or a copy edit will silently drift from the
other six pages. Output goes straight into this folder.

No build step on the host and no dependencies. Vercel serves the HTML from root and
picks up `api/` automatically. Framework preset: **Other**.

---

## Order of operations

The sequence matters — GHL can't map webhook fields until it has seen a
real payload, so the site has to be live before the workflows can be
finished.

**1. Create both GHL workflows, triggers only.**
Workflow → Inbound Webhook trigger → copy the URL. Once for deal analysis,
once for the book waitlist. Don't build the actions yet.

The buyer form is different: it's the existing GHL form embedded directly
on `for-buyers.html`, so it already runs through whatever workflow that
form is attached to. No webhook needed — but confirm the form ID, since
the one on the current page is named "Rachelle Test".

**2. Push and deploy.**

```bash
git init
git add .
git commit -m "Green Light Buying Machine site"
git branch -M main
git remote add origin git@github.com:USER/REPO.git
git push -u origin main
```

Import the repo in Vercel, framework preset **Other**, no build command,
output directory root.

**3. Set environment variables** in Vercel → Settings → Environment
Variables, for Production and Preview:

```
GHL_DEAL_WEBHOOK_URL=https://...
GHL_BOOK_WAITLIST_WEBHOOK_URL=https://...
```

Redeploy after adding them. Env vars are read at request time but the
deployment needs to exist with them attached.

**4. Submit each form once on the live URL.** Use a real address you
don't mind seeing in the account.

**5. Go back to GHL and map the fields.** The trigger will now show the
captured payload. Build out the actions per `ghl-build.md` — custom
fields must exist *before* this step or the mapping dropdowns come up
empty.

**6. Run the test list** at the end of `ghl-build.md`.

---

## Gotchas

**Don't post to GHL from the browser.** Those endpoints don't send CORS
headers, so a direct `fetch` from the page is blocked, and `no-cors`
mode gives you a response you can't read — the form would show success
whether or not anything arrived. That's why these functions exist.

**Keep the webhook URLs server-side.** No `NEXT_PUBLIC_` or `VITE_`
prefix. They're unauthenticated endpoints; anyone with the URL can
inject contacts into the workflow.

**Rate limiting.** There's a honeypot but no rate limit. If the forms get
hit, add Vercel's WAF rules or a per-IP check in the handler.

---

## Before launch

- [ ] Real bio and photo on `about.html`
- [ ] Confirm the ten stage names against the actual Pipeline A
- [ ] Answer the "is the buyer guaranteed" FAQ, with counsel review
- [ ] Confirm whether students can bring their own deal
- [ ] Real cover art for the book (300 DPI minimum)
- [ ] Replace `hello@example.com` in the form fallback message
- [ ] Decide whether to show the enrollment price
- [ ] Add testimonials from students who have closed
- [ ] Swap the "Rachelle Test" form ID for the production one
- [ ] Substantiate the 450+ doors / 15% market share / 26+ years figures
- [ ] Confirm what conveys with a buyer property (furnished, managed, tenanted)
- [ ] Confirm whether buyers are matched before or after renovation starts
- [ ] Disclose any buyer-side fee on for-buyers.html
- [ ] Point a custom domain at the deployment
