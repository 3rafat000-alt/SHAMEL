#!/usr/bin/env bash
# tool/bck/code-reviewer/diff-review.sh — Extract changed lines, flag SQL/security patterns
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" M="$(tput setaf 5)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [base-branch]
Review diff against base branch. Flags:
  - Raw SQL queries (DB::raw, DB::statement)
  - Potential N+1 queries
  - TODO/FIXME/HACK comments
  - Hardcoded secrets
  - Missing validation
  - Unsafe mass assignment
  base-branch  Default: main
--help"; exit 0; }

PRJ="$1"; BASE="${2:-main}"
[ "$PRJ" = "--help" ] && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
cd "$PRJ_DIR"

echo "${B}=== Diff Review: $PRJ (base: $BASE) ===$X"
echo

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  echo "${Y}Not a git repo$X"; exit 1
fi

DIFF=$(git diff "$BASE"...HEAD 2>/dev/null || git diff "$BASE" 2>/dev/null)
[ -z "$DIFF" ] && echo "${Y}No diff found against $BASE$X" && exit 0

echo "${B}Files changed:$X"
git diff "$BASE" --name-status 2>/dev/null | head -20
echo

score() { echo "${B}$1:$X $2"; }

FLAGS=0

# Raw SQL
RAW=$(echo "$DIFF" | grep -n "DB::raw\|DB::statement\|->raw(" || true)
if [ -n "$RAW" ]; then
  echo "${R}[SECURITY] Raw SQL detected:$X"; echo "$RAW"; FLAGS=$((FLAGS+1))
fi

# N+1
NPLUS=$(echo "$DIFF" | grep -n "::all()\|->load(\|->withCount(" || true)
[ -n "$NPLUS" ] && echo "${Y}[N+1] Possible lazy load:$X" && echo "$NPLUS" && FLAGS=$((FLAGS+1))

# TODOs
TODOS=$(echo "$DIFF" | grep -n "TODO\|FIXME\|HACK\|XXX" || true)
[ -n "$TODOS" ] && echo "${M}[DEBT] TODO/HACK found:$X" && echo "$TODOS" && FLAGS=$((FLAGS+1))

# Secrets
SECRETS=$(echo "$DIFF" | grep -ni "password\|secret\|api_key\|SECRET\|PASSWORD" | grep -v ".env\|config(" || true)
[ -n "$SECRETS" ] && echo "${R}[SECURITY] Possible secret in code:$X" && echo "$SECRETS" && FLAGS=$((FLAGS+1))

# Mass assignment
MASS=$(echo "$DIFF" | grep -n "fill(\|create(\|update(" | grep -v "Request\|validated" || true)
[ -n "$MASS" ] && echo "${Y}[WARN] Mass assignment without validated():$X" && echo "$MASS" && FLAGS=$((FLAGS+1))

echo
if [ "$FLAGS" -eq 0 ]; then echo "${G}No significant issues flagged.$X"
else echo "${Y}$FLAGS issue(s) flagged. Review each before merging.$X"; fi
