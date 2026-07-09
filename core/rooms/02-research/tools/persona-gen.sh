#!/usr/bin/env bash
# tool/res/ux-researcher/persona-gen.sh — Generate evidence-based persona from interview notes
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RED=$(tput setaf 1); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --name "<Persona Name>" --role "<role>" --goal "<JTBD>" [--pain "<pains>"] [--output <file>]
  Generate evidence-based persona document.
  Reads interview notes if --pain omitted.
EOF
exit 0
}

PRJ="${1:-}"; NAME=""; ROLE=""; GOAL=""; PAIN=""; OUTPUT=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --name) NAME="$2"; shift;; --role) ROLE="$2"; shift;;
  --goal) GOAL="$2"; shift;; --pain) PAIN="$2"; shift;;
  --output) OUTPUT="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$NAME" || -z "$ROLE" || -z "$GOAL" ]] && usage

OUTPUT="${OUTPUT:-$SOFI_ROOT/projects/$PRJ/docs/personas/${NAME// /_}.md}"
mkdir -p "$(dirname "$OUTPUT")"

# Try to extract pains from interview notes
if [[ -z "$PAIN" ]]; then
  NOTES="$SOFI_ROOT/projects/$PRJ/_context/INTERVIEW_NOTES.md"
  [[ -f "$NOTES" ]] && PAIN=$(grep -i 'pain|frustrat|struggle|hard to|difficult' "$NOTES" 2>/dev/null | head -5 | tr '\n' '; ') || PAIN="TBD from interview data"
fi

cat > "$OUTPUT" <<PERSONA
# Persona: $NAME

**Role:** $ROLE
**PRJ-ID:** $PRJ
**Created:** $(date '+%Y-%m-%d')

## Profile
- **Name:** $NAME
- **Role:** $ROLE
- **Archetype:** _e.g., Power User, Skeptical Buyer, First-Timer_

## Job-to-be-Done
$GOAL

## Pain Points
${PAIN}

## Behaviors & Preferences
- _How do they solve this today?_
- _What tools do they use?_
- _What would make them switch?_

## Quote
_"A representative quote from interview notes."_
PERSONA

echo "${GREEN}✓ Persona created: $OUTPUT${RESET}"
