"""
Validate that the ``.pre-commit-config.yaml`` file is valid.

There's no need to check that the schema is correct, as the pre-commit
framework will do that for us before running the hooks. However, we can
check that the file _contents_ are valid -- for example, that the hooks
listed in the ``ci.skip`` array are actually defined in the file.
"""

from __future__ import annotations

import argparse
import os
import pathlib
from collections.abc import Sequence

import yaml

from bills_hooks.pre_commit_validate.model import PreCommitConfig

# Return values
SUCCESS = 0
FAILURE = 1


def _validate_config(pre_commit_config_file: pathlib.Path) -> int:
    contents = yaml.safe_load(
        pre_commit_config_file.read_text(encoding="utf-8")
    )
    pre_commit_config = PreCommitConfig.from_dict(contents)

    try:
        _validate_ci(pre_commit_config)
        return SUCCESS
    except Exception:
        return FAILURE


def _validate_ci(pre_commit_config: PreCommitConfig) -> None:
    hooks = [
        hook["id"] for repo in pre_commit_config.repos for hook in repo.hooks
    ]
    for skipped_hook in pre_commit_config.ci.skip:
        if skipped_hook not in hooks:
            raise KeyError(f"Unknown hook '{skipped_hook}' found in 'ci.skip'")


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pre-commit-config-path",
        type=str,
        default=None,
        required=False,
        help=argparse.SUPPRESS,  # for testing purposes only
    )
    args = parser.parse_args(argv)

    pre_commit_config = (
        args.pre_commit_config_path or f"{os.getcwd()}/.pre-commit-config.yaml"
    )

    return _validate_config(pathlib.Path(pre_commit_config))


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
