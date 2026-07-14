---
name: rules-dart-security
description: >
  Dart-language security rules — extends rules-common-security with
  Dart-specific type-safety-at-boundary and data-handling guidance. Use for
  any task touching API responses, JSON parsing, or serialization in .dart
  code, before applying flutter/security.md.
paths:
  - "projects/PRJ-SAKK/mobile/lib/core/network/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/**/data/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/**/models/**/*.dart"
  - "**/*.dart"
---

## | أمن دارت | Dart Security

Purpose: Dart-specific security baseline on top of the common one. Activated
when: any agent parses external data, calls an API, or handles
tokens/PII in `.dart` code.

### Type safety at the API boundary (mandatory)
- Never assume a decoded JSON value matches the Dart type you expect. A
  server field typed as `int` can arrive as a `String` (or vice versa) after
  a backend change — reading it with `json['id'] as int` throws
  `type 'String' is not a subtype of type 'int'` at runtime, in production,
  on the user's device. This exact class of bug has already crashed
  account-creation in this project.
- At every JSON/API-response boundary, explicitly coerce: parse ints with
  `int.tryParse(value.toString())`, bools/enums with an explicit mapping
  function, and treat every field as **absent, wrong-typed, or malformed**
  until proven otherwise — do not use `as Type` on raw decoded JSON.
- Centralize parsing in a `fromJson` factory per model (see
  `dart/patterns.md`); never inline ad-hoc `map['field']` type-casts inside
  widgets or providers — that scatters the failure mode across the UI layer.
- A failed field parse must produce a typed error/null, not an uncaught
  exception that crashes the screen — fail one field, not the whole flow.

### Secrets & tokens
- Auth tokens, refresh tokens, PINs, and biometric keys never go into
  `shared_preferences` (unencrypted plist/XML on disk) — use
  `flutter_secure_storage` (Keychain/Keystore-backed) exclusively. See
  `flutter/security.md` for the storage-tier decision table.
- Never `print`/`log` a full `Response` object, request body, or header map
  that may carry a token, card number, or KYC document — mask before
  logging, same as the common-tier rule.

### Serialization
- Do not hand-roll `toJson`/`fromJson` for models with more than a couple of
  fields — use `json_serializable`/`json_annotation` (already a project
  dependency) so the generated code is consistent and reviewable as a diff.
- Never serialize a token or secret into a model that also gets logged,
  cached to disk in plaintext (Hive without encryption), or sent to
  analytics/crash reporting.

### Deserialization of untrusted collections
- When decoding a `List<dynamic>` from an API, validate each element's shape
  before mapping — one malformed element must not throw and abort the whole
  list render.
