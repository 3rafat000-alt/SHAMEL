---
name: ccpayment-integration
description: >
  Working knowledge of PRJ-SAKK's CCPayment integration (crypto deposit/
  withdrawal on-ramp bridge). Covers the HMAC signature scheme (confirmed
  correct against official docs), webhook handling, the two reconciliation
  jobs and the failure modes they guard against, and coin/chain ID gotchas.
  Use when touching app/Services/CCPaymentService.php, CCPaymentController.php,
  CCPaymentWebhookController.php, ReconcileCCPaymentDeposits.php,
  ReconcilePendingWithdrawals.php, or anything under the crypto-deposit
  feature. Recommended for: bck-integration-engineer, bck-domain-engineer,
  sec-appsec-engineer, sec-compliance-auditor, dat-etl-engineer (reconciliation).
user-invocable: true
metadata:
  project: PRJ-SAKK
  category: payments
  version: "1.1.0"
  grounded_in: "app/Services/CCPaymentService.php, CCPaymentController.php, CCPaymentWebhookController.php, ReconcileCCPaymentDeposits.php, ReconcilePendingWithdrawals.php, VerifyIdempotencyKey.php, config/services.php, IntegrationController.php — read 2026-07-11; cross-checked against the official https://github.com/cctip/ccpayment-sdk-skills repo (cloned 2026-07-11, doc version v2.1 / 2026-04-07) — see vendor-api-reference/ in this skill folder"
---

# CCPayment Integration — PRJ-SAKK

CCPayment is used here as a **crypto deposit/withdrawal on-ramp bridge**
(converts crypto deposits into wallet balance, and dispatches crypto
withdrawals). This skill covers PRJ-SAKK's specific implementation; for the
**full official API reference** (all 13 modules, 61 endpoints, plus an SDK
code generator), see `vendor-api-reference/` in this same skill folder —
cloned from the official `cctip/ccpayment-sdk-skills` repo. Re-clone if it's
been more than a few months (`git clone --depth 1
https://github.com/cctip/ccpayment-sdk-skills.git`) since CCPayment's API
evolves and that repo tracks it.

## When to use this skill
- Any change to deposit address creation, deposit crediting, or withdrawal
  dispatch.
- Debugging a CCPayment webhook signature failure.
- Adding a new CCPayment endpoint (e.g. swap, batch withdraw) — read the
  matching module doc in `vendor-api-reference/` first (see module table
  below), not just this summary.
- Reviewing the reconciliation jobs (deposit/withdrawal consistency).

## Architecture map (file:responsibility)

| File | Responsibility |
|---|---|
| `app/Services/CCPaymentService.php` | All CCPayment API calls via `request()` (POSTs to `https://ccpayment.com/ccpayment/v2/<endpoint>`, unwraps `{code:10000, msg, data}`), signature generation/verification, deposit webhook crediting, withdrawal webhook status sync. |
| `app/Http/Controllers/API/CCPaymentController.php` | HTTP surface: deposit address creation, withdrawal requests (two-phase: debit+reserve, then dispatch). |
| `app/Http/Controllers/Webhooks/CCPaymentWebhookController.php` | `deposit()`, `withdraw()`, and the dashboard `ActivateWebhookURL` handshake. Routed via `routes/web.php` (not `api.php` — CCPayment can't send Sanctum tokens). |
| `app/Console/Commands/ReconcileCCPaymentDeposits.php` | Manual/admin-triggered recovery for deposits stuck PENDING after a webhook silently mis-processed. |
| `app/Console/Commands/ReconcilePendingWithdrawals.php` | Scheduled every 5 min (`routes/console.php`) — closes the optimistic-debit gap (see below). |
| `app/Http/Middleware/VerifyIdempotencyKey.php` | Idempotency enforcement on outbound requests. |

## Signature scheme — confirmed CORRECT, do not "fix"

`CCPaymentService::generateSign()` builds `HMAC-SHA256(appId + timestamp +
body, appSecret)` with a **13-digit millisecond timestamp**
(`(string)(time()*1000)`). This is **verified correct** against the official,
current (2026-04-07) API docs:
- `vendor-api-reference/README.md:13` and `vendor-api-reference/api/README.md:13`
  both explicitly state `Timestamp: millisecond timestamp`.
- The exact signature formula (`appId + timestamp + body`, HMAC-SHA256, hex
  output) matches the official reference implementation.
- The error codes PRJ-SAKK's code comments cite as real production evidence
  (`11005 VerifySignFailed`, `13000 InvalidCoin`, `13001 InvalidChain`) match
  `vendor-api-reference/api/appendix.md` exactly.

**If you ever find web-search results claiming CCPayment wants a 10-digit
second timestamp, that is stale/v1 information — trust the millisecond
scheme confirmed above and in the vendor reference, and trust PRJ-SAKK's
existing `generateSign()`.** Do not "fix" it to seconds.

One real, separate finding still worth fixing: **body must be sent
byte-identical to what was hashed** — the code uses `Http::withBody($body, ...)`
rather than `->post($data)` specifically to avoid Guzzle re-encoding the JSON
differently than what was signed. Preserve this pattern in any new endpoint
you add; using `->post()`/`->asJson()->post()` instead will intermittently
break signature verification depending on Guzzle's key ordering.

## Webhook handling
- `deposit()` and `withdraw()` webhooks live on `routes/web.php` (not
  `api.php`) since CCPayment cannot present a Sanctum bearer token.
- `handleActivation()` must echo `{"msg":"Success"}` for the CCPayment
  dashboard's URL-registration handshake to succeed — do not add auth in
  front of this route or the dashboard activation will fail.
- **Never trust the webhook body's amount for crediting** —
  `handleDepositWebhook()` re-fetches the authoritative amount via
  `getAppDepositRecord` before crediting (code comment "SEC H3"). Preserve
  this re-fetch pattern in any new webhook-triggered money movement.
- IP allow-listing (`verifyWebhookIp()`, `CCPAYMENT_IP_WHITELIST` env, CIDR
  capable) is a bonus check beyond CCPayment's own spec and **fails OPEN**
  if no whitelist/debug mode is configured — unlike the signature check,
  which fails closed. If tightening security here, note this asymmetry.

## The two reconciliation jobs — know why each exists
1. **`ReconcileCCPaymentDeposits`** (manual/admin-only, not scheduled) —
   recovers deposits stuck PENDING when a webhook was received and 2xx'd
   but mis-processed internally (CCPayment then never retries a 200
   response). Works around a real CCPayment API limitation: `getAppDepositRecordList`
   cannot filter by `referenceId`, only `coinId`.
2. **`ReconcilePendingWithdrawals`** (scheduled every 5 min) — closes the
   **optimistic-debit gap**: withdrawal dispatch is a two-phase process
   (Phase A: debit + reserve funds, commit; Phase B: call CCPayment's
   withdraw API). If the process crashes between phases, funds are debited
   with nothing dispatched. This job queries `getAppWithdrawRecord` and
   either refunds (no record exists at CCPayment) or syncs status (record
   exists) — always under a fresh wallet row lock, never inside the
   original transaction. **Any new money-out flow through CCPayment must
   replicate this two-phase pattern** — do not call the gateway from inside
   a wallet row lock.

## Coin/chain ID gotchas
- `getCoinId()` maps a symbol to CCPayment's numeric `coinId` (e.g.
  USDT=1280) **per-coin only** — it intentionally ignores any chain
  argument. Passing a wrong-style ID triggers error `13000 InvalidCoin`.
- Chain parameters must use CCPayment's own symbol style (`TRX`/`ETH`/`BSC`/
  `BTC`), NOT the app's network codes (`TRC20`/`ERC20`/`BEP20`) — see
  `ccChain()`. Mismatch triggers `13001 InvalidChain`.

## Config
`config/services.php`: `CCPAYMENT_APP_ID`, `CCPAYMENT_APP_SECRET`,
`CCPAYMENT_IP_WHITELIST`, `CCPAYMENT_DEBUG_MODE`, `CCPAYMENT_WEBHOOK_BASE`
(defaults to `https://sakk.zanjour.com` — note this is decoupled from
`APP_URL`), `CCPAYMENT_RECONCILE_WITHDRAWALS_AFTER_MINUTES`. These are a
**fallback only** — `loadConfig()` prefers an `Integration` DB row
(`key='ccpayment'`) managed via the admin panel; if that row exists with
`is_active=false`, env creds are hard-ignored (fail-closed kill-switch).
Admin credential edits require email OTP. The admin `test()` endpoint only
checks that app_id/app_secret are non-empty — **it does not actually call
CCPayment** — don't rely on it to validate real credentials.

## Official API reference — module map
For any endpoint beyond what's already implemented, read the matching file
under `vendor-api-reference/api/`:

| Module | File | Endpoints | Currently used by PRJ-SAKK? |
|---|---|---|---|
| Basic Info | `01-basic-info.md` | 7 | Not directly (could replace hardcoded coin/chain lists) |
| Merchant Assets | `02-merchant-assets.md` | 3 | Yes — `getAppCoinAssetList`, `getAppCoinAsset` |
| Merchant Deposit | `03-merchant-deposit.md` | 4 | Yes — deposit address creation/lookup |
| Merchant Withdraw | `04-merchant-withdraw.md` | 8 | Yes — `applyAppWithdrawToNetwork`, record queries |
| Merchant Batch Withdraw | `05-merchant-batch-withdraw.md` | 7 | No |
| User Assets | `06-user-assets.md` | 2 | No (merchant-mode assets used instead) |
| User Deposit | `07-user-deposit.md` | 3 | No |
| User Withdraw | `08-user-withdraw.md` | 4 | No |
| User Transfer | `09-user-transfer.md` | 7 | No |
| Orders | `10-orders.md` | 3 | No |
| Swap | `11-swap.md` | 5 | No |
| User Swap | `12-user-swap.md` | 3 | No |
| Utilities | `13-utilities.md` | 5 | No (IP whitelist check implemented independently) |

`applyAppWithdrawToCwallet` (internal-wallet-to-wallet withdrawal) exists in
`CCPaymentService.php` but is currently **unused by any controller** — flag
if asked why a "dead" method exists; it's implemented but not yet wired to
a route, not dead code from a removed feature.

## Quick gotcha checklist
1. Signature/timestamp scheme is correct as-is — verified against current
   official docs. Do not "fix" the millisecond timestamp.
2. Send the exact byte-identical body you signed (`Http::withBody`, not
   `->post($data)`).
3. Never credit a deposit from the webhook body's amount — re-fetch via
   `getAppDepositRecord`.
4. Any new money-out flow: two-phase (debit+reserve, then dispatch),
   dispatch call OUTSIDE any wallet row lock.
5. `coinId` ignores chain; `chain` param uses CCPayment's own symbols, not
   app network codes.
6. IP whitelist check fails OPEN if unconfigured — signature check fails
   CLOSED. Don't assume both fail the same way.
7. Admin `test()` button does not call CCPayment — it only checks
   credentials are non-empty.
