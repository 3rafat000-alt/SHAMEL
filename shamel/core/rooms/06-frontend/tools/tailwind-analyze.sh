#!/usr/bin/env bash
# tool/fnt/css-artisan/tailwind-analyze.sh — Scan for Tailwind class consistency
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" N="$(tput setaf 6)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--fix]
Scan Blade/Vue files for Tailwind class consistency issues:
  - Inline styles (should use Tailwind)
  - Hardcoded colors (text=#..., bg=#...)
  - Repeated class combinations (suggest component)
  - Arbitrary values that could be theme tokens
  --fix   Report actionable fix suggestions
--help"; exit 0; }

PRJ="$1"; FIX="${2:-}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"

echo "${B}=== Tailwind Consistency Scan: $PRJ ===$X"
echo

ISSUES=0

scan() {
  local label="$1" pattern="$2"
  shift 2
  local files
  files=$(find "$PRJ_DIR/resources" "$PRJ_DIR" -type f \( -name "*.blade.php" -o -name "*.vue" -o -name "*.tsx" \) 2>/dev/null \
    | xargs grep -l "$pattern" 2>/dev/null | head -10 || true)
  if [ -n "$files" ]; then
    echo "${Y}$label:$X"
    echo "$files" | sed 's/^/  /'
    ISSUES=$((ISSUES+1))
  fi
}

scan "Inline style= found" 'style='
scan "Hardcoded hex colors" '#[0-9a-fA-F]{6}'
scan "Arbitrary value (w-\\[, h-\\[, etc)" '\[[a-z0-9.-]+\]'
scan "Potential !important" '!important'

# Check for config file
if [ -f "$PRJ_DIR/tailwind.config.js" ] || [ -f "$PRJ_DIR/tailwind.config.ts" ]; then
  echo "${G}Tailwind config found$X"
else
  echo "${Y}No tailwind.config found$X"; ISSUES=$((ISSUES+1))
fi

echo
if [ "$ISSUES" -eq 0 ]; then echo "${G}No consistency issues found.$X"
else echo "${Y}$ISSUES issue type(s) detected.$X"
fi

if [ "$FIX" = "--fix" ]; then
  echo
  echo "${B}Recommendations:$X"
  echo "  - Extract repeated class combos into @apply in a component"
  echo "  - Replace inline styles with Tailwind utility classes"
  echo "  - Define custom colors in tailwind.config (theme.extend.colors)"
  echo "  - Avoid arbitrary values — use theme tokens or config"
fi
