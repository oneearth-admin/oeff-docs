#!/usr/bin/env python3
"""
export-yamm-sheet.py — Export token-map.json to Mailmeteor-ready CSV

NOTE: OEFF switched from YAMM to Mailmeteor (Feb 2026). This script's
filename is legacy but the output format is compatible with both tools.
See also: export-merge-sheet.py (identical, updated name).

Produces a CSV with columns that map directly to Mailmeteor merge fields:
  - Email (Contact Email)
  - Venue Name
  - Host Helper URL
  - Financial Password
  - Packet Password

Import this CSV into a Google Sheet, populate missing emails,
then use Mailmeteor to send from a Gmail draft with {{ merge tags }}.

Usage:
    python3 export-yamm-sheet.py                  # writes merge-sheet.csv
    python3 export-yamm-sheet.py --output out.csv  # custom output path
    python3 export-yamm-sheet.py --check           # just show email coverage
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

TOKEN_MAP_PATH = Path(__file__).parent / "token-map.json"
HELPER_BASE_URL = "https://hosts.oneearthfilmfest.org/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Mailmeteor-ready CSV from token map.")
    parser.add_argument("--output", default="merge-sheet.csv", help="Output CSV path")
    parser.add_argument("--check", action="store_true", help="Just show email coverage stats")
    args = parser.parse_args()

    if not TOKEN_MAP_PATH.exists():
        print(f"Error: {TOKEN_MAP_PATH} not found. Run generate-token-map.py first.", file=sys.stderr)
        return 1

    with open(TOKEN_MAP_PATH, encoding="utf-8") as f:
        token_map = json.load(f)

    # Coverage check
    total = len(token_map)
    with_email = sum(1 for v in token_map.values() if v.get("contact_email"))
    missing = total - with_email

    if args.check:
        print(f"Venues: {total}")
        print(f"With email: {with_email}")
        print(f"Missing email: {missing}")
        if missing:
            print(f"\nMissing emails for:")
            for name, entry in sorted(token_map.items()):
                if not entry.get("contact_email"):
                    print(f"  - {name}")
        return 0

    # Export CSV
    output_path = Path(args.output)
    rows = []
    for name, entry in sorted(token_map.items()):
        token = entry.get("token", "")
        rows.append({
            "Email": entry.get("contact_email", ""),
            "Venue Name": name,
            "Host Helper URL": f"{HELPER_BASE_URL}{token}/" if token else "",
            "Financial Password": entry.get("financial_password_plaintext", ""),
            "Packet Password": entry.get("packet_password", ""),
        })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Email", "Venue Name", "Host Helper URL", "Financial Password", "Packet Password"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")
    if missing:
        print(f"\n⚠  {missing} of {total} venues are missing contact emails.")
        print(f"   Fill in the Email column before running Mailmeteor.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
