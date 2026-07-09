#!/usr/bin/env bash
# tool/qa/lead/qa-verdict.sh — Generate PASS/BLOCK with evidence
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID --gate <N> [--coverage <pct>] [--tests <pass/total>] [--tti <ms>] [--output verdict.md]"; exit 0; }
PRJ=""; GATE=""; COVERAGE=""; TESTS=""; TTI=""; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --gate) GATE="$2"; shift2 ;; --coverage) COVERAGE="$2"; shift2 ;; --tests) TESTS="$2"; shift2 ;; --tti) TTI="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" || -z "$GATE" ]] && usage

echo "${BLUE}[qa-verdict]${RESET} Verdict for $PRJ Gate $GATE"; echo ""
BLOCKERS=0; PASSES=0

check() { local label="$1" condition="$2"; echo -n "  $label ... "; if eval "$condition"; then echo "${GREEN}PASS${RESET}"; ((PASSES++)); else echo "${RED}BLOCK${RESET}"; ((BLOCKERS++)); fi; }

check "Gate $GATE deliverables exist" "[[ -d '$SOFI_ROOT/projects/$PRJ/_context' ]]"
check "STATE.md present" "[[ -f '$SOFI_ROOT/projects/$PRJ/_context/STATE.md' ]]"
check "CONTEXT.md present" "[[ -f '$SOFI_ROOT/projects/$PRJ/_context/CONTEXT.md' ]]"
check "HANDOFFS.md present" "[[ -f '$SOFI_ROOT/projects/$PRJ/_context/HANDOFFS.md' ]]"
check "DECISIONS.md present" "[[ -f '$SOFI_ROOT/projects/$PRJ/_context/DECISIONS.md' ]]"

if [[ -n "$COVERAGE" ]]; then check "Coverage ≥90% ($COVERAGE%)" "[[ ${COVERAGE%.*} -ge 90 ]]"
else echo "  Coverage  ... ${YELLOW}SKIP (no --coverage arg)${RESET}"; fi

if [[ -n "$TESTS" ]]; then
  local pass="${TESTS%%/*}" total="${TESTS##*/}"
  check "Tests pass ($pass/$total)" "[[ $pass -eq $total ]]"
else echo "  Tests     ... ${YELLOW}SKIP (no --tests arg)${RESET}"; fi

if [[ -n "$TTI" ]]; then check "TTI < 2000ms ($TTI ms)" "[[ $TTI -lt 2000 ]]"
else echo "  TTI       ... ${YELLOW}SKIP (no --tti arg)${RESET}"; fi

echo ""
VERDICT="PASS"; [[ $BLOCKERS -gt 0 ]] && VERDICT="BLOCK"
echo "${BLUE}[qa-verdict]${RESET} ${VERDICT} ($PASSES pass, $BLOCKERS blocker)"

if [[ -n "$OUTPUT" ]]; then
  cat > "$OUTPUT" <<EOF
# QA Verdict: $PRJ Gate $GATE
**Verdict:** $VERDICT
**Date:** $(date -Iseconds)
**Results:** $PASSES pass, $BLOCKERS blocker
**Evidence:**
- STATE.md: $([[ -f "$SOFI_ROOT/projects/$PRJ/_context/STATE.md" ]] && echo "present" || echo "missing")
- Coverage: ${COVERAGE:-N/A}
- Tests: ${TESTS:-N/A}
- TTI: ${TTI:-N/A}
EOF
  echo "${BLUE}[qa-verdict]${RESET} Report written to $OUTPUT"
fi
