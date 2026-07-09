# SHAMEL — Claude Code session contract

## Boot
1. `shamel doctor` first — confirm system health
2. Read `SHAMEL.md` (2min identity) + `core/CONSTITUTION.md` (supreme law)
3. Brain: `brain/BRAIN.md` (memory architecture) → `brain/org/DECISIONS.md` (ADRs)
4. Routemap: `core/nexus/` (registry · routing · gates · models)

## Operating contract
- RCCF work orders: `core/constitution/01-work-order.md`
- Gate lifecycle: `core/constitution/10-lifecycle-gates.md`
- Git discipline: `core/constitution/06-git-discipline.md`
- Protocol: `brain/PROTOCOL.md`

## Convictions
- Single source per concern — duplicate = defect
- Generated agents (`shamel agents build`) — no manual edit
- Evidence before claim — `validate_evidence()` fail-closed
- Questions → Gemini loop, not user

## CLI
```
shamel doctor | selftest | agents build|lint | new PRJ-XXXX
shamel sync | checkpoint | gate-check | dispatch
shamel brain query | oracle review
```
