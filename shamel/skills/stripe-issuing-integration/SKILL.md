---
name: stripe-issuing-integration
description: >
  Working knowledge of PRJ-SAKK's Stripe ISSUING integration (virtual cards) —
  not standard Payments/Checkout/Billing. Covers cardholder/card lifecycle,
  the real-time authorization webhook, custom signature verification, PCI
  posture, and known gaps. Use when touching app/Services/StripeIssuingService.php,
  CardService.php, CardController.php, StripeIssuingWebhookController.php,
  ProcessStripeIssuingWebhook.php, or anything under the /cards feature.
  Recommended for: bck-integration-engineer, bck-domain-engineer,
  sec-appsec-engineer, sec-compliance-auditor, qa-test-architect.
user-invocable: true
metadata:
  project: PRJ-SAKK
  category: payments
  version: "1.0.0"
  grounded_in: "app/Services/StripeIssuingService.php, CardService.php, CardController.php, StripeIssuingWebhookController.php, ProcessStripeIssuingWebhook.php, EnsureCardsEnabled.php, CardsFeature.php, VirtualCard.php, config/services.php — read 2026-07-11"
---

# Stripe Issuing Integration — PRJ-SAKK

This is Stripe **Issuing** (creating and operating virtual cards), a materially
different product from Stripe Payments/Checkout/Billing. Do not reach for
`stripe_implementation_planner` (the connected Stripe MCP's payment planner) —
it is oriented at accepting payments, not issuing cards. Instead use
`search_stripe_documentation` with `search_only_api_ref: true` for Issuing API
details, and plain `search_stripe_documentation` for conceptual/how-to guidance.

## When to use this skill
- Any change to cardholder creation, card issuance, spending controls, freeze/
  unfreeze/cancel, or card-detail retrieval.
- Any change to the Issuing webhook handler or the authorization decision path.
- Security/compliance review of card data handling (PCI scope).
- Debugging a Stripe Issuing webhook signature failure or a stuck authorization.

## Architecture map (file:responsibility)

| File | Responsibility |
|---|---|
| `app/Services/StripeIssuingService.php` | All direct Stripe Issuing API calls: cardholder/card create+update, spending controls, freeze/cancel, webhook signature verification, authorization/capture/reversal handlers. |
| `app/Services/CardService.php` | Domain-level card operations wrapping StripeIssuingService; owns the PCI-safe `getCardDetails()` path. |
| `app/Http/Controllers/API/CardController.php` | HTTP surface for the `/cards` feature. |
| `app/Http/Controllers/Webhooks/StripeIssuingWebhookController.php` | Single webhook endpoint, `POST /api/webhooks/stripe/issuing`. Answers `issuing_authorization.request` **synchronously** (Stripe's 2s SLA); dispatches everything else to a queued job. |
| `app/Jobs/ProcessStripeIssuingWebhook.php` | Queued handling of transaction/dispute/capture/reversal events (3 tries, 5s backoff). |
| `app/Http/Middleware/EnsureCardsEnabled.php` + `app/Support/CardsFeature.php` | Kill-switch gate on the whole `/cards` route group. |
| `app/Models/VirtualCard.php` | Local card record — `card_number`/`cvv` are in `$hidden`; masked PAN only for Stripe-backed cards. |

## Feature flag is DB-driven, not env-driven
`CardsFeature::enabled()` checks an `Integration` row (`key='stripe'`) in the
database, managed via the admin Integrations panel. **Setting `STRIPE_SECRET`
in `.env` does not turn cards on** if that row exists with `is_active=false` —
this is a deliberate admin kill-switch. Config resolution order:
`Integration` DB row → `.env` fallback only if no row exists.

## Webhook signature verification is hand-rolled
`StripeIssuingService::verifyWebhookSignature()` does NOT use the
`stripe/stripe-php` SDK's `Webhook::constructEvent`. It manually parses
`Stripe-Signature: t=...,v1=...`, recomputes `HMAC-SHA256("{t}.{payload}",
webhookSecret)`, and does a `hash_equals` constant-time compare, rejecting
timestamps >300s old. Functionally equivalent to the SDK's algorithm, but:
- **Only the last parsed `v1=` value is checked** — during a Stripe-side
  webhook secret rotation (which sends both old and new `v1=` values), this
  can cause false signature failures. If debugging a rotation-window failure,
  check this first.
- Required env: `STRIPE_ISSUING_WEBHOOK_SECRET` (separate from
  `STRIPE_WEBHOOK_SECRET`, which is for a different, non-Issuing webhook).
  **Known gap**: `.env.example` does not document `STRIPE_ISSUING_WEBHOOK_SECRET`
  or `STRIPE_TEST_MODE` — anyone bootstrapping from the example file alone
  will misconfigure this. Fix by adding both to `backend/.env.example`.

## The authorization path is latency-critical — do not add I/O
`issuing_authorization.request` must respond within Stripe's ~2 second SLA.
It is deliberately:
- Answered synchronously in the controller, not queued.
- Idempotency-checked NOT via the cache (`Cache::add`, used for every other
  event type) but by looking up an existing `Transaction` with
  `metadata->authorization_id` under a **wallet row lock** — this is
  necessary because a cache round-trip risks blowing the latency budget, and
  the row lock protects against Stripe's own retry-on-timeout behavior
  causing a double-authorization. If you touch this path, preserve the row-lock
  idempotency check; do not swap it for the cache-based dedup used elsewhere.

## PCI scope — known gap, needs remediation
`CardService::getCardDetails()` / `CardController::stripeCardDetails()` are
intentionally masked-only (comments cite PCI-DSS) — **this is the correct
pattern and the one to follow for new code.**

However, `StripeIssuingService::getCardDetails()` (a *different*, lower-level
method) calls `stripe->issuing->cards->retrieve($id, ['expand'=>['number','cvc']])`
and returns the **raw PAN and CVC** in a JSON API response — this is exactly
the pattern Stripe's own docs recommend AGAINST for anything beyond a one-off
Dashboard export. Current Stripe guidance: use **Issuing Elements**
(client-side, Stripe-hosted iframe via an ephemeral key) so PAN/CVC never
transit your server or hit your logs/APM. If asked to work on card-detail
display, treat migrating this to Issuing Elements as the correct fix, not
a nice-to-have — raw PAN/CVC in a server response body is a real PCI
scope-expansion risk (it can land in access logs, error trackers, browser
history via GET, etc.).

## Using the Stripe MCP for this integration
- `search_stripe_documentation({question: "...", search_only_api_ref: true})`
  for exact Issuing API parameters (cardholder/card create, spending_controls
  shape, authorization object fields).
- `search_stripe_documentation({question: "..."})` (no `search_only_api_ref`)
  for conceptual guidance — e.g. "Issuing Elements ephemeral key flow",
  "Issuing real-time authorization webhook requirements", "Issuing webhook
  signature verification".
- Do NOT use `stripe_implementation_planner` for Issuing work — it is scoped
  to Payments/Checkout/Billing use cases and will produce irrelevant guidance.
- `get_stripe_account_info` is safe to call to confirm which Stripe account/mode
  (test vs live) credentials are pointed at before making any live-mode change.

## Quick gotcha checklist before touching this integration
1. Raw PAN/CVC exposure in `StripeIssuingService::getCardDetails()` — treat as
   a known issue, prefer Issuing Elements for anything new.
2. `issuing_authorization.request` must stay synchronous + wallet-row-locked.
3. Webhook secret rotation can false-fail signature checks (last-`v1`-only bug).
4. `.env.example` is missing `STRIPE_ISSUING_WEBHOOK_SECRET` / `STRIPE_TEST_MODE`.
5. Feature enablement is DB (`Integration` row), not `.env` — check that first
   when cards appear "off" despite correct env vars.
