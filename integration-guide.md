# OEFF Data Visualization Integration Guide

> **For Ana and Support Staff**
> Step-by-step instructions to connect V7 Google Sheets data to the OEFF docs site — no coding required.

---

## Overview

This guide shows you how to:
1. Add auto-calculating formulas to V7's Dashboard sheet
2. Create filtered views for different workflows (pipeline, film status, action items)
3. Publish data ranges from Google Sheets
4. Embed live data widgets into the OEFF docs site

**Time estimate:** 30-45 minutes for initial setup, then 5 minutes per widget embed

**Prerequisites:**

*Phases 1-3 (Google Sheets only):*
- Edit access to the V7 Google Sheet
- Basic familiarity with Google Sheets (filtering, copy-paste formulas)

*Phases 4-5 (docs site integration — ask Garen for help if needed):*
- Edit access to the OEFF docs site repository (GitHub)
- Ability to edit HTML and CSS files

---

## Phase 1: Add Formulas to V7 Dashboard

### Step 1.1: Open V7 in Google Sheets

If V7 already opens as a Google Sheet (not an .xlsx file), skip to **Step 1.2**.

1. Go to **Google Drive** → locate **V7 spreadsheet**
2. Right-click → **Open with Google Sheets**
3. **Important:** Do NOT use the Excel file. Google Sheets formulas and publishing features only work in Google Sheets format.

If V7 is still in Excel format:
1. Upload `V7.xlsx` to Google Drive
2. Right-click → **Open with Google Sheets**
3. File → **Save as Google Sheets**

---

### Step 1.2: Create Dashboard_V2 Sheet

1. At the bottom of V7, click **+** (add new sheet)
2. Name it: **Dashboard_V2**
3. This will replace the old static Dashboard with auto-calculating formulas

---

### Step 1.3: Add Column Headers

In **Dashboard_V2**, add these labels:

| Cell | Label |
|------|-------|
| A1 | **OEFF 2026 Dashboard** |
| A3 | Total Hosts |
| A4 | Events - Scheduled |
| A5 | Events - Confirmed Interest |
| A6 | Events - Interested |
| A7 | Total Events 2026 |
| A9 | Total Films |
| A10 | Films with Intake |
| A11 | Films Missing Intake |
| A12 | Films with Captions |
| A14 | Total Intake Responses |
| A15 | Unmatched Intake Forms |
| A16 | Intake Match Rate |
| A17 | Confirmed Hosts with Intake |
| A19 | Events Without Dates |
| A20 | Events Without Contacts |
| A21 | Films Missing Intake |
| A22 | **Total Action Items** |

Make A1 bold, larger font (18pt). Make A22 bold.

---

### Step 1.4: Copy-Paste Formulas

**Reference:** See `formula-reference.md` for detailed explanations of each formula.

Copy the formulas below into the corresponding cells in column B:

| Cell | Formula | What it does |
|------|---------|--------------|
| B3 | `=COUNTA(Hosts!A2:A)` | Counts total hosts |
| B4 | `=COUNTIF(Events_2026!D2:D,"Scheduled")` | Counts scheduled events |
| B5 | `=COUNTIF(Events_2026!D2:D,"Confirmed Interest")` | Counts confirmed interest events |
| B6 | `=COUNTIF(Events_2026!D2:D,"Interested")` | Counts interested events |
| B7 | `=COUNTA(Events_2026!A2:A)` | Counts total events |
| B9 | `=COUNTA(Films_2026!A2:A)` | Counts total films |
| B10 | `=COUNTIF(Films_2026!E2:E,"Y")` | Counts films with intake |
| B11 | `=COUNTIF(Films_2026!E2:E,"N")` | Counts films missing intake |
| B12 | `=COUNTIF(Film_Contacts!F2:F,"Complete")` | Counts films with captions |
| B14 | `=COUNTA(Host_Intake!A2:A)` | Counts intake responses |
| B15 | `=COUNTA(Ana_Matching!A2:A)` | Counts unmatched intake forms |
| B16 | `=TEXT((B14-B15)/B14,"0%")` | Calculates match rate % |
| B17 | `=COUNTIFS(Events_2026!D2:D,"Scheduled",Events_2026!C2:C,"<>")` | Counts confirmed events with venue IDs |
| B19 | `=COUNTIF(Events_2026!F2:F,"")` | Counts events missing dates |
| B20 | `=COUNTIF(Events_2026!H2:H,"")` | Counts events missing contacts |
| B21 | `=COUNTIF(Films_2026!E2:E,"N")` | Repeats films missing intake |
| B22 | `=SUM(B19:B21)` | **Total action items** |

**How to copy-paste:**
1. Click on cell B3
2. Paste: `=COUNTA(Hosts!A2:A)`
3. Press **Enter**
4. Repeat for each cell

**Troubleshooting:**
- If you see `#REF!` error: Sheet name is misspelled. Check exact sheet names (case-sensitive, underscores vs spaces).
- If you see `#N/A` error: Data doesn't exist in the referenced sheet. Verify column letters match your sheets.
- If percentages show as decimals: Select cell → **Format** → **Number** → **Percent**

---

### Step 1.5: Add Conditional Formatting to Action Items

Highlight cell B22 (Total Action Items) in **yellow** when > 0:

1. Select cell **B22**
2. **Format** → **Conditional formatting**
3. Under "Format rules":
   - Format cells if: **Greater than**
   - Value: `0`
4. Formatting style:
   - Background color: `#FFE5CC` (pale amber)
   - Text color: Bold, `#9A5438` (dark brown)
5. Click **Done**

Now B22 will turn yellow whenever there are action items needing attention.

---

### Step 1.6: Test the Dashboard

1. Go to **Events_2026** sheet
2. Change one event's **Pipeline_Status** to "Scheduled"
3. Go back to **Dashboard_V2** → verify that **B4** (Events - Scheduled) increased by 1

If the number updates automatically, ✅ formulas are working!

---

## Phase 2: Create Filtered Views

Filtered views let you see subsets of data without changing the underlying sheet. Multiple people can use different filtered views at the same time.

---

### View 1: Ana Pipeline View

**Purpose:** Ana's main view — shows only active pipeline events (Scheduled, Confirmed Interest, Interested)

**Steps:**
1. Go to **Events_2026** sheet
2. Click **Data** → **Filter views** → **Create new filter view**
3. Name it: **Ana Pipeline View**
4. Click the filter icon (▼) on column **D** (Pipeline_Status)
5. **Uncheck**: "Blank", "Exploring" (if present)
6. **Keep checked**: "Scheduled", "Confirmed Interest", "Interested"
7. Click **OK**
8. Click **Sort** icon on column **D** → **Sort A → Z**
9. Then **Sort** icon on column **F** (Event_Date) → **Sort A → Z**
10. Click **Save** (top right of filter view bar)

**Share link:**
- Click the **link icon** in the filter view bar
- Copy the URL → share with team members

---

### View 2: Support Triage View (Action Needed)

**Purpose:** Shows events needing attention (missing dates or contacts)

**Challenge:** Google Sheets filters use AND logic, not OR. To show events missing dates **OR** contacts, we need a helper column.

**Steps:**

**Part A: Add Helper Column**
1. Go to **Events_2026** sheet
2. Click column **J** header (or first empty column)
3. In **J1**, type: **Action Needed**
4. In **J2**, paste:
   ```
   =IF(OR(F2="", H2=""), "ACTION NEEDED", "")
   ```
   - This checks if Event_Date (F2) or Team_Contact (H2) is empty
5. Drag the formula down to all rows (click J2 → drag blue handle down)

**Part B: Create Filtered View**
1. **Data** → **Filter views** → **Create new filter view**
2. Name it: **Support Triage — Action Needed**
3. Click filter icon on column **J** (Action Needed)
4. **Uncheck**: "Blanks"
5. **Keep checked**: "ACTION NEEDED"
6. Click **OK**
7. Sort by column **D** (Pipeline_Status) → **Sort A → Z** (so Scheduled events show first)
8. Click **Save**

---

### View 3: Film Status View

**Purpose:** Shows which films have intake, contacts, and captions

**Steps:**
1. Go to **Films_2026** sheet
2. **Data** → **Filter views** → **Create new filter view**
3. Name it: **Film Status — Ana Review**
4. No filters initially (show all films)
5. Sort by column **E** (Intake_Received) → **Sort A → Z**
   - This puts "N" (missing intake) at the top
6. Click **Save**

**Pro Tip:** To see contact/caption info side-by-side:
- Open **Film_Contacts** sheet in a new browser tab
- Arrange windows side-by-side for easy cross-reference

---

### View 4: Host Readiness View

**Purpose:** Which confirmed hosts have completed intake forms?

**Steps:**

**Part A: Add Helper Column**
1. Go to **Events_2026** sheet
2. In column **K1**, type: **Intake Status**
3. In **K2**, paste:
   ```
   =IF(C2="", "No Venue Assigned", IF(COUNTIF(Host_Intake!B:B, C2) > 0, "Intake Complete", "Intake Missing"))
   ```
   - This checks if the Venue_ID (C2) exists in the Host_Intake sheet
4. Drag formula down to all rows

**Part B: Create Filtered View**
1. **Data** → **Filter views** → **Create new filter view**
2. Name it: **Host Readiness Check**
3. Filter column **D** (Pipeline_Status): Check only "Scheduled" and "Confirmed Interest"
4. Filter column **K** (Intake Status): Check only "Intake Missing"
5. Sort by column **F** (Event_Date) → **Sort A → Z** (oldest first — these are urgent)
6. Click **Save**

---

## Phase 3: Publish Named Ranges

Named ranges let you publish specific data subsets as embeddable URLs.

---

### Step 3.1: Create Named Ranges

**Range 1: pipeline_summary**
1. In **Dashboard_V2**, select cells **A1:B22** (entire dashboard)
2. **Data** → **Named ranges**
3. Enter name: `pipeline_summary`
4. Click **Done**

**Range 2: host_status_2026**
1. In **Events_2026**, select **A1:H100** (adjust row count to include all events + room to grow)
2. **Data** → **Named ranges**
3. Enter name: `host_status_2026`
4. Click **Done**

**Range 3: film_status_2026**
1. In **Films_2026**, select **A1:E20** (adjust row count as needed)
2. **Data** → **Named ranges**
3. Enter name: `film_status_2026`
4. Click **Done**

**Range 4: action_items**
1. In **Dashboard_V2**, select **A18:B22** (just the Action Items section)
2. **Data** → **Named ranges**
3. Enter name: `action_items`
4. Click **Done**

---

### Step 3.2: Publish Named Ranges

For **each named range**:

1. **File** → **Share** → **Publish to web**
2. In the dropdown, select:
   - **Entire document** → change to: **[range name]** (e.g., `pipeline_summary`)
3. Format: **Web page** (for iframe embeds) **or CSV** (for programmatic fetch)
   - **Recommendation:** Use **Web page** for simple iframe embeds
4. Check: **Automatically republish when changes are made**
5. Click **Publish**
6. **Copy the link** → save it in a text file (you'll need these URLs for embedding)

**Example published URL:**
```
https://docs.google.com/spreadsheets/d/e/2PACX-1vT.../pubhtml?gid=123456&single=true&widget=true&headers=false&range=pipeline_summary
```

**Repeat for all 4 named ranges.** Keep the URLs handy.

---

## Phase 4: Embed Widgets in Docs Site

Now we'll replace the "coming soon" cards in the OEFF docs site with live data.

---

### Step 4.1: Locate the Docs Site Files

**If the docs site is on GitHub:**
1. Go to the repository (e.g., `github.com/your-org/oeff-docs`)
2. Navigate to the HTML file for the relevant page:
   - Hosts/Venues area: `area-hosts.html` or similar
   - Films/Content area: `area-films.html` or similar

**If the docs site is local:**
1. Open the project folder in a code editor (VS Code, Sublime, etc.)
2. Find the HTML files for each area

---

### Step 4.2: Add CSS for Embeds (One-Time)

In the main CSS file (e.g., `styles.css`), add this code **once**:

```css
/* Google Sheets Embed Container */
.google-embed {
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  border-radius: 12px;
  border: 1px solid #f0ede8;
  box-shadow: 0 4px 16px hsla(30, 20%, 20%, 0.08);
  margin: 1.5rem 0;
}

.google-embed iframe {
  width: 100%;
  min-height: 300px;
  border: none;
}
```

Save the CSS file.

---

### Step 4.3: Embed Widget 1 — Host Pipeline Status

**Location in docs:** `area-hosts.html` (or wherever "Host Tracker" card is marked "coming soon")

**Find this section** (it will look similar):
```html
<div class="resource-card">
  <h3>Host Tracker</h3>
  <p>Coming soon...</p>
</div>
```

**Replace with:**
```html
<div class="resource-card">
  <h3>Host Tracker</h3>
  <p>Live pipeline status for all 2026 venues</p>

  <div class="google-embed">
    <iframe
      src="YOUR_PUBLISHED_URL_FOR_host_status_2026_HERE"
      title="Host and Venue Pipeline Tracker"
      loading="lazy">
    </iframe>
  </div>

  <p class="caption">
    <a href="LINK_TO_FULL_DASHBOARD_WIDGET_HERE" target="_blank">
      View full tracker →
    </a>
  </p>
</div>
```

**What to replace:**
- `YOUR_PUBLISHED_URL_FOR_host_status_2026_HERE` → Paste the published URL for `host_status_2026` range
- `LINK_TO_FULL_DASHBOARD_WIDGET_HERE` → (Optional) Link to the standalone `host-tracker.html` widget for full-screen view

**Save the file.**

---

### Step 4.4: Embed Widget 2 — Film Intake Tracker

**Location in docs:** `area-films.html` (or wherever "Asset Tracker" card is marked "coming soon")

**Find:**
```html
<div class="resource-card">
  <h3>Asset Tracker</h3>
  <p>Coming soon...</p>
</div>
```

**Replace with:**
```html
<div class="resource-card">
  <h3>Film Intake & Asset Tracker</h3>
  <p>Track which films have intake forms, contacts, and captions</p>

  <div class="google-embed">
    <iframe
      src="YOUR_PUBLISHED_URL_FOR_film_status_2026_HERE"
      title="Film Intake Tracker"
      loading="lazy">
    </iframe>
  </div>
</div>
```

**What to replace:**
- `YOUR_PUBLISHED_URL_FOR_film_status_2026_HERE` → Paste the published URL for `film_status_2026`

**Save the file.**

---

### Step 4.5: Embed Widget 3 — Action Items Badge

**Location in docs:** Dashboard section (could be homepage or a team dashboard page)

**Add this HTML:**
```html
<div class="alert alert-warning" role="alert">
  <strong>⚠️ Action Items:</strong>
  <span id="action-count">—</span> items need attention

  <div class="google-embed" style="max-width: 400px; margin-top: 1rem;">
    <iframe
      src="YOUR_PUBLISHED_URL_FOR_action_items_HERE"
      title="Action Items"
      loading="lazy"
      style="min-height: 150px;">
    </iframe>
  </div>
</div>
```

**What to replace:**
- `YOUR_PUBLISHED_URL_FOR_action_items_HERE` → Paste the published URL for `action_items`

**Save the file.**

---

### Step 4.6: Link to Full Dashboard Widget

The standalone `host-tracker.html` widget is a full-featured, interactive table with search and sorting.

**Upload widget to docs site:**
1. Copy `/Users/garen/Desktop/OEFF Clean Data/dashboard-widgets/host-tracker.html` to your docs site repository
2. Upload to the same directory as your other HTML files (or create a `/widgets/` folder)
3. Commit and push to GitHub

**Link to it:**
```html
<a href="./host-tracker.html" target="_blank">View Full Host Tracker →</a>
```

Or, if you created a `/widgets/` folder:
```html
<a href="./widgets/host-tracker.html" target="_blank">View Full Host Tracker →</a>
```

**Note:** The standalone widget currently uses **mock data**. To connect it to live Google Sheets:
1. Open `host-tracker.html` in a code editor
2. Find the **GOOGLE SHEETS INTEGRATION** section (near bottom of `<script>`)
3. Uncomment the `fetchGoogleSheetsData()` function
4. Replace `YOUR_GOOGLE_SHEETS_PUBLISHED_CSV_URL_HERE` with the **CSV format** published URL for `host_status_2026`
5. Save and re-upload

---

### Step 4.7: Update "Coming Soon" Links in Quick Reference

**Location:** `area-hosts.html` (or Quick Reference section)

**Find:**
```html
<li><a href="#">Host FAQ</a> — Link pending</li>
<li><a href="#">Contact Directory</a> — Link pending</li>
```

**Replace with:**
```html
<li><a href="./host-tracker.html">Host Pipeline Tracker</a></li>
<li><a href="https://docs.google.com/spreadsheets/d/YOUR_V7_ID/edit#gid=CONTACTS_SHEET_ID" target="_blank">Contact Directory</a> (Google Sheet)</li>
```

**What to replace:**
- `YOUR_V7_ID` → The ID from your V7 Google Sheets URL
- `CONTACTS_SHEET_ID` → The gid= number for the Film_Contacts or relevant contact sheet

---

### Step 4.8: Deploy to Cloudflare Pages

**If using GitHub + Cloudflare Pages:**
1. Commit all changes to your repository:
   ```bash
   git add .
   git commit -m "Add live data widgets to docs site"
   git push origin main
   ```
2. Cloudflare Pages will automatically rebuild and deploy
3. Wait ~2 minutes → visit your docs site URL to see the live widgets

**If deploying manually:**
1. Upload the updated HTML files to your web host
2. Verify the widgets load correctly

---

## Phase 5: Auto-Refresh Options

Google Sheets published ranges auto-refresh **every ~5 minutes** by default. For most use cases, this is sufficient.

**Option A: Use Default Auto-Refresh (Recommended)**
- No setup needed
- Data updates within 5 minutes of changes in V7
- Works for iframe embeds automatically

**Option B: Force Refresh with JavaScript**
Add this script to your HTML pages:

```html
<script>
  // Auto-refresh embedded Google Sheets every 5 minutes
  setInterval(() => {
    document.querySelectorAll('.google-embed iframe').forEach(iframe => {
      iframe.src = iframe.src; // Reload iframe
    });
  }, 5 * 60 * 1000); // 5 minutes in milliseconds
</script>
```

**Option C: Google Apps Script for Real-Time Updates** (Advanced)
1. In V7: **Extensions** → **Apps Script**
2. Write a script that triggers on edit and posts to a webhook
3. Use the webhook to invalidate Cloudflare cache
4. **Complexity:** High — only needed if real-time updates are critical

**Recommendation:** Stick with **Option A** (default 5-minute refresh). Festival planning data doesn't change in real-time, so this latency is acceptable.

---

## Summary: Mapping Widgets to "Coming Soon" Slots

| Docs Site Location | Original Slot | New Widget | Data Source |
|-------------------|---------------|------------|-------------|
| Hosts/Venues area | "Host Tracker" | Embedded pipeline status + link to full widget | `host_status_2026` |
| Hosts/Venues area | "Contact Directory" | Link to Film_Contacts sheet | Direct Google Sheets link |
| Films/Content area | "Asset Tracker" | Embedded film intake status | `film_status_2026` |
| Films/Content area | "QC Checklist" | (Future) Link to Packet_QA sheet | Direct Google Sheets link |
| Dashboard callout | (New) | Action Items count | `action_items` |
| Quick Reference | "Host Quick Links" | Links to webinars, FAQ, toolkit | Static links (add as available) |

---

## Troubleshooting

### Problem: Iframe shows "You need permission"

**Cause:** The published range isn't publicly accessible.

**Fix:**
1. Go to **File** → **Share** → **Publish to web**
2. Verify the range is published
3. Check: **Automatically republish when changes are made**
4. Try the published URL in an incognito browser window — if it loads, the docs site will see it too

---

### Problem: Formulas show #REF! error

**Cause:** Sheet name mismatch.

**Fix:**
1. Check exact sheet names (case-sensitive, spaces vs underscores)
2. Example: `Events_2026` (with underscore) vs `Events 2026` (with space)
3. Update formulas to match exact sheet names

---

### Problem: Iframe is too small / cuts off content

**Fix:**
Adjust `min-height` in CSS:

```css
.google-embed iframe {
  min-height: 500px; /* Increase this value */
}
```

Or set a specific height per widget:

```html
<iframe src="..." style="min-height: 600px;">
```

---

### Problem: Widget doesn't auto-refresh

**Fix:**
1. Check that **"Automatically republish when changes are made"** is enabled in Publish to web settings
2. Wait 5 minutes after making a change in V7
3. Hard-refresh the browser (Ctrl+Shift+R or Cmd+Shift+R)

---

### Problem: Standalone widget (host-tracker.html) shows mock data

**Fix:**
1. Open `host-tracker.html` in a code editor
2. Scroll to the **GOOGLE SHEETS INTEGRATION** section (JavaScript)
3. Uncomment the `fetchGoogleSheetsData()` function
4. Replace `YOUR_GOOGLE_SHEETS_PUBLISHED_CSV_URL_HERE` with your actual published CSV URL
5. Replace `init();` with `fetchGoogleSheetsData();`
6. Save and re-upload

---

## Next Steps

### After Setup is Complete:
1. **Test the widgets** — verify data updates when you change V7
2. **Share with team** — send links to filtered views
3. **Train support staff** — show them how to use filtered views and the dashboard
4. **Lock historical sheets** — protect 2024/2025 data from accidental edits:
   - Right-click sheet tab → **Protect sheet** → Set permissions to "View only"

### Future Enhancements (Phase 3):
- [ ] Geographic map of venues
- [ ] Pipeline funnel chart
- [ ] Year-over-year comparison
- [ ] Weekly digest email (Google Apps Script)

---

## Reference Files

| File | Purpose |
|------|---------|
| `formula-reference.md` | Complete formula library with explanations |
| `dashboard-widgets/host-tracker.html` | Standalone interactive tracker widget |
| `integration-guide.md` | This guide (step-by-step for non-technical users) |

---

## Support

**Questions?** Contact:
- **Garen** (Tech Coordinator) — for technical issues, bugs, or custom widgets
- **Ana** (Executive Director) — for workflow questions or data accuracy

**Useful Resources:**
- [Google Sheets Publish to Web Guide](https://support.google.com/docs/answer/183965)
- [Google Sheets Filter Views](https://support.google.com/docs/answer/3540681)
- Beautiful-First Design System — ask Garen for access (for developers)

---

**Last Updated:** 2026-02-12
**Version:** 1.1
**Phase:** 1 → 2 (Dashboard complete, embedding in progress)
