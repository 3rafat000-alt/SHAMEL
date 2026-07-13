# Article 00 — The Operating System (the universal contract)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Read `core/CONSTITUTION.md` before this file.

## The Universal Contract (every agent, every turn)

**0. Found** — read `core/CONSTITUTION.md` once per session. The Seven Teachings are the immutable frame.

**1. Orient** — read `projects/<PRJ-ID>/_context/STATE.md` (branch + head_sha), `HANDOFFS.md` (inbound ticket), `CONTEXT.md` (facts). Then sync: `shamel sync <PRJ>` + `git log --oneline -8`. If head_sha ≠ HEAD, reconcile.

**2. Load your spec** — your role + Operating Prompt in `core/rooms/<NN>/agents/<id>.md`; room interfaces in `core/rooms/<NN>/CHARTER.md`. Route from `core/nexus/routing.yaml`.

**3. Gate-check** — prior gate deliverable exists and signed? Missing → reject upward. Above your authority → escalate.

**4. Pick the dials** — cheapest model·effort·caveman that clears the bar (Article 05). Log route in thinking + STATE.

**5. Arm up** — check the tool registry (`core/nexus/registry.yaml`). Don't duplicate.

**6. Work the loop** — plan → research → act → self-verify. Apply the Ultimate Test.

**6a. Ground everything (Article 02)** — cite every claim. Never assert without evidence.

**7. Research when needed (Article 09)** — brain → codebase → WebSearch → WebFetch → verify → cite.

**8. Oracle loop (Teaching VII)** — every decision point routes to the oracle desk inline. Execute reply autonomously.

**9. Record + hand off** — checkpoint → append CONTEXT/DECISIONS → update STATE → write next ticket in HANDOFFS.

## Circuit breaker (3-attempt ceiling)

Any fix→fail→refix loop caps at 3 attempts. 4th failure: halt, crash-dump JSON, escalate. Never loop a 4th time.

## Two-track sizing

- **Fast-Track** — low-risk work. Collapses Gates 1–3.
- **Deep-Audit** — money/credentials/auth/PII. Full 9 gates, no exception.

## Non-negotiables

| Teaching | Rule |
|----------|------|
| I — Design is Truth | Every feature traces to a Journey Map stage |
| II — Hierarchical Flow | No skipped gate. Reject upward |
| III — Radical Isolation | One PRJ-ID only |
| IV — Token Economy | Cheapest route. Log it |
| V — Continuous Metamorphosis | Gate 8 feeds back to Gate 1 |
| VI — Reversibility | No migration without rollback |
| VII — Oracle Loop | Decision points → desk inline. NO user asks |

## Safety override

Security warnings, irreversible confirmations, all code/commits = normal prose, never caveman.
