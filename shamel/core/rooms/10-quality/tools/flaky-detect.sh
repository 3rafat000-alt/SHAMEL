#!/usr/bin/env bash
# tool/qa/regression-warden/flaky-detect.sh — Detect + quarantine flaky tests
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--runs 5] [--threshold 2]"; exit 0; }
PRJ=""; RUNS=5; THRESHOLD=2
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --runs) RUNS="$2"; shift2 ;; --threshold) THRESHOLD="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[[ -d "$PRJ_DIR" ]] || { echo "${RED}Error: $PRJ_DIR not found${RESET}"; exit 1; }

echo "${BLUE}[flaky-detect]${RESET} Running tests $RUNS times to detect flakiness (threshold: $THRESHOLD failures)"; echo ""

detect_tool() {
  if [[ -f "$PRJ_DIR/phpunit.xml" ]] || [[ -f "$PRJ_DIR/pest.xml" ]]; then echo "phpunit"
  elif ls "$PRJ_DIR/pyproject.toml" 2>/dev/null; then echo "pytest"
  elif ls "$PRJ_DIR/package.json" 2>/dev/null; then echo "jest"
  else echo "unknown"; fi
}
TOOL=$(detect_tool)
FLAKY_REPORT=""

run_test_suite() {
  local run=1 tool="$1" log
  declare -A counts
  while [[ $run -le $RUNS ]]; do
    echo -n "  Run $run/$RUNS ... "
    log=$(mktemp)
    case "$tool" in
      phpunit) (cd "$PRJ_DIR" && ./vendor/bin/phpunit 2>/dev/null) > "$log" 2>&1 || true ;;
      pytest) (cd "$PRJ_DIR" && python -m pytest 2>/dev/null) > "$log" 2>&1 || true ;;
      jest) (cd "$PRJ_DIR" && npx jest 2>/dev/null) > "$log" 2>&1 || true ;;
      *) echo "${YELLOW}SKIP${RESET}"; return ;;
    esac
    local failed
    failed=$(grep -c "FAIL\|ERROR\|✗" "$log" 2>/dev/null || echo 0)
    if [[ "$failed" -gt 0 ]]; then
      local test_name
      while IFS= read -r line; do
        test_name=$(echo "$line" | grep -oP ":::.*?:::\|FAIL.*?!\|ERROR.*?!\|✗\s+\K\w+" | head -1)
        [[ -z "$test_name" ]] && test_name=$(echo "$line" | grep -o "tests/.*\.php.*" | head -1)
        if [[ -n "$test_name" ]]; then counts["$test_name"]=$((counts["$test_name"] + 1)); fi
      done < <(grep "FAIL\|ERROR\|✗" "$log" 2>/dev/null || true)
      echo "${RED}FAILED${RESET}"
    else echo "${GREEN}PASS${RESET}"; fi
    rm -f "$log"
    ((run++))
  done
  echo ""
  echo "${YELLOW}  Flaky candidates (failed ≥ $THRESHOLD times out of $RUNS):${RESET}"
  local found=0
  for test in "${!counts[@]}"; do
    if [[ ${counts["$test"]} -ge $THRESHOLD ]]; then
      echo "    ${RED}✗ $test (${counts[$test]}/$RUNS failures)${RESET}"
      ((found++))
    fi
  done
  [[ $found -eq 0 ]] && echo "    ${GREEN}None detected${RESET}"
  echo ""
  echo "${BLUE}[flaky-detect]${RESET} ${GREEN}Done.${RESET}"
}

run_test_suite "$TOOL"
