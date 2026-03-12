# OEFF 2026 Film Ingest Pipeline

**Purpose:** Get 13 films from filmmakers to 22 venues — on time, QC'd, correctly formatted, with captions.
**Owner:** Garen (pipeline architecture) + Interns (QC execution)
**Festival:** April 22-27, 2026
**Last updated:** 2026-03-12

This document contains five operational deliverables:

1. [File Delivery Instructions](#1-file-delivery-instructions) — filmmaker-facing, share directly
2. [Platform Comparison](#2-platform-comparison) — internal decision record
3. [File Naming Convention](#3-file-naming-convention) — reference for everyone
4. [QC Gate Checklist](#4-qc-gate-checklist) — intern-facing, technical
5. [Venue Delivery Packet Assembly](#5-venue-delivery-packet-assembly) — Garen + intern execution

---

## Timeline at a Glance

```
Mar 12 (today)    File delivery instructions sent to filmmakers
Mar 26            Soft deadline — all files should be in by now
Apr 1             HARD DEADLINE — films needed for QC pipeline
Apr 1-8           QC window (validate, normalize, caption burn)
Apr 8             QC complete — venue packets begin assembly
Apr 8-15          Venue packets assembled + delivered
Apr 15-18         Venues confirm receipt + successful playback
Apr 22            Festival opens
```

---

# 1. File Delivery Instructions

**Audience:** Filmmakers (Level 1 — assume no festival portal experience)
**Delivery method:** Email this section directly, or paste into a Google Doc and share the link
**Voice:** Warm-professional. Short. Respectful of their time.

---

### OEFF 2026 — File Delivery Guide

Hello — thank you for being part of the One Earth Film Festival.

We need your screening file and a few companion materials by **Tuesday, April 1**. This gives us time to run quality checks and prepare venue packets before the festival opens April 22.

#### What to send

| Item | Required? | Format | Notes |
|------|-----------|--------|-------|
| Screening file | Yes | MP4 (H.264) preferred. ProRes or DCP also accepted. | Minimum 1080p resolution. |
| Caption file | Yes | SRT format (.srt) | Timed to your screening file. English. |
| Film stills | Yes (2-3) | JPG or PNG, minimum 1920px wide | For venue marketing and social media. |
| Synopsis | Yes | Plain text, 2-3 sentences | We may already have this from intake — we'll confirm. |
| Poster or key art | If available | JPG or PNG, 300 DPI preferred | For printed materials at venues. |
| Trailer link | If available | YouTube or Vimeo URL | For pre-show reels. |

#### How to send

**Option A — Dropbox (preferred)**
Upload your files to our shared Dropbox folder. You'll receive an upload link by email. Drop your files in and you're done — no Dropbox account needed.

**Option B — Google Drive**
If you prefer Google Drive, share a folder with **garen@oneearthcollective.org** — view access is fine. We'll download from there.

**Option C — Your own method**
If you already use MASV, WeTransfer, Frame.io, or another service, send us the download link. Whatever works for you works for us.

#### File naming

Name your files like this:

```
OEFF2026_YourFilmTitle_Final_H264.mp4
OEFF2026_YourFilmTitle_Final_H264.srt
```

Replace spaces in the title with hyphens. Drop special characters. Examples:

```
OEFF2026_How-to-Power-a-City_Final_H264.mp4
OEFF2026_Drowned-Land_Final_ProRes.mov
OEFF2026_Jane-Goodall-Reasons-for-Hope_Final_H264.srt
```

If you're unsure about naming, don't let it slow you down — send the file however it's named and we'll sort it out.

#### Questions or issues

Email **garen@oneearthcollective.org** with subject line "OEFF 2026 File Delivery — [Your Film Title]". You'll hear back within 24 hours.

If your file is larger than 10 GB, or you're having trouble uploading, reach out and we'll find a path.

---

# 2. Platform Comparison

**Audience:** Internal (Garen + OEFF team)
**Purpose:** Confirm platform choice for film file collection

### The comparison

| Factor | Dropbox (current) | Google Drive | MASV | WeTransfer |
|--------|--------------------|--------------|------|------------|
| **Cost** | $0 (existing plan) | $0 (existing OEC workspace) | ~$0.25/GB received | Free tier: 2GB limit. Pro: $19/mo |
| **Max file size** | 50 GB (upload link) | 5 TB (workspace) | No limit | 2 GB free / 200 GB pro |
| **Filmmaker friction** | Low — upload link, no account needed | Low — share a folder, most people know Drive | Medium — need to create a MASV account or use a portal link | Low — drag and drop, but free tier too small for films |
| **Team workflow** | Already integrated with file-tracker.py and delivery pipeline | Would need new integration | Would need new integration | No team workflow — download and move |
| **Folder structure** | We control it | Filmmaker controls their share | Portal can enforce structure | Flat — no folders |
| **File integrity** | Good — checksums on upload | Good | Excellent — UDP acceleration, checksums, resume | Basic |
| **DCP handling** | Folder upload works | Folder upload works | Purpose-built for this | Cannot handle DCP folders on free tier |
| **Speed (large files)** | Good | Good | Best — built for film industry | Slow on free tier |

### Recommendation: Dropbox (stay the course)

Dropbox is already integrated with the existing tooling (`oeff-file-tracker.py` checks Dropbox links, the delivery pipeline uses Dropbox shared folders). The team knows it. Filmmakers don't need an account. The file size limits are adequate for our lineup.

MASV would be the upgrade choice if we had more DCP transfers or larger files — but at $0.25/GB, even a single 40 GB ProRes file costs $10. Across 13 films with possible ProRes and DCP variants, that's $50-150 we don't need to spend when Dropbox handles the same files at no additional cost.

Google Drive is a viable backup for filmmakers who are more comfortable sharing from their own Drive. Accept it as Option B — the manual download step is negligible for 13 films.

WeTransfer's free tier is too small for film files. Not viable without a paid plan.

**Decision: Dropbox primary, Google Drive accepted, filmmaker's preferred method accepted. No new platform spend.**

---

# 3. File Naming Convention

**Audience:** Everyone — filmmakers, interns, Garen
**Purpose:** Consistent naming so tools work and files don't get lost

### The pattern

```
OEFF2026_FilmTitle_Version_Format.ext
```

| Segment | Rules | Examples |
|---------|-------|---------|
| `OEFF2026` | Always. Literal prefix. | `OEFF2026` |
| `FilmTitle` | Title case, hyphens for spaces, drop punctuation | `Drowned-Land`, `40-Acres` |
| `Version` | `Final` for screening copy. `V2`, `V3` for revisions. `QC` for post-normalization. | `Final`, `V2`, `QC` |
| `Format` | Codec or format identifier | `H264`, `ProRes`, `DCP`, `HEVC` |
| `.ext` | File extension matching the content | `.mp4`, `.mov`, `.srt`, `.jpg` |

### Complete example set — every 2026 film

```
Screening files:
  OEFF2026_Jane-Goodall-Reasons-for-Hope_Final_H264.mp4
  OEFF2026_Plastic-People_Final_H264.mp4
  OEFF2026_Beyond-Zero_Final_H264.mp4
  OEFF2026_Drowned-Land_Final_ProRes.mov
  OEFF2026_Rooted_Final_H264.mp4
  OEFF2026_How-to-Power-a-City_Final_H264.mp4
  OEFF2026_The-Last-Ranger_Final_H264.mp4
  OEFF2026_Planetwalker_Final_H264.mp4
  OEFF2026_40-Acres_Final_H264.mp4
  OEFF2026_Whose-Water_Final_H264.mp4
  OEFF2026_Rails-to-Trails_Final_ProRes.mov
  OEFF2026_In-Our-Nature_Final_H264.mp4

Caption files (match the video filename, swap extension):
  OEFF2026_Jane-Goodall-Reasons-for-Hope_Final_H264.srt
  OEFF2026_Plastic-People_Final_H264.srt
  OEFF2026_Drowned-Land_Final_ProRes.srt
  ...

Post-QC normalized files:
  OEFF2026_Jane-Goodall-Reasons-for-Hope_QC_H264.mp4
  OEFF2026_Drowned-Land_QC_H264.mp4
  ...

Stills:
  OEFF2026_Jane-Goodall-Reasons-for-Hope_Still01.jpg
  OEFF2026_Jane-Goodall-Reasons-for-Hope_Still02.jpg

Poster / key art:
  OEFF2026_Drowned-Land_Poster.jpg
```

### DCP naming

DCPs are folder-based, not single files. Name the folder:

```
OEFF2026_How-to-Power-a-City_Final_DCP/
```

Contents inside the DCP folder keep their native names — don't rename internal DCP files.

### Rules

1. **No spaces.** Use hyphens. `How-to-Power-a-City` not `How to Power a City`.
2. **No special characters.** Drop apostrophes, colons, question marks, commas. `Whose-Water` not `Whose Water?`.
3. **Numbers stay as-is.** `40-Acres` not `Forty-Acres`.
4. **Articles included.** `The-Last-Ranger` not `Last-Ranger`. Consistency over brevity.
5. **Caption file names match video file names.** Same root, `.srt` extension. This is how `oeff-film-qc.py` finds the caption file automatically.
6. **Version only increments on re-delivery.** If a filmmaker sends a corrected file, it becomes `V2`. The QC pipeline adds `QC` after processing.

### What to do when a filmmaker sends a file with a different name

Rename it. This takes 30 seconds and saves hours downstream. The tools expect this pattern — `oeff-film-qc.py validate` and `oeff-file-tracker.py` both parse filenames.

---

# 4. QC Gate Checklist

**Audience:** Interns + Garen (Level 2 — practitioner, knows what ffprobe is or will learn)
**Trigger:** A film file arrives (any method)
**Time estimate:** 15-30 minutes per film (automated checks) + 10 minutes manual review
**Tools:** `oeff-film-qc.py`, `oeff-file-tracker.py`

### Before you start

- [ ] ffmpeg and ffprobe installed (`brew install ffmpeg` — ask Garen if unsure)
- [ ] You have the AIRTABLE_TOKEN environment variable set (ask Garen)
- [ ] You know where incoming files land (Dropbox sync folder)

### Gate 1: Receipt and Naming

| # | Check | How | Pass condition |
|---|-------|-----|----------------|
| 1.1 | File arrived | Check Dropbox / email / Drive | File is accessible and downloadable |
| 1.2 | Mark received in Airtable | `python3 oeff-file-tracker.py received "Film Title"` | Status updates to "Received" |
| 1.3 | File named correctly | Compare to naming convention (Section 3 above) | Matches `OEFF2026_Title_Version_Format.ext` |
| 1.4 | Rename if needed | Rename the file to match convention | Filename follows pattern |
| 1.5 | Caption file present | Look for matching `.srt` file | SRT file exists with matching name |

**If no caption file:** Email the filmmaker. Subject: "OEFF 2026 — Caption file needed for [Film Title]". Don't block the rest of QC — continue with video checks, flag the missing caption.

### Gate 2: Technical Validation (automated)

Run the automated validation:

```
python3 oeff-film-qc.py validate path/to/OEFF2026_Film-Title_Final_H264.mp4
```

The tool checks everything below automatically. Review the output:

| # | Check | Pass condition | What to do if it fails |
|---|-------|----------------|------------------------|
| 2.1 | Codec | H.264, H.265, or ProRes | Flag — may need re-encode. Ask Garen. |
| 2.2 | Resolution | >= 1920x1080 | Flag — filmmaker may need to send a higher-res copy |
| 2.3 | Aspect ratio | Documented (not necessarily 16:9 — documentaries vary) | Note the actual ratio. Not a fail condition, but needs documenting for venue setup. |
| 2.4 | Audio present | At least one audio track | Flag immediately — silent file is a blocker |
| 2.5 | Audio loudness | -16 LUFS +/- 1 dB (EBU R128) | Will be normalized in Gate 3. Note the current level. |
| 2.6 | True peak | <= -1.5 dBTP | Will be normalized in Gate 3 |
| 2.7 | Duration | Matches expected runtime (from Airtable, +/- 60 seconds) | If way off, confirm with filmmaker — may be wrong cut |
| 2.8 | File integrity | Plays without errors | Corrupted file = re-request from filmmaker |

### Gate 3: Caption Validation

If an SRT file is present:

```
python3 oeff-film-qc.py validate path/to/OEFF2026_Film-Title_Final_H264.srt
```

| # | Check | Pass condition | What to do if it fails |
|---|-------|----------------|------------------------|
| 3.1 | SRT format valid | Parses without errors | Manually check — encoding issues are common (UTF-8 required) |
| 3.2 | Runtime coverage | Captions cover >= 95% of film runtime | Flag — may indicate truncated or incomplete captions |
| 3.3 | Timing alignment | First caption starts within 30 seconds of film start | Spot-check against video — timing may be offset |

### Gate 4: Manual Playback Review

This cannot be automated. Open the file in VLC.

| # | Check | How | What you're looking for |
|---|-------|-----|-------------------------|
| 4.1 | First 30 seconds | Play from the start | Video and audio both present, no glitches, not a test pattern |
| 4.2 | Last 30 seconds | Scrub to the end | Film ends cleanly, no encoding artifacts, credits visible |
| 4.3 | Random mid-point | Scrub to ~40% of runtime | Audio/video sync looks right, no obvious quality drops |
| 4.4 | Caption spot-check | Enable SRT in VLC (Subtitle > Add Subtitle File) | Captions appear, timing roughly matches speech |

### Gate 5: QC Decision

All automated checks pass + manual review is clean:
```
python3 oeff-file-tracker.py qc-pass "Film Title"
```

Any check failed:
```
python3 oeff-file-tracker.py qc-fail "Film Title" "Brief reason: e.g., audio at -24 LUFS, needs normalization"
```

**After QC pass:** The film enters the normalization pipeline (Garen runs this):
```
python3 oeff-film-qc.py package path/to/file.mp4 --srt path/to/file.srt --apply
```

This produces the final screening file: H.264 MP4, -16 LUFS audio, open captions burned in.

### If something goes wrong

| Problem | What to do |
|---------|-----------|
| Filmmaker unreachable | Escalate to Ana or Josh — they have relationship context. Don't wait more than 48 hours. |
| File is corrupt or wrong cut | Email filmmaker immediately. CC garen@oneearthcollective.org. |
| No caption file after two requests | Garen decides whether to generate captions (auto-transcription) or push harder on filmmaker. |
| Film arrives after April 1 | Skip to the front of the QC queue. Same process, compressed timeline. |
| ffprobe/ffmpeg throws an error you don't understand | Screenshot the error, send to Garen. Don't guess. |

---

# 5. Venue Delivery Packet Assembly

**Audience:** Garen + interns
**Trigger:** A film passes QC (Gate 5 above)
**Timeline:** Packets assembled April 8-15, delivered April 15-18, playback confirmed by April 20

### What goes in each venue's packet

Every venue receives a Dropbox shared folder containing:

| File | Description | Source |
|------|-------------|--------|
| Screening file | QC'd, normalized, captions burned in. `OEFF2026_Film-Title_QC_H264.mp4` | QC pipeline output |
| Caption file | The SRT, even though captions are burned in. Backup for accessibility. | Filmmaker delivery |
| Cue sheet | Run-of-show timing document. PDF. When to press play, when Q&A starts, etc. | Generated from event data |
| Tech rider | Venue-specific AV requirements. What equipment is provided, what OEFF supplies. | Venue resource matrix |
| Pre-show content | Sponsor loop, YFC winner short, OEFF promo. Single concatenated file. | Assembled by Garen |
| Discussion guide | Post-film conversation prompts specific to this film. PDF. | Content team (Ana/Josh) |
| Emergency contact card | Who to call if something goes wrong day-of. | Generated from Airtable contacts |

### Per-venue format decisions

| Venue capability | What they receive | Why |
|------------------|-------------------|-----|
| Laptop + projector (most venues) | H.264 MP4, open captions burned in | Universal playback. No special software needed. |
| Cinema with DCP capability | DCP folder (if available for that film) + H.264 backup | DCP is higher quality. H.264 backup in case DCP ingest fails. |
| Hybrid streaming venue | H.264 MP4 + streaming-specific instructions | Same file works for projection and streaming input |

Films with DCP available (from intake): The Last Ranger, How to Power a City, Drowned Land, In Our Nature, Plastic People, Jane Goodall. For cinema venues screening these films, include the DCP alongside the H.264.

### Folder structure per venue

```
OEFF2026-Venue-Name/
├── SCREENING/
│   ├── OEFF2026_Film-Title_QC_H264.mp4       ← Press play on this
│   ├── OEFF2026_Film-Title_QC_H264.srt       ← Caption backup
│   └── OEFF2026_Film-Title_Final_DCP/         ← Only for DCP-capable venues
├── PRE-SHOW/
│   ├── OEFF2026_PreShow_SponsorLoop.mp4       ← Play before doors-open
│   └── OEFF2026_PreShow_YFC-Short.mp4         ← Play before feature
├── DOCS/
│   ├── CueSheet_Venue-Name.pdf
│   ├── TechRider_Venue-Name.pdf
│   ├── DiscussionGuide_Film-Title.pdf
│   └── EmergencyContacts_Venue-Name.pdf
└── README.txt                                  ← "Start here" file
```

The `README.txt` in each folder:

```
OEFF 2026 — Screening Packet for [Venue Name]
=============================================

Your screening: [Film Title]
Date: [Event Date] at [Event Time]

BEFORE YOUR EVENT:
1. Open the SCREENING folder
2. Play OEFF2026_Film-Title_QC_H264.mp4 in VLC (or your media player)
3. Confirm video plays with audio and visible captions
4. If anything looks wrong, contact Garen at garen@oneearthcollective.org
   or call/text [phone number]

DAY OF YOUR EVENT:
1. Play files from PRE-SHOW folder during guest arrival
2. Play the screening file from SCREENING folder at showtime
3. Refer to CueSheet in DOCS for exact timing

Questions? Email garen@oneearthcollective.org
```

### Delivery method

**Primary: Dropbox shared folder per venue.** Each venue gets a unique shared folder link via Mailmeteor email merge. The link is password-protected (passwords from `token-map.json`).

**Backup: USB drive.** For venues with unreliable internet or hosts who prefer physical media. Budget for 5-8 USB drives (16 GB each — ~$50 total). Label each drive with venue name and film title.

**When to use USB:** If a venue hasn't confirmed Dropbox receipt by April 18, switch to USB delivery. Don't wait for them to figure out the download.

### Assembly process — step by step

**Phase 1: Prepare common assets (April 8-10)**

1. Confirm all 13 films have passed QC
   - Run `python3 oeff-file-tracker.py status` — every film should show "QC Passed"
   - If any film is not QC'd, it's a blocker. Escalate immediately.

2. Build pre-show content package
   - Sponsor loop: assembled from sponsor slides + OEFF branding
   - YFC winner short: from Sandy's delivery (should already be in hand)
   - OEFF promo reel: from existing assets

3. Generate cue sheets from event data
   - One per venue, with film runtime, Q&A window, and pre-show timing

4. Collect discussion guides from Ana/Josh
   - One per film (not per venue — the same film gets the same guide)

**Phase 2: Build venue folders (April 10-14)**

For each of the 22 venues:

1. Create the Dropbox folder: `OEFF2026-Venue-Name/`
2. Copy the correct screening file into `SCREENING/`
3. Copy the caption SRT into `SCREENING/`
4. If venue has DCP capability and film has DCP available, copy DCP folder into `SCREENING/`
5. Copy pre-show content into `PRE-SHOW/`
6. Generate and place cue sheet, tech rider, discussion guide, emergency contacts into `DOCS/`
7. Write the `README.txt` with venue-specific details
8. Log the delivery: `python3 oeff-file-tracker.py deliver "Film Title" "Venue Name" --method dropbox`

**Phase 3: Send and confirm (April 15-18)**

1. Generate Dropbox share links for each venue folder
2. Send via Mailmeteor email merge — one email per host with their specific folder link + password
3. Track sends in Airtable (Film Delivered column)

**Phase 4: Playback verification (April 15-20)**

1. Each host receives a playback confirmation request in their delivery email:
   > "Please download and play the screening file before your event. Reply to this email to confirm it plays correctly."

2. Track confirmations: `python3 oeff-file-tracker.py confirm "Film Title" "Venue Name"`

3. Check delivery dashboard daily: `python3 oeff-file-tracker.py delivery-status`

4. **If a venue hasn't confirmed by April 18:**
   - Send a follow-up email (Day 1)
   - Call or text the host contact (Day 2 — April 19)
   - If still no confirmation by April 20, prepare a USB drive as backup

### If something goes wrong

| Problem | Response |
|---------|----------|
| Venue can't open Dropbox link | Resend link. If still failing, switch to Google Drive share or USB. |
| Venue reports playback issues | Ask them to try VLC. If VLC also fails, the file may be corrupt — re-upload from QC output. |
| Venue needs a format we don't have | Most likely DCP request from a non-DCP venue. Explain that H.264 MP4 plays on any laptop. If they insist, escalate to Garen. |
| A film hasn't passed QC by April 10 | Garen makes the call: ship what we have with a note, or hold and deliver late. Late is better than broken. |
| USB drive needed but none prepped | Buy a 16 GB drive ($6-8), copy the venue folder, label it clearly, hand-deliver or courier. |
| Filmmaker sends a revised cut after packets are assembled | Re-run QC on the new file. If it passes, replace the screening file in affected venue folders and notify those hosts. |

---

## Cross-Reference: Tools and Commands

| Task | Command |
|------|---------|
| Check all film statuses | `python3 oeff-file-tracker.py status` |
| Verify Dropbox links are live | `python3 oeff-file-tracker.py check-links` |
| Mark a film as received | `python3 oeff-file-tracker.py received "Film Title"` |
| Run automated QC | `python3 oeff-film-qc.py validate path/to/file.mp4` |
| Run full packaging pipeline | `python3 oeff-film-qc.py package path/to/file.mp4 --srt path/to/file.srt --apply` |
| Mark QC pass/fail | `python3 oeff-file-tracker.py qc-pass "Film Title"` |
| Log venue delivery | `python3 oeff-file-tracker.py deliver "Film Title" "Venue" --method dropbox` |
| Confirm venue receipt | `python3 oeff-file-tracker.py confirm "Film Title" "Venue"` |
| View delivery dashboard | `python3 oeff-file-tracker.py delivery-status` |
| Print intern task checklist | `python3 oeff-file-tracker.py intern-checklist` |
| Check media catalogue gaps | `python3 oeff-media-catalogue.py gaps` |

---

## Provenance

- Film lineup: Airtable Films table (`02-films.csv` snapshot, Feb 6 2026)
- Venue data: `venue-resource-matrix.json` (22 scheduled venues as of Mar 6 2026)
- QC specs: `oeff-film-qc.py` constants (1080p min, H.264/ProRes/HEVC, -16 LUFS EBU R128)
- Delivery method: Existing Dropbox infrastructure + `oeff-file-tracker.py` delivery commands
- Existing SOP context: `sop-library/02-deliverables-shipping.md` (Kim's delivery stream)
- DCP availability: Filmmaker intake data
