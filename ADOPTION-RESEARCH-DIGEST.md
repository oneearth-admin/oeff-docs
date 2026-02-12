# OEFF Airtable Migration — Adoption Research Digest

**Date:** 2026-02-11 (updated 2026-02-12)
**Source:** 3-agent parallel research (case studies, failure modes, onboarding strategies)
**Context:** OEFF is a Chicago film festival (~30 events, ~100 venues, 5-person team) migrating from a 33-sheet Excel workbook to an 11-table Airtable base with 739 records across CSVs.

---

## 1. Case Studies — What Similar Orgs Actually Did

### Direct Film Festival Parallel

**DC Shorts Film Festival / FestRunner (Jon Gann)** — The closest match. Gann migrated from "dozens and dozens of Google sheets" to Airtable, then built FestRunner — a reusable film festival template (public on Airtable Universe). Two main bases: SUBMISSIONS and EVENTS. Tables for: people, venues, shows/events, hospitality, sponsors, print traffic, shipping, marketing, press. He built role-specific views for press, social media, designers, and sponsors from a single base. His core insight: film festival data is *inherently relational* — films link to venues, sponsors, reviewers, press — making spreadsheets particularly inadequate. The Film Festival Alliance itself uses Airtable as part of their tech stack.

FestRunner's table structure (venues, shows, films, people, sponsors) is nearly 1:1 with OEFF's 11-table schema. This is the structural template to study.

### Case Study Summary Table

| Organization | Size | Old System | Migration Trigger | Time to "Normal" |
|---|---|---|---|---|
| **DC Shorts / FestRunner** | 1-5 staff | Dozens of Google Sheets | Relational data impossible in sheets | Templates now public |
| **She's the First** | 5 staff, 200+ chapters | Google Docs | "Nightmare" cross-referencing | 1-2 years incremental |
| **James Beard Foundation** | Small program team | 15+ tab Google Sheet with inconsistent naming/color-coding | Manual copy-paste, stakeholder confusion | Scaled 65 to 600 restaurants in 2.5 years |
| **ScholarMatch** | Small, no tech person | Messy shared Word docs | Growth from 39 to 600+ students | ~2-3 years to full maturity |
| **Mingei Museum** | Lean resources | Outdated desktop-only DB | 26,000-object collection move | Faster than expected |
| **Startup Grind** | Small events team | Spreadsheets + docs | Speaker/agenda/venue coordination across 600+ chapters | Immediately productive |
| **Sound Water Stewards** | Volunteer-driven | Single-person database | Previous DB owner passed away — institutional knowledge lost | Rebuilt as recovery project |
| **Insomniac Events (EDC)** | Festival crew | Excel then Google Docs | 1,000+ lost items per event | Iterative, show by show |
| **Allied Concert Services** | ~135 venue associations | Spreadsheets + paper | Scattered artist/venue/audience data | Ongoing with consultant |

### Key Case Details

**James Beard Foundation** — The 15-tab spreadsheet cautionary tale. Their old system had "inconsistent naming conventions, color codes, and highlighting" — the color-coding was one person's mental model, not a shared system. Sound familiar? OEFF's 33-sheet workbook has the same risk. After migration: "We're able to focus more on the educational piece — talking to chefs, rather than copy-and-pasting stuff from spreadsheets." Automated text reminders to chefs increased engagement more than email. Forms let non-desk workers (chefs working odd hours) enter data directly.

**She's the First** — Exact team size match (5 people managing 200+ chapters). Started with the Airtable Nonprofit Gala template and customized it. Expanded organically to intern hiring, mentor inquiries, chapter tracking. Key quote: "There's a lot of hesitation in older nonprofits to learn new stuff." But: "It is so worth learning Airtable...every minute is money."

**Startup Grind** — Best events model parallel. Forms for speaker data collection (headshots, bios auto-populate). Linked records connecting speakers to agenda/scheduling. Shared view links for external access (attendees see schedules without seeing internal data). Their events coordinator called the tables "kind of my bible." This speaker/agenda/venue model maps directly to OEFF's films/screenings/venues.

**Sound Water Stewards** — The bus-factor cautionary tale. When their previous database owner passed away, the organization lost critical institutional knowledge. The Airtable rebuild was a recovery project. Direct warning for OEFF: if the 33-sheet workbook is primarily understood by one person, migration is an opportunity to distribute that knowledge — or a risk of concentrating it further.

### Cross-Cutting Patterns

**What consistently works:**
1. Start with the spreadsheet interface ("everybody knows what it is" — Mingei Museum)
2. Pick ONE pain point first, not all 33 sheets (ScholarMatch started with just donor tracking)
3. Linked records are the breakthrough moment — explicitly teach it
4. Organic expansion follows: teams discover new uses on their own after the first win
5. Mobile/tablet access is critical for field work (museum storage rooms, festival grounds, venue visits)
6. Visual feedback loops build confidence (weekly progress charts, improving return rates)
7. Forms are the gateway drug — let external stakeholders (hosts, filmmakers, volunteers) enter data directly
8. Views replace tab proliferation — instead of duplicating data across tabs, create filtered views of one dataset
9. Templates as starting points lower the design burden (She's the First used Nonprofit Gala template; FestRunner is public)

**What consistently doesn't work:**
1. Building it without leadership involvement from day one
2. One-time training with no follow-up
3. Trying to migrate everything at once
4. Skipping 30-60 day check-ins post-launch
5. Color-coding as a knowledge system — it's one person's mental model, not shared understanding

**Timeline pattern:** 3-6 months for core comfort, 12-18 months for full ecosystem maturity. No org went from spreadsheets to full Airtable adoption overnight.

**Pricing note:** Nonprofits registered with TechSoup get 50% off Airtable Plus or Pro plans. OEFF should confirm TechSoup registration before committing.

---

## 2. Failure Modes — The 9 Ways This Dies

Research identified 9 named failure patterns. Three are rated **CRITICAL** for OEFF's specific situation.

### CRITICAL for OEFF

| # | Pattern | How It Manifests | OEFF Risk |
|---|---------|-----------------|-----------|
| 1 | **Over-Engineering** | Schema too complex for actual use. 11 tables with 32-column events CSV for 893 records may be more structure than a 5-person team can sustain. | HIGH — schema v1.1 added 14 fields to Events. Ask: will anyone actually fill in "License Invoice Received"? |
| 2 | **Data Champion Leaves** | One person holds all the knowledge. When they move on, the system becomes a black box. | HIGH — Garen is the sole technical coordinator, now distributed contractor. If engagement shifts, who maintains the base? |
| 3 | **Perpetual Pre-Launch** | Extensive planning, schema design, CSV prep, audit checklists — but no live Airtable base yet. Planning becomes a substitute for shipping. | HIGH — 11 CSVs ready, schema at v1.1, audit mostly resolved, but zero records in Airtable. |

### ELEVATED for OEFF

| # | Pattern | How It Manifests |
|---|---------|-----------------|
| 4 | **Shadow Spreadsheet** | Team keeps using the old Excel alongside Airtable "just in case." Dual systems = double work = abandonment of new system. |
| 5 | **Field of Dreams** | "Build it and they won't come." Technical excellence doesn't create adoption. The base needs to solve a pain point the team *already feels*. |
| 6 | **One-and-Done Demo** | Single training session, then silence. Knowledge decays in days without reinforcement. |

### MODERATE for OEFF

| # | Pattern | How It Manifests |
|---|---------|-----------------|
| 7 | **Desk-Bound Data** | System designed for laptop use but team works from phones at venues. No mobile-first views = no adoption in the field. |
| 8 | **Access Paradox** | Too locked down kills adoption; too open creates chaos. Need role-based views, not just permissions. |
| 9 | **Free Tier Trap** | Airtable free tier limits (1,000 records/base, 1GB attachments) force paid upgrade before team sees value. |

### Mitigation Strategies

For each critical pattern:

**Over-Engineering** → Audit every field: "Will someone enter this data within 30 days of go-live?" If not, hide it. Start with 4-5 core tables, add the rest later.

**Data Champion Leaves** → Document the "why" not just the "how." Record a 15-minute Loom walkthrough of the base structure. Make Ana (ED) a co-owner of the base, not just a viewer.

**Perpetual Pre-Launch** → Set a ship date. Import the foundation tables (Venues, Films) this week. Imperfect and live beats perfect and theoretical.

---

## 3. Onboarding Strategies — Making It Stick

### The 11 Strategies That Work

Ranked by effort-to-impact for OEFF's context:

#### Low Effort, High Impact

1. **Role-Based Interfaces** — Each person sees only their view. Ana sees the dashboard. Film coordinator sees film contacts and scheduling. Volunteer coordinator sees events and participant counts. Hide the 32-column complexity behind 5-8 column views.

2. **Pain-Point Framing** — Don't say "we're migrating to Airtable." Say "remember when we couldn't find Cultivate Collective's contact? That's fixed now." Connect every feature to a pain they've already felt.

3. **Quick Reference Cards** — One-page PDF per role: "How to look up a venue," "How to add a sponsor." Laminated, taped to desk. Not a training manual — a cheat sheet.

4. **Loom Videos** — 2-3 minute screen recordings for the 5 most common tasks. Async, rewatchable, zero scheduling overhead. "How to check which films are confirmed" not "Introduction to Airtable."

#### Medium Effort, High Impact

5. **Champion Model** — One team member becomes the go-to person (beyond Garen). Best candidate: whoever currently maintains the Excel workbook most actively. They get extra training and become the "ask me" person.

6. **Graduated Rollout** — Week 1: read-only access, explore the data. Week 2: edit their own records. Week 3: create new records. Week 4: full access. Don't hand someone 11 tables on day one.

7. **Mobile-First for Festival Week** — Design Airtable views specifically for phone use during the festival. Big text, few columns, tap-to-call on contact fields. This is where adoption either proves its value or breaks.

#### Medium Effort, Medium Impact

8. **Training vs. Adoption** — Training is a one-time event ("here's how Airtable works"). Adoption is behavior change ("I check Airtable before texting Ana for venue info"). Plan for adoption, not just training.

9. **Dual-Running Period** — Keep Excel accessible (read-only) for 4-6 weeks while Airtable becomes primary. Don't delete the old system cold turkey. But set a sunset date.

10. **Ongoing Cadences** — 15-minute weekly check-in for the first month: "What confused you? What couldn't you find?" Adjust views based on real friction, not assumptions.

11. **Push vs. Pull** — Some updates should be pushed (automated email when a film status changes). Some should be pulled (team member opens Airtable to check schedule). Design for both, but start with push — it builds the habit of trusting the system.

### Recommended OEFF Adoption Timeline

| Week | Action | Who |
|---|---|---|
| **Week 0** | Import foundation tables (Venues, Films). Create role-based views. Record 3 Loom walkthroughs. | Garen |
| **Week 1** | Read-only access for team. "Explore the data, flag what looks wrong." | All 5 |
| **Week 2** | Edit access. Quick reference cards distributed. First 15-min check-in. | All 5 |
| **Week 3** | Import remaining tables. Team starts entering new data in Airtable (not Excel). | All 5 |
| **Week 4** | Full access. Excel moved to read-only archive. Second check-in. | All 5 |
| **Week 6** | 30-day retrospective. What's working? What views need adjustment? | All 5 |
| **Week 8** | Excel archive access removed. Airtable is the single source of truth. Champion identified. | Garen + Champion |
| **Festival Week** | Mobile views deployed. Real-time data entry during events. | All |
| **Post-Festival** | Retrospective: Did Airtable help during the festival? What broke? Iterate for next cycle. | All 5 |

---

## 4. Synthesis — The Three Things That Matter Most

After reviewing 8 case studies, 9 failure modes, and 11 onboarding strategies, three principles emerge:

### A. Ship Before It's Perfect

The biggest risk isn't a missing field — it's never going live. OEFF has 11 CSVs, a v1.1 schema, and a resolved audit checklist. The technical work is essentially done. The next action is importing Venues and Films into a real Airtable base, not adding more columns.

Every case study that succeeded started smaller than they planned. ScholarMatch started with donor tracking, not their whole operation. Mingei started with one collection move, not their entire catalog system. OEFF should start with Venues + Films + Events, not all 11 tables.

### B. Make It About Their Pain, Not Your Schema

Nobody on the OEFF team woke up wanting a relational database. They woke up unable to find Cultivate Collective's AV contact, or confused about which film is screening where on April 24th. The schema exists to solve those problems. Every training touchpoint, every view name, every Loom video should connect to a pain point the team already experiences.

"Check the Events table" means nothing. "Look up your venue's film assignment" means everything.

### C. Plan for Life After Garen

The Data Champion Leaves pattern is OEFF's most existential risk. Garen built the schema, cleaned the data, resolved the audit issues, and is the only person who understands the table relationships. If Garen's engagement changes, the system dies unless:

- Ana (ED) can explain *why* the base is structured the way it is
- At least one other team member can add/edit records confidently
- The base has embedded documentation (field descriptions, view descriptions)
- A 15-minute Loom walkthrough of the base structure exists

This isn't about succession planning — it's about distributed ownership from day one.

---

## 5. Recommended Next Actions

**This week:**
1. Create the Airtable base. Import 01-venues.csv and 02-films.csv (Phase 1 foundation tables)
2. Create 3 role-based views in Events table (Film Coordinator, Venue Coordinator, Overview)
3. Record a 3-minute Loom: "Here's where OEFF data lives now"

**Next week:**
4. Import 03-events.csv and link to Venues/Films tables
5. Give team read-only access. Ask: "Does this look right?"
6. Create quick reference card for the most common lookup task

**Before festival:**
7. Import remaining tables (sponsors, contacts, media, etc.)
8. Build mobile-optimized views for festival week operations
9. Run a 15-minute "find this info" exercise with the team
10. Identify the champion (who's most comfortable? who asks the best questions?)

---

## Sources

### Case Studies
- BuiltOnAir: [Using Airtable for Film Festivals](https://builtonair.com/winter-series-using-airtable-for-film-festivals/) (DC Shorts)
- Airtable Blog: [ScholarMatch](https://blog.airtable.com/students-meet-your-match-how-scholarmatch-made-airtable-work-for-them-part-one/), [Mingei Museum](https://blog.airtable.com/how-mingei-international-museum-moved-26000-pieces-of-art/), [She's the First](https://blog.airtable.com/building-a-nonprofit-program-management-system-with-airtable/), [Insomniac Events](https://blog.airtable.com/how-insomniac-events-is-transforming-customer-experience-operations/), [James Beard Foundation](https://www.airtable.com/customer-stories/james-beard-foundation)
- ProsperSpark: [Allied Concert Services](https://www.prosperspark.com/case-study-event-management/)
- Nugget Newspaper: [Citizens4Community](https://www.nuggetnews.com/story/2025/10/08/business/navigating-spaces-in-sisters-made-easier/38267.html)

### Failure Modes & Change Management
- NonProfit PRO: [Breaking Through Resistance to Change](https://www.nonprofitpro.com/article/4-strategies-for-breaking-through-resistance-to-change-in-nonprofit-tech-projects/)
- Roundtable Technology: [Change Management Strategies for Tech Adoption](https://www.roundtabletechnology.com/blog/effective-change-management-strategies-for-tech-adoption-in-nonprofits)
- Datafold: [What Data Practitioners Wish They Knew](https://www.datafold.com/data-migration-guide/what-data-practitioners-wish-they-knew)
- NTEN, TechSoup, Idealware practitioner literature
- Airtable Community forums and Reddit threads on failed migrations

### Onboarding & Adoption
- UX research on enterprise tool adoption at small scale
- Nonprofit digital capacity building literature (NTEN, TechSoup, Capacity Commons)
- Practitioner blogs on Airtable/Notion onboarding
- Change management literature adapted for small orgs
