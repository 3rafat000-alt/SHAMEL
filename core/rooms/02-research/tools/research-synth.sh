#!/usr/bin/env bash
# tool/res/lead/research-synth.sh — Synthesize research findings into Journey Map
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RED=$(tput setaf 1); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--findings "<file>"]
  Synthesize research artifacts into draft Journey Map.
  Reads _context/RESEARCH_NOTES.md if no --findings given.
  Outputs to docs/Journey_Map.md (appends to existing).
EOF
exit 0
}

PRJ="${1:-}"; FINDINGS=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--findings" ]] && FINDINGS="${2:-}"

DOCS="$SOFI_ROOT/projects/$PRJ/docs"
NOTES="$SOFI_ROOT/projects/$PRJ/_context/RESEARCH_NOTES.md"
JM="$DOCS/Journey_Map.md"
mkdir -p "$DOCS"

INPUT="${FINDINGS:-$NOTES}"
[[ ! -f "$INPUT" ]] && { echo "${RED}✗ No findings file: $INPUT${RESET}"; exit 1; }

echo "${BLUE}═══ Research Synthesis :: $PRJ ═══${RESET}"
echo "  Source: $INPUT"
echo "  Target: $JM"
echo ""

# Extract potential journey stages
STAGES=$(grep -iE 'stage|phase|step|screen|page|flow' "$INPUT" 2>/dev/null | head -10 || true)
if [[ -z "$STAGES" ]]; then
  echo "${YELLOW}⚠ No explicit stages found — see Journey Map template${RESET}"
fi

TS=$(date '+%Y-%m-%d')
cat > "$JM" <<JOURNEY
# Journey Map: $PRJ
**Synthesized:** $TS
**Source:** $INPUT

## Stages

| Stage | User Goal | Touchpoint | Emotion | Pain Point |
|-------|-----------|------------|---------|------------|
| 1. | | | 😊 | |

## Notes
$STAGES
JOURNEY

echo "${GREEN}✓ Journey Map draft created at $JM${RESET}"
echo "  Edit stages/goals/touchpoints from research data."
