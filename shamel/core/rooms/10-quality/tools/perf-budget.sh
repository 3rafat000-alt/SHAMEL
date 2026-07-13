#!/usr/bin/env bash
# tool/qa/perf-analyst/perf-budget.sh — Run k6/Lighthouse against budgets
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --url URL [--lhr-budget budget.json] [--k6-script script.js] [--tti-max 2000] [--lcp-max 2500]"; exit 0; }
URL=""; LHR_BUDGET=""; K6_SCRIPT=""; TTI_MAX=2000; LCP_MAX=2500
while [[ $# -gt 0 ]]; do case "$1" in --url) URL="$2"; shift2 ;; --lhr-budget) LHR_BUDGET="$2"; shift2 ;; --k6-script) K6_SCRIPT="$2"; shift2 ;; --tti-max) TTI_MAX="$2"; shift2 ;; --lcp-max) LCP_MAX="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$URL" ]] && usage

echo "${BLUE}[perf-budget]${RESET} Performance budget check for $URL"; echo ""
FAIL=0

if command -v lighthouse &>/dev/null || command -v npx &>/dev/null; then
  echo "${YELLOW}  → Lighthouse${RESET}"
  local tmp
  tmp=$(mktemp)
  npx lighthouse "$URL" --output=json --quiet --chrome-flags="--headless" 2>/dev/null > "$tmp" || true
  if [[ -s "$tmp" ]]; then
    local tti lcp
    tti=$(python3 -c "import json; d=json.load(open('$tmp')); print(d.get('audits',{}).get('interactive',{}).get('numericValue',0))" 2>/dev/null || echo 0)
    lcp=$(python3 -c "import json; d=json.load(open('$tmp')); print(d.get('audits',{}).get('largest-contentful-paint',{}).get('numericValue',0))" 2>/dev/null || echo 0)
    echo "    TTI: ${tti}ms (budget: ${TTI_MAX}ms)"
    echo "    LCP: ${lcp}ms (budget: ${LCP_MAX}ms)"
    if (($(echo "$tti > $TTI_MAX" | bc -l 2>/dev/null || echo 0))); then echo "    ${RED}✗ TTI exceeds budget${RESET}"; ((FAIL++)); else echo "    ${GREEN}✓ TTI within budget${RESET}"; fi
    if (($(echo "$lcp > $LCP_MAX" | bc -l 2>/dev/null || echo 0))); then echo "    ${RED}✗ LCP exceeds budget${RESET}"; ((FAIL++)); else echo "    ${GREEN}✓ LCP within budget${RESET}"; fi
  else echo "    ${YELLOW}⚠ Lighthouse produce no output (no URL/Chrome?)${RESET}"; fi
  rm -f "$tmp"
fi

if [[ -n "$K6_SCRIPT" ]] && [[ -f "$K6_SCRIPT" ]]; then
  echo "${YELLOW}  → k6 load test${RESET}"
  if command -v k6 &>/dev/null; then
    k6 run "$K6_SCRIPT" 2>&1 | sed 's/^/    /'
  else echo "    ${YELLOW}⚠ k6 not installed — install grafana/k6${RESET}"; fi
fi

if [[ $FAIL -eq 0 ]]; then echo "${GREEN}[perf-budget] PASS${RESET}"; else echo "${RED}[perf-budget] $FAIL budget(s) exceeded${RESET}"; fi
exit $FAIL
