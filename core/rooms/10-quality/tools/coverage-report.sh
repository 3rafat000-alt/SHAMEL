#!/usr/bin/env bash
# tool/qa/automation-engineer/coverage-report.sh — Check test coverage ≥90%
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--threshold 90] [--tool pest|phpunit|pytest|jest]"; exit 0; }
PRJ=""; THRESHOLD=90; TOOL=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --threshold) THRESHOLD="$2"; shift2 ;; --tool) TOOL="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[[ -d "$PRJ_DIR" ]] || { echo "${RED}Error: $PRJ_DIR not found${RESET}"; exit 1; }

echo "${BLUE}[coverage]${RESET} Coverage report for $PRJ (threshold: ${THRESHOLD}%)"; echo ""

# Auto-detect tool
if [[ -z "$TOOL" ]]; then
  if [[ -f "$PRJ_DIR/phpunit.xml" ]] || [[ -f "$PRJ_DIR/phpunit.xml.dist" ]]; then TOOL="phpunit"
  elif [[ -f "$PRJ_DIR/pest.xml" ]] || ls "$PRJ_DIR/tests"/*.php 2>/dev/null | head -1 | grep -q "Pest"; then TOOL="pest"
  elif ls "$PRJ_DIR/pyproject.toml" 2>/dev/null || ls "$PRJ_DIR/requirements.txt" 2>/dev/null; then TOOL="pytest"
  elif ls "$PRJ_DIR/package.json" 2>/dev/null; then TOOL="jest"
  else TOOL="phpunit"; fi
fi

COVERAGE=0
case "$TOOL" in
  phpunit|pest)
    echo "  Running $TOOL with coverage..."
    (cd "$PRJ_DIR" && ./vendor/bin/phpunit --coverage-text 2>/dev/null | grep -oP 'Lines:\s+\K[\d.]+' | tail -1) && COVERAGE=$(cd "$PRJ_DIR" && ./vendor/bin/phpunit --coverage-text 2>/dev/null | grep -oP 'Lines:\s+\K[\d.]+' | tail -1) || true
    ;;
  pytest)
    COVERAGE=$(cd "$PRJ_DIR" && python -m pytest --cov --cov-report=term 2>/dev/null | grep -oP 'TOTAL\s+\d+\s+\d+\s+\K[\d.]+' | tail -1) || true
    ;;
  jest)
    COVERAGE=$(cd "$PRJ_DIR" && npx jest --coverage 2>/dev/null | grep -oP 'Lines\s*:\s*\K[\d.]+' | tail -1) || true
    ;;
esac

COVERAGE="${COVERAGE:-0}"
echo ""
echo "  Coverage: ${COVERAGE}%"
if (( $(echo "$COVERAGE >= $THRESHOLD" | bc -l 2>/dev/null || echo 0) )); then
  echo "${GREEN}[coverage] PASS — ${COVERAGE}% ≥ ${THRESHOLD}%${RESET}"
  exit 0
else
  echo "${RED}[coverage] BLOCK — ${COVERAGE}% < ${THRESHOLD}%${RESET}"
  exit 1
fi
