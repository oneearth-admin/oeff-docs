#!/usr/bin/env python3
"""
Batch-update OEFF 2026 Eventbrite events to match Josh's templates.

Updates:
  1. Structured content (full event page description)
  2. Ticket classes (free GA + suggested donation + additional donation)
  3. Event metadata (category, subcategory, format_id, capacity)

Two templates:
  - Launch Party (flagship/paid): rows 2, 6
  - Community (free): all others

Usage:
    EVENTBRITE_TOKEN=xxx python3 oeff_eventbrite_update_templates.py
"""

import json
import os
import sys
import urllib.request
import urllib.error
import time

TOKEN = os.environ.get("EVENTBRITE_TOKEN", "")
API = "https://www.eventbriteapi.com/v3"
STATE_FILE = os.path.join(os.path.dirname(__file__), "eventbrite-state.json")

# ── Event classification ─────────────────────────────────────────────

# Flagship paid events (Launch Party template)
FLAGSHIP_PAID_ROWS = {"row_2", "row_6"}

# Film titles by row (cleaned, no "(pending)")
FILM_TITLES = {
    "row_2": "Reasons for Hope: Dr. Jane Goodall",
    "row_3": "Beyond Zero",
    "row_4": "Plastic People",
    "row_5": "TBD",
    "row_6": "Drowned Land",
    "row_8": "How to Power a City",
    "row_9": "Rooted",
    "row_10": "How to Power a City",
    "row_11": "Young Filmmakers Winner Short Films",
    "row_12": "40 Acres",
    "row_13": "40 Acres",
    "row_14": "Rails to Trails",
    "row_17": "Young Filmmakers Contest Winner Short Films",
    "row_18": "Rails to Trails",
}

# Venue names by row (for description text)
VENUE_NAMES = {
    "row_2": "Columbia College - Film Row Cinema",
    "row_3": "Trinity Lutheran Church",
    "row_4": "Climate Action Evanston",
    "row_5": "Uncommon Ground",
    "row_6": "Columbia College - Film Row Cinema",
    "row_8": "Institute of Cultural Affairs in the USA",
    "row_9": "Bethel New Life",
    "row_10": "Triton College",
    "row_11": "Cultivate Collective / AGC",
    "row_12": "Kehrein Center / Spill the Beans Coffee House",
    "row_13": "Black Girl Environmentalists / UIC or Patagonia Fulton Market",
    "row_14": "Broadway United Methodist",
    "row_17": "BUILD Chicago",
    "row_18": "Calumet College of St. Joseph",
}


# ── API helpers ──────────────────────────────────────────────────────

def api(method, path, data=None):
    """Make an Eventbrite API call."""
    url = f"{API}{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    if body:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"  API ERROR {e.code}: {err_body[:300]}")
        return None


# ── Structured content templates ─────────────────────────────────────

def community_description_html(film_title, age_advisory):
    """Build the community event structured content HTML, matching Josh's template."""
    # Age advisory line
    age_html = ""
    if age_advisory and age_advisory.upper() != "TBD":
        if "18+" in age_advisory or "ONLY" in age_advisory.upper():
            age_html = f'<p><strong>Content Advisory: {age_advisory}</strong></p>'
        else:
            age_html = f'<p><em>Suggested audience: {age_advisory}</em></p>'

    return (
        '<p><em><strong>Doors open at 5:30.</strong></em></p>'
        '<p><em><strong>Film starts at 6:30.</strong></em></p>'
        '<p><em>Arrive early to talk with action partners, avoid lines,</em> and<em> get the best seats.</em></p>'
        '<p><strong>OEFF commits to an ongoing effort to make our events as open and as accessible as possible. '
        'Please click here for accessibility information related to our venue hosts and programs.</strong></p>'
        f'<p>Join One Earth Film Festival for a free movie and panel discussion from the film '
        f"<em>'{film_title}'</em>.</p>"
        f'{age_html}'
        '<p>You will be able to connect with local organizations and discover how you can get involved '
        'in this powerful movement.</p>'
        '<p><strong>Accessibility Note: A live captioner will be present during this event.</strong></p>'
        '<p><strong>FILM DESCRIPTION: </strong></p>'
        '<p></p>'
        '<p>We will additionally be screening one of the One Earth Young Filmmakers Runner-Up films '
        '<em><strong>TBD.</strong></em></p>'
        '<p>Stay after the film for an enlightening facilitated dialogue with relevant experts and advocates.</p>'
        '<p>Our Facilitator for the evening will be TBD</p>'
        '<p></p>'
        '<p><strong>Panelists:</strong></p>'
        '<p><strong>TBD</strong></p>'
        '<p><em><strong>ADA-compliant accessible venue.</strong></em></p>'
        '<p><strong>If you are having trouble registering in Eventbrite, then try a different browser, '
        '<a href="https://docs.google.com/forms/d/e/1FAIpQLSdisjfTMEEGtuthMoyObU6vXWOmgPfnGdVm0RAGFMU5BDl5tA/viewform?usp=header">'
        'register here</a>, or contact joshua@oneearthfilmfest.org. Or are you having trouble making '
        'your donation through Eventbrite? Then after you make your free reservation, please '
        '<a href="https://forms.donorsnap.com/form?id=98ffaec9-7fd0-4703-a2e0-8798e1169a68">'
        'use this link to make your donation</a> through our website.</strong></p>'
        '<p><em>Please note: When booking tickets, your information will never be shared with any '
        '3rd party outside of One Earth Film Festival and its co-hosting partners bringing you this event.</em></p>'
    )


def launch_party_description_html(film_title, age_advisory, venue_name):
    """Build the flagship/paid event structured content HTML, matching Josh's Launch Party template."""
    age_html = ""
    if age_advisory and age_advisory.upper() != "TBD":
        if "18+" in age_advisory or "ONLY" in age_advisory.upper():
            age_html = f'<p><strong>Content Advisory: {age_advisory}</strong></p>'
        else:
            age_html = f'<p><em>Suggested audience: {age_advisory}</em></p>'

    return (
        '<p><strong>OEFF commits to an ongoing effort to make our events as open and as accessible as possible. '
        'Please click here for accessibility information related to our venue hosts and programs.</strong></p>'
        f'{age_html}'
        f'<p><strong>Unite, celebrate, and help build resilient communities and a healthier planet!</strong> '
        f'Join One Earth Film Festival for a screening of <em>\'{film_title}\'</em> at {venue_name}.</p>'
        '<p><strong>Accessibility Note: A live captioner will be present during this event.</strong></p>'
        '<p><strong>Expect to Enjoy:</strong></p>'
        '<ul>'
        '<li>A chance to escape, recharge, and connect with like-minded filmmakers and advocates</li>'
        f'<li>A screening of the film <em>\'{film_title}\'</em></li>'
        '<li>Post-screening discussion with relevant experts and advocates</li>'
        '</ul>'
        '<p><strong>FILM DESCRIPTION:</strong></p>'
        '<p></p>'
        '<p><strong>Transportation Info: TBD</strong></p>'
        '<p>We may have a limited number of scholarship tickets for those experiencing hardship. '
        'Please reach out to michael@oneearthcollective.org for more info, with the subject line: '
        '<em>Scholarship Ticket Inquiry</em>.</p>'
        '<p>Thank you!</p>'
        '<p><em>Please note: When booking tickets, your information will never be shared with any '
        '3rd party outside of One Earth Film Festival and its co-hosting partners bringing you this event.</em></p>'
    )


# ── Update functions ─────────────────────────────────────────────────

def update_structured_content(event_id, html_body):
    """Set the structured content (full page description) for an event."""
    # Get current version
    sc = api("GET", f"/events/{event_id}/structured_content/")
    if not sc:
        return False
    version = sc["page_version_number"]

    # POST modules array to the version endpoint — this replaces all modules
    payload = {
        "modules": [{
            "type": "text",
            "data": {
                "body": {
                    "text": html_body,
                    "alignment": "left"
                }
            }
        }]
    }
    result = api("POST", f"/events/{event_id}/structured_content/{version}/", payload)
    if not result:
        return False

    # New version was created — publish it
    new_version = result.get("page_version_number", version)
    api("POST", f"/events/{event_id}/structured_content/{new_version}/publish/")
    return True


def delete_ticket_class(event_id, ticket_id):
    """Delete a ticket class."""
    return api("DELETE", f"/events/{event_id}/ticket_classes/{ticket_id}/")


def create_community_tickets(event_id, event_end_utc):
    """Create the 3-tier community ticket structure matching Josh's template."""
    tickets = []

    # 1. General Admission (free)
    ga = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "General Admission",
            "free": True,
            "quantity_total": 250,
            "minimum_quantity": 1,
            "maximum_quantity": 30,

            "sales_channels": ["online", "atd"],
            "delivery_methods": ["electronic"],
        }
    })
    if ga:
        tickets.append(ga.get("id", "?"))

    # 2. Suggested Donation $8
    don8 = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "Suggested Donation to One Earth $8 Ticket",
            "donation": True,
            "free": False,
            "quantity_total": 250,
            "minimum_quantity": 1,
            "maximum_quantity": 1,

            "sales_channels": ["online"],
            "delivery_methods": ["electronic"],
        }
    })
    if don8:
        tickets.append(don8.get("id", "?"))

    # 3. Additional Donation
    don_extra = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "Additional Donation to One Earth (not a ticket)",
            "donation": True,
            "free": False,
            "quantity_total": 0,
            "minimum_quantity": 1,
            "maximum_quantity": 1,

            "sales_channels": ["online"],
            "delivery_methods": ["electronic"],
        }
    })
    if don_extra:
        tickets.append(don_extra.get("id", "?"))

    return tickets


def create_flagship_tickets(event_id, event_end_utc):
    """Create the 3-tier flagship ticket structure matching Josh's Launch Party template."""
    tickets = []

    # 1. Launch Party Ticket ($80)
    t1 = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "Launch Party Ticket",
            "free": False,
            "cost": "USD,8000",
            "quantity_total": 150,
            "minimum_quantity": 1,
            "maximum_quantity": 10,
            "sales_channels": ["online", "atd"],
            "delivery_methods": ["electronic"],
        }
    })
    if t1:
        tickets.append(t1.get("id", "?"))

    # 2. Order 2 or More ($75)
    t2 = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "Order 2 or More Tickets",
            "free": False,
            "cost": "USD,7500",
            "quantity_total": 100,
            "minimum_quantity": 1,
            "maximum_quantity": 10,
            "sales_channels": ["online", "atd"],
            "delivery_methods": ["electronic"],
        }
    })
    if t2:
        tickets.append(t2.get("id", "?"))

    # 3. Additional Donation
    don = api("POST", f"/events/{event_id}/ticket_classes/", {
        "ticket_class": {
            "name": "Additional Donation to One Earth",
            "donation": True,
            "free": False,
            "quantity_total": 0,
            "minimum_quantity": 1,
            "maximum_quantity": 1,

            "sales_channels": ["online"],
            "delivery_methods": ["electronic"],
        }
    })
    if don:
        tickets.append(don.get("id", "?"))

    return tickets


def update_event_metadata(event_id, is_flagship_paid):
    """Update category, subcategory, format_id, and capacity."""
    data = {
        "event": {
            "category_id": "111",        # Charity & Causes
            "subcategory_id": "11002",   # Environment
            "capacity": 250,
        }
    }
    if is_flagship_paid:
        data["event"]["format_id"] = "11"   # Festival/Fair
    else:
        data["event"]["format_id"] = "7"    # Party/Social Gathering

    return api("POST", f"/events/{event_id}/", data)


# ── Main ─────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        print("Set EVENTBRITE_TOKEN env var.")
        sys.exit(1)

    with open(STATE_FILE) as f:
        state = json.load(f)

    events = state.get("events", {})
    success = 0
    fail = 0

    for row_key, ev in sorted(events.items()):
        event_id = ev["event_id"]
        event_name = ev["event_name"]
        age_advisory = ev.get("age_advisory", "")
        is_flagship_paid = row_key in FLAGSHIP_PAID_ROWS
        film_title = FILM_TITLES.get(row_key, "TBD")
        venue_name = VENUE_NAMES.get(row_key, "TBD")

        template_type = "FLAGSHIP" if is_flagship_paid else "COMMUNITY"
        print(f"\n{'='*60}")
        print(f"[{row_key}] {event_name}")
        print(f"  Template: {template_type} | Film: {film_title}")
        print(f"  Event ID: {event_id}")

        # 1. Update structured content
        print("  1. Updating structured content...")
        if is_flagship_paid:
            html = launch_party_description_html(film_title, age_advisory, venue_name)
        else:
            html = community_description_html(film_title, age_advisory)

        if update_structured_content(event_id, html):
            print("     OK — structured content set")
        else:
            print("     FAILED — structured content")
            fail += 1
            continue

        # 2. Update ticket classes
        print("  2. Updating ticket classes...")
        # Delete existing tickets
        existing = ev.get("ticket_ids", [])
        for tid in existing:
            print(f"     Deleting old ticket {tid}...")
            delete_ticket_class(event_id, tid)

        # Get event end time for sales_end
        ev_data = api("GET", f"/events/{event_id}/")
        end_utc = ev_data["end"]["utc"] if ev_data else None

        # Create new tickets
        if is_flagship_paid:
            new_tickets = create_flagship_tickets(event_id, end_utc)
        else:
            new_tickets = create_community_tickets(event_id, end_utc)

        if new_tickets:
            print(f"     OK — {len(new_tickets)} ticket classes created: {new_tickets}")
            ev["ticket_ids"] = new_tickets
        else:
            print("     FAILED — ticket classes")
            fail += 1
            continue

        # 3. Update event metadata
        print("  3. Updating event metadata...")
        if update_event_metadata(event_id, is_flagship_paid):
            print(f"     OK — category=111, subcategory=11002, format={'11' if is_flagship_paid else '7'}")
        else:
            print("     FAILED — metadata")
            fail += 1
            continue

        success += 1
        # Throttle slightly to be nice to the API
        time.sleep(0.3)

    # Save updated state
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)
    print(f"\n{'='*60}")
    print(f"Done: {success} updated, {fail} failed")
    print(f"State saved to {STATE_FILE}")


if __name__ == "__main__":
    main()
