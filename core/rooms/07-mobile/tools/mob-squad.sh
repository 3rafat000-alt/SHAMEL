#!/usr/bin/env bash
# tool/mob/lead/mob-squad.sh — Coordinate mobile worktrees
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <action> [name]
Actions:
  create    <name>  — Create worktree branch for mobile task
  list              — List active mobile worktrees
  merge     <name>  — Merge worktree branch to main
  remove    <name>  — Remove worktree
--help"; exit 0; }

PRJ="$1"; ACTION="${2:-}"; NAME="${3:-}"
[ "$PRJ" = "--help" ] && usage; [ -z "$ACTION" ] && echo "${R}Error: action required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: project not found$X" && exit 1

case "$ACTION" in
  create)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    BRANCH="squad/mobile/$NAME"
    WORKTREE="$PRJ_DIR/../_worktrees/mobile-$NAME"
    mkdir -p "$(dirname "$WORKTREE")"
    git -C "$PRJ_DIR" worktree add -b "$BRANCH" "$WORKTREE" main 2>/dev/null || true
    echo "${G}Worktree:$X $BRANCH → $WORKTREE"
    echo "cd $WORKTREE && flutter pub get"
    ;;
  list)
    git -C "$PRJ_DIR" worktree list 2>/dev/null | grep -v "(bare)" || echo "  None"
    ;;
  merge)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    BRANCH="squad/mobile/$NAME"
    git -C "$PRJ_DIR" checkout main 2>/dev/null || true
    git -C "$PRJ_DIR" merge --no-ff "$BRANCH" -m "feat: merge mobile/$NAME" 2>/dev/null || \
      echo "${Y}Merge conflict$X"
    echo "${G}Merged$X"
    ;;
  remove)
    [ -z "$NAME" ] && echo "${R}Error: name required$X" && exit 1
    WORKTREE="$PRJ_DIR/../_worktrees/mobile-$NAME"
    git -C "$PRJ_DIR" worktree remove "$WORKTREE" 2>/dev/null || true
    git -C "$PRJ_DIR" branch -D "squad/mobile/$NAME" 2>/dev/null || true
    echo "${G}Removed:$X $NAME"
    ;;
esac
