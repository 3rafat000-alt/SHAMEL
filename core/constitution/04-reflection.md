# Article 04 — Reflection (scheduled dreaming)

Foundation: serves Teaching V (Continuous Metamorphosis). Read `core/CONSTITUTION.md` and `brain/BRAIN.md` first.

## Three hard rules

1. **Scheduled, never per-turn.** Runs at gate-close or on demand (`shamel reflect`), never inside a working turn.
2. **Retain by default, consolidate deliberately.** Never overwrite raw history. Only add distilled lessons not already distilled (dedup by sig).
3. **Distil to a lesson, not a re-summary.** `situation · what-failed · rule` in one line.

## The loop

1. **Locate — 0 model tokens.** Python finds NEW learning candidates (escalations, circuit-breaker trips, rejected tickets, ≥3× recurrences).
2. **Distil — model judgment.** One grounded lesson per candidate. Cite source (G1).
3. **Write — idempotent on sig.** Append to `projects/<PRJ>/_context/LESSONS.md` as `## LES-NNN`.
4. **Promote — optional, gated.** If reusable pattern → propose lifting to agent spec, WO template, or registry power.
5. **Feed forward.** `LESSONS.md` read on boot alongside the brain.

## What reflection does NOT do

- Does not auto-rewrite doctrine or specs. Proposes; CEO decides.
- Does not build a vector store. Grep + frontmatter is sufficient.
- Does not run inside a specialist's turn.
