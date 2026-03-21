# Host Interface Buildout Spec — Airtable Interface Designer

**Purpose:** Create a per-venue host-facing dashboard that answers "Am I ready?" instead of showing a database row.
**Created:** 2026-03-20
**Status:** Template design ready. Build one (Uncommon Ground), test, then clone 22 more.

---

## Prerequisites (done)

- [x] `Days Until Event` formula field added to Events table: `IF({Date}, DATETIME_DIFF({Date}, TODAY(), "days"), "")`
- [x] `Host Next Action` text field added to Events table (team-editable, under 15 words)
- [x] Test interface "Host Helper 2026 copy" exists with working per-venue filter (can be deleted or reused)

## Step 1: Create the template interface

1. Go to **Interfaces** tab in OEFF 2026 base
2. Click **+ New interface** → choose **Dashboard** layout
3. Name it: **"Uncommon Ground"**

## Step 2: Set the data source and filter

1. The dashboard should source from the **Events** table
2. Set **designer-level filter**: Where **Venue Name** is **"Uncommon Ground"**
3. This ensures only this venue's event(s) appear

## Step 3: Add elements (top to bottom)

| Order | Element | Type | Source / Content | Notes |
|-------|---------|------|-----------------|-------|
| 1 | Header text | Text block | "Your OEFF 2026 Screening" | Static. Sets context. |
| 2 | Countdown | Number element | Events → `Days Until Event` | Large display. Label: "days until your screening" |
| 3 | Next action | Text element | Events → `Host Next Action` | No label. Shows what the host needs to do, or blank if nothing. Team updates this field manually. |
| 4 | Screening details | List element (1 record) | Events table, filtered to this venue | **Fields to show:** Film (linked record), Date, Start Time, Ticket Price, Venue Name (linked). **Fields to hide:** everything else. |
| 5 | Update button | Button element | URL: `https://airtable.com/appvUfaPd9ejb5fHb/pagqhyU3kM0AVP913/form` | Label: "Update Your Venue Details" |
| 6 | Guide button | Button element | URL: `https://hosts.oneearthfilmfest.org` | Label: "View Host Guide" |

### Optional elements (if space allows)

| Order | Element | Type | Source / Content | Notes |
|-------|---------|------|-----------------|-------|
| 7 | Contact info | Text block | Static: "Questions? Email hosts@oneearthcollective.org" | Footer-style |
| 8 | Venue details | List element (1 record) | Venues table, linked from Event | Fields: Address, Capacity, Region. Collapsed/below fold. |

## Step 4: Disable user actions

In the element properties panel for each list/grid element:
- **Sort:** OFF
- **Search:** OFF
- **Filter:** OFF
- **Group:** OFF
- **Row height:** ON (optional, doesn't hurt)
- **Edit records inline:** OFF
- **Add records through a form:** OFF

## Step 5: Publish and share

1. Click **Publish**
2. Click **Share** → bottom-left "Share" button
3. Go to **Share to web** tab
4. Toggle **Share to web** ON
5. Accept the "hidden data may be exposed" warning (venue names aren't sensitive)
6. **Copy the public link** — this is what the host gets

## Step 6: Test in incognito

Open the link in an incognito/private window. Verify:
- [ ] Only Uncommon Ground data visible
- [ ] No filter/sort/search controls
- [ ] No login required
- [ ] Countdown number displays correctly
- [ ] Film title and date show (if assigned)
- [ ] Buttons link to correct URLs
- [ ] No other venue data accessible anywhere on the page

## Step 7: Clone for all venues

Once the template passes testing:

1. Click **...** menu on "Uncommon Ground" interface → **Duplicate**
2. **Rename** to the next venue name
3. **Edit** → change the filter value to the new venue name
4. **Publish** → **Share to web** → copy link
5. Repeat for all 23 venues
6. Save all links to `host-interface-links.json`

---

## Design principles

1. **Status first.** The countdown number is the hero — it tells the host "this is real, it's coming."
2. **Single next action.** If the team needs something from the host, it shows in `Host Next Action`. If not, blank = "you're good."
3. **Don't show the database.** Hide internal fields (pipeline status, internal notes, record IDs). Show only what a host needs.
4. **No controls.** Hosts don't filter, sort, or search. They see their venue. That's it.
5. **Live data.** When the team updates Airtable, the host sees it immediately. No scripts, no deploys.

## Important URLs

| What | URL |
|------|-----|
| Airtable base | `https://airtable.com/appvUfaPd9ejb5fHb` |
| Host Submission Form | `https://airtable.com/appvUfaPd9ejb5fHb/pagqhyU3kM0AVP913/form` |
| Host Guide | `https://hosts.oneearthfilmfest.org` |
| Test interface (Uncommon Ground) | `https://airtable.com/appvUfaPd9ejb5fHb/shriogZpbL28XUgXd` |
