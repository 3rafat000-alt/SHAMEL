#!/usr/bin/env bash
# tool/res/fact-checker/ground-check.sh — Adversarial fact check against sources
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --claim "<claim>" [--expected-source "<path>"] [--depth <n>]
  Adversarially verify a factual claim.
  Checks: does file:line / brain / commit support the claim?
  Grounding clause: cite or mark [unverified].
EOF
exit 0
}

PRJ="${1:-}"; CLAIM=""; SOURCE=""; DEPTH=3
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --claim) CLAIM="$2"; shift;; --expected-source) SOURCE="$2"; shift;;
  --depth) DEPTH="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$CLAIM" ]] && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"

echo "${BLUE}═══ Fact Check :: $PRJ ═══${RESET}"
echo "  ${YELLOW}Claim:${RESET}  $CLAIM"
echo ""

FOUND=false

# 1. Check STATE.md
if grep -qi "$CLAIM" "$PRJ_DIR/_context/STATE.md" 2>/dev/null; then
  echo "  ${GREEN}✓${RESET} Found in STATE.md"
  FOUND=true
fi

# 2. Check CONTEXT.md
if grep -qi "$CLAIM" "$PRJ_DIR/_context/CONTEXT.md" 2>/dev/null; then
  echo "  ${GREEN}✓${RESET} Found in CONTEXT.md"
  FOUND=true
fi

# 3. Check DECISIONS.md
if grep -qi "$CLAIM" "$PRJ_DIR/_context/DECISIONS.md" 2>/dev/null; then
  echo "  ${GREEN}✓${RESET} Found in DECISIONS.md"
  FOUND=true
fi

# 4. Specific source
if [[ -n "$SOURCE" ]]; then
  if grep -qi "$CLAIM" "$PRJ_DIR/$SOURCE" 2>/dev/null; then
    echo "  ${GREEN}✓${RESET} Found in $SOURCE"
    FOUND=true
  else
    echo "  ${YELLOW}⚠${RESET} Not found in expected source: $SOURCE"
  fi
fi

# 5. Git log search
if git -C "$PRJ_DIR" log --oneline --grep="$CLAIM" 2>/dev/null | head -3 | grep -q .; then
  echo "  ${GREEN}✓${RESET} Found in git commit messages"
  FOUND=true
fi

echo ""
if $FOUND; then
  echo "${GREEN}[verified: $PRJ project brain]${RESET}"
else
  echo "${RED}[unverified]${RESET} — Claim not found in project sources"
  echo "  → Add to CONTEXT.md or append source"
  exit 1
fi
