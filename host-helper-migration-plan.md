# Host Helper Migration Plan

OEFF 2026 — March 9, 2026 — For Kim + team

---

> **The plan:** Replace the per-venue static HTML pages with Airtable shared grid views — one per venue, each with a unique link that shows only that host's data. The public host guide site (hosts.oneearthfilmfest.org) stays exactly as-is — it serves a different purpose. Use this as an Airtable pilot: two birds, one scone.

> **Why both exist:** The public host guide (hosts.oneearthfilmfest.org) is a designed, static site because host orientation — what to expect, how to prepare, FAQ answers, webinar recordings, marketing toolkit — is the same for every host and benefits from structured navigation and visual design. It's also a single link we can include in any Mailmeteor blast so every host has one place for shared resources. The per-venue helper is a different problem: personalized data that changes over time. That data needs to be live and maintainable by anyone on the team, which is why Airtable is the better tool for it.

> **Why Airtable and not just Sheets:** Sheets is where the team lives and that doesn't change. But Sheets can't give each host a scoped view of only their venue. Airtable shared views can — we create a filtered grid view per venue, each with its own link, so hosts see their data and nothing else. That's the specific capability that earns Airtable a seat here. This isn't a migration away from Sheets. It's adding a presentation layer for hosts on top of data we're already maintaining. If it works well, Airtable earns a bigger role next year. If it doesn't, Sheets is still right there.

> **Decision needed:** This changes the host experience (Airtable link instead of a custom page). Kim maintains the host-facing data in Airtable; Garen creates and manages the per-venue shared views. An example shared view will be ready for review once the first batch of venues are set up. I'd like sign-off from Kim and Ana before we share links with hosts.

**In this doc:**
1. What stays, what changes
2. What hosts have always gotten
3. Static site vs. Airtable shared views
4. Why Airtable is the better path
5. Gap analysis
6. Data readiness
7. Rollout phases

---

## 1. What stays, what changes

| Component | Status |
|-----------|--------|
| Public host guide (hosts.oneearthfilmfest.org) | Stays — general orientation, webinars, resources |
| Old Host Helper format (spreadsheet) | Retired — Airtable view replaces it (example included with this doc) |
| Per-venue static HTML helper pages | Replaced by Airtable shared grid views (one per venue, each with a unique link) |
| Token map + privacy lint system | Archived — reusable if needed later |
| Airtable base (venues, events, films, contacts) | Stays — data source for the interface |
| Mailmeteor email workflow | Stays — merge field changes from token URL to Airtable shared link |
| Kim's comms log + team Sheets | Stays — no change to team workflows |

## 2. What hosts have always gotten

Every year, each host receives a personalized document with their venue-specific details. In past years this was a per-venue Excel spreadsheet in the shared Drive, maintained manually by Josh and Ana.

| Field | How hosts used it | Update cadence |
|-------|-------------------|----------------|
| Film assignment + runtime | Core info — what they're screening | Once |
| Event date and time | Core info | Once |
| Run of show / doors open | Day-of reference — setup through close | Once, sometimes revised |
| RSVP / ticket count | Drove marketing decisions | Daily before noon during fest week |
| Host, AV, and marketing contacts | Day-of reference + coordination | Once |
| OEFF support contact + onsite rep | Day-of escalation | Once |
| Film file / program packet link | How hosts got their screening copy | Once (Dropbox link in the sheet) |
| Venue details (capacity, ADA, parking, transit, WiFi) | Planning + day-of logistics | Once, from intake |
| Volunteer names + signup form + training packet | Recruitment and day-of coordination | Updated as volunteers confirmed |
| Webinar recordings + host prep call schedule | Orientation — linked in column C sidebar | Once, updated as calls happened |
| Marketing toolkit links | Promotion — pre-written text, flyer templates, social handles | Once |
| Supplies + team checklist | Day-of readiness — checkboxes for tables, masks, signage | Once |
| Registration count tracker | Ticket tracking — manual daily entry rows | Daily during fest week |
| Invoice / billing contact | Internal — who to send the venue host fee invoice to | Once |
| T-shirt sizes | Swag coordination | Once |

The old Host Helper was comprehensive — it also included marketing toolkit links, webinar/call recording links, volunteer signup and training links, supplies checklists, COVID protocols, invoice contacts, and a registration count tracker, all in one sheet. Column C served as a running sidebar of key links and notes.

## 3. Static site vs. Airtable shared views

### STATIC SITE — Per-venue HTML pages

Python script pulls data from Airtable, generates a branded HTML page per venue, deploys to Cloudflare Pages. Each host gets a unique URL. Pages have temporal states (feb/mar/apr) that show only what's relevant now.

**What's built:** The public host guide, the generator script, the token map, privacy lint. The per-venue pages are templated but not yet deployed to hosts.

### AIRTABLE SHARED VIEWS — Filtered grid views from existing data

For each venue, Garen creates a grid view in the Events table filtered to that venue and year. Each view gets a shared link — hosts click their link and see only their event data in a clean read-only grid. Data changes appear instantly. No scripts, no deployment pipeline.

**What's built:** The Airtable base already has all the venue, event, film, and contact data. Shared grid views are available on our current plan tier. Internal fields (financial, licensing, pipeline status) are hidden from the shared views.

## 4. Why Airtable is the better path

### What Airtable gains

- **Live ticket counts:** If wired to Eventbrite, RSVP numbers update automatically — no more daily manual entry.
- **Instant updates:** Fix a typo, add a contact, change a time — hosts see it immediately.
- **Anyone can maintain it:** No technical handoff documentation needed. If you can use Airtable, you can update host-facing data.
- **Lower risk at festival time:** Seven weeks out, a simpler system with fewer moving parts is the safer choice.

### What Airtable gives up

- **Design control:** Airtable grid views are clean but generic — hosts won't see OEFF branding, but they will see correct, live data.
- **Offline access:** Hosts need internet to see their page. No cached/printable fallback.
- **Temporal states:** The static site showed hosts only what mattered right now (confirmed → prep → ready). Airtable grid views show all visible fields at once — no progressive disclosure.

### Why the tradeoff favors Airtable

The static site requires a specific person to operate. Updating host data means: edit Airtable, run a Python script, commit the output, push to git, wait for Cloudflare to deploy. Any OEFF team member can do step one. Steps two through five require someone comfortable with a command line. If that person isn't available, host data doesn't update.

Airtable removes the pipeline entirely. Data lives in Airtable. Hosts see a shared grid view filtered to their venue. When someone updates a field, hosts see the change. No build step, no deploy, no git. Kim, Ana, or Josh can update host-facing data directly.

## 5. Gap analysis

| Data / Feature | Old Helper (Excel) | Static | Airtable |
|----------------|-------------------|--------|----------|
| Venue, date, time, film | Yes | Yes | Yes |
| Run of show / timeline | Manual | Auto-computed | Formula field or manual |
| Host + AV contacts | Yes | Yes (token-gated) | Yes (scoped view) |
| RSVP / ticket counts | Daily manual | Snapshot at build | Can be live via sync |
| Film file / screening packet | Cell 27B | Token-gated, April only | URL field, visible when populated |
| Scholarship / financial data | Separate email | Password-gated section | Excluded from shared view |
| Emergency contacts | Phone + name | Email only (privacy lint) | Controlled by field visibility in shared view |
| Marketing assets | Separate Drive folder | Inline links, March state | URL or attachment fields |
| "Your Focus" callout | Did not exist | Yes | Not available in grid view |
| Temporal / progressive disclosure | No | Yes (feb/mar/apr) | No — grid views show all visible fields |
| Mobile-friendly | No (Excel) | Yes, works offline | Yes, requires internet |
| Host self-service updates | Email Josh/Ana | Pre-filled Google Form | Could allow limited editing |
| Maintainable without Garen | Yes | No | Yes |

## 6. Data readiness

Regardless of front end, this is what needs to be current in Airtable before host-facing views go live. The old host helper spreadsheets had more fields than just the scheduling core — hosts used them for day-of reference, marketing, and volunteer coordination. The full inventory:

### Scheduling + film core

| Data | Status |
|------|--------|
| Venue name, address, region | Complete (22 of 22) |
| Event date and time | Complete (22 of 22) |
| Film assignment | Complete (22 of 22) |
| Film runtime | **Not in any structured data source.** No runtime column in the Films table or any CSV. Needs to be added and populated from film websites or filmmaker survey responses. Blocks run-of-show computation. |
| Eventbrite event URL | 14 of 22 published. 8 not yet created — ~5 just need creating, ~3 blocked on venue or contact gaps. |
| Screening packet link | Not yet — blocked on film delivery (April) |
| RSVP / ticket counts | Live via Eventbrite sync (replaces daily manual entry) |
| Chasing Time film record | **Missing from Films table entirely** — assigned to 3 venues but has no F26 record. Needs to be added. |

### Contacts + team

| Data | Status |
|------|--------|
| Primary host contact (name, email, cell) | 21 of 22 have name + email across sources (intake forms, roadmap, 2025 host helpers). 7 have cell numbers (from 2025 sheets). Only CAM has zero contact anywhere. **4 venues have different contacts in 2025 vs 2026** (Oak Park, Bethel, Dominican, Go Green) — needs direct verification with the venue. |
| AV / tech contact | 10 named contacts recovered from 2025 host helper sheets — all need verification. 8 venues still have no AV contact in any source. The 2026 intake form captures "Has AV Lead" as a boolean but not a name or email. |
| Marketing contact | Partial — from intake responses |
| OEFF support contact | Known |
| OEFF rep (onsite day-of) | Not yet assigned |
| Volunteers assigned to event | Not yet — volunteer recruitment in progress |

### Venue operations (from host intake)

| Data | Status |
|------|--------|
| Venue capacity | Partial — some corrected by intake responses |
| Venue description | Partial — from intake responses |
| Parking info | Partial — from intake responses |
| Public transit info | Partial — from intake responses |
| Wayfinding / entry instructions | Partial — from intake responses |
| ADA compliance + accessible seating | Partial — from intake responses |
| Public vs private event | Partial — from intake responses |
| Doors open time | Not yet — depends on run of show |
| WiFi credentials | Partial — from intake responses |

### Moving out of the per-venue view

The old host helper put everything in one sheet. For 2026, some of this lives elsewhere — either because it's the same for every host (belongs on the public host guide) or because it's internal (doesn't need to be host-facing).

| Data | Old location | 2026 location |
|------|-------------|---------------|
| Webinar recordings + host prep call schedule | Column C sidebar in each sheet | Public host guide site (hosts.oneearthfilmfest.org) — one link for all hosts |
| Marketing toolkit | Rows 44-48 in each sheet | Public host guide site or URL fields in Airtable when ready |
| Volunteer signup form + training packet | Cell C9 in each sheet | Separate forms, linked from host guide |
| Supplies + team checklist | Rows 54-59 in each sheet | TBD — could be a host guide section or Airtable checklist |
| T-shirt sizes | Row 6 in each sheet | Internal tracking |
| Invoice / billing contact | Row 25 in each sheet | Internal — separate from host-facing view |
| Donations, photographer permissions | Rows 22-23 in each sheet | Internal operational flags |
| COVID protocols | Rows 51-53 in each sheet | Dropped for 2026 (no longer required) |

## 7. Rollout phases

### Phase 1: Get the data right

Before hosts see anything new, the underlying data needs to be current. Not everything is equally urgent.

| Priority | Data | Why |
|----------|------|-----|
| **Urgent — we need this** | Host contact info verified for all 22 venues | 21 of 22 have data somewhere — but 4 venues have different people in 2025 vs 2026 records. CAM has zero. Verification needs to go directly to venues (not through Ana/Josh — they don't know). |
| **Urgent — we need this** | Film runtimes added to Films table | No runtime exists in any data source. Needs a field added and populated. Blocks run-of-show. |
| **Urgent — we need this** | Chasing Time added to Films table | Assigned to 3 venues, no F26 record exists |
| **Urgent — hosts need this** | Event date, time, film assignment | Core info hosts plan around — already complete |
| **Urgent — hosts need this** | Eventbrite event URLs (remaining 8 of 22) | ~5 just need creating. ~3 blocked on venue/contact gaps. |
| **First priorities** | AV / tech contact per venue | 10 named contacts recovered from 2025 sheets — all need verification. 8 venues have none. |
| **First priorities** | Venue capacity (corrected) | Some intake responses corrected original estimates |
| **First priorities** | Run of show / doors open time | Can be computed from event time + runtime once runtimes are verified |
| **First priorities** | OEFF rep assignment per venue | Hosts need to know who's onsite day-of |
| **First priorities** | Venue operations fields (parking, transit, ADA, wayfinding) | Already partially captured in intake — needs Airtable migration |
| **Later** | Screening packet links | Blocked on film delivery pipeline — April delivery |
| **Later** | Volunteer assignments per event | Blocked on volunteer recruitment |
| **Later** | Marketing assets (poster, social kit) | Can be added as URLs when ready |

### Phase 2: Build and pilot the shared views

For each venue, Garen creates a grid view in the Events table — filtered to that venue, with internal fields hidden and host-facing fields visible. Each view gets a shared link that gives hosts read-only access to only their event data. This is a presentation layer on top of data we're already maintaining in Airtable. It doesn't require anyone to change their current workflow.

The team's operational infrastructure stays in Google Sheets. Kim's comms log stays in Sheets. Nobody adopts Airtable as a daily tool. The shared views are for hosts — a way to give them a clean, up-to-date view of their venue data without building custom pages.

This is also a pilot. If it works well this year, Airtable becomes a real option for next year's host system from the start. If it doesn't, we've learned that cheaply.

| Step | Who | Effort | Type |
|------|-----|--------|------|
| Create per-venue grid views with filters + hidden fields | Garen | 1-2 hours | One-time setup |
| Generate shared link for each venue view | Garen | 30 min | One-time setup |
| Verify each link shows only that venue's data | Garen | 30 min | One-time setup |
| Internal review — Kim + Garen look at a sample view together | Kim + Garen | 30 min | One-time review |

### Phase 3: Share with hosts, interns handle validation

As venues are ready — data verified, contacts confirmed, event page published — we share their Airtable view link. This doesn't have to be all at once. Venues can be turned on as they're ready.

| Step | Who | Effort | Type |
|------|-----|--------|------|
| Add Airtable shared links to Mailmeteor merge sheet | Kim | 30 min | One-time setup |
| Test with 1-2 real hosts before broader send | Kim + Garen | 1 day turnaround | One-time validation |
| Send "Your screening page is ready" emails as venues are ready | Kim | Per existing SOP | Ongoing |
| Validate venue data: contacts current, times correct, links working | Interns | Ongoing | Ongoing maintenance |
| Flag data gaps and follow up with hosts for missing info | Interns | Ongoing | Ongoing maintenance |

Intern work is the detail layer — checking that every field is populated, every link works, every contact email is current. This is exactly the kind of structured, repeatable task that scales with people rather than with technical infrastructure.

---

*Prepared March 9, 2026. For discussion with Kim and team.*
