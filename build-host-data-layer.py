#!/usr/bin/env python3
"""
build-host-data-layer.py — OEFF Host Portal Data Layer Builder

Creates lookup, rollup, and formula fields on the Venues table so that
a single venue record contains everything a host needs. This is the
data layer prerequisite for building Airtable Interface Designer pages.

Uses existing multi-link fields (Events, Host Contacts, Host Intake)
rather than creating new "Primary" single-link fields. ARRAYJOIN
naturally handles multi-event venues (e.g., Columbia with 2 screenings).

Safe to re-run: checks for existing fields by name before creating.

Stdlib Python 3 only — no pip dependencies.

Usage:
    # Dry run — show what would be created
    AIRTABLE_TOKEN=pat... python3 build-host-data-layer.py --dry-run

    # Create fields
    AIRTABLE_TOKEN=pat... python3 build-host-data-layer.py

    # Verbose output (show field IDs and API responses)
    AIRTABLE_TOKEN=pat... python3 build-host-data-layer.py --verbose
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Set

# Shared API layer
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "ops"))
from airtable_api import BASE_ID, api_call, get_token


# ---------------------------------------------------------------------------
# Field definitions
# ---------------------------------------------------------------------------

# Rollup fields on Venues table: (field_name, link_field_name, target_field_name, aggregation)
# link_field_name = the existing multipleRecordLinks field on Venues
# target_field_name = the field in the linked table to pull
# aggregation = Airtable rollup formula

VENUE_ROLLUPS: List[dict] = [
    # From Events
    {"name": "LKP Film Title",   "link": "Events", "target": "Film Title",   "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Event Date",   "link": "Events", "target": "Date",         "formula": "MAX(values)"},
    {"name": "LKP Event Time",   "link": "Events", "target": "Time",         "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Doors Open",   "link": "Events", "target": "Doors Open",   "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Ticket Price", "link": "Events", "target": "Ticket Price", "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Ticket URL",   "link": "Events", "target": "Ticket URL",   "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP OEFF Rep",     "link": "Events", "target": "OEFF Rep",     "formula": "ARRAYJOIN(values, \", \")"},
    # From Host Contacts
    {"name": "LKP Host Name",    "link": "Host Contacts", "target": "Contact Name", "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Host Email",   "link": "Host Contacts", "target": "Email",        "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Host Phone",   "link": "Host Contacts", "target": "Phone",        "formula": "ARRAYJOIN(values, \", \")"},
    # From Host Intake
    {"name": "LKP Intake Address",    "link": "Host Intake", "target": "Venue Address",   "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Intake WiFi",       "link": "Host Intake", "target": "Has Wifi",        "formula": "ARRAYJOIN(values, \", \")"},
    {"name": "LKP Intake Space Notes","link": "Host Intake", "target": "Space Notes",     "formula": "ARRAYJOIN(values, \"\\n\")"},
    {"name": "LKP Intake Wheelchair", "link": "Host Intake", "target": "Has Wheelchair",  "formula": "ARRAYJOIN(values, \", \")"},
]

# Display formula fields on Venues: (field_name, formula_expression)
VENUE_FORMULAS: List[dict] = [
    {"name": "Host - Film",          "formula": 'IF({LKP Film Title}, {LKP Film Title}, "Film to be confirmed")'},
    {"name": "Host - Screening Date","formula": 'IF({LKP Event Date}, DATETIME_FORMAT({LKP Event Date}, "dddd, MMMM D, YYYY"), "Date to be confirmed")'},
    {"name": "Host - Start Time",    "formula": 'IF({LKP Event Time}, {LKP Event Time}, "Start time to be confirmed")'},
    {"name": "Host - Doors Open",    "formula": 'IF({LKP Doors Open}, {LKP Doors Open}, "Doors-open time to be confirmed")'},
    {"name": "Host - Ticket Info",   "formula": 'IF({LKP Ticket URL}, {LKP Ticket URL}, "Ticket link coming soon")'},
    {"name": "Host - Contact Name",  "formula": 'IF({LKP Host Name}, {LKP Host Name}, "Host contact to be confirmed")'},
    {"name": "Host - Contact Phone", "formula": 'IF({LKP Host Phone}, {LKP Host Phone}, "Phone to be confirmed")'},
    {"name": "Host - Contact Email", "formula": 'IF({LKP Host Email}, {LKP Host Email}, "Email to be confirmed")'},
    {"name": "Host - Venue Address", "formula": 'IF({Address}, {Address}, IF({LKP Intake Address}, {LKP Intake Address}, "Address to be confirmed"))'},
    {"name": "Host - Parking",       "formula": 'IF({Parking Info}, {Parking Info}, "Parking details available on request")'},
    {"name": "Host - Transit",       "formula": 'IF({Transit Info}, {Transit Info}, "Transit details available on request")'},
    {"name": "Host - WiFi",          "formula": 'IF({WiFi Info}, {WiFi Info}, "WiFi details shared day-of")'},
    {"name": "Host - AV Notes",      "formula": 'IF({LKP Intake Space Notes}, {LKP Intake Space Notes}, "")'},
]

# Formula field on Events table
EVENTS_FORMULA = {
    "name": "Host Summary Line",
    "formula": '{Film Title} & " — " & IF({Date}, DATETIME_FORMAT({Date}, "MMM D"), "TBD") & IF({Time}, " at " & {Time}, "")',
}

# Final rollup on Venues using Host Summary Line
HOST_ALL_SCREENINGS = {
    "name": "Host - All Screenings",
    "link": "Events",
    "target": "Host Summary Line",
    "formula": "ARRAYJOIN(values, \"\\n\")",
}


# ---------------------------------------------------------------------------
# Schema discovery
# ---------------------------------------------------------------------------

def discover_schema(token: str, verbose: bool = False) -> dict:
    """Fetch base metadata and build field-ID maps.

    Returns:
        {
            "tables": {table_name: {"id": table_id, "fields": {field_name: field_id}}},
            "existing_venues_fields": set of field names on Venues,
            "existing_events_fields": set of field names on Events,
        }
    """
    endpoint = f"/meta/bases/{BASE_ID}/tables"
    result = api_call("GET", endpoint, token)

    tables: Dict[str, dict] = {}
    for t in result.get("tables", []):
        name = t["name"]
        if name.startswith("[DELETE]"):
            continue
        field_map = {}
        for f in t.get("fields", []):
            field_map[f["name"]] = f["id"]
        tables[name] = {"id": t["id"], "fields": field_map}

    if verbose:
        for tname, tinfo in sorted(tables.items()):
            print(f"  Table '{tname}' ({tinfo['id']}): {len(tinfo['fields'])} fields", file=sys.stderr)

    venues_fields = set(tables.get("Venues", {}).get("fields", {}).keys())
    events_fields = set(tables.get("Events", {}).get("fields", {}).keys())

    return {
        "tables": tables,
        "existing_venues_fields": venues_fields,
        "existing_events_fields": events_fields,
    }


# ---------------------------------------------------------------------------
# Field creation helpers
# ---------------------------------------------------------------------------

def create_rollup_field(
    token: str,
    table_id: str,
    field_name: str,
    link_field_id: str,
    target_field_id: str,
    rollup_formula: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> Optional[dict]:
    """Create a rollup field on the given table."""
    body = {
        "name": field_name,
        "type": "rollup",
        "options": {
            "fieldIdInLinkedTable": target_field_id,
            "recordLinkFieldId": link_field_id,
            "result": {"type": "singleLineText"},
            "formulaTextParsed": rollup_formula,
            "referencedFieldIds": [],
        },
    }

    if dry_run:
        print(f"  [dry-run] Would create rollup '{field_name}' "
              f"(link={link_field_id}, target={target_field_id})")
        return None

    endpoint = f"/meta/bases/{BASE_ID}/tables/{table_id}/fields"
    result = api_call("POST", endpoint, token, body=body)
    if verbose:
        print(f"  Created: {json.dumps(result, indent=2)[:300]}", file=sys.stderr)
    print(f"  Created rollup '{field_name}'", file=sys.stderr)
    return result


def create_formula_field(
    token: str,
    table_id: str,
    field_name: str,
    formula: str,
    dry_run: bool = False,
    verbose: bool = False,
) -> Optional[dict]:
    """Create a formula field on the given table."""
    body = {
        "name": field_name,
        "type": "formula",
        "options": {
            "formulaTextParsed": formula,
            "referencedFieldIds": [],
        },
    }

    if dry_run:
        print(f"  [dry-run] Would create formula '{field_name}'")
        return None

    endpoint = f"/meta/bases/{BASE_ID}/tables/{table_id}/fields"
    result = api_call("POST", endpoint, token, body=body)
    if verbose:
        print(f"  Created: {json.dumps(result, indent=2)[:300]}", file=sys.stderr)
    print(f"  Created formula '{field_name}'", file=sys.stderr)
    return result


# ---------------------------------------------------------------------------
# Resolve link/target field IDs for rollup creation
# ---------------------------------------------------------------------------

def resolve_link_field_id(
    schema: dict,
    source_table: str,
    link_field_name: str,
) -> Optional[str]:
    """Find the field ID of a link field on the source table."""
    table_info = schema["tables"].get(source_table)
    if not table_info:
        print(f"  ERROR: Table '{source_table}' not found in schema", file=sys.stderr)
        return None
    fid = table_info["fields"].get(link_field_name)
    if not fid:
        print(f"  ERROR: Link field '{link_field_name}' not found on '{source_table}'", file=sys.stderr)
        return None
    return fid


def resolve_target_field_id(
    schema: dict,
    link_field_name: str,
    target_field_name: str,
) -> Optional[str]:
    """Find the field ID of a target field in the linked table.

    The linked table is determined by the link field name mapping:
      "Events" → Events table
      "Host Contacts" → Host Contacts table
      "Host Intake" → Host Intake table
    """
    # The link field name IS the linked table name in our case
    linked_table = link_field_name
    table_info = schema["tables"].get(linked_table)
    if not table_info:
        print(f"  ERROR: Linked table '{linked_table}' not found in schema", file=sys.stderr)
        return None
    fid = table_info["fields"].get(target_field_name)
    if not fid:
        print(f"  ERROR: Target field '{target_field_name}' not found on '{linked_table}'", file=sys.stderr)
        return None
    return fid


# ---------------------------------------------------------------------------
# Main build logic
# ---------------------------------------------------------------------------

def build_data_layer(token: str, dry_run: bool, verbose: bool) -> int:
    """Create all host portal data layer fields."""

    print("Discovering schema...", file=sys.stderr)
    schema = discover_schema(token, verbose=verbose)

    venues_table = schema["tables"].get("Venues")
    events_table = schema["tables"].get("Events")
    if not venues_table:
        print("ERROR: Venues table not found", file=sys.stderr)
        return 1
    if not events_table:
        print("ERROR: Events table not found", file=sys.stderr)
        return 1

    venues_id = venues_table["id"]
    events_id = events_table["id"]
    existing_venues = schema["existing_venues_fields"]
    existing_events = schema["existing_events_fields"]

    created = 0
    skipped = 0
    errors = 0

    # --- Phase 1: Rollup fields on Venues ---
    print("\n--- Phase 1: Rollup fields on Venues ---", file=sys.stderr)

    for rollup_def in VENUE_ROLLUPS:
        name = rollup_def["name"]
        if name in existing_venues:
            print(f"  Skipping '{name}' — already exists", file=sys.stderr)
            skipped += 1
            continue

        link_fid = resolve_link_field_id(schema, "Venues", rollup_def["link"])
        target_fid = resolve_target_field_id(schema, rollup_def["link"], rollup_def["target"])

        if not link_fid or not target_fid:
            print(f"  SKIPPING '{name}' — could not resolve field IDs", file=sys.stderr)
            errors += 1
            continue

        if verbose:
            print(f"  {name}: link_fid={link_fid}, target_fid={target_fid}", file=sys.stderr)

        result = create_rollup_field(
            token, venues_id, name,
            link_fid, target_fid, rollup_def["formula"],
            dry_run=dry_run, verbose=verbose,
        )
        if result or dry_run:
            created += 1

    # --- Phase 2: Display formula fields on Venues ---
    # These depend on Phase 1 rollup fields existing, so must come after.
    # In dry-run mode we proceed regardless (just printing intent).
    print("\n--- Phase 2: Display formula fields on Venues ---", file=sys.stderr)

    for formula_def in VENUE_FORMULAS:
        name = formula_def["name"]
        if name in existing_venues:
            print(f"  Skipping '{name}' — already exists", file=sys.stderr)
            skipped += 1
            continue

        result = create_formula_field(
            token, venues_id, name, formula_def["formula"],
            dry_run=dry_run, verbose=verbose,
        )
        if result or dry_run:
            created += 1

    # --- Phase 3: Host Summary Line formula on Events ---
    print("\n--- Phase 3: Host Summary Line on Events ---", file=sys.stderr)

    evt_name = EVENTS_FORMULA["name"]
    if evt_name in existing_events:
        print(f"  Skipping '{evt_name}' — already exists", file=sys.stderr)
        skipped += 1
    else:
        result = create_formula_field(
            token, events_id, evt_name, EVENTS_FORMULA["formula"],
            dry_run=dry_run, verbose=verbose,
        )
        if result or dry_run:
            created += 1

    # --- Phase 4: Host - All Screenings rollup on Venues ---
    # Depends on Phase 3 (Host Summary Line must exist on Events).
    print("\n--- Phase 4: Host - All Screenings rollup on Venues ---", file=sys.stderr)

    all_name = HOST_ALL_SCREENINGS["name"]
    if all_name in existing_venues:
        print(f"  Skipping '{all_name}' — already exists", file=sys.stderr)
        skipped += 1
    else:
        link_fid = resolve_link_field_id(schema, "Venues", HOST_ALL_SCREENINGS["link"])

        if dry_run:
            # In dry-run, Host Summary Line won't exist yet — just show intent
            print(f"  [dry-run] Would create rollup '{all_name}' "
                  f"(Events → Host Summary Line, ARRAYJOIN)")
            created += 1
        elif link_fid:
            # Re-discover schema to pick up the newly created Host Summary Line
            print("  Re-discovering schema for Host Summary Line field ID...", file=sys.stderr)
            schema2 = discover_schema(token, verbose=False)
            target_fid = schema2["tables"].get("Events", {}).get("fields", {}).get("Host Summary Line")
            if not target_fid:
                print("  ERROR: Host Summary Line not found on Events after creation", file=sys.stderr)
                errors += 1
            else:
                result = create_rollup_field(
                    token, venues_id, all_name,
                    link_fid, target_fid, HOST_ALL_SCREENINGS["formula"],
                    dry_run=False, verbose=verbose,
                )
                if result:
                    created += 1

    # --- Summary ---
    mode = "DRY RUN" if dry_run else "COMPLETE"
    print(f"\n--- {mode} ---", file=sys.stderr)
    print(f"  Created: {created}", file=sys.stderr)
    print(f"  Skipped (already exist): {skipped}", file=sys.stderr)
    if errors:
        print(f"  Errors: {errors}", file=sys.stderr)

    return 1 if errors else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build OEFF host portal data layer fields on Airtable."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be created without touching Airtable.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show field IDs discovered and creation responses.",
    )
    args = parser.parse_args()

    token = get_token()
    return build_data_layer(token, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
