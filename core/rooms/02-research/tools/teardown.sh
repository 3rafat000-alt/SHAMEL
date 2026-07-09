#!/usr/bin/env bash
# tool/res/competitor-analyst/teardown.sh — Competitor feature-by-feature teardown
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); MAGENTA=$(tput setaf 5); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --competitor "<name>" [--features "<f1,f2,f3>"] [--notes "<notes>"]
  Scaffold competitor teardown document with feature scoring.
  Without --features, creates blank template.
EOF
exit 0
}

PRJ="${1:-}"; COMP=""; FEATURES=""; NOTES=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --competitor) COMP="$2"; shift;; --features) FEATURES="$2"; shift;;
  --notes) NOTES="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$COMP" ]] && usage

OUT="$SOFI_ROOT/projects/$PRJ/docs/competitor-teardown-${COMP// /_}.md"
mkdir -p "$(dirname "$OUT")"

{
  echo "# Competitor Teardown: $COMP"
  echo "**PRJ-ID:** $PRJ"
  echo "**Date:** $(date '+%Y-%m-%d')"
  echo ""
  echo "## Overview"
  echo "${NOTES:-*Brief description of the competitor and their market position.*}"
  echo ""
  echo "## Feature Comparison"
  echo ""
  echo "| Feature | Our Product | $COMP | Notes |"
  echo "|---------|-------------|-------|-------|"

  if [[ -n "$FEATURES" ]]; then
    IFS=',' read -ra FARR <<< "$FEATURES"
    for feat in "${FARR[@]}"; do
      echo "| $feat | TBD | TBD | |"
    done
  else
    echo "| _(add feature rows)_ | TBD | TBD | TBD |"
  fi

  echo ""
  echo "## Strengths"
  echo "- _What does $COMP do better?_"
  echo ""
  echo "## Weaknesses"
  echo "- _What do we do better?_"
  echo ""
  echo "## Gaps / Opportunities"
  echo "- _Features $COMP doesn't have that users want_"
} > "$OUT"

echo "${GREEN}✓ Teardown created: $OUT${RESET}"
