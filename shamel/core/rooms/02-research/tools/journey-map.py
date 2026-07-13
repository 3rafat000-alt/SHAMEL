#!/usr/bin/env python3
# tool/res/journey-architect/journey-map.py — Generate Mermaid journey map from CSV
import argparse, csv, sys
from pathlib import Path

SOFI_ROOT = Path(__file__).resolve().parents[3]


def csv_to_mermaid(csv_path, prj_id):
    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("Empty CSV", file=sys.stderr)
        sys.exit(1)

    # Detect columns
    cols = list(rows[0].keys())
    stage_col = next((c for c in cols if 'stage' in c.lower()), 'stage')
    goal_col = next((c for c in cols if 'goal' in c.lower()), cols[1] if len(cols) > 1 else 'goal')
    touch_col = next((c for c in cols if 'touch' in c.lower() or 'channel' in c.lower()), 'touchpoint')
    emotion_col = next((c for c in cols if 'emotion' in c.lower() or 'mood' in c.lower()), None)

    lines = [
        f"---",
        f"title: Journey Map — {prj_id}",
        f"---",
        f"journey",
        f"    title {prj_id} Customer Journey",
    ]

    for i, row in enumerate(rows):
        stage = row.get(stage_col, f"Step {i+1}")
        goal = row.get(goal_col, "")
        touch = row.get(touch_col, "")
        emo = row.get(emotion_col, "3") if emotion_col else "3"
        lines.append(f"    {touch}: {stage}: {goal}: {emo}")

    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Generate Mermaid journey map from CSV stages")
    ap.add_argument("csv_file", nargs="?", help="CSV with columns: stage,goal,touchpoint,emotion")
    ap.add_argument("--prj", "-p", required=True, help="Project ID")
    ap.add_argument("--output", "-o", help="Output .md file (default: docs/Journey_Map.md)")
    args = ap.parse_args()

    if not args.csv_file:
        # Interactive stdin mode
        print("Paste CSV (stage,goal,touchpoint,emotion) then Ctrl+D:", file=sys.stderr)
        csv_data = sys.stdin.read()
        tmp = Path("/tmp/journey_csv.txt")
        tmp.write_text(csv_data)
        args.csv_file = str(tmp)

    mermaid = csv_to_mermaid(args.csv_file, args.prj)

    output = args.output
    if not output:
        output = str(SOFI_ROOT / "projects" / args.prj / "docs" / "Journey_Map.md")

    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(f"```mermaid\n{mermaid}\n```\n")
    print(f"✓ Journey map written to {output}")


if __name__ == "__main__":
    main()
