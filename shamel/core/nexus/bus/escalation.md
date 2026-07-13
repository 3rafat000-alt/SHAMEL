# Escalation Chain

## Path

```
specialist → room Lead → gtw-conflict-resolver → brd-arbiter → brd-ceo
```

Security:
```
specialist → sec-lead → brd-cso (absolute veto below CEO)
```

## Circuit breaker (3-attempt ceiling)

1. Halt immediately.
2. Crash-dump JSON: `{ "commit": "<sha>", "loop_count": 4, "failed_context": "...", "last_command": "...", "error_delta": "...", "escalation_token": "<TKT>" }`
3. Escalate: `shamel escalate <PRJ> <TKT> <up-chain> "circuit breaker"`
4. Mark ticket `blocked → escalation_required`
5. Await decision; resume only after ADR recorded.

## When to escalate

- Decision above your authority (arbitration, contradictory constraints, security surface)
- 3 failed attempts on same sub-task
- Contradicting sources that can't be resolved (G5)
- SLO breach requiring formal Gate-1 reopen
