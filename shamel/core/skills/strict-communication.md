## | تواصل | Communication

Purpose: Standardize agent-to-agent and agent-to-user communication for clarity.
Activated when: agent sends message, hands off task, reports status, escalates.

### Tone Rules

- Professional: no slang, emoji, or casual phrasing
- Clear: one idea per paragraph, short sentences
- Concise: cut every word that doesn't add information
- Direct: state conclusion first, then supporting evidence

### Message Format — SCQA Structure

```
## Situation: (context — one sentence)
## Complication: (what changed / what's wrong — one sentence)
## Question: (what needs to be decided — one sentence)
## Answer: (your recommendation — one sentence)
```

### Handoff Format

```markdown
## Handoff: [task/skill name]
- **From:** [agent ID]
- **To:** [agent ID]
- **State:** Done / Blocked / In-progress (X%)
- **Artifacts:** [files, branches, URLs]
- **Decisions made:** (key decisions and rationale)
- **Open questions:** (what still needs resolution)
- **Next action:** (what the recipient should do first)
```

### Evidence Template

```markdown
**Claim:** [what is asserted]
**Evidence:** 
- Source: [file:line or URL]
- Excerpt: "relevant quote or snippet"
- Timestamp: [when observed, if applicable]
**Confidence:** High / Medium / Low
```

### Clarity Rules

1. **No ambiguous pronouns:** "It failed" → "The auth service returned 503."
2. **Quantify:** "Slow" → "p95 latency 2400ms (threshold: 500ms)."
3. **Explicit conclusions:** End every message with a clear call to action or summary.
4. **One topic per message:** If multiple unrelated issues, split into separate messages.
5. **Evidence always cited:** No claim without source reference.
