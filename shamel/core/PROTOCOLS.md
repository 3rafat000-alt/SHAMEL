# SHAMEL Protocols — البروتوكولات الملزمة

> **Protocols are operational law. Each protocol descends from the Constitution and binds every agent in every room. Violation of a protocol is a violation of the Constitution.**
>
> **البروتوكولات هي قانون تشغيلي. كل بروتوكول ينبثق من الدستور ويلزم كل وكيل في كل غرفة. خرق البروتوكول هو خرق للدستور.**

---

## Protocol 01 — Pipeline Protocol — بروتوكول خط الإنتاج

### Purpose
Enforce the mandatory pipeline flow from user input to final delivery. No agent, no room, no circumstance bypasses this flow.

### Rules
1. **P-01.1 — Mandatory entry.** Every session begins at gtw-intake-reformer. Direct response to user without intake processing → Level 3 violation.
2. **P-01.2 — Sequential gates.** Flow: `gtw-intake-reformer → brd-ceo → room lead(s) → agents → room lead → brd-ceo → user`. No step skipped. No step reordered. Parallel processing only within a single gate scope with CEO approval.
3. **P-01.3 — One artifact at a time.** An agent holds at most one uncommitted artifact. Violation → Level 1.
4. **P-01.4 — Gate check mandatory.** Every pipeline transition triggers `PYTHONPATH=shamel/engine python3 -m shamel_tools gates`. If gate-check fails → pipeline halts, artifact rejected, owning room notified.
5. **P-01.5 — No direct delivery.** No agent delivers directly to user. All output flows through room lead, then CEO, then user. Direct delivery → Level 3.
6. **P-01.6 — Pipeline restart on violation.** Any pipeline violation triggers restart from gtw-intake-reformer. No continuation from midpoint.
7. **P-01.7 — Pipeline timeout.** Each pipeline stage has a maximum duration (defined in `shamel/core/nexus/routing.yaml`). Timeout → auto-escalation to brd-ceo.
8. **P-01.8 — Fast-track bypass.** Only brd-ceo may authorize fast-track (gates 1-3 collapse for low-risk changes). Authorization must be documented in CORTEX. Unauthorized fast-track → Level 3.
9. **P-01.9 — Pipeline evidence chain.** Every pipeline transition produces: `[from → to] [evidence id] [timestamp] [artifacts]`. Chain maintained by receiving agent. Broken chain → Level 2.

### Violation consequence
Level 1–3 depending on severity. Pipeline bypass → Level 3 minimum. Repeat (2×) → Level 4.

---

## Protocol 02 — Handoff Protocol — بروتوكول التسليم

### Purpose
Define strict rules for task handoff between agents and rooms. Ensure no work is lost, no context is dropped, and every handoff is verifiable.

### Rules
1. **P-02.1 — Checkpoint before handoff.** The handing-off agent MUST checkpoint (git commit or brain checkpoint) before initiating handoff. Uncommitted work cannot be handed off. Violation → Level 2.
2. **P-02.2 — Handoff ticket required.** Every cross-room handoff requires a formal ticket: `RCCF` format with evidence, success_metric, and handoff note. Verbal handoff → Level 2.
3. **P-02.3 — Verbatim forwarding.** Leads forward handoff content VERBATIM. Summarization without original citations → Level 2.
4. **P-02.4 — Acceptance required.** The receiving agent/room MUST explicitly accept the handoff. Default acceptance not permitted. Unaccepted handoff → in-flight, not delivered.
5. **P-02.5 — Handoff receipt logging.** Every handoff logged to `brain/handoffs/` with: timestamp, from_agent, to_agent, ticket_id, artifacts, status. Missing log → Level 1.
6. **P-02.6 — Rejection protocol.** Rejecting agent must specify exactly what is missing (evidence, completeness, quality). Vague rejection → Level 1.
7. **P-02.7 — Room boundary enforcement.** Cross-room handoff MUST go through both room Leads. Direct agent-to-agent cross-room handoff → Level 3.
8. **P-02.8 — Handoff timeout.** Receiving agent must acknowledge within 3 agent turns. No response → escalation to receiving room's Lead.
9. **P-02.9 — Handoff verification.** Receiving agent must verify evidence before accepting. Verification steps: check file:line references exist, check exit codes, check screenshots exist. Skipped verification → Level 2.

### Violation consequence
Level 2 for procedural failures. Level 3 for cross-room boundary violation.

---

## Protocol 03 — Evidence Protocol — بروتوكول الأدلة

### Purpose
Define what constitutes valid evidence, how it must be formatted, and what is required before any handoff or gate passage.

### Rules
1. **P-03.1 — Evidence completeness.** Every agent action must produce evidence before handoff. Evidence types:
   - Code changes → `file:line` references for each change
   - Commands → exit code + truncated output (last 20 lines)
   - Research → source URL + verified extract (not LLM-generated summary)
   - Design → screenshot or reference to file in artifacts/
   - Tests → pass/fail output for all test suites run
2. **P-03.2 — File:line format.** Every code change reference: `path/to/file:123`. No vague references. Violation → Level 1.
3. **P-03.3 — No LLM-sourced evidence.** AI-generated claims without execution → Level 2. All evidence grounded in actual execution or observation.
4. **P-03.4 — Screenshot requirement.** UI changes must include screenshots (before/after). Missing screenshot → Gate failure.
5. **P-03.5 — Evidence log.** All evidence logged to `brain/evidence/`: agent_id, timestamp, action, evidence_type, reference, status. Missing log → Level 1.
6. **P-03.6 — Verification required.** Evidence must be independently verifiable. Unverifiable claims → rejected. Fabricated evidence → Level 3.
7. **P-03.7 — Gate evidence package.** Gate-owning room presents: trace to journey map, test results, security review, token efficiency report. Missing → Gate blocked.
8. **P-03.8 — Per-agent evidence checklist.** Each agent type has required evidence:
   - **Engineers:** code diff `file:line`, test output, build exit code
   - **Designers:** screen mockup before/after, design token changes, a11y audit
   - **Researchers:** source URL, search query, extracted fact, confidence score
   - **Architects:** architecture diagram, decision ADR, schema migration plan
   - **Security:** threat model, vulnerability scan, pentest report
   - **QA:** test plan, execution results, coverage report, regression status
   - **DevOps:** deployment log, health check, rollback plan

### Violation consequence
Level 1–2 for formatting. Level 3 for fabricated evidence. Level 4 for intentional falsification.

---

## Protocol 04 — Escalation Protocol — بروتوكول التصعيد

### Purpose
Define when and how escalation occurs, with strict time limits and clear escalation paths.

### Rules
1. **P-04.1 — Escalation triggers.** Required when:
   - Agent cannot complete task (uncertainty, missing dependency, blocked)
   - Violation detected
   - Handoff rejected twice
   - Pipeline times out
   - Security concern identified
   - Any Teaching potentially violated
   - Cross-room dispute unresolved after 3 turns
2. **P-04.2 — Escalation chain.** Fixed: `specialist → room Lead → gtw-conflict-resolver → brd-arbiter → brd-ceo`. Security → brd-cso before brd-arbiter. Chain skipping → Level 3.
3. **P-04.3 — Time limits.**
   - Agent escalates within 1 turn of detecting issue
   - Room Lead responds within 2 turns
   - gtw-conflict-resolver responds within 3 turns
   - brd-arbiter responds within 5 turns
   - brd-ceo responds within 10 turns
   - Missed limit → auto-escalation
4. **P-04.4 — Escalation format.** Must include: issue description, attempted resolution, evidence, suggested action. Incomplete → returned.
5. **P-04.5 — Escalation log.** All logged to `brain/escalations/`: timestamp, escalator, issue, level, resolution, time_to_resolve. Missing → Level 1.
6. **P-04.6 — False escalation.** Deliberate false escalation → Level 2. Repeat (2×) → Level 3.
7. **P-04.7 — No suppression.** No Lead may suppress agent's escalation. Suppression → Level 3.
8. **P-04.8 — Escalation acknowledgement.** Every escalation receives acknowledgement within 1 turn. Unacknowledged escalation → auto-escalates one level.

### Violation consequence
Level 1–3. Suppression → Level 3.

---

## Protocol 05 — Conflict Resolution Protocol — بروتوكول حل النزاعات

### Purpose
Establish binding process for resolving disputes between rooms, agents, or interpretations of the law.

### Rules
1. **P-05.1 — Mandatory resolution.** All conflicts formally resolved. Ignoring → Level 2 for both parties.
2. **P-05.2 — Resolution chain.**
   - Level 1 (procedural, same room): room Lead resolves. Deadline: 3 turns.
   - Level 2 (between rooms): gtw-conflict-resolver. Deadline: 5 turns.
   - Level 3 (constitution/protocol interpretation): brd-arbiter. Deadline: 10 turns.
   - Level 4 (fundamental values): brd-ceo + board vote. Deadline: 20 turns.
3. **P-05.3 — Conflict format.** Documented with: parties, subject, positions, evidence per party, attempted resolution. Undocumented → invalid.
4. **P-05.4 — Resolution binding.** Binding on all parties. Non-compliance → Level 3.
5. **P-05.5 — Precedent.** All resolutions logged to `brain/conflicts/`. Ignoring precedent → Level 1.
6. **P-05.6 — Good faith.** Bad faith (dilatory tactics, obstruction) → Level 3.
7. **P-05.7 — Rapid resolution.** Level 1 conflicts may use asynchronous communication. Level 2+ require synchronous resolution session. Delaying sync session → Level 1.

### Violation consequence
Level 1–3. Bad faith → Level 3.

---

## Protocol 06 — Memory Protocol — بروتوكول الذاكرة

### Purpose
Define what goes into the brain, what gets purged, retention periods, and memory hygiene standards.

### Rules
1. **P-06.1 — Mandatory storage.** Every consequential action stored: decisions, evidence, handoffs, escalations, violations, gate passages, lessons. Omission → Level 1.
2. **P-06.2 — Retention periods.**
   - Session logs: retained until project closure, then compressed
   - Evidence: retained until project closure
   - Violations: retained permanently
   - Handoffs: retained until project closure + 3 months
   - Escalations: retained permanently
   - Decisions (ADRs): retained permanently
   - Lessons learned: retained permanently
   - Session working data: purged at session end unless checkpointed
3. **P-06.3 — Purge criteria.** Data purged when: retention expires AND no active investigation references it AND not tagged `permanent`. Purge logged to `brain/purge/`.
4. **P-06.4 — Brain structure.** All memory follows `shamel/brain/BRAIN.md`. Custom structures → Level 1 unless approved by knw-lead.
5. **P-06.5 — Cross-project contamination.** No memory from one PRJ-ID leaks into another. Isolation check on every write enforced by `validate_room_boundary()`. Leak → Level 3.
6. **P-06.6 — Memory hygiene.** No redundant information. Duplicate entries → Level 1. No raw LLM outputs as facts → Level 2.
7. **P-06.7 — Memory consolidation.** knw-lead runs consolidation every 10 turns: deduplication, summarization, purge expired data. Skipped consolidation → Level 1 for knw-lead.
8. **P-06.8 — Memory access log.** Every brain read/write operation logged with agent_id, timestamp, path, operation_type. Missing log → Level 1.

### Violation consequence
Level 1 for hygiene failures. Level 2 for structural violations. Level 3 for cross-project contamination.

---

## Protocol 07 — Communication Protocol — بروتوكول التواصل

### Purpose
Define how agents communicate, message formatting rules, response structure, and communication channel assignments.

### Rules
1. **P-07.1 — Caveman mode.** Agent-to-agent/lead communication uses concise mode (fragments OK, no articles, no pleasantries). Prose reserved for code, commits, security warnings, user-facing output. Prose in agent communication → Level 1.
2. **P-07.2 — Fixed format.** Every response: `[action] [target] [evidence] [next_step]`. Missing structure → Level 1.
3. **P-07.3 — One topic per message.** Single-topic only. Multiple topics → Level 1.
4. **P-07.4 — No chit-chat.** No greetings, farewells, pleasantries, empty acknowledgements. Empty messages → Level 1.
5. **P-07.5 — Channel discipline.** Assigned channel only:
   - Room-internal: within room context
   - Cross-room: via Lead only
   - Emergency: via brd-ceo directly (`#emergency` prefix)
   - Security: via brd-cso directly (`#security` prefix)
6. **P-07.6 — Response deadline.** Respond within 1 turn. No response → escalation to room Lead.
7. **P-07.7 — Evidence in communication.** Every claim cites evidence: `[file:line]` or `[evidence:<id>]`. Unsupported claim → Level 1.
8. **P-07.8 — No hallway talk.** Cross-room coordination without Lead → Level 2.
9. **P-07.9 — Communication record.** All cross-room communication recorded in `brain/communications/`. Unrecorded → Level 1.

### Violation consequence
Level 1 for formatting. Level 2 for channel/coordination violations.

---

## Protocol 08 — Security Protocol — بروتوكول الأمان

### Purpose
Define secrets management, permissions, access control, and security boundaries. Enforced by brd-cso with absolute veto authority below CEO.

### Rules
1. **P-08.1 — Zero secrets in code.** No secrets, keys, tokens, passwords in code, commits, brain, or artifacts. Secrets in env vars or vault only. Violation → Level 4.
2. **P-08.2 — Commit hook scan.** Every commit scanned for secrets. Blocked commit must be cleaned. Bypassing scan → Level 4.
3. **P-08.3 — Permission boundaries.** Agent accesses only resources assigned to its room and current PRJ-ID. Cross-room read → Level 2. Cross-project read → Level 3.
4. **P-08.4 — CSO veto.** brd-cso has absolute veto over any artifact/decision/action with security risk. Veto overridden only by brd-ceo + unanimous board. Violation → Level 4.
5. **P-08.5 — Security gate mandatory.** Gate-3 and Gate-5 require sec-lead sign-off. Every gate requires sec-lead notification. Skipping security → Level 3.
6. **P-08.6 — Vulnerability reporting.** Any agent discovering vulnerability reports to sec-lead within 1 turn. Concealment → Level 4.
7. **P-08.7 — Input sanitization.** All external inputs sanitized. Injection-capable data validated. Bypass → Level 3.
8. **P-08.8 — Security audit trail.** All security-relevant actions logged to `brain/security/`. Missing log → Level 2.
9. **P-08.9 — Least privilege.** Agents operate with minimum required permissions. Elevated access temporary and logged. Unauthorized elevation → Level 3.
10. **P-08.10 — Dependency scan.** Every new dependency scanned for known vulnerabilities before use. Skipped scan → Level 2.
11. **P-08.11 — MCP access control.** MCP/brain server binds to 127.0.0.1 only. Remote access requires SSH tunnel + brd-cso approval. Violation → Level 3.

### Violation consequence
Level 2 for procedural. Level 3 for boundary violations. Level 4 for secrets, veto violations, or vulnerability concealment.

---

## Protocol 09 — Quality Protocol — بروتوكول الجودة

### Purpose
Establish minimum quality bar, review requirements, and quality gates. Enforced by qa-lead and brd-cqo.

### Rules
1. **P-09.1 — Quality gate mandatory.** Every artifact passes Gate-5. No pass → no delivery. Violation → Level 3.
2. **P-09.2 — Test requirements.** All code must have passing tests. Coverage minimum: 80% logic, 100% critical paths. Below threshold → blocked.
3. **P-09.3 — Review requirement.** Every commit requires review by ≥1 other agent in same room. Solo commit without review → Level 2.
4. **P-09.4 — Quality metrics.** Every artifact scored on: correctness, completeness, efficiency, traceability, security. Score <7/10 in any dimension → blocked.
5. **P-09.5 — Regression prevention.** All tests pass before AND after change. Regression → artifact rejected, owning room Lead notified.
6. **P-09.6 — Quality escalations.** qa-lead escalates to brd-cqo. brd-cqo escalates to brd-ceo. Escalation cannot be blocked.
7. **P-09.7 — Quality debt log.** Known quality issues logged to `brain/quality/debt.md`. Unlogged → Level 2 for qa-lead.
8. **P-09.8 — Minimum bar for handoff.** No cross-room handoff accepts artifacts with quality score <7/10. Accepting low-quality handoff → Level 2 for receiving Lead.
9. **P-09.9 — Quality sampling.** brd-cqo randomly samples 10% of artifacts per gate for independent quality audit. Sampled artifact failing audit → gate reverted.

### Violation consequence
Level 1–2 for procedural. Level 3 for gate skipping.

---

## Protocol 10 — Emergency Protocol — بروتوكول الطوارئ

### Purpose
Define response to system crashes, agent failure, data loss, and catastrophic failures.

### Rules
1. **P-10.1 — Emergency classification.**
   - **SEV-1 (Critical):** System crash, data loss, security breach, constitutional violation. Immediate halt. CEO+CSO notified. Response: immediate.
   - **SEV-2 (High):** Agent failure mid-task, pipeline corruption, brain inconsistency. Halt. Lead notified. Response: 3 turns.
   - **SEV-3 (Medium):** Gate failure, test failure, quality breach. Pause. Room notified. Response: 5 turns.
   - **SEV-4 (Low):** Minor violation, handoff failure. Warning. Response: 10 turns.
2. **P-10.2 — Emergency response chain.**
   - Agent detects → brain checkpoint immediately → notify room Lead
   - Lead assesses → classify SEV level → notify escalation path
   - SEV-1: brd-ceo + brd-cso + brd-cqo. Emergency board.
   - SEV-2: brd-ceo + relevant Lead. Task reassignment.
   - SEV-3: brd-cqo + qa-lead. Quality review.
   - SEV-4: Room Lead handles with documentation.
3. **P-10.3 — Brain checkpoint.** Before any recovery action, brain checkpoint created to `brain/checkpoints/`. No recovery without checkpoint → Level 3.
4. **P-10.4 — Root cause analysis.** SEV-1/2 require formal RCA within 20 turns. Filed to `brain/incidents/`. Skipped → Level 3 for Lead.
5. **P-10.5 — Recovery procedure.** Restore brain checkpoint → verify data integrity → resume from gtw-intake-reformer → replay lost work. No skipping → Level 3.
6. **P-10.6 — Agent failure.** Checkpoint created → task reassigned → failed agent quarantined → RCA → agent restored or replaced.
7. **P-10.7 — Communication blackout.** During SEV-1, only emergency traffic allowed. Violation → Level 2.
8. **P-10.8 — Post-emergency report.** Every emergency produces postmortem in `brain/postmortems/`. Missing → Level 2.
9. **P-10.9 — Emergency drill.** Full emergency drill every 50 agent turns. Missed drill → Level 1 for ops-lead.

### Violation consequence
Level 1–3 depending on handling failure. Level 4 for concealing emergency.

---

## Protocol 11 — Tool Protocol — بروتوكول الأدوات

### Purpose
Define which tools each agent class may use, enforce tool discipline, and prevent unauthorized tool access.

### Rules
1. **P-11.1 — Tool binding.** Every agent uses only tools assigned in its frontmatter (`tools:` field in `shamel/agents/<id>.md`). Unauthorized tool use → Level 2.
2. **P-11.2 — Categorized tool access.**
   - **All agents:** Read, Edit, Write, Bash, Grep (basic operations)
   - **Leads only:** Task (delegation to sub-agents)
   - **Board (CEO + staff):** Task, WebSearch, WebFetch (orchestration + research)
   - **Intake-reformer:** Read, Edit, Write, Bash, Grep, WebSearch, WebFetch (intelligence gathering)
   - **Researchers:** Read, Edit, Write, Bash, Grep, WebSearch, WebFetch (external data)
   - **Security:** Read, Edit, Write, Bash, Grep, WebSearch (threat intelligence)
   - **No agent:** Direct user messaging tools, filesystem outside repo, rm -rf
3. **P-11.3 — Tool logging.** Every invocation logged: agent_id, tool, input_summary, output_summary, duration. Missing log → Level 1.
4. **P-11.4 — No tool sharing.** Agent cannot lend tools to another agent. Violation → Level 2.
5. **P-11.5 — Tool timeout.** Tools exceeding max duration killed. Repeated → Level 1.
6. **P-11.6 — Chain execution.** Multi-tool sequences must be intentional with clear evidence for each step. Blind tool chaining → Level 1.
7. **P-11.7 — Tool preflight.** Before destructive tool use (rm, mv, chmod), agent confirms target path. Skip confirmation → Level 2.

### Violation consequence
Level 1–2.

---

## Protocol 12 — Token Economy Protocol — بروتوكول اقتصاد الرموز

### Purpose
Enforce token efficiency across all agents. Cheapest model for every task.

### Rules
1. **P-12.1 — Cheapest model rule.** Every task uses cheapest model that clears quality bar (defined in `shamel/core/nexus/models.yaml`). Deep-tier on routine task → Level 2.
2. **P-12.2 — Verbosity limit.** Essential information only. One sentence where sufficient. Verbose → Level 1.
3. **P-12.3 — Context discipline.** Minimum viable context. No dumping entire files when snippet suffices. Wasteful → Level 1.
4. **P-12.4 — Token audit.** `PYTHONPATH=shamel/engine python3 -m shamel_tools budget` audits every 20 turns. Threshold: 2× expected burn. Exceeding → review by brd-cqo.
5. **P-12.5 — Waste log.** All waste incidents logged to `brain/economy/waste.md`. Unlogged → Level 1 for room Lead.
6. **P-12.6 — Context budget per room.** Each room has max context allocation (defined in routing.yaml). Room exceeding allocation → Lead reports to brd-cqo.

### Violation consequence
Level 1–2.

---

## Protocol 13 — Gate Protocol — بروتوكول البوابات

### Purpose
Define the 9 lifecycle gates, their owners, exit criteria, and enforcement.

### Rules
1. **P-13.1 — Gate sequence immutable.** 0→1→2→3→4→5→6→7→8. No skipping, no reordering. Violation → Level 3.
2. **P-13.2 — Gate ownership.** Each gate has designated owner (defined in `shamel/core/nexus/gates.yaml`). Only owner may pass artifact through gate.
3. **P-13.3 — Exit criteria.** Defined per gate. Artifacts not meeting criteria cannot pass. Waiving criteria → Level 3.
4. **P-13.4 — Gate evidence.** Gate passage requires: trace to journey map, test results, security review, token report, quality score. Missing → blocked.
5. **P-13.5 — Gate rejection.** Rejected artifact returns to owning room with specific reason. Vague rejection → Level 1 for gate owner.
6. **P-13.6 — Gate log.** All passages logged to `brain/gates/`. Missing → Level 1 for gate owner.
7. **P-13.7 — Gate rollback.** If artifact fails post-gate verification, gate passage is rolled back and owning room notified. Failure to rollback → Level 2.

### Violation consequence
Level 1–3.

---

## Protocol 14 — Memory Isolation Protocol — بروتوكول عزل الذاكرة

### Purpose
Enforce strict memory boundaries between projects. Prevent cross-project data leakage, context poisoning, and authorization bypass.

### Rules
1. **P-14.1 — Project isolation.** Every PRJ-ID has isolated brain storage. No project reads another project's brain files. Violation → Level 3.
2. **P-14.2 — Context boundary.** Agent context for PRJ-X contains ONLY: PRJ-X STATE.md, PRJ-X HANDOFFS.md, PRJ-X CONTEXT.md. No other project files in context. Violation → Level 2.
3. **P-14.3 — Ticket scope.** Tickets reference exactly one PRJ-ID. Cross-project tickets → Level 3. Tckt with ambiguous PRJ-ID → rejected by gtw-intake-reformer.
4. **P-14.4 — Brain write isolation.** `brain/memdb.py` enforces project prefix on every write. Write without PRJ-ID prefix → Level 2.
5. **P-14.5 — Lesson isolation.** Lessons learned in PRJ-X tagged with `[PRJ-X]`. Cross-project lesson injection → Level 2.
6. **P-14.6 — Isolation audit.** knw-lead audits isolation monthly (every 40 turns). Breach found → Level 3 for responsible agent.

### Violation consequence
Level 1–3. Cross-project data leak → Level 3.

---

## Protocol 15 — MCP & Brain Access Protocol — بروتوكول الوصول إلى العقل

### Purpose
Secure the MCP (Model Context Protocol) brain server. Prevent unauthorized access, data exfiltration, and brain manipulation.

### Rules
1. **P-15.1 — Local binding only.** MCP server binds to `127.0.0.1` (localhost). Remote bind requires brd-cso written approval. Violation → Level 3.
2. **P-15.2 — Authentication.** Every MCP request includes agent_id header. Requests without valid agent_id → rejected with 401.
3. **P-15.3 — Authorization.** MCP server enforces room boundaries. Agent may read/write only its room's brain files. Violation attempt → logged, Level 2 for agent.
4. **P-15.4 — Path guard.** Every file write resolves against BRAIN_ROOT. Path traversal (`../`) → rejected. Attempted traversal → Level 3.
5. **P-15.5 — Rate limiting.** MCP server limits: 100 req/min per agent, 500 req/min total. Exceeding → 429 response, logged for brd-cso.
6. **P-15.6 — Audit trail.** Every MCP operation logged: agent_id, timestamp, operation, path, size. Log to `brain/audit/mcp.jsonl`. Missing log → Level 1.
7. **P-15.7 — TLS requirement.** Production MCP uses TLS. Non-TLS connections logged as warning. Certificate validation enforced. Violation → Level 2.
8. **P-15.8 — No persistent connections.** MCP connections are request-response only. No long-lived sessions. Violation → Level 1.
9. **P-15.9 — Brain write quorum.** Destructive brain writes (delete, overwrite organics) require 2-agent quorum (writer + room Lead). Single-agent destructive write → Level 3.
10. **P-15.10 — MCP health check.** `/health` endpoint returns: status, uptime, request_count, error_count, last_error. Health check every 10 turns. Unreachable MCP → escalation to knw-lead.

### Violation consequence
Level 1–3. Path traversal or authentication bypass → Level 3.

---

## Protocol Priority — ترتيب أولوية البروتوكولات

In case of conflict between protocols, resolution follows:

```
Pipeline (01) > Security (08) > Emergency (10) > Handoff (02) > Quality (09) > Gate (13) > Evidence (03) > Memory Isolation (14) > Escalation (04) > Conflict (05) > MCP/Brain (15) > Memory (06) > Communication (07) > Tool (11) > Token Economy (12)
```

A lower-priority protocol cannot override a higher-priority protocol. A protocol that contradicts the Constitution is void.

---

*All protocols enforced by `shamel gate-check` and `shamel doctor`. Violations logged to brain automatically.*
*جميع البروتوكولات مُنفَّذة بواسطة `shamel gate-check` و `shamel doctor`. المخالفات تُسجل في العقل تلقائياً.*
