# OEFF Airtable Import Manifest

## Import Order & Row Counts

This document lists all CSV files for Airtable import in the required dependency order.

| # | File | Rows | Cols | Airtable Table | Primary Key | Status |
|---|------|------|------|-----------------|------------|--------|
| 1 | 01-venues.csv | 100 | 9 | Venues | Venue ID | Ready (Previous Contacts field pending) |
| 2 | 02-films.csv | 12 | 14 | Films | Film ID | Ready (Runtime, Filmmakers pending) |
| 3 | 03-events.csv | 175 | 32 | Events | Event ID | **Updated 2026-02-11** — enriched, cleaned (dropped 1 dupe + 41 placeholders) |
| 4 | 04-film-contacts.csv | 9 | 15 | Film Contacts | Contact ID | **Updated 2026-02-11** — added Is Primary, Secondary Contact, Formats, Caption/AD/Spanish, Timestamp |
| 5 | 05-host-intake.csv | 28 | 26 | Host Intake | Intake ID | Ready |
| 6 | 06-sponsors.csv | 23 | 36 | Sponsors | Sponsor ID | **Updated 2026-02-11** — added Commitment Date + full 29-field benefits matrix |
| 7 | 07-media-assets.csv | 25 | 20 | Event Media Assets | Media ID | Ready |
| 8 | 08-packet-qa.csv | 23 | 18 | Packet QA | Packet ID | Ready |
| 9 | 09-participants.csv | 132 | 7 | Participants | Participant ID | Ready |
| 10 | 10-recordings.csv | 62 | 5 | Recordings | Recording ID | Ready |
| 11 | 11-partners.csv | 150 | 6 | Partners | Partner ID | Ready |


## Import Instructions

### Phase 1: Foundation Tables (No Dependencies)
Import these first - they establish the core data:

1. **01-venues.csv** → Venues table
   - Primary Key: Venue ID
   - No dependencies

2. **02-films.csv** → Films table
   - Primary Key: Film ID
   - No dependencies

### Phase 2: Contact/Reference Tables
Import after foundation tables:

3. **06-sponsors.csv** → Sponsors table
   - Primary Key: Sponsor ID
   - Links to: Event IDs (linked record)

4. **11-partners.csv** → Partners table
   - Primary Key: Partner ID
   - No dependencies

### Phase 3: Event-Related Tables (Depend on Venues & Films)
Import these after Phase 1 & 2:

5. **03-events.csv** → Events table
   - Primary Key: Event ID
   - Links to: Venue ID (lookup to Venues table), Film ID (lookup to Films table)
   - **Post-import action**: Create linked record fields:
     - Venue ID → Venues.Venue ID
     - Film ID → Films.Film ID

6. **04-film-contacts.csv** → Film Contacts table
   - Primary Key: Contact ID
   - Links to: Film ID (lookup to Films table)
   - **Post-import action**: Link Film ID to Films table

7. **05-host-intake.csv** → Host Intake table
   - Primary Key: Intake ID
   - Links to: Venue ID (lookup to Venues table)
   - **Post-import action**: Link Venue ID to Venues table

### Phase 4: Media & QA Tables (Depend on Events)
Import these after Phase 3:

8. **07-media-assets.csv** → Event Media Assets table
   - Primary Key: Media ID
   - Links to: Event ID (lookup to Events table)
   - **Post-import action**: Link Event ID to Events table

9. **08-packet-qa.csv** → Packet QA table
   - Primary Key: Packet ID
   - Links to: Event ID (lookup to Events table)
   - **Post-import action**: Link Event ID to Events table

### Phase 5: Participant/Recording Tables (Depend on Events)
Import these after Phase 3:

10. **09-participants.csv** → Participants table
    - Primary Key: Participant ID
    - Links to: Event Film (if applicable)

11. **10-recordings.csv** → Recordings table
    - Primary Key: Recording ID
    - Links to: Event (lookup to Events table)
    - **Post-import action**: Link Event to Events table

## Linking Instructions (Post-Import)

After all CSVs are imported, create these linked record fields:

### Events Table
- Link Venue ID → Venues table
- Link Film ID → Films table

### Film Contacts Table
- Link Film ID → Films table

### Host Intake Table
- Link Venue ID → Venues table

### Event Media Assets Table
- Link Event ID → Events table

### Packet QA Table
- Link Event ID → Events table

### Recordings Table
- Link Event → Events table

### Sponsors Table
- Link Event IDs → Events table (if formatted as array)

## Data Quality Notes

- All dates are in YYYY-MM-DD format
- Boolean fields use "true"/"false" values
- Empty cells represent NULL/missing data
- All text fields are UTF-8 encoded with no BOM
- Leading/trailing whitespace has been stripped from all values
- IDs are text fields to preserve leading zeros if any exist

## Export Metadata

- Original Export Date: 2026-02-06
- **Updated: 2026-02-11** (schema v1.1 compliance update)
- Source: OEFF V7 Workbook Suite + ACTIVE_Roadmap OEFF2026Films-Schedule-Programs.xlsx + Benefits Tracking 2026.xlsx
- Total Records Exported: 739
- Files updated in v1.1: 03-events.csv (12→32 columns), 04-film-contacts.csv (7→15 columns), 06-sponsors.csv (6→36 columns)

## Enrichment Notes (v1.1)

### 03-events.csv
- 2026 events (E26-001 to E26-014) enriched from 2026HostVenues sheet rows 4-25
- 2026 pipeline events (E26-015 to E26-020) have Event Tier from rows 18-25
- 2026 pipeline events (E26-021 to E26-029) matched to rows 66-77 where possible
- 2025/2024 events carry empty values for new columns (no retroactive enrichment)
- 2 metadata rows removed (empty Event ID, "LINK CHECK" row)
- E26-026 dropped (duplicate pipeline entry for Columbia College)
- 41 empty V-014 (Chicago Cultural Center) placeholder rows dropped from 2025 events
- Row count: 219 → 175 (28 for 2026, 139 for 2025, 8 for 2024)

### 04-film-contacts.csv
- Re-exported from V7 Film_Contacts sheet with all 15 columns
- Secondary contacts, formats, caption/AD/Spanish status, and timestamps now included

### 06-sponsors.csv
- Re-exported from Benefits Tracking 2026.xlsx FY26 Sponsors sheet
- Full 29-field benefits matrix preserved (checkboxes, ticket counts, promo status)
- Commitment Date added (format: MM.DD.YY from source)
- Contact Email column present but empty (not in source — needs manual population)
