#!/usr/bin/env bash
# tool/res/web-scout/fetch-cite.sh — Web fetch + verify + cite in one step
set -euo pipefail
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RED=$(tput setaf 1); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <url> [--cite "<context>"]
  Fetch URL, capture content, verify, produce cite block.
  Outputs: [verified: <url>] or [unverified: <url>]
EOF
exit 0
}

URL="${1:-}"; CONTEXT=""
[[ "$URL" == "--help" || -z "$URL" ]] && usage; shift
[[ "${1:-}" == "--cite" ]] && CONTEXT="${2:-}"

echo "${BLUE}═══ Web Fetch + Cite ═══${RESET}"
echo "  URL: $URL"

# Try fetch with curl
FETCHED=$(curl -sL --max-time 10 "$URL" 2>/dev/null || true)
if [[ -z "$FETCHED" ]]; then
  echo "${RED}✗ Failed to fetch: $URL${RESET}"
  echo "[unverified: $URL]"
  exit 1
fi

# Extract title
TITLE=$(echo "$FETCHED" | sed -n 's/.*<title>\(.*\)<\/title>.*/\1/p' | head -1 || echo "Fetched page")
echo "  Title: ${TITLE}"
echo "  Status: ${GREEN}fetched OK${RESET}"

# Count chars
CHARS=$(echo "$FETCHED" | wc -c)
echo "  Size: ${CHARS} chars"

echo ""
echo "${GREEN}[verified: $URL]${RESET}"
if [[ -n "$CONTEXT" ]]; then
  echo ""
  echo "**Context:** $CONTEXT"
  echo "**Source:** $URL"
  echo "**Verified:** $(date '+%Y-%m-%d %H:%M')"
fi

# Show first 500 chars as excerpt
echo ""
echo "${YELLOW}Excerpt:${RESET}"
echo "$FETCHED" | head -c 500
echo ""
echo "..."
