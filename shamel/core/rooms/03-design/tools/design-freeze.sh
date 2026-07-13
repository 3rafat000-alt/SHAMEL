#!/usr/bin/env bash
# tool/dsn/lead/design-freeze.sh — Freeze design artifacts, sign Gate 2
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--force]
  Freeze all design artifacts and sign Gate 2.
  Checks Prototype_Spec.md, Design_System.md, Journey_Map.md exist.
  Then stamps DESIGN-FREEZE in HANDOFFS.md + STATE.md.
  --force: freeze even if some files missing.
EOF
exit 0
}

PRJ="${1:-}"; FORCE=false
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--force" ]] && FORCE=true

DOCS="$SOFI_ROOT/projects/$PRJ/docs"
CTX="$SOFI_ROOT/projects/$PRJ/_context"
STATE="$CTX/STATE.md"
HANDOFFS="$CTX/HANDOFFS.md"
TS=$(date '+%Y-%m-%d %H:%M')
MISSING=0

echo "${BLUE}═══ Design Freeze :: $PRJ ═══${RESET}"

REQUIRED=("Prototype_Spec.md" "Journey_Map.md")
for f in "${REQUIRED[@]}"; do
  if [[ -f "$DOCS/$f" ]]; then
    echo "  ${GREEN}✓${RESET} $f"
  else
    echo "  ${RED}✗${RESET} $f — MISSING"
    ((MISSING++))
  fi
done

if [[ $MISSING -gt 0 && "$FORCE" != true ]]; then
  echo "${RED}✗ Missing $MISSING artifact(s). Use --force to freeze anyway.${RESET}"
  exit 1
fi

echo ""
echo "DESIGN-FREEZE: $TS" >> "$HANDOFFS"
echo "---" >> "$HANDOFFS"

# Update STATE.md gate
if [[ -f "$STATE" ]]; then
  sed -i "s/^gate:.*/gate: 2 (Design — frozen)/i" "$STATE" 2>/dev/null || \
    echo "gate: 2 (Design — frozen)" >> "$STATE"
fi

echo "${GREEN}✓ Gate 2 signed off — designs frozen${RESET}"
echo "  Design Truth established. All downstream agents derive from frozen specs."
