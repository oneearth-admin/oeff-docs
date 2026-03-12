# OEFF 2026 Filmmaker Pipeline — Airtable Operations Plan

**Date:** 2026-03-12 (41 days to festival)
**Author:** Garen
**Audience:** Ana (dashboard), Kim (follow-ups), Garen (QC), interns (assignments)
**Purpose:** Add the minimum Airtable fields, views, and automations to track each film from outreach through venue-confirmed playback

---

## Current State

Outreach went out March 5 via Mailmeteor. 12 films across 4 campaigns. Responses are landing in the merge sheet but aren't flowing into Airtable. The Events table has licensing fields — all 0/31 populated for 2026. The Film Contacts table is missing 3 of 12 films (Beyond Zero, 40 Acres, CAM). The file pipeline tools (`oeff-file-tracker.py`) already talk to Airtable for receive/QC/deliver/confirm — but there's no upstream tracking for the outreach-through-licensing phase.

The gap: nothing connects "we emailed the filmmaker" to "their file passed QC and reached the venue."

---

## 1. Field Additions

### Films Table (12 records)

| Field | Type | Purpose | Who populates | When | Tool |
|-------|------|---------|---------------|------|------|
| `Outreach Status` | Single Select | Track outreach state per film | Kim or Garen | After each send/response | Manual or sync script |
| | Options: `Not Sent`, `Sent`, `Responded`, `Follow-Up Needed`, `No Response` | | | | |
| `Outreach Sent Date` | Date | When the initial outreach email went out | Garen | After Mailmeteor send | Manual (one-time backfill from merge sheet) |
| `Last Contact Date` | Date | Most recent communication with filmmaker | Kim | After any email exchange | Manual |
| `File Status` | Single Select | Where the film file is in the receive-through-QC pipeline | Garen or intern | As files arrive | `oeff-file-tracker.py` |
| | Options: `Not Received`, `Received`, `QC In Progress`, `QC Passed`, `QC Failed`, `Normalized`, `Packaged` | | | | |
| `File Received Date` | Date | When the film file arrived | Intern or Garen | On receipt | `oeff-file-tracker.py received` |
| `QC Assigned To` | Single Select | Which intern is running QC | Garen | At assignment | Manual |
| | Options: intern names + `Garen` + `Unassigned` | | | | |
| `QC Notes` | Long Text | Failure reasons, re-submission notes, format issues | Intern or Garen | During QC | `oeff-file-tracker.py qc-fail --reason` |
| `Runtime (minutes)` | Number | Verified film runtime for scheduling | Intern | After file receipt or from intake survey | Manual or sync |
| `Social Handles` | Long Text | Filmmaker social media for promo | Kim or intern | From supplemental form | Sync from "Airtable Ready" sheet |
| `Premiere Status` | Single Select | Premiere tier for marketing | Kim | From supplemental form | Sync |
| | Options: `Chicago-area premiere`, `Midwest premiere`, `US premiere`, `Not a premiere`, `Unknown` | | | | |

**Total: 11 new fields.** The existing fields (Trailer Link, Caption Status, Audio Description, etc.) stay as-is. `File Status` replaces whatever the file tracker currently writes — verify the tracker's target field name before adding.

### Film Contacts Table (9 records — needs 3 more)

| Field | Type | Purpose | Who populates | When | Tool |
|-------|------|---------|---------------|------|------|
| `Licensing Rate Quoted` | Currency | The per-screening nonprofit rate the filmmaker quoted | Josh or Ana | When filmmaker responds to outreach | Manual |
| `Q&A Available` | Single Select | Filmmaker attendance for post-screening | Kim | From supplemental form | Sync |
| | Options: `Yes — in person`, `Yes — virtually`, `Maybe`, `No`, `Unknown` | | | | |
| `Q&A Contact Name` | Single Line Text | Name of person doing the Q&A (if different from primary) | Kim | From supplemental form | Sync |
| `Q&A Contact Email` | Email | Their email | Kim | From supplemental form | Sync |

**Also needed:** Create 3 new records for Beyond Zero (Nathan Havey), 40 Acres (Dan McCarthy / Magnolia), and CAM Awards. Contact info is in the merge sheet.

**Total: 4 new fields + 3 new records.**

### Events Table (219 records total, ~31 are 2026)

The licensing fields already exist. No new fields needed — just populate them.

| Existing Field | What to Populate | Source |
|----------------|-----------------|--------|
| `Licensing Request Status` | `Sent`, `Responded`, `Agreed`, `N/A` | Merge sheet → outreach status |
| `License Status` | `Pending`, `Agreed`, `Invoiced`, `Paid`, `Waived`, `N/A` | Email responses |
| `Film License Amount` | Dollar amount per screening | Filmmaker response |
| `Film Licensing Contact` | Name from Film Contacts | Link to Film Contacts table |
| `License Invoice Received` | Checkbox — did we get the invoice? | Ana or Josh |
| `License Invoice Paid` | Checkbox — did we pay it? | Ana |

**One field to add:**

| Field | Type | Purpose | Who populates | When | Tool |
|-------|------|---------|---------------|------|------|
| `Delivery Status` | Single Select | Track file delivery per event (per-venue, not per-film) | Garen or intern | After delivery | `oeff-file-tracker.py deliver` |
| | Options: `Not Started`, `Delivered`, `Confirmed`, `Playback Tested` | | | | |

The file tracker already tracks delivery status — this field gives it a home in the Events table where it belongs (a film screened at 3 venues has 3 delivery statuses).

**Total: 1 new field. 6 existing fields to populate.**

### Tables NOT Modified

- **Venues** — already has what it needs (tier, contacts, AV info). Delivery status lives on Events, not Venues.
- **Contractors** — no changes.
- **Timeline** — no changes.
- **SOPs** — no changes.

---

## 2. Key Views

### View A: Ana's Dashboard

**Table:** Films
**View type:** Kanban (grouped by `Outreach Status`)
**Purpose:** Ana checks this once a day. In 30 seconds she sees: how many films responded, how many are pending, what's blocked.

**Kanban columns (left to right):**

| Column | What it means |
|--------|--------------|
| Not Sent | Outreach hasn't gone out (should be 0 after March 5) |
| Sent | Waiting for response |
| Responded | Filmmaker replied — licensing conversation in progress |
| Follow-Up Needed | Flagged for re-contact |
| No Response | Past deadline, no reply |

**Card fields (what shows on each card):**
1. Film Title
2. File Status (color-coded pill)
3. Last Contact Date
4. Screening count (from linked Events)

**Sort:** Last Contact Date, oldest first (stale items rise to the top)

**Filter:** None — all 12 films visible. This is the full picture.

**Why Kanban:** Ana thinks in "what stage is each thing at" — Kanban answers that without reading a table. Five columns is scannable. Grid would require her to mentally group rows by status.

---

### View B: Garen's QC Pipeline

**Table:** Films
**View type:** Grid
**Purpose:** Garen checks this when working the file pipeline. Shows only films that need QC attention — files received but not yet through QC.

**Filter:**
- `File Status` is any of: `Received`, `QC In Progress`, `QC Failed`

**Sort:**
1. `File Received Date` — ascending (oldest files first = most urgent)
2. Then by `Film Title` — alphabetical

**Visible fields (6):**

| # | Field | Why |
|---|-------|-----|
| 1 | Film Title | Identify the film |
| 2 | File Status | Current QC state |
| 3 | File Received Date | How long it's been sitting |
| 4 | QC Assigned To | Who's on it |
| 5 | Caption Status | Captions are the most common QC issue |
| 6 | QC Notes | Failure reasons, re-submission context |

**Grouping:** By `File Status` — so "QC Failed" films are visually separated from "Received" (not yet started).

**Hidden fields:** Everything else. This view is intentionally narrow — when you're doing QC, you don't need to see Outreach Status or Premiere Status.

---

### View C: Kim's Follow-Up Queue

**Table:** Films
**View type:** Grid
**Purpose:** Kim works through this list daily. Shows films where outreach was sent but no response came back — sorted so the most overdue are at the top.

**Filter:**
- `Outreach Status` is any of: `Sent`, `Follow-Up Needed`, `No Response`
- `Outreach Sent Date` is not empty

**Sort:**
1. `Outreach Sent Date` — ascending (longest-waiting first)

**Visible fields (7):**

| # | Field | Why |
|---|-------|-----|
| 1 | Film Title | Identify the film |
| 2 | Outreach Status | Current state |
| 3 | Outreach Sent Date | When we reached out |
| 4 | Last Contact Date | Last time we heard anything |
| 5 | Intake Received | Did they submit the survey? |
| 6 | Notes | Context for the follow-up conversation |
| 7 | Linked Film Contacts → Email | Quick access to the contact |

**Grouping:** By `Outreach Status` — "No Response" group at top (most urgent), "Follow-Up Needed" next, "Sent" last.

**Color coding (row coloring):**
- Red: `Outreach Sent Date` is more than 10 days ago and status is still `Sent` — overdue
- Yellow: `Follow-Up Needed`
- No color: `Sent` within the last 10 days — still in the response window

---

### View D: Intern QC Assignments

**Table:** Films
**View type:** Grid (Gallery would work too, but Grid is more practical for checklists)
**Purpose:** Interns open this view to see what's assigned to them. Each row is a film they need to QC.

**Filter:**
- `QC Assigned To` is not empty
- `File Status` is any of: `Received`, `QC In Progress`, `QC Failed`

**Sort:**
1. `QC Assigned To` — alphabetical (each intern sees their block)
2. Then `File Received Date` — ascending

**Visible fields (8):**

| # | Field | Why |
|---|-------|-----|
| 1 | Film Title | What film |
| 2 | QC Assigned To | Whose assignment |
| 3 | File Status | Where it is |
| 4 | File Received Date | How long it's been waiting |
| 5 | Caption Status | Most common QC issue |
| 6 | Audio Description | Accessibility check |
| 7 | Formats Available (from Film Contacts) | What format to expect |
| 8 | QC Notes | Where to log findings |

**Grouping:** By `QC Assigned To`

**Why this works for interns:** They don't need to see the whole Films table. This view says "here are your films, here's what to check, here's where to write notes." One decision per row: run QC, log the result.

---

## 3. Automations (5)

These are ranked by value. If OEFF's Airtable plan limits automations, implement them in this order.

### Automation 1: Flag Overdue Outreach

**Trigger:** Every day at 9:00 AM, check Films where `Outreach Status` = `Sent` AND `Outreach Sent Date` is more than 7 days ago.

**Action:** Update `Outreach Status` to `Follow-Up Needed`.

**Why it's worth an automation slot:** Without this, Kim has to manually calculate "has it been a week?" for each film. The automation does the calendar math and moves the card into her Follow-Up queue automatically. With 12 films and 41 days left, one falling through the cracks is a real risk.

---

### Automation 2: Notify on File Received

**Trigger:** When `File Status` changes to `Received` on any Films record.

**Action:** Send an email to Garen with the film title, received date, and a link to the Airtable record.

**Why it's worth an automation slot:** File arrivals are unpredictable — filmmakers send links at random times via random channels. This ensures Garen knows the moment a file is logged, so QC assignment happens the same day rather than waiting for the next time someone checks the table.

---

### Automation 3: Licensing Status Roll-Up

**Trigger:** When `License Status` changes on any Events record (2026 filter).

**Action:** If ALL events linked to a film have `License Status` = `Agreed` or `Paid` or `Waived`, update the film's `Outreach Status` to `Responded` (if it's still `Sent`). — Actually, this is better handled by a rollup field + conditional formatting than an automation. **Revised:** Use a Rollup field on Films that counts linked Events where `License Status` is empty. If 0, all screenings are licensed.

**Replaced with field:** Add a Rollup field `Unlicensed Screenings` on Films → counts linked Events where `License Status` is empty. Ana can filter or color-code on this.

**Automation slot reclaimed.** Use it for:

### Automation 3 (revised): QC Failure Alert

**Trigger:** When `File Status` changes to `QC Failed` on any Films record.

**Action:** Send email to Garen with film title, QC Notes content, and link to the record.

**Why:** QC failures need immediate triage — the intern flags it, Garen decides whether to re-request the file from the filmmaker or fix it in post. Delay here eats into the delivery timeline.

---

### Automation 4: Delivery Confirmation Reminder

**Trigger:** When `Delivery Status` on an Events record has been `Delivered` for more than 5 days without changing to `Confirmed` or `Playback Tested`.

**Action:** Send email to Garen: "Venue [name] hasn't confirmed playback for [film]. Sent [date]."

**Why:** The worst festival-day failure is a venue that can't play the file. This catches the gap between "we sent it" and "they tested it" — the exact failure mode documented in the film pipeline reference.

---

### Automation 5: Weekly Pipeline Summary

**Trigger:** Every Monday at 8:00 AM.

**Action:** Send email to Ana with a summary:
- Films with `Outreach Status` still `Sent` or `No Response` (count)
- Films with `File Status` = `Received` or later (count)
- Events with `Delivery Status` = `Confirmed` (count of total)
- Any `QC Failed` films

**Why:** Ana needs a weekly pulse without opening Airtable. One email, four numbers, 30-second read. This is the push version of her dashboard — for weeks when she doesn't check the pull version.

---

## 4. Intake Form Field Mapping

Two forms feed data into Airtable: the **Film Intake Survey** (original, 9/12 submitted) and the **Film Supplemental Form** (follow-up for marketing/attendance fields).

### Film Intake Survey → Airtable

| Form Question | Target Table | Target Field | Status |
|---------------|-------------|-------------|--------|
| Film Title (dropdown) | Films | Film ID / Film Title | Mapped via `F26-XXX` prefix |
| Contact Name | Film Contacts | Contact Name | Mapped |
| Contact Email | Film Contacts | Email | Mapped |
| Contact Phone | Film Contacts | Phone | Mapped |
| Role | Film Contacts | Role | Mapped |
| Secondary Contact Name | Film Contacts | Secondary Contact Name | Mapped |
| Secondary Contact Email | Film Contacts | Secondary Email | Mapped |
| Formats Available | Film Contacts | Formats Available | Mapped |
| Caption Status | Film Contacts + Films | Caption Status | Mapped (exists in both tables) |
| Audio Description Available | Film Contacts + Films | Audio Description | Mapped |
| Spanish Version Available | Film Contacts + Films | Spanish Available | Mapped |
| Submission Timestamp | Film Contacts | Submission Timestamp | Mapped |
| *(licensing terms)* | Events | License fields | **GAP — form may ask but data isn't flowing to Events** |
| *(runtime)* | Films | Runtime (minutes) | **GAP — field doesn't exist yet on Films table** |

### Film Supplemental Form → Airtable

| Form Question | Target Table | Target Field | Status |
|---------------|-------------|-------------|--------|
| Film Title (dropdown) | — | Key for matching | Mapped via `F26-XXX` prefix |
| Your Name | — | Verification only | Not stored separately |
| Your Email | — | Verification only | Not stored separately |
| Post-screening conversation available? | Film Contacts | `Q&A Available` | **NEW FIELD — add per Section 1** |
| Attendee name/role | Film Contacts | `Q&A Contact Name` | **NEW FIELD** |
| Attendee email | Film Contacts | `Q&A Contact Email` | **NEW FIELD** |
| Preferred format (Q&A, panel, etc.) | Film Contacts | — | **GAP — no target field. Store in Notes or add `Q&A Format Preference` (Single Select)** |
| Social media handles | Films | `Social Handles` | **NEW FIELD** |
| Premiere status | Films | `Premiere Status` | **NEW FIELD** |
| Film updates since submission | Films | Notes | Append to existing Notes field |
| Has trailer? | Films | — | Implicit — if they provide a link, Trailer Link gets populated |
| Trailer/clip link | Films | Trailer Link | Existing field (currently 0/12 populated) |
| Post-festival availability | Films | — | **GAP — no target field. Low priority. Store in Notes.** |
| Purchase/platform link | Films | Film Website | Existing field (currently has placeholder "Film website" text) |
| Submission Timestamp | — | Metadata only | Not stored |

### Gaps Summary

| Gap | Severity | Recommendation |
|-----|----------|----------------|
| Q&A Format Preference has no field | Low | Add a Single Select on Film Contacts: `Brief Q&A`, `Moderated conversation`, `Panel`, `Open to any`. Or store in Notes. |
| Post-festival availability has no field | Low | Store in Notes. Not operationally needed before the festival. |
| Runtime not captured by either form | Medium | Add `Runtime (minutes)` to Films table. Populate manually from film websites or ask filmmakers directly during licensing conversations. |
| Licensing terms from intake form not flowing to Events | High | The intake form may capture licensing info but it's not synced to the Events table's licensing fields. After March 5 outreach responses come in, populate Events licensing fields from email replies — not the form. The form is a backup source. |
| 3 films missing from Film Contacts table | High | Create records for Beyond Zero, 40 Acres, CAM. Contact info exists in the merge sheet. |
| Film Website field has placeholder text ("Film website") not actual URLs | Medium | Populate from intake survey responses or filmmaker websites. The supplemental form's "purchase link" question will partially fill this. |

---

## Implementation Order

The 41-day countdown means we sequence by what unblocks the next person:

| Priority | Action | Unblocks | Time | Who |
|----------|--------|----------|------|-----|
| 1 | Add 3 missing Film Contacts records | Kim's follow-up queue covers all 12 films | 15 min | Garen |
| 2 | Add `Outreach Status` + `Outreach Sent Date` to Films, backfill from merge sheet | Ana's dashboard, Kim's queue | 30 min | Garen |
| 3 | Add `File Status` + `File Received Date` to Films | Garen's QC pipeline view | 15 min | Garen |
| 4 | Add `Delivery Status` to Events | Delivery tracking per venue | 10 min | Garen |
| 5 | Build the 4 views | Everyone can start using their pipeline view | 45 min | Garen |
| 6 | Set up Automation 1 (overdue outreach flag) | Kim's queue self-maintains | 15 min | Garen |
| 7 | Populate Events licensing fields from email responses | License tracking goes live | Ongoing | Josh/Ana |
| 8 | Add remaining fields (QC Assigned To, Social Handles, Premiere Status, etc.) | Intern QC assignments, promo pipeline | 30 min | Garen |
| 9 | Set up Automations 2-5 | Push notifications, weekly summary | 45 min | Garen |
| 10 | Sync supplemental form responses to new Airtable fields | Marketing/attendance data flows in | 30 min | Garen (script update) |

**Total estimated setup time: ~4 hours spread across priorities 1-9.**

Priority 10 (supplemental form sync) depends on when filmmakers actually submit the supplemental — not urgent until responses arrive.

---

## What This Does Not Cover

- **Venue packet assembly** — tracked by `oeff-file-tracker.py`, not this pipeline plan. The file tracker already handles the 12-component packet.
- **Eventbrite integration** — separate system, already built (`eventbrite-state.json`).
- **Host communications** — Kim's host pipeline is a different workflow.
- **Budget/invoicing** — OEFF's financial tracking is outside Airtable scope for now.
- **Historical film data (pre-2026)** — this plan is 2026 only. The media catalogue tools handle historical assets.
