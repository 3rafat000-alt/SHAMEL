#!/usr/bin/env bash
# tool/dat/privacy-officer/pii-map.sh — Scan models for PII fields + encryption status
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--json]
Scan Eloquent models for potential PII fields and encryption status.
  --json   JSON output for CI pipeline
  --help"; exit 0; }

PRJ="$1"; FORMAT="${2:-}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
MODEL_DIR="$PRJ_DIR/app/Models"
[ ! -d "$MODEL_DIR" ] && echo "${R}No models at $MODEL_DIR$X" && exit 1

echo "${B}=== PII Scan: $PRJ ===$X"
echo

PII_PATTERNS="email|phone|address|ssn|passport|dob|birth|name|first_name|last_name|credit_card|iban|bic"
ENC_TYPES="encrypted:cast|Crypt::encrypt|->encrypt"
PII_COUNT=0; UNENC=0

for model in "$MODEL_DIR"/*.php; do
  [ ! -f "$model" ] && continue
  mname=$(basename "$model" .php)
  echo "${B}Model: $mname$X"

  # Find fillable/guarded/casts
  FILLABLE=$(grep -oP "protected\s+\$fillable\s*=\s*\[([^\]]+)\]" "$model" 2>/dev/null | tr ',' '\n' | grep -oP "'[^']+'" | tr -d "'" || true)
  CASTS=$(grep -oP "protected\s+\$casts\s*=\s*\[([^\]]+)\]" "$model" 2>/dev/null || true)

  echo "$FILLABLE" | while read -r field; do
    [ -z "$field" ] && continue
    if echo "$field" | grep -qiP "$PII_PATTERNS"; then
      PII_COUNT=$((PII_COUNT+1))
      if echo "$CASTS" | grep -qi "$field.*encrypted\|encrypted.*$field"; then
        echo "  ${G}[ENCRYPTED]${X} $field"
      else
        echo "  ${R}[UNENCRYPTED PII]${X} $field"
        UNENC=$((UNENC+1))
      fi
    fi
  done
done

echo
echo "${B}Summary:$X $PII_COUNT PII fields, $UNENC unencrypted"

if [ "$FORMAT" = "--json" ]; then
  echo "{\"project\":\"$PRJ\",\"pii_fields\":$PII_COUNT,\"unencrypted\":$UNENC}"
fi

[ "$UNENC" -gt 0 ] && echo "${R}Unencrypted PII fields found. Add '\$casts' => ['field' => 'encrypted']$X"
