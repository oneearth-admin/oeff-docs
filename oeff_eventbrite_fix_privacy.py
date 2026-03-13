#!/usr/bin/env python3
"""Fix 'Private event' password gates on OEFF 2026 Eventbrite events.

Strategy: Toggle listed=true (to clear the 'Private' publish state), then
immediately set listed=false again so events stay unlisted/unsearchable.
This resets the internal state to match the original 14 events: published,
unlisted, but accessible via direct link with no password gate.

Usage:
    EVENTBRITE_TOKEN=xxx python3 oeff_eventbrite_fix_privacy.py
    EVENTBRITE_TOKEN=xxx python3 oeff_eventbrite_fix_privacy.py --dry-run
    EVENTBRITE_TOKEN=xxx python3 oeff_eventbrite_fix_privacy.py --test-one
"""
import json, os, sys, time, urllib.request, urllib.error

API = "https://www.eventbriteapi.com/v3"

token = os.environ.get("EVENTBRITE_TOKEN")
if not token:
    print("ERROR: EVENTBRITE_TOKEN not set")
    sys.exit(1)

dry_run = "--dry-run" in sys.argv
test_one = "--test-one" in sys.argv

# These events were created with 'Private' publish setting
# and have a password gate on their public pages.
# row_19 (Beyond Zero @Uncommon Ground, 1984830234662) was already
# fixed with listed=true only — include it so we can set it back to false.
FIX_IDS = [
    ("1984830234662", "Beyond Zero @Uncommon Ground"),
    ("1984831685000", "Rooted + Planetwalker @IIT"),
    ("1984885724634", "How to Power a City @OPRFHS"),
    ("1984886808877", "Chasing Time/Planetwalker @Euclid"),
    ("1984888976360", "Chasing Time + Planetwalker @Park Ridge"),
    ("1984828763261", "40 Acres @Urban Essentials Cafe"),
    ("1984985499062", "Whose Water? @Epiphany"),
    ("1984898199948", "Action Fair @Chicago Cultural Center"),
    ("1984895433674", "In Our Nature @Chicago Cultural Center"),
    ("1984832697027", "Rooted @Dominican"),
    ("1984883717631", "Rooted @Dominican (Hybrid)"),
]

if test_one:
    FIX_IDS = FIX_IDS[:1]
    print("=== TEST MODE — fixing only first event ===\n")

if dry_run:
    print("=== DRY RUN — would toggle these events ===\n")
    for eid, name in FIX_IDS:
        print(f"  {name} ({eid})")
    print(f"\n{len(FIX_IDS)} events. Re-run without --dry-run to apply.")
    sys.exit(0)


def api_post(event_id, payload_dict):
    """POST update to an event. Returns response dict or None."""
    payload = json.dumps(payload_dict).encode()
    req = urllib.request.Request(
        f"{API}/events/{event_id}/",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(f"    HTTP {e.code}: {body[:200]}")
        return None


print(f"Fixing privacy on {len(FIX_IDS)} events (toggle listed on→off)...\n")

success = 0
failed = 0

for eid, name in FIX_IDS:
    print(f"  {name} ({eid})")

    # Step 1: Set listed=true to clear 'Private' state
    print("    Step 1: listed=true, shareable=true ...")
    r1 = api_post(eid, {"event": {"listed": True, "shareable": True}})
    if not r1:
        print("    FAILED at step 1.")
        failed += 1
        continue
    time.sleep(0.5)

    # Step 2: Set listed=false to return to unlisted (no search visibility)
    print("    Step 2: listed=false (back to unlisted) ...")
    r2 = api_post(eid, {"event": {"listed": False}})
    if not r2:
        print("    FAILED at step 2.")
        failed += 1
        continue

    listed = r2.get("listed", "?")
    shareable = r2.get("shareable", "?")
    print(f"    Done. listed={listed}, shareable={shareable}")
    success += 1
    time.sleep(0.3)

print(f"\n{'='*50}")
print(f"Fixed: {success}  Failed: {failed}")
if success > 0:
    print("\nToggle complete. Test a link in browser to verify:")
    print("  - No password gate")
    print("  - Not showing up in Eventbrite search")
