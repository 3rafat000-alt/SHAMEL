"""
role: gtw-gatekeeper (mechanical layer)
purpose: the MECHANICAL half of fail-closed gates (EVOLUTION Round 2 item 2) —
  a _VALID_TRANSITIONS state machine over gates 0..8, and the boundary check the
  Stop hook / gates.validate_* call before letting a turn end or a gate advance.
  Doctrine → impossibility: a gate can no longer be skipped by a wrong word in a
  ticket, only by a code path that returns ILLEGAL_SKIP.
gate: all (cross-gate infrastructure; consumed by every gate's advance check)
inputs: from_gate/to_gate ints (0..8) and a PRJ-ID (reads STATE.md via brain.read_state)
outputs: pure (bool, str) / dict verdicts — never writes the brain itself
exit: 0 on import/self-test pass, non-zero if the __main__ assertions fail
"""
from __future__ import annotations

import re

from . import brain, gates, paths, tickets

# advance   N -> N+1                       (forward one step, the normal path)
# rework    N -> N                         (same gate, another lap)
# loopback  N -> M<N                       (earlier gate — allowed, flagged)
# ILLEGAL_SKIP  N -> M>N+1, or either gate out of GATE_ORDER
_KIND_ADVANCE = "advance"
_KIND_REWORK = "rework"
_KIND_LOOPBACK = "loopback"
_KIND_ILLEGAL = "ILLEGAL_SKIP"

_GATE_RE = re.compile(r"-?\d+")


def valid_transition(from_gate: int, to_gate: int) -> tuple[bool, str]:
    """The state machine: is `from_gate -> to_gate` a legal move, and what kind?

    Returns (ok, kind). kind is one of advance/rework/loopback/ILLEGAL_SKIP.
    Forward jumps of more than one gate (N -> N+2 or further) are the one
    hard-illegal case; everything else (advance, self, any loop-back) is legal.
    """
    if from_gate not in gates.GATE_ORDER or to_gate not in gates.GATE_ORDER:
        return False, _KIND_ILLEGAL
    if to_gate == from_gate:
        return True, _KIND_REWORK
    if to_gate == from_gate + 1:
        return True, _KIND_ADVANCE
    if to_gate < from_gate:
        return True, _KIND_LOOPBACK
    return False, _KIND_ILLEGAL


def _gate_num(raw: str) -> int | None:
    """Pull the first integer out of a STATE.md `gate:` value ('3', ' 3 ', ...)."""
    m = _GATE_RE.search(raw or "")
    return int(m.group(0)) if m else None


def gate_proof_required(prj: str | None) -> bool:
    """True only when an active project sits AT a gate boundary right now.

    False (never blocks) when: no prj given, the project doesn't exist, its
    STATE.active isn't true, or its STATE.gate isn't a valid integer — a
    framework-only session (no project in play) is never gated. "At a
    boundary" means no ticket is still open at the project's current gate:
    there is nothing left to dispatch at this level, so the next real move is
    necessarily a transition, and that transition owes pasted proof.
    """
    if not prj or not paths.project_exists(prj):
        return False
    state = brain.read_state(prj)
    if state.get("active", "").strip().lower() != "true":
        return False
    cur = _gate_num(state.get("gate", ""))
    if cur is None or cur not in gates.GATE_ORDER:
        return False
    open_here = [
        t for t in tickets.parse(prj)
        if t.is_open and _gate_num(t.gate) == cur
    ]
    return not open_here


def check_gate_advance(prj: str, to_gate: int) -> dict:
    """Validate a proposed advance against the project's current STATE.gate.

    Returns {ok, kind, reason}. Reads STATE.gate as the `from_gate`; if it is
    missing/unparseable the move is refused (fail-closed, not fail-open —
    gate 2's doctrine flip: a broken read never silently permits a skip).
    """
    state = brain.read_state(prj)
    raw = state.get("gate", "")
    from_gate = _gate_num(raw)
    if from_gate is None:
        return {
            "ok": False,
            "kind": _KIND_ILLEGAL,
            "reason": f"STATE.gate for {prj} is missing/unparseable ({raw!r}); refusing to advance.",
        }
    ok, kind = valid_transition(from_gate, to_gate)
    if ok:
        reason = f"gate {from_gate} -> {to_gate} is a legal {kind}."
    else:
        reason = (
            f"gate {from_gate} -> {to_gate} is {kind}: forward moves may only step "
            "one gate at a time (N->N+1); self (rework) and any loop-back to an "
            "earlier gate are allowed, a forward jump of 2+ is not."
        )
    return {"ok": ok, "kind": kind, "reason": reason}


if __name__ == "__main__":
    assert valid_transition(2, 3) == (True, _KIND_ADVANCE)
    assert valid_transition(3, 3) == (True, _KIND_REWORK)
    assert valid_transition(5, 2) == (True, _KIND_LOOPBACK)
    assert valid_transition(0, 0) == (True, _KIND_REWORK)
    assert valid_transition(8, 8) == (True, _KIND_REWORK)
    assert valid_transition(2, 4) == (False, _KIND_ILLEGAL)   # the +2 skip
    assert valid_transition(0, 8) == (False, _KIND_ILLEGAL)
    assert valid_transition(-1, 0) == (False, _KIND_ILLEGAL)
    assert valid_transition(3, 9) == (False, _KIND_ILLEGAL)

    # gate_proof_required must never block a framework-only (no project) session.
    assert gate_proof_required(None) is False
    assert gate_proof_required("PRJ-DOES-NOT-EXIST-0000") is False

    # fixture project in a tmp projects_dir (SOFI_PROJECTS_DIR override — no
    # wall-clock, no real workspace touched).
    import os
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as td:
        os.environ["SOFI_PROJECTS_DIR"] = td
        prj = "PRJ-TEST"
        ctx = Path(td) / prj / "_context"
        ctx.mkdir(parents=True)
        (ctx / "STATE.md").write_text(
            "# STATE\ngate: 3\nactive: true\nbranch: prj/PRJ-TEST\n", encoding="utf-8"
        )
        (ctx / "HANDOFFS.md").write_text(
            "## TKT-001 · gate 3\nfrom: a -> to: b\ntask: t\nexpected: e\nstatus: done\n",
            encoding="utf-8",
        )

        assert paths.project_exists(prj)
        # every ticket at gate 3 is closed -> sitting at the boundary
        assert gate_proof_required(prj) is True

        adv = check_gate_advance(prj, 4)
        assert adv == {"ok": True, "kind": _KIND_ADVANCE, "reason": adv["reason"]}
        skip = check_gate_advance(prj, 6)
        assert skip["ok"] is False and skip["kind"] == _KIND_ILLEGAL
        rework = check_gate_advance(prj, 3)
        assert rework == {"ok": True, "kind": _KIND_REWORK, "reason": rework["reason"]}
        loop = check_gate_advance(prj, 1)
        assert loop == {"ok": True, "kind": _KIND_LOOPBACK, "reason": loop["reason"]}

        # now open an in-flight ticket at the current gate -> not at a boundary
        with (ctx / "HANDOFFS.md").open("a", encoding="utf-8") as fh:
            fh.write("\n## TKT-002 · gate 3\nfrom: a -> to: b\ntask: t2\nexpected: e2\nstatus: open\n")
        assert gate_proof_required(prj) is False

        # inactive project is never gated
        (ctx / "STATE.md").write_text(
            "# STATE\ngate: 3\nactive: false\n", encoding="utf-8"
        )
        assert gate_proof_required(prj) is False

        del os.environ["SOFI_PROJECTS_DIR"]

    print("PASS")
