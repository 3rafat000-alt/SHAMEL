#!/usr/bin/env bash
# tool/bck/blade-engineer/blade-gen.sh — Generate Blade component from spec
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <component-name> [props]
Generate a Blade component (class + view) with props.
  component-name  e.g., user-profile, order-card
  props           Comma-separated: name(string),count(int)
Example: blade-gen.sh PRJ-SAKK user-profile name(string),avatar(string|null)
--help"; exit 0; }

PRJ="$1"; COMP="${2:-}"; PROPS="${3:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$COMP" ] && echo "${R}Error: component name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
PASCAL=$(echo "$COMP" | sed 's/-/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')
KEBAB=$(echo "$COMP" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')
DIR="$PRJ_DIR/app/View/Components"
VIEW_DIR="$PRJ_DIR/resources/views/components"
mkdir -p "$DIR" "$VIEW_DIR"

# Component class
CLASS_FILE="$DIR/${PASCAL}.php"
if [ ! -f "$CLASS_FILE" ]; then
  PROP_DECL=""; PROP_CTOR=""; PROP_BODY=""
  if [ -n "$PROPS" ]; then
    IFS=',' read -ra P <<< "$PROPS"
    for p in "${P[@]}"; do
      pname=$(echo "$p" | cut -d'(' -f1)
      ptype=$(echo "$p" | cut -d'(' -f2 | sed 's/)//')
      PROP_DECL+="    public $${pname};"$'\n'
      PROP_CTOR+="        \$this->${pname} = \$${pname};"$'\n'
      PROP_PARAMS+="        public ${ptype} \$${pname} = null,"$'\n'
    done
  fi

  cat > "$CLASS_FILE" <<PHP
<?php
namespace App\View\Components;
use Illuminate\View\Component;
class ${PASCAL} extends Component
{
${PROP_DECL}
    public function __construct(
$(echo "$PROP_PARAMS" | sed '$ s/,$//')
    ) {
$(echo "$PROP_CTOR")
    }

    public function render()
    {
        return view('components.${KEBAB}');
    }
}
PHP
echo "${G}Class:$X $CLASS_FILE"
fi

# View
VIEW_FILE="$VIEW_DIR/${KEBAB}.blade.php"
if [ ! -f "$VIEW_FILE" ]; then
cat > "$VIEW_FILE" <<HTML
<div {{ \$attributes->merge(['class' => '']) }}>
    <h3>{{ \$slot ?? '${PASCAL}' }}</h3>
</div>
HTML
echo "${G}View:$X $VIEW_FILE"
fi

echo "${B}Done.$X Usage: <x-${KEBAB} />"
