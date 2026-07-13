#!/usr/bin/env bash
# tool/brd/cso/deep-audit-trigger.sh — Deep audit trigger: flag money/auth surfaces
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--path <src-dir>]
  Scan project source for money/auth/PII surfaces.
  Flags: payment, wallet, withdrawal, card, KYC, auth, credentials.
  Outputs risk surfaces requiring Deep-Audit (full 9-gate) vs Fast-Track.
EOF
exit 0
}

PRJ="${1:-}"; [[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage
SRC_PATH="${SOFI_ROOT}/projects/${PRJ}"
if [[ "${2:-}" == "--path" ]]; then SRC_PATH="${3:-$SRC_PATH}"; fi
[[ ! -d "$SRC_PATH" ]] && { echo "${RED}✗ Project path not found: $SRC_PATH${RESET}"; exit 1; }

SURFACE_PATTERNS=(
  "payment|stripe|charge|invoice|transaction"
  "wallet|balance|deposit|withdraw"
  "card|credit_card|pci"
  "kyc|identity|verification|document"
  "password|credential|token|jwt|oauth"
  "sanctum|auth|login|register"
  "api_key|secret|encrypt|decrypt"
  "pii|email|phone|ssn|address"
)

FLAGGED=0
echo "${BLUE}═══ Deep Audit Surface Scan :: $PRJ ═══${RESET}"
echo "${YELLOW}Scanning: ${SRC_PATH}${RESET}"
echo ""

for pattern in "${SURFACE_PATTERNS[@]}"; do
  matches=$(grep -rl "$pattern" "$SRC_PATH" --include='*.php' --include='*.vue' --include='*.ts' --include='*.py' --include='*.yaml' --include='*.yml' --include='*.json' 2>/dev/null | head -5)
  if [[ -n "$matches" ]]; then
    echo "${RED}⚠ SURFACE:${RESET} /${pattern}/ found in:"
    echo "$matches" | sed 's/^/    /'
    ((FLAGGED++))
  fi
done

echo ""
if [[ $FLAGGED -gt 0 ]]; then
  echo "${RED}✗ ${FLAGGED} sensitive surface(s) detected — requires DEEP-AUDIT (full 9 gates)${RESET}"
  echo "${YELLOW}  → Route full lifecycle: no fast-track allowed${RESET}"
  echo "${YELLOW}  → Notify: CSO (security-lead) for threat model${RESET}"
  exit 1
else
  echo "${GREEN}✓ No money/auth/PII surfaces detected — Fast-Track permitted${RESET}"
fi
