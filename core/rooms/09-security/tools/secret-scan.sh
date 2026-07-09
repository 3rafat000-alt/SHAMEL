#!/usr/bin/env bash
# tool/sec/secrets-warden/secret-scan.sh — Scan repo for secrets, .env, keys
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--path dir] [--exit-on-find]"; exit 0; }
PRJ=""; SCAN_PATH=""; EXIT_ON_FIND=false
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --path) SCAN_PATH="$2"; shift2 ;; --exit-on-find) EXIT_ON_FIND=true ;; --help|-h) usage ;; *) usage ;; esac; shift; done
SCAN_DIR="${SCAN_PATH:-$SOFI_ROOT/projects/${PRJ:-$SOFI_ROOT}}"
[[ -d "$SCAN_DIR" ]] || { echo "${RED}Error: $SCAN_DIR not found${RESET}"; exit 1; }

echo "${BLUE}[secret-scan]${RESET} Scanning $SCAN_DIR for secrets"; echo ""
FOUND=0; REPORT=""

scan_pattern() {
  local label="$1" pattern="$2" highlight="$3"
  local matches
  matches=$(grep -rn "$pattern" "$SCAN_DIR" --include="*.{env,env.*,php,py,js,json,yaml,yml,toml,ini,cfg,conf}" \
    --exclude-dir=vendor --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=.opencode 2>/dev/null || true)
  if [[ -n "$matches" ]]; then
    echo "${RED}  ✗ $label${RESET}"
    echo "$matches" | head -10 | sed "s/$highlight/${RED}&${RESET}/g" | sed 's/^/    /'
    ((FOUND++))
    REPORT+="$label: found\n"
  fi
}

scan_pattern "AWS Access Key" "AKIA[0-9A-Z]{16}" "AKIA[0-9A-Z]\{16\}"
scan_pattern "GitHub Token" "ghp_[a-zA-Z0-9]{36}" "ghp_[a-zA-Z0-9]\{36\}"
scan_pattern "Stripe Key" "sk_live_[0-9a-zA-Z]{24,}" "sk_live_[0-9a-zA-Z]\{24,\}"
scan_pattern "Generic Secret" "SECRET.*=.*['\"]\w{16,}" "SECRET.*=.*"
scan_pattern "Password in code" "password.*=.*['\"]\w{6}" "password.*=.*"
scan_pattern "JWT Secret" "JWT_SECRET\|JWT_KEY" "JWT_SECRET\|JWT_KEY"
scan_pattern ".env committed" "DB_PASSWORD\|APP_KEY" "DB_PASSWORD\|APP_KEY"
scan_pattern "Private Key" "BEGIN.*PRIVATE KEY" "BEGIN.*PRIVATE KEY"

echo ""
if [[ $FOUND -eq 0 ]]; then echo "${GREEN}[secret-scan] PASS — 0 secrets found${RESET}"
else echo "${RED}[secret-scan] $FOUND secret patterns found — review each above${RESET}"
fi
$EXIT_ON_FIND && [[ $FOUND -gt 0 ]] && exit 1
exit 0
