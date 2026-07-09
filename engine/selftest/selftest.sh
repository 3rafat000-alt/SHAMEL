#!/usr/bin/env bash
# SHAMEL selftest — verify engine integrity
set -euo pipefail
SHAMEL_HOME="${SHAMEL_HOME:-$(cd "$(dirname "$0")/../.." && pwd)}"
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

check "paths resolve" 'python3 -c "import sys; sys.path.insert(0,\"engine\"); from shamel_tools import paths; paths.repo_root()"'
check "CLI exists" 'test -x engine/bin/shamel'
check "CLI runs" 'engine/bin/shamel --help'
check "CLI rooms" 'engine/bin/shamel rooms'
check "CLI registry" 'engine/bin/shamel registry'
check "CLI projects" 'engine/bin/shamel projects'
check "nexus YAMLs parse" 'python3 -c "import yaml; yaml.safe_load(open(\"core/nexus/registry.yaml\")); yaml.safe_load(open(\"core/nexus/routing.yaml\")); yaml.safe_load(open(\"core/nexus/gates.yaml\"))"'
check "15 rooms" 'test "$(engine/bin/shamel rooms | grep agents | grep -v TOTAL | wc -l)" -eq 15'
check "no sofi files" 'test "$(find . -path ./archive -prune -o -name "sofi*" -print | grep -c .)" -eq 0'
check "doctor passes" 'engine/bin/shamel doctor > /dev/null 2>&1'

echo "], \"pass\": $([ $pass -eq $tests ] && echo true || echo false), \"tests\": $tests, \"passed\": $pass"
echo "}"
