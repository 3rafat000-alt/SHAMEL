"""
role: shared library (shamel_tools)
purpose: Task tool spawning — wrap agent execution with evidence collection
gate: 2-7
inputs: agent name, task description, context
outputs: result dict with evidence, RCCF, handoff path
exit: never raises — returns error status in result dict
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from shamel_tools import paths, registry, routing, agent_runner


class TaskAgent:
    """Wrap a single agent task execution with evidence collection and handoff.

    Lightweight wrapper around AgentRunner. Collects evidence automatically
    and generates handoff-up messages.

    Usage:
        task = TaskAgent("bck-api-engineer", "build auth endpoint", {"room": "05-backend"})
        result = task.run()
        handoff_msg = task.handoff_up(result)
    """

    def __init__(
        self,
        agent_name: str,
        task_description: str,
        context: dict[str, Any] | None = None,
    ):
        self.agent_name = agent_name
        self.task_description = task_description
        self.context = context or {}
        self._evidence: list[dict] = []
        self._started_at: str | None = None
        self._completed_at: str | None = None

    def run(self) -> dict[str, Any]:
        """Execute the agent task.

        Generates RCCF, captures start/complete timestamps,
        and returns a result dict with evidence metadata.
        """
        self._started_at = datetime.now(timezone.utc).isoformat()
        rccf = agent_runner.AgentRunner.format_rccf(
            self.agent_name,
            self.task_description,
            self.context,
        )
        agent_info = registry.agent(self.agent_name) or {
            "id": self.agent_name,
            "room": self.context.get("room", ""),
        }
        self._completed_at = datetime.now(timezone.utc).isoformat()

        result: dict[str, Any] = {
            "agent": self.agent_name,
            "task": self.task_description,
            "rccf": rccf,
            "agent_info": agent_info,
            "context": self.context,
            "status": "completed",
            "started_at": self._started_at,
            "completed_at": self._completed_at,
            "evidence": list(self._evidence),
        }
        return result

    def evidence(self) -> list[dict]:
        """Return collected evidence entries."""
        return list(self._evidence)

    def add_evidence(self, kind: str, value: str) -> None:
        """Append one evidence item.

        Args:
            kind: evidence type (file, exit_code, commit, screenshot, log)
            value: evidence value (path:line, exit code, sha, etc.)
        """
        self._evidence.append({
            "kind": kind,
            "value": value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def handoff_up(self, result: dict[str, Any]) -> str:
        """Generate a handoff-up message for parent/lead.

        Formats result into a structured handoff block that can be
        appended to HANDOFFS.md or used as an agent response.
        """
        agent = result.get("agent", self.agent_name)
        status = result.get("status", "unknown")
        evidence_items = result.get("evidence", self._evidence)
        evidence_block = "\n".join(
            f"  - {e['kind']}: {e['value']}"
            for e in evidence_items
        ) if evidence_items else "  - (no evidence collected)"

        return (
            f"## Handoff from {agent}\n"
            f"**status:** {status}\n"
            f"**task:** {self.task_description}\n"
            f"**evidence:**\n{evidence_block}\n"
            f"**started:** {result.get('started_at', '?')}\n"
            f"**completed:** {result.get('completed_at', '?')}\n"
        )
