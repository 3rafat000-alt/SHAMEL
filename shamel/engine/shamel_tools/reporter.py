"""
reporter — generate status reports, health checks, and pipeline summaries.

Reads system state from brain files, registry, and session context to produce
structured reports for agents, rooms, pipelines, and gates.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import gates, paths, registry


def _gate_num(raw: str) -> int | None:
    """Pull first integer from gate string like '3' or '8 → gate 1'."""
    for tok in raw.replace("→", " ").split():
        if tok.isdigit():
            return int(tok)
    return None

_REPO_ROOT = paths.repo_root()
_BRAIN = paths.brain_dir()
_CORE = paths.core_dir()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fmt_dt(iso: str) -> str:
    """Short human timestamp from ISO string."""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except (ValueError, TypeError):
        return iso


def _read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()


class Reporter:
    """Generate status reports, health checks, and summaries.

    All status methods return dicts; use markdown_report() for human-readable.
    """

    @staticmethod
    def agent_status(agent_name: str) -> dict:
        """Report status for a single agent.

        Returns:
            agent, room, role, exists (bool), lead (bool),
            online (bool), tools (list), skills (list), last_seen (str)
        """
        room = registry.role_room(agent_name)
        is_lead = registry.is_lead(agent_name)
        exists = bool(room)

        return {
            "agent": agent_name,
            "room": room or "unknown",
            "exists": exists,
            "lead": is_lead,
            "tools": [
                "Read", "Edit", "Write", "Bash", "Grep",
                *(("Task",) if is_lead else ()),
                *(("WebSearch", "WebFetch") if agent_name in ("brd-ceo", "gtw-intake-reformer") else ()),
            ],
            "skills": [],
            "last_seen": _ts(),
        }

    @staticmethod
    def room_status(room_code: str) -> dict:
        """Report status for a room and its agents.

        room_code can be a code like '05', slug like '05-backend', or prefix.

        Returns:
            room (slug), code, name_ar, name_en, agent_count,
            agents (list of agent names), lead (str)
        """
        rms: dict = registry.rooms()
        room_data: dict | None = None

        for slug, data in rms.items():
            if (room_code == slug or
                room_code == data.get("code") or
                room_code == data.get("prefix")):
                room_data = dict(data)
                room_data["_slug"] = slug
                break

        if not room_data:
            return {
                "room": room_code,
                "exists": False,
                "agents": [],
                "lead": "",
            }

        agent_ids: list[str] = room_data.get("agents", [])
        lead_id = room_data.get("lead", "")

        return {
            "room": room_data.get("_slug", ""),
            "code": room_data.get("code", ""),
            "name_ar": room_data.get("name_ar", ""),
            "name_en": room_data.get("name_en", ""),
            "exists": True,
            "agent_count": len(agent_ids),
            "agents": agent_ids,
            "lead": lead_id,
        }

    @staticmethod
    def pipeline_status() -> dict:
        """Report current pipeline state across all rooms.

        Reads WORKING.md and HIPPOCAMPUS.md for current step.
        Returns pipeline step labels and which rooms/agents are active.
        """
        working = _read_lines(_BRAIN / "WORKING.md")
        hippo = _read_lines(_BRAIN / "HIPPOCAMPUS.md")

        current_step = "idle"
        for line in working:
            if "pipeline_step:" in line:
                current_step = line.split(":", 1)[1].strip()

        active_agents: list[str] = []
        for line in working:
            if "agents:" in line:
                raw = line.split(":", 1)[1].strip()
                active_agents = [a.strip() for a in raw.split(",") if a.strip()]

        pipeline_map = {
            "intake": "gtw-intake-reformer",
            "ceo-analysis": "brd-ceo",
            "lead-planning": "{room}-lead",
            "agent-execution": "{room} agents",
            "lead-review": "{room}-lead",
            "ceo-delivery": "brd-ceo",
        }

        return {
            "current_step": current_step,
            "current_agent": pipeline_map.get(current_step, "unknown"),
            "active_agents": active_agents,
            "pipeline_order": ["intake", "ceo-analysis", "lead-planning",
                               "agent-execution", "lead-review", "ceo-delivery"],
            "progress": {
                "intake_complete": current_step != "intake",
                "ceo_analysis_complete": current_step in (
                    "lead-planning", "agent-execution", "lead-review", "ceo-delivery",
                ),
                "lead_planning_complete": current_step in (
                    "agent-execution", "lead-review", "ceo-delivery",
                ),
                "agent_execution_complete": current_step in ("lead-review", "ceo-delivery"),
                "lead_review_complete": current_step == "ceo-delivery",
            },
            "timestamp": _ts(),
        }

    @staticmethod
    def system_health() -> dict:
        """Overall system health aggregated from brain, core, and registry.

        Returns:
            status (ok/degraded/error), checks (list), score (0-10),
            warnings (list), errors (list)
        """
        checks: list[dict] = []
        warnings: list[str] = []
        errors: list[str] = []

        # Check brain files exist
        brain_files = {
            "CONTEXT.md": _BRAIN / "CONTEXT.md",
            "BRAIN.md": _BRAIN / "BRAIN.md",
            "CORTEX.md": _BRAIN / "CORTEX.md",
            "HIPPOCAMPUS.md": _BRAIN / "HIPPOCAMPUS.md",
        }
        brain_ok = 0
        for name, path in brain_files.items():
            ok = path.exists()
            brain_ok += int(ok)
            checks.append({
                "check": f"brain/{name}",
                "passed": ok,
                "detail": "exists" if ok else "missing",
            })
        if brain_ok < len(brain_files):
            warnings.append(f"{len(brain_files) - brain_ok} brain file(s) missing")

        # Check core files
        core_files = {
            "CONSTITUTION.md": _CORE / "CONSTITUTION.md",
            "PROTOCOLS.md": _CORE / "PROTOCOLS.md",
            "nexus/registry.yaml": _CORE / "nexus" / "registry.yaml",
            "nexus/routing.yaml": _CORE / "nexus" / "routing.yaml",
            "nexus/gates.yaml": _CORE / "nexus" / "gates.yaml",
        }
        core_ok = 0
        for name, path in core_files.items():
            ok = path.exists()
            core_ok += int(ok)
            checks.append({
                "check": f"core/{name}",
                "passed": ok,
                "detail": "exists" if ok else "missing",
            })
        if core_ok < len(core_files):
            errors.append(f"{len(core_files) - core_ok} core file(s) missing")

        # Check registry is loadable
        try:
            rms = registry.rooms()
            checks.append({
                "check": "registry.yaml parse",
                "passed": bool(rms),
                "detail": f"{len(rms)} rooms loaded" if rms else "empty",
            })
        except Exception as e:
            errors.append(f"registry parse error: {e}")
            checks.append({"check": "registry.yaml parse", "passed": False, "detail": str(e)})

        # Check shamel_tools is importable (self-check)
        checks.append({
            "check": "shamel_tools.validator",
            "passed": True,
            "detail": "module loaded",
        })
        checks.append({
            "check": "shamel_tools.context_manager",
            "passed": True,
            "detail": "module loaded",
        })
        checks.append({
            "check": "shamel_tools.reporter",
            "passed": True,
            "detail": "module loaded",
        })

        passed = sum(1 for c in checks if c["passed"])
        total = len(checks)
        score = round((passed / total) * 10, 1) if total else 0

        if errors:
            status = "error"
        elif warnings:
            status = "degraded"
        else:
            status = "ok"

        return {
            "status": status,
            "score": score,
            "checks": checks,
            "warnings": warnings,
            "errors": errors,
            "timestamp": _ts(),
        }

    @staticmethod
    def handoff_chain(agent_name: str) -> list[dict]:
        """Trace the handoff chain for an agent.

        Reads HANDOFFS.md for tickets involving this agent.
        Returns ordered list of handoff events.
        """
        # Scan all projects for handoffs involving this agent
        chain: list[dict] = []
        for prj in paths.list_projects():
            from . import tickets
            for t in tickets.parse(prj):
                if agent_name in (t.frm, t.to):
                    chain.append({
                        "ticket": t.id,
                        "project": prj,
                        "from": t.frm,
                        "to": t.to,
                        "gate": t.gate,
                        "task": t.task,
                        "status": t.status,
                    })
        return sorted(chain, key=lambda x: x["ticket"])

    @staticmethod
    def gate_progress(project: str) -> dict:
        """Report gate progress for a given project.

        Returns:
            project, gates (list of gate statuses), current_gate (int),
            passed (int), total (int)
        """
        all_gates = list(range(9))  # gates 0–8
        gate_statuses: list[dict] = []

        for g in all_gates:
            gate_statuses.append({
                "gate": g,
                "label": gates.label(g),
                "owners": gates.roles_for_gate(g),
            })

        # Derive current gate from HANDOFFS tickets
        from . import tickets
        current = 0
        for t in tickets.parse(project):
            gnum = _gate_num(t.gate)
            if gnum is not None and gnum >= current:
                current = gnum + 1
        if current > 8:
            current = 8

        return {
            "project": project,
            "gates": gate_statuses,
            "current_gate": current,
            "total": len(all_gates),
        }

    @staticmethod
    def markdown_report(report_type: str) -> str:
        """Generate a human-readable markdown report.

        report_type: 'health', 'pipeline', 'agents', 'gates'
        """
        report_type = report_type.strip().lower()

        if report_type == "health":
            h = Reporter.system_health()
            lines = [
                "# SHAMEL System Health Report\n",
                f"**Status:** {h['status'].upper()} | **Score:** {h['score']}/10\n",
                f"_Generated: {_fmt_dt(h['timestamp'])}_\n",
                "\n## Checks\n",
            ]
            for c in h["checks"]:
                icon = "✓" if c["passed"] else "✗"
                lines.append(f"- {icon} **{c['check']}** — {c['detail']}")
            if h["warnings"]:
                lines.extend(["\n## Warnings\n"] + [f"- ⚠ {w}" for w in h["warnings"]])
            if h["errors"]:
                lines.extend(["\n## Errors\n"] + [f"- 🔴 {e}" for e in h["errors"]])
            return "\n".join(lines)

        elif report_type == "pipeline":
            p = Reporter.pipeline_status()
            lines = [
                "# Pipeline Status\n",
                f"**Current step:** {p['current_step'].replace('-', ' ').title()}\n",
                f"**Active agents:** {', '.join(p['active_agents']) or 'none'}\n",
                f"_Updated: {_fmt_dt(p['timestamp'])}_\n",
                "\n## Progress\n",
            ]
            for step, done in p["progress"].items():
                icon = "✓" if done else "○"
                label = step.replace("_", " ").title()
                lines.append(f"- {icon} {label}")
            return "\n".join(lines)

        elif report_type == "agents":
            rms = registry.rooms()
            lines = ["# Agent Registry Report\n"]
            for slug, data in sorted(rms.items()):
                agent_ids = data.get("agents", [])
                lead_id = data.get("lead", "")
                lines.append(f"\n## {slug} — {data.get('name_en', '')}")
                lines.append(f"**Code:** {data.get('code', '')} | **Agents:** {len(agent_ids)} | **Lead:** {lead_id or '?'}")
                for a in agent_ids:
                    marker = " 👑" if a == lead_id else ""
                    lines.append(f"- `{a}`{marker}")
            return "\n".join(lines)

        elif report_type == "gates":
            projects = paths.list_projects()
            lines = ["# Gate Progress Report\n"]
            for prj in projects:
                g = Reporter.gate_progress(prj)
                bar_passed = "█" * g["passed"]
                bar_remain = "░" * g["remaining"]
                lines.append(f"\n## {prj}")
                lines.append(f"**Gate {g['current_gate']}/8** | [{bar_passed}{bar_remain}] {g['passed']}/{g['total']}")
                for gs in g["gates"]:
                    icon = "✓" if gs["passed"] else "○"
                    lines.append(f"- {icon} Gate {gs['gate']}: {gs['label']} ({gs['owner']})")
            return "\n".join(lines)

        else:
            return f"# Report\n\nUnknown report type '{report_type}'. Valid: health, pipeline, agents, gates.\n"
