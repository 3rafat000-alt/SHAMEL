# BRAIN — Memory Architecture (3 layers)

## Layers

| Layer | Location | Writer | Enforcement |
|-------|----------|--------|-------------|
| **Org** | `brain/org/` (DECISIONS · LESSONS · EVOLUTION · PERSONAS · TEAM_STATUS) | knw-* + ADRs by CEO | LESSONS with sig (`LES-NNN·sig:...`) — idempotent, injected as vaccine via UserPromptSubmit hook |
| **Project** | `projects/<PRJ>/_context/` — inside project repo | Agents via universal contract | `shamel checkpoint` commits brain with code in same repo |
| **Session** | `brain/db/` (brain.db FTS5 · sessions.jsonl) | Hooks automatically | PostToolUse/Stop write observations |

## Org brain files

- `brain/org/DECISIONS.md` — Architectural Decision Records
- `brain/org/LESSONS.md` — Distilled procedural lessons (sig format)
- `brain/org/EVOLUTION.md` — System evolution log
- `brain/org/PERSONAS.yaml` — Persona mapping table (agent-id ↔ persona-name)
- `brain/org/TEAM_STATUS.md` — Team status (generated)

## Memory rules

- `MEMORY.md` = pointers only (routing map). Never store content here.
- "Remember" (تذكّر) = sole trigger for durable doctrine writes (this file, MEMORY.md, harness memory).
- Every number in the brain is **generated** (`shamel brain counts`) — no manual entry (P2).
- Reflection is **scheduled**, not per-turn (Article 04).
- Doctor detects STATE↔CONTEXT↔code contradictions.

## Templates

Located in `brain/templates/`:
- `STATE.md` — branch, head_sha, gate, facts (generated counts)
- `CONTEXT.md` — session context
- `DECISIONS.md` — ADR template
- `HANDOFFS.md` — ticket queue
- `LESSONS.md` — procedural memory (sig format)
- `FOUNDATIONS.md` — design foundations
