#!/usr/bin/env python3
"""
Regenerate Code.js with current film catalog from 02-films.csv.

Reads the CSV, builds the dropdown entries in the format
  "F26-XXX | Title (Year) — Primary Topic"
and replaces the film array block in Code.js.

Usage:
  python3 inject-films.py
  python3 inject-films.py --csv ../airtable-import/02-films.csv --template Code.js
"""

import csv
import re
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(SCRIPT_DIR, '..', 'airtable-import', '02-films.csv')
DEFAULT_JS = os.path.join(SCRIPT_DIR, 'Code.js')


def build_film_entries(csv_path):
    """Read film CSV and return formatted dropdown strings."""
    entries = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            film_id = row.get('Film ID', '').strip()
            title = row.get('Film Title', '').strip()
            year_raw = row.get('Release Year', '').strip()
            topic = row.get('Primary Topic', '').strip()

            if not film_id or not title:
                continue

            # Clean year: "2025.0" -> "2025", empty -> omit
            year = ''
            if year_raw:
                try:
                    year = str(int(float(year_raw)))
                except ValueError:
                    year = year_raw

            if year:
                entry = f"{film_id} | {title} ({year}) \u2014 {topic}"
            else:
                entry = f"{film_id} | {title} \u2014 {topic}"
            entries.append(entry)

    return entries


def inject_into_js(js_path, entries):
    """Replace the film choices array in Code.js."""
    with open(js_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # Match the Film dropdown's setChoiceValues block specifically.
    # We anchor to the .setTitle('Film') item that precedes it.
    # Pattern: from "setTitle('Film')" through the next setChoiceValues([...])
    pattern = (
        r"(\.setTitle\('Film'\)\s*\n"
        r".*?\.setChoiceValues\(\[\s*\n)"
        r"(.*?)"
        r"(^\s*\]\))"
    )

    # Build replacement lines (all films get trailing commas since Undecided follows)
    lines = []
    for entry in entries:
        lines.append(f"      '{entry}',")
    # Always include the "Undecided" option at the end (no trailing comma)
    lines.append("      'Undecided \u2014 help me choose'")
    replacement_block = '\n'.join(lines) + '\n'

    new_code = re.sub(
        pattern,
        lambda m: m.group(1) + replacement_block + m.group(3),
        code,
        count=1,
        flags=re.MULTILINE | re.DOTALL
    )

    if new_code == code:
        # Check if the pattern matched but content was already identical
        if re.search(pattern, code, re.MULTILINE | re.DOTALL):
            print("Film dropdown already up to date. No changes needed.")
            return
        print("WARNING: Film array pattern not found in Code.js. No changes made.")
        sys.exit(1)

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(new_code)

    print(f"Injected {len(entries)} films into {os.path.basename(js_path)}")
    for entry in entries:
        print(f"  {entry}")


def main():
    csv_path = DEFAULT_CSV
    js_path = DEFAULT_JS

    # Simple arg parsing
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--csv' and i + 1 < len(args):
            csv_path = args[i + 1]
            i += 2
        elif args[i] == '--template' and i + 1 < len(args):
            js_path = args[i + 1]
            i += 2
        else:
            i += 1

    if not os.path.exists(csv_path):
        print(f"Error: Film CSV not found at {csv_path}")
        sys.exit(1)
    if not os.path.exists(js_path):
        print(f"Error: Code.js not found at {js_path}")
        sys.exit(1)

    entries = build_film_entries(csv_path)
    if not entries:
        print("Error: No films found in CSV")
        sys.exit(1)

    inject_into_js(js_path, entries)


if __name__ == '__main__':
    main()
