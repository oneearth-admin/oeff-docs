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
    films = _fetch_by_ids("Films_2026", film_ids, token)

    # Film contacts are linked from films
    contact_ids: set = set()
    for film in films.values():
        for cid in film.get("fields", {}).get("Film_Contact", []):
            contact_ids.add(cid)
    contacts = _fetch_by_ids("Film_Contacts", contact_ids, token)

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


def render_helper_timeline(venue: Dict[str, Any]) -> str:
    """Render the day-of timeline for the helper page."""
    timeline = compute_day_of_timeline(
        venue.get("event_time", ""), venue.get("film_runtime", 0)
    )
    if not timeline:
        return ""

    rows = "".join(
        f'<tr><td class="ht-time">{_esc(t["time"])}</td>'
        f'<td class="ht-label">{_esc(t["label"])}</td></tr>'
        for t in timeline
    )
    return (
        '<section class="helper-section">'
        '<h2>Day-of Timeline</h2>'
        f'<table class="helper-timeline"><tbody>{rows}</tbody></table>'
        '</section>'
    )


def render_helper_contacts(venue: Dict[str, Any]) -> str:
    """Render the contacts section for the helper page."""
    rows = []

    # Host coordinator (always present)
    rows.append(
        '<div class="hc-row">'
        '<span class="hc-role">Host coordinator</span>'
        '<a class="hc-value" href="mailto:hosts@oneearthcollective.org">'
        'hosts@oneearthcollective.org</a>'
        '</div>'
    )

    # Venue contact
    vc_email = venue.get("venue_contact_email", "")
    vc_name = venue.get("venue_contact_name", "Venue contact")
    if vc_email:
        rows.append(
            f'<div class="hc-row">'
            f'<span class="hc-role">{_esc(vc_name)}</span>'
            f'<a class="hc-value" href="mailto:{_esc(vc_email)}">{_esc(vc_email)}</a>'
            f'</div>'
        )

    # Facility contact
    fc = venue.get("venue_facility_contact", "")
    if fc:
        rows.append(
            f'<div class="hc-row">'
            f'<span class="hc-role">Facility contact</span>'
            f'<a class="hc-value" href="mailto:{_esc(fc)}">{_esc(fc)}</a>'
            f'</div>'
        )

    # AV contact
    av = venue.get("venue_av_contact", "")
    if av:
        rows.append(
            f'<div class="hc-row">'
            f'<span class="hc-role">AV contact</span>'
            f'<a class="hc-value" href="mailto:{_esc(av)}">{_esc(av)}</a>'
            f'</div>'
        )

    # Emergency (Apr only — shown in all states for simplicity, safe info)
    rows.append(
        '<div class="hc-row">'
        '<span class="hc-role">Emergency support</span>'
        '<a class="hc-value" href="mailto:tech@oneearthfilmfest.org">'
        'tech@oneearthfilmfest.org</a>'
        '</div>'
    )

    return (
        '<section class="helper-section">'
        '<h2>Contacts</h2>'
        '<div class="helper-contacts">' + "\n".join(rows) + '</div>'
        '</section>'
    )


def render_helper_event_page(venue: Dict[str, Any]) -> str:
    """Render the event/RSVP page link section."""
    rsvp_url = venue.get("rsvp_url", "")
    if not rsvp_url:
        return ""
    return (
        '<section class="helper-section">'
        '<h2>Your Event Page</h2>'
        f'<a class="helper-btn" href="{_esc(rsvp_url)}" '
        f'target="_blank" rel="noopener">Open event page</a>'
        '</section>'
    )


def render_helper_screening_packet(venue: Dict[str, Any], state: str) -> str:
    """Render the screening packet section (Apr state only)."""
    if state != "apr":
        return (
            '<section class="helper-section helper-muted">'
            '<h2>Screening Packet</h2>'
            '<p>Your screening packet download link will appear here '
            'when it becomes available (typically 3 weeks before your event).</p>'
            '</section>'
        )

    packet_url = venue.get("screening_packet_url", "")
    if packet_url:
        return (
            '<section class="helper-section">'
            '<h2>Screening Packet</h2>'
            '<p>Download link sent via separate email. Check your inbox '
            'for the packet password.</p>'
            '<p class="helper-note">Test full playback before your event '
            '(not just the first 30 seconds).</p>'
            '<a class="helper-btn" href="https://www.videolan.org/vlc/" '
            'target="_blank" rel="noopener">Download VLC (recommended player)</a>'
            '</section>'
        )
    else:
        return (
            '<section class="helper-section">'
            '<h2>Screening Packet</h2>'
            '<p>Your screening packet download link is coming soon. '
            'You\'ll receive it via a separate email.</p>'
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
    """Render the 'something wrong?' section with update form link."""
    venue_name = _esc(venue["venue_name"])
    mailto = (
        f'mailto:hosts@oneearthcollective.org'
        f'?subject={_esc(venue["venue_name"])}%20-%20Update%20Request'
    )
    parts = [
        '<section class="helper-section helper-footer">',
        '<h2>Something wrong?</h2>',
        '<p>If any information on this page is incorrect or outdated:</p>',
        '<div class="helper-actions">',
    ]
    if update_form_url:
        parts.append(
            f'<a class="helper-btn" href="{_esc(update_form_url)}" '
            f'target="_blank" rel="noopener">Update your info</a>'
        )
    parts.append(
        f'<a class="helper-btn helper-btn-secondary" href="{mailto}">'
        f'Email the host team</a>'
    )
    parts.append('</div></section>')
    return "\n".join(parts)


def render_helper_styles() -> str:
    """CSS for the host helper page — mobile-first, semantic tokens."""
    return """\
<style>
/* Host helper page — generated by generate-venue-sections.py --helpers */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --color-bg: #fafaf7;
  --color-surface: #ffffff;
  --color-heading: #2c3e2d;
  --color-text: #3d4a3d;
  --color-text-muted: #6b7c6b;
  --color-border: #d5d0c8;
  --color-border-light: #e8e4dc;
  --color-accent: #4a7c59;
  --color-accent-light: #e8f0e8;
  --color-error: #c44;
  --font-display: 'Fraunces', Georgia, serif;
  --font-body: 'Source Serif 4', Georgia, serif;
  --font-body-sans: 'Source Sans 3', system-ui, sans-serif;
  --shadow-sm: 0 1px 3px hsla(25, 40%, 30%, 0.08);
  --shadow-md: 0 2px 8px hsla(25, 40%, 30%, 0.1);
  --radius: 8px;
}

body {
  font-family: var(--font-body);
  font-size: 16px;
  line-height: 1.6;
  color: var(--color-text);
  background: var(--color-bg);
  padding: 0;
  margin: 0;
  -webkit-text-size-adjust: 100%;
}

.helper-wrap {
  max-width: 600px;
  margin: 0 auto;
  padding: 1rem;
}

.helper-header {
  text-align: center;
  padding: 1.5rem 0 1rem;
  border-bottom: 1px solid var(--color-border-light);
  margin-bottom: 1rem;
}
.helper-header h1 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  color: var(--color-heading);
  margin-bottom: 0.25rem;
}
.helper-header .helper-subtitle {
  font-family: var(--font-body-sans);
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
.helper-header .helper-badge {
  display: inline-block;
  font-family: var(--font-body-sans);
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  background: var(--color-accent-light);
  color: var(--color-accent);
  margin-top: 0.5rem;
}
.helper-header .helper-film {
  font-size: 1rem;
  font-style: italic;
  color: var(--color-heading);
  margin-top: 0.5rem;
}
.helper-header .helper-date {
  font-family: var(--font-body-sans);
  font-size: 0.9375rem;
  color: var(--color-text);
  margin-top: 0.25rem;
}

.helper-section {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 1.25rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
}
.helper-section h2 {
  font-family: var(--font-body-sans);
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  margin-bottom: 0.75rem;
}
.helper-muted {
  opacity: 0.7;
}

/* Timeline */
.helper-timeline {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9375rem;
}
.helper-timeline td {
  padding: 0.5rem 0.5rem;
  border-bottom: 1px solid var(--color-border-light);
  vertical-align: top;
}
.ht-time {
  white-space: nowrap;
  font-weight: 600;
  width: 5.5rem;
  color: var(--color-heading);
  font-family: var(--font-body-sans);
}
.ht-label {
  color: var(--color-text);
}

/* Contacts */
.helper-contacts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.hc-row {
  display: flex;
  flex-direction: column;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--color-border-light);
}
.hc-row:last-child { border-bottom: none; }
.hc-role {
  font-family: var(--font-body-sans);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--color-text-muted);
  margin-bottom: 0.125rem;
}
.hc-value {
  font-size: 0.9375rem;
  color: var(--color-accent);
  text-decoration: none;
  word-break: break-all;
}
.hc-value:hover { text-decoration: underline; }

/* Buttons */
.helper-btn {
  display: inline-block;
  font-family: var(--font-body-sans);
  font-size: 0.9375rem;
  font-weight: 500;
  padding: 0.75rem 1.5rem;
  min-height: 44px;
  border-radius: var(--radius);
  background: var(--color-accent);
  color: #fff;
  text-decoration: none;
  text-align: center;
  border: none;
  cursor: pointer;
  transition: background 0.15s ease;
}
.helper-btn:hover { background: #3d6a4a; }
.helper-btn-secondary {
  background: transparent;
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
}
.helper-btn-secondary:hover {
  background: var(--color-accent-light);
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
  font-family: var(--font-body-sans);
  font-size: 0.9375rem;
  font-weight: 600;
  padding: 0.625rem 1.25rem;
  min-height: 44px;
  border: none;
  border-radius: var(--radius);
  background: var(--color-accent);
  color: #fff;
  cursor: pointer;
}
.gate-btn:hover { background: #3d6a4a; }
.gate-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

/* Footer */
.helper-footer {
  background: transparent;
  border: 1px dashed var(--color-border);
  box-shadow: none;
}
.helper-footer h2 {
  color: var(--color-text);
}

.helper-note {
  font-size: 0.875rem;
  color: var(--color-text-muted);
  font-style: italic;
  margin-top: 0.5rem;
}

/* Print */
@media print {
  body { background: #fff; }
  .helper-wrap { max-width: 100%; padding: 0; }
  .helper-section { box-shadow: none; break-inside: avoid; }
  .financial-gate, .helper-footer { display: none; }
}

@media (min-width: 640px) {
  .helper-wrap { padding: 2rem; }
  .gate-form { max-width: 400px; }
  .helper-actions { flex-direction: row; }
}
</style>"""


def render_helper_page(
    venue: Dict[str, Any],
    state: str,
    token_entry: Dict[str, Any],
) -> str:
    """Render a complete per-venue host helper page."""
    name = _esc(venue["venue_name"])
    film = _esc(venue["film_title"])
    event_date = _esc(venue.get("event_date", "TBD"))
    event_time = _esc(venue.get("event_time", "TBD"))
    password_hash = token_entry.get("financial_password_hash", "")

    # State-aware badge
    badge_map = {
        "feb": "Confirmed Host",
        "mar": "On Track",
        "apr": "Ready",
    }
    badge_text = badge_map.get(state, "")

    # Date/time display
    date_line = event_date
    if event_time and event_time != "TBD":
        date_line += f" at {event_time}"

    # Update form URL from token map
    update_form_url = token_entry.get("update_form_url", "")

    # Build page sections
    sections = [
        render_helper_timeline(venue),
        render_helper_contacts(venue),
        render_helper_event_page(venue),
        render_helper_screening_packet(venue, state),
    ]

    # Financial section (always present, password-gated)
    if password_hash:
        sections.append(render_helper_financial_section(venue, password_hash))

    # "Something wrong?" footer
    sections.append(render_helper_update_link(venue, update_form_url))

    # Filter empty sections
    body = "\n".join(s for s in sections if s)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{name} — OEFF 2026 Host Helper</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Source+Sans+3:wght@400;500;600&family=Source+Serif+4:opsz@8..60&display=swap" rel="stylesheet">
{render_helper_styles()}
</head>
<body>
<div class="helper-wrap">
<header class="helper-header">
<h1>{name}</h1>
<div class="helper-subtitle">One Earth Film Festival 2026</div>
<span class="helper-badge">{badge_text}</span>
<div class="helper-film">{film}</div>
<div class="helper-date">{date_line}</div>
</header>
{body}
</div>
{render_password_gate_js(password_hash) if password_hash else ''}
</body>
</html>
"""


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
        entry = token_map.get(name)

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
    records = fetch_all_records(TABLE_NAME, VIEW_NAME, token)

    if not records:
        print("Warning: No records returned from Airtable view.", file=sys.stderr)

    # Resolve linked records
    print("Resolving linked records...", file=sys.stderr)
    venues_cache, films_cache, contacts_cache = resolve_linked_records(records, token)

    # Assemble venue data
    venues = assemble_venues(records, venues_cache, films_cache, contacts_cache)
    print(f"Assembled {len(venues)} venue(s)", file=sys.stderr)

    # Render
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
    if not args.helpers:
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

    # Output — per-venue helper pages
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


if __name__ == "__main__":
    sys.exit(main())
