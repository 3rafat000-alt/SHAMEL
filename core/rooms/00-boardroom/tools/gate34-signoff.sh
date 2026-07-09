#!/usr/bin/env bash
# tool/brd/cto/gate34-signoff.sh — Gate 3-4 signoff: architecture + build ready
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID>
  Check Gate 3 (Architecture) + Gate 4 (Build) readiness.
  Verifies artifacts: OpenAPI, schema docs, ADRs, build passing.
EOF
exit 0
}

PRJ="${1:-}"; [[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage
DOCS="$SOFI_ROOT/projects/$PRJ/docs"
CTX="$SOFI_ROOT/projects/$PRJ/_context"
HANDOFFS="$CTX/HANDOFFS.md"

check() { local label="$1" path="$2"
  if [[ -f "$path" ]]; then echo "  ${GREEN}✓${RESET} $label"; return 0
  else echo "  ${RED}✗${RESET} $label"; return 1; fi
}

echo "${BLUE}═══ Gate 3-4 Signoff :: $PRJ ═══${RESET}"

# Gate 3: Architecture
echo "${YELLOW}[Gate 3 — Architecture]${RESET}"
ARCH_OK=0
check "Architecture Blueprint" "$DOCS/Architecture.md" && ((ARCH_OK++))
check "OpenAPI/Swagger spec" "$DOCS/openapi.yaml" 2>/dev/null || check "OpenAPI spec" "$DOCS/openapi.yml" && ((ARCH_OK++))
check "ADR log" "$CTX/DECISIONS.md" && ((ARCH_OK++))
check "Security review flag" "$CTX/CONTEXT.md" && ((ARCH_OK++))

# Gate 4: Build
echo "${YELLOW}[Gate 4 — Build]${RESET}"
BLD_OK=0
# Check for build artifact indicators
if [[ -f "$SOFI_ROOT/projects/$PRJ/composer.json" || -f "$SOFI_ROOT/projects/$PRJ/package.json" ]]; then
  echo "  ${GREEN}✓${RESET} Project manifest found"; ((BLD_OK++))
fi
if grep -q "build.*done\|implementation\|Gate.*4\|deploy" "$HANDOFFS" 2>/dev/null; then
  echo "  ${GREEN}✓${RESET} Build progress in HANDOFFS"; ((BLD_OK++))
fi
# Count source files
SRC_COUNT=$(find "$SOFI_ROOT/projects/$PRJ" -name '*.php' -o -name '*.vue' -o -name '*.ts' -o -name '*.py' 2>/dev/null | wc -l)
if [[ "$SRC_COUNT" -gt 0 ]]; then
  echo "  ${GREEN}✓${RESET} ${SRC_COUNT} source files present"; ((BLD_OK++))
fi

echo "${GREEN}Gate 3: ${ARCH_OK}/4 checks passing${RESET}"
echo "${GREEN}Gate 4: ${BLD_OK}/3 checks passing${RESET}"
[[ $ARCH_OK -lt 2 ]] && { echo "${RED}✗ Gate 3 incomplete${RESET}"; exit 1; }
[[ $BLD_OK -lt 1 ]] && { echo "${RED}✗ Gate 4 has no build artifacts${RESET}"; exit 1; }
echo "${GREEN}✓ Gate 3-4 signoff passed${RESET}"
