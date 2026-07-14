## | مراجعة الكود | Code Review

Purpose: Systematic code review for security, correctness, and maintainability.
Activated when: agent receives diff or file for review, PR check, pre-merge gate.

### Review Framework — Read Order

1. **Signature first:** function name, params, return type — does contract match intent?
2. **Control flow:** loops, conditions, early returns — any path unhandled?
3. **Data flow:** input → transformation → output — is data mutated unexpectedly?
4. **Error handling:** every error path caught? Appropriate recovery or propagation?
5. **Resource lifecycle:** allocations, connections, file handles — all released?

### Checklist (15+ items)

- [ ] **SEC-01** — Secrets/keys/tokens hardcoded? Use env vars or vault.
- [ ] **SEC-02** — User input sanitized? SQL injection, XSS, command injection.
- [ ] **SEC-03** — Authz checks on every protected path? Not just authn.
- [ ] **PERF-01** — N+1 queries? Batch or eager-load.
- [ ] **PERF-02** — Unbounded loops/recursion? Input-size bound checked.
- [ ] **PERF-03** — Sync calls in hot path? Async where possible.
- [ ] **STL-01** — Project conventions followed? Lint passes without new warnings.
- [ ] **STL-02** — Dead code/imports? Remove before landing.
- [ ] **STL-03** — Error messages user-actionable? Not cryptic codes.
- [ ] **STL-04** — Logging appropriate level? (info vs debug vs error)
- [ ] **LOG-01** — Off-by-one, null dereference, type confusion.
- [ ] **LOG-02** — Race condition in shared state? Lock or use atomics.
- [ ] **LOG-03** — State machine has illegal transitions?
- [ ] **EDG-01** — Empty collections, nil maps, zero values — handled?
- [ ] **EDG-02** — Network timeout, partial write, cancelled context — handled?
- [ ] **EDG-03** — Concurrent access to mutable state — synchronized?

### Severity Levels

| Level | Definition | Action |
|-------|-----------|--------|
| **Critical** | Prod bug, security hole, data loss | Block merge, fix immediately |
| **Major** | Incorrect behavior, perf regression, broken contract | Fix before merge |
| **Minor** | Style, naming, docs, edge case not covered | Fix preferred, can defer |
| **Suggestion** | Improvement, alternative approach | Consider for future |

### Output Format

```markdown
## Review: `<file>:<line>`
- **Severity:** Critical | Major | Minor | Suggestion
- **Evidence:** (code snippet, log line, test output)
- **Issue:** (what is wrong)
- **Fix:** (how to resolve)
```
