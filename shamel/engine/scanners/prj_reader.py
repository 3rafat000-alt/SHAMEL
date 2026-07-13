#!/usr/bin/env python3
"""prj_reader — token-economical project reader.

Reads a large project (e.g. PRJ-SAKK) without dumping full file contents
into an LLM context window. Five modes, cheapest first:

  tree     structural map: dirs + file counts/sizes (noise pruned)
  index    flat file inventory: path, lines, size (capped)
  outline  signature-level summary of a file/glob (classes, functions,
           routes) — ~10-30x smaller than the raw file
  search   grep wrapper with bounded context + result cap
  read     chunked file read (explicit line range, hard cap on lines)
  stats    rough token-cost estimate: raw vs outline, per top-level dir

Usage:
  python3 prj_reader.py tree <root> [--depth N]
  python3 prj_reader.py index <root> [--ext php,dart] [--limit N]
  python3 prj_reader.py outline <root> "<glob>" [--limit N]
  python3 prj_reader.py search <root> "<pattern>" [--glob GLOB] [--context N] [--max-results N]
  python3 prj_reader.py read <file> [--start N] [--end N] [--max-lines N]
  python3 prj_reader.py stats <root>

No third-party deps — stdlib only, so it runs anywhere Python 3.10+ runs.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from pathlib import Path

NOISE_DIRS = {
    ".git", "vendor", "node_modules", "build", ".dart_tool", ".gradle",
    ".kotlin", "__pycache__", "dist", ".next", ".idea", ".vscode",
    "bootstrap", "storage", ".gstack", ".worktrees", ".cache",
}
# dirs pruned only when they appear as *exactly* this path segment under
# a known noise root, so we don't accidentally nuke e.g. app/Support
NOISE_EXACT_PATHS = {"backend/bootstrap/cache", "backend/storage"}

SOURCE_EXTS = {
    ".php", ".dart", ".py", ".js", ".ts", ".jsx", ".tsx", ".blade.php",
    ".vue", ".go", ".rb", ".java", ".kt",
}


def is_noise_dir(name: str) -> bool:
    return name in NOISE_DIRS


def iter_files(root: Path, exts: set[str] | None = None):
    root = root.resolve()
    for dirpath, dirnames, filenames in _walk_pruned(root):
        for fn in filenames:
            p = Path(dirpath) / fn
            if exts is not None:
                suffix = "".join(p.suffixes[-2:]) if p.name.endswith(".blade.php") else p.suffix
                if suffix not in exts:
                    continue
            yield p


def _walk_pruned(root: Path):
    import os
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not is_noise_dir(d)]
        yield dirpath, dirnames, filenames


# ---------------------------------------------------------------- tree ----

def cmd_tree(root: Path, depth: int) -> dict:
    root = root.resolve()

    def walk(d: Path, level: int) -> dict:
        node = {"dir": d.name, "files": 0, "size": 0, "children": []}
        try:
            entries = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name))
        except PermissionError:
            return node
        for e in entries:
            if e.is_dir():
                if is_noise_dir(e.name):
                    continue
                if level < depth:
                    node["children"].append(walk(e, level + 1))
                else:
                    # still count files below, just don't recurse further
                    sub_files = sub_size = 0
                    for f in iter_files(e):
                        sub_files += 1
                        try:
                            sub_size += f.stat().st_size
                        except OSError:
                            pass
                    node["children"].append({
                        "dir": e.name + "/ (collapsed)", "files": sub_files,
                        "size": sub_size, "children": [],
                    })
            else:
                node["files"] += 1
                try:
                    node["size"] += e.stat().st_size
                except OSError:
                    pass
        for c in node["children"]:
            node["files"] += c["files"]
            node["size"] += c["size"]
        return node

    return walk(root, 0)


def print_tree(node: dict, prefix: str = ""):
    def human(n):
        for unit in ("B", "K", "M", "G"):
            if n < 1024:
                return f"{n:.0f}{unit}"
            n /= 1024
        return f"{n:.0f}T"

    print(f"{prefix}{node['dir']}  ({node['files']} files, {human(node['size'])})")
    for c in node["children"]:
        print_tree(c, prefix + "  ")


# --------------------------------------------------------------- index ----

def cmd_index(root: Path, exts: set[str] | None, limit: int):
    root = root.resolve()
    rows = []
    for f in iter_files(root, exts):
        try:
            text = f.read_text(errors="ignore")
            lines = text.count("\n") + 1
            size = len(text.encode("utf-8", "ignore"))
        except OSError:
            continue
        rows.append((str(f.relative_to(root)), lines, size))
    rows.sort(key=lambda r: -r[1])
    total = len(rows)
    for path, lines, size in rows[:limit]:
        print(f"{lines:>6}  {size:>8}B  {path}")
    if total > limit:
        print(f"... {total - limit} more files omitted (raise --limit)")
    print(f"\n{total} files total")


# ------------------------------------------------------------- outline ----

# Lightweight regex signature extractors. Not full parsers — good enough to
# map "what's in this file" without reading the body.

def outline_php(text: str) -> list[str]:
    out = []
    for m in re.finditer(r'^\s*namespace\s+([\w\\]+);', text, re.M):
        out.append(f"namespace {m.group(1)}")
    for m in re.finditer(
        r'^\s*(?:abstract\s+|final\s+)?(class|interface|trait|enum)\s+(\w+)'
        r'(?:\s+extends\s+([\w\\]+))?(?:\s+implements\s+([\w\\,\s]+))?',
        text, re.M,
    ):
        kind, name, extends, implements = m.groups()
        line = f"{kind} {name}"
        if extends:
            line += f" extends {extends}"
        if implements:
            line += f" implements {implements.strip()}"
        out.append(line)
    for m in re.finditer(
        r'^\s*(?:public|protected|private)\s+(?:static\s+)?function\s+(\w+)\s*\(([^)]*)\)'
        r'(?:\s*:\s*([\w\\|? ]+))?',
        text, re.M,
    ):
        name, params, ret = m.groups()
        params = re.sub(r'\s+', ' ', params).strip()
        sig = f"  fn {name}({params})"
        if ret:
            sig += f": {ret.strip()}"
        out.append(sig)
    for m in re.finditer(r"Route::(get|post|put|patch|delete|any|resource)\(\s*['\"]([^'\"]+)['\"]", text):
        out.append(f"route {m.group(1).upper()} {m.group(2)}")
    return out


def outline_dart(text: str) -> list[str]:
    out = []
    for m in re.finditer(
        r'^\s*(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+with\s+([\w,\s]+))?(?:\s+implements\s+([\w,\s]+))?',
        text, re.M,
    ):
        name, extends, mixins, impl = m.groups()
        line = f"class {name}"
        if extends:
            line += f" extends {extends}"
        if mixins:
            line += f" with {mixins.strip()}"
        if impl:
            line += f" implements {impl.strip()}"
        out.append(line)
    for m in re.finditer(
        r'^\s{0,4}(?:@override\s+)?(?:static\s+)?(?:Future<[\w<>, ]+>|void|[\w<>?,\s]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:async\s*)?\{',
        text, re.M,
    ):
        name, params = m.groups()
        if name in {"if", "for", "while", "switch", "catch"}:
            continue
        params = re.sub(r'\s+', ' ', params).strip()
        out.append(f"  fn {name}({params[:80]})")
    return out


def outline_generic(text: str) -> list[str]:
    out = []
    for m in re.finditer(r'^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+(\w+)\s*\(', text, re.M):
        out.append(f"  fn {m.group(1)}(...)")
    for m in re.finditer(r'^\s*(?:export\s+)?class\s+(\w+)', text, re.M):
        out.append(f"class {m.group(1)}")
    for m in re.finditer(r'^\s*def\s+(\w+)\s*\(([^)]*)\)', text, re.M):
        out.append(f"  fn {m.group(1)}({m.group(2)[:80]})")
    for m in re.finditer(r'^\s*class\s+(\w+)', text, re.M):
        out.append(f"class {m.group(1)}")
    return out


def outline_file(path: Path) -> list[str]:
    try:
        text = path.read_text(errors="ignore")
    except OSError:
        return []
    if path.name.endswith(".blade.php"):
        # templates: no real signatures, just report @section/@include hooks
        out = []
        for m in re.finditer(r"@(section|include|extends|component)\(['\"]([^'\"]+)", text):
            out.append(f"  @{m.group(1)} {m.group(2)}")
        return out
    if path.suffix == ".php":
        return outline_php(text)
    if path.suffix == ".dart":
        return outline_dart(text)
    return outline_generic(text)


def cmd_outline(root: Path, pattern: str, limit: int):
    root = root.resolve()
    matched = []
    for f in iter_files(root):
        rel = str(f.relative_to(root))
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(f.name, pattern):
            matched.append(f)
    matched.sort()
    shown = 0
    for f in matched:
        if shown >= limit:
            print(f"... {len(matched) - shown} more files matched, omitted (raise --limit)")
            break
        sig = outline_file(f)
        if not sig:
            continue
        print(f"\n### {f.relative_to(root)}")
        for line in sig:
            print(line)
        shown += 1
    if shown == 0:
        print(f"no files matched pattern: {pattern}")


# -------------------------------------------------------------- search ----

def cmd_search(root: Path, pattern: str, glob: str | None, context: int, max_results: int):
    root = root.resolve()
    rx = re.compile(pattern)
    hits = 0
    for f in iter_files(root):
        if glob and not fnmatch.fnmatch(str(f.relative_to(root)), glob):
            continue
        try:
            lines = f.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if rx.search(line):
                hits += 1
                if hits > max_results:
                    print(f"... stopped at {max_results} results (raise --max-results)")
                    return
                lo, hi = max(0, i - context), min(len(lines), i + context + 1)
                print(f"\n{f.relative_to(root)}:{i + 1}")
                for j in range(lo, hi):
                    marker = ">" if j == i else " "
                    print(f"{marker}{j + 1:>5}  {lines[j]}")
    if hits == 0:
        print("no matches")
    else:
        print(f"\n{hits} match(es)")


# ---------------------------------------------------------------- read ----

def cmd_read(path: Path, start: int | None, end: int | None, max_lines: int):
    lines = path.read_text(errors="ignore").splitlines()
    total = len(lines)
    if start is None:
        start = 1
    if end is None:
        end = min(total, start - 1 + max_lines)
    if end - start + 1 > max_lines:
        end = start - 1 + max_lines
        capped = True
    else:
        capped = False
    for i in range(start, min(end, total) + 1):
        print(f"{i:>6}  {lines[i - 1]}")
    if capped or end < total:
        print(f"... file has {total} lines total, showing {start}-{min(end, total)}."
              f" Use --start/--end to page further.")


# --------------------------------------------------------------- stats ----

def cmd_stats(root: Path):
    root = root.resolve()
    areas: dict[str, dict] = {}
    for f in iter_files(root):
        rel = f.relative_to(root)
        area = rel.parts[0] if rel.parts else "."
        a = areas.setdefault(area, {"files": 0, "raw_chars": 0, "outline_chars": 0})
        try:
            text = f.read_text(errors="ignore")
        except OSError:
            continue
        a["files"] += 1
        a["raw_chars"] += len(text)
        a["outline_chars"] += sum(len(l) + 1 for l in outline_file(f))

    print(f"{'area':<20}{'files':>8}{'raw~tok':>12}{'outline~tok':>14}{'savings':>10}")
    tot_raw = tot_out = 0
    for area, a in sorted(areas.items(), key=lambda kv: -kv[1]["raw_chars"]):
        raw_tok = a["raw_chars"] // 4
        out_tok = a["outline_chars"] // 4
        tot_raw += raw_tok
        tot_out += out_tok
        pct = f"{(1 - out_tok / raw_tok) * 100:.0f}%" if raw_tok else "-"
        print(f"{area:<20}{a['files']:>8}{raw_tok:>12}{out_tok:>14}{pct:>10}")
    pct = f"{(1 - tot_out / tot_raw) * 100:.0f}%" if tot_raw else "-"
    print(f"{'TOTAL':<20}{'':>8}{tot_raw:>12}{tot_out:>14}{pct:>10}")
    print("\n(rough estimate: 1 token ~= 4 chars. 'outline' = signatures only, see `outline` mode)")


# ---------------------------------------------------------------- main ----

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("tree")
    p.add_argument("root")
    p.add_argument("--depth", type=int, default=3)

    p = sub.add_parser("index")
    p.add_argument("root")
    p.add_argument("--ext", default="", help="comma-separated extensions, e.g. php,dart")
    p.add_argument("--limit", type=int, default=100)

    p = sub.add_parser("outline")
    p.add_argument("root")
    p.add_argument("pattern")
    p.add_argument("--limit", type=int, default=200)

    p = sub.add_parser("search")
    p.add_argument("root")
    p.add_argument("pattern")
    p.add_argument("--glob", default=None)
    p.add_argument("--context", type=int, default=2)
    p.add_argument("--max-results", type=int, default=50)

    p = sub.add_parser("read")
    p.add_argument("file")
    p.add_argument("--start", type=int, default=None)
    p.add_argument("--end", type=int, default=None)
    p.add_argument("--max-lines", type=int, default=400)

    p = sub.add_parser("stats")
    p.add_argument("root")

    args = ap.parse_args()

    if args.cmd == "tree":
        print_tree(cmd_tree(Path(args.root), args.depth))
    elif args.cmd == "index":
        exts = {("." + e.strip().lstrip(".")) for e in args.ext.split(",") if e.strip()} or None
        cmd_index(Path(args.root), exts, args.limit)
    elif args.cmd == "outline":
        cmd_outline(Path(args.root), args.pattern, args.limit)
    elif args.cmd == "search":
        cmd_search(Path(args.root), args.pattern, args.glob, args.context, args.max_results)
    elif args.cmd == "read":
        cmd_read(Path(args.file), args.start, args.end, args.max_lines)
    elif args.cmd == "stats":
        cmd_stats(Path(args.root))


if __name__ == "__main__":
    sys.exit(main())
