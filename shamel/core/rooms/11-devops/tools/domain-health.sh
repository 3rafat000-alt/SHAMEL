#!/usr/bin/env bash
# tool/ops/domain-warden/domain-health.sh — Check local domain + tunnel health
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--domain <slug>.local] [--check dns|tunnel|cert|all]"; exit 0; }
PRJ=""; DOMAIN=""; CHECK="all"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --domain) DOMAIN="$2"; shift2 ;; --check) CHECK="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$DOMAIN" && -n "$PRJ" ]] && DOMAIN="${PRJ,,}.local"
[[ -z "$DOMAIN" ]] && { echo "${RED}Flag --prj or --domain required${RESET}"; exit 1; }

echo "${BLUE}[domain-health]${RESET} Checking $DOMAIN (focus: $CHECK)"; echo ""

resolve_ip() {
  local host="$1"
  host "$host" 2>/dev/null | grep -oP 'has address \K\S+' || echo ""
}

check_dns() {
  echo "${YELLOW}  DNS${RESET}"
  local ip
  ip=$(resolve_ip "$DOMAIN")
  if [[ -n "$ip" ]]; then
    echo "    ${GREEN}✓ Resolves to $ip${RESET}"
  else
    echo "    ${RED}✗ DNS resolution failed${RESET}"
    echo "    Add to /etc/hosts: echo '127.0.0.1 $DOMAIN' | sudo tee -a /etc/hosts"
  fi
}

check_tunnel() {
  echo "${YELLOW}  Tunnel${RESET}"
  if pgrep -f "cloudflared.*$DOMAIN" &>/dev/null || pgrep -f "localtunnel.*$DOMAIN" &>/dev/null; then
    echo "    ${GREEN}✓ Tunnel process running${RESET}"
  else
    echo "    ${YELLOW}⚠ No tunnel process detected (optional for local dev)${RESET}"
  fi
}

check_cert() {
  echo "${YELLOW}  TLS${RESET}"
  if echo | openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null | grep -q "notAfter"; then
    echo "    ${GREEN}✓ TLS certificate valid${RESET}"
  else
    echo "    ${YELLOW}⚠ No TLS or not accessible on :443${RESET}"
  fi
}

check_http() {
  echo "${YELLOW}  HTTP${RESET}"
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 3 "http://$DOMAIN" 2>/dev/null || echo "000")
  local code_s
  code_s=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 3 "https://$DOMAIN" 2>/dev/null || echo "000")
  echo "    HTTP : $code   HTTPS: $code_s"
  if [[ "$code" != "000" ]] || [[ "$code_s" != "000" ]]; then echo "    ${GREEN}✓ Responding${RESET}"; else echo "    ${RED}✗ Not responding${RESET}"; fi
}

case "$CHECK" in dns) check_dns ;; tunnel) check_tunnel ;; cert) check_cert ;; all) check_dns; check_tunnel; check_http; check_cert ;; esac
echo "${GREEN}[domain-health] Done.${RESET}"
