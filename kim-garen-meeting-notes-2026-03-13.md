# Kim + Garen — Meeting Notes

Running doc. Reverse chronological. Both edit.

## Standing resources

| Resource | Link |
|----------|------|
| OEC Active Roadmap | [Roadmap](https://docs.google.com/spreadsheets/d/1uYJw8Whx29PQ6EpxWp8sUO_wRnhDx5-p0gROnyWU7Qg/edit) |
| Host email content sheet | [Content sheet](https://docs.google.com/spreadsheets/d/1FbRiZWshI_v-whMrCqBGOy4HH-VsfOjmEBlGE4FCYmc/edit) |
| Host guide (live site) | [hosts.oneearthfilmfest.org](https://hosts.oneearthfilmfest.org) |
| Host Helper interface | [Host Helper](https://airtable.com/app9DymWrbAQaHH0K/shrWiUJZFqE6ugneb) |
| Host Confirmations form | [Form](https://airtable.com/app9DymWrbAQaHH0K/shryhEHxXJ4mJdVfd) |
| Host Helper walkthrough | [Walkthrough doc](https://docs.google.com/document/d/1HcPPq2vbvmfIku9jbWYAN07e2daVI0kLOhzCnZieQPA/edit) |
| Host intake form | Google Form |
| Kim's tracker sheet | _(Kim's Google Sheet — screenings, contacts, venues, films)_ |
| Kim's resource hub | Resource Hub |
| Squad meeting (11a Weds) | Zoom |

---

## Mar 13, 2026 — Host Helper walkthrough + data architecture discovery (1 hr)

**Present:** Kim, Garen
**Festival countdown:** 40 days (Apr 22)

### What we covered

Walked through the Host Helper interface, form submission flow, and data layer spec. The call naturally shifted from "how does the host helper look" to "what's the right data architecture." Kim brought strong architecture thinking — her Google Sheets tracker already models the event-centric approach we landed on.

### Decisions

| Decision | Notes |
|----------|-------|
| Architecture: event-centric, not venue-centric | Events are the relational key linking venues, films, and contacts. Kim's tracker already models this. |
| "Directory" for contacts | One people table with type field (host, filmmaker, AV, marketing, partner, collaborator). Primary/secondary distinction. Hosts ≠ venues (BGE hosts at Patagonia). |
| Flagship vs Community: keep | Team support level distinction. Separate from T1-T4 (technical capability). |
| T1/T2 badges: hide from host view | Hosts don't need to see tier classifications. |
| Events (not screenings) as table name | More general — captures action fair, panels, non-screening events. Screenings may be a subtype. Open for further discussion. |
| Per-event interfaces | Moving toward per-event Airtable interfaces rather than shared grid views. Better isolation and presentation. |
| Host helper rollout target | Friday, March 20 |
| Data import approach | Mirror Airtable to Kim's validated Google Sheets structure. Rest of existing Airtable data treated as semi-validated corpus to pull from as needed. |

### Action items

| # | What | Who | By when |
|---|------|-----|---------|
| 1 | Clean up tracker sheet, notify Garen when ready for import | Kim | This weekend |
| 2 | Import Kim's validated data into Airtable, reorganize around event-centric model | Garen | Before next meeting |
| 3 | Write spec for per-event interfaces (fields, layout, data flow) | Garen | Before next meeting |
| 4 | Send recap of this call | Garen | Today |
| 5 | Airtable plan to Ana (updated with event-centric architecture) | Garen + Kim | Monday Mar 16 |
| 6 | Meet to finalize architecture + host helper fields | Garen + Kim | Early next week (Mon/Tue) |

### Insights

- **Kim's architecture was the unlock.** Her tracker uses validated dropdowns (contacts, venues, films) feeding into a screenings table. No free-text input at the screenings level — everything is pre-validated elsewhere. This is the right model.
- **"Events is the key that unlocks"** — Kim's phrase. Events link to everything; venues, films, and contacts are the persistent year-over-year master data.
- **Directory concept addresses a known gap.** OEFF has never had a central contacts source of truth. Kim proposed collapsing hosts, filmmakers, AV contacts, partners into one directory with a type/role field. She also distinguished between "people we work with" (partners/collaborators) and "people we work for" (members/audience).
- **Hosts ≠ venues.** Kim pointed out BGE hosts at Patagonia — host org and venue are different entities. This is why contacts and venues need separate tables.
- **Primary/secondary contacts** apply to both hosts and filmmakers. Distributor is primary for film business; filmmaker is primary for programming.
- **Kim's tracker may look duplicative but isn't.** She acknowledged it might overlap with existing data, but she needed it to do host comms. Garen confirmed: this is the missing piece, not duplication.
- **Shared views hit a wall.** Airtable shared grid views lock to column layout — can't reorganize fields for a prettier per-venue display. Interface Designer can't scope to one record. Per-event interfaces (or miniExtensions) are the path forward.

### Notes

- The interface deep links (`?F8hUa=recordId`) scroll to a venue but don't isolate — all venues visible in sidebar. Need true isolation before sending to hosts.
- Form submissions land in Host Confirmations table (unlinked from Venues). Merge step is manual — Kim would copy data from submission into venue record. Intentional for now (review before publishing), but worth automating later.
- Formula fixes (12 formulas) are written in `host-helper-formula-fixes.md` — ready to paste into Airtable field editor. Fixes placeholder tone, comma artifacts, truncated times.
- Kim interested in adding a "Resources and Materials" section to the interface — webinar recordings, program visioning call notes, decks. These link through films (film-specific materials) or are universal (webinars apply to everyone).

### Parking lot

| Item | Owner | Date parked | Status |
|------|-------|-------------|--------|
| miniExtensions for per-record public URLs | Garen | Mar 13 | To evaluate |
| "Events" vs "screenings" naming — deeper conversation | Both | Mar 13 | Open |
| Automations: are the 3 automations actually built and running? | Garen | Mar 13 | Verify |
| Contact type field naming (Kim uses "contact type" for primary/secondary already) | Both | Mar 13 | Open — figure out when building |
| Members table (14k email list) — separate from partners/directory | Both | Mar 13 | Future |

---

## Mar 3, 2026 — Week 1 Check-in (50 min)

**Present:** Kim, Garen

### Decisions

| Decision | Notes |
|----------|-------|
| _(no decisions recorded)_ | |

### Action items

| # | What | Who | By when |
|---|------|-----|---------|
| _(none recorded)_ | | |

### Notes

_(Meeting happened but notes were not captured in this doc.)_

---

## Mar 1, 2026 — Week 1 Check-in

**Present:** Kim, Garen

### Action items

| # | What | Who | By when |
|---|------|-----|---------|
| 1 | Schedule 1:1 with Ana | Kim | This week |
| 2 | Schedule Garen/Kim/Ana three-way | Garen | This week |
| 3 | Provide existing datasets — roadmap | Garen | This week |
| 4 | Add squad meeting link/info to top of this doc | Garen | ASAP |
| 5 | Finalize Kim's resource hub and link at top of this doc | Garen | ASAP |
| 6 | Finalize draft contract and send | Garen | Sun AM (Mar 2) |
| 7 | Share Airtable (host-specific views) with Kim — with caveat re: sync & migration constraints | Garen | This week |
| 8 | Send 30-min-before-call follow-up (standing practice) | Kim | Ongoing |
| 9 | Ongoing process documentation — not a dedicated deliverable, more likely end-of-fest timing | Kim | Ongoing |

### Decisions

| Decision | Notes |
|----------|-------|
| Approval routing — data/links | Josh validates (could also be intern role) |
| Approval routing — copy (repeatable/templateable) | Sign-off from Garen and/or Ana depending on audience |
| Approval routing — follow-ups | Don't need Josh — avoid bottlenecks |
| Kim's process documentation | Ongoing, not a dedicated deliverable — end-of-fest timing more likely |

### Notes

- More project management capacity needed — no resolution yet.
- Kim's 1:1 with Ana will detail process workflow and visioning for the rest of the festival.
- Garen walked Kim through the host email content sheet (per-webinar merge data).
- Josh can support with Zoom meeting links and other data contingencies for emails.

### Mailmeteor — setup

| What | Status |
|------|--------|
| Set OEC/OEFF alias as default sender | To do |
| Add hosts account | To do |
| Switch default account BACK after setup | To do |

### Parking lot

| Item | Owner | Date parked | Status |
|------|-------|-------------|--------|
| Alias vs. non-alias approach for Mailmeteor sends | Garen | Mar 1 | Parked |
| Sharing Mailmeteor with rest of team | Garen | Mar 1 | Parked |
| Process documentation timeline/format | Kim | Mar 1 | Ongoing — revisit end of fest |

---

## Standing context

- **Running question:** What questions are coming up for you — about the work, the process, how information gets to you, any of it?
- **Non-tactical placeholder:** Reserve 2-5 min each meeting for something beyond this week.
- **Meeting labels:** D = decision needed, Disc = discussion, I = info sharing
