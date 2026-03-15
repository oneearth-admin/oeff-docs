# Design Philosophy Refinement — OEFF Architecture Explorer

Apply these principles to the current build. These are not suggestions — they are the design philosophy this tool is built on. Every change should pass the test: "did someone care about this being understood?"

## 1. Cognitive Restoration, Not Cognitive Load

This tool should feel like a clearing in a forest, not a cockpit. The user's attention is a finite resource — the interface should restore it, not deplete it.

**Concrete changes:**
- Background must be warm cream (#f7f5f2), not dark/gray
- White space is a structural element, not empty space. Add generous padding between the ring diagram and any surrounding content. The ring should breathe.
- Remove all decorative elements that don't carry information. No badges that say "LIVE", no version numbers in the header, no "ID" tags.
- The ring diagram's circles should use soft, muted fills — not hard-edged geometric rings. Think watercolor washes, not engineering diagrams.
- Hover states should be gentle transitions (200ms ease), not instant snaps

## 2. Progressive Disclosure — Four Layers of Depth

Layer 0 (10 seconds): "OEFF's data architecture — 30 entities across 9 platforms, organized around Events as the hub." One sentence. Three clickable entry points below it.

Layer 1 (2 minutes): The ring diagram with labeled entities. Hover any entity → one-line tooltip. This is where most people stop.

Layer 2 (10 minutes): Click an entity → slide-in detail panel with full description, fields, relationships, platform, owner. The detail panel should carry its own context — don't assume the reader remembers what ring the entity was in.

Layer 3 (as needed): Expand sections within the detail panel for field schemas, QC status enums, migration notes. Use native `<details>/<summary>` elements. Hidden by default.

**The critical rule:** A newcomer (the Executive Director, 15 years of institutional knowledge but not technical) should find what she needs at Layer 0-1. The Technical Coordinator should find architecture rationale at Layer 2-3. ONE interface, not two.

## 3. ADHD-Aware Design

- **No memory dependency.** The detail panel must restate which ring/layer the entity belongs to, what it connects to, and who owns it. Don't assume the user remembers what they just looked at.
- **Resumable.** If someone switches browser tabs and comes back, the app state should be visually obvious — what's selected, what view they're in.
- **Single focus per interaction.** Clicking an entity does ONE thing: opens its detail panel. Don't simultaneously change the ring highlighting AND filter the platform view AND scroll to something.
- **Visual landmarks.** The tab navigation should always be visible. The currently active tab should be obvious. The ring diagram should be reachable from any view without scrolling.

## 4. Warmth Through Restraint

- **No marketing copy.** Remove "Data Visualization Tool", "Internal Architecture Map V1.2", "System Overview". The header should say "OEFF Architecture" and "One Earth Film Festival" and nothing else.
- **No explaining the tool to itself.** Remove "Select an entity to explore its role and dependencies." The interaction should be self-evident from the design. If it needs instructions, the design is wrong.
- **Headings should be sentences, not labels.** Not "System Overview" but "Everything connects through Events" or even just remove the heading and let the diagram speak.
- **The synthesis pattern.** Where text appears (detail panels, section descriptions), end with the "so what" — why this entity matters, not just what it contains. Example: "Delivery Log — who got what, when. Without this, post-festival filmmaker reports require manual email archaeology."

## 5. Play and Discovery

- **Hover should reward curiosity.** When hovering an entity, show faint SVG connection lines to everything it links to. These lines should fade in gently, not appear instantly. The user should feel like they're discovering relationships, not being shown a diagram.
- **The ring should be explorable.** Entities in the outer rings should subtly pulse or breathe (very subtle opacity animation, 0.97-1.0 over 4s) to suggest they're interactive. Not gamification — invitation.
- **Surprising connections matter most.** The relationship between Directory and Events is obvious. The relationship between Assets and Films AND Events AND Venues simultaneously — that's the interesting one. Connection lines for many-to-many relationships should use a different visual treatment (wider, or colored differently) than obvious one-to-many links.
- **Click history.** Subtly dim entities the user has already explored (opacity 0.85 vs 1.0). This gives a sense of progress without gamification.

## 6. Section Rhythm (for any text-heavy views)

If the platform map, timeline, or role views use text sections, each section follows this cadence:
1. Mono label — uppercase, letterspaced, forest green
2. Heading — a sentence, not a label
3. Prose context — max-width 72ch, one paragraph setting up what follows
4. Data content — the actual material (table, card grid, timeline)
5. Synthesis callout — the "so what" in a visually distinct block

## 7. The Ring Diagram Specifically

- The center "Events" hub should feel like gravity — everything radiates from it
- Ring bands should have subtle texture or variation, not flat solid fills. Even a 2% opacity noise pattern makes it feel organic rather than mechanical.
- Entity labels should use a monospace font at 12-13px. Core entities slightly larger/bolder than outer ring entities.
- Connection lines on hover should be curved (bezier), not straight. Straight lines feel like a database schema. Curved lines feel like a living system.
- The legend should be minimal — three colored dots with one-word labels (Core, Relational, Outputs, Resilience), tucked in a corner, not a separate section.

## 8. Color Psychology

The forest palette isn't arbitrary:
- Sage green (#5c7c6b) for core entities — grounded, stable, persistent
- Teal (#4b7c8c) for relational entities — flowing, connecting, in-motion
- Muted gray (#8a8580) for outputs and resilience — these are downstream, derived, supportive
- Cream (#f7f5f2) background — warm, papery, not clinical
- No pure black anywhere. Darkest text is #2c2825 (warm ink).
- No pure white backgrounds on cards. Use #faf9f7 (paper) or #ffffff only on hover-raised states.

## What Success Looks Like

Someone from the OEFF team opens this tool for the first time. Within 10 seconds they understand it's a map of their data system. Within 2 minutes they've hovered a few entities and understand the ring structure. They click "Host Helper 2026" because that's what they work in daily — and the detail panel tells them not just what fields it has, but why it exists ("script-assembled flat table that replaced the 3-layer rollup chain Kim couldn't edit"). They feel oriented, not overwhelmed. They leave knowing slightly more about how their own system works than when they arrived.

That's the test. Not "is the SVG rendering correctly" — "does a real person at a real nonprofit feel like someone cared about helping them understand their own work?"
