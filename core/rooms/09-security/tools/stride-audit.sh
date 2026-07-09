#!/usr/bin/env bash
# tool/sec/threat-modeler/stride-audit.sh — Run STRIDE threat model checklist
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--component name]"; exit 0; }
PRJ=""; COMPONENT=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --component) COMPONENT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done

echo "${BLUE}[STRIDE]${RESET} Threat model for ${COMPONENT:-all components} in ${PRJ:-workspace}"
echo ""

stride_check() {
  local letter="$1" name="$2" threat="$3" mitigation="$4"
  echo "${YELLOW}  $letter | $name${RESET}"
  echo "    Threat: $threat"
  echo "    Mitigation: $mitigation"
  echo -n "    Status: "
  if grep -qr "$threat" "$SOFI_ROOT/projects/${PRJ:-.}" 2>/dev/null | head -1 >/dev/null 2>&1; then
    echo "${GREEN}COVERED${RESET}"
  else
    echo "${RED}PENDING${RESET}"
  fi
  echo ""
}

stride_check "S" "Spoofing" "Attacker impersonates user/system" "Authenticate all identities; validate origins"
stride_check "T" "Tampering" "Attacker modifies data in transit/rest" "Checksums, signatures, immutable logs"
stride_check "R" "Repudiation" "User denies action" "Audit trail with timestamps + user_id"
stride_check "I" "Information Disclosure" "Sensitive data leaked" "Encrypt at rest+transit; least privilege"
stride_check "D" "Denial of Service" "Resource exhaustion" "Rate limits, quotas, auto-scaling"
stride_check "E" "Elevation of Privilege" "User escalates to admin" "RBAC enforcement every endpoint; test IDOR"

echo "${GREEN}[STRIDE] Audit complete for ${COMPONENT:-all}${RESET}"
