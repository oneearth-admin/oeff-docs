# OEFF 2026 — Filmmaker Outreach: Process and Instructions

**Purpose:** One document covering everything from filmmaker contact through screening-ready file at the venue. Goals, constraints, captions policy, file delivery, QC, and packet assembly — in one place.

**Author:** Garen Hudson, Technical Coordinator
**Date:** 2026-03-12 (41 days to festival)
**Audience:** Garen (execution), Ana (decisions), Kim (follow-ups), Interns (QC tasks)
**Status:** Active — updated after Ana 1:1 March 12

---

## Goals

1. **Get invoices submitted and paid, fast.** Filmmakers remember who pays promptly. Target: invoice → payment within 10 business days.
2. **Receive screening-quality assets.** Video files, caption files, stills, metadata — everything needed to build venue packets.
3. **Capture all metadata.** Film surveys from past years had valuable data (synopses, social handles, Q&A availability, premiere status, discussion guide materials). We need that same depth without sending filmmakers a 40-field form.
4. **Minimize filmmaker friction.** Three touchpoints max after initial outreach. Make the process easy — one filmmaker has already said "please make this as simple as possible, I'm leaving soon."

## Constraints

- **Licensing fees must be in hand** before we send file delivery instructions. No files without a confirmed rate.
- **Captions must meet WCAG SC 1.2.2 (Level A).** All pre-recorded audio content requires synchronized captions — dialogue, speaker ID, and non-speech audio. This is a legal floor, not a suggestion.
- **Packet delivery target: April 1.** Working backward, licensing must be signed by ~March 17 to stay on track.
- **Budget reality:** Caption costs come from the accessibility budget line (~$800–1,500). Rev.com pricing: ~$1.50/min automated, ~$3/min human-reviewed.
- **Some OEFF hosts are public institutions** (libraries, park districts, schools). The 2024 DOJ rule formally adopts WCAG 2.1 Level AA for government digital content — captions protect the host from ADA Title II liability, not just the audience.

---

## The Captions Handshake

**Confirmed with Ana — March 12, 2026.**

This is the policy we communicate to filmmakers:

> Send us your captions in SRT format, timed to your final cut. If you don't have captions, we will caption your film via Rev and take that off your plate.
>
> **Paid screenings:** We deduct the Rev captioning cost from your licensing fee.
> **Free screenings:** We absorb the captioning cost. You're already doing us a favor — we're not going to bill you for accessibility.

### Why this works

- Removes friction from filmmakers who don't have captions (they don't have to figure it out)
- Incentivizes filmmakers to provide their own (saves them money on paid screenings)
- Keeps OEFF's costs reasonable (free screenings = no licensing fee, so captioning cost is the only cost)
- Ensures every screening meets WCAG regardless of what the filmmaker provides

### Caption format requirements (SRT)

Per OEFF's internal caption standards (`oeff-caption-standards.md`):

| Requirement | Spec |
|---|---|
| Format | SubRip (.srt) |
| Content | All spoken dialogue + speaker ID + non-speech audio descriptions |
| Line length | 42 characters max, 2 lines max per segment |
| Reading speed | 150–160 words per minute |
| Sound descriptions | Parenthetical: `(gentle music)`, `(door slams)` |
| Speaker ID | Bracketed: `- [Jane] Over 60 years ago,` |
| Timing | Synchronized to final cut. Must pass duration sanity check. |

**Critical rule: caption lock.** The video must be declared final before captioning begins. If the filmmaker edits after captioning, the SRT must be re-synced. This is the #1 cause of caption drift — learned the hard way from the 2026 Trailer Reel.

### Films with known caption issues

| Film | Issue | Action |
|---|---|---|
| **Rooted** | Ana flagged corruption in existing captions | Investigate — may need full re-caption via Rev |
| [second film TBD] | Also flagged by Ana for corruption | Investigate alongside Rooted |

---

## Filmmaker Touchpoint Budget

Initial outreach went out March 5 via Mailmeteor. Three remaining contacts max:

| # | What | Who gets it | When | Content |
|---|---|---|---|---|
| 1 | Follow-up | Non-responders only | Mar 12–15 | Licensing rate ask. Short, warm, specific. |
| 2 | Film Delivery Kit | All confirmed filmmakers | Mar 21 | File upload link, specs, caption policy, intake form, deadline |
| 3 | File reminder OR QC failure | Non-deliverers / QC failures only | Apr 1 / as needed | Final nudge or re-upload request |

A responsive filmmaker who delivers on time gets **one more email** (the Delivery Kit). A filmmaker who ghosts and sends a corrupt file gets all three. The budget protects responsive filmmakers from unnecessary email.

**The filmmaker who said "make it easy, I'm leaving soon"** — prioritize their Delivery Kit. Send individually as soon as licensing is confirmed, don't wait for the batch.

---

## The Pipeline: Six Phases

### Phase 1: Response Collection (through March 19)

**Owner:** Garen (tracking) + Ana (escalation)

As filmmaker replies land in `films@oneearthcollective.org`, triage into four buckets:

| Bucket | Action |
|---|---|
| **Complete response** (rate + confirmation) | Update Airtable → forward to Ana with one line → move to Phase 2 |
| **Partial response** (missing rate or confirmation) | Reply in same thread asking for the specific missing piece |
| **Question or concern** | Answer if technical, route to Ana if about money/programming |
| **Decline** | Forward to Ana immediately. She decides replacement. |

**Follow-up (Mar 14):** One email to non-responders. Warm, brief, restates the ask:

> Following up on our screening confirmation for [Film]. Two things we need: (1) your nonprofit screening license rate, (2) confirmation you're available for [date].

**Escalation (Mar 19):** Anyone who hasn't responded after two emails → Ana decides: personal outreach, hold the slot, or replace the film.

### Phase 2: Licensing and Invoicing (through March 28)

**Owner:** Ana (approval + payment) + Garen (tracking)

| Rate quoted | Action |
|---|---|
| Under $500 (features) / $250 (shorts) | Ana confirms. Request invoice. |
| Over threshold | Ana decides: negotiate, accept, or decline. |
| Free/gratis | Confirm with thanks. Still need written confirmation for records. |
| "What's your budget?" | Ana provides the number. Garen does not quote budget figures. |

**Invoice request (same thread, within 24 hrs of approval):**

> Great — $[rate] works for us. Could you send an invoice to:
> One Earth Collective NFP / films@oneearthcollective.org
> For: Nonprofit screening license, [Film Title], OEFF 2026 (April 22–27)

**Payment target:** Invoice → paid within 10 business days. Filmmakers remember who pays fast.

### Phase 3: File Collection (through April 4)

**Owner:** Garen (instructions) + Intern (monitoring)

This is the Film Delivery Kit — the primary filmmaker-facing deliverable. Batch send to all confirmed filmmakers by March 21. For late responders or urgent cases (the filmmaker who's leaving), send within 48 hours of confirmation.

**What filmmakers receive:**

1. **Film Intake Survey link** (Google Form — already live)
2. **File delivery instructions** with upload link
3. **Technical specs:**

| Item | Required? | Format | Notes |
|---|---|---|---|
| Screening file | Yes | MP4 (H.264) preferred. ProRes or DCP also accepted. | Minimum 1080p. |
| Caption file | Yes | SRT (.srt) timed to final cut | Or tell us you need help — see captions policy above. |
| Film stills | Yes (2–3) | JPG or PNG, min 1920px wide | For venue marketing and social. |
| Synopsis | Yes | Plain text, 2–3 sentences | We may already have this from intake. |
| Poster / key art | If available | JPG or PNG, 300 DPI preferred | For printed materials at venues. |
| Trailer link | If available | YouTube or Vimeo URL | For pre-show reels. |

4. **The captions handshake** — send SRT or we'll Rev it (see policy above)
5. **Deadline: April 1** — stated once, clearly, not buried
6. **What we handle** (reduce filmmaker anxiety): audio normalization, caption formatting and burn-in, venue-specific packaging and delivery

**File delivery options (in order of preference):**

| Method | Why | Setup |
|---|---|---|
| **Dropbox upload link** | No account needed. Drag and drop. Works for large files. | OEFF creates shared folder, sends upload link |
| **Google Drive** | Familiar to most filmmakers. Share with `garen@oneearthcollective.org`. | Filmmaker shares, we download |
| **Their own service** | MASV, WeTransfer, Frame.io — whatever they already use. | Filmmaker sends link |

**File naming convention:**
```
OEFF2026_FilmTitle_Final_H264.mp4
OEFF2026_FilmTitle_Final_H264.srt
```

**What we've tried before and why we're converging:** Past years used Dropbox, Wasabi, and an FTP server — thrown at the wall without a standard. This year: Dropbox is the default (lowest friction for filmmakers), with Google Drive and filmmaker-native services as fallbacks. No FTP. No Wasabi. One primary method, two graceful fallbacks.

**Alignment with print traffic coordination standards:** The naming convention, QC gate structure, and delivery confirmation workflow mirror standard print traffic coordination practice — file naming that encodes format and version, multi-gate QC before final delivery, and written confirmation of receipt from the exhibitor.

### Phase 4: Quality Control (April 1–11)

**Owner:** Garen (QC execution) + Intern (first-pass validation)

Every file that arrives gets run through automated QC:

```
python3 oeff-film-qc.py validate <file>
```

**Automated checks:**
- Resolution (min 1920×1080)
- Codec (H.264, ProRes, or HEVC)
- Audio loudness (target -16 LUFS ± 1 dB)
- Duration (matches expected runtime from Airtable)
- File integrity (no corruption, plays to completion)

| Result | Action |
|---|---|
| All pass | Move to Phase 5 |
| Minor issues (loudness off, acceptable codec) | Fix in our pipeline — don't bother the filmmaker |
| Major issues (wrong resolution, corrupt, truncated) | Contact filmmaker for re-upload. This counts against touchpoint budget. |

**Escalation (5 business days after QC failure notification):** If replacement file doesn't arrive, Ana decides: screen with flawed file, request Vimeo screener as backup, or swap the film.

### Phase 5: Caption Processing (April 1–15)

**Owner:** Garen

Every film routes through one of four caption paths:

| Status | Route | Action |
|---|---|---|
| **Has SRT** | Standard pipeline | Validate SRT coverage → burn captions + normalize audio |
| **Burned-in captions** | Audio only | Verify captions visually → normalize audio only |
| **Needs help (paid screening)** | Rev route | Commission SRT via Rev → deduct cost from licensing fee → standard pipeline |
| **Needs help (free screening)** | Rev route | Commission SRT via Rev → OEFF absorbs cost → standard pipeline |

**Caption QC — intern task with programmatic support:**

Interns validate caption quality before burn-in. Criteria:

| Check | Method | Pass/fail |
|---|---|---|
| SRT parses without errors | Automated (`oeff-caption-validate.py`) | Fail = malformed file, ask filmmaker |
| Segment count is plausible for runtime | Automated (expect ~5–8 segments/min for dialogue-heavy) | Flag if <3/min or >12/min |
| No segments exceed 42 chars/line | Automated | Warn — fixable in pipeline |
| Reading speed ≤ 160 WPM per segment | Automated | Warn — may need re-timing |
| Speaker ID present for multi-speaker | Manual spot-check (5 random segments) | Warn — add if missing |
| Sound descriptions present | Manual spot-check | Warn — add if critical sounds missing |
| No auto-caption artifacts ("um", "[Music]" without context) | Manual scan | Fix before burn-in |
| Timing drift < 200ms at start, middle, end | Manual playback check at 3 points | Fail if > 500ms at any point |
| Duration matches video (within 30 seconds) | Automated (compare SRT last timestamp to ffprobe) | Fail = wrong version, investigate |
| Encoding is UTF-8 | Automated | Fix silently if not (`iconv`) |

**Where this fits in the timeline:** Caption QC happens between file receipt (Phase 4 pass) and caption burn-in. An intern can validate 3–4 SRT files per hour using the checklist + automated tool. Budget ~1 hour per film for manual checks.

**The validation tool** (`oeff-caption-validate.py`) runs the automated checks and outputs a pass/warn/fail report. Spec exists at `caption-validation-spec.md` — not yet built. ~200 lines, stdlib Python 3 only.

**Audio normalization** (all files, regardless of caption path):
EBU R128 standard: -16 LUFS, true peak ≤ -1.5 dBTP. Two-pass via ffmpeg. Ensures consistent volume across all venues.

### Phase 6: Venue Delivery (April 15–21)

**Owner:** Garen (assembly) + Kim (venue confirmation)

Each venue gets a packet:

1. **Screening file** — QC-passed, caption-burned, audio-normalized MP4
2. **Screening info sheet** — title, runtime, director, synopsis, playback notes, OEFF day-of contact
3. **Tech specs** — resolution, codec, audio levels (from QC report)

**Naming:** `OEFF2026_[FilmTitle]_[VenueShortName].mp4`

**Delivery:** Dropbox (primary), Google Drive (fallback), USB (backup).

**Confirmation:** Every venue must confirm download + successful playback by April 19. If no confirmation → call. Too important for email.

**Backup:** USB drives prepared for every screening. Erin carries a portable drive with all files for day-of emergencies.

---

## Timeline Summary

| Date | What | Who |
|---|---|---|
| **Mar 12–15** | Follow-up to non-responders | Garen drafts → Ana reviews |
| **Mar 17** | Licensing signatures target (needed for April 1 packet delivery) | Ana + filmmakers |
| **Mar 19** | Escalate persistent non-responders | Garen flags → Ana decides |
| **Mar 21** | Film Delivery Kit sent to all confirmed filmmakers | Garen |
| **Mar 28** | All invoices submitted (or escalated) | Garen tracks → Ana pays |
| **Apr 1** | **HARD DEADLINE** — all film files due | Filmmakers |
| **Apr 1–11** | QC window (validate, normalize, caption processing) | Garen + interns |
| **Apr 11** | All invoices paid. All files QC-passed. | Ana + Garen |
| **Apr 15** | All caption processing complete | Garen |
| **Apr 15–18** | Venue packets assembled + delivered | Garen |
| **Apr 19–21** | Venue playback confirmation. Backup USBs ready. | Kim + Garen |
| **Apr 22** | Festival opens | |

---

## Airtable Integration

The pipeline is tracked through these Airtable fields (see `filmmaker-pipeline-airtable-plan.md` for implementation details):

**Films table:** `Outreach Status`, `License Fee (Quoted)`, `License Fee (Approved)`, `License Status`, `Invoice Status`, `File Status`, `QC Status`, `QC Notes`, `Caption Status`, `Intake Received`, `Runtime (minutes)`

**Film Contacts table:** `Licensing Rate Quoted`, `Q&A Available`, `Q&A Contact Name/Email`

**Events table:** `Delivery Status`, `Delivery Method`, `Delivery Date`, `Confirmed Date`

**Tools that read/write these fields:**
- `oeff-file-tracker.py` — status dashboard, receive/QC/deliver/confirm workflows
- `oeff-film-qc.py` — automated validation + normalize + package
- `oeff-caption-validate.py` — SRT validation (not yet built)
- `caption-and-normalize.sh` — ffmpeg pipeline for open captions + EBU R128
- `oeff-airtable-sync.py` — bidirectional sync with merge sheet

---

## Escalation Paths

| Situation | First responder | Escalation | Trigger |
|---|---|---|---|
| Filmmaker not responding | Garen | Ana | No response after 2 emails (Mar 19) |
| Rate negotiation | Ana | — | Any. Garen does not discuss budget. |
| Invoice not received | Garen (one nudge) | Ana | 10 business days after request |
| File not received | Garen (one nudge) | Ana | April 5 (1 day after deadline) |
| QC failure needing filmmaker action | Garen | Ana | Replacement not received in 5 business days |
| Caption cost decision | Garen (presents options) | Ana (approves spend) | Any cost above $0 |
| Venue can't play file | Kim | Garen → Erin (backup drive) | Day-of |
| Filmmaker withdraws | Ana | — | Immediate |

---

## What's Not Covered Here

- **Host communications** — Kim's separate workflow. This pipeline hands off at "venue packet delivered."
- **Eventbrite / ticketing** — separate system.
- **Festival-week logistics** — AV setup, volunteer coordination, day-of operations.
- **Pre-event filmmaker email** (~1 week before festival) — separate template needed later.

---

## Related Documents

| Document | What | Location |
|---|---|---|
| Caption standards | OEFF's internal caption specs (typography, audio, SRT format) | `~/.claude/domains/oeff/oeff-caption-standards.md` |
| Airtable plan | Field additions, views, automations | `filmmaker-pipeline-airtable-plan.md` |
| Email templates | 5 post-outreach templates with merge fields | `email-drafts/filmmaker-pipeline-templates.html` |
| Film ingest pipeline | File delivery instructions, platform comparison, QC gates | `sop-library/film-ingest-pipeline.md` |
| Caption validation spec | Blueprint for `oeff-caption-validate.py` | `caption-validation-spec.md` |
| Delivery process (detailed) | 6-phase workflow with decision trees at every step | `filmmaker-delivery-process.md` |

---

*OEFF 2026 Technical Coordination — Garen Hudson*
*Updated after Ana 1:1 March 12, 2026*
