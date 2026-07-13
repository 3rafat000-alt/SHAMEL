#!/usr/bin/env bash
# tool/str/market-analyst/tam-calc.sh — TAM/SAM/SOM calculator
set -euo pipefail
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") --total-addressable <N> --serviceable <N> --obtainable <N>
  Calculate TAM / SAM / SOM from inputs.
  All numbers in same unit (users or $).
  --total-addressable TAM   Total market size
  --serviceable SAM         Segment you can serve
  --obtainable SOM          Realistic capture target
EOF
exit 0
}

TAM=""; SAM=""; SOM=""
while [[ $# -gt 0 ]]; do
  case "$1" in --total-addressable) TAM="$2"; shift;; --serviceable) SAM="$2"; shift;;
  --obtainable) SOM="$2"; shift;; --help) usage;; *) echo "Unknown: $1"; usage;; esac; shift
done
[[ -z "$TAM" || -z "$SAM" || -z "$SOM" ]] && usage

echo "${BLUE}══════════════════════════════════════${RESET}"
echo "${BLUE}  TAM / SAM / SOM Calculator${RESET}"
echo "${BLUE}══════════════════════════════════════${RESET}"
printf "  ${YELLOW}%-20s${RESET} %'15s\n" "TAM (Total Addressable)" "$TAM"
printf "  ${YELLOW}%-20s${RESET} %'15s\n" "SAM (Serviceable)" "$SAM"
printf "  ${YELLOW}%-20s${RESET} %'15s\n" "SOM (Obtainable)" "$SOM"
printf "  ${YELLOW}%-20s${RESET} %'14.1f%%\n" "SAM as % of TAM" "$(echo "scale=2; $SAM*100/$TAM" | bc 2>/dev/null || echo "?")"
printf "  ${YELLOW}%-20s${RESET} %'14.1f%%\n" "SOM as % of SAM" "$(echo "scale=2; $SOM*100/$SAM" | bc 2>/dev/null || echo "?")"
echo "${BLUE}══════════════════════════════════════${RESET}"
