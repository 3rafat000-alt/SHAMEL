---
name: rules-laravel-security
description: >
  Laravel-specific security rules for SHAMEL's PRJ-SAKK backend. Extends
  php/security.md with Laravel framework guards — mass assignment, Blade
  escaping, Sanctum auth, webhook route CSRF exemption. Use for any task
  writing models, controllers, Blade views, or webhook routes in Laravel.
paths:
  - "projects/PRJ-SAKK/backend/app/Models/**/*.php"
  - "projects/PRJ-SAKK/backend/app/Http/**/*.php"
  - "projects/PRJ-SAKK/backend/routes/**/*.php"
  - "projects/PRJ-SAKK/backend/resources/**/*.blade.php"
  - "**/app/Models/**/*.php"
  - "**/routes/**/*.php"
  - "**/*.blade.php"
---

## | أمن Laravel | Laravel Security

Extends `php/security.md`. Purpose: Laravel 12 framework-specific guards
on top of the PHP security baseline. Activated when: any agent writes a
model, controller, route, or Blade view in
`projects/PRJ-SAKK/backend/`.

### Mass assignment
- Every model has an explicit `$fillable` allow-list (preferred) or
  `$guarded` — never `protected $guarded = []` on a model reachable from
  user input. An open model lets a client set columns like `is_admin`,
  `balance`, or `kyc_status` through unrelated form fields.
- Money/status/role columns (`balance`, `status`, `role`, `is_verified`)
  should be **excluded** from `$fillable` and set only through explicit,
  authorized code paths — not via generic mass-assigned update.

### Authorization
- Every route touching a user-owned resource (wallet, card, transaction)
  must call a Policy (`$this->authorize(...)`) — see `laravel/patterns.md`.
  Authentication (valid Sanctum token) is not authorization.
- Sanctum-protected routes go under `auth:sanctum` middleware; never
  assume a route is protected just because it's under `/api`.

### Webhook routes
- Payment webhook routes (`app/Http/Controllers/Webhooks/
  CCPaymentWebhookController.php`, `StripeIssuingWebhookController.php`)
  are necessarily CSRF-exempt — signature verification is the *only*
  trust check. Verify before any DB write, per `ccpayment-integration` /
  `stripe-issuing-integration`.
- Webhook controllers must not trust the payload's stated user/wallet ID
  without cross-checking it against the signed transaction reference.

### Blade escaping
- Use `{{ $var }}` (auto-escaped) by default; `{!! $var !!}` (raw) is
  only for trusted, sanitized HTML — never a value from user/webhook input.

### Rate limiting
- Auth endpoints (login, OTP/2FA) and money-moving endpoints (withdraw,
  transfer, card load) get explicit `throttle:` middleware — abuse risk
  differs from a read-only endpoint.

### Signed/temporary URLs
- Any link granting time-limited access (KYC document, invoice PDF) uses
  `URL::temporarySignedRoute`, not a guessable ID with no expiry.
