# Reconciliation Script — Scope

**Goal:** Full-context diff between team-side data sources and Garen's Airtable build, with reconciliation output for any discrepancies.
**Constraint:** stdlib Python 3 only. No pip.
**Output:** Diff report (markdown) + reconciliation patch (CSV) for human review.

---

## The problem

Two parallel data worlds exist:

| Side | What it is | Who touches it |
|------|-----------|----------------|
| **Team-side** | Google Sheets (warm host list, roadmap, milestones), host intake responses | Josh, Ana, Erin — the team's working surfaces |
| **Airtable** | 11-table operational database (venues, events, films, contacts, intake, etc.) | Garen — the canonical build |

Garen built Airtable from the team-side sources, but the migration wasn't a clean 1:1 copy. He normalized venue names, assigned IDs, linked records across tables, filled gaps from intake forms, and filtered out 2025 data. The team-side sheets continue to be edited (new contacts, updated dates, status changes).

**The question this script answers:** Where does Airtable diverge from what the team sees? And where has the team updated something that Airtable hasn't caught yet?

The answer should be small — mostly one-directional (team → Airtable) and mostly known. But the script makes it auditable instead of assumed.

---

## Relationship to existing infrastructure

### `oeff_shadow_diff.py` (already built)

The shadow diff handles **event-level V7↔Airtable comparison** with:
- 9 field specs (Event_ID, Venue_ID, Film_ID, dates, times, status, asks, resources, contacts)
- Severity levels (high/medium/low)
- Hard gate at 2026-03-08 (fail on high mismatches after this date)
- Composite key matching (Event_ID primary, Venue_ID+Date fallback)
- Markdown report output

**This script does NOT replace shadow_diff.** It extends the diff surface beyond events to cover the full data relationship:

| Layer | Shadow diff covers? | This script covers |
|-------|--------------------|--------------------|
| Events (schedule, films, dates) | Yes | No — defer to shadow_diff |
| Venues (names, regions, capacity) | No | Yes |
| Contacts (who's associated with which venue) | No | Yes |
| Milestones (festival timeline, deadlines) | No | Yes |
| Host intake ↔ venue linkage | No | Yes |

---

## Data sources

### Team-side (what the team sees and edits)

| Source | File | Records | Key fields |
|--------|------|---------|------------|
| **Warm host list** | `oeff-warm-hosts-cleaned.csv` | 33 rows | First Name, Last Name, Email |
| **Mail merge contacts** | `hosts-mail-merge-contacts.csv` | 33 rows | First Name, Last Name, Email, Merge status |
| **Roadmap contacts** | `roadmap-venue-contacts.csv` | 22 rows | Host Name (= Venue Name), Venue Contacts (inline `Name <email>` format) |
| **Milestones** | `oeff-merged-timeline-airtable.csv` | ~80 rows | Milestone ID, Phase, Domain, Planned Date, Status, Owner |

### Airtable-side (Garen's build, exported as CSV)

| Source | File | Records | Key fields |
|--------|------|---------|------------|
| **Venues** | `airtable-import/01-venues.csv` | 103 rows | Venue_ID, Venue_Name, Region, Capacity, Tech_Tier |
| **Events** | `airtable-import/03-events.csv` | 190 rows | Event_ID, Venue_ID, Date, Film_ID, Pipeline_Status |
| **Host Intake** | `airtable-import/05-host-intake.csv` | 30 rows | Intake_Id, Venue_Id, Contact_Name, Contact_Email |

---

## Diff strategy

### Layer 1: Venue roster diff

**Compare:** Roadmap venue names ↔ Airtable venue names

The roadmap has 22 venue rows with `Host Name` as the venue identifier. Airtable has 103 venues with `Venue_ID` + `Venue_Name`.

- Match on normalized venue name (case-insensitive, strip punctuation, collapse whitespace)
- Flag: venues in roadmap not in Airtable (team added a venue Garen missed)
- Flag: venues in Airtable not in roadmap (Garen added from intake or historical data — expected, just document)
- Known fuzzy cases to handle:
  - "BUILD, Inc." ↔ "BUILD Chicago"
  - "Trinity Lutheran Church" ↔ "Trinity Lutheran, Des Plaines (Prospect)"
  - "Kehrein Center for the Arts at Urban Essentials" ↔ "Kehrein Center for the Arts at BlkRoom"

**Output:** venue presence table with match status (exact / fuzzy / team-only / airtable-only)

### Layer 2: Contact-venue linkage diff

**Compare:** Team-side contacts (warm list + roadmap inline contacts) ↔ Airtable contacts (host intake)

Match path:
1. Parse roadmap inline contacts: `"Name <email>, Name <email>"` → structured records
2. Match warm list emails → intake Contact_Email → Venue_Id
3. Match roadmap contacts → intake by email or by venue name

**Flag:**
- Contacts in warm list with no Airtable venue linkage (orphaned contacts)
- Contacts in intake with no warm list match (new intake entries team hasn't added to merge list)
- Email mismatches for same person/venue (typo or updated email)
- Shared email addresses (Johnny + Aruj Patney sharing `jpatney@hotmail.com`, Frances + Maranda sharing `bge.chicago773@gmail.com`)

### Layer 3: Milestone diff

**Compare:** Merged timeline CSV ↔ Airtable events (for date/status alignment)

This is lighter — mostly checking whether milestone dates in the team's planning sheet match what's in Airtable events. Not every milestone maps to an event (some are internal deadlines), so:
- Match where Milestone → Event is possible (by venue name + approximate date)
- Flag date discrepancies > 1 day
- Flag status disagreements (milestone says "Done" but event says "Confirmed Interest")

### Layer 4: Anomaly catalog

Cross-cutting issues that don't fit neatly into one layer:
- 9 host intake records with no Venue_ID (known gap — document which ones)
- Venue names in events table that don't match venues table
- 2025 vs 2026 event filtering — confirm Airtable events are properly year-filtered
- Pipeline status distribution (how many Scheduled vs Confirmed Interest vs other)

---

## Target output

### 1. `reconciliation-report.md`

Structured markdown report with sections per layer:

```
# OEFF Reconciliation Report
Run date: YYYY-MM-DD

## Summary
- Venue roster: X matched, Y team-only, Z airtable-only
- Contacts: X linked, Y orphaned, Z intake-only
- Milestones: X aligned, Y date discrepancy, Z status discrepancy
- Anomalies: N flagged

## Layer 1: Venue Roster
[table of matches, fuzzy matches, and unmatched]

## Layer 2: Contact Linkage
[table of linked contacts, orphaned contacts, intake-only contacts]

## Layer 3: Milestones
[table of date/status discrepancies]

## Layer 4: Anomalies
[catalog of cross-cutting issues]
```

### 2. `reconciliation-patch.csv`

One row per actionable discrepancy. Columns:

| Column | Description |
|--------|-------------|
| `Layer` | venue / contact / milestone / anomaly |
| `Source_Side` | team / airtable / both |
| `Record_ID` | Venue_ID or Milestone_ID or email |
| `Field` | What's different |
| `Team_Value` | What the team's source says |
| `Airtable_Value` | What Airtable says |
| `Severity` | high / medium / info |
| `Suggested_Action` | What to do (update airtable / update team sheet / investigate / no action) |
| `Notes` | Context for human reviewer |

### 3. stderr anomaly log

Print anomalies and warnings to stderr during run — shared emails, fuzzy match decisions, parse failures.

---

## What the script does NOT do

- **Does not write to Airtable or Google Sheets.** Output is files. Human acts on them.
- **Does not replace shadow_diff.** Events-level diffing stays in `oeff_shadow_diff.py`.
- **Does not resolve ambiguity.** Fuzzy matches are flagged, not decided. Human reviews.
- **Does not phone home.** No API calls. Reads local CSV exports only.
- **Does not generate merge sheets.** That's a separate downstream step (Mailmeteor merge data comes from Airtable exports, not from this script).

---

## Inputs

```
python3 oeff-reconcile.py \
  --warm       oeff-warm-hosts-cleaned.csv \
  --merge      hosts-mail-merge-contacts.csv \
  --roadmap    roadmap-venue-contacts.csv \
  --milestones oeff-merged-timeline-airtable.csv \
  --venues     airtable-import/01-venues.csv \
  --events     airtable-import/03-events.csv \
  --intake     airtable-import/05-host-intake.csv \
  --out-report reconciliation-report.md \
  --out-patch  reconciliation-patch.csv
```

All paths relative to `~/Desktop/OEFF Clean Data/`.

---

## Expected findings

Based on what we know, the diff should surface:
- **Small number of venue name mismatches** — Garen normalized during import, team sheets still have old names
- **A few orphaned warm-list contacts** — people on the email list who haven't submitted intake forms or don't have a 2026 event yet
- **Intake records without Venue_ID** — 9 known, script documents exactly which ones
- **Milestone-to-event date drift** — if the team updated a screening date in their sheet but Airtable hasn't caught up (or vice versa)

Most discrepancies should be one-directional: team source → Airtable (Garen updates Airtable to match). A few might go the other direction (Garen added structure in Airtable that the team sheets don't reflect — that's expected and fine).

---

## Open questions for build session

1. **Fuzzy matching threshold:** How aggressive for venue names? Token overlap? Edit distance? Or a hand-curated alias map for the ~5 known variants?
2. **Milestone mapping:** The merged timeline has 80+ milestones but most are internal deadlines, not screenings. Which milestone types should map to Airtable events?
3. **Should the script also check films table?** `airtable-import/02-films.csv` has film data that could be cross-referenced, but it's Garen's build — the team doesn't maintain a parallel film list.
4. **Run cadence:** One-shot audit, or designed to re-run weekly as data evolves toward festival?
