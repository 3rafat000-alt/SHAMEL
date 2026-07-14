"""
role: shared library (core/shamel_tools) — owner obs-monitoring-engineer
purpose: fleet telemetry (EVOLUTION.md Round 2 #10) — a one-line `send_event`
    every room's hooks can call so 105 agents "emit as well as guard". The
    durable record is always the local JSONL append (never lost, never blocks
    a hook on network flakiness); a best-effort POST to a live
    `event_server.py` is a pure bonus for a real-time dashboard and NEVER
    raises or stalls the caller. The LLM never touches this path — pure
    deterministic file I/O plus an optional fire-and-forget HTTP call.
gate: cross (every gate's hooks may emit; telemetry itself is gate-agnostic)
inputs: event dict (caller-supplied — source/kind/agent/prj/... any JSON-able
    keys), a now_ts string supplied by the caller (GOVERNANCE Rule 9 — no
    wall-clock inside this module), an optional server_url for the live POST.
outputs: append-only lines in .claude/memory/events.jsonl (workspace-root
    scoped via guard.assert_within_repo); an optional best-effort HTTP POST.
exit: send_event/read_events/summarize_events never raise on I/O or network
    faults they can swallow (network faults are always swallowed); a genuine
    disk write failure propagates (nothing durable was recorded — fail loud).
    __main__ demo prints PASS and exits 0.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path

from . import paths, guard

_EVENTS_REL = Path(".claude") / "memory" / "events.jsonl"
_POST_TIMEOUT_S = 0.75


def events_path() -> Path:
    return paths.repo_root() / _EVENTS_REL


def send_event(event: dict, now_ts: str, server_url: str | None = None) -> None:
    """Record one telemetry event.

    Always appends a JSONL line under .claude/memory/events.jsonl (created on
    demand). `now_ts` is stamped onto the record as `ts` (caller supplies the
    clock — GOVERNANCE Rule 9). If `server_url` is given, also fires a
    best-effort POST to `<server_url>/events` — short timeout, any failure
    (unreachable server, DNS, timeout, non-2xx) is swallowed silently so a
    hook can never be blocked or broken by a missing dashboard.
    """
    record = dict(event)
    record["ts"] = now_ts

    f = events_path()
    guard.assert_within_repo(f)
    f.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with f.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")

    if not server_url:
        return
    try:
        url = server_url.rstrip("/") + "/events"
        body = line.encode("utf-8")
        req = urllib.request.Request(
            url, data=body, method="POST",
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=_POST_TIMEOUT_S).close()
    except Exception:
        pass  # best-effort only — the JSONL append above is the durable record


def read_events(n: int = 100) -> list[dict]:
    """Return the last `n` events (oldest-first), skipping any malformed line."""
    f = events_path()
    if not f.exists():
        return []
    lines = f.read_text(encoding="utf-8").splitlines()
    out: list[dict] = []
    for raw in lines[-n:]:
        raw = raw.strip()
        if not raw:
            continue
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return out


def summarize_events(events: list[dict]) -> dict:
    """Counts by source / kind / agent, plus a total. Deterministic; no I/O."""
    by_source: dict[str, int] = {}
    by_kind: dict[str, int] = {}
    by_agent: dict[str, int] = {}
    for e in events:
        for bucket, key in ((by_source, "source"), (by_kind, "kind"), (by_agent, "agent")):
            val = e.get(key)
            if val:
                bucket[val] = bucket.get(val, 0) + 1
    return {
        "total": len(events),
        "by_source": by_source,
        "by_kind": by_kind,
        "by_agent": by_agent,
    }


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        # Isolate the demo from the real workspace events.jsonl.
        fake_root = Path(td)
        (fake_root / "CLAUDE.md").write_text("demo", encoding="utf-8")
        (fake_root / "company").mkdir()

        orig_repo_root = paths.repo_root
        paths.repo_root = lambda start=None: fake_root  # type: ignore[assignment]
        try:
            send_event(
                {"source": "obs-monitoring-engineer", "kind": "hook", "agent": "dev-backend-1", "prj": "PRJ-0001"},
                now_ts="2026-07-07T00:00:00Z",
                server_url="http://127.0.0.1:1",  # nothing listens here — must not raise/block
            )
            send_event(
                {"source": "gtw-dispatcher", "kind": "spawn", "agent": "qa-tester-2", "prj": "PRJ-0001"},
                now_ts="2026-07-07T00:00:05Z",
            )

            got = read_events(100)
            assert len(got) == 2, f"expected 2 events, got {len(got)}"
            assert got[0]["source"] == "obs-monitoring-engineer"
            assert got[1]["kind"] == "spawn"

            summary = summarize_events(got)
            assert summary["total"] == 2
            assert summary["by_source"]["obs-monitoring-engineer"] == 1
            assert summary["by_kind"]["spawn"] == 1
            assert summary["by_agent"]["dev-backend-1"] == 1

            print("events:", got)
            print("summary:", summary)
            print("PASS")
        finally:
            paths.repo_root = orig_repo_root  # type: ignore[assignment]
