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

from . import (paths, registry, brain, tickets, routing, gates, guard, runlog,
               brain_client, orchestrator, agent_runner, task_agent,
               validator, context_manager, reporter, skills_loader)  # noqa: F401

from .brain_client import BrainClient  # noqa: F401
from .orchestrator import Orchestrator, Workflow, WorkflowStep, WorkflowError  # noqa: F401
from .agent_runner import AgentRunner  # noqa: F401
from .task_agent import TaskAgent  # noqa: F401
from .validator import Validator, severity_of  # noqa: F401
from .context_manager import ContextManager  # noqa: F401
from .reporter import Reporter  # noqa: F401
from .skills_loader import SkillsLoader  # noqa: F401

__all__ = ["paths", "registry", "brain", "tickets", "routing", "gates", "guard", "runlog",
           "brain_client", "orchestrator", "agent_runner", "task_agent",
           "BrainClient", "Orchestrator", "Workflow", "WorkflowStep", "WorkflowError",
           "AgentRunner", "TaskAgent",
           "validator", "context_manager", "reporter", "skills_loader",
           "Validator", "severity_of", "ContextManager", "Reporter", "SkillsLoader"]
