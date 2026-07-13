#!/usr/bin/env bash
# tool/knw/doc-writer/diataxis-init.sh — Generate Diataxis doc structure for module
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --module module_name [--output docs/] [--overview 'Brief description']"; exit 0; }
MODULE=""; OUTPUT=""; OVERVIEW=""
while [[ $# -gt 0 ]]; do case "$1" in --module) MODULE="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --overview) OVERVIEW="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$MODULE" ]] && usage
OUTPUT="${OUTPUT:-$SOFI_ROOT/docs/$MODULE}"

echo "${BLUE}[diataxis-init]${RESET} Generating Diataxis docs for $MODULE at $OUTPUT"; echo ""

mkdir -p "$OUTPUT"

# Tutorial
cat > "$OUTPUT/tutorial.md" <<EOF
# Tutorial: Getting Started with $MODULE
**Audience:** Learner, first time
**Goal:** Hands-on experience

${OVERVIEW:-TODO: write tutorial overview}

## Prerequisites

## Step 1:

## Step 2:

## Next Steps
- See [How-to Guide](how-to.md)
EOF
echo "  ${GREEN}✓ tutorial.md${RESET}"

# How-to Guide
cat > "$OUTPUT/how-to.md" <<EOF
# How-to Guide: $MODULE
**Audience:** Practitioner, specific goal
**Goal:** Solve a real problem

## How to [Task A]

## How to [Task B]

## Troubleshooting
EOF
echo "  ${GREEN}✓ how-to.md${RESET}"

# Reference
cat > "$OUTPUT/reference.md" <<EOF
# Reference: $MODULE
**Audience:** Anyone looking up details
**Goal:** Accurate, complete description

## API / CLI Reference

## Configuration

## Schema
EOF
echo "  ${GREEN}✓ reference.md${RESET}"

# Explanation
cat > "$OUTPUT/explanation.md" <<EOF
# Explanation: $MODULE
**Audience:** Someone understanding the big picture
**Goal:** Context, background, design decisions

## Why $MODULE exists

## How it fits in the architecture

## Design decisions
EOF
echo "  ${GREEN}✓ explanation.md${RESET}"

# Index
cat > "$OUTPUT/README.md" <<EOF
# $MODULE Documentation

## Diataxis Quadrant

| Quadrant | File | Read this when… |
|----------|------|-----------------|
| Tutorial | [tutorial.md](tutorial.md) | You want your first hands-on experience |
| How-to | [how-to.md](how-to.md) | You need to accomplish a specific task |
| Reference | [reference.md](reference.md) | You need precise details (API, config, schema) |
| Explanation | [explanation.md](explanation.md) | You want to understand the big picture |

Created: $(date -Iseconds)
EOF
echo "  ${GREEN}✓ README.md${RESET}"

echo ""
echo "${BLUE}[diataxis-init]${RESET} ${GREEN}4 guides + index created at $OUTPUT${RESET}"
