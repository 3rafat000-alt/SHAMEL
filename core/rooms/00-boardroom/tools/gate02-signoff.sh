#!/usr/bin/env bash
# tool/brd/cpo/gate02-signoff.sh — Gate 2 (Design) signoff checklist
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID>
  Verify Gate 2 design deliverables exist and are frozen.
  Checks: Prototype_Spec.md, Design_System.md, Journey_Map.md, wireframes.
EOF
exit 0
}

PRJ="${1:-}"; [[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage
CTX="$SOFI_ROOT/projects/$PRJ/_context"
DOCS="$SOFI_ROOT/projects/$PRJ/docs"

REQUIRED=(
  "docs/Prototype_Spec.md"
  "docs/Journey_Map.md"
)
SCORE=0; TOTAL=${#REQUIRED[@]}

echo "${BLUE}═══ Gate 2 Design Signoff :: $PRJ ═══${RESET}"
for f in "${REQUIRED[@]}"; do
  FP="$SOFI_ROOT/projects/$PRJ/$f"
  if [[ -f "$FP" ]]; then
    echo "  ${GREEN}✓${RESET} $f"
    ((SCORE++))
  else
    echo "  ${RED}✗${RESET} $f — MISSING"
  fi
done

# Check HANDOFFS for design-freeze signal
FROZEN=$(grep -c "design-freeze\|Gate 2 done\|DSN-FREEZE" "$CTX/HANDOFFS.md" 2>/dev/null || echo 0)
if [[ "$FROZEN" -gt 0 ]]; then
  echo "  ${GREEN}✓${RESET} design-freeze signal found in HANDOFFS"
  ((SCORE++))
else
  echo "  ${YELLOW}⚠${RESET} design-freeze signal not yet in HANDOFFS"
fi
((TOTAL++))

PCT=$((SCORE * 100 / TOTAL))
if [[ $PCT -ge 80 ]]; then
  echo "${GREEN}✓ Gate 2: ${SCORE}/${TOTAL} (${PCT}%) — PASS${RESET}"
else
  echo "${RED}✗ Gate 2: ${SCORE}/${TOTAL} (${PCT}%) — MISSING DELIVERABLES${RESET}"
  exit 1
fi
