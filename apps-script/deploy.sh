#!/usr/bin/env bash
# OEFF Host Intake Form — clasp deploy
#
# Prerequisites (one-time):
#   npm install -g @google/clasp
#   clasp login
#
# Usage:
#   cd ~/Desktop/OEFF\ Clean\ Data/apps-script
#   ./deploy.sh           # push + run
#   ./deploy.sh push      # push only (no run)
#   ./deploy.sh regen     # regenerate Code.js from template + film CSV, then push + run

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

command -v clasp >/dev/null 2>&1 || {
  echo "Error: clasp not found. Install with: npm install -g @google/clasp"
  exit 1
}

ACTION="${1:-deploy}"

case "$ACTION" in
  regen)
    echo "Regenerating Code.js from template + film catalog..."
    python3 "$SCRIPT_DIR/inject-films.py"
    echo "Pushing to Apps Script..."
    clasp push
    echo "Running createHostIntakeForm..."
    clasp run createHostIntakeForm
    echo "Done. Check clasp logs for form URLs:"
    clasp logs --simplified
    ;;
  push)
    echo "Pushing to Apps Script..."
    clasp push
    echo "Push complete."
    ;;
  deploy|*)
    echo "Pushing to Apps Script..."
    clasp push
    echo "Running createHostIntakeForm..."
    clasp run createHostIntakeForm
    echo "Done. Check clasp logs for form URLs:"
    clasp logs --simplified
    ;;
esac
