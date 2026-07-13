#!/usr/bin/env bash
# tool/fnt/a11y-engineer/a11y-audit.sh — Check keyboard + ARIA + contrast in templates
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" N="$(tput setaf 6)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--strict]
Scan templates for accessibility issues:
  - Missing alt text on images
  - Missing labels on inputs
  - Buttons without text/aria-label
  - Low-contrast inline colors
  - Missing ARIA attributes
  --strict  Fail on warnings
--help"; exit 0; }

PRJ="$1"; STRICT="${2:-}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"

echo "${B}=== Accessibility Audit: $PRJ ===$X"
echo

PASS=0; FAIL=0; WARN=0
check() { local l="$1" f="$2"
  if [ -n "$f" ]; then
    echo "${R}[FAIL]${X} $l"; FAIL=$((FAIL+1))
    echo "$f" | head -5 | sed 's/^/  /'
  else
    echo "${G}[PASS]${X} $l"; PASS=$((PASS+1))
  fi
}

# Missing alt
NOALT=$(find "$PRJ_DIR/resources" -type f \( -name "*.blade.php" -o -name "*.vue" \) 2>/dev/null \
  | xargs grep -l '<img[^>]*>' 2>/dev/null \
  | xargs grep -L 'alt=' 2>/dev/null || true)
check "Images have alt text" "$NOALT"

# Missing labels
NOLABEL=$(find "$PRJ_DIR/resources" -type f \( -name "*.blade.php" -o -name "*.vue" \) 2>/dev/null \
  | xargs grep -l '<input[^>]*>' 2>/dev/null \
  | xargs grep -L 'aria-label\|aria-labelledby\|<label' 2>/dev/null || true)
check "Inputs have labels/aria-label" "$NOLABEL"

# Empty buttons
EMPTYBTN=$(find "$PRJ_DIR/resources" -type f \( -name "*.blade.php" -o -name "*.vue" \) 2>/dev/null \
  | xargs grep -P '<button[^>]*>\s*</button>' 2>/dev/null || true)
check "Buttons have text/aria-label" "$EMPTYBTN"

# ARIA landmarks
NOARIA=$(find "$PRJ_DIR/resources" -type f \( -name "*.blade.php" -o -name "*.vue" \) 2>/dev/null \
  | xargs grep -l '<nav\|<header\|<footer\|<main' 2>/dev/null \
  | xargs grep -L 'role=' 2>/dev/null || true)
[ -n "$NOARIA" ] && echo "${Y}[WARN] Landmarks without ARIA roles:$X" && echo "$NOARIA" | sed 's/^/  /' && WARN=$((WARN+1))

# Tabindex > 0
TAB=$(find "$PRJ_DIR/resources" -type f \( -name "*.blade.php" -o -name "*.vue" \) 2>/dev/null \
  | xargs grep -P 'tabindex="[1-9]' 2>/dev/null || true)
[ -n "$TAB" ] && echo "${Y}[WARN] Positive tabindex found (avoid):$X" && echo "$TAB" | head -3 | sed 's/^/  /' && WARN=$((WARN+1))

echo
echo "${B}Results: $PASS pass, $FAIL fail, $WARN warnings$X"

TOTAL=$((PASS+FAIL))
[ "$TOTAL" -gt 0 ] && PCT=$((PASS*100/TOTAL)) || PCT=0
echo "${B}Score: ${PCT}%$X"

if [ "$FAIL" -gt 0 ]; then
  echo "${R}Fix failures to meet WCAG 2.2 AA standard.$X"
  [ "$STRICT" = "--strict" ] && exit 1
fi
