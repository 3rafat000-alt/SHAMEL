"""
role: gtw-dispatcher
purpose: machine-checkable resume via breadcrumb JSON (EVOLUTION.md Round 2 #8) —
         replaces silent trust in STATE.md prose `head_sha` with a per-ticket
         breadcrumb {branch, base_sha, head_sha, completed[], next_step} and a
         FRESH/DEGRADED/UNKNOWN resolver so `shamel sync` never resumes silently on
         stale state (Round 2 anti-pattern list: "silent resume from stale state").
gate: cross (every gate's dispatcher reads/writes a breadcrumb before handing off)
inputs: prj, ticket id, branch/base_sha/head_sha/completed/next_step (caller-
        supplied), a now_ts (float, epoch seconds) supplied by the caller — never
        read from the wall clock inside this module — and, for classify(), the
        CURRENT working-tree head_sha (caller reads it via git, e.g. `shamel_tools.
        gitops` or `git rev-parse HEAD`).
outputs: projects/<PRJ>/_context/breadcrumbs/<ticket>.json (one file per ticket,
         overwritten — last-known-state, not an append-only log, mirrors budget.py
         write_heartbeat).
exit: functions raise guard.GovernanceError on a scope violation, ValueError on a
      malformed argument; __main__ demo prints PASS and exits 0.

Complements STATE.md's `head_sha` line — does NOT replace it. STATE.md stays the
human-readable project-level summary; a breadcrumb is the fine-grained, per-ticket,
machine-checkable proof a resumer verifies BEFORE trusting the summary. A mismatch
between the breadcrumb's `head_sha` and the current working tree means the tree
moved out from under the ticket since it last checkpointed — that always DEGRADES
to "needs reconstruction", never a silent resume (Round 2 anti-pattern list).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from . import paths, guard

_SAFE = re.compile(r"[^\w.-]")


def _breadcrumbs_dir(prj: str) -> Path:
    return paths.context_dir(prj) / "breadcrumbs"


def _breadcrumb_path(prj: str, ticket: str) -> Path:
    safe = _SAFE.sub("_", ticket)
    return _breadcrumbs_dir(prj) / f"{safe}.json"


def write_breadcrumb(prj: str, ticket: str, branch: str, base_sha: str, head_sha: str,
                      completed: list[str], next_step: str, now_ts: float | None = None) -> Path:
    """Write (overwrite) the resume breadcrumb for `ticket`. `now_ts` is caller-
    supplied (GOVERNANCE Rule 9 — no wall-clock inside a tool); omit it to leave
    `ts` out of the record. Returns the path written."""
    if not ticket:
        raise ValueError("ticket is required")
    if not head_sha:
        raise ValueError("head_sha is required")
    f = _breadcrumb_path(prj, ticket)
    guard.assert_within_project(f, prj)
    f.parent.mkdir(parents=True, exist_ok=True)
    body = {
        "ticket": ticket,
        "branch": branch,
        "base_sha": base_sha,
        "head_sha": head_sha,
        "completed": list(completed),
        "next_step": next_step,
    }
    if now_ts is not None:
        body["ts"] = now_ts
    f.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return f


def read_breadcrumb(prj: str, ticket: str) -> dict:
    """Return the breadcrumb dict for `ticket`, or {} if none exists / unreadable
    (fail-open — an absent breadcrumb is UNKNOWN, not an error; see classify())."""
    f = _breadcrumb_path(prj, ticket)
    if not f.exists():
        return {}
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def latest_breadcrumb(prj: str) -> dict:
    """The most-recently-written breadcrumb across all tickets for `prj` (by file
    mtime — the filesystem is the only ordering signal this module reads; no
    wall-clock is consulted). {} if the project has no breadcrumbs yet."""
    d = _breadcrumbs_dir(prj)
    if not d.is_dir():
        return {}
    files = sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(data, dict):
            return data
    return {}


def classify(prj: str, ticket: str, current_head: str) -> dict:
    """Resolve resume-safety for `ticket` against the working tree's actual head.

    Returns {mode, reason, next_step}:
      - UNKNOWN  — no breadcrumb on file; nothing to resume from, treat as fresh
                   start (not a silent resume — there is no prior state to trust).
      - FRESH    — breadcrumb.head_sha == current_head: the tree is exactly where
                   the ticket left it; safe to resume from `next_step`.
      - DEGRADED — mismatch: the tree moved since the breadcrumb was written
                   (someone else committed, a rebase happened, a stale checkout).
                   NEVER silently resume on this — `next_step` says reconstruct.
    """
    if not current_head:
        raise ValueError("current_head is required")
    crumb = read_breadcrumb(prj, ticket)
    if not crumb:
        return {
            "mode": "UNKNOWN",
            "reason": f"no breadcrumb on file for {ticket}",
            "next_step": "no prior state to resume from — start the ticket fresh.",
        }
    crumb_head = crumb.get("head_sha", "")
    if crumb_head == current_head:
        return {
            "mode": "FRESH",
            "reason": f"breadcrumb head_sha matches working tree ({current_head}).",
            "next_step": crumb.get("next_step", ""),
        }
    return {
        "mode": "DEGRADED",
        "reason": (
            f"breadcrumb head_sha {crumb_head!r} != current head {current_head!r} — "
            "the tree moved since this ticket last checkpointed."
        ),
        "next_step": (
            f"do NOT silently resume '{crumb.get('next_step', '')}'. Reconstruct: "
            "diff current head against the breadcrumb's base_sha/head_sha, confirm "
            "which of completed[] still holds, then re-plan before continuing."
        ),
    }


if __name__ == "__main__":
    import sys
    import tempfile
    import os

    # Point the workspace at a throwaway project so the demo never touches a real
    # project's brain (guard.assert_within_project still fires normally).
    tmp = Path(tempfile.mkdtemp(prefix="shamel-resume-demo-"))
    prj_name = "PRJ-DEMO-RESUME"
    (tmp / prj_name / "_context").mkdir(parents=True)
    os.environ["SOFI_PROJECTS_DIR"] = str(tmp)
    paths.projects_dir.cache_clear() if hasattr(paths.projects_dir, "cache_clear") else None

    # 1) write + read round-trip
    p = write_breadcrumb(
        prj_name, "TKT-007", branch="prj/DEMO", base_sha="aaa0000", head_sha="bbb1111",
        completed=["scaffold", "migration"], next_step="wire the controller",
        now_ts=1_700_000_000.0,
    )
    assert p.name == "TKT-007.json", p
    crumb = read_breadcrumb(prj_name, "TKT-007")
    assert crumb["head_sha"] == "bbb1111" and crumb["completed"] == ["scaffold", "migration"], crumb
    print(f"breadcrumb: {crumb}")

    # 2) FRESH — current head matches
    fresh = classify(prj_name, "TKT-007", current_head="bbb1111")
    assert fresh["mode"] == "FRESH", fresh
    assert fresh["next_step"] == "wire the controller", fresh
    print(f"classify FRESH: {fresh}")

    # 3) DEGRADED — current head diverged
    degraded = classify(prj_name, "TKT-007", current_head="ccc2222")
    assert degraded["mode"] == "DEGRADED", degraded
    assert "reconstruct" in degraded["next_step"].lower(), degraded
    print(f"classify DEGRADED: {degraded}")

    # 4) UNKNOWN — no breadcrumb for this ticket
    unknown = classify(prj_name, "TKT-999", current_head="ddd3333")
    assert unknown["mode"] == "UNKNOWN", unknown
    print(f"classify UNKNOWN: {unknown}")

    # 5) latest_breadcrumb — a second ticket becomes the latest by mtime
    write_breadcrumb(
        prj_name, "TKT-008", branch="prj/DEMO", base_sha="bbb1111", head_sha="ccc2222",
        completed=["controller"], next_step="tests", now_ts=1_700_000_100.0,
    )
    latest = latest_breadcrumb(prj_name)
    assert latest["ticket"] == "TKT-008", latest
    print(f"latest_breadcrumb: {latest}")

    print("PASS")
    sys.exit(0)
