# Host Helper System — Team Guide for OEFF 2026

**For:** OEFF operations team and interns
**Written by:** Garen Hudson, Technical Coordinator
**Last updated:** March 2026

---

## What is this?

This is the reference guide for the system that gives each OEFF host their own page showing their venue's screening details. You'll use this to create new host pages, understand what hosts see, and know what to update when things change.

The technical coordinator won't be on-site during festival week (April 22–27). This guide is written so anyone on the team can handle the day-to-day independently.

---

## 1. What hosts see

Each host gets a single link. That link opens a page showing only their venue — nothing else.

The page shows:
- Venue name and address
- Screening date and time
- Film title
- Current registration count
- AV setup, parking, and WiFi details (from their submission form)

No login required. The link is the access. If a host can click a link, they're in.

When the team updates a field in Airtable — changes a film assignment, updates a registration count, adds parking notes — the host's page reflects it immediately. No scripts, no deploys, no waiting.

---

## 2. How this is different from the spreadsheet

In 2024 and 2025, hosts had edit access to a shared Google Sheet. They could see their row and update it directly. The problem: the sheet had 30+ columns and no reliable way to limit what hosts could see. Privacy was fragile. Accidental edits happened.

This year, hosts can't edit their page directly. Here's the tradeoff:

| Old model (spreadsheet) | New model (Airtable) |
|------------------------|----------------------|
| One sheet, all venues visible | Each host sees only their venue |
| Hosts could edit their row | Hosts submit updates via a form |
| Changes appeared instantly | Updates still appear immediately — just through a different path |
| Easy for hosts but harder to protect | More controlled, cleaner separation |

The host-facing pages are built as Airtable Interface pages — a feature inside our Airtable base that displays data as a formatted, filtered, public-facing view. No external site to maintain.

---

## 3. Who maintains what

| What | Who | Where in Airtable |
|------|-----|-------------------|
| Venue details (address, capacity, description) | Operations team | Venues table |
| Film assignments | Operations team | Events table |
| Screening dates and times | Operations team | Events table |
| Registration counts | Interns — update 2–3x per week | Venues table |
| Host form responses | Operations team reviews | Host Submissions table |
| Creating a new venue interface page | Any trained team member | Interfaces tab (see Section 4) |
| Airtable schema changes, troubleshooting | Technical coordinator | — |
| Cloudflare deployment (hosts.oneearthfilmfest.org) | Technical coordinator | — |

---

## 4. How to create a new per-venue interface page

This takes about 2 minutes. Any team member can do it after reading these steps once.

1. Open the OEFF 2026 Airtable base: [airtable.com/appvUfaPd9ejb5fHb](https://airtable.com/appvUfaPd9ejb5fHb)
2. Click the **Interfaces** tab at the top of the page.
3. Find an existing venue interface — for example, "Uncommon Ground."
4. Click the **...** menu on that interface → click **Duplicate**.
5. Click the **...** menu on the new copy → click **Rename** → type the new venue name.
6. Open the new interface in edit mode.
7. Click the list element on the page.
8. Click **Filter** in the toolbar at the top.
9. Click the gear icon next to "Filter by."
10. Change the filter value from the old venue name to the new venue name.
11. Click **Publish**.
12. Click **Share interface** → go to the **Share to web** tab → toggle on "Share to web" → copy the public link.
13. Send the link to the host.

That's it. The new page will immediately show data for the new venue only.

---

## 5. What happens when data changes

The team updates a field in Airtable. The host's page updates instantly.

There's no step in between — no export, no sync, no handoff. The Airtable Interface pulls directly from the live base. This is the single biggest improvement over the static pages from previous years.

**Common updates and where to make them:**

| What changed | Go to | Field to update |
|-------------|-------|-----------------|
| Film title changed | Events table | Film name / linked record |
| Screening time adjusted | Events table | Date/time field |
| Registration count increased | Venues table | Registration count field |
| Host submitted parking/WiFi info | Host Submissions table | Review and copy to Venues table if needed |

---

## 6. What the team handles vs. the technical coordinator

**The team handles:**
- Day-to-day data entry in Airtable
- Updating registration counts (interns, 2–3x per week)
- Creating new venue interface pages (Section 4 above)
- Reviewing host form submissions
- Sending interface links to hosts

**Technical coordinator handles:**
- Changes to the Airtable structure (adding or removing fields, changing table relationships)
- Anything that breaks
- The host guide at hosts.oneearthfilmfest.org — that's a separate system on Cloudflare, managed separately from the Airtable pages

If something looks wrong in Airtable and you're not sure if it's a data issue or a structural issue, check the data first. Most "the page looks wrong" problems are just a field that needs updating.

---

## 7. Important links

| What | Link |
|------|------|
| Airtable base (OEFF 2026) | [airtable.com/appvUfaPd9ejb5fHb](https://airtable.com/appvUfaPd9ejb5fHb) |
| Host Submission Form | [View form](https://airtable.com/appvUfaPd9ejb5fHb/pagqhyU3kM0AVP913/form) |
| Host guide (public-facing) | [hosts.oneearthfilmfest.org](https://hosts.oneearthfilmfest.org) |
| Questions about this system | hosts@oneearthcollective.org |

---

*This guide covers the 2026 system. If something in here doesn't match what you're seeing in Airtable, the base is the authority — this doc might be slightly out of date.*
