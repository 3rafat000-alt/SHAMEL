# Article 06 — Git Discipline (the spine)

Foundation: serves Teaching VI (Reversibility) and Teaching II (Hierarchical Flow). Read `core/CONSTITUTION.md` first.

## Branch model

| Branch | Holds | Who commits |
|--------|-------|-------------|
| `main` | SHAMEL doctrine, constitution, nexus, rooms, tooling | brd-ceo |
| `prj/<PRJ-ID>` | All work for one project | every agent on that project |
| `worktrees/<PRJ-ID>-gate<N>-<squad>` | A parallel squad's isolated tree | one squad |

Project isolation is a branch boundary. A project branch never merges to `main`.

## Worktree-per-squad

Gates 3/4/5 run squads concurrently behind frozen input. Each squad its own worktree: `shamel worktree <PRJ> <gate> <squad>`. Merge at gate close, not before.

## Checkpoints (commit cadence)

- Minimum: one commit per ticket, before next ticket.
- During long work: checkpoint each sub-milestone (`wip:`) .
- Before risky op: checkpoint first.
- Before handoff: always. Receiver reads last SHA.

## Commit message format

```
<type>(<scope>): <subject ≤ 50 chars>

<body — the "why">

SHAMEL: <PRJ-ID> · <TKT-ID> · gate <N> · <agent-id>
```

type ∈ `feat fix chore docs refactor test perf ci build style revert wip`. SOFI: trailer still valid; SHAMEL: preferred.

## Git steps

**ORIENT:** `shamel sync <PRJ>` + `git log --oneline -8`
**CLAIM:** `shamel claim <PRJ> <path-glob>` → `_context/LOCKS.md`
**CHECKPOINT:** `shamel checkpoint <PRJ> "<type>(<scope>): <subject>"`
**HANDOFF:** `shamel checkpoint <PRJ>` → `shamel sync <PRJ> --push`

## Never commit

Secrets, runtime state, caches, `_scratch/`, build artifacts.

## Rollback

`git revert <sha>` — forward-only. Never `git reset --hard`, never `git push --force`. Tag at gate close: `shamel gate-tag <PRJ> <N>`.
