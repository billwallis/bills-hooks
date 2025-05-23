"""
Remove redundant .gitkeep files from the repository.

A `.gitkeep` file is redundant if the directory it is in has any other
tracked files. The tracked files can be in the same directory or in
subdirectories.
"""

from __future__ import annotations

import argparse
import os
import pathlib
import subprocess
from collections.abc import Sequence

# Return values
SUCCESS = 0
FAILURE = 1
SUBPROCESS_ERROR_CODE = 128


def _get_gitkeep_files(root_dir: pathlib.Path) -> list[pathlib.Path]:
    """
    Return a list of all `.gitkeep` files in the repository.
    """

    return list(root_dir.rglob(".gitkeep"))


def _is_file_ignored(file: pathlib.Path) -> bool:
    """
    Check if a file is ignored by git.

    https://git-scm.com/docs/git-check-ignore
    """

    completed_process = subprocess.run(  # noqa: S603
        f"git check-ignore {file} --quiet".split(" "),
        check=False,
    )

    if completed_process.returncode == SUCCESS:
        return True
    if completed_process.returncode == FAILURE:
        return False
    if completed_process.returncode == SUBPROCESS_ERROR_CODE:
        raise RuntimeError(completed_process.stderr)
    raise RuntimeError("Failed to check if file is ignored by git.")


def _remove_redundant_gitkeep_files(
    root_dir: pathlib.Path,
) -> int:
    """
    Remove redundant `.gitkeep` files from the repository.
    """

    outcome = SUCCESS
    for file in _get_gitkeep_files(root_dir):
        other_files = [
            other_file
            for other_file in file.parent.rglob("*")
            if other_file.is_file() and other_file != file
        ]
        if any(not _is_file_ignored(other_file) for other_file in other_files):
            print(f"Removing file '{file.relative_to(root_dir)}'")
            file.unlink()
            outcome = FAILURE

    return outcome


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--working-directory",
        type=str,
        default=None,
        required=False,
        help="The working directory to check for redundant .gitkeep files. Defaults to the current working directory.",
    )
    args = parser.parse_args(argv)

    working_directory = args.working_directory or os.getcwd()

    return _remove_redundant_gitkeep_files(pathlib.Path(working_directory))


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
