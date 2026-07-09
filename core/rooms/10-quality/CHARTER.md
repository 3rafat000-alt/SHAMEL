# الجودة (Quality)

## Mission
Gate 5 (gatekeeper room) — ONE aggregated PASS/BLOCK verdict, >=90% coverage, perf budgets, design-fidelity audit.

## Members
- lead
- test-architect
- automation-engineer
- manual-explorer
- perf-analyst
- design-auditor
- regression-warden

## Interfaces
Inbound: working software from bck/fnt/mob leads. Outbound: PASS/BLOCK verdict to ops-lead (Gate 6).

## Room-bar
- Each agent grounds claims to file:line
- Lead signs off on room deliverables
- Cross-room traffic goes specialist → own Lead → target room Lead → specialist
- Lead forwards findings verbatim

## Escalation
Specialist → qa-lead → brd-cqo → brd-ceo
