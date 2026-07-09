#!/usr/bin/env bash
# tool/str/monetization-strategist/pyramid.sh — Generate value metric + pricing tiers
set -euo pipefail
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); MAGENTA=$(tput setaf 5); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") --product "<name>" --metric "<unit>" [--tiers "<t1,t2,t3,t4>"] [--prices "<p1,p2,p3,p4>"]
  Generate pricing pyramid from value metric and tier names.
  Default: Free / Starter / Pro / Enterprise
EOF
exit 0
}

PRODUCT=""; METRIC=""; TIERS="Free,Starter,Pro,Enterprise"; PRICES="\$0,\$29,\$99,\$299"
while [[ $# -gt 0 ]]; do
  case "$1" in --product) PRODUCT="$2"; shift;; --metric) METRIC="$2"; shift;;
  --tiers) TIERS="$2"; shift;; --prices) PRICES="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$PRODUCT" || -z "$METRIC" ]] && usage

IFS=',' read -ra TARR <<< "$TIERS"
IFS=',' read -ra PARR <<< "$PRICES"

echo "${BLUE}══════════════════════════════════════${RESET}"
echo "${MAGENTA}  Pricing Pyramid: ${PRODUCT}${RESET}"
echo "${BLUE}══════════════════════════════════════${RESET}"
echo "${YELLOW}  Value Metric:${RESET} ${METRIC}"
echo ""

for i in "${!TARR[@]}"; do
  tier="${TARR[$i]}"
  price="${PARR[$i]:-\$$((i * 50))}"
  bar=""
  for ((j=0; j<=i; j++)); do bar="${bar}■"; done
  printf "  %-3s %-15s %-10s  %s\n" "$((i+1))" "$tier" "$price" "$bar"
done

echo ""
echo "${GREEN}✓ Pricing pyramid generated${RESET}"
echo "${YELLOW}→ Value metric:${RESET} charge per ${METRIC} consumed"
echo "${YELLOW}→ Gating:${RESET} lower tiers cap ${METRIC}; higher tiers unlock"
