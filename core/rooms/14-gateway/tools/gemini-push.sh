#!/usr/bin/env bash
# tool/gtw/external-reviewer/gemini-push.sh — Push finding to Gemini review desk
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --text "<finding>" [--ask "<question>"] [--stdin]
  Push a finding to the Gemini external review desk.
  Uses sofi gemini review if available, else prints formatted block.
  --stdin: read finding from stdin instead of --text.
EOF
exit 0
}

PRJ="${1:-}"; TEXT=""; ASK="guidance: which path? why? next steps?"
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --text) TEXT="$2"; shift;; --ask) ASK="$2"; shift;;
  --stdin) TEXT="$(cat)";; --help) usage;; esac; shift
done
[[ -z "$TEXT" ]] && usage

# Standing preamble — tells Gemini it's advising autonomous AI
PREAMBLE='[سياق ثابت] أنت مستشار معماري كبير تُوجّه وكيل ذكاء اصطناعي ذاتي التشغيل (SOFI AI)، لستَ تخاطب إنساناً. الوكيل سينفّذ توجيهك مباشرةً. أعطِ توجيهاً مفصّلاً ودقيقاً قابلاً للتنفيذ خطوة بخطوة، لكل توصية سبب + أثر + خطوة ملموسة، مرتّباً بالأولوية.'

FULL_TEXT="${PREAMBLE}

## Finding
${TEXT}

## Question
${ASK}"

# Try sofi gemini review
SOFI_CMD="${SOFI_ROOT}/engine/tooling/bin/sofi"
if [[ -x "$SOFI_CMD" ]]; then
  echo "${BLUE}Pushing to Gemini desk...${RESET}"
  echo "$FULL_TEXT" | "$SOFI_CMD" gemini review --prj "$PRJ" --json 2>/dev/null && {
    echo "${GREEN}✓ Pushed to Gemini desk${RESET}"
    exit 0
  }
fi

# Fallback: print formatted block
echo "${YELLOW}⚠ sofi gemini not available — printing standalone block${RESET}"
echo "${BLUE}════════════════════════════════════════════${RESET}"
echo "$FULL_TEXT"
echo "${BLUE}════════════════════════════════════════════${RESET}"
echo ""
echo "To push manually: cat << 'EOF' | sofi gemini review --prj $PRJ --json"
echo "$FULL_TEXT"
echo "EOF"
