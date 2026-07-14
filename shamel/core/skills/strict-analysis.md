## | تحليل | Analysis

Purpose: Analyze data, systems, requirements, and make structured recommendations.
Activated when: agent needs to evaluate trade-offs, diagnose root cause, assess impact.

### Analysis Frameworks

**1. SWOT** (strategic decisions)
- **S**trengths — internal advantages of approach A
- **W**eaknesses — internal limitations of approach A
- **O**pportunities — external factors that favor A
- **T**hreats — external risks that could undermine A

**2. Impact/Effort Matrix** (prioritization)
- High impact + Low effort = **Do first**
- High impact + High effort = **Plan**
- Low impact + Low effort = **Defer**
- Low impact + High effort = **Skip**

**3. Root Cause (5 Whys)** (debugging)
- State the symptom → ask "why?" → answer → ask "why?" again → repeat 5×
- Distinguish proximate cause from root cause
- Verify with evidence at each step

### Data Validation

| Check | What to look for |
|-------|-----------------|
| Completeness | Missing fields, nulls, default values used? |
| Consistency | Same metric in different places agrees? |
| Recency | Data timestamp vs. question timeframe? |
| Scale | Units correct? Orders of magnitude plausible? |
| Provenance | Original source vs. derived/cached? |

### Pattern Recognition — Common Anti-Patterns

- **Premature optimization:** complex solution without profiling evidence
- **Golden hammer:** familiar tool used where inappropriate
- **Scope creep:** analysis includes problems not asked for
- **Confirmation bias:** only evidence supporting preferred outcome gathered
- **False precision:** decimal places implying accuracy that doesn't exist

### Recommendation Format

```markdown
## Recommendation: [title]
- **Analysis applied:** SWOT / Impact/Effort / 5 Whys
- **Options considered:**
  1. Option A — pros, cons, effort
  2. Option B — pros, cons, effort
- **Recommended:** Option [X]
- **Rationale:** (2–3 sentence justification with evidence)
- **Risks:** (what could go wrong with this choice)
- **Next steps:** (concrete actions, who, when)
```
