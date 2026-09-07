# Green Light Buying Machine — Website to GHL Build

Two inbound webhooks, two workflows, one new custom field group. Everything
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

## 3. Webhook B — Book waitlist

**Workflow:** `WEB-B · Book Waitlist`
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

## 4. Tag index

Following `[Pipeline]-[Stage]-[Action]-[Result]`:

| Tag | Meaning |
|---|---|
| `A-001-DEAL-SUBMITTED` | Property came in through the website |
| `A-001-UNQUALIFIED-EXPERIENCE` | No completed renovations |
| `A-002-QUALIFIED-LIGHT` | 1–3 projects, needs human review |
| `A-002-QUALIFIED-CORE` | 4+ projects, straight to cohort conversation |
| `A-003-ANALYSIS-SENT` | Written verdict delivered |
| `BOOK-WAITLIST` | Wants the book at launch |
| `BOOK-PURCHASED` | Suppression tag for launch broadcast |
| `SRC-WEBSITE` | Attribution |

---

## 5. Email copy

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

## 6. Test before launch

- Submit the deal form with a real address. Confirm the contact, all seven
  custom fields, both tags, and the opportunity all land.
- Submit with `None yet` selected and confirm it takes the unqualified branch.
- Fill the hidden `company` field via devtools and confirm the contact is
  *not* created — the route should return 200 and drop it.
- Submit the waitlist form twice with the same email and confirm it updates
  rather than duplicating.
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
