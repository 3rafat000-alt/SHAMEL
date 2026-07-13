#!/usr/bin/env bash
# tool/obs/alerting-engineer/alert-test.sh — Dry-test alert rule against history
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --rule runbook.md [--metric-values '99.8 99.9 99.5 98.0 99.7'] [--threshold 99.0]"; exit 0; }
RULE=""; VALUES="95.0 98.5 99.9 99.5 97.0 96.5 99.8 99.2 98.0 99.1"; THRESHOLD=99.0
while [[ $# -gt 0 ]]; do case "$1" in --rule) RULE="$2"; shift2 ;; --metric-values) VALUES="$2"; shift2 ;; --threshold) THRESHOLD="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done

echo "${BLUE}[alert-test]${RESET} Dry-test alert against metric history"; echo ""
FIRED=0; TOTAL=0

if [[ -n "$RULE" && -f "$RULE" ]]; then
  CONDITION=$(grep "Condition:" "$RULE" | sed 's/.*Condition: *//' || echo "> ${THRESHOLD}%")
  echo "  Rule: $(basename "$RULE")"
  echo "  Condition: $CONDITION"
  echo ""
fi

echo "  Metric history:"
for val in $VALUES; do
  ((TOTAL++))
  local breached
  breached=$(echo "$val < $THRESHOLD" | bc -l 2>/dev/null || echo 0)
  if [[ "$breached" -eq 1 ]]; then
    echo "    ${RED}✗ $val (BREACH)${RESET}"
    ((FIRED++))
  else
    echo "    ${GREEN}✓ $val${RESET}"
  fi
done

echo ""
echo "  Summary: $FIRED/$TOTAL data points breached threshold ($THRESHOLD)"
if [[ $FIRED -gt 0 ]]; then
  local ratio
  ratio=$(echo "scale=2; $FIRED / $TOTAL * 100" | bc)
  echo "  ${YELLOW}Alert would have fired $FIRED times (${ratio}% of windows)${RESET}"
  echo "  Consider tuning threshold or evaluation window."
else
  echo "  ${GREEN}Alert would NOT have fired (clean history)${RESET}"
fi
echo "${BLUE}[alert-test] Done.${RESET}"
