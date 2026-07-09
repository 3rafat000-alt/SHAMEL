#!/usr/bin/env bash
# tool/sec/appsec-engineer/code-scan.sh — Scan PHP/Python/JS for injection, SSRF, IDOR patterns
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") [--prj PRJ-ID] [--path dir] [--format plain|json]"; exit 0; }
PRJ=""; SCAN_PATH=""; FORMAT="plain"
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --path) SCAN_PATH="$2"; shift2 ;; --format) FORMAT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done

SCAN_DIR="${SCAN_PATH:-$SOFI_ROOT/projects/${PRJ:-.}}"
[[ -d "$SCAN_DIR" ]] || { echo "${RED}Error: $SCAN_DIR not found${RESET}"; exit 1; }
echo "${BLUE}[code-scan]${RESET} Scanning $SCAN_DIR"; echo ""

scan_pattern() {
  local label="$1" ext="$2" pattern="$3"
  local matches
  matches=$(find "$SCAN_DIR" -name "*.$ext" -not -path "*/vendor/*" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null | xargs grep -n "$pattern" 2>/dev/null || true)
  if [[ -n "$matches" ]]; then
    echo "${RED}  ✗ $label ($pattern)${RESET}"
    echo "$matches" | head -20 | sed 's/^/    /'
  else
    echo "${GREEN}  ✓ $label${RESET}"
  fi
}

scan_pattern "SQL injection" "php" "DB::raw\|DB::statement\|->whereRaw\|DB::select("
scan_pattern "SQL injection" "py" "execute(\"\|raw("
scan_pattern "Command injection" "php" "shell_exec\|exec(\|system(\|passthru("
scan_pattern "Command injection" "py" "os\.system\|subprocess\.call\|shlex"
scan_pattern "SSRF (user URL)" "php" "file_get_contents(\$_"
scan_pattern "SSRF (user URL)" "py" "requests\.get.*input\|urllib.*request"
scan_pattern "Dangerous eval" "js" "eval(\|Function("
scan_pattern "Hardcoded secrets" "env" "SECRET\|PASSWORD\|API_KEY"
scan_pattern "IDOR (no policy)" "php" "::find(\|::first("

echo ""
echo "${BLUE}[code-scan]${RESET} ${GREEN}Done. Review findings above.${RESET}"
