# OEFF V7 → Airtable Import Package

**Export Date:** February 6, 2026  
**Total Records:** 783 across 11 tables  
**Format:** UTF-8 CSV (no BOM)  
**Status:** Ready for Airtable import

## Quick Start

1. **Read the guides in this order:**
   - This README (you are here)
   - `IMPORT-ORDER.md` (detailed import sequence)
   - `EXPORT-SUMMARY.txt` (comprehensive reference)

2. **Import the CSVs in dependency order:**
   - Phase 1: Foundation tables (Venues, Films)
   - Phase 2: Reference tables (Sponsors, Partners)
   - Phase 3: Event-related tables (Events, Contacts, Intake)
   - Phase 4: Media/QA tables (Media Assets, Packet QA)
   - Phase 5: Participants/Recordings

3. **Create linked record fields** after all data is imported

4. **Validate** that all records imported successfully

## Files in This Package

### CSV Data Files (11 total)

| File | Records | Description |
|------|---------|-------------|
| **01-venues.csv** | 100 | Venue/Host locations |
| **02-films.csv** | 12 | 2026 Films |
| **03-events.csv** | 219 | Events (2024-2026) |
| **04-film-contacts.csv** | 9 | Film contact info |
| **05-host-intake.csv** | 28 | Host intake forms |
| **06-sponsors.csv** | 23 | FY26 Sponsors |
| **07-media-assets.csv** | 25 | Event media files |
| **08-packet-qa.csv** | 23 | Packet QA data |
| **09-participants.csv** | 132 | Event participants |
| **10-recordings.csv** | 62 | Event recordings |
| **11-partners.csv** | 150 | Partner organizations |

### Documentation Files

- **README.md** (this file) - Quick reference
- **IMPORT-ORDER.md** - Detailed import instructions & dependencies
- **EXPORT-SUMMARY.txt** - Complete field reference & mapping guide

## Data Quality Standards

All CSV files meet these requirements:
- ✓ UTF-8 encoding (no BOM)
- ✓ Clean headers (spaces, title case, not underscores)
- ✓ No index column
- ✓ Leading/trailing whitespace stripped
- ✓ Empty cells for NULL/missing data
- ✓ Dates in YYYY-MM-DD format
- ✓ Boolean fields as "true"/"false"
- ✓ All IDs as text (not numbers)

## Key Data Points

**Venues:** 100 OEFF host locations
- All have Venue ID and name
- Region and capacity data is partial (as expected - many TBD)
- Contact info minimal in many cases

**Films:** 12 films in 2026 lineup
- All fields present and clean
- Boolean fields standardized to true/false
- Website/trailer links may be empty

**Events:** 219 total events across 3 years
- 31 in 2026 (planning status - many dates TBD)
- 180 in 2025 (completed)
- 8 in 2024 (completed)
- Sorted by year (desc) then date

**Sponsors:** 23 FY26 sponsors
- All have Sponsor ID, Name, Level
- Event IDs included for future linking
- Website and tagline included

**Participants:** 132 event participants
- Includes panelists, presenters, and attendees
- Role field is sparse (many empty)
- Email addresses for most

## Import Sequence Overview

### Phase 1: Foundation (No dependencies)
```
1. 01-venues.csv → Venues table
2. 02-films.csv → Films table
```

### Phase 2: References (Can import anytime)
```
3. 06-sponsors.csv → Sponsors table
4. 11-partners.csv → Partners table
```

### Phase 3: Event Core (After Phase 1)
```
5. 03-events.csv → Events table
6. 04-film-contacts.csv → Film Contacts table
7. 05-host-intake.csv → Host Intake table
```

### Phase 4: Media/QA (After Phase 3)
```
8. 07-media-assets.csv → Event Media Assets table
9. 08-packet-qa.csv → Packet QA table
```

### Phase 5: Participants (After Phase 3)
```
10. 09-participants.csv → Participants table
11. 10-recordings.csv → Recordings table
```

### Phase 6: Link Records (After all imports)
Create these linked record fields:
- Events → Venues (Venue ID)
- Events → Films (Film ID)
- Film Contacts → Films (Film ID)
- Host Intake → Venues (Venue ID)
- Event Media → Events (Event ID)
- Packet QA → Events (Event ID)
- Recordings → Events (Event ID)

## Airtable Import Steps

For each CSV file:

1. **Open Airtable workspace** → Select base
2. **Create new table** (or use existing if modifying)
3. **Use "Import" feature:**
   - Select the CSV file
   - Airtable auto-detects format
   - Review field mappings
   - Confirm primary key is correct
4. **Click "Import"** and wait for completion
5. **Verify** row count matches

## Common Issues & Solutions

### "Invalid UTF-8" error
- File is already valid UTF-8 (no BOM)
- Check your Airtable import settings

### Dates show as text
- Format is YYYY-MM-DD (valid)
- Airtable may need date field type
- Convert manually if needed

### IDs won't link after import
- IDs are TEXT not numbers
- Ensure exact match (case-sensitive)
- Check for leading/trailing spaces (shouldn't exist)

### Missing data in imported table
- Likely empty in source data
- This is normal - many fields are conditional
- Check EXPORT-SUMMARY.txt for field notes

## Post-Import Validation

After importing all 11 CSVs:

1. **Count records:**
   - Venues: 100
   - Films: 12
   - Events: 219
   - Film Contacts: 9
   - Host Intake: 28
   - Sponsors: 23
   - Media Assets: 25
   - Packet QA: 23
   - Participants: 132
   - Recordings: 62
   - Partners: 150
   - **TOTAL: 783 records**

2. **Test linking:**
   - Pick an Event record
   - Verify Venue ID links to Venues table
   - Verify Film ID links to Films table

3. **Sample data check:**
   - Verify first record in each table
   - Check that dates are parsed correctly
   - Verify boolean fields show properly

## File Descriptions

### Primary Keys (Unique Identifiers)

- **Venue ID**: V-001, V-002, etc.
- **Film ID**: F26-001, F26-002, etc.
- **Event ID**: E26-001, E25-001, E24-001, etc.
- **Contact ID**: FC26-001, FC26-002, etc.
- **Intake ID**: HIF-001, HIF-002, etc.
- **Sponsor ID**: S26-001, S26-002, etc.
- **Media ID**: M26-001, M26-002, etc.
- **Packet ID**: PKT-001, PKT-002, etc.
- **Participant ID**: P25-001, P25-002, etc.
- **Recording ID**: R25-001, R25-002, etc.
- **Partner ID**: ORG-001, ORG-002, etc.

### Foreign Keys (Link IDs)

- **Venue ID** → Links Events to Venues
- **Film ID** → Links Events to Films, Film Contacts to Films
- **Event ID** → Links Media Assets, Packet QA to Events
- **Event IDs** → Links Sponsors to multiple Events

## Next Steps After Import

1. **Test all linked record fields** - create 5 test records in each table
2. **Add automation** - create Airtable automations for workflows
3. **Set up views** - create filtered views by year, status, etc.
4. **Configure notifications** - set up alerts for status changes
5. **Train team** - walk through the data structure with team

## Support

For questions about:
- **Data mapping**: See `EXPORT-SUMMARY.txt`
- **Import order**: See `IMPORT-ORDER.md`
- **Specific fields**: Check the field mapping sections
- **Linking instructions**: See "Create Linked Records" section

## Export Details

**Source Files:**
- V7-with-Dashboard.xlsx (main workbook)
- Benefits-Tracking-with-IDs.xlsx (sponsors)
- V7-Event-Media-Fixed.xlsx (media assets)
- V7-Packet-QA-Fixed.xlsx (QA data)

**Export Script:** Python with pandas/openpyxl  
**Export Date:** 2026-02-06  
**Total Size:** 124 KB

---

Ready to import? Start with Phase 1 and follow the import sequence in `IMPORT-ORDER.md`.
