# OEFF Host Intake — Apps Script Project

Programmatic Google Form generator for OEFF host venue intake.
Managed via `clasp` for headless deploy from terminal.

## Files

| File | Purpose |
|------|---------|
| `Code.js` | Apps Script — creates form, response sheet, Airtable Ready sheet, onFormSubmit trigger |
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

# Push current Code.js and run it (creates a new form)
./deploy.sh

# Push only (no execution)
./deploy.sh push

# Regenerate Code.js from film CSV, then push + run
./deploy.sh regen
```

## For 2027

1. Update `../airtable-import/02-films.csv` with new film catalog
2. Run `./deploy.sh regen`
3. Check `clasp logs` for the new form URL

## Live Artifacts (2026)

- Form edit: https://docs.google.com/forms/d/1ewvYQKuEw3HG_L5ZpE9nXnbS8OZwtVY7NBQDmfpBFsk/edit
- Form live: https://docs.google.com/forms/d/e/1FAIpQLSepbwEH7QgCrRjyMpG3e3zRFVyKmTIWBp3tQyWW4mRHRNdIPA/viewform
- Response sheet: https://docs.google.com/spreadsheets/d/12Z9qyeFcLWcEsD0myngb_hRIc2B9-UtcEKoORV-tI5k/edit

## Airtable Interop

The `onFormSubmit` trigger auto-processes responses into an "Airtable Ready" sheet:
- Checkbox groups → individual boolean columns
- Film dropdown → Film_ID + Film_Title split
- Auto-generated Intake_ID (HIF-XXX)
- Headers match Table 7: HOST INTAKE schema exactly
