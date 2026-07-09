"""
role: knw-lead + ops-cicd-engineer
purpose: config lint in CI (EVOLUTION.md Round 2 #9) — static lint over the agent
         roster itself (frontmatter shape, RCCF body sections), a 105==105==105
         three-way parity check (`.claude/agents/` spawnables vs
         `core/rooms/*/agents/` specs vs `core/nexus/registry.yaml` agent
         entries), registry↔filesystem consistency (every registry id resolves
         both files; every registry spec/skill path exists on disk), and a
         SHA-256 content-pin manifest so a silent post-freeze edit to an agent
         or skill file shows up as drift instead of going unnoticed.
gate: cross (CI — runs on every push/pull_request via .github/workflows/lint-agents.yml)
inputs: root (workspace root, defaults to paths.repo_root()); write flag for
        content_pins (False = report drift only, True = (re)write the manifest).
        No wall-clock/randomness — SHA-256 is a pure function of file bytes.
outputs: core/nexus/agent-pins.json (SHA-256 manifest, written only when a
         caller passes write=True — content_pins never mutates on a plain check).
exit: main(argv) returns 0 when every check passes, 1 when any check fails;
      __main__ demo prints PASS/FAIL per check and exits accordingly.

Untested agent configs is one of the named anti-patterns in EVOLUTION.md Round 2
("audit the org against these each gate-close") — this module is the mechanical
answer: a broken agent frontmatter, a roster miscount, a dangling registry path,
or an unpinned drift now fails a build instead of surfacing three sessions later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from . import paths

_ALLOWED_MODELS = {"haiku", "sonnet", "opus", "inherit"}
_RCCF_SECTIONS = ("Role", "Context", "Command", "Format")
_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
_TOP_FIELD = re.compile(r"^([a-zA-Z_]+):\s*(.*)$")
_TRIGGER_HINTS = ("use when", "triggers", "trigger:")


def _root(root: str | Path | None) -> Path:
    return Path(root).resolve() if root else paths.repo_root()


def _agents_dir(root: Path) -> Path:
    return root / ".claude" / "agents"


def _rooms_dir(root: Path) -> Path:
    return root / "company" / "rooms"


def _registry_path(root: Path) -> Path:
    return root / "company" / "nexus" / "registry.yaml"


def _pins_path(root: Path) -> Path:
    return root / "company" / "nexus" / "agent-pins.json"


# ── frontmatter parsing (stdlib-only; top-level scalar keys, matches the rest
#    of shamel_tools' yaml-or-regex-fallback pattern — see routing.py `_load`) ──
def _parse_frontmatter(text: str) -> dict[str, str] | None:
    m = _FRONTMATTER.match(text)
    if not m:
        return None
    out: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        if not line or line[0] in " \t":
            continue  # nested block (tools:) — not needed for the fields we lint
        fm = _TOP_FIELD.match(line)
        if fm:
            key, val = fm.group(1), fm.group(2).strip()
            out[key] = val
    return out


def _body_after_frontmatter(text: str) -> str:
    m = _FRONTMATTER.match(text)
    return text[m.end():] if m else text


# ── lint_agents — per-file frontmatter + RCCF body shape ─────────────────────
def lint_agents(root: str | Path | None = None) -> dict:
    """Validate every .claude/agents/*.md: frontmatter (name/description/model)
    + all four RCCF body sections present. Returns {ok, errors, warnings, checked}."""
    r = _root(root)
    agents_dir = _agents_dir(r)
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    files = sorted(agents_dir.glob("*.md")) if agents_dir.is_dir() else []
    if not files:
        return {"ok": False, "errors": [f"no agent files found under {agents_dir}"],
                 "warnings": [], "checked": 0}

    for f in files:
        checked += 1
        stem = f.stem
        try:
            text = f.read_text(encoding="utf-8")
        except OSError as e:
            errors.append(f"{f.name}: unreadable ({e})")
            continue

        fm = _parse_frontmatter(text)
        if fm is None:
            errors.append(f"{f.name}: no frontmatter block (--- ... ---)")
            continue

        name = fm.get("name", "")
        if not name:
            errors.append(f"{f.name}: frontmatter missing 'name'")
        elif name != stem:
            errors.append(f"{f.name}: name '{name}' != filename stem '{stem}'")

        desc = fm.get("description", "")
        if not desc.strip():
            errors.append(f"{f.name}: frontmatter 'description' is empty")
        elif not any(h in desc.lower() for h in _TRIGGER_HINTS):
            warnings.append(f"{f.name}: description has no obvious trigger phrase "
                             "('Use when ...')")

        model = fm.get("model", "")
        if model not in _ALLOWED_MODELS:
            errors.append(f"{f.name}: model '{model}' not in {sorted(_ALLOWED_MODELS)}")

        body = _body_after_frontmatter(text)
        missing = [s for s in _RCCF_SECTIONS if s not in body]
        if missing:
            errors.append(f"{f.name}: body missing RCCF section(s) {missing}")

    return {"ok": not errors, "errors": errors, "warnings": warnings, "checked": checked}


# ── registry loading (stdlib-only; mirrors shamel_tools.registry's own
#    yaml-or-regex-fallback so this module never needs pyyaml) ───────────────
def _load_registry(root: Path) -> dict:
    """Return {"agents": {id: {spec, spawnable}}, "skills": {name: path}} — or
    empty maps on a missing/unreadable registry (fail-open, matches registry.py)."""
    p = _registry_path(root)
    empty = {"agents": {}, "skills": {}}
    if not p.exists():
        return empty
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return empty
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        if isinstance(data, dict) and isinstance(data.get("rooms"), list):
            return _registry_from_yaml(data)
    except Exception:
        pass
    return _registry_from_lines(text)


def _registry_from_yaml(data: dict) -> dict:
    agents: dict[str, dict] = {}
    for room in data.get("rooms") or []:
        for a in room.get("agents") or []:
            aid = str(a.get("id", "")).strip()
            if aid:
                agents[aid] = {"spec": str(a.get("spec", "")),
                                "spawnable": str(a.get("spawnable", ""))}
    skills: dict[str, str] = {}
    for s in data.get("skills") or []:
        sname = str(s.get("name", "")).strip()
        if sname:
            skills[sname] = str(s.get("path", ""))
    return {"agents": agents, "skills": skills}


_AGENT_ID = re.compile(r"^\s+-\s*id:\s*(\S+)")
_SPEC_FIELD = re.compile(r"^\s+spec:\s*(\S+)")
_SPAWN_FIELD = re.compile(r"^\s+spawnable:\s*(\S+)")
_SKILL_NAME = re.compile(r"^\s{2,4}-\s*name:\s*(\S+)")
_SKILL_PATH = re.compile(r"^\s+path:\s*(\S+)")


def _registry_from_lines(text: str) -> dict:
    """Stdlib fallback line-walker (same shape as registry.py `_from_lines`)."""
    agents: dict[str, dict] = {}
    skills: dict[str, str] = {}
    section = None  # "rooms" | "skills" | None
    cur_agent: str | None = None
    cur_skill: str | None = None
    for line in text.splitlines():
        if line.startswith("rooms:"):
            section = "rooms"
            continue
        if line.startswith("skills:"):
            section = "skills"
            continue
        if line and not line[0].isspace() and not line.lstrip().startswith("#") \
                and not line.startswith(("rooms:", "skills:")):
            section = None
            continue

        if section == "rooms":
            m = _AGENT_ID.match(line)
            if m:
                cur_agent = m.group(1)
                agents[cur_agent] = {"spec": "", "spawnable": ""}
                continue
            if cur_agent:
                m = _SPEC_FIELD.match(line)
                if m:
                    agents[cur_agent]["spec"] = m.group(1)
                    continue
                m = _SPAWN_FIELD.match(line)
                if m:
                    agents[cur_agent]["spawnable"] = m.group(1)
                    continue
        elif section == "skills":
            m = _SKILL_NAME.match(line)
            if m:
                cur_skill = m.group(1)
                skills[cur_skill] = ""
                continue
            if cur_skill:
                m = _SKILL_PATH.match(line)
                if m:
                    skills[cur_skill] = m.group(1)
                    continue
    return {"agents": agents, "skills": skills}


# ── parity_check — 105 == 105 == 105 ──────────────────────────────────────────
def parity_check(root: str | Path | None = None) -> dict:
    """Count .claude/agents/*.md == count core/rooms/*/agents/*.md ==
    registry agent count. Returns {ok, claude_agents, room_agents, registry_agents}."""
    r = _root(root)
    claude_agents = len(list(_agents_dir(r).glob("*.md"))) if _agents_dir(r).is_dir() else 0
    room_agents = len(list(_rooms_dir(r).glob("*/agents/*.md"))) if _rooms_dir(r).is_dir() else 0
    registry_agents = len(_load_registry(r)["agents"])
    ok = claude_agents == room_agents == registry_agents and claude_agents > 0
    return {"ok": ok, "claude_agents": claude_agents, "room_agents": room_agents,
            "registry_agents": registry_agents}


# ── registry_consistency — every registry path actually resolves ────────────
def registry_consistency(root: str | Path | None = None) -> dict:
    """Every registry agent id has both a spec file and a spawnable file on
    disk; every registry skill path resolves. Returns {ok, errors, checked}."""
    r = _root(root)
    reg = _load_registry(r)
    errors: list[str] = []
    checked = 0

    for aid, entry in sorted(reg["agents"].items()):
        checked += 1
        spec, spawnable = entry.get("spec", ""), entry.get("spawnable", "")
        if not spec:
            errors.append(f"{aid}: registry entry has no 'spec' path")
        elif not (r / spec).is_file():
            errors.append(f"{aid}: spec path does not resolve — {spec}")
        if not spawnable:
            errors.append(f"{aid}: registry entry has no 'spawnable' path")
        elif not (r / spawnable).is_file():
            errors.append(f"{aid}: spawnable path does not resolve — {spawnable}")
        expected_spawnable = f".claude/agents/{aid}.md"
        if spawnable and spawnable != expected_spawnable:
            errors.append(f"{aid}: spawnable '{spawnable}' != expected '{expected_spawnable}'")

    for sname, spath in sorted(reg["skills"].items()):
        checked += 1
        if not spath:
            errors.append(f"skill '{sname}': registry entry has no 'path'")
        elif not (r / spath).is_file():
            errors.append(f"skill '{sname}': path does not resolve — {spath}")

    if not reg["agents"]:
        errors.append(f"registry has zero agents — check {_registry_path(r)}")

    return {"ok": not errors, "errors": errors, "checked": checked}


# ── content_pins — SHA-256 drift detection ───────────────────────────────────
def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_pins(root: str | Path | None = None, write: bool = False) -> dict:
    """SHA-256 of every .claude/agents/*.md against the pinned manifest.

    write=False (default): report drift against the existing manifest. No
    manifest on disk yet is NOT a failure (bootstrap case) — call once with
    write=True to establish the baseline.
    write=True: (re)write the manifest to the current hashes.

    Returns {ok, written, added, removed, drifted, checked, path}.
    """
    r = _root(root)
    agents_dir = _agents_dir(r)
    pins_path = _pins_path(r)
    current = {f.name: _sha256(f) for f in sorted(agents_dir.glob("*.md"))} \
        if agents_dir.is_dir() else {}

    if write:
        pins_path.parent.mkdir(parents=True, exist_ok=True)
        pins_path.write_text(
            json.dumps({"agents": current}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return {"ok": True, "written": True, "added": [], "removed": [], "drifted": [],
                "checked": len(current), "path": str(pins_path)}

    if not pins_path.exists():
        return {"ok": True, "written": False, "added": [], "removed": [], "drifted": [],
                "checked": len(current), "path": str(pins_path),
                "note": "no manifest yet — run content_pins(write=True) to baseline"}

    try:
        manifest = json.loads(pins_path.read_text(encoding="utf-8")).get("agents", {})
    except (OSError, json.JSONDecodeError) as e:
        return {"ok": False, "written": False, "added": [], "removed": [], "drifted": [],
                "checked": len(current), "path": str(pins_path),
                "note": f"manifest unreadable: {e}"}

    added = sorted(set(current) - set(manifest))
    removed = sorted(set(manifest) - set(current))
    drifted = sorted(name for name in (set(current) & set(manifest))
                      if current[name] != manifest[name])
    ok = not added and not removed and not drifted
    return {"ok": ok, "written": False, "added": added, "removed": removed,
            "drifted": drifted, "checked": len(current), "path": str(pins_path)}


# ── main — CI entry point ─────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="agentlint", description=__doc__)
    ap.add_argument("--root", default=None, help="workspace root (default: auto-detect)")
    ap.add_argument("--pin", action="store_true",
                     help="(re)write the content-pin manifest instead of checking drift")
    args = ap.parse_args(argv or [])

    root = args.root

    if args.pin:
        result = content_pins(root, write=True)
        print(f"agentlint --pin: wrote {result['checked']} hashes -> {result['path']}")
        return 0

    checks = {
        "lint_agents": lint_agents(root),
        "parity_check": parity_check(root),
        "registry_consistency": registry_consistency(root),
        "content_pins": content_pins(root, write=False),
    }

    ok = True
    for name, result in checks.items():
        status = "PASS" if result["ok"] else "FAIL"
        if not result["ok"]:
            ok = False
        print(f"[{status}] {name}: {_summarize(name, result)}")
        for err in result.get("errors", []):
            print(f"    ERROR: {err}")
        for warn in result.get("warnings", []):
            print(f"    warn:  {warn}")
        for field in ("added", "removed", "drifted"):
            for item in result.get(field, []):
                print(f"    {field}: {item}")

    return 0 if ok else 1


def _summarize(name: str, result: dict) -> str:
    if name == "lint_agents":
        return f"{result['checked']} agent file(s) checked"
    if name == "parity_check":
        return (f"claude={result['claude_agents']} rooms={result['room_agents']} "
                f"registry={result['registry_agents']}")
    if name == "registry_consistency":
        return f"{result['checked']} registry path(s) checked"
    if name == "content_pins":
        return result.get("note") or f"{result['checked']} file(s) pinned"
    return ""


if __name__ == "__main__":
    print("=== agentlint self-test (real repo tree) ===")
    _root_path = paths.repo_root()

    lint = lint_agents(_root_path)
    print(f"lint_agents:            ok={lint['ok']} checked={lint['checked']} "
          f"errors={len(lint['errors'])} warnings={len(lint['warnings'])}")
    for e in lint["errors"]:
        print(f"  ERROR {e}")

    parity = parity_check(_root_path)
    print(f"parity_check:           ok={parity['ok']} claude={parity['claude_agents']} "
          f"rooms={parity['room_agents']} registry={parity['registry_agents']}")

    consistency = registry_consistency(_root_path)
    print(f"registry_consistency:   ok={consistency['ok']} checked={consistency['checked']} "
          f"errors={len(consistency['errors'])}")
    for e in consistency["errors"]:
        print(f"  ERROR {e}")

    # Bootstrap the pin manifest if this is the first run, then confirm a
    # freshly-baselined manifest reports zero drift.
    pins_report = content_pins(_root_path, write=False)
    if pins_report.get("note", "").startswith("no manifest"):
        pinned = content_pins(_root_path, write=True)
        print(f"content_pins (baseline): written={pinned['written']} "
              f"checked={pinned['checked']} -> {pinned['path']}")
        pins_report = content_pins(_root_path, write=False)
    print(f"content_pins:           ok={pins_report['ok']} checked={pins_report['checked']} "
          f"added={len(pins_report['added'])} removed={len(pins_report['removed'])} "
          f"drifted={len(pins_report['drifted'])}")

    all_ok = lint["ok"] and parity["ok"] and consistency["ok"] and pins_report["ok"]
    exit_code = main([])
    assert exit_code == (0 if all_ok else 1), "main() exit code disagrees with checks"

    print("PASS" if all_ok else "FAIL")
    sys.exit(0 if all_ok else 1)
