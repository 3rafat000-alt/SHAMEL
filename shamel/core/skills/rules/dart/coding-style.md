---
name: rules-dart-coding-style
description: >
  Dart-language coding-style rules — extends rules-common-coding-style with
  Dart-specific type system, null-safety, and formatting conventions. Use for
  any task writing or editing .dart files, before applying flutter/*.md.
paths:
  - "projects/PRJ-SAKK/mobile/**/*.dart"
  - "**/*.dart"
  - "**/pubspec.yaml"
---

## | نمط دارت | Dart Coding Style

Purpose: Dart-specific style rules on top of the common baseline. Activated
when: any agent writes or edits `.dart` code (any layer, not just Flutter UI).

### Null safety
- Do not use `!` (bang operator) to silence the analyzer unless the
  non-nullability is provably guaranteed at that point and you can state why
  in a comment — an unguarded `!` converts a compile-time null hazard into a
  runtime crash.
- Prefer `?.`, `??`, `??=`, and pattern matching (`if (x case final y?)`) over
  manual null checks that re-derive what the type system already encodes.
- Model "value may be absent" with nullable types or a `Result`/`Either`
  return, not a sentinel value (`-1`, `""`, `"N/A"`) — sentinels get
  mis-checked and silently propagate.

### Typing discipline
- No unnecessary `dynamic`. If a value's shape is not statically known
  (JSON, plugin channel result, `Map<String, dynamic>` from an API), narrow
  it to a typed model at the boundary — see `dart/patterns.md` for the
  required JSON-parsing pattern. `dynamic` inside business logic is a smell.
- Use `final` by default; `var` only when reassignment is intentional; never
  bare, untyped `var x;` — let inference or an explicit type make intent clear.
- Prefer immutable data classes (`final` fields, `const` constructors,
  `copyWith`) for models and state — mutable shared objects across
  widgets/providers are a common source of stale-UI bugs.

### Naming & structure
- File names `snake_case.dart`; classes `UpperCamelCase`; members
  `lowerCamelCase`; constants `lowerCamelCase` (not `SCREAMING_CASE`) per
  Dart convention — do not import naming habits from other languages.
- One public class per file unless the additional classes are small,
  private, and exist only to support the primary one.

### Formatting & lint
- Run `dart format` before committing; do not hand-align code that the
  formatter would reflow — that diff noise obscures real changes in review.
- Treat `flutter_lints`/`analysis_options.yaml` warnings as build errors for
  new code — do not add `// ignore:` without a one-line reason comment.

### Async
- Every `Future`/`async` call is awaited or explicitly fire-and-forget with a
  comment (`// ignore: unawaited_futures — fire and forget, see X`). A silent
  dangling Future can drop errors and hide bugs.
