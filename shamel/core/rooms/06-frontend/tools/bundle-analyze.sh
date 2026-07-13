#!/usr/bin/env bash
# tool/fnt/performance-engineer/bundle-analyze.sh — Check bundle size budgets
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--budget <kb>]
Check compiled JS/CSS bundle sizes against budget.
  --budget  Max total bundle size in KB (default: 300)
  --json    Output JSON for CI
  --help"; exit 0; }

PRJ="$1"; BUDGET="300"; JSON=""
shift || true
while [ $# -gt 0 ]; do
  case "$1" in --budget) BUDGET="$2"; shift;; --json) JSON=1;; *) ;;
  esac; shift
done
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"

echo "${B}=== Bundle Size Analysis: $PRJ ===$X"
echo

TOTAL=0
report() {
  local label="$1" file="$2"
  if [ -f "$file" ]; then
    size=$(stat -c%s "$file" 2>/dev/null || stat -f%z "$file" 2>/dev/null || echo 0)
    kb=$((size/1024))
    TOTAL=$((TOTAL+kb))
    if [ "$kb" -gt $((BUDGET/2)) ]; then
      echo "${Y}${label}: ${kb}KB${X} (large)"
    else
      echo "${G}${label}: ${kb}KB${X}"
    fi
  fi
}

report "JS bundle" "$PRJ_DIR/public/build/assets/app.js"
report "CSS bundle" "$PRJ_DIR/public/build/assets/app.css"
report "Vendor JS" "$PRJ_DIR/public/build/assets/vendor.js"

# Also check package.json for heavy deps
if [ -f "$PRJ_DIR/package.json" ]; then
  echo
  echo "${B}Heavy dependencies (package.json):$X"
  jq -r '.dependencies | to_entries[] | "\(.key): \(.value)"' "$PRJ_DIR/package.json" 2>/dev/null | head -10 || \
    grep "\"react\|"vue\|"lodash\|"axios\|"chart" "$PRJ_DIR/package.json" 2>/dev/null | head -5 | sed 's/^/  /'
fi

echo
echo "${B}Total bundled: ${TOTAL}KB / ${BUDGET}KB budget$X"
if [ "$TOTAL" -gt "$BUDGET" ]; then
  echo "${R}BUDGET EXCEEDED by $((TOTAL-BUDGET))KB${X}"
  exit 1
else
  echo "${G}Within budget ($((BUDGET-TOTAL))KB remaining)${X}"
fi

[ -n "$JSON" ] && echo "{\"total_kb\":$TOTAL,\"budget_kb\":$BUDGET,\"within_budget\":$([ "$TOTAL" -le "$BUDGET" ] && echo true || echo false)}"
