#!/usr/bin/env python3
"""
generate-token-map.py — OEFF Host Security Token Map Generator

Generates unique URL tokens and password hashes for each venue,
writing the result to token-map.json. This file is consumed by
generate-venue-sections.py --helpers to build per-venue helper pages.

Can read venue data from:
  1. Airtable (default) — uses the same API layer as the venue generator
  2. A CSV export from V7 — via --csv flag

Can push security fields back to Airtable via --push flag.

Stdlib Python 3 only — no pip dependencies.

Usage:
    # Generate token map from Airtable
    AIRTABLE_TOKEN=pat... python3 generate-token-map.py

    # Generate AND push security fields back to Airtable
    AIRTABLE_TOKEN=pat... python3 generate-token-map.py --push

    # From CSV export
    python3 generate-token-map.py --csv hosts-export.csv

    # Preserve existing tokens (default: true, use --regenerate to force new)
    AIRTABLE_TOKEN=pat... python3 generate-token-map.py --regenerate

    # Dry run — show what would be generated, no writes
    AIRTABLE_TOKEN=pat... python3 generate-token-map.py --dry-run
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import secrets
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_ID = "app9DymWrbAQaHH0K"
API = "https://api.airtable.com/v0"
VENUES_TABLE = "Venues"

TOKEN_MAP_PATH = Path(__file__).parent / "token-map.json"
TOKEN_LENGTH = 16  # hex chars = 64 bits entropy
HELPER_BASE_URL = "https://hosts.oneearthfilmfest.org/"

# Word list for human-readable passwords (nature + festival vocabulary)
PASSWORD_WORDS = [
    "maple", "river", "cedar", "meadow", "stone", "birch", "harbor",
    "summit", "grove", "willow", "prairie", "ember", "creek", "ridge",
    "aspen", "coral", "sage", "linden", "moss", "heron", "fern",
    "oak", "pine", "lake", "field", "brook", "cliff", "dune",
    "bloom", "wind", "frost", "dawn", "reef", "vale", "peak",
    "screening", "festival", "gather", "lantern", "canopy", "forage",
]


# ---------------------------------------------------------------------------
# Crypto helpers (stdlib only)
# ---------------------------------------------------------------------------

def generate_token(length: int = TOKEN_LENGTH) -> str:
    """Generate a cryptographically random hex token."""
    return secrets.token_hex(length // 2)  # token_hex returns 2 hex chars per byte


def generate_password() -> str:
    """Generate a human-readable word-word-number password."""
    w1 = secrets.choice(PASSWORD_WORDS)
    w2 = secrets.choice(PASSWORD_WORDS)
    while w2 == w1:
        w2 = secrets.choice(PASSWORD_WORDS)
    num = secrets.randbelow(90) + 10  # 10-99
    return f"{w1}-{w2}-{num}"


def sha256_hex(text: str) -> str:
    """SHA-256 hash a string, return lowercase hex."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Airtable API layer (same pattern as generate-venue-sections.py)
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Read Airtable PAT from environment."""
    token = os.environ.get("AIRTABLE_TOKEN", "")
    if not token:
        print("Error: AIRTABLE_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return token


def api_call(
    method: str,
    endpoint: str,
    token: str,
    body: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Make an Airtable API call with retry and rate limit handling."""
    url = f"{API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = json.dumps(body).encode("utf-8") if body else None
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=headers, method=method, data=data)
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            time.sleep(0.22)
            return result
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            if e.code == 429:
                print("  Rate limited, waiting 30s...", file=sys.stderr)
                time.sleep(30)
                continue
            if attempt == 3:
                print(f"  FAILED {e.code}: {err[:500]}", file=sys.stderr)
                raise
            print(f"  Retry {attempt + 1}: {e.code} {err[:300]}", file=sys.stderr)
            time.sleep(2)
    return {}


def _extract_email(text: str) -> str:
    """Extract first email address from a multiline text block."""
    import re
    match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    return match.group(0) if match else ""


def fetch_venues_from_airtable(
    token: str,
    season_filter: str = "2026",
) -> List[Dict[str, str]]:
    """Fetch 2026 venue names, contact emails, and record IDs from Airtable.

    Cross-references the Events table (Year=2026) to get the canonical
    list of venues with confirmed screenings or active interest.
    """
    # Step 1: Fetch 2026 Events to get linked venue record IDs
    event_venue_ids: set = set()
    offset: Optional[str] = None

    while True:
        formula = urllib.request.quote("Year=2026")
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote('Events')}"
            f"?filterByFormula={formula}"
            f"&fields%5B%5D=Venue"
            f"&fields%5B%5D=Venue+Name"
        )
        if offset:
            endpoint += f"&offset={offset}"

        result = api_call("GET", endpoint, token)
        for rec in result.get("records", []):
            for vid in rec.get("fields", {}).get("Venue", []):
                event_venue_ids.add(vid)

        offset = result.get("offset")
        if not offset:
            break

    print(f"  Found {len(event_venue_ids)} venue(s) linked from 2026 Events", file=sys.stderr)

    if not event_venue_ids:
        return []

    # Step 2: Fetch those venue records by ID
    venues: List[Dict[str, str]] = []
    id_list = list(event_venue_ids)

    for i in range(0, len(id_list), 20):
        batch = id_list[i : i + 20]
        or_clauses = ",".join(f'RECORD_ID()="{rid}"' for rid in batch)
        formula = urllib.request.quote(f"OR({or_clauses})")
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote(VENUES_TABLE)}"
            f"?filterByFormula={formula}"
        )
        result = api_call("GET", endpoint, token)

        for rec in result.get("records", []):
            fields = rec.get("fields", {})
            name = fields.get("Venue Name", "").strip()
            email = fields.get("Contact_Email", "").strip()
            if not email:
                contact_info = fields.get("Contact Info", "")
                email = _extract_email(contact_info)
            if name and name != "0" and len(name) > 2:
                venues.append({
                    "venue_name": name,
                    "contact_email": email,
                    "record_id": rec.get("id", ""),
                })

    print(f"  Fetched {len(venues)} venue records from Airtable", file=sys.stderr)
    return venues


def fetch_venues_from_csv(csv_path: str) -> List[Dict[str, str]]:
    """Read venue names and contact emails from a CSV export."""
    venues: List[Dict[str, str]] = []
    path = Path(csv_path)

    if not path.exists():
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Try common column name variations
            name = (
                row.get("Venue Name", "")
                or row.get("Name", "")
                or row.get("venue_name", "")
            ).strip()
            email = (
                row.get("Contact Email", "")
                or row.get("Contact_Email", "")
                or row.get("contact_email", "")
                or row.get("Email", "")
            ).strip()
            if name:
                venues.append({"venue_name": name, "contact_email": email})

    print(f"  Read {len(venues)} venues from {csv_path}", file=sys.stderr)
    return venues


# ---------------------------------------------------------------------------
# Token map generation
# ---------------------------------------------------------------------------

def load_existing_map() -> Dict[str, Any]:
    """Load existing token-map.json if it exists."""
    if TOKEN_MAP_PATH.exists():
        with open(TOKEN_MAP_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def generate_token_map(
    venues: List[Dict[str, str]],
    existing: Dict[str, Any],
    regenerate: bool = False,
) -> Dict[str, Any]:
    """Generate the token map, preserving existing tokens unless regenerate=True."""
    token_map: Dict[str, Any] = {}

    for venue in venues:
        name = venue["venue_name"]
        email = venue.get("contact_email", "")

        record_id = venue.get("record_id", "")

        if not regenerate and name in existing:
            # Preserve existing token and passwords
            entry = existing[name].copy()
            entry["contact_email"] = email
            if record_id:
                entry["record_id"] = record_id
            token_map[name] = entry
        else:
            # Generate new token and passwords
            financial_pw = generate_password()
            packet_pw = generate_password()
            token_map[name] = {
                "token": generate_token(),
                "contact_email": email,
                "record_id": record_id,
                "financial_password_hash": sha256_hex(financial_pw),
                "financial_password_plaintext": financial_pw,
                "packet_password": packet_pw,
            }

    return token_map


# ---------------------------------------------------------------------------
# Push to Airtable
# ---------------------------------------------------------------------------

SECURITY_FIELDS = [
    ("Host_Token", "singleLineText", "Unique URL token for host helper page"),
    ("Host_Helper_URL", "url", "Full host helper page URL"),
    ("Financial_Password_Hash", "singleLineText", "SHA-256 hash for password gate"),
    ("Financial_Password", "singleLineText", "Plaintext for YAMM merge (separate email)"),
    ("Packet_Password", "singleLineText", "Plaintext for YAMM merge (separate email)"),
]


def ensure_fields_exist(airtable_token: str) -> None:
    """Create security fields on the Venues table if they don't exist."""
    # Get the table ID for Venues
    endpoint = f"/meta/bases/{BASE_ID}/tables"
    result = api_call("GET", endpoint, airtable_token)

    table_id = None
    existing_fields: set = set()
    for t in result.get("tables", []):
        if t["name"] == VENUES_TABLE and not t["name"].startswith("[DELETE]"):
            table_id = t["id"]
            for f in t.get("fields", []):
                existing_fields.add(f["name"])
            break

    if not table_id:
        print(f"  Error: Could not find {VENUES_TABLE} table", file=sys.stderr)
        sys.exit(1)

    for field_name, field_type, description in SECURITY_FIELDS:
        if field_name in existing_fields:
            print(f"  Field '{field_name}' already exists", file=sys.stderr)
            continue

        body = {
            "name": field_name,
            "type": field_type,
            "description": description,
        }
        create_endpoint = f"/meta/bases/{BASE_ID}/tables/{table_id}/fields"
        api_call("POST", create_endpoint, airtable_token, body=body)
        print(f"  Created field '{field_name}' ({field_type})", file=sys.stderr)


def push_to_airtable(
    token_map: Dict[str, Any],
    airtable_token: str,
    dry_run: bool = False,
) -> int:
    """Write security fields back to Airtable Venues table.

    Fields written:
      - Host_Token: the URL token
      - Host_Helper_URL: full helper page URL
      - Financial_Password_Hash: SHA-256 hex for the password gate
      - Financial_Password: plaintext for YAMM merge (separate email)
      - Packet_Password: plaintext for YAMM merge (separate email)
    """
    # Airtable batch update: up to 10 records per PATCH
    updates: List[Dict[str, Any]] = []

    for name, entry in token_map.items():
        record_id = entry.get("record_id", "")
        if not record_id:
            print(f"  Skipping {name}: no Airtable record ID", file=sys.stderr)
            continue

        token = entry.get("token", "")
        helper_url = f"{HELPER_BASE_URL}{token}/" if token else ""

        updates.append({
            "id": record_id,
            "fields": {
                "Host_Token": token,
                "Host_Helper_URL": helper_url,
                "Financial_Password_Hash": entry.get("financial_password_hash", ""),
                "Financial_Password": entry.get("financial_password_plaintext", ""),
                "Packet_Password": entry.get("packet_password", ""),
            },
        })

    if not updates:
        print("  No records to push (no record IDs found).", file=sys.stderr)
        return 0

    if dry_run:
        for u in updates:
            name = next(
                (n for n, e in token_map.items() if e.get("record_id") == u["id"]),
                u["id"],
            )
            print(f"  [dry-run] Would update {name}: {list(u['fields'].keys())}")
        print(f"\n(dry run — {len(updates)} record(s) not written)", file=sys.stderr)
        return len(updates)

    # Batch in groups of 10 (Airtable limit)
    pushed = 0
    for i in range(0, len(updates), 10):
        batch = updates[i : i + 10]
        endpoint = f"/{BASE_ID}/{urllib.request.quote(VENUES_TABLE)}"
        body = {"records": batch}
        result = api_call("PATCH", endpoint, airtable_token, body=body)
        pushed += len(result.get("records", []))
        print(
            f"  Pushed batch {i // 10 + 1}: "
            f"{len(batch)} record(s)",
            file=sys.stderr,
        )

    print(f"  Pushed {pushed} venue(s) to Airtable", file=sys.stderr)
    return pushed


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate OEFF host security token map."
    )
    parser.add_argument(
        "--csv",
        metavar="FILE",
        help="Read venues from a CSV file instead of Airtable.",
    )
    parser.add_argument(
        "--regenerate",
        action="store_true",
        help="Force regeneration of all tokens and passwords (default: preserve existing).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing token-map.json.",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        help=f"Write token map to this path (default: {TOKEN_MAP_PATH}).",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push security fields (token, passwords, URLs) back to Airtable Venues table.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Fetch venues
    if args.csv:
        venues = fetch_venues_from_csv(args.csv)
    else:
        airtable_token = get_token()
        print("Fetching venues from Airtable...", file=sys.stderr)
        venues = fetch_venues_from_airtable(airtable_token)

    if not venues:
        print("Error: No venues found.", file=sys.stderr)
        return 1

    # Load existing map (for token preservation)
    existing = load_existing_map()
    preserved = sum(1 for v in venues if v["venue_name"] in existing)
    if preserved and not args.regenerate:
        print(
            f"  Preserving {preserved} existing token(s). "
            f"Use --regenerate to force new tokens.",
            file=sys.stderr,
        )

    # Generate
    token_map = generate_token_map(venues, existing, args.regenerate)
    print(f"  Generated token map for {len(token_map)} venue(s)", file=sys.stderr)

    # Output
    output_path = Path(args.output) if args.output else TOKEN_MAP_PATH

    if args.dry_run:
        # Show summary without plaintext passwords
        for name, entry in sorted(token_map.items()):
            print(f"  {name}: token={entry['token'][:8]}... hash={entry['financial_password_hash'][:12]}...")
        print(f"\n(dry run — {output_path} not written)", file=sys.stderr)
        return 0

    # Write token map
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(token_map, f, indent=2, ensure_ascii=False)
    print(f"Wrote token map to {output_path}", file=sys.stderr)

    # Summary
    new_count = len(token_map) - preserved if not args.regenerate else len(token_map)
    print(
        f"  {len(token_map)} total, {new_count} new, {preserved} preserved",
        file=sys.stderr,
    )

    # Push to Airtable if requested
    if args.push:
        if args.csv:
            print(
                "Error: --push requires Airtable (cannot push from CSV source).",
                file=sys.stderr,
            )
            return 1
        print("Ensuring security fields exist on Venues table...", file=sys.stderr)
        ensure_fields_exist(airtable_token)
        print("Pushing security fields to Airtable...", file=sys.stderr)
        push_to_airtable(token_map, airtable_token)

    return 0


if __name__ == "__main__":
    sys.exit(main())
