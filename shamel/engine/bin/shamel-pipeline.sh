#!/usr/bin/env bash
# shamel-pipeline.sh — SHAMEL master orchestrator library
# Source this in any SHAMEL bash script:
#   source "$(dirname "$0")/shamel-pipeline.sh"
set -euo pipefail

# ── Detect SHAMEL_HOME ─────────────────────────────────────────────────────────
SHAMEL_HOME="${SHAMEL_HOME:-$(cd "$(dirname "$0")/../../.." && pwd)}"
SHAMEL_BIN="${SHAMEL_HOME}/shamel/engine/bin"
SHAMEL_AGENTS="${SHAMEL_HOME}/shamel/agents"
SHAMEL_ROOMS="${SHAMEL_HOME}/shamel/core/rooms"
SHAMEL_BRAIN="${SHAMEL_HOME}/shamel/brain"
SHAMEL_TOOLS="${SHAMEL_HOME}/shamel/engine/shamel_tools"
export PYTHONPATH="${SHAMEL_HOME}/shamel/engine:${PYTHONPATH:-}"

# ── Colors ────────────────────────────────────────────────────────────────────
readonly C_RESET='\033[0m'
readonly C_RED='\033[0;31m'
readonly C_GREEN='\033[0;32m'
readonly C_YELLOW='\033[1;33m'
readonly C_BOLD='\033[1m'
readonly C_CYAN='\033[0;36m'

# ── Logging ────────────────────────────────────────────────────────────────────
shamel::log()     { echo -e "${C_GREEN}✓${C_RESET} $*"; }
shamel::warn()    { echo -e "${C_YELLOW}⚠${C_RESET} $*" >&2; }
shamel::error()   { echo -e "${C_RED}✗${C_RESET} $*" >&2; }
shamel::info()    { echo -e "${C_CYAN}→${C_RESET} $*"; }
shamel::header()  { echo -e "\n${C_BOLD}━━ $* ━━${C_RESET}"; }

# ── Health check ───────────────────────────────────────────────────────────────
shamel::check_health() {
  local ok=0
  shamel::header "SHAMEL Health Check"

  # Root structure
  for d in "$SHAMEL_AGENTS" "$SHAMEL_ROOMS" "$SHAMEL_BRAIN" "$SHAMEL_TOOLS"; do
    if [[ -d "$d" ]]; then
      shamel::log "$d exists"
    else
      shamel::error "$d missing"
      ok=1
    fi
  done

  # CLI dispatcher
  if [[ -x "${SHAMEL_BIN}/shamel" ]]; then
    shamel::log "CLI dispatcher: ${SHAMEL_BIN}/shamel"
  else
    shamel::error "CLI dispatcher missing or not executable"
    ok=1
  fi

  # Agent count
  local agent_count=0
  if [[ -d "$SHAMEL_AGENTS" ]]; then
    agent_count=$(find "$SHAMEL_AGENTS" -name '*.md' | wc -l)
    shamel::log "Agents: $agent_count"
  fi

  # Room count
  local room_count=0
  if [[ -d "$SHAMEL_ROOMS" ]]; then
    room_count=$(find "$SHAMEL_ROOMS" -mindepth 1 -maxdepth 1 -type d | wc -l)
    shamel::log "Rooms: $room_count"
  fi

  # Brain structure
  for f in BRAIN.md; do
    if [[ -f "${SHAMEL_BRAIN}/${f}" ]]; then
      shamel::log "brain/${f} present"
    else
      shamel::warn "brain/${f} missing"
    fi
  done
  for d in org db templates; do
    if [[ -d "${SHAMEL_BRAIN}/${d}" ]]; then
      shamel::log "brain/${d}/ present"
    else
      shamel::warn "brain/${d}/ missing"
    fi
  done

  return $ok
}

# ── Agent utilities ────────────────────────────────────────────────────────────
shamel::agent_exists() {
  local name="$1"
  [[ -f "${SHAMEL_AGENTS}/${name}.md" ]]
}

shamel::agent_frontmatter() {
  local name="$1"
  local file="${SHAMEL_AGENTS}/${name}.md"
  if [[ ! -f "$file" ]]; then
    shamel::error "agent '$name' not found"
    return 1
  fi
  awk '/^---$/{c++;next} c==1{print} c==2{exit}' "$file"
}

shamel::agent_spec_frontmatter() {
  local name="$1"
  local spec
  spec=$(find "$SHAMEL_ROOMS" -path "*/agents/${name}.md" -print -quit 2>/dev/null || true)
  if [[ -z "$spec" ]] || [[ ! -f "$spec" ]]; then
    return 1
  fi
  awk '/^---$/{c++;next} c==1{print} c==2{exit}' "$spec"
}

shamel::agent_field() {
  local name="$1" field="$2"
  local val
  val=$(shamel::agent_frontmatter "$name" | grep -E "^${field}:" | sed "s/^${field}: *//" | tr -d '"' | head -1)
  if [[ -z "$val" ]]; then
    val=$(shamel::agent_spec_frontmatter "$name" 2>/dev/null | grep -E "^${field}:" | sed "s/^${field}: *//" | tr -d '"' | head -1 || true)
  fi
  echo "$val"
}

shamel::agent_room() {
  local name="$1"
  # Try frontmatter from either spawnable or room spec
  local room
  room=$(shamel::agent_field "$name" "room" 2>/dev/null)
  if [[ -n "$room" ]]; then
    echo "$room"
    return 0
  fi
  # Fallback: match prefix to room code via CHARTER.md
  local prefix="${name%%-*}"
  for room_dir in "$SHAMEL_ROOMS"/*/; do
    local charter="${room_dir}CHARTER.md"
    if [[ -f "$charter" ]] && grep -q "Prefix: ${prefix}" "$charter" 2>/dev/null; then
      basename "$room_dir"
      return 0
    fi
  done
  echo "unknown"
}

shamel::agent_tools() {
  local name="$1"
  local raw
  raw=$(shamel::agent_field "$name" "tools")
  if [[ -z "$raw" ]]; then
    echo "Read Edit Write Bash Grep"
    return 0
  fi
  echo "$raw" | tr -d '[] ' | tr ',' ' '
}

shamel::agent_escalation() {
  local name="$1"
  local val
  val=$(shamel::agent_field "$name" "escalation" 2>/dev/null || true)
  if [[ -z "$val" ]] || [[ "$val" == "null" ]]; then
    val=$(shamel::agent_field "$name" "reports_to" 2>/dev/null || true)
  fi
  if [[ -z "$val" ]] || [[ "$val" == "null" ]]; then
    echo ""
    return 1
  fi
  echo "$val"
}

# ── Room utilities ─────────────────────────────────────────────────────────────
shamel::room_agents() {
  local room="$1"
  local room_dir="${SHAMEL_ROOMS}/${room}/agents"
  if [[ ! -d "$room_dir" ]]; then
    shamel::error "room '$room' not found"
    return 1
  fi
  find "$room_dir" -name '*.md' -exec basename -s '.md' {} \;
}

shamel::room_lead() {
  local room="$1"
  local charter="${SHAMEL_ROOMS}/${room}/CHARTER.md"
  if [[ -f "$charter" ]]; then
    grep -E "Room Lead:" "$charter" | sed 's/.*[:>] *//g' | sed 's/\*\*//g' | tr -d ' ' | head -1
  fi
}

# ── Handoff chain ──────────────────────────────────────────────────────────────
shamel::handoff_chain() {
  local agent="$1"
  local -a chain=()
  local visited="|"

  local current="$agent"
  while [[ -n "$current" ]]; do
    # Cycle detection
    if [[ "$visited" == *"|${current}|"* ]]; then
      break
    fi
    visited="${visited}${current}|"
    chain+=("$current")

    current=$(shamel::agent_escalation "$current" 2>/dev/null || true)
  done

  printf '%s\n' "${chain[@]}"
}

# ── RCCF formatting ────────────────────────────────────────────────────────────
shamel::rccf_format() {
  local agent="$1" task="$2" context="${3:-}"
  local room
  room=$(shamel::agent_room "$agent")
  local tools_str
  tools_str=$(shamel::agent_tools "$agent" 2>/dev/null || echo "Read Edit Write Bash Grep")

  cat <<RCCF
━━ RCCF: ${agent} ━━
Role: ${agent}
Room: ${room}
Task: ${task}
Context: ${context}
Tools: ${tools_str}
Evidence: file:line, exit code, commit sha, or screenshot
━━━━━━━━━━━━━━━━
RCCF
}

# ── Python bridge ──────────────────────────────────────────────────────────────
shamel::python() {
  PYTHONPATH="${SHAMEL_HOME}/shamel/engine" python3 "$@"
}

shamel::shamel_cli() {
  "${SHAMEL_BIN}/shamel" "$@"
}

# ── Brain helpers ──────────────────────────────────────────────────────────────
shamel::brain_read() {
  local path="$1"
  local full_path="${SHAMEL_BRAIN}/${path}"
  if [[ -f "$full_path" ]]; then
    cat "$full_path"
  else
    shamel::error "brain/${path} not found"
    return 1
  fi
}

shamel::brain_write() {
  local path="$1" content="$2"
  local full_path="${SHAMEL_BRAIN}/${path}"
  mkdir -p "$(dirname "$full_path")"
  echo "$content" > "$full_path"
  shamel::log "written brain/${path}"
}

shamel::brain_search() {
  local query="$1"
  grep -rl "$query" "${SHAMEL_BRAIN}" --include='*.md' --include='*.yaml' --include='*.yml' 2>/dev/null | while read -r f; do
    rel="${f#"${SHAMEL_HOME}/"}"
    matches=$(grep -c "$query" "$f" 2>/dev/null || true)
    echo "${rel}:${matches}"
  done
}

# ── Agent-to-room mapping (all room codes) ─────────────────────────────────────
shamel::all_rooms() {
  find "$SHAMEL_ROOMS" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort
}

shamel::all_agents() {
  find "$SHAMEL_AGENTS" -name '*.md' -exec basename -s '.md' {} \; | sort
}
