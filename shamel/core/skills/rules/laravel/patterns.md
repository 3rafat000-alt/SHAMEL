---
name: rules-laravel-patterns
description: >
  Laravel-specific design-pattern rules for SHAMEL's PRJ-SAKK backend.
  Extends php/patterns.md with Laravel 12 framework conventions —
  Eloquent, Form Requests, Resources, Jobs, migrations. Use for any task
  designing controllers, models, jobs, or migrations in the Laravel app.
paths:
  - "projects/PRJ-SAKK/backend/app/Http/Controllers/**/*.php"
  - "projects/PRJ-SAKK/backend/app/Models/**/*.php"
  - "projects/PRJ-SAKK/backend/app/Jobs/**/*.php"
  - "projects/PRJ-SAKK/backend/database/migrations/**/*.php"
  - "projects/PRJ-SAKK/backend/routes/**/*.php"
  - "**/app/Http/Controllers/**/*.php"
  - "**/database/migrations/**/*.php"
---

## | أنماط Laravel | Laravel Patterns

Extends `php/patterns.md`. Purpose: Laravel 12 framework-idiomatic
patterns on top of the PHP structural baseline. Activated when: any agent
touches a controller, model, job, or migration in
`projects/PRJ-SAKK/backend/`.

### Thin controllers
- Controllers validate (via Form Request, e.g. `app/Http/Requests/Wallet/
  DepositRequest.php`), delegate to a service/action, and return a
  Resource — no business logic, no raw query building in the controller.
- Use API Resources (`app/Http/Resources/`) to shape every API response —
  never return a raw Eloquent model/array; it leaks internal columns.

### Eloquent — N+1 avoidance
- Eager-load relations accessed in a loop or a Resource
  (`->with('wallet', 'transactions')`) — a Resource that lazy-loads a
  relation per row is an N+1 query hidden behind serialization.
- Use `Model::query()` with explicit `where`, not `DB::raw` unless
  unavoidable (see `php/security.md`).

### Jobs — idempotency
- Every queued job that mutates money (deposit credit, withdrawal debit,
  card load/unload) must be idempotent — at-least-once delivery must not
  double-apply. Use a unique constraint, processed-ledger check, or an
  idempotency key from the source event (webhook/provider ID).
- Jobs interacting with `ccpayment-integration` / `stripe-issuing-
  integration` follow those skills' reconciliation approach.

### Migrations
- Every migration's `down()` must actually reverse `up()` — irreversible
  migrations need an explicit comment why, not a silent no-op `down()`.
- Add columns nullable or with a default when the table has existing
  rows in any deployed environment.

### Policies over inline checks
- Authorization for a model action goes through a Policy
  (`app/Policies/`, e.g. `WalletPolicy`, `WithdrawalPolicy`) and
  `$this->authorize(...)`/`Gate` — not an inline ownership `if` check.

### Events for cross-cutting side effects
- Side effects outside an action's core purpose (notify, audit-log, sync
  elsewhere) go through an Event/Listener, not inlined into the method.
