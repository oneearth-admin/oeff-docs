# Host Helper Portal — Walkthrough

**March 13, 2026 · Garen + Kim**

We built a self-service portal for hosts. This doc walks through what it does, how it connects to Kim's outreach workflow, and what we need to decide before sending it to hosts.

---

## What is the Host Helper?

A public Airtable page where each host can:
- See their screening details (film, date, time, Eventbrite link)
- Check their venue info (parking, AV, WiFi, address)
- Submit missing details through a form (one click, pre-filled with their venue)

No login needed. Each venue gets a unique URL we can drop into outreach emails.

**Full venue list:** https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb

---

## Walkthrough

### Step 1: Open a venue page

Pick one to look at together:

| Venue | Link |
|-------|------|
| Uncommon Ground | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb?F8hUa=rec3uDHHjHUwNfZV1 |
| Columbia College | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb?F8hUa=recIkQNX2gTDjFqLp |
| Trinity Lutheran Church | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb?F8hUa=recj4WDmPoU0trMWs |

What we're looking at:
- **"Your Screening"** — Film, date, time, Eventbrite link, contact info
- **Venue details** — Parking, transit, WiFi, AV notes, address
- **"Take Action"** — Green button that opens the venue details form

**Question for both of us:** Does this have the right info? Anything missing that hosts would expect to see?

---

### Step 2: Click the green button

The green "Submit Your Venue Details" button opens a form pre-filled with the venue name.

The form asks for:
- Submitted By (their name)
- Doors Open Time
- Parking Instructions
- Transit Directions
- WiFi Network + Password
- AV Setup Notes
- Contact Phone
- Loading / Access Instructions
- Contact Email
- "Anything Look Wrong?" (open text)

Nothing is required. Hosts fill in what they have. They can submit more than once.

**Question for both of us:** Are these the right fields? Is the order right? Anything we should add or cut?

---

### Step 3: What happens after a host submits

Three automations are running:

**1. Instant confirmation → Host**
When someone submits the form, they get an email: "Got it! Thanks for submitting your venue details."

**2. Status update → Host**
When Kim reviews a submission and sets Status to "Reviewed," the host gets: "Your venue details have been reviewed."

**3. Weekly digest → Kim**
Every Monday at 9am, Kim gets an email listing any submissions with Status = "New" that need review.

The review workflow:
1. Submission arrives → Status = **New**
2. Kim reviews → changes to **Reviewed** (host gets notified)
3. Info merged into venue record → changes to **Merged**

**Question for both of us:** Does this review flow work for Kim's week? Is Monday the right day for the digest?

---

## How this connects to Mailmeteor

This doesn't replace anything. Kim's outreach flow stays the same:
- Google Sheets for merge data
- Mailmeteor for bulk sends
- Existing templates and follow-up cadence

What this adds:
- A **link to include in outreach emails** — each venue gets a unique URL to their Host Helper page
- A **form** that replaces "reply to this email with your parking info" — structured data, not email threads
- **Automated confirmations** so hosts know their info was received without Kim sending manual replies

**To integrate:** We can add a "Host Helper Link" column to Kim's merge sheet. Then her Mailmeteor template can include something like:

> View your screening details and submit your venue info: {Host Helper Link}

---

## What we need to decide

### Before sending to hosts

- [ ] **Data cleanup:** Some venues show "TBD" for film, "to be confirmed" for contacts and doors-open time. Which ones can we fill in now?
- [ ] **Pilot or batch?** Send to all hosts at once, or start with 2-3 responsive hosts to test?
- [ ] **Timing:** When do we start? Immediately after cleanup, or tied to the next Mailmeteor batch?

### About the portal itself

- [ ] **Button label:** "Submit Your Venue Details" — clear enough? Would hosts respond better to different wording?
- [ ] **Missing venues:** 4 venues don't have records yet (Chicago Climate Action Museum, CPL Harold Washington, CPL Rogers Park, IIT Bronzeville). Are any confirmed and need adding?
- [ ] **Doors-open default:** Do hosts decide their own doors-open time, or is there a standard (e.g., 30 min before)?

### About Kim's workflow

- [ ] **Merge sheet column:** Should we add the Host Helper links to Kim's mail merge spreadsheet?
- [ ] **Monday digest:** Is Monday morning the right time? Different day?
- [ ] **Review cadence:** How often would Kim realistically check new submissions — weekly with the digest, or more often?

---

## Quick reference

| What | Link |
|------|------|
| All venues (Host Helper) | https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb |
| Host Confirmations form | https://airtable.com/app9DymWrbAQaHH0K/shryhEHxXJ4mJdVfd |
| Host Confirmations table | Airtable → Data → Host Confirmations |
| Automations | Airtable → Automations tab |
