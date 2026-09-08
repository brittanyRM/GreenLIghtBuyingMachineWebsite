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
| Applicant Tier | `applicant_tier` | Dropdown |

Dropdown options must match the form exactly.
`completed_flips`: `Fewer than 5`, `5 to 9`, `10 to 15`, `More than 15`.
`crew_status`: `I run my own crew`, `I use the same trades on every job`,
`I hire per project`, `I'd need to build one`.
`applicant_tier`: `core`, `qualified`, `review`, `below_bar` — set by the
handler, don't edit by hand.

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

## 5. Webhook D — Book waitlist

**Workflow:** `WEB-D · Book Waitlist`
**Trigger:** Inbound Webhook → `GHL_BOOK_WAITLIST_WEBHOOK_URL`

Payload: `first_name, last_name, full_name, email, source, page, submitted_at`

### Actions

1. **Create/Update Contact**
2. **Add tag** `BOOK-WAITLIST`
3. **Add tag** `SRC-WEBSITE`
4. **Send email** — confirmation, copy below.
5. **Stop.** No drip.

The page promises one email at launch. Honor it. A waitlist that starts
selling the $15k program four days later burns a list you'll only get to
use once.

**On launch day:** SmartList on `BOOK-WAITLIST` and not `BOOK-PURCHASED`,
single broadcast. That list is also the cleanest audience for a Pipeline B
reactivation later, but give it the book first.

---

## 6. Tag index

Following `[Pipeline]-[Stage]-[Action]-[Result]`:

| Tag | Meaning |
|---|---|
| `A-001-APPLIED` | Operator applied through the website |
| `A-002-QUALIFIED-CORE` | Meets the bar, starting soon |
| `A-002-QUALIFIED` | Meets the bar, longer timeline |
| `A-002-REVIEW` | Borderline, needs a human read |
| `A-002-BELOW-BAR` | Under the experience or crew requirement |
| `DEAL-SUBMITTED` | Property came in from the supply side |
| `SUPPLY-WHOLESALER` / `SUPPLY-AGENT` | Who sent it |
| `D-001-BUYER-INQUIRY` | Buyer came in through the website |
| `D-002-BUYER-QUALIFIED` | Funded and moving inside three months |
| `D-002-BUYER-REVIEW` | Needs a human read before a call |
| `D-002-BUYER-NURTURE` | Researching, not ready |
| `D-003-BUYER-POF` | Proof of funds on file |
| `BOOK-WAITLIST` | Wants the book at launch |
| `BOOK-PURCHASED` | Suppression tag for launch broadcast |
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

### Book waitlist confirmation

Subject: `You're on the list`

> You'll get one email from us the day *The Green Light Buying Machine* is
> available. Nothing before that.
>
> If you'd rather not wait: send us an Arizona property and we'll tell you
> whether it converts. Same analysis the book teaches, applied to your actual
> deal. [link]
>
> — Brian and Gina

---

## 8. Test before launch

- Submit the application with `More than 15` + `I run my own crew` +
  `Next available cohort` and confirm it tags `core` and books.
- Submit with `Fewer than 5` and confirm it tags `below_bar`, sends the
  decline, and creates no opportunity.
- Submit the property form and confirm it lands on the supply side and does
  NOT enter the program nurture sequence.
- Fill the hidden `company` field via devtools and confirm the contact is
  *not* created — the route should return 200 and drop it.
- Submit the waitlist form twice with the same email and confirm it updates
  rather than duplicating.
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
- Decide who owns buyer relationships. The builder side and the buyer side are
  different jobs, and running both out of one inbox is how the second one gets
  dropped.
- Settle what is promised to buyers in writing before any income figures go on
  the site. Selling a finished property with projected room income attached is
  a different regulatory posture than teaching a class, and the wording needs
  counsel.
