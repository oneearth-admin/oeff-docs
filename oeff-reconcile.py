#!/usr/bin/env python3
"""
oeff-reconcile.py — Weekly parity check across OEFF 2026 data sources.

Compares team-side Google Sheets exports (venues, contacts, milestones) against
Airtable canonical tables. Generates a structured markdown report and an
actionable patch CSV.

Designed for weekly re-runs. Stdlib Python 3 only.

Usage:
    cd "~/Desktop/OEFF Clean Data"
    python3 oeff-reconcile.py
    python3 oeff-reconcile.py --report-dir /tmp/reports
    python3 oeff-reconcile.py --help
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime


# ── Paths (relative to CWD, overridable via CLI) ──────────────────────

DEFAULT_PATHS = {
    "warm_hosts": "oeff-warm-hosts-cleaned.csv",
    "mail_merge": "hosts-mail-merge-contacts.csv",
    "roadmap_venues": "roadmap-venue-contacts.csv",
    "timeline": "oeff-merged-timeline-airtable.csv",
    "at_venues": "airtable-import/01-venues.csv",
    "at_events": "airtable-import/03-events.csv",
    "at_intake": "airtable-import/05-host-intake.csv",
}

# ── Alias map: team-side name → Airtable name ─────────────────────────
# Hand-curated. Add entries here as new fuzzy matches appear.

VENUE_ALIASES = {
    # Values must be the NORMALIZED form of the Airtable venue name.
    # Use normalize_venue() output, not the raw Airtable name.
    "build chicago": "build inc",
    "kehrein center for the arts at urban essentials": "kehrein center for the arts at blkroom",
    "village of oak park at oprf high school": "village of oak park",
    "epiphany center for the arts": "epiphany center for the arts (said they are interested in 2026)",
}


# ── Utilities ──────────────────────────────────────────────────────────

def normalize_venue(name):
    """Lowercase, strip punctuation (except parens), collapse whitespace."""
    name = name.strip().lower()
    name = re.sub(r'[^\w\s()/-]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name


def read_csv(path):
    """Read CSV, return list of dicts. Warn on stderr if missing."""
    if not os.path.exists(path):
        print(f"WARNING: File not found: {path}", file=sys.stderr)
        return []
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def parse_inline_contacts(raw):
    """Parse 'Name <email>, Name <email>' into list of (name, email) tuples."""
    if not raw or not raw.strip():
        return []
    contacts = []
    # Match patterns like: Name <email> or just email
    for chunk in re.split(r',\s*(?=[A-Z"]|\w+@)', raw):
        chunk = chunk.strip().strip('"')
        m = re.match(r'(.+?)\s*<([^>]+)>', chunk)
        if m:
            contacts.append((m.group(1).strip().strip('"'), m.group(2).strip().lower()))
        elif '@' in chunk:
            contacts.append(('', chunk.strip().lower()))
    return contacts


def parse_date(s):
    """Try common date formats, return date or None."""
    if not s or not s.strip():
        return None
    s = s.strip()
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%Y-%m-%dT%H:%M:%S'):
        try:
            return datetime.strptime(s.split('.')[0], fmt).date()
        except ValueError:
            continue
    return None


# ── Layer 1: Venue Roster ──────────────────────────────────────────────

def reconcile_venues(roadmap_rows, at_venue_rows):
    """Compare roadmap venues (22) against Airtable venues (103+)."""
    # Build normalized lookup for Airtable venues
    at_venues = {}
    for row in at_venue_rows:
        name = row.get('Venue Name', '').strip()
        if not name or name == 'Venue Name':
            continue
        norm = normalize_venue(name)
        at_venues[norm] = name

    results = []
    roadmap_names = []
    matched_at = set()

    for row in roadmap_rows:
        team_name = row.get('Host Name', '').strip()
        if not team_name:
            continue
        roadmap_names.append(team_name)
        norm = normalize_venue(team_name)

        # Exact match
        if norm in at_venues:
            results.append({
                'team_name': team_name,
                'airtable_name': at_venues[norm],
                'match': 'exact',
                'severity': 'info',
            })
            matched_at.add(norm)
            continue

        # Alias match
        alias_norm = VENUE_ALIASES.get(norm)
        if alias_norm and alias_norm in at_venues:
            results.append({
                'team_name': team_name,
                'airtable_name': at_venues[alias_norm],
                'match': 'alias',
                'severity': 'info',
            })
            matched_at.add(alias_norm)
            continue

        # No match
        results.append({
            'team_name': team_name,
            'airtable_name': '',
            'match': 'team-only',
            'severity': 'medium',
        })

    # Airtable-only venues (not matched by any roadmap entry)
    # Only flag 2026 event venues that aren't in the roadmap
    at_only = []
    for norm, name in sorted(at_venues.items()):
        if norm not in matched_at:
            at_only.append(name)

    return results, at_only, roadmap_names


# ── Layer 2: Contact-Venue Linkage ─────────────────────────────────────

def reconcile_contacts(warm_rows, roadmap_rows, intake_rows, at_venue_rows):
    """Match contacts across warm list, roadmap, and intake."""
    findings = []

    # Build venue lookup by ID
    venue_by_id = {}
    for row in at_venue_rows:
        vid = row.get('Venue ID', '').strip()
        name = row.get('Venue Name', '').strip()
        if vid and name:
            venue_by_id[vid] = name

    # Build intake lookup by email and by venue ID
    intake_by_email = {}
    intake_by_venue_id = {}
    intake_no_venue = []
    for row in intake_rows:
        email = row.get('Contact Email', '').strip().lower()
        vid = row.get('Venue Id', '').strip()
        org = row.get('Org Name', '').strip()
        contact = row.get('Contact Name', '').strip()
        iid = row.get('Intake Id', '').strip()

        # Clean email: take only the first email if multiple
        if email:
            first_email = re.split(r'[,\s]+', email)[0].strip()
            if '@' in first_email:
                intake_by_email[first_email] = row
            else:
                first_email = ''

        if vid:
            intake_by_venue_id[vid] = row
        else:
            intake_no_venue.append({
                'intake_id': iid,
                'org': org,
                'contact': contact,
                'severity': 'high' if contact and org else 'medium',
            })

    # Warm list: check each contact against intake
    warm_emails = set()
    for row in warm_rows:
        email = row.get('Email', '').strip().lower()
        name = f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip()
        if not email:
            continue
        warm_emails.add(email)

        if email in intake_by_email:
            intake_row = intake_by_email[email]
            vid = intake_row.get('Venue Id', '').strip()
            venue_name = venue_by_id.get(vid, '(no venue)')
            findings.append({
                'type': 'warm-intake-match',
                'contact': name,
                'email': email,
                'venue': venue_name,
                'venue_id': vid,
                'severity': 'info',
            })
        else:
            findings.append({
                'type': 'warm-no-intake',
                'contact': name,
                'email': email,
                'venue': '',
                'venue_id': '',
                'severity': 'medium',
            })

    # Roadmap inline contacts: check against intake
    for row in roadmap_rows:
        venue = row.get('Host Name', '').strip()
        contacts = parse_inline_contacts(row.get('Venue Contacts', ''))
        for name, email in contacts:
            if not email:
                continue
            if email in intake_by_email:
                findings.append({
                    'type': 'roadmap-intake-match',
                    'contact': name,
                    'email': email,
                    'venue': venue,
                    'venue_id': intake_by_email[email].get('Venue Id', ''),
                    'severity': 'info',
                })
            else:
                findings.append({
                    'type': 'roadmap-no-intake',
                    'contact': name,
                    'email': email,
                    'venue': venue,
                    'venue_id': '',
                    'severity': 'medium',
                })

    # Intake-only contacts (not in warm list or roadmap)
    roadmap_emails = set()
    for row in roadmap_rows:
        for _, email in parse_inline_contacts(row.get('Venue Contacts', '')):
            if email:
                roadmap_emails.add(email)

    intake_only = []
    for email, row in intake_by_email.items():
        if email not in warm_emails and email not in roadmap_emails:
            intake_only.append({
                'contact': row.get('Contact Name', ''),
                'email': email,
                'org': row.get('Org Name', ''),
                'venue_id': row.get('Venue Id', ''),
                'severity': 'info',
            })

    return findings, intake_no_venue, intake_only


# ── Layer 3: Milestones ────────────────────────────────────────────────

def reconcile_milestones(timeline_rows, event_rows, at_venue_rows):
    """Match venue/host-related milestones to events where possible."""
    findings = []
    venue_domains = {'Venues', 'Hosts'}

    # Build venue lookup by normalized name
    venue_by_norm = {}
    for row in at_venue_rows:
        name = row.get('Venue Name', '').strip()
        if name:
            venue_by_norm[normalize_venue(name)] = name

    # Build event lookup by venue name (normalized) → list of events
    events_by_venue = defaultdict(list)
    for row in event_rows:
        vname = row.get('Venue Name', '').strip()
        if vname:
            events_by_venue[normalize_venue(vname)].append(row)

    for row in timeline_rows:
        domain = row.get('Domain', '').strip()
        planned = row.get('Planned Date', '').strip()
        status = row.get('Status', '').strip()
        milestone = row.get('Milestone', '').strip()
        mid = row.get('Milestone ID', '').strip()

        # Only venue/host domain milestones with planned dates
        if domain not in venue_domains:
            continue
        if not planned:
            continue

        planned_date = parse_date(planned)
        if not planned_date:
            continue

        # Try to link milestone text to a venue name
        linked_venue = None
        for norm_venue, venue_name in venue_by_norm.items():
            # Check if venue name appears in the milestone text
            if norm_venue in normalize_venue(milestone):
                linked_venue = venue_name
                break

        findings.append({
            'milestone_id': mid,
            'milestone': milestone,
            'domain': domain,
            'planned_date': planned,
            'status': status,
            'linked_venue': linked_venue or '',
            'severity': 'info',
        })

    return findings


# ── Layer 4: Anomalies ─────────────────────────────────────────────────

def find_anomalies(intake_rows, event_rows, at_venue_rows):
    """Cross-table consistency checks."""
    anomalies = []

    # Venue name lookup
    venue_names = set()
    venue_by_id = {}
    for row in at_venue_rows:
        vid = row.get('Venue ID', '').strip()
        name = row.get('Venue Name', '').strip()
        if vid and name:
            venue_by_id[vid] = name
            venue_names.add(normalize_venue(name))

    # Note: intake records with no Venue_Id are reported in Layer 2
    # (contact-venue linkage). Not duplicated here.

    # Event venue names not matching venues table
    for row in event_rows:
        vname = row.get('Venue Name', '').strip()
        vid = row.get('Venue ID', row.get('Venue Id', '')).strip()
        eid = row.get('Event ID', '').strip()
        year = row.get('Year', '').strip()

        if not vname or vname == 'Venue Name':
            continue

        # Check if venue name exists in venues table
        if normalize_venue(vname) not in venue_names:
            # Could be a data-only row (region marker, etc)
            # Only flag if it has an event ID
            if eid and eid.startswith('E'):
                anomalies.append({
                    'type': 'event-venue-mismatch',
                    'detail': f"{eid}: venue \"{vname}\" not in venues table",
                    'severity': 'medium',
                })

    # Pipeline status distribution
    status_counts = defaultdict(int)
    year_counts = defaultdict(int)
    for row in event_rows:
        status = row.get('Pipeline Status', '').strip()
        year = row.get('Year', '').strip()
        eid = row.get('Event ID', '').strip()
        if not eid or not eid.startswith('E'):
            continue
        if status:
            status_counts[status] += 1
        if year:
            year_counts[year] += 1

    return anomalies, dict(status_counts), dict(year_counts)


# ── Report generation ──────────────────────────────────────────────────

def generate_report(venue_results, at_only, contact_findings,
                    intake_no_venue, intake_only, milestone_findings,
                    anomalies, status_counts, year_counts, report_date):
    """Generate structured markdown report."""
    lines = []
    lines.append(f"# OEFF 2026 Reconciliation Report — {report_date}")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # ── Summary ──
    high = 0
    medium = 0
    info = 0
    for item in venue_results + contact_findings + milestone_findings + anomalies:
        sev = item.get('severity', 'info')
        if sev == 'high':
            high += 1
        elif sev == 'medium':
            medium += 1
        else:
            info += 1
    for item in intake_no_venue:
        sev = item.get('severity', 'info')
        if sev == 'high':
            high += 1
        elif sev == 'medium':
            medium += 1

    lines.append(f"**Summary: {high} high / {medium} medium / {info} info**")
    lines.append("")

    # ── Layer 1: Venue Roster ──
    lines.append("---")
    lines.append("## Layer 1: Venue Roster")
    lines.append("")
    exact = sum(1 for r in venue_results if r['match'] == 'exact')
    alias = sum(1 for r in venue_results if r['match'] == 'alias')
    team_only = sum(1 for r in venue_results if r['match'] == 'team-only')
    lines.append(f"Roadmap venues: {len(venue_results)} | "
                 f"Exact matches: {exact} | Alias matches: {alias} | "
                 f"Team-only: {team_only}")
    lines.append("")

    lines.append("| Team Name | Airtable Name | Match |")
    lines.append("|-----------|---------------|-------|")
    for r in sorted(venue_results, key=lambda x: ('exact', 'alias', 'team-only').index(x['match']) if x['match'] in ('exact', 'alias', 'team-only') else 3):
        at_name = r['airtable_name'] or '—'
        icon = {'exact': '', 'alias': ' (alias)', 'team-only': ' **TEAM-ONLY**'}[r['match']]
        lines.append(f"| {r['team_name']} | {at_name} | {r['match']}{icon} |")

    if at_only:
        lines.append("")
        lines.append(f"### Airtable-only venues ({len(at_only)} not in roadmap)")
        lines.append("")
        # Only show first 20 to keep report manageable
        for name in at_only[:20]:
            lines.append(f"- {name}")
        if len(at_only) > 20:
            lines.append(f"- ... and {len(at_only) - 20} more")

    # ── Layer 2: Contact-Venue Linkage ──
    lines.append("")
    lines.append("---")
    lines.append("## Layer 2: Contact-Venue Linkage")
    lines.append("")

    warm_match = [f for f in contact_findings if f['type'] == 'warm-intake-match']
    warm_miss = [f for f in contact_findings if f['type'] == 'warm-no-intake']
    roadmap_match = [f for f in contact_findings if f['type'] == 'roadmap-intake-match']
    roadmap_miss = [f for f in contact_findings if f['type'] == 'roadmap-no-intake']

    lines.append(f"Warm list → intake: {len(warm_match)} matched, "
                 f"{len(warm_miss)} orphaned")
    lines.append(f"Roadmap → intake: {len(roadmap_match)} matched, "
                 f"{len(roadmap_miss)} orphaned")
    lines.append(f"Intake-only contacts: {len(intake_only)}")
    lines.append("")

    if warm_miss:
        lines.append("### Warm list contacts with no intake match")
        lines.append("")
        lines.append("| Contact | Email |")
        lines.append("|---------|-------|")
        for f in warm_miss:
            lines.append(f"| {f['contact']} | {f['email']} |")
        lines.append("")

    if roadmap_miss:
        lines.append("### Roadmap contacts with no intake match")
        lines.append("")
        lines.append("| Contact | Email | Venue |")
        lines.append("|---------|-------|-------|")
        for f in roadmap_miss:
            lines.append(f"| {f['contact']} | {f['email']} | {f['venue']} |")
        lines.append("")

    if intake_no_venue:
        lines.append("### Intake records with no Venue_Id")
        lines.append("")
        lines.append("| Intake ID | Org | Contact | Severity |")
        lines.append("|-----------|-----|---------|----------|")
        for item in intake_no_venue:
            lines.append(f"| {item['intake_id']} | {item['org']} | "
                         f"{item['contact']} | {item['severity']} |")
        lines.append("")

    # ── Layer 3: Milestones ──
    lines.append("---")
    lines.append("## Layer 3: Venue/Host Milestones")
    lines.append("")
    lines.append(f"Venue/host-domain milestones with planned dates: "
                 f"{len(milestone_findings)}")
    lines.append("")

    if milestone_findings:
        lines.append("| ID | Milestone | Domain | Planned | Status | Linked Venue |")
        lines.append("|----|-----------|--------|---------|--------|--------------|")
        for f in milestone_findings[:30]:  # Cap at 30 for readability
            lines.append(f"| {f['milestone_id']} | {f['milestone'][:50]} | "
                         f"{f['domain']} | {f['planned_date']} | {f['status']} | "
                         f"{f['linked_venue'] or '—'} |")
        if len(milestone_findings) > 30:
            lines.append(f"| ... | {len(milestone_findings) - 30} more rows | | | | |")
    lines.append("")

    # ── Layer 4: Anomalies ──
    lines.append("---")
    lines.append("## Layer 4: Anomalies")
    lines.append("")

    if anomalies:
        for a in anomalies:
            sev_marker = {'high': '**HIGH**', 'medium': 'MEDIUM', 'info': 'info'}[a['severity']]
            lines.append(f"- [{sev_marker}] {a['type']}: {a['detail']}")
        lines.append("")

    lines.append("### Pipeline Status Distribution")
    lines.append("")
    if status_counts:
        lines.append("| Status | Count |")
        lines.append("|--------|-------|")
        for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {status} | {count} |")
        lines.append("")

    if year_counts:
        lines.append("### Events by Year")
        lines.append("")
        for year, count in sorted(year_counts.items()):
            lines.append(f"- {year}: {count} events")
        lines.append("")

    return '\n'.join(lines), high, medium, info


def generate_patch_csv(venue_results, contact_findings, intake_no_venue, anomalies):
    """Generate actionable discrepancy CSV."""
    rows = []

    # Venue discrepancies
    for r in venue_results:
        if r['match'] == 'team-only':
            rows.append({
                'Layer': 'Venue Roster',
                'Severity': r['severity'],
                'Type': 'team-only venue',
                'Team Value': r['team_name'],
                'Airtable Value': '',
                'Action': 'Add to Airtable or update alias map',
            })

    # Contact discrepancies
    for f in contact_findings:
        if f['type'] in ('warm-no-intake', 'roadmap-no-intake'):
            rows.append({
                'Layer': 'Contact Linkage',
                'Severity': f['severity'],
                'Type': f['type'],
                'Team Value': f"{f['contact']} <{f['email']}>",
                'Airtable Value': f.get('venue', ''),
                'Action': 'Match to intake or add intake record',
            })

    # Intake no venue
    for item in intake_no_venue:
        rows.append({
            'Layer': 'Contact Linkage',
            'Severity': item['severity'],
            'Type': 'intake-no-venue',
            'Team Value': f"{item['intake_id']}: {item['org']}",
            'Airtable Value': '',
            'Action': 'Assign Venue_Id in Airtable',
        })

    # Anomalies
    for a in anomalies:
        rows.append({
            'Layer': 'Anomalies',
            'Severity': a['severity'],
            'Type': a['type'],
            'Team Value': a['detail'],
            'Airtable Value': '',
            'Action': 'Investigate',
        })

    return rows


# ── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='OEFF 2026 weekly reconciliation — compare team-side '
                    'CSVs against Airtable exports')
    parser.add_argument('--report-dir', default='reconciliation-reports',
                        help='Output directory for reports (default: reconciliation-reports/)')
    parser.add_argument('--date', default=None,
                        help='Report date override (YYYY-MM-DD, default: today)')
    for key, default in DEFAULT_PATHS.items():
        parser.add_argument(f'--{key.replace("_", "-")}', default=default,
                            help=f'Path to {key} CSV (default: {default})')
    args = parser.parse_args()

    report_date = args.date or date.today().isoformat()

    # Resolve paths from args
    paths = {}
    for key in DEFAULT_PATHS:
        paths[key] = getattr(args, key.replace('-', '_'))

    # Read all inputs
    print(f"Reading inputs...", file=sys.stderr)
    warm = read_csv(paths['warm_hosts'])
    roadmap = read_csv(paths['roadmap_venues'])
    timeline = read_csv(paths['timeline'])
    at_venues = read_csv(paths['at_venues'])
    at_events = read_csv(paths['at_events'])
    at_intake = read_csv(paths['at_intake'])

    # Layer 1: Venue roster
    print("Layer 1: Venue roster...", file=sys.stderr)
    venue_results, at_only, roadmap_names = reconcile_venues(roadmap, at_venues)

    # Layer 2: Contact-venue linkage
    print("Layer 2: Contact-venue linkage...", file=sys.stderr)
    contact_findings, intake_no_venue, intake_only = reconcile_contacts(
        warm, roadmap, at_intake, at_venues)

    # Layer 3: Milestones
    print("Layer 3: Milestones...", file=sys.stderr)
    milestone_findings = reconcile_milestones(timeline, at_events, at_venues)

    # Layer 4: Anomalies
    print("Layer 4: Anomalies...", file=sys.stderr)
    anomalies, status_counts, year_counts = find_anomalies(
        at_intake, at_events, at_venues)

    # Generate report
    report_md, high, medium, info = generate_report(
        venue_results, at_only, contact_findings,
        intake_no_venue, intake_only, milestone_findings,
        anomalies, status_counts, year_counts, report_date)

    # Generate patch CSV
    patch_rows = generate_patch_csv(
        venue_results, contact_findings, intake_no_venue, anomalies)

    # Write outputs
    os.makedirs(args.report_dir, exist_ok=True)

    report_path = os.path.join(args.report_dir, f"reconciliation-{report_date}.md")
    with open(report_path, 'w') as f:
        f.write(report_md)

    patch_path = os.path.join(args.report_dir, f"patch-{report_date}.csv")
    if patch_rows:
        with open(patch_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'Layer', 'Severity', 'Type', 'Team Value',
                'Airtable Value', 'Action'])
            writer.writeheader()
            writer.writerows(patch_rows)

    # Summary to stdout
    print(f"{high} high / {medium} medium / {info} info — "
          f"report at {report_path}")

    # Exit code
    sys.exit(1 if (high > 0 or medium > 0) else 0)


if __name__ == '__main__':
    main()
