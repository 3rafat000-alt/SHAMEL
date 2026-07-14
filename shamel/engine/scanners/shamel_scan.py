"""shamel_scan — project structure scanner.
Counts models, controllers, migrations, routes for brain facts generation."""
import os
from pathlib import Path

SCAN_PATTERNS = {
    "models": ["*.php", "*.py", "*.dart", "*.ts", "*.js"],
    "controllers": ["*Controller.php", "*Controller.py", "*Controller.dart", "*Controller.ts"],
    "migrations": ["*_create_*", "*_add_*", "*_modify_*", "*_drop_*"],
}

def scan(prj_path: str | Path) -> dict:
    """Scan a project directory and return counts."""
    result = {"models": 0, "controllers": 0, "migrations": 0, "routes": 0}
    root = Path(prj_path).resolve()
    if not root.is_dir():
        return result
    for f in root.rglob("*"):
        if f.is_file() and ".git" not in f.parts and "vendor" not in f.parts and "node_modules" not in f.parts:
            name = f.name
            if name.endswith("Controller.php") or name.endswith("Controller.py"):
                result["controllers"] += 1
            if name.endswith(".php") or name.endswith(".py") or name.endswith(".dart"):
                result["models"] += 1
            if "migration" in f.parts or "migrations" in f.parts:
                result["migrations"] += 1
    return result

def main():
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    import json
    print(json.dumps(scan(path)))

if __name__ == "__main__":
    main()
