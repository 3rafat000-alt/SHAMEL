#!/usr/bin/env bash
# tool/knw/memory-curator/brain-compress.sh — Compress brain files (caveman format)
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--file CONTEXT.md|STATE.md|DECISIONS.md] [--backup]"; exit 0; }
PRJ=""; FILE=""; BACKUP=false
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --file) FILE="$2"; shift2 ;; --backup) BACKUP=true ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
CTX="$SOFI_ROOT/projects/$PRJ/_context"

compress_file() {
  local f="$1"
  [[ -f "$f" ]] || { echo "  ${RED}File $f not found${RESET}"; return; }
  if $BACKUP; then
    cp "$f" "${f}.bak"
    echo "  ${YELLOW}Backup: ${f}.bak${RESET}"
  fi

  local tmp
  tmp=$(mktemp)
  local in_frontmatter=false

  while IFS= read -r line; do
    # Preserve frontmatter (--- ... ---)
    if echo "$line" | grep -q "^---"; then
      if $in_frontmatter; then in_frontmatter=false; else in_frontmatter=true; fi
      echo "$line" >> "$tmp"
      continue
    fi
    if $in_frontmatter; then
      echo "$line" >> "$tmp"
      continue
    fi

    # Compress: drop filler words, short lines OK
    local compressed
    compressed=$(echo "$line" | sed -E \
      -e 's/\b(just|really|basically|actually|simply|quite|very|pretty|quite|rather)\b//gi' \
      -e 's/\b(a|an|the)\b//g' \
      -e 's/  +/ /g' -e 's/^ //' -e 's/ $//')
    echo "$compressed" >> "$tmp"
  done < "$f"

  mv "$tmp" "$f"
  echo "  ${GREEN}✓ Compressed $(basename "$f") ($(wc -c < "$f") bytes)${RESET}"
}

echo "${BLUE}[brain-compress]${RESET} Compressing brain files for $PRJ"; echo ""

if [[ -n "$FILE" ]]; then
  compress_file "$CTX/$FILE"
else
  for f in STATE.md CONTEXT.md DECISIONS.md HANDOFFS.md; do
    [[ -f "$CTX/$f" ]] && compress_file "$CTX/$f"
  done
fi

echo ""
echo "${GREEN}[brain-compress] Done.${RESET}"
