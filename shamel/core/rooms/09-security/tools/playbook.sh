#!/usr/bin/env bash
# tool/sec/incident-responder/playbook.sh — Generate incident playbook from scenario
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --scenario breach|dos|leak|insider|ransomware [--output playbook.md]"; exit 0; }
SCENARIO=""; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --scenario) SCENARIO="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$SCENARIO" ]] && usage

gen_playbook() {
  local s="$1"
  echo "# Incident Playbook: ${s^}"
  echo "## 1. Detection"
  echo "- Alert: [define trigger]"
  echo "- Severity: CRITICAL / HIGH / MEDIUM / LOW"
  echo "## 2. Triage (< 15 min)"
  echo "- [ ] Confirm incident is real (not false positive)"
  echo "- [ ] Determine scope: single user / subsystem / entire system"
  echo "- [ ] Tag affected resources in monitoring"
  echo "## 3. Containment"
  echo "- [ ] Isolate affected component (rate-limit / block / disable)"
  echo "- [ ] Revoke compromised credentials if applicable"
  echo "## 4. Eradication"
  echo "- [ ] Remove root cause"
  echo "- [ ] Patch vulnerability"
  echo "## 5. Recovery"
  echo "- [ ] Restore from clean backup"
  echo "- [ ] Verify integrity (checksums, logs)"
  echo "## 6. Post-mortem"
  echo "- [ ] Root cause analysis document"
  echo "- [ ] Update playbook with lessons"
  echo "- [ ] Adjust monitoring alerts"
}

case "$SCENARIO" in
  breach)   gen_playbook "breach" ;;
  dos)      gen_playbook "denial-of-service" ;;
  leak)     gen_playbook "data-leak" ;;
  insider)  gen_playbook "insider-threat" ;;
  ransomware) gen_playbook "ransomware" ;;
  *) echo "${RED}Unknown scenario: $SCENARIO (breach|dos|leak|insider|ransomware)${RESET}"; exit 1 ;;
esac

if [[ -n "$OUTPUT" ]]; then
  gen_playbook "$SCENARIO" > "$OUTPUT"
  echo "${GREEN}[playbook] Written to $OUTPUT${RESET}"
fi
echo "${BLUE}[playbook]${RESET} ${GREEN}Done.${RESET}"
