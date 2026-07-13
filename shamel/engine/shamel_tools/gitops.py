"""
gitops — the git spine of the SOFI brain (see protocols/git-discipline.md).

Gives every agent collision-proof, multi-session git: orient (sync), isolate
(worktree), checkpoint (commit early/often with a traceable trailer), and verify
(git-check). All commits carry a `SOFI: <PRJ> · <TKT> · gate <N> · <role>` trailer
so a *later session* can reconstruct who did what under which ticket.

Only SAFE git is issued here (no reset --hard, no force-push, no history rewrite);
those stay blocked at the harness hook. Commits/branches = normal prose, never caveman.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

from . import paths, brain, tickets

# Conventional-commit type the message MUST start with (mirrors the hook + protocol §4).
CONVENTIONAL = re.compile(
    r"^(feat|fix|chore|docs|refactor|test|perf|ci|build|style|revert|wip)"
    r"(\([\w./-]+\))?!?: .+"
)
# Paths that must never enter history (defense-in-depth beyond .gitignore).
FORBIDDEN = re.compile(
    r"(^|/)(\.gstack/|_scratch/|__pycache__/)|"
    r"\.env(\.bak|\.vault|\.testing)?$|"
    r"(^|/)audit\.jsonl$|\.(pem|key|p12|pfx|keystore|jks)$"
)


class GitError(RuntimeError):
    pass


def _git(*args: str, check: bool = False) -> subprocess.CompletedProcess:
    """Framework-repo git (worktrees, gate merges/tags) — runs in the SOFI root."""
    root = paths.repo_root()
    cp = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if check and cp.returncode != 0:
        raise GitError(f"git {' '.join(args)} → {cp.stderr.strip() or cp.stdout.strip()}")
    return cp


def _pg(prj: str, *args: str, check: bool = False) -> subprocess.CompletedProcess:
    """Project-repo git — runs in the project's OWN repo where the brain lives
    (single-root doctrine). Used by checkpoint/git_check, which persist _context."""
    cp = subprocess.run(["git", *args], cwd=paths.project_repo(prj),
                        capture_output=True, text=True)
    if check and cp.returncode != 0:
        raise GitError(f"git {' '.join(args)} → {cp.stderr.strip() or cp.stdout.strip()}")
    return cp


def branch_for(prj: str) -> str:
    return f"prj/{prj}"


def _has_remote() -> bool:
    return bool(_git("remote").stdout.strip())


def _branch_exists(name: str) -> bool:
    return _git("rev-parse", "--verify", "--quiet", name).returncode == 0


def _current_branch() -> str:
    return _git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()


def _short_head() -> str:
    return _git("rev-parse", "--short", "HEAD").stdout.strip()


def _dirty() -> bool:
    return bool(_git("status", "--porcelain").stdout.strip())


def _trailer(prj: str) -> str:
    """SOFI: <PRJ> · <TKT> · gate <N> · <role> — built from the open ticket + STATE."""
    st = brain.read_state(prj)
    t = tickets.next_open(prj)
    tkt = t.id if t else "—"
    gate = (t.gate if t else st.get("gate", "?"))
    role = st.get("active", "?")
    return f"SOFI: {prj} · {tkt} · gate {gate} · {role}"


# ── ORIENT ────────────────────────────────────────────────────────────────
def sync(prj: str, push: bool = False) -> int:
    branch = branch_for(prj)
    if _has_remote():
        _git("fetch", "--quiet")
    cur = _current_branch()
    if cur != branch:
        if _dirty():
            print(f"✗ working tree dirty on '{cur}' — checkpoint before switching to {branch}")
            return 2
        if _branch_exists(branch):
            _git("switch", branch, check=True)
        else:
            _git("switch", "-c", branch, check=True)
            print(f"✓ created branch {branch}")
    print(f"━━ sync {prj} ━━  branch={branch}  head={_short_head()}")
    if _has_remote():
        ahead_behind = _git("rev-list", "--left-right", "--count", f"origin/{branch}...{branch}")
        if ahead_behind.returncode == 0 and ahead_behind.stdout.strip():
            behind, ahead = ahead_behind.stdout.split()
            print(f"  vs origin/{branch}: {ahead} ahead, {behind} behind")
        if push:
            r = _git("push", "-u", "origin", branch)
            print("  push: " + ("✓" if r.returncode == 0 else "✗ " + r.stderr.strip()))
    print("  recent checkpoints (who did what):")
    log = _git("log", "--oneline", "-8")
    print("\n".join("    " + l for l in log.stdout.splitlines()) or "    (none yet)")
    return 0


# ── CHECKPOINT ──────────────────────────────────────────────────────────────
def checkpoint(prj: str, message: str) -> int:
    if not CONVENTIONAL.match(message):
        print("✗ commit message must start with a type: "
              "feat|fix|chore|docs|refactor|test|perf|ci|build|style|revert|wip\n"
              f"  got: {message!r}")
        return 2
    # Brain persistence runs in the project's OWN repo (single-root doctrine):
    # _context (+ docs) is committed on the app repo's own branch. App source is
    # committed by agents directly; checkpoint stays brain-scoped, no cross-PRJ bleed.
    repo = paths.project_repo(prj)
    targets = [d for d in ("_context", "docs") if (repo / d).is_dir()]
    if not targets:
        print(f"  no brain to checkpoint for {prj} (looked in {repo})")
        return 0
    _pg(prj, "add", "-A", "--", *targets)
    staged = [l for l in _pg(prj, "diff", "--cached", "--name-only").stdout.splitlines() if l]
    if not staged:
        print(f"  nothing to checkpoint for {prj} (brain clean)")
        return 0
    bad = [p for p in staged if FORBIDDEN.search(p)]
    if bad:
        print("✗ refusing to commit forbidden paths (secrets/scratch/cache):")
        print("\n".join("    " + b for b in bad))
        _pg(prj, "reset", "--quiet", "HEAD", "--", *bad)  # unstage them, never --hard
        return 3
    r = _pg(prj, "commit", "-m", message, "-m", _trailer(prj))
    if r.returncode != 0:
        print("✗ commit failed: " + (r.stderr.strip() or r.stdout.strip()))
        return 2
    sha = _pg(prj, "rev-parse", "--short", "HEAD").stdout.strip()
    branch = _pg(prj, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    try:
        brain.update_state(prj, {"branch": branch, "head_sha": sha})
    except FileNotFoundError:
        pass
    print(f"✓ checkpoint {sha} on {branch} — {len(staged)} brain file(s) in {repo.name}")
    print(f"  STATE.head_sha → {sha} (next session resumes here)")
    return 0


# ── CLAIM / RELEASE (soft lock for shared paths) ─────────────────────────────
def _locks_file(prj: str) -> Path:
    return paths.context_dir(prj) / "LOCKS.md"


def claim(prj: str, path_glob: str, release_it: bool = False) -> int:
    role = brain.read_state(prj).get("active", "unknown-role")
    lf = _locks_file(prj)
    lines = lf.read_text(encoding="utf-8").splitlines() if lf.exists() else [
        f"# LOCKS — {prj}  (path claims; check before editing shared paths)", ""]
    entry_pat = re.compile(r"^- `(.+?)` → ")
    kept = [l for l in lines if not (entry_pat.match(l) and entry_pat.match(l).group(1) == path_glob)]
    if release_it:
        lf.write_text("\n".join(kept) + "\n", encoding="utf-8")
        print(f"✓ released `{path_glob}`")
        return 0
    held = next((l for l in lines if entry_pat.match(l) and entry_pat.match(l).group(1) == path_glob), None)
    if held and f"by {role}" not in held:
        print(f"✗ `{path_glob}` already claimed → {held.split('→',1)[1].strip()}")
        print("  use a worktree or serialize via the lead (git-discipline §5).")
        return 2
    kept.append(f"- `{path_glob}` → claimed by {role} (head {_short_head()})")
    lf.write_text("\n".join(kept) + "\n", encoding="utf-8")
    print(f"✓ claimed `{path_glob}` for {role}")
    return 0


# ── WORKTREE per squad ───────────────────────────────────────────────────────
def worktree(prj: str, gate: str, squad: str) -> int:
    base = branch_for(prj)
    if not _branch_exists(base):
        print(f"✗ no {base} yet — run `shamel sync {prj}` to create the project branch first")
        return 2
    wt = f"worktrees/{prj}-gate{gate}-{squad}"
    wb = f"wt/{prj}-gate{gate}-{squad}"
    if (paths.repo_root() / wt).exists():
        print(f"  worktree already exists: {wt}")
        return 0
    r = _git("worktree", "add", "-b", wb, wt, base)
    if r.returncode != 0:
        print("✗ " + (r.stderr.strip() or r.stdout.strip()))
        return 2
    print(f"✓ worktree {wt} (branch {wb} off {base})")
    print(f"  squad '{squad}' works here in isolation; merge at gate close:")
    print(f"  → shamel gate-merge {prj} {gate} {squad}")
    return 0


def gate_merge(prj: str, gate: str, squad: str) -> int:
    base = branch_for(prj)
    wb = f"wt/{prj}-gate{gate}-{squad}"
    wt = f"worktrees/{prj}-gate{gate}-{squad}"
    if _current_branch() != base:
        _git("switch", base, check=True)
    r = _git("merge", "--no-ff", wb, "-m", f"chore(merge): gate {gate} {squad} → {base}\n\n{_trailer(prj)}")
    if r.returncode != 0:
        print("✗ merge conflict — resolve forward (never reset --hard):\n  " + r.stdout.strip())
        return 2
    _git("worktree", "remove", "--force", wt)
    _git("branch", "-d", wb)
    print(f"✓ merged {squad} into {base}; worktree removed")
    return 0


def gate_tag(prj: str, gate: str) -> int:
    tag = f"{prj}-gate{gate}-done"
    r = _git("tag", tag)
    if r.returncode != 0:
        print("✗ " + (r.stderr.strip() or "tag exists"))
        return 2
    print(f"✓ tagged {tag} (immutable restore point for gate {gate})")
    return 0


# ── VERIFY (gates the pipeline) ──────────────────────────────────────────────
def git_check(prj: str) -> int:
    print(f"━━ git-check {prj} ━━")
    ok = True
    repo = paths.project_repo(prj)
    branch = _pg(prj, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    print(f"  repo      : {repo}")
    print(f"  branch    : {branch}")
    if _pg(prj, "status", "--porcelain", "--", "_context").stdout.strip():
        print("  brain     : ✗ uncommitted _context changes — checkpoint before handoff"); ok = False
    else:
        print("  brain     : ✓ _context clean")
    tracked = _pg(prj, "ls-files").stdout.splitlines()
    leaks = [f for f in tracked if FORBIDDEN.search(f)]
    if leaks:
        print(f"  leaks     : ✗ {len(leaks)} forbidden file(s) tracked: " + ", ".join(leaks[:5])); ok = False
    else:
        print("  leaks     : ✓ no secrets/scratch/cache tracked")
    # recent project commits must carry the SOFI trailer
    log = _pg(prj, "log", "-10", "--format=%H%x1f%s%x1f%b").stdout.strip().split("\n\n")
    missing = 0
    for entry in log:
        if not entry.strip():
            continue
        parts = entry.split("\x1f")
        subj = parts[1] if len(parts) > 1 else ""
        body = parts[2] if len(parts) > 2 else ""
        if not CONVENTIONAL.match(subj):
            missing += 1
        elif "SOFI:" not in body and "SOFI:" not in subj:
            missing += 1
    if missing:
        print(f"  messages  : ⚠ {missing}/10 recent commits miss type or SOFI: trailer")
    else:
        print("  messages  : ✓ recent commits well-formed + traceable")
    print(f"  VERDICT   : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1
