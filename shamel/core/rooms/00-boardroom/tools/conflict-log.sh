#!/usr/bin/env bash
# tool/brd/arbiter/conflict-log.sh — Log design-vs-dev dispute, emit ADR
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --title "<desc>" --design "<viewpoint>" --dev "<viewpoint>" [--resolution "<decision>"]
  Log a design-vs-development dispute and ADR.
  Appends to DECISIONS.md and HANDOFFS.md.
EOF
exit 0
}

PRJ="${1:-}"; TITLE=""; DESIGN=""; DEV=""; RES=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --title) TITLE="$2"; shift;; --design) DESIGN="$2"; shift;;
  --dev) DEV="$2"; shift;; --resolution) RES="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$TITLE" || -z "$DESIGN" || -z "$DEV" ]] && usage

DECISIONS="$SOFI_ROOT/projects/$PRJ/_context/DECISIONS.md"
HANDOFFS="$SOFI_ROOT/projects/$PRJ/_context/HANDOFFS.md"
TS=$(date '+%Y-%m-%d %H:%M')
TID="ADR-$(date '+%Y%m%d%H%M')"

DISPUTE=$(cat <<ADR

## $TID — Conflict: $TITLE
- **Date:** $TS
- **Arbiter:** brd-arbiter
- **Design position:** $DESIGN
- **Dev position:** $DEV
- **Resolution:** ${RES:-pending — see HANDOFFS}
- **Doctrine invoked:** Teaching I (Design is Truth) — Design wins unless safety/cost forbids.
ADR
)

echo "$DISPUTE" >> "$DECISIONS"
echo "${GREEN}✓ ADR logged: $TID${RESET}"

if [[ -z "$RES" ]]; then
  TICKET="[TKT-${TID}] Conflict: $TITLE — resolve between dsn-lead and fnt-lead (unresolved)"
  echo "## Pending conflict

- **$TID** — $TITLE: $DESIGN vs $DEV
  → Requires CEO resolution. Doctrine: Design is Truth (Teaching I).
  → Escalate if unresolved after 1 round." >> "$HANDOFFS"
  echo "${YELLOW}⚠ Unresolved — escalation ticket written to HANDOFFS${RESET}"
fi

echo "${GREEN}✓ Conflict logged: $TITLE${RESET}"
