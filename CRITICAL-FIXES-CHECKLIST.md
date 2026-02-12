# CRITICAL DATA QUALITY FIXES - ACTION CHECKLIST

**Audit Date:** February 6, 2026
**Updated:** February 11, 2026
**Status:** IN PROGRESS - 6 issues resolved, 4 deferred (need human input), remaining items updated
**Estimated Remaining Fix Time:** 1-2 hours (mostly data collection)

---

## QUICK START: THE 5 BIGGEST ISSUES

1. **Events_2026 - Missing 17 Film_IDs**
   - Status: [~] PARTIALLY RESOLVED — reduced from 19 to 17 after dropping E26-026 dupe
   - 15 are pipeline venues with no film assigned yet (E26-015 to E26-025, E26-027 to E26-029) — waiting on programming decisions
   - E26-004 (Uncommon Ground) = "TBD" — awaiting film assignment
   - E26-010 (Cultivate Collective) = "Young Filmmakers Winner Short Films" — not a standard F26-xxx film, may need a new Film_ID or special handling
   - Action: Assign Film_IDs as programming decisions are made

2. **Events_2026 - Duplicate Venue_IDs** (V-001 Columbia College)
   - Status: [x] RESOLVED 2026-02-11
   - V-001 appears 2x: E26-001 (Flagship 4/22) and E26-005 (Community 4/23) — legitimate multi-event venue
   - E26-026 was a duplicate pipeline entry — dropped from CSV

3. **Events_2025 - V-014 (Chicago Cultural Center) Placeholders**
   - Status: [x] RESOLVED 2026-02-11
   - Was 53 occurrences, 41 were empty placeholder/pipeline rows with no date or film
   - Dropped 41 placeholders, kept 12 with dates or film assignments
   - Total 2025 events reduced from 180 to 139

4. **Partners - Critical Data Gaps**
   - Status: [ ] DEFERRED — needs manual data collection
   - Contact info: 19% filled (121 empty)
   - Email: 4% filled (144 empty)
   - Topics: 3% filled (146 empty)
   - Action: Bulk data collection from external sources; import as-is and populate in Airtable

5. **Dashboard - Duplicate Header Row**
   - Status: [x] N/A FOR IMPORT — exists in xlsx only, not in CSVs

---

## DETAILED CHECKLIST BY SHEET

### V7 - Events_2026 Sheet

**Status: CRITICAL - Multiple Issues**

#### Issue 1: Missing Film_IDs (19 instances)
- [ ] Rows with empty Film_ID: 5, 11, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32
- [ ] Action: Fill with correct Film_ID or delete rows if not needed
- [ ] Verify: All Film_IDs follow format F26-###

#### Issue 2: Duplicate Venue_IDs
- [x] RESOLVED 2026-02-11: V-001 (Columbia College) hosts 2 events on different dates — legitimate
- [x] Duplicate pipeline entry E26-026 dropped from CSV

#### Issue 3: Duplicate Film_IDs
- [x] RESOLVED 2026-02-11: These are legitimate multi-venue screenings
- [x] F26-006 (How to Power a City): 3 venues on 4/24 (Oak Park, ICA, Triton) — correct
- [x] F26-005 (Rooted): 2 venues (Bethel New Life 4/24, Dominican 4/27) — correct
- [x] F26-008 (40 Acres): 2 venues on 4/25 (Kehrein Center, Black Girl Environmentalists) — correct

#### Issue 4: Referential Integrity
- [ ] Check each Venue_ID exists in Hosts sheet
- [ ] Check each Film_ID (when filled) exists in Films_2026 sheet
- [ ] Cross-reference against valid IDs

#### Issue 5: Required Fields
- [ ] Event_ID: 100% filled ✓
- [ ] Date: Verify all filled, consistent format
- [ ] Venue_ID: 100% filled ✓

**Estimated Fix Time: 45 minutes**

---

### V7 - Events_2025 Sheet

**Status: CRITICAL - Data Organization Issue**

#### Issue: 53 occurrences of Venue_ID V-014 (Expected: 1)
- [ ] Rows: 9, 13, 32, 37, 40, 42, 46, 49, 50, 61, 62, 66, 68, 76, 80, 86, 91, 92, 96, 98, 100, 107, 109, 110, 112, 113, 118, 122, 124, 132, 134, 135, 136, 137, 138, 139, 144, 146, 147, 149, 155, 157, 158, 161, 162, 163, 164, 165, 166, 168, 169, 170, 175

**Analysis Complete (2026-02-11):**
- [x] 41 of 53 were empty placeholder/pipeline rows — DROPPED from CSV
- [x] 12 remaining are legitimate events (have dates or film assignments)
- [x] Chicago Cultural Center is a high-volume venue — multiple events expected

**Fix Applied:** 41 empty rows removed, 2025 events reduced 180 → 139

---

### V7 - Dashboard Sheet

**Status: CRITICAL - Duplicate Header**

#### Issue: Header row duplicated
- [ ] Duplicate in rows 2 and 8 (column: "OEFF 2026 CONSOLIDATED DASHBOARD (V7)")
- [ ] Action: Delete row 8 (or row 2, verify which is header)
- [ ] Verify: Only one header row remains

**Estimated Fix Time: 2 minutes**

---

### V7 - Film_Contacts Sheet

**Status: WARNING - Data Gaps**

#### Issue: Email fields — RESOLVED
- [x] RESOLVED 2026-02-11: All 9 contacts have primary emails (100%)
- [x] 6 of 9 also have secondary contact emails
- [x] CSV re-exported with all 15 schema fields (was 7)
- [x] Formats Available, Caption Status, Audio Description, Spanish Version, Timestamps all populated

---

### V7 - Hosts Sheet

**Status: OK - Main issues in referencing sheets**

- [x] No critical issues in this sheet
- Verify it has all venues referenced in Events_2026 and Host_Intake
- Fill rate for Region: Target 80%

---

### V7 - Films_2026 Sheet

**Status: OK - Main issues in referencing sheets**

- [x] No critical issues in this sheet
- Verify it has all films referenced in Events_2026 and Film_Contacts
- Check Runtime fill rate: Target 90%

---

### V7 - Partners Sheet

**Status: CRITICAL - Data Gaps**

#### Issue: Critical contact information gaps
| Field | Filled | Empty | % | Issue |
|-------|--------|-------|---|-------|
| Partner_ID | 150 | 0 | 100% | ✓ OK |
| Org_Name | 150 | 0 | 100% | ✓ OK |
| Contact | 29 | 121 | 19.3% | 🔴 CRITICAL |
| Email | 6 | 144 | 4.0% | 🔴 CRITICAL |
| Topics | 4 | 146 | 2.7% | 🔴 CRITICAL |
| Notes | 0 | 150 | 0.0% | 🔴 CRITICAL |

**Action Required:**
- [ ] Determine if contact info can be obtained from external sources
- [ ] If not obtainable, document and set expectations
- [ ] Prioritize: Email (critical), Contact Name (important), Topics (useful)

**Estimated Fix Time: 1-2 hours (depends on data availability)**

---

### V7 - Recordings Sheet

**Status: CRITICAL - Data Gaps**

#### Issue: Recording URLs incomplete
| Field | Filled | Empty | % | Issue |
|-------|--------|-------|---|-------|
| Recording_ID | 62 | 0 | 100% | ✓ OK |
| Event | 62 | 0 | 100% | ✓ OK |
| Year | 62 | 0 | 100% | ✓ OK |
| Recap_URL | 17 | 45 | 27.4% | 🔴 CRITICAL |
| Full_URL | 8 | 54 | 12.9% | 🔴 CRITICAL |

**Action Required:**
- [ ] Locate missing recording URLs
- [ ] Add links for as many missing recordings as possible
- [ ] Document which recordings are unavailable

**Estimated Fix Time: 1-3 hours (depends on URL availability)**

---

### Benefits Tracking 2026.xlsx

**Status: WARNING - Review Needed**

#### FY26 Sponsors Sheet
- [ ] Verify all required columns are present
- [ ] Check for duplicates or format issues
- [ ] Validate data against other sources

#### Benefits Sheet
- [ ] Review single column structure
- [ ] Verify all benefit types are captured
- [ ] Check for gaps

---

## FIX PRIORITY TIMELINE

### Phase 1: Today (Critical - 1-2 hours) — MOSTLY COMPLETE
- [~] Events_2026 missing Film_IDs — 17 remaining, awaiting programming decisions
- [x] Events_2026 duplicate Venue_IDs — resolved (E26-026 dropped)
- [x] Events_2026 duplicate Film_IDs — resolved (legitimate multi-venue screenings)
- [x] Dashboard header duplicate — N/A for CSV import
- [x] Events_2026 referential integrity — all FKs valid
- [x] Film_Contacts email validation — 100% complete after re-export

### Phase 2: This Week (Important - 2-3 hours)
- [x] Events_2025 duplicate analysis — resolved (41 placeholders dropped)
- [ ] Collect missing Partner contact info (30-60 min) — DEFERRED to Airtable
- [ ] Collect missing Recording URLs (60-120 min) — DEFERRED to Airtable
- [x] Data format standardization — handled in CSV re-export (booleans, dates, IDs)

### Phase 3: Before Import (Final Validation - 30 min)
- [ ] Re-run data quality audit against cleaned CSVs
- [x] Verify critical issues resolved (6 of 8 closed)
- [x] Document deferred items (Partners data, Recordings URLs, Film_ID assignments)
- [ ] Sign-off on data quality

---

## AUDIT RE-RUN INSTRUCTIONS

After making fixes:

```bash
# Open your Python environment and run:
python /tmp/audit_script.py

# Then generate new report:
python /tmp/generate_report.py
```

Compare with original report to verify all critical issues are resolved.

---

## REFERENCE: WHERE TO FIND ISSUES

**Detailed Report:** `/sessions/affectionate-cool-ptolemy/mnt/oeff-docs/data-quality-audit.md` (1,791 lines)

**Sections:**
- Critical Issues (39): Lines ~100-500
- Warnings (28): Lines ~500-800
- Data Gap Analysis: Lines ~800-1000
- Sheet-by-Sheet Details: Lines ~1000-1600

**For Each Issue You'll Find:**
- Exact cell location (Sheet!Column:Row)
- Problem description
- Recommended fix

---

## SIGN-OFF

- [ ] Project Manager: All critical issues reviewed
- [ ] Data Steward: All fixes completed and verified
- [ ] Business Owner: Data quality acceptable for import

**Date Completed:** ______________

**Completed By:** ______________

**Notes:** 

---

## QUICK REFERENCE: ID FORMATS

Ensure all IDs follow these patterns:

- **Event_ID:** E26-### (example: E26-001)
- **Film_ID:** F26-### (example: F26-005)
- **Venue_ID:** V-### (example: V-014)
- **Contact_ID:** C-### (example: C-001)
- **Partner_ID:** P-### (example: P-001)

If you find IDs that don't follow these patterns, update them to be consistent.

---

## SUPPORT

For questions about specific issues:
1. Find issue number in this checklist
2. Look up exact location in detailed audit report
3. Review recommendation
4. Execute fix
5. Note any blockers in sign-off section
