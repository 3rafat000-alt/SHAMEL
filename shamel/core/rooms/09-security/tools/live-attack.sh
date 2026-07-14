#!/usr/bin/env bash
# tool/sec/pentester/live-attack.sh — Proof-first penetration test checklist
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --url https://example.com [--scope narrow|full] [--output report.md]"; exit 0; }
URL=""; SCOPE="narrow"; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --url) URL="$2"; shift2 ;; --scope) SCOPE="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$URL" ]] && usage

echo "${BLUE}[pentest]${RESET} Penetration test: $URL (scope: $SCOPE)"; echo ""

check() { local label="$1" cmd="$2"; echo -n "  $label ... "; if eval "$cmd" >/dev/null 2>&1; then echo "${GREEN}PASS${RESET}"; else echo "${YELLOW}CHECK${RESET}"; fi; }

check "TLS 1.2+" "curl -sI --tlsv1.2 --connect-timeout 5 '$URL'"
check "TLS 1.3" "curl -sI --tlsv1.3 --connect-timeout 5 '$URL'"
check "No HSTS leak" "curl -sI '$URL' | grep -qi 'strict-transport-security'"
check "No X-Powered-By" "! curl -sI '$URL' | grep -qi 'X-Powered-By'"
check "CSP header" "curl -sI '$URL' | grep -qi 'content-security-policy'"
check "X-Frame-Options" "curl -sI '$URL' | grep -qi 'DENY\|SAMEORIGIN'"
check "No directory listing" "! curl -sL --connect-timeout 5 '$URL/../' | grep -qi 'index of\|directory listing'"
check "Rate limiting" "for i in {1..10}; do curl -s -o /dev/null -w '%{http_code}' '$URL' 2>/dev/null; done | grep -q 429"

if [[ "$SCOPE" == "full" ]]; then
  echo ""
  echo "${YELLOW}[deep] SQLi probe (time-based)${RESET}"
  echo "  curl -s -o /dev/null -w '%{http_code}' '$URL/?id=1+AND+SLEEP(3)'"
  echo "${YELLOW}[deep] XSS probe${RESET}"
  echo "  curl -s -o /dev/null -w '%{http_code}' '$URL/?q=<script>alert(1)</script>'"
  echo "${YELLOW}[deep] Open redirect${RESET}"
  echo "  curl -sI '$URL?url=https://evil.com'"
fi

if [[ -n "$OUTPUT" ]]; then
  echo "---" > "$OUTPUT"
  echo "url: $URL" >> "$OUTPUT"
  echo "scope: $SCOPE" >> "$OUTPUT"
  echo "timestamp: $(date -Iseconds)" >> "$OUTPUT"
  echo "finding: Manual review required for business-logic flaws" >> "$OUTPUT"
  echo "${BLUE}[pentest] Report written to $OUTPUT${RESET}"
fi
echo "${GREEN}[pentest] Surface scan complete.${RESET}"
