#!/usr/bin/env python3
# tool/gtw/dispatcher/work-order.py — Convert HANDOFFS ticket → RCCF block
import argparse, re, sys
from pathlib import Path

SOFI_ROOT = Path(__file__).resolve().parents[3]

def parse_handoffs(prj_id):
    handoffs = SOFI_ROOT / "projects" / prj_id / "_context" / "HANDOFFS.md"
    state = SOFI_ROOT / "projects" / prj_id / "_context" / "STATE.md"
    if not handoffs.exists():
        print(f"✗ HANDOFFS.md not found for {prj_id}", file=sys.stderr)
        sys.exit(1)
    tickets = []
    with open(handoffs) as f:
        content = f.read()
    # Extract ticket blocks: [TKT-xxxx] Description
    for m in re.finditer(r'\[(TKT-\d+)\]\s*(.+?)(?:\n|$)', content):
        tickets.append({"id": m.group(1), "desc": m.group(2).strip()})
    gate = "?"
    if state.exists():
        with open(state) as f:
            for line in f:
                if line.startswith("gate"):
                    gate = line.split(":")[-1].strip()
                    break
    return tickets, gate

def build_rccf(ticket, prj, gate):
    role = input(f"🎭 Role for {ticket['id']}? [default: generic-agent]: ") or "generic-agent"
    return f"""🎭 Role     You are {role}.
            Model: claude (session model)

📂 Context  Project {prj} · Gate {gate}.
            Read: projects/{prj}/_context/STATE.md · HANDOFFS.md · CONTEXT.md.

🎯 Command  {ticket['desc']}
            In-bounds: per ticket scope.
            Out-of-bounds: schema, other endpoints, other projects.

📐 Format   Path: projects/{prj}/
            Evidence: paste command output in handoff.
            Handoff: → next agent per HANDOFFS.md.
"""

def main():
    ap = argparse.ArgumentParser(description="Convert HANDOFFS ticket → RCCF work order")
    ap.add_argument("PRJ_ID", help="Project ID")
    ap.add_argument("--ticket", "-t", help="Specific ticket ID (TKT-xxxx)")
    args = ap.parse_args()

    tickets, gate = parse_handoffs(args.PRJ_ID)
    if not tickets:
        print(f"No tickets found in {args.PRJ_ID} HANDOFFS.md")
        sys.exit(0)

    for t in tickets:
        if args.ticket and t["id"] != args.ticket:
            continue
        print(f"\n{'='*60}")
        print(f"{t['id']}: {t['desc']}")
        print(f"{'='*60}")
        rccf = build_rccf(t, args.PRJ_ID, gate)
        print(rccf)

if __name__ == "__main__":
    main()
