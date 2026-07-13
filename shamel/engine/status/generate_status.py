#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مولّد صفحة الحالة العامة — Public Status Page Generator
========================================================
يفحص البورتات/الخدمات/الروابط/الأنفاق ويكتب لقطة HTML ثابتة إلى public/index.html.
للقراءة فقط بالكامل — لا API، لا أزرار تحكم، لا صلاحيات كتابة/قتل/إعادة تشغيل.
آمن للعرض العام لأنه لا ينفّذ أي كود عند كل زيارة، فقط يعيد توليد نفسه دورياً
(عبر systemd timer) ثم Caddy يخدم الملف الناتج كملف ثابت.

تشغيل يدوي: python3 generate_status.py
"""

import os
import re
import glob
import subprocess
from datetime import datetime, timezone
from urllib import request as urlreq
from urllib.error import HTTPError, URLError
from concurrent.futures import ThreadPoolExecutor

try:
    import yaml
except Exception:
    yaml = None

HOME = os.path.expanduser("~")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
OUT_FILE = os.path.join(OUT_DIR, "index.html")

KNOWN_SERVICES = [
    "mysql", "postgresql@18-main", "redis-server", "caddy",
    "php8.5-fpm", "tor@default", "docker", "cups", "cups-browsed", "cloudflared",
]

SITE_FILES = sorted(glob.glob(f"{HOME}/Desktop/SHAMEL/engine/caddy/sites/*.caddy"))


def run(cmd, timeout=15):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except Exception as e:  # noqa: BLE001
        return -1, "", str(e)


def services_status():
    out = []
    for name in KNOWN_SERVICES:
        rc, o, _ = run(["systemctl", "is-active", name])
        out.append({"name": name, "active": o.strip() or "unknown"})
    for name in ["cloudflared-sofi.service", "sofi-dashboard.service"]:
        rc, o, _ = run(["systemctl", "--user", "is-active", name])
        out.append({"name": name, "active": o.strip() or "unknown"})
    return out


def parse_tunnels():
    tunnels = []
    for path in glob.glob(f"{HOME}/.cloudflared/*.yml"):
        data = None
        if yaml:
            try:
                with open(path) as fh:
                    data = yaml.safe_load(fh)
            except Exception:  # noqa: BLE001
                data = None
        if not isinstance(data, dict):
            continue
        name = data.get("tunnel", os.path.basename(path))
        routes = []
        for ing in data.get("ingress", []) or []:
            if not isinstance(ing, dict):
                continue
            h = ing.get("hostname")
            s = ing.get("service", "")
            if h:
                routes.append({"hostname": h, "service": s})
        tunnels.append({"tunnel": str(name), "routes": routes})
    return tunnels


_SSL_CTX = None
try:
    import ssl
    _SSL_CTX = ssl.create_default_context()
    _SSL_CTX.check_hostname = False
    _SSL_CTX.verify_mode = ssl.CERT_NONE
except Exception:  # noqa: BLE001
    pass


def check_url(url, timeout=6):
    req = urlreq.Request(url, method="GET", headers={"User-Agent": "status-page/1.0"})
    try:
        r = urlreq.urlopen(req, timeout=timeout, context=_SSL_CTX)
        return {"status": r.getcode(), "ok": True}
    except HTTPError as e:
        return {"status": e.code, "ok": e.code < 500}
    except (URLError, TimeoutError) as e:
        return {"status": 0, "ok": False, "error": str(getattr(e, "reason", e))[:80]}
    except Exception as e:  # noqa: BLE001
        return {"status": 0, "ok": False, "error": str(e)[:80]}


def parse_site_files():
    """يستخرج (hostname, root-or-upstream) من ملفات Caddy لهذا المشروع فقط."""
    sites = []
    host_re = re.compile(r'^([a-z0-9][a-z0-9.\-]*\.[a-z]{2,}(?::\d+)?)\s*(?:,\s*([a-z0-9][a-z0-9.\-]*\.[a-z]{2,}(?::\d+)?))*\s*\{', re.I)
    for path in SITE_FILES:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except Exception:  # noqa: BLE001
            continue
        hosts_in_file = re.findall(r'([a-z0-9][a-z0-9.\-]*\.[a-z]{2,}):80', text)
        root = None
        m = re.search(r'root\s+\*\s+(\S+)', text)
        if m:
            root = m.group(1)
        upstream = None
        m2 = re.search(r'reverse_proxy\s+(\S+)', text)
        if m2:
            upstream = m2.group(1)
        for h in sorted(set(hosts_in_file)):
            sites.append({
                "host": h,
                "file": os.path.basename(path),
                "root": root,
                "upstream": upstream,
            })
    return sites


def build():
    services = services_status()
    tunnels = parse_tunnels()
    sites = parse_site_files()

    public_endpoints = []
    seen = set()
    for t in tunnels:
        for r in t["routes"]:
            h = r["hostname"]
            if h in seen or h.startswith("*"):
                continue
            seen.add(h)
            public_endpoints.append({"hostname": h, "tunnel": t["tunnel"]})

    with ThreadPoolExecutor(max_workers=8) as ex:
        checked = list(ex.map(
            lambda e: {**e, **check_url(f"https://{e['hostname']}/")},
            public_endpoints,
        ))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    def svc_rows():
        rows = []
        for s in services:
            cls = "good" if s["active"] == "active" else ("idle" if s["active"] in ("inactive", "unknown") else "bad")
            rows.append(f'<tr><td class="mono">{esc(s["name"])}</td><td><span class="chip {cls}">{esc(s["active"])}</span></td></tr>')
        return "\n".join(rows)

    def link_rows():
        rows = []
        for e in checked:
            cls = "good" if e.get("ok") else "bad"
            status = e.get("status", 0)
            label = f"HTTP {status}" if status else "لا استجابة"
            rows.append(
                f'<tr><td><a class="url" href="https://{esc(e["hostname"])}/" target="_blank" rel="noopener">{esc(e["hostname"])}</a></td>'
                f'<td class="mono">{esc(e["tunnel"])}</td>'
                f'<td><span class="chip {cls}">{esc(label)}</span></td></tr>'
            )
        return "\n".join(rows) or '<tr><td colspan="3" class="muted">لا يوجد</td></tr>'

    def site_rows():
        rows = []
        for s in sites:
            target = s["upstream"] or s["root"] or "—"
            rows.append(
                f'<tr><td class="mono">{esc(s["host"])}</td>'
                f'<td class="mono small">{esc(s["file"])}</td>'
                f'<td class="mono small">{esc(target)}</td></tr>'
            )
        return "\n".join(rows) or '<tr><td colspan="3" class="muted">لا يوجد</td></tr>'

    html = PAGE_TEMPLATE.format(
        generated_at=now,
        service_rows=svc_rows(),
        link_rows=link_rows(),
        site_rows=site_rows(),
        service_count=len(services),
        link_count=len(checked),
        site_count=len(sites),
    )

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {OUT_FILE} ({len(html)} bytes)")


def esc(s):
    return (str(s) if s is not None else "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


PAGE_TEMPLATE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>SHAMEL — لوحة الحالة</title>
<style>
:root{{
  --bg:#0c1017; --card:#141b26; --ink:#e6edf6; --muted:#8496ad; --border:#232d3c;
  --accent:#2dd4bf; --good:#3fb950; --good-bg:#132a19; --bad:#f85149; --bad-bg:#2c1516;
  --idle:#8b98a8; --idle-bg:#1a2230; --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Noto Kufi Arabic",sans-serif;
}}
@media (prefers-color-scheme:light){{
  :root{{--bg:#f5f7fa;--card:#fff;--ink:#182231;--muted:#5c6b82;--border:#e3e8ef;
    --accent:#0d9488;--good:#1a7f37;--good-bg:#e8f6ec;--bad:#cf222e;--bad-bg:#fbe9ea;
    --idle:#57606a;--idle-bg:#eef1f4;}}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:14px;line-height:1.6}}
.wrap{{max-width:1000px;margin:0 auto;padding:32px 20px 60px}}
header{{margin-bottom:24px}}
h1{{font-size:22px;margin:0 0 4px}}
.sub{{color:var(--muted);font-size:12.5px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin:20px 0 28px}}
.tile{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px}}
.tile .n{{font-family:var(--mono);font-size:26px;font-weight:700}}
.tile .l{{color:var(--muted);font-size:11.5px;margin-top:4px;text-transform:uppercase;letter-spacing:.04em}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:14px;overflow:hidden;margin-bottom:20px}}
.card>.hd{{padding:14px 18px;border-bottom:1px solid var(--border);font-weight:700;font-size:14px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th{{text-align:start;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.04em;padding:10px 18px;border-bottom:1px solid var(--border)}}
td{{padding:10px 18px;border-bottom:1px solid var(--border);vertical-align:middle}}
tr:last-child td{{border-bottom:none}}
.mono{{font-family:var(--mono);direction:ltr;unicode-bidi:plaintext}}
.small{{font-size:11.5px;color:var(--muted)}}
.muted{{color:var(--muted)}}
.url{{color:var(--accent);text-decoration:none;font-family:var(--mono);direction:ltr;unicode-bidi:plaintext}}
.url:hover{{text-decoration:underline}}
.chip{{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px;font-family:var(--mono)}}
.chip::before{{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}}
.chip.good{{color:var(--good);background:var(--good-bg)}}
.chip.bad{{color:var(--bad);background:var(--bad-bg)}}
.chip.idle{{color:var(--idle);background:var(--idle-bg)}}
footer{{color:var(--muted);font-size:11.5px;text-align:center;margin-top:20px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>SHAMEL — لوحة الحالة</h1>
    <div class="sub">آخر تحديث: {generated_at} · تُعاد هذه الصفحة تلقائياً كل بضع دقائق (قراءة فقط)</div>
  </header>

  <div class="tiles">
    <div class="tile"><div class="n">{service_count}</div><div class="l">خدمات مراقَبة</div></div>
    <div class="tile"><div class="n">{link_count}</div><div class="l">روابط عامة</div></div>
    <div class="tile"><div class="n">{site_count}</div><div class="l">مواقع Caddy</div></div>
  </div>

  <div class="card">
    <div class="hd">الروابط العامة</div>
    <table><thead><tr><th>الرابط</th><th>النفق</th><th>الحالة</th></tr></thead>
    <tbody>{link_rows}</tbody></table>
  </div>

  <div class="card">
    <div class="hd">الخدمات</div>
    <table><thead><tr><th>الخدمة</th><th>الحالة</th></tr></thead>
    <tbody>{service_rows}</tbody></table>
  </div>

  <div class="card">
    <div class="hd">مسارات Caddy</div>
    <table><thead><tr><th>الدومين</th><th>الملف</th><th>الوجهة</th></tr></thead>
    <tbody>{site_rows}</tbody></table>
  </div>

  <footer>صفحة للقراءة فقط — بدون أي تحكم أو صلاحيات كتابة</footer>
</div>
</body>
</html>
"""

if __name__ == "__main__":
    build()
