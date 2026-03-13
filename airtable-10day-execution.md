# OEFF Airtable — 10-Day Execution Plan

> Synthesized from: ChatGPT advisory (Mar 7), Garen's Phase 0-4 plan, Operational Intent matrix, and existing build infrastructure.
> Festival: April 22-27 (46 days). Today: March 7, 2026.

## Governing rule

Airtable is our operations visibility layer, not our entire workflow. V7 Sheets stays canonical for editing through April. Airtable answers questions; it doesn't replace the tools people already use.

---

## Day 1 — Delete dead tables + scope lock

**Already done:** 278 records cleared, 12 tables emptied, Milestones retired into Merged Timeline (Mar 6 session).

**Remaining:**
- [ ] Delete all 16 `[DELETE]`-prefixed shell tables in Airtable UI (API can't delete tables)
- [ ] Delete empty shells: Budget, Festival Metrics, Volunteers
- [ ] Delete Partners table (121 records already cleared, 29 kept — verify those 29 moved or aren't needed)
- [ ] Write scope sentence at top of base description: "Operations visibility layer — event tracking, venue readiness, film assignment, contact ownership, status tracking. Not for notes, documentation, or media processing."

**Tool:** Browser (manual deletion). ~30 min.

---

## Day 2 — Run data population scripts

**Already built:** `oeff-airtable-build.py` has all these flags.

```bash
# Dry run first, then --apply
python3 ~/tools/oeff-airtable-build.py --seed-hosts          # populate Host Contacts
python3 ~/tools/oeff-airtable-build.py --link-hosts           # match contacts → venues
python3 ~/tools/oeff-airtable-build.py --populate-tickets     # Eventbrite URLs → Events
python3 ~/tools/oeff-airtable-build.py --populate-venues      # passwords + tokens → Venues
python3 ~/tools/oeff-airtable-build.py --cleanup              # standardize select colors
python3 ~/tools/oeff-airtable-build.py --archive              # add Archive Status field
```

- [ ] Run each in dry-run mode, review output
- [ ] Run each with `--apply`
- [ ] Run audit mode after: `python3 ~/tools/oeff-airtable-build.py` — note gap counts

**Tool:** Terminal. ~1 hr including review.

---

## Day 3 — Fill critical fields manually

The scripts handle contacts, tickets, and venue tokens. What's left is judgment work:

- [ ] **OEFF Rep assignment** for all 28 events (need Garen's assignment logic — Josh: host-facing, Erin: accessibility-flagged, Garen: tech-heavy, Ana: flagships, Kim: comms-heavy)
- [ ] **Film assignments** — 57% of events are missing these. Pull from OEC Active Roadmap and enter.
- [ ] **Venue contact gaps** — 93% missing. Cross-reference intake forms, email threads, webinar attendance.

**Delegation opportunity:** Contact entry and film linking are data entry, not judgment. If Kim or an intern can do this from a source list, hand it off.

**Output:** A count of remaining gaps. The base starts becoming real.

---

## Day 4 — Build "missing data" triage views

Create filtered views that make cleanup visible and finite:

**Events table:**
- [ ] "Missing Film Assignment" — filter: Film field is empty, Status != Cancelled
- [ ] "Missing OEFF Rep" — filter: OEFF Rep is empty
- [ ] "Needs Date Confirmation" — filter: Date is empty or Status = "TBD"

**Venues table:**
- [ ] "Missing Contact Info" — filter: Primary Contact is empty
- [ ] "No Packet Status" — filter: Packet Status is empty, has linked Event

**Films table:**
- [ ] "Missing Caption Status" — filter: Caption Status is empty

**Output:** One place to say "these are the remaining holes." Shareable with anyone doing data entry.

**Tool:** Browser. ~45 min.

---

## Day 5 — Standardize statuses + color system

**Already coded:** `STATUS_COLORS` in `oeff-airtable-build.py`:

| Status | Airtable Color | Meaning |
|--------|---------------|---------|
| Confirmed / Complete / Delivered / Done | greenBright | No action needed |
| In Progress / Active | blueBright | Being worked on |
| Pending / Waiting / Contacted | yellowBright | Needs external input |
| Blocked / At Risk / Overdue | redBright | Immediate attention |
| Not Started / Unknown | grayBright | Not yet begun |
| Archived / Inactive | grayDark1 | Historical |

- [ ] Run `--cleanup --apply` if not already done on Day 2
- [ ] Manually verify colors render correctly in browser
- [ ] Check that every status field across Events, Films, Venues, Deliverables, Merged Timeline uses this same vocabulary — no table-specific synonyms

**Resist:** Don't create sub-status systems. If you need packet tracking, use a separate Packet Status field with its own 3-value set (Not Sent / Sent / Confirmed), not a 12-option mega-status.

---

## Day 6 — Build the three operational views

These are views (not interfaces) — the raw working surfaces.

### Festival Calendar
- [ ] Calendar view on Events table, date field = Event Date
- [ ] Color by Event Status
- [ ] Must show: date, event name, venue, status, OEFF rep

### Host Readiness
- [ ] Kanban view on Venues table, grouped by Comms Status (or Readiness)
- [ ] Must answer: who needs follow-up, which venues are risky, where contact info is missing

### Film + Accessibility Status
- [ ] Grid view on Films table showing: Film Title, Caption Status, QC Status, Format, Runtime, linked Events
- [ ] Must answer: which events lack confirmed films, which films lack captions

**Output:** Three views a team member can open and use without explanation.

---

## Day 7 — Build Interface: Festival Pulse (Ana)

**From the intent matrix:** Ana needs risk, blockers, and whether the team can execute without her. She reviews, doesn't edit. Summary-level only.

Layout in Interface Designer:
- [ ] **Top row:** 4 number elements — Films confirmed, Events scheduled, Venues with contacts, Overdue milestones
- [ ] **Middle:** Merged Timeline grid filtered to: Status != Done AND Planned Date <= today+7, sorted by Risk desc
- [ ] **Bottom:** Events grid filtered to: Status != Confirmed, grouped by what's missing (no film? no venue? no rep?)

**Do not include:** every field, long notes, technical fields, raw data tables.

**Test:** Can Ana answer "are we on track?" in under 10 seconds? If not, simplify.

---

## Day 8 — Build Interface: Host Operations (Josh + Kim)

**From the intent matrix:** Josh is overloaded. He needs to see which hosts require action without triaging a full list. Kim works from Google Sheets but could use a read-only status view.

Layout in Interface Designer:
- [ ] **Top:** Host Contacts grid filtered to Comms Status = "New" or "Unresponsive" or empty
- [ ] **Middle:** Venues grid grouped by Comms Status (or Kanban if Interface Designer supports it — check)
- [ ] **Bottom:** Recent Host Intake submissions sorted by date

**Test:** Can Josh answer "who do I need to contact today?" in under 10 seconds?

**Note:** This is the only interface Kim might use. Keep it clean enough for someone new to the system.

---

## Day 9 — Stress test with real events

Pick 5 actual upcoming events. For each one, answer:

- [ ] Can I tell who owns this event? (OEFF Rep)
- [ ] Can I tell whether the venue is ready? (Contact, Packet Status)
- [ ] Can I tell which film is assigned? (Film link)
- [ ] Can I tell whether captions/accessibility are accounted for? (Caption Status)
- [ ] Can I tell whether a packet has been sent? (Packet Status)
- [ ] Can I see what's missing without clicking into the record?

**For each failure:** write down whether it's a missing field, a missing view filter, a confusing label, or a structural issue.

**Output:** A short fix list. Execute the fixes same day if they're small.

---

## Day 10 — Lock v1 and write the usage guide

- [ ] Mark this as "Pre-Festival v1" in base description
- [ ] Retire or hide the 5 old interfaces that are now superseded (Pipeline Dashboard, Host Readiness, Film Status, Support Triage, Merged Timeline) — or keep any that still serve a purpose the new ones don't
- [ ] Write a usage guide (one page max):

```
## OEFF Airtable — How to Use This

### What Airtable is for
Event tracking, venue readiness, film assignments, contact ownership, status at a glance.

### What still lives elsewhere
- Day-to-day schedule editing → V7 Google Sheets
- Host comms/mail merge → Google Sheets + Mailmeteor
- Long-form docs → Google Docs
- Film processing details → Garen's scripts

### Where to look
- "Festival Pulse" — are we on track? (Ana, leadership)
- "Host Operations" — who needs what? (Josh, Kim)
- Festival Calendar view — what's happening when?
- Triage views — what data is missing?

### What the colors mean
Green = done. Blue = in progress. Yellow = waiting. Red = at risk. Gray = not started.

### Who updates what
- Garen: structure, scripts, data pipeline
- Josh: venue contacts, host comms status
- Erin: film/caption status updates
- Kim: host outreach status (in Sheets, synced by Garen)
```

- [ ] Share the guide with the team (Google Doc push or direct message)

---

## What's deferred (intentionally)

| Item | Why | When |
|------|-----|------|
| Erin's Film + Accessibility interface | Views cover her needs for now; interface is Phase 2 post-lock | After Day 10 if time allows |
| Garen's Tech Command interface | Garen works from raw views + scripts, not interfaces | Post-festival or never |
| Automations (overdue detection, intake notifications) | Data must be clean before automations are trustworthy | After stress test confirms data quality |
| Venue tier (T1-T4) field | No assignments exist yet; needs Josh/Ana input | When tier decisions are made |
| Film licensing budget tracking | Ceiling unresolved — awaiting Ana | When Ana decides |
| Host-as-Contributor model (Direction 4) | Operationally risky during ramp | Late-season pilot at earliest |
| Warm-Stack template extraction (Direction 1) | Post-festival work | May+ |
| Post-event archive tables (Direction 2) | Snapshot table can be added in April | April 1 |

---

## Minimal success criteria

By end of Day 10:
- [ ] Every live event has a venue assigned
- [ ] Every live event has a film assignment or an explicit "TBD — [reason]"
- [ ] Every venue has at least one real contact
- [ ] Every event has an OEFF rep
- [ ] Risky/incomplete events are visible in one view without clicking around
- [ ] Ana can check festival status without asking Garen
- [ ] Josh can see his contact queue without cross-referencing sheets

---

## Ownership

| Layer | Who |
|-------|-----|
| Structure, status logic, interfaces, scripts, validation | Garen |
| Contact entry, rep assignment, packet status | Josh (or delegated to Kim/intern) |
| Film links, caption/runtime/asset fields | Erin (or delegated with source materials) |
| Triage of ambiguous records | Garen |
| Final review of interfaces | Ana (Festival Pulse), Josh (Host Ops) |
