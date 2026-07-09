#!/usr/bin/env python3
"""tool/arc/system-architect/component-diagram.py — Generate Mermaid component diagram from JSON input"""
import argparse, json, sys, pathlib

def gen_diagram(components, title="System Architecture"):
    lines = [f"---\ntitle: {title}\n---\n", "graph TB"]
    for c in components:
        cid = c["id"].replace("-", "_").replace(" ", "_")
        lines.append(f'  {cid}["{c.get("label", c["id"])}"]')
        lines.append(f'  style {cid} fill:{c.get("color", "#e1f5fe")},stroke:#333')
    for c in components:
        cid = c["id"].replace("-", "_").replace(" ", "_")
        for dep in c.get("deps", []):
            did = dep.replace("-", "_").replace(" ", "_")
            lines.append(f"  {cid} --> {did}")
    for c in components:
        for sub in c.get("subcomponents", []):
            sid = sub["id"].replace("-", "_").replace(" ", "_")
            cid = c["id"].replace("-", "_").replace(" ", "_")
            lines.append(f"  subgraph {cid}_group [{c.get('label', c['id'])}]")
            lines.append(f'    {sid}["{sub.get("label", sub["id"])}"]')
            lines.append("  end")
    return "\n".join(lines)

def main():
    ap = argparse.ArgumentParser(description="Generate Mermaid component diagram from JSON")
    ap.add_argument("input", nargs="?", help="JSON file (reads stdin if omitted)", default="-")
    ap.add_argument("--title", default="System Architecture")
    ap.add_argument("--output", "-o", help="Output file (stdout if omitted)")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else pathlib.Path(args.input).read_text()
    data = json.loads(raw)
    components = data if isinstance(data, list) else data.get("components", [])
    mermaid = gen_diagram(components, args.title)

    if args.output:
        pathlib.Path(args.output).write_text(mermaid)
        print(f"Written: {args.output}")
    else:
        print(mermaid)

if __name__ == "__main__":
    main()
