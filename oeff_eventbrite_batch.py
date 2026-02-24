#!/usr/bin/env python3
"""
OEFF 2026 Eventbrite Batch Event Creator

Reads the Google Sheet (exported as CSV), validates data consistency,
and creates events via the Eventbrite REST API v3.

Usage:
    python3 oeff_eventbrite_batch.py validate          # Check data, report gaps
    python3 oeff_eventbrite_batch.py setup              # Create org profile + venues
    python3 oeff_eventbrite_batch.py create             # Create draft events + tickets (unlisted)
    python3 oeff_eventbrite_batch.py publish            # Publish drafts as unlisted (Josh reviews via link)
    python3 oeff_eventbrite_batch.py go-live            # Flip published events to listed (public/searchable)
    python3 oeff_eventbrite_batch.py status             # Show current event statuses

Environment:
    EVENTBRITE_TOKEN    — OAuth private token (from Eventbrite account settings)

Data source:
    Google Sheet: https://docs.google.com/spreadsheets/d/1kQT-MeA3CyXUN3NO3eJTd63uD9pJegxhqTG6SAvfR9Q/
    Exported as CSV on each run (no Google API dependency).
"""

import csv
import io
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta, timezone

# ── Config ──────────────────────────────────────────────────────────

SHEET_ID = "1kQT-MeA3CyXUN3NO3eJTd63uD9pJegxhqTG6SAvfR9Q"
SHEET_CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

API_BASE = "https://www.eventbriteapi.com/v3"
TIMEZONE = "America/Chicago"
CURRENCY = "USD"
DEFAULT_CAPACITY = 100  # default ticket quantity if not specified
DEFAULT_DURATION_HOURS = 2  # fallback if end time missing (for validation only)

# Chicago CDT offset (April = CDT = UTC-5)
CDT_OFFSET = timezone(timedelta(hours=-5))

STATE_FILE = os.path.join(os.path.dirname(__file__), "eventbrite-state.json")
LOCAL_CSV = os.path.join(os.path.dirname(__file__), "eventbrite-setup-for-josh.csv")

# Description template — placeholder until Josh provides the real one
DESCRIPTION_TEMPLATE = """<h3>{film_title}</h3>
<p>Join us for a community screening as part of the <strong>One Earth Environmental Film Festival 2026</strong>.</p>
<p><strong>Venue:</strong> {venue_name}<br>
<strong>Address:</strong> {address}</p>
{age_advisory_html}
<p>The One Earth Film Festival inspires Chicagoland communities to take action
for a healthy planet through the power of film. Learn more at
<a href="https://www.oneearthfilmfest.org">oneearthfilmfest.org</a>.</p>"""


def format_age_advisory_html(age_str):
    """Format age advisory for event description HTML.

    Returns an HTML paragraph for the advisory, or empty string if none.
    """
    if not age_str or age_str.upper() == "TBD":
        return ""
    # Bold the advisory if it contains "18+" or "ONLY"
    if "18+" in age_str or "ONLY" in age_str.upper():
        return f'<p><strong>Content Advisory: {age_str}</strong></p>'
    return f"<p><em>Suggested audience: {age_str}</em></p>"


# ── State management ────────────────────────────────────────────────

def load_state():
    """Load venue IDs and event IDs from previous runs."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"venues": {}, "events": {}, "org_id": None}


def save_state(state):
    """Persist venue IDs and event IDs for reuse."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"  State saved → {STATE_FILE}")


# ── API helpers ─────────────────────────────────────────────────────

def get_token():
    """Read token from environment."""
    token = os.environ.get("EVENTBRITE_TOKEN")
    if not token:
        print("ERROR: Set EVENTBRITE_TOKEN environment variable.")
        print("  Get your token from: Eventbrite → Account Settings → Developer → API Keys")
        sys.exit(1)
    return token


def api_request(method, path, data=None, token=None):
    """Make an authenticated Eventbrite API request. Returns parsed JSON."""
    url = f"{API_BASE}{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"  API ERROR {e.code}: {error_body}")
        try:
            return {"error": True, "status_code": e.code, **json.loads(error_body)}
        except json.JSONDecodeError:
            return {"error": True, "status_code": e.code, "message": error_body}


def get_org_id(token):
    """Discover the organization ID for this token."""
    result = api_request("GET", "/users/me/organizations/", token=token)
    if "error" in result:
        print("ERROR: Could not fetch organization. Is your token valid?")
        sys.exit(1)
    orgs = result.get("organizations", [])
    if not orgs:
        print("ERROR: No organizations found for this token.")
        sys.exit(1)
    if len(orgs) > 1:
        print("Multiple orgs found:")
        for i, org in enumerate(orgs):
            print(f"  [{i}] {org['name']} (id: {org['id']})")
        print("Using the first one. Set org_id in state file to override.")
    org = orgs[0]
    print(f"  Organization: {org['name']} (id: {org['id']})")
    return org["id"]


# ── CSV reader ──────────────────────────────────────────────────────

def fetch_sheet():
    """Download the Google Sheet as CSV, falling back to local CSV.

    The Google Sheet export requires the sheet to be publicly shared
    or the script to run with auth. Falls back to the local CSV backup
    which may be slightly stale (pre-cleanup addresses).
    """
    # Try Google Sheet export first
    try:
        print(f"Fetching sheet → {SHEET_CSV_URL[:80]}...")
        req = urllib.request.Request(SHEET_CSV_URL)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8-sig")
        print("  (live from Google Sheets)")
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(f"  Sheet not accessible ({e}), using local CSV...")
        if not os.path.exists(LOCAL_CSV):
            print(f"ERROR: Local CSV not found: {LOCAL_CSV}")
            sys.exit(1)
        with open(LOCAL_CSV, encoding="utf-8-sig") as f:
            raw = f.read()
        print(f"  (from {os.path.basename(LOCAL_CSV)})")

    reader = csv.DictReader(io.StringIO(raw))
    rows = []
    for i, row in enumerate(reader, start=2):  # row 2 = first data row
        row["_row"] = i
        rows.append(row)

    print(f"  {len(rows)} rows loaded.")
    return rows


def _col(row, *candidates):
    """Try multiple column name variants, return first match."""
    for key in candidates:
        val = row.get(key)
        if val is not None:
            return val.strip()
    return ""


def normalize_row(row):
    """Clean and normalize a single row into a consistent dict.

    Handles column naming variants between Google Sheet and local CSV.
    """
    return {
        "row": row["_row"],
        "event_name": _col(row, "Event Name"),
        "venue_name": _col(row, "Venue", "Venue Name"),
        "address_raw": _col(row, "Address", "Venue Address"),
        "date": _col(row, "Date"),
        "start_time": _col(row, "Start Time"),
        "end_time": _col(row, "End Time"),
        "film_title": _col(row, "Film Title"),
        "age_advisory": _col(row, "Age Group/Content Advisory"),
        "ticket_price": _col(row, "Ticket Price"),
        "event_type": _col(row, "Type", "Event Type"),
        "rep": _col(row, "Rep", "OEFF Rep"),
        "notes": _col(row, "Notes", "Josh TODO / Notes"),
    }


# ── Data parsing ────────────────────────────────────────────────────

def parse_address(address_raw):
    """Parse an address string into Eventbrite venue address fields.

    Expected formats:
        "1104 S Wabash Ave, Chicago IL 60605"
        "2000 Fifth Ave, Bldg R Rm 221, River Grove IL 60171"
        "TBD — possibly OPRF High School"  (returns None)
    """
    if not address_raw or "TBD" in address_raw.upper():
        return None

    # Remove venue name prefixes (e.g., "Film Row Cinema, 1104 S Wabash...")
    # We detect these by checking if the first segment doesn't start with a digit
    parts = [p.strip() for p in address_raw.split(",")]

    # Find the part that looks like a street address (starts with digit)
    street_start = 0
    for i, part in enumerate(parts):
        if part and part[0].isdigit():
            street_start = i
            break

    # If nothing starts with a digit, take the whole thing as address_1
    if not parts[street_start][0:1].isdigit():
        return {"address_1": address_raw, "city": "", "region": "", "postal_code": "", "country": "US"}

    # The last part should be "City ST ZIP" or "City ST"
    last = parts[-1].strip()
    city_state_zip = last.split()

    postal_code = ""
    region = ""
    city_parts = []

    # Walk backwards: zip (if digits), then state (2-letter), then city
    if city_state_zip and city_state_zip[-1].isdigit():
        postal_code = city_state_zip.pop()
    if city_state_zip and len(city_state_zip[-1]) == 2 and city_state_zip[-1].isalpha():
        region = city_state_zip.pop().upper()
    city_parts = city_state_zip

    # Street address is everything between street_start and the last part
    street_parts = parts[street_start:-1] if len(parts) > 1 else [parts[0]]
    address_1 = street_parts[0] if street_parts else ""
    address_2 = ", ".join(street_parts[1:]) if len(street_parts) > 1 else ""

    return {
        "address_1": address_1,
        "address_2": address_2,
        "city": " ".join(city_parts),
        "region": region,
        "postal_code": postal_code,
        "country": "US",
    }


def parse_time_to_utc(date_str, time_str):
    """Convert 'YYYY-MM-DD' + '6:30 PM' to Eventbrite UTC format.

    Returns: "2026-04-23T23:30:00Z" (UTC string for CDT input)
    """
    if not date_str or not time_str:
        return None

    # Normalize time string
    time_str = time_str.strip().upper()
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M %p")
    except ValueError:
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %I:%M%p")
        except ValueError:
            return None

    # Attach CDT timezone and convert to UTC
    dt_local = dt.replace(tzinfo=CDT_OFFSET)
    dt_utc = dt_local.astimezone(timezone.utc)
    return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_ticket_price(price_str):
    """Parse ticket price string into ticket class specs.

    Returns list of dicts, each representing one ticket class:
        [{"name": "General Admission", "free": True}]
        [{"name": "Single Ticket", "free": False, "cost": "USD,7500"},
         {"name": "Two-Pack", "free": False, "cost": "USD,15000", "min_qty": 2, "max_qty": 2}]
    """
    if not price_str or price_str.lower() == "free":
        return [{"name": "General Admission", "free": True, "quantity_total": DEFAULT_CAPACITY}]

    # Handle "$75 ea / two for $150" pattern
    if "/" in price_str:
        tiers = []
        parts = price_str.split("/")
        for part in parts:
            part = part.strip()
            # Extract dollar amount
            dollars = None
            for word in part.replace("$", " $ ").split():
                if word == "$":
                    continue
                try:
                    dollars = int(float(word))
                    break
                except ValueError:
                    continue

            if dollars is None:
                continue

            cents = dollars * 100
            if "two" in part.lower() or "pair" in part.lower() or "2" in part:
                tiers.append({
                    "name": "Two-Pack",
                    "free": False,
                    "cost": f"USD,{cents}",
                    "quantity_total": DEFAULT_CAPACITY,
                    "min_qty": 2,
                    "max_qty": 2,
                })
            else:
                tiers.append({
                    "name": "General Admission",
                    "free": False,
                    "cost": f"USD,{cents}",
                    "quantity_total": DEFAULT_CAPACITY,
                })
        return tiers if tiers else [{"name": "General Admission", "free": True, "quantity_total": DEFAULT_CAPACITY}]

    # Handle simple "$XX" pattern
    price_str_clean = price_str.replace("$", "").strip()
    try:
        dollars = int(float(price_str_clean))
        return [{
            "name": "General Admission",
            "free": False,
            "cost": f"USD,{dollars * 100}",
            "quantity_total": DEFAULT_CAPACITY,
        }]
    except ValueError:
        return [{"name": "General Admission", "free": True, "quantity_total": DEFAULT_CAPACITY}]


# ── Validation ──────────────────────────────────────────────────────

def validate(rows):
    """Validate all rows and report issues. Returns (ready, not_ready) lists."""
    ready = []
    not_ready = []

    # Track venue dedup
    venue_addresses = {}

    print("\n═══ VALIDATION REPORT ═══\n")

    for row in rows:
        r = normalize_row(row)
        issues = []
        warnings = []

        # Required fields
        if not r["event_name"]:
            issues.append("Missing event name")
        if not r["venue_name"]:
            issues.append("Missing venue name")
        if not r["date"]:
            issues.append("Missing date")
        if not r["start_time"]:
            issues.append("Missing start time")
        if not r["end_time"]:
            warnings.append("Missing end time (will default to +2h)")

        # Address quality
        addr = parse_address(r["address_raw"])
        if addr is None:
            issues.append(f"Address not usable: '{r['address_raw']}'")
        elif not addr.get("postal_code"):
            warnings.append("Address missing zip code")
        elif not addr.get("region"):
            warnings.append("Address missing state")

        # Film title
        if not r["film_title"] or r["film_title"].upper() == "TBD":
            warnings.append("Film title TBD")
        if "(pending)" in r["film_title"].lower():
            warnings.append("Film title marked (pending)")

        # Age advisory
        if not r["age_advisory"]:
            warnings.append("No age/content advisory set")
        elif r["age_advisory"].upper() == "TBD":
            warnings.append("Age advisory TBD")
        if "18+" in r.get("age_advisory", ""):
            warnings.append("18+ content — will be flagged prominently in description")

        # Time parsing
        start_utc = parse_time_to_utc(r["date"], r["start_time"])
        if r["start_time"] and not start_utc:
            issues.append(f"Cannot parse start time: '{r['start_time']}'")

        if r["end_time"]:
            end_utc = parse_time_to_utc(r["date"], r["end_time"])
            if not end_utc:
                issues.append(f"Cannot parse end time: '{r['end_time']}'")

        # Ticket parsing
        tickets = parse_ticket_price(r["ticket_price"])

        # Notes flags
        if "UNSCHEDULED" in r["notes"].upper():
            issues.append("Marked as UNSCHEDULED PLACEHOLDER")
        if "Q:" in r["notes"]:
            warnings.append("Has open question in Notes")

        # Venue dedup tracking
        venue_key = r["venue_name"].lower().strip()
        if venue_key in venue_addresses:
            if venue_addresses[venue_key] != r["address_raw"]:
                warnings.append(f"Same venue, different address vs row {venue_addresses[venue_key]}")
        venue_addresses[venue_key] = r["address_raw"]

        # Classify
        r["_issues"] = issues
        r["_warnings"] = warnings
        r["_tickets"] = tickets
        r["_address"] = addr
        r["_start_utc"] = start_utc

        if issues:
            not_ready.append(r)
        else:
            ready.append(r)

    # Print results
    print(f"READY to create:     {len(ready)} events")
    print(f"NOT READY (blocked): {len(not_ready)} events")
    print()

    if ready:
        print("── Ready ──")
        for r in ready:
            warn_str = f"  ⚠ {'; '.join(r['_warnings'])}" if r["_warnings"] else ""
            ticket_str = "FREE" if r["_tickets"][0]["free"] else r["_tickets"][0].get("cost", "?")
            age_str = r.get("age_advisory", "") or "—"
            print(f"  Row {r['row']:2d}  {r['date']}  {r['start_time']:>8s}  {ticket_str:>10s}  [{age_str:>16s}]  {r['event_name']}")
            if warn_str:
                print(f"         {warn_str}")
        print()

    if not_ready:
        print("── Not Ready ──")
        for r in not_ready:
            print(f"  Row {r['row']:2d}  {r['event_name']}")
            for issue in r["_issues"]:
                print(f"         BLOCKER: {issue}")
            for warn in r["_warnings"]:
                print(f"         warning: {warn}")
        print()

    # Venue dedup summary
    unique_venues = {}
    for r in ready + not_ready:
        vn = r["venue_name"]
        if vn and vn not in unique_venues:
            unique_venues[vn] = r["address_raw"]
    print(f"── Unique venues: {len(unique_venues)} ──")
    for name, addr in sorted(unique_venues.items()):
        print(f"  {name}")
        print(f"    → {addr}")
    print()

    # Ticket tier summary
    has_paid = [r for r in ready + not_ready if r["_tickets"] and not r["_tickets"][0]["free"]]
    if has_paid:
        print("── Paid events ──")
        for r in has_paid:
            for t in r["_tickets"]:
                print(f"  Row {r['row']:2d}  {t['name']}: {t.get('cost', '?')}")
        print()

    return ready, not_ready


# ── API operations ──────────────────────────────────────────────────

def cmd_setup(token, state):
    """Phase 1: Discover org, create venues."""
    # Get org ID
    if not state.get("org_id"):
        state["org_id"] = get_org_id(token)
        save_state(state)
    else:
        print(f"  Organization: {state['org_id']} (cached)")

    org_id = state["org_id"]

    # Fetch sheet and find unique venues
    rows = fetch_sheet()
    venues_needed = {}
    for row in rows:
        r = normalize_row(row)
        addr = parse_address(r["address_raw"])
        if r["venue_name"] and addr and r["venue_name"] not in venues_needed:
            venues_needed[r["venue_name"]] = {"name": r["venue_name"], "address": addr}

    print(f"\n  {len(venues_needed)} unique venues to create.")

    created = 0
    skipped = 0
    for venue_name, venue_data in venues_needed.items():
        if venue_name in state.get("venues", {}):
            print(f"  SKIP (exists): {venue_name} → {state['venues'][venue_name]}")
            skipped += 1
            continue

        payload = {
            "venue": {
                "name": venue_data["name"],
                "address": venue_data["address"],
            }
        }

        print(f"  Creating venue: {venue_name}...")
        result = api_request("POST", f"/organizations/{org_id}/venues/", data=payload, token=token)

        if result.get("error"):
            print(f"    FAILED: {result}")
            continue

        venue_id = result["id"]
        state.setdefault("venues", {})[venue_name] = venue_id
        save_state(state)
        print(f"    OK → venue_id: {venue_id}")
        created += 1

    print(f"\n  Venues: {created} created, {skipped} already existed.")


def cmd_create(token, state):
    """Phase 2: Create draft events and ticket classes."""
    org_id = state.get("org_id")
    if not org_id:
        print("ERROR: Run 'setup' first to discover org_id and create venues.")
        sys.exit(1)

    rows = fetch_sheet()
    ready, not_ready = validate(rows)

    if not ready:
        print("No events ready to create. Fix the blockers above first.")
        return

    print(f"\n═══ CREATING {len(ready)} EVENTS ═══\n")

    created = 0
    for r in ready:
        event_key = f"row_{r['row']}"

        if event_key in state.get("events", {}):
            print(f"  SKIP (exists): Row {r['row']} {r['event_name']} → {state['events'][event_key]['event_id']}")
            continue

        # Build event payload
        start_utc = parse_time_to_utc(r["date"], r["start_time"])
        if r["end_time"]:
            end_utc = parse_time_to_utc(r["date"], r["end_time"])
        else:
            # Default: start + 2 hours
            start_dt = datetime.strptime(start_utc, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            end_dt = start_dt + timedelta(hours=DEFAULT_DURATION_HOURS)
            end_utc = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        venue_id = state.get("venues", {}).get(r["venue_name"])

        age_html = format_age_advisory_html(r.get("age_advisory", ""))
        description = DESCRIPTION_TEMPLATE.format(
            film_title=r["film_title"],
            venue_name=r["venue_name"],
            address=r["address_raw"],
            age_advisory_html=age_html,
        )

        event_payload = {
            "event": {
                "name": {"html": r["event_name"]},
                "description": {"html": description},
                "start": {"timezone": TIMEZONE, "utc": start_utc},
                "end": {"timezone": TIMEZONE, "utc": end_utc},
                "currency": CURRENCY,
                "online_event": False,
                "listed": False,
                "shareable": False,
            }
        }

        if venue_id:
            event_payload["event"]["venue_id"] = venue_id

        print(f"  Creating: Row {r['row']} — {r['event_name']}...")
        result = api_request("POST", f"/organizations/{org_id}/events/", data=event_payload, token=token)

        if result.get("error"):
            print(f"    FAILED: {result}")
            continue

        event_id = result["id"]
        print(f"    OK → event_id: {event_id}")

        # Create ticket classes
        tickets = r["_tickets"]
        ticket_ids = []
        for ticket in tickets:
            tc_payload = {
                "ticket_class": {
                    "name": ticket["name"],
                    "free": ticket["free"],
                    "quantity_total": ticket.get("quantity_total", DEFAULT_CAPACITY),
                }
            }
            if not ticket["free"] and "cost" in ticket:
                tc_payload["ticket_class"]["cost"] = ticket["cost"]
            if "min_qty" in ticket:
                tc_payload["ticket_class"]["minimum_quantity"] = ticket["min_qty"]
            if "max_qty" in ticket:
                tc_payload["ticket_class"]["maximum_quantity"] = ticket["max_qty"]

            print(f"    Ticket: {ticket['name']} ({'free' if ticket['free'] else ticket.get('cost', '?')})...")
            tc_result = api_request("POST", f"/events/{event_id}/ticket_classes/", data=tc_payload, token=token)
            if tc_result.get("error"):
                print(f"      FAILED: {tc_result}")
            else:
                ticket_ids.append(tc_result["id"])
                print(f"      OK → ticket_class_id: {tc_result['id']}")

        # Save state
        state.setdefault("events", {})[event_key] = {
            "event_id": event_id,
            "event_name": r["event_name"],
            "age_advisory": r.get("age_advisory", ""),
            "ticket_ids": ticket_ids,
            "published": False,
            "listed": False,
        }
        save_state(state)
        created += 1

    print(f"\n  Events created: {created}")
    print(f"  Total in state: {len(state.get('events', {}))}")
    print(f"\n  Next step: review drafts on Eventbrite, then run 'publish'.")


def cmd_publish(token, state):
    """Phase 3: Publish all draft events (still unlisted — review via direct links)."""
    events = state.get("events", {})
    if not events:
        print("No events in state. Run 'create' first.")
        return

    unpublished = {k: v for k, v in events.items() if not v.get("published")}
    if not unpublished:
        print("All events already published.")
        return

    print(f"\n═══ PUBLISHING {len(unpublished)} EVENTS (unlisted) ═══\n")
    print("  Events will be live but NOT searchable on Eventbrite.")
    print("  Share direct links with Josh for review.")
    print("  Run 'go-live' when ready to make them public.\n")

    for key, info in unpublished.items():
        event_id = info["event_id"]
        print(f"  Publishing: {info['event_name']}...")
        result = api_request("POST", f"/events/{event_id}/publish/", token=token)

        if result.get("error"):
            print(f"    FAILED: {result}")
            continue

        info["published"] = True
        save_state(state)
        event_url = f"https://www.eventbrite.com/e/{event_id}"
        print(f"    OK — unlisted at {event_url}")

    published_count = sum(1 for v in events.values() if v.get("published"))
    print(f"\n  Published (unlisted): {published_count}/{len(events)}")
    print(f"  Next: review links, then run 'go-live' to make searchable.")


def cmd_go_live(token, state):
    """Phase 4: Flip published events from unlisted to listed (public/searchable)."""
    events = state.get("events", {})
    if not events:
        print("No events in state. Run 'create' first.")
        return

    # Only events that are published but not yet listed
    candidates = {k: v for k, v in events.items()
                  if v.get("published") and not v.get("listed")}
    if not candidates:
        already_live = sum(1 for v in events.values() if v.get("listed"))
        if already_live:
            print(f"All {already_live} events are already listed (public).")
        else:
            print("No published events to make public. Run 'publish' first.")
        return

    print(f"\n═══ GOING LIVE: {len(candidates)} EVENTS ═══\n")
    print("  This will make events searchable on Eventbrite.\n")

    made_live = 0
    for key, info in candidates.items():
        event_id = info["event_id"]
        print(f"  Listing: {info['event_name']}...")

        payload = {
            "event": {
                "listed": True,
                "shareable": True,
            }
        }
        result = api_request("POST", f"/events/{event_id}/", data=payload, token=token)

        if result.get("error"):
            print(f"    FAILED: {result}")
            continue

        info["listed"] = True
        save_state(state)
        print(f"    OK — now public and searchable")
        made_live += 1

    listed_count = sum(1 for v in events.values() if v.get("listed"))
    print(f"\n  Now public: {listed_count}/{len(events)}")


def cmd_status(token, state):
    """Show current state of all tracked events."""
    print("\n═══ EVENTBRITE STATE ═══\n")
    print(f"  Org ID: {state.get('org_id', 'not set')}")
    print(f"  Venues: {len(state.get('venues', {}))}")
    print(f"  Events: {len(state.get('events', {}))}")
    print()

    venues = state.get("venues", {})
    if venues:
        print("── Venues ──")
        for name, vid in sorted(venues.items()):
            print(f"  {name} → {vid}")
        print()

    events = state.get("events", {})
    if events:
        print("── Events ──")
        for key, info in sorted(events.items()):
            if info.get("listed"):
                status = "PUBLIC"
            elif info.get("published"):
                status = "UNLISTED"
            else:
                status = "DRAFT"
            age = info.get("age_advisory", "")
            age_tag = f" [{age}]" if age else ""
            print(f"  [{status:>8s}] {info['event_name']}{age_tag}")
            print(f"            event_id: {info['event_id']}")
            if info.get("published"):
                print(f"            url: https://www.eventbrite.com/e/{info['event_id']}")
        print()


# ── Main ────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    command = sys.argv[1].lower()
    state = load_state()

    if command == "validate":
        rows = fetch_sheet()
        validate(rows)
        return

    token = get_token()

    if command == "setup":
        cmd_setup(token, state)
    elif command == "create":
        cmd_create(token, state)
    elif command == "publish":
        cmd_publish(token, state)
    elif command in ("go-live", "golive"):
        cmd_go_live(token, state)
    elif command == "status":
        cmd_status(token, state)
    else:
        print(f"Unknown command: {command}")
        print("Commands: validate, setup, create, publish, go-live, status")
        sys.exit(1)


if __name__ == "__main__":
    main()
