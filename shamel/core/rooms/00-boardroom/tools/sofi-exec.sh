#!/usr/bin/env bash
# tool/brd/ceo/sofi-exec.sh — Executive command center: sync + route stamp + gate check
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PROJECTS_DIR="${SOFI_ROOT}/projects"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--check-gate <N>]
  Execute sync, stamp current route, optionally gate-check.
  Reads STATE.md, stamps head_sha, prints project status.
  --check-gate N   Also run adversarial gate check (2|3|4|5)
EOF
exit 0
}

PRJ="${1:-}"; GATE=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage
shift || true
[[ "${1:-}" == "--check-gate" ]] && { GATE="${2:-}"; [[ -z "$GATE" ]] && usage; }

STATE="$PROJECTS_DIR/$PRJ/_context/STATE.md"
[[ ! -f "$STATE" ]] && { echo "${RED}✗ STATE.md not found for $PRJ${RESET}"; exit 1; }

echo "${BLUE}═══ SOFI EXEC :: $PRJ ═══${RESET}"
echo "${YELLOW}[sync]${RESET} $(git log --oneline -1 2>/dev/null || echo 'no commits')"
grep -E '^(gate|branch|head_sha|status)' "$STATE" 2>/dev/null | while IFS= read -r line; do
  key="${line%%:*}"
  val="${line#*: }"
  echo "  ${BLUE}${key}${RESET}: ${GREEN}${val}${RESET}"
done

if [[ -n "$GATE" ]]; then
  echo "${YELLOW}[gate-check G$GATE]${RESET} running..."
  GATE_SCRIPT="${SOFI_ROOT}/tools/gtw/gatekeeper/gate-check.sh"
  if [[ -f "$GATE_SCRIPT" ]]; then
    bash "$GATE_SCRIPT" "$PRJ" "$GATE"
  else
    echo "${RED}gate-check.sh not found${RESET}"
    exit 1
  fi
fi

echo "${GREEN}✓ exec complete${RESET}"
