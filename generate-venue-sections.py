#!/usr/bin/env python3
"""
generate-venue-sections.py — OEFF host guide venue section generator

Reads the 2026_Venue_Sections view from Airtable, renders per-venue HTML
sections with temporal state logic (feb/mar/apr), validates SARC ordering
and privacy constraints, then injects into hosts/index.html between sentinels.

Stdlib Python 3 only — no pip dependencies.

Usage:
    # Dry run (fetch + generate + validate, no file writes)
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py --dry-run

    # Generate and inject into hosts/index.html
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py

    # Override date for testing state logic
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py --today 2026-03-15

    # Output standalone HTML fragment (no injection)
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py --output venue-sections.html

    # Generate per-venue host helper pages (requires token-map.json)
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py --helpers

    # Helpers dry run with date override
    AIRTABLE_TOKEN=pat... python3 generate-venue-sections.py --helpers --dry-run --today 2026-04-10
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

BASE_ID = "app9DymWrbAQaHH0K"
API = "https://api.airtable.com/v0"
VIEW_NAME = "2026_Venue_Sections"
TABLE_NAME = "Events"

# ---------------------------------------------------------------------------
# Field name mapping — Airtable actual names → script canonical names
#
# The 2026_Venue_Sections view was designed with normalized field names.
# Until that view exists, we fetch with filterByFormula and normalize here.
# If the view IS created with the correct field names, normalize_record()
# becomes a no-op for fields that already match.
# ---------------------------------------------------------------------------
EVENTS_FIELD_MAP = {
    # Airtable actual name  →  script canonical name
    "Date": "Event_Date",
    "Time": "Event_Time",
    "Ticket URL": "RSVP_URL",
    "Pipeline Select": "Pipeline_Status",
    "Pipeline Status": "Pipeline_Status",  # fallback if text field exists
    "Volunteer Needs": "Volunteer_Needs",
    # Fields below are direct matches — included for documentation
    # "Venue": "Venue",  (link field — already correct)
    # "Film": "Film",    (link field — already correct)
}

# Venue linked-record field mapping (Venues table)
VENUE_FIELD_MAP = {
    "Venue Name": "Name",       # If Venues table uses "Venue Name" as primary
    "Contact Info": "_contact_info_raw",  # multiline → parsed for email
    "Notes": "Equipment_Notes",
    # "Region": "Region",       # already matches
    # "Capacity": "Capacity",   # already matches
}


def normalize_record(rec: Dict[str, Any], field_map: Dict[str, str]) -> Dict[str, Any]:
    """Return a copy of rec with fields renamed per field_map.

    Fields not in field_map are passed through unchanged. If both an
    old name and a new name exist, the mapped (new) name wins.
    """
    original = rec.get("fields", {})
    normalized: Dict[str, Any] = {}

    for k, v in original.items():
        canonical = field_map.get(k, k)
        normalized[canonical] = v

    return {**rec, "fields": normalized}


def normalize_venue_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a Venues linked record, including email extraction from Contact Info."""
    rec = normalize_record(rec, VENUE_FIELD_MAP)
    f = rec.get("fields", {})

    # Extract email from Contact Info multiline text if Contact_Email not present
    if not f.get("Contact_Email") and f.get("_contact_info_raw"):
        import re as _re
        m = _re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', f["_contact_info_raw"])
        if m:
            f["Contact_Email"] = m.group(0)

    return rec


SENTINEL_BEGIN = "<!-- BEGIN:VENUE_SECTIONS -->"
SENTINEL_END = "<!-- END:VENUE_SECTIONS -->"
HOSTS_HTML = Path(__file__).parent / "hosts" / "index.html"
TOKEN_MAP_PATH = Path(__file__).parent / "token-map.json"
HELPERS_DIR = Path(__file__).parent / "hosts"

# State transition dates (2026 season)
STATE_MAR_DATE = date(2026, 3, 10)
STATE_APR_DATE = date(2026, 4, 5)

# SARC ordering labels — every venue state div must have these in order
SARC_LABELS = ["Status", "What We Need From You", "Resources", "Contacts"]

# Privacy patterns — if any match the output, the build fails
PHONE_RE = re.compile(r"\b\d{3}[-.)\s]?\d{3}[-.\s]?\d{4}\b")
PRIVATE_WORD_RE = re.compile(
    r"\b(password|passcode|pin|dropbox)\b", re.IGNORECASE
)
PRIVATE_URL_RE = re.compile(r"https?://[^\s]*dropbox[^\s]*", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Airtable API layer (pattern from push-timeline-to-airtable.py)
# ---------------------------------------------------------------------------

def get_token() -> str:
    """Read Airtable PAT from environment."""
    token = os.environ.get("AIRTABLE_TOKEN", "")
    if not token:
        print("Error: AIRTABLE_TOKEN environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return token


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


def fetch_all_records(table: str, view: str, token: str) -> List[Dict[str, Any]]:
    """Paginated fetch of all records from an Airtable view."""
    records: List[Dict[str, Any]] = []
    offset: Optional[str] = None
    page = 0

    while True:
        page += 1
        endpoint = f"/{BASE_ID}/{urllib.request.quote(table)}?view={urllib.request.quote(view)}"
        if offset:
            endpoint += f"&offset={offset}"
        print(f"  Fetching page {page}...", file=sys.stderr)
        result = api_call("GET", endpoint, token)
        records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break

    print(f"  Fetched {len(records)} records from {table}/{view}", file=sys.stderr)
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
        endpoint = f"/{BASE_ID}/{urllib.request.quote(table)}?filterByFormula={encoded}"
        if offset:
            endpoint += f"&offset={offset}"
        print(f"  Fetching page {page}...", file=sys.stderr)
        result = api_call("GET", endpoint, token)
        records.extend(result.get("records", []))
        offset = result.get("offset")
        if not offset:
            break

    print(f"  Fetched {len(records)} records from {table} (filtered)", file=sys.stderr)
    return records


def resolve_linked_records(
    records: List[Dict[str, Any]], token: str
) -> Tuple[Dict[str, Dict], Dict[str, Dict], Dict[str, Dict]]:
    """Fetch linked Venue, Film, and Film_Contact records. Cache by ID."""
    venue_ids: set = set()
    film_ids: set = set()

    for rec in records:
        fields = rec.get("fields", {})
        for vid in fields.get("Venue", []):
            venue_ids.add(vid)
        for fid in fields.get("Film", []):
            film_ids.add(fid)

    venues = _fetch_by_ids("Venues", venue_ids, token)
    films = _fetch_by_ids("Films", film_ids, token)

    # Film contacts are linked from films
    contact_ids: set = set()
    for film in films.values():
        for cid in film.get("fields", {}).get("Film_Contact", []):
            contact_ids.add(cid)
    contacts = _fetch_by_ids("Film Contacts", contact_ids, token)

    return venues, films, contacts


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
        endpoint = f"/{BASE_ID}/{urllib.request.quote(table)}?filterByFormula={encoded}"
        result = api_call("GET", endpoint, token)
        for rec in result.get("records", []):
            cache[rec["id"]] = rec

    print(f"  Resolved {len(cache)} linked {table} records", file=sys.stderr)
    return cache


# ---------------------------------------------------------------------------
# State logic
# ---------------------------------------------------------------------------

def infer_state(today: date) -> str:
    """Determine content state based on date."""
    if today < STATE_MAR_DATE:
        return "feb"
    if today < STATE_APR_DATE:
        return "mar"
    return "apr"


def venue_slug(name: str) -> str:
    """Generate a short hash slug for venue section IDs."""
    return hashlib.sha256(f"{name}-oeff2026".encode()).hexdigest()[:8]


# ---------------------------------------------------------------------------
# Data assembly — flatten Airtable records into venue dicts
# ---------------------------------------------------------------------------

def assemble_venues(
    records: List[Dict[str, Any]],
    venues_cache: Dict[str, Dict],
    films_cache: Dict[str, Dict],
    contacts_cache: Dict[str, Dict],
) -> List[Dict[str, Any]]:
    """Flatten linked records into per-venue dicts for rendering."""
    assembled: List[Dict[str, Any]] = []

    for rec in records:
        f = rec.get("fields", {})

        # Resolve linked venue
        venue_ids = f.get("Venue", [])
        venue_rec = venues_cache.get(venue_ids[0], {}) if venue_ids else {}
        vf = venue_rec.get("fields", {})

        # Resolve linked film
        film_ids = f.get("Film", [])
        film_rec = films_cache.get(film_ids[0], {}) if film_ids else {}
        ff = film_rec.get("fields", {})

        # Resolve film contact
        contact_ids = ff.get("Film_Contact", [])
        contact_rec = contacts_cache.get(contact_ids[0], {}) if contact_ids else {}
        cf = contact_rec.get("fields", {})

        venue = {
            # Event fields
            "event_id": rec.get("id", ""),
            "event_date": f.get("Event_Date", ""),
            "event_time": f.get("Event_Time", ""),
            "doors_time": f.get("Doors_Time", ""),
            "rsvp_url": f.get("RSVP_URL", ""),
            "rsvp_count": f.get("RSVP_Count", 0),
            "pipeline_status": f.get("Pipeline_Status", ""),
            "volunteer_needs": f.get("Volunteer_Needs", ""),
            "screening_packet_url": f.get("Screening_Packet_URL", ""),
            # Venue fields
            "venue_name": vf.get("Name", "Unknown Venue"),
            "venue_city": vf.get("City", ""),
            "venue_region": vf.get("Region", ""),
            "venue_capacity": vf.get("Capacity", ""),
            "venue_contact_name": vf.get("Contact_Name", ""),
            "venue_contact_email": vf.get("Contact_Email", ""),
            "venue_facility_contact": vf.get("Facility_Contact", ""),
            "venue_av_contact": vf.get("AV_Contact", ""),
            "venue_equipment_notes": vf.get("Equipment_Notes", ""),
            # Film fields
            "film_title": ff.get("Title", "TBD"),
            "film_runtime": ff.get("Runtime_Min", 0),
            # Film contact
            "film_contact_name": cf.get("Name", ""),
            "film_contact_email": cf.get("Email", ""),
        }
        assembled.append(venue)

    # Sort by venue name for consistent output
    assembled.sort(key=lambda v: v["venue_name"])
    return assembled


def _load_host_intake_by_venue(token: str) -> Dict[str, Dict[str, Any]]:
    """Fetch Host Intake records and index by linked Venue ID.

    Returns dict mapping venue record ID → intake fields for venue
    details enrichment (capacity, ADA, parking, transit, WiFi, AV, etc.).
    """
    print("  Fetching Host Intake records...", file=sys.stderr)
    intake_records = fetch_by_filter("Host Intake", "NOT({Venue Id}='')", token)
    by_venue: Dict[str, Dict[str, Any]] = {}

    for rec in intake_records:
        f = rec.get("fields", {})
        # Host Intake links to Venues via a linked record field or text ID
        venue_links = f.get("Venue", [])
        if venue_links:
            vid = venue_links[0] if isinstance(venue_links, list) else venue_links
            by_venue[vid] = f
        # Fallback: match by Venue Id text field
        venue_id_text = f.get("Venue Id", "")
        if venue_id_text:
            by_venue[venue_id_text] = f

    print(f"  Indexed {len(by_venue)} Host Intake record(s)", file=sys.stderr)
    return by_venue


def assemble_venues_for_helpers(
    records: List[Dict[str, Any]],
    token: str,
) -> List[Dict[str, Any]]:
    """Assembly for helper pages: Events + Venues + Host Intake data.

    Pulls denormalized Event fields, linked Venue records for contacts,
    and Host Intake records for venue details (capacity, ADA, parking,
    transit, WiFi, AV equipment, wayfinding).
    """
    # Collect linked venue IDs to fetch contact info
    venue_ids: set = set()
    for rec in records:
        for vid in rec.get("fields", {}).get("Venue", []):
            venue_ids.add(vid)

    # Fetch venue records for contact info
    venues_cache = _fetch_by_ids("Venues", venue_ids, token)

    # Fetch Host Intake for venue details enrichment
    intake_by_venue = _load_host_intake_by_venue(token)

    # Deduplicate by venue name (some venues have multiple events)
    seen: set = set()
    assembled: List[Dict[str, Any]] = []

    for rec in records:
        f = rec.get("fields", {})
        name = f.get("Venue Name", "").strip()
        if not name or name in seen:
            continue
        seen.add(name)

        # Resolve linked venue for contact info
        venue_ids_list = f.get("Venue", [])
        venue_rec = venues_cache.get(venue_ids_list[0], {}) if venue_ids_list else {}
        vf = venue_rec.get("fields", {})
        venue_record_id = venue_ids_list[0] if venue_ids_list else ""

        # Extract email from Contact Info multiline text
        contact_info = vf.get("Contact Info", "")
        import re as _re
        email_match = _re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', contact_info)
        contact_email = email_match.group(0) if email_match else ""

        # Extract contact name from Contact Info (first line often "Name")
        contact_name = ""
        if contact_info:
            lines = [l.strip() for l in contact_info.strip().splitlines() if l.strip()]
            if lines and not _re.match(r'[\w.+-]+@', lines[0]):
                contact_name = lines[0]

        # Enrich from Host Intake (match by record ID or text Venue Id)
        intake = intake_by_venue.get(venue_record_id, {})
        if not intake:
            # Try matching by text Venue Id field (e.g. "V-008")
            venue_text_id = vf.get("Venue ID", "")
            intake = intake_by_venue.get(venue_text_id, {})

        # Parse intake fields — checkmarks are "✓" strings
        def _check(val: Any) -> bool:
            return str(val).strip() in ("✓", "Yes", "yes", "true", "True", "1")

        venue = {
            "event_id": rec.get("id", ""),
            "event_date": f.get("Date", ""),
            "event_time": f.get("Time", ""),
            "ticket_price": f.get("Ticket Price", ""),
            "doors_time": "",
            "rsvp_url": f.get("Ticket URL", ""),
            "rsvp_count": f.get("RSVP Count", 0),
            "pipeline_status": f.get("Pipeline Status", ""),
            "volunteer_needs": f.get("Volunteer Needs", ""),
            "screening_packet_url": f.get("Screening Packet URL", ""),
            "oeff_rep": f.get("OEFF Rep", ""),
            # Venue fields
            "venue_name": name,
            "venue_address": intake.get("Venue Address", ""),
            "venue_city": "",
            "venue_region": vf.get("Region", ""),
            "venue_capacity": vf.get("Capacity", ""),
            "venue_contact_name": intake.get("Contact Name", "") or contact_name,
            "venue_contact_email": intake.get("Contact Email", "") or contact_email,
            "venue_facility_contact": "",
            "venue_av_contact": vf.get("AV Contact", ""),
            "venue_equipment_notes": vf.get("Notes", ""),
            # Host Intake venue details
            "has_projector": _check(intake.get("Has Projector", "")),
            "has_sound": _check(intake.get("Has Sound", "")),
            "has_screen": _check(intake.get("Has Screen", "")),
            "has_computer": _check(intake.get("Has Computer", "")),
            "has_wifi": _check(intake.get("Has Wifi", "")),
            "has_av_lead": _check(intake.get("Has Av Lead", "")),
            "has_wheelchair": _check(intake.get("Has Wheelchair", "")),
            "space_notes": intake.get("Space Notes", ""),
            # Film fields (denormalized on Events)
            "film_title": f.get("Film Title", "TBD"),
            "film_runtime": 0,
            # Film contact
            "film_contact_name": "",
            "film_contact_email": "",
        }
        assembled.append(venue)

    assembled.sort(key=lambda v: v["venue_name"])
    return assembled


# ---------------------------------------------------------------------------
# Timeline computation
# ---------------------------------------------------------------------------

def compute_day_of_timeline(event_time: str, runtime: int) -> List[Dict[str, str]]:
    """Generate day-of timeline items from event time and runtime."""
    if not event_time:
        return []

    try:
        # Parse time like "7:00 PM" or "19:00"
        for fmt in ("%I:%M %p", "%H:%M"):
            try:
                t = datetime.strptime(event_time.strip(), fmt)
                break
            except ValueError:
                continue
        else:
            return []
    except Exception:
        return []

    base = datetime(2026, 4, 22, t.hour, t.minute)  # Date doesn't matter, just time math
    runtime_mins = runtime or 90  # Default if unknown

    items = [
        (-60, "Venue opens for setup"),
        (-45, "Test playback (full file, not just start)"),
        (-30, "Volunteers arrive"),
        (-15, "Doors open"),
        (0, "Pre-show content begins (~5 min)"),
        (5, "Feature film starts"),
        (5 + runtime_mins, "Film ends — Q&A or discussion"),
        (5 + runtime_mins + 15, "Wrap up, thank guests"),
        (5 + runtime_mins + 30, "Venue teardown complete"),
    ]

    timeline = []
    for offset, label in items:
        item_time = base + timedelta(minutes=offset)
        timeline.append({
            "time": item_time.strftime("%-I:%M %p"),
            "label": label,
        })

    return timeline


# ---------------------------------------------------------------------------
# HTML rendering helpers
# ---------------------------------------------------------------------------

def _esc(text: Any) -> str:
    """HTML-escape a value."""
    s = str(text) if text else ""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def render_screening_detail(label: str, value: str, confirmed: bool = True) -> str:
    """Render one screening detail row."""
    status_class = "confirmed" if confirmed else "pending"
    status_text = "" if confirmed else " (pending)"
    return (
        f'<div class="screening-detail">'
        f'<span class="screening-label">{_esc(label)}</span>'
        f'<span class="screening-value {status_class}">{_esc(value)}{status_text}</span>'
        f'</div>'
    )


def render_status_badge(state: str) -> str:
    """Render the status badge for the current state."""
    badges = {
        "feb": ("Confirmed Host", "badge-confirmed"),
        "mar": ("On Track", "badge-ontrack"),
        "apr": ("Ready", "badge-ready"),
    }
    text, css_class = badges.get(state, ("", ""))
    return f'<span class="venue-badge {css_class}">{_esc(text)}</span>'


def render_sarc_group(label: str, content: str) -> str:
    """Wrap content in a SARC group div with label."""
    return (
        f'<div class="sarc-group">'
        f'<h4 class="sarc-label">{_esc(label)}</h4>'
        f'{content}'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Per-state renderers (SARC order: Status > Asks > Resources > Contacts)
# ---------------------------------------------------------------------------

def render_feb_state(venue: Dict[str, Any]) -> str:
    """February state — confirmed but details pending."""
    # Status
    status = (
        f'{render_status_badge("feb")}'
        f'{render_screening_detail("Film", venue["film_title"], confirmed=True)}'
        f'{render_screening_detail("Date", "Week of April 22-26", confirmed=False)}'
        f'{render_screening_detail("Time", "To be confirmed", confirmed=False)}'
    )

    # Asks
    asks = (
        '<ul class="venue-asks">'
        '<li>Confirm your preferred screening date and time</li>'
        '<li>Review AV requirements in the Tech Specs section above</li>'
        '<li>Complete the host intake form if you haven\'t already</li>'
        '</ul>'
    )

    # Resources
    resources = (
        '<ul class="venue-resources">'
        '<li><a href="https://us02web.zoom.us/meeting/register/YOUR_MEETING_ID" '
        'target="_blank" rel="noopener">Upcoming host webinars</a> — '
        'live Q&amp;A with the OEFF team</li>'
        '<li><a href="https://bit.ly/oeff2026hostinterestform" '
        'target="_blank" rel="noopener">Host interest form</a></li>'
        '<li>Previous webinar recordings shared via email</li>'
        '</ul>'
    )

    # Contacts
    contacts = (
        '<div class="venue-contacts">'
        '<div class="contact-row">'
        '<strong>Your host coordinator:</strong> '
        '<a href="mailto:hosts@oneearthcollective.org">hosts@oneearthcollective.org</a>'
        '</div>'
        '<div class="contact-row">'
        '<strong>General inquiries:</strong> '
        '<a href="mailto:info@oneearthfilmfest.org">info@oneearthfilmfest.org</a>'
        '</div>'
        '</div>'
    )

    return (
        render_sarc_group(SARC_LABELS[0], status)
        + render_sarc_group(SARC_LABELS[1], asks)
        + render_sarc_group(SARC_LABELS[2], resources)
        + render_sarc_group(SARC_LABELS[3], contacts)
    )


def render_mar_state(venue: Dict[str, Any]) -> str:
    """March state — details confirmed, marketing push."""
    event_date = venue.get("event_date", "TBD")
    event_time = venue.get("event_time", "TBD")
    rsvp_url = venue.get("rsvp_url", "")

    # Status
    status = (
        f'{render_status_badge("mar")}'
        f'{render_screening_detail("Film", venue["film_title"])}'
        f'{render_screening_detail("Date", event_date)}'
        f'{render_screening_detail("Time", event_time)}'
    )

    # Asks
    volunteer_needs = _esc(venue.get("volunteer_needs", "")) or "Details coming soon"
    asks = (
        '<ul class="venue-asks">'
        '<li>Share your event page with your community</li>'
        '<li>Confirm AV setup and test equipment</li>'
        f'<li>Volunteer needs: {volunteer_needs}</li>'
        '</ul>'
    )

    # Resources
    rsvp_link = ""
    if rsvp_url:
        rsvp_link = (
            f'<li><a href="{_esc(rsvp_url)}" target="_blank" rel="noopener">'
            f'Your event page</a> — share with your audience</li>'
        )
    resources = (
        '<ul class="venue-resources">'
        f'{rsvp_link}'
        '<li>Marketing kit (logos, social templates) — shared via email</li>'
        '<li>Promotional copy and event description available on request</li>'
        '</ul>'
    )

    # Contacts
    venue_contact = venue.get("venue_contact_email", "")
    venue_contact_name = venue.get("venue_contact_name", "")
    venue_team_line = ""
    if venue_contact:
        label = _esc(venue_contact_name) if venue_contact_name else "Venue team"
        venue_team_line = (
            f'<div class="contact-row">'
            f'<strong>{label}:</strong> '
            f'<a href="mailto:{_esc(venue_contact)}">{_esc(venue_contact)}</a>'
            f'</div>'
        )

    contacts = (
        '<div class="venue-contacts">'
        '<div class="contact-row">'
        '<strong>Your host coordinator:</strong> '
        '<a href="mailto:hosts@oneearthcollective.org">hosts@oneearthcollective.org</a>'
        '</div>'
        f'{venue_team_line}'
        '</div>'
    )

    return (
        render_sarc_group(SARC_LABELS[0], status)
        + render_sarc_group(SARC_LABELS[1], asks)
        + render_sarc_group(SARC_LABELS[2], resources)
        + render_sarc_group(SARC_LABELS[3], contacts)
    )


def render_apr_state(venue: Dict[str, Any]) -> str:
    """April state — ready, day-of details, screening packet."""
    event_date = venue.get("event_date", "TBD")
    event_time = venue.get("event_time", "TBD")
    doors_time = venue.get("doors_time", "")
    capacity = venue.get("venue_capacity", "")
    rsvp_count = venue.get("rsvp_count", 0)
    runtime = venue.get("film_runtime", 0)

    # Status
    status_details = (
        f'{render_status_badge("apr")}'
        f'{render_screening_detail("Film", venue["film_title"])}'
        f'{render_screening_detail("Date", event_date)}'
        f'{render_screening_detail("Time", event_time)}'
    )
    if doors_time:
        status_details += render_screening_detail("Doors", doors_time)
    if capacity:
        status_details += render_screening_detail("Capacity", str(capacity))
    if rsvp_count:
        status_details += render_screening_detail("RSVPs", str(rsvp_count))

    # Asks
    asks = (
        '<ul class="venue-asks">'
        '<li>Test your screening packet (full playback, not just first 30 seconds)</li>'
        '<li>Confirm volunteer assignments for day-of</li>'
        '<li>Post final reminder to your community channels</li>'
        '</ul>'
    )

    # Resources — screening packet link, VLC, timeline, volunteer roster
    packet_url = venue.get("screening_packet_url", "")
    packet_line = ""
    if packet_url:
        packet_line = (
            '<li>Screening packet: download link sent via separate email '
            '(check your inbox)</li>'
        )
    else:
        packet_line = (
            '<li>Screening packet: download link coming soon via email</li>'
        )

    timeline = compute_day_of_timeline(event_time, runtime)
    timeline_html = ""
    if timeline:
        rows = "".join(
            f'<tr><td class="timeline-time">{_esc(t["time"])}</td>'
            f'<td class="timeline-label">{_esc(t["label"])}</td></tr>'
            for t in timeline
        )
        timeline_html = (
            '<li>Day-of timeline:'
            f'<table class="timeline-table"><tbody>{rows}</tbody></table>'
            '</li>'
        )

    resources = (
        '<ul class="venue-resources">'
        f'{packet_line}'
        '<li><a href="https://www.videolan.org/vlc/" target="_blank" '
        'rel="noopener">Download VLC</a> — recommended playback app</li>'
        f'{timeline_html}'
        '</ul>'
    )

    # Contacts — emergency email + hotline hours, no phone numbers
    facility_contact = venue.get("venue_facility_contact", "")
    facility_line = ""
    if facility_contact:
        facility_line = (
            f'<div class="contact-row">'
            f'<strong>Facility contact:</strong> '
            f'<a href="mailto:{_esc(facility_contact)}">{_esc(facility_contact)}</a>'
            f'</div>'
        )

    contacts = (
        '<div class="venue-contacts">'
        '<div class="contact-row">'
        '<strong>Emergency support:</strong> '
        '<a href="mailto:tech@oneearthfilmfest.org">tech@oneearthfilmfest.org</a>'
        '<span class="contact-note"> &middot; Hotline staffed April 22-26, hours in your packet</span>'
        '</div>'
        '<div class="contact-row">'
        '<strong>Host coordinator:</strong> '
        '<a href="mailto:hosts@oneearthcollective.org">hosts@oneearthcollective.org</a>'
        '</div>'
        f'{facility_line}'
        '</div>'
    )

    return (
        render_sarc_group(SARC_LABELS[0], status_details)
        + render_sarc_group(SARC_LABELS[1], asks)
        + render_sarc_group(SARC_LABELS[2], resources)
        + render_sarc_group(SARC_LABELS[3], contacts)
    )


# ---------------------------------------------------------------------------
# Venue section wrapper with state toggle
# ---------------------------------------------------------------------------

def render_venue_section(venue: Dict[str, Any], active_state: str) -> str:
    """Render a complete venue section with 3-state toggle."""
    name = venue["venue_name"]
    slug = venue_slug(name)
    city = venue.get("venue_city", "")
    region = venue.get("venue_region", "")
    location = ", ".join(filter(None, [city, region]))
    location_html = f'<span class="venue-location">{_esc(location)}</span>' if location else ""

    states = {
        "feb": render_feb_state(venue),
        "mar": render_mar_state(venue),
        "apr": render_apr_state(venue),
    }

    state_divs = ""
    for state_key in ("feb", "mar", "apr"):
        active_class = " active" if state_key == active_state else ""
        state_divs += (
            f'<div class="venue-state venue-state-{state_key}{active_class}" '
            f'data-state="{state_key}">'
            f'{states[state_key]}'
            f'</div>'
        )

    return (
        f'<div class="venue-section" id="venue-{slug}">'
        f'<div class="venue-header">'
        f'<h3 class="venue-name">{_esc(name)}</h3>'
        f'{location_html}'
        f'</div>'
        f'<div class="venue-toggle" role="tablist" aria-label="View by planning phase">'
        f'<button class="venue-toggle-btn{" active" if active_state == "feb" else ""}" '
        f'data-target="feb" role="tab" aria-selected="{"true" if active_state == "feb" else "false"}">February</button>'
        f'<button class="venue-toggle-btn{" active" if active_state == "mar" else ""}" '
        f'data-target="mar" role="tab" aria-selected="{"true" if active_state == "mar" else "false"}">March</button>'
        f'<button class="venue-toggle-btn{" active" if active_state == "apr" else ""}" '
        f'data-target="apr" role="tab" aria-selected="{"true" if active_state == "apr" else "false"}">April</button>'
        f'</div>'
        f'<div class="venue-states">'
        f'{state_divs}'
        f'</div>'
        f'</div>'
    )


def render_venue_styles() -> str:
    """CSS for venue sections — uses existing OEFF design tokens."""
    return """<style>
/* Venue sections — generated by generate-venue-sections.py */
.venue-sections-wrapper {
  margin: var(--space-lg, 2rem) 0;
}
.venue-sections-wrapper > h2 {
  font-family: var(--font-display, Georgia, serif);
  color: var(--color-heading, #2c3e2d);
  margin-bottom: var(--space-md, 1.5rem);
}
.venue-section {
  background: var(--color-surface, #fafaf7);
  border: 1px solid var(--color-border, #d5d0c8);
  border-radius: 8px;
  padding: var(--space-md, 1.5rem);
  margin-bottom: var(--space-md, 1.5rem);
}
.venue-header {
  margin-bottom: var(--space-sm, 0.75rem);
}
.venue-name {
  font-family: var(--font-display, Georgia, serif);
  font-size: 1.25rem;
  color: var(--color-heading, #2c3e2d);
  margin: 0;
}
.venue-location {
  font-size: 0.875rem;
  color: var(--color-text-muted, #6b7c6b);
}
.venue-toggle {
  display: flex;
  gap: 0.25rem;
  margin-bottom: var(--space-sm, 0.75rem);
  background: var(--color-bg-subtle, #f0ede6);
  border-radius: 6px;
  padding: 3px;
}
.venue-toggle-btn {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--color-text-muted, #6b7c6b);
  font-size: 0.8125rem;
  font-family: var(--font-body-sans, system-ui, sans-serif);
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease;
  min-height: 44px;
}
.venue-toggle-btn.active {
  background: var(--color-surface, #fff);
  color: var(--color-heading, #2c3e2d);
  box-shadow: 0 1px 3px hsla(25, 40%, 30%, 0.08);
}
.venue-state { display: none; }
.venue-state.active { display: block; }
.sarc-group {
  margin-bottom: var(--space-sm, 0.75rem);
}
.sarc-label {
  font-family: var(--font-body-sans, system-ui, sans-serif);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted, #6b7c6b);
  margin: 0 0 0.375rem 0;
}
.venue-badge {
  display: inline-block;
  font-family: var(--font-body-sans, system-ui, sans-serif);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.625rem;
  border-radius: 999px;
  margin-bottom: 0.5rem;
}
.badge-confirmed { background: #e8f0e8; color: #2c5f2d; }
.badge-ontrack { background: #eef3e0; color: #4a6420; }
.badge-ready { background: #e0f0e8; color: #1a5c3a; }
.screening-detail {
  display: flex;
  justify-content: space-between;
  padding: 0.375rem 0;
  border-bottom: 1px solid var(--color-border-light, #e8e4dc);
  font-size: 0.875rem;
}
.screening-label {
  color: var(--color-text-muted, #6b7c6b);
}
.screening-value {
  font-weight: 500;
  color: var(--color-heading, #2c3e2d);
}
.screening-value.pending {
  color: var(--color-text-muted, #6b7c6b);
  font-style: italic;
}
.venue-asks, .venue-resources {
  margin: 0;
  padding-left: 1.25rem;
  font-size: 0.875rem;
  line-height: 1.7;
}
.venue-asks li, .venue-resources li {
  margin-bottom: 0.375rem;
}
.venue-contacts {
  font-size: 0.875rem;
}
.contact-row {
  padding: 0.375rem 0;
}
.contact-note {
  color: var(--color-text-muted, #6b7c6b);
  font-size: 0.8125rem;
}
.timeline-table {
  width: 100%;
  font-size: 0.8125rem;
  margin-top: 0.5rem;
  border-collapse: collapse;
}
.timeline-table td {
  padding: 0.25rem 0.5rem;
  border-bottom: 1px solid var(--color-border-light, #e8e4dc);
}
.timeline-time {
  white-space: nowrap;
  font-weight: 500;
  width: 5rem;
  color: var(--color-heading, #2c3e2d);
}
</style>"""


def render_venue_toggle_script() -> str:
    """JS for venue state toggle."""
    return """<script>
/* Venue section toggle — generated by generate-venue-sections.py */
document.querySelectorAll('.venue-toggle-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var section = btn.closest('.venue-section');
    var target = btn.dataset.target;
    section.querySelectorAll('.venue-toggle-btn').forEach(function(b) {
      b.classList.remove('active');
      b.setAttribute('aria-selected', 'false');
    });
    btn.classList.add('active');
    btn.setAttribute('aria-selected', 'true');
    section.querySelectorAll('.venue-state').forEach(function(s) {
      s.classList.remove('active');
    });
    var targetState = section.querySelector('.venue-state-' + target);
    if (targetState) targetState.classList.add('active');
  });
});
</script>"""


# ---------------------------------------------------------------------------
# Helper page rendering — per-venue mobile-first one-pagers
# ---------------------------------------------------------------------------

def load_token_map(path: Path) -> Dict[str, Any]:
    """Load the venue → token/password mapping from JSON."""
    if not path.exists():
        print(f"Error: Token map not found at {path}", file=sys.stderr)
        print("  Run generate-token-map.py first.", file=sys.stderr)
        sys.exit(1)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def render_password_gate_js(password_hash: str) -> str:
    """Inline JS for client-side password gate on the financial section."""
    return dedent(f"""\
    <script>
    /* Financial section password gate — generate-venue-sections.py */
    (function() {{
      var gate = document.getElementById('financial-gate');
      var section = document.getElementById('financial-section');
      var input = document.getElementById('financial-pw');
      var btn = document.getElementById('financial-submit');
      var err = document.getElementById('financial-error');
      if (!gate || !section) return;
      btn.addEventListener('click', function() {{
        var pw = input.value.trim();
        if (!pw) return;
        crypto.subtle.digest('SHA-256', new TextEncoder().encode(pw))
          .then(function(buf) {{
            var hex = Array.from(new Uint8Array(buf))
              .map(function(b) {{ return b.toString(16).padStart(2, '0'); }})
              .join('');
            if (hex === '{password_hash}') {{
              gate.style.display = 'none';
              section.style.display = 'block';
            }} else {{
              err.style.display = 'block';
              input.value = '';
              input.focus();
            }}
          }});
      }});
      input.addEventListener('keydown', function(e) {{
        if (e.key === 'Enter') btn.click();
      }});
    }})();
    </script>""")


def render_helper_hero(venue: Dict[str, Any], state: str) -> str:
    """Render the hero card — Tier 1 info: film, date, venue, event link."""
    name = _esc(venue["venue_name"])
    film = _esc(venue["film_title"])
    event_date = _esc(venue.get("event_date", ""))
    event_time = _esc(venue.get("event_time", ""))
    address = _esc(venue.get("venue_address", ""))
    rsvp_url = venue.get("rsvp_url", "")
    ticket_price = _esc(venue.get("ticket_price", ""))

    # Format date display
    date_display = event_date
    if event_date:
        try:
            dt = datetime.strptime(event_date, "%Y-%m-%d")
            date_display = dt.strftime("%A, %B %-d")
        except (ValueError, TypeError):
            pass

    date_line = date_display
    if event_time and event_time != "TBD":
        date_line += f" at {event_time}"

    price_line = ""
    if ticket_price:
        price_line = f'<div class="hero-price">{ticket_price}</div>'

    address_line = ""
    if address:
        address_line = f'<div class="hero-address">{address}</div>'

    btn = ""
    if rsvp_url:
        btn = (
            f'<a class="helper-btn hero-btn" href="{_esc(rsvp_url)}" '
            f'target="_blank" rel="noopener">Your Event Page</a>'
        )

    return (
        '<section class="hero-card">'
        f'<div class="hero-film">{film}</div>'
        f'<div class="hero-date">{date_line if date_line else "Date coming soon"}</div>'
        f'{address_line}'
        f'{price_line}'
        f'{btn}'
        '</section>'
    )


def render_helper_ticket_count(venue: Dict[str, Any], state: str) -> str:
    """Render the ticket/RSVP count — visible in apr state, dimmed in mar."""
    rsvp_count = venue.get("rsvp_count", 0)

    if state == "feb":
        return ""  # Hidden before events are public

    muted = ' helper-muted' if state == "mar" else ""
    prominent = ' ticket-prominent' if state == "apr" else ""

    count_display = str(rsvp_count) if rsvp_count else "0"

    return (
        f'<section class="helper-section ticket-section{muted}{prominent}">'
        '<h2>Registrations</h2>'
        f'<div class="ticket-count">{_esc(count_display)}</div>'
        '<div class="ticket-label">registered so far</div>'
        '</section>'
    )


def render_helper_run_of_show(venue: Dict[str, Any], state: str) -> str:
    """Render the run of show — Tier 2 info. Hidden until data exists."""
    timeline = compute_day_of_timeline(
        venue.get("event_time", ""), venue.get("film_runtime", 0)
    )

    # Only show when we have enough data (time + runtime)
    if not timeline:
        if state == "apr":
            return (
                '<section class="helper-section helper-muted">'
                '<h2>Run of Show</h2>'
                '<p>Timeline details are being finalized. '
                'Check back closer to your event.</p>'
                '</section>'
            )
        return ""

    rows = "".join(
        f'<tr><td class="ht-time">{_esc(t["time"])}</td>'
        f'<td class="ht-label">{_esc(t["label"])}</td></tr>'
        for t in timeline
    )
    return (
        '<section class="helper-section">'
        '<h2>Run of Show</h2>'
        f'<table class="helper-timeline"><tbody>{rows}</tbody></table>'
        '</section>'
    )


def render_helper_contacts(venue: Dict[str, Any], state: str) -> str:
    """Render the contacts section — Tier 2 info."""
    cards = []

    # Host lead (from intake data)
    vc_email = venue.get("venue_contact_email", "")
    vc_name = venue.get("venue_contact_name", "")
    if vc_name or vc_email:
        label = _esc(vc_name) if vc_name else "Your host contact"
        email_link = f'<a class="hc-value" href="mailto:{_esc(vc_email)}">{_esc(vc_email)}</a>' if vc_email else ""
        cards.append(
            f'<div class="contact-card">'
            f'<span class="hc-role">Host lead</span>'
            f'<span class="hc-name">{label}</span>'
            f'{email_link}'
            f'</div>'
        )

    # AV contact
    av = venue.get("venue_av_contact", "")
    if av:
        cards.append(
            f'<div class="contact-card">'
            f'<span class="hc-role">AV contact</span>'
            f'<a class="hc-value" href="mailto:{_esc(av)}">{_esc(av)}</a>'
            f'</div>'
        )

    # OEFF rep
    oeff_rep = venue.get("oeff_rep", "")
    if oeff_rep:
        cards.append(
            f'<div class="contact-card">'
            f'<span class="hc-role">OEFF onsite rep</span>'
            f'<span class="hc-name">{_esc(oeff_rep)}</span>'
            f'</div>'
        )

    # Host coordinator (always present)
    cards.append(
        '<div class="contact-card">'
        '<span class="hc-role">Host coordinator</span>'
        '<a class="hc-value" href="mailto:hosts@oneearthcollective.org">'
        'hosts@oneearthcollective.org</a>'
        '</div>'
    )

    # Emergency support (expanded in apr)
    if state == "apr":
        cards.append(
            '<div class="contact-card contact-emergency">'
            '<span class="hc-role">Emergency support</span>'
            '<a class="hc-value" href="mailto:tech@oneearthfilmfest.org">'
            'tech@oneearthfilmfest.org</a>'
            '<span class="hc-note">Staffed April 22-26</span>'
            '</div>'
        )

    return (
        '<section class="helper-section">'
        '<h2>Your Contacts</h2>'
        '<div class="contact-grid">' + "\n".join(cards) + '</div>'
        '</section>'
    )


def render_helper_venue_details(venue: Dict[str, Any]) -> str:
    """Render venue details — Tier 3 info. Collapsible."""
    items = []

    capacity = venue.get("venue_capacity", "")
    if capacity:
        items.append(("Capacity", str(capacity)))

    # AV equipment summary
    av_items = []
    if venue.get("has_projector"):
        av_items.append("Projector")
    if venue.get("has_screen"):
        av_items.append("Screen")
    if venue.get("has_sound"):
        av_items.append("Sound system")
    if venue.get("has_computer"):
        av_items.append("Computer")
    if av_items:
        items.append(("AV equipment", ", ".join(av_items)))
    elif venue.get("venue_equipment_notes"):
        items.append(("AV notes", _esc(venue["venue_equipment_notes"])))

    if venue.get("has_wifi"):
        items.append(("WiFi", "Available"))

    if venue.get("has_wheelchair"):
        items.append(("Accessible seating", "Available"))

    space_notes = venue.get("space_notes", "")
    if space_notes:
        items.append(("Space notes", _esc(space_notes)))

    address = venue.get("venue_address", "")
    if address:
        items.append(("Address", _esc(address)))

    if not items:
        return ""

    rows = "".join(
        f'<div class="detail-row">'
        f'<span class="detail-label">{label}</span>'
        f'<span class="detail-value">{value}</span>'
        f'</div>'
        for label, value in items
    )

    return (
        '<section class="helper-section venue-details-section">'
        '<details class="venue-details">'
        '<summary><h2>Venue Details</h2></summary>'
        f'<div class="detail-grid">{rows}</div>'
        '</details>'
        '</section>'
    )


def render_helper_resources(venue: Dict[str, Any], state: str) -> str:
    """Render resources section — Tier 4 info. Links shown when populated."""
    links = []

    # Screening packet (hidden until April)
    if state == "apr":
        packet_url = venue.get("screening_packet_url", "")
        if packet_url:
            links.append(
                '<a class="resource-link" href="' + _esc(packet_url) + '" '
                'target="_blank" rel="noopener">'
                '<span class="resource-icon">&#9744;</span>'
                'Download screening packet</a>'
            )
        else:
            links.append(
                '<div class="resource-link resource-pending">'
                '<span class="resource-icon">&#9744;</span>'
                'Screening packet coming soon via email</div>'
            )

    # Host guide (always shown)
    links.append(
        '<a class="resource-link" href="https://hosts.oneearthfilmfest.org" '
        'target="_blank" rel="noopener">'
        '<span class="resource-icon">&#9782;</span>'
        'Host guide</a>'
    )

    # VLC download (apr only)
    if state == "apr":
        links.append(
            '<a class="resource-link" href="https://www.videolan.org/vlc/" '
            'target="_blank" rel="noopener">'
            '<span class="resource-icon">&#9654;</span>'
            'Download VLC (recommended player)</a>'
        )

    if not links:
        return ""

    return (
        '<section class="helper-section">'
        '<h2>Resources</h2>'
        '<div class="resource-grid">' + "\n".join(links) + '</div>'
        '</section>'
    )


def render_helper_financial_section(venue: Dict[str, Any], password_hash: str) -> str:
    """Render the password-gated financial section."""
    return (
        '<section class="helper-section">'
        '<h2>Financial Information</h2>'
        '<div id="financial-gate" class="financial-gate">'
        '<p>This section contains scholarship and financial information. '
        'Enter the password from your separate notification email.</p>'
        '<div class="gate-form">'
        '<input type="password" id="financial-pw" class="gate-input" '
        'placeholder="Enter password" autocomplete="off">'
        '<button type="button" id="financial-submit" class="gate-btn">Unlock</button>'
        '</div>'
        '<p id="financial-error" class="gate-error" style="display:none">'
        'Incorrect password. Check the email with the subject line '
        '"OEFF 2026 — Financial Information."</p>'
        '</div>'
        '<div id="financial-section" style="display:none">'
        '<p class="helper-note">Scholarship and financial details will appear here '
        'once populated by the OEFF team.</p>'
        '</div>'
        '</section>'
    )


def render_helper_update_link(venue: Dict[str, Any], update_form_url: str) -> str:
    """Render the footer with contact info and update link."""
    mailto = (
        f'mailto:hosts@oneearthcollective.org'
        f'?subject={_esc(venue["venue_name"])}%20-%20Update%20Request'
    )
    parts = [
        '<section class="helper-section helper-footer-section">',
        '<p class="helper-note">Questions? Something on this page look wrong?</p>',
        '<div class="helper-actions">',
    ]
    if update_form_url:
        parts.append(
            f'<a class="helper-btn" href="{_esc(update_form_url)}" '
            f'target="_blank" rel="noopener">Update your info</a>'
        )
    parts.append(
        f'<a class="helper-btn helper-btn-secondary" href="{mailto}">'
        f'Email hosts@oneearthcollective.org</a>'
    )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_helper_styles() -> str:
    """CSS for the host helper page — matches main host guide design."""
    return """\
<style>
/* Host helper page — generated by generate-venue-sections.py --helpers */
/* Design matched to hosts/index.html (OEFF brand: sage, Avenir, Georgia) */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --font-display: 'Avenir Next', 'Avenir', 'Segoe UI', system-ui, sans-serif;
  --font-body: Georgia, 'Times New Roman', serif;
  --font-body-sans: 'Avenir Next', 'Avenir', 'Segoe UI', system-ui, sans-serif;

  --oeff-black: #231F20;
  --oeff-sage: #92BEAA;
  --oeff-sage-deep: #6a9a84;
  --oeff-sage-light: #c8ddd2;
  --oeff-sage-mist: #F5F8F6;
  --oeff-sage-whisper: #EEF3F0;
  --oeff-warm-white: #FAFAF8;
  --oeff-ivory: #FFF3DF;

  --color-bg: var(--oeff-warm-white);
  --color-surface: #ffffff;
  --color-heading: var(--oeff-black);
  --color-text: var(--oeff-black);
  --color-text-soft: #4a4542;
  --color-text-muted: #7a746f;
  --color-border: #e5e2dc;
  --color-border-light: #edeae5;
  --color-accent: var(--oeff-sage-deep);
  --color-accent-light: var(--oeff-sage-whisper);
  --color-error: #c44;

  --shadow-soft:
    0 1px 2px rgba(146, 190, 170, 0.08),
    0 4px 8px rgba(146, 190, 170, 0.06),
    0 8px 16px rgba(35, 31, 32, 0.03);
  --shadow-elevated:
    0 2px 4px rgba(146, 190, 170, 0.10),
    0 8px 16px rgba(146, 190, 170, 0.08),
    0 16px 32px rgba(35, 31, 32, 0.04);

  --radius: 6px;
  --radius-lg: 10px;
  --radius-organic: 10px 12px 9px 11px;
  --radius-organic-sm: 5px 7px 6px 8px;

  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;

  --ease: cubic-bezier(0.4, 0, 0.2, 1);

  /* Layered grain */
  --grain-fine: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E");
}

html {
  font-size: 17px;
  -webkit-font-smoothing: antialiased;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--color-text);
  background: var(--color-bg);
  line-height: 1.7;
  letter-spacing: 0.01em;
  word-spacing: 0.02em;
  font-feature-settings: 'kern' 1, 'liga' 1, 'onum' 1;
  text-rendering: optimizeLegibility;
  -webkit-text-size-adjust: 100%;
}

/* Grain overlay */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  background: var(--grain-fine);
  opacity: 0.03;
  mix-blend-mode: multiply;
}

:focus-visible {
  outline: 2px solid var(--oeff-sage);
  outline-offset: 2px;
}
:focus:not(:focus-visible) { outline: none; }

a { color: var(--color-accent); }
a:hover { color: var(--oeff-sage-deep); }

.helper-wrap {
  max-width: 640px;
  margin: 0 auto;
  padding: var(--space-md);
}

/* Logo header — matches main host guide */
.helper-logo-header {
  background: var(--oeff-black);
  text-align: center;
  padding: var(--space-xl) var(--space-md) var(--space-lg);
  position: relative;
}
.helper-logo-header::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(146, 190, 170, 0.3), transparent);
}
.helper-logo-header img {
  height: 80px;
  width: auto;
  margin-bottom: var(--space-sm);
}
.helper-logo-header .helper-logo-label {
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--oeff-sage-light);
}

/* Header — venue name + badge */
.helper-header {
  text-align: center;
  padding: var(--space-xl) 0 var(--space-lg);
  margin-bottom: var(--space-md);
}
.helper-header h1 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}
.helper-header .helper-subtitle {
  font-family: var(--font-display);
  font-size: 0.85rem;
  color: var(--color-text-muted);
}
.helper-header .helper-badge {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.3rem 0.85rem;
  border-radius: var(--radius-organic-sm);
  background: var(--oeff-sage-whisper);
  color: var(--oeff-sage-deep);
  margin-top: var(--space-sm);
}

/* Hero card — Tier 1 */
.hero-card {
  background: var(--oeff-sage-mist);
  border: 1px solid var(--oeff-sage-light);
  border-radius: var(--radius-lg);
  padding: var(--space-2xl) var(--space-xl);
  margin-bottom: var(--space-lg);
  text-align: center;
  box-shadow: var(--shadow-soft);
}
.hero-film {
  font-family: var(--font-body);
  font-size: 1.5rem;
  font-style: italic;
  color: var(--color-heading);
  margin-bottom: var(--space-sm);
  line-height: 1.3;
}
.hero-date {
  font-family: var(--font-display);
  font-size: 1.0625rem;
  font-weight: 500;
  color: var(--color-text-soft);
  margin-bottom: 0.25rem;
}
.hero-address {
  font-family: var(--font-display);
  font-size: 0.875rem;
  color: var(--color-text-muted);
  margin-bottom: 0.25rem;
}
.hero-price {
  font-family: var(--font-display);
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  margin-bottom: var(--space-md);
}
.hero-btn {
  margin-top: var(--space-md);
}

/* Ticket count */
.ticket-section {
  text-align: center;
  padding: var(--space-xl);
}
.ticket-count {
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--oeff-sage-deep);
  line-height: 1;
  margin-bottom: 0.25rem;
}
.ticket-label {
  font-family: var(--font-display);
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.ticket-prominent {
  border-left-color: var(--oeff-sage);
  border-left-width: 4px;
}
.ticket-prominent .ticket-count {
  font-size: 3rem;
  color: var(--oeff-sage-deep);
}

/* Standard section */
.helper-section {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--oeff-sage-light);
  border-radius: var(--radius-lg);
  padding: var(--space-xl);
  margin-bottom: var(--space-lg);
  box-shadow: var(--shadow-soft);
}
.helper-section h2 {
  font-family: var(--font-display);
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--oeff-sage-deep);
  margin-bottom: var(--space-sm);
}
.helper-muted {
  opacity: 0.6;
}

/* Run of show / Timeline */
.helper-timeline {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.92rem;
}
.helper-timeline td {
  padding: var(--space-sm) var(--space-sm);
  border-bottom: 1px solid var(--color-border-light);
  vertical-align: top;
}
.ht-time {
  white-space: nowrap;
  font-weight: 600;
  width: 5.5rem;
  color: var(--color-heading);
  font-family: var(--font-display);
  font-size: 0.85rem;
}
.ht-label {
  color: var(--color-text-soft);
  line-height: 1.65;
}

/* Contact cards */
.contact-grid {
  display: grid;
  gap: var(--space-sm);
}
.contact-card {
  display: flex;
  flex-direction: column;
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--color-border-light);
}
.contact-card:last-child { border-bottom: none; }
.contact-emergency {
  border-left: 3px solid var(--oeff-sage);
  padding-left: var(--space-sm);
  margin-top: var(--space-xs);
}
.hc-role {
  font-family: var(--font-display);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.125rem;
}
.hc-name {
  font-size: 0.9375rem;
  color: var(--color-heading);
  font-weight: 500;
}
.hc-value {
  font-size: 0.92rem;
  color: var(--oeff-sage-deep);
  text-decoration: none;
  word-break: break-all;
}
.hc-value:hover { text-decoration: underline; }
.hc-note {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  font-style: italic;
}

/* Venue details (collapsible) */
.venue-details-section {
  padding: 0;
  border-left-width: 1px;
}
.venue-details {
  padding: var(--space-xl);
}
.venue-details summary {
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: var(--space-xs);
  min-height: 44px;
}
.venue-details summary::before {
  content: '+';
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 600;
  color: var(--oeff-sage-deep);
  width: 1.25rem;
  text-align: center;
  flex-shrink: 0;
}
.venue-details[open] summary::before {
  content: '\\2212';
}
.venue-details summary h2 {
  margin-bottom: 0;
}
.venue-details summary::-webkit-details-marker { display: none; }
.detail-grid {
  margin-top: var(--space-md);
}
.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--color-border-light);
  font-size: 0.9375rem;
  gap: var(--space-md);
}
.detail-row:last-child { border-bottom: none; }
.detail-label {
  color: var(--color-text-muted);
  font-family: var(--font-display);
  font-size: 0.8125rem;
  flex-shrink: 0;
}
.detail-value {
  color: var(--color-heading);
  text-align: right;
}

/* Resource links */
.resource-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
.resource-link {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: var(--oeff-sage-mist);
  border-radius: var(--radius);
  text-decoration: none;
  color: var(--color-heading);
  font-size: 0.9375rem;
  min-height: 44px;
  transition: background 0.15s var(--ease);
}
.resource-link:hover {
  background: var(--oeff-sage-whisper);
}
.resource-pending {
  opacity: 0.6;
  cursor: default;
}
.resource-icon {
  font-size: 1.1rem;
  width: 1.5rem;
  text-align: center;
  flex-shrink: 0;
}

/* Buttons */
.helper-btn {
  display: inline-block;
  font-family: var(--font-display);
  font-size: 0.9375rem;
  font-weight: 600;
  padding: var(--space-sm) var(--space-xl);
  min-height: 44px;
  line-height: 1.5;
  border-radius: var(--radius-organic-sm);
  background: var(--oeff-sage);
  color: var(--oeff-black);
  text-decoration: none;
  text-align: center;
  border: none;
  cursor: pointer;
  transition: all 0.15s var(--ease);
}
.helper-btn:hover { background: var(--oeff-sage-deep); color: #fff; }
.helper-btn-secondary {
  background: transparent;
  color: var(--oeff-sage-deep);
  border: 1.5px solid var(--oeff-sage-light);
}
.helper-btn-secondary:hover {
  background: var(--oeff-sage-mist);
  border-color: var(--oeff-sage);
}
.helper-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

/* Password gate */
.financial-gate p {
  font-size: 0.9375rem;
  margin-bottom: 0.75rem;
}
.gate-form {
  display: flex;
  gap: 0.5rem;
}
.gate-input {
  flex: 1;
  font-family: var(--font-body-sans);
  font-size: 1rem;
  padding: 0.625rem 0.75rem;
  min-height: 44px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg);
}
.gate-input:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: -1px;
}
.gate-btn {
  font-family: var(--font-display);
  font-size: 0.9375rem;
  font-weight: 600;
  padding: 0.625rem 1.25rem;
  min-height: 44px;
  border: none;
  border-radius: var(--radius-organic-sm);
  background: var(--oeff-sage);
  color: var(--oeff-black);
  cursor: pointer;
  transition: all 0.15s var(--ease);
}
.gate-btn:hover { background: var(--oeff-sage-deep); color: #fff; }
.gate-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Footer */
.helper-footer-section {
  background: transparent;
  border: 1px dashed var(--color-border);
  box-shadow: none;
  text-align: center;
}
.helper-footer-section h2 {
  color: var(--color-text);
}
.helper-footer-section .helper-note {
  margin-bottom: var(--space-md);
}

.helper-note {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  font-style: italic;
  margin-top: 0.5rem;
}

.helper-updated {
  text-align: center;
  font-family: var(--font-display);
  font-size: 0.75rem;
  color: var(--color-text-muted);
  padding: var(--space-lg) 0;
}

/* Print */
@media print {
  body { background: #fff; }
  body::before { display: none; }
  .helper-wrap { max-width: 100%; padding: 0; }
  .helper-section, .hero-card { box-shadow: none; break-inside: avoid; }
  .financial-gate, .helper-footer-section { display: none; }
  .venue-details[open] { display: block; }
}

@media (min-width: 640px) {
  .helper-wrap { padding: 2rem; }
  .gate-form { max-width: 400px; }
  .helper-actions { flex-direction: row; justify-content: center; }
  .contact-grid { grid-template-columns: 1fr 1fr; }
}
</style>"""


def render_helper_page(
    venue: Dict[str, Any],
    state: str,
    token_entry: Dict[str, Any],
) -> str:
    """Render a complete per-venue host helper page.

    Section order follows the information design hierarchy:
      1. Header — OEFF logo + venue name + badge
      2. Hero card — Film title, date/time, venue address, event page button (Tier 1)
      3. Ticket count — RSVP number, hidden in feb, dimmed in mar, prominent in apr (Tier 2)
      4. Run of Show — Day-of timeline, hidden until data exists (Tier 2)
      5. Your Contacts — Host lead, AV, OEFF rep, coordinator (Tier 2)
      6. Venue Details — Collapsible: capacity, AV, WiFi, ADA (Tier 3)
      7. Resources — Host guide, screening packet, VLC (Tier 4)
      8. Footer — "Questions?" + last-updated timestamp
    """
    name = _esc(venue["venue_name"])
    password_hash = token_entry.get("financial_password_hash", "")

    # State-aware badge
    badge_map = {
        "feb": "Confirmed Host",
        "mar": "On Track",
        "apr": "Ready",
    }
    badge_text = badge_map.get(state, "")

    # Build page sections in hierarchy order
    sections = [
        render_helper_hero(venue, state),
        render_helper_ticket_count(venue, state),
        render_helper_run_of_show(venue, state),
        render_helper_contacts(venue, state),
        render_helper_venue_details(venue),
        render_helper_resources(venue, state),
    ]

    # Financial section (password-gated, only if hash exists)
    if password_hash:
        sections.append(render_helper_financial_section(venue, password_hash))

    # "Something wrong?" footer
    update_form_url = token_entry.get("update_form_url", "")
    sections.append(render_helper_update_link(venue, update_form_url))

    # Filter empty sections
    body = "\n".join(s for s in sections if s)

    # Last-updated timestamp
    today_str = date.today().strftime("%B %-d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{name} — OEFF 2026 Host Helper</title>
{render_helper_styles()}
</head>
<body>
<div class="helper-logo-header">
<img src="/OEFF_Logo_Reverse_Stacked.png" alt="One Earth Film Festival" width="200" height="auto">
<div class="helper-logo-label">Your Screening Page</div>
</div>
<div class="helper-wrap">
<header class="helper-header">
<h1>{name}</h1>
<div class="helper-subtitle">One Earth Film Festival 2026</div>
<span class="helper-badge">{badge_text}</span>
</header>
{body}
<div class="helper-updated">Last updated {today_str}</div>
</div>
{render_password_gate_js(password_hash) if password_hash else ''}
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Venue name reconciliation — Airtable names ↔ token map keys
# ---------------------------------------------------------------------------

# Explicit aliases: Airtable venue name → token map key.
# The token map was generated from an earlier Airtable snapshot where venue
# names had different formatting or parenthetical notes. This table maps
# current Airtable names to the token map's canonical keys.
VENUE_NAME_ALIASES: Dict[str, str] = {
    "Academy for Global Citizenship":
        "Cultivate Collective (at Academy for Global Citizenship)",
    "Cultivate Collective at Academy for Global Citizenship":
        "Cultivate Collective (at Academy for Global Citizenship)",
    "Chicago Climate Action Museum":
        "Chicago Climate Action Museum",  # needs token — no alias, just new
    "Chicago Public Library Harold Washington Branch":
        "Chicago Public Library Harold Washington Branch",  # needs token
    "Chicago Public Library Rogers Park Branch":
        "Chicago Public Library Rogers Park Branch",  # needs token
    "IIT Bronzeville":
        "IIT Bronzeville",  # needs token
    "Andersonville Chamber of Commerce":
        "Andersonville Chamber of Commerce",  # needs token
    "Calumet College of St. Joseph":
        "Calumet College of St. Joseph",  # needs token
}


def _match_venue_to_token(
    name: str, token_map: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Match an Airtable venue name to a token map entry.

    Strategy (in order):
      1. Exact match on token map key
      2. Explicit alias lookup
      3. Substring containment — if the Airtable name is contained in
         exactly one token map key (handles parenthetical suffixes)
    """
    # 1. Exact match
    entry = token_map.get(name)
    if entry:
        return entry

    # 2. Alias lookup
    alias = VENUE_NAME_ALIASES.get(name, "")
    if alias and alias in token_map:
        return token_map[alias]

    # 3. Substring containment — Airtable name inside token map key
    candidates = [
        (k, v) for k, v in token_map.items()
        if name.lower() in k.lower() or k.lower() in name.lower()
    ]
    if len(candidates) == 1:
        return candidates[0][1]

    return None


def generate_helper_pages(
    venues: List[Dict[str, Any]],
    state: str,
    token_map: Dict[str, Any],
    dry_run: bool = False,
) -> int:
    """Generate per-venue helper pages. Returns count of pages generated."""
    generated = 0
    skipped = []

    for venue in venues:
        name = venue["venue_name"]
        entry = _match_venue_to_token(name, token_map)

        if not entry:
            skipped.append(name)
            continue

        token = entry.get("token", "")
        if not token:
            skipped.append(name)
            continue

        html = render_helper_page(venue, state, entry)

        # Privacy check on the helper page (allow password gate keywords)
        privacy_findings = check_privacy(html, allow_password_gate=True)
        if privacy_findings:
            print(f"Privacy lint FAILED for {name}:", file=sys.stderr)
            for finding in privacy_findings:
                print(f"  {finding}", file=sys.stderr)
            return -1

        if dry_run:
            print(f"  [dry-run] Would write hosts/{token}/index.html for {name}")
            generated += 1
            continue

        # Create directory and write
        page_dir = HELPERS_DIR / token
        page_dir.mkdir(parents=True, exist_ok=True)
        page_path = page_dir / "index.html"
        page_path.write_text(html, encoding="utf-8")
        generated += 1

    if skipped:
        print(
            f"  Skipped {len(skipped)} venue(s) with no token mapping: "
            f"{', '.join(skipped[:5])}{'...' if len(skipped) > 5 else ''}",
            file=sys.stderr,
        )

    return generated


# ---------------------------------------------------------------------------
# Full render
# ---------------------------------------------------------------------------

def render_all_sections(venues: List[Dict[str, Any]], active_state: str) -> str:
    """Render the complete venue sections block."""
    if not venues:
        return (
            f'\n{SENTINEL_BEGIN}\n'
            '<!-- No venue data available -->\n'
            f'{SENTINEL_END}\n'
        )

    sections = "\n".join(render_venue_section(v, active_state) for v in venues)

    return (
        f'\n{SENTINEL_BEGIN}\n'
        f'{render_venue_styles()}\n'
        '<div class="venue-sections-wrapper">\n'
        '<h2 class="section-title">Your Screening</h2>\n'
        f'{sections}\n'
        '</div>\n'
        f'{render_venue_toggle_script()}\n'
        f'{SENTINEL_END}\n'
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_sarc_order(html: str) -> List[str]:
    """Check that every venue-state div has 4 SARC labels in correct order."""
    errors: List[str] = []
    # Find each venue-state block
    state_pattern = re.compile(r'class="venue-state\s[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>', re.DOTALL)
    # Find sarc labels within
    label_pattern = re.compile(r'class="sarc-label">([^<]+)<')

    # Simpler approach: find all sarc-label sequences within venue-state divs
    state_blocks = re.findall(r'<div class="venue-state [^"]*"[^>]*>(.*?)</div>\s*(?=<div class="venue-state|</div>\s*</div>\s*</div>)', html, re.DOTALL)

    if not state_blocks:
        # Fallback: just check global ordering of labels
        labels = label_pattern.findall(html)
        # Labels should repeat in groups of 4
        for i in range(0, len(labels), 4):
            group = labels[i : i + 4]
            if group != SARC_LABELS[:len(group)]:
                errors.append(
                    f"SARC order violation at label group {i // 4 + 1}: "
                    f"got {group}, expected {SARC_LABELS[:len(group)]}"
                )
    else:
        for idx, block in enumerate(state_blocks):
            labels = label_pattern.findall(block)
            if labels != SARC_LABELS:
                errors.append(
                    f"SARC order violation in state block {idx + 1}: "
                    f"got {labels}, expected {SARC_LABELS}"
                )

    return errors


def check_privacy(html: str, allow_password_gate: bool = False) -> List[str]:
    """Reject phone patterns, Dropbox URLs, and password keywords.

    Args:
        html: The HTML to check.
        allow_password_gate: If True, skip the 'password' keyword check.
            Used for helper pages that intentionally contain a password gate UI.
            Phone numbers and Dropbox URLs are always checked.
    """
    findings: List[str] = []
    for i, line in enumerate(html.splitlines(), 1):
        if PHONE_RE.search(line):
            findings.append(f"Phone number pattern at line {i}: {line.strip()[:120]}")
        if not allow_password_gate and PRIVATE_WORD_RE.search(line):
            findings.append(f"Private keyword at line {i}: {line.strip()[:120]}")
        if PRIVATE_URL_RE.search(line):
            findings.append(f"Dropbox URL at line {i}: {line.strip()[:120]}")
    return findings


# ---------------------------------------------------------------------------
# Injection
# ---------------------------------------------------------------------------

def inject_into_html(sections_html: str, html_path: Path) -> None:
    """Replace content between sentinels in the host guide HTML."""
    if not html_path.exists():
        print(f"Error: {html_path} not found", file=sys.stderr)
        sys.exit(1)

    content = html_path.read_text(encoding="utf-8")

    begin_idx = content.find(SENTINEL_BEGIN)
    end_idx = content.find(SENTINEL_END)

    if begin_idx == -1 or end_idx == -1:
        print(
            f"Error: Sentinel comments not found in {html_path}\n"
            f"  Expected: {SENTINEL_BEGIN}\n"
            f"  And:      {SENTINEL_END}",
            file=sys.stderr,
        )
        sys.exit(1)

    end_idx += len(SENTINEL_END)
    new_content = content[:begin_idx] + sections_html + content[end_idx:]
    html_path.write_text(new_content, encoding="utf-8")
    print(f"Injected venue sections into {html_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate OEFF venue sections from Airtable data."
    )
    parser.add_argument(
        "--today",
        help="Override today's date (YYYY-MM-DD) for state inference.",
    )
    parser.add_argument(
        "--output",
        help="Write standalone HTML fragment to this path instead of injecting.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch, generate, and validate — but don't write any files.",
    )
    parser.add_argument(
        "--helpers",
        action="store_true",
        help="Generate per-venue host helper pages at hosts/[token]/index.html.",
    )
    parser.add_argument(
        "--token-map",
        metavar="FILE",
        help=f"Path to token-map.json (default: {TOKEN_MAP_PATH}).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    # Determine date and state
    if args.today:
        today = date.fromisoformat(args.today)
    else:
        today = date.today()

    state = infer_state(today)
    print(f"Date: {today.isoformat()}  State: {state}", file=sys.stderr)

    # Fetch from Airtable
    token = get_token()
    print("Fetching records from Airtable...", file=sys.stderr)
    if args.helpers:
        # Helper pages don't require the 2026_Venue_Sections view —
        # fetch Events filtered by Year=2026, excluding archived records
        records = fetch_by_filter(TABLE_NAME, 'AND({Year}=2026,{Archive Status}!="Archived")', token)
    else:
        # Try the named view first; fall back to filterByFormula if it doesn't exist.
        # The 2026_Venue_Sections view may not yet exist in Airtable — filter client-side
        # after fetching, or use formula to pre-filter on the server.
        #
        # Strategy: fetch with filterByFormula for 2026 events in an active pipeline
        # state. This works without requiring the view to exist, and the field mapping
        # in normalize_record() handles field name differences.
        pipeline_filter = (
            'AND('
            '{Year}=2026,'
            '{Archive Status}!="Archived",'
            'OR({Pipeline Select}="Scheduled",{Pipeline Select}="Confirmed Interest",'
            '{Pipeline Select}="Confirmed",{Pipeline Status}="Confirmed",'
            '{Pipeline Status}="Scheduled")'
            ')'
        )
        try:
            records = fetch_all_records(TABLE_NAME, VIEW_NAME, token)
            print(f"  Using view: {VIEW_NAME}", file=sys.stderr)
        except Exception as e:
            print(
                f"  View '{VIEW_NAME}' not found ({e}), falling back to filterByFormula",
                file=sys.stderr,
            )
            records = fetch_by_filter(TABLE_NAME, pipeline_filter, token)

    if not records:
        print("Warning: No records returned from Airtable.", file=sys.stderr)

    # Normalize field names on Event records to match script's canonical names.
    # This handles the gap between Airtable's actual field names and the names
    # the script was designed around (Event_Date, RSVP_URL, etc.).
    records = [normalize_record(r, EVENTS_FIELD_MAP) for r in records]
    print(f"  Normalized {len(records)} event record(s)", file=sys.stderr)

    # Resolve linked records
    print("Resolving linked records...", file=sys.stderr)
    venues_cache, films_cache, contacts_cache = resolve_linked_records(records, token)

    # Normalize Venue linked records for field name compatibility
    venues_cache = {k: normalize_venue_record(v) for k, v in venues_cache.items()}

    # Assemble venue data
    venues = assemble_venues(records, venues_cache, films_cache, contacts_cache)
    print(f"Assembled {len(venues)} venue(s)", file=sys.stderr)

    # For helpers mode, use a simpler assembly path
    if args.helpers:
        # Events records have denormalized fields — assemble directly
        # without the full linked-record resolution
        venues = assemble_venues_for_helpers(records, token)
        print(f"Assembled {len(venues)} venue(s) for helper pages", file=sys.stderr)

        token_map_path = Path(args.token_map) if args.token_map else TOKEN_MAP_PATH
        print(f"Loading token map from {token_map_path}...", file=sys.stderr)
        token_map = load_token_map(token_map_path)
        print(f"  {len(token_map)} venue(s) in token map", file=sys.stderr)

        print("Generating helper pages...", file=sys.stderr)
        count = generate_helper_pages(venues, state, token_map, args.dry_run)

        if count < 0:
            print("Build FAILED — privacy lint errors above.", file=sys.stderr)
            return 2

        if args.dry_run:
            print(f"(dry run — {count} page(s) validated, no files written)", file=sys.stderr)
        else:
            print(f"Generated {count} helper page(s) in {HELPERS_DIR}/", file=sys.stderr)

        return 0

    # Render public venue sections
    sections_html = render_all_sections(venues, state)

    # Validate SARC order
    sarc_errors = validate_sarc_order(sections_html)
    if sarc_errors:
        print("SARC validation errors:", file=sys.stderr)
        for err in sarc_errors:
            print(f"  {err}", file=sys.stderr)
        return 2

    # Privacy check
    privacy_findings = check_privacy(sections_html)
    if privacy_findings:
        print("Privacy lint failures:", file=sys.stderr)
        for finding in privacy_findings:
            print(f"  {finding}", file=sys.stderr)
        return 2

    print(f"Validation passed (SARC OK, privacy OK)", file=sys.stderr)

    # Output — standard venue sections
    if args.dry_run:
        print(sections_html)
        print("(dry run — no files written)", file=sys.stderr)
        return 0

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(sections_html, encoding="utf-8")
        print(f"Wrote standalone fragment to {output_path}", file=sys.stderr)
    else:
        inject_into_html(sections_html, HOSTS_HTML)

    return 0


if __name__ == "__main__":
    sys.exit(main())
