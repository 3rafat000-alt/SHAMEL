# Gate 8: Observe Checklist

**Owner:** obs-lead (Naomi Brooks)
**Deliverable:** SLO Report

## Service Levels

- [ ] SLOs defined per critical path — uptime, latency, error rate
- [ ] SLOs met — error budget remaining ≥ 50%
- [ ] SLI data collected — real metrics for each SLO
- [ ] Performance baselines established — TTI, LCP, CLS, INP

## Observability

- [ ] All critical alerts tested — dry-run, not just configured
- [ ] Runbooks verified — every alert has 1:1 runbook
- [ ] Logs searched — no unexpected errors
- [ ] Tracing active — critical paths captured

## Journey Analysis

- [ ] Journey leaks detected via telemetry — drop-off points
- [ ] User feedback collected — surveys, support tickets, NPS
- [ ] Funnel analysis — conversion rates per journey stage
- [ ] Pain points identified — where do users struggle

## Incident Readiness

- [ ] Incident response playbooks reviewed
- [ ] Postmortem from any production incident (if any) complete
- [ ] Action items from postmortem tracked in Gate 0 issues

## Continuous Improvement

- [ ] Lessons documented — what went well, what didn't
- [ ] Gate 0 issues filed for:
  - Journey leaks found
  - Performance regressions
  - UX friction points
  - Technical debt discovered
- [ ] Next cycle planned — "what do we build next"

## Sign-off

- [ ] obs-lead signs: "Gate 8 PASS — cycle complete"
- [ ] Insights feed back to Gate 0: "Observation → Improvement"
