# MEMORY — routing map (pointers only)

## Quick nav
- `SHAMEL.md` — identity
- `CLAUDE.md` — session contract
- `core/CONSTITUTION.md` — supreme law (7 Teachings)
- `brain/BRAIN.md` — memory architecture

## Constitution (core/constitution/)
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

## Nexus (core/nexus/)
- `registry.yaml` — rooms → agents → skills → tools
- `routing.yaml` — route definitions (aliases only)
- `models.yaml` — alias → model-id mapping
- `gates.yaml` — 9 gates with exit bars
- `pins.json` — agent file SHA-256 pins
- `bus/` — ticket-schema, escalation

## Rooms (core/rooms/)
15 rooms: 00-boardroom, 01-strategy, 02-research, 03-design, 04-architecture, 05-backend, 06-frontend, 07-mobile, 08-data, 09-security, 10-quality, 11-devops, 12-observability, 13-knowledge, 14-gateway

Each: `CHARTER.md`, `agents/<id>.md`, `playbooks/`, `tools/`

## Engine (engine/)
- `bin/shamel` — unified dispatcher
- `shamel_tools/` — core/nexus/brain/net/pipeline
- `scanners/` — feature_scan, code_scan, verify
- `selftest/` — deterministic tests

## Brain (brain/)
- `BRAIN.md` — 3-layer memory architecture
- `org/` — DECISIONS, LESSONS, EVOLUTION, PERSONAS, TEAM_STATUS
- `db/` — brain.db, taskq.db, sessions.jsonl
- `templates/` — STATE, CONTEXT, DECISIONS, HANDOFFS, LESSONS, FOUNDATIONS

## Archive
- `archive/README.md` — tombstone index
- `archive/g1-opencode/`, `g2-engine-v5/`, `g4-org-rooms/`, `g6-orchestrator-fork/`
