---
type: brain
mem: episodic
prj: PRJ-XXXX
---
# HANDOFFS — PRJ-XXXX · the ticket bus

> Schema: `company/nexus/bus/ticket-schema.md`. Status ∈ open | accepted | done | rejected | blocked.
> Room Isolation Law: specialist → own Lead → target room's Lead → specialist; boardroom + gateway room may address any Lead (`company/nexus/NEXUS.md`). Cross-room violations are rejected by `validate_room_boundary` inside `sofi gate-check`.
> `done` requires an evidence block (cmd+exit code | file:line | diff/SHA) — `validate_evidence` is fail-closed (constitution/03-verification.md V1).
> Escalation files an up-chain ticket carrying `escalated_from:` and flips the original to blocked (`sofi escalate <PRJ> <TKT> <to> "<reason>"`; chain: `company/nexus/bus/escalation.md`).

## TKT-001 · gate 0
- **from:** gtw-dispatcher
- **to:** str-lead
- **type:** work-order
- **mem:** episodic
- **date:** YYYY-MM-DD
- **task:** Open Gate 0 for PRJ-XXXX. Run the strategy room per `company/rooms/01-strategy/CHARTER.md`: str-product-strategist drafts the Problem Statement + scope boundary (5 deep questions answered); str-business-analyst attaches success metrics + acceptance criteria; str-risk-analyst files the risk register with kill criteria. Assemble the Blueprint.
- **consumes:** intake brief (Work Order Context field) · `_context/FOUNDATIONS.md` (frozen)
- **expected:** `docs/Blueprint.md` + `docs/Problem_Statement.md` + risk register section · local domain `<slug>.local` confirmed in STATE.md · evidence block on completion
- **route:** gatekeeper · high · lite (nexus/routing.yaml: str-lead)
- **status:** open
