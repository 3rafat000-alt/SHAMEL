---
name: rules-php-security
description: >
  PHP-specific security rules for SHAMEL projects. Extends common/security.md
  with PHP attack surfaces — raw SQL, deserialization, file handling. Use for
  any task writing code that handles input, DB queries, or file I/O in PHP.
paths:
  - "projects/PRJ-SAKK/backend/**/*.php"
  - "**/*.php"
  - "**/.env*"
  - "**/config/**/*.php"
---

## | أمن PHP | PHP Security

Extends `common/security.md`. Purpose: PHP-specific attack surfaces on top
of the language-agnostic baseline. Activated when: any agent writes PHP code
touching a DB query, file path, serialized data, or external input.

### SQL injection
- Never interpolate a variable into a raw SQL string (`DB::raw`,
  `whereRaw`, `selectRaw`) — use parameter bindings (`?` or named
  bindings) even inside raw fragments. String-concatenated table/column
  names are still an injection vector if ever derived from input.
- Query-builder methods (`where`, `find`, `create`) bind parameters
  automatically — prefer them over raw SQL unless a raw fragment is
  unavoidable, and bind explicitly when it is.

### Deserialization
- Never call `unserialize()` on data crossing a trust boundary (webhook
  body, user upload, queue payload from an external source) — use `json_decode`
  instead. PHP object deserialization of untrusted input is a known RCE vector.

### File handling
- Never build a filesystem path by concatenating user input — validate
  against an allow-list or use a generated/hashed filename or path
  traversal is possible (`../../etc/passwd` style).
- Validate uploaded file MIME type and extension server-side (not just the
  client-reported `Content-Type`); store uploads outside the public web
  root or behind a controller that enforces authz per download.

### Secrets & config
- `.env` values are read via `config()`, never `env()` directly outside
  config files (config is cached in production; direct `env()` calls
  elsewhere return null after `config:cache`).
- Never log a full `Request` object or an exception's `getTrace()` for a
  route that touches secrets, tokens, or PII — mask before logging (see
  `common/security.md`).

### Type juggling
- Use strict comparison (`===`, `!==`) for security-relevant checks —
  loose `==` on strings starting with `0e` risks PHP's "magic hash"
  false-positive match. Use `hash_equals()` for comparing signatures/
  HMACs/tokens — plain `===` on raw strings is timing-attack-vulnerable.

### Payment webhooks
- Per `common/security.md` "Payment/webhook integrations": verify the
  signature in the controller before the payload reaches any service/job
  code, using the exact scheme in `ccpayment-integration` /
  `stripe-issuing-integration`.
