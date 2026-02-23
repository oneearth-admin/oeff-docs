# OEFF Host Portal & Contact Security — Recommendation

**Prepared:** 2026-02-23
**For:** Ana, Josh, Garen, OEFF 2026 team
**Status:** Recommendation only — nothing built

---

## Executive Summary

**Problem 1 — Secure host pages:** Use unique URL tokens (unguessable links) as the default protection layer for contact info, and reserve a browser-based password prompt for financial data (scholarships). Requires no new infrastructure, and is right-sized for the actual risk.

**Problem 2 — Host helper page:** Generate a mobile-first, per-venue one-pager from existing Airtable data alongside the current venue sections. It should live behind the host's unique URL token. Static HTML, printable, phone-friendly. No new pipeline needed — it's an extension of the existing venue page generator.

**Problem 3 — Persistent self-service updates:** A pre-filled Google Form per host, landing in a "Host Updates" sheet that the team reviews before merging. This requires zero new infrastructure, works on any phone, and fits how the OEFF team already operates. An email-link fallback covers the small percentage of hosts who won't use a form.

---

## Problem 1: Secure Host-Facing Pages

### What's actually at risk

The threat model here is: contact info and scholarship data appearing in search engine results, or being accessed by someone who stumbles on the URL. This is not a nation-state threat. It's a casual-access problem. The protection bar is "not googleable and not visible to a curious stranger" — not "secure against a determined attacker."

This distinction matters because it shapes which options are proportionate.

### Option Evaluation

**Option A: Unique URL tokens**
Each host gets a URL like `/hosts/a3f9x7k2` — a short, unguessable string. No password required. Anyone with the link can see the page; the protection is obscurity of the URL itself.

- Fits the OEFF stack completely. Static HTML, no login system, no new infrastructure.
- A one-time script generates one token per venue.
- Maintenance: tokens are stable. Once generated and distributed, they don't expire.
- Host friction: zero. They click a link. Works on any device.
- Risk: if a host forwards their link to someone, that person can see the page. For contact info, this is acceptable. For financial data (scholarships), it is not sufficient on its own.
- **Verdict: Recommended for contact info tier.**

**Option B: Client-side password gate**
Each host page has a JavaScript prompt or form. The page is served publicly but content is hidden until the correct password is entered. Password can be stored as a hashed value in the HTML; the JS compares on entry.

- Fits the stack. Vanilla JS, no server needed.
- Realistic protection: client-side JS is bypassable by anyone who views source or disables JS. This is not real encryption.
- For the actual threat model (keeping info out of search results, casual browsers), it's adequate.
- Host friction: moderate. One extra step, but one they understand — "enter the password we emailed you."
- Maintenance: if a host loses their password, you email it again. Low burden.
- **Verdict: Recommended for financial data (scholarship) tier only.** The extra friction is worth it for the most sensitive category.

**Option C: Cloudflare Access**
Cloudflare Access provides email-based one-time codes. A host navigates to the page, enters their email, receives a code, and gets in.

- Real authentication. Appropriate for genuinely sensitive data.
- **Note:** This would add a new platform dependency — Cloudflare Access — beyond our current static hosting setup.
- Host friction: higher. Requires the host to use the same email they registered with, access their email mid-event, and enter a code. For a day-of reference page, this is a real usability problem.
- Maintenance: Garen would need to manage the Access policy as hosts change emails or contacts.
- **Verdict: Not recommended for 2026.** The friction is disproportionate to the threat model, and it introduces a new infrastructure dependency. Worth revisiting if OEFF moves to an authenticated host portal in a future season.

### Recommendation: Two-tier approach

| Data category | Protection method |
|---------------|------------------|
| Contact info (emails, co-host contacts) | Unique URL token |
| Event logistics (timeline, packet link) | Unique URL token |
| Financial info (scholarship status, amounts) | Unique URL token + client-side password gate |

Scholarship data is the highest-sensitivity category. The two-layer approach (token + password) means an attacker would need both the link and the password — which is reasonable protection for volunteer-festival-scale financial data.

---

## Problem 2: Host Helper Page

### What it is

A distilled, mobile-first one-pager for each host. They pull it up on their phone at 6:45 PM when they can't remember the AV contact's name. It needs to be fast, scannable, and work offline (cached in browser or printed).

### Design recommendation

The host helper should be generated alongside the existing venue sections — same Airtable view (`2026_Venue_Sections`), same script (`generate-venue-sections.py`, the existing venue page generator), but output to a separate file per venue at the token URL path.

It should NOT be a separate pipeline. It's a second template fed by the same data.

### Layout description (mobile-first)

```
+-------------------------------------+
|  [VENUE NAME]                        |
|  April [DATE] . [TIME]               |
|  Film: [TITLE] ([RUNTIME] min)       |
+-------------------------------------+

TONIGHT'S TIMELINE
------------------
[TIME -60]  Venue opens / setup
[TIME -30]  Volunteers arrive
[TIME -15]  Doors open
[TIME]      Film starts
[TIME +RUN] Q&A / close

YOUR KEY CONTACTS
------------------
[HOST NAME]           [email]
[AV CONTACT]          [email]
OEFF line             hosts@oneearthfilmfest.org

YOUR EVENT PAGE
------------------
[RSVP URL as big tap target]
RSVPs as of [DATE]: [COUNT]

SCREENING PACKET
------------------
[LINK -- apr state only, behind token]
Password: [via separate YAMM email]

SOMETHING WRONG?
------------------
Email: hosts@oneearthfilmfest.org
[Pre-filled mailto: "Re: [VENUE NAME] -- [FILM TITLE]"]
```

### Design notes

- Font size minimum 16px — this is read on a phone, often in a dim room.
- All tap targets minimum 44px tall.
- Timeline is the most-used section — put it first after the header.
- RSVP count as a snapshot (from Airtable at generation time), not a live feed. Label it clearly: "RSVPs as of [date]."
- Packet link only appears in `apr` state. An automated build-time check already enforces this.
- Phone numbers are still not in the HTML. Emergency contact is email + hotline hours (same as existing venue sections).
- Print styles: single column, black on white, page breaks between sections.
- The "something wrong?" section with a pre-filled mailto reduces the threshold for hosts to flag errors.

### What needs team input before building

- Confirm the day-of timeline offsets with Ana/Josh (see open question in `host-helper-comparison.md` — mockup uses -90/-60/-45, generator uses -60/-30/-15).
- Confirm whether RSVP count should be snapshot-only or whether daily updates via YAMM email are needed in parallel.
- Confirm whether the helper page should be linked from the main host guide, or distributed only via direct URL.

---

## Problem 3: Persistent Self-Service Updates

### The core tension

Updates need to be easy enough that hosts actually use them, reviewed enough that bad data doesn't enter the master data source, and persistent enough that hosts aren't limited to survey windows.

### Option Evaluation

**Option A: Pre-filled Google Form per host**
Each host gets a Google Form link with their current data pre-populated. They edit and submit. Responses land in a "Host Updates" Google Sheet that the team reviews before merging into V7 (our master Google Sheet).

- Zero new infrastructure. Fits the OEFF stack completely.
- Works on any phone. Hosts already use Google Forms.
- Review step is built-in: responses go to a sheet, team merges manually.
- Pre-filling requires a one-time script to generate the URLs. Buildable now.
- Limitation: pre-filling via URL parameters works for simple fields but breaks for checkboxes and multi-select questions. Keep the form simple (name, email, phone, notes).
- **Verdict: Recommended.**

**Option B: Airtable shared view with inline editing**
Airtable supports shared views with edit permissions scoped to a filtered record set. Each host could theoretically edit their own venue record directly.

- No new infrastructure beyond what's already there.
- Risk: Airtable's UX is unfamiliar to non-technical users. Inline editing in a grid view is confusing for someone who primarily uses a phone and email.
- Risk: A shared edit view for one record is hard to scope correctly — hosts could accidentally see or edit other venues' records if the filter is misconfigured.
- Maintenance: Ana or Garen would need to manage Airtable permissions for 100 hosts.
- **Verdict: Not recommended for 2026.** The UX complexity and permission management burden outweigh the convenience.

**Option C: Simple mailto template**
A link that opens an email with a structured template: "To update your contact info, reply with: Name, Email, Phone, Notes." OEFF team processes manually.

- Zero infrastructure.
- Works for every host on every device.
- Doesn't scale to 100 hosts if many use it simultaneously.
- No review step — it is the review step.
- **Verdict: Recommended as a fallback for hosts who won't use a form.** Not the primary channel, but always available.

**Option D: Cloudflare Worker + JSON log**
A small serverless function accepts form POSTs and appends to a JSON file.

- **Note:** This would require a new serverless function outside our current hosting setup.
- More infrastructure to maintain than the problem warrants.
- Provides no advantage over Google Form + Sheet for OEFF's scale.
- **Verdict: Not recommended. The infrastructure cost exceeds the benefit for ~100 hosts.**

### Recommendation: Google Form primary, mailto fallback

Each host's helper page (or confirmation email) includes:
1. A "Update your info" link that leads to a pre-filled Google Form
2. A "Something wrong? Email us" mailto link with pre-filled subject

The Google Form collects: venue name (pre-filled, locked), contact name, contact email, contact phone, and a free-text notes field. Responses land in a "Host Updates" tab in V7. The team reviews and merges on a weekly cadence during active season (March-April).

Generating the pre-filled form URLs requires a one-time Python script. That script reads from V7 (or Airtable) and outputs a list of (venue_name, form_url) pairs. This is buildable now without new infrastructure.

---

## Data Flow Map

Where sensitive info lives and how it moves:

```
CANONICAL SOURCE
V7 Google Sheets
  +-- Hosts tab: venue name, contact name, contact email, phone, tech tier
  +-- Events_2026: dates, films, RSVP counts, screening packet URLs
  +-- Benefits Tracking: scholarship data (most sensitive)
          |
          v
AIRTABLE (coordination layer)
  +-- Venues table: mirrors Hosts tab, adds linked records
  +-- Events table: pre-joins venue + film + contact
  +-- 2026_Venue_Sections view: output for generator
          |
          v
GENERATOR (generate-venue-sections.py)
  +-- Reads 2026_Venue_Sections view
  +-- Privacy lint: fails build if phone numbers, Dropbox URLs, or packet URLs appear pre-April
  +-- Outputs: venue sections in hosts/index.html + per-venue helper pages
          |
          v
CLOUDFLARE PAGES (public)
  +-- hosts/index.html -- all venue sections (public, no sensitive data)
  +-- hosts/[token]/index.html -- per-venue helper (token-gated, has contact + packet info)
          |
          v (scholarship data only)
  hosts/[token]/index.html -- password gate (JS, client-side)
  Password distributed via separate YAMM email, not stored in HTML
```

**Who sees what:**

| Data | Public (no gate) | Token gate | Password gate |
|------|-----------------|------------|---------------|
| Venue name, film, date | Yes | -- | -- |
| RSVP page link | Yes | -- | -- |
| Contact emails | No | Yes | -- |
| Packet link (Apr only) | No | Yes | -- |
| Co-host contacts | No | Yes | -- |
| Scholarship status/amount | No | No | Yes |

---

## What's Buildable Now vs. Needs Team Input

### Buildable now (no team input needed)

- **Token generation script:** Python `secrets` module, one token per venue, output to a JSON mapping file. Tokens are stable — generate once, store in the mapping file, redeploy if regeneration is needed.
- **Host helper HTML template:** Extension of existing venue section template. Same data fields, different layout.
- **Generator modification:** Add `--helper` flag to `generate-venue-sections.py` to output per-venue helper pages to a `hosts/[token]/` directory structure.
- **Browser password gate:** ~20 lines of vanilla JS. Password stored as a hash in the HTML; plaintext delivered separately via email.
- **Pre-filled form URL generator:** Reads V7/Airtable, outputs form links per venue.
- **Mailto fallback:** Pre-filled subject line template, one line of HTML per venue.

### Needs team input before building

- **Day-of timeline offsets:** Ana/Josh to confirm whether setup window is -90/-60/-45 or -60/-30/-15 minutes before showtime. (See `host-helper-comparison.md`.)
- **Scholarship data inclusion:** Ana/Michael to confirm whether scholarship status should appear in the host helper at all, or remain only in V7/internal docs. If it appears anywhere in the helper, the password gate tier is required.
- **Token distribution plan:** Tokens need to be distributed to hosts. YAMM (Yet Another Mail Merge — our bulk personalized email tool) is the existing mechanism. Does the token go in the confirmation email? The March prep email? A dedicated "your host page is ready" email?
- **RSVP count cadence:** If hosts relied on daily counts to drive marketing, snapshot-only isn't sufficient. Does OEFF want to send daily YAMM emails with current RSVPs during fest week, or is the snapshot acceptable?
- **Update form timing:** When should the pre-filled update form go out? After confirmation, or in the March prep wave?

---

## Infrastructure Notes

No new platform dependencies are required by the recommended approach. All three solutions use tools we already have:
- Static HTML + Cloudflare Pages (existing hosting)
- Python scripts (existing tooling)
- Google Workspace — Forms + Sheets (existing)
- A small amount of vanilla JavaScript for the password gate

If the team later decides to pursue Cloudflare Access or a serverless update handler, those choices would need to be documented as infrastructure decisions before building.

---

## Unexpected Connections

The historical Host Helper stored film file access in "cell 27B" — a confidential link in a spreadsheet that hosts had to find and use. That system relied on obscurity (a specific cell in a document you had to know to look for). The token URL approach is structurally similar — protection through unguessability — but it's intentional and documented rather than accidental. The design philosophy hasn't changed much; what's changed is that it's now explicit and enforced.

---

*Research by OEFF Coordinator agent -- Session sw-20260223-e61f -- February 23, 2026*
*Sources: host-portal-security-design.md, host-helper-comparison.md, venue-view-spec.md, host-onboarding-runbook.md, oeff-knowledge-base-summary.md, oeff-airtable-overview.md, oeff-context-extraction.md*
