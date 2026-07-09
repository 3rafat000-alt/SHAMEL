#!/usr/bin/env bash
# tool/fnt/react-engineer/react-component.sh — Scaffold typed React component
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <ComponentName> [props...]
Scaffold a typed React component with props interface.
  props  Comma-separated: title:string,onClick:()=>void
Example: react-component.sh PRJ-SAKK UserCard name:string,age:number
--help"; exit 0; }

PRJ="$1"; COMP="${2:-}"; PROPS="${3:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$COMP" ] && echo "${R}Error: ComponentName required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
KEBAB=$(echo "$COMP" | sed 's/\([A-Z]\)/-\L\1/g; s/^-//')
DIR="$PRJ_DIR/resources/ts/components"
mkdir -p "$DIR"

FILE="$DIR/${COMP}.tsx"
if [ ! -f "$FILE" ]; then
  PROP_IFACE=""
  if [ -n "$PROPS" ]; then
    IFS=',' read -ra P <<< "$PROPS"
    for p in "${P[@]}"; do
      pn=$(echo "$p" | cut -d: -f1)
      pt=$(echo "$p" | cut -d: -f2)
      PROP_IFACE+="  ${pn}: ${pt};"$'\n'
    done
  fi

cat > "$FILE" <<TSX
interface ${COMP}Props {
${PROP_IFACE}}

export default function ${COMP}({ children, ...props }: React.PropsWithChildren<${COMP}Props>) {
  return (
    <div className="${KEBAB}">
      {children}
    </div>
  )
}
TSX
echo "${G}Component:$X $FILE"
fi

echo "${B}Done.$X Import: import ${COMP} from '@/components/${COMP}'"
