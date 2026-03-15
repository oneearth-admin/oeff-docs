# Prompt: OEFF Data Architecture Explorer

## Instructions

This prompt has 3 parts:
1. **Information design constraints** — established patterns to follow (not suggestions, requirements)
2. **Reference artifacts** — an HTML document (attached) and a reference image (attached) that contain all the data and the target visual direction
3. **Interactive app spec** — what to build on top of those foundations

**Attached files you must use:**
- `oeff-architecture-map.html` — the complete static HTML document with all 21 sections of architecture content. This is your data source. Preserve all content.
- `ring-diagram-reference.png` — visual reference for the concentric ring layout. Match this spatial arrangement but make it interactive and cleaner.

---

## Part 1: Information Design Constraints

These are codified, validated design patterns from a real production system. They are non-negotiable. Apply every one of them.

### Orientation First (10-Second Test)
Every view must answer two questions within 10 seconds of arrival: "What is this?" and "Is this for me?"
- The app's landing state should orient a first-time visitor before showing any complex visualization
- Even internal tools need this — context loss between sessions means every return visit is partially a first visit
- Provide a one-sentence description + recommended starting point before the ring diagram loads

### Progressive Disclosure (4 Layers)
Layer information by time-to-value:
```
Layer 0 (10 seconds): What is this? One sentence.
Layer 1 (2 minutes):  How do I use it? Quick example.
Layer 2 (10 minutes): Full reference. All options.
Layer 3 (as needed):  Design rationale. Edge cases.
```
- Hide depth, don't remove it
- A newcomer (Executive Director) should find what they need without wading through contributor-level detail (field schemas, QC status enums)
- A contributor (Technical Coordinator) should find the design rationale without it cluttering the newcomer path
- Use native `<details>/<summary>` elements for Layer 2/3 content

### Section Rhythm (5-Part Cadence)
Every section follows this consistent editorial cadence:
1. **Mono label** — uppercase, letterspaced, accent color (monospace font)
2. **Heading** — a sentence, not a label ("Your product works. Search can catch up." not "SEO Summary")
3. **Prose context** — max-width 72ch, sets up what follows
4. **Data content** — stats, tables, cards, the actual material
5. **Synthesis callout** — the "so what," not just emphasis

Consistency teaches the reader how to parse. After section one, the brain learns the pattern and stops working to decode structure.

### Layout Mode: Dashboard + Letter Hybrid
This app serves two reading patterns:
- **Dashboard mode** for the ring diagram, platform map, and timeline — scan/compare/drill-down, card-based, filterable
- **Letter mode** for the canonical sources and synthesis sections — single-column, max-width 900px, narrative context, advisor tone

Don't force everything into one mode. Let the content dictate which mode each view uses.

### Audience Calibration (4 Readers)
This app will be read by four people simultaneously:

| Role | Expertise | What They Need |
|------|-----------|---------------|
| Executive Director | Strategic, not technical. 15 years of institutional knowledge. | Big picture: what exists, what's at risk, who owns what. Will not click more than twice to find an answer. |
| Technical Coordinator | Built the system. Knows every field and script. | Architecture rationale, relationship details, handoff documentation. Wants completeness. |
| Host Comms Coordinator | Spreadsheet-fluent, 1 year in role. Created her own tracker sheets. | Where her data lives, what's automated vs manual, what she can edit. |
| Digital Communications | Eventbrite-focused, 3 years. | Ticketing integration, what feeds the newsletter, event scheduling. |

Design ONE interface that serves all four. Progressive disclosure is the mechanism — not role-based login gates.

### Data Presentation Rules
- **Numbers as display typography** — when KPIs are fewer than 10 and qualitative context matters more than quantitative precision. Large font, not charts.
- **Charts only when comparison or trend matters** — three numbers don't need a bar chart
- **72ch max-width** on body paragraphs
- **Callouts provide synthesis** — each callout names the insight and provides the "so what"
- **Shadows only on hover** — cards are bordered at rest, shadowed on interaction. Quiet until engaged.

### ADHD-Aware Design
- **No memory dependency** — every panel includes its own context. Don't assume the reader remembers what they saw in another view.
- **Resumable** — if someone switches tabs and comes back, the app state should be obvious
- **Single focus per interaction** — clicking an entity should do one clear thing, not trigger five simultaneous changes

### Navigation
- **Group navigation semantically** — not alphabetically, not by entity count
- **Landing view carries orienting weight** — headers step back
- **Commitment produces coherence** — pick one clear hierarchy and let everything cascade from it

### Anti-Patterns to Avoid
| Don't | Do Instead |
|-------|-----------|
| Flat navigation without grouping | Group semantically. Label the groups. |
| Dropping into the ring diagram without orientation | Landing view first. One sentence + "start here." |
| Charts for 3 numbers | Display typography. Large font. |
| Competing visual hierarchies | Commit to one hierarchy. |
| Wall of text with no structural landmarks | Headers, lists, white space. Let the page breathe. |
| Tooltips as the only way to access information | Tooltips supplement; panels provide. Keyboard-accessible. |
| Purple gradients | Never. This is AI slop. |

---

## Part 2: Reference Artifacts

### The Attached HTML Document (`oeff-architecture-map.html`)
This 21-section static HTML document IS the complete data source. It contains:
- Section 01: Data completeness dashboard (28 events, 19 with dates, 14 with films)
- Section 02: Team table (8 roles with data relationships)
- Section 03: Canonical sources (Kim's 2 tracker sheets with 7 tabs, OEC Active Roadmap with 16 tabs, Airtable with 16 tables)
- Section 04: Operational map (5 tables: platforms, festival cycle, role ownership, YOY persistence, centralization vs personal)
- Section 05: Ring diagram + comprehensive entity list (30+ entities across 5 layers)
- Section 06-08: v1 vs v2 comparison, 7 architecture decisions, Airtable inventory
- Section 09: Data flow pipeline (3 canonical inputs → assembly → outputs)
- Section 10-12: Host Helper schema, field ownership model, unified directory design
- Section 13: Asset + delivery tracking blueprint (5 tables with full field schemas)
- Section 14: 8 industry patterns from Codex research
- Section 15: 10 anti-patterns with mitigations
- Section 16-21: Cleanup checklist, timeline, handoff resilience, scale transitions, open questions, 24 sources

**Your job is to make this content interactive, not to rewrite it.** Extract the structured data from the HTML and build the interactive views described in Part 3.

### The Attached Reference Image (`ring-diagram-reference.png`)
This shows the target spatial layout for the concentric ring diagram:
- Center: Events (sage green circle)
- Ring 1 (inner): Master tables — Directory, Venues, Films, Sponsors, Members
- Ring 2 (middle): Relational + tracking — Assets, Deliverables, Delivery Log, Comms Log, Asset Versions, Packet QA, Host Helper 2026, Host Confirmations, Event Media Assets, Host Intake
- Ring 3 (outer): Stakeholder outputs — Host Helper Pages, Screening Packets, Filmmaker Kits, Email Campaigns
- Beyond rings: Resilience — Routing Rules, Integration Registry

Match this layout but:
- Fix the placement errors (Host Helper should be in ring 2, not ring 1; Filmmaker Kits should appear only once in ring 3)
- Make every entity interactive (hover → tooltip, click → detail panel)
- Add visible connection lines between related entities on hover
- Ensure no label overlap — distribute entities evenly around each ring

---

## Part 3: Interactive App Specification

Build a single-page React application. Use React with hooks for state management. No additional libraries beyond what AI Studio provides — no D3, no charting libraries, no UI component kits. SVG for the ring diagram, CSS for everything else.

### Visual Design
- **Palette:** Forest greens. Core: `#1a2e22` (canopy), `#3a5c4d` (deep), `#5c7c6b` (sage), `#8aaa98` (lichen), `#c8d9ce` (mist). Neutrals: `#2c2825` (ink), `#f7f5f2` (cream), `#faf9f7` (paper), `#f0ede8` (linen). Signals: `#c44b4b` (critical/high risk), `#996622` (warning/medium), `#5c8c4b` (success/low risk), `#4b7c8c` (info).
- **Typography:** System sans-serif for body. System monospace for labels and data. Large display numbers where KPI counts appear.
- **Minimum font size: 12px.** Nothing smaller, ever.
- **Minimum touch target: 44px.**
- **Border-radius minimum: 6px.** No sharp corners.
- **No pure black shadows.** Use warm-tinted: `hsla(25, 40%, 30%, 0.08)`.

### Landing State (Orientation First)
When the app loads, before the ring diagram:
- One sentence: "OEFF's data architecture — 30+ entities across 9 platforms, organized around Events as the relational hub."
- Three entry points (large clickable cards): "Explore the Architecture" (→ ring diagram), "Who Owns What" (→ role view), "Where Things Live" (→ platform map)
- Current status bar: 28 events, 19 with dates, 14 with films, 39 days to festival

### View 1: Interactive Ring Diagram (Hero)
The primary visualization. Render as SVG for precise control.

**Ring structure (from the reference image):**
- Center hub: Events (sage green filled circle, labeled)
- Ring 1 — Core (5 entities): Directory, Venues, Films, Sponsors, Members
- Ring 2 — Relational + Tracking (14 entities): Host Helper 2026, Assets, Asset Versions, Deliverables, Delivery Log, Comms Log, Host Confirmations, Host Intake, Event Media Assets, Packet QA, Webinar Content, Participants, Recordings, Merged Timeline
- Ring 3 — Stakeholder Outputs (4 entities): Host Helper Pages, Screening Packets, Filmmaker Kits, Email Campaigns
- Beyond rings — Resilience (4 entities): Routing Rules, Integration Registry, Seasons, Decision Log

**Entity cards:** White rounded rectangles with 1px border. Border color indicates layer:
- Core: `#5c7c6b` (sage)
- Relational: `#4b7c8c` (info blue)
- Output: `#8a8580` (muted)
- Resilience: `#8a8580` (muted), dashed border

**Interactions:**
- **Hover** on any entity → tooltip appears with: description (one line), platform it lives on, who owns it (by role), year-over-year or seasonal badge, handoff risk level (Low/Medium/High with color)
- **Click** on any entity → slide-in detail panel from right side showing: full description, all fields (from the HTML's schema tables), what it links to, what links to it, platform, owner, lifecycle
- **Hover** on an entity → highlight all entities it connects to with visible SVG lines/paths. Use the relationship data:
  - Directory ↔ Events, Venues, Films, Assets, Deliverables
  - Events → Venues, Films, Directory (many:many)
  - Assets ↔ Films, Events, Venues
  - Deliverables ↔ Assets (many:many), Events
  - Delivery Log → Deliverables, Directory
  - Host Helper 2026 → Events (1:1)

**Filter controls above the ring:**
- Layer filter: All | Core | Relational | Outputs | Resilience
- Platform filter: All | Airtable | Google Sheets | Eventbrite | Drive | Cloudflare
- Lifecycle filter: All | Year-over-year | Seasonal
- Risk filter: All | Low | Medium | High

When a filter is active, non-matching entities fade to 20% opacity. Matching entities stay fully visible.

### View 2: Platform Map
A card grid showing 9 platforms. Click a platform → its card expands to show all entities that live there, with role access badges.

Platforms (from section 04 of the HTML):
| Platform | Entities | Access |
|----------|----------|--------|
| Airtable | Events, Directory, Venues, Films, Sponsors, Host Helper, Deliverables, Assets, Comms Log, Host Confirmations, Webinar Content | Centralized |
| Google Sheets (Tracker) | Host-venue-film links, directory, venues, films, screenings, comms RACI, host engagements | Personal → Team |
| Google Sheets (Roadmap) | 2026HostVenues, 2026Programs, 2026EarthDayActionFair, ProgPartners + 2024-2025 archives | Centralized |
| Google Drive | Film copies, press kits, slide decks, recordings, host logos, marketing assets | Centralized |
| Eventbrite | 14+ events, access codes, tax settings, attendee data | Centralized |
| Cloudflare Pages | Host guide site | Personal infra |
| GitHub | Scripts, sync tooling, architecture decisions, host guide source | Personal infra |
| Mailchimp / Mailmeteor | 14k member list, outreach campaigns | Centralized |
| Google Forms | Host intake form, film intake survey | Centralized |

Color-code cards by access model: green border (centralized), dashed yellow border (personal → team), dashed red border (personal infra).

### View 3: Festival Cycle Timeline
Horizontal timeline with 6 phases. Click a phase → entities and platforms active during that phase highlight.

| Phase | Timeframe | Key Activity |
|-------|-----------|-------------|
| Off-season | May–Oct | Archive, tooling. Drive + GitHub active. |
| Planning | Nov–Jan | Film selection, venue outreach. Roadmap + Forms + Airtable. |
| Build-out | Feb–Mar | Everything assembled. ALL platforms active. |
| Crunch | Apr 1–21 | Schema frozen Apr 11. Data finalized, packets assembled. |
| Festival | Apr 22–27 | Read-only. Day-of edits only. |
| Wind-down | Apr 28–May | Reporting, thank-yous, season close-out. |

Currently the festival is in **Build-out** phase (39 days to festival). Highlight this phase by default.

### View 4: Role-Based Ownership
Cards for 7 roles. Click a role → highlights all entities they own/edit/consume in the ring diagram.

| Role | Creates/Owns | Edits/Maintains | Reads/Consumes |
|------|-------------|-----------------|----------------|
| Executive Director | Greenlights | Roadmap | All reporting views |
| Technical Coordinator | Scripts, schema, host guide, decisions | Events, script-owned fields, Eventbrite batch | Trackers (import source), all tables |
| Host Comms Coordinator | Tracker sheets, comms campaigns, intake | Team-editable fields, directory, venues, comms log | Host guide, Eventbrite links, packets |
| Digital Communications | Eventbrite events, newsletter, social | Ticketing, access codes | Roadmap, film/venue data |
| Creative Assets | Slide decks, video, experiential flow | Creative assets in Drive | Film copies, venue AV specs |
| Development | Sponsor relationships, grants | Sponsors table | Budget views |
| Marketing/Creative | Brand assets, social content, press | Marketing in Drive | Film metadata, venue photos |

Use three colors for the three relationship types: solid fill (owns), striped/hatched (edits), outline only (reads).

### View 5: Persistence Toggle
A toggle switch: "Year-over-year" ← → "Seasonal"

**Year-over-year** (green badge): Directory, Venues, Films, Sponsors, OEC Roadmap, Scripts, Host guide site, Architecture decisions, Seasons.

**Seasonal** (gray badge): Events, Host Helper tables, Eventbrite events, Comms campaigns, Assets/Deliverables, Kim's tracker sheets (structure persists, content is fresh).

When toggled, the ring diagram fades the non-selected entities.

### View 6: Handoff Risk Assessment
Color-code all entities and systems by handoff risk:
- **Low (green):** Centralized org accounts. Airtable, OEC Roadmap, Drive, Eventbrite.
- **Medium (yellow):** Shared from personal account. Kim's trackers, architecture decisions (git but not team-discovered).
- **High (red):** Personal machine only. Sync scripts, Cloudflare deployment, API tokens, batch scripts, email pipelines.

Synthesis callout: "Centralized platforms survive role changes. Personal infrastructure is the fragile layer. The Integration Registry makes personal infra legible — not centralized overnight, but documented so a successor can find it."

### View 7: Canonical Sources (Always Visible)
Not a tab — a persistent callout panel (collapsible but open by default) showing:

1. **Host Comms Coordinator's Tracker Sheets** — "Process knowledge in spreadsheet form."
   - Sheet 1 (5 tabs): Host-Venue-Film Link, Directory, Venues (56 cols), Films, Screenings (35 cols)
   - Sheet 2 (2 tabs): Host Communications (RACI ownership), Host Engagements
   - Why it matters: "Built while doing the work. Structure reflects operational reality."

2. **OEC Active Roadmap** — "The team's working document."
   - 16 tabs spanning 2024–2026
   - Key 2026 tabs: HostVenues (31 cols), Programs (43 cols), EarthDayActionFair (30 cols)
   - Why it matters: "What the team actually references in meetings."

3. **Airtable** — "Relational infrastructure."
   - 16 active tables
   - Why it matters: "Links between entities that spreadsheets can't express."

**Dual-canonical principle:** "Tracker sheets for validated operational data. Roadmap for team-facing planning. Airtable for relational structure. Sync scripts bridge them."

### View 8: Data Flow Animation
An animated flow showing how data moves through the system:

```
Tracker Sheets (5 tabs) ──→ Directory + Venues + Films
OEC Active Roadmap ──→ Events
Comms Tracker (2 tabs) ──→ Comms Log + Deliverables
          ↓
Events + master tables ──→ [assemble-host-helper.py] ──→ Host Helper 2026
          ↓
Host Helper 2026 ──→ Interface Designer ──→ Host-facing pages
Host Helper 2026 ──→ Mailmeteor ──→ Outreach campaigns
```

Animate with dots flowing along the paths. Click any node to see its detail panel.

### Cross-View Linking
**This is critical:** All views should be linked. When you click an entity in any view, it should highlight in ALL views simultaneously:
- Click "Assets" in the ring → the platform map highlights Airtable, the timeline highlights Build-out + Crunch, the role view highlights Technical Coordinator (owns) and Host Comms Coordinator (reads), the persistence view shows Seasonal, the risk view shows Low.

### Keyboard Navigation
- Tab through entities in the ring diagram
- Arrow keys to move between rings
- Enter to open detail panel
- Escape to close panel
- `1`-`8` to switch between views

---

## Context

- **OEFF** = One Earth Film Festival, a 6-day community film festival in Chicago
- **Festival dates:** April 22–27, 2026 (~39 days away)
- **Scale:** ~30 events, ~22 venues, ~16 films
- **Team:** Small contractor-based (no full-time tech staff)
- **Architecture goal:** Survive turnover — if any person leaves, the system is discoverable
- **This visualization is FOR the team** — to understand their own system
- The feel should be **inviting rather than intimidating**. Think museum exhibit, not database admin panel.
