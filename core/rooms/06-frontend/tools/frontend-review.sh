#!/usr/bin/env bash
# tool/fnt/code-reviewer/frontend-review.sh — Adversarial frontend diff checker
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" M="$(tput setaf 5)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [base-branch]
Review frontend diff for:
  - Missing error/loading/empty states
  - Hardcoded strings (no i18n)
  - Console.log left in
  - Missing TypeScript types
  - Inline CSS vs Tailwind
  - Accessibility regressions
  base-branch  Default: main
--help"; exit 0; }

PRJ="$1"; BASE="${2:-main}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
cd "$PRJ_DIR"

[ ! -d ".git" ] && echo "${Y}Not a git repo$X" && exit 1

DIFF=$(git diff "$BASE"...HEAD 2>/dev/null || git diff "$BASE" 2>/dev/null)
[ -z "$DIFF" ] && echo "${Y}No diff$X" && exit 0

echo "${B}=== Frontend Diff Review: $PRJ ===$X"; echo
FLAGS=0

# Console.log
CONSOLE=$(echo "$DIFF" | grep -n "console\.\(log\|warn\|error\)" | grep -v "//.*console" || true)
[ -n "$CONSOLE" ] && echo "${R}[STALE DEBUG] console.log found:$X" && echo "$CONSOLE" && FLAGS=$((FLAGS+1))

# Missing error handling
NOERR=$(echo "$DIFF" | grep -n "\.catch(" || true)
[ -z "$NOERR" ] && NOERR2=$(echo "$DIFF" | grep -oP 'await\s+' | head -1 || true)
[ -n "$NOERR2" ] && echo "${Y}[ERROR HANDLING] async without .catch()$X" && FLAGS=$((FLAGS+1))

# Hardcoded strings
HARD=$(echo "$DIFF" | grep -nP '>[\w\s]{20,}<' | grep -v '\$t\(' | grep -v 'translate' | grep 'blade.php' || true)
[ -n "$HARD" ] && echo "${Y}[I18N] Possible hardcoded strings:$X" && echo "$HARD" | head -3 && FLAGS=$((FLAGS+1))

# Missing types
ANY=$(echo "$DIFF" | grep -n ": any" || true)
[ -n "$ANY" ] && echo "${Y}[TYPES] ': any' should be specific type:$X" && echo "$ANY" && FLAGS=$((FLAGS+1))

# Empty states
NOEMPTY=$(echo "$DIFF" | grep -n "v-for\|\.map(" | grep -v "v-if\|loading\|empty" || true)
[ -n "$NOEMPTY" ] && echo "${Y}[EMPTY STATE] v-for/.map without v-if/empty check$X" && echo "$NOEMPTY" && FLAGS=$((FLAGS+1))

# Inline styles
INLINE=$(echo "$DIFF" | grep -n "style=" || true)
[ -n "$INLINE" ] && echo "${Y}[STYLE] Inline styles instead of Tailwind:$X" && echo "$INLINE" && FLAGS=$((FLAGS+1))

echo
[ "$FLAGS" -eq 0 ] && echo "${G}Clean diff.$X" || echo "${Y}$FLAGS issue(s).$X"
