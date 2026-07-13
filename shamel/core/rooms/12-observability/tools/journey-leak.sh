#!/usr/bin/env bash
# tool/obs/insights-analyst/journey-leak.sh — Detect journey leaks from telemetry
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--from-date 2026-07-01] [--journey-map docs/Journey_Map.md] [--logs dir]"; exit 0; }
PRJ=""; FROM_DATE=""; JMAP=""; LOGS=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --from-date) FROM_DATE="$2"; shift2 ;; --journey-map) JMAP="$2"; shift2 ;; --logs) LOGS="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
JMAP="${JMAP:-$PRJ_DIR/docs/Journey_Map.md}"
LOGS="${LOGS:-$PRJ_DIR/storage/logs}"
FROM_DATE="${FROM_DATE:-$(date -d '7 days ago' +%Y-%m-%d)}"

echo "${BLUE}[journey-leak]${RESET} Journey leak detection for $PRJ (since $FROM_DATE)"; echo ""

# Extract journey stages from Journey Map
stages=()
if [[ -f "$JMAP" ]]; then
  while IFS= read -r line; do
    if echo "$line" | grep -qE '^\|.*\|.*\|'; then
      local stage
      stage=$(echo "$line" | cut -d'|' -f2 | xargs)
      [[ -n "$stage" ]] && stages+=("$stage")
    fi
  done < "$JMAP"
fi

if [[ ${#stages[@]} -eq 0 ]]; then
  stages=("landing" "signup" "onboarding" "engagement" "purchase" "retention")
  echo "${YELLOW}  No Journey_Map.md at $JMAP — using default stages${RESET}"
fi

echo "${YELLOW}  Journey stages:${RESET}"
for s in "${stages[@]}"; do echo "    - $s"; done

echo ""
echo "${YELLOW}  Drop-off analysis (from $FROM_DATE):${RESET}"
for ((i=0; i<${#stages[@]}-1; i++)); do
  local from="${stages[$i]}" to="${stages[$i+1]}"
  local from_count to_count
  from_count=$(grep -r "$from" "$LOGS" 2>/dev/null | grep -c "$from" 2>/dev/null || echo 0)
  to_count=$(grep -r "$to" "$LOGS" 2>/dev/null | grep -c "$to" 2>/dev/null || echo 0)
  local drop=0
  if [[ $from_count -gt 0 ]]; then
    drop=$(( (from_count - to_count) * 100 / from_count ))
  fi
  echo "    $from → $to: ${from_count}→${to_count} (drop: ${drop}%)"
  if [[ $drop -gt 50 ]]; then
    echo "      ${RED}⚠ Critical drop-off${RESET}"
  elif [[ $drop -gt 25 ]]; then
    echo "      ${YELLOW}⚠ Significant drop-off — investigate${RESET}"
  fi
done

echo ""
echo "${YELLOW}  Anomaly patterns:${RESET}"
echo "    - 4xx errors in $LOGS: $(find "$LOGS" -name "*.log" -newermt "$FROM_DATE" 2>/dev/null | xargs grep -c ' 4[0-9][0-9] ' 2>/dev/null || echo 0)"
echo "    - 5xx errors in $LOGS: $(find "$LOGS" -name "*.log" -newermt "$FROM_DATE" 2>/dev/null | xargs grep -c ' 5[0-9][0-9] ' 2>/dev/null || echo 0)"

echo "${GREEN}[journey-leak] Done.${RESET}"
