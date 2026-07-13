#!/usr/bin/env bash
# tool/dat/db-engineer/migration-consolidate.sh — Consolidate migration files into fewer files
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--dry-run]
Analyze migration files and suggest consolidation grouping by table.
  --dry-run   Only show consolidation plan, don't execute
  --help"; exit 0; }

PRJ="$1"; DRY="${2:-}"
[ "$PRJ" = "--help" ] && usage
MIGR_DIR="$SOFI_ROOT/projects/$PRJ/database/migrations"
[ ! -d "$MIGR_DIR" ] && echo "${R}No migrations at $MIGR_DIR$X" && exit 1

echo "${B}=== Migration Consolidation: $PRJ ===$X"
echo

declare -A TABLE_FILES
for m in "$MIGR_DIR"/*.php; do
  [ ! -f "$m" ] && continue
  tables=$(grep -oP "Schema::(create|table)\(['\"]([^'\"]+)['\"]" "$m" 2>/dev/null | cut -d"'" -f2 || true)
  for t in $tables; do
    TABLE_FILES["$t"]+="$(basename "$m") "
  done
done

CONSOL=0
echo "${Y}Consolidation candidates:$X"
for table in "${!TABLE_FILES[@]}"; do
  files=(${TABLE_FILES[$table]})
  count=${#files[@]}
  if [ "$count" -gt 1 ]; then
    echo "  ${B}$table$X: $count files → can merge into 1"
    for f in "${files[@]}"; do echo "    - $f"; done
    CONSOL=$((CONSOL+1))
  fi
done

[ "$CONSOL" -eq 0 ] && echo "  No consolidation needed (each table has 1 migration)"

# Check total
TOTAL=$(ls "$MIGR_DIR"/*.php 2>/dev/null | wc -l)
echo
echo "${B}Total migrations: $TOTAL files$X"
echo "${B}Consolidation candidates: $CONSOL table(s)$X"

if [ "$DRY" = "--dry-run" ]; then
  echo "${Y}Dry-run only — no files changed.$X"
  echo "To consolidate, merge the above files manually and run:"
  echo "  php artisan migrate:fresh"
fi
