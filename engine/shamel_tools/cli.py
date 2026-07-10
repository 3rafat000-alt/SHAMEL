"""
cli — the `shamel` dispatcher every agent calls.

    shamel projects                 list project workspaces
    shamel rooms                    list the 15 rooms (lead · members · gates)
    shamel registry [query]         print/query the org index (nexus/registry.yaml)
    shamel budget                   effort-scaling + budgeted-autonomy (nexus/routing.yaml)
    shamel brain   <PRJ>            show STATE + the next open ticket
    shamel route   <agent> [PRIO]   cheapest clearing route (model·effort·caveman)
    shamel gate-check <PRJ>         validate gate order + artifacts + rooms + evidence
    shamel dispatch <PRJ> [agent]   render the delegation prompt for the open ticket
    shamel squad <PRJ> <gate>       render parallel delegation for a gate's squad (3·4·5)
    shamel powers                   list the team's superpowers (external_powers)
    shamel handoff <PRJ> close <ID> mark a ticket done
    shamel escalate <PRJ> <ID> <to> "<reason>"  funnel a blocked ticket up-chain
    shamel scratch <PRJ> [clean]    list / purge ephemeral temp scripts
    shamel sync    <PRJ> [--push]   orient: fetch + switch to prj branch + show who did what
    shamel checkpoint <PRJ> "<msg>" commit early/often; auto-appends the SOFI: trailer
    shamel claim   <PRJ> <path>     soft-lock a shared path in LOCKS.md (before editing)
    shamel release <PRJ> <path>     drop a claim
    shamel worktree <PRJ> <gate> <squad>  isolated tree for a parallel squad (gate 3/4/5)
    shamel gate-merge <PRJ> <gate> <squad>  merge a squad's worktree into prj branch at gate close
    shamel gate-tag <PRJ> <gate>    immutable restore point <PRJ>-gate<N>-done
    shamel git-check <PRJ>          verify git hygiene (clean·no leaks·traceable) — gates pipeline
    shamel domain <action> [PRJ]    local domain: init·register·up·down·list·rm·status (e.g. sakk.local)
    shamel tunnel <action> [PRJ]    public tunnel: up·down·list·status (share <slug>.local on the internet)
    shamel oracle <op> ...          external review desk: review·capture·status (alias: shamel gemini)
    shamel tools                    list the tooling registry (shared + per-role scripts)
    shamel doctor                   self-check the library + governance (105↔105 agent parity)
    shamel plan   <PRJ> [--file F]  freeze a task list (JSON, --file or stdin) into PLAN.dag.json
    shamel run    <PRJ> [--mark ID:STATUS]  dry driver: render next dispatchable DAG nodes
    shamel resume <PRJ> [ticket]     machine-checkable resume: FRESH/DEGRADED/UNKNOWN vs git HEAD
    shamel events [-n N]             tail + summarize the fleet telemetry log
    shamel lint                      lint the agent roster (frontmatter·RCCF·parity·registry·pins)
    shamel recall <PRJ> --text Q     search the memory db (memdb) for a project

Exit 0 = ok, non-zero = a gate/governance check failed (CI can gate on it).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from . import (paths, brain, tickets, routing, gates, guard, runlog, gitops,
               domain, tunnel, registry, scheduler, memdb, resume,
               telemetry, agentlint, transitions)

_ROUTE_DELEGATION = """\
You are {role}. Project: {prj}.
BEFORE acting, read in order:
  - core/constitution/00-operating-system.md   (your contract)
  - core/constitution/06-git-discipline.md     (shared-repo rules — read once, obey always)
  - projects/{prj}/_context/STATE.md              (where we are — note branch + head_sha)
  - projects/{prj}/_context/HANDOFFS.md           (your ticket: {tkt})
  - projects/{prj}/_context/CONTEXT.md            (facts so far)
Then ORIENT git — never start blind:
  shamel sync {prj}        # fetch + switch to prj/{prj} + show prior sessions' checkpoints
  git log --oneline -8   # who did what under which ticket (SHAMEL: trailers)
Before editing a shared path: `shamel claim {prj} <path>` (check LOCKS.md first).
Your spec + Operating Prompt: {spec}
Your route: {route} (core/nexus/routing.yaml).
Ticket task: {task}
Expected artifact: {expected}
Do the work loop (00-operating-system.md). Tools per your registry grant
(core/nexus/registry.yaml).
CHECKPOINT as you go — never hold >1 artifact uncommitted:
  shamel checkpoint {prj} "<type>(<scope>): <subject>"
AFTER: write artifact, append CONTEXT.md, final `shamel checkpoint {prj} "..."`,
`shamel sync {prj} --push`, record head_sha in STATE.md, write the next ticket in
HANDOFFS.md, mark {tkt} done. An uncommitted session is invisible to the next one.
"""


def _spec_for(role: str) -> str:
    return registry.spec_path(role) or f"core/rooms/<room>/agents/{role}.md (not in registry — check shamel registry)"


def _need_project(prj: str) -> None:
    if not paths.project_exists(prj):
        print(f"✗ no such project: {prj} (scaffold with engine/bin/new-project.sh)", file=sys.stderr)
        raise SystemExit(2)


def cmd_projects(_a) -> int:
    pl = paths.list_projects()
    print("\n".join(pl) if pl else "(blank board — no projects)")
    return 0


def cmd_rooms(_a) -> int:
    """List the 15 rooms (غرف) with lead + member count, straight from the registry."""
    rooms = registry.rooms()
    if not rooms:
        print("✗ registry empty/unreadable: core/nexus/registry.yaml", file=sys.stderr)
        return 2
    total = 0
    print(f"━━ rooms — {len(rooms)} ━━")
    for code, r in rooms.items():
        n = len(r.get("agents", []))
        total += n
        print(f"  {r.get('emoji', '')} {code:4} {r.get('dir', ''):17} "
              f"lead {r.get('lead', '?'):22} {n:3} agents · gates {r.get('gates', '?')}")
    print(f"  TOTAL    : {total} agents")
    return 0


def cmd_registry(a) -> int:
    """Print/query the org index. No arg → per-room roster. With a query →
    case-insensitive substring match on agent id/title."""
    agents = registry.agents()
    if not agents:
        print("✗ registry empty/unreadable: core/nexus/registry.yaml", file=sys.stderr)
        return 2
    q = (a.query or "").lower()
    if not q:
        for code, r in registry.rooms().items():
            print(f"{r.get('emoji', '')} {code} — {r.get('name', '')} (lead: {r.get('lead', '?')})")
            for aid in r.get("agents", []):
                ag = agents.get(aid, {})
                mark = "★" if aid == r.get("lead") else "·"
                print(f"  {mark} {aid:26} {ag.get('route', ''):28} {ag.get('title', '')[:52]}")
        return 0
    hits = [ag for aid, ag in agents.items()
            if q in aid.lower() or q in ag.get("title", "").lower()]
    if not hits:
        print(f"(no agent matches '{a.query}')")
        return 1
    for ag in hits:
        print(f"━━ {ag['id']} ━━")
        print(f"  room     : {ag.get('room', '?')}" + ("  (Room Lead)" if registry.is_lead(ag["id"]) else ""))
        print(f"  title    : {ag.get('title', '')}")
        print(f"  route    : {ag.get('route', '')}  | budget {ag.get('budget', '')}")
        print(f"  spec     : {ag.get('spec', '')}")
        print(f"  spawnable: {ag.get('spawnable', '')}")
        tools = ag.get("tools")
        print(f"  tools    : {tools if isinstance(tools, str) else ', '.join(tools or [])}")
    return 0


def cmd_budget(_a) -> int:
    """Surface the spawn-width grid + hard-ceiling doctrine from nexus/routing.yaml
    (what gtw-budget-warden audits against)."""
    data = routing._load()
    eff = data.get("effort_scaling") or {}
    auto = data.get("budgeted_autonomy") or {}
    if not eff and not auto:
        print("✗ effort_scaling/budgeted_autonomy not found in core/nexus/routing.yaml",
              file=sys.stderr)
        return 2
    print("━━ effort_scaling (spawn-width axis) ━━")
    for k, v in eff.items():
        if isinstance(v, dict):
            sub = v.get("subagents", "?")
            sub = {True: "yes", False: "no"}.get(sub, str(sub))   # yaml no/ok/yes
            print(f"  {k:12} spawn {str(v.get('spawn', '?')):4} · subagents {sub:3} "
                  f"· calls {v.get('budget_calls', '?')}")
            if v.get("note"):
                print(f"               {v['note']}")
        else:
            print(f"  {k:12} {v}")
    print("━━ budgeted_autonomy ━━")
    for k, v in auto.items():
        print(f"  {k}: {v}")
    return 0


def cmd_brain(a) -> int:
    _need_project(a.prj)
    st = brain.read_state(a.prj)
    print(f"━━ {a.prj} ━━")
    for k in ("title", "gate", "active", "status", "priority", "blockers", "last_route"):
        if k in st:
            print(f"  {k:10} {st[k]}")
    nxt = tickets.next_open(a.prj)
    if nxt:
        print(f"  next-open  {nxt.id} (gate {nxt.gate}) → {nxt.to}: {nxt.task[:60]}")
    else:
        print("  next-open  (none — queue clear)")
    return 0


def cmd_brain_facts(a) -> int:
    """Generate counted facts block with sha for a project."""
    import hashlib, json
    _need_project(a.prj)
    prj = paths.project_dir(a.prj)
    # Count models, controllers, tests, migrations, blade files
    counts = {}
    for pat, label in [("**/*.php", "php_files"), ("**/*.py", "py_files"),
                       ("**/*.js", "js_files"), ("**/*.vue", "vue_files"),
                       ("**/*.blade.php", "blade_files")]:
        files = list(prj.glob(pat)) if prj.exists() else []
        counts[label] = len(files)
    counts_sha = hashlib.sha256(json.dumps(counts, sort_keys=True).encode()).hexdigest()[:12]
    print(json.dumps({"counts": counts, "counts_sha": counts_sha}, indent=2))
    return 0


def cmd_brain_audit(a) -> int:
    """Compare brain facts against code; exit ≠0 on deviation."""
    import subprocess, json
    _need_project(a.prj)
    # Re-run brain facts to get current SHA
    result = subprocess.run([sys.argv[0], "brain-facts", a.prj],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ brain-facts failed: {result.stderr}", file=sys.stderr)
        return 2
    try:
        current = json.loads(result.stdout)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"✗ brain-facts output invalid: {e}", file=sys.stderr)
        return 2
    # Read the stored counts_sha from STATE.md
    st_path = paths.project_dir(a.prj) / "_context" / "STATE.md"
    if st_path.exists():
        stored = st_path.read_text()
        import re
        m = re.search(r'counts_sha[:\s]+(\w+)', stored)
        if m and m.group(1) != current["counts_sha"]:
            print(f"✗ counts_sha MISMATCH: stored={m.group(1)} current={current['counts_sha']}")
            print(f"  Run `shamel brain-facts {a.prj}` and update STATE.md")
            return 1
        elif m:
            print(f"✓ counts_sha match: {current['counts_sha']}")
            return 0
        else:
            print(f"~ STATE.md has no counts_sha field — run brain-facts to generate")
            return 0
    else:
        print(f"~ No STATE.md found at {st_path}")
        return 0


def cmd_brain_query(a) -> int:
    """Structured-brain query: `shamel brain-query PRJ status=blocked type=feature`.
    Filters the ticket queue by any field (canonical or frontmatter) — case-insensitive
    substring match. Empty filters lists every ticket."""
    _need_project(a.prj)
    filters: dict[str, str] = {}
    for f in a.filters:
        if "=" not in f:
            print(f"  bad filter '{f}' — use key=value"); return 2
        k, v = f.split("=", 1)
        filters[k.strip()] = v.strip()
    rows = tickets.query(a.prj, **filters)
    label = " · ".join(f"{k}={v}" for k, v in filters.items()) or "all"
    print(f"━━ brain-query {a.prj} [{label}] — {len(rows)} match ━━")
    for t in rows:
        extra = " ".join(f"{k}={v}" for k, v in t.extra.items() if k in ("type", "mem"))
        print(f"  {t.id} · gate {t.gate} · {t.status[:24]:24} {extra}  {t.task[:48]}")
    return 0


def cmd_route(a) -> int:
    try:
        r = routing.route_for(a.role, a.priority)
    except KeyError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    print(f"{r['tier']} {r['model']} ({r['model_id']}) · {r['effort']} · {r['caveman']}"
          f"  | gate {r['gate']} | budget {r['budget']} | priority {r['priority']}")
    return 0


def cmd_gate_check(a) -> int:
    _need_project(a.prj)
    order = gates.validate_no_skip(a.prj)
    arts = gates.validate_artifacts(a.prj)
    room = gates.validate_room_boundary(a.prj)
    evid = gates.validate_evidence(a.prj)
    print(f"━━ gate-check {a.prj} ━━")
    print(f"  sequence : {' '.join(map(str, order['sequence']))}")
    print(f"  no-skip  : {'✓' if order['ok'] else '✗ ' + '; '.join(order['skips'])}")
    if order.get("transitions"):
        print(f"  hops     : {' · '.join(order['transitions'])}")
    if order["loops"]:
        print(f"  loops    : {', '.join(order['loops'])}")
    print(f"  artifacts: {'✓ all ' + str(len(arts['checked'])) + ' present' if arts['ok'] else '✗ missing ' + '; '.join(arts['missing'])}")
    print(f"  rooms    : {'✓ no boundary violations' if room['ok'] else '✗ ' + '; '.join(room['violations'])}")
    print(f"  evidence : {'✓ done-tickets carry proof' if evid['ok'] else '✗ ' + '; '.join(evid['unproven'])}")
    ok = order["ok"] and arts["ok"] and room["ok"] and evid["ok"]
    if a.to_gate is not None:
        adv = transitions.check_gate_advance(a.prj, a.to_gate)
        mark = "✓" if adv["ok"] else "✗"
        print(f"  advance→{a.to_gate} : {mark} {adv['kind']} — {adv['reason']}")
        ok = ok and adv["ok"]
    print(f"  VERDICT  : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def cmd_plan(a) -> int:
    """Freeze a task list into a DAG (`scheduler.build_dag`+`save_dag`) and
    print it as mermaid. Tasks JSON: a list of {id, room, agent, gate, deps,
    task, status?} dicts, read from --file or stdin."""
    _need_project(a.prj)
    raw = Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
    try:
        tasks = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"✗ invalid tasks JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(tasks, list):
        print("✗ tasks JSON must be a list of task objects", file=sys.stderr)
        return 2
    try:
        dag = scheduler.build_dag(tasks)
    except ValueError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    out = scheduler.save_dag(a.prj, dag)
    print(f"✓ saved {out} ({len(dag['nodes'])} node(s))")
    print(scheduler.to_mermaid(dag))
    return 0


def cmd_run(a) -> int:
    """Dry driver: load the frozen DAG, optionally mark one node, render the
    next dispatchable (ready) nodes. Never spawns a model."""
    _need_project(a.prj)
    try:
        dag = scheduler.load_dag(a.prj)
    except FileNotFoundError as e:
        print(f"✗ {e}", file=sys.stderr)
        return 2
    if a.mark:
        if ":" not in a.mark:
            print("✗ --mark must be NODE_ID:STATUS", file=sys.stderr)
            return 2
        nid, status = a.mark.split(":", 1)
        try:
            scheduler.mark(dag, nid, status)
        except KeyError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 2
        scheduler.save_dag(a.prj, dag)
        print(f"✓ marked {nid} → {status}")
    if scheduler.is_complete(dag):
        print("✓ DAG complete — all nodes done")
        return 0
    ready = scheduler.ready_nodes(dag)
    if not ready:
        print("(no ready nodes — blocked on open deps, or an empty plan)")
        return 0
    print(f"━━ ready nodes ({len(ready)}) ━━")
    for n in ready:
        print(f"  {n['id']:12} {n.get('room', ''):5} {n.get('agent', ''):26} "
              f"gate {n.get('gate', '')}: {n.get('task', '')[:60]}")
    return 0


def cmd_resume(a) -> int:
    """Machine-checkable resume: classify a ticket (or the latest breadcrumb)
    FRESH/DEGRADED/UNKNOWN against the project repo's actual current HEAD."""
    _need_project(a.prj)
    proc = subprocess.run(
        ["git", "-C", str(paths.project_repo(a.prj)), "rev-parse", "HEAD"],
        capture_output=True, text=True,
    )
    current_head = proc.stdout.strip() if proc.returncode == 0 else ""
    if not current_head:
        print(f"✗ could not resolve current HEAD for {a.prj}", file=sys.stderr)
        return 2
    ticket = a.ticket
    if not ticket:
        crumb = resume.latest_breadcrumb(a.prj)
        if not crumb:
            print(f"(no breadcrumbs yet for {a.prj})")
            return 0
        ticket = crumb.get("ticket", "")
    result = resume.classify(a.prj, ticket, current_head)
    print(f"━━ resume {a.prj} {ticket} ━━")
    print(f"  mode      : {result['mode']}")
    print(f"  reason    : {result['reason']}")
    print(f"  next_step : {result['next_step']}")
    return 0 if result["mode"] != "DEGRADED" else 1


def cmd_events(a) -> int:
    events = telemetry.read_events(a.n)
    summary = telemetry.summarize_events(events)
    print(f"━━ events — last {len(events)} (of log) ━━")
    print(f"  total     : {summary['total']}")
    print(f"  by_source : {summary['by_source']}")
    print(f"  by_kind   : {summary['by_kind']}")
    print(f"  by_agent  : {summary['by_agent']}")
    if a.verbose:
        for e in events[-20:]:
            print(f"  {e}")
    return 0


def cmd_lint(a) -> int:
    return agentlint.main(a.rest)


def cmd_recall(a) -> int:
    _need_project(a.prj)
    hits = memdb.search(a.text, k=a.k, project=a.prj)
    if not hits:
        print("(no matches)")
        return 0
    print(f"━━ recall {a.prj} — {len(hits)} match(es) ━━")
    for h in hits:
        if h["type"] == "observation":
            print(f"  [{h['id']}] obs · {h.get('kind', '')} · {h.get('ts', '')} — {h['summary']}")
        else:
            print(f"  [{h['id']}] sec · {h.get('heading', '')} ({h.get('file', '')}) — {h['summary']}")
    return 0


def cmd_dispatch(a) -> int:
    _need_project(a.prj)
    t = tickets.next_open(a.prj)
    if t is None:
        print("(no open ticket to dispatch)")
        return 0
    role = a.role or t.to
    try:
        route = routing.format_route(role)
    except KeyError:
        route = "(set route per core/nexus/routing.yaml)"
    print(_ROUTE_DELEGATION.format(
        role=role, prj=a.prj, tkt=t.id, route=route, spec=_spec_for(role),
        task=t.task or "(see ticket)", expected=t.expected or "(see ticket)"))
    return 0


def cmd_handoff(a) -> int:
    _need_project(a.prj)
    if a.op == "close":
        ok = tickets.set_status(a.prj, a.tkt, "done")
    else:
        ok = tickets.set_status(a.prj, a.tkt, a.op)
    print(f"{'✓' if ok else '✗ not found:'} {a.tkt} → {a.op}")
    return 0 if ok else 2


def cmd_escalate(a) -> int:
    _need_project(a.prj)
    tk = next((t for t in tickets.parse(a.prj) if t.id == a.tkt), None)
    if tk is None:
        print(f"✗ no such ticket: {a.tkt}", file=sys.stderr)
        return 2
    nid = tickets.escalate(a.prj, tkt_id=a.tkt, frm=(tk.to or "?"),
                           to=a.to, reason=a.reason, gate=tk.gate)
    print(f"✓ escalated {a.tkt} ({tk.to or '?'}) → {a.to} as {nid}")
    return 0


def cmd_scratch(a) -> int:
    _need_project(a.prj)
    sd = paths.scratch_dir(a.prj)
    sd.mkdir(parents=True, exist_ok=True)
    scripts = sorted(p.name for p in sd.glob("*.py"))
    if a.clean:
        for p in sd.glob("*.py"):
            guard.assert_within_project(p, a.prj)
            p.unlink()
        print(f"✓ purged {len(scripts)} temp script(s) from {a.prj}/_scratch/")
        return 0
    print(f"{a.prj}/_scratch/ — {len(scripts)} temp script(s):")
    for s in scripts:
        print(f"  {s}")
    return 0


def cmd_sync(a) -> int:
    _need_project(a.prj)
    return gitops.sync(a.prj, push=a.push)


def cmd_checkpoint(a) -> int:
    _need_project(a.prj)
    return gitops.checkpoint(a.prj, a.message)


def cmd_claim(a) -> int:
    _need_project(a.prj)
    return gitops.claim(a.prj, a.path)


def cmd_release(a) -> int:
    _need_project(a.prj)
    return gitops.claim(a.prj, a.path, release_it=True)


def cmd_worktree(a) -> int:
    _need_project(a.prj)
    return gitops.worktree(a.prj, str(a.gate), a.squad)


def cmd_gate_merge(a) -> int:
    _need_project(a.prj)
    return gitops.gate_merge(a.prj, str(a.gate), a.squad)


def cmd_gate_tag(a) -> int:
    _need_project(a.prj)
    return gitops.gate_tag(a.prj, str(a.gate))


def cmd_git_check(a) -> int:
    _need_project(a.prj)
    return gitops.git_check(a.prj)


def cmd_domain(a) -> int:
    return domain.run(a.action, getattr(a, "prj", None), getattr(a, "slug", None))


def cmd_tunnel(a) -> int:
    return tunnel.run(a.action, getattr(a, "prj", None), getattr(a, "provider", None))


def cmd_agents(a) -> int:
    """Generate spawnable .claude/agents/*.md from legal core/rooms/*/agents/*.md specs."""
    from pathlib import Path
    import shutil

    op = a.op or "build"
    root = Path(paths.repo_root())
    claude_agents = root / ".claude" / "agents"
    claude_agents.mkdir(parents=True, exist_ok=True)

    if op == "build":
        specs = sorted(root.glob("core/rooms/*/agents/*.md"))
        if not specs:
            print("✗ no agent specs found in core/rooms/*/agents/")
            return 2
        count = 0
        for spec in specs:
            agent_id = spec.stem
            content = spec.read_text(encoding="utf-8")

            # Extract frontmatter fields
            desc = agent_id
            model = "inherit"
            tools = "Read, Edit, Write, Bash, Grep"
            for line in content.splitlines():
                if line.startswith("success_metric:"):
                    desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                if line.startswith("tools:"):
                    tools = line.split(":", 1)[1].strip().strip("[]").strip()

            # Generate spawnable with explicit tools from legal spec
            spawnable = f"""---
name: {agent_id}
description: "{desc}"
model: {model}
tools: [{tools}]
---

{desc}
"""
            out = claude_agents / f"{agent_id}.md"
            out.write_text(spawnable, encoding="utf-8")
            print(f"  {agent_id}")
            count += 1
        print(f"\n{count} spawnables written to .claude/agents/")
        return 0

    elif op == "lint":
        # Check: every spec file has tools: and authority: in frontmatter
        ok = True
        specs = sorted(root.glob("core/rooms/*/agents/*.md"))
        for spec in specs:
            content = spec.read_text(encoding="utf-8")
            if "tools:" not in content:
                print(f"  ✗ {spec.stem}: missing tools: in frontmatter")
                ok = False
            if "authority:" not in content:
                print(f"  ✗ {spec.stem}: missing authority: in frontmatter")
                ok = False
        if ok:
            print("✓ all 105 agent specs pass lint")
        return 0 if ok else 1

    elif op == "pins":
        import hashlib
        specs = sorted(root.glob("core/rooms/*/agents/*.md"))
        pins = {}
        for spec in specs:
            sha = hashlib.sha256(spec.read_bytes()).hexdigest()
            pins[spec.stem] = sha
        pins_path = root / "core" / "nexus" / "pins.json"
        import json
        pins_path.write_text(json.dumps({"version": 1, "pins": pins, "count": len(pins)},
                                         indent=2), encoding="utf-8")
        print(f"{len(pins)} pins written to core/nexus/pins.json")
        return 0

    return 0


def cmd_tools(_a) -> int:
    reg = paths.tooling_dir() / "registry.yaml"
    print(reg.read_text(encoding="utf-8") if reg.exists() else "(no registry.yaml)")
    return 0


# Parallel squads per gate — v6 room specialists behind the frozen upstream input
# (nexus/gates.yaml squad_rooms; effort class: cross-room).
_SQUADS = {
    "3": ["arc-data-architect", "arc-api-architect", "sec-threat-modeler"],
    "4": ["dat-db-engineer", "bck-api-engineer", "bck-blade-engineer",
          "fnt-vue-engineer", "mob-flutter-engineer"],
    "5": ["qa-automation-engineer", "qa-manual-explorer",
          "qa-perf-analyst", "sec-pentester"],
}


def cmd_squad(a) -> int:
    """Render parallel delegation prompts for a gate's squad — agents run concurrently
    behind the frozen upstream input (the parallelism pattern, as a command)."""
    _need_project(a.prj)
    roles = _SQUADS.get(str(a.gate))
    if not roles:
        print(f"✗ no parallel squad for gate {a.gate} (squads: {', '.join(_SQUADS)})", file=sys.stderr)
        return 2
    t = tickets.next_open(a.prj)
    tkt = t.id if t else "(open a ticket in HANDOFFS)"
    print(f"━━ Gate {a.gate} parallel squad — {len(roles)} agents run CONCURRENTLY ━━")
    for role in roles:
        try:
            route = routing.format_route(role)
        except KeyError:
            route = "(set route per core/nexus/routing.yaml)"
        print("\n" + _ROUTE_DELEGATION.format(
            role=role, prj=a.prj, tkt=tkt, route=route, spec=_spec_for(role),
            task="your slice of this gate — see your ticket in HANDOFFS.md",
            expected="your gate artifact (no skipping)"))
    return 0


def cmd_powers(a) -> int:
    """Surface the team's superpowers (external_powers) from the tooling registry."""
    reg = paths.tooling_dir() / "registry.yaml"
    if not reg.exists():
        print("(no registry.yaml)")
        return 0
    out, grab = [], False
    for ln in reg.read_text(encoding="utf-8").splitlines():
        if ln.startswith("external_powers:"):
            grab = True
        elif grab and ln and not ln[0].isspace() and not ln.lstrip().startswith("#"):
            break
        if grab:
            out.append(ln)
    print("\n".join(out) if out else "(no external_powers — see company/superpowers/SUPERPOWERS.md)")
    print("\nfull catalog: company/superpowers/SUPERPOWERS.md")
    return 0


def cmd_doctor(a) -> int:
    import re as _re, glob as _glob
    print("━━ shamel doctor ━━")
    ok = True
    root = None
    try:
        root = paths.repo_root()
        print(f"  workspace : {root}")
    except Exception as e:
        print(f"  workspace : ✗ {e}"); ok = False
    try:
        nroutes = len(routing.all_roles())
        print(f"  routing   : ✓ {nroutes} routes (core/nexus/routing.yaml)")
    except Exception as e:
        print(f"  routing   : ✗ {e}"); ok = False
    nreg = len(registry.agents())
    nrooms = len(registry.rooms())
    if nreg and nrooms:
        print(f"  registry  : ✓ {nrooms} rooms · {nreg} agents (core/nexus/registry.yaml)")
    else:
        print("  registry  : ✗ core/nexus/registry.yaml empty or unreadable"); ok = False
    print(f"  net-roles : {len(guard.NET_ALLOWED_ROLES)} agents may reach the web")
    print(f"  projects  : {len(paths.list_projects())}")

    # ── agent wiring: spawnables ↔ room specs (dual-file parity, 105 ↔ 105) ──
    if root:
        subs = _glob.glob(str(root / ".claude/agents/*.md"))
        specs = _glob.glob(str(root / "core/rooms/*/agents/*.md"))
        if len(subs) == len(specs) == 105:
            print(f"  agents    : ✓ {len(subs)} spawnables ↔ {len(specs)} room specs (105↔105)")
        elif len(subs) == len(specs):
            if len(subs) == 0:
                print(f"  agents    : ~ no agents yet (Phase 4 delivers 105)")
            else:
                print(f"  agents    : ~ parity {len(subs)}↔{len(specs)} but roster target is 105")
        else:
            print(f"  agents    : ✗ {len(subs)} spawnables ≠ {len(specs)} room specs"); ok = False

    # ── registry claims: every cited .claude/skills path must exist ───────
    # catches a skill row whose SKILL.md is missing.
    if root:
        reg = root / "core/nexus/registry.yaml"
        broken = []
        if reg.exists():
            for m in _re.findall(r'\.claude/skills/[A-Za-z0-9_./-]+',
                                 reg.read_text(encoding="utf-8", errors="ignore")):
                if not (root / m).exists():
                    broken.append(m)
        if broken:
            print(f"  skills    : ✗ registry cites {len(broken)} missing path(s): "
                  f"{', '.join(sorted(set(broken)))}"); ok = False
        else:
            print("  skills    : ✓ registry skill paths exist")

    # ── brain checks (--brain flag adds detailed brain audit) ──────────────
    brain_ok = True
    if root and getattr(a, "brain", False):
        brain_dir = root / "brain"
        if not brain_dir.exists():
            print("  brain     : ✗ brain/ directory not found"); brain_ok = False
        else:
            # Count templates
            tmpl = list(brain_dir.glob("templates/*.md"))
            print(f"  brain     : templates: {len(tmpl)}/8")
            if len(tmpl) < 8:
                print(f"             ✗ expected 8 templates, got {len(tmpl)}"); brain_ok = False
            # Check OWNERS.yaml parses
            owners_path = brain_dir / "OWNERS.yaml"
            if owners_path.exists():
                try:
                    import yaml
                    own = yaml.safe_load(owners_path.read_text())
                    assert own.get("version") == 1
                    n_own = len(own.get("owners", {}))
                    print(f"             : OWNERS.yaml: {n_own} entries")
                except Exception as e:
                    print(f"             ✗ OWNERS.yaml: {e}"); brain_ok = False
            else:
                print("             ✗ OWNERS.yaml missing"); brain_ok = False
            # Check brain.db exists and has observations
            db_path = brain_dir / "db" / "brain.db"
            if db_path.exists():
                import sqlite3
                try:
                    conn = sqlite3.connect(str(db_path))
                    n_obs = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]
                    print(f"             : brain.db: {n_obs} observations")
                    conn.close()
                except Exception as e:
                    print(f"             ✗ brain.db: {e}"); brain_ok = False
            else:
                print("             ✗ brain.db missing"); brain_ok = False
            # Check LESSONS sig format
            lessons_path = brain_dir / "org" / "LESSONS.md"
            if lessons_path.exists():
                lessons_text = lessons_path.read_text()
                if "LES-" in lessons_text or "LES-NNN" in lessons_text:
                    print(f"             : LESSOMS: sig format")
                else:
                    print(f"             ✗ LESSONS: missing sig format"); brain_ok = False
        if brain_ok:
            print(f"  brain     : ✓ PASS")
        else:
            ok = False

    print(f"  VERDICT   : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def cmd_selftest(a) -> int:
    """Run the selftest suite."""
    import subprocess
    selftest = paths.engine_dir() / "selftest" / "selftest.sh"
    if not selftest.exists():
        print("✗ selftest not found", file=sys.stderr)
        return 2
    result = subprocess.run(["bash", str(selftest)], capture_output=True, text=True)
    try:
        import json
        d = json.loads(result.stdout)
        if a.json:
            print(result.stdout)
        else:
            for r in d.get("results", []):
                status = "✓" if r["status"] == "PASS" else "✗"
                print(f"  {status}  {r['name']}")
            print(f"  VERDICT: {'PASS' if d.get('pass') else 'FAIL'} ({d.get('passed',0)}/{d.get('tests',0)})")
        return 0 if d.get("pass") else 1
    except (json.JSONDecodeError, KeyError) as e:
        print(f"✗ selftest parse error: {e}", file=sys.stderr)
        print(result.stdout)
        return 2


def cmd_oracle(a) -> int:
    """External review desk: forward to gemini_review.py (push→receive→parse→act).
    `shamel oracle ...` is the v6 verb; `shamel gemini ...` stays as the muscle-memory alias."""
    import subprocess
    script = paths.tooling_dir() / "agents" / "ceo" / "gemini_review.py"
    if not script.exists():
        print(f"✗ gemini_review.py not found at {script}", file=sys.stderr)
        return 2
    return subprocess.call([sys.executable, str(script), a.op, *a.rest])


def cmd_new(a) -> int:
    """Scaffold new project: git init + remote + commit#1 + _context/ + domain register."""
    import subprocess, shutil
    prj_dir = paths.project_dir(a.prj)
    if prj_dir.exists():
        print(f"✗ project {a.prj} already exists at {prj_dir}", file=sys.stderr); return 2
    prj_dir.mkdir(parents=True)
    try:
        # git init
        subprocess.run(["git", "init", "-b", "main"], cwd=str(prj_dir), check=True,
                       capture_output=True, timeout=15)
        # _context from templates
        ctx = prj_dir / "_context"
        ctx.mkdir()
        tmpl = paths.repo_root() / "brain" / "templates"
        if tmpl.exists():
            for t in tmpl.glob("*.md"):
                shutil.copy2(str(t), str(ctx / t.name))
        # STATE.md with project identity
        state = ctx / "STATE.md"
        state.write_text(
            f"# {a.prj}\n---\ntitle: {a.title}\n"
            f"branch: main\nhead_sha: none\ngate: 0\n"
            f"priority: {a.priority}\nstatus: inception\n"
            f"active: str-lead\n---\n")
        # CONTEXT.md stub
        (ctx / "CONTEXT.md").write_text(f"# {a.prj} Context\n\nInitial scaffolding.\n")
        # HANDOFFS.md
        (ctx / "HANDOFFS.md").write_text(f"# Handoffs\n\n## Gate-0 / Ticket-001\n\nInit {a.title}\n")
        # first commit
        subprocess.run(["git", "add", "-A"], cwd=str(prj_dir), check=True, capture_output=True, timeout=15)
        subprocess.run(["git", "commit", "-m", f"feat({a.prj}): init {a.title}\n\nSHAMEL: {a.prj} · gate 0 · str-lead"],
                       cwd=str(prj_dir), check=True, capture_output=True, timeout=15)
        print(f"✓ {a.prj} scaffolded at {prj_dir}")
        # domain register
        try:
            subprocess.run(["engine/bin/shamel", "domain", "register", a.prj], timeout=10)
        except Exception:
            print("  ~ domain register skipped (not available)")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"✗ scaffold failed: {e.stderr.decode() if e.stderr else e}", file=sys.stderr)
        shutil.rmtree(str(prj_dir), ignore_errors=True)
        return 2


def cmd_gate_advance(a) -> int:
    """Advance gate: validate then tag. V2: adversarial check follows in CI."""
    _need_project(a.prj)
    # Validate current gate can advance to to_gate
    cur = gates.validate_no_skip(a.prj)
    current_gate = max(list(cur.keys())) if cur else 0
    if a.to_gate <= current_gate:
        print(f"✗ already at gate {current_gate} (requested {a.to_gate})", file=sys.stderr)
        return 2
    # Run gate check
    print(f"  gate-check gate-{current_gate} → gate-{a.to_gate} ...")
    check_passed = True
    for fn_name, fn in [("no_skip", gates.validate_no_skip),
                        ("artifacts", gates.validate_artifacts),
                        ("room_boundary", gates.validate_room_boundary)]:
        try:
            result = fn(a.prj)
            if isinstance(result, dict) and "errors" in result and result["errors"]:
                print(f"  ✗ {fn_name}: {result['errors']}"); check_passed = False
            else:
                print(f"  ✓ {fn_name}")
        except Exception as e:
            print(f"  ✗ {fn_name}: {e}"); check_passed = False
    if not check_passed:
        print(f"✗ gate advance to {a.to_gate} BLOCKED — fix errors above", file=sys.stderr)
        return 1
    # Tag
    import subprocess
    tag = f"{a.prj}-gate-{a.to_gate}-done"
    try:
        subprocess.run(["git", "tag", "-a", tag, "-m", f"Gate {a.to_gate}"],
                       cwd=a.prj, check=True, capture_output=True, timeout=10)
        print(f"  ✓ tagged {tag}")
    except subprocess.CalledProcessError as e:
        print(f"  ✗ tag failed: {e.stderr.decode() if e.stderr else e}", file=sys.stderr)
        return 2
    print(f"✓ gate-{a.to_gate} advanced. Next: adversarial check via gtw-gatekeeper.")
    return 0


def cmd_reflect(a) -> int:
    """Run reflection/dreaming loop: distil lessons from HANDOFFS into LESSONS."""
    import subprocess, json
    if a.prj:
        # Per-project reflection
        ctx = paths.project_dir(a.prj) / "_context"
        if not ctx.exists():
            print(f"✗ no _context for {a.prj}", file=sys.stderr); return 2
        handoffs = ctx / "HANDOFFS.md"
        lessons = ctx / "LESSONS.md"
        if handoffs.exists():
            h_text = handoffs.read_text()
            # Count tickets
            tickets_found = sum(1 for l in h_text.splitlines() if l.startswith("## "))
            print(f"  {a.prj}: {tickets_found} ticket(s) found in HANDOFFS.md")
            print(f"  Run `shamel brain recall {a.prj} --text lessons` to search memory.")
            print(f"  To write a lesson, add to {lessons} in sig format.")
        else:
            print(f"  {a.prj}: no HANDOFFS.md found")
    else:
        # Org-level reflection: check brain/org/LESSONS.md
        lessons_path = paths.repo_root() / "brain" / "org" / "LESSONS.md"
        if lessons_path.exists():
            lessons_text = lessons_path.read_text()
            sig_count = lessons_text.count("LES-") if "LES-" in lessons_text else 0
            print(f"  org-level LESSONS: ~{sig_count} lessons (sig format)")
        else:
            print(f"  no org LESSONS.md found")
    print("✓ reflect done. To schedule: add `claude -p '/reflect'` to cron.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="shamel", description="SOFI AI agent tooling dispatcher")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("projects").set_defaults(fn=cmd_projects)

    sub.add_parser("rooms", help="list the 15 rooms: lead · member count · gates").set_defaults(fn=cmd_rooms)

    s = sub.add_parser("registry", help="print/query the org index (core/nexus/registry.yaml)")
    s.add_argument("query", nargs="?", default=None); s.set_defaults(fn=cmd_registry)

    sub.add_parser("budget", help="effort_scaling + budgeted_autonomy from nexus/routing.yaml").set_defaults(fn=cmd_budget)

    s = sub.add_parser("brain", help="show project brain state"); s.add_argument("prj"); s.set_defaults(fn=cmd_brain)

    s = sub.add_parser("brain-facts", help="generate counted facts block with sha")
    s.add_argument("prj"); s.set_defaults(fn=cmd_brain_facts)

    s = sub.add_parser("brain-audit", help="compare brain facts against code; exit ≠0 on deviation")
    s.add_argument("prj"); s.set_defaults(fn=cmd_brain_audit)

    s = sub.add_parser("brain-query", help="query the ticket queue by field, e.g. status=blocked type=feature")
    s.add_argument("prj"); s.add_argument("filters", nargs="*", default=[])
    s.set_defaults(fn=cmd_brain_query)

    s = sub.add_parser("route"); s.add_argument("role")
    s.add_argument("priority", nargs="?", default=None); s.set_defaults(fn=cmd_route)

    s = sub.add_parser("gate-check"); s.add_argument("prj")
    s.add_argument("--to-gate", type=int, default=None, dest="to_gate",
                   help="also validate this proposed advance via transitions.check_gate_advance")
    s.set_defaults(fn=cmd_gate_check)

    s = sub.add_parser("dispatch"); s.add_argument("prj")
    s.add_argument("role", nargs="?", default=None); s.set_defaults(fn=cmd_dispatch)

    s = sub.add_parser("squad"); s.add_argument("prj"); s.add_argument("gate")
    s.set_defaults(fn=cmd_squad)

    sub.add_parser("powers").set_defaults(fn=cmd_powers)

    s = sub.add_parser("handoff"); s.add_argument("prj")
    s.add_argument("op"); s.add_argument("tkt"); s.set_defaults(fn=cmd_handoff)

    s = sub.add_parser("escalate"); s.add_argument("prj")
    s.add_argument("tkt"); s.add_argument("to"); s.add_argument("reason")
    s.set_defaults(fn=cmd_escalate)

    s = sub.add_parser("scratch"); s.add_argument("prj")
    s.add_argument("clean", nargs="?", const=True, default=False,
                   help="pass 'clean' to purge temp scripts")
    s.set_defaults(fn=cmd_scratch)

    s = sub.add_parser("sync"); s.add_argument("prj")
    s.add_argument("--push", action="store_true"); s.set_defaults(fn=cmd_sync)

    s = sub.add_parser("checkpoint"); s.add_argument("prj")
    s.add_argument("message"); s.set_defaults(fn=cmd_checkpoint)

    s = sub.add_parser("claim"); s.add_argument("prj")
    s.add_argument("path"); s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("release"); s.add_argument("prj")
    s.add_argument("path"); s.set_defaults(fn=cmd_release)

    s = sub.add_parser("worktree"); s.add_argument("prj")
    s.add_argument("gate"); s.add_argument("squad"); s.set_defaults(fn=cmd_worktree)

    s = sub.add_parser("gate-merge"); s.add_argument("prj")
    s.add_argument("gate"); s.add_argument("squad"); s.set_defaults(fn=cmd_gate_merge)

    s = sub.add_parser("gate-tag"); s.add_argument("prj")
    s.add_argument("gate"); s.set_defaults(fn=cmd_gate_tag)

    s = sub.add_parser("git-check"); s.add_argument("prj"); s.set_defaults(fn=cmd_git_check)

    s = sub.add_parser("domain", help="local domains: init|register|up|down|list|rm|status")
    s.add_argument("action", choices=["init", "register", "up", "down", "list", "rm", "status"])
    s.add_argument("prj", nargs="?", default=None)
    s.add_argument("slug", nargs="?", default=None)
    s.set_defaults(fn=cmd_domain)

    s = sub.add_parser("tunnel", help="public tunnels: up|down|list|status")
    s.add_argument("action", choices=["up", "down", "list", "status"])
    s.add_argument("prj", nargs="?", default=None)
    s.add_argument("provider", nargs="?", default=None,
                   help="cloudflared | localtunnel | auto (default: auto)")
    s.set_defaults(fn=cmd_tunnel)

    for verb in ("oracle", "gemini"):   # gemini = v5 muscle-memory alias
        s = sub.add_parser(verb, help="external review desk: review|capture|status (push→receive→act)")
        s.add_argument("op", choices=["review", "capture", "status"])
        s.add_argument("rest", nargs=argparse.REMAINDER,
                       help="args passed through to gemini_review.py (e.g. --file --prj --out --ask)")
        s.set_defaults(fn=cmd_oracle)

    s = sub.add_parser("agents", help="manage agent roster: build|lint|pins")
    s.add_argument("op", choices=["build", "lint", "pins"], nargs="?", default="build")
    s.set_defaults(fn=cmd_agents)

    sub.add_parser("tools").set_defaults(fn=cmd_tools)
    s = sub.add_parser("selftest"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_selftest)
    s = sub.add_parser("doctor"); s.add_argument("--brain", action="store_true"); s.set_defaults(fn=cmd_doctor)

    s = sub.add_parser("plan", help="freeze a task list (JSON, --file or stdin) into PLAN.dag.json")
    s.add_argument("prj"); s.add_argument("--file", default=None)
    s.set_defaults(fn=cmd_plan)

    s = sub.add_parser("run", help="dry driver — render the DAG's next dispatchable nodes")
    s.add_argument("prj"); s.add_argument("--mark", default=None,
                   help="NODE_ID:STATUS — mark a node before rendering ready nodes")
    s.set_defaults(fn=cmd_run)

    s = sub.add_parser("resume", help="machine-checkable resume vs git HEAD (FRESH/DEGRADED/UNKNOWN)")
    s.add_argument("prj"); s.add_argument("ticket", nargs="?", default=None)
    s.set_defaults(fn=cmd_resume)

    s = sub.add_parser("events", help="tail + summarize the fleet telemetry log")
    s.add_argument("-n", type=int, default=100, dest="n")
    s.add_argument("--verbose", action="store_true")
    s.set_defaults(fn=cmd_events)

    s = sub.add_parser("lint", help="lint the agent roster (frontmatter·RCCF·parity·registry·pins)")
    s.add_argument("rest", nargs=argparse.REMAINDER, help="passthrough args (e.g. --pin)")
    s.set_defaults(fn=cmd_lint)

    s = sub.add_parser("recall", help="search the memory db (memdb) for a project")
    s.add_argument("prj"); s.add_argument("--text", required=True, dest="text")
    s.add_argument("--k", type=int, default=8)
    s.set_defaults(fn=cmd_recall)

    s = sub.add_parser("new", help="scaffold a new project: shamel new PRJ-XXXX 'Title' [MEDIUM|HIGH|LOW]")
    s.add_argument("prj"); s.add_argument("title")
    s.add_argument("priority", nargs="?", default="MEDIUM")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("gate-advance", help="advance gate (validate + tag + checkpoint)")
    s.add_argument("prj"); s.add_argument("to_gate", type=int)
    s.set_defaults(fn=cmd_gate_advance)

    s = sub.add_parser("reflect", help="run the dreaming loop: distil lessons from HANDOFFS")
    s.add_argument("prj", nargs="?")
    s.set_defaults(fn=cmd_reflect)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    # normalize 'scratch <prj> clean'
    if getattr(args, "cmd", None) == "scratch" and args.clean == "clean":
        args.clean = True
    try:
        return args.fn(args)
    except guard.GovernanceError as e:
        print(f"✗ GOVERNANCE: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
