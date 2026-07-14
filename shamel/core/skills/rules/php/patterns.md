---
name: rules-php-patterns
description: >
  PHP-specific design-pattern rules for SHAMEL projects. Extends
  common/coding-style.md with structural patterns for PHP OOP — value
  objects, DTOs, enums, composition. Use when designing classes/services,
  not just formatting existing code.
paths:
  - "projects/PRJ-SAKK/backend/app/**/*.php"
  - "**/app/Services/**/*.php"
  - "**/app/Enums/**/*.php"
  - "**/app/Casts/**/*.php"
---

## | أنماط PHP | PHP Patterns

Extends `common/coding-style.md`. Purpose: structural/design patterns for
PHP OOP on top of the language-agnostic style baseline. Activated when: any
agent designs a class, service, or value type — not just edits an existing one.

### Money as integers, never floats
- Store and pass monetary amounts as integer minor units (cents) or a
  dedicated decimal type — never `float`/`double` for balances, fees, or
  transfer amounts. Float rounding error compounds across arithmetic and
  is unacceptable in wallet/transaction code.
- If a Money value object exists or is warranted, encapsulate
  amount+currency together so they cannot drift apart across a call chain.

### Enums over string/int constants
- Use native PHP enums (`app/Enums/`, e.g. `TransactionStatus`,
  `KycStatus`) for closed sets of values instead of string literals
  scattered across the codebase — the type system then rejects invalid
  states at compile time, and `match` over an enum is exhaustive-checked.

### DTOs at boundaries
- Cross a layer boundary (controller → service, service → job payload)
  with a typed DTO or Form Request object, not a raw associative array —
  arrays give no static guarantee about which keys exist or their types.

### Composition over inheritance
- Prefer injecting a collaborator (constructor-promoted dependency) over
  extending a base class for shared behavior; reserve inheritance for a
  true is-a relationship, use traits/interfaces for shared capability.
- A service class (e.g. `app/Services/CCPaymentService.php`) should have
  one reason to change — if it both calls an external API and computes
  business rules, split the concerns.

### Avoid primitive obsession
- Don't pass a bare `string $status`/`int $currencyCode` through multiple
  layers when an enum or value object already models the concept — the
  extra type gives IDE/static-analysis support and rejects typos early.

### Immutability
- Prefer `readonly` properties for value objects and DTOs constructed
  once and never mutated (e.g. a parsed webhook payload) — this makes
  accidental mutation a compile error, not a runtime surprise.

### Static analysis alignment
- New patterns must stay Larastan-clean (see `php/coding-style.md`) — a
  pattern that requires suppressing static analysis is usually wrong.
