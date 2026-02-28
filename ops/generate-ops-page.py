#!/usr/bin/env python3
"""
generate-ops-page.py — OEFF Ops Dashboard generator

Reads ops/kim-tasks.json, generates hosts/ops/index.html.
With --airtable flag, also fetches live venue/event data from Airtable
and renders a Host Readiness section.

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
OUTPUT_FILE = SCRIPT_DIR.parent / "hosts" / "ops" / "index.html"

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
# HTML generation
# ---------------------------------------------------------------------------

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

    # Newest first
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

def html_escape(s):
    return (s
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;"))

# ---------------------------------------------------------------------------
# Airtable: Host Readiness
# ---------------------------------------------------------------------------

# Privacy guard — strip any phone numbers or emails that leak through
PHONE_RE = re.compile(r"\b\d{3}[-.)\s]?\d{3}[-.\s]?\d{4}\b")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

def fetch_readiness_data():
    """Fetch Events + linked Venues from Airtable, return readiness summary.

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

    # Build per-venue readiness — only 2026 events
    venue_events = {}  # venue_name -> list of event dicts
    for rec in records:
        fields = rec.get("fields", {})

        # Filter to 2026 season
        if fields.get("Year") != 2026 and fields.get("Season") != "2026":
            continue

        # Venue name is denormalized on the Event record
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

        # Pipeline is "confirmed" if Scheduled or Confirmed
        pipeline_ok = pipeline_status in ("Scheduled", "Confirmed")

        event_info = {
            "film_title": film_title,
            "event_date": event_date,
            "event_tier": event_tier,
            "pipeline_status": pipeline_status,
            "pipeline_confirmed": pipeline_ok,
            "ticket_set": bool(rsvp_url),
            "packet_delivered": bool(packet_url),
            "volunteer_noted": bool(volunteer_needs),
        }

        if venue_name not in venue_events:
            venue_events[venue_name] = []
        venue_events[venue_name].append(event_info)

    return venue_events


def compute_readiness(venue_events):
    """Classify venues into needs_attention and on_track.

    Current checklist (adapts as fields are populated in Airtable):
    - Pipeline confirmed? (Pipeline Status == Scheduled or Confirmed)
    - Ticket link set? (RSVP_URL non-empty — future field)
    - Screening packet delivered? (Screening_Packet_URL — future field)
    """
    needs_attention = []
    on_track = []

    for venue_name, events in sorted(venue_events.items()):
        missing_items = []
        primary = events[0]

        for ev in events:
            if not ev["pipeline_confirmed"]:
                status = ev.get("pipeline_status", "Unknown")
                missing_items.append(f"Pipeline: {status}")
            if not ev["ticket_set"]:
                missing_items.append("No ticket link")
            if not ev["packet_delivered"]:
                missing_items.append("No screening packet")

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


def render_readiness_section(venue_events):
    """Render the Host Readiness HTML section."""
    needs_attention, on_track = compute_readiness(venue_events)
    total = len(needs_attention) + len(on_track)
    on_track_count = len(on_track)

    # Build venue cards for "needs attention"
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

        missing_html = "  ".join(
            f'<span class="readiness-missing">{html_escape(m)}</span>'
            for m in v["missing"]
        )

        attention_cards.append(f"""<div class="task-card">
          <div class="task-header">
            <span class="readiness-venue">{html_escape(v["name"])}</span>
          </div>
          {"" if not detail_str else f'<div class="readiness-detail">{detail_str}</div>'}
          <div class="readiness-items">{missing_html}</div>
        </div>""")

    attention_html = "\n".join(attention_cards) if attention_cards else ""

    # On-track summary
    on_track_html = ""
    if on_track:
        on_track_html = f"""<div class="readiness-summary">
          <span class="readiness-ok">On track ({on_track_count})</span> &mdash; all items confirmed
        </div>"""

    return f"""
    <!-- Host Readiness (from Airtable) -->
    <!-- BEGIN:HOST_READINESS -->
    <section class="section" id="readiness">
      <h2>Host Readiness &mdash; {on_track_count} of {total} venues on track</h2>
      {"" if not needs_attention else f'<h3>Needs attention ({len(needs_attention)})</h3>'}
      {attention_html}
      {on_track_html}
    </section>
    <!-- END:HOST_READINESS -->
"""


# ---------------------------------------------------------------------------
# Full page template
# ---------------------------------------------------------------------------

def generate_page(data, today, readiness_html=""):
    festival_date = parse_date(data["festivalDate"])
    countdown = render_countdown(today, festival_date)
    last_updated = data["lastUpdated"]
    current_week = data.get("currentWeek", 1)

    active_tasks = render_tasks(data["tasks"], "active")
    upcoming_tasks = render_tasks(data["tasks"], "upcoming")
    done_tasks = render_tasks(data["tasks"], "done")
    updates_html = render_updates(data["updates"])
    webinars_html = render_webinars(data["webinars"])

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
    :root {{
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
    }}

    *, *::before, *::after {{ box-sizing: border-box; }}

    html {{
      font-size: 17px;
      -webkit-font-smoothing: antialiased;
      scroll-behavior: smooth;
    }}

    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
      *, *::before, *::after {{
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }}
    }}

    body {{
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
    }}

    .container {{
      max-width: 720px;
      margin: 0 auto;
      padding: var(--space-lg) var(--space-lg) var(--space-3xl);
    }}

    /* --- Header --- */

    .header {{
      text-align: center;
      padding: var(--space-2xl) 0 var(--space-xl);
      border-bottom: 1px solid var(--color-border);
      margin-bottom: var(--space-2xl);
    }}

    .header h1 {{
      font-family: var(--font-display);
      font-size: 1.6rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      margin: 0 0 var(--space-sm);
      color: var(--color-text);
    }}

    .countdown-badge {{
      display: inline-block;
      font-family: var(--font-display);
      font-size: 0.85rem;
      font-weight: 600;
      color: white;
      background: var(--oeff-sage-deep);
      padding: 0.35em 1em;
      border-radius: 20px;
      letter-spacing: 0.02em;
    }}

    .meta {{
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
      margin-top: var(--space-sm);
    }}

    /* --- Sections --- */

    .section {{
      margin-bottom: var(--space-2xl);
    }}

    .section h2 {{
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 600;
      letter-spacing: -0.01em;
      color: var(--color-text);
      margin: 0 0 var(--space-md);
      padding-bottom: var(--space-xs);
      border-bottom: 2px solid var(--oeff-sage-light);
    }}

    .section h3 {{
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--color-text-soft);
      margin: var(--space-lg) 0 var(--space-sm);
    }}

    /* --- Task cards --- */

    .task-card {{
      background: white;
      border: 1px solid var(--color-border);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      margin-bottom: var(--space-sm);
      box-shadow: var(--shadow-soft);
    }}

    .task-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: var(--space-xs);
    }}

    .stream-pill {{
      font-family: var(--font-display);
      font-size: 0.7rem;
      font-weight: 600;
      color: white;
      padding: 0.2em 0.7em;
      border-radius: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}

    .task-due {{
      font-family: var(--font-display);
      font-size: 0.78rem;
      color: var(--color-text-muted);
    }}

    .task-title {{
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    .task-notes {{
      font-size: 0.82rem;
      color: var(--color-text-muted);
      margin-top: var(--space-xs);
      font-style: italic;
    }}

    /* --- Updates --- */

    .update-item {{
      display: flex;
      gap: var(--space-md);
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      align-items: baseline;
    }}

    .update-item:last-child {{
      border-bottom: none;
    }}

    .update-date {{
      font-family: var(--font-display);
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
      white-space: nowrap;
      min-width: 3.5em;
    }}

    .update-text {{
      font-size: 0.9rem;
      color: var(--color-text-soft);
    }}

    /* --- Tables --- */

    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
    }}

    th {{
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--color-text-muted);
      text-align: left;
      padding: var(--space-xs) var(--space-sm);
      border-bottom: 2px solid var(--oeff-sage-light);
    }}

    td {{
      padding: var(--space-sm);
      border-bottom: 1px solid var(--color-border);
      vertical-align: top;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    /* Webinar rows */
    .webinar-done {{ opacity: 0.55; }}
    .webinar-next {{ background: rgba(66, 167, 194, 0.08); }}

    .webinar-status {{
      font-family: var(--font-display);
      font-size: 0.72rem;
      font-weight: 600;
      padding: 0.2em 0.6em;
      border-radius: 10px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}

    .webinar-status.done {{
      color: var(--color-text-muted);
      background: var(--oeff-sage-whisper);
    }}

    .webinar-status.next {{
      color: white;
      background: var(--oeff-aqua);
    }}

    .webinar-status.upcoming {{
      color: var(--color-text-muted);
      background: transparent;
      border: 1px solid var(--color-border);
    }}

    /* --- Host Readiness --- */

    .readiness-venue {{
      font-family: var(--font-display);
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--color-text);
    }}

    .readiness-detail {{
      font-size: 0.85rem;
      color: var(--color-text-soft);
      margin-bottom: var(--space-xs);
    }}

    .readiness-items {{
      display: flex;
      flex-wrap: wrap;
      gap: var(--space-xs);
    }}

    .readiness-missing {{
      font-family: var(--font-display);
      font-size: 0.75rem;
      font-weight: 600;
      color: #a0564e;
      background: rgba(160, 86, 78, 0.08);
      padding: 0.2em 0.6em;
      border-radius: 10px;
    }}

    .readiness-summary {{
      background: var(--oeff-sage-mist);
      border: 1px solid var(--oeff-sage-light);
      border-radius: var(--radius-lg);
      padding: var(--space-md);
      margin-top: var(--space-sm);
      font-size: 0.9rem;
      color: var(--color-text-soft);
    }}

    .readiness-ok {{
      font-family: var(--font-display);
      font-weight: 600;
      color: var(--oeff-sage-deep);
    }}

    /* --- Tools / reference tables --- */

    .ref-table td:first-child {{
      font-family: var(--font-display);
      font-weight: 600;
      font-size: 0.85rem;
      white-space: nowrap;
      width: 30%;
    }}

    .ref-table a {{
      color: var(--oeff-blue);
      text-decoration: none;
    }}

    .ref-table a:hover {{
      text-decoration: underline;
    }}

    /* --- SOP list --- */

    .sop-item {{
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      gap: var(--space-md);
    }}

    .sop-item:last-child {{
      border-bottom: none;
    }}

    .sop-number {{
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 0.85rem;
      color: var(--oeff-sage-deep);
      min-width: 1.5em;
    }}

    .sop-title {{
      flex: 1;
    }}

    .sop-title a {{
      color: var(--oeff-blue);
      text-decoration: none;
      font-weight: 600;
    }}

    .sop-title a:hover {{
      text-decoration: underline;
    }}

    .sop-desc {{
      font-size: 0.82rem;
      color: var(--color-text-muted);
      display: block;
    }}

    .sop-status {{
      font-family: var(--font-display);
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--color-text-muted);
      white-space: nowrap;
    }}

    .sop-status.active {{
      color: var(--oeff-sage-deep);
    }}

    /* --- Escalation --- */

    .escalation-item {{
      display: flex;
      gap: var(--space-md);
      padding: var(--space-sm) 0;
      border-bottom: 1px solid var(--color-border);
      font-size: 0.9rem;
    }}

    .escalation-item:last-child {{
      border-bottom: none;
    }}

    .escalation-trigger {{
      flex: 1;
      color: var(--color-text-soft);
    }}

    .escalation-action {{
      font-family: var(--font-display);
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--oeff-sage-deep);
      white-space: nowrap;
    }}

    /* --- Three questions --- */

    .questions-list {{
      list-style: none;
      padding: 0;
      margin: 0;
      counter-reset: q;
    }}

    .questions-list li {{
      counter-increment: q;
      padding: var(--space-sm) 0;
      padding-left: var(--space-xl);
      position: relative;
      font-size: 0.92rem;
      color: var(--color-text-soft);
      border-bottom: 1px solid var(--color-border);
    }}

    .questions-list li:last-child {{
      border-bottom: none;
    }}

    .questions-list li::before {{
      content: counter(q);
      position: absolute;
      left: 0;
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1rem;
      color: var(--oeff-sage-deep);
    }}

    /* --- Footer --- */

    .footer {{
      text-align: center;
      padding: var(--space-xl) 0;
      border-top: 1px solid var(--color-border);
      margin-top: var(--space-xl);
    }}

    .footer p {{
      font-family: var(--font-display);
      font-size: 0.75rem;
      color: var(--color-text-muted);
      margin: 0;
    }}

    .footer a {{
      color: var(--oeff-blue);
      text-decoration: none;
    }}

    /* --- Responsive --- */

    @media (max-width: 600px) {{
      .container {{
        padding: var(--space-md) var(--space-md) var(--space-2xl);
      }}

      .header h1 {{
        font-size: 1.3rem;
      }}

      .task-header {{
        flex-wrap: wrap;
        gap: var(--space-xs);
      }}

      .escalation-item {{
        flex-direction: column;
        gap: var(--space-xs);
      }}

      .sop-item {{
        flex-direction: column;
        gap: var(--space-xs);
      }}

      .ref-table td:first-child {{
        white-space: normal;
      }}
    }}
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
    <!-- DYNAMIC SECTIONS (from kim-tasks.json) -->
    <!-- BEGIN:DYNAMIC_CONTENT -->
    <!-- ============================================= -->

    <!-- What's Current -->
    <section class="section" id="current">
      <h2>What's Current</h2>
      {active_tasks}
    </section>

    <!-- Upcoming -->
    <section class="section" id="upcoming">
      <h3>Coming up</h3>
      {upcoming_tasks}
    </section>

    <!-- Done -->
    {"" if not [t for t in data["tasks"] if t["status"] == "done"] else '''<section class="section" id="done">
      <h3>Completed</h3>
      ''' + done_tasks + '''
    </section>'''}

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

    {readiness_html}

    <!-- ============================================= -->
    <!-- STATIC SECTIONS (from resource hub content) -->
    <!-- ============================================= -->

    <!-- Your Tools -->
    <section class="section" id="tools">
      <h2>Your Tools</h2>
      <table class="ref-table">
        <tbody>
          <tr>
            <td>hosts@ Gmail</td>
            <td>Shared inbox — all host replies come here</td>
          </tr>
          <tr>
            <td>Airtable</td>
            <td>Master data source — hosts, events, screening dates</td>
          </tr>
          <tr>
            <td>Mailmeteor</td>
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
            <td>Google Drive</td>
            <td>Shared folder for templates, recordings, working docs</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Email Templates -->
    <section class="section" id="templates">
      <h2>Email Templates</h2>
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
    </section>

    <!-- SOPs -->
    <section class="section" id="sops">
      <h2>SOPs</h2>
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
    </section>

    <!-- Team — Who Does What -->
    <section class="section" id="team">
      <h2>Team — Who Does What</h2>
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
            <td>Templates need review, technical questions, anything you're unsure about</td>
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
    </section>

    <!-- Escalation Rules -->
    <section class="section" id="escalation">
      <h2>Escalation Rules</h2>
      <div class="escalation-item">
        <span class="escalation-trigger">Host asks something you can answer</span>
        <span class="escalation-action">Answer from hosts@, your judgment</span>
      </div>
      <div class="escalation-item">
        <span class="escalation-trigger">Host asks something you're not sure about</span>
        <span class="escalation-action">Flag to Garen in Google Chat</span>
      </div>
      <div class="escalation-item">
        <span class="escalation-trigger">Host can't make a webinar</span>
        <span class="escalation-action">Reassure — recording will be sent</span>
      </div>
      <div class="escalation-item">
        <span class="escalation-trigger">Mailmeteor merge looks wrong in test</span>
        <span class="escalation-action">Don't send — screenshot to Garen</span>
      </div>
      <div class="escalation-item">
        <span class="escalation-trigger">Anything about budget, scope, or commitments</span>
        <span class="escalation-action">Escalate to Executive Director</span>
      </div>
    </section>

    <!-- Your Three Questions -->
    <section class="section" id="questions">
      <h2>Your Three Questions</h2>
      <p style="font-size: 0.88rem; color: var(--color-text-soft); margin-bottom: var(--space-md);">
        Keep a running doc with your observations. These make the system better for next time.
      </p>
      <ol class="questions-list">
        <li><strong>What tripped you up?</strong> Where did the process assume context you didn't have?</li>
        <li><strong>What's missing?</strong> If someone else needed to do this next year, what would you add?</li>
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
# Main
# ---------------------------------------------------------------------------

def main():
    today = get_today()
    data = load_data()

    # Optionally fetch Airtable data for Host Readiness
    readiness_html = ""
    if has_airtable_flag():
        try:
            venue_events = fetch_readiness_data()
            readiness_html = render_readiness_section(venue_events)
            needs, ok = compute_readiness(venue_events)
            print(
                f"Readiness: {len(ok)} on track, {len(needs)} need attention "
                f"({len(ok) + len(needs)} total venues)",
                file=sys.stderr,
            )
        except Exception as e:
            print(f"Warning: Airtable fetch failed: {e}", file=sys.stderr)
            print("Generating page without Host Readiness section.", file=sys.stderr)

    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    html = generate_page(data, today, readiness_html)

    # Privacy check — no phone numbers or emails in output
    if PHONE_RE.search(html) or EMAIL_RE.search(html):
        print("ERROR: Output contains PII (phone/email). Aborting.", file=sys.stderr)
        sys.exit(1)

    OUTPUT_FILE.write_text(html, encoding="utf-8")

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"Generated: {OUTPUT_FILE}")
    print(f"Size: {size_kb:.1f} KB")
    if size_kb > 60:
        print(f"WARNING: Output exceeds 60 KB target ({size_kb:.1f} KB)", file=sys.stderr)
    print(f"Countdown: {render_countdown(today, parse_date(data['festivalDate']))}")
    print(f"Tasks: {len(data['tasks'])} ({sum(1 for t in data['tasks'] if t['status'] == 'active')} active)")
    if readiness_html:
        print("Host Readiness: included (from Airtable)")


if __name__ == "__main__":
    main()
