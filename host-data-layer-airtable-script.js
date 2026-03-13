// =============================================================================
// OEFF Host Portal Data Layer — Airtable Scripting Extension
// =============================================================================
// Paste this into the Airtable Scripting extension (Extensions > Scripting > Edit code)
// and click Run. Creates all rollup and formula fields for the host portal.
//
// Safe to re-run: checks for existing fields by name before creating.
// Run in 4 phases (rollups → formulas → Events formula → All Screenings rollup)
// =============================================================================

// Phase 1: Rollup fields on Venues (from Events, Host Contacts, Host Intake)
const venuesTable = base.getTable("Venues");
const eventsTable = base.getTable("Events");

const existingVenueFields = venuesTable.fields.map(f => f.name);
const existingEventFields = eventsTable.fields.map(f => f.name);

let created = 0;
let skipped = 0;

// Helper: find field by name in a table
function fieldId(table, name) {
    const f = table.fields.find(f => f.name === name);
    if (!f) { output.text(`  ERROR: field "${name}" not found on ${table.name}`); return null; }
    return f.id;
}

// Helper: find link field on source table
function linkFieldId(sourceTable, linkFieldName) {
    const f = sourceTable.fields.find(f => f.name === linkFieldName);
    if (!f) { output.text(`  ERROR: link field "${linkFieldName}" not found on ${sourceTable.name}`); return null; }
    return f.id;
}

output.text("=== Phase 1: Rollup fields on Venues ===");

const rollups = [
    // From Events
    {name: "LKP Film Title",   link: "Events", target: "Film Title",   formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Event Date",   link: "Events", target: "Date",         formula: "MAX(values)"},
    {name: "LKP Event Time",   link: "Events", target: "Time",         formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Doors Open",   link: "Events", target: "Doors Open",   formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Ticket Price", link: "Events", target: "Ticket Price", formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Ticket URL",   link: "Events", target: "Ticket URL",   formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP OEFF Rep",     link: "Events", target: "OEFF Rep",     formula: 'ARRAYJOIN(values, ", ")'},
    // From Host Contacts
    {name: "LKP Host Name",    link: "Host Contacts", target: "Contact Name", formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Host Email",   link: "Host Contacts", target: "Email",        formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Host Phone",   link: "Host Contacts", target: "Phone",        formula: 'ARRAYJOIN(values, ", ")'},
    // From Host Intake
    {name: "LKP Intake Address",     link: "Host Intake", target: "Venue Address",  formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Intake WiFi",        link: "Host Intake", target: "Has Wifi",       formula: 'ARRAYJOIN(values, ", ")'},
    {name: "LKP Intake Space Notes", link: "Host Intake", target: "Space Notes",    formula: 'ARRAYJOIN(values, "\\n")'},
    {name: "LKP Intake Wheelchair",  link: "Host Intake", target: "Has Wheelchair", formula: 'ARRAYJOIN(values, ", ")'},
];

for (const r of rollups) {
    if (existingVenueFields.includes(r.name)) {
        output.text(`  SKIP "${r.name}" — already exists`);
        skipped++;
        continue;
    }
    const linkedTable = base.getTable(r.link);
    const lnkId = linkFieldId(venuesTable, r.link);
    const tgtId = fieldId(linkedTable, r.target);
    if (!lnkId || !tgtId) continue;

    await venuesTable.createFieldAsync(r.name, "rollup", {
        recordLinkFieldId: lnkId,
        fieldIdInLinkedTable: tgtId,
        formulaTextParsed: r.formula,
    });
    output.text(`  CREATED rollup "${r.name}"`);
    created++;
}

// Phase 2: Display formula fields on Venues
output.text("\n=== Phase 2: Display formula fields on Venues ===");

const formulas = [
    {name: "Host - Film",           formula: 'IF({LKP Film Title}, {LKP Film Title}, "Film to be confirmed")'},
    {name: "Host - Screening Date", formula: 'IF({LKP Event Date}, DATETIME_FORMAT({LKP Event Date}, "dddd, MMMM D, YYYY"), "Date to be confirmed")'},
    {name: "Host - Start Time",     formula: 'IF({LKP Event Time}, {LKP Event Time}, "Start time to be confirmed")'},
    {name: "Host - Doors Open",     formula: 'IF({LKP Doors Open}, {LKP Doors Open}, "Doors-open time to be confirmed")'},
    {name: "Host - Ticket Info",    formula: 'IF({LKP Ticket URL}, {LKP Ticket URL}, "Ticket link coming soon")'},
    {name: "Host - Contact Name",   formula: 'IF({LKP Host Name}, {LKP Host Name}, "Host contact to be confirmed")'},
    {name: "Host - Contact Phone",  formula: 'IF({LKP Host Phone}, {LKP Host Phone}, "Phone to be confirmed")'},
    {name: "Host - Contact Email",  formula: 'IF({LKP Host Email}, {LKP Host Email}, "Email to be confirmed")'},
    {name: "Host - Venue Address",  formula: 'IF({Address}, {Address}, IF({LKP Intake Address}, {LKP Intake Address}, "Address to be confirmed"))'},
    {name: "Host - Parking",        formula: 'IF({Parking Info}, {Parking Info}, "Parking details available on request")'},
    {name: "Host - Transit",        formula: 'IF({Transit Info}, {Transit Info}, "Transit details available on request")'},
    {name: "Host - WiFi",           formula: 'IF({WiFi Info}, {WiFi Info}, "WiFi details shared day-of")'},
    {name: "Host - AV Notes",       formula: 'IF({LKP Intake Space Notes}, {LKP Intake Space Notes}, "")'},
];

// Refresh field list after Phase 1
const updatedVenueFields = venuesTable.fields.map(f => f.name);

for (const f of formulas) {
    if (updatedVenueFields.includes(f.name)) {
        output.text(`  SKIP "${f.name}" — already exists`);
        skipped++;
        continue;
    }
    await venuesTable.createFieldAsync(f.name, "formula", {
        formulaTextParsed: f.formula,
    });
    output.text(`  CREATED formula "${f.name}"`);
    created++;
}

// Phase 3: Host Summary Line formula on Events
output.text("\n=== Phase 3: Host Summary Line on Events ===");

if (existingEventFields.includes("Host Summary Line")) {
    output.text('  SKIP "Host Summary Line" — already exists');
    skipped++;
} else {
    await eventsTable.createFieldAsync("Host Summary Line", "formula", {
        formulaTextParsed: '{Film Title} & " — " & IF({Date}, DATETIME_FORMAT({Date}, "MMM D"), "TBD") & IF({Time}, " at " & {Time}, "")',
    });
    output.text('  CREATED formula "Host Summary Line"');
    created++;
}

// Phase 4: Host - All Screenings rollup on Venues
output.text("\n=== Phase 4: Host - All Screenings rollup on Venues ===");

const finalVenueFields = venuesTable.fields.map(f => f.name);

if (finalVenueFields.includes("Host - All Screenings")) {
    output.text('  SKIP "Host - All Screenings" — already exists');
    skipped++;
} else {
    // Need fresh references after Phase 3 created the field
    const freshEvents = base.getTable("Events");
    const summaryField = freshEvents.fields.find(f => f.name === "Host Summary Line");
    const eventsLinkId = linkFieldId(venuesTable, "Events");

    if (!summaryField || !eventsLinkId) {
        output.text("  ERROR: Could not find Host Summary Line or Events link field");
    } else {
        await venuesTable.createFieldAsync("Host - All Screenings", "rollup", {
            recordLinkFieldId: eventsLinkId,
            fieldIdInLinkedTable: summaryField.id,
            formulaTextParsed: 'ARRAYJOIN(values, "\\n")',
        });
        output.text('  CREATED rollup "Host - All Screenings"');
        created++;
    }
}

output.text(`\n=== DONE: ${created} created, ${skipped} skipped ===`);
