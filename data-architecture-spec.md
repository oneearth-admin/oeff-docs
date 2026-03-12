# OEFF 2026 Data Architecture Spec

**For:** Kim (and team reference)
**Last updated:** 2026-03-11
**Author:** Garen

---

## What This Document Covers

How OEFF's data systems work, what lives where, what syncs, and what hosts see. This is the ground truth for anyone touching OEFF data.

---

## 1. What's Canonical

| Data | Lives In | Role | Who Edits |
|------|----------|------|-----------|
| Venues, events, films, contacts | **Airtable** | Source of truth for all structured data | Garen (schema), Kim + team (records) |
| Team planning, film assignments, timeline | **OEC Active Roadmap** (Google Sheet) | Planning layer — where the team coordinates | Ana, Josh, Kim, Garen |
| Filmmaker outreach tracking | **Filmmaker Merge Sheet** (Google Sheet) | Mailmeteor campaign source | Josh, Ana |
| Host outreach tracking | **Host Merge Sheet** (Google Sheet) | Mailmeteor campaign source | Kim, Garen |
| Eventbrite event IDs | **eventbrite-state.json** (local file) | Maps venues → ticket pages | Garen (script-managed) |
| V7 spreadsheet | **Retired** | Historical reference only — do not update | Nobody |

**The rule:** If it's about a venue, event, film, or contact — Airtable is the answer. If it's about who's doing what and when — the Roadmap sheet is the answer.

---

## 2. How Things Sync

```
Airtable (canonical)
  │
  ├──→ Google Sheets (merge sheets for Mailmeteor campaigns)
  │     └──→ Mailmeteor sends emails
  │     └──← Responses sync back to Airtable
  │
  ├──→ Shared Airtable Views (host-facing, read-only)
  │     24 per-venue views, public links, no login needed
  │
  ├──→ Host Guide website (hosts.oneearthfilmfest.org)
  │     Generated from Airtable data, deployed via Cloudflare
  │
  └──→ Eventbrite (ticket pages)
        Venue/event mapping in local state file
```

**Sync scripts** (all stdlib Python, run manually by Garen):
- `oeff-airtable-sync.py` — pushes Airtable → Sheets, pulls Sheets → Airtable
- `generate-venue-sections.py` — reads Airtable, renders venue sections in host guide HTML
- `build-host-data-layer.py` — creates display formulas in Airtable so venue records show host-ready data

**What's NOT automated:** Sync is manual (Garen runs scripts). There's no live auto-sync between Airtable and Sheets. Changes in one system don't appear in the other until a sync is run.

---

## 3. What Hosts See Today

### Host Guide (public website)
**URL:** hosts.oneearthfilmfest.org
**What it is:** Onboarding guide for new + returning hosts. Action cards, webinar recordings, timeline, FAQ.
**Updated:** By Garen via git push (auto-deploys to Cloudflare).

### Per-Venue Shared Views (Airtable)
**What they are:** 24 read-only Airtable grid views, one per venue. Each shows only that venue's screenings.
**Access:** Public link, no login required.
**What's visible (10 fields):**

| Field | Example |
|-------|---------|
| Event ID | E26-001 |
| Venue Name | Chicago Cultural Center |
| Date | April 22, 2026 |
| Time | 6:00 PM |
| Ticket Price | Free |
| Film Title | The Last Ranger |
| Ticket URL | eventbrite.com/... |
| OEFF Rep | Kim |
| Volunteer Needs | 2 greeters |
| Screening Packet URL | drive.google.com/... |

**What's hidden (40+ fields):** All internal data — licensing fees, pipeline status, contact info, financial data, edit history.

### What's Wrong With the Current Views

1. **One long row** — all data is flat. No grouping, no visual hierarchy.
2. **Venue ID is the first column** — it's the primary key so Airtable forces it first, but hosts don't need to see it.
3. **No sensitive data separation** — licensing info is hidden, but there's no clear boundary between "host data" and "internal data."
4. **No QA layer** — if data is wrong, hosts see wrong data immediately.

---

## 4. What We're Building Next

### Information Redesign (Kim + Garen collaboration)

**Goal:** Host views should be grouped and scannable, not one long row.

**Approach options:**
- **Option A: Airtable Interface Designer** — custom layouts within Airtable (grouped fields, sections, conditional visibility). No code. Kim can help design.
- **Option B: Embedded Airtable views in static site** — one `<iframe>` embed per venue on our hosted pages. Auto-updates from Airtable. Very light code lift.
- **Option C: Custom HTML pages** — most control, most maintenance. (Likely overkill.)

**Current leaning:** Option A for the views themselves, possibly Option B for the wrapper.

### Backend / Frontend Split

**Concept:** Two layers of the same data.

| Layer | Who sees it | What's there |
|-------|-------------|--------------|
| **Backend (editing view)** | Kim, Garen, interns | Full data, in-progress edits, QA status columns |
| **Frontend (verified view)** | Hosts | Only confirmed, QA'd data. Clean layout. |

**QA/QC process:**
1. Data enters Airtable (from intake forms, manual entry, scripts)
2. Intern validates (checks accuracy, finds headshots, confirms contacts)
3. Intern marks field as "Verified" (checkbox or status field)
4. Verified data becomes visible in host-facing view (via Airtable filter: `Verified = true`)

This means hosts only ever see confirmed information.

### Sensitive Data — Licensing & Fees

**Current state:** Hidden in shared views (40+ fields suppressed). Not exposed anywhere.

**Proposed approach:** Licensing fees and filmmaker financial terms should NOT live in any shared or host-facing view. Options:
1. **Email-only** — send licensing details to only the people who need them (Ana, Josh, the filmmaker). No persistent shared table.
2. **Restricted Airtable view** — a view filtered to licensing fields, shared only with Ana/Josh via private link.

**Open question for Ana:** Does licensing info need to live in a persistent shared location, or is email sufficient?

---

## 5. Intern Scope

### What interns would do:
- **Column validation** — given specific fields in a spreadsheet, verify data is correct and current
- **Headshot sourcing** — find headshots for filmmakers, facilitators, program partners online
- **Contact gathering** — facilitator contacts, program partner contacts → specific Airtable fields
- **Slide deck validation** — after a script populates Google Slides from data, interns check content
- **QA marking** — after validating a field, mark it as verified in Airtable

### What interns would NOT do:
- Schema changes or field creation
- Sync script operation
- Direct host communication
- Financial/licensing data access

### Tool access:
- Specific Airtable views (filtered to their task columns)
- Google Sheets (read + edit on assigned columns only)
- NOT full Airtable base editor access

---

## 6. Slide Deck Pipeline

**Historical reference:** Kim needs past event slide decks (Garen to send).

**Automated pipeline (planned):**
1. Garen writes a script that pulls from Airtable → populates Google Slides template
2. Script fills: film title, synopsis, director, runtime, venue info, sponsor logos
3. Interns validate: check headshots, bios, spelling, formatting
4. Kim reviews final deck before event

**What the script handles:** Data population (the boring part).
**What humans handle:** Visual judgment, headshot quality, bio accuracy.

---

## 7. Airtable Table Overview

For Kim's reference — the tables that matter most:

| Table | Records | What's in it |
|-------|---------|-------------|
| **Venues** | ~24 active | Location info, contacts, equipment, linked events |
| **Events** | ~30 for 2026 | Screenings: date, time, film, tickets, OEFF rep |
| **Films** | ~16 for 2026 | Film metadata: title, director, runtime, genre |
| **Film Contacts** | ~12 | Filmmaker contact info for licensing |
| **Host Contacts** | ~24 | Venue contact people |
| **Host Intake** | ~20 | Form responses: AV, WiFi, accessibility, space notes |
| **Deliverables** | ~40 | Task tracking with due dates and owners |
| **Milestones** | ~15 | Project timeline checkpoints |

Tables like Sponsors, Partners, Participants, Recordings are reference/historical — not actively edited for 2026 planning.

---

## 8. Open Questions

1. **For Ana:** Licensing info — email-only or persistent restricted view?
2. **For Kim + Garen:** Interface Designer vs embedded views — try both, see what feels right?
3. **For team:** Intern start date and availability — affects QA layer timeline
4. **Airtable plan level:** Interface Designer features vary by plan. Need to check what's available on current plan.
5. **Venue ID column:** Can we create a "Display Name" as the primary field and move the ID to a secondary column?

---

## Glossary

| Term | Meaning |
|------|---------|
| **Canonical** | The authoritative source — if two systems disagree, this one wins |
| **Merge sheet** | A Google Sheet formatted for Mailmeteor mail merge campaigns |
| **Shared view** | A read-only Airtable grid accessible via public URL (no login) |
| **Sync script** | A Python script that copies data between Airtable and Google Sheets |
| **Display formula** | An Airtable formula field that formats data for host readability |
| **QA/QC** | Quality check — verifying data is correct before hosts see it |
| **Primary field** | Airtable's first column — always visible, can't be hidden or reordered |
