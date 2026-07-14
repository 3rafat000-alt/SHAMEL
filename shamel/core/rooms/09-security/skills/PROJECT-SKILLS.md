# Security room — PRJ-SAKK project skills

Canonical location: `~/Desktop/SHAMEL/.claude/skills/<name>/SKILL.md`

- **stripe-issuing-integration** — flags a real, unresolved PCI gap:
  `StripeIssuingService::getCardDetails()` returns raw PAN+CVC in a server
  JSON response (Stripe recommends Issuing Elements instead, so PAN/CVC
  never touch the server). Also documents the hand-rolled webhook signature
  verification (not the SDK's `constructEvent`) and a rotation-window bug
  (only the last `v1=` value is checked during a Stripe secret rotation).

- **ccpayment-integration** — documents the webhook security posture: HMAC
  signature check fails CLOSED (verified correct against official docs),
  but IP allow-listing fails OPEN if unconfigured — an asymmetry worth
  reviewing. Also documents the "never trust the webhook body's amount"
  pattern used for deposit crediting.

Both are grounded in a full code read (2026-07-11), not generic docs — use
them as a starting point for a security review of either integration, then
verify current state before relying on any specific claim.
