"""
role: gtw-budget-warden
purpose: budgets enforced at the SPAWNING layer (EVOLUTION.md Round 2 #3) — every
         delegation carries a hard ceiling (concurrency · rounds · tokens · deadline),
         a per-squad heartbeat file, and a circuit-breaker ledger that trips a
         structured crash-dump + escalation token at the 3-attempt ceiling
         (constitution/00-operating-system.md §escalation, nexus/bus/escalation.md §3).
gate: cross (every gate's dispatcher/squad call passes through this before spawning)
inputs: effort_class (nexus/routing.yaml effort_scaling row), prj, squad/ticket ids,
        counters (active_count/rounds_used/tokens_used) and a now_ts/start_ts supplied
        by the caller — never read from the wall clock inside this module.
outputs: projects/<PRJ>/_context/_heartbeats/<squad>.json (heartbeat, overwritten);
         projects/<PRJ>/_context/_circuit.jsonl (append-only attempt/trip ledger).
exit: functions raise guard.GovernanceError on a scope violation; ValueError on a
      malformed argument; __main__ demo prints PASS and exits 0.

Budgeted Autonomy (routing.yaml `budgeted_autonomy`): "every delegation carries a
hard ceiling — a scope, a call/attempt budget, and a fail-safe STOP. On breach:
stop and escalate, never 'keep trying'. Unbounded agents complete FEWER tasks, not
more." This module makes that mechanical instead of a discipline agents must
remember. Uses pyyaml when present, else the small stdlib regex fallback the rest
of shamel_tools uses (routing.py `_load`, gates.py `_load_gate_roles`).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from . import paths, guard

# ── Builtin fallbacks (used only when routing.yaml can't be parsed) ───────────
# Mirrors nexus/routing.yaml `effort_scaling:` — spawn width, round ceiling, and a
# token cap this module adds (routing.yaml has no token axis yet; these are the
# conservative per-class defaults gtw-budget-warden enforces until one lands there).
_BUILTIN_EFFORT_SCALING: dict[str, dict] = {
    "trivial-fix": {"spawn": "1", "budget_calls": "1-3", "token_cap": 20_000, "deadline_s": 600},
    "single-role": {"spawn": "1", "budget_calls": "3-10", "token_cap": 60_000, "deadline_s": 1800},
    "cross-room": {"spawn": "2-5", "budget_calls": "per-agent", "token_cap": 150_000, "deadline_s": 3600},
    "audit-sweep": {"spawn": "3-8", "budget_calls": "bounded", "token_cap": 250_000, "deadline_s": 5400},
    "arbitration": {"spawn": "1", "budget_calls": "as-needed", "token_cap": None, "deadline_s": None},
}

# routing.yaml `budgeted_autonomy.circuit_breaker` prose: "self-correction caps at
# 3 attempts; the 4th failure HALTS and triggers the circuit breaker" — parsed out
# of the yaml text when present, else this is the doctrine default.
_DEFAULT_CIRCUIT_BREAKER_CEILING = 3

# escalation.md §2 "general" decision chain + the security spur (§4) + boardroom
# accountability spans (§2) — the offline fallback when no machine-readable ladder
# is found in nexus/.
_BUILTIN_ESCALATION_LADDER: dict[str, object] = {
    "general": ["specialist", "room-lead", "gtw-conflict-resolver", "brd-arbiter", "brd-ceo"],
    "security": ["any-agent", "sec-lead", "brd-cso", "brd-ceo"],
    "boardroom_spans": {"0-2": "brd-cpo", "3-4": "brd-cto", "5": "brd-cqo"},
}


def _routing_path() -> Path:
    return paths.nexus_dir() / "routing.yaml"


@lru_cache(maxsize=1)
def _load_routing_text() -> str:
    return _routing_path().read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def _load_effort_scaling() -> dict[str, dict]:
    """Parse `effort_scaling:` from nexus/routing.yaml. pyyaml when present, else a
    stdlib regex fallback matching the other modules' `{ k: v, ... }` line style."""
    text = _load_routing_text()
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        block = (data or {}).get("effort_scaling")
        if isinstance(block, dict) and block:
            return block
    except Exception:
        pass
    return _fallback_effort_scaling(text)


def _fallback_effort_scaling(text: str) -> dict[str, dict]:
    blk = re.search(r"^effort_scaling:\s*$(.*?)^\S", text, re.M | re.S)
    body = blk.group(1) if blk else ""
    inner = re.compile(r"^\s*([\w-]+):\s*\{([^}]*)\}", re.M)
    out: dict[str, dict] = {}
    for m in inner.finditer(body):
        row, kv = m.group(1), m.group(2)
        d: dict[str, str] = {}
        for pair in kv.split(","):
            if ":" in pair:
                k, v = pair.split(":", 1)
                d[k.strip()] = v.strip().strip('"')
        if d:
            out[row] = d
    return out or dict(_BUILTIN_EFFORT_SCALING)


@lru_cache(maxsize=1)
def _load_budgeted_autonomy() -> dict[str, str]:
    """Parse the `budgeted_autonomy:` prose block (rule / circuit_breaker /
    context_boundary) — used only to pull the circuit-breaker ceiling out of the
    doctrine text so the number stays single-sourced from routing.yaml."""
    text = _load_routing_text()
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        block = (data or {}).get("budgeted_autonomy")
        if isinstance(block, dict) and block:
            return {k: str(v) for k, v in block.items()}
    except Exception:
        pass
    blk = re.search(r"^budgeted_autonomy:\s*$(.*?)(?:^\S|\Z)", text, re.M | re.S)
    body = blk.group(1) if blk else ""
    out: dict[str, str] = {}
    for m in re.finditer(r'^\s*(\w+):\s*"([^"]*)"', body, re.M):
        out[m.group(1)] = m.group(2)
    return out


def circuit_breaker_ceiling() -> int:
    """Attempts allowed before the breaker trips (routing.yaml `budgeted_autonomy.
    circuit_breaker` — "self-correction caps at N attempts"). Falls back to the
    doctrine default of 3 (escalation.md §3) if the prose can't be parsed."""
    prose = _load_budgeted_autonomy().get("circuit_breaker", "")
    m = re.search(r"caps at (\d+) attempts?", prose)
    return int(m.group(1)) if m else _DEFAULT_CIRCUIT_BREAKER_CEILING


def _parse_upper_bound(raw: str, default: int) -> int:
    """'1' -> 1, '2-5' -> 5, '3-8' -> 8. Non-numeric tokens (bounded/as-needed/
    per-agent) fall through to `default`."""
    if raw is None:
        return default
    raw = str(raw).strip().strip('"')
    nums = [int(n) for n in re.findall(r"\d+", raw)]
    return max(nums) if nums else default


# ── The Budget contract ────────────────────────────────────────────────────────
@dataclass
class Budget:
    """A spawn-layer ceiling. `None` on any cap means "unbounded for this class"
    (only `arbitration` reaches this — routing.yaml: "the only row where deep tier
    is reachable... depth not width"). Never construct with a wall-clock default;
    `deadline_ts` is either `None` or `start_ts + duration`, both caller-supplied.
    """
    effort_class: str
    max_concurrency: int | None
    max_rounds: int | None
    token_cap: int | None
    deadline_ts: float | None
    note: str = ""


def parse_budget_for(effort_class: str, start_ts: float | None = None) -> Budget:
    """Resolve the hard ceiling for one effort class (nexus/routing.yaml
    `effort_scaling`). No wall clock is read here (GOVERNANCE Rule 9) — pass
    `start_ts` (the CEO's clock) to anchor a deadline; omit it to get an
    un-anchored budget (`deadline_ts=None`, checked as "no deadline yet").
    """
    rows = _load_effort_scaling()
    row = rows.get(effort_class)
    if row is None:
        raise ValueError(
            f"unknown effort class '{effort_class}'; must be one of {sorted(rows or _BUILTIN_EFFORT_SCALING)}"
        )
    builtin = _BUILTIN_EFFORT_SCALING.get(effort_class, {})

    spawn_raw = row.get("spawn", builtin.get("spawn", "1"))
    calls_raw = row.get("budget_calls", builtin.get("budget_calls", ""))

    max_concurrency = _parse_upper_bound(spawn_raw, 1)

    # budget_calls is free text in the yaml (numeric range, "bounded", "per-agent",
    # "as-needed"). Numeric ranges parse directly; the doctrine words map to the
    # circuit-breaker ceiling ("bounded"/"per-agent" — a boundable sub-task caps at
    # the same 3-attempt ceiling) or unbounded ("as-needed" — arbitration only).
    calls_str = str(calls_raw).strip().strip('"')
    if re.search(r"\d", calls_str):
        max_rounds = _parse_upper_bound(calls_str, circuit_breaker_ceiling())
    elif calls_str == "as-needed":
        max_rounds = None
    else:  # "bounded", "per-agent", or unrecognized — bound it, never guess unbounded
        max_rounds = circuit_breaker_ceiling()

    token_cap = row.get("token_cap", builtin.get("token_cap"))
    if isinstance(token_cap, str):
        token_cap = int(token_cap) if token_cap.strip().isdigit() else None

    deadline_s = builtin.get("deadline_s")
    deadline_ts = (start_ts + deadline_s) if (start_ts is not None and deadline_s is not None) else None

    return Budget(
        effort_class=effort_class,
        max_concurrency=max_concurrency,
        max_rounds=max_rounds,
        token_cap=token_cap,
        deadline_ts=deadline_ts,
        note=str(row.get("note", "")),
    )


def check_spawn(active_count: int, rounds_used: int, tokens_used: int,
                 budget: Budget, now_ts: float) -> tuple[bool, str]:
    """Enforce every cap before a spawn is allowed. Returns (ok, reason) — reason
    is human-readable and always populated, even on ok (routing.yaml: "an unlogged
    route is an unauditable expense"). Checked in ceiling-severity order so the
    first breach found is the one reported.
    """
    if budget.max_concurrency is not None and active_count >= budget.max_concurrency:
        return False, (
            f"max_concurrency reached: {active_count}/{budget.max_concurrency} active "
            f"for effort class '{budget.effort_class}' — stop and escalate, never widen silently."
        )
    if budget.max_rounds is not None and rounds_used >= budget.max_rounds:
        return False, (
            f"max_rounds reached: {rounds_used}/{budget.max_rounds} — the circuit breaker "
            "ceiling; file a crash-dump + escalate (budget.trip), never 'one more try'."
        )
    if budget.token_cap is not None and tokens_used >= budget.token_cap:
        return False, f"token_cap reached: {tokens_used}/{budget.token_cap} for '{budget.effort_class}'."
    if budget.deadline_ts is not None and now_ts >= budget.deadline_ts:
        return False, f"deadline exceeded: now={now_ts} >= deadline={budget.deadline_ts}."
    return True, f"within budget ({active_count}/{budget.max_concurrency or '∞'} spawns, {rounds_used}/{budget.max_rounds or '∞'} rounds)"


# ── Per-squad heartbeat ─────────────────────────────────────────────────────────
def _heartbeat_path(prj: str, squad: str) -> Path:
    safe = re.sub(r"[^\w.-]", "_", squad)
    return paths.context_dir(prj) / "_heartbeats" / f"{safe}.json"


def write_heartbeat(prj: str, squad: str, ts: float, payload: dict) -> None:
    """Overwrite the squad's heartbeat with the latest snapshot (last-known-state,
    not an append-only log — a stale/missing heartbeat is what a budget-warden
    reads to detect a stalled squad). `ts` is caller-supplied (GOVERNANCE Rule 9)."""
    f = _heartbeat_path(prj, squad)
    guard.assert_within_project(f, prj)
    f.parent.mkdir(parents=True, exist_ok=True)
    body = {"squad": squad, "ts": ts, **payload}
    f.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_heartbeat(prj: str, squad: str) -> dict | None:
    f = _heartbeat_path(prj, squad)
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


# ── Circuit-breaker ledger ──────────────────────────────────────────────────────
def _circuit_path(prj: str) -> Path:
    return paths.context_dir(prj) / "_circuit.jsonl"


def _append_jsonl(f: Path, entry: dict) -> None:
    f.parent.mkdir(parents=True, exist_ok=True)
    with f.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")


def _read_ledger(prj: str) -> list[dict]:
    f = _circuit_path(prj)
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _attempts_since_last_trip(prj: str, ticket: str) -> int:
    """Attempt count for `ticket` since its most recent trip (a trip resets the
    counter — escalation.md §3: the breaker is per-sub-task, not cumulative)."""
    count = 0
    for entry in _read_ledger(prj):
        if entry.get("ticket") != ticket:
            continue
        if entry.get("event") == "trip":
            count = 0
        elif entry.get("event") == "attempt":
            count += 1
    return count


def record_attempt(prj: str, ticket: str) -> int:
    """Log one self-correction attempt for `ticket`; return its running count
    since the last trip (or since the ticket's first attempt)."""
    f = _circuit_path(prj)
    guard.assert_within_project(f, prj)
    count = _attempts_since_last_trip(prj, ticket) + 1
    _append_jsonl(f, {"ticket": ticket, "event": "attempt", "n": count})
    return count


_CRASH_DUMP_FIELDS = ("commit", "loop_count", "failed_context", "error_delta", "ts")


def trip(prj: str, ticket: str, crash_dump: dict) -> str:
    """Trip the breaker at the ceiling: append the structured crash-dump (shape
    matches nexus/bus/escalation.md §3) to `_circuit.jsonl` and return a
    deterministic escalation token for `shamel escalate <PRJ> <TKT> <up-chain>
    "circuit breaker"` to carry. Resets this ticket's attempt count.
    """
    missing = [k for k in _CRASH_DUMP_FIELDS if k not in crash_dump]
    if missing:
        raise ValueError(f"crash_dump missing required field(s): {missing} (need {_CRASH_DUMP_FIELDS})")
    f = _circuit_path(prj)
    guard.assert_within_project(f, prj)
    trip_n = sum(
        1 for e in _read_ledger(prj) if e.get("ticket") == ticket and e.get("event") == "trip"
    ) + 1
    token = f"ESC-{ticket}-T{trip_n:03d}"
    entry = {"ticket": ticket, "event": "trip", "escalation_token": token, **crash_dump}
    _append_jsonl(f, entry)
    return token


def breaker_tripped(prj: str, ticket: str) -> bool:
    """True once `ticket` has hit the ceiling (attempts >= circuit_breaker_ceiling())
    without a trip recorded yet — the signal a dispatcher checks before allowing
    a 4th self-correction round."""
    return _attempts_since_last_trip(prj, ticket) >= circuit_breaker_ceiling()


# ── Escalation ladder ────────────────────────────────────────────────────────────
def load_escalation_ladder() -> dict:
    """The decision chain a trip escalates along (escalation.md §2/§4). Looks for a
    machine-readable `nexus/escalation.yaml` first (none shipped yet — future-proof
    hook), then regex-parses the fenced chain diagrams out of
    `nexus/bus/escalation.md`, then falls back to the builtin table mirroring that
    doc's prose exactly.
    """
    yaml_path = paths.nexus_dir() / "escalation.yaml"
    if yaml_path.exists():
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data:
                return data
        except Exception:
            pass

    md_path = paths.nexus_dir() / "bus" / "escalation.md"
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError:
        return dict(_BUILTIN_ESCALATION_LADDER)

    chains = re.findall(r"```\n(.*?)\n```", text, re.S)
    general = next(
        (c.strip().split(" → ") for c in chains if "specialist" in c and "brd-ceo" in c), None
    )
    security = next(
        (c.strip().split(" → ") for c in chains if "sec-lead" in c and "brd-cso" in c), None
    )
    if not general or not security:
        return dict(_BUILTIN_ESCALATION_LADDER)
    return {
        "general": [s.strip() for s in general],
        "security": [s.strip() for s in security],
        "boardroom_spans": dict(_BUILTIN_ESCALATION_LADDER["boardroom_spans"]),
    }


if __name__ == "__main__":
    import sys
    import tempfile

    # Point the workspace at a throwaway project so the demo never touches a real
    # project's brain (guard.assert_within_project still fires normally).
    tmp = Path(tempfile.mkdtemp(prefix="shamel-budget-demo-"))
    prj_name = "PRJ-DEMO-BUDGET"
    (tmp / prj_name / "_context").mkdir(parents=True)

    import os
    os.environ["SOFI_PROJECTS_DIR"] = str(tmp)
    paths.projects_dir.cache_clear() if hasattr(paths.projects_dir, "cache_clear") else None

    # 1) parse a budget for a real effort class
    b = parse_budget_for("cross-room", start_ts=1_000_000.0)
    assert b.max_concurrency == 5, b
    assert b.deadline_ts == 1_000_000.0 + 3600, b
    print(f"budget: {b}")

    ok, reason = check_spawn(active_count=5, rounds_used=0, tokens_used=0, budget=b, now_ts=1_000_000.0)
    assert not ok and "max_concurrency" in reason, (ok, reason)
    ok, reason = check_spawn(active_count=1, rounds_used=0, tokens_used=0, budget=b, now_ts=1_000_000.0)
    assert ok, reason
    print(f"check_spawn: ok={ok} reason={reason}")

    # 2) heartbeat round-trip
    write_heartbeat(prj_name, "gate4-backend", ts=1_000_000.0, payload={"status": "running", "ticket": "TKT-042"})
    hb = read_heartbeat(prj_name, "gate4-backend")
    assert hb and hb["ticket"] == "TKT-042", hb
    print(f"heartbeat: {hb}")

    # 3) circuit breaker: 3 attempts then trip
    ceiling = circuit_breaker_ceiling()
    assert ceiling == 3, ceiling
    for i in range(ceiling):
        n = record_attempt(prj_name, "TKT-042")
        assert n == i + 1, n
    assert breaker_tripped(prj_name, "TKT-042")
    token = trip(prj_name, "TKT-042", {
        "commit": "abc1234",
        "loop_count": ceiling + 1,
        "failed_context": "bck-api-engineer refixing the same 500 on POST /orders",
        "error_delta": "nothing — identical stack trace across all 3 attempts",
        "ts": 1_000_050.0,
    })
    assert token == "ESC-TKT-042-T001", token
    assert not breaker_tripped(prj_name, "TKT-042")  # trip resets the counter
    print(f"trip: escalation_token={token}")

    # 4) escalation ladder
    ladder = load_escalation_ladder()
    assert ladder["general"][0] == "specialist" and ladder["general"][-1] == "brd-ceo", ladder
    assert "sec-lead" in ladder["security"], ladder
    print(f"ladder: {ladder}")

    print("PASS")
    sys.exit(0)
