#!/usr/bin/env bash
# tool/arc/data-architect/schema-map.sh — Map migration → table → columns → indexes
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--json]
Parse database migrations and output table/column/index mapping.
--json   Output as JSON
--help   Show this"; exit 0; }

PRJ="$1"; FORMAT="${2:-table}"
[ "$PRJ" = "--help" ] && usage

MIGR_DIR="$SOFI_ROOT/projects/$PRJ/database/migrations"
[ ! -d "$MIGR_DIR" ] && echo "${R}No migrations at $MIGR_DIR$X" && exit 1

echo "${B}Schema map for $PRJ$X"
echo "---"

for m in "$MIGR_DIR"/*.php; do
  [ ! -f "$m" ] && continue
  fname=$(basename "$m")
  echo "${Y}Migration: $fname$X"
  tables=$(grep -oP "Schema::(create|table)\(['\"]([^'\"]+)['\"]" "$m" 2>/dev/null | cut -d"'" -f2 || true)
  for t in $tables; do
    echo "  ${G}TABLE:${X} $t"
    grep -oP "->([a-z]+)\('([^'\"]+)'" "$m" 2>/dev/null | while read -r line; do
      coltype=$(echo "$line" | cut -d"(" -f1 | sed 's/->//')
      colname=$(echo "$line" | cut -d"'" -f2)
      echo "    ├─ $colname ($coltype)"
    done
    grep -oP "->index\(\[?['\"][^'\"]+['\"]?\]?\)" "$m" 2>/dev/null && echo "    └─ ${B}INDEXED$X" || true
  done
  echo
done

if [ "$FORMAT" = "--json" ]; then
  echo "---"
  echo "${Y}JSON mode: pipe to jq for structured output.$X"
  for m in "$MIGR_DIR"/*.php; do
    [ ! -f "$m" ] && continue
    tables=$(grep -oP "Schema::(create|table)\(['\"]([^'\"]+)['\"]" "$m" 2>/dev/null | cut -d"'" -f2 || true)
    for t in $tables; do
      cols=$(grep -oP "->([a-z]+)\('([^'\"]+)'" "$m" 2>/dev/null | sed "s/.*/'&',/" | tr -d '\n')
      echo "{\"migration\":\"$fname\",\"table\":\"$t\",\"columns\":[$cols]}"
    done
  done
fi
