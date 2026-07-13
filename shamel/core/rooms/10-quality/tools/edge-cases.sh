#!/usr/bin/env bash
# tool/qa/manual-explorer/edge-cases.sh — Generate edge-case checklist by persona
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID --persona guest|member|admin|anonymous [--feature name]"; exit 0; }
PRJ=""; PERSONA=""; FEATURE=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --persona) PERSONA="$2"; shift2 ;; --feature) FEATURE="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" || -z "$PERSONA" ]] && usage

echo "${BLUE}[edge-cases]${RESET} Edge cases for $PRJ — persona: $PERSONA ${FEATURE:+($FEATURE)}"; echo ""

case "$PERSONA" in
  guest)
    echo "  [ ] Empty cart → checkout"
    echo "  [ ] Rate limit after N anonymous actions"
    echo "  [ ] Session expiry mid-flow"
    echo "  [ ] Concurrent sessions on same device"
    echo "  [ ] Browser back button after action"
    echo "  [ ] Double-click submit prevention"
    echo "  [ ] Network disconnect during submit"
    echo "  [ ] Invalid input (XSS, SQLi in forms)"
    echo "  [ ] Upload: oversized file, wrong type, empty file"
    echo "  [ ] Pagination: page -1, 0, NaN, beyond total"
    ;;
  member)
    echo "  [ ] Email change → re-verify"
    echo "  [ ] Password change → session invalidate"
    echo "  [ ] Account deletion → cascade: orders, data, references"
    echo "  [ ] Subscription expiry → access denied gracefully"
    echo "  [ ] Profile with all fields empty"
    echo "  [ ] Name: 255 chars, unicode, emoji, null byte"
    echo "  [ ] Multiple devices: logout one vs all"
    echo "  [ ] 2FA lost device → recovery code flow"
    echo "  [ ] Membership tier upgrade/downgrade mid-billing-cycle"
    echo "  [ ] Notification preferences: all off → silence"
    ;;
  admin)
    echo "  [ ] Impersonate user → audit trail check"
    echo "  [ ] Soft delete → restore vs permanent delete"
    echo "  [ ] Bulk action: 0 items, 10k items, all items"
    echo "  [ ] Permission: missing role → 403 vs 404 (no leak)"
    echo "  [ ] Export: empty data, 1M rows, CSV injection"
    echo "  [ ] Timezone: UTC vs local in logs and timestamps"
    echo "  [ ] Search: SQL wildcards (% _), empty string, unicode"
    echo "  [ ] Filter: all params empty, overlapping, impossible combo"
    echo "  [ ] Mass assignment: extra fields in POST body"
    echo "  [ ] Config change → hot reload vs restart required"
    ;;
  anonymous)
    echo "  [ ] Registration: existing email, weak password, missing fields"
    echo "  [ ] Login: wrong password 5x → lockout"
    echo "  [ ] Login: SQLi in email field"
    echo "  [ ] Password reset: invalid token, expired token, re-use"
    echo "  [ ] OAuth: cancel mid-flow, deny permissions, re-link"
    echo "  [ ] Public page: authenticated vs unauthenticated diff"
    echo "  [ ] robots.txt: no sensitive paths leaked"
    echo "  [ ] Cookie-less request: session fallback"
    echo "  [ ] Legal: GDPR consent before data collection"
    echo "  [ ] Email verification: skip, expire, re-send spam"
    ;;
  *) echo "${RED}Unknown persona: $PERSONA${RESET}"; exit 1 ;;
esac

echo ""
echo "${BLUE}[edge-cases]${RESET} ${GREEN}Checklist generated — verify each case manually.${RESET}"
