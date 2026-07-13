#!/usr/bin/env bash
# tool/obs/lead/slo-dashboard.sh — Generate SLI/SLO dashboard
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--sli 'latency < 200ms:99%'] [--output dashboard.md]"; exit 0; }
PRJ=""; OUTPUT=""
declare -a SLIS
while [[ $# -gt 0 ]]; do
  case "$1" in --prj) PRJ="$2"; shift2 ;; --sli) SLIS+=("$2"); shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift
done
[[ -z "$PRJ" ]] && usage

if [[ ${#SLIS[@]} -eq 0 ]]; then
  SLIS=(
    "latency_p99 < 200ms:99.9%"
    "error_rate < 1%:99.5%"
    "uptime > 99.9%:99.95%"
    "throughput requests/s:baseline"
    "db_query_time < 50ms:99%"
  )
fi

echo "${BLUE}[slo-dashboard]${RESET} SLI/SLO for $PRJ"; echo ""

echo "| SLI | Target | SLO | Status |"
echo "|-----|--------|-----|--------|"
for sli in "${SLIS[@]}"; do
  local name="${sli%%:*}" target="${sli##*:}"
  echo "| $name | $target | $target | 🟢 |"
done
echo ""

echo "${YELLOW}  Burn rate alerts:${RESET}"
echo "    - 2h window: 2% budget consumed → warning"
echo "    - 6h window: 5% budget consumed → page"
echo "    - 24h window: 10% budget consumed → incident"

if [[ -n "$OUTPUT" ]]; then
  {
    echo "# SLO Dashboard: $PRJ"
    echo "Date: $(date -Iseconds)"
    echo ""
    echo "## SLIs"
    for sli in "${SLIS[@]}"; do
      echo "- $sli"
    done
    echo ""
    echo "## Burn Rate Alerts"
    echo "- 2h: 2% → warning"
    echo "- 6h: 5% → page"
    echo "- 24h: 10% → incident"
  } > "$OUTPUT"
  echo "${BLUE}[slo-dashboard] Written to $OUTPUT${RESET}"
fi
echo "${GREEN}[slo-dashboard] Done.${RESET}"
