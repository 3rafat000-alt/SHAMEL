#!/usr/bin/env bash
# tool/obs/sre/sli-calc.sh — Calculate SLI from metrics
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --metric latency|error_rate|uptime|throughput [--total 1000] [--good 995] [--window 5m]"; exit 0; }
METRIC=""; TOTAL=0; GOOD=0; WINDOW="5m"
while [[ $# -gt 0 ]]; do case "$1" in --metric) METRIC="$2"; shift2 ;; --total) TOTAL="$2"; shift2 ;; --good) GOOD="$2"; shift2 ;; --window) WINDOW="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$METRIC" ]] && usage

if [[ "$TOTAL" -eq 0 ]]; then
  echo "${YELLOW}Error: --total required (number of requests/events)${RESET}" >&2; exit 1
fi

echo "${BLUE}[sli-calc]${RESET} SLI calculation for $METRIC (window: $WINDOW)"; echo ""
echo "  Total events: $TOTAL"
echo "  Good events:  $GOOD"

SLI=0
BAD=$((TOTAL - GOOD))
if [[ "$TOTAL" -gt 0 ]]; then
  SLI=$(echo "scale=4; $GOOD / $TOTAL * 100" | bc 2>/dev/null || echo 0)
  SLI=$(echo "$SLI" | sed 's/\.$//')
fi

echo "  Bad events:   $BAD"
echo ""
echo "  ${BLUE}SLI = ${SLI}%${RESET}"

case "$METRIC" in
  latency)    echo "  Type: Request latency — good = p99 under threshold" ;;
  error_rate) echo "  Type: Error rate — good = non-5xx responses" ;;
  uptime)     echo "  Type: Uptime — good = successful health checks" ;;
  throughput) echo "  Type: Throughput — good = requests served within capacity" ;;
esac

echo ""
if (($(echo "$SLI >= 99.9" | bc -l 2>/dev/null || echo 0))); then echo "${GREEN}✓ SLI meets 99.9% SLO${RESET}"
elif (($(echo "$SLI >= 99.5" | bc -l 2>/dev/null || echo 0))); then echo "${YELLOW}✓ SLI meets 99.5% SLO${RESET}"
else echo "${RED}✗ SLI below 99.5% SLO — improvement needed${RESET}"; fi
