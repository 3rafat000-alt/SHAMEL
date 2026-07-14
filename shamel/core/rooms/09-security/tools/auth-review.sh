#!/usr/bin/env bash
# tool/sec/authn-engineer/auth-review.sh — Review auth flow: sessions, tokens, MFA, PIN
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--path dir] [--check sessions|tokens|mfa|all]"; exit 0; }
PRJ=""; SCAN_PATH=""; CHECK="all"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --path) SCAN_PATH="$2"; shift2 ;; --check) CHECK="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
SCAN_DIR="${SCAN_PATH:-$SOFI_ROOT/projects/${PRJ:-.}}"
[[ -d "$SCAN_DIR" ]] || { echo "${RED}Error: $SCAN_DIR not found${RESET}"; exit 1; }

echo "${BLUE}[auth-review]${RESET} Checking auth in $SCAN_DIR (focus: $CHECK)"; echo ""

review_sessions() {
  echo "${YELLOW}  Sessions${RESET}"
  if grep -rl "session" "$SCAN_DIR" --include="*.php" --include="*.py" --include="*.js" 2>/dev/null | head -3 | xargs grep -l "regenerate\|invalidate\|rotate" 2>/dev/null >/dev/null; then
    echo "    ${GREEN}✓ Session regeneration found${RESET}"
  else echo "    ${RED}✗ No session regeneration detected — CSRF/session-fixation risk${RESET}"; fi
  if grep -rl "expire\|ttl\|lifetime" "$SCAN_DIR" --include="*.php" 2>/dev/null | grep -i session >/dev/null 2>&1; then
    echo "    ${GREEN}✓ Session expiry configured${RESET}"
  else echo "    ${YELLOW}⚠ Session TTL not found — verify config/session.php${RESET}"; fi
}

review_tokens() {
  echo "${YELLOW}  Tokens${RESET}"
  if grep -rl "sanctum\|passport\|jwt\|oauth" "$SCAN_DIR" --include="*.php" --include="*.json" 2>/dev/null | head -5 >/dev/null; then
    echo "    ${GREEN}✓ Token auth library present${RESET}"
    local ttl
    ttl=$(grep -r "expiration\|ttl" "$SCAN_DIR" --include="*.php" 2>/dev/null | grep -i "token\|sanctum\|passport" | head -3)
    if [[ -n "$ttl" ]]; then echo "    ${GREEN}✓ Token TTL found${RESET}"; else echo "    ${YELLOW}⚠ Token TTL not explicit${RESET}"; fi
  else echo "    ${YELLOW}⚠ Token auth library not detected${RESET}"; fi
}

review_mfa() {
  echo "${YELLOW}  MFA${RESET}"
  if grep -rl "mfa\|2fa\|totp\|google2fa\|multi.factor" "$SCAN_DIR" --include="*.php" --include="*.py" 2>/dev/null | head -5 >/dev/null; then
    echo "    ${GREEN}✓ MFA detected${RESET}"
  else echo "    ${YELLOW}⚠ MFA not detected — required for admin surfaces${RESET}"; fi
  if grep -rl "backup.codes\|recovery" "$SCAN_DIR" --include="*.php" 2>/dev/null | head -3 >/dev/null; then
    echo "    ${GREEN}✓ Recovery codes present${RESET}"
  else echo "    ${YELLOW}⚠ Recovery codes not found${RESET}"; fi
}

case "$CHECK" in sessions) review_sessions ;; tokens) review_tokens ;; mfa) review_mfa ;; all) review_sessions; review_tokens; review_mfa ;; esac
echo "${GREEN}[auth-review] Done.${RESET}"
