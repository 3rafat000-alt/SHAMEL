# Ticket Schema

## Fields

| Field | Required | Format |
|-------|----------|--------|
| id | yes | TKT-NNN (regex: `^TKT-\d{3,}$`) |
| gate | yes | digit 0-8 |
| from | yes | agent-id from registry |
| to | yes | agent-id from registry |
| task | yes | free text, one line |
| consumes | no | comma-separated file paths |
| expected | yes | comma-separated deliverable paths |
| route | yes | alias·effort·caveman |
| status | yes | open | accepted | done | rejected | escalated |

## Validation

`validate_ticket()` in `shamel gate-check`:
- from/to must be valid agent IDs in registry
- Room-boundary: same room, agent→Lead, Lead→Lead, or boardroom/gateway→Lead
- Status must be in allowed set
- `done` requires evidence block attached
