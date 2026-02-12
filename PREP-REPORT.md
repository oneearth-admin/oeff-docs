# OEFF Data Viz — Phase 1 Prep Report

> **Date:** 2026-02-08
> **Scope:** Verify all Phase 1 deliverables before implementation in live V7 Google Sheet

---

## 1. Formula Reference (`formula-reference.md`)

### Summary

- **Total formulas documented:** 24 (cells B3–B22, D3–D9)
- **Formula types used:** COUNTA (4), COUNTIF (8), COUNTIFS (1), SUM (1), TEXT (4), INDEX-MATCH (4 examples), VLOOKUP (1 example), IF+OR (1 helper)
- **All formulas use valid Google Sheets syntax:** Yes

### Verified Formulas (20 of 24)

All 24 dashboard formulas use correct Google Sheets syntax. COUNTA, COUNTIF, COUNTIFS, SUM, and TEXT are native to Google Sheets. INDEX-MATCH and VLOOKUP examples also use correct syntax with the `0` exact-match parameter.

No Excel-only syntax was found (no XLOOKUP, FILTER with array spill, or structured table references).

### Items Requiring Manual Verification (4)

These formulas are syntactically correct but reference sheet names and column positions that must be confirmed against the actual V7 sheet:

| Formula | Sheet Referenced | What to Verify | Status |
|---------|-----------------|----------------|--------|
| `=COUNTIF(Film_Contacts!F2:F,"Complete")` (B12) | Film_Contacts | Column F is actually Caption_Status (not another column) | [NEEDS VERIFICATION] |
| `=COUNTA(Host_Intake!A2:A)` (B14) | Host_Intake | Column A is Venue_Name (doc says this); confirm sheet exists with this name | [NEEDS VERIFICATION] |
| `=COUNTA(Ana_Matching!A2:A)` (B15) | Ana_Matching | This sheet is assumed to exist; confirm exact name | [NEEDS VERIFICATION] |
| `=COUNTIF(Host_Intake!B:B, C2)` (K2 helper) | Host_Intake | Column B is Venue_ID for lookup; confirm this column assignment | [NEEDS VERIFICATION] |

### Sheet Names Referenced

The formulas reference 6 source sheets. All must exist with **exact** names (case-sensitive, underscores):

1. **Hosts** — referenced in B3, and all INDEX-MATCH venue lookups
2. **Events_2026** — referenced in B4, B5, B6, B7, B17, B19, B20, and filtered views
3. **Films_2026** — referenced in B9, B10, B11, and INDEX-MATCH film lookups
4. **Film_Contacts** — referenced in B12, and VLOOKUP example
5. **Host_Intake** — referenced in B14, and K2 helper formula
6. **Ana_Matching** — referenced in B15

**Risk:** If any sheet uses spaces instead of underscores (e.g., "Events 2026" vs "Events_2026"), all formulas referencing that sheet will return `#REF!`. The troubleshooting section correctly documents this risk.

### Column Assignment Assumptions

The following column-to-header mappings are assumed throughout and should be verified against V7:

| Sheet | Column | Assumed Header |
|-------|--------|----------------|
| Events_2026 | A | Event_ID |
| Events_2026 | C | Venue_ID |
| Events_2026 | D | Pipeline_Status |
| Events_2026 | E | Film_ID |
| Events_2026 | F | Event_Date |
| Events_2026 | H | Team_Contact |
| Films_2026 | A | Film_ID |
| Films_2026 | B | Film_Title |
| Films_2026 | E | Intake_Received |
| Film_Contacts | A | Film_ID |
| Film_Contacts | C | Email |
| Film_Contacts | F | Caption_Status |
| Hosts | A | Venue_ID |
| Hosts | B | Venue_Name |
| Hosts | D | Region |

### Additional Notes

- B16 (`=TEXT((B14-B15)/B14,"0%")`) will return `#DIV/0!` if B14 is 0 (no intake responses). Consider wrapping: `=IF(B14=0,"—",TEXT((B14-B15)/B14,"0%"))`
- B21 is intentionally a duplicate of B11 (Films Missing Intake) — this is noted in the doc and is correct for the "Action Items" section
- The COUNTIF for empty cells (`=COUNTIF(Events_2026!F2:F,"")`) works in Google Sheets — verified syntax
- COUNTIFS with `"<>"` for non-empty (B17) is valid Google Sheets syntax

### Formula Verdict

**20 verified, 4 need manual confirmation against V7 sheet structure.** Syntax is uniformly correct for Google Sheets. No Excel-only functions detected.

---

## 2. Widget HTML Quality (`dashboard-widgets/host-tracker.html`)

### Rendering

**Would this render properly?** Yes.

- Valid HTML5 document with `<!DOCTYPE html>`, `<html lang="en">`, proper head/body structure
- All CSS is inline (single-file, no external dependencies beyond Google Fonts)
- JavaScript is inline and self-contained — no external JS libraries
- `init()` is called at script end, which correctly populates the table on load
- All DOM element IDs referenced in JS (`search`, `table-body`, `stat-total`, etc.) exist in the HTML
- Google Fonts link loads Fraunces, Source Sans 3, and Source Serif 4 (matches canonical typography)
- Responsive breakpoint at 768px handles mobile layout correctly

**Minor rendering note:** The `data-domain="oeff"` attribute on `<html>` is not used by any CSS rules in this file. It's a correct convention for future domain-switching but currently inert.

### Accessibility

**ARIA labels present:**

| Element | ARIA Attribute | Value |
|---------|---------------|-------|
| Search input | `aria-label` | "Search venues by name, region, or contact" |
| Filter pills container | `role="group"`, `aria-label` | "Filter by pipeline status" |
| Each filter pill | `aria-pressed` | "true" / "false" (toggled by JS) |
| Data table | `role="table"`, `aria-label` | "Host venue pipeline tracker" |
| Column headers | `role="columnheader"`, `aria-sort` | "none" / "ascending" / "descending" (updated by JS) |
| Status badges | `role="status"` | On each badge span |
| Table rows | `tabindex="0"` | Keyboard-focusable rows |
| `.sr-only` class | defined | Screen-reader-only utility class is present |

**Keyboard accessibility:**
- Filter pills respond to Enter and Space keys (explicit keydown handler)
- Table headers respond to Enter and Space keys (explicit keydown handler)
- Search input is natively keyboard-accessible
- `tabindex="0"` on table rows enables keyboard navigation

**Accessibility gaps:**

1. **Live region missing:** When search/filter results update, screen readers won't announce the change. Should add `aria-live="polite"` to the table container or a results summary element.
2. **Sort indicator announcement:** `aria-sort` updates correctly on headers, but the sort arrow characters (`⇅`, `↑`, `↓`) are CSS pseudo-elements — screen readers may or may not read these depending on the browser. The `aria-sort` attribute is the correct mechanism regardless.
3. **Empty state not announced:** The "No venues match" message appears via innerHTML replacement but has no `role="alert"` to announce to screen readers.

### Color Contrast (WCAG AA)

| Element | Foreground | Background | Contrast Ratio | Pass? |
|---------|-----------|------------|----------------|-------|
| Body text (`--color-ink: #2c2825`) | #2c2825 | #f7f5f2 | ~12.5:1 | Yes (AAA) |
| Soft text (`--color-ink-soft: #5c5550`) | #5c5550 | #f7f5f2 | ~5.7:1 | Yes (AA) |
| Muted text (`--color-ink-muted: #8a8580`) | #8a8580 | #f7f5f2 | ~3.3:1 | **Borderline** |
| Badge: Scheduled (green) | #5c8c4b on #e8f5e8 | — | ~4.0:1 | Yes (AA for large text) |
| Badge: Confirmed (amber) | #996622 on #fff5e6 | — | ~5.3:1 | Yes (AA) |
| Badge: Interested (teal) | #4b7c8c on #e6f3f7 | — | ~4.5:1 | Yes (AA) |
| Badge: Exploring (gray) | #8a8580 on #f0ede8 | — | ~3.1:1 | **Marginal** |
| Active filter pill (white on sage) | #fff on #5c7c6b | — | ~4.1:1 | Yes (AA for large text) |

**Contrast concerns:**
- `--color-ink-muted` (#8a8580) on cream backgrounds is borderline at ~3.3:1. Used for the "Exploring" badge and stat labels. Not a failure for large text (14px bold+), but the stat labels at 0.875rem may fall below AA for normal text.
- The "Exploring" badge specifically uses muted ink on linen — this is the weakest contrast in the file.

### Mock Data Quality

**Realistic?** Yes — well-crafted.

- **100 venues** total: 15 Scheduled, 20 Confirmed Interest, 35 Interested, 30 Exploring (realistic funnel distribution)
- Venue names are plausible Chicago-area locations (neighborhoods, suburbs, venue types)
- **5 regions:** Central, North, South, West, Suburbs — evenly distributed
- **4 team contacts:** Ana Martinez, Taylor Brooks, Jordan Lee, Casey Smith
- Scheduled venues have dates (April 22-26, 2026) — realistic festival window
- Confirmed Interest/Interested/Exploring venues correctly have empty dates
- Interested and Exploring venues correctly have empty contacts
- Date format is ISO 8601 (`2026-04-22`), displayed via `toLocaleDateString('en-US')` — correct

**One data modeling note:** The mock uses "Confirmed Interest" as a status value, but the filter pill displays "Confirmed" as the label. The `data-status` attribute correctly matches "Confirmed Interest", so filtering works — the label is just a shorter display name. This could briefly confuse a user.

### Design System Compliance

- Uses semantic tokens throughout (`--color-primary`, not `--forest-sage` directly) — **correct**
- Warm-tinted shadows (`hsla(30, 20%, 20%, 0.08)`) — **correct**, no pure black
- Border radius minimum 8px — **correct** (uses 8px and 12px)
- Font stack matches canonical: Fraunces, Source Serif 4, Source Sans 3 — **correct**
- No IBM Plex Mono — **correct**
- No emojis in UI elements — **two emojis found** in the data notice section (line 476-477: `📊` and `🔗`). These are in an informational footer, not core UI. Minor violation of the no-emojis-in-UI rule.
- 12px font floor — the smallest font is 0.75rem (12px) for the sort arrow pseudo-element, and 0.8rem (12.8px) for badges. **Passes.**
- 44px touch targets — filter pills have padding `0.5rem 1rem` plus 2px border. At default font size, this yields roughly 36px height. **Below the 44px minimum** on small viewports. Table header cells are similarly compact.

### Widget Verdict

**Renders correctly, strong accessibility foundation, good mock data.** Three items to address: (1) add `aria-live` region for dynamic content updates, (2) bump filter pill padding to meet 44px touch target, (3) verify "Exploring" badge contrast is acceptable for the context.

---

## 3. Integration Guide Readability (`integration-guide.md`)

### Readability Score: **4 out of 5**

### What Works Well

- **Clear audience targeting:** Opens with "For Ana and Support Staff" — immediately sets expectations
- **Phase structure:** Logical progression (Formulas → Filtered Views → Named Ranges → Embed → Auto-Refresh)
- **Step numbering is sequential and correct:** No missing or out-of-order steps
- **Menu paths are accurate:** "Data > Filter views > Create new filter view", "Format > Conditional formatting", "File > Share > Publish to web" — all correct for Google Sheets
- **Troubleshooting section is excellent:** 5 common problems with clear cause/fix pairs
- **Time estimate given upfront:** "30-45 minutes for initial setup" — helpful for planning
- **Summary table at the end** maps widgets to docs site locations — very practical
- **Support contacts listed** with clear role distinction (Garen for tech, Ana for workflow)

### Issues Found

**Issue 1: Prerequisite gap (Minor)**
The prerequisites list "Edit access to the OEFF docs site repository (GitHub)" — but Phase 1 (adding formulas to V7) doesn't require GitHub access at all. This could intimidate Ana or support staff. Recommend splitting prerequisites by phase: Phase 1-2 need only Google Sheets access; Phase 4 needs GitHub.

**Issue 2: "Right-click > Open with Google Sheets" path (Minor)**
Step 1.1 says "Right-click → Open with Google Sheets" in Google Drive. This works in Drive's web interface, but the state file notes "V7 already in Google Sheets" and "No migration needed." If V7 is already a Google Sheet, the Excel migration instructions (steps 1-3 under "If V7 is still in Excel format") may cause confusion. Consider adding: "If V7 already opens as a Google Sheet, skip to Step 1.2."

**Issue 3: Named range publishing dropdown (Medium)**
Step 3.2 says to change the dropdown from "Entire document" to the range name. In current Google Sheets (2026), the "Publish to web" dialog uses a dropdown for **sheets**, not named ranges directly. Named ranges don't appear in this dropdown — you select the **sheet** and optionally specify a cell range in the URL parameters. This step may not work as written.

[NEEDS VERIFICATION] — confirm whether Google Sheets' "Publish to web" dialog in 2026 supports selecting named ranges directly, or if the URL must be manually constructed.

**Issue 4: Placeholder URLs (Expected but should be flagged)**
Several `YOUR_..._HERE` placeholders appear in Phase 4 HTML snippets. These are intentionally placeholder — but a non-technical user might not realize they need to be replaced even after reading the instructions. Each placeholder is explained in a "What to replace" callout, which is good. No action needed.

**Issue 5: CSS code in a non-technical guide (Minor)**
Step 4.2 asks the user to add CSS code to a stylesheet. The guide is labeled "For Ana and Support Staff — no coding required" but Phase 4 requires editing HTML and CSS files. The "no coding required" claim applies to Phase 1-3 only. Consider adding a note: "Phases 4-5 require editing HTML/CSS files. Ask Garen for help if needed."

**Issue 6: Beautiful-First design system link (Minor)**
The "Useful Resources" section links to `~/.claude/skills/beautiful-first-design/` which is a local Claude development path, not a URL Ana could visit. This should either be removed or replaced with a relevant public resource.

**Issue 7: The guide mentions a file that doesn't exist**
Step 1.4 references "See `formula-reference.md` for detailed explanations" — this file exists and is correct. But the bottom of formula-reference.md references "See `Google-Sheets-Quick-Start.md` for step-by-step screenshots" — this file is referenced in the state JSON as a deliverable but was not found in the directory listing. Either it hasn't been created yet or it's stored elsewhere.

[NEEDS VERIFICATION] — locate or create `Google-Sheets-Quick-Start.md`.

### Step Ordering

All steps within each phase are correctly ordered. Phase dependencies are also correct:
- Phase 1 (formulas) is independent
- Phase 2 (filtered views) requires Phase 1 sheet names to exist
- Phase 3 (named ranges) requires Phase 1 data to exist
- Phase 4 (embedding) requires Phase 3 published URLs
- Phase 5 (auto-refresh) requires Phase 4 embeds to exist

No circular dependencies. No steps that should be reordered.

### Assumptions Made

1. V7 is already in Google Sheets format (confirmed by state JSON)
2. Sheet names use underscores (`Events_2026`, not `Events 2026`) — not yet verified
3. Ana has edit access to V7 — reasonable assumption given she's ED
4. Docs site is on GitHub + Cloudflare Pages — mentioned but alternative manual deploy is also documented
5. Film_Contacts has 6+ columns (VLOOKUP references column 6) — [NEEDS VERIFICATION]

---

## 4. Items Requiring Manual Verification (When V7 is Open)

These cannot be checked without opening the actual V7 Google Sheet:

| # | Item | Where | What to Check |
|---|------|-------|---------------|
| 1 | Sheet names | V7 tab list | Exact names: `Hosts`, `Events_2026`, `Films_2026`, `Film_Contacts`, `Host_Intake`, `Ana_Matching` |
| 2 | Column assignments | All 6 sheets | Verify the 15 column-to-header mappings listed in Section 1 above |
| 3 | Film_Contacts column count | Film_Contacts sheet | Confirm at least 6 columns (VLOOKUP references column 6) |
| 4 | Pipeline_Status values | Events_2026 column D | Exact values: "Scheduled", "Confirmed Interest", "Interested" (case-sensitive) |
| 5 | Intake_Received values | Films_2026 column E | Exact values: "Y" and "N" |
| 6 | Caption_Status values | Film_Contacts column F | Exact value: "Complete" |
| 7 | Host_Intake column B | Host_Intake sheet | Confirm column B contains Venue_ID (used in K2 helper lookup) |
| 8 | Ana_Matching sheet exists | V7 tab list | This sheet may have a different name or not exist yet |
| 9 | Named range publishing | Google Sheets UI | Confirm "Publish to web" supports named range selection in current Google Sheets |
| 10 | Google-Sheets-Quick-Start.md | Project files | Locate or create this referenced file |

---

## 5. Recommended Next Steps for Phase 2

Based on the state file (`OEFF-DATA-VIZ-state-UPDATED.json`), Phase 1 status is "implementation_ready" and Phase 2 is "ready_to_start." Here's the recommended sequence:

### Immediate (Before Phase 2)

1. **Open V7 in Google Sheets** and verify all 10 items in Section 4 above. Record exact sheet names and column positions. Update `formula-reference.md` if any column letters differ.

2. **Create Dashboard_V2 sheet** in V7 and paste all 24 formulas. Test by changing one Pipeline_Status value and confirming the count updates.

3. **Create at least 2 filtered views** (Ana Pipeline View + Support Triage). Confirm the filter mechanics work as documented.

4. **Wrap B16 in IFERROR** — the match rate formula will break if no intake responses exist:
   ```
   =IF(B14=0,"—",TEXT((B14-B15)/B14,"0%"))
   ```

### Phase 2: Docs Site Integration

5. **Publish named ranges** from V7. Test each published URL in an incognito window to confirm public access.

6. **Test iframe embedding** — before editing the docs site, create a minimal test HTML file locally that loads one published range in an iframe. Confirm no CSP or CORS issues.

7. **Update `host-tracker.html`:**
   - Add `aria-live="polite"` to the table container for screen reader announcements
   - Increase filter pill vertical padding to meet 44px touch target minimum
   - Remove emojis from the data notice section (lines 476-477)
   - When ready for live data: uncomment the fetch section and insert the published CSV URL

8. **Locate or create `Google-Sheets-Quick-Start.md`** — referenced by `formula-reference.md` but not present in the project directory.

9. **Embed widgets in docs site** following integration-guide.md Phase 4. Start with the host pipeline embed (most valuable to Ana's workflow).

10. **Add a Phase 2 note to the integration guide** clarifying that Phases 1-3 require no coding, while Phase 4+ requires HTML editing (or Garen's help).

### Phase 3 (Future)

Per the state file, Phase 3 includes geographic map, pipeline funnel chart, year-over-year comparison, and weekly digest email. These are correctly scoped as future work and should not block Phase 2 deployment.

---

## Summary

| Deliverable | Status | Score |
|-------------|--------|-------|
| Formula Reference | 20/24 verified, 4 need V7 confirmation | Syntax: Pass |
| Host Tracker Widget | Renders correctly, strong a11y, minor contrast + touch target issues | Quality: 4/5 |
| Integration Guide | Clear, well-ordered, a few assumptions to flag for non-technical users | Readability: 4/5 |

**Overall assessment:** Phase 1 prep work is solid and implementation-ready. The main gate is verifying sheet names and column positions against the live V7 file. Once those 10 manual checks pass, formulas can be pasted directly and the dashboard will work.

---

*Generated 2026-02-08 by prep verification pass*
