"""
guard — enforce GOVERNANCE.md at runtime. The strict rules, in code.

Every script that writes, reaches the network, or gets promoted to the shared
library passes through here first. A violation raises GovernanceError — scripts
should let it propagate (fail loud, exit non-zero) rather than swallow it.
"""
from __future__ import annotations

import re
from pathlib import Path

from . import paths


class GovernanceError(Exception):
    """A script tried to step outside the rules. Fail loud."""


# ── Rule 2: network policy — only agents that hold Web tools may reach the net.
# Loaded from core/nexus/registry.yaml: an agent is web-holding when its tools
# list grants WebSearch/WebFetch, or it inherits the full session toolset
# (boardroom + Room Leads). Source of intent stays the .claude/agents frontmatter;
# the registry is the machine-checkable shadow of it. The literal set below is
# the offline fallback for a broken/absent registry only.
_NET_FALLBACK = frozenset({
    "brd-ceo", "brd-cso",
    "res-web-scout", "res-ux-researcher", "res-competitor-analyst",
    "res-data-researcher", "res-fact-checker",
    "str-product-strategist", "str-market-analyst", "str-monetization-strategist",
    "dsn-ui-designer", "dsn-design-system",
    "arc-system-architect", "arc-api-architect", "arc-integration-architect",
    "arc-infra-architect",
    "sec-threat-modeler", "sec-pentester", "sec-compliance-auditor",
    "qa-perf-analyst", "ops-cloud-engineer", "obs-sre", "gtw-external-reviewer",
})


def _net_roles() -> frozenset:
    try:
        from . import registry
        roles = registry.net_allowed_roles()
        if roles:
            return roles
    except Exception:
        pass
    return _NET_FALLBACK


NET_ALLOWED_ROLES = _net_roles()

# Obvious hardcoded-secret patterns blocked at promotion (Rule 7).
_SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|passwd|token)\s*[:=]\s*['\"][^'\"]{8,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),                     # AWS access key id
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def _resolve(path: str | Path) -> Path:
    return Path(path).resolve()


def assert_within_project(path: str | Path, prj: str) -> Path:
    """Rule 1: a project script may write only inside its own project tree."""
    target = _resolve(path)
    root = paths.project_dir(prj).resolve()
    if root not in (target, *target.parents):
        raise GovernanceError(
            f"scope violation: {target} is outside project {prj} ({root}). "
            "A script writes only inside its own project."
        )
    return target


def assert_within_repo(path: str | Path) -> Path:
    """Floor rule: nothing ever writes outside the workspace root."""
    target = _resolve(path)
    root = paths.repo_root().resolve()
    if root not in (target, *target.parents):
        raise GovernanceError(f"scope violation: {target} is outside the SOFI AI workspace ({root}).")
    return target


def assert_within_tooling(path: str | Path) -> Path:
    """Shared-library dev writes only inside core/."""
    target = _resolve(path)
    root = paths.tooling_dir().resolve()
    if root not in (target, *target.parents):
        raise GovernanceError(f"scope violation: {target} is outside core/ ({root}).")
    return target


def net_allowed(role: str) -> bool:
    return role in NET_ALLOWED_ROLES


def assert_net_allowed(role: str) -> None:
    """Rule 2: block network use by heads-down roles (devs, QA, content)."""
    if not net_allowed(role):
        raise GovernanceError(
            f"net policy: agent '{role}' has no web access. "
            "Pull web findings through your Room Lead (core/nexus/registry.yaml tools grants)."
        )


def scan_secrets(text: str) -> list[str]:
    """Rule 7: return offending snippets so promotion can be refused."""
    hits = []
    for pat in _SECRET_PATTERNS:
        for m in pat.finditer(text):
            hits.append(m.group(0)[:40])
    return hits


def check_script_header(path: str | Path) -> list[str]:
    """Rule 4: a shared/promotable script must carry a governance header.

    Returns a list of problems (empty = compliant).
    """
    p = _resolve(path)
    problems: list[str] = []
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as e:
        return [f"unreadable: {e}"]

    head = "\n".join(text.splitlines()[:25])
    required = ("role:", "purpose:", "gate:", "exit:")
    for token in required:
        if token not in head:
            problems.append(f"missing header field '{token}'")
    secrets = scan_secrets(text)
    if secrets:
        problems.append(f"hardcoded secret(s) detected: {secrets}")
    return problems
