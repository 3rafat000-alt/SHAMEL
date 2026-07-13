---
title: DECISIONS
owner: knw-historian
description: "Architecture Decision Record log"
generated: false
---

# SOFI-AI Architectural Decisions & ADRs

## ADR-001: State-Hydration Boot Loop (Proven)
**Date:** 2026-06-15  
**Status:** ACTIVE  
**Decision:** Force `sofi sync <PRJ>` to read isolated git-backed `_context/` (STATE/CONTEXT/DECISIONS/HANDOFFS) before any agent executes.  
**Rationale:** Eliminates stateless amnesia; enables resumable multi-session work.  
**Outcome:** 60+ successful multi-session handoffs in PRJ-SAKK without context loss.

---

## ADR-002: Asymmetric Token Routing (routing.yaml v4.2)
**Date:** 2026-06-20  
**Status:** ACTIVE  
**Decision:** 80% haiku → 15% sonnet → 4% Fable → 1% Opus. Gatekeeper (Fable 5) hard-gates critical decisions (spec-review 7 steel rules).  
**Rationale:** Cost efficiency + quality preservation on arbitration.  
**Outcome:** Token burn ~60% lower than equivalent vanilla-agent approach.

---

## ADR-003: Blind Spot Filter (Context Reduction)
**Date:** 2026-06-22  
**Status:** SUPERSEDED (2026-07-03) — `lean-ctx` removed from the workspace  
**Decision:** Use `.claudeignore` for context window reduction.  
**Rationale:** Makes continuous local execution financially viable.  
**Outcome:** `.claudeignore` remains in use; the `lean-ctx` runtime was pulled out.

---

## ADR-004: 7 Steel Rules Spec-Review Gate
**Date:** 2026-06-25  
**Status:** ACTIVE  
**Decision:** /sofi-spec-review hard-gates (422-not-302, ApiException, /admin-in-503, unique-race, money-math, contract-parity, Tier-A ≥90%).  
**Rationale:** Catch money-safety + usability + security violations before merge.  
**Outcome:** Zero Tier-A regressions since implementation.

---

## ADR-005: Single Physical Projects Root + Per-Project Git Repos
**Date:** 2026-07-01  
**Status:** SUPERSEDED by ADR-008 (2026-07-03)  
**Decision:** Kill symlink at Lorka/projects. One real root ~/Desktop/projects/. Each PRJ-XXXX = own git repo + isolated brain (_context/).  
**Rationale:** Prevent cross-project bleed; clean git history per project.  
**Outcome:** Caddy docroots fixed (symlink→physical). Clear project isolation.

---

## ADR-006: SOFI-AI Architectural Hardening (Gemini Audit 2026-07-02)
**Date:** 2026-07-02  
**Status:** REMEDIATION IN PROGRESS  
**Decision:** Address 3 critical vulnerabilities identified in Gemini architectural audit:
1. **Semantic Drift Telephone Effect** → Triple-Contract Check in handoff protocol
2. **Port Collision & Environment Bleed** → Per-project port ranges + Caddy teardown + resource locks
3. **Fable-5 Lockout Loop** → Pre-flight Sonnet 5 classification + circuit breaker tuning

**Rationale:** Ensure multi-agent coordination remains bulletproof at scale. Prevent business logic loss across handoff chains. Isolate parallel squad execution.  
**Timeline:** 13 days (3 weeks parallel squads)  
**Phase 1:** Handoff integrity (Days 1–2)  
**Phase 2:** Resource isolation (Days 3–5)  
**Phase 3:** Gatekeeper hardening (Days 6–8)  
**Phase 4:** Exfiltration guard (Day 9)  
**Phase 5:** Observe loop (Days 10–11)  
**Phase 6:** Orchestration v2 (Days 12–13)  

**Success Metrics:**
- Handoff semantic drift incidents: 0 per 50 tickets (baseline: 2–3)
- Cross-project test failures: 0% (baseline: 15%)
- Spec-review arbitration loops (avg): 1.2 attempts (baseline: 3.1)
- Exfiltration incidents: 0 detected

**Owner:** CEO (Tier-0) + sofi-backend-tech-lead (Phase 2–3) + sofi-security-compliance-architect (Phase 4)  
**Dependencies:** None. All 6 phases can run in parallel (separate squads per phase).

---

## ADR-007: Gemini-Loop Teaching VII (4-Layer Enforcement)
**Date:** 2026-07-02  
**Status:** ACTIVE  
**Decision:** Autonomous Gemini loop with 4-layer runtime enforcement:
1. **Output Guard** (Critical) — Agent output interceptor validates no unsafe state mutations
2. **Circuit Breaker** (High) — Escalation on repeated failures
3. **Context Pruning** (Medium) — Strip sensitive data before external review desk push
4. **Pre-flight Hydration** (Operational) — Mandate state hydration before agent spawn

**Rationale:** Prevent runaway autonomous loops; enforce guardrails at runtime.  
**Outcome:** Teaching VII autonomous loop validated; safe for production.

---

## ADR-008: Projects Root Moved In-Repo (supersedes ADR-005)
**Date:** 2026-07-03  
**Status:** ACTIVE  
**Decision:** Moved physical projects root from `~/Desktop/projects/` to `~/Desktop/Lorka/projects/`, at explicit user request despite the 2026-07-01 incident that prompted ADR-005 (in-repo location broke every Caddy docroot). Each `PRJ-XXXX/` remains its own separate git repo, gitignored from Lorka's own history. Updated on the move: crontab (`PRJ-SAKK` schedule:run cwd), `.sofi-run/caddy/sites/{PRJ-SYRH,zanjour}.caddy` docroots (validated + reload pending manual `sudo systemctl reload caddy`, blocked for agents), and hardcoded literal-path fallbacks in `caddy_isolation.py`, `squad_orchestrator_v2.py`, `gemini-github-sync.py`, `observe_sentry_loop.py`, `ooda/engine/config.yaml`, `.claude/settings.local.json` that bypassed `sofi_tools.paths.projects_dir()`.  
**Rationale:** `paths.projects_dir()` already tolerates this (env override → `~/Desktop/projects` if present → in-repo fallback), so the *designed* resolution path was never actually broken — only the files hardcoding a literal string outside that function were. User-directed change; risk was disclosed and accepted.  
**Outcome:** pending — Caddy config validated but daemon reload requires manual sudo.

---

## ADR-009: SOFI v5.0 — The Integrity & Intelligence Layer
**Date:** 2026-07-03
**Status:** ACTIVE
**Decision:** Add a grounding + verification + self-improvement layer on top of the v4 structure, rather than rebuilding the structure. Six deep frontier-research sweeps (`.claude/docs/ai-guides/research/`: orchestration, context/memory, grounding, self-improvement, verification, spec-design — each cited to Anthropic engineering + arXiv 2025-2026) independently **validated v4's 5-tier/Advisor-gateway/gate-lifecycle/git-brain structure as correct** for a compliance-oriented gated SDLC, and flagged the alternatives (peer-to-peer mesh, vector-DB memory, 50-agent fan-out, trained verifier models) as over-engineering for SOFI's shape. So v5 is additive. Six components: **C1 Grounding** (`grounding.md` + universal-contract hooks + RCCF clause) — cite-or-abstain, execution-truth, verified-vs-inferred, conflict-surfacing; **C2 Reflection** (`reflection_engine.py` + `reflection.md` + `/sofi-reflect`) — scheduled "dreaming" distilling HANDOFFS→LESSONS.md, retain-by-default, never per-turn; **C3 Structured brain** (`tickets.py` query + `sofi brain-query` + memory-type frontmatter in `context-and-memory.md`); **C4 Verification** (`verification.md` + `gates.validate_evidence()` wired into `gate-check` + spec-review UNKNOWN verdict + `/sofi-secure` adversarial pass); **C5 Budgeted autonomy** (`routing.yaml` `effort_scaling`+`budgeted_autonomy` + verbatim-forwarding in handoff); **C6 RCCF v2** (clarify-before-commit, frozen brief, evidence block, effort class).
**Rationale:** The research verdict was consistent and cited: v4 got the org *structure* right; what it lacked was the integrity layer (agents couldn't be stopped from hallucinating unchecked or self-reporting success) and the intelligence layer (the org didn't learn from its own history). That's the genuine, grounded "radical development" — not a teardown of validated work.
**Outcome:** All new Python compiles; routing/registry YAML valid; `sofi doctor` PASS (30 agents unchanged); evidence-check + brain-query + reflection-engine dry-run all verified against real project data. Framework-only change — no project code touched, tier-isolation + git-discipline preserved. Design record: `.claude/docs/v5/SOFI-V5-ARCHITECTURE.md`.

---

## ADR-010: Git Reconciliation — `origin/main` as Sole Lineage (SHAMEL Phase 1)
**Date:** 2026-07-10
**Status:** ACTIVE
**Decision:** Lorka had three diverging git truths: `origin/main` (9 commits ahead of the others — the full v6 scaffold: 105 agents, Nexus, Constitution, Brain, merged via PR #10 / ADR context), local `main` (9 commits ahead of `origin/main`, all pre-v6 n8n/WhatsApp orchestration build-out later torn down on the other branch), and `prj/PRJ-SAKK` (23 commits ahead of `origin/main`, superset of local `main`'s commits plus the n8n teardown itself, plus four more: `8777cf8` intake-orchestration doctrine, `9a439ce` removal of `/sofi-*` slash commands, `4b4d9ed` port of the full OpenCode enterprise into a native `.claude/` (creating a second, stub-quality `.claude/agents/` — 105 files in 15 room-folders, `model: inherit`, no tools — coexisting with `origin/main`'s mature flat RCCF `.claude/agents/*.md`), and `483d355` a small fix on top of that port. **`origin/main` is adopted as the sole reference lineage.** Its git history is NOT rewritten to absorb the other two branches' commit history — investigation (SHAMEL Phase 0/1 audit) found nothing in `main` or `prj/PRJ-SAKK` uniquely valuable enough to justify reviving the pre-v6 `engine/` tree or the OpenCode-port `.claude/agents` duplicate; everything genuinely unique was already captured, out-of-band, in Phase 0: `rescue/g6-main` (the live orchestrator fork), `rescue/g1-assets` (114 OpenCode tool scripts + browser-eyes + gate checklists), `rescue/stash-teardown`, `rescue/main-misc`. The one piece of real **doctrine** value — the intake-orchestration "wear-the-hierarchy" flat-topology flow (`8777cf8`) — is not merged as-is (it lives in the now-superseded `engine/protocols/` tree); it is carried forward *conceptually* into `company/constitution/11-intake-orchestration.md`, to be authored fresh against v6's structure (SHAMEL `ARCHITECTURE.md` §2.4, Phase 2 of `MASTER-PLAN.md`).
**Rationale:** A destructive rebase/force-merge of already-diverged, partly-obsolete history is higher-risk than a clean adopt-and-supersede; the rescue branches preserve every byte for retrieval without carrying dead weight (duplicate `.claude/agents`, torn-down n8n orchestration) into the reference lineage. This matches SHAMEL's Phase 1 goal ("one lineage, one constitution") without reopening GAP-02/GAP-08 by literally merging the duplicate `.claude/agents/` tree back in.
**Outcome:** `origin/main` independently verified already healthy on the concrete Phase 1 acceptance bars: zero `engine/tooling` dead references in `.claude/settings.json`, exactly one root `MEMORY.md` (96 lines, <200 per FR-14) within `find -maxdepth 2`, exactly one `CLAUDE.md`, 9 pre-existing ADRs. Remaining open item, deliberately left to a human step rather than an unattended branch switch: Lorka MAIN's own live checkout (`~/Desktop/Lorka`) is still sitting on `prj/PRJ-SAKK` @ `483d355` and lacks `company/`, `org-rooms/`, `tools/` in its working tree — moving it onto `origin/main` (or this `reconcile/unify` branch) changes the active working directory of a session that may have other uncommitted work in flight, so it is not done automatically here. Local branches `main` and `prj/PRJ-SAKK` are left intact (not deleted) pending that move; both are recorded superseded by this ADR, not their history.

---

## ADR-011: PRJ-SAKK Second Git-History Loss — Rescue Adopted, Two Items Deferred to Owner
**Date:** 2026-07-10
**Status:** ACTIVE (rescue resolved; 2 backlog items below explicitly await an owner decision, not decided here)
**Decision:** `projects/PRJ-SAKK`'s git history (root commit `cc8cf82` through `8db4745`, ~40 commits spanning the whole Admin UI Unification initiative per its own `_context/STATE.md`) is confirmed unrecoverable — `git cat-file -t` fails for every SHA `_context/STATE.md` cites, in both known checkouts (`SHAMEL/projects/PRJ-SAKK` and `~/Desktop/Lorka/projects/PRJ-SAKK`), and each was independently re-inited with a different root commit (`c7390c1` vs `881f75b` — siblings, not shared history). This is a second, separate loss on top of the already-documented 2026-07-04 Trash incident (recovered that time; root cause of *this* loss not diagnosed — out of scope for this pass). Per **ADR-005/ADR-008** (per-project git repos, independent of the SHAMEL/Lorka meta-repo lineage), the fix is scoped to PRJ-SAKK's own repo only: **`c7390c1` is adopted as the sole lineage for the SHAMEL checkout**, going forward on branch `worktree-prj-sakk-gate-progress` (4 new commits: 3 defect fixes + 1 STATE.md doc update, all pushed to the only remote that exists — a **local-only bare mirror** `rescue-mirror`; there is no GitHub remote for this project, so no PR is possible, by design of the per-project-repo model, not an oversight). `_context/STATE.md`'s historical LATEST-log entries are kept as-is (file-level outcomes they describe were independently verified still true in the working tree) but flagged with a notice that their SHAs no longer resolve.
- **Two items surfaced during this pass are explicitly NOT decided here — flagged for the project owner, per this session's own instruction not to unilaterally resolve design/deletion calls:**
  1. **Dead-file cleanup (STATE.md backlog "G7/G8"):** investigation-only pass found ~15 files as HIGH-to-VERY-HIGH-confidence dead (zero references) — most notably `backend/public/sakk-admin/admin.js.orphaned` (1,629L, self-marked dead by filename) and `admin.css.bak` (2,360L), 5 orphaned dashboard partials, 3 superseded sort-link partials, 4 duplicate filter/KPI-grid partials, and 2 stray Claude-Code hook-log files that leaked into the tree from the original SOFI-ENGINEERING import (`resources/views/errors/.claude/memory/hooks/*.jsonl`) — plus a lower-confidence item (`backend/css-audit.php` + report, misplaced tooling, not clearly dead). Full list with per-file confidence and reasoning: this session's PRJ-SAKK worktree transcript (`worktree-prj-sakk-gate-progress`) and `_context/STATE.md`'s 2026-07-10 LATEST entry. **Nothing was deleted.**
  2. **Brand-color token gaps (STATE.md backlog "cosmetic token gaps"):** investigation-only pass found 8 concrete gaps, most notably `.badge-gold` being silently overridden by a duplicate later CSS rule (renders wine/burgundy instead of gold on ~9 live views today — a real, live visual bug, not just a gap) and `.badge-primary`/`.badge-secondary` referencing undefined CSS custom properties. Full detail in the same transcript/STATE.md entry. **Nothing was changed.**
**Rationale:** Re-diagnosing or reconstructing lost history has no reliable source (no GitHub remote ever existed to fall back on; the two independent re-inits confirm both known local copies already lost it before today). Continuing forward from a clean, verified-working single-commit baseline — after actually fixing the 3 live defects and confirming 1148/1148 tests green — is lower-risk than any reconstruction attempt. File deletion and cross-cutting color-token changes are exactly the class of decision this org's own G7/G8 note and cosmetic-token backlog entry already flagged as "needs a design decision, not a bug fix" — deferring them here is consistent with that standing call, not a new one.
**Outcome:** PRJ-SAKK backend: 1148/1148 tests passing (was 1142/6 this morning), 0 new PHPStan errors, 0 new security findings (`sec-appsec-engineer` + `sec-secrets-warden` reviewed the full diff), 4 commits pushed to `rescue-mirror`. One pre-existing, not-currently-exploitable hardening item surfaced but not fixed (unescaped `$currency` fallback in `App\Support\Money::symbol()`) — new backlog, no live write path reaches it today. Owner decision still needed on items 1–2 above before closing this ADR's open items.

---

## Future ADRs (Backlog)
- **ADR-012:** Sidecar observability (Sentry → DECISIONS.md feedback loop) — Gate 8 integration
- **ADR-013:** Parallel squad orchestration v2 — Dynamic resource binding + auto-cleanup
- **ADR-014:** Cross-project audit tooling — Automated compliance checks across all PRJ-* repos

