"""
context_manager — session context lifecycle for HIPPOCAMPUS/CORTEX/AMYGDALA.

Writes to brain/HIPPOCAMPUS.md (working memory) during session, promotes
important entries to brain/CORTEX.md (long-term memory), and pushes alerts
to brain/AMYGDALA.md. Tracks agents, pipeline steps, decisions, and blockers.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import paths

_SESSION_STORE = paths.brain_dir() / "CONTEXT.md"
_HIPPOCAMPUS = paths.brain_dir() / "HIPPOCAMPUS.md"
_CORTEX = paths.brain_dir() / "CORTEX.md"
_AMYGDALA = paths.brain_dir() / "AMYGDALA.md"
_WORKING = paths.brain_dir() / "WORKING.md"


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_file(path: Path) -> None:
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def _append_line(path: Path, text: str) -> None:
    _ensure_file(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(text + "\n")


def _read_all(path: Path) -> str:
    _ensure_file(path)
    return path.read_text(encoding="utf-8")


def _write_all(path: Path, text: str) -> None:
    _ensure_file(path)
    path.write_text(text, encoding="utf-8")


class ContextManager:
    """Session context lifecycle manager.

    Writes to HIPPOCAMPUS (working memory), promotes to CORTEX (long-term),
    pushes alerts to AMYGDALA, and maintains a CONTEXT.md session overview.
    """

    def __init__(self, session_id: str | None = None) -> None:
        self.session_id: str = session_id or ""
        self._data: dict[str, Any] = {
            "session_id": self.session_id,
            "started": "",
            "agents_involved": [],
            "current_pipeline_step": "",
            "active_tasks": [],
            "decisions": [],
            "blockers": [],
            "notes": [],
        }

    # ── Session lifecycle ─────────────────────────────────────────────────

    def start_session(self) -> str:
        """Begin a new session. Generates session_id, writes initial context.

        Returns session_id.
        """
        self.session_id = self.session_id or f"SES-{uuid.uuid4().hex[:8].upper()}"
        now = _ts()
        self._data["session_id"] = self.session_id
        self._data["started"] = now
        self._data["current_pipeline_step"] = "intake"
        self._data["agents_involved"] = []
        self._data["active_tasks"] = []
        self._data["decisions"] = []
        self._data["blockers"] = []
        self._data["notes"] = []

        content = (
            f"# CONTEXT — Session Context\n\n"
            f"## Session Info\n"
            f"- Session ID: {self.session_id}\n"
            f"- Started: {now}\n"
            f"- Agents involved: (none yet)\n"
            f"- Current pipeline step: intake\n\n"
            f"## Active Tasks\n"
            f"| Task | Assigned to | Status | Started | Blockers |\n"
            f"|------|-------------|--------|---------|----------|\n\n"
            f"## Current Focus\n"
            f"What is being worked on right now:\n"
            f"- Session started. Awaiting pipeline.\n\n"
            f"## Decisions Made This Session\n"
            f"| Decision | Rationale | Made by |\n"
            f"|----------|-----------|--------|\n\n"
            f"## Blockers & Issues\n"
            f"| Issue | Severity | Owner | Status |\n"
            f"|-------|----------|-------|--------|\n\n"
            f"## Notes\n"
            f"- \n"
        )
        _write_all(_SESSION_STORE, content)

        # Log to HIPPOCAMPUS
        _append_line(_HIPPOCAMPUS,
                     f"| {now} | session_start | {self.session_id} | initiated |")

        return self.session_id

    def update_context(self, key: str, value: str) -> bool:
        """Update a named field in the session context.

        Supported keys: current_pipeline_step, current_focus, notes.
        Also updates the underlying CONTEXT.md file.
        Returns True on success.
        """
        key = key.strip().lower()
        valid_keys = {
            "current_pipeline_step", "current_focus", "notes",
            "agents_involved", "current_step",
        }
        normalised = "current_pipeline_step" if key == "current_step" else key

        if normalised not in valid_keys:
            msg = f"unknown context key '{key}'. Valid: {sorted(valid_keys)}"
            _append_line(_HIPPOCAMPUS, f"| {_ts()} | context_error | {msg} |")
            return False

        if normalised == "current_pipeline_step":
            self._data["current_pipeline_step"] = value
        elif normalised == "current_focus":
            # Append to CONTEXT.md Current Focus section
            existing = _read_all(_SESSION_STORE)
            new = value.strip()
            if "## Current Focus" in existing:
                before, after = existing.split("## Current Focus\n", 1)
                after_lines = after.split("\n")
                new_section = "## Current Focus\n" + new + "\n"
                if len(after_lines) > 2:
                    new_section += "\n".join(after_lines[1:]) + "\n"
                _write_all(_SESSION_STORE, before + new_section)
            self._data["current_focus"] = value
        elif normalised == "notes":
            self._data.setdefault("notes", []).append(value)
            _append_line(_SESSION_STORE, f"- {value}")

        _append_line(_HIPPOCAMPUS,
                     f"| {_ts()} | context_update | {normalised}={value} |")

        return True

    def get_context(self, key: str) -> str:
        """Read a named field from session context.

        Checks in-memory dict first, falls back to CONTEXT.md parse.
        """
        key = key.strip().lower()
        normalised = "current_pipeline_step" if key == "current_step" else key
        if normalised in self._data:
            val = self._data[normalised]
            if isinstance(val, list):
                return json.dumps(val, ensure_ascii=False)
            return str(val)

        # Fallback: parse CONTEXT.md
        raw = _read_all(_SESSION_STORE)
        for line in raw.splitlines():
            if line.lower().startswith(f"- {key}:"):
                return line.split(":", 1)[1].strip()
        return ""

    def snapshot(self) -> dict:
        """Return full session state snapshot."""
        return {
            "session_id": self.session_id,
            "started": self._data.get("started", ""),
            "agents_involved": list(self._data.get("agents_involved", [])),
            "current_pipeline_step": self._data.get("current_pipeline_step", ""),
            "active_tasks": list(self._data.get("active_tasks", [])),
            "decisions": list(self._data.get("decisions", [])),
            "blockers": list(self._data.get("blockers", [])),
            "notes": list(self._data.get("notes", [])),
            "timestamp": _ts(),
        }

    def log_interaction(
        self, from_agent: str, to_agent: str, action: str, result: str
    ) -> bool:
        """Log an agent-to-agent interaction to HIPPOCAMPUS.

        Records handoff, action, and result for traceability (Protocol 02).
        """
        timestamp = _ts()
        agents = self._data.setdefault("agents_involved", [])
        for a in (from_agent, to_agent):
            if a not in agents:
                agents.append(a)

        line = f"| {timestamp} | {from_agent} → {to_agent} | {action} | {result} |"
        _append_line(_HIPPOCAMPUS, line)

        # Also update CONTEXT.md agents list
        existing = _read_all(_SESSION_STORE)
        if "- Agents involved:" in existing:
            agent_str = ", ".join(sorted(set(agents)))
            existing = existing.replace(
                "- Agents involved:",
                f"- Agents involved: {agent_str}",
            )

        return True

    def promote_to_cortex(self, key: str) -> bool:
        """Move a context entry from HIPPOCAMPUS to CORTEX.

        Once promoted, the entry is written to CORTEX.md for permanent storage.
        """
        timestamp = _ts()
        hippo = _read_all(_HIPPOCAMPUS)

        # Find matching lines in HIPPOCAMPUS
        promoted_lines: list[str] = []
        remaining: list[str] = []
        for line in hippo.splitlines():
            if key in line:
                promoted_lines.append(line)
            else:
                remaining.append(line)

        if not promoted_lines:
            return False

        # Write to CORTEX
        _ensure_file(_CORTEX)
        cortex_entry = (
            f"\n## Promoted from HIPPOCAMPUS ({timestamp})\n"
            f"key: {key}\n"
            f"lines:\n"
        )
        for pl in promoted_lines:
            cortex_entry += f"  - {pl}\n"
        _append_line(_CORTEX, cortex_entry)

        # Remove from HIPPOCAMPUS
        _write_all(_HIPPOCAMPUS, "\n".join(remaining) + "\n")

        return True

    def push_alert(self, level: str, message: str, source: str) -> str:
        """Push an alert to AMYGDALA.

        level: L1–L4 matching severity classification.
        message: description of the alert.
        source: agent or system that triggered the alert.

        Returns alert_id.
        """
        timestamp = _ts()
        alert_id = f"ALT-{uuid.uuid4().hex[:6].upper()}"
        level = level.upper()
        if level not in ("L1", "L2", "L3", "L4"):
            level = "L2"

        entry = (
            f"\n## {alert_id} | {level} | {timestamp}\n"
            f"source: {source}\n"
            f"message: {message}\n"
            f"status: open\n"
        )
        _append_line(_AMYGDALA, entry)

        # Log to HIPPOCAMPUS too
        _append_line(_HIPPOCAMPUS,
                     f"| {timestamp} | alert:{alert_id} | {level} | {source} | {message} |")

        return alert_id

    def close_session(self) -> dict:
        """Finalise the session. Writes summary to CORTEX and returns final state.

        Important context is promoted automatically before closing.
        """
        timestamp = _ts()
        summary = self.snapshot()
        summary["ended"] = timestamp

        # Write final summary to CORTEX
        _ensure_file(_CORTEX)
        cortex_entry = (
            f"\n## Session End: {self.session_id} ({timestamp})\n"
            f"- Duration: {self._data.get('started', '')} → {timestamp}\n"
            f"- Agents involved: {', '.join(sorted(set(self._data.get('agents_involved', []))))}\n"
            f"- Pipeline steps completed: {self._data.get('current_pipeline_step', 'none')}\n"
            f"- Decisions: {len(self._data.get('decisions', []))}\n"
            f"- Blockers: {len(self._data.get('blockers', []))}\n"
        )
        _append_line(_CORTEX, cortex_entry)

        # Write WORKING.md snapshot
        working = (
            f"# WORKING — Session Snapshot\n\n"
            f"- session_id: {self.session_id}\n"
            f"- started: {self._data.get('started', '')}\n"
            f"- ended: {timestamp}\n"
            f"- agents: {', '.join(sorted(set(self._data.get('agents_involved', []))))}\n"
            f"- pipeline_step: {self._data.get('current_pipeline_step', '')}\n"
            f"- active_tasks: {len(self._data.get('active_tasks', []))}\n"
        )
        _write_all(_WORKING, working)

        return summary
