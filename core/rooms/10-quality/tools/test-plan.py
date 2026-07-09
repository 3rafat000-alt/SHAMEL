#!/usr/bin/env python3
"""tool/qa/test-architect/test-plan.py — Generate test plan from architecture spec"""
import argparse, json, sys, os, re
from pathlib import Path

SOFI_ROOT = os.environ.get("SOFI_ROOT", os.path.expanduser("~/Desktop/Lorka"))

def parse_spec(path: str) -> list:
    features = []
    if not os.path.isfile(path):
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        for line in f:
            m = re.search(r'(GET|POST|PUT|DELETE|PATCH)\s+(\S+)', line)
            if m:
                features.append({"method": m.group(1), "endpoint": m.group(2)})
            m = re.search(r'(class|function|def)\s+(\w+)', line)
            if m:
                features.append({"type": m.group(1), "name": m.group(2)})
    return features

def gen_tests(features: list) -> list:
    tests = []
    for f in features:
        if "endpoint" in f:
            tests.append({
                "suite": "API",
                "test": f"test_{f['method'].lower()}_{f['endpoint'].strip('/').replace('/','_').replace('-','_')}",
                "type": "integration",
                "checks": ["status 200/401/403", "JSON body shape match", "auth enforced"]
            })
        elif "name" in f:
            tests.append({
                "suite": "Unit",
                "test": f"test_{f['name']}",
                "type": "unit",
                "checks": ["happy path", "error handling", "boundary values"]
            })
    return tests

def main():
    parser = argparse.ArgumentParser(description="Generate test plan from architecture spec")
    parser.add_argument("--spec", required=True, help="Path to architecture/API spec file")
    parser.add_argument("--output", default="", help="Output test plan file")
    parser.add_argument("--format", choices=["md","json"], default="md")
    args = parser.parse_args()

    features = parse_spec(args.spec)
    if not features:
        print("Warning: no features extracted from spec", file=sys.stderr)
    tests = gen_tests(features)

    if args.format == "json":
        out = json.dumps({"source": args.spec, "tests": tests}, indent=2)
    else:
        lines = [f"# Test Plan: {args.spec}", ""]
        for t in tests:
            lines.append(f"## {t['test']}")
            lines.append(f"- Suite: {t['suite']}")
            lines.append(f"- Type: {t['type']}")
            for c in t['checks']:
                lines.append(f"  - [ ] {c}")
            lines.append("")
        out = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(out)
        print(f"Test plan written to {args.output}")
    else:
        print(out)

if __name__ == "__main__":
    main()
