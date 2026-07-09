#!/usr/bin/env bash
# tool/str/lead/blueprint-init.sh — Scaffold Project Blueprint from template
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --title "<Project Title>" --problem "<problem>" --user "<target user>"
  Scaffold Project_Blueprint.md from template.
  Initializes Gate 0: Inception artifact.
EOF
exit 0
}

PRJ="${1:-}"; TITLE=""; PROBLEM=""; USER=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --title) TITLE="$2"; shift;; --problem) PROBLEM="$2"; shift;;
  --user) USER="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$TITLE" || -z "$PROBLEM" || -z "$USER" ]] && usage

DOCS="$SOFI_ROOT/projects/$PRJ/docs"
mkdir -p "$DOCS"
BP="$DOCS/Project_Blueprint.md"
[[ -f "$BP" ]] && { echo "${YELLOW}⚠ Blueprint already exists at $BP${RESET}"; exit 1; }

TS=$(date '+%Y-%m-%d')

cat > "$BP" <<BLUEPRINT
# Project Blueprint: $TITLE

**PRJ-ID:** $PRJ
**Created:** $TS
**Gate:** 0 (Inception)
**Author:** str-lead

## Problem Statement
$PROBLEM

## Target User
$USER

## Job-to-be-Done (JTBD)
_What job is the user hiring this product for?_

## Scope
_In-scope:_
_Out-of-scope:_

## Success Metrics
- _Metric 1:_
- _Metric 2:_

## Risks
-
BLUEPRINT

echo "${GREEN}✓ Blueprint created: $BP${RESET}"
echo "  Edit the JTBD, scope, and metrics sections."
