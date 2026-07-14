---
name: rules-common-coding-style
description: >
  Base coding-style rules shared by every language/stack in SHAMEL projects.
  Language tiers (php/, dart/, ...) extend this file with stack-specific
  content. Use for any code-writing or code-review task before applying a
  language-specific rules file.
paths:
  - "**/*.php"
  - "**/*.dart"
  - "**/*.ts"
  - "**/*.js"
  - "**/*.py"
  - "**/*.go"
  - "**/*.blade.php"
---

## | نمط الكود العام | Common Coding Style

Purpose: Language-agnostic style rules — the foundation every language/framework
rules file builds on. Activated when: any agent writes or edits source code.

### Naming
- Names describe intent, not implementation. No single-letter vars outside
  tight loop counters. No unexplained abbreviations (`usr`, `amt`, `cfg`).
- Booleans read as predicates: `isActive`, `hasPermission`, `canWithdraw` —
  never bare nouns for a bool (`active` as a flag name is ambiguous).
- One vocabulary per concept across the codebase — do not mix `user`/`account`/
  `member` for the same entity in different files.

### Functions & files
- Single responsibility per function. If you need "and" to describe what it
  does, split it.
- Keep functions short enough to read without scrolling (~30-40 lines is a
  smell threshold, not a hard cap).
- One primary class/concept per file; file name matches the primary export.

### Comments
- Comments explain **why**, not what — the code already says what. A comment
  restating the next line is noise and rots when the code changes.
- Every workaround/hack needs a comment with the reason and, if known, the
  removal condition (e.g. "remove once upstream fixes #123").

### Constants & magic values
- No magic numbers/strings in logic — name them as constants/enums, especially
  for status codes, currency codes, thresholds, and time windows.

### Error handling
- Never silently swallow an error (empty `catch`). Log with context, rethrow,
  or return a typed failure — pick one deliberately.
- Fail loud in development/CI; fail safe (degrade, don't crash the request)
  in production for non-critical paths.

### Formatting
- Defer to the project's configured formatter/linter (see language-tier rules
  for the exact tool). Do not hand-format against a linter that would reformat
  it anyway — run the tool.

### DRY discipline
- Extract shared logic on the third repetition, not the first — premature
  abstraction that guesses wrong is costlier than duplication.
