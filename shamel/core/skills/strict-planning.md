## | تخطيط | Planning

Purpose: Break down work into tracked, estimated, dependency-aware tasks.
Activated when: agent receives new task, bug report, feature request.

### Task Decomposition

1. **One task = one deliverable.** If it produces multiple outputs, split.
2. **Leaf tasks ≤ 4 hours.** If estimated larger, decompose further.
3. **Every task has:** ID, title, description, acceptance criteria, owner.

**Template:**
```markdown
- [ ] T-001: [action verb] [object]
  - AC: [measurable outcome]
  - Depends on: T-002, T-003
  - Effort: Small
  - Risk: Low
```

### Dependency Mapping

```
A → B → C    (sequential: A must finish before B starts)
A ─→ C       (A and B can run in parallel; both feed C)
    B ─→ C
```

- Blocking deps: predecessor MUST finish (hard dep)
- Informational deps: predecessor SHOULD finish (soft dep)
- Visualize with Mermaid `graph LR` for >3 tasks

### Estimation Scale

| Size | Definition | Effort range | Example |
|------|-----------|-------------|---------|
| Trivial | Config change, typo fix | <15 min | Fix env var name |
| Small | Single file, known pattern | 0.5–2 h | Add new API endpoint |
| Medium | Multiple files, moderate complexity | 2–6 h | Implement auth middleware |
| Large | Cross-cutting, new subsystem | 6–20 h | Add payment integration |
| XLarge | Multi-day, multiple people | >20 h | Migrate database |

### Risk Identification

| Risk type | What to watch for | Mitigation |
|-----------|------------------|------------|
| Unknown domain | Team hasn't done this before | Spike first (timeboxed) |
| External dependency | API, library, third-party | Fallback strategy ready |
| Integration point | Connects to 3+ systems | Contract test first |
| Performance | Affects existing perf targets | Benchmark before/after |
| Security | Handles PII, auth, money | Security review gate |

### Review Gates — Stop Before Starting If

- AC not written or not testable
- External dep not verified (API key, service status)
- Task >XLarge and not decomposed
- No rollback plan for destructive changes
