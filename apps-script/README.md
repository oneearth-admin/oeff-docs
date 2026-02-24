# OEFF Host Intake — Apps Script Project

Programmatic Google Form generator for OEFF host venue intake.
Managed via `clasp` for headless deploy from terminal.

## Files

| File | Purpose |
|------|---------|
| `Code.js` | Apps Script — creates form, response sheet, Airtable Ready sheet, onFormSubmit trigger, updateFormText |
| `appsscript.json` | Apps Script project manifest (timezone, runtime) |
| `.clasp.json` | Links to the Apps Script project (scriptId) |
| `inject-films.py` | Reads `02-films.csv` and updates the film dropdown in Code.js |
| `deploy.sh` | Push and/or run via clasp |

## One-Time Setup

```bash
npm install -g @google/clasp
clasp login                    # opens browser for OAuth
```

## Usage

```bash
cd ~/Desktop/OEFF\ Clean\ Data/apps-script

# Patch text on the EXISTING form (safe — no new artifacts)
./deploy.sh update

# Push only (no execution)
./deploy.sh push

# Push + create a NEW form (use sparingly — generates new form + sheet)
./deploy.sh

# Regenerate Code.js from film CSV, then push + create new form
./deploy.sh regen
```

## Functions

| Function | Purpose | Safe to re-run? |
|----------|---------|-----------------|
| `createHostIntakeForm` | Creates a brand new form, response sheet, and trigger | No — creates duplicates |
| `updateFormText` | Patches section descriptions, help text, confirmation on existing form | Yes — idempotent |
| `processNewResponse` | onFormSubmit trigger handler | Auto-invoked |
| `reprocessAllResponses` | Re-run all responses through the Airtable Ready processor | Yes |

## Known Limitation: `clasp run`

`clasp run` requires the Apps Script Execution API enabled in the linked GCP project.
Currently **not configured**, so `clasp run` fails with a permission error.

**Workaround:** `clasp push` then run manually:
1. Open the [Apps Script editor](https://script.google.com/home/projects/1gZuy7QIGxk58lcSktBTOgXEDSEwBc-wm_xaiBphR1F9a9QARLdkkj53i/edit)
2. Select the function from the dropdown
3. Click Run

**To fix permanently:** Enable the Apps Script API in the OEFF GCP project.
See `~/decisions/2026-02-23-clasp-standalone-script-patterns.md` for details.

## Standalone Script Pattern

This is a **standalone** Apps Script project (managed via clasp), not a
container-bound script. Use `FormApp.openById(FORM_ID)` — never `getActiveForm()`.

## For 2027

1. Update `../airtable-import/02-films.csv` with new film catalog
2. Run `./deploy.sh regen`
3. Check `clasp logs` for the new form URL

## Live Artifacts (2026)

- Form edit: https://docs.google.com/forms/d/1QHXvvXU9JPsKIITC50cbq77XKHReAUcC8ymKXMkboig/edit
- Form live: https://docs.google.com/forms/d/e/1FAIpQLScSmS4i--WT6rgm6p8wIuLHVLnoyQNsn52hfSW4Qe1rDQVhrw/viewform
- Response sheet: https://docs.google.com/spreadsheets/d/1wQkiGySU9Z4zd08MAQHGIxTDZtTgDbTd_IpPFHqjX9k/edit
- Apps Script project: https://script.google.com/home/projects/1gZuy7QIGxk58lcSktBTOgXEDSEwBc-wm_xaiBphR1F9a9QARLdkkj53i/edit

## Airtable Interop

The `onFormSubmit` trigger auto-processes responses into an "Airtable Ready" sheet:
- Checkbox groups → individual boolean columns
- Film dropdown → Film_ID + Film_Title split
- Auto-generated Intake_ID (HIF-XXX)
- Headers match Table 7: HOST INTAKE schema exactly
