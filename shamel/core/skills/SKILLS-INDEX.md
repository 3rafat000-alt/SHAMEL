# مهارات | SHAMEL Skills Index

| Skill | File | Purpose | Agent assignment |
|-------|------|---------|------------------|
| Code Review | `strict-code-review.md` | Systematic code review: security, correctness, maintainability | `fnt-*`, `bck-*`, `arc-*`, `sec-*` |
| Research | `strict-research.md` | Web research with query crafting, source scoring, synthesis | `res-*`, `str-*`, `any agent needing external data` |
| Analysis | `strict-analysis.md` | Data/system/requirements analysis with frameworks and recommendations | `arc-*`, `str-*`, `dat-*` |
| Communication | `strict-communication.md` | Agent-agent and agent-user structured messaging | **ALL agents** (base skill) |
| Planning | `strict-planning.md` | Task decomposition, estimation, dependency mapping, risk | `str-*`, `arc-*`, `lead agents` |
| Memory | `strict-memory.md` | Brain system usage: HIPPOCAMPUS, CORTEX, AMYGDALA | **ALL agents** (base skill) |
| Tools | `strict-tools.md` | Correct SHAMEL tooling: selection, chaining, error handling | **ALL agents** (base skill) |

## Load Order — Recommended Stack

1. **Communication** (base layer — how to speak)
2. **Tools** (base layer — how to act)
3. **Memory** (base layer — how to remember)
4. **Planning** (before executing work)
5. **Research** (when external info needed)
6. **Analysis** (when evaluating options)
7. **Code Review** (before landing code)

## Activation Rules

- **Base skills** (Communication, Tools, Memory) — load automatically on agent init
- **Task skills** (Planning, Research, Analysis, Code Review) — load on demand based on task type
- Agent names with prefix `ALL` get all skills loaded

## Adding New Skills

1. Create file `strict-<name>.md` in `core/skills/`
2. Add entry to this index with purpose and agent assignment
3. Skills must start with `## | [Arabic title] | [English title]` header
4. Keep under 60 lines; use checklists, tables, and templates
