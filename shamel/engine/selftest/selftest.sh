#!/usr/bin/env bash
# SHAMEL selftest — verify engine integrity
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SHAMEL_HOME="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$SHAMEL_HOME"

tests=0
pass=0

check() {
    local name="$1" cmd="$2"
    tests=$((tests + 1))
    if eval "$cmd" >/dev/null 2>&1; then
        pass=$((pass + 1))
        echo "  PASS  $name"
    else
        echo "  FAIL  $name"
    fi
}

echo "{\"results\": ["

first=true
check() {
    local name="$1" cmd="$2"
    tests=$((tests + 1))
    if eval "$cmd" >/dev/null 2>&1; then
        pass=$((pass + 1))
        $first || echo ","; first=false
        echo "{\"name\":\"$name\",\"status\":\"PASS\"}"
    else
        $first || echo ","; first=false
        echo "{\"name\":\"$name\",\"status\":\"FAIL\"}"
    fi
}

SHAMEL_PYTHONPATH="shamel/engine"
SHAMEL_CLI="shamel/engine/bin/shamel"

check "paths resolve" "PYTHONPATH=$SHAMEL_PYTHONPATH python3 -c \"import sys; sys.path.insert(0,'$SHAMEL_PYTHONPATH'); from shamel_tools import paths; paths.repo_root()\""
check "CLI exists" "test -x $SHAMEL_CLI"
check "CLI runs" "$SHAMEL_CLI --help"
check "CLI rooms" "PYTHONPATH=$SHAMEL_PYTHONPATH $SHAMEL_CLI rooms"
check "CLI registry" "PYTHONPATH=$SHAMEL_PYTHONPATH $SHAMEL_CLI registry"
check "CLI projects" "PYTHONPATH=$SHAMEL_PYTHONPATH $SHAMEL_CLI projects"
check "nexus YAMLs parse" "python3 -c \"import yaml; yaml.safe_load(open('shamel/core/nexus/registry.yaml')); yaml.safe_load(open('shamel/core/nexus/routing.yaml')); yaml.safe_load(open('shamel/core/nexus/gates.yaml'))\""
check "15 rooms" "test \"$(PYTHONPATH=$SHAMEL_PYTHONPATH $SHAMEL_CLI rooms | grep agents | grep -v TOTAL | wc -l)\" -eq 15"
check "no sofi files" 'test "$(find . -path ./archive -prune -o -path "*/tools/*" -prune -o -name "sofi*" -print | grep -c .)" -eq 0'
check "doctor passes" "PYTHONPATH=$SHAMEL_PYTHONPATH $SHAMEL_CLI doctor > /dev/null 2>&1"

echo "], \"pass\": $([ $pass -eq $tests ] && echo true || echo false), \"tests\": $tests, \"passed\": $pass"
echo "}"
