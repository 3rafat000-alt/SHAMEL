"""
registry — load the Nexus org index (core/nexus/registry.yaml) once, answer
"who is this agent?" questions everywhere.

v6 replaced the v5 hardcoded ROLE_TIER map with this loader (v5 debt #4 paid):
15 rooms · 105 agents live in ONE machine-readable file, and every consumer —
tickets.validate_room_boundary, guard.assert_net_allowed, gates.GATE_ROLES,
shamel rooms/registry/doctor, the dashboard — reads it from here instead of
carrying its own stale copy.

Fail-open by design: an unreadable or partial registry yields empty maps, and
callers treat unknown agent ids as "cannot identify — do not block". Uses
pyyaml when present, else a small stdlib line parser for the rooms/agents block.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from . import paths


def registry_path() -> Path:
    return paths.nexus_dir() / "registry.yaml"


# ── loading ───────────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _load() -> dict:
    """Return {"rooms": {code: room}, "agents": {id: agent}} — or empty maps.

    room  = {code, dir, name, emoji, gates, lead, agents: [id, ...]}
    agent = {id, room, title, spec, spawnable, model, route, budget, tools}
    """
    empty = {"rooms": {}, "agents": {}}
    p = registry_path()
    if not p.exists():
        return empty
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return empty
    data = None
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
    except Exception:
        data = None
    if isinstance(data, dict):
        rooms_raw = data.get("rooms")
        if isinstance(rooms_raw, list):
            return _from_yaml(data)
        if isinstance(rooms_raw, dict):
            # Convert dict-keyed registry (SHAMEL format) to list-based
            rooms_list = []
            for code, room in rooms_raw.items():
                room["code"] = code
                rooms_list.append(room)
            data["rooms"] = rooms_list
            return _from_yaml(data)
    return _from_lines(text)


def _from_yaml(data: dict) -> dict:
    rooms: dict[str, dict] = {}
    agents: dict[str, dict] = {}
    for room in data.get("rooms") or []:
        code = str(room.get("code", "")).strip()
        if not code:
            continue
        ids: list[str] = []
        for a in room.get("agents") or []:
            if isinstance(a, str):
                aid = a.strip()
            else:
                aid = str(a.get("id", "")).strip()
            if not aid:
                continue
            ids.append(aid)
            if isinstance(a, str):
                agents[aid] = {"id": aid, "room": code}
            else:
                agents[aid] = {
                    "id": aid, "room": code,
                    "title": str(a.get("title", "")),
                    "spec": str(a.get("spec", "")),
                    "spawnable": str(a.get("spawnable", "")),
                    "model": str(a.get("model", "")),
                    "route": str(a.get("route", "")),
                    "budget": str(a.get("budget", "")),
                    "tools": a.get("tools", []),
                }
        rooms[code] = {
            "code": code,
            "dir": str(room.get("dir", "")),
            "name": str(room.get("name", "")),
            "emoji": str(room.get("emoji", "")),
            "gates": str(room.get("gates", "")),
            "lead": str(room.get("lead", "")),
            "agents": ids,
        }
    return {"rooms": rooms, "agents": agents}


_ROOM_KEY = re.compile(r"^\s{2,4}-\s*code:\s*(\S+)")
_AGENT_KEY = re.compile(r"^\s+-\s*id:\s*(\S+)")
_FIELD = re.compile(r"^\s+([a-z_]+):\s*(.+?)\s*$")


def _from_lines(text: str) -> dict:
    """Stdlib fallback: walk the rooms block line by line. Good enough for the
    fields the library needs (code/dir/name/lead + agent id/spec/tools)."""
    rooms: dict[str, dict] = {}
    agents: dict[str, dict] = {}
    room: dict | None = None
    agent: dict | None = None
    in_rooms = False
    for line in text.splitlines():
        if line.startswith("rooms:"):
            in_rooms = True
            continue
        if in_rooms and line and not line[0].isspace() and not line.lstrip().startswith("#"):
            break  # left the rooms: block (skills:/tools:/superpowers:)
        if not in_rooms:
            continue
        m = _ROOM_KEY.match(line)
        if m:
            room = {"code": m.group(1), "dir": "", "name": "", "emoji": "",
                    "gates": "", "lead": "", "agents": []}
            rooms[room["code"]] = room
            agent = None
            continue
        m = _AGENT_KEY.match(line)
        if m and room is not None:
            agent = {"id": m.group(1), "room": room["code"], "title": "",
                     "spec": "", "spawnable": "", "model": "", "route": "",
                     "budget": "", "tools": []}
            room["agents"].append(agent["id"])
            agents[agent["id"]] = agent
            continue
        m = _FIELD.match(line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip().strip('"')
        if agent is not None and key in agent:
            if key == "tools":
                agent[key] = ([t.strip() for t in val.strip("[]").split(",") if t.strip()]
                              if val.startswith("[") else val)
            else:
                agent[key] = val
        elif room is not None and key in room and key != "agents":
            room[key] = val
    return {"rooms": rooms, "agents": agents}


def reload() -> None:
    """Drop the cache (tests / long-lived servers after a registry edit)."""
    _load.cache_clear()


# ── queries (all fail-open: unknown id → falsy, never an exception) ──────────
def rooms() -> dict[str, dict]:
    return _load()["rooms"]


def agents() -> dict[str, dict]:
    return _load()["agents"]


def agent(slug: str) -> dict:
    return agents().get(slug, {})


def role_room(slug: str) -> str:
    """Agent id → room code ('' when unknown — caller must not block on '')."""
    return agent(slug).get("room", "")


def room_lead(code: str) -> str:
    return rooms().get(code, {}).get("lead", "")


def is_lead(slug: str) -> bool:
    """True when this agent is a Room Lead (its room's sole gateway)."""
    r = role_room(slug)
    return bool(r) and rooms().get(r, {}).get("lead", "") == slug


def spec_path(slug: str) -> str:
    """Repo-relative spec file (core/rooms/<NN-room>/agents/<id>.md)."""
    a = agent(slug)
    if a.get("spec"):
        return a["spec"]
    r = rooms().get(a.get("room", ""), {})
    if r.get("dir"):
        return f"core/rooms/{r['dir']}/agents/{slug}.md"
    return ""


def net_allowed_roles() -> frozenset[str]:
    """Agents allowed to reach the internet: those whose registry tools grant
    WebSearch/WebFetch, plus full-inherit agents (boardroom + room Leads inherit
    the session toolset). Empty registry → empty set (guard then fails open only
    for the explicit fallback list it keeps)."""
    out: set[str] = set()
    for aid, a in agents().items():
        tools = a.get("tools")
        if tools == "inherit":
            out.add(aid)
        elif isinstance(tools, (list, tuple)) and any(
                t in ("WebSearch", "WebFetch") for t in tools):
            out.add(aid)
    return frozenset(out)
