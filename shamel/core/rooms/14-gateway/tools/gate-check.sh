#!/usr/bin/env bash
# tool/gtw/gatekeeper/gate-check.sh — Adversarial fresh-context gate check
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> <gate-number>
  Adversarial gate verification. Checks all upstream deliverables exist.
  Gate 2: Prototype_Spec, Journey_Map
  Gate 3: Architecture.md, DECISIONS.md
  Gate 4: source files, OpenAPI
  Gate 5: tests, coverage signals
EOF
exit 0
}

PRJ="${1:-}"; GATE="${2:-}"
[[ "$PRJ" == "--help" || -z "$PRJ" || -z "$GATE" ]] && usage

CTX="$SOFI_ROOT/projects/$PRJ/_context"
DOCS="$SOFI_ROOT/projects/$PRJ/docs"
ERRORS=0

echo "${BLUE}═══ Adversarial Gate Check :: $PRJ Gate $GATE ═══${RESET}"

case "$GATE" in
  2)
    for f in "docs/Prototype_Spec.md" "docs/Journey_Map.md"; do
      [[ -f "$SOFI_ROOT/projects/$PRJ/$f" ]] || { echo "${RED}✗ Missing: $f${RESET}"; ((ERRORS++)); }
    done
    grep -q 'design-freeze\|Gate 2 done' "$CTX/HANDOFFS.md" 2>/dev/null || { echo "${RED}✗ No Gate 2 signoff in HANDOFFS${RESET}"; ((ERRORS++)); }
    ;;
  3)
    [[ -f "$DOCS/Architecture.md" ]] || { echo "${RED}✗ Missing Architecture.md${RESET}"; ((ERRORS++)); }
    [[ -f "$CTX/DECISIONS.md" ]] || { echo "${RED}✗ Missing DECISIONS.md${RESET}"; ((ERRORS++)); }
    [[ -f "$DOCS/openapi.yaml" || -f "$DOCS/openapi.yml" ]] || { echo "${YELLOW}⚠ No OpenAPI spec found${RESET}"; }
    ;;
  4)
    SRC=$(find "$SOFI_ROOT/projects/$PRJ" -name '*.php' -o -name '*.vue' -o -name '*.ts' 2>/dev/null | wc -l)
    [[ "$SRC" -gt 0 ]] || { echo "${RED}✗ No source files${RESET}"; ((ERRORS++)); }
    [[ -f "$DOCS/openapi.yaml" ]] && echo "  ${GREEN}✓ OpenAPI spec${RESET}"
    grep -q 'build.*done\|implementation.*complete' "$CTX/HANDOFFS.md" 2>/dev/null || echo "  ${YELLOW}⚠ No build-complete signal${RESET}"
    ;;
  5)
    TEST_DIR="$SOFI_ROOT/projects/$PRJ/tests"
    [[ -d "$TEST_DIR" ]] || { echo "${RED}✗ No tests/ directory${RESET}"; ((ERRORS++)); }
    grep -q 'qa-pass\|quality.*green' "$CTX/HANDOFFS.md" 2>/dev/null || echo "  ${YELLOW}⚠ No QA signoff${RESET}"
    ;;
  *)
    echo "${RED}Unknown gate: $GATE${RESET}"; exit 1
    ;;
esac

if [[ $ERRORS -eq 0 ]]; then
  echo "${GREEN}✓ Gate $GATE: adversarial check PASSED${RESET}"
else
  echo "${RED}✗ Gate $GATE: $ERRORS failure(s) — reject upward${RESET}"
  exit 1
fi
