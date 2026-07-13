"""
runlog — append-only record of tool runs against a project.

Rule 6: any script that mutates state leaves a trace. Writes to
projects/<PRJ>/_context/_runlog.md (sandboxed). Timestamps are passed in by the
caller (the CEO owns the clock); tools never invent a date.
"""
from __future__ import annotations

from pathlib import Path

from . import paths, guard


def log(prj: str, role: str, action: str, *, when: str = "", to_context: bool = False) -> None:
    f = paths.context_dir(prj) / "_runlog.md"
    guard.assert_within_project(f, prj)
    if not f.exists():
        f.write_text(f"# RUN LOG — {prj}\n> append-only; one line per tool run.\n", encoding="utf-8")
    stamp = f"{when} " if when else ""
    with f.open("a", encoding="utf-8") as fh:
        fh.write(f"- {stamp}[{role}] {action}\n")
    if to_context:
        from . import brain
        brain.append_context(prj, f"tool run by {role}: {action}")
