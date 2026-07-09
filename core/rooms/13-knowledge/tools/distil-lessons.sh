#!/usr/bin/env bash
# tool/knw/reflector/distil-lessons.sh — Distil HANDOFFS history into LESSONS.md
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--output LESSONS.md] [--max 10]"; exit 0; }
PRJ=""; OUTPUT=""; MAX=10
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --max) MAX="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
CTX="$SOFI_ROOT/projects/$PRJ/_context"
OUTPUT="${OUTPUT:-$CTX/LESSONS.md}"

echo "${BLUE}[distil-lessons]${RESET} Distilling HANDOFFS history for $PRJ"; echo ""

declare -a lessons
declare -a observations
HANDOFFS="$CTX/HANDOFFS.md"
COUNT=0

if [[ -f "$HANDOFFS" ]]; then
  echo "${YELLOW}  Reading $HANDOFFS${RESET}"
  while IFS= read -r line; do
    # Extract "blocked" patterns
    if echo "$line" | grep -qi "blocked\|failure\|error\|bug\|issue\|regression"; then
      observations+=("BLOCKER: $line")
      ((COUNT++))
    fi
    # Extract "fixed" or "resolved" patterns
    if echo "$line" | grep -qi "fixed\|resolved\|solved\|patched"; then
      observations+=("RESOLVED: $line")
      ((COUNT++))
    fi
    # Extract "learned" patterns
    if echo "$line" | grep -qi "learned\|lesson\|insight\|note"; then
      observations+=("LESSON: $line")
      ((COUNT++))
    fi
  done < "$HANDOFFS"

  # Also scan CONTEXT.md for decision patterns
  if [[ -f "$CTX/CONTEXT.md" ]]; then
    while IFS= read -r line; do
      if echo "$line" | grep -qi "decision\|conclusion\|agreed\|chose\|opted"; then
        observations+=("DECISION: $line")
        ((COUNT++))
      fi
    done < "$CTX/CONTEXT.md"
  fi
fi

echo ""
if [[ ${#observations[@]} -eq 0 ]]; then
  echo "  ${YELLOW}No lessons extracted from HANDOFFS.md for $PRJ${RESET}"
  echo "  Pattern: mark entries with 'lesson:', 'learned:', 'insight:'"
fi

# Deduplicate and limit
readarray -t deduped < <(printf "%s\n" "${observations[@]}" | sort -u)
LESSONS_OUT=("${deduped[@]:0:$MAX}")
echo "  ${GREEN}${#deduped[@]} observations found, ${#LESSONS_OUT[@]} written${RESET}"

mkdir -p "$(dirname "$OUTPUT")"
{
  echo "# Lessons Learned: $PRJ"
  echo "**Generated:** $(date -Iseconds)"
  echo "**Source:** HANDOFFS.md + CONTEXT.md"
  echo "---"
  echo ""
  for obs in "${LESSONS_OUT[@]}"; do
    echo "- $obs"
  done
  echo ""
  echo "---"
  echo "_${COUNT} total signals; ${#deduped[@]} unique; top ${#LESSONS_OUT[@]} shown._"
} > "$OUTPUT"

echo "${GREEN}[distil-lessons] Written to $OUTPUT${RESET}"
