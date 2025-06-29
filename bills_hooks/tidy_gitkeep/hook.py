"""
Remove redundant .gitkeep files from the repository.

A `.gitkeep` file is redundant if the directory it is in has any other
tracked files. The tracked files can be in the same directory or in
subdirectories.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
from collections.abc import Sequence

# Return values
SUCCESS = 0
FAILURE = 1
SUBPROCESS_ERROR_CODE = 128


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


def _remove_redundant_gitkeep_file(gitkeep_file: pathlib.Path) -> int:
    """
    Remove redundant `.gitkeep` files from the repository.
    """

    outcome = SUCCESS
    other_files = [
        other_file
        for other_file in gitkeep_file.parent.rglob("*")
        if other_file.is_file() and other_file != gitkeep_file
    ]
    if any(not _is_file_ignored(other_file) for other_file in other_files):
        gitkeep_file.unlink()
        print(f"Removed file '{gitkeep_file}'")
        outcome = FAILURE

    return outcome


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    return_code = SUCCESS
    for filename in args.filenames:
        return_code |= _remove_redundant_gitkeep_file(pathlib.Path(filename))

    return return_code


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
