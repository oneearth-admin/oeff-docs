# OEFF 2026 Caption QC Checklist

**For:** Interns and volunteers doing caption quality control
**Audience:** No captioning experience assumed. Every step tells you what to do and how to know if it worked.
**Time estimate:** 15-25 minutes per film (longer for films over 60 minutes)

---

## Before You Start

You need:
- [ ] The video file (MP4 or MOV)
- [ ] The SRT caption file (should have the same name as the video, with `.srt` extension)
- [ ] A computer with VLC installed (free: [videolan.org](https://www.videolan.org))
- [ ] Terminal access (for running the validation script)
- [ ] This checklist open next to you

**What you're checking for:** DCMP (Described and Captioned Media Program) defines four principles for quality captions. Every check below maps to one of these:

| Principle | What it means |
|-----------|---------------|
| **Accurate** | Words on screen match words spoken. Names and terms are spelled correctly. |
| **Synchronous** | Captions appear when the person speaks and disappear when they stop. |
| **Complete** | All speech is captioned. Significant sounds are described. |
| **Properly Placed** | Captions don't block important visuals. Lines aren't too long to read. |

---

## Phase 1: File Check

_Can we even work with what we received?_

### Step 1. Confirm the SRT file opens

Open the `.srt` file in a text editor (TextEdit, VS Code, Notepad — anything).

- **Pass:** You see numbered blocks with timestamps and text, like this:
  ```
  1
  00:00:05,200 --> 00:00:08,100
  The river runs through everything.
  ```
- **Fail:** The file is empty, garbled, or full of strange characters.
- **If it fails:** Check the file encoding. It should be UTF-8. If you see `Ã©` instead of `e`, the encoding is wrong. Re-save as UTF-8 in your text editor, or flag for Garen.

### Step 2. Run the validation script

Open Terminal. Run:

```bash
python3 ~/tools/oeff-caption-validate.py path/to/captions.srt --video path/to/video.mp4
```

This checks timing, line length, gaps, and formatting automatically. It produces a pass/fail report.

- **Pass:** All checks pass, or only minor warnings.
- **Fail:** Any check marked FAIL in the output.
- **If it fails:** Note which checks failed. Some are fixable (timing drift, line length). Some require new captions. See "Escalation" below.

### Step 3. Check SRT duration against video duration

The script does this automatically, but if you're checking manually:

```bash
ffprobe -v quiet -show_entries format=duration -of csv=p=0 path/to/video.mp4
```

Compare that number (in seconds) to the last timestamp in the SRT file.

- **Pass:** They're within 30 seconds of each other.
- **Fail:** The SRT ends significantly before or after the video.
- **If it fails:** The SRT was probably made from a different cut of the film. Stop here — this needs new captions or a re-sync. Flag for Garen.

---

## Phase 2: Sync Check (Manual)

_Do captions appear when people actually speak?_

Open the video in VLC. Load the SRT file: **Subtitle > Add Subtitle File** and select the `.srt` file.

### Step 4. Check the first 2 minutes

Play the video from the beginning.

- **Pass:** Captions appear when people start speaking and disappear when they stop. The words match what's being said.
- **Fail:** Captions appear too early, too late, or show the wrong text.
- **If it fails:** Note the timestamp and how far off the captions are (e.g., "captions are ~2 seconds late at 00:01:30"). Flag for Garen.

### Step 5. Check the middle of the film

Jump to the halfway point of the film.

- **Pass:** Captions are still synced. No drift.
- **Fail:** Captions have drifted — they were fine at the start but are now early or late.
- **If it fails:** This is cumulative drift, usually from captioning against a different cut. Note the timestamp and the drift amount. Flag for Garen.

### Step 6. Check the last 2 minutes

Jump to near the end of the film.

- **Pass:** Captions are still synced. Credits are not captioned (they don't need to be, unless there's narration over credits).
- **Fail:** Drift has gotten worse, or captions continue after speech has ended.
- **If it fails:** Same as Step 5 — note timestamp and drift. Flag for Garen.

---

## Phase 3: Content Check (Manual)

_Are the captions accurate and complete?_

Pick any 3-minute section of the film. Watch it closely with captions on.

### Step 7. Accuracy check

- **Pass:** Caption text matches spoken words. Names, places, and technical terms are spelled correctly.
- **Fail:** Words are wrong, names are misspelled, or significant phrases are missing.
- **If it fails:** Note the timestamp and what's wrong. Minor typos can be fixed in the SRT. Major inaccuracies (wrong words, missing sentences) need escalation.

### Step 8. Completeness check

- **Pass:** All speech is captioned. Significant non-speech sounds are described in brackets (e.g., `[birds chirping]`, `[audience laughing]`). Speaker changes are identified when it's not obvious from the image who's talking.
- **Fail:** Speech is missing. Important sounds aren't described. You can't tell who's speaking.
- **If it fails:** Note what's missing and the timestamp. If it's a few missing lines, they can be added manually. If large sections are uncaptioned, the SRT needs rework.

### Step 9. Placement and readability check

- **Pass:** No more than 2 lines per caption block. Lines are short enough to read comfortably (roughly 32 characters or fewer per line). Captions stay on screen long enough to read (at least 1 second) but not so long they feel stuck (no more than about 6 seconds).
- **Fail:** Three or more lines stacked. Lines wrap awkwardly or run off screen. Captions flash by too fast to read or linger after the speaker has moved on.
- **If it fails:** The validation script catches most of these. If you're seeing issues the script missed, note the timestamp and describe what you see.

---

## Phase 4: Record Your Results

### Step 10. Fill in the QC log

For each film, record:

| Field | Your entry |
|-------|-----------|
| Film title | |
| SRT filename | |
| QC date | |
| Your name | |
| Script result | PASS / FAIL (attach output) |
| Sync check | PASS / FAIL (note drift if any) |
| Content check | PASS / FAIL (note issues) |
| Overall | PASS / NEEDS FIXES / FAIL |
| Notes | |

### Where to save this

Save the QC log entry and the script output to the film's folder in the OEFF shared drive.

---

## Escalation

When to fix it yourself:
- Minor typos in caption text (fix directly in the SRT file with a text editor)
- A single missing sound description (add it to the SRT file)

When to flag for Garen:
- Any sync drift (early/late captions)
- SRT duration doesn't match video duration
- Large sections of missing captions
- Encoding issues (garbled characters)
- Script reports FAIL on timing checks

When to flag for Ana:
- Film was delivered without captions and needs Rev commission (cost decision)
- Filmmaker sent a different cut than expected (scope/relationship question)

---

## Quick Reference: What Good Captions Look Like

```
42
00:03:15,400 --> 00:03:18,200
The water table has dropped
six feet in ten years.

43
00:03:18,800 --> 00:03:21,500
[Dr. Chen] That's not a trend.
That's a cliff.
```

- Two lines maximum
- Short enough to read in the display time
- Speaker identified when not visually obvious
- Gap between blocks (the 600ms between 18,200 and 18,800) lets the eye reset
