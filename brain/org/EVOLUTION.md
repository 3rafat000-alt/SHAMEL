---
title: EVOLUTION
owner: knw-lead
description: "Org evolution — structural changes, room creation, retirements"
generated: false
---

# SOFI EVOLUTION — framework improvement roadmap

> Teaching V (Continuous Metamorphosis). Improvements to the framework itself, triaged from
> external-review-desk critiques. Executed items link the commit; backlog items carry a priority +
> concrete first step. Large architectural changes are NOT auto-applied — they land here for
> deliberate staging (the review-desk loop's "break out for real scope change" exception).

## Round 1 — external review desk (Gemini), 2026-07-02

Pushed a full SOFI system description (team · gates · commands · routing · engine · brain · tooling ·
behaviors) and asked for a prioritized plan toward **frugal · economic · flexible**. Reply distilled
below. Source ask: `sofi gemini review` loop.

### ✅ Executed now (cheap, safe, reversible)

| Item | Where | Why |
|------|-------|-----|
| **Self-correction hard ceiling (3 attempts → escalate)** | `00-operating-system.md` §Escalation | fix→fail→refix loops burn tokens silently; hard cap is the single biggest cost leak plug |
| **Task-sizing: Fast-Track vs Deep-Audit** | `00-operating-system.md` §Escalation | trivial changes shouldn't traverse all 9 gates; money surfaces still take the full 9. Flexibility without weakening Tier-A |
| **Per-worktree build-cache isolation** | `git-discipline.md` §2 | parallel squads on one physical root corrupt shared `vendor/`/`.pub-cache`; export per-worktree cache dirs |

### 🗺 Backlog — deliberate implementation (priority-ordered)

1. **[HIGH] Differential context injection** — `lean_ctx_injector.py` at SessionStart builds a compact,
   target-scoped context per agent instead of passing whole `_context/*.md`. Est. −60% inter-agent
   context tokens. First step: prototype the injector reading the inbound ticket + only the DECISIONS
   entries tagged to the current feature.
2. **[HIGH] AST function-level truncation** — `sofi_scan.py` returns the target function body (via
   Python AST) not just `file:line`, so the model never reads the whole file. First step: add an
   `--extract` mode that emits the enclosing function/class for each hit.
3. **[HIGH] Self-correction & drift guards (partly done)** — the 3-attempt ceiling is live; still open:
   a **Context Lock** on `_context/` (require `git pull --rebase` + `sofi_verify` before any brain
   write) to kill the recurring shared-index race, and **brain divergence** protection at merge.
4. **[MED] Routing refinement** — shift file-reading/structure-scan from Sonnet→Haiku; render RCCF via
   Python templating + Haiku tone-pass instead of a Sonnet CEO call. Re-evaluate Fable→Sonnet+strict
   guards for spec-review gate (measure quality delta before committing — Fable gate exists for a
   reason; do NOT drop it blind).
5. **[MED] Runtime state in SQLite** — `.engine/state.db` as the fast read/write runtime; regenerate the
   human-readable `_context/*.md` only on checkpoint/close. Big change — needs a migration + a
   fallback; stage behind a flag. Note tension: markdown brain is the audit trail; DB must stay a
   cache, not the source of truth.
6. **[MED] Command consolidation** — desk proposes collapsing the 10 palette + ~25 dispatcher commands
   (e.g. `/sofi-pipeline`, `/sofi-squad`, `/sofi-close`). CAUTION: the tight 10-command palette was a
   deliberate anti-clutter decision; consolidate only where it removes real friction, measure
   wrong-command/arg-mismatch debug loops first.
7. **[MED] Cyclomatic-complexity / maintainability guard** — `sofi_scan.py` blocks merges that raise
   complexity even when tests pass (kills "green but spaghetti" debt).
8. **[MED, careful] Fail-CLOSED for Tier-1 security/money hooks** — desk flags fail-open as a risk on
   money surfaces. Tension: fail-open was chosen so a broken scanner never bricks a session. Proposed
   compromise: keep fail-open globally, but for edits under money/credential paths, a broken security
   scanner aborts THAT edit (not the session) + alerts. Needs careful scoping — do not flip globally.
9. **[STRUCTURAL] Cascading delegation** — CEO delegates to Tier-Heads, who generate sub-RCCF for their
   tier, shrinking CEO context. Large behavioral change to the org model; prototype with one tier
   (Tier-1) before rolling out.

### 🚨 Top risks the desk surfaced (all now tracked above)
- Infinite self-correction loops → **ceiling live** (#3).
- Context drift / brain divergence under parallel worktrees → Context Lock (#3).
- Silent technical-debt accumulation (green tests, bad code) → complexity guard (#7).

---

## Round 2 — GitHub research desk (13-agent sweep), 2026-07-07 · v6 mechanization

Source: `company/research/PATTERNS.md` — 13 parallel agents distilled 15 ranked patterns from the
most-recently-updated `claude` repositories. **Convergence finding:** independent projects
(cognitive-night, autonomous-work-harness, edict, molyanov, AgentHub, wshobson) all arrived at SOFI's
own `03-verification.md` / `04-reflection.md` doctrines. The v6 delta is therefore **mechanization**,
not new doctrine — turn prose laws into code that blocks, lints, budgets, and self-surfaces.

### ✅ Executed in the v6 rebuild
| Item | Where | Pattern |
|------|-------|---------|
| **Rooms replace tiers** — 15 self-contained departments, filesystem = org chart | `company/rooms/**`, `nexus/registry.yaml` | P1 (room-as-plugin), P15 |
| **Nexus staffed & addressable** — a Gateway room (6 operators) is the connecting layer, not prose | `company/rooms/14-gateway/`, `nexus/NEXUS.md` | P15, P3 |
| **Model tier stamped in every agent frontmatter** + single-source routing.yaml | `.claude/agents/*.md`, `nexus/routing.yaml` | P12 |
| **Least-privilege tool grants encode identity** — verifiers/reviewers get Read/Grep/Glob only | every `.claude/agents/*.md` | agent-def best practices |
| **Trigger-form descriptions as router keys** (progressive disclosure L1) | every agent/skill frontmatter | P2 |
| **Fresh-context gatekeeper owns gate advancement**, never the implementer | `gtw-gatekeeper`, `03-verification.md` | P5 |

### ✅ v6.1 mechanization — EXECUTED 2026-07-07 (all 10 items shipped)

Built as 9 isolated `sofi_tools` modules (parallel) + one integrator wiring CLI/hooks/gates/dashboard.
Verified: `sofi doctor` PASS (105↔105) · `py_compile` clean on all 20 files · every new verb exercised ·
every hook exits 0 on a project-less tree (fail-open, project-scoped) · telemetry captured live from this
session's own edits · `[LEARN]` capture confirmed end-to-end. Modules are **plumbing** — the rooms invoke
them; nothing runs a model on the write path.

| # | Item | Shipped as | Verb / wiring |
|---|------|-----------|---------------|
| 1 | Deterministic scheduler | `scheduler.py` (build/validate DAG, topo, ready-set, mermaid) | `sofi plan <PRJ> --file` → `_context/PLAN.dag.json`; `sofi run <PRJ> [--mark id:status]` |
| 2 | Fail-closed gate transitions | `transitions.py` (`_VALID_TRANSITIONS`, advance/rework/loopback/ILLEGAL_SKIP) | `sofi gate-check` prints the transition verdict; Stop hook gates project-scoped, fail-open, deadlock-capped |
| 3 | Spawner-level budgets | `budget.py` (Budget dataclass, `check_spawn`, heartbeat, 3-attempt circuit-breaker + crash-dump ledger) | reads `nexus/routing.yaml` effort_scaling/budgeted_autonomy |
| 4+6 | Harness-remembers brain pipeline | `memdb.py` (SQLite FTS5: capture · heading-indexed sections + SHA-256 drift · search→summaries · inject_digest ≤1k · compress_session · learn_match) | PostToolUse captures · SessionStart injects · `sofi recall <PRJ> --text` |
| 5 | LESSONS as managed cache | `lessons_cache.py` (confidence, decay 5%/wk, injection cap ≤6@0.7, occurrence-promotion, vaccine_for) | knw-reflector doctrine, UserPromptSubmit vaccine |
| 7 | Zero-cost acceptance router | `acceptance.py` (heuristic score, escalate@<0.80, override rules before classifier) | composes `routing.route_for` |
| 8 | Breadcrumb-JSON resume | `resume.py` (write/read breadcrumb, FRESH/DEGRADED/UNKNOWN classifier) | `sofi resume <PRJ> [TKT]` — DEGRADED exits non-zero |
| 9 | Config lint in CI | `agentlint.py` (frontmatter · 105↔105 parity · registry consistency · SHA-256 pins → `nexus/agent-pins.json`) | `sofi lint`; `.github/workflows/lint-agents.yml` |
| 10 | Fleet telemetry | `telemetry.py` + `event_server.py` (JSONL emit, best-effort POST, stdlib event server) | every hook emits; `sofi events`; dashboard `/api/events` + `/api/plan` |

New hook: `.claude/hooks/user_prompt_submit.py` (vaccine + `[LEARN]` capture) wired in `settings.json`.

### 🗺 Backlog — future rounds (priority-ordered, each a concrete room ticket)
1. **[MED] Wire the plumbing into the room playbooks.** The v6.1 modules exist and pass; now update the
   Gateway/Knowledge room playbooks so gtw-dispatcher actually calls `sofi plan/run`, gtw-budget-warden
   enforces `budget.check_spawn` per squad, and knw-reflector runs `lessons_cache` on gate-close.
2. **[MED] Dashboard live swimlanes.** Consume the new `/api/events` + `/api/plan` endpoints in the
   dashboard UI (per-session lanes from `telemetry`, DAG progress from `scheduler`).
3. **[LOW] Family-diverse verification.** Route gtw-gatekeeper's highest-stakes verdicts (money/auth/PII)
   through the oracle desk for a non-Claude second opinion (V2 judge-bias guard).
4. **[LOW] pass^k reliability harness.** A `sofi verify --k N` that re-runs a gate's critical-path check
   k times and blocks on any flake (V3), owned by qa-lead.

### 🚨 Anti-patterns the research flags (audit the org against these each gate-close)
LLM-as-coordinator · free-form inter-agent chat · self-graded completion · description-as-workflow-summary ·
whole-roster-in-context · transcript-passing handoffs · reactive auto-compaction · uncapped loops ·
budgets by self-discipline · trusting consensus among clones (multi-agent echo) · silent resume from stale
state · multiple writers to shared artifacts · untested agent configs · the frontier model routing itself ·
everything-persistent sessions.
