---
name: rules-dart-patterns
description: >
  Dart-language design-pattern rules — idiomatic Dart data modeling, error
  handling, and boundary-parsing patterns. No common-tier ancestor (patterns
  are language-specific); flutter/patterns.md extends this file with
  widget/state-management patterns. Use before designing a model, service,
  or repository class in .dart code.
paths:
  - "projects/PRJ-SAKK/mobile/lib/**/data/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/**/domain/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/core/**/*.dart"
  - "**/*.dart"
---

## | أنماط دارت | Dart Patterns

Purpose: Idiomatic Dart structural patterns this project relies on.
Activated when: any agent designs or edits a model, repository, or service.

### Explicit JSON boundary parsing (the core pattern)
- Every API response type gets a dedicated model with a `factory
  Model.fromJson(Map<String, dynamic> json)` that explicitly coerces each
  field's type — never spread/cast a raw `Map<String, dynamic>` past the
  data layer. This is the structural fix for the type-confusion crash class
  described in `dart/security.md`; treat it as non-negotiable at every new
  API integration, not just the ones that have already broken.
- Helper pattern for tolerant coercion:
  ```dart
  static int _asInt(dynamic v, {int fallback = 0}) =>
      v is int ? v : int.tryParse(v?.toString() ?? '') ?? fallback;
  ```
  Apply the equivalent for bool/enum/DateTime fields — never trust the
  declared API contract to match the runtime payload.

### Result/Either over exceptions for expected failures
- Repository and service methods that can fail in an *expected* way
  (network error, validation error, business-rule rejection) return
  `Either<Failure, T>` (project uses `dartz`) rather than throwing — reserve
  thrown exceptions for programmer errors (bad arguments, unreachable state).
- Define a small `Failure` hierarchy (e.g. `NetworkFailure`,
  `ValidationFailure`, `ParsingFailure`, `ServerFailure`) so callers can
  branch on failure type instead of parsing message strings.

### Repository pattern
- UI/state layers never call `Dio`/`http` directly — they call a repository
  interface; the repository owns the API client and the `fromJson` mapping.
  This keeps the type-coercion boundary in one reviewable place per feature.

### Immutability & equality
- Data/model classes extend `Equatable` (already a dependency) or implement
  value equality explicitly — relying on default identity equality causes
  spurious rebuilds/comparisons in state management.

### Extension methods over utility classes
- Prefer an extension (`extension StringX on String { ... }`) over a static
  `Utils.doThing(x)` class for single-type helpers — it reads at the call
  site and keeps related behavior discoverable via IDE autocomplete.
