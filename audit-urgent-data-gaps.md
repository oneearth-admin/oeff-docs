# Audit: Where Does the Urgent Host Helper Data Already Live?

## Context

The Host Helper Migration Plan identifies these urgent data needs before the Airtable interface can go live. Before we treat these as gaps to fill, check whether the data already exists somewhere — stale, scattered, or under a different field name — and just needs to be reconciled into Airtable.

## Urgent items to audit

### 1. Host contact info (name, email, cell) for all 22 scheduled venues

**Check these sources in order:**

- **Airtable Venues table** — does it have contact fields? What's populated vs empty?
- **Host intake form responses** (`airtable-import/05-host-intake.csv`) — column `Contact Name`, `Contact Email`. These are self-reported by hosts. Cross-reference against the 22 scheduled venues.
- **Roadmap venue contacts** (`roadmap-venue-contacts.csv`) — has a `Venue Contacts` column. Some are populated, some empty. How many of the 22 have data here?
- **2025 Host Helper sheets** (`Host Helper Links` spreadsheet: `1nkPZVNQMdAIQm1F3OFcUI87RGzK8KOceH5nyfOdMxyA`) — rows 3-5 of each sheet had host contact, AV contact, and marketing contact with names, emails, and cell numbers. Many 2026 venues were also 2025 venues. Which contacts carry over?
- **Eventbrite state** (`eventbrite-state.json`) — may have organizer contact info from event creation.

**Output:** For each of the 22 venues, report: contact name, email, cell, and which source it came from. Flag any venue with zero contact info across all sources.

### 2. Film runtimes verified

**Check these sources:**

- **Airtable Films table** — is there a runtime field? What's populated?
- **Films CSV** (`airtable-import/02-films.csv`) — check if runtime column exists (it may not — look at headers).
- **Roadmap JSON** (`roadmap-2026-host-venues.json`) — the roadmap rows may include runtime in the schedule columns.
- **Film intake survey responses** — if filmmakers submitted runtimes via the intake form, check whether those made it into Airtable.
- **Film websites / trailer links** — the Films CSV has `Film Website` and `Trailer Link` columns. Runtime is often listed on film websites.

**Output:** For each of the ~16 unique films in the 2026 lineup, report: film title, runtime (if found), and source. Flag any film with no runtime in any source.

### 3. Eventbrite event URLs (remaining 8 of 22)

**Check these sources:**

- **Eventbrite state file** (`eventbrite-state.json`) — this tracks which events have been created. Which 14 are published? Which 8 are missing?
- **Events CSV** (`airtable-import/03-events.csv`) — does it have an Eventbrite URL column?
- **Airtable Events table** — check for an Eventbrite URL or Event Page field.

**Output:** List all 22 venues. For each, show: Eventbrite URL (if exists), publish status, and what's blocking the remaining 8.

### 4. AV / tech contact per venue (first priority but check while we're here)

**Check these sources:**

- **Host intake responses** (`05-host-intake.csv`) — `Has Av Lead` column exists but it's a boolean. The actual AV contact name/email may not be captured.
- **2025 Host Helper sheets** — row 4 had "Host AV Contact (Name, Email)" for each venue. Returning venues may have the same AV contact.
- **Airtable Venues table** — check for an AV contact field.

**Output:** For each venue, report: AV contact (if found), source, and whether it's likely current or stale from 2025.

## How to run this

This is a read-only research task. Don't modify any data — just report what exists and where. Use the Airtable API for live data, local CSVs for the Feb 6 snapshot, and the 2025 host helper sheets (via the links spreadsheet) for carry-over contacts.

**Airtable base ID:** `app9DymWrbAQaHH0K`
**Local CSVs:** `~/Desktop/OEFF Clean Data/airtable-import/`
**Eventbrite state:** `~/Desktop/OEFF Clean Data/eventbrite-state.json`
**Roadmap JSON:** `~/Desktop/OEFF Clean Data/roadmap-2026-host-venues.json`
**Roadmap contacts:** `~/Desktop/OEFF Clean Data/roadmap-venue-contacts.csv`
**2025 Host Helper Links:** Google Sheet `1nkPZVNQMdAIQm1F3OFcUI87RGzK8KOceH5nyfOdMxyA`

The goal is to turn "partial" into a specific count and a specific list of what's actually missing vs what's just not in the right place yet.
