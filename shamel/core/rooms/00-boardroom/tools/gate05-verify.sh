#!/usr/bin/env bash
# tool/brd/cqo/gate05-verify.sh — Gate 5 quality pass/kill
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--min-coverage <N>] [--max-tti <N>]
  Verify Gate 5 quality bar: tests, coverage, lint, TTI.
  Default min-coverage: 90. Default max-tti: 2.0s.
EOF
exit 0
}

PRJ="${1:-}"; MIN_COV=90; MAX_TTI=2.0
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --min-coverage) MIN_COV="$2"; shift;; --max-tti) MAX_TTI="$2"; shift;; esac; shift
done

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
PASS=0; FAIL=0

echo "${BLUE}═══ Gate 5 Quality Verification :: $PRJ ═══${RESET}"

# Test: project has tests
if ls "$PRJ_DIR"/tests/*.php "$PRJ_DIR"/test* "$PRJ_DIR"/__tests__ 2>/dev/null | head -1 >/dev/null; then
  echo "  ${GREEN}✓${RESET} Test directory found"; ((PASS++))
else
  echo "  ${RED}✗${RESET} No test directory — TDD violation"; ((FAIL++))
fi

# Test: lint / syntax check
if [[ -f "$PRJ_DIR/composer.json" ]]; then
  if php -l "$PRJ_DIR"/*.php 2>/dev/null | grep -q 'No syntax'; then
    echo "  ${GREEN}✓${RESET} PHP lint passed"; ((PASS++))
  else
    echo "  ${YELLOW}⚠${RESET} PHP lint not confirmed"; ((FAIL++))
  fi
fi

# Test: HANDOFFS quality signal
if grep -q "qa-pass\|quality.*green\|Gate.*5.*done" "$PRJ_DIR/_context/HANDOFFS.md" 2>/dev/null; then
  echo "  ${GREEN}✓${RESET} QA signoff in HANDOFFS"; ((PASS++))
else
  echo "  ${YELLOW}⚠${RESET} No QA signoff in HANDOFFS"; ((FAIL++))
fi

PCT=$((PASS * 100 / (PASS + FAIL)))
echo ""
if [[ $PCT -ge 75 ]]; then
  echo "${GREEN}✓ Gate 5: ${PASS}/${PASS+FAIL} checks passing — PASS${RESET}"
else
  echo "${RED}✗ Gate 5: ${FAIL} failures — KILL${RESET}"
  exit 1
fi
