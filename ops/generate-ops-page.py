#!/usr/bin/env python3
"""
generate-ops-page.py — OEFF Ops Dashboard generator

Generates two pages:
  1. Hub page (hosts/ops/index.html) — Kim's daily bookmark with tasks, updates,
     quick links, and collapsible reference sections.
  2. Readiness page (hosts/ops/readiness/index.html) — Standalone venue readiness
     with timeline-gated checklist items. Only generated with --airtable flag.

Reads ops/kim-tasks.json for task/update data.
With --airtable flag, fetches live venue data from Airtable.

Stdlib Python 3 only — no pip dependencies.

Usage:
    python3 ops/generate-ops-page.py
    python3 ops/generate-ops-page.py --today 2026-03-15
    AIRTABLE_TOKEN=pat... python3 ops/generate-ops-page.py --airtable
"""

import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
DATA_FILE = SCRIPT_DIR / "kim-tasks.json"
OUTPUT_HUB = SCRIPT_DIR.parent / "hosts" / "ops" / "index.html"
OUTPUT_READINESS = SCRIPT_DIR.parent / "hosts" / "ops" / "readiness" / "index.html"

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()

def get_today():
    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--today" and i < len(sys.argv) - 1:
            return parse_date(sys.argv[i + 1])
    return date.today()

def has_airtable_flag():
    return "--airtable" in sys.argv

# ---------------------------------------------------------------------------
# Stream labels
# ---------------------------------------------------------------------------

STREAM_LABELS = {
    0: "Onboarding",
    1: "Webinars",
    2: "Deliverables",
    3: "Milestones",
    4: "Surveys",
    5: "Cool Hosts",
}

STREAM_COLORS = {
    0: "#3960AC",  # oeff-blue
    1: "#42A7C2",  # oeff-aqua
    2: "#92BEAA",  # oeff-sage
    3: "#6a9a84",  # oeff-sage-deep
    4: "#2d4a8a",  # oeff-blue-deep
    5: "#4a4542",  # warm gray
}

# ---------------------------------------------------------------------------
# Timeline gating — readiness checklist items unlock on schedule
# ---------------------------------------------------------------------------

READINESS_GATES = {
    "pipeline_confirmed": None,         # Always shown
    "film_assigned":      "2026-03-01",
    "ticket_set":         "2026-03-15",
    "packet_delivered":   "2026-04-01",
    "volunteer_noted":    "2026-04-05",
}

READINESS_LABELS = {
    "pipeline_confirmed": "Pipeline confirmed",
    "film_assigned":      "Film assigned",
    "ticket_set":         "Ticket link set",
    "packet_delivered":   "Screening packet",
    "volunteer_noted":    "Volunteer plan",
}

def is_gated(field_key, today):
    """Return True if this checklist item is not yet due."""
    gate = READINESS_GATES.get(field_key)
    if gate is None:
        return False
    return today < parse_date(gate)

# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def html_escape(s):
    return (s
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;"))

def render_countdown(today, festival_date):
    delta = festival_date - today
    days = delta.days
    if days < 0:
        return "Festival complete"
    elif days == 0:
        return "Festival day!"
    else:
        return f"{days} days to festival"

def render_tasks(tasks, status):
    filtered = [t for t in tasks if t["status"] == status]
    if not filtered:
        return "<p style='color: var(--color-text-muted); font-style: italic;'>None right now.</p>"

    rows = []
    for t in filtered:
        stream = t.get("stream", 0)
        label = STREAM_LABELS.get(stream, "General")
        color = STREAM_COLORS.get(stream, "#4a4542")
        due = t.get("due", "")
        due_display = ""
        if due:
            d = parse_date(due)
            due_display = d.strftime("%b %d")

        notes_html = ""
        if t.get("notes"):
            notes_html = f'<div class="task-notes">{html_escape(t["notes"])}</div>'

        rows.append(f"""<div class="task-card">
          <div class="task-header">
            <span class="stream-pill" style="background: {color};">{html_escape(label)}</span>
            <span class="task-due">{html_escape(due_display)}</span>
          </div>
          <div class="task-title">{html_escape(t["title"])}</div>
          {notes_html}
        </div>""")

    return "\n".join(rows)

def render_updates(updates):
    if not updates:
        return "<p style='color: var(--color-text-muted); font-style: italic;'>No updates yet.</p>"

    sorted_updates = sorted(updates, key=lambda u: u["date"], reverse=True)
    items = []
    for u in sorted_updates:
        d = parse_date(u["date"])
        date_str = d.strftime("%b %d")
        items.append(f"""<div class="update-item">
          <span class="update-date">{html_escape(date_str)}</span>
          <span class="update-text">{html_escape(u["text"])}</span>
        </div>""")
    return "\n".join(items)

def render_webinars(webinars):
    rows = []
    for w in webinars:
        d = parse_date(w["date"])
        date_str = d.strftime("%b %d")
        status = w["status"]

        row_class = ""
        status_label = ""
        if status == "done":
            row_class = "webinar-done"
            status_label = '<span class="webinar-status done">Done</span>'
        elif status == "next":
            row_class = "webinar-next"
            status_label = '<span class="webinar-status next">Next up</span>'
        else:
            status_label = '<span class="webinar-status upcoming">Upcoming</span>'

        rows.append(f"""<tr class="{row_class}">
          <td>{html_escape(date_str)}</td>
          <td>{html_escape(w["topic"])}</td>
          <td>{status_label}</td>
        </tr>""")

    return "\n".join(rows)

# ---------------------------------------------------------------------------
# Privacy guard
# ---------------------------------------------------------------------------

PHONE_RE = re.compile(r"\b\d{3}[-.)\s]?\d{3}[-.\s]?\d{4}\b")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

# ---------------------------------------------------------------------------
# Airtable: Host Readiness
# ---------------------------------------------------------------------------

def fetch_readiness_data():
    """Fetch Events + linked Venues from Airtable, return per-venue event data.

    Actual Airtable field names (as of 2026-02-28):
      - "Venue Name" (denormalized text on Event)
      - "Pipeline Status" (e.g. "Scheduled", "Confirmed Interest", "Confirmed")
      - "Film Title" (may not exist yet on all records)
      - "Event Date" (may not exist yet)
      - "RSVP_URL", "Screening_Packet_URL", "Volunteer_Needs" (future fields)
    Only 2026-season events are included.
    """
    from airtable_api import get_token, fetch_all_records

    token = get_token()
    print("Fetching Airtable data for Host Readiness...", file=sys.stderr)

    records = fetch_all_records("Events", "Grid view", token)

    venue_events = {}  # venue_name -> list of event dicts
    for rec in records:
        fields = rec.get("fields", {})

        if fields.get("Year") != 2026 and fields.get("Season") != "2026":
            continue

        venue_name = fields.get("Venue Name", "").strip()
        if not venue_name:
            continue

        # Guard: strip any PII that might leak through
        venue_name = PHONE_RE.sub("[redacted]", venue_name)
        venue_name = EMAIL_RE.sub("[redacted]", venue_name)

        film_title = fields.get("Film Title", fields.get("Name", ""))
        event_date = fields.get("Event Date", "")
        pipeline_status = fields.get("Pipeline Status", "")
        rsvp_url = fields.get("RSVP_URL", "")
        packet_url = fields.get("Screening_Packet_URL", "")
        volunteer_needs = fields.get("Volunteer_Needs", "")
        event_tier = fields.get("Event Tier", fields.get("Tier", ""))

        pipeline_ok = pipeline_status in ("Scheduled", "Confirmed")

        event_info = {
            "film_title": film_title,
            "event_date": event_date,
            "event_tier": event_tier,
            "pipeline_status": pipeline_status,
            "pipeline_confirmed": pipeline_ok,
            "film_assigned": bool(film_title),
            "ticket_set": bool(rsvp_url),
            "packet_delivered": bool(packet_url),
            "volunteer_noted": bool(volunteer_needs),
        }

        if venue_name not in venue_events:
            venue_events[venue_name] = []
        venue_events[venue_name].append(event_info)

    return venue_events


def compute_readiness(venue_events, today):
    """Classify venues into needs_attention and on_track.

    Only checks items whose gate date has arrived. Before the gate date,
    a missing field is simply not evaluated — it's not due yet.
    """
    needs_attention = []
    on_track = []

    checklist_fields = [
        "pipeline_confirmed",
        "film_assigned",
        "ticket_set",
        "packet_delivered",
        "volunteer_noted",
    ]

    for venue_name, events in sorted(venue_events.items()):
        missing_items = []
        primary = events[0]

        for ev in events:
            for field in checklist_fields:
                if is_gated(field, today):
                    continue  # Not due yet — skip entirely
                if not ev.get(field, False):
                    if field == "pipeline_confirmed":
                        status = ev.get("pipeline_status", "Unknown")
                        missing_items.append(f"Pipeline: {status}")
                    else:
                        missing_items.append(READINESS_LABELS[field])

        # Deduplicate
        missing_items = sorted(set(missing_items))

        venue_info = {
            "name": venue_name,
            "events": events,
            "primary": primary,
            "missing": missing_items,
        }

        if missing_items:
            needs_attention.append(venue_info)
        else:
            on_track.append(venue_info)

    return needs_attention, on_track


# ---------------------------------------------------------------------------
# Shared CSS — used by both hub and readiness pages
# ---------------------------------------------------------------------------

def render_base_css():
    """CSS custom properties, reset, typography, and shared component styles."""
    return """
    :root {
      --font-display: 'Avenir Next', 'Avenir', 'Segoe UI', system-ui, sans-serif;
      --font-body: Georgia, 'Times New Roman', serif;

      --oeff-black: #231F20;
      --oeff-blue: #3960AC;
      --oeff-aqua: #42A7C2;
      --oeff-light-aqua: #BAE1E2;
      --oeff-sage: #92BEAA;
      --oeff-ivory: #FFF3DF;

      --oeff-warm-white: #FAFAF8;
      --oeff-sage-mist: #F5F8F6;
      --oeff-sage-whisper: #EEF3F0;

      --oeff-blue-deep: #2d4a8a;
      --oeff-sage-deep: #6a9a84;
      --oeff-sage-light: #c8ddd2;

      --color-text: var(--oeff-black);
      --color-text-soft: #4a4542;
      --color-text-muted: #7a746f;
      --color-bg: var(--oeff-warm-white);
      --color-bg-soft: var(--oeff-sage-mist);
      --color-border: #e5e2dc;

      --space-xs: 0.5rem;
      --space-sm: 0.75rem;
      --space-md: 1rem;
      --space-lg: 1.5rem;
      --space-xl: 2rem;
      --space-2xl: 3rem;
      --space-3xl: 4rem;

      --radius: 6px;
      --radius-lg: 10px;

      --shadow-soft:
        0 1px 2px rgba(146, 190, 170, 0.08),
        0 4px 8px rgba(146, 190, 170, 0.06),
        0 8px 16px rgba(35, 31, 32, 0.03);
      --shadow-elevated:
        0 2px 4px rgba(146, 190, 170, 0.10),
        0 8px 16px rgba(146, 190, 170, 0.08),
        0 16px 32px rgba(35, 31, 32, 0.04);

      --ease: cubic-bezier(0.4, 0, 0.2, 1);
    }

    *, *::before, *::after { box-sizing: border-box; }

    html {
      font-size: 17px;
      -webkit-font-smoothing: antialiased;
      scroll-behavior: smooth;
    }

    @media (prefers-reduced-motion: reduce) {
      html { scroll-behavior: auto; }
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
      min-height: 100vh;
    }

    .container {
      max-width: 720px;
      margin: 0 auto;
      padding: var(--space-lg) var(--space-lg) var(--space-3xl);
    }

    /* --- Header --- */

    .header {
      text-align: center;
      padding: var(--space-2xl) 0 var(--space-xl);
      border-bottom: 1px solid var(--color-border);
      margin-bottom: var(--space-2xl);
    }

    .header h1 {
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      margin: 0 0 var(--space-sm);
      color: var(--color-text);
    }

    .countdown-badge {
      display: inline-block;
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-weight: 600;
      color: white;
      background: var(--oeff-sage-deep);
      padding: 0.35em 1em;
      border-radius: 20px;
      letter-spacing: 0.02em;
    }

    .meta {
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
      margin-top: var(--space-sm);
    }

    /* --- Sections --- */

    .section {
      margin-bottom: var(--space-2xl);
    }

    .section h2 {
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      color: var(--color-text);
      margin: 0 0 var(--space-md);
      padding-bottom: var(--space-xs);
      border-bottom: 2px solid var(--oeff-sage-light);
    }

    .section h3 {
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--color-text-soft);
      margin: var(--space-lg) 0 var(--space-sm);
    }

    /* --- Task cards --- */

    .task-card {
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      margin-bottom: var(--space-sm);
      box-shadow: var(--shadow-soft);
    }

    .task-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: var(--space-xs);
    }

    .stream-pill {
      font-family: var(--font-display);
      font-size: 0.7rem;
      font-weight: 600;
      color: white;
      padding: 0.2em 0.7em;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .task-due {
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
    }

    .task-title {
      font-size: 0.95rem;
      line-height: 1.5;
    }

    .task-notes {
      font-size: 0.82rem;
      color: var(--color-text-muted);
      margin-top: var(--space-xs);
      font-style: italic;
    }

    /* --- Updates --- */

    .update-item {
      display: flex;
      gap: var(--space-md);
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      align-items: baseline;
    }

    .update-item:last-child {
      border-bottom: none;
    }

    .update-date {
      font-family: var(--font-display);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
      white-space: nowrap;
      min-width: 3.5em;
    }

    .update-text {
      font-size: 0.9rem;
      color: var(--color-text-soft);
    }

    /* --- Tables --- */

    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }

    th {
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--color-text-muted);
      text-align: left;
      padding: var(--space-xs) var(--space-sm);
      border-bottom: 2px solid var(--oeff-sage-light);
    }

    td {
      padding: var(--space-sm);
      border-bottom: 1px solid var(--color-border);
      vertical-align: top;
    }

    tr:last-child td {
      border-bottom: none;
    }

    /* Webinar rows */
    .webinar-done { opacity: 0.55; }
    .webinar-next { background: rgba(66, 167, 194, 0.08); }

    .webinar-status {
      font-family: var(--font-display);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.2em 0.6em;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }

    .webinar-status.done {
      color: var(--color-text-muted);
      background: var(--oeff-sage-whisper);
    }

    .webinar-status.next {
      color: white;
      background: var(--oeff-aqua);
    }

    .webinar-status.upcoming {
      color: var(--color-text-muted);
      background: transparent;
      border: 1px solid var(--color-border);
    }

    /* --- Host Readiness --- */

    .readiness-venue {
      font-family: var(--font-display);
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--color-text);
    }

    .readiness-detail {
      font-size: 0.85rem;
      color: var(--color-text-soft);
      margin-bottom: var(--space-xs);
    }

    .readiness-items {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-xs);
    }

    .readiness-missing {
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      color: #a0564e;
      background: rgba(160, 86, 78, 0.08);
      padding: 0.2em 0.6em;
      border-radius: 10px;
    }

    .readiness-ok-pill {
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
      background: rgba(106, 154, 132, 0.10);
      padding: 0.2em 0.6em;
      border-radius: 10px;
    }

    .readiness-summary {
      background: var(--oeff-sage-mist);
      border: 1px solid var(--oeff-sage-light);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      margin-top: var(--space-sm);
      font-size: 0.9rem;
      color: var(--color-text-soft);
    }

    .readiness-ok {
      font-family: var(--font-display);
      font-weight: 600;
      color: var(--oeff-sage-deep);
    }

    /* --- Footer --- */

    .footer {
      text-align: center;
      padding: var(--space-xl) 0;
      border-top: 1px solid var(--color-border);
      margin-top: var(--space-xl);
    }

    .footer p {
      font-family: var(--font-display);
      font-size: 0.75rem;
      color: var(--color-text-muted);
      margin: 0;
    }

    .footer a {
      color: var(--oeff-blue);
      text-decoration: none;
    }

    /* --- Responsive --- */

    @media (max-width: 600px) {
      .container {
        padding: var(--space-md) var(--space-md) var(--space-2xl);
      }

      .header h1 {
        font-size: 1.3rem;
      }

      .task-header {
        flex-wrap: wrap;
        gap: var(--space-xs);
      }
    }
"""


# ---------------------------------------------------------------------------
# Hub page CSS (page-specific additions)
# ---------------------------------------------------------------------------

def render_hub_css():
    """CSS specific to the hub page — quick links, collapsible sections, ref tables."""
    return """
    /* --- Quick Links --- */

    .quick-links {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: var(--space-sm);
      margin-bottom: var(--space-2xl);
    }

    .quick-link {
      display: block;
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      text-decoration: none;
      color: var(--color-text);
      min-height: 44px;
      box-shadow: var(--shadow-soft);
      transition: border-color 0.15s var(--ease), box-shadow 0.15s var(--ease);
    }

    .quick-link:hover {
      border-color: var(--oeff-sage);
      box-shadow: var(--shadow-elevated);
    }

    .quick-link-label {
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--oeff-blue);
      display: block;
      margin-bottom: 0.15em;
    }

    .quick-link-desc {
      font-size: 0.78rem;
      color: var(--color-text-muted);
      line-height: 1.4;
    }

    @media (max-width: 600px) {
      .quick-links {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    /* --- Readiness link card --- */

    .readiness-link-card {
      display: block;
      background: var(--oeff-sage-mist);
      border: 1px solid var(--oeff-sage-light);
      border-radius: var(--radius-lg);
      padding: var(--space-md) var(--space-lg);
      margin-bottom: var(--space-2xl);
      text-decoration: none;
      color: var(--color-text);
      transition: border-color 0.15s var(--ease), box-shadow 0.15s var(--ease);
    }

    .readiness-link-card:hover {
      border-color: var(--oeff-sage);
      box-shadow: var(--shadow-elevated);
    }

    .readiness-link-title {
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
    }

    .readiness-link-arrow {
      float: right;
      font-size: 1.1rem;
      color: var(--oeff-sage-deep);
    }

    .readiness-link-meta {
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
      margin-top: 0.2em;
    }

    /* --- Collapsible reference sections --- */

    details.ref-section {
      margin-bottom: var(--space-2xl);
    }

    details.ref-section summary {
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      color: var(--color-text);
      padding-bottom: var(--space-xs);
      border-bottom: 2px solid var(--oeff-sage-light);
      cursor: pointer;
      list-style: none;
      display: flex;
      justify-content: space-between;
      align-items: center;
      min-height: 44px;
    }

    details.ref-section summary::-webkit-details-marker {
      display: none;
    }

    details.ref-section summary::after {
      content: '+';
      font-size: 1.2rem;
      color: var(--color-text-muted);
      transition: transform 0.15s var(--ease);
    }

    details[open].ref-section summary::after {
      content: '\\2212';
    }

    details.ref-section > .ref-content {
      padding-top: var(--space-md);
    }

    /* --- Tools / reference tables --- */

    .ref-table td:first-child {
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.85rem;
      white-space: nowrap;
      width: 30%;
    }

    .ref-table a {
      color: var(--oeff-blue);
      text-decoration: none;
    }

    .ref-table a:hover {
      text-decoration: underline;
    }

    /* --- SOP list --- */

    .sop-item {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      gap: var(--space-md);
    }

    .sop-item:last-child {
      border-bottom: none;
    }

    .sop-number {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 0.85rem;
      color: var(--oeff-sage-deep);
      min-width: 1.5em;
    }

    .sop-title {
      flex: 1;
    }

    .sop-title a {
      color: var(--oeff-blue);
      text-decoration: none;
      font-weight: 600;
    }

    .sop-title a:hover {
      text-decoration: underline;
    }

    .sop-desc {
      font-size: 0.82rem;
      color: var(--color-text-muted);
      display: block;
    }

    .sop-status {
      font-family: var(--font-display);
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--color-text-muted);
      white-space: nowrap;
    }

    .sop-status.active {
      color: var(--oeff-sage-deep);
    }

    /* --- Escalation --- */

    .escalation-item {
      display: flex;
      gap: var(--space-md);
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      font-size: 0.9rem;
    }

    .escalation-item:last-child {
      border-bottom: none;
    }

    .escalation-trigger {
      flex: 1;
      color: var(--color-text-soft);
    }

    .escalation-action {
      font-family: var(--font-display);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
      white-space: nowrap;
    }

    /* --- Three questions --- */

    .questions-list {
      list-style: none;
      padding: 0;
      margin: 0;
      counter-reset: q;
    }

    .questions-list li {
      counter-increment: q;
      padding: var(--space-sm) 0;
      padding-left: var(--space-xl);
      position: relative;
      font-size: 0.92rem;
      color: var(--color-text-soft);
      border-bottom: 1px solid var(--color-border);
    }

    .questions-list li:last-child {
      border-bottom: none;
    }

    .questions-list li::before {
      content: counter(q);
      position: absolute;
      left: 0;
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1rem;
      color: var(--oeff-sage-deep);
    }

    @media (max-width: 600px) {
      .escalation-item {
        flex-direction: column;
        gap: var(--space-xs);
      }

      .sop-item {
        flex-direction: column;
        gap: var(--space-xs);
      }

      .ref-table td:first-child {
        white-space: normal;
      }
    }
"""


# ---------------------------------------------------------------------------
# Readiness page CSS (page-specific additions)
# ---------------------------------------------------------------------------

def render_readiness_css():
    """CSS specific to the readiness page — pipeline bar, legend, back link."""
    return """
    /* --- Back link --- */

    .back-link {
      display: inline-block;
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--oeff-blue);
      text-decoration: none;
      margin-bottom: var(--space-lg);
      min-height: 44px;
      line-height: 44px;
    }

    .back-link:hover {
      text-decoration: underline;
    }

    /* --- Data freshness --- */

    .data-freshness {
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
      margin-top: var(--space-xs);
    }

    /* --- Pipeline summary bar --- */

    .pipeline-bar {
      display: flex;
      gap: var(--space-sm);
      margin-bottom: var(--space-2xl);
      flex-wrap: wrap;
    }

    .pipeline-stat {
      flex: 1;
      min-width: 120px;
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      text-align: center;
      box-shadow: var(--shadow-soft);
    }

    .pipeline-stat-count {
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 700;
      color: var(--color-text);
      display: block;
    }

    .pipeline-stat-label {
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--color-text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    /* --- Checklist legend --- */

    .checklist-legend {
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-sm);
      margin-bottom: var(--space-xl);
      padding: var(--space-md);
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
    }

    .legend-item {
      font-family: var(--font-display);
      font-size: 0.78rem;
      font-weight: 600;
      padding: 0.3em 0.8em;
      border-radius: 10px;
    }

    .legend-active {
      color: var(--oeff-sage-deep);
      background: rgba(106, 154, 132, 0.10);
    }

    .legend-gated {
      color: var(--color-text-muted);
      background: transparent;
      border: 1px dashed var(--color-border);
    }
"""


# ---------------------------------------------------------------------------
# Hub page generator
# ---------------------------------------------------------------------------

def generate_hub_page(data, today, readiness_summary=None):
    """Generate the hub page — Kim's daily bookmark."""
    festival_date = parse_date(data["festivalDate"])
    countdown = render_countdown(today, festival_date)
    last_updated = data["lastUpdated"]
    current_week = data.get("currentWeek", 1)

    active_tasks = render_tasks(data["tasks"], "active")
    upcoming_tasks = render_tasks(data["tasks"], "upcoming")
    done_tasks = render_tasks(data["tasks"], "done")
    updates_html = render_updates(data["updates"])
    webinars_html = render_webinars(data["webinars"])

    # Readiness link card (only when Airtable data is available)
    readiness_card = ""
    if readiness_summary:
        on_track = readiness_summary["on_track"]
        total = readiness_summary["total"]
        readiness_card = f"""
    <!-- Readiness link card -->
    <a href="readiness/" class="readiness-link-card">
      <span class="readiness-link-arrow">&rarr;</span>
      <div class="readiness-link-title">Host Readiness &mdash; {on_track} of {total} on track</div>
      <div class="readiness-link-meta">View venue status and checklist details</div>
    </a>
"""

    # Done section (conditional)
    done_section = ""
    if [t for t in data["tasks"] if t["status"] == "done"]:
        done_section = f"""
    <!-- Done -->
    <section class="section" id="done">
      <h3>Completed</h3>
      {done_tasks}
    </section>"""

    base_css = render_base_css()
    hub_css = render_hub_css()

    return f"""<!DOCTYPE html>
<!--
  OEFF 2026 — Ops Dashboard
  Generated by generate-ops-page.py on {today.isoformat()}
  Do not edit directly — edit kim-tasks.json and regenerate.
-->
<html lang="en" data-domain="oeff">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>OEFF 2026 — Ops Dashboard</title>
  <style>
{base_css}
{hub_css}
  </style>
</head>
<body>
  <div class="container">

    <!-- ============================================= -->
    <!-- HEADER -->
    <!-- ============================================= -->
    <header class="header">
      <h1>OEFF 2026 — Ops Dashboard</h1>
      <div class="countdown-badge">{html_escape(countdown)}</div>
      <div class="meta">Week {current_week} &middot; Updated {html_escape(last_updated)}</div>
    </header>

    <!-- ============================================= -->
    <!-- QUICK LINKS -->
    <!-- ============================================= -->
    <div class="quick-links">
      <a href="https://groups.google.com/a/oneearthfilmfest.org/g/hosts" class="quick-link">
        <span class="quick-link-label">hosts@ Gmail</span>
        <span class="quick-link-desc">Shared inbox</span>
      </a>
      <a href="https://airtable.com/app9DymWrbAQaHH0K" class="quick-link">
        <span class="quick-link-label">Airtable</span>
        <span class="quick-link-desc">Master data</span>
      </a>
      <a href="https://mailmeteor.com/app" class="quick-link">
        <span class="quick-link-label">Mailmeteor</span>
        <span class="quick-link-desc">Mail merge</span>
      </a>
      <a href="https://hosts.oneearthfilmfest.org" class="quick-link">
        <span class="quick-link-label">Host Guide</span>
        <span class="quick-link-desc">Public reference</span>
      </a>
      <div class="quick-link">
        <span class="quick-link-label">Claude Project</span>
        <span class="quick-link-desc">AI comms assistant</span>
      </div>
      <a href="https://drive.google.com/drive/folders/1C8DzM8TCfkfvTlW4yiu0Wyw5F63OPm4K" class="quick-link">
        <span class="quick-link-label">Google Drive</span>
        <span class="quick-link-desc">Templates &amp; docs</span>
      </a>
    </div>

    <!-- ============================================= -->
    <!-- DYNAMIC SECTIONS (from kim-tasks.json) -->
    <!-- BEGIN:DYNAMIC_CONTENT -->
    <!-- ============================================= -->

    <!-- What's Current -->
    <section class="section" id="current">
      <h2>What&#39;s Current</h2>
      {active_tasks}
    </section>

    <!-- Upcoming -->
    <section class="section" id="upcoming">
      <h3>Coming up</h3>
      {upcoming_tasks}
    </section>

    {done_section}

    <!-- Updates -->
    <section class="section" id="updates">
      <h2>Updates</h2>
      {updates_html}
    </section>

    <!-- Webinar Schedule -->
    <section class="section" id="webinars">
      <h2>Webinar Schedule</h2>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Topic</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {webinars_html}
        </tbody>
      </table>
    </section>

    <!-- END:DYNAMIC_CONTENT -->

    {readiness_card}

    <!-- ============================================= -->
    <!-- REFERENCE SECTIONS (collapsible) -->
    <!-- ============================================= -->

    <!-- Tools -->
    <details class="ref-section" id="tools">
      <summary>Your Tools</summary>
      <div class="ref-content">
        <table class="ref-table">
          <tbody>
            <tr>
              <td><a href="https://groups.google.com/a/oneearthfilmfest.org/g/hosts">hosts@ Gmail</a></td>
              <td>Shared inbox — all host replies come here</td>
            </tr>
            <tr>
              <td><a href="https://airtable.com/app9DymWrbAQaHH0K">Airtable</a></td>
              <td>Master data source — hosts, events, screening dates</td>
            </tr>
            <tr>
              <td><a href="https://mailmeteor.com/app">Mailmeteor</a></td>
              <td>Mail merge — build and send campaigns</td>
            </tr>
            <tr>
              <td><a href="https://hosts.oneearthfilmfest.org">Host Guide</a></td>
              <td>The persistent reference hosts are pointed to in every email</td>
            </tr>
            <tr>
              <td>Claude Project</td>
              <td>AI assistant scoped to OEFF host comms — helps draft emails, process data</td>
            </tr>
            <tr>
              <td><a href="https://drive.google.com/drive/folders/1C8DzM8TCfkfvTlW4yiu0Wyw5F63OPm4K">Google Drive</a></td>
              <td>Shared folder for templates, recordings, working docs</td>
            </tr>
          </tbody>
        </table>
      </div>
    </details>

    <!-- Email Templates -->
    <details class="ref-section" id="templates">
      <summary>Email Templates</summary>
      <div class="ref-content">
        <table class="ref-table">
          <thead>
            <tr>
              <th>Template</th>
              <th>When to use</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>03 — Webinar Preview</td>
              <td>7 days before webinar</td>
            </tr>
            <tr>
              <td>04 — Webinar Reminder</td>
              <td>1 day before webinar</td>
            </tr>
            <tr>
              <td>05 — Webinar Recap</td>
              <td>Day after webinar (with recording link)</td>
            </tr>
            <tr>
              <td>01 — Host Helper URL</td>
              <td>When sharing host-specific page links</td>
            </tr>
            <tr>
              <td>02 — Financial/Password</td>
              <td>When sending secure credentials</td>
            </tr>
          </tbody>
        </table>
      </div>
    </details>

    <!-- SOPs -->
    <details class="ref-section" id="sops">
      <summary>SOPs</summary>
      <div class="ref-content">
        <div class="sop-item">
          <span class="sop-number">1</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1NxmvMUHP2Rk3vaNzzDKzwHAAUyb7s1EvpaJ-H262KKA/edit?usp=drivesdk">Webinar Cycle Process</a>
            <span class="sop-desc">Your primary playbook</span>
          </span>
          <span class="sop-status active">Active now</span>
        </div>
        <div class="sop-item">
          <span class="sop-number">2</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1zNZAYPdQV-V7hyCnGnJ9Wy2UGnv_wWIWlGAOIp5ftQQ/edit?usp=drivesdk">Deliverables Shipping</a>
            <span class="sop-desc">Film files, promo, slides, t-shirts</span>
          </span>
          <span class="sop-status">Late March</span>
        </div>
        <div class="sop-item">
          <span class="sop-number">3</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/19WmKK3AexuxIvuEP7aGqHkKoHrFPq9GWHqaa3URn-xg/edit?usp=drivesdk">Milestone Communications</a>
            <span class="sop-desc">Key-date emails (film confirmed, one week out, etc.)</span>
          </span>
          <span class="sop-status">Sends start Mar 9</span>
        </div>
        <div class="sop-item">
          <span class="sop-number">4</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1jXlsgP9l0sfhHUKufHnzL-nHNxz4zCAJZI4m-YrNy5U/edit?usp=drivesdk">Host Surveys</a>
            <span class="sop-desc">3 forms: pre-event, day-of, post-screening</span>
          </span>
          <span class="sop-status">Before Apr 1</span>
        </div>
        <div class="sop-item">
          <span class="sop-number">5</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1nlqqnt070WJgBPPmHhPD6M5Z6z73fgiPdhF-WVIb20k/edit?usp=drivesdk">Cool Host Conversion</a>
            <span class="sop-desc">Uncommitted venues pipeline</span>
          </span>
          <span class="sop-status">If needed</span>
        </div>

        <h3>Supporting References</h3>
        <div class="sop-item">
          <span class="sop-number">&bull;</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1qUuZgCqqbAvU41vY9cB_JQwGDpd_MyPv3Ypifv8e0Ks/edit?usp=drivesdk">Email Template Quick Reference</a>
            <span class="sop-desc">All templates, merge fields, send checklist</span>
          </span>
        </div>
        <div class="sop-item">
          <span class="sop-number">&bull;</span>
          <span class="sop-title">
            <a href="https://docs.google.com/document/d/1PXox5bpJK8SDFxjCS-LYBFX2vAkOVZopMC5OaMJZL1I/edit?usp=drivesdk">Who Does What</a>
            <span class="sop-desc">Team roles, decision rights, routing rules</span>
          </span>
        </div>
      </div>
    </details>

    <!-- Team -->
    <details class="ref-section" id="team">
      <summary>Team — Who Does What</summary>
      <div class="ref-content">
        <table class="ref-table">
          <thead>
            <tr>
              <th>Role</th>
              <th>Scope</th>
              <th>When to reach out</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Executive Director</td>
              <td>Strategic direction, messaging approval, budget, scope</td>
              <td>Outside your playbook, touches budget/scope</td>
            </tr>
            <tr>
              <td>Operations</td>
              <td>Eventbrite, scheduling, venue logistics</td>
              <td>Event details or scheduling questions</td>
            </tr>
            <tr>
              <td>Technical Coordinator (Garen)</td>
              <td>Comms infrastructure, data systems, your primary contact</td>
              <td>Templates need review, technical questions, anything you&#39;re unsure about</td>
            </tr>
            <tr>
              <td>AV/Production</td>
              <td>Equipment, technical specs, on-site setup</td>
              <td>Venue tech questions</td>
            </tr>
            <tr>
              <td>Marketing/Creative</td>
              <td>Trailer reel, graphics, social assets</td>
              <td>Route through AV/Production or Technical Coordinator</td>
            </tr>
          </tbody>
        </table>
      </div>
    </details>

    <!-- Escalation Rules -->
    <details class="ref-section" id="escalation">
      <summary>Escalation Rules</summary>
      <div class="ref-content">
        <div class="escalation-item">
          <span class="escalation-trigger">Host asks something you can answer</span>
          <span class="escalation-action">Answer from hosts@, your judgment</span>
        </div>
        <div class="escalation-item">
          <span class="escalation-trigger">Host asks something you&#39;re not sure about</span>
          <span class="escalation-action">Flag to Garen in Google Chat</span>
        </div>
        <div class="escalation-item">
          <span class="escalation-trigger">Host can&#39;t make a webinar</span>
          <span class="escalation-action">Reassure — recording will be sent</span>
        </div>
        <div class="escalation-item">
          <span class="escalation-trigger">Mailmeteor merge looks wrong in test</span>
          <span class="escalation-action">Don&#39;t send — screenshot to Garen</span>
        </div>
        <div class="escalation-item">
          <span class="escalation-trigger">Anything about budget, scope, or commitments</span>
          <span class="escalation-action">Escalate to Executive Director</span>
        </div>
      </div>
    </details>

    <!-- Your Three Questions -->
    <section class="section" id="questions">
      <h2>Your Three Questions</h2>
      <p style="font-size: 0.88rem; color: var(--color-text-soft); margin-bottom: var(--space-md);">
        Keep a running doc with your observations. These make the system better for next time.
      </p>
      <ol class="questions-list">
        <li><strong>What tripped you up?</strong> Where did the process assume context you didn&#39;t have?</li>
        <li><strong>What&#39;s missing?</strong> If someone else needed to do this next year, what would you add?</li>
        <li><strong>What could be tighter?</strong> Patterns you see that could become templates or checklists.</li>
      </ol>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>OEFF 2026 &middot; <a href="https://hosts.oneearthfilmfest.org">Host Guide</a></p>
    </footer>

  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Readiness page generator
# ---------------------------------------------------------------------------

def generate_readiness_page(venue_events, today, festival_date):
    """Generate the standalone readiness page."""
    countdown = render_countdown(today, festival_date)
    needs_attention, on_track = compute_readiness(venue_events, today)
    total = len(needs_attention) + len(on_track)
    on_track_count = len(on_track)
    now_str = datetime.now().strftime("%b %d, %Y %I:%M %p")

    # Pipeline summary — count venues by pipeline status
    pipeline_counts = {}
    for venue_name, events in venue_events.items():
        primary_status = events[0].get("pipeline_status", "Unknown")
        # Normalize similar statuses
        if primary_status in ("Scheduled", "Confirmed"):
            key = "Confirmed"
        elif primary_status == "Confirmed Interest":
            key = "Interest"
        else:
            key = primary_status or "Unknown"
        pipeline_counts[key] = pipeline_counts.get(key, 0) + 1

    pipeline_cards = []
    for status_label in ["Confirmed", "Interest", "Unknown"]:
        count = pipeline_counts.get(status_label, 0)
        if count > 0 or status_label == "Confirmed":
            pipeline_cards.append(f"""<div class="pipeline-stat">
        <span class="pipeline-stat-count">{count}</span>
        <span class="pipeline-stat-label">{html_escape(status_label)}</span>
      </div>""")
    pipeline_html = "\n      ".join(pipeline_cards)

    # Checklist legend — show which items are active vs gated
    legend_items = []
    for field_key in ["pipeline_confirmed", "film_assigned", "ticket_set",
                      "packet_delivered", "volunteer_noted"]:
        label = READINESS_LABELS[field_key]
        if is_gated(field_key, today):
            gate_date = parse_date(READINESS_GATES[field_key])
            gate_str = gate_date.strftime("%b %d")
            legend_items.append(
                f'<span class="legend-item legend-gated">{html_escape(label)} (unlocks {gate_str})</span>'
            )
        else:
            legend_items.append(
                f'<span class="legend-item legend-active">{html_escape(label)}</span>'
            )
    legend_html = "\n        ".join(legend_items)

    # Venue cards — needs attention
    attention_cards = []
    for v in needs_attention:
        primary = v["primary"]
        date_display = ""
        if primary["event_date"]:
            try:
                d = datetime.strptime(primary["event_date"], "%Y-%m-%d").date()
                date_display = d.strftime("%b %d")
            except ValueError:
                date_display = html_escape(primary["event_date"])

        film_display = html_escape(primary["film_title"]) if primary["film_title"] else ""
        tier = html_escape(primary.get("event_tier", ""))
        detail_parts = [p for p in [film_display, date_display, tier] if p]
        detail_str = " &middot; ".join(detail_parts)

        # Show confirmed items as sage pills, missing as red
        pills = []
        for field_key in ["pipeline_confirmed", "film_assigned", "ticket_set",
                          "packet_delivered", "volunteer_noted"]:
            if is_gated(field_key, today):
                continue  # Not due yet — don't show at all
            label = READINESS_LABELS[field_key]
            # Check across all events for this venue
            has_it = any(ev.get(field_key, False) for ev in v["events"])
            if has_it:
                pills.append(f'<span class="readiness-ok-pill">{html_escape(label)}</span>')
            else:
                if field_key == "pipeline_confirmed":
                    status = primary.get("pipeline_status", "Unknown")
                    pills.append(f'<span class="readiness-missing">Pipeline: {html_escape(status)}</span>')
                else:
                    pills.append(f'<span class="readiness-missing">{html_escape(label)}</span>')

        pills_html = "  ".join(pills)

        attention_cards.append(f"""<div class="task-card">
          <div class="task-header">
            <span class="readiness-venue">{html_escape(v["name"])}</span>
          </div>
          {"" if not detail_str else f'<div class="readiness-detail">{detail_str}</div>'}
          <div class="readiness-items">{pills_html}</div>
        </div>""")

    attention_html = "\n".join(attention_cards) if attention_cards else ""

    # On-track summary
    on_track_html = ""
    if on_track:
        on_track_names = ", ".join(html_escape(v["name"]) for v in on_track[:5])
        more = f" and {len(on_track) - 5} more" if len(on_track) > 5 else ""
        on_track_html = f"""<div class="readiness-summary">
          <span class="readiness-ok">On track ({on_track_count})</span> &mdash;
          {on_track_names}{more}
        </div>"""

    base_css = render_base_css()
    readiness_css = render_readiness_css()

    return f"""<!DOCTYPE html>
<!--
  OEFF 2026 — Host Readiness
  Generated by generate-ops-page.py on {today.isoformat()}
  Do not edit directly — regenerate with: python3 ops/generate-ops-page.py --airtable
-->
<html lang="en" data-domain="oeff">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>OEFF 2026 — Host Readiness</title>
  <style>
{base_css}
{readiness_css}
  </style>
</head>
<body>
  <div class="container">

    <a href="../" class="back-link">&larr; Ops Dashboard</a>

    <header class="header">
      <h1>Host Readiness</h1>
      <div class="countdown-badge">{html_escape(countdown)}</div>
      <div class="data-freshness">Data from Airtable &middot; Generated {html_escape(now_str)}</div>
    </header>

    <!-- Pipeline summary -->
    <div class="pipeline-bar">
      {pipeline_html}
    </div>

    <!-- Checklist legend -->
    <div class="checklist-legend">
      {legend_html}
    </div>

    <!-- Needs attention -->
    {"" if not needs_attention else f'<section class="section" id="attention"><h2>Needs attention ({len(needs_attention)})</h2>{attention_html}</section>'}

    <!-- On track -->
    {on_track_html}

    <!-- Footer -->
    <footer class="footer">
      <p>OEFF 2026 &middot; <a href="../">Ops Dashboard</a> &middot; <a href="https://hosts.oneearthfilmfest.org">Host Guide</a></p>
    </footer>

  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def check_pii(html, label):
    """Abort if output contains phone numbers or emails."""
    if PHONE_RE.search(html) or EMAIL_RE.search(html):
        print(f"ERROR: {label} contains PII (phone/email). Aborting.", file=sys.stderr)
        sys.exit(1)

def write_and_report(path, html, label):
    """Write HTML to path, report size, warn if over 60 KB."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    size_kb = path.stat().st_size / 1024
    print(f"Generated: {path} ({size_kb:.1f} KB)")
    if size_kb > 60:
        print(f"WARNING: {label} exceeds 60 KB target ({size_kb:.1f} KB)", file=sys.stderr)
    return size_kb


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    today = get_today()
    data = load_data()
    festival_date = parse_date(data["festivalDate"])

    # Optionally fetch Airtable data
    venue_events = None
    readiness_summary = None
    if has_airtable_flag():
        try:
            venue_events = fetch_readiness_data()
            needs, ok = compute_readiness(venue_events, today)
            readiness_summary = {
                "on_track": len(ok),
                "needs_attention": len(needs),
                "total": len(ok) + len(needs),
            }
            print(
                f"Readiness: {len(ok)} on track, {len(needs)} need attention "
                f"({readiness_summary['total']} total venues)",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Warning: Airtable fetch failed: {e}", file=sys.stderr)
            print("Generating hub page without readiness data.", file=sys.stderr)

    # Generate hub page
    hub_html = generate_hub_page(data, today, readiness_summary)
    check_pii(hub_html, "Hub page")
    write_and_report(OUTPUT_HUB, hub_html, "Hub page")

    # Generate readiness page (only with Airtable data)
    if venue_events is not None:
        readiness_html = generate_readiness_page(venue_events, today, festival_date)
        check_pii(readiness_html, "Readiness page")
        write_and_report(OUTPUT_READINESS, readiness_html, "Readiness page")

    # Summary
    print(f"Countdown: {render_countdown(today, festival_date)}")
    print(f"Tasks: {len(data['tasks'])} ({sum(1 for t in data['tasks'] if t['status'] == 'active')} active)")
    if readiness_summary:
        print("Host Readiness: hub link card + standalone page generated")
    else:
        print("Host Readiness: skipped (no --airtable flag)")


if __name__ == "__main__":
    main()
