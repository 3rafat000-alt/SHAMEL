"""
validator — validate system state, agent actions, pipeline integrity.
Enforces SHAMEL protocols (P-01 through P-13) at runtime with structured
violation reporting and severity classification (L1–L4).

Every check returns a dict with: valid (bool), violations (list), severity (str).
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

from . import paths, registry

# ── Severity levels matching Protocol 10 (Emergency Classification) ────────────
SEVERITY_ORDER = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
SEVERITY_LABELS = {
    "L1": "Procedural — warning issued",
    "L2": "Moderate — task paused, Lead notified",
    "L3": "High — pipeline halt, escalation required",
    "L4": "Critical — session invalidation, constitutional violation",
}


def severity_of(violation: str) -> str:
    """Return L1–L4 based on violation content heuristics.

    Matches protocol-level language to severity bands.
    """
    v_lower = violation.lower()
    if any(w in v_lower for w in ("constitutional", "secret", "veto", "fabricated", "conceal")):
        return "L4"
    if any(w in v_lower for w in ("bypass", "skipping", "pipeline halt", "chain skip", "boundary", "cross-room", "direct delivery")):
        return "L3"
    if any(w in v_lower for w in ("missing evidence", "handoff", "incomplete", "rejected", "acceptance")):
        return "L2"
    if any(w in v_lower for w in ("format", "redundant", "verbose", "header", "log")):
        return "L1"
    return "L2"


# ── Pipeline step validation ──────────────────────────────────────────────────

_PIPELINE_STEPS = frozenset({
    "intake",           # gtw-intake-reformer
    "ceo-analysis",     # brd-ceo
    "lead-planning",    # room lead
    "agent-execution",  # room agents
    "lead-review",      # room lead
    "ceo-delivery",     # brd-ceo → user
})

_PIPELINE_ORDER = ["intake", "ceo-analysis", "lead-planning",
                   "agent-execution", "lead-review", "ceo-delivery"]

# Hardcoded known boardroom + gateway agents. Room agents resolved by pattern.
_KNOWN_STEPS = {
    "gtw-intake-reformer": "intake",
    "brd-ceo": "ceo-analysis",
    "brd-cpo": "ceo-analysis",
    "brd-cto": "ceo-analysis",
    "brd-cqo": "ceo-analysis",
    "brd-cso": "ceo-analysis",
    "brd-chief-of-staff": "ceo-analysis",
    "brd-arbiter": "ceo-analysis",
}


def _resolve_step(agent_name: str) -> str:
    """Determine pipeline step for an agent by name pattern."""
    if agent_name in _KNOWN_STEPS:
        return _KNOWN_STEPS[agent_name]
    if agent_name.startswith("brd-"):
        return "ceo-analysis"
    if agent_name.startswith("gtw-intake"):
        return "intake"
    if agent_name.startswith("gtw-"):
        return "lead-planning"
    if registry.is_lead(agent_name):
        return "lead-planning"
    return "agent-execution"


class Validator:
    """Validate system state, agent actions, and pipeline integrity.

    All methods return structured dicts for machine consumption.
    """

    @staticmethod
    def check_pipeline_step(agent_name: str, step: str) -> dict:
        """Check if *step* is the correct pipeline step for *agent_name*.

        Returns:
            valid: bool
            expected_step: str | None
            violations: list[str]
            severity: str
        """
        violations: list[str] = []
        if step not in _PIPELINE_STEPS:
            violations.append(f"unknown pipeline step '{step}'; must be one of {sorted(_PIPELINE_STEPS)}")
        expected = _resolve_step(agent_name)
        if expected and step != expected:
            violations.append(
                f"P-01.2 violation: agent '{agent_name}' at step '{step}' "
                f"— expected '{expected}'. Sequential gate order: {' → '.join(_PIPELINE_ORDER)}"
            )
        return {
            "valid": len(violations) == 0,
            "expected_step": expected,
            "violations": violations,
            "severity": max((severity_of(v) for v in violations), key=lambda s: SEVERITY_ORDER.get(s, 0)) if violations else "L0",
        }

    @staticmethod
    def check_handoff(from_agent: str, to_agent: str) -> dict:
        """Validate handoff against Protocol 02 rules.

        Checks: room boundary, lead mediation, ticket requirement,
        agent existence in registry.
        """
        violations: list[str] = []

        frm_room = registry.role_room(from_agent)
        to_room = registry.role_room(to_agent)

        if not frm_room:
            violations.append(f"P-02.7: unknown origin agent '{from_agent}' — not in registry")
        if not to_room:
            violations.append(f"P-02.7: unknown target agent '{to_agent}' — not in registry")

        if frm_room and to_room and frm_room != to_room:
            frm_lead = registry.is_lead(from_agent)
            to_lead = registry.is_lead(to_agent)
            is_board_gateway = (
                from_agent.startswith(("brd-", "gtw-")) or
                to_agent.startswith(("brd-", "gtw-"))
            )
            if not (frm_lead or to_lead or is_board_gateway):
                lead = registry.room_lead(frm_room) or f"{frm_room}-lead"
                violations.append(
                    f"P-02.7 violation: cross-room handoff {from_agent} ({frm_room}) → "
                    f"{to_agent} ({to_room}) skips both room Leads. "
                    f"Must route via {lead}."
                )

        return {
            "valid": len(violations) == 0,
            "from_room": frm_room or "",
            "to_room": to_room or "",
            "needs_ticket": frm_room != to_room if (frm_room and to_room) else True,
            "violations": violations,
            "severity": max((severity_of(v) for v in violations), key=lambda s: SEVERITY_ORDER.get(s, 0)) if violations else "L0",
        }

    @staticmethod
    def check_room_boundary(agent: str, target_room: str) -> dict:
        """Check if *agent* may address *target_room*.

        Boardroom (brd-*) and Gateway (gtw-*) may address any room.
        Other agents may only address their own room or reach via Lead.
        """
        violations: list[str] = []
        agent_room = registry.role_room(agent)

        if not agent_room:
            violations.append(f"unknown agent '{agent}' — not in registry")

        room_codes: set[str] = set()
        for rc, rd in registry.rooms().items():
            room_codes.add(rd.get("code", ""))
            room_codes.add(rc)

        if target_room not in room_codes:
            violations.append(f"unknown target room '{target_room}'")

        if agent_room and target_room != agent_room:
            if not agent.startswith(("brd-", "gtw-")):
                violations.append(
                    f"P-07.5 violation: agent '{agent}' (room {agent_room}) "
                    f"addressing room '{target_room}' without Lead mediation. "
                    f"Cross-room communication requires Lead."
                )

        return {
            "valid": len(violations) == 0,
            "agent_room": agent_room or "",
            "target_room": target_room,
            "violations": violations,
            "severity": max((severity_of(v) for v in violations), key=lambda s: SEVERITY_ORDER.get(s, 0)) if violations else "L0",
        }

    @staticmethod
    def check_evidence(result: dict) -> list[dict]:
        """Validate evidence against Protocol 03.

        Accepts a result dict with optional keys:
            code_changes: list[dict] — each {path, line, change}
            commands: list[dict] — each {command, exit_code, output}
            research: list[dict] — each {url, extract}
            screenshots: list[str] — paths
            tests: list[dict] — each {suite, passed, output}

        Returns a list of evidence checks, each:
            {check: str, passed: bool, detail: str}
        """
        checks: list[dict] = []
        now = datetime.now(timezone.utc).isoformat()

        code_changes = result.get("code_changes") or []
        commands = result.get("commands") or []
        research = result.get("research") or []
        screenshots = result.get("screenshots") or []
        tests = result.get("tests") or []

        # P-03.1: evidence completeness
        if not any([code_changes, commands, research, screenshots, tests]):
            checks.append({
                "check": "P-03.1 — evidence completeness",
                "passed": False,
                "detail": "No evidence provided. Every action must produce evidence before handoff.",
                "severity": "L2",
            })
        else:
            checks.append({
                "check": "P-03.1 — evidence completeness",
                "passed": True,
                "detail": f"Found {len(code_changes)} code changes, {len(commands)} commands, "
                          f"{len(research)} research items, {len(screenshots)} screenshots, {len(tests)} tests.",
                "severity": "L0",
            })

        # P-03.2: file:line format
        for change in code_changes:
            path = change.get("path", "")
            line = change.get("line", "")
            if not re.match(r"^.+\.\w+:\d+$", f"{path}:{line}"):
                checks.append({
                    "check": "P-03.2 — file:line format",
                    "passed": False,
                    "detail": f"Bad format: '{path}:{line}'. Expected 'path/to/file:NNN'.",
                    "severity": "L1",
                })

        # P-03.4: screenshot requirement for UI changes
        if result.get("has_ui_changes") and not screenshots:
            checks.append({
                "check": "P-03.4 — screenshot requirement",
                "passed": False,
                "detail": "UI changes detected but no screenshots provided (before/after required).",
                "severity": "L2",
            })

        # P-03.3: no LLM-sourced evidence
        for cmd in commands:
            if cmd.get("exit_code") is None:
                checks.append({
                    "check": "P-03.3 — grounded evidence",
                    "passed": False,
                    "detail": f"Command '{cmd.get('command', '')}' has no exit code — "
                              f"evidence must come from actual execution, not LLM generation.",
                    "severity": "L2",
                })

        return checks

    @staticmethod
    def check_constitutional(rule_ref: str, action: str) -> dict:
        """Check if *action* complies with constitutional rule *rule_ref*.

        rule_ref format: 'A-0X.Y' (article), 'P-0X.Y' (protocol), 'G-0X' (gate).
        Returns structured compliance result.
        """
        violations: list[str] = []
        rule_ref = rule_ref.upper().strip()

        if not re.match(r"^(A|P|G)-\d{2}(\.\d)?$", rule_ref):
            violations.append(f"invalid rule reference '{rule_ref}'. Use A-NN, P-NN.Y, or G-NN.")

        action_lower = action.lower()

        # Hard-coded constitutional checks (mirrors CLAUDE.md + CONSTITUTION.md)
        _CONSTITUTIONAL_RULES = {
            "A-01": {
                "pattern": "bypass|skip pipeline|direct response|direct delivery",
                "desc": "Pipeline flow is mandatory (Article 01)",
                "severity": "L4",
            },
            "A-02": {
                "pattern": r"no evidence|without evidence|unverified",
                "desc": "Evidence is mandatory (Article 02)",
                "severity": "L3",
            },
            "P-01.2": {
                "pattern": r"skip (intake|ceo|lead)|direct.*user|parallel.*pipeline",
                "desc": "Sequential gates must not be skipped (Protocol 01)",
                "severity": "L3",
            },
            "P-02.7": {
                "pattern": r"cross.*room.*direct|direct.*cross.*room",
                "desc": "Cross-room handoff requires Lead mediation (Protocol 02)",
                "severity": "L3",
            },
            "P-08.1": {
                "pattern": r"api.?key|secret|token|password|credential",
                "desc": "Zero secrets in code (Protocol 08)",
                "severity": "L4",
            },
            "P-11.1": {
                "pattern": r"unauthorized tool|tool.*not.*allowed|wrong tool",
                "desc": "Tool binding — agents use only assigned tools (Protocol 11)",
                "severity": "L2",
            },
        }

        rule = _CONSTITUTIONAL_RULES.get(rule_ref)
        if not rule:
            violations.append(f"unknown rule '{rule_ref}' — not in constitutional rules index")
            return {
                "valid": False,
                "rule_desc": "",
                "violations": violations,
                "severity": "L1",
            }

        if re.search(rule["pattern"], action_lower):
            violations.append(f"{rule_ref}: {rule['desc']}. Action '{action}' matches violation pattern.")

        return {
            "valid": len(violations) == 0,
            "rule_desc": rule["desc"],
            "violations": violations,
            "severity": rule["severity"] if violations else "L0",
        }

    @staticmethod
    def validate_rccf(task: str) -> dict:
        """Validate an RCCF work order format.

        RCCF = Room · Context · Command · Evidence.
        Validates that the task string contains all four required components.
        """
        violations: list[str] = []

        sections = {
            "room": r"room:\s*\S+",
            "context": r"context:\s*\S+",
            "command": r"command:\s*\S+",
            "evidence": r"evidence:\s*\S+",
        }

        found = {}
        for section, pattern in sections.items():
            m = re.search(pattern, task, re.IGNORECASE)
            found[section] = bool(m)
            if not m:
                violations.append(
                    f"missing RCCF section '{section}'. RCCF format: "
                    f"room: <code>, context: <situation>, command: <action>, evidence: <proof>."
                )

        return {
            "valid": len(violations) == 0,
            "sections_found": found,
            "violations": violations,
            "severity": "L2" if violations else "L0",
        }
