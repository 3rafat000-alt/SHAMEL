#!/usr/bin/env bash
# tool/sec/compliance-auditor/data-flow.sh — Map data flow to GDPR/PCI requirements
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--framework gdpr|pci|all]"; exit 0; }
PRJ=""; FRAMEWORK="all"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --framework) FRAMEWORK="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
PROJ_DIR="$SOFI_ROOT/projects/${PRJ:-no-project}"
[[ -d "$PROJ_DIR" ]] || { echo "${YELLOW}No project dir — scanning SOFI root for patterns${RESET}"; PROJ_DIR="$SOFI_ROOT"; }

echo "${BLUE}[data-flow]${RESET} Data flow mapping (${FRAMEWORK}) for ${PRJ:-workspace}"; echo ""

find_tables() {
  grep -rn "Schema::create\|createTable\|class.*extends.*Migration" "$PROJ_DIR" --include="*.php" --exclude-dir=vendor 2>/dev/null | head -20 || true
}
find_models() {
  grep -rn "class.*extends\Model" "$PROJ_DIR" --include="*.php" --exclude-dir=vendor 2>/dev/null | head -20 || true
}
find_pii_fields() {
  grep -rni "email\|phone\|address\|ssn\|dob\|passport\|bank\|card_number" "$PROJ_DIR" --include="*.php" --include="*.sql" \
    --exclude-dir=vendor --exclude-dir=node_modules 2>/dev/null | grep -v "test\|mock\|fake" | head -20 || true
}

echo "${YELLOW}  Tables defined:${RESET}"
find_tables | sed 's/^/    /'
echo ""
echo "${YELLOW}  Models:${RESET}"
find_models | sed 's/^/    /'
echo ""
echo "${YELLOW}  PII fields detected:${RESET}"
pii=$(find_pii_fields)
if [[ -n "$pii" ]]; then echo "$pii" | sed 's/^/    /'
else echo "    ${GREEN}None found${RESET}"; fi
echo ""

if [[ "$FRAMEWORK" == "gdpr" || "$FRAMEWORK" == "all" ]]; then
  echo "${BLUE}  GDPR Checklist:${RESET}"
  echo "    ☐ Data inventory complete"
  echo "    ☐ Lawful basis documented per processing"
  echo "    ☐ Right to erasure implemented"
  echo "    ☐ Data portability (export) available"
  echo "    ☐ DPA in place with subprocessors"
fi
if [[ "$FRAMEWORK" == "pci" || "$FRAMEWORK" == "all" ]]; then
  echo "${BLUE}  PCI DSS Checklist:${RESET}"
  echo "    ☐ Cardholder data encrypted at rest (AES-256)"
  echo "    ☐ Transmission over TLS 1.2+"
  echo "    ☐ No storage of CVV or track data"
  echo "    ☐ Access logged and monitored"
fi
echo "${GREEN}[data-flow] Done.${RESET}"
