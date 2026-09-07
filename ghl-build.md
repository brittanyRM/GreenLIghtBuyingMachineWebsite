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

**Group: Deal Analysis**

| Field name | Key | Type |
|---|---|---|
| Property Address | `property_address` | Single line |
| Asking Price | `asking_price` | Single line |
| Property Specs | `property_specs` | Single line |
| Completed Renovations | `completed_renovations` | Dropdown |
| Deal Notes | `notes` | Multi line |
| Analysis Verdict | `analysis_verdict` | Dropdown |
| Analysis Sent On | `analysis_sent_on` | Date |

`completed_renovations` options must match the form exactly: `None yet`,
`1 to 3`, `4 to 10`, `More than 10`.

`analysis_verdict` options: `Converts`, `Converts with conditions`,
`Does not convert`, `Not analyzed`. This one is set by hand after the
analysis, and it drives the follow-up branch.

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

## 2. Webhook A — Deal analysis

**Workflow:** `WEB-A · Deal Analysis Intake`
**Trigger:** Inbound Webhook

Copy the trigger URL into `GHL_DEAL_WEBHOOK_URL` on Vercel. Submit the live
form once before you map anything — GHL only exposes payload fields after it
has captured a real sample.

Payload keys arriving from the route handler:

```
first_name, last_name, full_name, email, phone,
property_address, asking_price, property_specs,
completed_renovations, notes, source, page, submitted_at
```

### Actions, in order

1. **Create/Update Contact** — map name, email, phone, then every custom field
   above by matching key.
2. **Add tag** `A-001-DEAL-SUBMITTED`
3. **Add tag** `SRC-WEBSITE`
4. **Create Opportunity** — Pipeline A, first stage, opportunity name
   `{{contact.property_address}}`, value blank until the analysis is done.
5. **Internal notification** — SMS or email to Brian and Gina with the address
   and the experience level. This is the one action worth getting right on day
   one: the promise on the site is an answer within a few days, and nothing
   erodes that faster than a submission sitting unseen.
6. **Send email** — confirmation, copy below.
7. **Wait** 3 days.
8. **If/Else** — has `analysis_verdict` been set?
   - No → internal reminder to Brian and Gina. This is the SLA backstop.
   - Yes → continue.

### Qualification branch

Split on `completed_renovations`:

- **None yet** → tag `A-001-UNQUALIFIED-EXPERIENCE`. Still send the property
  analysis, since it was promised, but route to a nurture list rather than the
  cohort conversation. These people are worth keeping — some of them will have
  three projects done in eighteen months.
- **1 to 3** → tag `A-002-QUALIFIED-LIGHT`. Human review before a cohort offer.
- **4 to 10 / More than 10** → tag `A-002-QUALIFIED-CORE`, move opportunity to
  the next Pipeline A stage, and trigger the existing intake sequence.

---

## 3. Webhook B — Buyer list

**Workflow:** `WEB-B · Buyer Qualification`
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

## 4. Webhook C — Book waitlist

**Workflow:** `WEB-C · Book Waitlist`
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

## 5. Tag index

Following `[Pipeline]-[Stage]-[Action]-[Result]`:

| Tag | Meaning |
|---|---|
| `A-001-DEAL-SUBMITTED` | Property came in through the website |
| `A-001-UNQUALIFIED-EXPERIENCE` | No completed renovations |
| `A-002-QUALIFIED-LIGHT` | 1–3 projects, needs human review |
| `A-002-QUALIFIED-CORE` | 4+ projects, straight to cohort conversation |
| `A-003-ANALYSIS-SENT` | Written verdict delivered |
| `D-001-BUYER-INQUIRY` | Buyer came in through the website |
| `D-002-BUYER-QUALIFIED` | Funded and moving inside three months |
| `D-002-BUYER-REVIEW` | Needs a human read before a call |
| `D-002-BUYER-NURTURE` | Researching, not ready |
| `D-003-BUYER-POF` | Proof of funds on file |
| `BOOK-WAITLIST` | Wants the book at launch |
| `BOOK-PURCHASED` | Suppression tag for launch broadcast |
| `SRC-WEBSITE` | Attribution |

---

## 6. Email copy

### Deal analysis confirmation — sends immediately

Subject: `We've got {{contact.property_address}}`

> Thanks for sending this over.
>
> Brian or Gina will look at the property and come back to you with whether it
> converts, roughly what room count it supports, and what the conversion would
> involve. That usually takes a few days.
>
> If the answer is no, you'll get that too, along with the reason. A quick no
> on the wrong house is worth more than a slow maybe.
>
> — Green Light Buying Machine

### Analysis delivered — sent manually or triggered by `analysis_verdict`

Subject: `Your analysis on {{contact.property_address}}`

> Here's what we found. [analysis]
>
> If you want to talk through what a conversion on this one would actually
> look like, reply and we'll set up a call.

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

## 7. Test before launch

- Submit the deal form with a real address. Confirm the contact, all seven
  custom fields, both tags, and the opportunity all land.
- Submit with `None yet` selected and confirm it takes the unqualified branch.
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
