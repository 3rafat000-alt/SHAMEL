#!/usr/bin/env bash
# tool/fnt/lead/frontend-squad.sh — Coordinate parallel frontend tasks
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <action> [name]
Actions:
  create    <name>  — Create worktree branch for frontend task
  list              — List active frontend worktrees
  merge     <name>  — Merge worktree branch to main
  remove    <name>  — Remove worktree after merge
--help"; exit 0; }

PRJ="$1"; ACTION="${2:-}"; NAME="${3:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$ACTION" ] && echo "${R}Error: action required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: $PRJ_DIR not found$X" && exit 1

case "$ACTION" in
  create)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    BRANCH="squad/frontend/$NAME"
    WORKTREE="$PRJ_DIR/../_worktrees/frontend-$NAME"
    mkdir -p "$(dirname "$WORKTREE")"
    git -C "$PRJ_DIR" worktree add -b "$BRANCH" "$WORKTREE" main 2>/dev/null || true
    echo "${G}Worktree:$X $BRANCH → $WORKTREE"
    echo "cd $WORKTREE && npm install"
    ;;
  list)
    git -C "$PRJ_DIR" worktree list 2>/dev/null | grep -v "(bare)" || echo "  None"
    ;;
  merge)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    BRANCH="squad/frontend/$NAME"
    git -C "$PRJ_DIR" checkout main 2>/dev/null || true
    git -C "$PRJ_DIR" merge --no-ff "$BRANCH" -m "feat: merge frontend/$NAME" 2>/dev/null || \
      echo "${Y}Merge conflict — resolve manually$X"
    echo "${G}Merged $BRANCH → main$X"
    ;;
  remove)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    WORKTREE="$PRJ_DIR/../_worktrees/frontend-$NAME"
    git -C "$PRJ_DIR" worktree remove "$WORKTREE" 2>/dev/null || true
    git -C "$PRJ_DIR" branch -D "squad/frontend/$NAME" 2>/dev/null || true
    echo "${G}Removed: $NAME$X"
    ;;
esac
