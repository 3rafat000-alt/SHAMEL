"""
brain — read and update the company brain (STATE / CONTEXT / DECISIONS / HANDOFFS).

The universal contract in code: BEFORE acting read STATE; AFTER acting append
CONTEXT (+DECISIONS if irreversible) and update STATE. Every write is sandboxed
to the project via guard.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import paths, guard

_KV = re.compile(r"^([a-zA-Z_][\w -]*?):\s*(.*)$")


def read_state(prj: str) -> dict[str, str]:
    """Parse STATE.md `key: value` lines into a dict (order not preserved)."""
    f = paths.brain_file(prj, "STATE")
    state: dict[str, str] = {}
    if not f.exists():
        return state
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = _KV.match(line)
        if m:
            state[m.group(1).strip()] = m.group(2).strip()
    return state


def update_state(prj: str, updates: dict[str, str]) -> None:
    """Rewrite STATE.md in place, replacing known keys and appending new ones.

    Preserves the file's line order and any comment/title lines.
    """
    f = paths.brain_file(prj, "STATE")
    guard.assert_within_project(f, prj)
    if not f.exists():
        raise FileNotFoundError(f"no STATE.md for {prj}; scaffold the project first.")

    remaining = dict(updates)
    out: list[str] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        m = _KV.match(line.strip())
        if m and m.group(1).strip() in remaining:
            key = m.group(1).strip()
            out.append(f"{key}: {remaining.pop(key)}")
        else:
            out.append(line)
    for key, val in remaining.items():  # new keys appended at end
        out.append(f"{key}: {val}")
    f.write_text("\n".join(out) + "\n", encoding="utf-8")


def append_context(prj: str, bullet: str, gate: str | None = None) -> None:
    """Append one durable fact to CONTEXT.md (append-only ledger)."""
    f = paths.brain_file(prj, "CONTEXT")
    guard.assert_within_project(f, prj)
    prefix = f"- [gate {gate}] " if gate is not None else "- "
    with f.open("a", encoding="utf-8") as fh:
        fh.write(f"{prefix}{bullet}\n")


def append_decision(prj: str, title: str, why: str, reversible: str, date: str) -> None:
    """Append an ADR entry to DECISIONS.md. Date is supplied by the caller (CEO),
    never invented inside a tool."""
    f = paths.brain_file(prj, "DECISIONS")
    guard.assert_within_project(f, prj)
    existing = f.read_text(encoding="utf-8") if f.exists() else ""
    n = existing.count("## ADR-") + 1
    block = (
        f"\n## ADR-{n:03d} ({date}) — {title}\n"
        f"{why}\nReversible? {reversible}\n"
    )
    with f.open("a", encoding="utf-8") as fh:
        fh.write(block)


def read_raw(prj: str, name: str) -> str:
    f = paths.brain_file(prj, name)
    return f.read_text(encoding="utf-8") if f.exists() else ""
