#!/usr/bin/env bash
# tool/obs/incident-commander/incident-triage.sh — Triage incident → rollback/fix-forward
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --alert 'description' --severity sev1|sev2|sev3 [--prj PRJ-ID] [--auto]"; exit 0; }
ALERT=""; SEVERITY=""; PRJ=""; AUTO=false
while [[ $# -gt 0 ]]; do case "$1" in --alert) ALERT="$2"; shift ;; --severity) SEVERITY="$2"; shift ;; --prj) PRJ="$2"; shift ;; --auto) AUTO=true ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$ALERT" || -z "$SEVERITY" ]] && usage

echo "${BLUE}[triage]${RESET} Incident: $ALERT"
echo "  Severity: ${SEVERITY^^}"
echo "  Project: ${PRJ:-unknown}"; echo ""

case "$SEVERITY" in
  sev1)  RESPONSE="5 min"; ACTION="Rollback immediately. Declare incident. Notify all-hands." ;;
  sev2)  RESPONSE="15 min"; ACTION="Rollback or feature-flag off. Notify team lead." ;;
  sev3)  RESPONSE="1 hour"; ACTION="Fix-forward in normal cycle. Log in standup." ;;
  *) echo "${RED}Unknown severity${RESET}"; exit 1 ;;
esac

echo "  Response SLA: $RESPONSE"
echo "  Action: $ACTION"
echo ""

echo "  Triage checklist:"
echo "    [ ] Acknowledge incident"
echo "    [ ] Determine blast radius"
echo "    [ ] Tag affected version: \$(git log -1 --format='%h')"
echo "    [ ] Open incident channel"
echo "    [ ] Capture current state (logs, metrics, traces)"
echo ""

if $AUTO && [[ "$SEVERITY" == "sev1" || "$SEVERITY" == "sev2" ]]; then
  echo "${YELLOW}  Auto-rollback triggered${RESET}"
  sha=$(git -C "$SOFI_ROOT" log --oneline -2 --format='%h' | tail -1)
  echo "    git revert $sha --no-edit && git push"
  echo "    Command: (cd $SOFI_ROOT && git revert $sha --no-edit && git push)"
fi

echo ""
echo "${BLUE}[triage]${RESET} ${GREEN}Done.${RESET}"
