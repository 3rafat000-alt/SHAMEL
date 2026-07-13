#!/usr/bin/env bash
# tool/dsn/ui-designer/screen-spec.sh — Generate text UI spec from journey stage
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --screen "<name>" --stage "<stage>" [--elements "<h1,p,button>"] [--states "<loading,empty,error>"]
  Generate text-format UI spec for a single screen.
  Outputs to docs/screens/<name>.md.
EOF
exit 0
}

PRJ="${1:-}"; SCREEN=""; STAGE=""; ELEMENTS=""; STATES=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --screen) SCREEN="$2"; shift;; --stage) STAGE="$2"; shift;;
  --elements) ELEMENTS="$2"; shift;; --states) STATES="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$SCREEN" || -z "$STAGE" ]] && usage

OUT="$SOFI_ROOT/projects/$PRJ/docs/screens/${SCREEN// /_}.md"
mkdir -p "$(dirname "$OUT")"
TS=$(date '+%Y-%m-%d')

{
  echo "# Screen Spec: $SCREEN"
  echo "**PRJ-ID:** $PRJ | **Journey Stage:** $STAGE | **Date:** $TS"
  echo ""
  echo "## Layout"
  echo "\`\`\`"
  echo "+--------------------------------------------+"
  echo "|  [HEADER — app title / back / actions]     |"
  echo "|                                            |"
  echo "|  [MAIN CONTENT AREA]                       |"
  echo "|                                            |"
  echo "|  [FOOTER / NAVIGATION]                     |"
  echo "+--------------------------------------------+"
  echo "\`\`\`"
  echo ""
  echo "## Elements"

  if [[ -n "$ELEMENTS" ]]; then
    IFS=',' read -ra EARR <<< "$ELEMENTS"
    for elem in "${EARR[@]}"; do
      echo "- **\`<$elem>\`** — _description, behavior, constraints_"
    done
  else
    echo "- _List UI elements here_"
  fi

  echo ""
  echo "## Interaction States"
  if [[ -n "$STATES" ]]; then
    IFS=',' read -ra SARR <<< "$STATES"
    for st in "${SARR[@]}"; do
      echo "- **$st:** _what happens in this state_"
    done
  else
    echo "- _Loading, empty, error, edge cases_"
  fi

  echo ""
  echo "## Acceptance"
  echo "- [ ] Screen matches layout above"
  echo "- [ ] All elements render correctly"
  echo "- [ ] States handled gracefully"
  echo "- [ ] WCAG 2.2 AA compliance"
} > "$OUT"

echo "${GREEN}✓ Screen spec created: $OUT${RESET}"
