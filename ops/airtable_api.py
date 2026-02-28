#!/usr/bin/env python3
"""
airtable_api.py — Shared Airtable API functions for OEFF scripts

Extracted from generate-venue-sections.py. Provides paginated fetch,
filter queries, and linked record resolution against the OEFF Airtable base.

Stdlib Python 3 only — no pip dependencies.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_ID = "app9DymWrbAQaHH0K"
API = "https://api.airtable.com/v0"


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Read Airtable PAT from environment."""
    token = os.environ.get("AIRTABLE_TOKEN", "")
    if not token:
        print("Error: AIRTABLE_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return token


# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def api_call(method: str, endpoint: str, token: str) -> Dict[str, Any]:
    """Make an Airtable API call with retry and rate limit handling."""
    url = f"{API}{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            time.sleep(0.22)  # Stay under 5 req/s
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


# ---------------------------------------------------------------------------
# Paginated fetchers
# ---------------------------------------------------------------------------

def fetch_all_records(
    table: str, view: str, token: str
) -> List[Dict[str, Any]]:
    """Paginated fetch of all records from an Airtable view."""
    records: List[Dict[str, Any]] = []
    offset: Optional[str] = None
    page = 0

    while True:
        page += 1
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote(table)}"
            f"?view={urllib.request.quote(view)}"
        )
        if offset:
            endpoint += f"&offset={offset}"
        print(f"  Fetching page {page}...", file=sys.stderr)
        result = api_call("GET", endpoint, token)
        records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break

    print(
        f"  Fetched {len(records)} records from {table}/{view}",
        file=sys.stderr,
    )
    return records


def fetch_by_filter(
    table: str, formula: str, token: str
) -> List[Dict[str, Any]]:
    """Paginated fetch with a filterByFormula (no view required)."""
    records: List[Dict[str, Any]] = []
    offset: Optional[str] = None
    page = 0

    while True:
        page += 1
        encoded = urllib.request.quote(formula)
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote(table)}"
            f"?filterByFormula={encoded}"
        )
        if offset:
            endpoint += f"&offset={offset}"
        print(f"  Fetching page {page}...", file=sys.stderr)
        result = api_call("GET", endpoint, token)
        records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break

    print(
        f"  Fetched {len(records)} records from {table} (filtered)",
        file=sys.stderr,
    )
    return records


# ---------------------------------------------------------------------------
# Linked record resolution
# ---------------------------------------------------------------------------

def _fetch_by_ids(
    table: str, ids: set, token: str
) -> Dict[str, Dict[str, Any]]:
    """Fetch records by ID using filterByFormula OR()."""
    if not ids:
        return {}
    cache: Dict[str, Dict[str, Any]] = {}
    id_list = list(ids)

    # Airtable formula length limit — batch in groups of 20
    for i in range(0, len(id_list), 20):
        batch = id_list[i : i + 20]
        or_clauses = ",".join(f'RECORD_ID()="{rid}"' for rid in batch)
        formula = f"OR({or_clauses})"
        encoded = urllib.request.quote(formula)
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote(table)}"
            f"?filterByFormula={encoded}"
        )
        result = api_call("GET", endpoint, token)
        for rec in result.get("records", []):
            cache[rec["id"]] = rec

    print(
        f"  Resolved {len(cache)} linked {table} records",
        file=sys.stderr,
    )
    return cache
