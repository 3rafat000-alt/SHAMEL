# Gate 3: Architecture Checklist

**Owner:** arc-lead (Vikram Rao)
**Deliverable:** Architecture Package (frozen)

## Validation

- [ ] Component diagram complete (system-architect)
- [ ] Screen → component → endpoint traceability map
- [ ] Data schema finalized — every migration has rollback (data-architect)
- [ ] OpenAPI/GraphQL contract frozen (api-architect)
- [ ] Third-party integrations mapped — field-by-field from authoritative source (integration-architect)
- [ ] Infrastructure plan: network segmentation, scaling strategy, DR posture (infra-architect)
- [ ] STRIDE threat model complete (sec-threat-modeler)
- [ ] 4-pillar spec review passed (review-architect)
- [ ] Performance budget defined — TTI < 2s, bundle sizes, API response times
- [ ] Caching strategy documented — what, where, TTL, invalidation
- [ ] Error handling strategy — error codes, fallbacks, user messaging
- [ ] Security architecture reviewed — auth, encryption, secrets (sec-authn-engineer)

## Evidence Required

- [ ] Component diagram [verified: artifact]
- [ ] Traceability matrix (screen → endpoint)
- [ ] ER diagram with migration plan
- [ ] OpenAPI spec (openapi.yaml)
- [ ] STRIDE threat model document
- [ ] 4-pillar spec review report

## Verification

- [ ] Gatekeeper runs spec review in clean context (never self-grade)
- [ ] Every migration proven reversible with rollback script
- [ ] No secret in code — secrets-warden scans pass
- [ ] API contracts validated against prototype spec

## Sign-off

- [ ] Architecture Package signed by arc-lead: "Gate 3 PASS — proceed to Build"
- [ ] arc-lead confirms CTO review (brd-cto)
