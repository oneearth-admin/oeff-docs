#!/usr/bin/env python3
"""Validate OEFF Eventbrite event links are accessible without password gates.

Checks every event in eventbrite-state.json by hitting the public URL and
inspecting the response for: password inputs, error pages, redirects, and
ticket availability.

Usage:
    python3 oeff_eventbrite_validate.py              # Check all events
    python3 oeff_eventbrite_validate.py --api         # Also check API status fields
    EVENTBRITE_TOKEN=xxx python3 oeff_eventbrite_validate.py --api

Exit codes:
    0 = all events pass
    1 = one or more events have issues
"""
import json, os, sys, time, urllib.request, urllib.error

STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eventbrite-state.json")
API = "https://www.eventbriteapi.com/v3"

def load_state():
    with open(STATE_FILE) as f:
        return json.load(f)

def check_public_page(event_id):
    """Hit the public event URL and check for password gates or errors."""
    url = f"https://www.eventbrite.com/e/{event_id}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            final_url = resp.url
            status = resp.status
    except urllib.error.HTTPError as e:
        return {"status": e.code, "ok": False, "issue": f"HTTP {e.code}"}
    except Exception as e:
        return {"status": 0, "ok": False, "issue": str(e)[:80]}

    issues = []

    # Check for password gate
    if 'type="password"' in body or "Enter event password" in body:
        issues.append("PASSWORD_GATE")

    # Check for error/not-found pages
    if "This event has been cancelled" in body:
        issues.append("CANCELLED")
    if "This event has ended" in body:
        issues.append("ENDED")
    if "Sorry, this event is not available" in body:
        issues.append("NOT_AVAILABLE")
    if "page not found" in body.lower() or "<title>404" in body.lower():
        issues.append("404_PAGE")

    # Check for ticket availability signals
    has_tickets = any(kw in body for kw in ["Register", "Get tickets", "Get Tickets", "Tickets"])

    return {
        "status": status,
        "ok": len(issues) == 0,
        "issues": issues,
        "has_tickets": has_tickets,
        "final_url": final_url,
    }


def check_api_status(event_id, token):
    """Check event status via REST API."""
    req = urllib.request.Request(
        f"{API}/events/{event_id}/",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return {
                "status": data.get("status"),
                "listed": data.get("listed"),
                "shareable": data.get("shareable"),
                "privacy": data.get("privacy_setting"),
            }
    except Exception as e:
        return {"error": str(e)[:80]}


def main():
    use_api = "--api" in sys.argv
    token = os.environ.get("EVENTBRITE_TOKEN") if use_api else None

    if use_api and not token:
        print("WARNING: --api flag set but EVENTBRITE_TOKEN not found. Skipping API checks.\n")
        use_api = False

    state = load_state()
    events = state.get("events", {})

    if not events:
        print("No events found in state file.")
        sys.exit(0)

    print(f"Validating {len(events)} events...\n")

    passed = 0
    failed = 0
    results = []

    for row_key, event in sorted(events.items()):
        eid = event["event_id"]
        name = event.get("event_name", row_key)
        short_name = name.replace("OEFF 2026: ", "")[:50]

        result = check_public_page(eid)
        time.sleep(0.5)  # polite

        api_info = ""
        if use_api:
            api = check_api_status(eid, token)
            time.sleep(0.3)
            if "error" not in api:
                api_info = f"  API: status={api['status']} listed={api['listed']} shareable={api['shareable']}"

        if result["ok"]:
            tickets = "tickets=yes" if result.get("has_tickets") else "tickets=?"
            print(f"  PASS  {short_name} ({eid}) [{tickets}]{api_info}")
            passed += 1
        else:
            issues_str = ", ".join(result.get("issues", [result.get("issue", "unknown")]))
            print(f"  FAIL  {short_name} ({eid}) [{issues_str}]{api_info}")
            failed += 1
            results.append({"row": row_key, "event_id": eid, "name": short_name, "issues": issues_str})

    print(f"\n{'='*60}")
    print(f"Passed: {passed}  Failed: {failed}  Total: {passed + failed}")

    if failed > 0:
        print(f"\nFailed events:")
        for r in results:
            print(f"  {r['name']} ({r['event_id']}): {r['issues']}")
        print(f"\nFix: unpublish via API, then republish through Eventbrite dashboard UI.")
        sys.exit(1)
    else:
        print("\nAll events accessible via direct link. No password gates detected.")
        sys.exit(0)


if __name__ == "__main__":
    main()
