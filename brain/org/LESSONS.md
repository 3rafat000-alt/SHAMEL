---
type: brain
description: Distilled lessons from retrospectives
owner: knw-reflector
mem: procedural
scope: org
---
# LESSONS — org-level procedural memory

> Company-wide lessons distilled from v5 operating history (`company/brain/org/DECISIONS.md`, `EVOLUTION.md`, `archive-v5/`).
> Format per `company/brain/templates/LESSONS.md`; idempotent on `sig:`. Written by knw-reflector via `/sofi-reflect`; read by every agent once per session (`/sofi-boot`).
> Rules here bind like doctrine footnotes: they explain WHY the constitution says what it says.

## LES-001
- **sig:** blind-start-amnesia
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Early multi-session work on PRJ-SAKK: agents resumed from model memory instead of recorded state, re-deciding settled questions and losing thread across sessions.
- **what_failed:** Stateless boots — no forced hydration from the git-backed brain before acting.
- **rule:** No agent acts before `sofi sync <PRJ>` + reading `_context/STATE.md` (branch · head_sha) and its ticket in `HANDOFFS.md`. State-hydration produced 60+ clean multi-session handoffs once enforced.
- **source:** ADR-001, company/brain/org/DECISIONS.md

## LES-002
- **sig:** self-correction-loop
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Agents caught in fix→fail→refix cycles burned tokens silently — the single biggest cost leak the external review desk found in v5.
- **what_failed:** No ceiling on self-correction; failure looked like diligence.
- **rule:** Three self-correction attempts maximum; the 4th failure = HALT + structured crash-dump JSON + escalation ticket (`sofi escalate`). The circuit breaker is not optional (constitution/00-operating-system.md).
- **source:** EVOLUTION.md Round 1 "Executed now" · company/brain/org/EVOLUTION.md

## LES-003
- **sig:** handoff-semantic-drift
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** The 2026-07-02 architectural audit measured 2–3 semantic-drift incidents per 50 tickets: business logic degraded across handoff chains like a telephone game, each relay re-phrasing the finding.
- **what_failed:** Gateways summarizing and re-authoring findings in flight — the translation tax.
- **rule:** Leads forward findings VERBATIM across room boundaries — citations and evidence intact; leads route and gate, never re-author (constitution/08-handoff-law.md, `company/nexus/NEXUS.md`).
- **source:** ADR-006 §1, company/brain/org/DECISIONS.md

## LES-004
- **sig:** parallel-resource-bleed
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Parallel squads at gates 4–5 collided: port clashes between projects, ~15% cross-project test failures, and shared `vendor/`/build caches corrupted across worktrees on one physical root.
- **what_failed:** Parallelism without resource isolation — shared ports, shared caches, no locks.
- **rule:** Parallel work runs behind per-project port ranges (`sofi domain`), per-worktree build caches, and claimed paths in `LOCKS.md` (`sofi claim`/`release`). Fan out only behind a FROZEN input; never fan out sequential phases of one ticket.
- **source:** ADR-006 §2 + EVOLUTION.md Round 1 (per-worktree cache isolation), company/brain/org/DECISIONS.md

## LES-005
- **sig:** gatekeeper-lockout-loop
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Spec-review arbitration averaged 3.1 attempts per verdict: work reached the gatekeeper tier unclassified and bounced repeatedly (the "Fable-5 lockout loop").
- **what_failed:** Sending raw, unscanned work straight to the most expensive judge.
- **rule:** Two-phase always: mechanical/workhorse scan + SEV draft FIRST, then one full-context handover to the gatekeeper for the hard gate. Pre-flight classification before any gatekeeper spawn (v6: gtw-router assigns, `nexus/routing.yaml` is the only source).
- **source:** ADR-006 §3, company/brain/org/DECISIONS.md

## LES-006
- **sig:** hardcoded-path-bypass
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Moving the projects root (2026-07-03) broke crontab entries, Caddy docroots, and six scripts — every breakage was a literal path string bypassing `sofi_tools.paths.projects_dir()`. The designed resolution path itself never broke.
- **what_failed:** Hardcoded literals scattered outside the one path-resolving function; same failure class as v5's `ROLE_TIER`/`GATE_ROLES`/30-agent hardcodes lagging their YAML sources.
- **rule:** One source of truth per fact, resolved through one function: paths via `sofi_tools.paths`, routes via `nexus/routing.yaml`, roles via `nexus/registry.yaml`, gates via `nexus/gates.yaml`. A hardcoded copy of registry data is a defect — `sofi doctor` checks parity (105↔105).
- **source:** ADR-008 + BLUEPRINT §6 debt list, company/brain/org/DECISIONS.md

## LES-007
- **sig:** gate-overkill-trivial
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Trivial changes (copy edits, i18n strings, a non-money field) were traversing all 9 gates, spending gatekeeper-tier attention on zero-risk work.
- **what_failed:** One-size lifecycle — flexibility confused with weakening the bar.
- **rule:** Two-track sizing: Fast-Track (low-risk) collapses gates 1–3 into one blueprint check → prod on green tests; Deep-Audit (money/credentials/auth/PII) = full 9 gates, no exception. Unsure → Deep-Audit (constitution/10-lifecycle-gates.md).
- **source:** EVOLUTION.md Round 1 "Executed now", company/brain/org/EVOLUTION.md

## LES-008
- **sig:** self-graded-gate
- **mem:** procedural
- **date:** 2026-07-07
- **situation:** Before v5's integrity layer, implementers reported "done" and gates advanced on that self-report; hallucinated success passed unchecked until downstream breakage exposed it.
- **what_failed:** Outcome conflated with self-report; the grader was the implementer.
- **rule:** A gate advances only on a fresh-context adversarial check against the ORIGINAL criteria (v6: gtw-gatekeeper — never the implementer) plus mechanical evidence (`validate_evidence`, fail-closed, in `sofi gate-check`). Self-report ≠ evidence (constitution/03-verification.md V1–V2).
- **source:** ADR-009 C1+C4, company/brain/org/DECISIONS.md


<!-- Sig format: LES-NNN·sig·situation·what_failed·rule·source:TKT/SHA -->
