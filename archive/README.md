# Archive — Retired Generations

> ⛔ These are tombstones, not living code. Each directory holds the remains of a prior generation, captured and preserved for reference. No file here is loaded by the live system. No hook, skill, or agent reads from here.

## Index

| Directory | Generation | What it was | Content rescued into SHAMEL | Tag | ADR |
|-----------|-----------|-------------|----------------------------|-----|-----|
| `g1-opencode/` | G1 (OpenCode `.opencode/`) | Original system: 114 tools + 16 room scripts + browser-eyes + gate checklists | 114 tools → `core/rooms/*/tools/`; browser-eyes → `engine/scanners/`; checklists → `core/gates/checklists/` | `archive/g1-opencode` | ADR-001 |
| `g2-engine-v5/` | G2 (engine/ v5) | Bash→Python tooling, `sofi` CLI, `sofi_tools` 24 modules, templates, scanners | Article 11 intake concept; scanners → `engine/scanners/` ; `sofi_tools` base logic absorbed into `engine/shamel_tools/` | `archive/g2-engine-v5` | ADR-001 |
| `g4-org-rooms/` | G4 (org-rooms 100 personas) | 105 Arabic personas + 7-agent rooms + 6-column governance | Frontmatter governance merged into `core/rooms/*/agents/*.md`; persona canon → `brain/org/PERSONAS.yaml` via mapping table | `archive/g4-org-rooms` | ADR-001/003 |
| `g6-orchestrator-fork/` | G6 (orchestrator fork) | Python orchestrator (`ceo_agent.py`, `translator_gateway.py`, `state_db.py`) + n8n/WhatsApp pipeline | Pipeline → `engine/shamel_tools/pipeline/` ; orchestrator architecture absorbed | `archive/g6-orchestrator-fork` | ADR-001/002 |
| (Dashboard v5) | Dashboard v5 | `index.html` — 30-agent visual dashboard | None — to be rebuilt on SHAMEL data | `archive/dashboard-v5` | ADR-001 |

## Manifest format

Each directory contains `MANIFEST.md` with:
- What this generation contained
- When and why it was retired
- What was rescued and where it lives
- Snapshot SHA/tag reference
- Any orphaned content that may still be useful
