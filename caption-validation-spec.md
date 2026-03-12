# SRT Programmatic Validation Spec

**For:** The developer building `oeff-caption-validate.py`
**Constraints:** stdlib Python 3 only. No pip dependencies. SRT is a text format — no media libraries needed for validation.
**Output:** JSON report with per-check pass/fail and a summary.

---

## SRT Format Reference

An SRT file is a sequence of blocks separated by blank lines:

```
<sequence number>
<start timestamp> --> <end timestamp>
<caption text, one or two lines>

```

Timestamp format: `HH:MM:SS,mmm` (hours, minutes, seconds, milliseconds). The delimiter between start and end is ` --> ` (space-arrow-arrow-space).

Encoding: UTF-8 (with or without BOM). Some tools produce UTF-8 with BOM (`\xef\xbb\xbf`) — the parser must handle both.

---

## Checks

### 1. File Encoding

**What:** Confirm the file is valid UTF-8.

**How:** Open with `encoding="utf-8-sig"` (handles BOM transparently). If the file raises `UnicodeDecodeError`, it fails.

| Result | Criteria |
|--------|----------|
| PASS | File reads cleanly as UTF-8 |
| FAIL | `UnicodeDecodeError` on open |

**Output fields:** `encoding_detected` (always "utf-8" or "utf-8-sig" on pass), `has_bom` (boolean).

---

### 2. Block Structure

**What:** Every block must have a sequence number, a timestamp line, and at least one line of text.

**How:** Split the file on `\n\n` (or `\r\n\r\n`). For each block:
1. First line must be a positive integer (the sequence number).
2. Second line must match the timestamp pattern: `\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}`
3. At least one non-empty text line must follow the timestamp.

| Result | Criteria |
|--------|----------|
| PASS | All blocks are well-formed |
| FAIL | Any block is missing a sequence number, timestamp, or text |

**Output fields:** `total_blocks`, `malformed_blocks` (count), `malformed_details` (list of `{block_number, line_number, reason}`).

---

### 3. Sequence Numbering

**What:** Sequence numbers must start at 1 and increment by 1 without gaps or duplicates.

**How:** Extract the first line of each block. Check: starts at 1, each subsequent number is previous + 1.

| Result | Criteria |
|--------|----------|
| PASS | Sequential 1, 2, 3, ... N with no gaps or duplicates |
| WARN | Starts at a number other than 1, or has gaps, but no duplicates |
| FAIL | Duplicate sequence numbers |

**Output fields:** `first_number`, `last_number`, `expected_count`, `actual_count`, `gaps` (list of missing numbers, cap at 10), `duplicates` (list).

**Note:** Many captioning tools produce correct sequences, but hand-editing can introduce gaps. Gaps are cosmetic (most players ignore sequence numbers entirely), so this is a WARN, not a FAIL. Duplicates are a FAIL because they indicate a copy-paste or merge error.

---

### 4. Timestamp Validity

**What:** All timestamps must be valid times where end > start within each block.

**How:** Parse each timestamp pair. Validate:
- Hours 00-99 (SRT allows >24h for very long files)
- Minutes 00-59
- Seconds 00-59
- Milliseconds 000-999
- End timestamp > start timestamp (no zero-duration or negative-duration blocks)

| Result | Criteria |
|--------|----------|
| PASS | All timestamps valid, all end > start |
| FAIL | Any invalid timestamp or end <= start |

**Output fields:** `invalid_timestamps` (list of `{block_number, start, end, reason}`).

---

### 5. Display Duration

**What:** Each caption must be on screen long enough to read but not so long it feels stuck.

**Thresholds:**
- Minimum: 1.0 seconds
- Maximum: 6.0 seconds (soft — longer captions for slow, narrated content are acceptable)
- Warning threshold: 0.5-1.0 seconds (very fast) or 7.0-10.0 seconds (very slow)
- Hard fail: < 0.5 seconds or > 10.0 seconds

**How:** For each block, compute `end - start` in seconds.

| Result | Criteria |
|--------|----------|
| PASS | All durations between 1.0 and 6.0 seconds |
| WARN | Any duration 0.5-1.0s or 6.0-10.0s |
| FAIL | Any duration < 0.5s or > 10.0s |

**Output fields:** `min_duration`, `max_duration`, `avg_duration`, `too_short` (list of `{block_number, duration}`), `too_long` (list of `{block_number, duration}`).

---

### 6. Timing Gaps and Overlaps

**What:** Blocks should not overlap in time. Small gaps between blocks are normal and expected.

**How:** Sort blocks by start time. For each consecutive pair, check whether block N's end time exceeds block N+1's start time.

| Result | Criteria |
|--------|----------|
| PASS | No overlaps |
| WARN | Overlaps of < 100ms (common in automated captions, usually invisible) |
| FAIL | Any overlap >= 100ms |

**Output fields:** `overlaps` (list of `{block_a, block_b, overlap_ms}`), `largest_gap_ms`, `smallest_gap_ms`.

**Note:** Gaps are informational, not pass/fail. A 0ms gap (back-to-back captions) is fine. Overlaps cause visual stacking in some players.

---

### 7. Line Count

**What:** No caption block should have more than 2 lines of text.

**How:** Count non-empty lines in the text portion of each block (everything after the timestamp line, before the next blank line).

| Result | Criteria |
|--------|----------|
| PASS | All blocks have 1-2 lines |
| FAIL | Any block has 3+ lines |

**Output fields:** `max_lines`, `blocks_over_2_lines` (list of `{block_number, line_count}`).

---

### 8. Line Length

**What:** Lines should be short enough to read comfortably on screen.

**Thresholds:**
- Target: ~32 characters per line
- Warning: 33-42 characters
- Fail: > 42 characters

**How:** For each line of text in each block, count characters (excluding leading/trailing whitespace).

| Result | Criteria |
|--------|----------|
| PASS | All lines <= 32 characters |
| WARN | Any line 33-42 characters |
| FAIL | Any line > 42 characters |

**Output fields:** `max_line_length`, `avg_line_length`, `lines_over_32` (count), `lines_over_42` (list of `{block_number, line_number, length, text}`).

**Note:** These thresholds assume standard HD resolution (1920x1080) with OEFF's default caption font size (21pt Source Sans 3). Outdoor/community venue settings use 24pt, which means fewer characters fit — but the SRT file is the same. Venue-specific rendering is handled at burn time, not in the SRT.

---

### 9. Empty Blocks

**What:** No block should have a timestamp but no text (or only whitespace).

**How:** After parsing each block, check whether the text portion (stripped) is empty.

| Result | Criteria |
|--------|----------|
| PASS | All blocks contain text |
| FAIL | Any block has empty or whitespace-only text |

**Output fields:** `empty_blocks` (list of block numbers).

---

### 10. Video Duration Match (optional, requires video path)

**What:** The SRT's last timestamp should roughly match the video's duration.

**How:** If a video path is provided, run `ffprobe` to get duration. Compare to the last block's end timestamp.

**Threshold:** Within 30 seconds.

| Result | Criteria |
|--------|----------|
| PASS | SRT end and video duration within 30 seconds |
| WARN | SRT end is 30-120 seconds before video end (may be missing end credits — fine if credits have no speech) |
| FAIL | SRT end is > 120 seconds before video end, or SRT end exceeds video duration by > 10 seconds |

**Output fields:** `video_duration_s`, `srt_last_timestamp_s`, `delta_s`.

**Note:** This check requires `ffprobe`. If ffprobe is not available or no video path is given, skip the check and note it as `SKIPPED` in the output.

---

## Output Format

The script should write JSON to stdout. Structure:

```json
{
  "file": "path/to/captions.srt",
  "video_file": "path/to/video.mp4 or null",
  "validated_at": "2026-03-12T15:30:00Z",
  "summary": {
    "status": "PASS | WARN | FAIL",
    "total_checks": 10,
    "passed": 8,
    "warned": 1,
    "failed": 1,
    "skipped": 0
  },
  "checks": {
    "encoding": {
      "status": "PASS",
      "encoding_detected": "utf-8",
      "has_bom": false
    },
    "block_structure": {
      "status": "PASS",
      "total_blocks": 245,
      "malformed_blocks": 0,
      "malformed_details": []
    },
    "sequence_numbering": {
      "status": "PASS",
      "first_number": 1,
      "last_number": 245,
      "expected_count": 245,
      "actual_count": 245,
      "gaps": [],
      "duplicates": []
    },
    "timestamp_validity": {
      "status": "PASS",
      "invalid_timestamps": []
    },
    "display_duration": {
      "status": "WARN",
      "min_duration": 0.8,
      "max_duration": 5.2,
      "avg_duration": 2.7,
      "too_short": [{"block_number": 42, "duration": 0.8}],
      "too_long": []
    },
    "timing_gaps_overlaps": {
      "status": "PASS",
      "overlaps": [],
      "largest_gap_ms": 3200,
      "smallest_gap_ms": 100
    },
    "line_count": {
      "status": "PASS",
      "max_lines": 2,
      "blocks_over_2_lines": []
    },
    "line_length": {
      "status": "PASS",
      "max_line_length": 31,
      "avg_line_length": 22,
      "lines_over_32": 0,
      "lines_over_42": []
    },
    "empty_blocks": {
      "status": "PASS",
      "empty_blocks": []
    },
    "video_duration_match": {
      "status": "SKIPPED",
      "reason": "no video path provided"
    }
  }
}
```

### Status Roll-Up Logic

The `summary.status` is determined by the worst individual check status:

1. If any check is FAIL -> summary is FAIL
2. If no FAILs but any check is WARN -> summary is WARN
3. If all checks PASS (or SKIPPED) -> summary is PASS

SKIPPED checks do not affect the summary status.

---

## CLI Interface

```
python3 oeff-caption-validate.py <srt-file> [--video <video-file>] [--pretty]
```

- `<srt-file>` — required. Path to the SRT file to validate.
- `--video <video-file>` — optional. Path to the video file for duration matching.
- `--pretty` — optional. Pretty-print the JSON output (indent=2). Default is compact JSON.

Exit codes:
- 0 = PASS
- 1 = WARN
- 2 = FAIL
- 3 = Script error (bad arguments, file not found)

---

## Implementation Notes

- **SRT parsing:** Split on `\n\s*\n` to handle both `\n\n` and `\r\n\r\n`. Trim each block. Handle Windows line endings throughout.
- **Timestamp parsing:** Use a regex: `(\d{2}):(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2})[,.](\d{3})`. Accept both `,` and `.` as the millisecond separator (some tools produce `.`).
- **ffprobe call:** `subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", video_path], capture_output=True, text=True, timeout=10)`. Parse the output as a float.
- **Encoding detection:** Open with `encoding="utf-8-sig"`. If that raises, try `encoding="latin-1"` as a fallback to read the file, but report FAIL for encoding — the content will render wrong with non-ASCII characters.
- **No pip dependencies.** Everything here uses `json`, `re`, `subprocess`, `sys`, `pathlib`, `datetime` — all stdlib.
- **Cap detail lists.** For lists like `too_short`, `lines_over_42`, etc., cap at 20 entries in the output. Append `"...and N more"` if truncated. This keeps the JSON readable for films with systemic issues (e.g., every line is too long).
