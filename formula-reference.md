# OEFF V7 Formula Reference — Phase 1 Dashboard

> **Complete formula guide for Dashboard_V2 sheet**
> All formulas auto-calculate from source sheets (Hosts, Events_2026, Films_2026, Film_Contacts, Host_Intake, Ana_Matching)

---

## Dashboard Counters

### Pipeline Status Counts

**Cell B3: Total Hosts**
```
=COUNTA(Hosts!A2:A)
```
Counts all non-empty cells in column A (Venue_ID) of Hosts sheet. Excludes header row.

**Cell B4: Events Scheduled**
```
=COUNTIF(Events_2026!D2:D,"Scheduled")
```
Counts rows in Events_2026 sheet where column D (Pipeline_Status) = "Scheduled"

**Cell B5: Events Confirmed Interest**
```
=COUNTIF(Events_2026!D2:D,"Confirmed Interest")
```
Counts rows where status = "Confirmed Interest"

**Cell B6: Events Interested**
```
=COUNTIF(Events_2026!D2:D,"Interested")
```
Counts rows where status = "Interested"

**Cell B7: Total Events 2026**
```
=COUNTA(Events_2026!A2:A)
```
Counts all event IDs (non-empty cells in Event_ID column)

---

### Film Status Counts

**Cell B9: Total Films**
```
=COUNTA(Films_2026!A2:A)
```
Counts all Film_IDs in Films_2026 sheet

**Cell B10: Films with Intake**
```
=COUNTIF(Films_2026!E2:E,"Y")
```
Counts films where column E (Intake_Received) = "Y"

**Cell B11: Films Missing Intake**
```
=COUNTIF(Films_2026!E2:E,"N")
```
Counts films where Intake_Received = "N"

**Cell B12: Films with Captions**
```
=COUNTIF(Film_Contacts!F2:F,"Complete")
```
Counts entries in Film_Contacts sheet where Caption_Status (column F) = "Complete"

---

### Host Intake Tracking

**Cell B14: Total Intake Responses**
```
=COUNTA(Host_Intake!A2:A)
```
Counts all intake form responses (non-empty Venue_Name cells)

**Cell B15: Unmatched Intake Forms**
```
=COUNTA(Ana_Matching!A2:A)
```
Counts rows in Ana_Matching sheet awaiting her review

**Cell B16: Intake Match Rate**
```
=TEXT((B14-B15)/B14,"0%")
```
Calculates percentage: (Total - Unmatched) / Total. Formats as percentage (e.g., "64%")

**Cell B17: Confirmed Hosts with Intake**
```
=COUNTIFS(Events_2026!D2:D,"Scheduled",Events_2026!C2:C,"<>")
```
Counts events with status "Scheduled" AND non-empty Venue_ID (column C)

---

### Action Items (What Needs Attention)

**Cell B19: Events Without Dates**
```
=COUNTIF(Events_2026!F2:F,"")
```
Counts events where Event_Date column (F) is empty

**Cell B20: Events Without Contacts**
```
=COUNTIF(Events_2026!H2:H,"")
```
Counts events where Team_Contact column (H) is empty

**Cell B21: Films Missing Intake**
```
=COUNTIF(Films_2026!E2:E,"N")
```
Same as B11 — repeated here for the "Action Items" section

**Cell B22: Total Action Items**
```
=SUM(B19:B21)
```
Adds up all action items. Use conditional formatting: if > 0, highlight yellow.

---

## Pipeline Progress (Funnel Percentages)

**Cell D3: % Scheduled**
```
=TEXT(B4/B7,"0%")
```
Scheduled events / Total events 2026. Formats as percentage.

**Cell D4: % Confirmed Interest**
```
=TEXT(B5/B7,"0%")
```
Confirmed Interest / Total events

**Cell D5: % Interested**
```
=TEXT(B6/B7,"0%")
```
Interested / Total events

**Cell D9: % Films with Intake**
```
=TEXT(B10/B9,"0%")
```
Films with intake / Total films

---

## Cross-Sheet Lookups (INDEX-MATCH)

### Find Venue Name from Venue_ID

Use this pattern to look up venue details from the Hosts sheet:

**Example: Get Venue Name for Event**
```
=INDEX(Hosts!B:B, MATCH(Events_2026!C2, Hosts!A:A, 0))
```
- `INDEX(Hosts!B:B, ...)` returns value from column B (Venue_Name)
- `MATCH(Events_2026!C2, Hosts!A:A, 0)` finds the row where Venue_ID matches
- `0` means exact match

**Example: Get Region for a Venue_ID**
```
=INDEX(Hosts!D:D, MATCH(A2, Hosts!A:A, 0))
```
Returns Region (column D) for the Venue_ID in cell A2

### Find Film Title from Film_ID

**Example: Get Film Title**
```
=INDEX(Films_2026!B:B, MATCH(Events_2026!E2, Films_2026!A:A, 0))
```
Looks up Film_Title (column B) by matching Film_ID (column A)

### Find Contact Info from Film_Contact Sheet

**Example: Get Filmmaker Email**
```
=INDEX(Film_Contacts!C:C, MATCH(A2, Film_Contacts!A:A, 0))
```
Returns Email (column C) for a given Film_ID in A2

---

## Filtered View Definitions

### 1. Ana Pipeline View

**Purpose:** Ana's main view — shows the pipeline funnel for 2026 events

**Source Sheet:** Events_2026

**Filters:**
- Pipeline_Status (column D): Show only "Scheduled", "Confirmed Interest", "Interested"
- Sort by: Pipeline_Status (A→Z), then Event_Date (oldest first)

**Visible Columns:**
- A: Event_ID
- B: Event_Name
- C: Venue_ID
- D: Pipeline_Status
- E: Film_ID
- F: Event_Date
- H: Team_Contact

**How to Create:**
1. Open Events_2026 sheet
2. Click **Data > Filter views > Create new filter view**
3. Name it: "Ana Pipeline View"
4. Click filter icon on column D (Pipeline_Status)
5. Uncheck "Blank", keep only: Scheduled, Confirmed Interest, Interested
6. Sort: Column D (A→Z), then Column F (A→Z)

---

### 2. Support Triage View (Action Needed)

**Purpose:** Shows only events/hosts needing attention

**Source Sheet:** Events_2026

**Filters:**
- Event_Date (column F): is empty **OR**
- Team_Contact (column H): is empty

**Sort by:** Pipeline_Status (Scheduled first)

**How to Create:**
1. Data > Filter views > Create new filter view
2. Name: "Support Triage — Action Needed"
3. Column F filter: Check "Blanks"
4. Column H filter: Check "Blanks"
5. **Note:** Google Sheets interprets multiple filters as AND, not OR. For OR logic, use a helper column:
   - Add column J: `=IF(OR(F2="", H2=""), "ACTION NEEDED", "")`
   - Filter column J: Show only "ACTION NEEDED"

---

### 3. Film Status View

**Purpose:** Shows which films have intake, contacts, captions

**Source Sheet:** Films_2026

**Join with:** Film_Contacts (manual reference — Google Sheets doesn't auto-join, so use VLOOKUP or side-by-side)

**Visible Columns:**
- A: Film_ID
- B: Film_Title
- C: Topics (comma-separated)
- E: Intake_Received (Y/N)
- Then refer to Film_Contacts sheet for:
  - Delivery_Format
  - Caption_Status

**How to Create:**
1. Open Films_2026 sheet
2. Data > Filter views > Create new filter view
3. Name: "Film Status — Ana Review"
4. No filters initially — show all films
5. Sort by: Intake_Received (N first, so missing intake shows at top)

**Pro Tip:** Create a second tab called "Film_Status_Combined" that uses VLOOKUP to merge Films_2026 + Film_Contacts into one view:
```
=VLOOKUP(A2, Film_Contacts!A:F, 6, FALSE)
```
This pulls Caption_Status (column 6) for each Film_ID.

---

### 4. Host Readiness View

**Purpose:** Cross-reference — which confirmed hosts have completed intake forms?

**Source Sheet:** Events_2026

**Filters:**
- Pipeline_Status (column D): "Scheduled" or "Confirmed Interest"

**Helper Column (add to Events_2026 if not present):**
- Column K: Intake_Status
  ```
  =IF(C2="", "No Venue Assigned", IF(COUNTIF(Host_Intake!B:B, C2) > 0, "Intake Complete", "Intake Missing"))
  ```
  - Checks if Venue_ID (C2) exists in Host_Intake sheet column B
  - Returns: "Intake Complete" or "Intake Missing"

**How to Create:**
1. Add formula to column K (Intake_Status)
2. Data > Filter views > Create new filter view
3. Name: "Host Readiness Check"
4. Filter column D: Scheduled, Confirmed Interest
5. Filter column K: Show only "Intake Missing"
6. Sort by Event_Date (oldest first) — these are urgent

---

### 5. Participants & Partners View

**Purpose:** Simple list views — who's been booked, who are our partners?

**Source Sheet:** Participants (for panelists/speakers)

**Filters:** None (show all)

**Sort by:** Event_ID (to group by event), then Name

**How to Create:**
1. Open Participants sheet
2. Data > Filter views > Create new filter view
3. Name: "All Participants by Event"
4. Sort: Column A (Event_ID), then Column B (Name)

**Source Sheet:** Partners (for sponsors/orgs)

**Filters:** None

**Sort by:** Partner_Type (e.g., Sponsor, Media Partner, Community Org)

---

## Named Ranges for Publishing

Named ranges let you publish specific data subsets as embeddable iframes.

### How to Create Named Ranges

1. Select the range (e.g., Dashboard_V2!A1:B22)
2. **Data > Named ranges**
3. Enter name (e.g., `pipeline_summary`)
4. Click **Done**

### Recommended Named Ranges

**1. pipeline_summary**
- Range: `Dashboard_V2!A1:B22`
- Contains: All dashboard metrics (hosts, events, films, action items)
- Use for: Docs site embed — quick numbers at a glance

**2. host_status_2026**
- Range: `Events_2026!A1:H100` (adjust row count as needed)
- Contains: Event pipeline with venue names, dates, status
- Use for: "Host Tracker" widget in docs site

**3. film_status_2026**
- Range: `Films_2026!A1:E20`
- Contains: Film titles, topics, intake status
- Use for: "Film Intake Tracker" widget

**4. action_items**
- Range: `Dashboard_V2!A18:B22`
- Contains: Just the "Action Items" section
- Use for: Inline badge/alert in docs site showing count of items needing attention

---

## Conditional Formatting Rules

### Action Items Warning (Cell B22)

**Purpose:** Highlight the total action items count if > 0

**Rule:**
1. Select cell B22
2. **Format > Conditional formatting**
3. Format rule: "Greater than"
4. Value: 0
5. Formatting style:
   - Background: #FFE5CC (pale amber — from OEFF Color_Legend)
   - Text: Bold, #9A5438 (warm-700)

---

## Troubleshooting

### Formula Returns #REF!

**Cause:** Sheet name doesn't match exactly (case-sensitive)

**Fix:** Check that sheet names in formulas match the actual tab names. Common issues:
- `Events_2026` vs `Events 2026` (underscore vs space)
- `Films_2026` vs `Films2026`

**Solution:** Use the sheet tab list to copy-paste the exact name into your formula.

---

### Formula Returns #N/A

**Cause:** MATCH or VLOOKUP can't find the value

**Fix:**
1. Check that lookup column (e.g., Venue_ID) has no extra spaces
2. Verify data types match (text vs number)
3. Use `IFERROR` to handle missing data gracefully:
   ```
   =IFERROR(INDEX(Hosts!B:B, MATCH(C2, Hosts!A:A, 0)), "Not Found")
   ```

---

### COUNTIF Returns 0 When Data Exists

**Cause:** Case mismatch or extra spaces

**Fix:** Use `TRIM` to remove spaces:
```
=COUNTIF(Events_2026!D2:D, "Scheduled")
```
If data has trailing spaces, wrap column reference:
```
=COUNTIF(ARRAYFORMULA(TRIM(Events_2026!D2:D)), "Scheduled")
```

---

### Percentages Show as Decimals

**Cause:** Cell format is "Number" instead of "Percentage"

**Fix:**
1. Select the cell (e.g., D3)
2. **Format > Number > Percent**

**Or use TEXT formula (already included above):**
```
=TEXT(B4/B7, "0%")
```
This forces percentage display even if cell format changes.

---

## Summary: Where Each Formula Goes

| Cell | Metric | Formula |
|------|--------|---------|
| B3 | Total Hosts | `=COUNTA(Hosts!A2:A)` |
| B4 | Scheduled | `=COUNTIF(Events_2026!D2:D,"Scheduled")` |
| B5 | Confirmed Interest | `=COUNTIF(Events_2026!D2:D,"Confirmed Interest")` |
| B6 | Interested | `=COUNTIF(Events_2026!D2:D,"Interested")` |
| B7 | Total Events | `=COUNTA(Events_2026!A2:A)` |
| B9 | Total Films | `=COUNTA(Films_2026!A2:A)` |
| B10 | Films with Intake | `=COUNTIF(Films_2026!E2:E,"Y")` |
| B11 | Films Missing Intake | `=COUNTIF(Films_2026!E2:E,"N")` |
| B12 | Films with Captions | `=COUNTIF(Film_Contacts!F2:F,"Complete")` |
| B14 | Intake Responses | `=COUNTA(Host_Intake!A2:A)` |
| B15 | Unmatched Intake | `=COUNTA(Ana_Matching!A2:A)` |
| B16 | Match Rate % | `=TEXT((B14-B15)/B14,"0%")` |
| B17 | Confirmed w/ Intake | `=COUNTIFS(Events_2026!D2:D,"Scheduled",Events_2026!C2:C,"<>")` |
| B19 | Events w/o Dates | `=COUNTIF(Events_2026!F2:F,"")` |
| B20 | Events w/o Contacts | `=COUNTIF(Events_2026!H2:H,"")` |
| B21 | Films Missing Intake | `=COUNTIF(Films_2026!E2:E,"N")` |
| B22 | **Total Action Items** | `=SUM(B19:B21)` ⚠️ |
| D3 | % Scheduled | `=TEXT(B4/B7,"0%")` |
| D4 | % Confirmed Interest | `=TEXT(B5/B7,"0%")` |
| D5 | % Interested | `=TEXT(B6/B7,"0%")` |
| D9 | % Films with Intake | `=TEXT(B10/B9,"0%")` |

⚠️ = Apply conditional formatting (yellow background if > 0)

---

## Next Steps (Phase 1 Implementation)

1. **Create Dashboard_V2 sheet** in V7 Google Sheets
2. **Copy-paste formulas** from table above into cells B3-D9
3. **Add labels** in column A (e.g., A3: "Total Hosts")
4. **Create filtered views** following specs above
5. **Define named ranges** for publishing
6. **Test:** Change a value in Events_2026 → verify dashboard updates

**Exit criteria:** Dashboard auto-calculates, at least 3 filtered views work, named ranges are ready to publish.

---

**Reference:** See `Google-Sheets-Quick-Start.md` for step-by-step screenshots and non-technical walkthrough.
