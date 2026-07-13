# Article 01 — The Work Order (RCCF)

Foundation: serves Teaching II (Hierarchical Flow) and Teaching IV (Token Economy). Read `core/CONSTITUTION.md` and `00-operating-system.md` first.

Every spawn is a contract: **Role · Context · Command · Format.**

## The four fields

### Role — who it is
- Persona + agent ID from `core/nexus/registry.yaml`
- Room + authority. Room Isolation Law applies.
- Route from `core/nexus/routing.yaml` — verbatim, never invented.

### Context — the full file
- Project PRJ-ID. Enforces Teaching III.
- Gate number from `core/nexus/gates.yaml`.
- Brain pointers: STATE → HANDOFFS → CONTEXT. Never paste.
- THE frozen upstream artifact (path + section). Not frozen → reject upward.

### Command — the exact ask
- Verb + object. One coherent deliverable.
- In-bounds: concrete sub-parts.
- Out-of-bounds: what NOT to touch, with owning agent per exclusion.
- Success metric: from agent spec frontmatter.
- Effort class + fail-safe: from `core/nexus/routing.yaml`.

### Format — how to deliver
- Deliverable shape: exact paths.
- Gate-bar: objective pass condition.
- Grounding clause: cite file:line, mark unverified, abstain.
- Evidence block: command + output/exit code or file:line proof.
- Handoff: who receives next.

## Self-check (before spawn)

1. Persona + room + exact route from routing.yaml?
2. Brain + one frozen artifact (path + section)?
3. One bounded unit with out-of-bounds?
4. "Done" gradeable — path, gate-bar, evidence block?
5. Effort class + fail-safe stated?
6. Every field a real specific?

Six yeses → spawn. Any no → clarify.

## Compact form (shared context)

```
@Room.agent → ask → bar {route} ⮕ next
@05-backend.bck-blade-engineer → POST /auth/login → matches OpenAPI {workhorse·medium·ultra} ⮕ bck-code-reviewer
```
