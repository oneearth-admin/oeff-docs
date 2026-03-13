# Host Helper Walkthrough — Kim 1:1

**Date:** Friday, March 13, 2026
**Duration:** 30 min
**Goal:** Show Kim the new Host Helper portal + automations, get her input on what needs adjusting before sending to hosts.

---

## Agenda (30 min)

| Time | Topic | Purpose |
|------|-------|---------|
| 0:00 | Big picture: what this replaces | Orient — she's been in Google Sheets world |
| 0:05 | Live demo: Host Helper interface | Walk through what a host sees |
| 0:12 | Live demo: form submission flow | Show the button → form → confirmation email loop |
| 0:18 | Automations overview | 3 automations, including her Monday digest |
| 0:22 | Her workflow: what changes, what doesn't | Mailmeteor stays. This adds, doesn't replace. |
| 0:25 | Data gaps + next steps | What we need before sending to hosts |
| 0:30 | End | |

---

## Step-by-Step Guide

### 1. Big Picture (5 min)

**Open:** The shared Host Helper URL in a browser:
```
https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb
```

**Key framing for Kim:**
- "This is a portal hosts can visit to see their screening info and submit missing venue details."
- "It pulls live from Airtable — when we update data, hosts see it immediately."
- "It doesn't replace your Mailmeteor workflow. You still send emails the same way. This gives hosts a place to look things up and send us info back."

**What to emphasize:**
- No login required — it's a public shared link
- Each venue gets its own deep-link URL (for personalized emails)
- Hosts can't edit anything directly — they submit changes through a form

---

### 2. Live Demo: Host Helper Interface (7 min)

**Walk through the Uncommon Ground record as an example.**

**Point out these sections:**

**"Your Screening" group:**
- Film (currently TBD for some — that's a data gap we'll fix)
- Screening Date + Start Time
- Doors Open time
- Ticket Info (clickable Eventbrite link)
- Contact Name / Phone / Email

**Venue details below:**
- Parking, Transit, WiFi, AV Notes
- Venue Address

**"Take Action" group:**
- Green "Submit Your Venue Details" button — this is the call to action
- "Help us prepare for your screening" — warm framing

**Show the venue list on the left:**
- All confirmed venues are listed with tier badges (T1, T2)
- Search bar works — Kim can look up any venue
- Three view options at top (grid, filter, card views)

**Click a different venue** (e.g., Columbia College - Film Row Cinema, which is T1) to show how data changes per record.

---

### 3. Live Demo: Form Submission Flow (6 min)

**Click the green "Submit Your Venue Details" button** on any venue.

This opens the Host Confirmations form, pre-filled with the venue name. Walk through the form fields:
- Submitted By (who's filling this out)
- Doors Open Time
- Parking Instructions
- Transit Directions
- WiFi Network / Password
- AV Setup Notes
- Contact Phone
- Loading / Access Instructions
- Contact Email
- "Anything Look Wrong?" (free-text catch-all)

**Key points:**
- The venue is pre-selected — hosts don't have to pick from a dropdown
- Nothing is required — they can fill in whatever they have
- They can submit multiple times (each creates a new record)

**After submitting:**
- A confirmation email goes to the Contact Email they provided (Automation 1)
- The submission appears in the Host Confirmations table with Status = "New"
- Kim can review it and change Status to "Reviewed" → triggers a notification back to the host (Automation 2)

---

### 4. Automations Overview (4 min)

**Open Airtable → Automations tab** to show the 3 new automations:

| Automation | Trigger | What it does |
|-----------|---------|-------------|
| **Host Confirmation → Thank You** | Form submitted | Sends "Got it!" email to the person who submitted |
| **Host Confirmation → Status Update** | Status changes to "Reviewed" | Sends "We've reviewed your submission" email |
| **Weekly Digest → Kim** | Every Monday 9am | Emails Kim a list of new submissions awaiting review |

**For Kim specifically:**
- "Every Monday morning you'll get an email if there are new submissions."
- "When you've reviewed one, change Status to 'Reviewed' — the host gets a notification automatically."
- "If you want to merge the info into the venue record, change Status to 'Merged.'"

**Show the Host Confirmations table** in the Data tab so Kim can see where submissions land and the Status column workflow: New → Reviewed → Merged.

---

### 5. Her Workflow: What Changes, What Doesn't (3 min)

**What stays the same:**
- Mailmeteor for bulk host outreach (screening confirmations, logistics emails)
- Google Sheets as her working spreadsheet for mail merge fields
- Her existing email templates and merge process

**What's new:**
- Each host outreach email can now include a personalized link to their Host Helper page
- Hosts who need to send us parking/AV/WiFi details get a form instead of replying to email
- Kim gets a Monday digest instead of manually checking for responses
- The review → notification loop gives hosts confidence their info was received

**Suggested workflow integration:**
- In Mailmeteor templates, add a line like: "View your screening details: {Host Helper Link}"
- The per-venue links are ready — we can add a column to her merge sheet
- When a host submits the form, Kim reviews in Airtable and merges into the Venues record

---

### 6. Data Gaps + Next Steps (5 min)

**Ask Kim:**

1. **Film assignments:** Some venues still show "TBD" — which ones are actually confirmed? Can she flag which are truly pending vs. which we just haven't entered?

2. **Contact info:** Most venues show "Host contact to be confirmed" — does Kim have contact names/phones/emails from her outreach that we should enter?

3. **Doors Open times:** Almost all say "to be confirmed" — is this something hosts decide, or does OEFF set a standard (e.g., 30 min before)?

4. **Per-venue links for Mailmeteor:** Does she want us to add a "Host Helper Link" column to her mail merge sheet? We have the links ready for all 20 venues.

5. **Email phrasing:** Is the green button label "Submit Your Venue Details" clear? Would she word it differently for her hosts?

6. **Missing venues:** 4 venues don't have Venues table records yet (Chicago Climate Action Museum, CPL Harold Washington, CPL Rogers Park, IIT Bronzeville). Are any of these confirmed and need records?

**Decisions to make together:**
- When to start sending Host Helper links to hosts (immediately? after data cleanup?)
- Whether to include the form link in the next Mailmeteor batch or send separately
- Which venues to pilot with first (suggest 2-3 responsive hosts)

---

## Key Links to Have Open

| What | URL |
|------|-----|
| Host Helper (public) | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb |
| Example: Uncommon Ground | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb?F8hUa=rec3uDHHjHUwNfZV1 |
| Example: Columbia College | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb?F8hUa=recIkQNX2gTDjFqLp |
| Form (generic) | https://airtable.com/app9DymWrbAQaHH0K/shryhEHxXJ4mJdVfd |
| Airtable Automations | Open from Airtable → Automations tab |
| Host Confirmations table | Open from Airtable → Data tab → Host Confirmations |
