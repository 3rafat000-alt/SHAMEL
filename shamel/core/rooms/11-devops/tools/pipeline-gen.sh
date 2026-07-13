#!/usr/bin/env bash
# tool/ops/cicd-engineer/pipeline-gen.sh — Generate CI pipeline (lint→test→build→scan→deploy)
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
RED=$(tput setaf 1); GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { echo "Usage: $(basename "$0") --prj PRJ-ID [--stack php|python|node|flutter] [--provider github|gitlab] [--output .github/workflows/ci.yml]"; exit 0; }
PRJ=""; STACK=""; PROVIDER="github"; OUTPUT=""
while [[ $# -gt 0 ]]; do case "$1" in --prj) PRJ="$2"; shift2 ;; --stack) STACK="$2"; shift2 ;; --provider) PROVIDER="$2"; shift2 ;; --output) OUTPUT="$2"; shift2 ;; --help|-h) usage ;; *) usage ;; esac; shift; done
[[ -z "$PRJ" ]] && usage

# Auto-detect stack
if [[ -z "$STACK" ]]; then
  if [[ -f "$SOFI_ROOT/projects/$PRJ/composer.json" ]]; then STACK="php"
  elif [[ -f "$SOFI_ROOT/projects/$PRJ/requirements.txt" ]] || [[ -f "$SOFI_ROOT/projects/$PRJ/pyproject.toml" ]]; then STACK="python"
  elif [[ -f "$SOFI_ROOT/projects/$PRJ/package.json" ]]; then STACK="node"
  elif ls "$SOFI_ROOT/projects/$PRJ/pubspec.yaml" 2>/dev/null; then STACK="flutter"
  else STACK="php"; fi
fi

OUTPUT="${OUTPUT:-$SOFI_ROOT/projects/$PRJ/.github/workflows/ci.yml}"
mkdir -p "$(dirname "$OUTPUT")"

cat > "$OUTPUT" <<EOF
name: CI — $PRJ

on:
  push:
    branches: [main, develop, prj/$PRJ/**]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-${STACK}@v4
EOF

case "$STACK" in
  php)
    cat >> "$OUTPUT" <<'PHPEOF'
        with: { php-version: '8.3' }
      - run: composer install --no-progress
      - run: ./vendor/bin/phpcs --standard=PSR12 app/ tests/
PHPEOF
    ;;
  python)
    cat >> "$OUTPUT" <<'PYEOF'
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: ruff check .
PYEOF
    ;;
  node)
    cat >> "$OUTPUT" <<'NODEEOF'
        with: { node-version: '22' }
      - run: npm ci
      - run: npx eslint .
NODEEOF
    ;;
  flutter)
    cat >> "$OUTPUT" <<'FLUTTEOF'
        with: { flutter-version: '3.x' }
      - run: flutter pub get
      - run: flutter analyze
FLUTTEOF
    ;;
esac

cat >> "$OUTPUT" <<'COMMONEOF'

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
COMMONEOF

case "$STACK" in
  php)  echo "      - run: ./vendor/bin/phpunit" >> "$OUTPUT" ;;
  python) echo "      - run: python -m pytest" >> "$OUTPUT" ;;
  node) echo "      - run: npx jest --coverage" >> "$OUTPUT" ;;
  flutter) echo "      - run: flutter test --coverage" >> "$OUTPUT" ;;
esac

cat >> "$OUTPUT" <<'SCANEOF'

  scan:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          echo "Security scan placeholder"
          echo "Replace with: trufflehog, semgrep, or gitleaks"

  deploy:
    needs: [lint, test, scan]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy
        run: |
          echo "Deploy: ${{ github.sha }}"
          echo "Target: $PRJ production"
          echo "Strategy: blue/green with rollback"
SCANEOF

echo "${GREEN}[pipeline-gen] Written to $OUTPUT${RESET}"
