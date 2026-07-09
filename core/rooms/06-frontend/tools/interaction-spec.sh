#!/usr/bin/env bash
# tool/fnt/interaction-engineer/interaction-spec.sh — Generate interaction spec from description
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <component-name> <description>
Generate a structured interaction spec from natural language description.
  component-name  e.g., dropdown-menu, modal-dialog
  description     e.g., 'opens on click, closes on blur, animates with fade'
Outputs a YAML interaction spec file.
--help"; exit 0; }

PRJ="$1"; COMP="${2:-}"; shift 2 2>/dev/null || true
DESC="${*:-}"
[ "$PRJ" = "--help" ] && usage
[ -z "$COMP" ] && echo "${R}Error: component name required$X" && usage
[ -z "$DESC" ] && echo "${R}Error: description required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SPEC_DIR="$PRJ_DIR/docs/interactions"
mkdir -p "$SPEC_DIR"
FILE="$SPEC_DIR/${COMP}-interaction.yaml"

# Parse description keywords into spec
TRIGGERS="click"; EFFECTS="toggle"
echo "$DESC" | grep -qi "hover" && TRIGGERS="$TRIGGERS, hover"
echo "$DESC" | grep -qi "focus" && TRIGGERS="$TRIGGERS, focus"
echo "$DESC" | grep -qi "blur" && TRIGGERS="$TRIGGERS, blur"
echo "$DESC" | grep -qi "key" && TRIGGERS="$TRIGGERS, keyboard"
echo "$DESC" | grep -qi "anim" && EFFECTS="$EFFECTS, animation"
echo "$DESC" | grep -qi "fade" && EFFECTS="$EFFECTS, fade"
echo "$DESC" | grep -qi "slide" && EFFECTS="$EFFECTS, slide"

cat > "$FILE" <<YAML
# Interaction Spec: ${COMP}
# Generated from: "${DESC}"
component: $COMP

states:
  - idle
  - active
  - disabled

triggers:
$(echo "$TRIGGERS" | tr ',' '\n' | sed 's/^ //' | sed 's/^/  - /')

effects:
$(echo "$EFFECTS" | tr ',' '\n' | sed 's/^ //' | sed 's/^/  - /')

accessibility:
  keyboard: "[Enter/Space] to activate"
  aria: "aria-expanded, aria-controls"
  focus_trap: ${COMP} contains focus

transitions:
  duration: "200ms"
  easing: "ease-in-out"
YAML

echo "${G}Interaction spec created:$X $FILE"
echo "${Y}Edit $FILE to refine.$X"
