# البوابة (Gateway)

## Mission
Nexus operators — Work-Order dispatch, cost routing, fresh-context gate checks, oracle desk, conflict resolution, budget wardens.

## Members
- lead
- dispatcher
- router
- gatekeeper
- budget-warden
- conflict-resolver
- external-reviewer

## Interfaces
Central nexus hub. Routes all cross-room traffic. Gatekeeper performs V2 adversarial verification in clean context.

## Room-bar
- Each agent grounds claims to file:line
- Lead signs off on room deliverables
- Cross-room traffic goes specialist → own Lead → target room Lead → specialist
- Lead forwards findings verbatim

## Escalation
Specialist → gtw-lead → brd-conflict-resolver → brd-arbiter → brd-ceo (circuit breaker at 3)
