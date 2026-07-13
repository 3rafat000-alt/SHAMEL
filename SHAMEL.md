# شامل / SHAMEL

> Unified AI Software Enterprise Framework
> Successor to SOFI v1–v6. One entry point, one registry, one brain.

## Identity

- **Name:** SHAMEL (شامل) — "comprehensive, all-encompassing"
- **Root:** `~/Desktop/SHAMEL/`
- **Remote:** `https://github.com/3rafat000-alt/SHAMEL`
- **Genesis:** 2026-07-10 — clean break from Lorka lineage

## Layer Map

| Layer | Path | Purpose |
|-------|------|---------|
| Governance | `shamel/core/` | Constitution, Nexus, rooms, gates |
| Deterministic | `shamel/engine/` | `shamel` CLI, tooling, scanners |
| Memory | `shamel/brain/` | Org knowledge, templates, memdb |
| Projects | `projects/` | Isolated product repos |
| Integration | `.claude/` | Hooks, skills, agents, commands |
| Archive | `archive/` | Retired generations with tombstones |

## Key Principles

- Single source per concern (P1)
- Code is truth — every number generated (P2)
- No claim without automated enforcement (P3)
- Git day-zero for every project (P4)
- Builder never self-grades (P5)
- Flat topology inside Claude Code (P6)

## Pipeline (MANDATORY — no exceptions)

```
User raw input
    ↓ [إجباري — لا يمكن تخطي]
gtw-intake-reformer → brd-ceo (+ board via Task) → room leads (via Task) → agents
    ↓ [إجباري]
room lead → brd-ceo → user
```

**مخالفة التدفق = مخالفة دستورية. النظام يرفض الرد.**

## Entry

```bash
PYTHONPATH=shamel/engine shamel doctor      # system health
PYTHONPATH=shamel/engine shamel selftest    # deterministic pass/fail
PYTHONPATH=shamel/engine shamel agents lint # agent file checks
```
