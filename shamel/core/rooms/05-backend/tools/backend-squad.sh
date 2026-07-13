#!/usr/bin/env bash
# tool/bck/lead/backend-squad.sh — Coordinate parallel backend worktrees
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <action> [name]
Actions:
  create    <name>  — Create git worktree branch for parallel task
  list              — List active backend worktrees
  merge     <name>  — Merge worktree branch back to main
  remove    <name>  — Remove worktree after merge
Example:
  backend-squad.sh PRJ-SAKK create api-auth
  backend-squad.sh PRJ-SAKK list
--help"; exit 0; }

PRJ="$1"; ACTION="${2:-}"; NAME="${3:-}"
[ "$PRJ" = "--help" ] && usage
[ -z "$ACTION" ] && echo "${R}Error: action required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
[ ! -d "$PRJ_DIR" ] && echo "${R}Error: $PRJ_DIR not found$X" && exit 1
[ ! -d "$PRJ_DIR/.git" ] && echo "${Y}Warning: not a git repo — worktree commands will fail$X"

case "$ACTION" in
  create)
    [ -z "$NAME" ] && echo "${R}Error: worktree name required$X" && exit 1
    BRANCH="squad/backend/$NAME"
    WORKTREE="$PRJ_DIR/../_worktrees/$NAME"
    mkdir -p "$(dirname "$WORKTREE")"
    git -C "$PRJ_DIR" worktree add -b "$BRANCH" "$WORKTREE" main 2>/dev/null || \
      echo "${Y}Worktree already exists or failed$X"
    echo "${G}Worktree created: $BRANCH → $WORKTREE$X"
    echo "cd $WORKTREE && composer install && cp .env.example .env"
    ;;
  list)
    echo "${B}Active backend worktrees:$X"
    git -C "$PRJ_DIR" worktree list 2>/dev/null | grep -v "(bare)" || echo "  None"
    ;;
  merge)
    [ -z "$NAME" ] && echo "${R}Error: worktree name required$X" && exit 1
    BRANCH="squad/backend/$NAME"
    git -C "$PRJ_DIR" checkout main 2>/dev/null || true
    git -C "$PRJ_DIR" merge --no-ff "$BRANCH" -m "feat: merge backend/$NAME" 2>/dev/null || \
      echo "${Y}Merge conflict — resolve manually$X"
    echo "${G}Merged $BRANCH → main$X"
    ;;
  remove)
    [ -z "$NAME" ] && echo "${R}Error: worktree name required$X" && exit 1
    WORKTREE="$PRJ_DIR/../_worktrees/$NAME"
    git -C "$PRJ_DIR" worktree remove "$WORKTREE" 2>/dev/null || true
    git -C "$PRJ_DIR" branch -D "squad/backend/$NAME" 2>/dev/null || true
    echo "${G}Worktree removed: $NAME$X"
    ;;
esac
