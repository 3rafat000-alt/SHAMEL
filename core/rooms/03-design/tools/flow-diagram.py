#!/usr/bin/env python3
# tool/dsn/ux-architect/flow-diagram.py — Generate Mermaid flow diagram from CSV steps
import argparse, csv, sys
from pathlib import Path

SOFI_ROOT = Path(__file__).resolve().parents[3]


def csv_to_mermaid(csv_path, title="User Flow"):
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Empty CSV", file=sys.stderr)
        sys.exit(1)

    cols = list(rows[0].keys())
    id_col = next((c for c in cols if 'id' in c.lower() or 'step' in c.lower()), 'id')
    label_col = next((c for c in cols if 'label' in c.lower() or 'desc' in c.lower() or 'action' in c.lower()), cols[1])
    next_col = next((c for c in cols if 'next' in c.lower() or 'goto' in c.lower() or 'transition' in c.lower()), None)
    branch_col = next((c for c in cols if 'branch' in c.lower() or 'condition' in c.lower()), None)

    lines = [
        f"---",
        f"title: {title}",
        f"---",
        f"flowchart TD",
    ]

    for row in rows:
        sid = row.get(id_col, "").strip().replace(" ", "_")
        label = row.get(label_col, f"Step {sid}").strip().replace('"', "'")
        lines.append(f"    {sid}[\"{label}\"]")

        if next_col and row.get(next_col, "").strip():
            next_ids = row[next_col].strip().split(";")
            for nid in next_ids:
                nid = nid.strip()
                if nid and nid != sid:
                    if branch_col and row.get(branch_col, "").strip():
                        cond = row[branch_col].strip().replace('"', "'")
                        lines.append(f"    {sid}-->|{cond}| {nid}")
                    else:
                        lines.append(f"    {sid}-->{nid}")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Generate Mermaid flow diagram from CSV steps")
    ap.add_argument("csv_file", nargs="?", help="CSV with columns: id,label,next,branch")
    ap.add_argument("--prj", "-p", required=True, help="Project ID")
    ap.add_argument("--title", "-t", default="User Flow", help="Diagram title")
    ap.add_argument("--output", "-o", help="Output file path")
    args = ap.parse_args()

    if not args.csv_file:
        print("Paste CSV (id,label,next) then Ctrl+D:", file=sys.stderr)
        csv_data = sys.stdin.read()
        tmp = Path("/tmp/flow_csv.txt")
        tmp.write_text(csv_data)
        args.csv_file = str(tmp)

    mermaid = csv_to_mermaid(args.csv_file, args.title)

    output = args.output
    if not output:
        output = str(SOFI_ROOT / "projects" / args.prj / "docs" / f"flow-{args.title.replace(' ', '_')}.md")

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(f"```mermaid\n{mermaid}\n```\n")
    print(f"✓ Flow diagram written to {output}")


if __name__ == "__main__":
    main()
