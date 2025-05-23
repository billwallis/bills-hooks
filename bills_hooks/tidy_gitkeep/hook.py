"""
Remove redundant .gitkeep files from the repository.

A `.gitkeep` file is redundant if the directory it is in has any other
tracked files. The tracked files can be in the same directory or in
subdirectories.
"""

from __future__ import annotations

import os
import pathlib
import subprocess

# Return values
SUCCESS = 0
FAILURE = 1


def _get_gitkeep_files(root_dir: pathlib.Path) -> list[pathlib.Path]:
    """
    Return a list of all `.gitkeep` files in the repository.
    """

    return [
        path for path in root_dir.rglob(".gitkeep")
    ]


def _is_file_ignored(file: pathlib.Path) -> bool:
    """
    Check if a file is ignored by git.

    https://git-scm.com/docs/git-check-ignore
    """

    completed_process = subprocess.run(
        f"git check-ignore {file} --quiet".split(" ")
    )

    if completed_process.returncode == 0:
        return True
    if completed_process.returncode == 1:
        return False
    if completed_process.returncode == 128:
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


def main() -> int:
    """
    Parse the arguments and run the hook.
    """

    return _remove_redundant_gitkeep_files(pathlib.Path(os.getcwd()))


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
