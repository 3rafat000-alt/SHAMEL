# MEMORY — routing map (pointers only)

## Pipeline (intake → CEO → rooms → agents)
```
User raw input
    ↓
gtw-intake-reformer   ← research, think, rewrite into optimal prompt
    ↓
brd-ceo               ← analyze, consult board + room leads, decide, distribute
    ↓
brd-cpo|cto|cqo|cso   ← board members — domain expertise, veto power
brd-arbiter            ← dispute resolution
    ↓
room leads (Task tool) ← plan, distribute to agents, review, consolidate
    ├─ str-lead → strategy agents
    ├─ res-lead → research agents
    ├─ dsn-lead → design agents
    ├─ arc-lead → architecture agents (Task → arc-system-architect, etc.)
    ├─ bck-lead → backend agents (Task → bck-api-engineer, etc.)
    ├─ fnt-lead → frontend agents
    ├─ mob-lead → mobile agents
    ├─ dat-lead → data agents
    ├─ sec-lead → security agents
    ├─ qa-lead  → quality agents
    ├─ ops-lead → devops agents
    ├─ obs-lead → observability agents
    └─ knw-lead → knowledge agents
    ↓
agents execute        ← each agent knows room, lead, handoff protocol
    ↓
room lead → brd-ceo  ← consolidate, verify, deliver
```

## Team awareness
- Every agent knows its room, room lead, and peer agents
- Room Isolation Law: agents talk only to their room lead
- Room leads delegate via Task tool → sub-agents run in parallel
- Handoff: agent → room lead → CEO
- All 106 agents share awareness of the 15 rooms and their functions

## Quick nav
- `SHAMEL.md` — identity
- `CLAUDE.md` — session contract
- `shamel/core/CONSTITUTION.md` — supreme law (7 Teachings)
- `shamel/brain/BRAIN.md` — memory architecture

## Constitution (shamel/core/constitution/)
- `00-operating-system.md` — universal turn contract
- `01-work-order.md` — RCCF delegation
- `02-grounding.md` — G1–G5
- `03-verification.md` — V1–V5
- `04-reflection.md` — scheduled dreaming
- `05-token-economy.md` — routing ladder
- `06-git-discipline.md` — git law
- `07-security-law.md` — CSO veto, secrets
- `08-handoff-law.md` — tickets, room boundaries
- `09-research-law.md` — web research protocol
- `10-lifecycle-gates.md` — 9 gates + two-track
- `11-intake-orchestration.md` — hierarchy protocol

## Nexus (shamel/core/nexus/)
- `registry.yaml` — rooms → agents → skills → tools
- `routing.yaml` — route definitions (aliases only)
- `models.yaml` — alias → model-id mapping
- `gates.yaml` — 9 gates with exit bars
- `pins.json` — agent file SHA-256 pins
- `bus/` — ticket-schema, escalation

## Rooms (shamel/core/rooms/)
15 rooms: 00-boardroom, 01-strategy, 02-research, 03-design, 04-architecture, 05-backend, 06-frontend, 07-mobile, 08-data, 09-security, 10-quality, 11-devops, 12-observability, 13-knowledge, 14-gateway

Each: `CHARTER.md`, `agents/<id>.md`, `playbooks/`, `tools/`

## Engine (shamel/engine/)
- `bin/shamel` — unified dispatcher
- `shamel_tools/` — core/nexus/brain/net/pipeline
- `scanners/` — feature_scan, code_scan, verify
- `selftest/` — deterministic tests

## Brain (shamel/brain/)
- `BRAIN.md` — 3-layer memory architecture
- `org/` — DECISIONS, LESSONS, EVOLUTION, PERSONAS, TEAM_STATUS
- `db/` — brain.db, taskq.db, sessions.jsonl
- `templates/` — STATE, CONTEXT, DECISIONS, HANDOFFS, LESSONS, FOUNDATIONS

## Archive
- `archive/README.md` — tombstone index
- `archive/g1-opencode/`, `g2-engine-v5/`, `g4-org-rooms/`, `g6-orchestrator-fork/`
