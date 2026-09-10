# Green Light Buying Machine — Website to GHL Build

Three inbound webhooks, three workflows, two new custom field groups.
The site serves two audiences — operators who build a house, and investors
who buy one — and they need separate pipelines, separate qualification, and
separate follow-up. Everything
here attaches to the existing Marcus AI Trigger System rather than replacing
any of it.

**Assumption to confirm before building:** the website deal-analysis form enters
at the front of the existing Pipeline A rather than starting a new pipeline. If
Pipeline A currently starts at a sales call instead, this becomes a pre-stage
and the tag numbering below shifts.

---

## 1. Custom fields

Create these before building either workflow — the webhook mapping dropdown
comes up empty for fields that don't exist yet.

**Group: Operator Application**

| Field name | Key | Type |
|---|---|---|
| Completed Flips | `completed_flips` | Dropdown |
| Crew Status | `crew_status` | Dropdown |
| Financing Method | `financing_method` | Dropdown |
| Market Status | `market_status` | Dropdown |
| Start Timeline | `start_timeline` | Dropdown |
| Recent Project | `recent_project` | Multi line |
| Operating Market | `operating_market` | Single line |
| Outside Home Market | `outside_home_market` | Dropdown |
| Applicant Tier | `applicant_tier` | Dropdown |

Dropdown options must match the form exactly.
`completed_flips`: `Fewer than 5`, `5 to 9`, `10 to 15`, `More than 15`.
`crew_status`: `I run my own crew`, `I use the same trades on every job`,
`I hire per project`, `I'd need to build one`.
`applicant_tier`: `core`, `qualified`, `review`, `below_bar`, `not_yet` — set
by the handler, don't edit by hand.

`not_yet` comes from the funnel page (`funnel.html`), where operators under ten
flips can choose an information path instead of applying. They answered every
qualifying question and told you they're not there yet — that's a warm lead with
a known gap, not a rejection. `intent` will be `more_info`.
`outside_home_market`: `yes` when the applicant works outside Arizona. The
program is nationwide, so this is routing information, not a filter — use it to
group members by market and to know which local rules will come up on the call.

### Partial applications

The landing page (`start.html`) posts twice: contact details when they clear
step 1, then everything when they submit. So expect two payloads per applicant,
matched on email, with `stage` set to `partial` then `complete`.

A partial arrives with `applicant_tier: incomplete`. Treat it as a live lead,
not a bad one — they gave you their name, email and market and then hesitated
on the experience questions. That is a person to call.

- `stage` = `partial` → tag `A-000-STARTED`. Wait 1 hour, then if
  `A-001-APPLIED` has not landed, send the nudge below. Follow with an
  internal task at 24 hours.
- `stage` = `complete` → remove `A-000-STARTED`, continue the normal branch.

Do not create an opportunity on a partial. It skews the pipeline and someone
will work it as though it were a real application.

**Group: Property Submission**

| Field name | Key | Type |
|---|---|---|
| Property Address | `property_address` | Single line |
| Asking Price | `asking_price` | Single line |
| Property Specs | `property_specs` | Single line |
| Submitter Role | `submitter_role` | Dropdown |
| Deal Notes | `notes` | Multi line |
| Analysis Verdict | `analysis_verdict` | Dropdown |

`submitter_role`: `Wholesaler`, `Agent`, `Owner`, `Investor`, `Other`.
`analysis_verdict`: `Converts`, `Converts with conditions`, `Does not convert`,
`Not analyzed` — set by hand after review, drives the follow-up.

**Group: Buyer**

| Field name | Key | Type |
|---|---|---|
| Funding Method | `buyer_funding` | Dropdown |
| Purchase Timeline | `buyer_timeline` | Dropdown |
| Rentals Owned | `buyer_portfolio` | Dropdown |
| Buying Criteria | `buyer_criteria` | Multi line |
| Buyer Tier | `buyer_tier` | Dropdown |
| Proof of Funds Received | `buyer_pof` | Checkbox |

Dropdown options must match the form exactly.
`buyer_funding`: `Cash`, `Conventional or DSCR financing`, `1031 exchange`,
`Partnership or fund`, `Still figuring it out`.
`buyer_timeline`: `Ready now`, `Next 3 months`, `3 to 6 months`, `Just researching`.
`buyer_portfolio`: `None yet`, `1 to 3`, `4 to 10`, `More than 10`.
`buyer_tier`: `core`, `review`, `nurture` — set by the handler, don't edit by hand.

**Group: Attribution**

| Field name | Key | Type |
|---|---|---|
| Lead Source Detail | `source` | Single line |
| Entry Page | `page` | Single line |

---

## 2. Webhook A — Program applications

**Workflow:** `WEB-A · Operator Application`
**Trigger:** Inbound Webhook

Copy the trigger URL into `GHL_APPLICATION_WEBHOOK_URL` on Vercel. Submit the live
form once before you map anything — GHL only exposes payload fields after it
has captured a real sample.

Payload keys arriving from the route handler:

```
first_name, last_name, full_name, email, phone,
completed_flips, crew_status, financing_method, market_status,
start_timeline, recent_project, applicant_tier,
source, page, submitted_at
```

`applicant_tier` is computed by the handler against the stated bar — 10+
flips and a crew they already run — so the workflow branches on one field
instead of three: `core` (meets the bar and starting soon), `qualified`
(meets the bar, longer timeline), `review` (borderline, needs a human),
`below_bar` (under 5 flips or no crew).

### Actions, in order

1. **Create/Update Contact** — map name, email, phone, then every Operator
   Application field by matching key.
2. **Add tag** `A-001-APPLIED` and `SRC-WEBSITE`
3. **If/Else** on `applicant_tier`:
   - `core` → tag `A-002-QUALIFIED-CORE`, create the Pipeline A opportunity,
     notify Brian and Gina, send the booking link.
   - `qualified` → tag `A-002-QUALIFIED`, create the opportunity, send a
     nurture sequence until their timeline arrives. Don't lose these to the
     three-month gap.
   - `review` → tag `A-002-REVIEW`, internal task. No auto-booking; a human
     reads the recent-project answer and decides.
   - `below_bar` → tag `A-002-BELOW-BAR`, send the honest decline below. No
     opportunity created.
   - `not_yet` → tag `A-002-NOT-YET` and `BOOK-DOWNLOAD`, send the book and the
     not-yet email below. No opportunity, no sales call, no drip beyond the
     book sequence. Add to a quarterly check-in list instead.
4. **If** `outside_home_market` is `yes` → add a market tag derived from
   `operating_market` (`MKT-DFW`, `MKT-TAMPA`, and so on). Same branch as any
   other applicant otherwise — the market tag just groups members geographically
   and flags which local occupancy and parking rules to raise on the call.
4. **Send email** — confirmation or decline, copy below.

The decline matters more than it looks. An operator with four flips today has
twelve in three years, and how you turn them down decides whether they come
back or go to a competitor.

---

## 3. Webhook B — Property submissions

**Workflow:** `WEB-B · Property Intake`
**Trigger:** Inbound Webhook → `GHL_PROPERTY_WEBHOOK_URL`

Deal flow from wholesalers, agents and owners — not student applications.
These contacts are a supply-side list and should never receive the program
nurture sequence.

Payload keys:

```
first_name, last_name, full_name, email, phone,
property_address, asking_price, property_specs, submitter_role,
notes, source, page, submitted_at
```

### Actions

1. **Create/Update Contact** — map name, email, phone, and the Property
   Submission fields.
2. **Add tag** `DEAL-SUBMITTED`, `SRC-WEBSITE`, and a role tag
   (`SUPPLY-WHOLESALER`, `SUPPLY-AGENT`, and so on).
3. **Create Opportunity** in the acquisitions pipeline, named
   `{{contact.property_address}}`. <span>Confirm which pipeline letter is
   free — this is deal flow, not student intake, and shouldn't sit in
   Pipeline A.</span>
4. **Internal notification** to whoever runs acquisitions.
5. **Send email** — acknowledgement.
6. **Wait** 3 days → if `analysis_verdict` is unset, internal reminder.

A wholesaler who sends one good property will send twenty more if you answer
quickly. Response time is the whole relationship here.

---

## 4. Webhook C — Buyer list

**Workflow:** `WEB-C · Buyer Qualification`
**Trigger:** Inbound Webhook → `GHL_BUYER_WEBHOOK_URL`

**Pipeline:** new buyer pipeline. I've called it **Pipeline D** below to
avoid colliding with A, B, and C in the existing Marcus system —
confirm that letter is free before building.

Payload keys:

```
first_name, last_name, full_name, email, phone,
buyer_funding, buyer_timeline, buyer_portfolio, buyer_criteria,
buyer_tier, source, page, submitted_at
```

`buyer_tier` is pre-computed by the handler so the workflow doesn't have
to re-derive it: `core` means funded and moving inside three months,
`nurture` means still researching or undecided on funding, `review`
means anything in between.

### Actions

1. **Create/Update Contact** — map name, email, phone, and all six buyer fields.
2. **Add tag** `D-001-BUYER-INQUIRY` and `SRC-WEBSITE`
3. **If/Else** on `buyer_tier`:
   - `core` → tag `D-002-BUYER-QUALIFIED`, create opportunity in Pipeline D,
     notify Brian and Gina, send the booking link for a criteria call.
   - `review` → tag `D-002-BUYER-REVIEW`, internal task to look at it manually.
     Don't auto-book; these need a human read.
   - `nurture` → tag `D-002-BUYER-NURTURE`, send the education sequence, no call.
4. **Send email** — confirmation, copy below.

### Proof of funds

Nothing on the site asks for proof of funds, on purpose — asking on a first
form kills conversion. Collect it on the criteria call and set `buyer_pof`
manually. A buyer without it should never receive an off-market address.

### Matching buyers to inventory

The payoff for all of this is the SmartList: `buyer_tier` is `core`, `buyer_pof`
is checked, and criteria match the property. That list is what makes the
promise on the builder side real — you can only tell an operator you'll bring
the buyer if you already have qualified buyers waiting.

---

## 5. Webhook D — Lender pre-qualification

**Workflow:** `WEB-E · Buyer Pre-Qualification`
**Trigger:** Inbound Webhook → `GHL_PREQUAL_WEBHOOK_URL`

Replaces the embedded GHL form on `for-buyers.html` with a native form so the
page matches the rest of the site. Same destination, better styling, and the
data arrives already triaged.

Payload:

```
first_name, last_name, full_name, email, phone,
buyer_state, buyer_funding, buyer_timeline, buyer_price_range,
prequal_status, buyer_notes, buyer_tier, source, page, submitted_at
```

`buyer_tier` is computed by the handler:
`registry_ready` (already pre-qualified and moving inside three months),
`send_to_lender` (funding identified, moving soon — hand to Rachelle),
`nurture` (just researching), `review` (anything else).

### Actions

1. **Create/Update Contact** with all buyer fields.
2. **Add tag** `D-001-BUYER-INQUIRY` and `SRC-WEBSITE`.
3. **If/Else** on `buyer_tier`:
   - `registry_ready` → tag `D-002-BUYER-QUALIFIED`, add to the buyer registry
     SmartList, notify Brian and Gina.
   - `send_to_lender` → notify Rachelle with the contact details and send the
     introduction email below.
   - `nurture` → education sequence, no lender handoff, no call.
   - `review` → internal task.

**Deliberately not collected:** SSN, income, assets, bank details, documents.
Those belong in Rachelle's own secure intake. Keep it that way — a marketing
site collecting financial documents is a liability with no upside.

---

## 6. Webhook E — Book waitlist

**Workflow:** `WEB-F · Book Download`
**Trigger:** Inbound Webhook → `GHL_BOOK_WAITLIST_WEBHOOK_URL`

Payload: `first_name, last_name, full_name, email, source, page, submitted_at`

### Actions

1. **Create/Update Contact**
2. **Add tag** `BOOK-DOWNLOAD`
3. **Add tag** `SRC-WEBSITE`
4. **Send email** — the book, copy below.
5. **Wait 5 days**, then send the follow-up below.
6. **Wait 10 days**, then a second follow-up — one, not a campaign.

The book is now the top of the funnel rather than a launch announcement.
It's 80 pages of the actual system, which means it does the selling: someone
who reads it and still wants coaching is a far warmer applicant than someone
who filled in a form off an ad.

Suppress anyone already tagged `A-001-APPLIED` — don't send book follow-ups
to someone who has already applied.

---

## 6. Tag index

Following `[Pipeline]-[Stage]-[Action]-[Result]`:

| Tag | Meaning |
|---|---|
| `A-000-STARTED` | Began an application, didn't finish |
| `A-001-APPLIED` | Operator applied through the website |
| `A-002-QUALIFIED-CORE` | Meets the bar, starting soon |
| `A-002-QUALIFIED` | Meets the bar, longer timeline |
| `A-002-REVIEW` | Borderline, needs a human read |
| `A-002-BELOW-BAR` | Under the experience or crew requirement |
| `A-002-NOT-YET` | Chose the information path; building toward the bar |
| `MKT-<CITY>` grouping | Which market the member operates in |
| `MKT-<CITY>` | Which market they operate in |
| `DEAL-SUBMITTED` | Property came in from the supply side |
| `SUPPLY-WHOLESALER` / `SUPPLY-AGENT` | Who sent it |
| `D-001-BUYER-INQUIRY` | Buyer came in through the website |
| `D-002-BUYER-QUALIFIED` | Funded and moving inside three months |
| `D-002-BUYER-REVIEW` | Needs a human read before a call |
| `D-002-BUYER-NURTURE` | Researching, not ready |
| `D-003-BUYER-POF` | Proof of funds on file |
| `BOOK-DOWNLOAD` | Downloaded the book |
| `BOOK-NURTURE-DONE` | Finished the two follow-ups |
| `SRC-WEBSITE` | Attribution |

---

## 7. Email copy

### Application received — sends immediately

Subject: `We got your application`

> Thanks for sending your background over.
>
> Brian or Gina will read it — an actual person, not a filter — and come back
> to you either way. If it's a fit we'll set up a call. If the timing isn't
> right yet, we'll tell you what would change that.
>
> — Green Light Buying Machine

### Below the bar — honest decline

Subject: `Not yet — here's what we'd want to see`

> Thanks for applying. Straight answer: we're looking for operators with ten
> to fifteen flips behind them and a crew already working, and you're not
> there yet.
>
> That's a timing problem, not a verdict on you. Keep building, and when
> you've got the volume and the crew, come back — we'd rather work with
> someone who learned it the hard way.
>
> In the meantime, the [FAQ] covers how the co-living model actually works.
>
> — Green Light Buying Machine

### Started but didn't finish — sends 1 hour after a partial

Subject: `You started an application`

> You got as far as your contact details and stopped. That's usually one of
> two things: either the experience questions gave you pause, or life got in
> the way.
>
> If it was the questions — we ask about completed flips and whether you run
> your own crew because the program only works for operators who already
> build. If you're close but not quite there, tell us where you are and we'll
> give you a straight answer about timing.
>
> [Finish your application]
>
> — Green Light Buying Machine

### Chose the information path — sends immediately

Subject: `Here's the book — come back when you're ready`

> Thanks for being straight with us about where you are. You're under the ten
> flips we look for, so we're not going to put you on a sales call.
>
> Here's the book instead. [link] It's the whole model — the buy box, the
> underwriting, the build standard, launch day. Nothing held back and nothing
> gated behind the program.
>
> Keep building. When you've got ten or more behind you and a crew you trust,
> email us and we'll pick this straight back up. A good number of our members
> were exactly where you are a couple of years ago.
>
> — Brian and Gina

### Pre-qualification introduction — sends when routed to the lender

Subject: `Introducing you to Rachelle`

> Thanks for sending this over. We've passed your details to Rachelle Coffey,
> the lender we work with.
>
> Rachelle finances PadSplit conversions specifically, which matters more than
> it sounds: a lender pricing this house against ordinary residential comps
> will undervalue what you're buying. She'll walk you through what you can
> close on and get you a pre-qualification letter.
>
> Once that's done you're on the list, and you'll hear from us when certified
> properties are listed.
>
> — Green Light Buying Machine

### Property received

Subject: `Got {{contact.property_address}}`

> Thanks for sending this over. We'll run it and come back to you with what we
> see — whether it converts, roughly what room count it supports, and what the
> conversion would involve.
>
> If it's a no, you'll get that too, with the reason. Send us the next one
> either way.

### Buyer list confirmation — sends immediately

Subject: `You're on the buyer list`

> Thanks for sending this over.
>
> We'll reach out to talk through what you're looking for — area, budget,
> and how the numbers need to work for you. Once we know that, you'll hear
> from us when a property matches, usually before it's listed anywhere.
>
> One thing worth saying now: co-living properties earn from multiple rooms,
> which means vacancy and management work differently than they do on a
> standard rental. We'd rather you understand that going in than find out
> in month three.
>
> — Green Light Buying Machine

### Book delivery — sends immediately

Subject: `Here's the book`

> Here it is. [link]
>
> Read it in order — the sequence matters, and every chapter builds on the one
> before it. We didn't hold anything back; this is the whole machine, not a
> teaser for something else.
>
> One thing worth saying up front: the goal isn't to understand this. It's to
> do it. Understanding without action is just entertainment.
>
> All green lights.
>
> — Brian and Gina

### Book follow-up, day 5

Subject: `Get to Chapter 4 yet?`

> The buy box chapter is where most people either lean in or realize this
> isn't for them. Both are useful answers.
>
> If you're leaning in and you've got ten or more flips behind you, the next
> step is applying. We take a small number of operators, we bring the deal,
> and we work to line up your buyer while you're still building. [Apply]
>
> If you're not there yet, keep reading. The book works on its own.
>
> — Brian and Gina

### Book follow-up, day 10 — last one

Subject: `The part the book can't do`

> The book gives you the system. What it can't do is walk a house with you,
> tell you the wall you're about to move is load-bearing, or hand you a buyer
> when you're finished.
>
> That's what the program is. If you want that, [apply here]. If not, we hope
> the book earns its keep either way.
>
> — Brian and Gina

---

## 8. Test before launch

- Submit the application with `More than 15` + `I run my own crew` +
  `Next available cohort` and confirm it tags `core` and books.
- On funnel.html, pick a `send me more info instead` option and confirm the
  notice appears, the button changes, and the submission tags `not_yet` with
  `intent: more_info` — and that no booking link is sent.
- Submit with `Fewer than 5` and confirm it tags `below_bar`, sends the
  decline, and creates no opportunity.
- Submit the property form and confirm it lands on the supply side and does
  NOT enter the program nurture sequence.
- On the landing page, complete step 1 and then close the tab. Confirm the
  contact exists with `A-000-STARTED` and no opportunity, and that the nudge
  fires an hour later.
- Then finish the same application with the same email and confirm it updates
  that contact rather than creating a second one.
- Fill the hidden `company` field via devtools and confirm the contact is
  *not* created — the route should return 200 and drop it.
- Submit the book form twice with the same email and confirm it updates
  rather than duplicating.
- Tag a test contact `A-001-APPLIED`, then submit the book form as that
  contact and confirm the follow-ups are suppressed.
- Submit the buyer form once as `Cash` + `Ready now` and confirm it tags
  `core`, and once as `Still figuring it out` + `Just researching` and
  confirm it tags `nurture` and does *not* send a booking link.
- Kill the webhook URL in Vercel env and confirm the form shows the error
  state instead of a false success.

---

## Open items

- Confirm Pipeline A's actual first stage name and whether website leads enter
  there or at a pre-stage.
- Decide who owns the SLA on deal analysis. The site promises "a few days" and
  that number should match what Brian and Gina can actually hold.
- Set the real fallback inbox in the site's form script — it currently reads
  `hello@example.com`.
- Decide whether unqualified leads get a standing nurture sequence or sit in a
  SmartList until someone works them.
- Confirm Pipeline D is a free letter in the existing Marcus system.
- Build a SmartList grouped by market tag. As members spread across the
  country, that grouping is how you keep track of which local rules and which
  buyer pools you're dealing with.
- Decide how buyer registration works outside Arizona. The registry is the
  thinnest part of a nationwide model — an operator in Tampa needs Tampa buyers,
  and that side has to be built market by market.
- Decide who owns buyer relationships. The builder side and the buyer side are
  different jobs, and running both out of one inbox is how the second one gets
  dropped.
- Settle what is promised to buyers in writing before any income figures go on
  the site. Selling a finished property with projected room income attached is
  a different regulatory posture than teaching a class, and the wording needs
  counsel.


---

## Webhook — Webinar registration

**Workflow:** `WEB-G · Webinar Registration`
**Trigger:** Inbound Webhook → `GHL_WEBINAR_WEBHOOK_URL`
**Page:** `/webinar`

Payload:

```
first_name, last_name, email, phone, city, state,
flips_completed, webinar_goal, source, page, submitted_at
```

### Actions

1. **Create/Update Contact** with all fields.
2. **Add tag** `WEBINAR-REGISTERED` and `SRC-WEBSITE`.
3. **Send email** immediately with the join link — the page tells people to
   expect it, so it has to arrive.
4. **Reminders:** 24 hours before, and 1 hour before. Attendance on a free
   webinar lives and dies on the reminder sequence.
5. **After the session,** split on attendance:
   - Attended → the replay plus a link to apply.
   - Didn't attend → the replay, then the apply link a day later.

`flips_completed` is the qualifier. Registrants at 10+ flips who attend are the
warmest applicants you'll get all year — tag them and treat the follow-up
accordingly.

**Set the join link before promoting the page.** The registration email is the
only thing standing between a signup and an attendee.
