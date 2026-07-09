# Gate 7: Production Checklist

**Owner:** ops-lead (Linda Schmidt)
**Deliverable:** Live Deployment

## Pre-Deploy

- [ ] Blue/green or canary deploy configured
- [ ] Rollback procedure tested on staging — proven < 5 min
- [ ] Traffic drain configured for blue/green cutover
- [ ] Database migration double-checked — no destructive DDL
- [ ] Feature flags ready for gradual rollout

## Security

- [ ] SSL/TLS valid — no expiration in < 30 days
- [ ] Security headers verified: CSP, HSTS, X-Frame-Options, X-Content-Type-Options
- [ ] CORS configured — production origins only
- [ ] Rate limiting active
- [ ] WAF rules (if applicable) — tested against staging

## Monitoring

- [ ] Production monitoring alerts active
- [ ] Dashboards populated — real metrics flowing
- [ ] Synthetic monitoring configured (if applicable)
- [ ] On-call engineer notified and acknowledged

## Communication

- [ ] Release notes published (internal)
- [ ] Stakeholders notified of deploy window
- [ ] Rollback decision criteria defined — "what triggers a rollback"

## Verification

- [ ] Canary: 5% traffic → observe 10 min → no errors → ramp
- [ ] Post-deploy smoke tests pass on production
- [ ] SSL Labs grade ≥ B (A preferred)

## Sign-off

- [ ] ops-lead signs: "Gate 7 PASS — production live"
- [ ] Release manager confirms: "Deploy complete, monitoring active"
