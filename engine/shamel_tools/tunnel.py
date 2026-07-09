"""
tunnel — expose a SOFI project to the public internet via an on-demand tunnel.

Sits ON TOP of `shamel domain`. The local domain (`<slug>.local`) + the shared
Caddy on `:80` already route a `Host` header to each project's php server. A
tunnel just gives that same Caddy a PUBLIC name, so a teammate, client, or a real
phone can reach the exact same app for a demo / UAT — then you tear it down.

Both providers point at Caddy `:80` and set the `Host` header to the project's
existing `<slug>.local`, so Caddy routes through the vhost that already exists —
no vhost edits, no reload races, clean teardown.

Providers (auto-detected; cloudflared preferred — no account, no interstitial):
  - cloudflared → https://<rand>.trycloudflare.com
        `--http-host-header <slug>.local` makes Caddy see the local Host it
        already routes.
  - localtunnel → https://<rand>.loca.lt
        `--local-host <slug>.local` overrides the forwarded Host the same way.
        (loca.lt shows a one-time interstitial asking for the "tunnel password"
        = the server's public IP — cloudflared has none, hence the preference.)

SECURITY — a tunnel publishes a local dev app to the open internet with NO auth
in front of it. Treat every live tunnel as hostile-reachable: no real secrets, no
production data, scope it to a demo, and run `shamel tunnel down` the moment you're
done. Full rules: core/rooms/11-devops/agents/ops-domain-warden.md (owner) +
core/constitution/07-security-law.md; v5 text preserved at
brain/org/archive-v5/protocols/public-tunnels.md.

Flow:
  shamel tunnel up   <PRJ> [provider]   # ensure app+caddy, open tunnel, record URL
  shamel tunnel down <PRJ>              # close tunnel, clear the public URL
  shamel tunnel list                    # project · public url · provider · state
  shamel tunnel status                  # which tunnel clients are installed
"""
from __future__ import annotations

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

from . import domain, paths

# Public-URL shapes each provider prints to its log.
_LT_RE = re.compile(r"https://[a-z0-9][a-z0-9-]*\.loca\.lt")
_CF_RE = re.compile(r"https://[a-z0-9][a-z0-9-]*\.trycloudflare\.com")
URL_WAIT_S = 25  # how long to wait for the provider to hand back a public URL


# ───────────────────────── run state ─────────────────────────

def tunnels_dir() -> Path:
    return domain.run_dir() / "tunnels"


def _state_file(prj: str) -> Path:
    return tunnels_dir() / f"{prj}.json"


def _log_file(prj: str) -> Path:
    return tunnels_dir() / f"{prj}.log"


def _read_state(prj: str) -> dict | None:
    f = _state_file(prj)
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None


def _write_state(prj: str, data: dict) -> None:
    tunnels_dir().mkdir(parents=True, exist_ok=True)
    _state_file(prj).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _pid_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError, ValueError, TypeError):
        return False


# ───────────────────────── providers ─────────────────────────

def _providers() -> dict[str, bool]:
    """Which tunnel clients are installed on this machine."""
    return {
        "cloudflared": shutil.which("cloudflared") is not None,
        "localtunnel": shutil.which("lt") is not None or shutil.which("npx") is not None,
    }


def _resolve_provider(pref: str | None) -> str | None:
    avail = _providers()
    if pref and pref not in ("auto",):
        if pref in ("lt", "localtunnel"):
            pref = "localtunnel"
        elif pref in ("cf", "cloudflare", "cloudflared"):
            pref = "cloudflared"
        return pref if avail.get(pref) else None
    # auto: cloudflared first (stable, no interstitial), else localtunnel.
    if avail["cloudflared"]:
        return "cloudflared"
    if avail["localtunnel"]:
        return "localtunnel"
    return None


def _tunnel_cmd(provider: str, host: str) -> tuple[list[str], re.Pattern]:
    """Build the client command. Always targets Caddy :80, forcing the project's
    own `<slug>.local` Host so Caddy routes through the existing vhost."""
    if provider == "cloudflared":
        return (
            ["cloudflared", "tunnel", "--no-autoupdate",
             "--url", "http://127.0.0.1:80", "--http-host-header", host],
            _CF_RE,
        )
    # localtunnel: prefer the `lt` binary, fall back to `npx localtunnel`.
    lt = shutil.which("lt")
    base = [lt] if lt else ["npx", "--yes", "localtunnel"]
    return base + ["--port", "80", "--local-host", host], _LT_RE


def _await_url(log: Path, rgx: re.Pattern, proc: subprocess.Popen) -> str | None:
    """Poll the client's log until it prints its public URL (or it dies / times out)."""
    end = time.time() + URL_WAIT_S
    while time.time() < end:
        if proc.poll() is not None:
            break  # client exited early — final scan below catches a late URL
        try:
            m = rgx.search(log.read_text(encoding="utf-8", errors="ignore"))
        except OSError:
            m = None
        if m:
            return m.group(0)
        time.sleep(0.5)
    try:
        m = rgx.search(log.read_text(encoding="utf-8", errors="ignore"))
        return m.group(0) if m else None
    except OSError:
        return None


# ───────────────────────── STATE.md stamp ─────────────────────────

def _state_set(prj: str, key: str, value: str | None) -> None:
    """Set (or, with value=None, remove) a `key: value` line in the project's
    STATE.md brain — keeps the public URL discoverable by the next session."""
    sf = paths.brain_file(prj, "STATE")
    if not sf.exists():
        return
    out: list[str] = []
    seen = False
    for ln in sf.read_text(encoding="utf-8").splitlines():
        if ln.startswith(f"{key}:"):
            if value is not None and not seen:
                out.append(f"{key}: {value}")
                seen = True
            continue  # drop old / duplicate / removed
        out.append(ln)
    if value is not None and not seen:
        anchor = next((i for i, l in enumerate(out) if l.startswith("local_domain:")), None)
        if anchor is None:
            anchor = next((i for i, l in enumerate(out) if l.startswith("title:")), len(out) - 1)
        out.insert(anchor + 1, f"{key}: {value}")
    sf.write_text("\n".join(out) + "\n", encoding="utf-8")


# ───────────────────────── subcommands ─────────────────────────

def cmd_up(prj: str, provider_pref: str | None) -> int:
    if not paths.project_exists(prj):
        print(f"✗ no such project: {prj}", file=sys.stderr)
        return 2
    reg = domain._read_domain(prj)
    if not reg:
        print(f"✗ {prj} has no local domain yet — run: shamel domain register {prj}",
              file=sys.stderr)
        return 2
    host, _port = reg

    st = _read_state(prj)
    if st and _pid_alive(st.get("pid")):
        print(f"• {prj} already tunneled → {st.get('url')}  (provider {st.get('provider')})")
        return 0

    provider = _resolve_provider(provider_pref)
    if not provider:
        print("✗ no tunnel client found. Install one:\n"
              "    cloudflared  (preferred): https://github.com/cloudflare/cloudflared\n"
              "    localtunnel             : npm i -g localtunnel", file=sys.stderr)
        return 2

    # Make sure the thing we're about to expose is actually serving locally.
    if domain.caddy_bin():
        try:
            domain._reload_or_start_caddy()
        except subprocess.CalledProcessError:
            pass
    domain.cmd_up(prj)  # idempotent — starts the php server if it's down

    tunnels_dir().mkdir(parents=True, exist_ok=True)
    cmd, rgx = _tunnel_cmd(provider, host)
    log = _log_file(prj)
    with open(log, "wb") as lf:
        proc = subprocess.Popen(cmd, stdout=lf, stderr=lf, start_new_session=True)

    url = _await_url(log, rgx, proc)
    if not url:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
        tail = "\n    ".join(log.read_text(errors="ignore").splitlines()[-6:])
        print(f"✗ {provider} did not return a public URL in {URL_WAIT_S}s.\n"
              f"    {tail}", file=sys.stderr)
        return 1

    _write_state(prj, {"pid": proc.pid, "url": url, "provider": provider,
                       "host": host})
    _state_set(prj, "public_url", url)
    print(f"✓ {prj} is PUBLIC → {url}")
    print(f"  via {provider}  ·  Caddy :80  ·  Host {host}  ·  log {log}")
    print("  ⚠ no auth in front of this. No real secrets / prod data. "
          f"Tear down when done: shamel tunnel down {prj}")
    return 0


def cmd_down(prj: str) -> int:
    st = _read_state(prj)
    if st and _pid_alive(st.get("pid")):
        try:
            os.killpg(os.getpgid(st["pid"]), signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
    _state_file(prj).unlink(missing_ok=True)
    _state_set(prj, "public_url", None)
    print(f"✓ tunnel closed for {prj}")
    return 0


def cmd_list() -> int:
    td = tunnels_dir()
    states = sorted(td.glob("*.json")) if td.exists() else []
    if not states:
        print("(no tunnels — `shamel tunnel up <PRJ>`)")
        return 0
    print(f"{'PROJECT':22} {'PUBLIC URL':40} {'PROVIDER':12} STATE")
    for f in states:
        prj = f.stem
        st = _read_state(prj) or {}
        state = "up" if _pid_alive(st.get("pid")) else "down"
        print(f"{prj:22} {str(st.get('url', '?')):40} {str(st.get('provider', '?')):12} {state}")
    return 0


def cmd_status() -> int:
    avail = _providers()
    td = tunnels_dir()
    states = list(td.glob("*.json")) if td.exists() else []
    up = sum(1 for f in states if _pid_alive((_read_state(f.stem) or {}).get("pid")))
    print("━━ shamel tunnel ━━")
    print(f"  cloudflared : {'✓ installed' if avail['cloudflared'] else '✗ not found'}")
    print(f"  localtunnel : {'✓ installed' if avail['localtunnel'] else '✗ not found'}")
    print(f"  default     : {_resolve_provider(None) or '(none — install a client)'}")
    print(f"  live tunnels: {up}")
    return 0


# ───────────────────────── dispatch ─────────────────────────

def run(action: str, prj: str | None, provider: str | None) -> int:
    if action == "status":
        return cmd_status()
    if action == "list":
        return cmd_list()
    if action in ("up", "down"):
        if not prj:
            print(f"✗ `shamel tunnel {action}` needs a project id", file=sys.stderr)
            return 2
        return cmd_up(prj, provider) if action == "up" else cmd_down(prj)
    print(f"✗ unknown tunnel action: {action} (up|down|list|status)", file=sys.stderr)
    return 2
