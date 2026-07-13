#!/usr/bin/env bash
# tool/sec/lead/sec-sweep.sh — Full security sweep across all surfaces
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--quick|--deep]"; exit 0; }
PRJ=""; DEPTH="--quick"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --quick) DEPTH="--quick" ;; --deep) DEPTH="--deep" ;; --help|-h) usage ;; *) usage ;; esac; shift; done

echo "${BLUE}[sec-sweep]${RESET} Starting security sweep $DEPTH for project: ${PRJ:-all}"
FAIL=0

echo "${YELLOW}  → Secret scan${RESET}"
"$SOFI_ROOT/tools/sec/secrets-warden/secret-scan.sh" --prj "$PRJ" 2>&1 | sed 's/^/    /' || { echo "${RED}  ✗ Secret scan failed${RESET}"; ((FAIL++)); }

echo "${YELLOW}  → STRIDE threat model${RESET}"
"$SOFI_ROOT/tools/sec/threat-modeler/stride-audit.sh" --prj "$PRJ" 2>&1 | sed 's/^/    /' || { echo "${RED}  ✗ STRIDE audit failed${RESET}"; ((FAIL++)); }

echo "${YELLOW}  → Code scan${RESET}"
"$SOFI_ROOT/tools/sec/appsec-engineer/code-scan.sh" --prj "$PRJ" 2>&1 | sed 's/^/    /' || { echo "${RED}  ✗ Code scan failed${RESET}"; ((FAIL++)); }

if [[ "$DEPTH" == "--deep" ]]; then
  echo "${YELLOW}  → Auth review${RESET}"
  "$SOFI_ROOT/tools/sec/authn-engineer/auth-review.sh" --prj "$PRJ" 2>&1 | sed 's/^/    /' || { echo "${RED}  ✗ Auth review failed${RESET}"; ((FAIL++)); }
  echo "${YELLOW}  → Penetration test${RESET}"
  "$SOFI_ROOT/tools/sec/pentester/live-attack.sh" --prj "$PRJ" 2>&1 | sed 's/^/    /' || { echo "${RED}  ✗ Pentest failed${RESET}"; ((FAIL++)); }
fi

if [[ $FAIL -eq 0 ]]; then echo "${GREEN}[sec-sweep] PASS — $DEPTH sweep complete (0 failures)${RESET}"
else echo "${RED}[sec-sweep] BLOCK — $FAIL sub-sweeps failed${RESET}"; fi
exit $FAIL
