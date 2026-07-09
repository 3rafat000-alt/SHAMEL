#!/usr/bin/env bash
# tool/knw/lead/knowledge-sync.sh — Sync knowledge across memory files
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--check lessons|decisions|state|all] [--dry-run]"; exit 0; }
PRJ=""; CHECK="all"; DRY_RUN=false
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --check) CHECK="$2"; shift2 ;; --dry-run) DRY_RUN=true ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
CTX="$SOFI_ROOT/projects/$PRJ/_context"

echo "${BLUE}[knowledge-sync]${RESET} Syncing knowledge for $PRJ${DRY_RUN:+ (DRY RUN)}"; echo ""
DIRTY=false

sync_file() {
  local name="$1" file="$2" required=${3:-false}
  if [[ -f "$file" ]]; then
    local size
    size=$(wc -l < "$file")
    echo "  ${GREEN}✓ $name ($size lines at $file)${RESET}"
  else
    echo "  ${YELLOW}⚠ $name missing at $file${RESET}"
    $required && DIRTY=true
  fi
}

if [[ "$CHECK" == "all" || "$CHECK" == "state" ]]; then
  echo "${YELLOW}  Brain files:${RESET}"
  sync_file "STATE.md" "$CTX/STATE.md" true
  sync_file "CONTEXT.md" "$CTX/CONTEXT.md" true
  sync_file "HANDOFFS.md" "$CTX/HANDOFFS.md" true
  sync_file "DECISIONS.md" "$CTX/DECISIONS.md" true
fi

if [[ "$CHECK" == "all" || "$CHECK" == "lessons" ]]; then
  echo "${YELLOW}  Learning files:${RESET}"
  sync_file "LESSONS.md" "$CTX/LESSONS.md" false
  sync_file "MEMORY.md" "$SOFI_ROOT/MEMORY.md" false
fi

if [[ "$CHECK" == "all" || "$CHECK" == "decisions" ]]; then
  echo "${YELLOW}  Decision consistency:${RESET}"
  if [[ -f "$CTX/DECISIONS.md" ]]; then
    local decisions
    decisions=$(grep -c "^|" "$CTX/DECISIONS.md" 2>/dev/null || echo 0)
    echo "  ${GREEN}✓ $decisions ADR entries logged${RESET}"
  fi
  if [[ -f "$SOFI_ROOT/engine/DOCTRINE.md" ]]; then
    echo "  ${GREEN}✓ Doctrine loaded ($(wc -l < "$SOFI_ROOT/engine/DOCTRINE.md") lines)${RESET}"
  fi
fi

if $DIRTY; then
  echo "${RED}  Missing required brain files — run 'sofi checkpoint' to seed them${RESET}"
fi

if ! $DRY_RUN; then
  echo ""
  ${DIRTY:+echo "${YELLOW}  Run: sofi checkpoint $PRJ 'knowledge-sync: seed brain files'${RESET}"}
fi

echo "${GREEN}[knowledge-sync] Done.${RESET}"
