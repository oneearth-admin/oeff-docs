# OEFF 2026 Filmmaker Pipeline — Overview & Index

**Date:** 2026-03-12 (41 days to festival)
**Author:** Garen
**Audience:** Ana (decisions + dashboard), Garen (execution), Kim (follow-ups), Interns (QC)

---

## What This Is

A complete operational system for getting 13 films from "outreach sent" to "screening-ready file confirmed at every venue." Initial outreach went out March 5. This pipeline covers everything from here through festival week (April 22-27).

The system is split into focused documents — each built for its audience. This overview connects them.

---

## Document Map

| Document | Audience | What It Covers | Location |
|----------|----------|----------------|----------|
| **Delivery Process** | Garen, Ana, Kim | 6-phase workflow: responses → licensing → file collection → QC → captions → venue delivery | `filmmaker-delivery-process.md` |
| **Caption Policy** | Filmmakers | What to send, the 4 caption scenarios, caption lock rule, specs | `caption-policy.md` |
| **Caption QC Checklist** | Interns | Step-by-step SRT validation (manual + automated) | `caption-qc-checklist.md` |
| **Caption Validation Spec** | Developer (Garen) | Blueprint for `oeff-caption-validate.py` — 10 checks, JSON output, stdlib only | `caption-validation-spec.md` |
| **Film Ingest Pipeline** | Garen, Interns | File delivery instructions, naming convention, QC gates, venue packet assembly | `sop-library/film-ingest-pipeline.md` |
| **Airtable Plan** | Ana (presentation), Garen (implementation) | 16 new fields, 4 views, 5 automations, form mapping | `filmmaker-pipeline-airtable-plan.md` |
| **Email Templates** | Garen (sends), Ana (review) | 5 post-outreach emails: follow-up, file delivery, captions, urgent, confirmation | `email-drafts/filmmaker-pipeline-templates.html` |

---

## Timeline Summary

Working backward from April 22 (Day 1):

| Date | What | Owner |
|------|------|-------|
| **Mar 12-15** | Send follow-up to non-responders (Template 1) | Garen → Ana reviews |
| **Mar 14** | Implement Airtable field additions (priorities 1-5, ~2 hrs) | Garen |
| **Mar 19** | Escalate persistent non-responders to Ana | Garen → Ana decides |
| **Mar 21** | Send Film Delivery Kit to all confirmed filmmakers (Template 2) | Garen |
| **Mar 28** | All invoices submitted (or escalated) | Ana |
| **Apr 1** | **HARD DEADLINE** — all film files due. Final chase for missing files. | Garen |
| **Apr 1-11** | QC window (validate, normalize, caption burn) | Garen + Interns |
| **Apr 11** | All invoices paid. All files QC-passed. | Ana + Garen |
| **Apr 15** | All caption processing complete | Garen |
| **Apr 15-18** | Venue packets assembled and delivered via Dropbox | Garen |
| **Apr 19-21** | Venue playback confirmation (call if needed). Backup USBs ready. | Kim + Garen |
| **Apr 22** | Festival opens | |

---

## Decisions Needing Ana's Input

These are flagged across the documents. None block the follow-up email (Template 1), but some block Template 2 (file delivery) and the caption pipeline.

| # | Decision | Context | Urgency |
|---|----------|---------|---------|
| 1 | **Caption cost policy** | Proposed: deduct Rev cost from licensing fee for paid screenings; OEFF absorbs for free screenings. This is in the Caption Policy doc — don't share with filmmakers until Ana confirms. | Before Template 2 goes out (~Mar 21) |
| 2 | **Licensing rate thresholds** | Process doc proposes: features <$500, shorts <$250 = auto-approve. Over threshold → Ana decides. Are these the right numbers? | Before first filmmaker response |
| 3 | **Whose Water? status** | Still on hold (Ana + Josh rewatching for Epiphany fit). Decision determines whether it enters the pipeline or gets cut. | By Mar 19 (escalation gate) |
| 4 | **Beyond Zero + 40 Acres contacts** | Merge sheet has contacts (Nathan Havey, Dan McCarthy/Magnolia). Are these confirmed? Were they sourced? | Before follow-up email |
| 5 | **Discussion guides** | Venue packets include per-film discussion guides. Ana/Josh need to produce these. | By Apr 10 (packet assembly) |

---

## Filmmaker Touchpoint Budget

The March 5 outreach was touchpoint 0. Three remaining contacts max:

| # | Content | Who Gets It | When |
|---|---------|-------------|------|
| 1 | Follow-up (licensing ask) | Non-responders only | Mar 12-15 |
| 2 | Film Delivery Kit (file upload + specs + caption info) | All confirmed filmmakers | Mar 21 |
| 3 | File reminder OR QC failure re-request | Non-deliverers or QC failures only | Apr 1 / as needed |

A responsive filmmaker who delivers on time gets **one more email** (the Delivery Kit). A filmmaker who ghosts and sends a corrupt file gets all three. The budget protects responsive filmmakers from unnecessary email.

---

## Tools Already Built

Every tool referenced in the pipeline documents already exists:

| Tool | Commands Used | File |
|------|-------------|------|
| `oeff-file-tracker.py` | `status`, `received`, `qc-pass`, `qc-fail`, `deliver`, `confirm`, `delivery-status`, `intern-checklist` | `~/tools/` |
| `oeff-film-qc.py` | `validate`, `normalize`, `package` | `~/tools/` |
| `caption-and-normalize.sh` | Full ffmpeg pipeline | `~/Desktop/claude/domains/oeff/` |
| `fix-srt-drift.py` | SRT timing correction | `~/Desktop/claude/domains/oeff/` |
| `oeff-airtable-sync.py` | Bidirectional Airtable ↔ merge sheet | `~/tools/` |
| `oeff-media-catalogue.py` | `build`, `status`, `gaps` | `~/tools/` |

**One tool not yet built:** `oeff-caption-validate.py` (SRT validation). The spec is in `caption-validation-spec.md`. Stdlib Python 3 only — ~200 lines, can be built in one session.

---

## Validation Checklist

| Principle | Check | Status |
|-----------|-------|--------|
| Filmmaker friction | ≤3 touchpoints remaining after March 5 outreach? | Yes — follow-up, delivery kit, file reminder |
| Caption coverage | All 4 scenarios handled (SRT, burned-in, no captions paid, no captions free)? | Yes — Caption Policy + Process Phase 5 |
| Invoice speed | Response → invoice → payment ≤10 business days? | Yes — Process Phase 2 targets this |
| QC automation | ≥50% of caption QC criteria checkable programmatically? | Yes — 10 automated checks in validation spec |
| Airtable integration | Every process step has a corresponding status field? | Yes — 16 new fields mapped |
| Accessibility | Process is accessible (plain language, clear structure)? | Yes — intern checklist assumes no experience |
| Scalability | Process works for 13 films and for 40 films? | Yes — all tools are per-film, not batch-dependent |
| Corruption handling | Clear escalation for Rooted and similar? | Yes — QC Gate 2 + Phase 4.2 escalation path |
| Print traffic alignment | Naming, delivery, QC aligned with standards? | Yes — OEFF2026_ convention + 5-gate QC |
| Team clarity | Every step has exactly one owner? | Yes — owner named on every step |

---

## What's Not Covered

- **Pre-event email** to filmmakers (~1 week before festival) — not in this pipeline. Separate template needed later.
- **Venue host communications** — Kim's separate workflow. This pipeline hands off at "venue packet delivered."
- **Eventbrite / ticketing** — separate system (`eventbrite-state.json`).
- **Budget tracking** — outside Airtable scope for now.
- **Festival-week logistics** — AV setup, volunteer coordination, day-of operations.

---

## Immediate Next Actions

1. **Today (Mar 12):** Send follow-up email (Template 1) to non-responders. Garen drafts, Ana reviews.
2. **This week:** Implement Airtable priorities 1-5 from the Airtable Plan (~2 hours).
3. **By Mar 21:** Send Film Delivery Kit (Template 2) to all confirmed filmmakers.
4. **When ready:** Build `oeff-caption-validate.py` from the validation spec (~1 session).
