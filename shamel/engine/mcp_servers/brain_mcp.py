"""
role: shared library (engine/mcp_servers)
purpose: MCP server exposing brain memory as tools/resources for agents
gate: 0-8
inputs: brain file paths, FTS5 queries, working memory key/values
outputs: JSON-RPC responses over HTTP on port 8765
exit: 0 on clean shutdown, 1 on fatal startup error
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

from shamel_tools import paths, registry, routing

BRAIN_ROOT = paths.brain_dir()
ORG_DIR = BRAIN_ROOT / "org"

_RESOURCE_MAP = {
    "brain://org/decisions": ORG_DIR / "DECISIONS.md",
    "brain://org/lessons": ORG_DIR / "LESSONS.md",
    "brain://org/evolutions": ORG_DIR / "EVOLUTION.md",
    "brain://org/handoffs": ORG_DIR / "HANDOFFS.md",
    "brain://org/personas": ORG_DIR / "PERSONAS.md",
    "brain://state": BRAIN_ROOT / "STATE.md",
    "brain://session/latest": BRAIN_ROOT / "db" / "sessions.jsonl",
}

_RESOURCE_ALIASES = {
    "decisions": "brain://org/decisions",
    "lessons": "brain://org/lessons",
    "evolutions": "brain://org/evolutions",
    "handoffs": "brain://org/handoffs",
    "personas": "brain://org/personas",
    "state": "brain://state",
    "session": "brain://session/latest",
}

_WORKING_MEM_DB = BRAIN_ROOT / "db" / "working_mem.db"




def _resolve_resource_path(path: str) -> Path | None:
    if path in _RESOURCE_MAP:
        return _RESOURCE_MAP[path]
    if path in _RESOURCE_ALIASES:
        return _RESOURCE_MAP[_RESOURCE_ALIASES[path]]
    p = ORG_DIR / f"{path.upper()}.md" if not path.endswith(".md") else ORG_DIR / path
    p = p.resolve()
    if p.exists() and BRAIN_ROOT.resolve() in (p, *p.parents):
        return p
    p2 = (BRAIN_ROOT / path).resolve()
    if p2.exists() and BRAIN_ROOT.resolve() in (p2, *p2.parents):
        return p2
    return None


def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise RuntimeError(f"cannot read {path}: {e}")


def _write_file(path: Path, content: str, append: bool = False) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    try:
        with path.open(mode, encoding="utf-8") as fh:
            fh.write(content)
        return True
    except OSError as e:
        raise RuntimeError(f"cannot write {path}: {e}")


# ── Working Memory ────────────────────────────────────────────────────────────

def _mem_cleanup(conn: sqlite3.Connection):
    now = time.time()
    conn.execute("DELETE FROM wmem WHERE expires <= ?", (now,))
    conn.commit()


def _wmem_conn() -> sqlite3.Connection:
    _WORKING_MEM_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_WORKING_MEM_DB))
    conn.execute("CREATE TABLE IF NOT EXISTS wmem (key TEXT PRIMARY KEY, value TEXT NOT NULL, expires REAL NOT NULL)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_wmem_expires ON wmem(expires)")
    conn.commit()
    return conn


def _remember(key: str, value: str, ttl_hours: int = 24) -> bool:
    conn = _wmem_conn()
    try:
        _mem_cleanup(conn)
        expires = time.time() + ttl_hours * 3600
        conn.execute(
            "INSERT OR REPLACE INTO wmem (key, value, expires) VALUES (?, ?, ?)",
            (key, value, expires),
        )
        conn.commit()
        return True
    except sqlite3.Error as e:
        raise RuntimeError(f"wmem write failed: {e}")
    finally:
        conn.close()


def _recall(key: str) -> str:
    conn = _wmem_conn()
    try:
        _mem_cleanup(conn)
        row = conn.execute(
            "SELECT value FROM wmem WHERE key = ? AND expires > ?",
            (key, time.time()),
        ).fetchone()
        return row[0] if row else ""
    finally:
        conn.close()


# ── FTS5 Search ───────────────────────────────────────────────────────────────

def _fts_query(text: str) -> str:
    import re
    toks = re.findall(r"[A-Za-z0-9_]+", text)
    if not toks:
        return '""'
    return " OR ".join(f'"{t}"' for t in toks[:24])


def _search(query: str, section: str | None = None) -> list[dict]:
    hits: list[dict] = []
    q = _fts_query(query)
    brain_db = BRAIN_ROOT / "db" / "brain.db"
    if not brain_db.exists():
        return hits
    try:
        conn = sqlite3.connect(str(brain_db))
        conn.row_factory = sqlite3.Row
        sql = (
            "SELECT o.id, o.ts, o.source, o.kind, o.summary, o.project, "
            "bm25(observations_fts) AS rank "
            "FROM observations_fts JOIN observations o ON o.id = observations_fts.rowid "
            "WHERE observations_fts MATCH ?"
        )
        params: list = [q]
        if section:
            sql += " AND o.kind = ?"
            params.append(section)
        sql += " ORDER BY rank LIMIT 16"
        for r in conn.execute(sql, params):
            hits.append({
                "id": f"obs-{r['id']}", "type": "observation",
                "kind": r["kind"], "source": r["source"],
                "project": r["project"], "ts": r["ts"],
                "summary": r["summary"], "rank": r["rank"],
            })
        conn.close()
    except sqlite3.Error:
        pass
    return hits


# ── JSON-RPC Handler ──────────────────────────────────────────────────────────

class BrainMCPHandler(BaseHTTPRequestHandler):
    """JSON-RPC handler for brain MCP protocol."""

    def log_message(self, fmt, *args):
        sys.stderr.write(f"[brain-mcp] {args[0]} {args[1]} {args[2]}\n")

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code: int, message: str, req_id: Any = None):
        self._send_json({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        })

    def _result(self, result: Any, req_id: Any = None):
        self._send_json({"jsonrpc": "2.0", "id": req_id, "result": result})

    def do_GET(self):
        if self.path == "/health":
            self._send_json({"status": "ok", "service": "brain-mcp"})
            return
        if self.path == "/resources":
            resources = []
            for uri, fpath in _RESOURCE_MAP.items():
                resources.append({
                    "uri": uri,
                    "name": fpath.stem,
                    "exists": fpath.exists(),
                })
            self._result(resources)
            return
        if self.path == "/tools":
            self._result([
                {"name": "brain_read", "params": {"resource_path": "string"}},
                {"name": "brain_search", "params": {"query": "string", "section?": "string"}},
                {"name": "brain_write", "params": {"resource_path": "string", "content": "string", "append?": "boolean"}},
                {"name": "brain_record_decision", "params": {"title": "string", "context": "string", "decision": "string", "consequences": "string"}},
                {"name": "brain_remember", "params": {"key": "string", "value": "string", "ttl_hours?": "integer"}},
                {"name": "brain_recall", "params": {"key": "string"}},
                {"name": "agent_lookup", "params": {"name": "string"}},
                {"name": "room_lookup", "params": {"room_code": "string"}},
                {"name": "route_lookup", "params": {"agent_name": "string"}},
            ])
            return
        self._error(-32000, f"not found: {self.path}")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return self._error(-32700, "empty request body")
        raw = self.rfile.read(length)
        try:
            req = json.loads(raw)
        except json.JSONDecodeError:
            return self._error(-32700, "invalid JSON")

        req_id = req.get("id", None)
        method = req.get("method", "")
        params = req.get("params", {}) or {}
        handler = _METHODS.get(method)
        if handler is None:
            return self._error(-32601, f"unknown method: {method}", req_id)
        try:
            result = handler(**params)
            self._result(result, req_id)
        except TypeError as e:
            self._error(-32602, f"invalid params: {e}", req_id)
        except Exception as e:
            self._error(-32603, str(e), req_id)

    do_PUT = do_POST


# ── Tool Implementations ──────────────────────────────────────────────────────

def _tool_brain_read(resource_path: str) -> str:
    fpath = _resolve_resource_path(resource_path)
    if fpath is None:
        raise ValueError(f"unknown resource path: {resource_path}")
    return _read_file(fpath)


def _tool_brain_search(query: str, section: str | None = None) -> list[dict]:
    return _search(query, section)


def _tool_brain_write(resource_path: str, content: str, append: bool = False) -> bool:
    fpath: Path | None = None
    if resource_path.startswith("brain://"):
        fpath = _resolve_resource_path(resource_path)
        if fpath is None:
            fpath = (BRAIN_ROOT / resource_path.removeprefix("brain://")).resolve()
    else:
        fpath = (BRAIN_ROOT / resource_path).resolve()
    if not fpath or BRAIN_ROOT.resolve() not in (fpath, *fpath.parents):
        raise ValueError("write path outside brain directory — denied")
    return _write_file(fpath, content, append)


def _tool_brain_record_decision(title: str, context: str, decision: str, consequences: str) -> str:
    dec_path = ORG_DIR / "DECISIONS.md"
    existing = _read_file(dec_path) if dec_path.exists() else ""
    n = existing.count("## ADR-") + 1
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    block = (
        f"\n## ADR-{n:03d} ({date}) — {title}\n"
        f"**Status:** ACTIVE\n"
        f"**Context:** {context}\n"
        f"**Decision:** {decision}\n"
        f"**Consequences:** {consequences}\n"
    )
    _write_file(dec_path, block, append=True)
    return f"ADR-{n:03d}"


def _tool_brain_remember(key: str, value: str, ttl_hours: int = 24) -> bool:
    return _remember(key, value, ttl_hours)


def _tool_brain_recall(key: str) -> str:
    return _recall(key)


def _tool_agent_lookup(name: str) -> dict:
    agent = registry.agent(name)
    if not agent:
        raise ValueError(f"unknown agent: {name}")
    return agent


def _tool_room_lookup(room_code: str) -> dict:
    rooms = registry.rooms()
    room = rooms.get(room_code)
    if not room:
        for code, r in rooms.items():
            if code == room_code or code.endswith(room_code) or r.get("prefix") == room_code:
                room = r
                break
    if not room:
        for code, r in rooms.items():
            if code.startswith(room_code):
                room = r
                break
    if not room:
        raise ValueError(f"unknown room: {room_code}")
    return room


def _tool_route_lookup(agent_name: str) -> dict:
    try:
        return routing.route_for(agent_name)
    except KeyError:
        raise ValueError(f"no route for agent: {agent_name}")


_METHODS: dict[str, Any] = {
    "brain_read": _tool_brain_read,
    "brain_search": _tool_brain_search,
    "brain_write": _tool_brain_write,
    "brain_record_decision": _tool_brain_record_decision,
    "brain_remember": _tool_brain_remember,
    "brain_recall": _tool_brain_recall,
    "agent_lookup": _tool_agent_lookup,
    "room_lookup": _tool_room_lookup,
    "route_lookup": _tool_route_lookup,
}


# ── Server ────────────────────────────────────────────────────────────────────

class BrainMCPServer:
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None

    def start(self, daemon: bool = True) -> str:
        self._server = HTTPServer((self.host, self.port), BrainMCPHandler)
        addr = f"http://{self.host}:{self.port}"
        if daemon:
            self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._thread.start()
        else:
            print(f"[brain-mcp] listening on {addr}", file=sys.stderr)
            self._server.serve_forever()
        return addr

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server = None

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


def serve(host: str = "127.0.0.1", port: int = 8765):
    server = HTTPServer((host, port), BrainMCPHandler)
    print(f"[brain-mcp] listening on http://{host}:{port}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[brain-mcp] shutting down", file=sys.stderr)
        server.server_close()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(prog="brain-mcp", description="SHAMEL Brain MCP Server")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    serve(a.host, a.port)
