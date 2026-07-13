#!/usr/bin/env bash
# tool/str/risk-analyst/risk-register.sh — Business risk register scaffold
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RED=$(tput setaf 1); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--add <risk>] [--impact <H|M|L>] [--likelihood <H|M|L>] [--mitigation "<plan>"]
  Create or update risk register in projects/<PRJ>/_context/RISK_REGISTER.md.
  Without --add, scaffold empty register.
EOF
exit 0
}

PRJ="${1:-}"; RISK=""; IMPACT=""; LIKELIHOOD=""; MITIGATION=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --add) RISK="$2"; shift;; --impact) IMPACT="$2"; shift;;
  --likelihood) LIKELIHOOD="$2"; shift;; --mitigation) MITIGATION="$2"; shift;; --help) usage;; esac; shift
done

REG="$SOFI_ROOT/projects/$PRJ/_context/RISK_REGISTER.md"
mkdir -p "$(dirname "$REG")"

if [[ ! -f "$REG" ]]; then
  cat > "$REG" <<REGISTER
# Risk Register: $PRJ
**Created:** $(date '+%Y-%m-%d')
**Owner:** str-risk-analyst

## Risk Scoring
- Impact × Likelihood: H×H=🔴 Critical, H×M=🟡 High, M×M=🟠 Medium, L×any=🟢 Low

## Register

| ID | Risk | Impact | Likelihood | Score | Mitigation | Owner | Status |
|----|------|--------|------------|-------|------------|-------|--------|
REGISTER
  echo "${GREEN}✓ Risk register created: $REG${RESET}"
fi

if [[ -n "$RISK" ]]; then
  : "${IMPACT:=M}" "${LIKELIHOOD:=M}" "${MITIGATION:=TBD}"
  RID="RISK-$(date '+%Y%m%d%H%M')"
  echo "| $RID | $RISK | $IMPACT | $LIKELIHOOD | ${IMPACT}×${LIKELIHOOD} | $MITIGATION | str-risk-analyst | open |" >> "$REG"
  echo "${GREEN}✓ Risk added: $RID — $RISK${RESET}"
fi
