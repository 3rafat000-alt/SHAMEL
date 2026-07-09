#!/usr/bin/env bash
# tool/brd/chief-of-staff/rccf-gen.sh — Generate RCCF work order block
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") --role <name> --agent <agent> --project <PRJ-ID> --ticket <TKT> [--gate <N>] [--artifact <path>]
  Generate a complete RCCF delegation block (4 fields).
EOF
exit 0
}

ROLE=""; AGENT=""; PRJ=""; TKT=""; GATE=""; ARTIFACT=""
while [[ $# -gt 0 ]]; do
  case "$1" in --role) ROLE="$2"; shift;; --agent) AGENT="$2"; shift;;
  --project) PRJ="$2"; shift;; --ticket) TKT="$2"; shift;;
  --gate) GATE="$2"; shift;; --artifact) ARTIFACT="$2"; shift;;
  --help) usage;; *) echo "Unknown: $1"; usage;;
  esac; shift
done
[[ -z "$ROLE" || -z "$AGENT" || -z "$PRJ" || -z "$TKT" ]] && usage

ROSTER="$SOFI_ROOT/engine/ROSTER.md"
# Try to extract route from roster
MODEL="claude"

cat <<RCCF
🎭 Role     You are ${ROLE} — ${AGENT}.
            Model: ${MODEL} (session model)
            Spec: engine/agents/${AGENT}.md

📂 Context  Foundation: Teaching I (Design is Truth) + Teaching IV (Token Economy).
            Project ${PRJ} · Gate ${GATE:-current}.
            Read: ${PRJ}/_context/STATE.md · HANDOFFS.md · CONTEXT.md.
            Frozen artifact: ${ARTIFACT:-none specified}.

🎯 Command  Execute ticket ${TKT} per HANDOFFS.md.
            In-bounds: defined in ticket.
            Out-of-bounds: schema changes, other endpoints, other projects.
            Success: ticket definition of done.

📐 Format   Path: projects/${PRJ}/
            Standards: per role spec.
            Gate-bar: per gate-check.
            Evidence: paste command output + exit code in handoff.
            Handoff: → next agent per HANDOFFS.md.

RCCF
echo "${GREEN}✓ RCCF block generated${RESET}"
