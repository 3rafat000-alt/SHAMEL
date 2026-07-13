"""
role: knw-reflector
purpose: LESSONS as a MANAGED CACHE, not an append-only log (EVOLUTION.md Round 2
    #5). Every lesson block carries cache frontmatter — confidence, uses,
    successes, last_seen_week — on top of the usual sig/mem/situation/
    what_failed/rule/source fields (tickets.py lesson-block convention). A
    confidence score decays 5%/week when a lesson goes unused and is bumped by
    evidence (record_use); only lessons that still clear a confidence bar get
    injected into a Work Order brief (select_for_injection), capped so a brief
    never drowns in doctrine; lessons that recur across enough projects surface
    as promotion candidates to the org-level LESSONS.md; vaccine_for matches an
    incoming task's topic against known failure patterns before work starts.
gate: cross (reflection writes at gate-close; injection/vaccine reads happen at
    any gate's RCCF brief construction — nexus/registry.yaml knw-reflector)
inputs: prj id, a now_week integer supplied by the caller (GOVERNANCE Rule 9 —
    no wall clock in here), lesson fields, an occurrence_by_sig map built by the
    caller from scanning multiple projects' LESSONS.md files.
outputs: projects/<PRJ>/_context/LESSONS.md (managed cache blocks, rewritten in
    canonical bullet form on every mutating call). brain/org/LESSONS.md
    is READ ONLY here (vaccine_for merges org + project matches) — the actual
    org-level write is a separate, deliberate CEO/reflector action, not this
    module's job (promote_candidates only IDENTIFIES qualifying sigs).
exit: functions raise guard.GovernanceError on a scope violation, KeyError when
    record_use targets an unknown sig, ValueError on malformed input; __main__
    demo prints PASS and exits 0.

Parses two on-disk lesson-block dialects so it works over both the v5 plain
`key: value` blocks (tickets.py append_lesson) and the v6 bulleted
`- **key:** value` blocks already live in brain/org/LESSONS.md and
brain/templates/LESSONS.md. Any block this module WRITES is re-rendered
in the canonical bulleted form — round-tripping a file through add_lesson/
record_use normalizes it, which is a feature of a managed cache, not a bug.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import paths, guard

_HEAD = re.compile(r"^##\s*(LES-\d+)(?:\s*\(([^)]*)\))?\s*$")
_BULLET_FIELD = re.compile(r"^-\s*\*\*([a-zA-Z_]+):\*\*\s*(.*)$")
_PLAIN_FIELD = re.compile(r"^([a-zA-Z_]+):\s*(.*)$")

# Canonical render order — cache fields up front (what a machine reads first),
# procedural fields after (what a human reads).
_FIELD_ORDER = (
    "sig", "mem", "confidence", "uses", "successes", "last_seen_week",
    "date", "situation", "what_failed", "rule", "source",
)

_DEFAULT_NEW_CONFIDENCE = 0.8
_DECAY_RATE = 0.05
_STOPWORDS = frozenset({
    "the", "and", "for", "with", "that", "this", "from", "into", "onto",
    "your", "have", "will", "would", "should", "could", "must", "been",
    "were", "was", "not", "but", "when", "while", "then", "than", "also",
    "each", "only", "over", "across", "before", "after", "about", "some",
})


# ── paths ─────────────────────────────────────────────────────────────────────
def _org_lessons_path() -> Path:
    """brain/org/LESSONS.md — org-level procedural memory. Read only."""
    return paths.repo_root() / "company" / "brain" / "org" / "LESSONS.md"


def _project_lessons_path(prj: str) -> Path:
    return paths.brain_file(prj, "LESSONS")


# ── block parse/render ───────────────────────────────────────────────────────
def _parse_blocks(text: str) -> list[dict]:
    blocks: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        h = _HEAD.match(line.strip())
        if h:
            cur = {"id": h.group(1), "fields": {}}
            if h.group(2):
                cur["fields"]["date"] = h.group(2).strip()
            blocks.append(cur)
            continue
        if cur is None:
            continue
        s = line.strip()
        m = _BULLET_FIELD.match(s) or _PLAIN_FIELD.match(s)
        if m:
            cur["fields"][m.group(1).strip().lower()] = m.group(2).strip()
    return blocks


def _load_file(path: Path) -> tuple[str, list[dict]]:
    """Returns (preamble_text, blocks). preamble is everything before the first
    '## LES-NNN' header (frontmatter + title + doc comment) — preserved verbatim
    on rewrite."""
    if not path.exists():
        return "", []
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = next((i for i, l in enumerate(lines) if _HEAD.match(l.strip())), len(lines))
    preamble = "\n".join(lines[:idx])
    blocks = _parse_blocks("\n".join(lines[idx:]))
    return preamble, blocks


def _read_blocks(path: Path) -> list[dict]:
    return _load_file(path)[1]


def _render_block(les_id: str, fields: dict) -> str:
    lines = [f"\n## {les_id}"]
    seen = set()
    for key in _FIELD_ORDER:
        val = fields.get(key, "")
        if val not in ("", None):
            lines.append(f"- **{key}:** {val}")
            seen.add(key)
    for key, val in fields.items():  # forward-compat: unknown fields survive
        if key not in seen and val not in ("", None):
            lines.append(f"- **{key}:** {val}")
    return "\n".join(lines) + "\n"


def _default_preamble(prj: str) -> str:
    return (
        "---\ntype: brain\nmem: procedural\nprj: " + prj + "\n---\n"
        f"# LESSONS — {prj} · managed cache\n"
    )


def _rewrite_file(path: Path, blocks: list[dict], preamble: str) -> None:
    body = preamble.rstrip("\n")
    for b in blocks:
        body += _render_block(b["id"], b["fields"])
    if not body.endswith("\n"):
        body += "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def _next_id(blocks: list[dict]) -> str:
    nums = [int(b["id"].split("-")[1]) for b in blocks if b["id"].split("-")[1].isdigit()]
    return f"LES-{(max(nums) + 1) if nums else 1:03d}"


# ── writers ───────────────────────────────────────────────────────────────────
def add_lesson(prj: str, *, situation: str, what_failed: str, rule: str, sig: str,
                mem: str = "procedural", source: str = "", date: str = "",
                confidence: float = _DEFAULT_NEW_CONFIDENCE, uses: int = 0,
                successes: int = 0, last_seen_week: int = 0) -> str:
    """Append one lesson to a project's managed LESSONS.md cache. Extends
    tickets.py's append_lesson (sig + one grounded rule) with the cache fields
    a v5 writer never carried. Returns the new lesson id (LES-NNN)."""
    f = _project_lessons_path(prj)
    guard.assert_within_project(f, prj)
    preamble, blocks = _load_file(f)
    les_id = _next_id(blocks)
    fields = {
        "sig": sig,
        "mem": mem,
        "confidence": f"{max(0.0, min(1.0, confidence)):.2f}",
        "uses": str(max(0, int(uses))),
        "successes": str(max(0, int(successes))),
        "last_seen_week": str(int(last_seen_week)),
        "situation": situation,
        "what_failed": what_failed,
        "rule": rule,
    }
    if date:
        fields["date"] = date
    if source:
        fields["source"] = source
    blocks.append({"id": les_id, "fields": fields})
    _rewrite_file(f, blocks, preamble or _default_preamble(prj))
    return les_id


def record_use(prj: str, sig: str, success: bool, now_week: int) -> None:
    """A lesson fired (auto-injected or vaccine-matched) and was actually used —
    bump uses/successes, recompute confidence from the fresh counts
    (score_confidence), and reset last_seen_week so its decay clock restarts.
    Raises KeyError if no lesson in this project carries `sig`."""
    f = _project_lessons_path(prj)
    guard.assert_within_project(f, prj)
    preamble, blocks = _load_file(f)
    target = next((b for b in blocks if b["fields"].get("sig", "").lower() == sig.lower()), None)
    if target is None:
        raise KeyError(f"no lesson with sig '{sig}' in {f}")
    ff = target["fields"]
    uses = int(ff.get("uses", "0") or 0) + 1
    successes = int(ff.get("successes", "0") or 0) + (1 if success else 0)
    ff["uses"] = str(uses)
    ff["successes"] = str(successes)
    ff["confidence"] = f"{score_confidence(uses, successes):.2f}"
    ff["last_seen_week"] = str(int(now_week))
    _rewrite_file(f, blocks, preamble)


# ── confidence math ───────────────────────────────────────────────────────────
def score_confidence(uses: int, successes: int) -> float:
    """Laplace-smoothed success rate (Beta(1,1) prior) — deterministic, bounded
    (0, 1). uses=0 -> 0.5 (no evidence either way; neither trusted nor doubted).
    Pure evidence bumps it up; pure failure walks it down; only ever moved by
    record_use, never by the passage of time (that's apply_decay's job)."""
    uses = max(0, int(uses))
    successes = max(0, min(int(successes), uses))
    return (successes + 1) / (uses + 2)


def apply_decay(conf: float, weeks_elapsed: int, rate: float = _DECAY_RATE) -> float:
    """5%/week multiplicative decay (default rate) toward zero for a lesson that
    hasn't been reinforced. weeks_elapsed<=0 is a no-op. Bounded to [0, 1]."""
    weeks_elapsed = max(0, int(weeks_elapsed))
    decayed = float(conf) * ((1.0 - rate) ** weeks_elapsed)
    return max(0.0, min(1.0, decayed))


def _effective_confidence(fields: dict, now_week: int) -> tuple[float, int]:
    """The confidence a lesson block would score RIGHT NOW: its stored
    (evidence-based) confidence, decayed by the weeks since it was last seen.
    Missing `confidence` falls back to score_confidence(uses, successes);
    missing `last_seen_week` is treated as "seen this week" (no decay applied
    to a lesson we have no history for — never punish silence we can't measure).
    """
    raw = fields.get("confidence", "")
    try:
        base = float(raw)
    except ValueError:
        base = score_confidence(int(fields.get("uses", 0) or 0), int(fields.get("successes", 0) or 0))
    raw_week = fields.get("last_seen_week", "")
    try:
        last_seen = int(raw_week) if raw_week != "" else now_week
    except ValueError:
        last_seen = now_week
    weeks_elapsed = max(0, int(now_week) - last_seen)
    return apply_decay(base, weeks_elapsed), weeks_elapsed


# ── injection selection ───────────────────────────────────────────────────────
def select_for_injection(prj: str, now_week: int, cap: int = 6, min_conf: float = 0.7) -> list[dict]:
    """Top lessons above `min_conf` (after decay), capped at `cap`, sorted by
    decayed confidence descending — this is what gets woven into a Work Order
    brief. Never dumps the whole log; the cache earns its place every call."""
    blocks = _read_blocks(_project_lessons_path(prj))
    scored: list[dict] = []
    for b in blocks:
        f = b["fields"]
        sig = f.get("sig", "")
        if not sig:
            continue
        conf, weeks = _effective_confidence(f, now_week)
        if conf < min_conf:
            continue
        scored.append({
            "id": b["id"], "sig": sig, "rule": f.get("rule", ""),
            "mem": f.get("mem", "procedural"), "source": f.get("source", ""),
            "confidence": round(conf, 4), "weeks_since_seen": weeks,
        })
    scored.sort(key=lambda r: (-r["confidence"], r["id"]))
    return scored[:max(0, int(cap))]


# ── promotion (project cache -> org-level candidate list) ────────────────────
def promote_candidates(occurrence_by_sig: dict[str, list[str]], threshold: int = 5,
                        min_projects: int = 2) -> list[dict]:
    """Which sigs qualify to promote to brain/org/LESSONS.md.
    `occurrence_by_sig` maps sig -> list of project ids it was seen in, one
    entry per occurrence (a project may repeat). Qualifies when total
    occurrences >= threshold AND it spans >= min_projects distinct projects.
    Returns candidate dicts (best-effort enriched with rule/situation/mem
    pulled from the first project whose LESSONS.md still has that sig) sorted
    by occurrence count descending. This only IDENTIFIES candidates — writing
    to the org-level file is a deliberate separate act, never automatic."""
    out: list[dict] = []
    for sig, hits in occurrence_by_sig.items():
        occurrences = len(hits)
        projects = sorted(set(hits))
        if occurrences < threshold or len(projects) < min_projects:
            continue
        rule = situation = ""
        mem = "procedural"
        for prj in projects:
            if not paths.project_exists(prj):
                continue
            block = next(
                (b for b in _read_blocks(_project_lessons_path(prj))
                 if b["fields"].get("sig", "").lower() == sig.lower()),
                None,
            )
            if block:
                rule = block["fields"].get("rule", rule)
                situation = block["fields"].get("situation", situation)
                mem = block["fields"].get("mem", mem)
                break
        out.append({
            "sig": sig, "occurrences": occurrences, "projects": projects,
            "rule": rule, "situation": situation, "mem": mem,
        })
    out.sort(key=lambda r: (-r["occurrences"], r["sig"]))
    return out


# ── vaccine: topical match against an incoming task ──────────────────────────
def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z_-]{2,}", (text or "").lower())
    return {w for w in words if len(w) >= 4 and w not in _STOPWORDS}


def vaccine_for(prj: str, task_text: str, cap: int = 3) -> list[dict]:
    """Lessons (project + org scope) whose sig/rule/situation topically overlaps
    an incoming task's keywords — the auto-injection a Work Order's brief gets
    BEFORE work starts, so the same failure pattern doesn't repeat blind.
    Project-scope hits win over an org-scope duplicate of the same sig."""
    task_kw = _keywords(task_text)
    if not task_kw:
        return []
    scored: list[dict] = []
    for scope, path in (("project", _project_lessons_path(prj)), ("org", _org_lessons_path())):
        for b in _read_blocks(path):
            f = b["fields"]
            sig = f.get("sig", "")
            if not sig:
                continue
            topical = (
                _keywords(sig.replace("-", " "))
                | _keywords(f.get("rule", ""))
                | _keywords(f.get("situation", ""))
            )
            overlap = task_kw & topical
            if not overlap:
                continue
            scored.append({
                "id": b["id"], "sig": sig, "rule": f.get("rule", ""), "scope": scope,
                "score": len(overlap), "matched": sorted(overlap),
            })
    best: dict[str, dict] = {}
    for r in scored:
        cur = best.get(r["sig"])
        if cur is None or (cur["scope"] == "org" and r["scope"] == "project") or r["score"] > cur["score"]:
            best[r["sig"]] = r
    out = sorted(best.values(), key=lambda r: (-r["score"], r["sig"]))
    return out[:max(0, int(cap))]


if __name__ == "__main__":
    import os
    import sys
    import tempfile

    tmp = Path(tempfile.mkdtemp(prefix="shamel-lessons-cache-demo-"))
    prj = "PRJ-DEMO-LESSONS"
    (tmp / prj / "_context").mkdir(parents=True)
    os.environ["SOFI_PROJECTS_DIR"] = str(tmp)

    # 1) add a lesson
    les_id = add_lesson(
        prj,
        situation="Parallel worktrees on gate 4 corrupted a shared vendor/ cache across squads.",
        what_failed="No per-worktree cache isolation.",
        rule="Export a per-worktree build-cache dir before any parallel gate-4 squad starts.",
        sig="parallel-cache-bleed",
        source="TKT-777",
        date="2026-07-07",
        confidence=0.8, uses=0, successes=0, last_seen_week=1,
    )
    assert les_id == "LES-001", les_id
    blocks = _read_blocks(_project_lessons_path(prj))
    assert len(blocks) == 1 and blocks[0]["fields"]["sig"] == "parallel-cache-bleed", blocks
    print(f"add_lesson: {les_id}")

    # 2) score_confidence
    assert score_confidence(0, 0) == 0.5, score_confidence(0, 0)
    assert round(score_confidence(9, 9), 3) == round(10 / 11, 3)
    print("score_confidence: ok")

    # 3) apply_decay — 5%/week, multiplicative, bounded
    d0 = apply_decay(0.8, 0)
    d6 = apply_decay(0.8, 6)
    assert d0 == 0.8, d0
    assert round(d6, 4) == round(0.8 * (0.95 ** 6), 4), d6
    assert d6 < 0.7, d6
    print(f"apply_decay: week0={d0} week6={round(d6, 4)}")

    # 4) select_for_injection — fresh (1 week elapsed) clears the 0.7 bar
    sel_early = select_for_injection(prj, now_week=2, cap=6, min_conf=0.7)
    assert len(sel_early) == 1 and sel_early[0]["sig"] == "parallel-cache-bleed", sel_early
    print(f"select_for_injection (early, 1wk decay): {sel_early}")

    # ... but decays below the bar by now_week=10 (9 weeks unused)
    sel_late = select_for_injection(prj, now_week=10, cap=6, min_conf=0.7)
    assert sel_late == [], sel_late
    print("select_for_injection (late, decayed below bar): []")

    # cap enforcement — 7 more fresh, high-confidence lessons; still capped at 6
    for i in range(2, 9):
        add_lesson(prj, situation=f"s{i}", what_failed=f"f{i}", rule=f"r{i}",
                   sig=f"sig-{i}", confidence=0.9, uses=0, successes=0, last_seen_week=1)
    sel_capped = select_for_injection(prj, now_week=2, cap=6, min_conf=0.7)
    assert len(sel_capped) == 6, sel_capped
    print(f"select_for_injection cap enforced: {len(sel_capped)} <= 6")

    # 5) record_use — reinforce the first lesson twice, resets its clock
    record_use(prj, "parallel-cache-bleed", success=True, now_week=10)
    record_use(prj, "parallel-cache-bleed", success=True, now_week=10)
    reinforced = next(b for b in _read_blocks(_project_lessons_path(prj))
                       if b["fields"]["sig"] == "parallel-cache-bleed")
    assert reinforced["fields"]["uses"] == "2", reinforced
    assert reinforced["fields"]["last_seen_week"] == "10", reinforced
    assert reinforced["fields"]["confidence"] == "0.75", reinforced  # (2+1)/(2+2)
    sel_after_reinforce = select_for_injection(prj, now_week=10, cap=6, min_conf=0.7)
    assert any(r["sig"] == "parallel-cache-bleed" for r in sel_after_reinforce), sel_after_reinforce
    print("record_use: reinforced lesson (uses=2, conf=0.75) clears the bar again at now_week=10")

    # 6) promote_candidates — 5+ occurrences across 2+ projects qualifies
    occ = {
        "parallel-cache-bleed": ["PRJ-A", "PRJ-A", "PRJ-B", "PRJ-B", "PRJ-C"],
        "one-off-typo": ["PRJ-A"],
    }
    promo = promote_candidates(occ, threshold=5, min_projects=2)
    assert [p["sig"] for p in promo] == ["parallel-cache-bleed"], promo
    print(f"promote_candidates: {[p['sig'] for p in promo]}")

    # 7) vaccine_for — topical match against an incoming task's brief
    hits = vaccine_for(prj, "Spin up a parallel gate-4 squad sharing the vendor cache across worktrees")
    assert any(h["sig"] == "parallel-cache-bleed" for h in hits), hits
    print(f"vaccine_for: {[h['sig'] for h in hits]}")

    # vaccine_for also reaches org-level LESSONS.md (read-only merge)
    org_hits = vaccine_for(prj, "Agents keep skipping shamel sync before acting and losing thread across sessions")
    assert any(h["scope"] == "org" for h in org_hits), org_hits
    print(f"vaccine_for (org-scope match): {[(h['sig'], h['scope']) for h in org_hits]}")

    print("PASS")
    sys.exit(0)
