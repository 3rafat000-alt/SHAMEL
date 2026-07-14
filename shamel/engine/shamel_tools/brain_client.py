"""
role: shared library (shamel_tools)
purpose: Python client for brain MCP server — agents import
gate: 0-8
outputs: dict/list/str from brain MCP server
exit: methods return empty/falsy on error, never raise
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any


def _rpc(url: str, method: str, params: dict[str, Any] | None = None) -> dict | list | str | bool | None:
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {},
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError,
            json.JSONDecodeError, OSError) as e:
        return None
    if "error" in data:
        return None
    return data.get("result")


class BrainClient:
    """Client for the SHAMEL Brain MCP server.

    Agents instantiate this to read/write brain memory, search,
    look up agents/rooms, and manage working memory.

    Usage:
        client = BrainClient()
        state = client.read("state")
        agent = client.agent("brd-ceo")
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = (
            base_url
            or os.environ.get("BRAIN_MCP_URL")
            or "http://localhost:8765"
        )
        self._rpc_url = f"{self.base_url.rstrip('/')}/"

    def _call(self, method: str, **kwargs) -> Any:
        return _rpc(self._rpc_url, method, kwargs)

    def read(self, path: str) -> str:
        """Read a brain file by resource path.

        Accepts full URIs (brain://org/decisions) or short names (decisions).
        """
        result = self._call("brain_read", resource_path=path)
        return result if isinstance(result, str) else ""

    def search(self, query: str, section: str | None = None) -> list:
        """FTS5 search across brain files.

        Args:
            query: free-text search string
            section: optional kind filter

        Returns:
            list of match dicts with id/type/summary/rank
        """
        params: dict = {"query": query}
        if section is not None:
            params["section"] = section
        result = self._call("brain_search", **params)
        return result if isinstance(result, list) else []

    def write(self, path: str, content: str, append: bool = False) -> bool:
        """Write or append content to a brain file."""
        result = self._call("brain_write", resource_path=path, content=content, append=append)
        return result is True

    def record_decision(self, title: str, context: str, decision: str, consequences: str) -> str:
        """Record an Architectural Decision Record (ADR).

        Returns the ADR id string (e.g. 'ADR-004').
        """
        result = self._call(
            "brain_record_decision",
            title=title,
            context=context,
            decision=decision,
            consequences=consequences,
        )
        return result if isinstance(result, str) else ""

    def remember(self, key: str, value: str, ttl: int = 24) -> bool:
        """Store a working memory fact with TTL in hours."""
        result = self._call("brain_remember", key=key, value=value, ttl_hours=ttl)
        return result is True

    def recall(self, key: str) -> str:
        """Retrieve a working memory fact by key."""
        result = self._call("brain_recall", key=key)
        return result if isinstance(result, str) else ""

    def agent(self, name: str) -> dict:
        """Look up agent info from registry.yaml."""
        result = self._call("agent_lookup", name=name)
        return result if isinstance(result, dict) else {}

    def room(self, code: str) -> dict:
        """Look up room info from registry.yaml."""
        result = self._call("room_lookup", room_code=code)
        return result if isinstance(result, dict) else {}

    def route(self, agent: str) -> dict:
        """Find routing config for an agent."""
        result = self._call("route_lookup", agent_name=agent)
        return result if isinstance(result, dict) else {}
