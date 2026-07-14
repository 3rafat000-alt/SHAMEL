---
name: rules-flutter-security
description: >
  Flutter-framework security rules — extends rules-dart-security with
  secure-storage tier selection, platform-channel, and UI-layer data
  exposure guidance for this project's biometric/PIN/secure-storage stack.
  Use for any task touching tokens, biometrics, screen capture, or native
  platform channels under mobile/lib.
paths:
  - "projects/PRJ-SAKK/mobile/lib/core/services/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/features/auth/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/features/pin/**/*.dart"
  - "projects/PRJ-SAKK/mobile/lib/features/kyc/**/*.dart"
  - "**/*.dart"
---

## | أمن فلاتر | Flutter Security

Purpose: Flutter-specific security baseline on top of `dart/security.md`.
Activated when: any agent handles tokens, biometrics, screen protection, or
platform channels.

### Storage tier — pick deliberately
| Data | Storage |
|------|---------|
| Auth/refresh tokens, PIN hash/salt, biometric-derived keys | `flutter_secure_storage` only |
| Non-sensitive user prefs (theme, language, onboarding-seen) | `shared_preferences` |
| Structured local cache (transaction history cache, draft forms) | `hive_flutter`, and if it can contain PII/balances, encrypt the Hive box |
- Never store a token or PIN in `shared_preferences` or an unencrypted Hive
  box "temporarily" — temporary storage decisions outlive their intent.

### Biometrics & PIN
- `local_auth` results are a boolean gate, not a secret — the actual
  authorization (API call, unlocking a stored credential) must happen after
  the biometric check succeeds, never assume "device has biometrics enrolled"
  implies "user is authorized".
- PIN verification happens against a securely stored hash (see
  `pin_service.dart`), never a plaintext PIN compared in memory/logs.
- Lock out / backoff after repeated failed PIN attempts; do not rely on the
  OS biometric prompt's own rate-limiting as the only defense.

### Screen protection
- Sensitive screens (card number reveal, PIN entry, KYC document capture,
  seed/recovery data if any) use the project's screen-security service
  (`screen_security_service.dart`) to block screenshots/screen-recording —
  do not add a new sensitive screen without wiring this in.

### Platform channels
- Any `MethodChannel` call crossing to native code validates/sanitizes
  arguments going out and the result coming back with the same rigor as an
  API boundary (see `dart/security.md`) — a native side crash or malformed
  return value must not propagate as an unhandled exception into the UI.
- Do not pass secrets through a `MethodChannel` argument that could be
  intercepted by a compromised native-side plugin without first confirming
  the plugin is first-party/trusted.

### Deep links & external input
- Treat `app_links`/deep-link payloads (referral, pay links) as untrusted
  input — validate scheme, host, and every query param shape before routing
  or acting on them (see `deep_link_parser.dart`); a malformed or malicious
  link must fail closed, not crash the app or silently authorize an action.

### Logging & crash reporting
- Never let a crash/log report include the raw payload from an API boundary
  parse failure if that payload could contain a token, card PAN, or KYC
  field — scrub before attaching to Crashlytics/Firebase logs.
