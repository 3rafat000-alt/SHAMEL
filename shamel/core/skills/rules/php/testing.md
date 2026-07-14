---
name: rules-php-testing
description: >
  PHP-specific testing rules for SHAMEL projects using Pest. Extends
  common/testing.md with Pest/PHPUnit tooling conventions. Use for any task
  writing or reviewing PHP tests.
paths:
  - "projects/PRJ-SAKK/backend/tests/**/*.php"
  - "**/tests/**/*.php"
  - "**/*Test.php"
  - "**/Pest.php"
  - "**/phpunit.xml"
---

## | اختبار PHP | PHP Testing

Extends `common/testing.md`. Purpose: PHP/Pest-specific tooling conventions
on top of the language-agnostic baseline. Activated when: any agent writes
or reviews tests under `tests/` in a PHP project (Pest 3.x is the configured
runner per `composer.json`).

### Tooling
- Use Pest syntax (`it(...)`, `test(...)`, `expect(...)`) consistently —
  do not mix raw PHPUnit `TestCase` assertion style into a Pest suite
  without reason.
- Run via `vendor/bin/pest` (or `composer test`), not `phpunit` directly —
  Pest plugins (`pest-plugin-laravel`, `pest-plugin-faker`) only load
  through the Pest runner.
- Use `pestphp/pest-plugin-faker` for generating realistic fake data
  (amounts, emails, card numbers) instead of hardcoded literals that
  don't exercise edge values.

### Database
- Use `RefreshDatabase`/`DatabaseTransactions` traits so each test starts
  from a known DB state — never assume the DB is clean or reuse rows
  created by a previous test.
- Use Model Factories (`database/factories/`) to build test fixtures, not
  raw `DB::insert` — factories stay in sync with model casts/fillable.

### Mocking external services
- Mock HTTP calls to Stripe/CCPayment/Firebase with Laravel's `Http::fake()`
  or a Mockery double on the service class — never let a test suite hit
  `stripe-php`'s real client or CCPayment's real API (see
  `common/testing.md` "External systems").
- For webhook-handling tests, construct the request with a real/valid
  signature computed the same way the provider does (per
  `ccpayment-integration` / `stripe-issuing-integration`), plus a separate
  test asserting an invalid signature is rejected.

### Money-handling assertions
- Assert exact integer/decimal amounts after an operation (balance,
  transaction row, fee) — never assert only that "no exception was thrown".
- Cover concurrent-write scenarios for balance mutations (e.g. two
  simultaneous withdrawal jobs) where the code path allows concurrent
  access — see `common/testing.md` money-path coverage requirement.

### CI expectations
- New/changed money code (`app/Services/*Payment*`, `app/Jobs/*`,
  wallet/transaction logic) does not land without a Pest test — see
  `testsprite-testing` skill for this project's test-execution tooling.
