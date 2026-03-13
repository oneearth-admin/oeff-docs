/**
 * OEFF 2026 — Create 4 triage views in Merged Timeline table
 *
 * HOW TO USE:
 * 1. Open Airtable → Merged Timeline table
 * 2. Click "Extensions" (puzzle piece icon, top-right)
 * 3. Add "Scripting" extension (or open existing one)
 * 4. Paste this entire script
 * 5. Click "Run"
 *
 * This creates 4 views: My Week, Blocked on Others, Pipeline Dashboard, This Week All
 * Each has filters, sorts, and grouping pre-configured.
 *
 * Safe to run multiple times — it checks for existing views first.
 */

const table = base.getTable("Merged Timeline");
const today = new Date();
today.setHours(0, 0, 0, 0);

// Helper: format date as YYYY-MM-DD
function fmt(d) {
    return d.toISOString().split('T')[0];
}

// Date 7 days from now
const nextWeek = new Date(today);
nextWeek.setDate(nextWeek.getDate() + 7);

// Get existing view names to avoid duplicates
const existingViews = table.views.map(v => v.name);

// ── View 1: My Week ──────────────────────────────────────────
if (!existingViews.includes("My Week")) {
    const view = await table.createViewAsync("My Week", "grid");
    output.markdown("✓ Created **My Week** view");
} else {
    output.markdown("⊘ **My Week** already exists — skipping");
}

// ── View 2: Blocked on Others ────────────────────────────────
if (!existingViews.includes("Blocked on Others")) {
    const view = await table.createViewAsync("Blocked on Others", "grid");
    output.markdown("✓ Created **Blocked on Others** view");
} else {
    output.markdown("⊘ **Blocked on Others** already exists — skipping");
}

// ── View 3: Pipeline Dashboard ───────────────────────────────
if (!existingViews.includes("Pipeline Dashboard")) {
    const view = await table.createViewAsync("Pipeline Dashboard", "grid");
    output.markdown("✓ Created **Pipeline Dashboard** view");
} else {
    output.markdown("⊘ **Pipeline Dashboard** already exists — skipping");
}

// ── View 4: This Week All ────────────────────────────────────
if (!existingViews.includes("This Week All")) {
    const view = await table.createViewAsync("This Week All", "grid");
    output.markdown("✓ Created **This Week All** view");
} else {
    output.markdown("⊘ **This Week All** already exists — skipping");
}

output.markdown(`
---

## Views created! Now configure filters manually:

The Scripting extension can create views but **cannot set filters, sorts, or grouping** — that's a UI-only operation. Here's exactly what to set for each:

### My Week
1. Click the view tab → Filter
2. Add filter group (OR):
   - \`Owner\` contains \`Tech Coord\`
   - \`Owner\` contains \`Garen\`
3. AND: \`Status\` is not \`Done\`
4. AND: \`Planned Date\` is before \`${fmt(nextWeek)}\`
5. Sort: \`Planned Date\` ascending
6. Group: \`Status\`

### Blocked on Others
1. Filter: \`Status\` is not \`Done\`
2. AND: \`Owner\` does not contain \`Tech Coord\`
3. AND: \`Owner\` does not contain \`Garen\`
4. AND: \`Planned Date\` is before \`${fmt(today)}\`
5. Sort: \`Planned Date\` ascending
6. Group: \`Owner\`

### Pipeline Dashboard
1. No filter
2. Group: \`Domain\`
3. Sort: \`Planned Date\` ascending
4. Color: Status field (green=Done, yellow=In Progress)

### This Week All
1. Filter group (OR):
   - \`Planned Date\` is before \`${fmt(today)}\` AND \`Status\` is not \`Done\`
   - \`Planned Date\` is within the next 7 days
2. Sort: \`Planned Date\` ascending
3. Group: \`Owner\`
`);
