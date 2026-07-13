## | ذاكرة | Memory Management

Purpose: Use brain system (HIPPOCAMPUS, CORTEX, AMYGDALA) for persistent knowledge.
Activated when: agent learns something, encounters anomaly, needs prior context.

### HIPPOCAMPUS — Session Working Memory

Write immediately when:
- User states a preference, constraint, or project rule
- You fix a bug (store the root cause + fix)
- You discover a non-obvious design decision
- You learn a person's role, expertise, or preference
- You encounter a workaround for a known issue

**Format:**
```json
{
  "type": "hippocampus",
  "topic": "short label",
  "fact": "one-sentence observation",
  "source": "conversation | code | investigation",
  "timestamp": "ISO-8601"
}
```

### CORTEX — Long-Term Memory

Promote from HIPPOCAMPUS daily / session-end when:
- Pattern repeated 3+ times → becomes project rule
- Bug fixed → root cause + resolution archived
- Design decision → rationale + alternatives stored
- User preference stated explicitly → saved as rule

**Format:**
```
CORTEX ENTRY: [Rule / Decision / Learning]
Topic: [one word]
Content: [what was learned]
Context: [why relevant, when applies]
Expires: [date or "permanent"]
```

### AMYGDALA — Alerts

Trigger alert when:
- Security vulnerability discovered
- Data loss or corruption confirmed
- Production incident observed
- Contradictory instructions received
- Critical deadline at risk

**Format:**
```
⚠️ AMYGDALA ALERT
Signal: [what triggered]
Evidence: [file, log, quote]
Impact: [what's at stake]
Suggested action: [what to do next]
```

### Brain Read Protocol

On session start / task begin:
1. Query CORTEX for entries relevant to current task
2. Scan AMYGDALA for active alerts
3. Load HIPPOCAMPUS for any in-progress context
4. Merge into task context before proceeding
