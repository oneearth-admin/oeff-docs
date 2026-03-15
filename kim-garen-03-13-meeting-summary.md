# Kim + Garen — March 13, 2026 Meeting Summary

**Duration:** 63 minutes (3:15–4:18 PM)
**Present:** Kim Pham, Garen Hudson
**Format:** Video call — Host Helper walkthrough → data architecture pivot
**Festival countdown:** 40 days (April 22)

---

## What happened

This meeting started as a Host Helper walkthrough but pivoted into a foundational data architecture conversation. Kim's data modeling experience surfaced a cleaner hierarchy than what Garen had been building toward. The call produced 7 architectural decisions and agreement on a March 20 rollout target.

---

## Decisions

| # | Decision | Detail | Timestamp |
|---|----------|--------|-----------|
| 1 | **Events as relational key** | Events/screenings are the most specific data level. They link to master tables (venues, films, contacts) rather than the reverse. Kim: "The most specific our data will ever get is by event." | ~26:36 |
| 2 | **Unified directory** | All people-data in one table ("Directory") with a Contact Type field, replacing scattered host/venue/filmmaker contact lists. Kim: "What if we just called this table a directory?" | ~52:56 |
| 3 | **Partnership categorization** | Collaborators (mission-oriented, working in step) vs. transactional contacts (filmmakers where "we send money so you can give us this thing"). Garen named the distinction; Kim found "collaborator" as the term. | ~51:04 |
| 4 | **Members vs Partners** | 14k email list = members (who we work for). Active stakeholders = partners (who we work with). Different interaction levels, different data needs. Kim: "Distinguish who we work with and who we work for." | ~48:32 |
| 5 | **Per-event interface pages** | Replace 24 shared views with event-centric Interface Designer pages. Shared views are locked to master grid column layout — too rigid. Per-event tables + interfaces give Kim direct edit access. | ~31:24, ~1:01:04 |
| 6 | **Dual venue classification** | Flagship/Community (team presence level) alongside T1–T4 (technical needs). Two separate systems, not competing. Garen: "Flagship vs community is a teamwide distinction." Kim confirmed. | ~11:48 |
| 7 | **"Events" umbrella term** | "Screenings" becomes a subtype of "events." Events covers action fairs, concerts, panels. Future-proofs the data model. Garen: "A screening is a subtype of an event." | ~43:36 |

---

## Action items

| # | What | Who | By when |
|---|------|-----|---------|
| 1 | Clean up tracker sheet, notify Garen when ready for import | Kim | Today (Mar 13) |
| 2 | Pull Kim's cleaned data into Airtable, begin reorganizing per new architecture | Garen | Before next meeting |
| 3 | Write spec for per-event interfaces — fields, layout, data sourcing | Garen | Before next meeting |
| 4 | Send meeting recap | Garen | Today |
| 5 | Schedule early-week meeting (Mon or Tue) | Both | This weekend |
| 6 | Shore up architecture + Host Helper fields at next meeting | Both | Mon/Tue |
| 7 | **Roll out Host Helper to hosts** | Both | **Friday, March 20** |

---

## Open questions

| Question | Context | Owner |
|----------|---------|-------|
| Where do filmmakers live — Directory table or separate? | Kim asked; not resolved. Garen noted filmmakers sometimes attend events (filmmaker toast). Directory with Contact Type field seems likely but needs confirmation. | Garen + Kim |
| Contact Type field naming | Kim currently uses "Contact Type" for primary/secondary distinction. Need separate fields: one for role (host/filmmaker/venue/panelist), one for priority (primary/secondary/marketing/AV). | Kim + Garen |
| "Events" vs "Screenings" terminology — when to finalize? | Agreed "events" is better umbrella, but Garen flagged "this deserves a larger conversation." Impacts labels across all tools. | Both |
| Does a directory already exist somewhere? | Garen: "I'm 90% sure it hasn't been solved for." Kim: "Maybe Anna's brain." Low risk of duplication, but worth asking Ana. | Garen |
| Per-event tables vs per-event Interface Designer pages | Garen floated per-event tables at ~32:12. This is architecturally risky (22+ tables, no rollups via API). Interface Designer pages with record-parameter deep links may achieve the same UX without the table proliferation. Needs spec. | Garen |

---

## Key quotes

> **Kim (~26:36):** "The most specific our data will ever get is by event."

> **Kim (~25:48):** "You can't add anything new to screenings. It's all like data dropdown values. So you're making sure whatever you've input has been pre-validated."

> **Kim (~52:56):** "What if we just called this table a directory?"

> **Kim (~49:04):** "Distinguish who we work with and who we work for."

> **Garen (~40:48):** "I think you just basically solved something that is one of the core threads that has been a point of friction with all of this."

> **Garen (~1:00:48):** "We're starting at Host Helper — oh wait, actually this isn't quite about Host Helper yet because we still haven't solved this larger architectural piece."

---

## Data hierarchy — agreed model

```
Master Tables (persistent, year-over-year):
├── Directory (all people — Contact Type + Priority fields)
├── Venues (physical spaces — capacity, ADA, AV, address)
├── Films (titles, runtimes, licensing)
├── Members (14k email list — separate from active partners)
│
└── Events (relational key — links to all master tables)
    ├── Screenings (subtype)
    ├── Action Fairs (subtype)
    ├── Concerts (subtype)
    └── etc.
```

---

## Meeting dynamics

This call shifted from a walkthrough into a co-design session. Kim brought structured data modeling thinking (dropdown validation, relational keys, pre-validated inputs) that Garen recognized as solving a long-standing architectural friction. The pivot happened organically — Kim's "events as the most specific level" insight reframed the entire data hierarchy. Both left energized, with clear next steps and a realistic timeline.

Kim's willingness to say "this might be duplicative but I needed it" and Garen's response ("I think you've solved it") set a healthy collaborative tone — practical, not precious about prior work.
