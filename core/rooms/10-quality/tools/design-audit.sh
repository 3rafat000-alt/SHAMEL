#!/usr/bin/env bash
# tool/qa/design-auditor/design-audit.sh — Compare built vs frozen spec field-by-field
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --spec spec.yaml --built built.yaml [--output diff.md]"; exit 0; }
SPEC=""; BUILT=""; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --spec) SPEC="$2"; shift2 ;; --built) BUILT="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$SPEC" || -z "$BUILT" ]] && usage
for f in "$SPEC" "$BUILT"; do [[ -f "$f" ]] || { echo "${RED}Error: $f not found${RESET}"; exit 1; }; done

echo "${BLUE}[design-audit]${RESET} Auditing $(basename "$SPEC") vs $(basename "$BUILT")"; echo ""
MISMATCHES=0
MISSING=0
EXTRA=0

# Extract keys from both files
spec_keys=$(grep -oP '^\s+\w+(?=:)' "$SPEC" | sort -u || true)
built_keys=$(grep -oP '^\s+\w+(?=:)' "$BUILT" | sort -u || true)

echo "${YELLOW}  Comparing keys...${RESET}"
for key in $spec_keys; do
  if echo "$built_keys" | grep -qx "$key"; then
    spec_val=$(grep -oP "(?<=^\\s+${key}:\\s).*" "$SPEC" | head -1)
    built_val=$(grep -oP "(?<=^\\s+${key}:\\s).*" "$BUILT" | head -1)
    if [[ "$spec_val" != "$built_val" ]]; then
      echo "    ${RED}✗ $key: spec='$spec_val' ≠ built='$built_val'${RESET}"
      ((MISMATCHES++))
    fi
  else
    echo "    ${YELLOW}⚠ $key: in spec, MISSING from built${RESET}"
    ((MISSING++))
  fi
done

for key in $built_keys; do
  if ! echo "$spec_keys" | grep -qx "$key"; then
    echo "    ${YELLOW}⚠ $key: in built, EXTRA (not in spec)${RESET}"
    ((EXTRA++))
  fi
done

echo ""
echo "${BLUE}[design-audit]${RESET} Summary: $MISMATCHES mismatches, $MISSING missing, $EXTRA extra"

if [[ -n "$OUTPUT" ]]; then
  {
    echo "# Design Audit: $(basename "$SPEC") vs $(basename "$BUILT")"
    echo "Date: $(date -Iseconds)"
    echo "- Mismatches: $MISMATCHES"
    echo "- Missing from built: $MISSING"
    echo "- Extra in built: $EXTRA"
  } > "$OUTPUT"
  echo "${BLUE}[design-audit] Report written to $OUTPUT${RESET}"
fi

[[ $MISMATCHES -eq 0 && $MISSING -eq 0 && $EXTRA -eq 0 ]] && echo "${GREEN}[design-audit] PASS — spec matches built${RESET}" && exit 0
echo "${YELLOW}[design-audit] REVIEW — discrepancies found${RESET}"
exit 1
