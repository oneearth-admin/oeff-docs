#!/usr/bin/env python3
"""
v7-health.py — OEFF V7 reconciliation health check

Reads V7 CSV exports (from published URLs or local files), counts key
metrics, compares against the previous snapshot, and prints a plain-text
diff report.

Usage:
    python3 tools/v7-health.py                  # use local CSVs in airtable-import/
    python3 tools/v7-health.py --urls urls.json  # use published Google Sheets CSV URLs
    python3 tools/v7-health.py --csv-dir /path/  # use CSVs in a specific directory

Stdlib only — no pip dependencies.
"""

import argparse
import csv
import json
import os
import sys
from datetime import date
from io import StringIO
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# ---------------------------------------------------------------------------
# Configuration: expected CSV filenames and their V7 sheet equivalents
# ---------------------------------------------------------------------------

# Map from V7 sheet name -> local CSV filename (in airtable-import/)
SHEET_MAP = {
    "Hosts":          "01-venues.csv",
    "Films_2026":     "02-films.csv",
    "Events_2026":    "03-events.csv",
    "Film_Contacts":  "04-film-contacts.csv",
    "Host_Intake":    "05-host-intake.csv",
}

# Pipeline status values (case-sensitive, must match V7 exactly)
PIPELINE_STATUSES = ["Scheduled", "Confirmed Interest", "Interested"]

# ---------------------------------------------------------------------------
# CSV reading
# ---------------------------------------------------------------------------

def read_csv_from_file(filepath):
    """Read a CSV file, return list of dicts."""
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def read_csv_from_url(url):
    """Fetch a published Google Sheets CSV URL, return list of dicts."""
    try:
        with urlopen(url, timeout=15) as resp:
            text = resp.read().decode("utf-8-sig")
        return list(csv.DictReader(StringIO(text)))
    except URLError as e:
        print(f"  Warning: Could not fetch {url}: {e}")
        return None


def load_sheets(csv_dir=None, urls=None):
    """Load all sheets from either local CSVs or published URLs.

    Returns dict: sheet_name -> list of row dicts, or None if unavailable.
    """
    sheets = {}

    if urls:
        # urls is a dict: sheet_name -> published CSV URL
        for sheet_name, url in urls.items():
            print(f"  Fetching {sheet_name} from URL...")
            sheets[sheet_name] = read_csv_from_url(url)
    else:
        # Fall back to local CSV directory
        if csv_dir is None:
            # Default: look for airtable-import/ relative to this script
            script_dir = Path(__file__).resolve().parent.parent
            csv_dir = script_dir / "airtable-import"

        csv_dir = Path(csv_dir)
        if not csv_dir.is_dir():
            print(f"Error: CSV directory not found: {csv_dir}")
            sys.exit(1)

        for sheet_name, filename in SHEET_MAP.items():
            filepath = csv_dir / filename
            if filepath.exists():
                sheets[sheet_name] = read_csv_from_file(filepath)
            else:
                print(f"  Warning: {filepath} not found")
                sheets[sheet_name] = None

    return sheets


# ---------------------------------------------------------------------------
# Metrics extraction
# ---------------------------------------------------------------------------

def count_nonempty(rows, column):
    """Count rows where the given column is non-empty."""
    if rows is None:
        return None
    count = 0
    for row in rows:
        val = row.get(column, "").strip()
        if val:
            count += 1
    return count


def count_matching(rows, column, value):
    """Count rows where column exactly matches value."""
    if rows is None:
        return None
    count = 0
    for row in rows:
        if row.get(column, "").strip() == value:
            count += 1
    return count


def filter_2026(rows):
    """Filter event rows to 2026 only (the airtable export includes all years)."""
    if rows is None:
        return None
    filtered = []
    for row in rows:
        year = row.get("Year", "").strip()
        # Match "2026" or "2026.0" (Excel float artifact)
        if year in ("2026", "2026.0"):
            filtered.append(row)
    # If no Year column exists (V7 published CSV may not have it), return all
    if not filtered and rows and "Year" not in rows[0]:
        return rows
    return filtered


def extract_metrics(sheets):
    """Extract all health metrics from loaded sheet data."""
    hosts = sheets.get("Hosts")
    events_raw = sheets.get("Events_2026")
    events = filter_2026(events_raw)
    films = sheets.get("Films_2026")
    contacts = sheets.get("Film_Contacts")
    intake = sheets.get("Host_Intake")

    m = {}

    # Hosts
    m["hosts_total"] = len(hosts) if hosts is not None else None

    # Events (2026 only)
    if events is not None:
        m["events_total"] = len(events)
        for status in PIPELINE_STATUSES:
            key = f"events_{status.lower().replace(' ', '_')}"
            m[key] = count_matching(events, "Pipeline Status", status)
        m["events_with_film"] = count_nonempty(events, "Film ID")
        m["events_missing_film"] = (
            m["events_total"] - m["events_with_film"]
            if m["events_with_film"] is not None else None
        )
        m["events_with_date"] = count_nonempty(events, "Date")
        m["events_missing_date"] = (
            m["events_total"] - m["events_with_date"]
            if m["events_with_date"] is not None else None
        )
    else:
        m["events_total"] = None

    # Films
    if films is not None:
        m["films_total"] = len(films)
        m["films_intake_yes"] = count_matching(films, "Intake Received", "true")
        # Also check for "Y" in case V7 uses different values
        if m["films_intake_yes"] == 0:
            m["films_intake_yes"] = count_matching(films, "Intake Received", "Y")
        m["films_intake_no"] = m["films_total"] - m["films_intake_yes"]
    else:
        m["films_total"] = None

    # Film Contacts
    if contacts is not None:
        m["film_contacts_total"] = len(contacts)
        m["captions_complete"] = count_matching(
            contacts, "Caption Status", "Complete"
        )
        # Also check for the longer form used in actual data
        if m["captions_complete"] == 0:
            # Count any non-empty caption status as having some response
            m["captions_complete"] = count_matching(
                contacts, "Caption Status", "Captions are burned into video"
            )
            # For reporting, count all contacts with ANY caption status
            m["captions_any_response"] = count_nonempty(
                contacts, "Caption Status"
            )
        m["film_contacts_columns"] = (
            len(contacts[0]) if contacts else 0
        )
    else:
        m["film_contacts_total"] = None

    # Host Intake
    if intake is not None:
        m["intake_responses"] = len(intake)
        m["intake_matched"] = count_nonempty(intake, "Venue Id")
        m["intake_unmatched"] = m["intake_responses"] - m["intake_matched"]
    else:
        m["intake_responses"] = None

    # Fill rates (percentages)
    if m.get("events_total") and m["events_total"] > 0:
        scheduled = m.get("events_scheduled", 0) or 0
        confirmed = m.get("events_confirmed_interest", 0) or 0
        m["pipeline_active_rate"] = round(
            (scheduled + confirmed) / m["events_total"] * 100, 1
        )

    if m.get("films_total") and m["films_total"] > 0:
        m["film_intake_rate"] = round(
            (m.get("films_intake_yes", 0) or 0) / m["films_total"] * 100, 1
        )

    return m


# ---------------------------------------------------------------------------
# Snapshot management
# ---------------------------------------------------------------------------

def get_snapshot_dir():
    """Return the v7-snapshots directory path."""
    return Path(__file__).resolve().parent.parent / "v7-snapshots"


def save_snapshot(metrics, snapshot_date=None):
    """Save metrics as a dated JSON snapshot."""
    if snapshot_date is None:
        snapshot_date = date.today().isoformat()

    snap_dir = get_snapshot_dir()
    snap_dir.mkdir(exist_ok=True)

    snapshot = {
        "date": snapshot_date,
        "metrics": metrics,
    }

    filepath = snap_dir / f"{snapshot_date}.json"
    with open(filepath, "w") as f:
        json.dump(snapshot, f, indent=2)

    return filepath


def load_previous_snapshot():
    """Load the most recent snapshot before today, if any."""
    snap_dir = get_snapshot_dir()
    if not snap_dir.is_dir():
        return None

    today = date.today().isoformat()
    snapshots = sorted(snap_dir.glob("*.json"), reverse=True)

    for snap_path in snapshots:
        snap_date = snap_path.stem
        if snap_date < today:
            with open(snap_path) as f:
                return json.load(f)

    # If no previous snapshot, try loading today's (first run re-check)
    for snap_path in snapshots:
        with open(snap_path) as f:
            return json.load(f)

    return None


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

METRIC_LABELS = {
    "hosts_total":              "Hosts (total)",
    "events_total":             "Events (total)",
    "events_scheduled":         "  Scheduled",
    "events_confirmed_interest":"  Confirmed Interest",
    "events_interested":        "  Interested",
    "events_with_film":         "  With Film assigned",
    "events_missing_film":      "  Missing Film ID",
    "events_with_date":         "  With Date",
    "events_missing_date":      "  Missing Date",
    "films_total":              "Films (total)",
    "films_intake_yes":         "  Intake received",
    "films_intake_no":          "  Intake missing",
    "film_contacts_total":      "Film Contacts (total)",
    "film_contacts_columns":    "  Column count",
    "captions_complete":        "  Captions complete",
    "captions_any_response":    "  Any caption response",
    "intake_responses":         "Host Intake responses",
    "intake_matched":           "  Matched to venue",
    "intake_unmatched":         "  Unmatched",
    "pipeline_active_rate":     "Pipeline active rate (%)",
    "film_intake_rate":         "Film intake rate (%)",
}


def format_val(v):
    """Format a metric value for display."""
    if v is None:
        return "—"
    return str(v)


def print_report(metrics, previous):
    """Print a plain-text health report with optional diff."""
    today = date.today().isoformat()
    print()
    print(f"{'=' * 52}")
    print(f"  OEFF V7 Health Check — {today}")
    print(f"{'=' * 52}")
    print()

    prev_metrics = previous.get("metrics", {}) if previous else {}
    prev_date = previous.get("date", "none") if previous else "none"

    if previous:
        print(f"  Comparing against: {prev_date}")
        print()

    for key, label in METRIC_LABELS.items():
        current = metrics.get(key)
        prev = prev_metrics.get(key)

        if current is None and prev is None:
            continue

        line = f"  {label:<30} {format_val(current):>6}"

        if previous and prev is not None and current is not None:
            diff = round(current - prev, 1)
            if diff > 0:
                line += f"  (+{diff})"
            elif diff < 0:
                line += f"  ({diff})"

        print(line)

    # Warnings
    print()
    warnings = []

    events_total = metrics.get("events_total")
    if events_total is not None:
        missing_film = metrics.get("events_missing_film", 0) or 0
        missing_date = metrics.get("events_missing_date", 0) or 0
        scheduled = metrics.get("events_scheduled", 0) or 0

        if missing_film > 0 and scheduled > 0:
            warnings.append(
                f"{missing_film} events still need Film IDs assigned"
            )
        if missing_date > 0 and scheduled > 0:
            warnings.append(
                f"{missing_date} events still need dates"
            )

    films_missing = metrics.get("films_intake_no")
    if films_missing and films_missing > 0:
        warnings.append(
            f"{films_missing} films still missing intake forms"
        )

    intake_unmatched = metrics.get("intake_unmatched")
    if intake_unmatched and intake_unmatched > 0:
        warnings.append(
            f"{intake_unmatched} intake responses not matched to a venue"
        )

    if warnings:
        print("  Needs attention:")
        for w in warnings:
            print(f"    - {w}")
    else:
        print("  No warnings. Looking good.")

    print()
    print(f"{'=' * 52}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="OEFF V7 health check and reconciliation tool"
    )
    parser.add_argument(
        "--urls", type=str, default=None,
        help="Path to JSON file mapping sheet names to published CSV URLs"
    )
    parser.add_argument(
        "--csv-dir", type=str, default=None,
        help="Directory containing CSV exports (default: airtable-import/)"
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="Print report without saving a snapshot"
    )
    args = parser.parse_args()

    # Load URLs if provided
    urls = None
    if args.urls:
        with open(args.urls) as f:
            urls = json.load(f)

    # Load sheet data
    print("Loading V7 data...")
    sheets = load_sheets(csv_dir=args.csv_dir, urls=urls)

    # Check what we got
    loaded = [name for name, data in sheets.items() if data is not None]
    missing = [name for name, data in sheets.items() if data is None]

    if not loaded:
        print("Error: No sheets could be loaded.")
        sys.exit(1)

    if missing:
        print(f"  Missing sheets: {', '.join(missing)}")

    # Extract metrics
    metrics = extract_metrics(sheets)

    # Load previous snapshot for comparison
    previous = load_previous_snapshot()

    # Print report
    print_report(metrics, previous)

    # Save snapshot
    if not args.no_save:
        filepath = save_snapshot(metrics)
        print(f"  Snapshot saved: {filepath}")
        print()


if __name__ == "__main__":
    main()
