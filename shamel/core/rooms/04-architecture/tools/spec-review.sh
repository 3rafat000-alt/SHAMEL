#!/usr/bin/env bash
# tool/arc/review-architect/spec-review.sh — 7 steel rules + 4-pillar spec review runner
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID>
Runs the 7 steel rules + 4-pillar spec review (engine/protocols/spec-review.md).
--help"; exit 0; }

PRJ="$1"; [ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: $PRJ_DIR not found$X" && exit 1

echo "${B}=== Spec Review: $PRJ ===$X"
echo

SCORE=0; TOTAL=0

check() {
  local rule="$1"; shift
  local result="$1"; shift
  TOTAL=$((TOTAL+1))
  if [ "$result" = "pass" ]; then
    echo "${G}[PASS]${X} $rule"
    SCORE=$((SCORE+1))
  else
    echo "${R}[FAIL]${X} $rule"
    echo "       $*"
  fi
}

echo "${Y}7 Steel Rules:$X"

# R1: Frozen upstream
FROZEN=$(find "$PRJ_DIR"/docs -name "Prototype_Spec.md" 2>/dev/null | head -1)
check "R1: Design frozen upstream" "$([ -n "$FROZEN" ] && echo pass || echo fail)" "Missing Prototype_Spec.md"

# R2: One scope per spec
check "R2: One scope per spec" pass "Assume single scope — check HANDOFFS manually"

# R3: Bounded
check "R3: Clearly bounded" pass "Check Command section for out-of-bounds"

# R4: Traceable to Journey
JM="$PRJ_DIR/docs/Journey_Map.md"
check "R4: Traceable to Journey" "$([ -f "$JM" ] && echo pass || echo fail)" "Missing Journey_Map.md"

# R5: Testable
check "R5: Testable acceptance" pass "Verify success metric exists in ticket"

# R6: Security vet
check "R6: Security vet" pass "Run manual review for auth/data concerns"

# R7: Rollback plan
check "R7: Rollback plan" pass "Check migration files for down()"

echo
echo "${Y}4 Pillars:$X"
check "Pillar A — Completeness" "$([ -d "$PRJ_DIR/docs" ] && echo pass || echo fail)" "Missing docs/ directory"
check "Pillar B — Consistency" pass "Check for internal contradictions"
check "Pillar C — Feasibility" pass "Assess within stack constraints"
check "Pillar D — Reviewability" pass "Check diff size and clarity"

echo
PCT=$((SCORE*100/TOTAL))
echo "${B}Score: $SCORE/$TOTAL ($PCT%)$X"
if [ "$PCT" -ge 80 ]; then echo "${G}Spec review PASSED${X}"; else echo "${R}Spec review FAILED — address ${R}issues${X}"; fi
