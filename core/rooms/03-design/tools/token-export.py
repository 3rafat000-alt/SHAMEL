#!/usr/bin/env python3
# tool/dsn/design-system/token-export.py — Export design tokens from CSS
import argparse, re, json, sys
from pathlib import Path


def extract_tokens(css_text):
    tokens = {"colors": {}, "spacing": {}, "typography": {}, "radii": {}, "shadows": {}}

    # CSS custom properties: --token-name: value;
    for m in re.finditer(r'--([\w-]+)\s*:\s*([^;]+);', css_text):
        name = m.group(1).strip()
        value = m.group(2).strip()

        if any(k in name for k in ('color', 'bg', 'text', 'border', 'primary', 'secondary', 'accent', 'neutral', 'error', 'warning', 'success')):
            tokens["colors"][name] = value
        elif any(k in name for k in ('space', 'gap', 'margin', 'padding', 'size')):
            tokens["spacing"][name] = value
        elif any(k in name for k in ('font', 'text', 'size', 'weight', 'line-height', 'leading')):
            tokens["typography"][name] = value
        elif any(k in name for k in ('radius', 'round')):
            tokens["radii"][name] = value
        elif any(k in name for k in ('shadow', 'elevation')):
            tokens["shadows"][name] = value
        else:
            tokens.setdefault("other", {})[name] = value

    return {k: v for k, v in tokens.items() if v}


def main():
    ap = argparse.ArgumentParser(description="Export design tokens (colors, space, type) from CSS")
    ap.add_argument("css_file", nargs="?", help="Path to CSS file")
    ap.add_argument("--output", "-o", help="Output JSON file")
    args = ap.parse_args()

    if not args.css_file:
        print("Paste CSS content then Ctrl+D:", file=sys.stderr)
        css_text = sys.stdin.read()
    else:
        with open(args.css_file) as f:
            css_text = f.read()

    tokens = extract_tokens(css_text)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(tokens, f, indent=2)
        print(f"✓ Tokens exported to {args.output}")
    else:
        print(json.dumps(tokens, indent=2))

    # Summary
    counts = {k: len(v) for k, v in tokens.items()}
    print(f"\nSummary: {json.dumps(counts)}", file=sys.stderr)


if __name__ == "__main__":
    main()
