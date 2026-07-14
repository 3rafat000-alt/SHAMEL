"""
role: shared library (core/shamel_tools)
purpose: "the harness remembers" — capture -> compress -> inject brain pipeline
    over SQLite FTS5 (EVOLUTION.md Round 2 #4 + #6). PostToolUse captures raw
    observations, SessionEnd folds a session into one summary row, SessionStart
    injects a token-bounded digest, UserPromptSubmit does a topical FTS match
    for [LEARN]/vaccine injection. A second table indexes brain markdown files
    by heading (byte offsets + sha256) for cheap section-level retrieval
    (~12k -> ~400 tokens/lookup). The LLM never touches the write path — every
    function here is pure deterministic storage/index/string-assembly.
gate: 0-8 (memory is gate-agnostic; callers stamp project/kind per gate)
inputs: source/kind/summary/body/ts strings (caller-supplied, never wall-clock);
    a project id; a brain markdown file path; a free-text query.
outputs: rows in .claude/memory/brain.db (observations, sections + their FTS5
    shadow indexes); search()/fetch() return plain dict lists, never a live
    cursor; inject_digest()/compress_session() return plain strings.
exit: 0 on success. Raises sqlite3.Error on a DB fault, ValueError on a
    malformed id passed to fetch(), GovernanceError if a caller points connect()
    outside the workspace root.
"""
from __future__ import annotations

import hashlib
import re
import sqlite3
from pathlib import Path

from . import paths, guard, brain, tickets

_DB_REL = Path(".claude") / "memory" / "brain.db"

_SCHEMA = """
CREATE TABLE IF NOT EXISTS observations (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT NOT NULL,
    source  TEXT NOT NULL DEFAULT '',
    kind    TEXT NOT NULL DEFAULT '',
    summary TEXT NOT NULL DEFAULT '',
    body    TEXT NOT NULL DEFAULT '',
    project TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_observations_project ON observations(project);
CREATE INDEX IF NOT EXISTS idx_observations_source  ON observations(source);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(summary, body);

CREATE TABLE IF NOT EXISTS sections (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    file       TEXT NOT NULL,
    heading    TEXT NOT NULL DEFAULT '',
    byte_start INTEGER NOT NULL DEFAULT 0,
    byte_end   INTEGER NOT NULL DEFAULT 0,
    sha256     TEXT NOT NULL DEFAULT '',
    summary    TEXT NOT NULL DEFAULT '',
    project    TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sections_file ON sections(file, project);

CREATE VIRTUAL TABLE IF NOT EXISTS sections_fts USING fts5(heading, summary);
"""

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def db_path() -> Path:
    """Single db location: .claude/memory/brain.db (created on first connect)."""
    return paths.repo_root() / _DB_REL


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    """Open (creating schema idempotently) the memory db. WAL + busy_timeout
    guard against the multi-writer locking this pipeline is built for
    (PostToolUse/SessionEnd/SessionStart/UserPromptSubmit all write or read)."""
    p = Path(path) if path is not None else db_path()
    guard.assert_within_repo(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=30000")
    conn.executescript(_SCHEMA)
    conn.commit()
    return conn


def _insert_observation(conn: sqlite3.Connection, *, ts: str, source: str, kind: str,
                        summary: str, body: str, project: str) -> int:
    cur = conn.execute(
        "INSERT INTO observations (ts, source, kind, summary, body, project) VALUES (?,?,?,?,?,?)",
        (ts, source, kind, summary, body, project),
    )
    oid = int(cur.lastrowid)
    conn.execute(
        "INSERT INTO observations_fts (rowid, summary, body) VALUES (?,?,?)",
        (oid, summary, body),
    )
    return oid


def capture(source: str, kind: str, summary: str, body: str, ts: str, project: str = "") -> int:
    """PostToolUse (or any caller) feeds one raw observation. Pure insert — no
    model call, no wall-clock (ts is supplied by the caller)."""
    conn = connect()
    try:
        oid = _insert_observation(conn, ts=ts, source=source, kind=kind,
                                   summary=summary, body=body, project=project)
        conn.commit()
        return oid
    finally:
        conn.close()


def _line_byte_offsets(lines: list[str]) -> list[int]:
    offsets = []
    pos = 0
    for line in lines:
        offsets.append(pos)
        pos += len(line.encode("utf-8"))
    offsets.append(pos)  # sentinel: total byte length
    return offsets


def index_brain_file(path: str | Path, project: str = "") -> int:
    """Parse a markdown brain file by ATX heading (#..######) into `sections`
    rows carrying byte offsets + a sha256 of the section body (drift
    detection). Re-indexing a file REPLACES its prior rows (keyed on
    file+project) rather than accumulating duplicates."""
    p = Path(path).resolve()
    text = p.read_text(encoding="utf-8")
    file_key = str(p)
    lines = text.splitlines(keepends=True)
    offsets = _line_byte_offsets(lines)

    heads: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        m = _HEADING.match(line.rstrip("\n"))
        if m:
            heads.append((i, m.group(2).strip()))

    spans: list[tuple[int, int, str]] = []
    if not heads:
        spans.append((0, len(lines), "(document)"))
    else:
        if heads[0][0] > 0:
            spans.append((0, heads[0][0], "(preamble)"))
        for idx, (line_i, heading) in enumerate(heads):
            end_i = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
            spans.append((line_i, end_i, heading))

    conn = connect()
    try:
        old_ids = [r[0] for r in conn.execute(
            "SELECT id FROM sections WHERE file = ? AND project = ?", (file_key, project)
        ).fetchall()]
        for oid in old_ids:
            conn.execute("DELETE FROM sections_fts WHERE rowid = ?", (oid,))
        conn.execute("DELETE FROM sections WHERE file = ? AND project = ?", (file_key, project))

        n = 0
        for start_i, end_i, heading in spans:
            content = "".join(lines[start_i:end_i])
            if not content.strip():
                continue
            byte_start = offsets[start_i]
            byte_end = offsets[end_i]
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            body_lines = [ln.strip() for ln in content.splitlines()
                          if ln.strip() and not _HEADING.match(ln)]
            summary = (body_lines[0] if body_lines else heading)[:200]
            cur = conn.execute(
                "INSERT INTO sections (file, heading, byte_start, byte_end, sha256, summary, project) "
                "VALUES (?,?,?,?,?,?,?)",
                (file_key, heading, byte_start, byte_end, digest, summary, project),
            )
            sid = int(cur.lastrowid)
            conn.execute(
                "INSERT INTO sections_fts (rowid, heading, summary) VALUES (?,?,?)",
                (sid, heading, summary),
            )
            n += 1
        conn.commit()
        return n
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _fts_query(text: str) -> str:
    """Tokens OR'd and individually quoted — tolerant of any punctuation in
    `text` that would otherwise be invalid FTS5 query syntax."""
    toks = re.findall(r"[A-Za-z0-9_]+", text)
    if not toks:
        return '""'
    return " OR ".join(f'"{t}"' for t in toks[:24])


def search(query: str, k: int = 8, project: str | None = None) -> list[dict]:
    """ID + summary index over BOTH observations and sections, ranked by FTS5
    bm25 (lower = better match). Never returns full bodies — callers pull
    those via fetch(), ~10x cheaper on the common case of scanning many hits."""
    q = _fts_query(query)
    conn = connect()
    try:
        hits: list[dict] = []

        obs_sql = (
            "SELECT o.id, o.ts, o.source, o.kind, o.summary, o.project, "
            "bm25(observations_fts) AS rank "
            "FROM observations_fts JOIN observations o ON o.id = observations_fts.rowid "
            "WHERE observations_fts MATCH ?"
        )
        params: list = [q]
        if project:
            obs_sql += " AND o.project = ?"
            params.append(project)
        obs_sql += " ORDER BY rank LIMIT ?"
        params.append(k)
        for r in conn.execute(obs_sql, params).fetchall():
            hits.append({
                "id": f"obs-{r['id']}", "type": "observation", "kind": r["kind"],
                "source": r["source"], "project": r["project"], "ts": r["ts"],
                "summary": r["summary"], "rank": r["rank"],
            })

        sec_sql = (
            "SELECT s.id, s.file, s.heading, s.summary, s.project, "
            "bm25(sections_fts) AS rank "
            "FROM sections_fts JOIN sections s ON s.id = sections_fts.rowid "
            "WHERE sections_fts MATCH ?"
        )
        params2: list = [q]
        if project:
            sec_sql += " AND s.project = ?"
            params2.append(project)
        sec_sql += " ORDER BY rank LIMIT ?"
        params2.append(k)
        for r in conn.execute(sec_sql, params2).fetchall():
            hits.append({
                "id": f"sec-{r['id']}", "type": "section", "heading": r["heading"],
                "file": r["file"], "project": r["project"],
                "summary": r["summary"], "rank": r["rank"],
            })

        hits.sort(key=lambda d: d["rank"])
        return hits[:k]
    finally:
        conn.close()


def fetch(ids: list) -> list[dict]:
    """Pull full rows (body/heading text included) for ids returned by
    search() (tagged 'obs-N'/'sec-N') or a bare int/numeric-string id from
    capture() (assumed observations)."""
    conn = connect()
    try:
        out: list[dict] = []
        for raw in ids:
            s = str(raw)
            if "-" in s and s.split("-", 1)[0] in ("obs", "sec"):
                tag, _, num_s = s.partition("-")
            else:
                tag, num_s = "obs", s
            if not num_s.isdigit():
                continue
            num = int(num_s)
            table = "observations" if tag == "obs" else "sections"
            r = conn.execute(f"SELECT * FROM {table} WHERE id = ?", (num,)).fetchone()
            if r is None:
                continue
            d = dict(r)
            d["id"] = f"{tag}-{num}"
            d["type"] = "observation" if tag == "obs" else "section"
            out.append(d)
        return out
    finally:
        conn.close()


def inject_digest(project: str, token_budget: int = 1000, now_ts: str | None = None) -> str:
    """SessionStart digest: identity + latest STATE head + next open ticket +
    top-3 recent observations, hard-capped to ~token_budget (chars/4, a cheap
    deterministic proxy — no tokenizer dependency). `now_ts`, when given,
    excludes observations captured after it (reproducible replay/tests)."""
    lines = [f"# memory digest — {project or '(no project)'}"]

    state = brain.read_state(project) if project else {}
    if state:
        branch = state.get("branch", "")
        head = state.get("head_sha", "")
        gate = state.get("gate", "")
        lines.append(f"state: gate={gate} branch={branch} head_sha={head}")

    tkt = None
    if project:
        try:
            tkt = tickets.next_open(project)
        except Exception:
            tkt = None
    if tkt is not None:
        lines.append(f"next ticket: {tkt.id} (gate {tkt.gate}) -> {tkt.to}: {tkt.task}")

    conn = connect()
    try:
        q = "SELECT id, ts, kind, summary FROM observations"
        clauses, params = [], []
        if project:
            clauses.append("project = ?")
            params.append(project)
        if now_ts:
            clauses.append("ts <= ?")
            params.append(now_ts)
        if clauses:
            q += " WHERE " + " AND ".join(clauses)
        q += " ORDER BY id DESC LIMIT 3"
        rows = conn.execute(q, params).fetchall()
    finally:
        conn.close()
    if rows:
        lines.append("recent:")
        for r in rows:
            lines.append(f"- [{r['kind']}] {r['summary']}")

    text = "\n".join(lines)
    max_chars = max(token_budget * 4, 200)
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip() + "..."
    return text


def compress_session(session_id: str, ts: str) -> str:
    """SessionEnd: fold every observation captured under `source == session_id`
    into one summary row (kind='session'), so SessionStart injection reads one
    compact line per past session instead of replaying its raw log. Pure
    string-fold — no model call. Returns '' (no row written) if the session
    left no observations."""
    conn = connect()
    try:
        rows = conn.execute(
            "SELECT kind, summary, project FROM observations "
            "WHERE source = ? AND kind != 'session' ORDER BY id",
            (session_id,),
        ).fetchall()
        if not rows:
            return ""
        project = next((r["project"] for r in reversed(rows) if r["project"]), "")
        bullets = [f"[{r['kind']}] {r['summary']}" for r in rows]
        summary = f"session {session_id} ({len(rows)} obs): " + " | ".join(bullets)
        if len(summary) > 4000:
            summary = summary[:3997] + "..."
        body = "\n".join(bullets)
        _insert_observation(conn, ts=ts, source=session_id, kind="session",
                             summary=summary, body=body, project=project)
        conn.commit()
        return summary
    finally:
        conn.close()


def learn_match(prompt_text: str, k: int = 3) -> list[dict]:
    """Topical FTS match against the memory db for [LEARN]/vaccine injection
    at UserPromptSubmit — a thin, purpose-named wrapper over search() (mixed
    observation+section hits, ranked) so callers don't have to know the
    underlying table split."""
    return search(prompt_text, k=k, project=None)


if __name__ == "__main__":
    import shutil
    import tempfile

    tmp_dir = Path(tempfile.mkdtemp(prefix="memdb_selftest_"))
    tmp_db = tmp_dir / "brain.db"

    def _connect():
        c = sqlite3.connect(str(tmp_db), timeout=30.0)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA busy_timeout=30000")
        c.executescript(_SCHEMA)
        c.commit()
        return c

    # Monkeypatch connect() to the tmp db for the duration of this self-test —
    # keeps the demo from touching the real .claude/memory/brain.db.
    _real_connect = connect
    globals()["connect"] = lambda path=None: _connect()

    try:
        id1 = capture("sess-1", "tool_use", "ran pytest, 3 failures", "full pytest -q output here",
                       ts="2026-07-07T10:00:00Z", project="PRJ-TEST")
        id2 = capture("sess-1", "edit", "fixed off-by-one in parser.py", "diff body...",
                       ts="2026-07-07T10:05:00Z", project="PRJ-TEST")
        id3 = capture("sess-1", "tool_use", "reran pytest, all green", "full pytest -q output here",
                       ts="2026-07-07T10:10:00Z", project="PRJ-TEST")
        assert id1 and id2 and id3 and id1 != id2 != id3, "capture() must return distinct ids"

        brain_md = tmp_dir / "STATE.md"
        brain_md.write_text(
            "# STATE\n"
            "gate: 4\nbranch: prj/test\nhead_sha: abc123\n\n"
            "## Notes\nSome free text about the current milestone.\n",
            encoding="utf-8",
        )
        n = index_brain_file(brain_md, project="PRJ-TEST")
        assert n >= 2, f"expected >=2 sections indexed, got {n}"
        n2 = index_brain_file(brain_md, project="PRJ-TEST")  # re-index must replace, not accumulate
        assert n2 == n, f"re-index should replace prior rows: {n} vs {n2}"

        hits = search("pytest", k=8, project="PRJ-TEST")
        assert hits, "search('pytest') found no hits"
        assert any(h["type"] == "observation" for h in hits), "expected an observation hit"

        sec_hits = search("milestone", k=8, project="PRJ-TEST")
        assert any(h["type"] == "section" for h in sec_hits), "expected a section hit for 'milestone'"

        fetched = fetch([hits[0]["id"]])
        assert fetched and "body" in fetched[0], "fetch() must return the full row incl. body"

        digest = inject_digest("PRJ-TEST", token_budget=200, now_ts="2026-07-07T11:00:00Z")
        assert len(digest) <= 800, f"digest exceeded budget: {len(digest)} chars"
        assert "recent" in digest, "digest missing recent-observations section"

        summary = compress_session("sess-1", ts="2026-07-07T10:15:00Z")
        assert summary and "session sess-1" in summary, "compress_session produced no summary"
        post = search("pytest", k=8, project="PRJ-TEST")
        assert any(h["kind"] == "session" for h in post if h["type"] == "observation"), \
            "compressed session row not found by search()"

        matches = learn_match("pytest failures", k=3)
        assert matches, "learn_match found no topical hits"

        print("PASS")
    finally:
        globals()["connect"] = _real_connect
        shutil.rmtree(tmp_dir, ignore_errors=True)
