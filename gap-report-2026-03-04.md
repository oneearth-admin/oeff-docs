# OEFF 2026 Venue Data — Gap Report
Generated: 2026-03-04

## Summary

- **26 confirmed 2026 venues** in the Active Roadmap
- **12 capacity values** can be pre-filled from prior-year Host Helpers (need host confirmation)
- **8 venues** still have no capacity data from any source
- **No address column** exists in the 2026HostVenues sheet — addresses extracted from 13 Host Helpers
- **Host intake form has 0 responses** — this is the designed mechanism for collecting this data

---

## Action 1: Pre-fill from Host Helpers (ready now)

These values come from last year's Host Helpers. They should be treated as estimates
until confirmed by each host through the intake form or direct communication.

| Row | Venue | Current | Proposed | Source |
|-----|-------|---------|----------|--------|
| 8 | Village of Oak Park at OPRF High School | TBD | **150 seats** | OEFF2025 04.23 Host Helper: Village |
| 10 | Triton College | Check last yr HH | **400** | OEFF2025 04.24 Host Helper: Triton  |
| 11 | Bethel New Life | 120? | **180-200** | OEFF2024 04.20-PM Host Helper: Beth |
| 12 | IIT Bronzeville | Check last yr HH | **155** | OEFF2025 04.23 Host Helper: Organic |
| 13 | Park Ridge Community Church (Go Green Park Ri | TBD | **100+** | OEFF2024 04.18 Host Helper: Go Gree |
| 16 | Cultivate Collective (at Academy for Global C | Check last yr HH | **150 pple** | OEFF2025 04.26 Host Helper: Cultiva |
| 17 | BUILD Chicago | Check last yr HH | **100** | OEFF2025 04.26 Host Helper: BUILDCh |
| 18 | Broadway United Methodist Church | Check last yr HH | **100** | OEFF2025 04.25 Host Helper: Broadwa |
| 19 | Calumet College of St. Joseph | TBD | **75-80** | 0_MiniFest_Host Helper: Ford Calume |
| 24 | Dominican University | Check email thread | **100** | OEFF2025 04.24 Host Helper: Dominic |
| 56 | Academy for Global Citizenship | (empty) | **150 pple** | OEFF2025 04.26 Host Helper: Cultiva |
| 60 | Andersonville Chamber of Commerce | (empty) | **50** | OEFF2025 04.26 Host Helper: Anderso |

---

## Action 2: Needs host intake (no prior data)

These venues have TBD capacity and no matching Host Helper from prior years.
Data must come from the host intake form or direct outreach.

- **Climate Action Evanston likely at Evanston Public Libra** (4/23/26) — capacity unknown, no prior Host Helper
- **Institute of Cultural Affairs in the USA** (4/24/26) — capacity unknown, no prior Host Helper
- **Chicago Climate Action Museum** (4/24/26) — capacity unknown, no prior Host Helper
- **Euclid Ave United Methodist Church** (4/24/26) — capacity unknown, no prior Host Helper
- **Kehrein Center for the Arts at Urban Essentials Cafe** (4/25/26) — capacity unknown, no prior Host Helper
- **Black Girl Environmentalists at UIC or Patagonia Fulton** (4/25/26) — capacity unknown, no prior Host Helper
- **Chicago Public Library Rogers Park Branch** (4/26) — capacity unknown, no prior Host Helper
- **Chicago Public Library Harold Washington Branch** (4/26) — capacity unknown, no prior Host Helper

---

## Action 3: Address data

The 2026HostVenues sheet has no address column. Addresses were extracted from
prior-year Host Helpers for 13 venues. Options:

1. Add an address column to 2026HostVenues and populate from Host Helper data
2. Store addresses in Airtable (Venues table) and reference from there
3. Rely on the host intake form to collect current addresses

**Extracted addresses available:**

| Venue | Address (from prior HH) |
|-------|-------------------------|
| Village of Oak Park at OPRF High School | Village of Oak Park, Oak Park Village Hall, 123 Madison St., Coun |
| Triton College | Triton College 2000 Fifth Ave River Grove, IL 60171 (Showing loca |
| Bethel New Life | Bethel New Life, 1140 N Lamon Ave, Chicago, IL 60651 |
| IIT Bronzeville | Illinois Tech MTCC Building |
| Park Ridge Community Church (Go Green Park Ri | Park Ridge Community Church, 100 Courtland Ave., Park Ridge, IL 6 |
| Cultivate Collective (at Academy for Global C | Academy for Global Citizenship, 4942 W 44th St, Chicago, IL 60638 |
| BUILD Chicago | BUILD Chicago, Performance Hall, 5100 W Harrison St., Chicago 606 |
| Broadway United Methodist Church | Broadway United Methodist Church, 3338 N Broadway, Chicago 60657 |
| Calumet College of St. Joseph | Big Marsh Bike Park, , 11559 S. Stony Island Ave., Chicago |
| Dominican University | Dominican University, Parmer Hall, Room 108, 7900 Division St., R |
| Academy for Global Citizenship | Academy for Global Citizenship, 4942 W 44th St, Chicago, IL 60638 |
| Andersonville Chamber of Commerce | 5706 N Clark, Chicago IL 60660 |

---

## Data Quality Notes

- Capacity values from Host Helpers are self-reported by hosts and may not reflect current conditions
- Some venues may have changed physical space or seating arrangement since last year
- "150 pple" and "100+" are informal — standardize to numbers when confirming
- Bethel New Life: sheet says "120?" but 2024 Host Helper says 180-200 — worth clarifying
- Calumet College matched to 2023 MiniFest at Ford Calumet Education Center — may be different space
- Kehrein Center: Host Helper exists but capacity field was not found in it
- ICA (Institute of Cultural Affairs): Host Helper exists but capacity wasn't extracted — may need manual check

---

## Structured Data Files

All data has been saved locally for further processing:

| File | Contents |
|------|----------|
| `venue-data-combined.json` | All 26 venues with capacity, address, contacts, confidence levels |
| `hh-extracted-data.json` | Raw extractions from 16 Host Helper spreadsheets |
| `gdrive-pull-log.json` | Index of all 84 Host Helper files on OEC Drive |
| `hh-venue-match.json` | Mapping from 2026 venues to their prior Host Helper files |
| `gap-analysis-2026-active.json` | Gap flags for all 2026 venues |
| `sheet-update-preview.json` | Exact cells to update in the roadmap sheet |
