#!/usr/bin/env bash
# tool/str/roadmap-planner/milestones.sh — Generate milestone timeline from gates
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RED=$(tput setaf 1); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--start-date YYYY-MM-DD] [--days-per-gate N]
  Generate milestone timeline from SOFI 9-gate lifecycle.
  Default start: today. Default days per gate: 5.
EOF
exit 0
}

PRJ="${1:-}"; START=""; DPG=5
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --start-date) START="$2"; shift;; --days-per-gate) DPG="$2"; shift;; --help) usage;; esac; shift
done
START="${START:-$(date '+%Y-%m-%d')}"

gates=(
  "0:Inception"
  "1:Discovery"
  "2:Design"
  "3:Architecture"
  "4:Build"
  "5:Quality"
  "6:Staging"
  "7:Production"
  "8:Observe"
)

echo "${BLUE}═══ Milestone Timeline :: $PRJ ═══${RESET}"
echo "${YELLOW}Start:${RESET} $START  |  ${YELLOW}Pace:${RESET} ${DPG}d/gate"
echo ""

for gate in "${gates[@]}"; do
  NUM="${gate%%:*}"
  NAME="${gate#*:}"
  OFFSET=$((NUM * DPG))
  DATE=$(date -d "$START + $OFFSET days" '+%Y-%m-%d' 2>/dev/null || echo "T+${OFFSET}d")
  BAR=$(printf "%${NUM}s" | tr ' ' '▬')
  echo "  ${YELLOW}G${NUM}${RESET} ${DATE}  ${BLUE}${BAR}▶${RESET} ${NAME}"
done

echo ""
echo "${GREEN}✓ Timeline generated${RESET}"
echo "${YELLOW}→ Check:${RESET} who owns each gate? what artifacts gate each?"
