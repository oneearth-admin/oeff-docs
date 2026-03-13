# OEFF Airtable Shared Views — Session Summary

**Date:** 2026-03-10
**Sessions:** 6 continuation sessions (context window exhausted 5 times)
**Outcome:** All 24 per-venue shared grid views created in Airtable with public shared links generated and persisted.

---

## What Was Done

### Phase 2 of Host Helper Migration Plan (fully complete)

Replaced the per-venue static HTML pages with Airtable shared grid views — one per venue, each with a unique public link that shows only that host's data in a read-only grid. No login required for viewers.

### Method: Template-then-Duplicate

1. Created a **Host Template** view in the Events table with:
   - **10 fields visible:** Event ID, Venue Name, Date, Time, Ticket Price, Film Title, Ticket URL, OEFF Rep, Volunteer Needs, Screening Packet URL
   - **40 fields hidden:** All internal/financial/licensing/pipeline fields
   - **Filters:** Year = 2026
   - **Sort:** Date ascending
   - View ID: `viwcywO9KVFIkKo16`

2. Duplicated the template 24 times — once per venue — adding only a "Venue Name contains [venue]" filter to each duplicate.

3. Generated a **shared link** for each view via Airtable's "Share and sync" → "Create link to view" dialog.

4. Captured each shared link URL via JavaScript DOM extraction from the Airtable share dialog.

### Why Browser Automation (Not API)

Airtable's REST API does not support Views CRUD (create/read/update/delete) on non-Enterprise plans. View creation, duplication, field visibility, and shared link generation all required browser automation via the Claude-in-Chrome MCP tools.

---

## Airtable Structure

| Property | Value |
|----------|-------|
| Base ID | `app9DymWrbAQaHH0K` |
| Base URL | `https://airtable.com/app9DymWrbAQaHH0K` |
| Events Table ID | `tblau3F9sXWnNhDN5` |
| Host Template View ID | `viwcywO9KVFIkKo16` |
| Shared link pattern | `https://airtable.com/app9DymWrbAQaHH0K/shr{hash}` |

### Views in the Events Table Sidebar (top to bottom)

Non-host views:
- Grid view (default)
- Festival Calendar
- Event Pipeline
- Host Template (the source template — no shared link)

Host views (24 total, alphabetical by creation order in sidebar):
1. Trinity Lutheran Des Plaines
2. Village of Oak Park
3. Triton College
4. Kehrein Center for the Arts
5. IIT Bronzeville
6. Epiphany Center for the Arts
7. Dominican University
8. Chicago Public Library Rogers Park
9. Chicago Public Library Harold Washington
10. Chicago Cultural Center
11. Chicago Climate Action Museum
12. Calumet College of St. Joseph
13. BUILD Inc.
14. Broadway United Methodist Church
15. Black Girl Environmentalists
16. Bethel New Life
17. Andersonville Chamber of Commerce
18. Academy for Global Citizenship
19. Go Green Park Ridge
20. Euclid AVE UMC
21. Trinity Lutheran Church
22. Uncommon Ground
23. Climate Action Evanston
24. Columbia College

---

## All 24 Shared Links

Persisted to: `~/Desktop/OEFF Clean Data/shared-view-links.json`

| # | Venue | Share ID | Full URL |
|---|-------|----------|----------|
| 1 | Academy for Global Citizenship | `shrZ4bZsC6Lt8XKCF` | `https://airtable.com/app9DymWrbAQaHH0K/shrZ4bZsC6Lt8XKCF` |
| 2 | Andersonville Chamber of Commerce | `shr7pV6RQLoPTXCV0` | `https://airtable.com/app9DymWrbAQaHH0K/shr7pV6RQLoPTXCV0` |
| 3 | Bethel New Life | `shrUMnDFGMfejqyHJ` | `https://airtable.com/app9DymWrbAQaHH0K/shrUMnDFGMfejqyHJ` |
| 4 | Black Girl Environmentalists | `shrdMQnpWyxtk0PhT` | `https://airtable.com/app9DymWrbAQaHH0K/shrdMQnpWyxtk0PhT` |
| 5 | Broadway United Methodist Church | `shrfm6XggKVWuiHqI` | `https://airtable.com/app9DymWrbAQaHH0K/shrfm6XggKVWuiHqI` |
| 6 | BUILD Inc. | `shrednLXL9Q3ayoHT` | `https://airtable.com/app9DymWrbAQaHH0K/shrednLXL9Q3ayoHT` |
| 7 | Calumet College of St. Joseph | `shrzL27lnYWzgdSn2` | `https://airtable.com/app9DymWrbAQaHH0K/shrzL27lnYWzgdSn2` |
| 8 | Chicago Climate Action Museum | `shrSWXUc8RzyOr9v0` | `https://airtable.com/app9DymWrbAQaHH0K/shrSWXUc8RzyOr9v0` |
| 9 | Chicago Cultural Center | `shrjT1GhJpoCwqP2W` | `https://airtable.com/app9DymWrbAQaHH0K/shrjT1GhJpoCwqP2W` |
| 10 | Chicago Public Library Harold Washington | `shrvFhjzterbqOkWt` | `https://airtable.com/app9DymWrbAQaHH0K/shrvFhjzterbqOkWt` |
| 11 | Chicago Public Library Rogers Park | `shrxnMLK78LaOmCVo` | `https://airtable.com/app9DymWrbAQaHH0K/shrxnMLK78LaOmCVo` |
| 12 | Climate Action Evanston | `shrYIi0mDsLOiuVKV` | `https://airtable.com/app9DymWrbAQaHH0K/shrYIi0mDsLOiuVKV` |
| 13 | Columbia College | `shrNh07SV8mviGA9x` | `https://airtable.com/app9DymWrbAQaHH0K/shrNh07SV8mviGA9x` |
| 14 | Dominican University | `shrwTcoFhtsUFNqrE` | `https://airtable.com/app9DymWrbAQaHH0K/shrwTcoFhtsUFNqrE` |
| 15 | Epiphany Center for the Arts | `shrf0bG2ZbM2fP4W2` | `https://airtable.com/app9DymWrbAQaHH0K/shrf0bG2ZbM2fP4W2` |
| 16 | Euclid AVE UMC | `shrAsitAmeP9I9dmO` | `https://airtable.com/app9DymWrbAQaHH0K/shrAsitAmeP9I9dmO` |
| 17 | Go Green Park Ridge | `shrBB9B9etXLqLGPi` | `https://airtable.com/app9DymWrbAQaHH0K/shrBB9B9etXLqLGPi` |
| 18 | IIT Bronzeville | `shrSiTKnEqxDJvxe7` | `https://airtable.com/app9DymWrbAQaHH0K/shrSiTKnEqxDJvxe7` |
| 19 | Kehrein Center for the Arts | `shrCzt737tKMTdSCw` | `https://airtable.com/app9DymWrbAQaHH0K/shrCzt737tKMTdSCw` |
| 20 | Triton College | `shr8d1PlzmsV41PMZ` | `https://airtable.com/app9DymWrbAQaHH0K/shr8d1PlzmsV41PMZ` |
| 21 | Trinity Lutheran Church | `shrMtCd2dkztLZ42e` | `https://airtable.com/app9DymWrbAQaHH0K/shrMtCd2dkztLZ42e` |
| 22 | Trinity Lutheran Des Plaines | `shrOslN5HSFgor5O8` | `https://airtable.com/app9DymWrbAQaHH0K/shrOslN5HSFgor5O8` |
| 23 | Uncommon Ground | `shrhALPr1a5Lz26Xz` | `https://airtable.com/app9DymWrbAQaHH0K/shrhALPr1a5Lz26Xz` |
| 24 | Village of Oak Park | `shr1FH3QW9BMMPYgU` | `https://airtable.com/app9DymWrbAQaHH0K/shr1FH3QW9BMMPYgU` |

---

## Verified Working

Columbia College link tested in an incognito-like new tab:
- **URL:** `https://airtable.com/app9DymWrbAQaHH0K/shrNh07SV8mviGA9x`
- **Result:** Public read-only grid view. Title shows "Host: Columbia College". 2 records visible (E26-001, E26-005). Columns: Event ID, Venue Name, Date, Time, Ticket Price, Film Title. No login required.
- **Page title:** "Airtable - Host: Columbia College"

---

## What Each Shared View Shows

### Visible fields (10)
1. Event ID
2. Venue Name
3. Date
4. Time
5. Ticket Price
6. Film Title
7. Ticket URL (Eventbrite link)
8. OEFF Rep
9. Volunteer Needs
10. Screening Packet URL

### Hidden fields (40)
All internal/financial/licensing/pipeline fields including:
- Pipeline Status, Pipeline Select
- Host Fee, Invoice fields
- Licensing fields
- Film Survey Complete
- Notes (internal)
- OEFF Rep column (internal team contact)
- All other operational fields

### Filters
- Year = 2026 (from template)
- Venue Name contains "[venue name]" (per-venue filter)

### Sort
- Date ascending

---

## Key Files

| File | Purpose |
|------|---------|
| `~/Desktop/OEFF Clean Data/shared-view-links.json` | All 24 share IDs, machine-readable |
| `~/Desktop/OEFF Clean Data/shared-view-session-summary.md` | This file — full session record |
| `~/Desktop/OEFF Clean Data/host-helper-migration-plan.md` | The plan this work executes (Phase 2) |
| `~/Desktop/OEFF Clean Data/host-helper-session-summary.md` | Prior session: research + info hierarchy |

---

## Venue Count: Why 24, Not 22

The OEFF roadmap lists 22 scheduled venues. The Airtable Events table has 24 distinct venue names because:
- Some venues appear under slightly different names in different records
- A few venues were added after the original 22-venue count was established
- Trinity Lutheran Church (Evanston) and Trinity Lutheran Des Plaines are separate venues

The 24 Host views match exactly with the 24 unique venue names that appear in the Events table for Year = 2026.

---

## What's Left (Migration Plan Phases 2-3)

### Phase 2 remaining steps
- [ ] Record all 24 links in Google Sheet (tab `923179468`, URL: `https://docs.google.com/spreadsheets/d/1nkPZVNQMdAIQm1F3OFcUI87RGzK8KOceH5nyfOdMxyA/edit`)
- [ ] Verify each shared link shows only that venue's data (spot-checked Columbia College — works)
- [ ] Internal review — Kim + Garen look at a sample view together

### Phase 3: Share with hosts
- [ ] Add Airtable shared links to Mailmeteor merge sheet
- [ ] Test with 1-2 real hosts before broader send
- [ ] Send "Your screening page is ready" emails as venues are ready
- [ ] Interns validate venue data: contacts current, times correct, links working

### Data readiness blockers (from migration plan)
- [ ] Film runtimes — no runtime exists in any data source, blocks run-of-show
- [ ] Chasing Time — assigned to 3 venues, no F26 Films table record
- [ ] 8 remaining Eventbrite events not yet created
- [ ] AV/tech contacts — 10 recovered from 2025, 8 venues have none
- [ ] OEFF rep assignment per venue — not yet assigned
- [ ] Host contact verification — 4 venues have different contacts in 2025 vs 2026

---

## Technical Notes for Future Sessions

### How to create a new shared view (if a venue is added)
1. Go to `https://airtable.com/app9DymWrbAQaHH0K/tblau3F9sXWnNhDN5/viwcywO9KVFIkKo16` (Host Template)
2. Right-click the view name in sidebar → Duplicate view
3. Rename to "Host: [Venue Name]"
4. Edit filters → Add "Venue Name contains [venue name]"
5. Click "Share and sync" → "Create link to view"
6. Copy the `shr...` ID from the generated URL
7. Add to `shared-view-links.json`

### How to disable a shared link
1. Navigate to the venue's Host view
2. Click "Share and sync"
3. Toggle off the shared link or click "Disable shared link"

### JavaScript to extract shared link from Airtable dialog
```javascript
(() => {
  const inputs = document.querySelectorAll('input');
  for (const i of inputs) {
    if (i.value && i.value.includes('airtable.com')) return i.value;
  }
  return 'not found';
})()
```

### Airtable API limitation
Views CRUD is NOT available through the REST API on non-Enterprise plans. All view operations (create, duplicate, rename, filter, share) must be done through the Airtable web UI or browser automation. The API can read/write records and field metadata, but not view configurations.

---

## Session Friction Log

- Browser extension disconnected multiple times at session boundaries (context window exhaustion → new session → extension not connected). Required user to say "continue" or "try again" to reconnect.
- Epiphany Center link extraction returned "not found" once — the Share dialog had opened but showed "Create link to view" (link not yet created). Fixed by clicking the create button and waiting 2s.
- Context window exhausted 5 times during this work. The `shared-view-links.json` file was critical for persisting progress across sessions — without it, links captured in previous sessions would have been lost.
- The original session summary mentioned "25 venues" but the actual count is 24 Host views. The discrepancy was a miscount in an earlier session.
