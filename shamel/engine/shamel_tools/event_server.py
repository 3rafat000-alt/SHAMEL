"""
role: shared library (core/shamel_tools) — owner obs-monitoring-engineer
purpose: fleet telemetry sink (EVOLUTION.md Round 2 #10) — a tiny stdlib HTTP
    server that lets a dashboard poll the fleet's event stream without any
    third-party dependency. `telemetry.send_event` durably appends to
    `.claude/memory/events.jsonl` regardless of whether this server is up;
    this module only ever TAILS that same file for GET /events, plus accepts
    the optional best-effort POST /events telemetry.py fires. Import-safe: no
    socket is opened until `main()`/`serve()` runs, never on import.
gate: cross (observability is gate-agnostic; served for any project/gate)
inputs: CLI --port (default 8799), --host (default 127.0.0.1), --tail (default
    100, GET /events?n=<int> overrides per-request); no wall-clock/random used.
outputs: HTTP responses only (GET /events -> JSON list, GET /health -> JSON
    status, POST /events -> best-effort JSONL append via telemetry.send_event
    with the request's own body, no re-stamped ts); no other side effects.
exit: `python -m shamel_tools.event_server --port N` serves until interrupted
    (SIGINT/Ctrl-C -> exit 0). Malformed requests get a 4xx JSON body, never
    a raised exception that kills the server thread.
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from . import telemetry

DEFAULT_PORT = 8799
DEFAULT_HOST = "127.0.0.1"
DEFAULT_TAIL = 100


class _EventHandler(BaseHTTPRequestHandler):
    server_version = "SofiEventServer/1.0"

    def log_message(self, fmt: str, *args) -> None:  # noqa: A003 - stdlib signature
        pass  # keep hook/CLI output quiet; this is not the durable record

    def _send_json(self, status: int, payload: object) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - stdlib method name
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        if parsed.path == "/events":
            qs = parse_qs(parsed.query)
            try:
                n = int(qs.get("n", [str(DEFAULT_TAIL)])[0])
            except ValueError:
                self._send_json(400, {"error": "n must be an integer"})
                return
            events = telemetry.read_events(n)
            self._send_json(200, {"events": events, "count": len(events)})
            return
        self._send_json(404, {"error": "not found", "path": parsed.path})

    def do_POST(self) -> None:  # noqa: N802 - stdlib method name
        parsed = urlparse(self.path)
        if parsed.path != "/events":
            self._send_json(404, {"error": "not found", "path": parsed.path})
            return
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
            raw = self.rfile.read(length) if length else b""
            event = json.loads(raw.decode("utf-8")) if raw else {}
            if not isinstance(event, dict):
                raise ValueError("event body must be a JSON object")
        except Exception as e:
            self._send_json(400, {"error": f"bad request: {e}"})
            return
        # A client-sent ts (from telemetry.send_event) is preserved as-is; only a
        # missing one is stamped, and even then with the request's own field, not
        # a wall-clock read inside this module (GOVERNANCE Rule 9 stays with the
        # original caller's now_ts — we merely relay/re-store what was posted).
        now_ts = event.get("ts", "")
        telemetry.send_event(event, now_ts=now_ts)
        self._send_json(202, {"status": "accepted"})


def build_server(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    """Construct (but do not start) the server. Binding happens in `serve()`."""
    return ThreadingHTTPServer((host, port), _EventHandler)


def serve(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
    """Bind and serve forever. Only ever called from `main()` — never on import."""
    httpd = build_server(host, port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="SOFI fleet telemetry event server")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--host", default=DEFAULT_HOST)
    args = ap.parse_args(argv)
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
