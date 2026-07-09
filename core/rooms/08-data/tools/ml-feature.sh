#!/usr/bin/env bash
# tool/dat/ml-engineer/ml-feature.sh — Scaffold ML feature with eval + failover
set -euo pipefail
SOFI_ROOT="${SOFI_ROOT:-$HOME/Desktop/Lorka}"
R="$(tput setaf 1)" G="$(tput setaf 2)" Y="$(tput setaf 3)" B="$(tput setaf 4)" X="$(tput sgr0)"

usage() { echo "Usage: $(basename $0) <PRJ-ID> <feature-name> [type]
Scaffold an ML feature with evaluation harness and fallback logic.
  type  recommendation|classification|regression (default: recommendation)
Example: ml-feature.sh PRJ-SAKK product_relevance recommendation
--help"; exit 0; }

PRJ="$1"; FEATURE="${2:-}"; TYPE="${3:-recommendation}"
[ "$PRJ" = "--help" ] && usage; [ -z "$FEATURE" ] && echo "${R}Error: feature name required$X" && usage

PRJ_DIR="$SOFI_ROOT/projects/$PRJ"
SNAKE=$(echo "$FEATURE" | tr '[:upper:]' '[:lower:]')
PASCAL=$(echo "$FEATURE" | sed 's/_/ /g' | sed 's/\b\(.\)/\u\1/g' | tr -d ' ')
DIR="$PRJ_DIR/app/ML"
mkdir -p "$DIR"

# Pipeline class
PIPE_FILE="$DIR/${PASCAL}Pipeline.php"
[ ! -f "$PIPE_FILE" ] && cat > "$PIPE_FILE" <<PHP
<?php
namespace App\ML;
class ${PASCAL}Pipeline
{
    public function __construct(
        private array \$config = []
    ) {}

    public function predict(array \$input): array
    {
        try {
            // @todo call model inference
            return ['prediction' => null, 'confidence' => 0.0];
        } catch (\Throwable \$e) {
            return \$this->fallback(\$input);
        }
    }

    public function fallback(array \$input): array
    {
        // Rule-based fallback when model is unavailable
        return ['prediction' => 'default', 'confidence' => 0.0, 'fallback' => true];
    }

    public function evaluate(array \$testSet): array
    {
        \$correct = 0; \$total = count(\$testSet);
        foreach (\$testSet as \$sample) {
            \$result = \$this->predict(\$sample['input']);
            if ((\$result['prediction'] ?? null) === (\$sample['expected'] ?? null)) {
                \$correct++;
            }
        }
        return ['accuracy' => \$total > 0 ? round(\$correct / \$total, 4) : 0, 'samples' => \$total];
    }
}
PHP
echo "${G}Pipeline:$X $PIPE_FILE"

# Config
CONFIG_FILE="$DIR/config/${SNAKE}.php"
mkdir -p "$DIR/config"
[ ! -f "$CONFIG_FILE" ] && cat > "$CONFIG_FILE" <<PHP
<?php
return [
    'type' => '$TYPE',
    'model_path' => env('${PASCAL^^}_MODEL_PATH', ''),
    'min_confidence' => 0.7,
    'fallback_on_error' => true,
    'batch_size' => 100,
];
PHP
echo "${G}Config:$X $CONFIG_FILE"

echo "${B}Done.$X Usage: app(${PASCAL}Pipeline::class)->predict(\$data)"
