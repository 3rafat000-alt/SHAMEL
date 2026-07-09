"""
shamel_tools — SOFI AI shared agent library ("desks").

Stdlib-first toolkit every agent imports to do its job against the company brain:
read/write project state, chain handoff tickets, resolve routes, validate gates,
and stay inside the governance sandbox.

Law: core/os/GOVERNANCE.md. Tooling index: core/registry.yaml.
Org index: core/nexus/registry.yaml (rooms · agents · skills · tools).
Nothing here reaches outside the repo or a project's own directory.
"""
__version__ = "2.0.0"

from . import paths, registry, brain, tickets, routing, gates, guard, runlog  # noqa: F401

__all__ = ["paths", "registry", "brain", "tickets", "routing", "gates", "guard", "runlog"]
