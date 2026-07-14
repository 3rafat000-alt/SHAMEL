#!/usr/bin/env bash
# tool/ops/lead/ci-status.sh — Check CI/CD pipeline health
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--workflow <name>] [--check lint|test|build|scan]"; exit 0; }
PRJ=""; WORKFLOW=""; CHECK=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --workflow) WORKFLOW="$2"; shift2 ;; --check) CHECK="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done

echo "${BLUE}[ci-status]${RESET} CI/CD health for ${PRJ:-all projects}"; echo ""
FAIL=0

scan_ci() {
  local dir="$1" label="$2"
  local ci_files
  ci_files=$(find "$dir" -maxdepth 3 -name ".github" -type d 2>/dev/null || true)
  if [[ -z "$ci_files" ]]; then
    echo "  $label: ${YELLOW}No CI config detected${RESET}"
    return
  fi

  for wf in "$dir/.github/workflows"/*.yml "$dir/.github/workflows"/*.yaml; do
    [[ -f "$wf" ]] || continue
    local name
    name=$(basename "$wf" .yml)
    name="${name%.yaml}"
    local wf_check="${WORKFLOW:-}"
    [[ -n "$wf_check" && "$name" != "$wf_check" ]] && continue

    echo "  $label — $name:"
    local has_lint=false has_test=false has_build=false
    grep -q "lint\|phpcs\|eslint\|ruff" "$wf" 2>/dev/null && has_lint=true
    grep -q "test\|phpunit\|pytest\|jest" "$wf" 2>/dev/null && has_test=true
    grep -q "build\|compile\|vite\|mix" "$wf" 2>/dev/null && has_build=true

    echo -n "    lint: "; $has_lint && echo "${GREEN}✓${RESET}" || echo "${YELLOW}—${RESET}"
    echo -n "    test: "; $has_test && echo "${GREEN}✓${RESET}" || echo "${YELLOW}—${RESET}"
    echo -n "    build: "; $has_build && echo "${GREEN}✓${RESET}" || echo "${YELLOW}—${RESET}"
  done
}

if [[ -n "$PRJ" ]]; then
  scan_ci "$SOFI_ROOT/projects/$PRJ" "PRJ-$PRJ"
else
  for d in "$SOFI_ROOT/projects"/*/; do
    [[ -d "$d" ]] && scan_ci "$d" "$(basename "$d")"
  done
  scan_ci "$SOFI_ROOT" "SOFI Framework"
fi

echo "${GREEN}[ci-status] Done.${RESET}"
