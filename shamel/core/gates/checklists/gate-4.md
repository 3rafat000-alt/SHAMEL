# Gate 4: Build Checklist

**Owners:** bck-lead · fnt-lead · mob-lead
**Deliverable:** Working Software

## Backend (bck-lead)

- [ ] All endpoints match OpenAPI spec — 422-JSON rule enforced
- [ ] Domain services complete — business logic, money math (buy ≥ sell, precision)
- [ ] Queue jobs idempotent — retry/backoff/DLQ configured
- [ ] All migrations reversible — rollback scripts tested
- [ ] Integration connections live — webhook handlers per documented shape
- [ ] Coverage ≥ 90% (unit + integration)

## Frontend (fnt-lead)

- [ ] Blade/Vue views cover all states — empty, loading, error, success, edge
- [ ] Responsive — 320px to 1200+px, no horizontal scroll
- [ ] WCAG 2.2 AA enforced — keyboard nav, ARIA, contrast
- [ ] Micro-interactions complete — with reduced-motion alternative
- [ ] Bundle budgets met — code-split, lazy load
- [ ] Core Web Vitals pass — TTI < 2s

## Mobile (mob-lead)

- [ ] Flutter clean architecture — feature-first with GetIt DI
- [ ] All states covered via Bloc/Cubit
- [ ] Platform channels typed — ApiException pattern
- [ ] Perf profile: no leaks, shrink-wrap verified

## Cross-Cutting

- [ ] No secrets in code — pre-tool hook pass
- [ ] Code review passed (code-reviewer) — clean context V2
- [ ] All team leads sign: "Build complete"

## Verification

- [ ] CI pipeline: lint → test → build → scan all green
- [ ] Gatekeeper: endpoint count matches spec, no scope creep
- [ ] TTI measurement: Lighthouse / k6

## Sign-off

- [ ] bck-lead, fnt-lead, mob-lead sign: "Gate 4 PASS — proceed to Quality"
