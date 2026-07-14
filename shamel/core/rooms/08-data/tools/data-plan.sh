#!/usr/bin/env bash
# tool/dat/lead/data-plan.sh — Generate data plan from Gate 3 architecture
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [--output <file>]
Read Gate 3 architecture artifacts and generate a data plan covering:
  - Database tables/relationships
  - Cache strategy
  - Analytics events
  - Data retention
  - Backup schedule
--help"; exit 0; }

PRJ="$1"; OUTPUT="${2:-$PRJ_DIR/docs/data-plan.md}"
[ "$PRJ" = "--help" ] && usage
PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: project not found$X" && exit 1

# Collect info
MIGRATIONS=$(find "$PRJ_DIR/database/migrations" -name "*.php" 2>/dev/null | wc -l)
MODELS=$(find "$PRJ_DIR/app/Models" -name "*.php" 2>/dev/null | wc -l)
SCHEMA_FILE="$PRJ_DIR/docs/api/openapi.yaml"
MONGO=$(find "$PRJ_DIR" -name "*.mongodb" -o -name "mongo*" 2>/dev/null | head -3 || true)

OUTPUT="$PRJ_DIR/docs/data-plan.md"
mkdir -p "$(dirname "$OUTPUT")"

cat > "$OUTPUT" <<MD
# Data Plan: $PRJ
**Generated:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Source:** Gate 3 architecture artifacts

## Database
- **Engine:** MySQL/PostgreSQL (Laravel default)
- **Migrations:** $MIGRATIONS files
- **Models:** $MODELS Eloquent models
- **Relationships:** See model files for \$hasMany/\$belongsTo

## Cache Strategy
- **Application:** Redis (cache + sessions)
- **Query Cache:** recommended for read-heavy endpoints
- **TTL:** Default 3600s — adjust per endpoint criticality

## Analytics Events
- Track key user actions (\`AnalyticsEvent::dispatch(...)\`)
- Events: page_view, action_performed, error_occurred
- Pipeline: Event → DB → Export

## Data Retention
- Active data: indefinite
- Soft deletes: 30 days before pruning
- Logs: 90 days rotation

## Backup Schedule
- Daily: database dump
- Weekly: full project backup
- DR: cross-region replication (if configured)

## Security
- Encryption: Laravel ENV-based AES-256
- PII fields: \`\$casts\` with encrypted:cast
MD

[ -n "$MONGO" ] && echo "- MongoDB configs found: $MONGO" >> "$OUTPUT"

echo "${G}Data plan created:$X $OUTPUT"
