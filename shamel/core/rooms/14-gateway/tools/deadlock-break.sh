#!/usr/bin/env bash
# tool/gtw/conflict-resolver/deadlock-break.sh — Inter-room deadlock triage
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --room-a <room> --room-b <room> --issue "<desc>"
  Resolve inter-room deadlock by documenting positions and escalating.
  Logs deadlock, writes escalation ticket, suggests resolution path.
EOF
exit 0
}

PRJ="${1:-}"; ROOM_A=""; ROOM_B=""; ISSUE=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --room-a) ROOM_A="$2"; shift;; --room-b) ROOM_B="$2"; shift;;
  --issue) ISSUE="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$ROOM_A" || -z "$ROOM_B" || -z "$ISSUE" ]] && usage

HANDOFFS="$SOFI_ROOT/projects/$PRJ/_context/HANDOFFS.md"
TS=$(date '+%Y-%m-%d %H:%M')
DL_ID="DL-$(date '+%Y%m%d%H%M')"

cat <<DEADLOCK >> "$HANDOFFS"

## $DL_ID — Deadlock: $ROOM_A ⚔ $ROOM_B
- **Date:** $TS
- **Rooms:** $ROOM_A ↔ $ROOM_B
- **Issue:** $ISSUE
- **Triaged by:** gtw-conflict-resolver
- **Resolution path:**
  1. Room leads meet (gtw-facilitated)
  2. Document both positions in DECISIONS.md
  3. If no resolution → escalate to brd-arbiter
- **Status:** ⏳ unresolved

DEADLOCK

echo "${BLUE}═══ Deadlock Triage ═══${RESET}"
echo "  ${YELLOW}ID:${RESET}     $DL_ID"
echo "  ${YELLOW}Rooms:${RESET}  $ROOM_A ↔ $ROOM_B"
echo "  ${YELLOW}Issue:${RESET}  $ISSUE"
echo ""
echo "${YELLOW}Path:${RESET} leads meet → DECISIONS.md → escalate to brd-arbiter"
echo "${GREEN}✓ Deadlock logged to HANDOFFS${RESET}"
