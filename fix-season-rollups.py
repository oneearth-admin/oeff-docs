#!/usr/bin/env python3
"""
fix-season-rollups.py — Fix host data layer rollups to filter by 2026 season

Problem: LKP rollup fields on Venues pull from ALL linked Events (2025+2026),
causing mixed-year data (e.g., Climate Action Evanston shows 4 films instead of 1).

Fix (no formula fields needed — Airtable blocks their creation):
  1. Create a "2026 Events" link field on Venues (API supports link field creation)
  2. Populate it with only Season=2026 event records
  3. PATCH existing LKP rollup fields to use "2026 Events" instead of "Events"

Safe to re-run: checks for existing fields, skips populated links, PATCHes are idempotent.
Stdlib Python 3 only.

Usage:
    AIRTABLE_TOKEN=pat... python3 fix-season-rollups.py --dry-run
    AIRTABLE_TOKEN=pat... python3 fix-season-rollups.py
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional

sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "ops"))
from airtable_api import BASE_ID, api_call, get_token

API = "https://api.airtable.com/v0"

LINK_FIELD_NAME = "2026 Events"

# Mapping: existing LKP rollup field on Venues → target field name on Events
# These rollups currently target fields via the "Events" link — we'll retarget to "2026 Events"
ROLLUP_FIELDS = [
    "LKP Film Title",
    "LKP Event Date",
    "LKP Event Time",
    "LKP Doors Open",
    "LKP Ticket Price",
    "LKP Ticket URL",
    "LKP OEFF Rep",
    "All Screenings",
]


# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------

def get_schema(token: str) -> dict:
    """Fetch base metadata."""
    endpoint = f"/meta/bases/{BASE_ID}/tables"
    result = api_call("GET", endpoint, token)
    tables = {}
    for t in result.get("tables", []):
        if t["name"].startswith("[DELETE]"):
            continue
        fields = {}
        for f in t.get("fields", []):
            fields[f["name"]] = {
                "id": f["id"],
                "type": f["type"],
                "options": f.get("options", {}),
            }
        tables[t["name"]] = {"id": t["id"], "fields": fields}
    return tables


def fetch_all_records(token: str, table_id: str, fields: list, formula: str = "") -> list:
    """Paginated fetch of all records from a table."""
    records = []
    offset = None
    while True:
        params = []
        for f in fields:
            params.append(f"fields%5B%5D={urllib.parse.quote(f)}")
        if formula:
            params.append(f"filterByFormula={urllib.parse.quote(formula)}")
        if offset:
            params.append(f"offset={offset}")
        qs = "&".join(params)
        url = f"{API}/{BASE_ID}/{table_id}?{qs}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
        time.sleep(0.25)
    return records


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Fix LKP rollups with 2026 Events link field")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    token = get_token()
    print("Discovering schema...")
    schema = get_schema(token)

    events_table = schema.get("Events")
    venues_table = schema.get("Venues")
    if not events_table or not venues_table:
        print("ERROR: Events or Venues table not found")
        return 1

    events_id = events_table["id"]
    venues_id = venues_table["id"]
    events_fields = events_table["fields"]
    venues_fields = venues_table["fields"]

    # --- Phase 1: Create "2026 Events" link field on Venues ---
    print(f"\n--- Phase 1: Create '{LINK_FIELD_NAME}' link field on Venues ---")

    if LINK_FIELD_NAME in venues_fields:
        print(f"  '{LINK_FIELD_NAME}' already exists — skipping creation")
        link_field_id = venues_fields[LINK_FIELD_NAME]["id"]
    else:
        if args.dry_run:
            print(f"  [dry-run] Would create '{LINK_FIELD_NAME}' link field on Venues → Events")
            link_field_id = "???"
        else:
            body = {
                "name": LINK_FIELD_NAME,
                "type": "multipleRecordLinks",
                "options": {
                    "linkedTableId": events_id,
                },
            }
            endpoint = f"/meta/bases/{BASE_ID}/tables/{venues_id}/fields"
            result = api_call("POST", endpoint, token, body=body)
            link_field_id = result.get("id", "???")
            print(f"  Created '{LINK_FIELD_NAME}' → {link_field_id}")

    # --- Phase 2: Populate "2026 Events" with Season=2026 records ---
    print(f"\n--- Phase 2: Populate '{LINK_FIELD_NAME}' with 2026 events ---")

    # Get all 2026 events
    print("  Fetching 2026 events...")
    events_2026 = fetch_all_records(token, events_id, ["Event ID", "Season", "Venue"], '{Season}="2026"')
    print(f"  Found {len(events_2026)} events with Season=2026")

    # Build venue_record_id → [event_record_ids] mapping
    venue_to_events: Dict[str, List[str]] = {}
    for evt in events_2026:
        venue_links = evt["fields"].get("Venue", [])
        for venue_rec_id in venue_links:
            venue_to_events.setdefault(venue_rec_id, []).append(evt["id"])

    print(f"  {len(venue_to_events)} venues have 2026 events")

    # Get current state of 2026 Events field on venues
    if not args.dry_run and LINK_FIELD_NAME in venues_fields:
        print("  Fetching current venue records...")
        all_venues = fetch_all_records(token, venues_id, ["Venue Name", LINK_FIELD_NAME])

        updated = 0
        skipped = 0
        for venue_rec in all_venues:
            venue_rec_id = venue_rec["id"]
            current_links = venue_rec["fields"].get(LINK_FIELD_NAME, [])
            target_links = venue_to_events.get(venue_rec_id, [])

            if not target_links:
                continue

            # Check if already correctly populated
            if set(current_links) == set(target_links):
                skipped += 1
                continue

            # Update the link field
            body = {
                "fields": {
                    LINK_FIELD_NAME: [{"id": eid} for eid in target_links]
                }
            }
            url = f"{API}/{BASE_ID}/{venues_id}/{venue_rec_id}"
            req = urllib.request.Request(
                url,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="PATCH",
                data=json.dumps(body).encode(),
            )
            with urllib.request.urlopen(req) as resp:
                json.loads(resp.read())

            venue_name = venue_rec["fields"].get("Venue Name", venue_rec_id)
            event_count = len(target_links)
            print(f"  Linked {venue_name} → {event_count} event(s)")
            updated += 1
            time.sleep(0.25)

        print(f"  Updated: {updated}, Already correct: {skipped}")
    elif args.dry_run:
        for venue_rec_id, event_ids in venue_to_events.items():
            print(f"  [dry-run] Would link venue {venue_rec_id} → {len(event_ids)} event(s)")

    # --- Phase 3: Retarget LKP rollups to use "2026 Events" link ---
    print(f"\n--- Phase 3: Retarget LKP rollups to use '{LINK_FIELD_NAME}' ---")

    # Re-fetch schema to pick up newly created field
    if not args.dry_run:
        schema = get_schema(token)
        venues_fields = schema["Venues"]["fields"]
        events_fields = schema["Events"]["fields"]

    link_info = venues_fields.get(LINK_FIELD_NAME)
    if not link_info and not args.dry_run:
        print(f"  ERROR: '{LINK_FIELD_NAME}' not found after creation")
        return 1
    new_link_id = link_info["id"] if link_info else "???"

    patched = 0
    skipped = 0

    for rollup_name in ROLLUP_FIELDS:
        rollup_info = venues_fields.get(rollup_name)
        if not rollup_info:
            print(f"  SKIP '{rollup_name}' — not found on Venues")
            continue

        # Check current link field
        current_link_id = rollup_info.get("options", {}).get("recordLinkFieldId", "")
        if current_link_id == new_link_id:
            print(f"  '{rollup_name}' already uses '{LINK_FIELD_NAME}' — skipping")
            skipped += 1
            continue

        # Get the current target field and formula
        current_target_id = rollup_info.get("options", {}).get("fieldIdInLinkedTable", "")
        current_formula = rollup_info.get("options", {}).get("formulaTextParsed", 'ARRAYJOIN(values, ", ")')

        if args.dry_run:
            print(f"  [dry-run] Would retarget '{rollup_name}' → '{LINK_FIELD_NAME}'")
            patched += 1
            continue

        body = {
            "name": rollup_name,
            "type": "rollup",
            "options": {
                "fieldIdInLinkedTable": current_target_id,
                "recordLinkFieldId": new_link_id,
                "formulaTextParsed": current_formula,
                "referencedFieldIds": [],
            },
        }
        endpoint = f"/meta/bases/{BASE_ID}/tables/{venues_id}/fields/{rollup_info['id']}"
        try:
            result = api_call("PATCH", endpoint, token, body=body)
            print(f"  Retargeted '{rollup_name}' → '{LINK_FIELD_NAME}'")
            patched += 1
        except Exception as e:
            print(f"  ERROR retargeting '{rollup_name}': {e}")
        time.sleep(0.3)

    # --- Summary ---
    mode = "DRY RUN" if args.dry_run else "COMPLETE"
    print(f"\n--- {mode} ---")
    print(f"  Rollup fields retargeted: {patched}")
    print(f"  Already correct: {skipped}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
