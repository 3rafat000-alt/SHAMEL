#!/usr/bin/env bash
# tool/arc/integration-architect/webhook-map.sh — Generate webhook flow diagram (Mermaid)
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" N="$(tput setaf 6)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> [event-name]
Scan webhook/event config and generate Mermaid sequence diagram.
If event-name given, filter to that event.
--help"; exit 0; }

PRJ="$1"; FILTER="${2:-}"
[ "$PRJ" = "--help" ] && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
EVENTS_DIR="$PRJ_DIR/app/Events"
LISTEN_DIR="$PRJ_DIR/app/Listeners"

echo "${B}Webhook Flow: $PRJ${FILTER:+ (filter: $FILTER)}$X"
echo
echo 'sequenceDiagram'
echo '  participant External as External System'
echo '  participant Webhook as Webhook Controller'
echo '  participant Event as Event Dispatcher'
echo '  participant Handler as Handler/Job'

# Scan event files
for f in "$EVENTS_DIR"/*.php; do
  [ -f "$f" ] || continue
  ev=$(basename "$f" .php)
  [[ -n "$FILTER" && "$ev" != *"$FILTER"* ]] && continue
  echo "  External->>Webhook: POST webhook/$ev"
  echo "  Webhook->>Event: dispatch(new ${ev}(...))"

  # Find listeners for this event
  grep -rl "$ev" "$LISTEN_DIR" 2>/dev/null | while read -r lf; do
    lname=$(basename "$lf" .php)
    echo "  Event->>Handler: $lname"
    echo "  Handler-->>External: 200 OK"
  done
done

# Also scan webhook routes
for r in "$PRJ_DIR/routes/webhooks.php" "$PRJ_DIR/routes/api.php"; do
  [ -f "$r" ] || continue
  grep -oP "Route::post\(['\"]([^'\"]+)['\"]" "$r" 2>/dev/null | while read -r route; do
    endpoint=$(echo "$route" | cut -d"'" -f2)
    [[ -n "$FILTER" && "$endpoint" != *"$FILTER"* ]] && continue
    echo "  External->>Webhook: POST $endpoint"
  done
done

echo
echo "${G}Add '%%| diagram' in your markdown to render.$X"
