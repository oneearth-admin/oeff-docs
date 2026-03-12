// Airtable Scripting Extension — Create 2026 season-filtered formula fields on Events table
// Paste this into: Extensions → Scripting → paste → Run
//
// Creates 8 formula fields that return values only for 2026 events.
// These become the targets for the LKP rollup fields on Venues,
// so hosts only see current-year data.

const eventsTable = base.getTable("Events");

const fieldsToCreate = [
    {
        name: "2026 Film Title",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Film Title}, "")' }
    },
    {
        name: "2026 Date",
        type: "formula",
        options: { formula: 'IF({Season}="2026", Date, BLANK())' }
    },
    {
        name: "2026 Time",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Time}, "")' }
    },
    {
        name: "2026 Doors Open",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Doors Open}, "")' }
    },
    {
        name: "2026 Ticket Price",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Ticket Price}, "")' }
    },
    {
        name: "2026 Ticket URL",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Ticket URL}, "")' }
    },
    {
        name: "2026 OEFF Rep",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {OEFF Rep}, "")' }
    },
    {
        name: "2026 Summary Line",
        type: "formula",
        options: { formula: 'IF({Season}="2026", {Film Title} & " — " & IF({Date}, DATETIME_FORMAT({Date}, "MMM D"), "TBD") & IF({Time}, " at " & {Time}, ""), "")' }
    },
];

// Check which fields already exist
const existingFields = eventsTable.fields.map(f => f.name);

let created = 0;
let skipped = 0;

for (const fieldDef of fieldsToCreate) {
    if (existingFields.includes(fieldDef.name)) {
        output.text(`⏭ Skipping "${fieldDef.name}" — already exists`);
        skipped++;
        continue;
    }

    try {
        await eventsTable.createFieldAsync(fieldDef.name, fieldDef.type, fieldDef.options);
        output.text(`✅ Created "${fieldDef.name}"`);
        created++;
    } catch (e) {
        output.text(`❌ Failed "${fieldDef.name}": ${e.message}`);
    }
}

output.text(`\nDone. Created: ${created}, Skipped: ${skipped}`);
output.text(`\nNext step: Run fix-season-rollups.py to retarget the LKP rollup fields.`);
