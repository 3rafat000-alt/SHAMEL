#!/usr/bin/env bash
# tool/knw/brain-query/brain-search.sh — grep + brain-query hybrid search
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID --query 'search terms' [--context] [--max 10] [--mode grep|brain|hybrid]"; exit 0; }
PRJ=""; QUERY=""; CONTEXT=false; MAX=10; MODE="hybrid"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --query) QUERY="$2"; shift2 ;; --context) CONTEXT=true ;; --max) MAX="$2"; shift2 ;; --mode) MODE="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" || -z "$QUERY" ]] && usage
CTX="$SOFI_ROOT/projects/$PRJ/_context"

echo "${BLUE}[brain-search]${RESET} Searching brain for '$QUERY' (mode: $MODE, max: $MAX)"; echo ""

RESULTS=0
search_grep() {
  local label="$1" target="$2"
  [[ -f "$target" ]] || return
  local matches
  matches=$(grep -in "$QUERY" "$target" 2>/dev/null | head -"$MAX" || true)
  if [[ -n "$matches" ]]; then
    echo "  ${YELLOW}$label:${RESET}"
    while IFS= read -r line; do
      echo "    $(echo "$line" | head -c 120)"
      ((RESULTS++))
    done < <(echo "$matches")
    echo ""
  fi
}

search_grep_dir() {
  local label="$1" dir="$2"
  [[ -d "$dir" ]] || return
  local matches
  matches=$(grep -rni "$QUERY" "$dir" --include="*.md" --include="*.txt" --include="*.yaml" --include="*.json" 2>/dev/null | head -"$MAX" || true)
  if [[ -n "$matches" ]]; then
    echo "  ${YELLOW}$label:${RESET}"
    while IFS= read -r line; do
      echo "    $(echo "$line" | head -c 140)"
      ((RESULTS++))
    done < <(echo "$matches")
    echo ""
  fi
}

if [[ "$MODE" == "grep" || "$MODE" == "hybrid" ]]; then
  search_grep "STATE.md" "$CTX/STATE.md"
  search_grep "CONTEXT.md" "$CTX/CONTEXT.md"
  search_grep "HANDOFFS.md" "$CTX/HANDOFFS.md"
  search_grep "DECISIONS.md" "$CTX/DECISIONS.md"
  search_grep "LESSONS.md" "$CTX/LESSONS.md" 2>/dev/null || true
  search_grep_dir "docs" "$SOFI_ROOT/projects/$PRJ/docs"
fi

if [[ "$MODE" == "hybrid" && $RESULTS -lt 3 ]]; then
  echo "${YELLOW}  → Fallback: searching SOFI protocols${RESET}"
  search_grep_dir "protocols" "$SOFI_ROOT/engine/protocols"
  search_grep_dir "agents" "$SOFI_ROOT/engine/agents"
fi

if [[ "$MODE" == "brain" ]]; then
  echo "${YELLOW}  → Brain-only search (grep on _context/)${RESET}"
  search_grep_dir "brain" "$CTX"
fi

if [[ $RESULTS -eq 0 ]]; then
  echo "  ${YELLOW}No results for '$QUERY' in brain files${RESET}"
  echo "  Try broader query or add information to CONTEXT.md"
fi

echo "${BLUE}[brain-search]${RESET} ${GREEN}Done — $RESULTS result(s)${RESET}"
