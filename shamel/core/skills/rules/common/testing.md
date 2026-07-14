---
name: rules-common-testing
description: >
  Base testing rules shared by every language/stack in SHAMEL projects —
  what to test, how to structure tests, and coverage expectations for
  money-handling code. Language tiers (php/testing.md, ...) extend this
  with stack-specific tooling. Use for any task writing or reviewing tests.
paths:
  - "**/*test*.php"
  - "**/*Test.php"
  - "**/tests/**"
  - "**/*.spec.ts"
  - "**/*_test.dart"
---

## | الاختبار العام | Common Testing

Purpose: Language-agnostic testing baseline — the foundation every
language/framework testing file builds on. Activated when: any agent writes,
edits, or reviews tests, or ships code without accompanying tests.

### What to test
- Test observable behavior (inputs → outputs/side effects), not internal
  implementation details — refactoring should not break tests that don't
  change behavior.
- Every bug fix gets a regression test that fails before the fix and passes
  after — otherwise the bug can silently return.
- Money-handling code paths (balances, transfers, payouts, fee calculation,
  currency conversion) require explicit test coverage for: zero amount,
  negative/invalid amount, boundary/overflow values, rounding behavior, and
  concurrent-access/race scenarios where relevant. This is not optional —
  see `ccpayment-integration`/`stripe-issuing-integration` for the money
  paths already flagged in this project. See `testsprite-testing` skill for
  this project's test-execution tooling.

### Structure
- Arrange–Act–Assert (or Given–When–Then): one clear setup, one action under
  test, explicit assertions. Do not bury the assertion under setup noise.
- One logical behavior per test. A test named for one thing that silently
  asserts three unrelated things is a debugging trap later.

### Determinism
- No `sleep()`-based waits for async conditions — poll with a timeout or use
  the framework's async test utilities.
- Freeze/inject time and randomness in tests; never assert against
  `now()`/`rand()` directly.
- Tests must not depend on execution order or leak state (DB rows, cache
  keys, files) into the next test.

### External systems
- Never call real third-party APIs (payment providers, email, push) from
  tests — mock/fake the client at the boundary.

### Coverage is a signal, not the goal
- A high percentage with weak assertions (no assert, or asserting only "no
  exception thrown") is worse than a lower percentage with real assertions on
  behavior. Review test quality, not just the coverage number.
