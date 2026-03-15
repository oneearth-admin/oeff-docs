# OEFF 2026 Data Architecture Spec — v2

**For:** Kim, Ana, Garen
**Last updated:** 2026-03-13
**Author:** Garen
**Supersedes:** `data-architecture-spec.md` (v1, March 11)
**Decision source:** Kim/Garen March 13 meeting — see `kim-garen-03-13-meeting-summary.md`

---

## What Changed

v1 was venue-centric: venues were the organizing principle, and screenings were attributes of venues. The March 13 conversation with Kim surfaced a cleaner model: **events as the relational key**, with master tables feeding into event records. This changes how Host Helper works, how data flows, and how Kim interacts with the system.

The core insight (Kim's): "The most specific our data will ever get is by event."

---

## 1. Data Hierarchy

```
Master Tables (persistent, year-over-year)
├── Directory         All people — one record per person, typed by role + priority
├── Venues            Physical spaces — capacity, ADA, AV, address
├── Films             Titles, runtimes, licensing terms
└── Members           14k email list (separate from active partners)

Relational Layer (season-specific)
└── Events            Links a venue + film + contacts + date/time
    ├── Screenings    Film screenings (the primary event type)
    ├── Action Fairs  Community events
    └── Panels, concerts, etc.

Assembled Layer (script-generated, editable by Kim)
└── Per-Event Tables  Flat tables with ~18 text/date/URL fields
    └── One table per event → one Interface Designer page per event
```

### How this differs from v1

| Aspect | v1 (venue-centric) | v2 (event-centric) |
|--------|-------------------|-------------------|
| Organizing principle | Venues | Events |
| Host Helper shows | Per-venue shared views | Per-event Interface Designer pages |
| Data chain | 3-layer rollup (link → LKP → Host formula) | Flat text fields, script-assembled |
| Kim's edit model | Can't edit rollups/formulas | Edits flat fields directly |
| Multi-event venues | Concatenated values with commas | One table per event — no ambiguity |
| Contact model | Separate Host Contacts + Film Contacts tables | Unified Directory with role + priority |
| Debuggability | Requires tracing link → rollup → formula | What you see is what's stored |

---

## 2. Master Tables

### Directory (NEW — replaces Host Contacts + Film Contacts)

One record per person. All stakeholders in one table.

| Field | Type | Purpose |
|-------|------|---------|
| Name | Text (primary) | Full name |
| Email | Email | Primary email |
| Phone | Phone | Primary phone |
| Organization | Text | Host org, film company, etc. |
| Role | Single Select | `Host`, `Venue Contact`, `Filmmaker`, `Distributor`, `Panelist`, `Volunteer Lead`, `AV Tech`, `Partner Org` |
| Priority | Single Select | `Primary`, `Secondary`, `Marketing`, `AV/Tech` |
| Relationship Type | Single Select | `Collaborator` (mission-oriented), `Transactional` (business), `Internal` (team) |
| Notes | Long Text | Context, history |
| Linked Events | Link → Events | Which events this person is associated with |
| Linked Venues | Link → Venues | Which venues (persistent across years) |
| Linked Films | Link → Films | Which films (for filmmakers/distributors) |

**Why unified:** Kim's current Google Sheet already puts all contacts in one place with a "contact type" field. Separate tables created friction — the same person might be a host contact AND a panelist. A unified directory with typed roles handles this cleanly.

**What this replaces:** Host Contacts table (24 records) + Film Contacts table (12 records) → ~36 records in Directory. Some deduplication likely — a venue's primary contact might also be a panelist.

### Venues (STAYS — minor field additions)

No structural changes. Venues remain persistent, year-over-year entities.

| New Field | Type | Purpose |
|-----------|------|---------|
| Classification | Single Select | `Flagship`, `Community` |
| Technical Tier | Single Select | `T1`, `T2`, `T3`, `T4` |
| Linked Directory | Link → Directory | Replaces Host Contacts link |

**Removing:** The `Host Contacts` and `Host Intake` link fields become obsolete once Directory is in place. Keep them through festival for safety, hide from views.

### Films (STAYS — fields from filmmaker pipeline plan)

No structural changes beyond what `filmmaker-pipeline-airtable-plan.md` already specifies. Key additions from that plan:

- `Outreach Status`, `File Status`, `Delivery Status` (Single Selects)
- `Runtime (minutes)` (Number — currently missing, blocks run-of-show)
- `Social Handles`, `Premiere Status` (from supplemental form)

### Members (NEW — conceptual, deferred)

The 14k email list is conceptually distinct from active partners. This table is **not needed for 2026 festival operations** — the Mailchimp/Mailmeteor list serves this purpose. Document the distinction now, build the table when there's a concrete use case.

### Events (STAYS — becomes the relational key)

The Events table already exists with ~31 records for 2026. Its role changes from "attribute of venues" to "the most specific data level that links everything together."

| Existing Field | Status |
|----------------|--------|
| Event ID | Keep — primary key |
| Venue (link → Venues) | Keep |
| Film Title | Keep |
| Date, Time, Doors Open | Keep |
| Ticket Price, Ticket URL | Keep |
| OEFF Rep | Keep |
| Season | Keep — enables year filtering |
| Licensing fields (6) | Keep — per-event, not per-film |
| Delivery Status | Add per filmmaker pipeline plan |

| New Field | Type | Purpose |
|-----------|------|---------|
| Event Type | Single Select | `Screening`, `Action Fair`, `Panel`, `Concert`, `Workshop` |
| Primary Contact | Link → Directory | Who to call day-of |
| AV Contact | Link → Directory | Technical contact |
| Marketing Contact | Link → Directory | Promo contact |

---

## 3. Per-Event Flat Tables (the Host Helper mechanism)

### The problem with the current approach

The current Host Helper uses a 3-layer rollup chain on the Venues table:

```
Events ──→ "2026 Events" link ──→ LKP rollups ──→ "Host -" display formulas
```

This breaks on multi-event venues (Columbia shows comma-concatenated values), generates confusing placeholder text, and is completely opaque — during the March 13 call, even Garen couldn't trace where Interface Designer was pulling data from.

### The solution: script-assembled flat tables

A Python script (`assemble-event-tables.py`) reads from master tables and writes assembled, flat data to per-event tables. Each table has ~20 simple fields — no formulas, no rollups, no link fields. Kim can edit any field directly.

```
Master Tables                    assemble-event-tables.py           Per-Event Tables
─────────────                    ───────────────────────            ────────────────
Events ──────────┐                                                 ┌─ E26-001 Table
Venues ──────────┼──→ Read, join, format, write ──→               ├─ E26-002 Table
Films ───────────┤                                                 ├─ E26-003 Table
Directory ───────┘                                                 └─ ... (22 tables)
                                                                        │
                                                                        ↓
                                                                   Interface Designer
                                                                   (one page per table)
```

### Per-event table schema (~22 fields)

| Field | Type | Source |
|-------|------|--------|
| Event Name | Text | Events.Film Title + " at " + Venues.Venue Name |
| Film Title | Text | Films via Events |
| Film Runtime | Text | Films.Runtime |
| Filmmaker Name | Text | Directory (Role=Filmmaker, linked to Film) |
| Filmmaker Email | Email | Directory |
| Screening Date | Date | Events.Date |
| Start Time | Text | Events.Time (normalized by script) |
| Doors Open | Text | Events.Doors Open |
| Venue Name | Text | Venues.Venue Name |
| Venue Address | Text | Venues.Address (full, validated) |
| Venue Capacity | Number | Venues.Capacity |
| Parking | Long Text | Venues or Host Intake |
| Transit | Long Text | Venues or Host Intake |
| WiFi | Text | Venues or Host Intake |
| AV Notes | Long Text | Venues or Host Intake — equipment-specific only |
| Contact Name | Text | Directory (Role=Host, Priority=Primary) |
| Contact Email | Email | Directory |
| Contact Phone | Phone | Directory |
| Contact Role | Text | Directory.Role |
| Ticket URL | URL | Events.Ticket URL |
| Ticket Price | Text | Events.Ticket Price |
| OEFF Rep | Text | Events.OEFF Rep |
| Volunteer Needs | Long Text | Events or manual |
| Screening Packet URL | URL | Populated when ready (April) |
| Webinar Recording | URL | Universal — same for all events |
| Host Guide Link | URL | Universal — hosts.oneearthfilmfest.org |

### What the script does

```
assemble-event-tables.py [--dry-run] [--event E26-003] [--refresh]

1. Read all Events where Season = "2026"
2. For each event:
   a. Fetch linked Venue record
   b. Fetch linked Film record
   c. Fetch Directory contacts (by venue + role)
   d. Fetch Host Intake data (if exists)
   e. Normalize times (6:30P → 6:30 PM)
   f. Validate addresses (city/state/ZIP)
   g. CREATE table if it doesn't exist (POST /meta/bases/{baseId}/tables)
   h. UPSERT assembled record (PATCH if exists, POST if new)
3. Output: table IDs + Interface Designer page URLs
```

**Re-run behavior:** The script checks for existing per-event tables by name (e.g., "E26-003 — Uncommon Ground"). If found, it updates the record. Kim's manual edits to fields the script doesn't write (e.g., Volunteer Needs) are preserved. Fields the script owns (Film Title, Screening Date, etc.) are overwritten from master tables.

**Field ownership convention:**
- **Script-owned fields** (overwritten on re-run): Film Title, Screening Date, Start Time, Venue Name, Venue Address, Contact Name/Email/Phone, Ticket URL, Filmmaker Name/Email
- **Kim-editable fields** (preserved on re-run): Volunteer Needs, AV Notes, Screening Packet URL, any manual additions

### Why NOT per-event shared views

Shared views are locked to the master grid's column layout. You can't reorder columns, add sections, or create a scannable layout. Interface Designer pages on flat tables solve all of these problems.

### Why NOT per-event tables with rollups

The Airtable API cannot create formula, rollup, or lookup fields. Per-event tables with rollups would require manual UI work for every event × every rollup field — approximately 22 events × 15 rollups = 330 manual field configurations. Flat tables with script-assembled data eliminate this entirely.

---

## 4. Kim's Google Sheets Model → Airtable Mapping

Kim has built a clean relational model in Google Sheets with dropdown validation. Here's how it maps:

| Kim's Sheet Concept | Airtable Equivalent |
|---------------------|---------------------|
| Contacts tab (master list) | Directory table |
| Venues tab (physical spaces) | Venues table |
| Films tab (titles + metadata) | Films table |
| Hosts tab (links contacts + venues + films) | Events table (relational key) |
| Dropdown validation ("can only select existing values") | Linked Record fields (select from existing records) |
| Contact Type (primary/secondary) | Directory.Priority field (Single Select) |
| Screenings tab (event-level detail) | Events table |

**Key mapping insight:** Kim's dropdown validation model — "you can't add anything new to screenings, it's all dropdown values" — maps exactly to Airtable's linked record fields. When Events links to Venues, you can only select an existing venue. This preserves the data integrity Kim's model enforces.

---

## 5. Terminology

### Recommendation: keep both "event" and "screening"

The terminology audit (93 occurrences of "screening" across 17 scripts, 353 of "event" across 14 scripts) shows both terms are embedded in:

- Airtable field names: `Screening Date`, `Screening Time`, `Screening Packet Sent`
- Python variable names: `screening_date`, `screening_count`, `screening_list`
- Deliverable types: `Screening Packet` (Single Select in Deliverables table)
- Asset classification: `screening_copy` type in media catalogue
- Google Sheets columns: merge sheet headers reference both terms

**Rename risk:** HIGH. Renaming "screening" to "event" would require updating Airtable field metadata, 17 Python scripts, Google Sheet headers, and deliverable type options. The semantic distinction is also valuable:

| Term | Meaning | Used for |
|------|---------|----------|
| **Event** | A scheduled occurrence (venue + film + date) | Data architecture, Airtable records, Eventbrite |
| **Screening** | The act of showing a film + associated deliverables | Operational workflows, host communications, file pipeline |

**Decision:** Use "events" as the umbrella term in data architecture. Keep "screening" for operational language (screening packet, screening copy, screening date). Don't rename existing fields — the cost exceeds the benefit with 40 days to festival.

---

## 6. Filmmaker Placement

### Recommendation: Directory table, with Contact Type = "Filmmaker" or "Distributor"

**Arguments for unified Directory:**
- Kim's model already puts all contacts in one table with a type field
- Filmmakers sometimes attend events (filmmaker toast), making them event participants
- A single directory enables cross-role queries ("show me everyone associated with this event")
- Reduces table count (Director + Film Contacts merge into one)

**Arguments for separate Film Contacts table:**
- Film Contacts has film-specific fields (Formats Available, Caption Status, Q&A Available)
- Filmmaker pipeline plan already specifies additions to Film Contacts
- Mixing 14k member records with 36 contact records could be unwieldy

**Recommendation:** Move filmmaker contacts into Directory but keep film-specific operational fields (Formats Available, Caption Status, Licensing Rate Quoted, Q&A fields) on the Films table directly. The Directory stores *who they are*; the Films table stores *what they've provided/agreed to*.

This means:
- Directory gets ~12 filmmaker records (Name, Email, Phone, Organization, Role=Filmmaker)
- Films table keeps its operational fields (Caption Status, Formats Available, etc.)
- Events table links to Directory for contacts, to Films for film metadata
- No separate Film Contacts table needed

**Migration:** Move Film Contacts records to Directory, add Role=Filmmaker. Move film-specific fields to Films table. Delete Film Contacts table after verification.

---

## 7. Contact Type Field Design

Kim currently uses "Contact Type" for primary/secondary distinction. The March 13 conversation identified that we need two separate dimensions:

| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| **Role** | Single Select | Host, Venue Contact, Filmmaker, Distributor, Panelist, Volunteer Lead, AV Tech, Partner Org, Board Member | *What this person does* |
| **Priority** | Single Select | Primary, Secondary, Marketing, AV/Tech, Billing | *How important they are for communications* |

**Why two fields:** A venue's AV tech contact is "AV Tech" by role but "Secondary" by priority. The primary host contact is "Host" by role and "Primary" by priority. A marketing contact at a partner org is "Partner Org" by role and "Marketing" by priority. One field can't capture both dimensions.

**Kim's existing "Contact Type" field** maps to Priority. The new Role field adds the dimension she was implicitly using organization names for.

---

## 8. Migration Path

### What to do now (March 13–20, before Host Helper rollout)

| Step | Action | Risk | Effort |
|------|--------|------|--------|
| 1 | Create Directory table with schema above | None — new table, no existing data affected | 30 min |
| 2 | Import Kim's cleaned tracker sheet contacts into Directory | Low — Kim validates before import | 1 hour |
| 3 | Import Host Contacts + Film Contacts into Directory (dedup) | Low — keep originals until verified | 1 hour |
| 4 | Build `assemble-event-tables.py` | None — new script | 2-3 hours |
| 5 | Run script to create per-event tables (dry-run first) | Low — creates new tables only | 30 min |
| 6 | Create Interface Designer pages per event | Medium — some manual UI work | 1-2 hours |
| 7 | Test with Kim — verify she can edit flat fields | None | 30 min |
| 8 | Generate per-event deep links for Mailmeteor merge sheet | Low | 30 min |

### What to defer until after festival

| Action | Why defer |
|--------|----------|
| Delete Host Contacts + Film Contacts tables | Keep as backup through festival |
| Delete 24 per-venue shared views | Keep as backup through festival |
| Remove LKP rollup + Host display formula fields from Venues | Not hurting anything — leave in place |
| Members table build | No operational need before festival |
| Full terminology standardization | Too many scripts to update safely in 40 days |
| Delete 16 empty table shells | Requires Airtable UI (API can't delete tables) |

### What breaks if we restructure now

**Nothing critical.** The per-event flat tables are additive — they don't modify or depend on the existing rollup chain. Both systems can coexist during the transition:

- Old shared views still work (they read from the Events table, which isn't changing)
- New per-event Interface Designer pages read from flat tables (independent)
- `oeff-airtable-sync.py` still works (reads/writes Events + Films)
- `oeff-venue-sync.py` still works (patches Venues + Events)
- `eventbrite-state.json` still works (maps venues to Eventbrite events)

The only script that needs updating is `build-host-data-layer.py` (creates display formulas on Venues) — but we're replacing that mechanism entirely with flat tables, so it just doesn't need to run again.

---

## 9. Interface Designer Page Layout

Each per-event Interface Designer page should show:

```
┌─────────────────────────────────────────────┐
│  [Film Title] at [Venue Name]               │
│  [Screening Date] · [Start Time]            │
├─────────────────────────────────────────────┤
│  SCREENING DETAILS                          │
│  Film: [Film Title]     Runtime: [Runtime]  │
│  Date: [Date]           Start: [Time]       │
│  Doors Open: [Time]     Tickets: [URL]      │
│  Price: [Price]                             │
├─────────────────────────────────────────────┤
│  VENUE                                      │
│  [Venue Name]                               │
│  [Full Address]         Capacity: [N]       │
│  Parking: [info]        Transit: [info]     │
│  WiFi: [info]           AV: [notes]         │
├─────────────────────────────────────────────┤
│  CONTACTS                                   │
│  [Contact Name] · [Role]                    │
│  [Email] · [Phone]                          │
│  OEFF Rep: [Name]                           │
├─────────────────────────────────────────────┤
│  RESOURCES                                  │
│  Screening Packet: [URL]                    │
│  Webinar Recording: [URL]                   │
│  Host Guide: hosts.oneearthfilmfest.org     │
│                                             │
│  [Submit Your Venue Details →]              │
└─────────────────────────────────────────────┘
```

**Key difference from v1:** Each page sources from ONE flat table with ONE record. No formula chains to trace. If a field is blank, it's because the data isn't there — not because a rollup failed silently.

---

## 10. Sync and Maintenance

### Data flow (v2)

```
Kim's Tracker Sheet (validated)
  │
  ├──→ Directory table (via import/sync)
  │
  ├──→ Events table (relational key)
  │
  └──→ assemble-event-tables.py
        │
        ├──→ Per-Event Tables (flat, editable by Kim)
        │     └──→ Interface Designer pages (host-facing)
        │
        ├──→ Merge Sheet (Mailmeteor deep links)
        │
        └──→ eventbrite-state.json (unchanged)
```

### Who maintains what

| System | Who | How |
|--------|-----|-----|
| Master tables (Events, Venues, Films, Directory) | Garen (schema), Kim (records) | Airtable UI |
| Per-event flat tables | Kim (corrections, additions) | Airtable UI — direct field editing |
| Per-event flat tables | Garen (refresh from master data) | `assemble-event-tables.py --refresh` |
| Interface Designer pages | Garen (layout, field visibility) | Airtable Interface Designer |
| Host guide website | Garen | git push → Cloudflare auto-deploy |
| Merge sheet deep links | Kim | Updated after `assemble-event-tables.py` generates new URLs |

### Script re-run protocol

When to run `assemble-event-tables.py --refresh`:
- After film assignments change
- After venue contacts are updated in Directory
- After Eventbrite ticket URLs change
- After Kim imports cleaned tracker data

The script preserves Kim's manual edits to fields it doesn't own (Volunteer Needs, AV Notes corrections, etc.). It overwrites script-owned fields from master data.

---

## Glossary (updated from v1)

| Term | Meaning |
|------|---------|
| **Master table** | Persistent, year-over-year data (Directory, Venues, Films) |
| **Relational key** | The Events table — links master tables together for a specific occurrence |
| **Per-event table** | Flat, script-assembled table with ~22 text/date/URL fields — one per event |
| **Assembled data** | Data joined from multiple master tables and written to a flat per-event table |
| **Script-owned field** | A per-event table field that gets overwritten when `assemble-event-tables.py` runs |
| **Kim-editable field** | A per-event table field the script does not overwrite — Kim can edit freely |
| **Interface Designer page** | An Airtable-hosted page with custom layout, sourced from one per-event table |
| **Deep link** | The published URL for a specific Interface Designer page — what hosts receive |
| **Directory** | Unified contacts table — all people, typed by Role + Priority |
| **Collaborator** | Mission-oriented partner (hosts, community orgs) — in-step relationship |
| **Transactional** | Business relationship (filmmakers, vendors) — exchange-based |

---

## Open Items

1. **Kim's cleaned tracker sheet** — blocked on her notification (expected today, March 13)
2. **Interface Designer page creation** — requires some Airtable UI clicks (see patterns doc)
3. **Host intake form routing** — does the per-event model change the form? Need to discuss at next meeting
4. **Film = TBD for Uncommon Ground** — needs film assignment from Ana/Josh
5. **Members table** — deferred, no operational need before festival
6. **AV contact data for 8 venues** — still missing, needs direct outreach

---

## Files Reference

| File | Role in v2 |
|------|-----------|
| This doc (`data-architecture-spec-v2.md`) | Architecture reference |
| `airtable-data-layer-spec.md` | v1 technical spec — still accurate for existing rollup chain (being replaced) |
| `kim-garen-03-13-meeting-summary.md` | Decision source for architecture pivot |
| `~/decisions/2026-03-13-oeff-data-architecture-pivot.md` | Decision record |
| `filmmaker-pipeline-airtable-plan.md` | Films table field additions (compatible with v2) |
| `~/.claude/domains/oeff/airtable-interface-designer-patterns.md` | Interface Designer operational patterns |
| `host-helper-migration-plan.md` | v1 rollout plan — superseded by this doc's migration path |
| `assemble-event-tables.py` | To be built — the core v2 mechanism |
