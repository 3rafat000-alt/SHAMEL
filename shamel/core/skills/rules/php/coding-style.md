---
name: rules-php-coding-style
description: >
  PHP-specific coding-style rules for SHAMEL projects (PHP 8.4). Extends
  common/coding-style.md with PHP language conventions — typing, PSR-12,
  Composer autoloading. Use for any task writing or editing .php files.
paths:
  - "projects/PRJ-SAKK/backend/**/*.php"
  - "**/*.php"
  - "**/composer.json"
  - "**/composer.lock"
---

## | نمط PHP | PHP Coding Style

Extends `common/coding-style.md`. Purpose: PHP-specific conventions on top of
the language-agnostic baseline. Activated when: any agent writes/edits `.php`
files in a SHAMEL project (e.g. `projects/PRJ-SAKK/backend/`).

### Typing
- Declare `strict_types=1` where the file allows it; type every function
  parameter and return, including nullable (`?int`) and union types (PHP
  8.4 supports both).
- Type class properties, not just constructor params — `public readonly
  int $amount` beats an untyped property assigned in the constructor body.
- Avoid `mixed` unless the value genuinely varies in type; it defeats the
  point of typing and downstream static analysis (Larastan).

### PSR standards
- Follow PSR-12 formatting (4-space indent, brace placement, one class per
  file) and PSR-4 autoloading — namespace must match directory path exactly
  (`App\Services\CCPaymentService` → `app/Services/CCPaymentService.php`).
- Run the project's formatter/linter (Pint if configured) rather than
  hand-formatting — see `common/coding-style.md` on deferring to tooling.

### Composer
- Pin dependency versions with care in `composer.json`; do not widen a
  constraint just to unblock a local install — verify compatibility first.
- Never commit changes to `composer.lock` without running `composer
  install`/`update` — a hand-edited lock file drifts from the real
  dependency graph.

### Null & error handling
- Prefer `?->` (nullsafe operator) over chained `isset()` checks for
  optional relations/objects.
- Throw typed exceptions (custom exception classes under `app/Exceptions/`)
  rather than generic `\Exception` for domain errors — callers need to
  `catch` specific failure modes.
- Use `match` over `switch` for exhaustive value mapping — it errors on an
  unhandled case instead of silently falling through.

### Static analysis
- Code must pass Larastan (`larastan/larastan`, already in
  `composer.json` require-dev) at the project's configured level before
  it is considered done — do not introduce new baseline-ignored errors.
