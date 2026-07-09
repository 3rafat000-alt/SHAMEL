#!/usr/bin/env bash
# tool/str/product-strategist/problem-statement.sh — Generate problem statement questionnaire
set -euo pipefail
SOFI_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
GREEN=$(tput setaf 2); YELLOW=$(tput setaf 3); BLUE=$(tput setaf 4); RESET=$(tput sgr0)

usage() { cat <<EOF
Usage: $(basename "$0") [--output <file>]
  Generate structured problem-statement questionnaire.
  Outputs questions to surface the real problem, not the symptom.
EOF
exit 0
}

OUTPUT="${2:-/dev/stdout}"
[[ "${1:-}" == "--help" ]] && usage
[[ "${1:-}" == "--output" ]] && OUTPUT="${2:-/dev/stdout}"

cat > "$OUTPUT" <<QUESTIONS
# Problem Statement Questionnaire
## Fill each section — answers define the product

### 1. THE PAIN
- What specifically is broken or painful today?
- Who feels this pain? (role, not name)
- How much time/money does this pain cost per week?
- What do people do today as a workaround?

### 2. THE USER
- Who is the primary user? (describe their day)
- Who else touches this problem? (secondary/tertiary)
- What does "success" look like from their chair?

### 3. THE SOLUTION HYPOTHESIS
- If we built the perfect fix, what would it do?
- What's the smallest possible version that delivers value?
- What would make a user switch from their workaround?

### 4. THE MARKET
- How many people have this problem? (TAM estimate)
- What do competitors do about it? (name 3)
- Why aren't existing solutions good enough?

### 5. THE RISKS
- What assumptions must be true for this to work?
- Which assumption is most likely false?
- How would we validate that assumption cheaply?

---
When complete: transfer answers to Project_Blueprint.md
QUESTIONS

[[ "$OUTPUT" != "/dev/stdout" ]] && echo "${GREEN}✓ Questionnaire written to $OUTPUT${RESET}"
