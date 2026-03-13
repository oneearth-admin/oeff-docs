# OEFF Ana 1:1 Post-Call Action Plan — March 10, 2026

> **This document knows what it is.**
> Living plan for 10 action items from the Mar 10 Ana 1:1. Priority-ordered, session-resumable.

## Current Reality

| What Persists | What's Ephemeral |
|---------------|------------------|
| This plan file | Call context (captured in `ana-1on1-running.md`) |
| Contract files in `contracts/` | Exact conversation nuance |
| Email drafts in `email-drafts/` | Ana's verbal commitments (written up in shared notes GDoc) |
| `threads.json`, `action-state.json` | Licensing negotiation state (changes daily) |

## Reading This Plan

- **Resuming work** → Jump to first unchecked phase
- **New to this** → Read the Mar 10 entry in `ana-1on1-running.md` first
- **Reviewing** → Decision Log at bottom

## Overview

10 action items from the Mar 10 Ana 1:1. One is a blocker (squad@ broken), one is time-sensitive (invoice), the rest are this-week deliverables. Co-direction conversation happened — significant but no action item yet.

---

## 🔄 Phase 1: Fix squad@ Email List

**Priority:** BLOCKER — do first
**Goal:** Ana can send to squad@oneearthcollective.org and all 14 members receive it, including Garen.
**Constraint:** Must use Google Admin console (OEC account). Cannot test from personal account.

**Tools & Resources:**
- Google Admin console: admin.google.com → Groups → squad@
- Sync script: `~/tools/group-sync.py` (created the groups originally)
- Group membership doc: `~/Desktop/OEFF Clean Data/google-groups-team-doc.md` (14 members listed)
- Google Groups troubleshooting: check delivery settings, spam filters, posting permissions

**Tasks:**
- [ ] Log into Google Admin (OEC account) → Groups → squad@oneearthcollective.org
- [ ] Verify `garen@oneearthcollective.org` is in the member list
- [ ] Check group settings: Who can post? Is there a moderation queue? Delivery setting (each email vs digest)?
- [ ] Check Garen's Gmail spam/filters for squad@ messages
- [ ] If member missing: run `python3 ~/tools/group-sync.py` or add manually
- [ ] Test: send to squad@ from OEC account, confirm Garen receives
- [ ] Reply to Ana confirming fix

**Gate:** Garen receives a test email sent to squad@.

---

## 🔲 Phase 2: Invoice (Garen + Tell Erin)

**Priority:** HIGH — you've been working unpaid since November
**Goal:** Submit back-pay invoice (Nov 2025–Feb 2026) to finance@oneearthcollective.org. Notify Erin she can invoice too.
**Constraint:** Invoice by 5th of following month (per contract). Back-pay requires itemized hour log within 2 weeks of signing. Keep under 75% cap trigger ($7,500) unless you want to trigger the check-in conversation.

**Tools & Resources:**
- Garen's contract: `~/Desktop/OEFF Clean Data/contracts/garen-contract-v2.md` (rate: $70/hr, cap: $10,000, back-pay clause at line 100-102)
- Erin's contract: `~/Desktop/OEFF Clean Data/contracts/erin-contract-v2.md` (rate: $45/hr, cap: $5,490)
- Both invoice to: finance@oneearthcollective.org
- Format: brief descriptions of work completed + hours

**Tasks:**
- [ ] Draft Garen invoice with line items:

| Period | Work Description | Est. Hours | Amount |
|--------|-----------------|------------|--------|
| Nov–Dec 2025 | Pre-contract planning: scoping, budget structure, contractor evaluation | ~20 hrs | $1,400 |
| Jan 2026 | Infrastructure: host guide, Google Groups, Airtable architecture, Eventbrite setup, Kim/Erin onboarding | ~28 hrs | $1,960 |
| Feb 2026 | Communication systems: email templates, filmmaker outreach, meeting facilitation, process documentation | ~27 hrs | $1,890 |
| **Total** | | **~75 hrs** | **$5,250** |

- [ ] Adjust hours to reflect actual work (estimates above are from contract phases — true up)
- [ ] Send invoice to finance@oneearthcollective.org
- [ ] Email Erin: "We're clear to invoice — submit to finance@oneearthcollective.org, monthly, brief descriptions + hours. Your cap is $5,490."
- [ ] Note: March invoice due by April 5

**Gate:** Invoice sent. Erin notified.

---

## 🔲 Phase 3: Squad Meeting Tech Updates

**Priority:** Due tomorrow AM (Tue Mar 11)
**Goal:** Written tech updates in squad meeting notes so the team has visibility even if Garen can't attend.
**Constraint:** Outcome-focused language, not infrastructure language. Ana will share if Garen is absent.

**Tools & Resources:**
- Squad meeting notes doc: _(need link from Ana or Kim — check Ana-Kim shared doc, or the shared running doc)_
- Content sources: this plan, `ana-1on1-running.md` Mar 10 entry, `eventbrite-state.json`, `google-groups-team-doc.md`

**Tasks:**
- [ ] Get squad meeting notes doc link (ask Ana, or find in Kim/Ana shared notes)
- [ ] Write tech update section (~5 bullets):
  - Email groups live: squad@ (14), core@ (7), interns@ (4) — [reference doc link]
  - Host guide live at hosts.oneearthfilmfest.org — accepting intake forms
  - 14 Eventbrite events ready (unlisted/preview) — public launch pending
  - Filmmaker outreach in progress — licensing status being compiled
  - Open captions plan underway for CCC screenings
- [ ] Paste into squad meeting notes doc
- [ ] Tell Ana it's there so she can present if needed

**Gate:** Updates visible in shared doc before Tuesday meeting.

---

## 🔲 Phase 4: Consolidate Kim Contract

**Priority:** This week
**Goal:** Move festival week on-site scope from "Proposed" to confirmed in Kim's contract. One budget line: $3,120 total ($1,920 pre-fest + $1,200 fest week).
**Constraint:** Contract is in lawyer's hands — check if edits are still possible, or if this needs an addendum. The contract itself says "a brief addendum or written acknowledgment will confirm" fest week.

**Tools & Resources:**
- Kim's contract (local): `~/Desktop/OEFF Clean Data/contracts/kim-contract-v2.md`
- Kim's contract (GDoc): [link](https://docs.google.com/document/d/1SHBuuGBZjmNvKmFvj35PcXzLebtfuDjkmemKnhrvYxo/edit)
- Budget breakdown: `~/Desktop/OEFF Clean Data/budget/2026-tech-ops-budget-breakdown.md`

**Tasks:**
- [ ] Edit `kim-contract-v2.md`:
  - Line 15: Budget → $3,120 (~78 hrs at $40/hr)
  - Line 20: Remove "Festival week on-site support... is scoped and budgeted separately"
  - Section "Festival Week On-Site Support — Proposed": change header to "Festival Week On-Site Support" (remove "Proposed")
  - Line 99: Update compensation from "TBD" to "$1,200 (~30 hrs @ $40/hr)"
  - Line 101: Remove "Festival week scope is proposed but not yet committed" paragraph
  - Hour allocation table: add festival week row ($1,200), update total to $3,120
- [ ] Push updated contract to GDoc: `gdocs push contracts/kim-contract-v2.md --account oec --update`
- [ ] Flag to Ana: "Kim contract updated — fest week confirmed, one budget line, $3,120 total"

**Gate:** Contract reflects single budget. GDoc updated. Ana notified.

---

## 🔲 Phase 5: Host Helper Plan (with Kim)

**Priority:** EOW (Mar 14)
**Goal:** One-pager defining what hosts receive from OEFF pre-fest. Shared with Ana by Friday.
**Constraint:** Must feel like a partnership deliverable, not a top-down mandate. Kim co-authors — she's the one executing it.

**Tools & Resources:**
- Host guide (live): [hosts.oneearthfilmfest.org](https://hosts.oneearthfilmfest.org)
- Host intake form: hosted in OEC Google account
- Host onboarding runbook: `~/Desktop/OEFF Clean Data/host-onboarding-runbook.md`
- Host helper session summary: `~/Desktop/OEFF Clean Data/host-helper-session-summary.md`
- Host helper migration plan: `~/Desktop/OEFF Clean Data/host-helper-migration-plan.md`
- Kim meeting notes: [GDoc](https://docs.google.com/document/d/1C_5AuN-Glj-xnn9t_Q5nC5DB5KkxuMWLP8u5hk1X5rw/edit)
- Ana's ask: connect Garen with KCA and Bethel contacts (for host helper context)

**Tasks:**
- [ ] Read `host-helper-migration-plan.md` and `host-helper-session-summary.md` for existing thinking
- [ ] Kim sync: frame as "what do hosts get between now and April 1?"
  - Packet contents: guide link, run-of-show template, FAQ, venue-specific info sheet
  - Delivery format: email with links? Single PDF? Google Doc per venue?
  - Training: webinar date? Recording distribution?
  - Escalation: who do hosts contact during fest week?
- [ ] Draft one-pager with Kim
- [ ] Send to Ana by Friday with "What do you think?" framing
- [ ] Follow up on Ana connecting Garen with KCA and Bethel contacts

**Gate:** One-pager sent to Ana by Mar 14. Kim co-owns it.

---

## 🔲 Phase 6: Climate Action Museum Outreach

**Priority:** This week
**Goal:** Explore upgrading Climate Action Museum (Evanston) from community to flagship. Warm outreach.
**Constraint:** Exploratory — not committing to flagship yet. Check personal connection first.

**Tools & Resources:**
- Current venue data: Climate Action Evanston, hosting "Plastic People" (Sat 4/23 or similar)
- Venue resource matrix: `~/Desktop/OEFF Clean Data/venue-resource-matrix.json`
- Roadmap: `~/Desktop/OEFF Clean Data/roadmap-2026-host-venues.json`

**Tasks:**
- [ ] Check personal connection — who do you know at Climate Action Museum?
- [ ] Review current venue data (capacity, AV, contact)
- [ ] If upgrading to flagship: what changes? (More OEFF staffing, Erin capture, expanded programming)
- [ ] Draft warm outreach: "We're looking at expanding some screenings — would love to chat about what that could look like"
- [ ] Send

**Gate:** Outreach sent or decision made to keep as community.

---

## 🔲 Phase 7: Filmmaker Licensing Numbers for Ana + Josh

**Priority:** This week
**Goal:** Clean summary of licensing status so Ana + Josh can set early access pricing.
**Constraint:** Simple table format. No infrastructure language. They need: film, fee, status.

**Tools & Resources:**
- Inbox triage (from this session): ~5 confirmed/quoted, ~5 pending
- Email threads: `~/inboxes/threads.json`
- Action state: `~/inboxes/action-state.json`
- Filmmaker merge sheet: [GDoc](https://docs.google.com/spreadsheets/d/1eFyEiENnjiOdy5eYAVwZUpWKvtfxhdZ2L-_YlWSSxFQ/edit)
- Email drafts: `~/Desktop/OEFF Clean Data/email-drafts/2026-03-04-filmmaker-outreach-full.html`

**Tasks:**
- [ ] Compile licensing status table:

| Film | Distributor/Contact | Fee | Status |
|------|-------------------|-----|--------|
| Drowned Land | Colleen Thurston | $300 | Confirmed 3/6 |
| Beyond Zero | Nathan Havey | FREE | Confirmed |
| Rails to Trails | Dan Protess | FREE | Confirmed |
| 40 Acres | Magnolia / Danielle | $350 (2 screenings) | Quoted, awaiting Ana approval |
| That Which Once Was | Kimi Takesue | $350-400 | Quoted, awaiting Garen confirm |
| Planetwalker | Dominic Shaw | $650 (corrected to 3 screenings) | Quoted, awaiting response |
| In Our Nature | James Parker | TBD (tier-dependent) | Rates provided, Garen to confirm |
| Rooted | Lauren Waring Douglas | TBD | Asked for nonprofit rate, no response |
| How to Power a City | Melanie La Rosa | TBD | Asked, no response (OOO) |
| Jane Goodall | John Wickstrom / Cosmic Picture | TBD | Asked, no response |
| Plastic People | Ruth Pindilli / White Pine | TBD | Asked, no response |

- [ ] Verify against `threads.json` and merge sheet for any updates since triage
- [ ] Format as email or add to merge sheet
- [ ] Send to Ana + Josh: "Here's where we are on licensing — need your input on [40 Acres approval, early access pricing]"

**Gate:** Ana + Josh have current licensing numbers.

---

## 🔲 Phase 8: Film Ingestion Timeline

**Priority:** This week (async with Ana)
**Goal:** Clear timeline from licensing signature → film delivery → QC → open captions → venue-ready.
**Constraint:** Packet delivery target is April 1. Working backwards: need licensing signed by ~March 17 to hit that date.

**Tools & Resources:**
- QC checklist: referenced in Garen's contract Area 1
- `/oeff-caption` skill: for open captions pipeline
- Budget: captioning cost = Ana's budget; gear cost = OEFF tech ops
- CCC tech team: coordinate early for Jane Goodall DCP
- Columbia tech team: may have capacity for open captions support

**Tasks:**
- [ ] Draft timeline:

| Milestone | Target Date | Depends On |
|-----------|------------|------------|
| Licensing agreements signed (first batch) | Mar 17 | Ana approval on quoted fees |
| Filmmakers send screening copies | Mar 17-21 | Signed agreements + file delivery specs |
| Garen runs QC on received files | Mar 21-25 | Files received |
| Open captions burn (Jane Goodall DCP + others) | Mar 25-28 | QC pass + captioning files |
| Venue-ready packages assembled | Mar 28-31 | All above |
| **Packet delivery to hosts** | **Apr 1** | **All above** |

- [ ] Identify blockers: which films are at risk of missing the timeline?
- [ ] Research: Chicago shared equipment library for captioning gear (TV monitors?)
- [ ] Research: lower thirds feasibility — how hard? What gear?
- [ ] Reach out to CCC tech team re: Jane Goodall DCP coordination
- [ ] Reach out to Columbia tech team re: open captions capacity
- [ ] Share timeline with Ana: "Here's the path to April 1 — licensing signatures are the gate"

**Gate:** Timeline shared. CCC + Columbia outreach started. Ana knows the March 17 licensing deadline.

---

## 🔲 Phase 9: Filmmaker Accessibility Responses

**Priority:** Reactive — flag to Ana this week
**Goal:** Be ready to respond to filmmaker accessibility questions. Know what OEFF provides.
**Constraint:** Cost commitments need Ana's sign-off. Garen can answer technical questions autonomously.

**Tools & Resources:**
- Open captions plan (from this call): Ana covers captioning cost, OEFF covers gear
- Live captioning: 2 events (live content — Q&A, panels), not the films
- `/oeff-caption` skill for technical pipeline
- Budget: accessibility line in `2026-tech-ops-budget-breakdown.md` Section 5 (~$800-1,500, separate from tech ops)

**Tasks:**
- [ ] Draft standard accessibility response template:
  - What OEFF provides: open captions on screening copies, live captioning for select events
  - What we need from filmmakers: SRT files if available, or we'll generate via Rev
  - File delivery format preferences: DCP with baked captions preferred for CCC; ProRes/H.264 for others
- [ ] Flag to Ana: "Filmmaker accessibility questions may start coming in — here's what I'll say. Loop you on anything with cost implications."
- [ ] James Parker (In Our Nature) asked for festival laurel — respond or confirm OEFF doesn't have one

**Gate:** Template ready. Ana aware. James Parker responded to.

---

## 🔲 Phase 10: Joana Outreach (PARKED — Next Call)

**Priority:** Next Ana 1:1
**Goal:** Coordinate with Ana before reaching out to Joana.
**Constraint:** Do NOT reach out before talking to Ana.

**Tasks:**
- [ ] Add to next 1:1 agenda: "I'd like to reach out to Joana about [X] — wanted to check with you first"
- [ ] Prep: what specifically do you want from Joana? Have the ask clear before the call.

**Gate:** Ana gives the green light.

---

## Decision Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Kim contract: consolidate to one budget line | Simpler for everyone. Fest week was always the plan, "proposed" language was a soft start. | Mar 10 |
| Garen + Erin invoice now | Contracts in force. Back-pay clause covers Nov-Feb. People should be paid. | Mar 10 |
| DCP with open captions for Jane Goodall | CCC is a flagship, Jane Goodall is high-profile. Open captions in the DCP is the right format for this venue. | Mar 10 |
| KCA + BGE fest-sponsored | Community orgs shouldn't be priced out. Fest absorbs the cost. | Mar 10 |
| Live captioning = live content, not films | Captioning the Q&A/panels/discussion, not the film screenings themselves. Films get open captions separately. | Mar 10 |
| Co-direction: open and curious | Garen expressed openness to exploring co-direction with Ana. Significant shift in the relationship. No action item yet — let it breathe. | Mar 10 |

---

## Session Protocol

**Start:** Read this plan → find first unchecked phase → check `ana-1on1-running.md` for context
**End:** Check off tasks → update decision log if anything changed → commit

---

*Plan created: March 10, 2026*
*Source: Ana 1:1 call + post-call debrief*
*Next review: March 14 (host helper EOW deadline)*
