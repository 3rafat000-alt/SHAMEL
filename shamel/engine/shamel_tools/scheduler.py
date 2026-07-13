"""
role: shared library (core/shamel_tools)
purpose: deterministic DAG scheduler — `shamel plan` freezes a task list into a
    DAG artifact, `shamel run` walks it mechanically. The ONE model call that
    decomposes a goal into tasks happens OUTSIDE this module (the CEO/Fable
    produces the task list); everything here is pure code — build/validate the
    graph, persist it, and answer "what's ready / are we done" with zero
    tokens spent on coordination (EVOLUTION.md Round 2 #1).
gate: 0-8 (scheduler is gate-agnostic; each node carries its own `gate`)
inputs: list[dict] task specs {id, room, agent, gate, deps:[ids], task, status?}
outputs: projects/<PRJ>/_context/PLAN.dag.json ; in-memory dag dict ; mermaid str
exit: 0 on success; raises ValueError on malformed/cyclic input, KeyError on
    unknown node id, FileNotFoundError when loading a DAG that was never saved.
"""
from __future__ import annotations

import json
from pathlib import Path

from . import paths, guard

_PLAN_FILE = "PLAN.dag.json"


def _dag_path(prj: str) -> Path:
    return paths.context_dir(prj) / _PLAN_FILE


def build_dag(tasks: list[dict]) -> dict:
    """Validate a flat task list into a DAG artifact {"nodes": {id: node}}.

    Raises ValueError on: missing/blank id, duplicate id, a dep referencing an
    unknown id, or a cycle (detected via topo_order). Deterministic — same
    task list always produces the same dag.
    """
    nodes: dict[str, dict] = {}
    for t in tasks:
        tid = t.get("id")
        if not tid:
            raise ValueError(f"task missing 'id': {t!r}")
        if tid in nodes:
            raise ValueError(f"duplicate task id: {tid}")
        nodes[tid] = {
            "id": tid,
            "room": t.get("room", ""),
            "agent": t.get("agent", ""),
            "gate": t.get("gate", ""),
            "deps": list(t.get("deps") or []),
            "task": t.get("task", ""),
            "status": t.get("status") or "open",
        }
    for nid, n in nodes.items():
        for d in n["deps"]:
            if d not in nodes:
                raise ValueError(f"{nid}: unknown dependency '{d}'")
    dag = {"nodes": nodes}
    topo_order(dag)  # raises ValueError on cycle
    return dag


def save_dag(prj: str, dag: dict) -> Path:
    """Freeze the DAG to projects/<PRJ>/_context/PLAN.dag.json."""
    f = _dag_path(prj)
    guard.assert_within_project(f, prj)
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(dag, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return f


def load_dag(prj: str) -> dict:
    """Read the frozen DAG back. Raises FileNotFoundError if never planned."""
    f = _dag_path(prj)
    if not f.exists():
        raise FileNotFoundError(f"no {_PLAN_FILE} for {prj} — run `shamel plan {prj}` first ({f})")
    return json.loads(f.read_text(encoding="utf-8"))


def topo_order(dag: dict) -> list[str]:
    """Kahn's algorithm. Deterministic (sorted tie-breaks). Raises ValueError
    naming the remaining node ids when a cycle prevents full ordering."""
    nodes = dag.get("nodes", {})
    indegree = {nid: 0 for nid in nodes}
    children: dict[str, list[str]] = {nid: [] for nid in nodes}
    for nid, n in nodes.items():
        for d in n["deps"]:
            if d not in nodes:
                raise ValueError(f"{nid}: unknown dependency '{d}'")
            children[d].append(nid)
            indegree[nid] += 1

    ready = sorted(nid for nid, deg in indegree.items() if deg == 0)
    order: list[str] = []
    while ready:
        ready.sort()
        nid = ready.pop(0)
        order.append(nid)
        for child in sorted(children[nid]):
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)

    if len(order) != len(nodes):
        remaining = sorted(set(nodes) - set(order))
        raise ValueError(f"cycle detected involving: {remaining}")
    return order


def ready_nodes(dag: dict) -> list[dict]:
    """Nodes whose status is 'open' and every dep is 'done'. Sorted by id."""
    nodes = dag.get("nodes", {})
    done = {nid for nid, n in nodes.items() if n.get("status") == "done"}
    out = []
    for nid in sorted(nodes):
        n = nodes[nid]
        if n.get("status") != "open":
            continue
        if all(d in done for d in n["deps"]):
            out.append(dict(n))
    return out


def mark(dag: dict, node_id: str, status: str) -> dict:
    """Set a node's status in place; returns the same dag for chaining."""
    nodes = dag.get("nodes", {})
    if node_id not in nodes:
        raise KeyError(f"unknown node id: {node_id}")
    nodes[node_id]["status"] = status
    return dag


def is_complete(dag: dict) -> bool:
    nodes = dag.get("nodes", {})
    return bool(nodes) and all(n.get("status") == "done" for n in nodes.values())


def to_mermaid(dag: dict) -> str:
    """Render the DAG as a mermaid flowchart (dashboard swimlane view)."""
    nodes = dag.get("nodes", {})
    lines = ["flowchart TD"]
    css = {"done": ":::done", "blocked": ":::blocked"}
    for nid in sorted(nodes):
        n = nodes[nid]
        who = n.get("agent") or n.get("room") or ""
        lines.append(f'    {nid}["{nid}: {who}"]{css.get(n.get("status", ""), "")}')
    for nid in sorted(nodes):
        for d in sorted(nodes[nid]["deps"]):
            lines.append(f"    {d} --> {nid}")
    lines.append("    classDef done fill:#9f9,stroke:#393;")
    lines.append("    classDef blocked fill:#f99,stroke:#933;")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import os
    import tempfile

    # ── DAG build + topo order + ready/mark/complete ────────────────────────
    tasks = [
        {"id": "A", "room": "arc", "agent": "arc-lead", "gate": 3, "deps": [], "task": "design schema"},
        {"id": "B", "room": "bck", "agent": "bck-api-engineer", "gate": 4, "deps": ["A"], "task": "build API"},
        {"id": "C", "room": "fnt", "agent": "fnt-ui-engineer", "gate": 4, "deps": ["A"], "task": "build UI"},
        {"id": "D", "room": "qa", "agent": "qa-lead", "gate": 5, "deps": ["B", "C"], "task": "integration test"},
    ]
    dag = build_dag(tasks)
    order = topo_order(dag)
    assert order.index("A") < order.index("B") < order.index("D"), order
    assert order.index("A") < order.index("C") < order.index("D"), order
    assert len(order) == 4 and set(order) == {"A", "B", "C", "D"}

    assert [n["id"] for n in ready_nodes(dag)] == ["A"], ready_nodes(dag)
    mark(dag, "A", "done")
    assert [n["id"] for n in ready_nodes(dag)] == ["B", "C"], ready_nodes(dag)
    assert not is_complete(dag)
    mark(dag, "B", "done")
    mark(dag, "C", "done")
    assert [n["id"] for n in ready_nodes(dag)] == ["D"], ready_nodes(dag)
    mark(dag, "D", "done")
    assert is_complete(dag)

    mer = to_mermaid(dag)
    assert mer.startswith("flowchart TD") and "A --> B" in mer and "B --> D" in mer

    # ── cycle detection ──────────────────────────────────────────────────
    try:
        build_dag([{"id": "X", "deps": ["Y"]}, {"id": "Y", "deps": ["X"]}])
        raise SystemExit("FAIL: cycle not detected")
    except ValueError as e:
        assert "cycle" in str(e)

    # ── duplicate id / unknown dep ──────────────────────────────────────
    try:
        build_dag([{"id": "A", "deps": []}, {"id": "A", "deps": []}])
        raise SystemExit("FAIL: duplicate id not detected")
    except ValueError:
        pass
    try:
        build_dag([{"id": "A", "deps": ["ghost"]}])
        raise SystemExit("FAIL: unknown dep not detected")
    except ValueError:
        pass

    # ── save/load round trip against a scratch project tree ────────────
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["SOFI_PROJECTS_DIR"] = tmp
        prj = "PRJ-TEST"
        (Path(tmp) / prj / "_context").mkdir(parents=True)
        fresh = build_dag(tasks)
        out_path = save_dag(prj, fresh)
        assert out_path.exists()
        loaded = load_dag(prj)
        assert loaded == fresh, "round trip must be exact"
        del os.environ["SOFI_PROJECTS_DIR"]

    print("PASS")
