# OEFF 2026: Filmmaker Outreach Through Delivery

**Purpose:** Get 13 films from "outreach sent" to "screening-ready file in every venue's hands" — with invoices paid, captions burned, QC passed, and no filmmaker contacted more than 3 more times.

**Audience:** Garen, Ana, Kim, interns. Level 1 — every step includes its own context.

**Trigger:** Initial outreach sent March 5. This process covers everything from here.

**Season:** Harvesting. 41 days to festival (April 22). No room for exploration — complete, deliver, close loops.

**Last updated:** 2026-03-12

---

## How This Document Works

Six phases, running roughly in sequence but with significant overlap. Each phase has a timeline gate — the date by which it must be substantially complete or you escalate.

Phases 1-3 are filmmaker-facing (response, money, files). Phases 4-6 are internal (QC, captions, delivery). The handoff between phase 3 and phase 4 is the critical seam — that's where filmmaker work becomes Garen's work.

**Tools already built:**
- `oeff-file-tracker.py` — Airtable-connected status tracking (run `status` for dashboard, `intern-checklist` for task list)
- `oeff-film-qc.py` — ffprobe validation, loudness normalization, caption burn-in
- `caption-and-normalize.sh` — ffmpeg pipeline for open captions + EBU R128
- Airtable base `app9DymWrbAQaHH0K` — Films, Film Contacts, Events tables
- Mailmeteor merge sheet — outreach tracking
- Film Intake Survey — Google Form, live

---

## Phase 1: Response Collection

**Timeline gate:** March 19 (all filmmakers responded or escalated)
**Owner:** Garen (tracking) + Ana (escalation)
**Filmmaker touchpoint:** 1 of 3 remaining (the follow-up)

### 1.1 Triage responses as they arrive [P]

**Who:** Garen
**When:** Within 24 hours of each filmmaker reply landing in `films@oneearthcollective.org`
**What:** Read the reply. Classify it into one of four buckets:

- **Complete response** — filmmaker provided license rate AND confirmed availability
  - Update Airtable: set `Outreach Status` to `Responded`, note the rate in `License Fee (Quoted)`
  - Forward to Ana with one line: "[Film] quoted $X for nonprofit screening license"
  - Move to Phase 2 (invoicing)

- **Partial response** — filmmaker replied but missing rate or confirmation
  - Reply same thread asking for the missing piece. Be specific: "Could you share your nonprofit screening rate?" or "Can you confirm you're available for [date]?"
  - This counts as part of the follow-up touchpoint, not a separate one

- **Question or concern** — filmmaker has questions about format, audience, logistics
  - Answer directly if it's technical (file specs, AV setup, audience size)
  - Route to Ana if it's about programming, partnership, or money
  - Update Airtable `Notes` with the question and your answer

- **Decline or conflict** — filmmaker can't participate
  - Forward to Ana immediately. She decides whether to find a replacement film.
  - Update Airtable: set `Outreach Status` to `Declined`, note reason

**Verification:** Every reply has an Airtable update within 24 hours. No email sits unanswered for more than 2 business days.

### 1.2 Send follow-up to non-responders [D — wait until March 14]

**Who:** Garen drafts, Ana reviews before send
**When:** March 14 (9 days after initial outreach — enough time for busy people)
**What:** Send one follow-up email to every filmmaker who hasn't responded.

Draft the follow-up for Ana's review. Tone: warm, brief, no pressure. Not "just checking in" — restate what you need:

> Following up on our screening confirmation for [Film Title] at OEFF 2026 ([Venue], [Date]). Two things we need from you:
> 1. Your nonprofit screening license rate
> 2. Confirmation that you're available for [date]
>
> Happy to answer any questions — just reply here.

**Inputs:** Mailmeteor merge sheet (who was sent, who replied)
**Outputs:** Follow-up emails sent to non-responders. Airtable updated with follow-up date.

**Verification:** Check Mailmeteor "Opened" status. If an email was opened but not replied to, flag for Ana — the filmmaker saw it and chose not to respond. Different situation than an email that bounced or went to spam.

### 1.3 Escalate persistent non-responders to Ana [D — March 19]

**Who:** Garen flags, Ana decides
**When:** March 19 (14 days after outreach, 5 days after follow-up)
**What:** Any filmmaker who hasn't responded after both outreach + follow-up gets escalated.

Prepare a one-line brief for each:
> [Film Title] — no response after 2 emails. Opened: yes/no. Contact: [name, email]. Screening: [venue, date].

Ana decides one of three things:
- **She reaches out personally** (different relationship, higher signal)
- **Hold the screening slot** (give it one more week)
- **Replace the film** (find an alternative for that venue/date)

**Verification:** Every non-responder has a documented decision by March 19. No film is in limbo.

### If Something Goes Wrong
- Email bounced → Check Mailmeteor bounce report. Try alternate contact from Airtable `Film Contacts`. If no alternate, Ana finds one through her network.
- Filmmaker wants to negotiate terms → Route to Ana. Garen does not negotiate fees or terms.
- Filmmaker ghosts after opening emails → This is information. Flag for Ana with the open/click data.

---

## Phase 2: Licensing and Invoicing

**Timeline gate:** March 28 (all invoices submitted) / April 11 (all invoices paid)
**Owner:** Ana (approval + payment) + Garen (tracking)
**Filmmaker touchpoint:** Part of the file delivery email (Phase 3) — no separate touchpoint needed

### 2.1 Process each quoted rate [P — as responses arrive]

**Who:** Garen routes, Ana approves
**When:** Within 48 hours of receiving a filmmaker's quoted rate
**What:**

### Is the quoted rate within budget?

- **Yes (under $500 for features, $250 for shorts)** → Ana confirms. Move to step 2.2.
- **No (over threshold)** → Ana decides:
  - **Negotiate** — Ana replies directly, Garen stays CC'd
  - **Accept anyway** — Ana confirms, note the exception
  - **Decline** — Ana handles the conversation. Update Airtable.
- **Filmmaker offers free/gratis** → Confirm with thanks. Still need a $0 invoice or written confirmation for records. Move to step 2.2.
- **Filmmaker asks "what's your budget?"** → Ana provides the number. Garen does not quote budget figures.
- **Unsure** → Ask Ana. Include the quoted rate, the film, and the venue.

### 2.2 Request invoice [P]

**Who:** Garen
**When:** Same email thread, within 24 hours of Ana's approval
**What:** Reply to the filmmaker in the existing thread:

> Great — $[rate] works for us. Could you send an invoice to:
>
> One Earth Collective NFP
> films@oneearthcollective.org
>
> For: Nonprofit screening license, [Film Title], OEFF 2026 (April 22-27)
>
> We'll also be sending file delivery instructions separately.

Update Airtable: set `License Status` to `Approved`, `License Fee (Approved)` to the confirmed amount.

### 2.3 Track invoice receipt [P]

**Who:** Garen (monitoring) or Kim (if she's onboarded to the inbox)
**When:** Check every 3 business days
**What:** When an invoice arrives at `films@`:

1. Forward to Ana for payment processing
2. Update Airtable: set `Invoice Status` to `Received`, note the date
3. If invoice is missing details (wrong amount, missing OEFF reference), reply to filmmaker with the specific correction needed

**Escalation trigger:** If no invoice arrives within 10 business days of the request, send one nudge:
> Quick reminder — we're ready to process your invoice for [Film Title] whenever you can send it over. Invoice to: One Earth Collective NFP, films@oneearthcollective.org.

This is the filmmaker's second touchpoint (if it happens). After one nudge, escalate to Ana.

### 2.4 Confirm payment [D — requires Ana]

**Who:** Ana processes payment, notifies Garen
**When:** Within 5 business days of invoice receipt
**What:** Ana pays the invoice through OEC's payment system. Notifies Garen (email or Slack).

Garen updates Airtable: set `Invoice Status` to `Paid`, note payment date.

**Target:** Invoice submitted → paid within 10 business days. Filmmakers remember who pays fast.

### If Something Goes Wrong
- Filmmaker sends invoice to wrong address → Forward to Ana, reply to filmmaker confirming receipt
- Invoice amount doesn't match approved rate → Flag for Ana before payment
- Filmmaker needs a W-9 or tax form → Route to Ana/Josh (OEC financial admin)
- Payment delayed beyond 10 business days → Garen flags to Ana with the date gap

---

## Phase 3: File Collection

**Timeline gate:** April 4 (all screening files received)
**Owner:** Garen (instructions + tracking) + Intern (monitoring Dropbox)
**Filmmaker touchpoint:** 2 of 3 remaining (the Film Delivery Kit)

### 3.1 Send Film Delivery Kit [D — send after license is confirmed, not before]

**Who:** Garen drafts, Ana approves template once (not per-film)
**When:** Batch send to all confirmed filmmakers by March 21. For late responders, send within 48 hours of confirmation.
**What:** One email per filmmaker containing everything they need to deliver their film. This is the primary filmmaker-facing deliverable of the entire process.

The email includes:
1. **Film Intake Survey link** (Google Form — already live)
2. **File delivery instructions** — Dropbox upload link OR instructions to share their own link
3. **Technical specs** (what we need):
   - Video: MP4, H.264 or ProRes, minimum 1920x1080
   - Audio: stereo, mixed and mastered (we normalize loudness on our end)
   - Captions: SRT file strongly preferred. If captions are burned in, note that in the survey.
4. **Deadline: April 4** — stated clearly, once, not buried
5. **What we'll handle** (reduce filmmaker anxiety):
   - Audio normalization to broadcast standard
   - Caption formatting and burn-in if they provide an SRT
   - Venue-specific packaging and delivery

**Inputs:** Confirmed filmmaker list from Phase 1. Approved license rates from Phase 2.
**Outputs:** Email sent. Airtable `Outreach Status` updated to `Kit Sent`. Date logged.

**Template:** Use existing `filmmaker-template-single.html` and `filmmaker-template-multi.html` as structural references. The kit email replaces the "we'll follow up separately" promise from the initial outreach.

### 3.2 Monitor file arrivals [P — ongoing]

**Who:** Intern (primary), Garen (oversight)
**When:** Check daily starting March 22. Run the tracker every morning.
**What:**

1. Run `python3 oeff-file-tracker.py status` — see what's arrived
2. Run `python3 oeff-file-tracker.py check-links` — verify Dropbox links work
3. When a new file arrives:
   - Download it to the local QC staging folder
   - Run `python3 oeff-file-tracker.py received "[Film Title]"` — marks it in Airtable
   - Move to Phase 4 (QC)

**Intern checklist shortcut:** Run `python3 oeff-file-tracker.py intern-checklist` — generates a prioritized task list from current Airtable state.

### 3.3 Chase missing files [D — April 1]

**Who:** Garen
**When:** April 1 (3 days before deadline, 21 days before festival)
**What:** For any film where `File Status` is still `Not Received`:

Send one final nudge in the existing email thread:
> Quick reminder — we need your screening file for [Film Title] by April 4 so we can complete QC and get everything to the venues on time. Upload link: [Dropbox link]

This is the filmmaker's third and final touchpoint. After this, if no file arrives by April 4, escalate to Ana.

**Escalation trigger (April 5):** Film not received after 3 contacts. Ana decides:
- Request a Vimeo screener link as backup (lower quality but playable)
- Swap the film
- Contact filmmaker by phone

### 3.4 Process intake survey responses [P — as they arrive]

**Who:** Intern
**When:** Within 24 hours of each survey submission
**What:** The Film Intake Survey captures:
- Caption status (SRT file available / burned-in / needs help / none)
- Preferred delivery method
- Promotional materials (poster, stills, director bio, trailer link)
- Any special playback requirements

For each response:
1. Update Airtable with the intake data
2. Flag caption status — this drives Phase 5 routing:
   - `Has SRT` → standard pipeline
   - `Burned-in` → skip caption burn, still normalize audio
   - `Needs help` → flag for Garen (budget decision with Ana)
   - `None / unknown` → follow up with filmmaker: "Do you have an SRT file? If not, we can discuss options."

Update Airtable: set `Intake Received` to `true`.

### If Something Goes Wrong
- File is too large for Dropbox upload → Offer Google Drive as alternative. Or ask filmmaker to share their own cloud link.
- File format is wrong (DVD, Blu-ray image, etc.) → Reply with specific format needed. "We need an MP4 or MOV file, not a disc image."
- Filmmaker sends a streaming link instead of a file → "We need a downloadable file for offline playback at the venues. Could you share a direct download link?"
- Intake survey data contradicts what the filmmaker said by email → Trust the survey (more recent). Note the discrepancy in Airtable.

---

## Phase 4: Quality Control

**Timeline gate:** April 11 (all files QC'd and ready for caption processing)
**Owner:** Garen (QC execution) + Intern (first-pass validation)
**Filmmaker touchpoint:** Only if QC fails and we need a replacement file

### 4.1 First-pass validation [P — as files arrive]

**Who:** Intern
**When:** Within 24 hours of marking a file as `Received`
**What:** Run the automated QC tool:

```
python3 oeff-film-qc.py validate <file>
```

The tool checks:
- Resolution (minimum 1920x1080)
- Codec (H.264, ProRes, or HEVC)
- Audio loudness (target -16 LUFS, tolerance +/- 1 dB)
- Duration (matches expected runtime from Airtable)
- File integrity (no corruption, plays to completion)

### Does the file pass validation?

- **All checks pass** → Run `oeff-file-tracker.py qc-pass "[Film Title]"`. Move to Phase 5.
- **Minor issues (loudness off, acceptable codec)** → Flag for Garen. These are fixable in our pipeline — no need to bother the filmmaker.
- **Major issues (wrong resolution, corrupt file, truncated)** → Run `oeff-file-tracker.py qc-fail "[Film Title]" "reason"`. Move to step 4.2.

### 4.2 Handle QC failures [D — requires filmmaker response]

**Who:** Garen
**When:** Within 24 hours of a QC failure
**What:**

### Is the issue fixable on our end?

- **Yes (loudness, minor codec issue)** → Fix it in Phase 5. Note the fix in Airtable `QC Notes`. Do not contact the filmmaker.
- **No (wrong file, corrupt, too low resolution, truncated)** → Contact the filmmaker in the existing email thread:

> We ran QC on [Film Title] and found an issue: [specific problem]. Could you re-upload a corrected file? Specifically, we need: [specific fix].
>
> Upload link: [same Dropbox link]

This counts against the 3-touchpoint limit. If a filmmaker has already been contacted 3 times, route through Ana.

Update Airtable: `QC Status` to `Failed`, `QC Notes` with the specific issue and date.

**Escalation trigger:** If a replacement file doesn't arrive within 5 business days, escalate to Ana with options:
- Screen with the flawed file (note what the audience will experience)
- Request a Vimeo screener as backup
- Swap the film

### 4.3 Second-pass QC on replacement files [D]

**Who:** Intern (validation), Garen (review)
**When:** Within 24 hours of replacement file arrival
**What:** Same as 4.1. If it fails again, Garen handles directly — no more intern back-and-forth.

### If Something Goes Wrong
- ffprobe/ffmpeg not installed → `brew install ffmpeg`. The QC tools require this.
- File too large to download locally → QC on the filmmaker's cloud storage if possible (stream + probe). Or use Garen's machine with more storage.
- Ambiguous QC result (passes some checks, borderline on others) → Garen makes the call. Document the decision in QC Notes.

---

## Phase 5: Caption Processing

**Timeline gate:** April 15 (all caption work complete)
**Owner:** Garen
**Filmmaker touchpoint:** None (this is internal work)

### 5.1 Route each film through the caption matrix [P]

**Who:** Garen
**When:** After QC pass (Phase 4). Batch process when possible.
**What:** Every film falls into one of four caption scenarios. Route accordingly:

### What is this film's caption status? (from intake survey, Airtable `Caption Status`)

**A. Has SRT file** (target: 6 films)
1. Validate SRT coverage: `python3 oeff-film-qc.py burn <file> --srt <srt>` (dry run — shows coverage %)
2. If coverage >= 95%: burn captions and normalize audio in one pass:
   ```
   python3 oeff-film-qc.py package <file> --srt <srt> --apply
   ```
3. If coverage < 95%: flag the gap. Likely missing opening/closing credits or non-dialogue audio descriptions. Decide whether to accept or ask filmmaker for updated SRT.
4. Output goes to `output/` subdirectory. Original file is never modified.

**B. Captions burned in** (target: 2 films)
1. Verify visually — play the file and confirm captions are visible and readable
2. Normalize audio only:
   ```
   python3 oeff-film-qc.py normalize <file> --apply
   ```
3. No caption burn step needed

**C. Needs caption help** (target: 1 film — Rooted)
1. Estimate caption cost. Options:
   - Rev.com or similar service (~$1.50/min for automated, ~$3/min for human)
   - Ask filmmaker if they have a transcript (convert to SRT is cheaper)
   - In-house: if runtime is short, Garen can generate SRT from audio using Whisper (local, no cost)
2. Present options to Ana with cost estimates. Ana approves the spend.
3. Once SRT is obtained, route through path A.

**D. Unknown / no intake** (target: 3 films)
1. Check if the intake survey has been submitted. If not, this is a Phase 3 problem — chase the intake form first.
2. If intake says "none" — same as path C. Estimate cost, present to Ana.
3. If filmmaker doesn't know — ask: "Do you have a transcript or subtitle file in any format?"

### 5.2 Audio normalization for all files [P]

**Who:** Garen
**When:** After caption processing (or alongside, for burned-in caption films)
**What:** Every file gets normalized to EBU R128 (-16 LUFS, true peak <= -1.5 dBTP). The QC tool handles this:

```
python3 oeff-film-qc.py normalize <file> --apply
```

If a file was already packaged with captions (path A), normalization happened during packaging — don't double-process.

**Verification:** Run `oeff-film-qc.py validate` on the output file. Loudness should be within tolerance.

### If Something Goes Wrong
- SRT file has wrong encoding → Convert to UTF-8: `iconv -f [encoding] -t UTF-8 input.srt > output.srt`
- SRT timing is offset → Ask filmmaker for corrected SRT. Or adjust offset in ffmpeg: `-itsoffset [seconds]`
- Caption font not installed → Install Source Sans 3 (OEFF standard). The QC tool uses this by default.
- Caption cost exceeds budget → Ana decides. Options: accept without captions (not ideal for accessibility), find a cheaper captioning service, or ask the filmmaker to provide.

---

## Phase 6: Venue Delivery

**Timeline gate:** April 18 (all venues have confirmed receipt — 4 days before festival)
**Owner:** Garen (assembly + delivery) + Kim (venue confirmation)
**Filmmaker touchpoint:** None (this is between OEFF and venues)

### 6.1 Assemble venue-specific screening packets [D — requires QC-passed files]

**Who:** Garen
**When:** April 11-15 (after all QC and caption work is complete)
**What:** Each venue gets a packet containing:

1. **Screening file** — the QC-passed, caption-burned, audio-normalized MP4
2. **Screening info sheet** — one page with:
   - Film title, runtime, director
   - Synopsis (from Airtable or intake survey)
   - Any special playback notes (e.g., "starts with 30 seconds of black — this is intentional")
   - OEFF contact for day-of issues: Garen's cell
3. **Tech specs** — resolution, codec, audio levels (from QC report)

For venues screening multiple films: one packet per film, clearly labeled.

Naming convention: `OEFF2026_[FilmTitle]_[VenueShortName].mp4`

### 6.2 Deliver to venues [P — one delivery per venue]

**Who:** Garen
**When:** April 15-17 (one week before festival)
**What:** Deliver via the venue's preferred method. Most will be Dropbox.

For each delivery:
1. Upload/share the file
2. Run `python3 oeff-file-tracker.py deliver "[Film Title]" "[Venue Name]" --method dropbox`
3. Send the venue host a brief email or message:
   > Your screening file for [Film Title] is ready. [Dropbox link]. Please download it before your event on [date] — don't plan to stream it. Let us know when you've got it.

This email goes through the host communication channel (Kim's domain), not the filmmaker channel.

### 6.3 Confirm venue receipt [P]

**Who:** Kim (primary), Intern (follow-up)
**When:** April 17-21 (final confirmation window)
**What:** Every venue must confirm they've downloaded and can play the file.

For each venue:
1. Check if the host has confirmed receipt (reply, Airtable update, or verbal)
2. Run `python3 oeff-file-tracker.py confirm "[Film Title]" "[Venue Name]"`
3. If no confirmation by April 19: call the host. This is too important for email.

**Verification:** Run `python3 oeff-file-tracker.py delivery-status` — shows the full delivery dashboard. Target: 100% confirmed by April 21 (day before festival).

### 6.4 Prepare backup delivery [P]

**Who:** Garen
**When:** April 18-20
**What:** For each screening:
1. Prepare a USB drive with the screening file as backup
2. Erin should have a copy of every file on a portable drive for day-of emergencies
3. If a venue can't play the Dropbox file, Erin or a runner delivers the USB

### If Something Goes Wrong
- Venue host can't download from Dropbox → Try Google Drive. If that fails, USB delivery.
- Venue has no compatible player → VLC runs on everything. Include a note in the screening info sheet: "If the file won't play, download VLC (free) from videolan.org."
- File plays but captions are wrong → Garen re-burns from original SRT and re-delivers. This is why we keep originals.
- Venue loses the file → Re-share the Dropbox link. This is why we don't delete the shared folder until after the festival.
- Day-of playback failure → Erin has the backup drive. Worst case: stream from Vimeo (if the filmmaker provided a link).

---

## Timeline Summary

Working backward from April 22 (Day 1 of festival):

| Date | Phase | Gate | What must be true |
|------|-------|------|-------------------|
| Mar 14 | 1 | Follow-up | Non-responder follow-ups sent |
| Mar 19 | 1 | Escalation | All filmmakers responded or escalated to Ana |
| Mar 21 | 3 | Kit sent | Film Delivery Kit emailed to all confirmed filmmakers |
| Mar 28 | 2 | Invoices | All invoices submitted (or escalated) |
| Apr 1 | 3 | File chase | Final file reminder sent to non-deliverers |
| Apr 4 | 3 | Files in | All screening files received |
| Apr 11 | 2/4 | Paid + QC'd | All invoices paid. All files QC-passed. |
| Apr 15 | 5 | Captions | All caption processing complete |
| Apr 17 | 6 | Delivered | All venue packets delivered |
| Apr 19 | 6 | Confirm | All venues confirmed receipt (call if needed) |
| Apr 21 | 6 | Backup | Backup USBs + Erin's portable drive ready |
| Apr 22 | — | Festival | Day 1 |

## Parallel Work Map

These can run simultaneously without blocking each other:

- **Phase 1 (responses)** and **Phase 2 (invoicing)** overlap — process each filmmaker as they respond
- **Phase 3 (file collection)** starts after Phase 1 confirmation but runs alongside Phase 2 — you don't need to wait for payment to collect files
- **Phase 4 (QC)** runs as files arrive, not as a batch — each file enters QC independently
- **Phase 5 (captions)** can start as soon as each individual file passes QC
- **Phase 6 (delivery)** is the only true sequential dependency — it requires completed files from Phase 5

## Escalation Paths

| Situation | First responder | Escalation | Trigger |
|-----------|----------------|------------|---------|
| Filmmaker not responding | Garen | Ana | No response after 2 emails (March 19) |
| Rate negotiation | Ana | — | Any negotiation. Garen does not discuss budget. |
| Invoice not received | Garen (one nudge) | Ana | 10 business days after request |
| File not received | Garen (one nudge) | Ana | April 5 (1 day after deadline) |
| QC failure needing filmmaker action | Garen | Ana | Replacement file not received in 5 business days |
| Caption cost decision | Garen (presents options) | Ana (approves spend) | Any caption cost above $0 |
| Venue can't play file | Kim | Garen | Day-of: Erin (backup drive) |
| Filmmaker withdraws | Ana | — | Immediate. Ana decides replacement. |

## Airtable Field Reference

These fields drive the process. If they're not in Airtable yet, add them before starting.

**Films table:**
- `Outreach Status`: Not Sent / Sent / Responded / Kit Sent / Declined
- `License Fee (Quoted)`: number — what the filmmaker asked for
- `License Fee (Approved)`: number — what Ana approved
- `License Status`: Pending / Approved / Declined
- `Invoice Status`: Not Requested / Requested / Received / Paid
- `File Status`: Not Received / Received / QC Passed / QC Failed
- `QC Status`: Not Started / Passed / Failed
- `QC Notes`: text — issues found, fixes applied
- `Caption Status`: Has SRT / Burned-in / Needs Help / Unknown
- `Intake Received`: checkbox

**Events table:**
- `Delivery Status`: Not Started / Delivered / Confirmed
- `Delivery Method`: Dropbox / Google Drive / USB / Vimeo
- `Delivery Date`: date
- `Confirmed Date`: date

## Filmmaker Touchpoint Budget

The initial outreach (March 5) was touchpoint 0. Three remaining:

| Touchpoint | Content | Phase | When |
|------------|---------|-------|------|
| 1 | Follow-up (non-responders only) | 1 | March 14 |
| 2 | Film Delivery Kit (all confirmed) | 3 | March 21 |
| 3 | File reminder (non-deliverers only) OR QC failure re-request | 3/4 | April 1 / as needed |

Not every filmmaker gets all 3. A filmmaker who responds immediately and delivers files on time gets touchpoint 2 only. A filmmaker who ghosts and sends a corrupt file gets all 3. The budget protects responsive filmmakers from unnecessary email.

## Exception Handling

### Whose Water? (on hold)

Ana and Josh are deciding. This film is excluded from all phases until Ana confirms. When she does:
- Add to Airtable with all fields
- Enter at Phase 1 (even if late — the process is the same, just compressed)
- Adjust touchpoint timing — may need to combine the follow-up and kit into one email

### Films screening at multiple venues

Some films screen at 2+ venues. The process is the same through Phase 5 (one QC'd file per film). Phase 6 diverges — the same file gets delivered to multiple venues with venue-specific screening info sheets.

`oeff-file-tracker.py deliver` handles this per-event, not per-film.

### Late-arriving films (after April 4 deadline)

If a file arrives after April 4:
1. QC immediately (same day if possible)
2. Expedite caption processing — skip batch, process individually
3. Deliver directly to venue — skip the April 15-17 batch window
4. If file arrives after April 18, deliver via USB on day-of through Erin

### Filmmaker wants to attend their screening

Route to Ana. This is a programming/logistics question, not a file delivery question. If they need travel details, venue access, or Q&A coordination, Ana handles it or delegates to Kim for host coordination.

---

## Done When

- [ ] All 13 films (or 12 + Whose Water? decision) have responded to outreach
- [ ] All invoices submitted and paid
- [ ] All screening files received, QC-passed, and caption-processed
- [ ] All venue packets delivered and confirmed
- [ ] Backup drives prepared
- [ ] Airtable reflects reality for every film and every event
