---
name: mcp-capability-map
description: >
  What MCP servers/tools this SHAMEL environment already has connected for
  PRJ-SAKK work, and a ranked shortlist of additional MCPs surveyed from
  mcpmarket.com that would help the team's actual stack (Laravel/PHP,
  Flutter, Stripe Issuing, CCPayment, bare-metal php-fpm+Caddy). None of the
  shortlisted additions are installed — they need the project owner's
  decision (credentials/cost/access). Use when scoping what tooling a room
  needs before reaching for ad-hoc web research. Recommended for: all room
  leads, especially ops-cloud-engineer, sec-lead, qa-lead, mob-lead.
user-invocable: true
metadata:
  project: PRJ-SAKK
  category: tooling
  version: "1.0.0"
  surveyed: "2026-07-11, via res-web-scout agent against mcpmarket.com"
---

# MCP Capability Map — PRJ-SAKK

## Already connected in this environment (verified via ToolSearch, 2026-07-11)
- **TestSprite** — automated test-plan generation + execution. See the
  companion `testsprite-testing` skill for PRJ-SAKK-specific adaptation
  (this app has no Vite dev server, unlike TestSprite's default assumptions).
- **Stripe** (`claude_ai_Stripe`) — docs search, API search, account info,
  and a payment-implementation planner. Note: the planner tool is scoped to
  Payments/Checkout/Billing — PRJ-SAKK uses Stripe **Issuing**, a different
  product; see the companion `stripe-issuing-integration` skill.
- General productivity MCPs also connected but not stack-specific to SAKK's
  engineering work: Figma, Gmail, Google Calendar/Drive, Lucid, Meta Ads,
  Miro, Notion, Postman, Resend, Supabase, Vercel, GoDaddy. Relevant only if
  a specific task calls for them (e.g. Postman for API-contract work, Figma
  if design work moves off pure Blade/CSS).
- No CCPayment-specific MCP exists on the market (confirmed by survey) — the
  `ccpayment-integration` skill's vendor reference (an official docs clone)
  is the substitute.

## Shortlist — surveyed from mcpmarket.com, ranked, NOT installed
Each needs an explicit owner decision (most require credentials; a few are
zero-config but still worth a deliberate yes/no). Do not install any of
these without asking first — several touch production infrastructure or
external accounts.

| # | MCP | What it does | Room | Credentials needed? |
|---|---|---|---|---|
| 1 | Laravel Artisan MCP | Runs whitelisted `artisan` commands through the agent (migrations, queue inspection, cache clears) | backend | No — but MUST configure a command whitelist so agents can't run `migrate:fresh`/`db:wipe` unattended |
| 2 | Laravel MCP Server Core | Exposes route table + DB schema + diagnostics without grepping the codebase | backend | No |
| 3 | Playwright MCP (Microsoft official) | Real browser automation/E2E — distinct from TestSprite's generated-test focus; good for exploratory QA and visual regression on the 3 partner portals | quality, frontend | No — needs local Chromium/Playwright binaries |
| 4 | Sentry MCP | Query production error groups/stack traces/release health directly | backend, devops | Yes — Sentry account + API token (paid tier likely needed at fintech volume) |
| 5 | Security Analyzer / SAST MCP | Wraps Semgrep/Bandit/TruffleHog + SBOM generation behind one interface | security | No (wraps free OSS scanners) — review which binaries it shells out to before granting execution rights |
| 6 | Socket MCP | Supply-chain risk scoring for `composer.json`/`composer.lock` (confirmed Composer/Packagist support, not just npm) | security | Yes — Socket.dev API key (free tier exists) |
| 7 | SSH MCP server | Restart php-fpm, reload Caddy, tail logs, check systemd units — relevant since this is bare-metal, not Docker/K8s | devops | Yes — SSH key. **Highest-risk item on this list** — scope to a locked-down deploy user on staging only, never a root/prod key handed to an unattended agent |
| 8 | Flutter MCP + Pub.dev MCP | Keeps generated Dart/Flutter code current against live docs/package metadata | mobile | No |
| 9 | Redis MCP (official, Redis Inc.) | Only relevant if Laravel queues/cache/sessions move to Redis (currently OTP throttling/queues may be DB/file-based — confirm before adding) | data, backend | Yes — Redis connection creds |
| 10 | Generic MySQL/SQLite MCP | Ad-hoc read-only query + schema-diff for the data room | data | Yes — DB creds; **never grant write access to production** |

## The one gap the market can't close
**No viable SMS-OTP MCP exists for Syria.** Twilio (the dominant SMS MCP on
mcpmarket.com) formally stopped delivering SMS/voice/email to Syrian numbers
on 2025-09-15. This is a known, already-flagged pending business decision
for PRJ-SAKK (SMS OTP vendor selection) — it requires a custom integration
with a regional aggregator or local carrier gateway (Syriatel/MTN Syria),
not an MCP install. Don't waste time looking for a marketplace shortcut here.

## How to act on this list
1. Anything marked "No" credentials-needed and clearly useful (Laravel
   Artisan/Core MCP, Playwright, Flutter/Pub.dev) is low-risk to propose
   installing — still surface it to the project owner once, don't silently
   add MCP servers to the environment config.
2. Anything requiring credentials (Sentry, Socket, SSH, Redis, DB) is a
   real access/cost decision — present the shortlist, let the owner pick.
3. The SSH MCP in particular should never be added without a written scope
   (which host, which user, which commands) agreed with the owner first —
   it is the single highest blast-radius item here.
