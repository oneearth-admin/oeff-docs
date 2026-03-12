// Airtable Scripting Extension — Create 2026 season-filtered rollup fields on Venues
// Paste into: Extensions → Scripting → paste → Run
//
// Creates 8 rollup fields that aggregate from the "2026 Events" link field
// instead of the "Events" link field, so only 2026 data flows through.

const venuesTable = base.getTable("Venues");

// "2026 Events" link field ID (already created via API)
const link2026Id = "fldjkmi6lxLsZGgZm";

const rollupsToCreate = [
    { name: "2026 Film Title",     targetFieldId: "fldgnaQ1tPG0lA8ZT" },
    { name: "2026 Event Date",     targetFieldId: "fld3OmeOCoH7n5nJe" },
    { name: "2026 Event Time",     targetFieldId: "fldkbAWVXddXBfeLS" },
    { name: "2026 Doors Open",     targetFieldId: "fldWUIUapFwLrGZuL" },
    { name: "2026 Ticket Price",   targetFieldId: "fldi0ThCVwwtDx1Ck" },
    { name: "2026 Ticket URL",     targetFieldId: "fldKa12N8M9ncVIt9" },
    { name: "2026 OEFF Rep",       targetFieldId: "fldW2DBOXNIei10bg" },
    { name: "2026 All Screenings", targetFieldId: "fldlheYujL3faxWiP" },
];

const existingFields = venuesTable.fields.map(f => f.name);
let created = 0;
let skipped = 0;

for (const rollup of rollupsToCreate) {
    if (existingFields.includes(rollup.name)) {
        output.text(`⏭ Skipping "${rollup.name}" — already exists`);
        skipped++;
        continue;
    }

    try {
        await venuesTable.createFieldAsync(rollup.name, "rollup", {
            recordLinkFieldId: link2026Id,
            fieldIdInLinkedTable: rollup.targetFieldId,
        });
        output.text(`✅ Created "${rollup.name}"`);
        created++;
    } catch (e) {
        output.text(`❌ Failed "${rollup.name}": ${e.message}`);
    }
}

output.text(`\nDone. Created: ${created}, Skipped: ${skipped}`);
output.text(`\nNext: Update "Host -" display formulas to reference these new "2026 *" rollup fields.`);
