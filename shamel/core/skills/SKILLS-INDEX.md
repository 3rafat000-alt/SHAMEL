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

## Stack Rules — Auto-Attach by Path (3-Tier: common → language → framework)

| Tier | File | Extends | Paths (auto-attach) |
|------|------|---------|----------------------|
| common | `rules/common/coding-style.md`, `security.md`, `testing.md` | — | all projects |
| php | `rules/php/coding-style.md`, `security.md`, `testing.md`, `patterns.md` | `common/*` | `projects/PRJ-SAKK/backend/**/*.php`, `**/composer.{json,lock}` |
| laravel | `rules/laravel/patterns.md`, `security.md` | `php/*` | `app/Http/Controllers/**`, `routes/**`, `database/migrations/**` |
| dart | `rules/dart/coding-style.md`, `security.md`, `testing.md`, `patterns.md` | `common/*` | `projects/PRJ-SAKK/mobile/**/*.dart`, `**/pubspec.yaml` |
| flutter | `rules/flutter/patterns.md`, `security.md` | `dart/*` | `lib/**` (widget/state layer) |

Unlike the flat `strict-*.md` skills (agent-invoked, no auto-attach), `rules/**/*.md` files carry a `paths:` frontmatter glob and are meant to load automatically for `bck-*`/`mob-*` agents touching matching files. Assigned rooms: `bck-*` for php/laravel, `mob-*` for dart/flutter, both extending `common/*` for language-agnostic baseline (coding style, security, testing). Cross-reference, don't duplicate, the dedicated `ccpayment-integration`, `stripe-issuing-integration`, and `testsprite-testing` skills for PRJ-SAKK-specific integration detail.

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

## Adding New Stack Rules

1. Create file `rules/<tier>/<topic>.md` (tier = common/php/laravel/dart/flutter, or a new language/framework tier)
2. Frontmatter: `name`, `description`, `paths:` (glob list for auto-attach)
3. Language tiers extend `common/*`; framework tiers extend their language tier — state this in the opening line
4. Add a row to the Stack Rules table above
5. Keep under 60 lines, matching Token Economy law
