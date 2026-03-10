# Host Helper Interface — Session Summary

**Date:** 2026-03-09
**Outcome:** Static page approach scratched. Garen building shared Airtable views instead.

---

## Research Findings

### Airtable Interface Designer — Capabilities & Limits

| Capability | Available? |
|---|---|
| Record detail pages with grouped sections | Yes |
| Text blocks, dividers, headers between fields | Yes |
| Hide empty fields automatically | No (requires Business plan) |
| Custom colors, fonts, branding | No — always looks like Airtable |
| Per-venue URLs on shared interface | **No** — shared link shows all records |
| Shared view URL filters | Yes, but viewer can remove them |
| Direct record URLs | Require Airtable login |
| Accordion/collapsible sections | No native support |

**Bottom line:** Airtable Interface Designer is a team tool, not a host-facing portal. Good for Ana, Josh, and Kim. Cannot deliver branded, per-venue host experience.

### Three Paths Identified

**Path A — miniExtensions per-record links (2-3 hours, free)**
- Airtable marketplace add-on that generates a unique public URL per record
- No login required for viewers. Select which fields are visible.
- Display is basic but functional. Fastest path to "hosts can see their data."

**Path B — Static site wired to Airtable API (half day, already built)**
- `generate-venue-sections.py --helpers` already existed and was deployed to Cloudflare
- Wire to Airtable API instead of CSV. Run one command when data changes.
- Full OEFF branding, temporal states, per-venue URLs.
- **This is what was built and then scratched this session.**

**Path C — Auto-rebuilding static site (1 day, permanent fix)**
- Same as Path B + Airtable webhook or cron that triggers Cloudflare rebuild
- Kim edits Airtable → pages auto-update. Zero pipeline friction.
- Best long-term solution if branded pages are needed.

---

## Airtable Team Dashboard — Recommended Views

Three views for the OEFF team (not host-facing):

1. **Ana/Kim: Festival Overview** — Dashboard page. Count widgets (venues confirmed, events published, films licensed). Venue list sorted by date with status indicators.
2. **Josh: Host Readiness** — Venue list with contact status, AV status, data gaps flagged.
3. **Event Detail** — Record detail page with all fields grouped into sections (Scheduling, Contacts, Venue Ops, Licensing/Internal).

---

## Information Design — What Hosts Should See

### Hierarchy by urgency and use frequency

**Tier 1 — "What am I screening?" (always visible, top)**
- Film title (large, prominent)
- Event date + day of week + time
- Venue name + address
- Eventbrite event URL
- Ticket price / free

**Tier 2 — "Day-of reference" (prominent, checked intensely during festival week)**
- Run of show: Doors → Program → Screening → Q&A → Close
- RSVP / ticket count
- OEFF onsite rep (name + cell)
- AV contact (name + cell)
- Primary host contact

**Tier 3 — "Planning reference" (below the fold, looked up once)**
- Venue capacity
- AV equipment status / notes
- WiFi
- ADA / accessible seating
- Space notes / wayfinding

**Tier 4 — "Resources" (links, shown only when populated)**
- Screening packet download (hidden until April)
- Host guide (hosts.oneearthfilmfest.org)
- Marketing toolkit
- Volunteer signup form

### Fields that NEVER appear in host view
- Host fee / invoice fields
- Licensing fields
- Internal team contact (OEFF Rep column)
- Film Survey Complete, Pipeline Status
- Notes field (internal)

---

## Airtable Field Names — Reference

### Events table
`Venue Name`, `Film Title`, `Date`, `Time`, `Ticket Price`, `Ticket URL`, `Pipeline Status`, `Pipeline Select`, `OEFF Rep`, `Volunteer Needs`, `Screening Packet URL`, `RSVP Count`, `Year`, `Archive Status`, `Venue` (linked), `Film` (linked)

### Venues table
`Venue Name`, `Region`, `Capacity`, `Contact Info` (multiline), `AV Contact`, `Notes`, `Venue ID`

### Host Intake table
`Venue Id`, `Contact Name`, `Contact Email`, `Venue Address`, `Has Projector`, `Has Sound`, `Has Screen`, `Has Computer`, `Has Wifi`, `Has Av Lead`, `Has Wheelchair`, `Cap 60Plus` (boolean — NOT the capacity number), `Space Notes`, `Promo Channels`, `Promo Notes`, `Motivation`

### Films table
`Film Title`, `Runtime_Min`, `Primary Topic`, `Caption Status`

---

## Venue Name Mismatches — Airtable vs Token Map

These venues have different names in Airtable Events vs the token-map.json (generated from an earlier snapshot):

| Airtable Events name | Token map key |
|---|---|
| Academy for Global Citizenship | Cultivate Collective (at Academy for Global Citizenship) |
| Chicago Climate Action Museum | *(no prior entry — new venue)* |
| Chicago Public Library Harold Washington Branch | *(no prior entry)* |
| Chicago Public Library Rogers Park Branch | *(no prior entry)* |
| IIT Bronzeville | *(no prior entry)* |
| Andersonville Chamber of Commerce | *(no prior entry)* |
| Calumet College of St. Joseph | *(no prior entry)* |

Also in token map but NOT in current Airtable events:
- Discover Card/Capital One
- Lizadro Museum (gem museum), Northbrook
- Loyola University Law School
- Northbrook Public Library
- Seven Generations Ahead (unscheduled)
- Illinois Clinicians for Climate Action (unscheduled)

---

## What Was Built (Can Be Reverted)

All changes in `generate-venue-sections.py`:

1. **`_load_host_intake_by_venue()`** — fetches Host Intake records, indexes by venue ID
2. **`assemble_venues_for_helpers()`** — enriched to pull intake data (ADA, WiFi, AV, address, capacity)
3. **`_match_venue_to_token()`** — 3-tier name matching (exact → alias → substring containment)
4. **New section renderers:** `render_helper_hero()`, `render_helper_ticket_count()`, `render_helper_run_of_show()`, `render_helper_contacts()`, `render_helper_venue_details()`, `render_helper_resources()`
5. **Updated `render_helper_page()`** — new section order matching information hierarchy
6. **Updated CSS** — hero card, contact grid, collapsible details, resource links, ticket count

Also:
- **`token-map.json`** — 6 new entries added (33 total)
- **25 generated pages** in `hosts/{token}/index.html`

---

## Key Files

- Airtable base: `app9DymWrbAQaHH0K`
- Generator script: `~/Desktop/OEFF Clean Data/generate-venue-sections.py`
- Token map: `~/Desktop/OEFF Clean Data/token-map.json`
- Venue slugs: `~/Desktop/OEFF Clean Data/venue-slugs.json`
- Host guide (live): `~/Desktop/OEFF Clean Data/hosts/index.html`
- Migration plan: `~/Desktop/OEFF Clean Data/host-helper-migration-plan.md`
- Audit results: `~/Desktop/OEFF Clean Data/audit-results-2026-03-09.md`
