#!/usr/bin/env python3
"""
Remove Eventbrite access codes from all OEFF 2026 events.

Queries all events for the OEC org, lists any access codes on each,
and deletes them. This makes tickets directly purchasable without
entering a code (the Squarespace password gate is the single access layer).

Usage:
    python3 oeff_eventbrite_remove_access_codes.py --dry-run   # List codes without deleting
    python3 oeff_eventbrite_remove_access_codes.py              # Delete all access codes

Environment:
    EVENTBRITE_TOKEN    — OAuth private token (from Eventbrite account settings)
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

API_BASE = "https://www.eventbriteapi.com/v3"
ORG_ID = "133838916899"

STATE_FILE = os.path.join(os.path.dirname(__file__), "eventbrite-state.json")


def get_token():
    token = os.environ.get("EVENTBRITE_TOKEN")
    if not token:
        print("ERROR: EVENTBRITE_TOKEN environment variable not set.")
        print("Get it from: Eventbrite > Account Settings > Developer > API Keys")
        sys.exit(1)
    return token


def api_get(path, token):
    """GET request to Eventbrite API."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code} on GET {path}: {body[:300]}")
        return None


def api_delete(path, token):
    """DELETE request to Eventbrite API."""
    url = f"{API_BASE}{path}"
    req = urllib.request.Request(url, method="DELETE", headers={
        "Authorization": f"Bearer {token}",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            return True
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code} on DELETE {path}: {body[:300]}")
        return False


def load_state():
    """Load state file for event IDs."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"events": {}}


def get_org_events(token):
    """Get all live events for the org (handles pagination)."""
    events = []
    page = 1
    while True:
        data = api_get(
            f"/organizations/{ORG_ID}/events/?status=live&page_size=50&page={page}",
            token
        )
        if not data or "events" not in data:
            break
        events.extend(data["events"])
        if not data.get("pagination", {}).get("has_more_items", False):
            break
        page += 1
        time.sleep(0.3)
    return events


def get_access_codes(event_id, token):
    """List access codes for an event."""
    data = api_get(f"/events/{event_id}/access_codes/", token)
    if not data:
        return []
    return data.get("access_codes", [])


def get_discount_codes(event_id, token):
    """List discount/promo codes for an event (separate from access codes)."""
    data = api_get(f"/events/{event_id}/discounts/", token)
    if not data:
        return []
    return data.get("discounts", [])


def main():
    dry_run = "--dry-run" in sys.argv
    token = get_token()

    if dry_run:
        print("=== DRY RUN — listing codes only, no deletions ===\n")
    else:
        print("=== REMOVING ACCESS CODES from all OEFF events ===\n")

    # Read 2026 event IDs directly from state file — no need to paginate
    # through all 700+ org events
    state = load_state()
    all_event_ids = []
    for row_key, event_data in state.get("events", {}).items():
        eid = event_data["event_id"]
        name = event_data.get("event_name", row_key)
        all_event_ids.append((eid, name))

    print(f"Checking {len(all_event_ids)} events from state file.\n")

    total_codes_found = 0
    total_codes_deleted = 0

    for event_id, event_name in all_event_ids:
        short_name = event_name[:60]
        print(f"Checking: {short_name} ({event_id})")

        # Check access codes
        access_codes = get_access_codes(event_id, token)
        time.sleep(0.3)

        # Check discount/promo codes
        discounts = get_discount_codes(event_id, token)
        time.sleep(0.3)

        if not access_codes and not discounts:
            print("  No codes found.\n")
            continue

        for code in access_codes:
            code_id = code.get("id")
            code_text = code.get("code", "???")
            total_codes_found += 1
            print(f"  ACCESS CODE: '{code_text}' (id: {code_id})")

            if not dry_run:
                ok = api_delete(f"/events/{event_id}/access_codes/{code_id}/", token)
                if ok:
                    print(f"    DELETED.")
                    total_codes_deleted += 1
                else:
                    print(f"    FAILED to delete.")
                time.sleep(0.3)

        for disc in discounts:
            disc_id = disc.get("id")
            disc_code = disc.get("code", "???")
            disc_type = disc.get("type", "unknown")
            total_codes_found += 1
            print(f"  DISCOUNT/PROMO: '{disc_code}' type={disc_type} (id: {disc_id})")

            if not dry_run:
                ok = api_delete(f"/discounts/{disc_id}/", token)
                if ok:
                    print(f"    DELETED.")
                    total_codes_deleted += 1
                else:
                    print(f"    FAILED to delete.")
                time.sleep(0.3)

        print()

    # Summary
    print("=" * 50)
    print(f"Events checked:  {len(all_event_ids)}")
    print(f"Codes found:     {total_codes_found}")
    if dry_run:
        print(f"\nDry run complete. Re-run without --dry-run to delete.")
    else:
        print(f"Codes deleted:   {total_codes_deleted}")
        if total_codes_found > total_codes_deleted:
            print(f"FAILED:          {total_codes_found - total_codes_deleted}")
        if total_codes_deleted > 0:
            print(f"\nAccess codes removed. Tickets are now directly purchasable.")
            print(f"The Squarespace password (OEFF2026) remains the single gate.")


if __name__ == "__main__":
    main()
