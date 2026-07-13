#!/usr/bin/env bash
# tool/dat/cache-engineer/cache-strategy.sh — Generate Redis cache strategy with invalidation plan
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--analyze]
Analyze controllers/services and generate a Redis cache strategy.
  --analyze  Scan for Cache::/Cache facade usage
  --help"; exit 0; }

PRJ="$1"; MODE="${2:-}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
OUTPUT="$PRJ_DIR/docs/cache-strategy.md"

echo "${B}=== Cache Strategy: $PRJ ===$X"
echo

# Scan existing cache usage
CACHE_USAGE=$(grep -rn "Cache::\|cache(" "$PRJ_DIR/app" 2>/dev/null | grep -v ".md" | head -20 || true)
if [ -n "$CACHE_USAGE" ]; then
  echo "${Y}Existing cache usage:$X"
  echo "$CACHE_USAGE" | head -10 | while IFS= read -r line; do
    echo "  $line"
  done
else
  echo "${Y}No Cache:: calls found. Generating fresh strategy.$X"
fi

mkdir -p "$(dirname "$OUTPUT")"
cat > "$OUTPUT" <<YAML
# Cache Strategy: $PRJ
## Redis Configuration
redis:
  host: \${REDIS_HOST}
  port: \${REDIS_PORT}
  prefix: "${PRJ,,}:"

## Cache Keys
# Format: {prefix}:{type}:{id}
keys:
  model_cache: "${PRJ,,}:models:{model}:{id}"
  query_result: "${PRJ,,}:queries:{hash}"
  session: "${PRJ,,}:session:{id}"

## TTL Strategy
ttl:
  default: 3600
  hot_data: 300
  cold_data: 86400
  session: 7200

## Invalidation Plan
invalidation:
  - on_model_save: flush model cache key
  - on_bulk_update: flush query result cache
  - on_schema_change: flush entire prefix

## Tagging (Redis >= 4.0)
tags:
  user: ["user:{id}", "roles:{id}"]
  content: ["content:{id}", "category:{cat_id}"]
YAML

echo "${G}Strategy created:$X $OUTPUT"

if [ "$MODE" = "--analyze" ]; then
  echo
  echo "${B}Recommendations:$X"
  echo "  - Use Cache::remember() for read-heavy endpoints"
  echo "  - Tag related caches for bulk invalidation"
  echo "  - Monitor cache hit ratio in production"
fi
