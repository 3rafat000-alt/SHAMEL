## | البحث | Research

Purpose: Conduct efficient, verifiable web research with cited sources.
Activated when: agent needs external info, fact-check, competitor analysis, market data.

### Query Crafting

**Formula:** `[domain] [specific question] [exclusion] site:[trusted-source]`
- Bad: "how to fix memory leak"
- Good: "golang http handler memory leak pprof goroutine site:go.dev OR stackoverflow.com"

**Query types by goal:**
| Goal | Pattern |
|------|---------|
| Fact-finding | `[concept] [specific attribute] [year]` |
| Comparison | `[X] vs [Y] comparison [criteria]` |
| Troubleshooting | `[error message] OR [symptom] [technology] solution` |
| Latest info | `[topic] [current_year] [update OR changes]` |

### Source Evaluation (1–5 Scale)

| Score | Criteria |
|-------|----------|
| 5 | Official docs, peer-reviewed paper, primary source, gov/edu domain |
| 4 | Well-known tech blog, established news, official repository |
| 3 | Community wiki, medium-quality blog, forum with expert replies |
| 2 | Personal blog, unverified forum, anonymous source |
| 1 | No date, no author, promotional, clearly biased, self-published |

### Timeboxing

| Query scope | Max queries | Total time |
|-------------|-------------|------------|
| Single fact | 2–3 | 5 min |
| Topic overview | 4–6 | 10 min |
| Deep research | 8–12 | 25 min |

Stop when: 3 independent sources agree OR diminishing returns (last 2 queries found nothing new).

### Synthesis Format

```markdown
### Finding: [claim/answer]
- **Confidence:** High / Medium / Low
- **Sources:**
  - [Title](URL) — score 5 — key quote
  - [Title](URL) — score 4 — key quote
- **Conflict:** (if sources disagree, note both sides)
- **Implication:** (how this affects the current task)
```
