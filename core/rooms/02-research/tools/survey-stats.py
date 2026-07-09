#!/usr/bin/env python3
# tool/res/data-researcher/survey-stats.py — Quantitative stats from CSV survey data
import argparse, csv, sys, json
from pathlib import Path
from collections import Counter


def analyze(csv_path):
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Empty CSV", file=sys.stderr)
        return

    cols = list(rows[0].keys())
    results = {}

    for col in cols:
        vals = [r[col].strip() for r in rows if r[col].strip()]
        if not vals:
            continue

        # Try numeric
        try:
            nums = [float(v) for v in vals]
            mean = sum(nums) / len(nums)
            sdev = (sum((x - mean) ** 2 for x in nums) / len(nums)) ** 0.5
            results[col] = {
                "type": "numeric",
                "count": len(nums),
                "mean": round(mean, 2),
                "min": round(min(nums), 2),
                "max": round(max(nums), 2),
                "stddev": round(sdev, 2),
            }
        except ValueError:
            # Categorical
            counter = Counter(vals)
            total = len(vals)
            dist = {k: {"count": v, "pct": round(v / total * 100, 1)}
                    for k, v in counter.most_common()}
            results[col] = {"type": "categorical", "total": total, "distribution": dist}

    return results


def main():
    ap = argparse.ArgumentParser(description="Quantitative survey stats from CSV")
    ap.add_argument("csv_file", nargs="?", help="CSV survey data file")
    ap.add_argument("--prj", "-p", help="Project ID (for output path)")
    ap.add_argument("--json", "-j", action="store_true", help="Output raw JSON")
    args = ap.parse_args()

    if not args.csv_file:
        print("Paste CSV data (with header row) then Ctrl+D:", file=sys.stderr)
        csv_data = sys.stdin.read()
        tmp = Path("/tmp/survey_data.csv")
        tmp.write_text(csv_data)
        args.csv_file = str(tmp)

    results = analyze(args.csv_file)
    if not results:
        print("No data analyzed", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    for col, info in results.items():
        print(f"\n{'='*50}")
        print(f"  {col} ({info['type']})")
        print(f"{'='*50}")
        if info['type'] == 'numeric':
            print(f"    n={info['count']}  mean={info['mean']}  "
                  f"min={info['min']}  max={info['max']}  sd={info['stddev']}")
        else:
            for val, dist in info['distribution'].items():
                bar = "█" * (dist['pct'] // 2)
                print(f"    {val:<30} {dist['count']:>4} ({dist['pct']:>5.1f}%) {bar}")

    # Output path
    if args.prj:
        out = Path(f"projects/{args.prj}/docs/survey-analysis.md")
        print(f"\n→ Wrote analysis to {out}")


if __name__ == "__main__":
    main()
