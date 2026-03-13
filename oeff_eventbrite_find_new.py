#!/usr/bin/env python3
"""Find Eventbrite events not yet in state file."""
import json, os, sys, urllib.request, time

token = os.environ.get("EVENTBRITE_TOKEN")
if not token:
    print("ERROR: EVENTBRITE_TOKEN not set")
    sys.exit(1)

API = "https://www.eventbriteapi.com/v3"
ORG_ID = "133838916899"

with open(os.path.join(os.path.dirname(__file__), "eventbrite-state.json")) as f:
    state = json.load(f)
known_ids = {v["event_id"] for v in state["events"].values()}

events = []
page = 1
while True:
    url = f"{API}/organizations/{ORG_ID}/events/?status=live&time_filter=current_future&page_size=50&page={page}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())
    events.extend(data.get("events", []))
    if not data.get("pagination", {}).get("has_more_items", False):
        break
    page += 1
    time.sleep(0.3)

print(f"Found {len(events)} current/future events.\n")

new_count = 0
for e in events:
    eid = e["id"]
    name = e.get("name", {}).get("text", "Unknown")
    start = e.get("start", {}).get("local", "?")
    marker = "    " if eid in known_ids else "NEW "
    if eid not in known_ids:
        new_count += 1
    print(f"{marker} {name}")
    print(f"      ID: {eid}  Start: {start}\n")

print(f"---")
print(f"{len(events)} total, {len(events) - new_count} in state file, {new_count} new")
