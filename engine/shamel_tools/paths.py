"""
paths — resolve SHAMEL workspace + per-project directories.
Single source of truth for SHAMEL file layout.
"""
from __future__ import annotations

import os
from pathlib import Path


def repo_root(start: str | os.PathLike | None = None) -> Path:
    """Walk upward from `start` until SHAMEL root (CLAUDE.md + core/) found."""
    here = Path(start or __file__).resolve()
    for d in (here, *here.parents):
        if (d / "CLAUDE.md").exists() and (d / "core").is_dir():
            return d
    raise FileNotFoundError(
        "SHAMEL root not found (need CLAUDE.md + core/). "
        f"Searched from {here}."
    )


def core_dir() -> Path:
    """Law, nexus, rooms, brain."""
    return repo_root() / "core"


def shamel_dir() -> Path:
    """Alias for core_dir — backwards compat."""
    return core_dir()


def engine_dir() -> Path:
    """The executable layer — shamel_tools, bin/shamel."""
    return repo_root() / "engine"


def nexus_dir() -> Path:
    """registry.yaml, routing.yaml, gates.yaml, bus/."""
    return core_dir() / "nexus"


def brain_dir() -> Path:
    """Brain — BRAIN.md, org/, db/, templates/."""
    return repo_root() / "brain"


def projects_dir() -> Path:
    """Physical projects root.
    Override with SHAMEL_PROJECTS_DIR; defaults to <repo>/projects.
    """
    env = os.environ.get("SHAMEL_PROJECTS_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return (repo_root() / "projects").resolve()


def project_dir(prj: str) -> Path:
    return projects_dir() / prj


def project_repo(prj: str) -> Path:
    d = project_dir(prj).resolve()
    for c in (d, *d.parents):
        if (c / ".git").exists():
            return c
    return d


def context_dir(prj: str) -> Path:
    return project_dir(prj) / "_context"


def brain_file(prj: str, name: str) -> Path:
    return context_dir(prj) / f"{name}.md"


def docs_dir(prj: str) -> Path:
    return project_dir(prj) / "docs"


def scratch_dir(prj: str) -> Path:
    return project_dir(prj) / "_scratch"


def project_exists(prj: str) -> bool:
    return project_dir(prj).is_dir() and context_dir(prj).is_dir()


def list_projects() -> list[str]:
    pd = projects_dir()
    if not pd.is_dir():
        return []
    return sorted(p.name for p in pd.iterdir() if p.is_dir() and (p / "_context").is_dir())
