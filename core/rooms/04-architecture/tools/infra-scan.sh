#!/usr/bin/env bash
# tool/arc/infra-architect/infra-scan.sh — Scan network/scaling/dr posture
set -euo pipefail
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID|--self>
Scan infrastructure configuration for a project.
  --self   Scan the SOFI framework itself
  --help"; exit 0; }

TARGET="${1:---self}"
[ "$TARGET" = "--help" ] && usage

if [ "$TARGET" = "--self" ]; then
  SCAN_DIR="$HOME/Desktop/Lorka"
else
  SCAN_DIR="$HOME/Desktop/Lorka/projects/$TARGET"
fi

[ ! -d "$SCAN_DIR" ] && echo "${R}Error: $SCAN_DIR not found$X" && exit 1

echo "${B}=== Infrastructure Scan: $(basename $SCAN_DIR) ===$X"
echo

# Docker
echo "${Y}[Network]$X"
find "$SCAN_DIR" -maxdepth 2 -name "docker-compose*" -o -name "Dockerfile" 2>/dev/null | while read -r f; do
  echo "  ${G}Found:$X $f"
done
[ -z "$(find "$SCAN_DIR" -maxdepth 2 \( -name "docker-compose*" -o -name "Dockerfile" \) 2>/dev/null)" ] && echo "  No Docker config found"

# Scaling
echo "${Y}[Scaling]$X"
for f in "$SCAN_DIR"/Procfile "$SCAN_DIR"/.fly.yaml "$SCAN_DIR"/render.yaml; do
  [ -f "$f" ] && echo "  ${G}Deploy config:$X $f" || true
done

# DR / backup
echo "${Y}[Backup/DR]$X"
cron_files=$(find "$SCAN_DIR"/database -name "backup*" -o -name "*.sh" 2>/dev/null | head -5)
[ -n "$cron_files" ] && echo "$cron_files" | sed 's/^/  /'
[ -z "$cron_files" ] && echo "  No backup scripts found"

# Health checks
echo "${Y}[Health Checks]$X"
grep -r "health.*check\|healthcheck\|/health" "$SCAN_DIR/routes" 2>/dev/null | head -5 | sed 's/^/  /' || echo "  No health check endpoint found"

# Resources
echo "${Y}[Resource Config]$X"
find "$SCAN_DIR" -name ".env.example" -maxdepth 1 | while read -r f; do
  grep -E "DB_|REDIS_|QUEUE_" "$f" 2>/dev/null | sed 's/^/  /' || echo "  No resource vars found"
done

echo
echo "${B}Scan complete.$X ${Y}Address gaps before Gate 3 signoff.$X"
