# Article 08 — Handoff Law (tickets, boundaries, sign-off)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching V (Continuous Metamorphosis). Read `core/CONSTITUTION.md` first.

## The ticket

```md
## TKT-014 · gate 3
from: arc-system-architect
to:   dat-db-engineer
task: model entities for audit-log; reversible migrations.
consumes: docs/PRJ-0001_Tech_Stack.md, docs/PRJ-0001_OpenAPI.yaml
expected: Schema.sql + ERD + migrations(+rollback)
route: workhorse · high · full
status: open
```

Lifecycle: `open → accepted → done | rejected`. `shamel dispatch` operates the queue.

## Room-boundary validation

Ticket `from:`/`to:` same room, agent→Lead, Lead→Lead, or boardroom/gateway→Lead. Specialist never addresses another room's specialist directly. `validate_room_boundary()` in `shamel gate-check` — violation fails the gate.

## Verbatim forwarding

Lead forwards findings verbatim, citations and evidence intact. Never re-author.

## Gate sign-off

- Producer: mark `done` only with evidence block.
- Receiver: `accepted` after fresh-context check against original criteria.
- Gate advance: gtw-gatekeeper adversarial verdict + shamel gate-check → shamel gate-tag.

## Claims & LOCKS

`shamel claim <PRJ> <path-glob>` → `_context/LOCKS.md`. Release with `shamel release`.

## Session continuity

Every handoff records producer's commit SHA in STATE head_sha. Next session resumes exactly.
