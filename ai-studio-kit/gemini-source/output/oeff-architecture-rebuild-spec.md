# OEFF Architecture Explorer Rebuild Spec

## Purpose

Rebuild the OEFF Architecture Explorer as a single-file vanilla HTML document with inline CSS and JavaScript. The rebuild must preserve the full information architecture of the React/Vite source while translating the interface into Beautiful-First conventions: warm paper surfaces, Forest palette semantics, inspectable SVG, restrained motion, and document-like clarity.

This spec is derived from:

- `src/data.ts`
- `src/App.tsx`
- `src/components/RingDiagram.tsx`
- `src/components/DataFlowView.tsx`
- `src/components/EvolutionView.tsx`
- `src/index.css`
- `oeff-architecture-explorer.html`
- `design-philosophy-prompt.md`
- `~/claude-ecosystem/skills/design-core/VOCABULARY.md`

## Build Constraints

- Single-file `oeff-architecture-explorer.html`
- No React, no Tailwind, no Framer Motion, no Lucide, no npm, no build step
- Inline the data from `oeff-architecture-data.json` inside a `<script type="application/json" id="oeff-data">` block
- Use semantic HTML landmarks: `header`, `nav`, `main`, `section`, `aside`, `footer`
- Use inline SVG for the ring diagram and any icons that remain
- Include reduced-motion handling and print-friendly detail panel styling
- Replace dependency icons with inline SVG or simple text marks

## Global Shell

- Background: warm cream paper, not white, not gray, not dark
- Header content: only `OEFF Architecture` and `One Earth Film Festival`
- Page width: centered container around 1100-1150px max width with generous horizontal padding
- Navigation: always visible near the top; make it sticky in the rebuild even though the React build is static
- Main interaction state:
  - active tab
  - selected entity
  - hovered entity for connection-line rendering
- Global keyboard:
  - `1` = `DIAGRAM`
  - `2` = `PLATFORMS`
  - `3` = `TIMELINE`
  - `4` = `ROLES`
  - `5` = `RISK`
  - `6` = `DECISIONS`
  - `7` = `FLOW`
  - `8` = `EVOLUTION`
  - `Escape` closes the detail panel

## 1. View Inventory

### View 1: `DIAGRAM`

- What it shows:
  - The concentric ring diagram centered on `Events`
  - The headline `Everything connects through Events`
  - Four stacked layer sections under the diagram
  - Entity cards grouped by `type`
- Layout structure:
  - Centered SVG hero, 380px square on desktop
  - Minimal legend under or tucked into the lower corner of the ring
  - Four full-width stacked sections in this exact order:
    - `Core`
    - `Relational + Tracking`
    - `Stakeholder Outputs`
    - `Resilience`
  - Each section contains wrapped entity cards
- Interactive behaviors:
  - Hover an entity card: show a curved connection line from card center to the corresponding ring band
  - Click an entity card: open the detail panel
  - If a detail panel is already open, clicking another entity swaps the content in place
  - Selected card should visibly remain selected
- Data sources:
  - `entities`
  - group by `type`
  - derive ring target from `ring`
- Keyboard shortcut:
  - `1`

### View 2: `PLATFORMS`

- What it shows:
  - One card per platform
  - Platform name plus access classification
- Layout structure:
  - Responsive grid
  - 1 column mobile, 2 columns tablet, 3 columns desktop
  - Each card centered and text-only
- Interactive behaviors:
  - Hover elevation only
  - No deep linking in the React build; preserve that unless you add optional grouping by entity
- Data sources:
  - `platforms`
- Keyboard shortcut:
  - `2`

### View 3: `TIMELINE`

- What it shows:
  - The six seasonal phases of OEFF work
  - One phase marked as current
- Layout structure:
  - Six-column row on desktop
  - Stacked cards on mobile
  - Each card shows period, phase name, and optional `Current` badge
- Interactive behaviors:
  - No click behavior required
  - Current phase receives stronger border, background, and ring highlight
- Data sources:
  - `timeline`
- Keyboard shortcut:
  - `3`

### View 4: `ROLES`

- What it shows:
  - Seven role cards
  - Each role split into `Creates`, `Edits`, and `Reads`
- Layout structure:
  - Two-column grid on desktop, one column on mobile
  - Each card has a display heading and three chip groups beneath it
- Interactive behaviors:
  - Hover elevation only
  - No modal behavior
- Data sources:
  - `roles`
- Keyboard shortcut:
  - `4`

### View 5: `RISK`

- What it shows:
  - One high-level quote about fragility
  - Three columns of entity pills grouped by risk level
- Layout structure:
  - Intro quote centered above
  - Three columns ordered exactly:
    - `High Risk`
    - `Medium Risk`
    - `Low Risk`
  - Each column contains pill buttons for matching entities
- Interactive behaviors:
  - Clicking a pill switches back to the `DIAGRAM` tab and opens that entity in the detail panel
- Data sources:
  - `entities`
  - group by `risk`
- Keyboard shortcut:
  - `5`

### View 6: `DECISIONS`

- What it shows:
  - The architecture decision record set
  - A heading framing the session as `The March 13, 2026 Strategy Session`
  - Seven decision cards
  - A synthesis footer callout
- Layout structure:
  - Centered header block
  - Two-column card grid on desktop, one column on mobile
  - Full-width synthesis block at bottom
- Interactive behaviors:
  - Card hover only; no modal
  - Quotes appear only when `quote` exists
- Data sources:
  - `decisions`
- Keyboard shortcut:
  - `6`

### View 7: `FLOW`

- What it shows:
  - The downhill pipeline from source sheets to flat outputs
  - Three inputs, one assembly step, two outputs
  - Two explanatory callouts below
- Layout structure:
  - Centered header block
  - Vertical flow with arrow separators between sections
  - Inputs as a three-card grid
  - Assembly as one centered card
  - Outputs as a two-card grid
  - Two callout cards below the pipeline
- Interactive behaviors:
  - Hover elevation only
  - No selection state required
- Data sources:
  - `dataFlow`
- Keyboard shortcut:
  - `7`

### View 8: `EVOLUTION`

- What it shows:
  - A side-by-side v1 vs v2 comparison
  - Eight aligned comparison rows
  - One synthesis callout explaining the main tradeoff
- Layout structure:
  - Centered header
  - Three-column comparison grid:
    - column 1 = dimension labels
    - column 2 = v1
    - column 3 = v2
  - Full-width synthesis card below
- Interactive behaviors:
  - Static comparison
  - Hover emphasis optional but not necessary
- Data sources:
  - `evolution`
- Keyboard shortcut:
  - `8`

## 2. Component Catalog

### App Header

- Title: `OEFF Architecture`
- Subtitle: `One Earth Film Festival`
- Styling:
  - Fraunces display heading
  - Source Code Pro small uppercase subtitle
  - bottom border in forest-sage
- Do not add version labels, marketing copy, or helper text

### Tab Navigation

- Exact labels:
  - `DIAGRAM`
  - `PLATFORMS`
  - `TIMELINE`
  - `ROLES`
  - `RISK`
  - `DECISIONS`
  - `FLOW`
  - `EVOLUTION`
- Visual treatment:
  - mono uppercase, letterspaced
  - 2px underline for active tab
  - minimum 44px tap target
  - wrap on small screens
- Behavior:
  - click changes tab
  - number keys `1-8` change tab
  - active tab state must remain obvious after returning to the page

### Ring Diagram

- Rendering method:
  - inline SVG
  - `viewBox="0 0 400 400"`
  - element id: `ring-diagram-svg`
- Geometry:
  - center at `200,200`
  - five concentric circles with radii `40`, `80`, `120`, `160`, `200`
  - render from outside in for clean overlaps
- Circle fills from current source:
  - center `Events`: `#c8d9ce`
  - Core band: `#dce8e0`
  - Relational band: `#e8e3dd`
  - Outputs band: `#f0ede8`
  - Resilience band: `#f5f3f0`
- Ring stroke:
  - `#1a3a32`
  - `0.5px`
  - `0.1` opacity
- Text:
  - center label `Events` at `x=200`, `y=205`
  - band labels centered at top:
    - `Core` at `y=155`
    - `Relational` at `y=115`
    - `Outputs` at `y=75`
    - `Resilience` at `y=35`
- Animation:
  - outermost ring only
  - 8s ease-in-out infinite
  - oscillate `rotate(0deg)` to `rotate(0.5deg)` and back
  - disable in `prefers-reduced-motion`
- Rebuild improvement:
  - keep SVG inspectable and printable
  - add very light texture or tonal variation to ring fills so they feel organic rather than flat

### Diagram Legend

- Minimal legend with four dots and one-word labels:
  - `Core`
  - `Relational`
  - `Outputs`
  - `Resilience`
- Do not treat legend as a separate major section
- Tuck it under the ring or into a lower corner of the hero

### Entity Card

- Content:
  - entity label
  - one-line description
- Desktop size:
  - max width roughly `200-220px`
  - full width within its lane on mobile
- Visual treatment:
  - white or paper-raised surface
  - warm border
  - rounded corners at least `8px`, preferably `12px`
  - compact spacing; the Gemini build is too loose vertically
  - add a left border keyed by type in the rebuild
- Left border colors:
  - Core: forest green
  - Relational: teal
  - Outputs: ochre/amber
  - Resilience: muted gray
- Typography:
  - label: Source Sans 3 semibold, about `15px`
  - description: Source Serif 4, about `13px`
- Hover behavior:
  - border strengthens
  - warm shadow increases
  - slight lift of `1-2px`
  - matching connection line appears on the ring
- Selected behavior:
  - border and shadow remain active while detail panel is open

### Layer Section

- One wrapper per entity type
- Backgrounds:
  - Core band section = green-tinted paper
  - Relational section = warm neutral with teal cast
  - Outputs section = linen/amber cast
  - Resilience section = pale paper with muted gray tone
- Section labels:
  - italic display style
  - exact text:
    - `Core`
    - `Relational + Tracking`
    - `Stakeholder Outputs`
    - `Resilience`
- Resilience section:
  - `3px` dashed left border
  - muted gray

### Detail Panel

- Container:
  - fixed right-side `aside`
  - width `min(480px, 92vw)`
  - full height
  - scrollable
  - paper-raised background
  - strong warm shadow
- Open/close:
  - slide in from the right
  - scrim behind panel
  - close via `X`, scrim click, or `Escape`
  - trap focus while open
  - lock body scroll while open
- Header content order:
  - type/layer marker
  - entity title
  - synthesis paragraph
  - badge row
- Badge row:
  - type
  - platform
  - lifecycle
  - risk
  - optional field count
- Sections inside panel:
  - `Ownership`
  - `Data Flow`
  - `Field Schema`
  - `Related Entities`
- Ownership section:
  - three-column or stacked definition layout for `Creates`, `Edits`, `Reads`
  - optional `notes` paragraph below in serif italic
- Data Flow section:
  - inbound block, arrow, outbound block
  - if absent, omit entire section
- Field Schema section:
  - native `<details>` / `<summary>`
  - open by default
  - simple entities: bullet list of field names
  - grouped entities: one subgroup heading per group
- Host Helper 2026 grouped schema:
  - preserve exact group names `Script-owned` and `Team-editable`
  - present as grouped subsections, not one flat list
- Related entities:
  - inline links or pill links
  - clicking one swaps the panel content to that entity
- Rebuild improvement:
  - treat the panel as a document sidebar, not a modal
  - ensure print styles render the selected entity content clearly

### Decision Card

- Layout:
  - relative card container
  - oversized background decision number in top-right corner
  - main content block above
  - quote block at bottom if present
- Content:
  - mono label `Decision N`
  - bold title
  - explanation paragraph
  - optional quote
  - quoted speaker: `Kim`
- Visual treatment:
  - faint numeral opacity around `0.05`
  - numeral can intensify slightly on hover
  - quote separated by top border

### Flow Node

- Base structure:
  - subtitle at top
  - title
  - italic description
  - footer row `Feeds → target`
- Color modes:
  - inputs = green-tinted
  - assembly = blue/teal-tinted
  - outputs = paper/gray
- Exact input cards:
  - `Kim's Tracker Sheets`
  - `OEC Active Roadmap`
  - `Kim's Comms Tracker`
- Exact assembly card:
  - `assemble-host-helper.py`
- Exact output cards:
  - `Interface Designer`
  - `oeff-airtable-sync.py`
- Use arrows between the sections, not between every card

### Flow Callout Blocks

- Two blocks under the pipeline:
  - dark forest synthesis card for the downhill principle
  - paper card for the dual-canonical principle
- Preserve the exact text from `oeff-architecture-data.json`

### Evolution Grid

- Structure:
  - CSS grid with `1fr 2fr 2fr`
  - use `gap: 1px` and a shared border color so the grid reads like a soft table
- Header row:
  - `Dimension`
  - `v1 — Venue-Centric`
  - `v2 — Event-Centric`
- Row content:
  - align each dimension directly across both versions
  - use the eight dimension rows from the JSON
- Colors:
  - left header/cells use coral tint `#f0dede`
  - right header/cells use green tint `#e3eedf`
- Footer:
  - full-width dark forest synthesis card

### Supporting Cards and Pills

- Platform card:
  - centered text
  - platform name + access label
- Timeline phase card:
  - period in mono
  - phase as heading
  - optional `Current` badge
- Role card:
  - title plus three chip clusters
- Risk pill:
  - pill button
  - clicking it opens the entity detail via the `DIAGRAM` tab

## 3. Design System Translation

### Beautiful-First Stance

Use OEFF domain semantics from the Beautiful-First vocabulary. The right default stance for this app is:

- `data-domain="oeff"`
- `data-world="personal"`
- `data-flavor="reference"`

That combination yields grounded warmth, reference-document pacing, and OEFF-specific palette choices. If you borrow the OEFF motion curve from the vocabulary, reserve it for tab/view entrances and panel reveals, not for every hover state.

### Core Token Set

Use hex fallbacks first and OKLCH declarations second where practical.

```css
:root {
  --forest-canopy: #1a2e22;
  --forest-understory: #2d4a3a;
  --forest-deep: #3a5c4d;
  --forest-sage: #4a6a5a;
  --forest-lichen: #8aaa98;
  --forest-mist: #c8d9ce;

  --teal: #4b7c8c;
  --ochre: #b8863a;
  --ink: #2c2825;
  --ink-soft: #5c5550;
  --ink-muted: #8a8580;
  --cream: #f7f5f2;
  --paper: #faf9f7;
  --linen: #f0ede8;

  --color-ground: var(--cream);
  --color-surface: var(--paper);
  --color-surface-raised: #ffffff;
  --color-surface-inset: var(--linen);
  --color-text: var(--ink);
  --color-text-soft: var(--ink-soft);
  --color-text-muted: var(--ink-muted);
  --color-border: var(--forest-mist);
  --color-primary: var(--forest-sage);
  --color-primary-deep: var(--forest-deep);
  --color-primary-dark: var(--forest-canopy);
  --color-primary-light: var(--forest-mist);

  --shadow-warm: 0 4px 20px hsla(25, 40%, 30%, 0.08);
  --shadow-warm-lg: 0 10px 30px hsla(25, 40%, 30%, 0.12);
  --radius-sm: 8px;
  --radius-md: 12px;
}
```

### Tailwind-to-Token Mapping

| React/Tailwind source | Rebuild token |
| --- | --- |
| `bg-[#f7f5f2]` | `var(--cream)` or `var(--color-ground)` |
| `bg-white` | `var(--color-surface-raised)` |
| `text-[#2c2825]` | `var(--ink)` or `var(--color-text)` |
| `text-[#8a8580]` | `var(--ink-muted)` or `var(--color-text-muted)` |
| `text-[#5c7c6b]` | `var(--forest-sage)` or `var(--color-primary)` |
| `border-[#c8d9ce]` | `var(--forest-mist)` or `var(--color-border)` |
| `bg-[#dce8e0]` | `--layer-core-bg` using a forest-tinted paper value |
| `bg-[#e8e3dd]` | `--layer-relational-bg` using teal-influenced neutral paper |
| `bg-[#f0ede8]` | `--layer-output-bg` using linen/ochre cast |
| `bg-[#f5f3f0]` | `--layer-resilience-bg` using pale paper with muted gray cast |

### Type/Badge Color Mapping

- Core = green
- Relational = teal
- Outputs = amber/ochre
- Resilience = muted gray
- Risk badges:
  - Low = green signal
  - Medium = amber signal
  - High = muted red signal
- Access labels:
  - `centralized` = green
  - `shared` = amber
  - `personal` = muted red

### Typography

- Display/headings: Fraunces with `font-optical-sizing: auto`
- Body/interface copy: Source Sans 3
- Synthesis text, quotes, descriptions: Source Serif 4
- Labels, tabs, badges, dimensions: Source Code Pro
- Hierarchy rules:
  - use Fraunces for page title, view titles, and card titles that need emphasis
  - use Source Serif 4 for synthesis copy and quotes
  - keep utility text mono and uppercase only when it is truly metadata

### Paper Grain

- Add a full-page SVG noise overlay using `feTurbulence`
- Opacity target: `0.03`
- Keep it just barely there
- Prefer `mix-blend-mode: multiply`
- Use the Beautiful-First low-grain approach, not heavy visible speckle

### Radius, Borders, and Shadows

- Minimum radius: `8px`
- Standard card radius: `12px`
- Border color: warm mist, never stark gray-black
- Use warm shadows everywhere, never pure black shadows

### Motion

- Hover transitions: `200ms ease`
- Tab/view transitions: `250-400ms`
- Detail panel entrance can use a softer, more expressive curve, but keep it restrained
- Preserve the outer-ring breathing animation
- Honor `prefers-reduced-motion`

### Accessibility and Ergonomics

- 44px minimum touch targets
- Visible focus styles on all buttons, cards, and tabs
- Support keyboard-only navigation
- Preserve context in the detail panel so users do not have to remember where they came from

## 4. Interaction Model

### Navigation

- Top tab buttons switch views without page reload
- Numeric keys `1-8` switch directly to the corresponding tab
- Active tab underline and text color update immediately

### Entity Discovery

- Hovering an entity card in the `DIAGRAM` view draws a connection line to its band
- Use a quadratic Bezier, not a straight line
- Source geometry in the React build:
  - start point = hovered card center
  - end point = top anchor of target ring band
  - control point = midpoint in x, lifted roughly `100px` upward
- Rebuild behavior:
  - keep the same logic, but smooth the curve and let it fade in over ~300ms
  - suppress hover-only behavior on touch devices

### Entity Selection

- Clicking an entity card opens the detail panel
- Clicking a related entity link inside the panel swaps the panel content to that related entity
- Clicking a risk pill switches to `DIAGRAM` and opens that entity immediately

### Detail Panel

- Opens from the right
- Closes via:
  - close button
  - scrim click
  - `Escape`
- The panel must restate:
  - layer/type
  - platform
  - lifecycle
  - risk
  - ownership
  - related entities
- This is an explicit design-philosophy requirement: no memory dependency

### Resilience Layer

- The resilience group in the diagram view keeps a dashed left rule
- Use `3px` dashed muted gray
- This is a structural cue, not decoration

### Motion and State Clarity

- Preserve visible selected state on the current entity card
- Keep the active tab visually obvious if a user leaves and returns
- Use one action per click:
  - card click opens detail
  - risk pill click opens detail via diagram
  - tab click changes tab only

## 5. Improvement Recommendations

### Color

The Gemini build uses generic green-leaning hex values. The rebuild should use the actual Forest palette and semantic aliases from Beautiful-First:

- forest greens for structural hierarchy
- teal for relational/flowing systems
- ochre/amber for outputs where needed
- warm neutrals for paper surfaces

### Typography Hierarchy

Use the full OEFF stack, not browser serif substitutions:

- Fraunces for display moments
- Source Sans 3 for interface text
- Source Serif 4 for synthesis, descriptions, and quotes
- Source Code Pro for metadata

### Ring Diagram

- Keep it in SVG, not Canvas
- Make it inspectable, printable, and easy to style
- Preserve band labels and center gravity
- Add subtle texture, not hard-edged flat geometry

### Card Density

The React build wastes vertical space in cards and sections. Tighten:

- card padding
- section spacing
- badge spacing
- line-height on metadata

Keep the app airy overall, but do not make every card feel oversized.

### Mobile

The React source does not meaningfully solve mobile. The rebuild should:

- wrap or horizontally scroll the tab row cleanly
- stack multi-column grids into one column
- convert the detail panel into a full-width overlay or bottom sheet on small screens
- suppress hover-only connection behavior on touch devices

### Detail Panel Tone

Make the panel feel like a document sidebar, not a product modal:

- readable section rhythm
- printable content
- native `<details>` for depth
- long-form scroll that feels intentional

### Paper Texture

The current feTurbulence treatment can become too noticeable. Keep the rebuild at “just barely there”:

- around `3%` opacity
- multiply blend
- no visible dirt or speckle pattern

### Connection Lines

The hover-to-show-connection-line idea is worth preserving. Improve it by:

- using smoother quadratic Beziers
- keeping the stroke light and soft
- optionally varying stroke weight slightly for more complex many-to-many entities

### Dependency Removal

The rebuild cannot depend on Lucide or motion libraries. Replace them with:

- inline SVG icons for the few places that truly need an icon
- CSS transitions and keyframes for animation
- native DOM state and event handling

## Implementation Notes

- Keep the data model externalized in a JSON block even though this is a single-file build
- Use progressive disclosure:
  - ring overview first
  - details only on click
  - schema inside `<details>`
- Keep the header quiet and the content load-bearing
- The single sentence users should feel immediately is:
  - OEFF's architecture is organized around Events as the hub, with supporting systems radiating outward
