"""
gates — the 9-gate lifecycle, in code. Enforce order, forbid skips.

Gate 0 Inception → 1 Discovery → 2 Design → 3 Architecture → 4 Build →
5 Quality → 6 Staging/UAT → 7 Prod → 8 Observe→loop.

The gate→agents map is loaded from core/nexus/gates.yaml (v5 debt #5 paid:
no hardcoded gate→role table — the yaml is the source; a minimal builtin map of
owner-room Leads remains only as the offline fallback).
"""
from __future__ import annotations

import re
from functools import lru_cache

from . import paths, tickets

GATE_ORDER = list(range(0, 9))

GATE_LABEL = {
    0: "Inception", 1: "Discovery", 2: "Solution Design", 3: "Architecture",
    4: "Build", 5: "Quality", 6: "Staging/UAT", 7: "Production", 8: "Observe",
}

# Minimal fallback: each gate's owner-room Lead (nexus/gates.yaml owner_room).
# Used only when gates.yaml is unreadable — the yaml agent lists win.
_BUILTIN_GATE_ROLES: dict[int, list[str]] = {
    0: ["str-lead"],
    1: ["res-lead"],
    2: ["dsn-lead"],
    3: ["arc-lead", "dat-lead", "sec-lead"],
    4: ["bck-lead", "fnt-lead", "mob-lead", "dat-lead"],
    5: ["qa-lead", "sec-lead"],
    6: ["ops-lead"],
    7: ["ops-lead", "ops-release-manager"],
    8: ["obs-lead"],
}


@lru_cache(maxsize=1)
def _load_gate_roles() -> dict[int, list[str]]:
    """Parse core/nexus/gates.yaml → {gate id: [agent ids]}. Fail-open to the
    builtin Lead map on any read/parse problem."""
    p = paths.nexus_dir() / "gates.yaml"
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return dict(_BUILTIN_GATE_ROLES)
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        out: dict[int, list[str]] = {}
        for g in (data or {}).get("gates") or []:
            gid = g.get("id")
            agents = g.get("agents") or []
            if isinstance(gid, int) and isinstance(agents, list):
                out[gid] = [str(a) for a in agents]
        if out:
            return out
    except Exception:
        pass
    # stdlib fallback: `- id: N` blocks with an `agents: [...]` list (may wrap lines)
    out = {}
    gid = None
    collecting = False
    buf = ""
    for line in text.splitlines():
        m = re.match(r"^\s*-\s*id:\s*(\d+)", line)
        if m:
            gid = int(m.group(1))
            collecting = False
            continue
        if gid is None:
            continue
        if re.match(r"^\s*agents:\s*\[", line):
            collecting = True
            buf = line.split("[", 1)[1]
        elif collecting:
            buf += " " + line.strip()
        if collecting and "]" in buf:
            inner = buf.split("]", 1)[0]
            out[gid] = [a.strip() for a in inner.split(",") if a.strip()]
            collecting, buf = False, ""
    return out or dict(_BUILTIN_GATE_ROLES)


# Module-level view for existing consumers (dashboard, shamel gate-check output).
try:
    GATE_ROLES: dict[int, list[str]] = _load_gate_roles()
except Exception:
    GATE_ROLES = dict(_BUILTIN_GATE_ROLES)


def label(gate: int) -> str:
    return GATE_LABEL.get(gate, "?")


def roles_for_gate(gate: int) -> list[str]:
    return _load_gate_roles().get(gate, [])


def _gate_num(raw: str) -> int | None:
    """Pull the first integer out of a gate string like '3' or '8 → gate 1'."""
    for tok in raw.replace("→", " ").split():
        if tok.isdigit():
            return int(tok)
    return None


def validate_no_skip(prj: str) -> dict:
    """Walk the ticket queue forward; confirm gates never skip a step.

    Returns {ok, sequence, skips, loops, transitions}. A loop-back (gate N →
    gate M<N) is allowed and reported separately, not counted as a skip.
    `transitions` (v6.1) additionally names the transitions.valid_transition
    kind (advance/rework/loopback/ILLEGAL_SKIP) for each adjacent hop in the
    ticket sequence — the mechanical state-machine verdict layered on top of
    this validator's own +1-jump heuristic, without changing this function's
    existing return shape (only a field is added).
    """
    # Local import: transitions.py imports gates at module scope, so importing
    # transitions at gates.py module scope would cycle; both modules are fully
    # loaded by the time this function actually runs.
    from . import transitions

    seq: list[int] = []
    loops: list[str] = []
    for t in tickets.parse(prj):
        g = _gate_num(t.gate)
        if g is None:
            continue
        if "→" in t.gate:  # explicit loop-back ticket
            loops.append(t.id + ": " + t.gate)
        seq.append(g)

    # forward sequence = monotonic non-decreasing in its first appearance order,
    # never jumping more than +1 between distinct gate levels.
    skips: list[str] = []
    highest = 0
    for g in seq:
        if g > highest + 1:
            skips.append(f"jumped {highest}→{g}")
        highest = max(highest, g)

    trans: list[str] = []
    for i in range(1, len(seq)):
        _ok, kind = transitions.valid_transition(seq[i - 1], seq[i])
        trans.append(f"{seq[i - 1]}→{seq[i]}: {kind}")

    return {
        "ok": not skips,
        "sequence": seq,
        "skips": skips,
        "loops": loops,
        "transitions": trans,
    }


def validate_room_boundary(prj: str) -> dict:
    """Every ticket's from:/to: must stay within a room or cross via a Room Lead /
    boardroom / gateway (`shamel_tools.tickets.validate_room_boundary`). Same
    PASS/FAIL shape as the other gate validators, so `cmd_gate_check` combines
    all four uniformly.
    """
    violations = tickets.validate_room_boundary(prj)
    return {"ok": not violations, "violations": violations}


# Back-compat alias for v5 callers.
validate_tier_boundary = validate_room_boundary


def validate_artifacts(prj: str) -> dict:
    """Confirm every ticket's `expected: <path>` artifact exists on disk.

    Tickets whose `expected` is a free-text action (no path) are skipped.
    """
    missing, checked = [], []
    base = paths.project_dir(prj)
    for t in tickets.parse(prj):
        exp = t.expected.split()[0] if t.expected else ""
        if exp.startswith(("docs/", "src/")):
            checked.append(exp)
            if not (base / exp).exists():
                missing.append(f"{t.id}: {exp}")
    return {"ok": not missing, "checked": checked, "missing": missing}


# ── v5 Verification: outcome over self-report (verification.md V1, grounding.md G3) ──
# A done-ticket that asserts completion must carry evidence — a run command + its
# output/exit code, a file:line proof, or a git diff/SHA — not just the word "done".
_EVIDENCE = re.compile(
    r"exit[\s_-]?code|exit\s*[:=]?\s*0|passing|passed|\btests?\b.*\b(ran|pass)|"
    r"\.py:\d|\.php:\d|\.dart:\d|:\d+\b|"          # file:line proof
    r"\b[0-9a-f]{7,40}\b|diff|commit|"             # git evidence
    r"```|\$\s",                                    # a pasted command/output block
    re.I,
)


def validate_evidence(prj: str) -> dict:
    """Reject done/passing tickets that assert completion without pasted evidence.

    Same PASS/FAIL shape as the other validators. A ticket is "asserting completion"
    when its status starts with done/passed/complete. Evidence may live in the
    `expected`, `status`, or any `extra` field (e.g. an `evidence:` line). Fail-closed:
    a completion claim with no evidence anywhere in the block is a violation.
    """
    unproven = []
    for t in tickets.parse(prj):
        st = t.status.lower()
        if not st.startswith(("done", "passed", "passing", "complete")):
            continue
        blob = " ".join([t.status, t.expected, t.task, *t.extra.values()])
        if not _EVIDENCE.search(blob):
            unproven.append(
                f"{t.id}: marked '{t.status[:24]}' but carries no evidence "
                f"(paste command+exit code, a file:line proof, or a commit — verification.md V1)."
            )
    return {"ok": not unproven, "unproven": unproven}
