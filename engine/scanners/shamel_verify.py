"""shamel_verify — verify project structure compliance.
Checks that a project matches SHAMEL scaffolding standards."""
from pathlib import Path

def verify(prj_path: str | Path) -> dict:
    root = Path(prj_path).resolve()
    checks = {
        "has_git": (root / ".git").exists() or (root / ".git").is_dir(),
        "has_context": (root / "_context").is_dir(),
        "has_claude": (root / ".claude").is_dir(),
        "has_state": (root / "_context" / "STATE.md").exists(),
    }
    checks["pass"] = all(checks.values())
    return checks

def main():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    import json
    print(json.dumps(verify(path)))

if __name__ == "__main__":
    main()
