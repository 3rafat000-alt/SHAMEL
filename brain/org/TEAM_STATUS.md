---
title: TEAM_STATUS
owner: gtw-dispatcher
description: "@generated — per-room team health summary"
generated: false
---

# 📊 SOFI AI — Team Status (snapshot 2026-06-24)

Where the agent enterprise stands today. Doctrine intact: **Design is Truth · few token do trick · big brain small mouth.** 🪨

## The team
- **30 agents · 5 tiers + CEO** — all spawnable (`.claude/agents/sofi-*.md`), each with a persona spec (`engine/agents/**`).
- **9-gate lifecycle** (0 Inception → 8 Observe→loop), no skipping, validated by `sofi gate-check`.
- **Company brain** per project (`projects/<PRJ>/_context/{STATE,CONTEXT,DECISIONS,HANDOFFS}.md`), isolated by PRJ-ID.
- **Governed tooling** — `sofi_tools` library + `sofi` dispatcher, GOVERNANCE enforced (scope sandbox, net policy, secret scan, exit-code gating).

## What's new (this build cycle)
| Upgrade | State | Where |
|---|---|---|
| 🧊 **FossFLOW** isometric diagrams | 🛠️ built | `…/principal-system-architect/fossflow_export.py` (Gate 3) |
| 🎨 **Design taste** skill | ✅ implemented | `.claude/skills/sofi-design-taste/SKILL.md` |
| 🏢 **Escalation chain** | ✅ applied | `tickets.escalate()` + `sofi escalate` |
| 🧩 **Parallel squads** | ✅ command | `sofi squad <PRJ> <gate>` (gates 3·4·5) |
| 📇 **Power discovery** | ✅ command | `sofi powers` |
| 🎯 **Success metrics** | ✅ 30/30 | `success_metric:` in every spec frontmatter |
| 📜 **Operating contract** | ✅ upgraded | `protocols/00-operating-system.md` (arm-up, escalate, parallel, metric) — all 30 inherit |
| 🔫 **Armed wielders** | ✅ 9/9 | architects→fossflow, designers→taste, CEO→escalate |

## CLI surface (22 commands)
`projects · brain · route · gate-check · dispatch · squad · powers · handoff · escalate · scratch · sync · checkpoint · claim · release · worktree · gate-merge · gate-tag · git-check · domain · tunnel · tools · doctor`

## Powers status (`sofi powers`)
- fossflow → **pilot** (tool built) · taste-skill → **implemented** · agency-agents → **applied** (escalation) · armory → **reference**

## Health
`sofi doctor` PASS · 32 routes · 14 net-roles · **30 subagents ↔ 30 specs** · **registry skill paths exist** · library compiles · board blank.
> `doctor` now gates agent-wiring parity and registry-cited `.claude/skills/*` existence — a "status: implemented" claim fails CI if its SKILL.md is missing.

## Public face
Landing page `index.html` — bilingual EN/AR, reference-matched identity (three.js starfield, SVG icons, theme toggle). Sections: Hero · Nine Gates · Commands · **Superpowers** · Roster · Best Practices · Footer.

## Open / next
- Optional: `sofi verify` to check artifacts against each role's `success_metric`.
- Optional future wing: Growth & Ops (Product/Marketing/Finance) — gated separately, never blocking the build cascade.
