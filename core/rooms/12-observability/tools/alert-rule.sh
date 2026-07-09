#!/usr/bin/env bash
# tool/obs/monitoring-engineer/alert-rule.sh — Scaffold alert rule + runbook
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --name error-rate --metric http_error_rate --condition '> 1%' --severity warning|c critical --runbook runbook.md"; exit 0; }
NAME=""; METRIC=""; CONDITION=""; SEVERITY="critical"; RUNBOOK=""
while [[ $# -gt 0 ]]; do case "$1" in --name) NAME="$2"; shift2 ;; --metric) METRIC="$2"; shift2 ;; --condition) CONDITION="$2"; shift2 ;; --severity) SEVERITY="$2"; shift2 ;; --runbook) RUNBOOK="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$NAME" || -z "$CONDITION" ]] && usage
RUNBOOK="${RUNBOOK:-$SOFI_ROOT/projects/runbooks/${NAME}.md}"
mkdir -p "$(dirname "$RUNBOOK")"

cat > "$RUNBOOK" <<EOF
# Alert: $NAME
**Metric:** $METRIC
**Condition:** $CONDITION
**Severity:** $SEVERITY
**Owner:** \`ops-\`

## Symptoms
- [Describe what the user or operator sees]

## Triage (5 min)
- [ ] Pager acknowledged
- [ ] Check [$METRIC] dashboard
- [ ] Correlate with recent deploys
- [ ] Determine blast radius

## Mitigation
- Option A:
- Option B:

## Resolution
- [ ] Apply fix
- [ ] Verify metric recovers below threshold
- [ ] Post-mortem ticket created
EOF

echo "${BLUE}[alert-rule]${RESET} Generated rule: $NAME"
echo "  Metric:    $METRIC"
echo "  Condition: $CONDITION"
echo "  Severity:  $SEVERITY"
echo "  Runbook:   $RUNBOOK"
echo "${GREEN}[alert-rule] Done.${RESET}"
