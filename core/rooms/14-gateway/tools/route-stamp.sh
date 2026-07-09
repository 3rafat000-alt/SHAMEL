#!/usr/bin/env bash
# tool/gtw/router/route-stamp.sh — Log caveman level + effort before every call
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); MAGENTA=$(tput setaf 5); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --role <agent-role> [--caveman <off|lite|full|ultra>] [--effort <low|medium|high|max>]
  Stamp and log routing decision.
  Model: claude (session model).
  Logs to projects/<PRJ>/_context/ROUTE_LOG.md.
EOF
exit 0
}

PRJ="${1:-}"; ROLE=""; CAVEMAN=""; EFFORT=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --role) ROLE="$2"; shift;; --caveman) CAVEMAN="$2"; shift;;
  --effort) EFFORT="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$ROLE" ]] && usage

ROUTE_LOG="$SOFI_ROOT/projects/$PRJ/_context/ROUTE_LOG.md"

: "${CAVEMAN:=lite}" "${EFFORT:=medium}"

STAMP=$(cat <<STAMP

## Route Stamp: $(date '+%Y-%m-%d %H:%M')
| Field | Value |
|-------|-------|
| **Role** | $ROLE |
| **Model** | claude (session model) |
| **Caveman** | $CAVEMAN |
| **Effort** | $EFFORT |

STAMP
)

echo "$STAMP" >> "$ROUTE_LOG"
echo "${MAGENTA}═══ Route Stamp ═══${RESET}"
echo "  ${BLUE}Role${RESET}:    $ROLE"
echo "  ${GREEN}Model${RESET}:   claude (session model)"
echo "  ${YELLOW}Caveman${RESET}: $CAVEMAN"
echo "  ${YELLOW}Effort${RESET}:  $EFFORT"
echo "${GREEN}✓ Stamped to ${ROUTE_LOG}${RESET}"
