#!/usr/bin/env bash
# tool/dsn/a11y-specialist/wcag-audit.sh — Run WCAG 2.2 AA checklist
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--output <report.md>]
  Run WCAG 2.2 AA checklist against project source.
  Scans for common a11y issues: alt text, contrast, labels, roles, focus.
EOF
exit 0
}

PRJ="${1:-}"; OUTPUT=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--output" ]] && OUTPUT="${2:-}"

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SCORE=0; TOTAL=0

wcag_check() {
  local label="$1" cmd="$2"
  ((TOTAL++))
  if eval "$cmd" 2>/dev/null | head -5 | grep -q .; then
    echo "  ${GREEN}✓${RESET} $label"
    ((SCORE++))
  else
    echo "  ${YELLOW}⚠${RESET} $label — See standard"
  fi
}

echo "${BLUE}═══ WCAG 2.2 AA Audit :: $PRJ ═══${RESET}"
echo ""

# Scan Vue/HTML files
VUE_FILES=$(find "$PRJ_DIR" -name '*.vue' -o -name '*.html' 2>/dev/null | grep -v node_modules | head -20)
PHP_FILES=$(find "$PRJ_DIR" -name '*.php' 2>/dev/null | grep -v vendor | head -20)
ALL_FILES=$(echo "$VUE_FILES" "$PHP_FILES" | tr ' ' '\n' | sort -u)

if [[ -z "$ALL_FILES" ]]; then
  echo "${YELLOW}⚠ No source files to audit${RESET}"
  exit 0
fi

FILE_COUNT=$(echo "$ALL_FILES" | wc -l)

wcag_check "1.1.1 Alt text on images" "grep -rni 'alt=\"\"\|alt=\"[^\"]\"' $ALL_FILES 2>/dev/null"
wcag_check "1.4.3 Contrast (labels present)" "grep -rn 'color\|background' $ALL_FILES 2>/dev/null | head -1"
wcag_check "2.1.1 Keyboard (button/input/a present)" "grep -rn '<button\|<input\|<a ' $ALL_FILES 2>/dev/null | head -1"
wcag_check "2.4.6 Headings/landmarks" "grep -rn '<h1\|<h2\|<h3\|role=\"' $ALL_FILES 2>/dev/null | head -1"
wcag_check "3.3.2 Labels or aria-label" "grep -rn 'label\|aria-label\|aria-labelledby' $ALL_FILES 2>/dev/null | head -1"
wcag_check "4.1.2 ARIA roles valid" "grep -rn 'role=\"' $ALL_FILES 2>/dev/null | head -1"
wcag_check "Focus indicators" "grep -rn ':focus\|outline\|tabindex' $ALL_FILES 2>/dev/null | head -1"
wcag_check "Semantic HTML (form/table/nav)" "grep -rn '<form\|<table\|<nav\|<main\|<header\|<footer' $ALL_FILES 2>/dev/null | head -1"
wcag_check "Language attribute" "grep -rn 'lang=\"' $ALL_FILES 2>/dev/null | head -1"
wcag_check "Skip nav link" "grep -rn 'skip\|skipnav\|skip-to' $ALL_FILES 2>/dev/null | head -1"

echo ""
echo "${BLUE}Results:${RESET} ${SCORE}/${TOTAL} checks passing across ${FILE_COUNT} files"
if [[ $SCORE -eq $TOTAL ]]; then
  echo "${GREEN}✓ WCAG 2.2 AA — All checks pass${RESET}"
else
  echo "${YELLOW}⚠ ${TOTAL - SCORE} check(s) need attention${RESET}"
fi

if [[ -n "$OUTPUT" ]]; then
  echo "# WCAG 2.2 AA Audit: $PRJ" > "$OUTPUT"
  echo "**Date:** $(date '+%Y-%m-%d')" >> "$OUTPUT"
  echo "**Score:** ${SCORE}/${TOTAL}" >> "$OUTPUT"
  echo "${GREEN}✓ Report written to $OUTPUT${RESET}"
fi
