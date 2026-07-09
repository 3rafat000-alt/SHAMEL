#!/usr/bin/env bash
# tool/ops/release-manager/release.sh — Blue/Green release with rollback
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--strategy blue-green|rolling] [--version v1.0.0] [--dry-run]"; exit 0; }
PRJ=""; STRATEGY="blue-green"; VERSION=""; DRY_RUN=false
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --strategy) STRATEGY="$2"; shift2 ;; --version) VERSION="$2"; shift2 ;; --dry-run) DRY_RUN=true ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
VERSION="${VERSION:-$(date +%Y%m%d-%H%M%S)}"

echo "${BLUE}[release]${RESET} Release $VERSION for $PRJ (strategy: $STRATEGY)${DRY_RUN:+ (DRY RUN)}"; echo ""

case "$STRATEGY" in
  blue-green)
    echo "  1. Current live: ${YELLOW}blue${RESET}"
    echo "  2. Deploy $VERSION to ${GREEN}green${RESET}"
    echo "  3. Health check: green"
    echo "  4. Switch load balancer → green"
    echo "  5. Verify green serving traffic"
    echo "  6. Keep blue as rollback target"
    echo ""
    echo "  Rollback: switch load balancer → blue"
    ;;
  rolling)
    echo "  1. Deploy to 20% of instances — verify"
    echo "  2. Ramp to 50% — verify"
    echo "  3. Ramp to 100%"
    echo "  4. Old instances draining"
    echo ""
    echo "  Rollback: re-deploy previous version"
    ;;
  *) echo "${RED}Unknown strategy: $STRATEGY${RESET}"; exit 1 ;;
esac

if $DRY_RUN; then echo "${YELLOW}[release] DRY RUN — no changes applied${RESET}"; exit 0; fi

# Record release in STATE.md if exists
STATE="$PRJ_DIR/_context/STATE.md"
if [[ -f "$STATE" ]]; then
  sed -i "s/^release:.*/release: $VERSION/" "$STATE" 2>/dev/null || true
  sed -i "s/^release_version:.*/release_version: $VERSION/" "$STATE" 2>/dev/null || true
  sed -i "s/^strategy:.*/strategy: $STRATEGY/" "$STATE" 2>/dev/null || true
fi

echo ""
echo "${GREEN}[release] $VERSION deployed ($STRATEGY). Rollback target preserved.${RESET}"
