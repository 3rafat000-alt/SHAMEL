# Article 11 — Intake & Orchestration (the hierarchy protocol)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Resolves the historical tension between slash-command skills and role-wearing: **skills are the discipline interface inside the session; role-wearing is the delegation protocol between agents.** They serve different concerns and are both legitimate.

## The protocol

Every delegation follows one path:
```
main session → specialist agent (one hop, RCCF Work Order)
```

- **Flat topology:** main session is the ONLY context that spawns. A subagent NEVER spawns subagents. Depth is faked by rounds (main → leaf A, collect → main → leaf B), not nesting.
- **One hop:** delegation is main session → leaf specialist. The CEO/tier-advisors are personas the main session WEARS, not live orchestrators.
- **Parallelism:** multiple spawns in one message (cross-tier class).
- **RCCF bindings:** every spawn carries Role·Context·Command·Format (Article 01). No spawn without all four.

## Skills vs Role-Wearing — the distinction

| Concern | Skills | Role-Wearing |
|---------|--------|-------------|
| What | Palette of discipline routines | Protocol for agent delegation |
| When | During a session, invoked by `/name` | When spawning a specialist for a task |
| Owner | The session itself | The RCCF Work Order |
| Interface | Claude Code skill loader | `.claude/agents/<id>.md` spawnable |
| Source | `.claude/skills/` (13 skills) | `core/rooms/*/agents/*.md` (105 agents) |
| Conflict | Skills do NOT replace agents | Agents do NOT replace skills |

**Skills are legitimate.** They are NOT a legacy artifact. The 13 core skills (boot/gate/handoff/team/delegate/reflect + audit/spec-review/feature/secure/fix/report/design-taste) are the discipline interface within a session. They are not "agents lite" — they are structured workflow routines.

**Role-wearing is legitimate.** Delegating to an agent via RCCF is the sanctioned way to distribute work. It is not "skill proliferation" — it is hierarchical flow made real.

The two never collide because they operate at different layers: skills structure *the session's own work*; role-wearing distributes *work to subagents*.

## The 13 core skills

Spine (6): boot · gate · handoff · team · delegate · reflect
Power (7): audit · spec-review · feature · secure · fix · report · design-taste

All live in `.claude/skills/`. No duplicates, no mirrors.

## Commands

≤15 curated commands in `.claude/commands/`. Shortcuts over `shamel` — no logic, just routing.

## Intake flow

```
raw human input → [translator] → structured JSON → CEO agent
```

The translator (semantic gateway) refines raw human intent into structured work: project, gate, agent, intent. The CEO then produces the RCCF Work Order and delegates.
