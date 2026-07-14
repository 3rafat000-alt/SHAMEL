---
name: rules-flutter-patterns
description: >
  Flutter-framework pattern rules — extends rules-dart-patterns with
  widget-tree, state-management, and navigation conventions for this
  project's Riverpod + go_router stack. Use for any task writing or editing
  widgets, providers, or routes under mobile/lib.
paths:
  - "projects/PRJ-SAKK/mobile/lib/features/**/presentation/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/features/**/providers/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/core/router/**/*.dart"
  - "**/*.dart"
---

## | أنماط فلاتر | Flutter Patterns

Purpose: Flutter-specific structural patterns on top of `dart/patterns.md`.
Activated when: any agent writes or edits a widget, provider, or route.

### No business logic in `build()`
- `build()` methods stay declarative: layout + reading already-computed
  state. Parsing, calculation, filtering, and API calls do not belong in
  `build()` — they belong in the provider/notifier/repository. `build()` can
  re-run many times (rebuilds, hot reload, theme change); side-effecting or
  expensive logic there is both a correctness and a performance bug.
- If a widget needs derived data, compute it in a `Riverpod` provider
  (`Provider`/`select`) or a plain method on the model — not inline in the
  widget tree.

### State management (Riverpod, this project's stack)
- One `Notifier`/`AsyncNotifier` per cohesive feature-state concern; do not
  merge unrelated state into one provider "for convenience" — it causes
  unrelated widgets to rebuild on unrelated changes.
- Prefer `AsyncNotifier`/`AsyncValue` for anything backed by an API call so
  loading/error/data states are modeled explicitly — do not represent
  "loading" with a nullable field plus a separate `isLoading` bool that can
  drift out of sync.
- Use `ref.watch` with `.select()` when a widget only needs one field of a
  larger state object, to avoid rebuilding the whole subtree.
- Dispose/cancel subscriptions (streams, timers, listeners) in
  `ref.onDispose` — a leaked listener after a provider is torn down is a
  silent memory/behavior bug that will not show up in a quick manual test.

### Widget composition
- Extract a `StatelessWidget`/`ConsumerWidget` once a `build()` method mixes
  more than one visual concern or exceeds ~1 screenful — large inline widget
  trees hide the actual layout structure from the reader.
- Prefer `const` constructors wherever the widget's inputs are compile-time
  constant — this is a real rebuild-avoidance win in Flutter, not a style
  nit.

### Navigation (go_router)
- Routes are declared centrally in `core/router/`; feature widgets navigate
  via named routes/`context.go`/`context.push`, not hardcoded path strings
  scattered across features — a typo'd literal path fails silently at
  runtime with no compile-time check.
- Guard authenticated routes at the router redirect level, not by scattering
  `if (!isLoggedIn)` checks inside individual page widgets.

### Error boundaries in the UI
- Every `AsyncValue`/`FutureBuilder` consumer handles all three states
  (`data`/`loading`/`error`) explicitly — an unhandled `error` case that
  falls through to rendering `null`-derived data is exactly how a boundary
  parsing failure becomes a visible crash instead of a graceful error state.
