---
title: HANDOFFS
owner: gtw-dispatcher
description: "Cross-room handoff index"
generated: false
---

# SOFI-AI Handoffs (Architectural Phase Queue)

## Current Cycle: ADR-006 Hardening Roadmap Execution
**Gemini Audit Complete:** 2026-07-02  
**Verdict:** High Maturity (Tier-1 Elite) with 3 critical vulnerabilities  
**Status:** Remediation In Progress (6 parallel phases, 13 days total)

---

## Phase 1: Handoff Integrity (Days 1–2)
**Owner:** sofi-principal-system-architect  
**Task:** Carve Triple-Contract Check into handoff protocol; update sofi CLI validator

### Deliverables:
1. Update `engine/protocols/04-handoff-interconnect.md`
   - Add Triple-Contract Check schema (UX trace + contract parity + immutability ADR)
   - Document rationale: prevent semantic drift Telephone effect
   
2. Extend `engine/tooling/bin/sofi checkpoint` 
   - Validate every handoff includes contract check block before accepting commit
   - Error message if validation fails (guide user to add schema)

3. Backfill: Run retrospective on 10 recent PRJ-SAKK handoffs
   - Append contract validation blocks
   - Verify no semantic drift occurred (compare original spec vs. final code)

4. Test: Create mock handoff with missing contract check → verify sofi checkpoint rejects it

### Success Criteria:
- [ ] Protocol document reviewed + merged
- [ ] sofi checkpoint validates + rejects invalid handoffs
- [ ] 10 backfilled handoffs passed validation
- [ ] Mock test passes (rejection on missing schema)

---

## Phase 2: Resource Isolation (Days 3–5)
**Owner:** sofi-devops-cloud-lead  
**Task:** Port ranges, Caddy teardown, resource-binding lock for parallel squads

### Deliverables:
1. Expand `engine/protocols/local-domains.md`
   - Define per-project port ranges (PRJ-SAKK: 8000–8099, PRJ-SYRH: 8100–8199, etc.)
   - Caddy auto-teardown on squad completion (hook in sofi dispatch)
   - XFH (X-Forwarded-Host) validation rules per tunnel host

2. Build resource-binding lock in `engine/tooling/bin/sofi dispatch`
   - Acquire port:database pairing lock before squad execution
   - Detect collision; fail with clear error message
   - Release lock on squad completion or 4-hour timeout

3. Caddy automation (`engine/tooling/agents/devops/caddy_isolation.py`)
   - Auto-generate per-project Caddy configs (subdomains, ports)
   - Teardown script: remove Caddy entries on squad exit

4. Integration test: Parallel PRJ-SAKK + PRJ-SYRH runs
   - Both squads launch simultaneously
   - Verify zero port collisions, zero DB cross-contamination
   - Both complete successfully, Caddy subdomains torn down

### Success Criteria:
- [ ] Protocol updated + reviewed
- [ ] sofi dispatch --squad acquires/releases locks
- [ ] Caddy automation in place
- [ ] Integration test passes (parallel squads, zero collision)

---

## Phase 3: Gatekeeper Hardening (Days 6–8)
**Owner:** sofi-ceo (orchestration) + sofi-backend-tech-lead (Sonnet 5 classifier)  
**Task:** Pre-flight error classification, circuit breaker tuning, verdict caching

### Deliverables:
1. Pre-flight Sonnet 5 Classifier
   - When spec-review fails, route error to cheap Sonnet 5 first
   - Classify root cause: Tier-0 (design) vs Tier-1 (contract) vs Tier-2+ (execution)
   - Feed classification to escalation router (don't auto-retry on design/contract failures)

2. Circuit Breaker Tuning
   - Current: 4 attempts before escalation
   - New: 2 attempts on same finding → escalate classification to CEO (not retry)
   - Log each attempt + classification in `_context/DECISIONS.md`

3. Verdict Caching (`engine/tooling/agents/ceo/spec_review_cache.py`)
   - Store prior spec-review verdicts by feature ID + preconditions hash
   - Reuse cached verdict if identical preconditions, skip Fable 5 call
   - Invalidate cache on: protocol change, new steel rule, architecture shift

4. Test: Intentional spec-review violations
   - Inject 422-to-302, ApiException missing, invalid money-math
   - Verify each routes to correct tier + escalation path
   - Measure: avg spec-review attempts (target: 1.2, baseline: 3.1)

### Success Criteria:
- [ ] Sonnet 5 classifier implemented + tested
- [ ] Circuit breaker tuning in place (2 attempts → escalate)
- [ ] Verdict caching reduces spec-review calls by 40%+
- [ ] Test suite passes (all violations route correctly)

---

## Phase 4: Exfiltration Guard (Day 9)
**Owner:** sofi-security-compliance-architect  
**Task:** Regex scrubbing layer in gemini_bridge.py (strip DB hashes, tokens, keys)

### Deliverables:
1. Automated Regex Scrubbing Layer (`engine/tooling/agents/ceo/sanitize_gemini_payload.py`)
   - Strip patterns: DB hashes, Caddy auth tokens, API keys, SSH keys, .env values
   - Whitelist: code structure, logic, error messages, architectural patterns
   - Log what was redacted (separate audit trail)

2. Integration into `gemini_bridge.py`
   - Every report push goes through sanitizer before external transmission
   - Fail-open: if sanitizer errors, escalate to CEO (don't silently skip)
   - Document all redaction rules in `engine/protocols/external-review-desk.md`

3. Automated Unit Tests
   - Push mock secrets (DB password, API key, SSH key, .env) → verify redaction
   - Push legitimate code → verify unchanged
   - Push mixed (code + secret) → verify secret redacted, code intact

4. Audit Trail
   - Log all external pushes + what was redacted to `_context/REDACTIONS.log`
   - Periodic review (monthly) for patterns of near-misses

### Success Criteria:
- [ ] Sanitizer implemented + tested
- [ ] Unit tests pass (100% mock-secret redaction)
- [ ] gemini_bridge.py wired + live
- [ ] External review desk pushes contain zero secrets (audit trail review)

---

## Phase 5: Observe Loop (Days 10–11)
**Owner:** sofi-observability-sre  
**Task:** Gate 8 automated feedback hook: Sentry → `_context/DECISIONS.md`

### Deliverables:
1. Gate 8 Feedback Hook (`engine/tooling/agents/tier-4-infrastructure/observe_sentry_loop.py`)
   - Poll Sentry for high-frequency exceptions (query: last 24h, error rate >threshold)
   - Classify root cause (data constraint, API contract, user input)
   - Write to `_context/DECISIONS.md` with timestamp + evidence link

2. Automated Anomaly Classification
   - Categorize: business logic (needs design review) vs. data validation (needs schema update) vs. perf (needs optimization)
   - Route to appropriate tier for remediation decision

3. Backfill: 30 Recent Project Decisions
   - Scan PRJ-SAKK past month (7 ADRs/major decisions)
   - Retroactively annotate with runtime-observed constraints from Sentry
   - Example: "ADR-003 gold auto-sync precision" + observed: "exchange rate rounding loses $0.01 on large conversions"

4. Integration Test
   - Inject test exception in staging
   - Verify: exception appears in Sentry → Gate 8 hook processes → decision logged in _context/DECISIONS.md within 10 min

### Success Criteria:
- [ ] Observe loop implemented + live
- [ ] Anomaly classification working
- [ ] 30 backfilled decisions annotated with runtime constraints
- [ ] Integration test passes (<10 min latency)

---

## Phase 6: Orchestration v2 (Days 12–13)
**Owner:** sofi-ceo (architecture) + sofi-backend-tech-lead (implementation)  
**Task:** Dynamic resource binding + orchestration for 3-way concurrent squads

### Deliverables:
1. Resource Manifest (`engine/tooling/bin/sofi dispatch --squad`)
   - Create manifest.json per squad: port, DB socket, tunnel host, lock state
   - Query existing manifests before execution
   - Fail if collision detected; guide user to wait or kill stale squad

2. Orchestration v2 (`engine/tooling/agents/ceo/squad_orchestrator_v2.py`)
   - `sofi dispatch --squad <PRJ> <AGENTS>` acquires locks, validates no collision
   - Parallel squad runs: monitor manifests in real-time
   - On completion/failure: `sofi dispatch --cleanup <SQUAD_ID>` releases locks + tears down resources

3. Timeout Guard
   - Orphaned locks auto-release after 4 hours (stale squad detection)
   - Slack notification: "Squad ABC stale for 4h, releasing resources"
   - Manual unlock: `sofi dispatch --force-unlock <SQUAD_ID>` (CEO only, logs audit trail)

4. Integration Test: 3-Way Concurrent Squads
   - Launch PRJ-SAKK (backend build), PRJ-SYRH (mobile build), local test suite simultaneously
   - Monitor: zero cross-contamination, all complete successfully
   - Measure performance: token cost per squad vs. sequential baseline
   - Target: <10% overhead vs. sequential (due to lock contention + re-planning)

### Success Criteria:
- [ ] Manifest system + locks implemented
- [ ] Orchestration v2 live (sofi dispatch --squad supports parallel)
- [ ] Timeout guard auto-releases stale locks
- [ ] 3-way test passes (zero contamination, <10% overhead)

---

## Phase Success Metrics (All Phases)

| Metric | Target | Baseline | Measurement Method |
|--------|--------|----------|---|
| Handoff semantic drift incidents | 0 per 50 tickets | 2–3 per 50 | Retrospective audit of HANDOFFS.md + code review |
| Cross-project test failures (parallel squads) | 0% | 15% | Integration test (3-way concurrent squads) |
| Spec-review arbitration loops (avg attempts) | 1.2 | 3.1 | Log + analyze sofi spec-review attempts |
| Exfiltration near-misses detected | 0 | 1 (sakk KYC) | Audit trail review (monthly) |
| Gate 8 anomaly detection latency | <10 min | N/A | Integration test (exception → decision log) |
| Parallel squad orchestration overhead | <10% | N/A | Token cost comparison (concurrent vs. sequential) |

---

## Re-Audit Schedule
**Date:** 2026-07-23 (3 weeks post-Phase 6)  
**Task:** Full re-audit via Gemini; compare metrics vs. baselines  
**Output:** ADR-007 "ADR-006 Remediation Outcomes" + lessons learned

---

## Current Queue (After ADR-006 Phases Complete)

1. **ADR-007 Outcome Report** — Gemini re-audit + results summary
2. **ADR-008 Sidecar Observability** — Expand Gate 8 to multi-project cross-correlation
3. **ADR-009 Parallel Squad Orchestration v3** — Auto-scaling based on available resources
4. **ADR-010 Cross-Project Compliance** — Automated audits across all PRJ-* repos

---

**Last Updated:** 2026-07-02  
**Next Handoff Check:** 2026-07-05 (Phase 1 completion)  
**Owner:** CEO (sofi-ceo)
