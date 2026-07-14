# Article 07 — Security Law

Foundation: serves Teaching VI (Reversibility) and Teaching III (Radical Isolation). Read `core/CONSTITUTION.md` first. All security text = normal prose.

## The CSO veto

brd-cso holds company-wide security veto, absolute below CEO. Any gate/merge/deploy/tunnel blocked on security grounds. Lifted only by remediation with evidence or CEO override in ADR.

## Secrets & PII

- Secrets never enter git. Hook-blocked, pattern-scanned.
- Secrets never enter a Work Order, ticket, brain file, or chat. Point at env var name.
- PII classified before stored. Deep-Audit track for anything money/auth/PII.
- Suspicion = rotation. Isolate, rotate, invalidate, preserve evidence, patch, redeploy.

## Sanitized-external-only

- Oracle desk: Python redacts keys/tokens/PII before sending. `--no-sanitize` only for verified-safe payloads.
- Public tunnels: seed/dummy data only.
- Web research: no project secrets, no NDA'd names, no PII.

## Tunnel bounds

- Owner: ops-domain-warden. Seed/dummy data only.
- Scoped and torn down after one task.
- A tunnel is NOT staging or prod.

## Mechanical enforcement

| Guard | What it blocks |
|-------|----------------|
| PreToolUse hook | dangerous commands, .env reads, bad commit format |
| Commit hook | secrets staged, reset --hard/--force |
| guard.scan_secrets | key/token patterns in content |
| guard.assert_net_allowed | network by non-web roles |
