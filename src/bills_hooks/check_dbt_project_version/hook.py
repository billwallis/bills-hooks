from __future__ import annotations

import argparse
import contextlib
import importlib.metadata
import pathlib
import textwrap
from collections.abc import Sequence

import yaml

SUCCESS = 0
FAILURE = 1
RED = "\033[1;31m"
RESET = "\033[0m"


def _get_dbt_project_version(dbt_project_dir: pathlib.Path) -> str | None:
    with open(dbt_project_dir / "dbt_project.yml") as f:
        content = yaml.safe_load(f)

    return content.get("version")


def _get_python_project_version(package_name: str) -> str | None:
    with contextlib.suppress(importlib.metadata.PackageNotFoundError):
        return importlib.metadata.version(package_name)

    return None


def warn() -> int:
    """
    Print a warning if the hook is used via the repo rather than via the
    CLI.
    """

    print(
        textwrap.dedent(
            f"""\
            {RED}This hook must be used in a `local` repo.{RESET}

            Install the repo and add the following hook configuration for
            this hook instead:

              - repo: local
                hooks:
                  - id: check-dbt-project-version
                    name: Check dbt project version
                    entry: >
                      check-dbt-project-version
                      --dbt-project-dir '<dbt_project.yml directory>'
                      --python-project-name '<target repo name>'
                    language: unsupported
                    always_run: true
                    pass_filenames: false
            """
        )
    )
    return FAILURE


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--python-project-name", required=True)
    parser.add_argument("--dbt-project-dir", default=".")
    args = parser.parse_args(argv)

    dbt_project_version = _get_dbt_project_version(
        pathlib.Path(args.dbt_project_dir).resolve()
    )
    python_project_version = _get_python_project_version(
        args.python_project_name
    )
    if dbt_project_version == python_project_version:
        return SUCCESS

    print(
        textwrap.dedent(
            f"""\
            {RED}Version mismatch found{RESET}
                dbt_project.yml: {dbt_project_version}
                Python project:  {python_project_version}
            """
        )
    )
    return FAILURE


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
