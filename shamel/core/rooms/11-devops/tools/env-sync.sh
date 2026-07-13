#!/usr/bin/env bash
# tool/ops/cloud-engineer/env-sync.sh — Compare staging/prod environment parity
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--staging .env.staging] [--production .env.production] [--ignore APP_KEY,DB_PASSWORD]"; exit 0; }
PRJ=""; STAGING=""; PRODUCTION=""; IGNORE="APP_KEY,DB_PASSWORD,APP_URL"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --staging) STAGING="$2"; shift2 ;; --production) PRODUCTION="$2"; shift2 ;; --ignore) IGNORE="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[[ -d "$PRJ_DIR" ]] || { echo "${RED}Error: $PRJ_DIR not found${RESET}"; exit 1; }

STAGING="${STAGING:-$PRJ_DIR/.env.staging}"
PRODUCTION="${PRODUCTION:-$PRJ_DIR/.env.production}"

for f in "$STAGING" "$PRODUCTION"; do
  [[ -f "$f" ]] || { echo "${YELLOW}Warning: $f not found${RESET}"; }
done

echo "${BLUE}[env-sync]${RESET} Environment parity for $PRJ"; echo ""
MISMATCHES=0

join_env() {
  local file="$1"
  grep -v '^#' "$file" 2>/dev/null | grep '=' | sed 's/ *= */=/' | sort || true
}

staging_vars=$(join_env "$STAGING")
prod_vars=$(join_env "$PRODUCTION")

if [[ -z "$staging_vars" ]]; then echo "${YELLOW}  Staging: empty or missing${RESET}"; fi
if [[ -z "$prod_vars" ]]; then echo "${YELLOW}  Production: empty or missing${RESET}"; fi

# Check keys in staging that differ or missing in prod
while IFS='=' read -r key val; do
  [[ -z "$key" ]] && continue
  local skip=false
  for ig in ${IGNORE//,/ }; do [[ "$key" == "$ig" ]] && skip=true && break; done
  $skip && continue

  local prod_val
  prod_val=$(echo "$prod_vars" | grep "^${key}=" | head -1 | cut -d= -f2- || echo "__MISSING__")
  if [[ "$prod_val" == "__MISSING__" ]]; then
    echo "  ${RED}✗ $key: in staging, MISSING in production${RESET}"
    ((MISMATCHES++))
  elif [[ "$val" != "$prod_val" ]]; then
    echo "  ${YELLOW}⚠ $key: staging='$val' ≠ production='...'${RESET}"
    ((MISMATCHES++))
  fi
done < <(echo "$staging_vars")

# Check keys in production that are extra
while IFS='=' read -r key val; do
  [[ -z "$key" ]] && continue
  local skip=false
  for ig in ${IGNORE//,/ }; do [[ "$key" == "$ig" ]] && skip=true && break; done
  $skip && continue

  if ! echo "$staging_vars" | grep -q "^${key}="; then
    echo "  ${YELLOW}⚠ $key: in production, EXTRA (not in staging)${RESET}"
    ((MISMATCHES++))
  fi
done < <(echo "$prod_vars")

echo ""
if [[ $MISMATCHES -eq 0 ]]; then echo "${GREEN}[env-sync] PASS — environments in sync${RESET}"
else echo "${YELLOW}[env-sync] $MISMATCHES difference(s) found${RESET}"; fi
exit $MISMATCHES
