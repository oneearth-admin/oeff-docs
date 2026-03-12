# OEFF Airtable Data Layer — Technical Spec

**Author:** Garen
**Last updated:** 2026-03-12
**Status:** Implemented and verified


## What This Is

A complete reference for the data layer that sits between raw Airtable records and the host-facing views. It covers every script, field, link, and formula involved in making venue data presentable and season-filtered for OEFF 2026 hosts.


## 1. Architecture Overview

```
Airtable Base (app9DymWrbAQaHH0K)
│
├── Events table (tblau3F9sXWnNhDN5)
│   ├── Raw fields: Film Title, Date, Time, Doors Open, Ticket Price, Ticket URL, OEFF Rep, Season
│   ├── Host Summary Line (formula): "{Film Title} — {Date} at {Time}"
│   └── Venue (link → Venues, multi-record)
│
├── Venues table (tblAQVT8F4jRxbRzs)
│   ├── Raw fields: Venue Name, Address, Capacity, Region, etc.
│   ├── Events (link → Events, multi-record, ALL years)
│   ├── 2026 Events (link → Events, multi-record, 2026 ONLY)  ← NEW
│   ├── Host Contacts (link → Host Contacts)
│   ├── Host Intake (link → Host Intake)
│   ├── LKP rollup fields (8) — pull from "2026 Events" link
│   ├── LKP contact/intake rollups (7) — pull from Host Contacts / Host Intake links
│   └── Host - display formula fields (13) — format LKP values for hosts
│
├── Host Contacts table
│   └── Contact Name, Email, Phone
│
├── Host Intake table
│   └── Venue Address, Has Wifi, Space Notes, Has Wheelchair
│
└── 24 per-venue shared views (on Events table)
    └── Public URLs, read-only, one per venue
```


## 2. The Three Layers

### Layer 1: Link Fields (the wiring)

| Field | Table | Type | Target | Purpose |
|-------|-------|------|--------|---------|
| Events | Venues | multipleRecordLinks | Events | ALL events, all years — historical reference |
| **2026 Events** | Venues | multipleRecordLinks | Events | **Only Season=2026 events** — host-facing data source |
| Host Contacts | Venues | multipleRecordLinks | Host Contacts | Venue contact people |
| Host Intake | Venues | multipleRecordLinks | Host Intake | Form responses (AV, WiFi, accessibility) |
| Venue | Events | multipleRecordLinks | Venues | Reverse link (which venue hosts this event) |

**"2026 Events" link field** (ID: `fldjkmi6lxLsZGgZm`):
- Created via REST API by `fix-season-rollups.py`
- Populated programmatically: queries Events where `{Season}="2026"`, builds venue→event mapping, PATCHes each venue record
- Contains 28 event records across 27 venues (Columbia has 2 screenings)
- **Must be re-populated each year** when events are added or season changes

### Layer 2: LKP Rollup Fields (the data pull)

Rollup fields aggregate values from linked records. Each one specifies: (1) which link to follow, (2) which field to grab, (3) how to combine values.

**Event rollups (season-filtered via "2026 Events" link):**

| Rollup Field | Field ID | Follows Link | Grabs Field | Aggregation |
|-------------|----------|-------------|-------------|-------------|
| LKP Film Title | `fldHlJP4W7v9QU01Z` | 2026 Events | Film Title | ARRAYJOIN |
| LKP Event Date | `fldOkqChh3XGnhSst` | 2026 Events | Date | MAX |
| LKP Event Time | `fldhgKF9eBYM6bE78` | 2026 Events | Time | ARRAYJOIN |
| LKP Doors Open | `fldT6h4lwqWIRKYsD` | 2026 Events | Doors Open | ARRAYJOIN |
| LKP Ticket Price | `fldCGDO0VE73xQqHy` | 2026 Events | Ticket Price | ARRAYJOIN |
| LKP Ticket URL | `fld2SlWrRNuyOYhBC` | 2026 Events | Ticket URL | ARRAYJOIN |
| LKP OEFF Rep | `fld8FCnuQ2QkSczh9` | 2026 Events | OEFF Rep | ARRAYJOIN |
| All Screenings | `fldTc57O3VncAbAJu` | 2026 Events | Host Summary Line | ARRAYJOIN(\\n) |

**Contact/intake rollups (not season-filtered — no need):**

| Rollup Field | Follows Link | Grabs Field |
|-------------|-------------|-------------|
| LKP Host Name | Host Contacts | Contact Name |
| LKP Host Email | Host Contacts | Email |
| LKP Host Phone | Host Contacts | Phone |
| LKP Intake Address | Host Intake | Venue Address |
| LKP Intake WiFi | Host Intake | Has Wifi |
| LKP Intake Space Notes | Host Intake | Space Notes |
| LKP Intake Wheelchair | Host Intake | Has Wheelchair |

### Layer 3: Host - Display Formula Fields (the presentation)

Formula fields that wrap LKP values with friendly fallbacks. These are what hosts see.

| Display Field | Formula Logic |
|--------------|---------------|
| Host - Film | LKP Film Title, or "Film to be confirmed" |
| Host - Screening Date | LKP Event Date formatted as "Friday, April 24, 2026", or "Date to be confirmed" |
| Host - Start Time | LKP Event Time, or "Start time to be confirmed" |
| Host - Doors Open | LKP Doors Open, or "Doors-open time to be confirmed" |
| Host - Ticket Info | LKP Ticket URL, or "Ticket link coming soon" |
| Host - Contact Name | LKP Host Name, or "Host contact to be confirmed" |
| Host - Contact Phone | LKP Host Phone, or "Phone to be confirmed" |
| Host - Contact Email | LKP Host Email, or "Email to be confirmed" |
| Host - Venue Address | Address field (preferred) → LKP Intake Address (fallback) → "Address to be confirmed" |
| Host - Parking | Parking Info, or "Parking details available on request" |
| Host - Transit | Transit Info, or "Transit details available on request" |
| Host - WiFi | WiFi Info, or "WiFi details shared day-of" |
| Host - AV Notes | LKP Intake Space Notes (no fallback — blank if empty) |


## 3. Season Filtering — How It Works

**Problem:** Venues link to events across all years via the "Events" field. Rollup fields that aggregate from "Events" show mixed-year data (e.g., Climate Action Evanston showed 4 films from 2024-2026 instead of just 1 from 2026).

**Solution:** A parallel link field ("2026 Events") that only connects venues to their Season=2026 events. All 8 event-sourced rollups were retargeted to use this filtered link instead of the unfiltered "Events" link.

**Why not filter within the rollup?** Airtable rollups have no filter clause. You can't say "ARRAYJOIN values WHERE Season=2026." The only way to filter is at the link level — by controlling which records are linked.

**Why not use formula fields on Events?** Tried. Airtable blocks formula field creation via both the REST API and Scripting Extension. "Creating or updating options for formula fields is not supported at this time."

**Why not create new rollup fields?** Tried. Airtable also blocks rollup field creation via REST API and Scripting Extension. Rollups can only be created in the Airtable UI.

**Why not PATCH existing rollups via API?** Tried. Changing `recordLinkFieldId` on an existing rollup returns 422 across all body formats.

**What worked:** Create the "2026 Events" link field via API (link fields ARE supported), populate it via API, then manually retarget each rollup in the Airtable UI (Edit field → change link dropdown → Save). 8 manual edits.


## 4. Scripts

### `ops/airtable_api.py` — Shared API Layer

Stdlib Python 3. Used by all Airtable scripts.

| Export | Purpose |
|--------|---------|
| `BASE_ID` | `app9DymWrbAQaHH0K` |
| `API` | `https://api.airtable.com/v0` |
| `get_token()` | Reads `AIRTABLE_TOKEN` from environment |
| `api_call(method, endpoint, token, body)` | Retry + rate-limit aware API call. Prepends `/v0` to endpoint. |
| `fetch_all_records(table, view, token)` | Paginated fetch by view |
| `fetch_by_filter(table, formula, token)` | Paginated fetch by filterByFormula |

**Important:** `api_call` prepends `/v0`, so endpoints should start with `/meta/bases/...` or `/{BASE_ID}/...`, not `/v0/...`.

### `build-host-data-layer.py` — Field Creator

Creates the full data layer on Venues: 14 rollup + 13 display formula + 1 Events formula + 1 All Screenings rollup = 29 fields total. Safe to re-run (checks for existing fields by name).

**Note:** This script was written before the Airtable API restrictions were fully understood. Rollup creation via API actually fails — the existing rollup fields were created when the API briefly supported it or were created manually. The script's `create_rollup_field()` function no longer works for new rollup creation.

### `fix-season-rollups.py` — Season Filter Applier

Three-phase script:
1. **Phase 1:** Creates "2026 Events" link field on Venues → Events (via REST API) ✅
2. **Phase 2:** Populates the link with only Season=2026 event records ✅
3. **Phase 3:** Retargets LKP rollups to use new link (via API PATCH) ❌ — blocked by API limitation

Phase 3 was completed manually in the Airtable UI.

**Re-run safety:** Phase 1 skips if field exists. Phase 2 skips venues already correctly linked. Phase 3 skips rollups already pointing at "2026 Events."

### `airtable-season-filter-script.js` — Failed Approach (Scripting Extension)

Attempted to create 8 formula fields on Events with `IF({Season}="2026", value, "")` wrappers. Failed: "Creating or updating options for formula fields is not supported at this time."

### `airtable-create-2026-rollups.js` — Failed Approach (Scripting Extension)

Attempted to create 8 rollup fields via `createFieldAsync("rollup", ...)`. Failed: "Creating or updating options for rollup fields is not supported at this time."

### `generate-venue-sections.py` — Host Guide Generator

Reads Airtable data, renders venue sections for the host guide website (hosts.oneearthfilmfest.org).

### `generate-token-map.py` — Venue Token Generator

Creates per-venue access tokens for shared views. Outputs `token-map.json`.

### `airtable-create-views.js` — Shared View Creator (Scripting Extension)

Creates 24 per-venue shared views on the Events table. Outputs to `shared-view-links.json`.


## 5. Airtable API Limitations (Hard-Won Knowledge)

| Operation | REST API | Scripting Extension | UI Only |
|-----------|----------|-------------------|---------|
| Create link field | ✅ | ✅ | ✅ |
| Create text/number/select field | ✅ | ✅ | ✅ |
| Create formula field | ❌ | ❌ | ✅ |
| Create rollup field | ❌ | ❌ | ✅ |
| Create lookup field | ❌ | ❌ | ✅ |
| Create count field | ❌ | ❌ | ✅ |
| PATCH rollup link source | ❌ | N/A | ✅ |
| PATCH formula expression | ❌ | ❌ | ✅ |
| Populate link field values | ✅ | ✅ | ✅ |
| Read schema/metadata | ✅ | ✅ (partial) | ✅ |
| Delete table | ❌ | ❌ | ✅ |

**Bottom line:** Anything involving formulas, rollups, or lookups requires manual UI work. The API is useful for link fields, record CRUD, and schema discovery.


## 6. Per-Venue Shared Views

24 public-link shared views on the Events table, one per venue. Created by `airtable-create-views.js`. Links stored in `shared-view-links.json`.

**Current limitation:** Views are on the Events table, so the primary field (Event ID like "E26-003") is the first column. Hosts see a technical ID as column 1. This was flagged in the Kim 1:1 — Interface Designer pages would solve this by allowing custom field ordering.

**Visible fields (10):** Event ID, Venue Name, Date, Time, Ticket Price, Film Title, Ticket URL, OEFF Rep, Volunteer Needs, Screening Packet URL.

**Hidden fields (40+):** All internal data — licensing, pipeline status, contacts, financial.


## 7. Yearly Maintenance

When rolling over to a new season:

1. **Create new link field** (or repopulate existing): Run `fix-season-rollups.py` with updated `LINK_FIELD_NAME` and season filter, OR repopulate "2026 Events" with new season's records
2. **Verify rollups still point at correct link** — the link field swap only needs to happen once per link field name
3. **Update shared views** if new venues are added
4. **Repopulate token map** if venue roster changes

**The "2026 Events" naming is intentional.** When 2027 rolls around, create a "2027 Events" link field and retarget the rollups again. The old "2026 Events" link stays as historical reference.


## 8. Key IDs Reference

| Entity | ID |
|--------|-----|
| Base | `app9DymWrbAQaHH0K` |
| Venues table | `tblAQVT8F4jRxbRzs` |
| Events table | `tblau3F9sXWnNhDN5` |
| "Events" link (all years) | `fldiOS3tgPvjLThQj` |
| "2026 Events" link (filtered) | `fldjkmi6lxLsZGgZm` |
| Host Contacts link | `fldAdrWdhVcHMtDln` |
| Host Intake link | `fldj3BAeQk5jkFIOe` |


## 9. Data Flow Diagram

```
Events table                    Venues table                   Host sees
─────────────                   ────────────                   ─────────
Film Title ──────────┐
Date ────────────────┤
Time ────────────────┤
Doors Open ──────────┤     "2026 Events" link
Ticket Price ────────┼──── (Season=2026 only) ───→ LKP rollups ───→ "Host -" formulas ───→ Shared view
Ticket URL ──────────┤                              (aggregate)      (format + fallback)    or Interface
OEFF Rep ────────────┤
Host Summary Line ───┘

Host Contacts table
───────────────────
Contact Name ────────┐
Email ───────────────┼──── Host Contacts link ───→ LKP rollups ───→ "Host -" formulas
Phone ───────────────┘     (no season filter)

Host Intake table
─────────────────
Venue Address ───────┐
Has Wifi ────────────┼──── Host Intake link ────→ LKP rollups ───→ "Host -" formulas
Space Notes ─────────┤     (no season filter)
Has Wheelchair ──────┘
```


## 10. Open Items

1. **Interface Designer pages** — next step for grouped, scannable host views (Kim + Garen collaboration)
2. **Primary field swap** — Event ID as first column in shared views; Interface Designer would solve this
3. **Licensing data isolation** — needs Ana input on email-only vs restricted view
4. **16 empty table shells** in Airtable — API can't delete tables, must use UI
5. **Formula field updates** — if any "Host -" display formulas need changing, it's manual UI work only
