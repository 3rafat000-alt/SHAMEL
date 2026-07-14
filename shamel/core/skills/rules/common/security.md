---
name: rules-common-security
description: >
  Base security rules shared by every language/stack in SHAMEL projects —
  trust boundaries, secrets handling, input validation. Language tiers
  (php/security.md, ...) extend this with stack-specific attack surfaces.
  Use for any task touching input handling, auth, secrets, or external
  integrations (payments, webhooks, third-party APIs).
paths:
  - "**/*.php"
  - "**/*.dart"
  - "**/*.ts"
  - "**/*.js"
  - "**/.env*"
  - "**/config/**"
---

## | الأمن العام | Common Security

Purpose: Language-agnostic security baseline — the foundation every
language/framework security file builds on. Activated when: any agent writes
code that handles input, auth, secrets, or talks to an external system.

### Trust boundaries
- Nothing crossing a trust boundary is safe by default: user input, query
  params, HTTP headers, webhook payloads, queue job payloads, third-party API
  responses. Validate/sanitize at the boundary, before business logic touches it.
- A signature on a webhook does not make the payload "trusted data" — it
  means the *sender* is verified. Still validate shape/types of the payload.

### Secrets
- Secrets (API keys, webhook signing secrets, DB credentials) live in env
  vars or a vault — never hardcoded, never committed, never logged.
- Never print/log a full request/response that may contain secrets or PII
  (auth headers, tokens, card numbers, KYC documents) — mask before logging.

### Input validation
- Validate type, range, and format before use — not just "is it present".
- Validate on the server regardless of client-side validation; client checks
  are UX, not security.

### Output
- Encode/escape output for its destination context (HTML, SQL, shell, log
  line) — the same string is dangerous differently in each context.

### Dependencies
- Pin dependency versions; do not silently allow floating majors in
  production manifests. Check for known CVEs before adding a new dependency
  that touches money, auth, or crypto.

### Payment/webhook integrations
- Any code touching a payment provider webhook (deposits, withdrawals, card
  authorizations) MUST verify the provider's signature before trusting the
  payload — see `ccpayment-integration` and `stripe-issuing-integration`
  skills for this project's exact HMAC/signature schemes. Do not re-derive
  or approximate a signature scheme from memory.

### Least privilege
- Service accounts/DB users/API keys get the minimum scope needed for their
  task — a job that only reads balances should not hold a withdrawal-capable key.
