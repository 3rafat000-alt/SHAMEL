#!/usr/bin/env bash
# tool/arc/api-architect/openapi-validate.sh — Validate OpenAPI spec against Laravel routes
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--routes-only]
Compare OpenAPI spec paths against registered Laravel routes.
  --routes-only  Only show registered routes (no comparison)
  --help"; exit 0; }

PRJ="$1"; MODE="${2:-}"
[ "$PRJ" = "--help" ] && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SPEC="$PRJ_DIR/docs/api/openapi.yaml"
[ ! -f "$SPEC" ] && echo "${Y}Warning: no OpenAPI spec at $SPEC$X"

echo "${B}=== OpenAPI ↔ Route Validation for $PRJ ===$X"

# Extract paths from OpenAPI spec
if [ -f "$SPEC" ]; then
  echo "${G}OpenAPI spec paths:$X"
  grep -oP '^\s+/[a-z0-9{}/_-]+' "$SPEC" 2>/dev/null | sed 's/^[[:space:]]*//' | sort -u | while read -r p; do
    echo "  $p"
  done
  echo
fi

# Look for Laravel routes
ARTISAN="$PRJ_DIR/artisan"
if [ -f "$ARTISAN" ]; then
  echo "${B}Registered Laravel routes:$X"
  php "$ARTISAN" route:list --compact 2>/dev/null | grep -oP '\s/[a-z0-9{}/_-]+' | sort -u || echo "  ${Y}(php artisan not available, check manually)$X"
else
  # Fallback: grep routes files
  echo "${Y}No artisan found — grepping route files...$X"
  for r in "$PRJ_DIR/routes"/*.php; do
    [ -f "$r" ] || continue
    echo "${B}$(basename $r):$X"
    grep -oP "Route::[a-z]+\([^)]*\)" "$r" 2>/dev/null | grep -oP "'[^']+'" | tr -d "'" | sort -u | while read -r p; do
      echo "  $p"
    done
  done
fi

echo
echo "${Y}Tip: Compare the two lists for endpoints in routes but missing from spec.$X"
