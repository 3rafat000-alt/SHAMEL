"""
skills_loader — load skills from core/skills/ into agent context.

Reads the SKILLS-INDEX.md to discover skills, loads their markdown content,
and injects relevant skills into agent context dicts for pipeline execution.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from . import paths, registry

_SKILLS_DIR = paths.core_dir() / "skills"
_SKILLS_INDEX = _SKILLS_DIR / "SKILLS-INDEX.md"

_SKILL_FILE_RE = re.compile(r"`([^`]+)`")
_SKILL_HEADER_RE = re.compile(r"^\| ([^|]+) \| `([^`]+)` \|", re.MULTILINE)


def _parse_index() -> dict[str, dict[str, str]]:
    """Parse SKILLS-INDEX.md into {skill_name: {file, purpose, agents}}."""
    skills: dict[str, dict[str, str]] = {}
    if not _SKILLS_INDEX.exists():
        return skills

    text = _SKILLS_INDEX.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_data = False

    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_data = False
            continue
        if "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.split("|") if c.strip()]
        if len(cells) >= 4:
            name = cells[0]
            file_ref = cells[1]
            purpose = cells[2]
            agents = cells[3] if len(cells) > 3 else ""
            # Skip header row
            if name.lower() == "skill":
                continue
            skills[name.lower()] = {
                "name": name,
                "file": file_ref.strip("`"),
                "purpose": purpose,
                "agents": agents,
            }

    return skills


class SkillsLoader:
    """Load skills from core/skills/ into agent context.

    Skills are markdown files containing structured checklists, tables,
    and templates that agents use during pipeline execution.
    """

    def __init__(self) -> None:
        self._index: dict[str, dict[str, str]] | None = None

    @property
    def index(self) -> dict[str, dict[str, str]]:
        if self._index is None:
            self._index = _parse_index()
        return self._index

    def list_skills(self) -> list[dict[str, str]]:
        """Return all registered skills with metadata.

        Each entry: {name, file, purpose, agents}
        """
        return list(self.index.values())

    def load_skill(self, skill_name: str) -> str:
        """Load a single skill's markdown content by name.

        Returns full file content, or error message if not found.
        """
        info = self.index.get(skill_name.lower())
        if not info:
            return f"# Skill Not Found\n\nSkill '{skill_name}' not in SKILLS-INDEX.md.\n"

        skill_path = _SKILLS_DIR / info["file"]
        if not skill_path.exists():
            return f"# Skill File Missing\n\nFile '{skill_path}' does not exist.\n"

        return skill_path.read_text(encoding="utf-8")

    def load_skills_for(self, agent_name: str) -> list[str]:
        """Load all skills assigned to *agent_name*.

        Checks agent pattern against the 'agents' column in SKILLS-INDEX.md.
        Patterns: exact match, prefix match (e.g. fnt-*), ALL.

        Returns list of skill file contents.
        """
        results: list[str] = []
        for _name, info in self.index.items():
            agent_pattern = info.get("agents", "")
            if self._agent_matches(agent_name, agent_pattern):
                content = self.load_skill(info["name"])
                if not content.startswith("# Skill Not Found"):
                    results.append(content)
        return results

    @staticmethod
    def _agent_matches(agent_name: str, pattern: str) -> bool:
        """Check if *agent_name* matches a skill's agent assignment pattern.

        Patterns from SKILLS-INDEX.md agents column:
        - 'ALL agents' — base skills loaded for everyone
        - 'fnt-*, bck-*' — prefix match
        - 'res-*' — single prefix match
        """
        if not pattern or not agent_name:
            return False
        if pattern.strip() == "**ALL agents**" or pattern == "ALL":
            return True

        parts = [p.strip() for p in pattern.replace("**", "").split(",")]
        for part in parts:
            part = part.strip()
            if part.endswith("-*"):
                prefix = part[:-2]
                if agent_name.startswith(prefix):
                    return True
                # Also check room prefix (e.g. bck for bck-api-engineer)
                if agent_name.startswith(prefix + "-"):
                    return True
            elif part == agent_name:
                return True
        return False

    def inject_skill(self, skill_name: str, context: dict) -> str:
        """Load a skill and inject its content into a context dict.

        Adds key 'skill:<skill_name>' to the context with the content.
        Returns the skill content.
        """
        content = self.load_skill(skill_name)
        context[f"skill:{skill_name}"] = content
        return content

    def skill_exists(self, skill_name: str) -> bool:
        """Check if a skill is registered in SKILLS-INDEX.md."""
        return skill_name.lower() in self.index
