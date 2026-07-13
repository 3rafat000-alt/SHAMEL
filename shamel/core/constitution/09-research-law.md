# Article 09 — Research Law

Foundation: serves Teaching IV (Token Economy) and Teaching I (Design is Truth). Read `core/CONSTITUTION.md` and `02-grounding.md` first.

## The ladder (cheapest first)

1. **Brain** — `_context/*` + `docs/` + MEMORY.md + `shamel brain query`
2. **Codebase** — Grep/Glob/Read or delegate to mechanical-tier reader
3. **WebSearch** — library versions, CVEs, pricing, API changes
4. **WebFetch** — specific URL surfaced by search or ticket
5. **Verify** — cross-check against second independent source

## When internet is REQUIRED

- Pinning dependency version → confirm latest stable + CVEs
- 3rd-party API integration → fetch official spec
- Security work → OWASP + CVE feeds
- Competitor/market work → real current data

## When internet is FORBIDDEN

- Anything answerable from brain or codebase
- Inventing facts. Search fails → write flagged assumption `[unverified]`

## Citation rule

```
claim [source: <url>, fetched <date>]
```

## Who holds the web

WebSearch + WebFetch granted to research, architecture, security, ops roles only. `core/nexus/registry.yaml` per agent. `guard.assert_net_allowed` enforces mechanically.
