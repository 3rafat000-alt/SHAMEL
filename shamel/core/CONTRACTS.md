# SHAMEL Cross-Room Service Contracts — العقود البينية لغرف SHAMEL

> **These contracts define the formal service relationships between rooms. Each contract is binding. A room that fails to meet its SLA may be escalated. These contracts descend from the Constitution and Protocols and cannot contradict them.**
>
> **هذه العقود تحدد علاقات الخدمة الرسمية بين الغرف. كل عقد ملزم. الغرفة التي لا تفي بمستوى الخدمة المتفق عليه يمكن تصعيدها. هذه العقود تنبثق من الدستور والبروتوكولات ولا يمكن أن تخالفهما.**

---

## Contract Structure — هيكل العقد

Each contract specifies:
- **Service:** What is provided
- **Provider:** The room that provides
- **Consumer:** The room that consumes
- **Description:** Service details
- **SLA:** Service Level Agreement — time limits and quality bars
- **Handoff format:** How the service output is delivered
- **Dispute resolution:** How conflicts are resolved

---

## Contract 01 — Direction Setting — تحديد التوجيه

**Service:** Strategic direction and prioritization
**Provider:** 00-boardroom
**Consumer:** 01-strategy
**Description:** Boardroom provides strategic goals, market context, resource allocation decisions, and priority framework to strategy room. Strategy room executes within the defined boundaries.
**SLA:** Boardroom responds to strategy requests within 5 agent turns. Strategic directives issued in writing with measurable objectives. Vague direction → returned.
**Handoff format:** Formal directive via `RCCF` ticket with: PRJ-ID, strategic objective, success metric, resource envelope, time constraint, constraints list. Boardroom retains veto on strategy proposals.
**Dispute resolution:** Strategy escalates to brd-ceo. If brd-ceo is the source of dispute, escalated to board vote (3/4 majority). Resolution binding within 10 agent turns.

---

## Contract 02 — Research Informing Design — البحث يغذي التصميم

**Service:** User research, journey maps, behavioral insights
**Provider:** 02-research
**Consumer:** 03-design
**Description:** Research room provides validated user research (journey maps, persona insights, pain points, behavioral data) to design room. Design relies on research output as source of truth for all design decisions.
**SLA:** Research delivers within current session unless scope exceeds 10 agent turns. Research output must include: source data, methodology, key findings, journey maps, confidence level. Research without methodology → returned. Research output validity: 20 agent turns (after which re-validation required).
**Handoff format:** Research dossier via `RCCF` ticket with: `journey-map/`, `persona/`, `findings/` sections. All claims cite evidence (Protocol 03). Handoff triggers Gate-1 closure.
**Dispute resolution:** Disagreement on research findings escalated to gtw-conflict-resolver. If unresolved → brd-arbiter. Design cannot override research findings without boardroom approval.

---

## Contract 03 — Design Handoff to Frontend — تسليم التصميم للواجهة الأمامية

**Service:** UI designs, design system tokens, interaction specs
**Provider:** 03-design
**Consumer:** 06-frontend
**Description:** Design room delivers validated designs, design system tokens, interaction specifications, and asset exports to frontend room for implementation. Frontend implements exactly what is designed — no creative interpretation.
**SLA:** Design delivers within current session for screens up to 5 states. Each delivery includes: Figma/HTML references, design tokens (colors, typography, spacing, motion), responsive breakpoints, interaction states (hover, focus, error, loading, disabled, empty). Design without interaction states → returned. Design validity: 30 agent turns.
**Handoff format:** Design package via `RCCF` ticket with: `screens/`, `tokens/`, `specs/` directories. Implicit handoff triggers Gate-2 closure and Gate-4 readiness.
**Dispute resolution:** Implementation questions → dsn-lead responds within 3 agent turns. Disagreement on design fidelity → escalated to gtw-conflict-resolver → brd-arbiter. Frontend cannot modify design without dsn-lead approval.

---

## Contract 04 — Architecture to Backend — الهندسة للخلفية

**Service:** System architecture, API design, data models, technical specifications
**Provider:** 04-architecture
**Consumer:** 05-backend
**Description:** Architecture room provides system architecture decisions, API contracts, data models, technology choices, and integration specs to backend room. Backend builds to the architecture — no deviation without ADR.
**SLA:** Architecture delivers specifications before any backend implementation begins. API contracts must include: endpoints, request/response schemas, auth requirements, rate limits, error codes. Architecture without error handling spec → returned. Architecture validity: 40 agent turns.
**Handoff format:** Architecture package via `RCCF` ticket with: `api/`, `data/`, `infra/` sections. ADR for every significant decision. Handoff triggers Gate-3 closure.
**Dispute resolution:** Backend requests clarification → arc-lead responds within 3 agent turns. Architecture change request requires arc-lead approval + ADR. Escalation to brd-cto if unresolved.

---

## Contract 05 — Backend to Data — الخلفية للبيانات

**Service:** Data storage, caching, query services, data pipelines
**Provider:** 05-backend
**Consumer:** 08-data
**Description:** Backend room provides data requirements (schemas, access patterns, volume estimates, caching strategy) to data room. Data room implements and maintains data infrastructure aligned to backend needs.
**SLA:** Data delivers schema migrations within 5 agent turns of receipt. Data access layer ready within 10 agent turns. Data must implement: schemas, indices, migrations with `down()`, connection pooling, query optimization. Migration without `down()` → returned. Data validity: 50 agent turns.
**Handoff format:** Data requirements via `RCCF` ticket with: `schema/`, `migrations/`, `queries/` sections. Backend provides estimated QPS, data volume, access patterns. Handoff closure requires Gate-4 sign-off.
**Dispute resolution:** Data disputes escalated to arc-lead for architecture review. If architecture confirms → binding. Otherwise → gtw-conflict-resolver.

---

## Contract 06 — Security Review at Every Gate — مراجعة الأمان عند كل بوابة

**Service:** Security review, threat modeling, vulnerability assessment
**Provider:** 09-security
**Consumer:** ALL rooms (00–14)
**Description:** Security room provides security review at every gate. Security has veto authority at every gate (absolute below brd-cso). No artifact passes a gate without sec-lead sign-off. Security provides threat models, vulnerability assessments, and remediation guidance.
**SLA:** Security review initiated within 2 agent turns of notification. Gate-3 and Gate-5: mandatory deep review (≤10 agent turns). Other gates: rapid review (≤3 agent turns). Security must provide clear pass/fail with specific findings. Vague findings → returned.
**Handoff format:** Security review via `#security` channel with: `findings/`, `severity/`, `remediation/` sections. Findings must include `file:line` references, CWE/CVE where applicable, and remediation priority. Pass signed by sec-lead or brd-cso.
**Dispute resolution:** Security veto can only be overridden by brd-cso (self-review) or brd-ceo with unanimous board vote. Disagreement on severity → escalated to brd-cso. Security findings cannot be ignored — they must be fixed or explicitly waived by brd-cso.

**Special clauses:**
- sec-09.1: Any room may request emergency security review with `#security-emergency` prefix. Response within 1 agent turn.
- sec-09.2: brd-cso may unilaterally halt any room's work on security grounds. Halt stands until board review.
- sec-09.3: Every security review is logged to `brain/security/reviews/`.

---

## Contract 07 — QA Handoff — تسليم الجودة

**Service:** Quality assurance, test validation, regression detection
**Provider:** 10-quality
**Consumer:** ALL rooms (00–14)
**Description:** Quality room provides QA services to all rooms. Every artifact must pass quality review before crossing Gate-5. Quality provides test validation, regression detection, performance benchmarking, and quality scoring.
**SLA:** Standard QA review within 5 agent turns of receipt. Deep QA (full regression) within 10 agent turns. Critical path QA within 3 agent turns. QA score must be: ≥7/10 overall, ≥7/10 in each dimension (correctness, completeness, efficiency, traceability, security). Below threshold → blocked.
**Handoff format:** QA request via `RCCF` ticket with: artifact reference, test scope, priority. QA response includes: `score/`, `findings/`, `recommendations/`. Critical findings must specify severity and remediation.
**Dispute resolution:** Room disputes QA score → escalated to brd-cqo. brd-cqo may order re-test or override with written justification. QA cannot block without specific, actionable findings.

**Special clauses:**
- qa-07.1: Pre-merge QA mandatory for all cross-gate artifacts. Missing QA → merge blocked.
- qa-07.2: Quality debt (known issues) must be logged before handoff. Hidden debt → qa-lead escalates to brd-cqo.

---

## Contract 08 — Deploy to Monitor — النشر للمراقبة

**Service:** Deployment pipeline, infrastructure, monitoring, alerting
**Provider:** 11-devops
**Consumer:** 12-observability
**Description:** DevOps room deploys artifacts to production/staging and provides infrastructure. Observability room receives deployment notification and activates monitoring, alerting, and dashboards. Observability feeds telemetry back to all rooms.
**SLA:** Deploy within 3 agent turns of Gate-7 pass. Infrastructure ready before deploy. DevOps provides: deploy log, environment info, rollback procedure, health check endpoint. Deploy without rollback plan → blocked. Observability activates monitoring within 2 agent turns of deploy notification.
**Handoff format:** Deploy notification via `RCCF` ticket with: `deploy/`, `infra/`, `rollback/` sections. Observability response includes: `dashboard/`, `alerts/`, `slo/` sections. Monitoring activation closes Gate-7.
**Dispute resolution:** Monitoring disagreements escalated to brd-cto. SLO breach handling follows Protocol 10 (Emergency). Infrastructure disputes escalated to arc-lead.

---

## Contract 09 — Knowledge Services — خدمات المعرفة

**Service:** Brain query, documentation, knowledge management
**Provider:** 13-knowledge
**Consumer:** ALL rooms (00–14)
**Description:** Knowledge room provides brain query services, documentation generation, knowledge consolidation, and cross-session memory services to all rooms. Knowledge is the single source of organizational memory.
**SLA:**
- Brain query: within 2 agent turns
- Documentation generation: within 5 agent turns
- Knowledge consolidation: within 10 agent turns
- Cross-session memory retrieval: within 3 agent turns (if brain synced)
- Query without context → returned. Request without PRJ-ID → returned.
**Handoff format:** Knowledge request via `RCCF` ticket with: query type (read/write/consolidate), scope, context. Knowledge response includes: findings with citations, confidence level, source references.
**Dispute resolution:** Knowledge accuracy dispute → escalated to brd-cqo for verification. Knowledge not found → query logged as knowledge gap for future consolidation.

**Special clauses:**
- knw-09.1: All rooms MUST contribute lessons learned to knowledge at project milestones. Missing contribution → Level 1 for room Lead.
- knw-09.2: Knowledge runs consolidation every 10 agent turns. All rooms must respond to consolidation requests within 3 agent turns.

---

## Contract 10 — Intake and Routing — الاستقبال والتوجيه

**Service:** Intake processing, routing, reformulation, gatekeeping
**Provider:** 14-gateway
**Consumer:** ALL rooms (00–14), EXTERNAL (user input)
**Description:** Gateway room is the single entry point for all external input. Gateway processes intake, reformulates into structured format, routes to appropriate room via next room's Lead, and maintains routing tables. No external input reaches any room without passing through gateway.
**SLA:** Intake processing within 1 agent turn. Reformulation and routing within 2 agent turns. Gateway must: classify input type (request/report/question/emergency), extract PRJ-ID context, determine target room, reformulate into RCCF format, log to brain. Unprocessable input → return to sender with specific reason.
**Handoff format:** Reformulated input via formal `RCCF` ticket with: `intake/`, `routing/`, `context/` sections. Gateway provides: classification, priority, target room, suggested work order. Emergency prefix (`#emergency`) triggers immediate brd-ceo notification.
**Dispute resolution:** Routing dispute → escalated to brd-ceo within 2 agent turns. Gateway routing is presumptively correct — overridden only by brd-ceo or brd-cso (for security routing).

**Special clauses:**
- gtw-10.1: Gateway maintains `core/nexus/routing.yaml` as single source of routing truth. No agent hardcodes routing.
- gtw-10.2: Gateway has authority to reject malformed input. Rejection must specify: what is missing, what is expected, how to resubmit.
- gtw-10.3: Emergency intake bypasses normal queue and routes directly to brd-ceo + brd-cso.

---

## Contract 11 — Strategy to Research — الاستراتيجية للبحث

**Service:** Research briefs, strategic questions, market hypotheses
**Provider:** 01-strategy
**Consumer:** 02-research
**Description:** Strategy room provides research briefs, strategic questions, market hypotheses to research room. Research investigates and validates/invalidates hypotheses. Strategy prioritizes what is researched.
**SLA:** Strategy delivers research brief within 5 agent turns of boardroom direction. Brief must include: hypothesis, scope, success criteria, constraints. Vague brief → returned. Research validates within 10 agent turns of receipt.
**Handoff format:** Research brief via `RCCF` ticket with: `hypothesis/`, `scope/`, `methods/` sections. Research returns findings with evidence, confidence level, and recommendations.
**Dispute resolution:** Strategy disputes research findings → escalated to brd-cpo. Research refutes strategy assumptions → escalated to boardroom.

---

## Contract 12 — Backend to Frontend — الخلفية للواجهة الأمامية

**Service:** API endpoints, data access, business logic services
**Provider:** 05-backend
**Consumer:** 06-frontend
**Description:** Backend room provides API endpoints, data access services, and business logic execution to frontend room. Frontend consumes backend APIs as specified in architecture contracts. Backend implements API contracts exactly as specified.
**SLA:** API endpoints delivered within 10 agent turns of architecture spec. Backend provides: working endpoints, request/response validation, error handling, rate limiting, API documentation. API without error codes → returned. API stability guarantee: changes require ADR.
**Handoff format:** API handoff via `RCCF` ticket with: `endpoints/`, `schemas/`, `auth/` sections. Includes OpenAPI spec or equivalent. Frontend integration test at Gate-5 validates contract compliance.
**Dispute resolution:** API contract disputes → escalated to arc-lead. Breaking changes require arc-lead approval and frontend Lead notification minimum 5 agent turns before change.

---

## Contract 13 — Design to Architecture — التصميم للهندسة

**Service:** UX requirements, interaction constraints, design constraints
**Provider:** 03-design
**Consumer:** 04-architecture
**Description:** Design room provides UX requirements, interaction constraints, user flow specifications, and design constraints to architecture room. Architecture incorporates design constraints into system architecture. Design feasibility must be validated before architecture finalization.
**SLA:** Design provides UX requirements within 5 agent turns of Gate-1. Requirements include: user flows, interaction patterns, performance expectations (load time, animation fps), accessibility requirements. Missing accessibility requirements → returned. Architecture validates feasibility within 5 agent turns.
**Handoff format:** Design constraints via `RCCF` ticket with: `flows/`, `constraints/`, `accessibility/` sections. Architecture responds with feasibility assessment and any necessary trade-offs.
**Dispute resolution:** Feasibility disagreement → escalated to gtw-conflict-resolver → brd-cto + brd-cqo. Design cannot override architecture feasibility determination without boardroom.

---

## Contract 14 — Data to Frontend — البيانات للواجهة الأمامية

**Service:** Data query services, real-time data, cached data
**Provider:** 08-data
**Consumer:** 06-frontend
**Description:** Data room provides data query services, cached responses, and real-time data feeds to frontend room. Frontend consumes data through backend APIs (not directly to data layer). Data room ensures query performance and data freshness.
**SLA:** Query performance: p99 < 200ms for standard queries. Data freshness: as specified in architecture. Cached data TTL: as specified. Data provides: query performance reports, cache hit rates, data freshness guarantees. Degraded performance → data room notifies frontend within 2 agent turns.
**Handoff format:** Data service via backend API (indirect). Frontend does not directly query data room. Data concerns raised through backend room.
**Dispute resolution:** Data performance disputes → escalated to arc-lead for architecture review → brd-cto.

---

## Contract 15 — Testing and QA Feedback Loop — حلقة ردود الجودة

**Service:** Test results, quality metrics, regression reports
**Provider:** 10-quality
**Consumer:** 05-backend, 06-frontend, 07-mobile
**Description:** Quality room provides test results, quality metrics, and regression reports to implementation rooms (backend, frontend, mobile). Implementation rooms fix issues and resubmit. Loop continues until quality bar is met.
**SLA:** Test results within 3 agent turns of submission. Quality report includes: pass/fail counts, coverage metrics, performance benchmarks, security scan results, regression comparison. Report without regression comparison → returned.
**Handoff format:** Quality report via `RCCF` ticket with: `results/`, `metrics/`, `regression/` sections. Critical failures include specific `file:line` references. Fix required within 5 agent turns for critical, 10 for medium.
**Dispute resolution:** Quality score dispute → escalated to brd-cqo. Repeated failure to clear quality bar → escalated to brd-ceo for resource review.

---

## SLA Violation Escalation — تصعيد خرق مستوى الخدمة

| SLA Miss | First Offense | Second Offense | Third Offense |
|----------|---------------|----------------|---------------|
| <2 agent turns late | Warning (Level 1) | Level 2 | Level 2 + CEO notified |
| 2–5 turns late | Level 2 | Level 2 + Lead notified | Level 3 + CEO review |
| >5 turns late | Level 2 + Lead notified | Level 3 | Level 3 + board notification |

**SLA clock starts** when handoff ticket is accepted by consumer room. **SLA clock pauses** when provider requests clarification and resumes when consumer responds.

---

## Conflict Resolution Between Contracts — حل النزاعات بين العقود

If two contracts are in conflict:
1. Contract with higher-priority room (lower room number) prevails
2. If same priority: boardroom contract > security contract > quality contract > all others
3. If still unresolved: escalated to brd-arbiter → brd-ceo

---

*All contracts enforced by `shamel gate-check`. SLA audit run at Gate-8 by brd-cqo. Violations logged to `brain/contracts/`.*
*جميع العقود مُنفَّذة بواسطة `shamel gate-check`. تدقيق مستوى الخدمة يُجرى في البوابة 8 من قبل brd-cqo. المخالفات تُسجل في `brain/contracts/`.*
