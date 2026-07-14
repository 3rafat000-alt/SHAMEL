"""
role: shared library (shamel_tools)
purpose: spawn and manage agent execution with RCCF task format
gate: 2-7
inputs: agent name, task string, context dict
outputs: result dict with RCCF evidence and handoff chain
exit: never raises — returns error status in result dict
"""
from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime, timezone
from typing import Any

from shamel_tools import paths, registry, routing, brain, tickets, guard


class AgentRunner:
    """Spawn and manage agent execution.

    Generates RCCF (Request for Code Creation Form) task descriptions,
    validates handoffs, and tracks evidence.

    Usage:
        runner = AgentRunner()
        result = runner.spawn("bck-api-engineer", "build user auth endpoint")
    """

    HANOFF_SIG_RE = re.compile(
        r"evidence:\s*\n"
        r"(?:\s*-\s*(?:file:\S+:\d+|exit code: \d+|commit: \S+|screenshot: \S+)\s*\n)+",
        re.MULTILINE | re.IGNORECASE,
    )

    @classmethod
    def spawn(
        cls,
        agent_name: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Generate an RCCF task for an agent.

        Returns dict with agent info, rendered task, route, and metadata.
        """
        ctx = context or {}
        agent_info = registry.agent(agent_name)
        if not agent_info:
            agent_info = {"id": agent_name, "room": ctx.get("room", "")}

        route_info: dict = {}
        try:
            route_info = routing.route_for(agent_name)
        except KeyError:
            route_info = {"model": "workhorse", "effort": "medium", "caveman": "full"}

        rccf = cls.format_rccf(agent_name, task, ctx)
        result = {
            "agent": agent_name,
            "task": task,
            "rccf": rccf,
            "route": route_info,
            "agent_info": agent_info,
            "context": ctx,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "ready",
            "evidence": [],
        }
        return result

    @classmethod
    def spawn_with_handoff(
        cls,
        agent_name: str,
        task: str,
        parent_agent: str,
        room: str,
    ) -> dict[str, Any]:
        """Generate an RCCF and record a handoff ticket.

        Creates a handoff from parent_agent to agent_name within the given room.
        """
        result = cls.spawn(agent_name, task, {"room": room, "parent": parent_agent})
        try:
            tkt_id = tickets.next_id(room) if hasattr(tickets, "next_id") else f"TKT-{uuid.uuid4().hex[:4]}"
            if hasattr(tickets, "append_ticket"):
                tickets.append_ticket(
                    room,
                    tkt_id=tkt_id,
                    gate="0",
                    frm=parent_agent,
                    to=agent_name,
                    task=task,
                    expected=f"completion evidence for {task[:40]}",
                    status="open",
                )
            result["ticket"] = tkt_id
        except Exception as e:
            result["ticket_error"] = str(e)
        result["status"] = "handoff_created"
        return result

    @classmethod
    def validate_handoff(cls, result: dict[str, Any]) -> bool:
        """Check that result dict carries required evidence fields.

        Validates presence of: file:line references, exit codes, or commit hashes.
        """
        if not isinstance(result, dict):
            return False
        evidence = result.get("evidence") or []
        if not evidence:
            text = json.dumps(result, default=str)
            return bool(cls.HANOFF_SIG_RE.search(text))
        for item in evidence:
            if isinstance(item, dict):
                if any(k in item for k in ("file", "exit_code", "commit", "screenshot")):
                    return True
            elif isinstance(item, str):
                if re.match(r"^\S+:\d+", item):
                    return True
        return False

    @classmethod
    def format_rccf(
        cls,
        agent_name: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Format a Request for Code Creation Form string.

        RCCF is the SHAMEL standard task assignment format carrying
        agent identity, task, context, and routing.
        """
        ctx = context or {}
        agent_info = registry.agent(agent_name)
        route_info: dict = {}
        try:
            route_info = routing.route_for(agent_name)
        except KeyError:
            pass

        fields = {
            "agent": agent_name,
            "role": agent_info.get("title", agent_name),
            "room": agent_info.get("room", ctx.get("room", "")),
            "task": task,
            "route": f"{route_info.get('model', '')} · {route_info.get('effort', '')} · {route_info.get('caveman', '')}",
            "model_id": route_info.get("model_id", ""),
            "priority": ctx.get("priority", "—"),
        }
        context_block = ""
        if ctx:
            items = "\n".join(f"  {k}: {v}" for k, v in ctx.items()
                              if k not in ("room", "priority"))
            if items:
                context_block = f"\ncontext:\n{items}"

        return (
            f"RCCF: {agent_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"agent: {fields['agent']}\n"
            f"role: {fields['role']}\n"
            f"room: {fields['room']}\n"
            f"task: {fields['task']}\n"
            f"route: {fields['route']}\n"
            f"model: {fields['model_id']}\n"
            f"priority: {fields['priority']}"
            f"{context_block}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"BEFORE: read STATE/CONTEXT/HANDOFFS. AFTER: checkpoint + evidence.\n"
        )
