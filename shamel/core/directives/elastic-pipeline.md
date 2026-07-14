# CEO Operational Directive — Elastic Pipeline (tiered ceremony within the mandatory flow)

**Status: Operational Directive, NOT a Constitutional Article.** This file does not appear in CONSTITUTION.md's "Twelve Articles" table and is not one of Articles 00–11. It carries no article number, does not require the Amendment Process (`CONSTITUTION.md` §Amendment Process), and can be revised or revoked by brd-ceo alone, logged as an ADR in `brain/org/DECISIONS.md` — the same weight class as `P-01.8` (Fast-track bypass), just scoped to ceremony-density instead of gate-collapse. Reference: ADR-015.

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Read `core/CONSTITUTION.md`, `01-work-order.md`, and `10-lifecycle-gates.md` first.

## Authority

This directive is issued under the CEO's existing standing authority to scale procedure without a boardroom vote (CEO Covenant item 7 — "I build the system that builds the product"; the same class of authority that already lets brd-ceo authorize Fast-Track gate collapse under `P-01.8`, though this directive is broader in scope than P-01.8 and is therefore logged separately as ADR-015 rather than a one-off P-01.8 authorization). It changes **nothing** in `CONSTITUTION.md` — not the Seven Teachings, not the fixed pipeline of Law 1, not Articles 00–11, and not the Twelve Articles table. It answers a narrower operational question those articles leave open: *how much scaffolding does a given work order need between the fixed checkpoints?* If this directive is ever found to conflict with any Article or Teaching, the Article/Teaching prevails and this directive is void in that case until revised (same override rule CONSTITUTION.md applies to Articles, applied here one level down).

## The problem this solves

Article 01 mandates an RCCF Work Order for every spawn. Article 10 mandates 9 lifecycle gates. Neither states how much ceremony a one-line config fix needs versus a new payment integration — both would otherwise default to the same weight, which either starves large work of rigor or drowns small work in process (a Teaching IV violation). This directive supplies a size/density classifier that scales ceremony without ever touching the checkpoint sequence itself.

## The four tiers

Classify by the **single highest-triggered tier** — never additive scoring. One LARGE trigger outweighs any number of TRIVIAL signals.

| Tier | Trigger (any ONE qualifies) |
|------|------|
| **TRIVIAL** | 1–2 files touched, no new dependency, no design ambiguity, no security trigger |
| **SMALL** | 3–5 files touched, or one small localized addition, no new dependency, no design ambiguity, no security trigger |
| **STANDARD** | 6+ files, or one new dependency with a clear/pinned version, or one open design question that doesn't touch architecture, no security trigger |
| **LARGE** | Many files (double-digit+), OR a new dependency with unresolved compatibility/version risk, OR design ambiguity affecting architecture, OR touches any Security Trigger domain below |

## Security trigger list — force-escalates regardless of computed tier

The following domains always compute as **LARGE**, no matter how few files are touched, and always require 09-security involvement (Article 07 CSO authority):

- Auth flows (login, session, token issuance/refresh)
- User input handling (parsing, validation, sanitization boundaries)
- Database / migrations (schema change, data shape change)
- External API or webhook integration
- Crypto / secrets (keys, signing, encryption at rest or in transit)
- Payment flows — e.g. PRJ-SAKK's live **CCPayment** crypto rails and **Stripe Issuing** virtual-card integration are canonical examples of this trigger

File count never overrides this list. A one-line change to a webhook signature check is LARGE.

## Ceremony by tier

| Tier | Work Order | Gate-A pause | Security consult | Evidence |
|------|-----------|--------------|-------------------|----------|
| TRIVIAL | Single RCCF, mechanical route | Logged, not blocking | — | Standard Article 03 block |
| SMALL | Single RCCF | Lead reviews before execute | — | Standard Article 03 block |
| STANDARD | RCCF + explicit sign-off | Blocking, lead must clear | On request | Standard Article 03 block |
| LARGE | RCCF + explicit sign-off | Blocking, lead must clear | Mandatory, sec-lead notified (Article 07 §Security gate mandatory) | Pass^k where money/auth/PII applies (Article 03 V3) |

Tier is recorded alongside effort class in the Work Order Command field (Article 01). A tier discovered to be under-classified after the fact reopens GATE-A.

## The two hard gates

Both gates sit **inside** the existing mandatory pipeline of Law 1 (`gtw-intake-reformer → brd-ceo(+board) → room lead(s) → agents → room lead → brd-ceo → user`). They govern how much scaffolding fills the space *between* those fixed checkpoints — they do not add, remove, skip, or reorder a checkpoint. No tier ever authorizes bypassing brd-ceo or a room lead.

**GATE-A — after plan, before execution.** Sits after the room lead's RCCF Work Order is approved but before any agent begins executing it. Bar: tier is classified and logged, plan traces to a frozen upstream artifact (Article 01 Context field), out-of-bounds is stated, and — for LARGE — sec-lead has been notified per Article 07.

**GATE-B — before CEO hands off.** Sits after agents' work returns to the room lead and before brd-ceo hands off to the user (or before any commit crosses into a shared branch, per Article 06). Bar: Article 03 evidence block present, the tier's required ceremony is complete, and — for LARGE — the adversarial second-check of Protocol 02 has run.

## What this directive does not do

- Does not create a third path around brd-ceo or a room lead.
- Does not let a Lead self-classify LARGE work down to skip sec-room.
- Does not replace Article 10's 9 gates — GATE-A/GATE-B are sub-checkpoints inside whichever lifecycle gate is currently open, not a parallel gate system.
- Does not change RCCF's four fields (Article 01) — tier is a value carried inside them, not a new field.
