# Quality/QA room — PRJ-SAKK project skills

Canonical location: `~/Desktop/SHAMEL/.claude/skills/<name>/SKILL.md`

- **testsprite-testing** — how to drive the connected TestSprite MCP against
  PRJ-SAKK correctly. Critical adaptation: this project has NO Vite/npm dev
  server (pure server-rendered Blade over php-fpm+Caddy), so TestSprite's
  default `localPort`/`serverMode` assumptions are wrong out of the box.
  Also maps PRJ-SAKK's 6 distinct authenticated surfaces (admin/company/
  merchant/agent/public/API) to separate test plans rather than one pass.
  Read this BEFORE calling any `mcp__TestSprite__*` tool on this project.

Use alongside the existing Pest test suite (`php artisan test`) — TestSprite
and Pest catch different failure classes here (UI/flow vs financial-invariant
correctness); the skill explains which to reach for when.
