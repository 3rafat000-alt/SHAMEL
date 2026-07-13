"""
routing — resolve the cheapest clearing route for an agent from the Nexus grid.

Three dials: model · effort · caveman. This reads core/nexus/routing.yaml —
the SINGLE source of routing truth (v5 debt #1 paid: the module-level ladder
below mirrors the yaml `models:` block and includes the gatekeeper tier, so a
CRITICAL bump can actually reach it) — and applies the priority override
(CRITICAL bumps one step up the ladder, clamped; LOW is capped at workhorse).
Uses pyyaml when present, else a small stdlib fallback for the `routes:` block.
"""
from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from . import paths

EFFORT = ["low", "medium", "high", "max"]
# The ladder, cheapest → dearest: 🟢 → 🔵 → 🔮 → 🟣 (nexus/routing.yaml `models:`).
MODEL_ORDER = ["mechanical", "workhorse", "gatekeeper", "deep"]
MODEL_IDS = {
    "mechanical": "claude-haiku-4-5",
    "workhorse": "claude-sonnet-5",
    "gatekeeper": "claude-fable-5",
    "deep": "claude-opus-4-8",
}
MODEL_TIER = {"mechanical": "🟢", "workhorse": "🔵", "gatekeeper": "🔮", "deep": "🟣"}


def _routing_path() -> Path:
    return paths.nexus_dir() / "routing.yaml"


@lru_cache(maxsize=1)
def _load() -> dict:
    text = _routing_path().read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        if isinstance(data, dict) and "routes" in data:
            return data
    except Exception:
        pass
    return {"routes": _fallback_routes(text), "defaults": _fallback_defaults(text)}


def _fallback_defaults(text: str) -> dict:
    out = {"model": "workhorse", "effort": "medium", "caveman": "full"}
    blk = re.search(r"^defaults:\s*$(.*?)^\S", text, re.M | re.S)
    if blk:
        for k in out:
            m = re.search(rf"^\s+{k}:\s*(\S+)", blk.group(1), re.M)
            if m:
                out[k] = m.group(1)
    return out


def _fallback_routes(text: str) -> dict:
    """Parse `role: { model: .., effort: .., caveman: .., gate: .. }` lines."""
    routes: dict[str, dict] = {}
    inner = re.compile(r"(\w[\w-]*?):\s*\{([^}]*)\}")
    for line in text.splitlines():
        m = inner.match(line.strip())
        if not m:
            continue
        role, body = m.group(1), m.group(2)
        d = {}
        for kv in body.split(","):
            if ":" in kv:
                k, v = kv.split(":", 1)
                d[k.strip()] = v.strip().strip('"')
        if {"model", "effort"} & set(d):
            routes[role] = d
    return routes


def route_for(role: str, priority: str | None = None) -> dict:
    """Return a resolved route dict for a role, applying priority override."""
    data = _load()
    routes = data.get("routes", {})
    if role not in routes:
        raise KeyError(f"no route for role '{role}' in routing.yaml")
    r = dict(routes[role])
    model = r.get("model", "workhorse")
    effort = r.get("effort", "medium")
    caveman = r.get("caveman", "full")

    pr = (priority or "").upper()
    if pr == "CRITICAL":
        # +1 step along the ladder, clamped at the top — so a workhorse route under
        # CRITICAL lands on gatekeeper, and only an already-gatekeeper route reaches
        # deep (nexus/routing.yaml escalation.priority_override).
        model = MODEL_ORDER[min(MODEL_ORDER.index(model) + 1, len(MODEL_ORDER) - 1)] \
            if model in MODEL_ORDER else model
        effort = EFFORT[min(EFFORT.index(effort) + 1, len(EFFORT) - 1)] \
            if effort in EFFORT else effort
    elif pr == "LOW":
        if model in MODEL_ORDER and MODEL_ORDER.index(model) > MODEL_ORDER.index("workhorse"):
            model = "workhorse"
        if effort in EFFORT and EFFORT.index(effort) > EFFORT.index("medium"):
            effort = "medium"

    # Model id: the yaml `models:` block wins (single source); the module map is
    # only the offline fallback for a stdlib-parsed file.
    models = data.get("models") or {}
    yaml_id = (models.get(model) or {}).get("id") if isinstance(models, dict) else None

    return {
        "role": role,
        "model": model,
        "model_id": yaml_id or MODEL_IDS.get(model, model),
        "tier": MODEL_TIER.get(model, ""),
        "effort": effort,
        "caveman": caveman,
        "gate": r.get("gate", ""),
        "budget": r.get("budget", ""),
        "priority": pr or "—",
    }


def format_route(role: str, priority: str | None = None) -> str:
    r = route_for(role, priority)
    return f"{r['model']} · {r['effort']} · {r['caveman']}"


def all_roles() -> list[str]:
    return sorted(_load().get("routes", {}).keys())
