# Gate 5: Quality Checklist

**Owner:** qa-lead (Barb Jensen)
**Deliverable:** PASS/BLOCK Verdict

## Automated Quality

- [ ] All unit tests green — phpunit/pest/jest
- [ ] All integration tests green
- [ ] All E2E tests green (critical paths)
- [ ] Coverage report ≥ 90% — enforced in CI
- [ ] Mutation score ≥ 80% if applicable
- [ ] Flaky tests quarantined — zero flaky in CI

## Design Audit

- [ ] Built vs frozen spec — field-by-field comparison
- [ ] Visual regression — screenshots match design tokens
- [ ] Responsive check — 320, 768, 1024, 1440 breakpoints
- [ ] Animation/motion matches spec

## Performance

- [ ] TTI < 2s (Lighthouse)
- [ ] LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] API P95 response < 500ms
- [ ] Bundle size under budget
- [ ] k6 load test: no errors at 3x expected traffic

## Security

- [ ] SAST scan clean (no critical/high findings)
- [ ] Secrets scan clean
- [ ] Dependency scan: no critical CVEs
- [ ] Manual pentest findings (if deep-audit) — all fixed or risk-accepted

## Manual Exploration (qa-manual-explorer)

- [ ] Happy path works end-to-end
- [ ] Edge cases tested: empty, massive, offline, timeout
- [ ] Error messages user-friendly
- [ ] Cross-browser: Chrome, Firefox, Safari
- [ ] Mobile: iOS Safari, Android Chrome

## Verification

- [ ] qa-test-architect: risk classification matches test coverage
- [ ] qa-perf-analyst: budget compliance report
- [ ] qa-regression-warden: no regressions introduced

## Sign-off

- [ ] qa-lead signs: "Gate 5 PASS — ship to Staging" or "Gate 5 BLOCK — rework required"
