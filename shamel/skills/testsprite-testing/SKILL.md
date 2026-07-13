---
name: testsprite-testing
description: >
  How to drive the connected TestSprite MCP against PRJ-SAKK — a
  server-rendered Laravel/Blade app served by php-fpm+Caddy (NOT a Vite/npm
  dev-server app), so TestSprite's default assumptions need adjustment.
  Covers backend vs frontend test-plan generation, when to bootstrap vs skip
  it, and how PRJ-SAKK's multiple surfaces (admin/portal/company/merchant/
  agent/API) map to TestSprite's "needLogin" frontend flow. Use before
  running any TestSprite test generation/execution on this project.
  Recommended for: qa-automation-engineer, qa-test-architect,
  qa-regression-warden, bck-api-engineer (backend test plans).
user-invocable: true
metadata:
  project: PRJ-SAKK
  category: testing
  version: "1.0.0"
---

# TestSprite Testing — PRJ-SAKK

TestSprite's tools assume a typical JS-app shape (a local dev server on a
port like 5173, `npm run build && npm run start/preview` to distinguish
dev/production mode). **PRJ-SAKK does not match that shape** — it has no
`package.json`/Vite, and is server-rendered Blade over php-fpm (sofi pool)
behind Caddy. Read this before calling any TestSprite tool here.

## Available tools (this session)
- `mcp__TestSprite__testsprite_check_account_info` — confirm plan/credits
  before a large run.
- `mcp__TestSprite__testsprite_bootstrap` — **first-time init ONLY**. Before
  calling, check whether `.testsprite/config.json` already exists in the
  project — if it does, skip bootstrap entirely and go straight to test-plan
  generation or execution. Never re-bootstrap an already-configured project.
- `mcp__TestSprite__testsprite_generate_standardized_prd` — generates a PRD
  from the codebase; useful once at project onboarding, not per-change.
- `mcp__TestSprite__testsprite_generate_backend_test_plan` — plan for API/
  controller-level tests. This is the primary tool for PRJ-SAKK's actual
  business logic (wallets, withdrawals, AML, Stripe Issuing, CCPayment).
- `mcp__TestSprite__testsprite_generate_frontend_test_plan` — plan for
  UI-driven tests (`needLogin: true/false`). Relevant to the admin panel and
  the 3 partner portals (company/merchant/agent) — all server-rendered Blade,
  not a JS SPA, but this tool still works against a live URL via browser
  automation, it just won't find a Vite entry point.
- `mcp__TestSprite__testsprite_generate_code_and_execute` — generates and
  runs the actual tests. Don't call `testsprite_bootstrap` first if a test
  plan already exists — call this directly.
- `mcp__TestSprite__testsprite_generate_code_summary` /
  `mcp__TestSprite__testsprite_open_test_result_dashboard` — post-run summary
  and dashboard (schemas not preloaded this session — use ToolSearch
  `select:mcp__TestSprite__testsprite_generate_code_summary,mcp__TestSprite__testsprite_open_test_result_dashboard`
  to load them when needed).

## Adapting to PRJ-SAKK's serving model

| TestSprite assumption | PRJ-SAKK reality | What to do |
|---|---|---|
| `localPort` = Vite dev port (default 5173) | Served by Caddy at `http://sakk.local` (port 80, no explicit port needed) or the public `https://sakk.zanjour.com` for the public surface only | Confirm the live port first: `curl -I http://sakk.local`. Pass that resolved port to `bootstrap`/wherever a port is required — do NOT default to 5173. |
| `serverMode: 'development'` vs `'production'` (build+start vs dev server) | There is no dev/prod distinction — php-fpm+Caddy serving IS the only serving mode, and it's always the equivalent of "production" (compiled, cached views once `artisan view:cache` has run) | Always pass `serverMode: 'production'` to `testsprite_generate_code_and_execute`. Passing `'development'` will silently cap frontend tests at 15 high-priority tests under the assumption of a fragile dev server that doesn't apply here. |
| Single frontend app | PRJ-SAKK has **6 distinct authenticated surfaces**: admin (`/admin/*`, `is_admin` guard), company portal (`/company/*`, `company` middleware), merchant portal (`/merchant/*`), agent portal (`/agent/*`), the public landing/legal pages (no auth), and a JSON API consumed by the Flutter mobile app (`/api/*`, Sanctum) | Generate SEPARATE frontend test plans per surface rather than one pass with `needLogin: true` — each has a different login flow and role. Point `projectPath` at the same repo but scope `additionalInstruction` in `generate_code_and_execute` to name the surface and its login route (e.g. "Test only the /company/* portal; log in via POST /company/login with a payrollReady() company fixture user"). |
| Frontend = the thing you test for UI bugs | The Blade views ARE the backend's output — a rendering bug here is often a controller/data bug, not a pure frontend bug | For business-logic-critical surfaces (withdrawals, AML holds, card issuance, CCPayment deposits), prefer `testsprite_generate_backend_test_plan` over the frontend plan — it will exercise the actual money-movement logic, not just DOM assertions. |

## Recommended flow for a single-page redesign cycle
This matches the "full cycle per page" pattern requested for the dashboard
redesign initiative: after rebuilding a page's data/controller/view, drive it
through TestSprite before considering the cycle closed:
1. `testsprite_generate_backend_test_plan` (if the page's controller/data
   logic changed) — confirms the underlying data contract is correct.
2. `testsprite_generate_frontend_test_plan({needLogin: true})` scoped to the
   admin surface — confirms the page renders and is navigable post-redesign.
3. `testsprite_generate_code_and_execute({serverMode: 'production', testIds: [...]})`
   — restrict `testIds` to just the new/changed tests when iterating quickly;
   omit `testIds` for a full pass before shipping.
4. Cross-check TestSprite's findings against the project's own Pest test
   suite (`php artisan test`) — TestSprite catches UI/flow issues Pest
   won't (visual breakage, JS errors, broken links); Pest catches
   business-logic/financial-invariant issues TestSprite won't reliably catch
   (ledger correctness, AML rule behavior). Use both — neither replaces the
   other for this project.

## Gotchas
1. Never call `testsprite_bootstrap` on an already-bootstrapped project —
   check for `.testsprite/config.json` first.
2. Always pass `serverMode: 'production'` — there is no dev server here.
3. Resolve the real port/URL before running — do not trust the tool's
   `localPort: 5173` default.
4. Test each of the 6 surfaces (admin/company/merchant/agent/public/API)
   separately — a single `needLogin: true` pass cannot cover all of them.
5. This project uses SQLite for tests (`RefreshDatabase`) — if TestSprite
   needs seed data, prefer the project's existing factories
   (`User::factory()`, `Company::factory()->payrollReady()`, etc.) over
   inventing new fixtures, to stay consistent with the Pest suite.
