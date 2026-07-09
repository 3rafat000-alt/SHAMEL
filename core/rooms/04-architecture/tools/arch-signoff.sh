#!/usr/bin/env bash
# tool/arc/lead/arch-signoff.sh — Assemble + sign Gate 3 architecture package
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" N="$(tput setaf 6)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--check-only]
Sign off Gate 3 architecture package for a project.

Checks:
  - docs/Project_Blueprint.md exists
  - docs/Journey_Map.md exists  
  - docs/Prototype_Spec.md exists
  - Component diagram exists
  - Schema migration exists
  - API spec exists

Options:
  --check-only   Only audit, don't write signoff
  --help         Show this message"; exit 0; }

PRJ="$1"; CHECK_ONLY="${2:-}"

[ "$PRJ" = "--help" ] && usage
[ -z "$PRJ" ] && echo "${R}Error: PRJ-ID required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: $PRJ_DIR not found$X" && exit 1

ARCH_DIR="$PRJ_DIR/docs/architecture"
SIGNOFF="$PRJ_DIR/_context/signoffs/gate3-signoff.md"

REQUIRED=(
  "$PRJ_DIR/docs/Project_Blueprint.md"
  "$PRJ_DIR/docs/Journey_Map.md"
  "$PRJ_DIR/docs/Prototype_Spec.md"
  "$ARCH_DIR/component-diagram.md"
  "$PRJ_DIR/database/migrations"
  "$PRJ_DIR/docs/api/openapi.yaml"
)

PASS=0; FAIL=0
for f in "${REQUIRED[@]}"; do
  if [ -e "$f" ] || [ -d "$f" ]; then
    echo "${G}[PASS]${X} $f"; ((PASS++))
  else
    echo "${R}[FAIL]${X} $f"; ((FAIL++))
  fi
done

echo
echo "${B}Results:${X} $PASS/${#REQUIRED[@]} pass, $FAIL fail"

if [ "$CHECK_ONLY" = "--check-only" ]; then
  [ $FAIL -gt 0 ] && exit 1 || exit 0
fi

if [ $FAIL -gt 0 ]; then
  echo "${R}Cannot sign off — $FAIL deliverables missing$X"
  exit 1
fi

mkdir -p "$(dirname "$SIGNOFF")"
cat > "$SIGNOFF" <<SIG
# Gate 3 Signoff — $PRJ
**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Signed by:** Architecture Lead (arc-lead)
**Status:** ✅ APPROVED

## Deliverables verified
$(for f in "${REQUIRED[@]}"; do echo " - [x] $f"; done)

**Architecture frozen.** No structural changes without ADR.
SIG

echo "${G}Signoff written: $SIGNOFF$X"
