#!/usr/bin/env python3
"""
match-contacts-to-venues.py — Match host contacts to venues

Cross-references hosts-mail-merge-contacts.csv with token-map.json
using email domain matching and Airtable Events data.

Produces a merged Mailmeteor-ready CSV with venue, contact, and security columns.

Usage:
    python3 match-contacts-to-venues.py
    AIRTABLE_TOKEN=pat... python3 match-contacts-to-venues.py  # also checks Airtable
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).parent
TOKEN_MAP_PATH = BASE_DIR / "token-map.json"
CONTACTS_PATH = BASE_DIR / "hosts-mail-merge-contacts.csv"
OUTPUT_PATH = BASE_DIR / "merge-sheet-matched.csv"
HELPER_BASE_URL = "https://hosts.oneearthfilmfest.org/"

# Manual domain → venue mapping (from email domain inspection)
DOMAIN_TO_VENUE = {
    "bethelnewlife.org": "Bethel New Life",
    "triton.edu": "Triton College",
    "ilclimateandhealth.org": "Illinois Clinicians for Climate Action",
    "kcachicago.org": "Kehrein Center for the Arts at BlkRoom",
    "buildchicago.org": "BUILD, Inc.",
    "dom.edu": "Dominican University",
    "cultivate-collective.org": "Cultivate Collective (at Academy for Global Citizenship)",
    "oak-park.us": "Village of Oak Park at Oak Park Village Hall (with Sustainability Department, Chief Sustainability Officer)",
    "chipublib.org": "Chicago Cultural Center",
    "colum.edu": "Columbia College - Film Row Cinema",
    "ica-usa.org": "Institute of Cultural Affairs in the USA",
    "luc.edu": "Loyola University Law School",
    "ccsj.edu": "Calumet College of St. Joseph",  # from Roadmap — NOT in our 27 venue list
}

# Exact email → venue mapping (from Roadmap column M + Hosts_Mail-Merge cross-ref)
EMAIL_TO_VENUE = {
    "uncommonmichaelcameron@gmail.com": "Uncommon Ground",
    "ohhelencameron@gmail.com": "Uncommon Ground",
    "jstoff304@gmail.com": "Trinity Lutheran, Des Plaines (Prospect)",
    "markkleiny@gmail.com": "Go Green Park Ridge",
    "eacarlstrom1@comcast.net": "Climate Action Evanston",
    "bge.chicago773@gmail.com": "Black Girl Environmentalists at UIC or Patagonia Fulton Market",
    "lgunn3@gmail.com": "Seven Generations Ahead",
    "meg.hagenah@gmail.com": "Seven Generations Ahead",
    "lmdini@sbcglobal.net": "Northbrook Public Library",
    "natalielynn.lichtenbert@gmail.com": "Lizadro Museum (gem museum), Northbrook",
    "magicfox8@gmail.com": "Epiphany Center for the Arts (said they are interested in 2026)",
    "jpatney@hotmail.com": "Euclid AVE UMC",
    "richard.alton@gmail.com": "Broadway United Methodist Church",
    "vs.ashvin@gmail.com": "Discover Card/Capital One",
    "whitey1600@gmail.com": "Uncommon Ground",
}

# Airtable config
BASE_ID = "app9DymWrbAQaHH0K"
API = "https://api.airtable.com/v0"


def api_call(method, endpoint, token, body=None):
    url = f"{API}{endpoint}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode("utf-8") if body else None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers, method=method, data=data)
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            time.sleep(0.22)
            return result
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(30)
                continue
            if attempt == 2:
                raise
            time.sleep(2)
    return {}


def fetch_event_contacts(token):
    """Fetch 2026 Events with venue names and contact info."""
    contacts = {}  # venue_name → [emails]
    offset = None

    while True:
        formula = urllib.request.quote("Year=2026")
        endpoint = (
            f"/{BASE_ID}/{urllib.request.quote('Events')}"
            f"?filterByFormula={formula}"
        )
        if offset:
            endpoint += f"&offset={offset}"

        result = api_call("GET", endpoint, token)
        for rec in result.get("records", []):
            fields = rec.get("fields", {})
            # Venue Name is a lookup field (returns array)
            venue_names = fields.get("Venue Name", [])
            if isinstance(venue_names, list) and venue_names:
                venue_name = venue_names[0]
            elif isinstance(venue_names, str):
                venue_name = venue_names
            else:
                continue

            # Look for contact fields
            for field_name in ["Host Contact", "Contact Email", "Contact Info",
                               "Host Email", "Primary Contact"]:
                val = fields.get(field_name, "")
                if val and "@" in str(val):
                    contacts.setdefault(venue_name, set()).add(str(val).strip().lower())

        offset = result.get("offset")
        if not offset:
            break

    return contacts


def match_email_to_venue(email, token_map, airtable_contacts=None):
    """Try to match an email address to a venue name."""
    email_lower = email.lower().strip()
    domain = email_lower.split("@")[-1] if "@" in email_lower else ""

    # 1. Check exact email mapping (known from Roadmap + cross-referencing)
    if email_lower in EMAIL_TO_VENUE:
        venue = EMAIL_TO_VENUE[email_lower]
        if venue in token_map:
            return venue

    # 2. Check domain mapping
    if domain in DOMAIN_TO_VENUE:
        venue = DOMAIN_TO_VENUE[domain]
        if venue in token_map:
            return venue

    # 3. Check Airtable event contacts (if available)
    if airtable_contacts:
        for venue_name, venue_emails in airtable_contacts.items():
            if email_lower in venue_emails:
                # Find matching venue in token map (fuzzy)
                for tm_name in token_map:
                    if venue_name.lower() in tm_name.lower() or tm_name.lower() in venue_name.lower():
                        return tm_name
                return venue_name  # Return even if not in token map

    # 4. Partial domain match against venue names
    if domain and not domain.endswith(("gmail.com", "hotmail.com", "yahoo.com",
                                        "comcast.net", "sbcglobal.net", "aol.com")):
        org_part = domain.split(".")[0].lower()
        for venue_name in token_map:
            if org_part in venue_name.lower().replace(" ", ""):
                return venue_name

    return ""  # Unmatched


def main():
    # Load token map
    if not TOKEN_MAP_PATH.exists():
        print(f"Error: {TOKEN_MAP_PATH} not found.", file=sys.stderr)
        return 1

    with open(TOKEN_MAP_PATH, encoding="utf-8") as f:
        token_map = json.load(f)

    # Load contacts
    if not CONTACTS_PATH.exists():
        print(f"Error: {CONTACTS_PATH} not found.", file=sys.stderr)
        return 1

    contacts = []
    with open(CONTACTS_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("Email", "").strip():
                contacts.append(row)

    print(f"Loaded {len(contacts)} contacts, {len(token_map)} venues", file=sys.stderr)

    # Try Airtable for additional matching
    airtable_contacts = None
    airtable_token = os.environ.get("AIRTABLE_TOKEN", "")
    if airtable_token:
        print("Fetching event contacts from Airtable...", file=sys.stderr)
        try:
            airtable_contacts = fetch_event_contacts(airtable_token)
            print(f"  Found contact info for {len(airtable_contacts)} events", file=sys.stderr)
        except Exception as e:
            print(f"  Airtable fetch failed: {e}", file=sys.stderr)

    # Match contacts to venues
    matched = []
    unmatched = []

    for contact in contacts:
        email = contact["Email"].strip()
        venue = match_email_to_venue(email, token_map, airtable_contacts)

        if venue and venue in token_map:
            entry = token_map[venue]
            matched.append({
                "Email": email,
                "First Name": contact.get("First Name", ""),
                "Last Name": contact.get("Last Name", ""),
                "Venue Name": venue,
                "Host Helper URL": f"{HELPER_BASE_URL}{entry['token']}/",
                "Financial Password": entry.get("financial_password_plaintext", ""),
                "Packet Password": entry.get("packet_password", ""),
            })
        else:
            unmatched.append({
                "email": email,
                "name": f"{contact.get('First Name', '')} {contact.get('Last Name', '')}".strip(),
                "guessed_venue": venue,
            })

    # Check for venues with no matched contact
    matched_venues = {m["Venue Name"] for m in matched}
    unmatched_venues = [v for v in token_map if v not in matched_venues]

    # Write output
    fieldnames = ["Email", "First Name", "Last Name", "Venue Name",
                  "Host Helper URL", "Financial Password", "Packet Password"]

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(matched, key=lambda r: r["Venue Name"]))

        # Add unmatched venues as empty-email rows
        for venue_name in sorted(unmatched_venues):
            entry = token_map[venue_name]
            writer.writerow({
                "Email": "",
                "First Name": "",
                "Last Name": "",
                "Venue Name": venue_name,
                "Host Helper URL": f"{HELPER_BASE_URL}{entry['token']}/",
                "Financial Password": entry.get("financial_password_plaintext", ""),
                "Packet Password": entry.get("packet_password", ""),
            })

    print(f"\nResults:", file=sys.stderr)
    print(f"  Matched: {len(matched)} contacts → venues", file=sys.stderr)
    print(f"  Unmatched contacts: {len(unmatched)}", file=sys.stderr)
    print(f"  Venues without contacts: {len(unmatched_venues)}", file=sys.stderr)

    if unmatched:
        print(f"\nUnmatched contacts (need manual venue assignment):", file=sys.stderr)
        for u in unmatched:
            guess = f" (maybe: {u['guessed_venue']})" if u["guessed_venue"] else ""
            print(f"  - {u['name']}: {u['email']}{guess}", file=sys.stderr)

    if unmatched_venues:
        print(f"\nVenues without contacts (need email from Ana/Erin):", file=sys.stderr)
        for v in sorted(unmatched_venues):
            print(f"  - {v}", file=sys.stderr)

    print(f"\nWrote {OUTPUT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
