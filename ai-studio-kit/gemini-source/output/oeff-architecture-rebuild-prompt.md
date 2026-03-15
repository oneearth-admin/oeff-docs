Build a single-file vanilla HTML app called `oeff-architecture-explorer.html` following the spec in `oeff-architecture-rebuild-spec.md`.

Read the architecture data from `oeff-architecture-data.json` and inline it into the final HTML as a `<script type="application/json" id="oeff-data">` block. Do not fetch external JSON at runtime.

Follow Beautiful-First design system conventions from `~/claude-ecosystem/skills/design-core/VOCABULARY.md`. Use the OEFF / Forest palette, warm paper surfaces, semantic tokens, Fraunces + Source Sans 3 + Source Serif 4 + Source Code Pro, subtle paper grain, and restrained motion.

Use the local references for tone and constraints:

- `~/Desktop/OEFF Clean Data/ai-studio-kit/design-philosophy-prompt.md`
- `~/Desktop/OEFF Clean Data/ai-studio-kit/oeff-architecture-explorer.html`

Required implementation constraints:

- No frameworks
- No npm
- No build step
- One self-contained static HTML file
- Deployable to Cloudflare Pages as-is
- Use inline CSS and vanilla JavaScript only
- Use an inspectable SVG ring diagram, not Canvas
- Preserve all 8 views, keyboard shortcuts `1-8`, `Escape` to close the detail panel, the right-side slide-in detail panel, and hover connection lines in the diagram view

Required UX goals:

- The app should feel like a warm reference document, not a dashboard
- The ring diagram should have visual gravity around `Events`
- Cards should be denser and more compact than the Gemini version
- Mobile layout must stack gracefully
- The detail panel should feel like a document sidebar and print cleanly
- Paper texture should be barely visible

Use the exact content from `oeff-architecture-data.json` and the exact structure from `oeff-architecture-rebuild-spec.md`. Do not invent additional entities, fields, decisions, or pipeline steps. If you derive helper structures in JavaScript, derive them from the provided JSON.
