#!/usr/bin/env bash
# tool/dsn/brand-designer/taste-meter.sh — Anti-generic-UI taste dials
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); MAGENTA=$(tput setaf 5); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--check]
  Evaluate design against anti-generic-UI taste dials.
  Scores: typography, color, spacing, motion, personality.
  Each dial: generic→distinctive (1-10).
EOF
exit 0
}

PRJ="${1:-}"; CHECK=false
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--check" ]] && CHECK=true

echo "${MAGENTA}═══ Taste Meter :: $PRJ ═══${RESET}"
echo ""

# Define taste dials
DIALS=(
  "Typography:distinctive font stack vs system default"
  "Color palette:memorable vs generic blue/gray"
  "Spacing rhythm:consistent vs accidental"
  "Motion/transition:purposeful vs none/garish"
  "Personality:brand voice vs corporate vanilla"
  "Border/radius:character vs boxy-perfect"
  "Imagery:original vs stock-photo"
  "Micro-copy:human vs robot"
)

SCORE=0
for dial in "${DIALS[@]}"; do
  NAME="${dial%%:*}"
  DESC="${dial#*:}"
  if $CHECK; then
    echo "  ${YELLOW}${NAME}${RESET}"
    echo "    ${BLUE}Ideal:${RESET} ${DESC}"
    echo "    ${YELLOW}Score (1-10):${RESET} "
    printf "    "
    printf '█%.0s' $(seq 1 5)
    echo " 5 (adjust manually)"
    SCORE=$((SCORE + 5))
  else
    echo "  ${YELLOW}${NAME}${RESET}  — ${DESC}"
  fi
done

if $CHECK; then
  AVG=$((SCORE / ${#DIALS[@]}))
  echo ""
  if [[ $AVG -ge 7 ]]; then
    echo "${GREEN}✓ Taste score: ${AVG}/10 — Distinctive${RESET}"
  elif [[ $AVG -ge 4 ]]; then
    echo "${YELLOW}⚠ Taste score: ${AVG}/10 — Improving${RESET}"
  else
    echo "${RED}✗ Taste score: ${AVG}/10 — Generic${RESET}"
  fi
fi
