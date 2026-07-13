#!/usr/bin/env bash
# tool/dsn/motion-designer/motion-spec.sh — Generate micro-interaction spec
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") <PRJ-ID> --element "<name>" --trigger "<hover|click|scroll|load>" [--duration "<ms>"] [--easing "<ease-in-out|spring>"] [--output "<file>"]
  Generate micro-interaction motion spec document.
EOF
exit 0
}

PRJ="${1:-}"; ELEM=""; TRIGGER=""; DUR="200ms"; EASING="ease-in-out"; OUTPUT=""
[[ "$PRJ" == "--help" || -z "$PRJ" ]] && usage; shift
while [[ $# -gt 0 ]]; do
  case "$1" in --element) ELEM="$2"; shift;; --trigger) TRIGGER="$2"; shift;;
  --duration) DUR="$2"; shift;; --easing) EASING="$2"; shift;;
  --output) OUTPUT="$2"; shift;; --help) usage;; esac; shift
done
[[ -z "$ELEM" || -z "$TRIGGER" ]] && usage

OUTPUT="${OUTPUT:-$SOFI_ROOT/projects/$PRJ/docs/motion/${ELEM// /_}.md}"
mkdir -p "$(dirname "$OUTPUT")"

cat > "$OUTPUT" <<MOTION
# Motion Spec: ${ELEM}

**PRJ-ID:** $PRJ
**Trigger:** $TRIGGER
**Duration:** $DUR
**Easing:** $EASING

## Animation Sequence

| Phase | Property | From | To | Duration | Easing |
|-------|----------|------|----|----------|--------|
| 1 | opacity | 0 | 1 | $DUR | $EASING |
| 2 | transform: translateY | 10px | 0 | $DUR | $EASING |

## States
- **Enter:** _Describe entrance_
- **Exit:** _Describe exit_
- **Loading:** _Skeleton or spinner_
- **Error:** _Shake or flash_

## Accessibility
- Respects \`prefers-reduced-motion\`: fall back to instant
- No motion triggered without user action

## Implementation Notes
- CSS transitions preferred over JS animation
- Use \`will-change: transform, opacity\` on the animated element

## Acceptance
- [ ] Animation matches spec timing/easing
- [ ] \`prefers-reduced-motion\` respected
- [ ] No layout shift on animation end
MOTION

echo "${GREEN}✓ Motion spec created: $OUTPUT${RESET}"
