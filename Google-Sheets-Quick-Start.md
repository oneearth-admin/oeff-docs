# Google Sheets Quick Start — OEFF Dashboard

> **For Ana and support staff**
> Get the V7 dashboard formulas working in 15 minutes. No coding needed.

---

## Before You Start

You need:
- **Edit access** to the V7 Google Sheet (not the Excel file)
- About **15 minutes** of uninterrupted time

If V7 is still in Excel format, open it in Google Sheets first:
1. Upload `V7.xlsx` to Google Drive
2. Right-click the file, choose **Open with Google Sheets**
3. Go to **File** then **Save as Google Sheets**

---

## Part 1: Create the Dashboard Sheet

### Step 1: Add a new sheet

1. At the bottom of V7, click the **+** button to add a new sheet
2. Name it **Dashboard_V2**

### Step 2: Add labels

Type these labels in column A:

| Cell | Type This |
|------|-----------|
| A1 | OEFF 2026 Dashboard |
| A3 | Total Hosts |
| A4 | Events - Scheduled |
| A5 | Events - Confirmed Interest |
| A6 | Events - Interested |
| A7 | Total Events 2026 |
| A9 | Total Films |
| A10 | Films with Intake |
| A11 | Films Missing Intake |
| A13 | Film Contacts |
| A14 | Captions Complete |
| A16 | Intake Responses |
| A17 | Unmatched Intake |

### Step 3: Paste the formulas

Click each cell in column B and paste the formula shown. Press Enter after each one.

| Cell | Paste This Formula |
|------|--------------------|
| B3 | `=COUNTA(Hosts!A2:A)` |
| B4 | `=COUNTIF(Events_2026!D2:D,"Scheduled")` |
| B5 | `=COUNTIF(Events_2026!D2:D,"Confirmed Interest")` |
| B6 | `=COUNTIF(Events_2026!D2:D,"Interested")` |
| B7 | `=COUNTA(Events_2026!A2:A)` |
| B9 | `=COUNTA(Films_2026!A2:A)` |
| B10 | `=COUNTIF(Films_2026!E2:E,"Y")` |
| B11 | `=COUNTIF(Films_2026!E2:E,"N")` |
| B13 | `=COUNTA(Film_Contacts!A2:A)` |
| B14 | `=COUNTIF(Film_Contacts!F2:F,"Complete")` |
| B16 | `=COUNTA(Host_Intake!A2:A)` |
| B17 | `=COUNTA(Ana_Matching!A2:A)` |

### Step 4: Check that they work

Each cell in column B should now show a number. If any cell shows **#REF!**, the sheet name in the formula doesn't match the actual sheet tab name. Check for:
- Spaces vs. underscores (e.g., `Events_2026` vs `Events 2026`)
- Capitalization (sheet names are case-sensitive)
- Missing sheets

---

## Part 2: Create a Filtered View

Filtered views let you see a subset of data without affecting what other people see.

### Ana's Pipeline View

1. Click the **Events_2026** sheet tab
2. Go to **Data** then **Create a filter view**
3. Name it: **Ana Pipeline View**
4. Click the filter arrow on the **Pipeline_Status** column (column D)
5. Uncheck "Select all", then check only: **Scheduled**, **Confirmed Interest**
6. Click **OK**

Now you can switch between this filtered view and the full data anytime:
- **Data** then **Filter views** then **Ana Pipeline View**

### Film Status View

1. Click the **Films_2026** sheet tab
2. Go to **Data** then **Create a filter view**
3. Name it: **Film Status View**
4. Click the filter arrow on the **Intake_Received** column (column E)
5. Uncheck "Select all", then check only: **N**
6. Click **OK**

This shows only films that still need intake forms.

---

## Part 3: Publish a Named Range

Publishing makes data visible to the dashboard widgets on the docs site.

### Step 1: Create a named range

1. Go to **Data** then **Named ranges**
2. Click **Add a range**
3. Name: **pipeline_summary**
4. Range: Select `Dashboard_V2!A1:B17`
5. Click **Done**

### Step 2: Publish it

1. Go to **File** then **Share** then **Publish to web**
2. In the first dropdown, select **pipeline_summary** (the named range you just created)
3. In the second dropdown, select **Web page** (default)
4. Check the box: **Automatically republish when changes are made**
5. Click **Publish**
6. Copy the URL that appears — you'll need this for the docs site widgets

### Step 3: Test the URL

1. Open a new **incognito/private browser window**
2. Paste the published URL
3. You should see the dashboard data as a simple table
4. If you see "You need permission," go back and check the publish settings

---

## Troubleshooting

**Formula shows #REF!**
- The sheet name in the formula doesn't match the tab name. Check spelling, spaces, and capitalization.

**Formula shows 0 when it shouldn't**
- The column letter in the formula might be wrong. Check that the data is actually in the column the formula references (e.g., column D for Pipeline_Status).

**Published URL says "You need permission"**
- Re-publish: **File** then **Share** then **Publish to web**. Make sure the correct range is selected and "Automatically republish" is checked.

**Filtered view disappeared**
- It's still there. Go to **Data** then **Filter views** and select it from the list.

---

## What's Next

Once the formulas are working and at least one named range is published, let Garen know. He'll connect the published data to the docs site widgets so the dashboard updates automatically.

**Reference:** See `formula-reference.md` for detailed explanations of each formula, and `integration-guide.md` for the full 5-phase implementation plan.
