# Backend room — PRJ-SAKK project skills

Canonical location: `~/Desktop/SHAMEL/.claude/skills/<name>/SKILL.md`
(discoverable by any Claude Code session; invoke via the Skill tool).

- **stripe-issuing-integration** — Stripe Issuing (virtual cards) integration
  facts: cardholder/card lifecycle, real-time authorization webhook,
  hand-rolled signature verification, DB-driven feature flag, known PCI gap.
  Use before touching `StripeIssuingService.php`, `CardService.php`,
  `CardController.php`, or the Issuing webhook/job.

- **ccpayment-integration** — CCPayment (crypto on-ramp) integration facts:
  HMAC signature scheme (confirmed correct against official docs — do not
  "fix" the millisecond timestamp), webhook handling, the two reconciliation
  jobs and what they guard against, coin/chain ID gotchas. Includes a cloned
  copy of the official API reference (13 modules / 61 endpoints) under
  `ccpayment-integration/vendor-api-reference/`. Use before touching
  `CCPaymentService.php`, `CCPaymentController.php`, or either reconcile
  command.

Both grounded in a full read of PRJ-SAKK's actual implementation (2026-07-11)
— not generic vendor docs. Re-verify against current code if it's been a
while since this date.
