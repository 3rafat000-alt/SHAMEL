#!/usr/bin/env bash
# tool/gtw/budget-warden/token-audit.sh — Token waste report
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); MAGENTA=$(tput setaf 5); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--verbose]
  Audit token efficiency: route stamps, caveman discipline, model choices.
  Reads ROUTE_LOG.md and calculates waste score.
EOF
exit 0
}

PRJ="${1:-}"; VERBOSE=false
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--verbose" ]] && VERBOSE=true

ROUTE_LOG="$SOFI_ROOT/projects/$PRJ/_context/ROUTE_LOG.md"
STATE="$SOFI_ROOT/projects/$PRJ/_context/STATE.md"
WASTE=0; TOTAL=0

echo "${BLUE}═══ Token Waste Audit :: $PRJ ═══${RESET}"

if [[ ! -f "$ROUTE_LOG" ]]; then
  echo "${YELLOW}⚠ No ROUTE_LOG.md — audit requires route stamps${RESET}"
  echo "  Run route-stamp.sh before each delegation."
  exit 0
fi

# Count route stamps
STAMPS=$(grep -c "^| \*\*Model\*\*" "$ROUTE_LOG" 2>/dev/null || echo 0)
echo "  Route stamps logged: $STAMPS"

if [[ $STAMPS -eq 0 ]]; then
  echo "${RED}✗ Zero route stamps — all delegations un-audited${RESET}"
  exit 1
fi

# Check for expensive models
OPUS_COUNT=$(grep -c "| Opus" "$ROUTE_LOG" 2>/dev/null || echo 0)
if [[ "$OPUS_COUNT" -gt 0 ]]; then
  echo "  ${RED}⚠ ${OPUS_COUNT} Opus delegations — expensive${RESET}"
  WASTE=$((WASTE + OPUS_COUNT * 10))
fi

# Check caveman discipline
OFF_COUNT=$(grep -c "| off " "$ROUTE_LOG" 2>/dev/null || echo 0)
UFO=$(grep -c "| ultra " "$ROUTE_LOG" 2>/dev/null || echo 0)
FULL=$(grep -c "| full " "$ROUTE_LOG" 2>/dev/null || echo 0)
echo "  Caveman: off=$OFF_COUNT ultra=$UFO full=$FULL"

if [[ "$VERBOSE" == true ]]; then
  echo ""
  echo "${MAGENTA}Route details:${RESET}"
  while IFS= read -r line; do echo "  $line"; done < "$ROUTE_LOG"
fi

echo ""
if [[ $WASTE -eq 0 ]]; then
  echo "${GREEN}✓ No token waste detected${RESET}"
else
  echo "${YELLOW}⚠ Waste score: $WASTE — review Opus routes${RESET}"
fi
echo "${GREEN}✓ Audit complete${RESET}"
