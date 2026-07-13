"""
role: shared library (shamel_tools)
purpose: multi-agent workflow orchestration (DAG-based pipelines)
gate: 3-7
inputs: workflow definitions, step templates, context dicts
outputs: execution results, status updates, workflow JSON
exit: raises ValueError on invalid DAG, otherwise returns result dicts
"""
from __future__ import annotations

import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shamel_tools import paths, brain, tickets, runlog


class WorkflowError(Exception):
    """Raised on invalid workflow operations."""


class WorkflowStep:
    """A single step in a multi-agent workflow.

    Attributes:
        id: unique step id (auto-generated)
        agent_name: target agent for this step
        input_template: jinja-like template string with {context_var} placeholders
        depends_on: list of step ids that must complete first
        result: output dict after execution
        status: pending/running/success/failed/skipped
        condition: optional dict {field, operator, value} to evaluate before running
    """

    def __init__(
        self,
        agent_name: str,
        input_template: str,
        depends_on: list[str] | None = None,
        *,
        step_id: str | None = None,
        condition: dict | None = None,
    ):
        self.id = step_id or uuid.uuid4().hex[:10]
        self.agent_name = agent_name
        self.input_template = input_template
        self.depends_on = depends_on or []
        self.condition = condition
        self.result: dict | None = None
        self.status: str = "pending"
        self.error: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "agent_name": self.agent_name,
            "input_template": self.input_template,
            "depends_on": self.depends_on,
            "condition": self.condition,
            "status": self.status,
            "error": self.error,
            "result": self.result,
        }

    @classmethod
    def from_dict(cls, d: dict) -> WorkflowStep:
        step = cls(
            agent_name=d["agent_name"],
            input_template=d["input_template"],
            depends_on=d.get("depends_on", []),
            step_id=d.get("id"),
            condition=d.get("condition"),
        )
        step.status = d.get("status", "pending")
        step.result = d.get("result")
        step.error = d.get("error")
        return step


class Workflow:
    """A multi-step DAG workflow.

    Attributes:
        id: unique workflow id
        name: human-readable name
        description: purpose
        steps: ordered dict of step_id -> WorkflowStep
        context: shared context dict passed between steps
        status: draft/active/completed/failed
        created_at / updated_at: ISO timestamps
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        *,
        workflow_id: str | None = None,
    ):
        self.id = workflow_id or uuid.uuid4().hex[:12]
        self.name = name
        self.description = description
        self.steps: dict[str, WorkflowStep] = {}
        self.context: dict[str, Any] = {}
        self.status: str = "draft"
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at

    def add_step(
        self,
        agent_name: str,
        input_template: str,
        depends_on: list[str] | None = None,
        *,
        step_id: str | None = None,
        condition: dict | None = None,
    ) -> str:
        step = WorkflowStep(
            agent_name=agent_name,
            input_template=input_template,
            depends_on=depends_on,
            step_id=step_id,
            condition=condition,
        )
        if step.id in self.steps:
            raise WorkflowError(f"step {step.id} already exists")
        self.steps[step.id] = step
        self.updated_at = datetime.now(timezone.utc).isoformat()
        return step.id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "steps": {sid: s.to_dict() for sid, s in self.steps.items()},
            "context": self.context,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, default=str)

    @classmethod
    def from_dict(cls, d: dict) -> Workflow:
        wf = cls(
            name=d["name"],
            description=d.get("description", ""),
            workflow_id=d.get("id"),
        )
        wf.status = d.get("status", "draft")
        wf.context = d.get("context", {})
        wf.created_at = d.get("created_at", wf.created_at)
        wf.updated_at = d.get("updated_at", wf.updated_at)
        for sid, sdata in d.get("steps", {}).items():
            wf.steps[sid] = WorkflowStep.from_dict(sdata)
        return wf

    @classmethod
    def from_json(cls, text: str) -> Workflow:
        return cls.from_dict(json.loads(text))


class Orchestrator:
    """Manages multi-agent workflow pipelines.

    Creates, executes, and persists workflows as JSON files.
    Handles DAG dependency resolution, context passing, and branching.
    """

    def __init__(self, storage_dir: str | Path | None = None):
        self.storage_dir = Path(storage_dir) if storage_dir else paths.engine_dir() / "workflows"
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._workflows: dict[str, Workflow] = {}
        self._lock = threading.Lock()

    def create_workflow(self, name: str, description: str = "") -> Workflow:
        wf = Workflow(name=name, description=description)
        with self._lock:
            self._workflows[wf.id] = wf
        return wf

    def add_step(
        self,
        workflow_id: str,
        agent_name: str,
        input_template: str,
        depends_on: list[str] | None = None,
        *,
        condition: dict | None = None,
    ) -> str:
        wf = self._get(workflow_id)
        step_id = wf.add_step(
            agent_name=agent_name,
            input_template=input_template,
            depends_on=depends_on,
            condition=condition,
        )
        return step_id

    def _get(self, workflow_id: str) -> Workflow:
        wf = self._workflows.get(workflow_id)
        if wf is None:
            wf = self._load(workflow_id)
        if wf is None:
            raise WorkflowError(f"unknown workflow: {workflow_id}")
        return wf

    def execute(self, workflow_id: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a workflow: resolve the DAG, run ready steps, collect results.

        Steps that have no unresolved dependencies run in order. Branching
        via condition: {field, operator, value} skips steps whose condition
        is not met based on previous step outputs in context.
        """
        wf = self._get(workflow_id)
        if context:
            wf.context.update(context)

        wf.status = "active"
        wf.updated_at = datetime.now(timezone.utc).isoformat()
        completed: set[str] = set()

        while True:
            ready = self._ready_steps(wf, completed)
            if not ready:
                break
            for step in ready:
                self._evaluate_step(step, wf)
                if step.status == "success" and step.result is not None:
                    wf.context[step.id] = step.result
                    if step.result.get("output"):
                        wf.context["_last_output"] = step.result["output"]
                completed.add(step.id)

        all_done = all(s.status in ("success", "skipped") for s in wf.steps.values())
        wf.status = "completed" if all_done else "failed"
        self._save(wf)
        return wf.to_dict()

    def _ready_steps(self, wf: Workflow, completed: set[str]) -> list[WorkflowStep]:
        ready: list[WorkflowStep] = []
        for step in wf.steps.values():
            if step.status != "pending":
                continue
            if any(dep not in completed for dep in step.depends_on):
                continue
            if step.condition and not self._check_condition(step.condition, wf.context):
                step.status = "skipped"
                continue
            ready.append(step)
        return ready

    def _check_condition(self, condition: dict, context: dict) -> bool:
        field = condition.get("field", "")
        op = condition.get("operator", "eq")
        value = condition.get("value")
        actual = context.get(field, context.get("_last_output", ""))
        if op == "eq":
            return str(actual) == str(value)
        elif op == "neq":
            return str(actual) != str(value)
        elif op == "contains":
            return str(value) in str(actual)
        elif op == "not_contains":
            return str(value) not in str(actual)
        return True

    def _evaluate_step(self, step: WorkflowStep, wf: Workflow):
        step.status = "running"
        try:
            rendered = step.input_template.format(**wf.context)
        except KeyError as e:
            step.status = "failed"
            step.error = f"template render failed: missing key {e}"
            return

        step.result = {
            "output": rendered,
            "agent": step.agent_name,
            "step_id": step.id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        step.status = "success"

    def get_status(self, workflow_id: str) -> str:
        return self._get(workflow_id).status

    def get_results(self, workflow_id: str) -> dict[str, Any]:
        wf = self._get(workflow_id)
        results: dict[str, Any] = {
            "workflow_id": wf.id,
            "name": wf.name,
            "status": wf.status,
            "steps": {},
            "context": wf.context,
        }
        for sid, step in wf.steps.items():
            results["steps"][sid] = {
                "agent_name": step.agent_name,
                "status": step.status,
                "error": step.error,
                "output": step.result.get("output") if step.result else None,
            }
        return results

    def save(self, workflow_id: str) -> str:
        wf = self._get(workflow_id)
        return self._save(wf)

    def _save(self, wf: Workflow) -> str:
        path = self.storage_dir / f"{wf.id}.json"
        path.write_text(wf.to_json(), encoding="utf-8")
        return str(path)

    def _load(self, workflow_id: str) -> Workflow | None:
        path = self.storage_dir / f"{workflow_id}.json"
        if not path.exists():
            return None
        try:
            text = path.read_text(encoding="utf-8")
            wf = Workflow.from_json(text)
            with self._lock:
                self._workflows[wf.id] = wf
            return wf
        except (json.JSONDecodeError, OSError):
            return None

    def load(self, workflow_id: str) -> Workflow | None:
        return self._load(workflow_id)

    def list_workflows(self) -> list[dict]:
        workflows: list[dict] = []
        for path in sorted(self.storage_dir.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                workflows.append({
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "status": data.get("status"),
                    "step_count": len(data.get("steps", {})),
                    "updated_at": data.get("updated_at"),
                })
            except (json.JSONDecodeError, OSError):
                continue
        return workflows
