#!/usr/bin/env bash
# tool/knw/historian/adr-log.sh — Generate ADR index from DECISIONS.md
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--output adr-index.md] [--format table|json]"; exit 0; }
PRJ=""; OUTPUT=""; FORMAT="table"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --format) FORMAT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
DECISIONS="$SOFI_ROOT/projects/$PRJ/_context/DECISIONS.md"

echo "${BLUE}[adr-log]${RESET} ADR index for $PRJ"; echo ""

if [[ ! -f "$DECISIONS" ]]; then
  echo "${YELLOW}  No DECISIONS.md at $DECISIONS${RESET}"
  echo "  Creating empty ADR log ..."
  echo "# Architecture Decision Records: $PRJ" > "$DECISIONS"
  echo "" >> "$DECISIONS"
  echo "| # | Date | Decision | Status |" >> "$DECISIONS"
  echo "|---|------|----------|--------|" >> "$DECISIONS"
  echo "${GREEN}  Created $DECISIONS${RESET}"
fi

echo "${YELLOW}  Parsing ADR entries from DECISIONS.md${RESET}"
echo ""

entries=$(grep -nE "^\|.*\|" "$DECISIONS" 2>/dev/null | grep -v "#\|---" || true)
count=$(echo "$entries" | grep -c . || echo 0)

if [[ "$count" -eq 0 ]]; then
  echo "  No ADR entries found."
else
  if [[ "$FORMAT" == "table" ]]; then
    while IFS= read -r line; do
      echo "  $line"
    done < <(echo "$entries")
  elif [[ "$FORMAT" == "json" ]]; then
    echo "  {"
    echo '    "project": "'"$PRJ"'",'
    echo '    "adr_count": '"$count",','
    echo '    "entries": ['
    local first=true
    while IFS='|' read -r num date decision status rest; do
      $first || echo ","
      echo -n "      {\"num\":\"${num// /}\",\"date\":\"${date// /}\",\"decision\":\"${decision// /}\",\"status\":\"${status// /}\"}"
      first=false
    done < <(echo "$entries" | grep -v "^--" || true)
    echo ""
    echo "    ]"
    echo "  }"
  fi
fi

echo ""
echo "  ${BLUE}Total ADRs: $count${RESET}"

if [[ -n "$OUTPUT" ]]; then
  {
    echo "# ADR Index: $PRJ"
    echo "Source: $DECISIONS"
    echo "Generated: $(date -Iseconds)"
    echo ""
    echo "$entries"
  } > "$OUTPUT"
  echo "${BLUE}[adr-log] Written to $OUTPUT${RESET}"
fi

echo "${GREEN}[adr-log] Done.${RESET}"
