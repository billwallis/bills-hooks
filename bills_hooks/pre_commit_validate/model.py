"""
Dataclasses corresponding to the schema of a ``.pre-commit-config.yaml``
file.

See below for more info:

- https://pre-commit.com/#pre-commit-configyaml---top-level
- https://pre-commit.ci/#configuration
"""

from __future__ import annotations

import dataclasses
from typing import Literal

AutoUpdateSchedule = Literal["weekly", "monthly", "quarterly"]


@dataclasses.dataclass
class PreCommitRepo:
    repo: str
    hooks: list[dict]
    rev: str = ""  # not required for `meta` or `local` repos


@dataclasses.dataclass
class PreCommitCI:
    autofix_commit_msg: str = "[pre-commit.ci] auto fixes [...]"
    autofix_prs: bool = True
    autoupdate_branch: str = ""
    autoupdate_commit_msg: str = "[pre-commit.ci] pre-commit autoupdate"
    autoupdate_schedule: AutoUpdateSchedule = "weekly"
    skip: list[str] = dataclasses.field(default_factory=list)
    submodules: bool = False


@dataclasses.dataclass
class PreCommitConfig:
    repos: list[PreCommitRepo]
    default_install_hook_types: list[str] = dataclasses.field(
        default_factory=list
    )
    default_language_version: dict[str, str] = dataclasses.field(
        default_factory=dict
    )
    default_stages: list[str] = dataclasses.field(default_factory=list)
    files: str = ""
    exclude: str = "^$"
    fail_fast: bool = False
    minimum_pre_commit_version: str = "0"
    ci: PreCommitCI = dataclasses.field(default_factory=PreCommitCI)

    @classmethod
    def from_dict(cls, data: dict) -> PreCommitConfig:
        """
        Create a PreCommitConfig instance from a dictionary.
        """

        kwargs = {
            "repos": [PreCommitRepo(**repo) for repo in data.get("repos")],
            "default_install_hook_types": data.get(
                "default_install_hook_types"
            ),
            "default_language_version": data.get("default_language_version"),
            "default_stages": data.get("default_stages"),
            "files": data.get("files"),
            "exclude": data.get("exclude"),
            "fail_fast": data.get("fail_fast"),
            "minimum_pre_commit_version": data.get(
                "minimum_pre_commit_version"
            ),
            "ci": PreCommitCI(**data.get("ci")) if data.get("ci") else None,
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        return cls(**kwargs)
