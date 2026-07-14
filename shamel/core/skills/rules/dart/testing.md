---
name: rules-dart-testing
description: >
  Dart-language testing rules — extends rules-common-testing with Dart's
  package:test conventions, mocking, and coverage tooling. Use for any task
  writing or reviewing unit tests in .dart code, before applying
  flutter/patterns.md widget-test guidance.
paths:
  - "projects/PRJ-SAKK/mobile/test/**/*.dart"
  - "projects/PRJ-SAKK/mobile/**/*_test.dart"
  - "**/*_test.dart"
---

## | اختبار دارت | Dart Testing

Purpose: Dart-specific testing baseline on top of the common one. Activated
when: any agent writes, edits, or reviews unit tests for pure-Dart logic
(models, repositories, services) — see `flutter/patterns.md` for widget tests.

### Structure & tooling
- Use `package:test` (`flutter_test` for anything touching Flutter bindings)
  with `group`/`test`; mirror the `lib/` path under `test/` so a reader can
  find `lib/features/auth/data/repositories/auth_repository.dart` at
  `test/features/auth/.../auth_repository_test.dart` without searching.
- Mock external dependencies (Dio clients, secure storage, platform
  channels) with `mocktail` (already a project dev-dependency) — never let a
  unit test perform real HTTP, real disk I/O, or real biometric prompts.

### Model/parsing coverage (mandatory)
- Every model with a `fromJson` factory needs tests for: the well-formed
  response, a missing/null field, and a wrong-typed field (e.g. server sends
  `"id": "42"` where an `int` is expected) — this is the direct regression
  test for the type-coercion rule in `dart/security.md`. A parsing bug that
  reaches production without this test class is a preventable repeat.
- Repository/service methods that call the API need a test per Dio outcome:
  2xx success, 4xx client error (mapped to a typed failure), 5xx/timeout
  (mapped to a retryable failure), and malformed-body response.

### Assertions
- Assert on the returned value/typed failure, not just "did not throw" —
  a test that only wraps a call in `expect(() => fn(), returnsNormally)`
  hides logic bugs.
- For `Either`/`Result`-based repositories (project uses `dartz`), assert
  both the `Left` and `Right` branches explicitly; do not assume `isRight()`
  is enough without checking the payload.

### Determinism
- Inject `Clock`/time providers into anything using `DateTime.now()`
  (expiry checks, OTP timers, transaction timestamps) — do not assert
  against wall-clock time in a test.

### Coverage focus
- Prioritize coverage on money paths (`wallets`, `transfer`, `cards`,
  `cashback`, `gold`) and auth/KYC over low-risk display-only widgets —
  coverage percentage is not the goal, risk-weighted coverage is.
