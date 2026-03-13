# Host Helper: Then and Now

How the 2026 venue section replaces — and extends — the historical Host Helper.

---

## What the Host Helper Was

A per-venue Excel spreadsheet maintained in `05 Logistics and Venues / Host Helpers` on the OEC Shared Drive. One file per venue, updated manually by Josh and Ana. It combined logistics, film delivery, and emergency info into a single document.

The format question — "Is Excel the best format?" — surfaced repeatedly across meeting notes without resolution. Three possible explanations kept circling: the resources aren't being read, they don't answer the right questions, or hosts just want human contact. That question was never tested with hosts directly.

---

## What It Contained

| Field | How it was maintained | Update cadence |
|-------|----------------------|----------------|
| Venue name | Static, set at creation | Once |
| Event date and time | Added when confirmed | Once |
| Host contact name | Static | Once |
| AV contact | Added by Josh/Ana when known | Once |
| Film assignment | Set when programming finalized | Once |
| Ticket / RSVP counts | Updated manually | Daily before noon during fest week |
| Run of show | Typed manually | Once, sometimes revised |
| Film file download link | Cell 27B, marked "confidential, limited distribution" | Once |
| Emergency contacts | Phone number + on-call staff name | Once |

Not in the Host Helper but maintained separately:

| Item | Where it lived |
|------|---------------|
| Marketing toolkit (flyer, social assets, print PDF) | Separate folder in Shared Drive |
| Webinar registration links | Sent via email |
| Webinar recordings | Sent via email |
| Volunteer coordination | SignUp Genius (managed independently by hosts) |
| Forms (check-in, AV verification, feedback) | Did not exist as structured tools |

---

## What the 2026 Venue Section Does Differently

### Structure

| Then | Now |
|------|-----|
| One Excel file per venue | One section per venue inside the host guide |
| Static — all info visible at all times | Temporal — feb/mar/apr states show what's relevant now |
| No consistent information order | SARC ordering: Status, Asks, Resources, Contacts (every state, every venue) |
| Updated manually by Josh/Ana | Generated from Airtable by script, validated by privacy lint |
| Separate document hosts had to find | Inside the guide hosts already use |

### Content: What Migrated

| Host Helper field | 2026 location | What changed |
|-------------------|---------------|-------------|
| Venue name, date, time | STATUS block (all states) | Confirmed/pending indicators show what's settled vs. in progress |
| Host contact name | STATUS block (feb: pending, mar/apr: confirmed) | Was static text; now shows progression |
| AV contact | STATUS block (same pattern) | Was added manually; now pulled from `Venues.AV_Contact` in Airtable |
| Film assignment | STATUS block, film title row | Same info, now includes runtime for timeline computation |
| Ticket / RSVP counts | STATUS block (apr only) | Was daily manual updates; now a snapshot from Airtable. Live daily counts would need a different pipeline |
| Run of show | RESOURCES block (apr: day-of timeline) | Was manually typed; now computed from event time + film runtime. Offset timings need verification with Ana/Josh |
| Emergency contacts | CONTACTS block (apr) | Email + hotline hours only. Phone number delivered via Mailmeteor, not in the guide. Privacy lint enforces this |

### Content: What Was Deliberately Removed

| Host Helper field | Why it's not in the guide |
|-------------------|--------------------------|
| Film file download link (cell 27B) | Film delivery is now a separate channel: Dropbox link via Mailmeteor email with per-venue password. The guide is for logistics and orientation, not file distribution. Privacy lint fails the build if a Dropbox URL appears in the HTML |
| Phone numbers in emergency contacts | Delivered via Mailmeteor email and screening packet readme. The guide shows email + staffed hours. Privacy lint catches phone number patterns |

### Content: What's New (Host Helper Didn't Have These)

| New element | What it does | State |
|-------------|-------------|-------|
| "Your Focus" callout | Single most important action, visually prominent | All states |
| "What's happening now" context | Brief paragraph explaining the current phase | All states |
| Temporal toggle (feb/mar/apr) | Progressive disclosure — hosts see what's relevant now, can preview what's coming | All states |
| Form links (check-in, AV verification, playback test) | Inline action items with direct links, not emailed separately | Feb, Mar, Apr respectively |
| Marketing asset links | Poster, social kit, press blurb, trailer, discussion guide — linked at the moment they're needed | Mar |
| Volunteer needs (structured) | Roles with counts and status, not free text | Mar |
| Volunteer roster (named) | Named volunteers with assigned roles | Apr |
| Named OEFF staff contacts | Ana (program), Garen (tech), Josh (event liaison) with roles and emails | All states |
| Privacy guardrails | No phone numbers, no Dropbox URLs, no passwords in HTML — build fails if present | Enforced at generation time |

---

## Data Source Change

The Host Helper was maintained in Excel/Sheets with no automation.

The 2026 venue section reads from an Airtable view (`2026_Venue_Sections`) that pre-joins Events, Venues, Films, and Film Contacts. V7 Google Sheets remain canonical — data flows V7 → Airtable → generator → HTML. The view solves the 19/31 missing Film_ID problem that occurred in flat CSV exports.

See `decisions/2026-02-21-venue-pipeline-reads-from-airtable.md` for full rationale.

---

## Open Questions

**Timeline offsets:** The mockup uses -90/-60/-45 min (venue opens / volunteers / doors). The generator uses -60/-30/-15. Which setup window is standard for 2026 community venues? Ana/Josh to confirm.

**Ticket count cadence:** The Host Helper had daily updates before noon during fest week. The 2026 guide shows a snapshot RSVP count from Airtable. If hosts relied on daily counts to drive marketing push, the current design doesn't replace that. Would need either a live-updating field or a daily Mailmeteor email with counts.

**Volunteer data source:** The volunteer roster and structured volunteer needs have no Airtable schema yet. Options: a `Volunteers_2026` table, or a SignUp Genius CSV export keyed by venue name.

**The format question:** "Is Host Helper a documentation problem or a relationship problem?" is still unresolved internally. This design tests both hypotheses — named contacts are the relationship layer, the toggle + SARC is the documentation layer. Measurable signal: do host support emails decrease after this ships?

---

## Files

| File | What |
|------|------|
| `host-guide-venue-mockup.html` | Design mockup with visible annotations (toggle on/off) |
| `generate-venue-sections.py` | Generator script — Airtable → HTML with SARC validation + privacy lint |
| `venue-view-spec.md` | Airtable view field contract |
| `hosts/index.html` | Live guide with sentinel comments for injection |

---

Last updated: 2026-02-22
