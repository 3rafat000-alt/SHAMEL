# Article 03 — Verification (outcome over self-report)

Foundation: serves Teaching VI (Reversibility) and Teaching II (Hierarchical Flow). Read `02-grounding.md` first, then `core/nexus/gates.yaml`.

## V1 — Outcome over self-report (mechanical)

A ticket marked `done` must carry an evidence block (command + output/exit code, file:line proof, or diff/SHA). `shamel gate-check` validates evidence and rejects bare "done" — fail-closed.

## V2 — Fresh-context adversarial verify

Before any gate advances: `gtw-gatekeeper` checks the diff/output against the ORIGINAL ticket criteria, never the implementer's reasoning. UNKNOWN is a valid verdict. For high stakes, route through the oracle desk (family-diverse judge).

## V3 — Pass^k at Gates 5–6

Money/auth/PII paths heading to staging/prod: re-run critical check k times. Flaky correctness blocks the gate.

## V4 — Never gate an irreversible action on verbalized confidence

Ship/rollback decisions gate on behavioral proxies only (exit 0, artifact exists, k runs pass, rollback script tested). Never the model's self-rated certainty.

## V5 — Judges drift; sample the transcripts

Periodically spot-check the trajectory behind a PASS and behind a 0-finding report (brd-cqo owns the audit cadence).

## Wiring

| Wire | Mechanism |
|------|-----------|
| V1 mechanical | `shamel gate-check` → `validate_evidence()` fail-closed |
| V1 at handover | Work Order Format requires evidence block |
| V2 gate advance | `gtw-gatekeeper` fresh-context adversarial check |
| V2 in-room | `bck-code-reviewer` / `fnt-code-reviewer` review diffs fresh-context |
| V3 | pass^k plan in Gate-5 test strategy |
| V4 | `ops-release-manager` gates on behavioral proxies |
| V5 | brd-cqo transcript spot-checks |
