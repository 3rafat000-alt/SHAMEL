#!/usr/bin/env bash
# tool/dsn/content-strategist/voice-check.sh — Audit copy for tone consistency
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> [--voice "<formal|casual|playful|professional>"]
  Audit project copy for tone consistency.
  Scans .md, .vue, .php, .ts files for tone indicators.
EOF
exit 0
}

PRJ="${1:-}"; VOICE="professional"
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
[[ "${1:-}" == "--voice" ]] && VOICE="${2:-professional}"

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"

# Tone patterns
declare -A TONE_SIGNALS
TONE_SIGNALS["formal"]="please|kindly|regarding|hereby|pursuant|shall|herewith"
TONE_SIGNALS["casual"]="hey|ok|cool|awesome|oops|btw|gonna|wanna"
TONE_SIGNALS["professional"]="thank you|welcome|let us|contact|support|team|help"
TONE_SIGNALS["playful"]="whoops|yay|oopsie|nifty|sparkle|magic|boom"

START_SIGNALS="${TONE_SIGNALS[$VOICE]}"
if [[ -z "$START_SIGNALS" ]]; then
  echo "${RED}Unknown voice: $VOICE (formal|casual|professional|playful)${RESET}"
  exit 1
fi

echo "${BLUE}═══ Voice Consistency Check :: $PRJ ═══${RESET}"
echo "${YELLOW}Target voice:${RESET} $VOICE"
echo ""

# Scan for target voice signals
MATCHES=$(grep -rni "$START_SIGNALS" "$PRJ_DIR" --include='*.vue' --include='*.md' --include='*.php' --include='*.ts' 2>/dev/null | grep -v node_modules | grep -v vendor | head -20)
if [[ -n "$MATCHES" ]]; then
  echo "${GREEN}✓ Voice signals found:${RESET}"
  echo "$MATCHES" | while IFS= read -r line; do echo "  $line"; done
else
  echo "${YELLOW}⚠ No voice signals matching '$VOICE' found${RESET}"
fi

# Scan for conflicting tones
echo ""
echo "${YELLOW}Conflicting tone check:${RESET}"
for other_voice in "casual" "formal" "playful"; do
  [[ "$other_voice" == "$VOICE" ]] && continue
  CONFLICT=$(grep -rni "${TONE_SIGNALS[$other_voice]}" "$PRJ_DIR" --include='*.vue' --include='*.md' 2>/dev/null | grep -v node_modules | grep -v vendor | head -5)
  if [[ -n "$CONFLICT" ]]; then
    echo "  ${RED}⚠${RESET} $other_voice tone detected:"
    echo "$CONFLICT" | sed 's/^/      /'
  fi
done

echo ""
echo "${GREEN}✓ Voice check complete${RESET}"
