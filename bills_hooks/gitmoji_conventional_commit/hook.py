"""
Validate that commit messages follow conventional commits, with an
optional gitmoji at the start of the header.

References to conventional commits and gitmoji:

- https://www.conventionalcommits.org/en/v1.0.0/
- https://gitmoji.dev/

This is partly inspired by:

- https://github.com/compilerla/conventional-pre-commit
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Sequence

# Basic pattern for a conventional commit message, not the full spec
PATTERN = re.compile(
    r"^(\W+ )?(build|chore|docs|feat|fix|perf|refactor|style|test)(\(.*\))?!?: [A-Z][\s\S]*(\s#\d+)?\S$"
)

# Return values
SUCCESS = 0
FAILURE = 1


def is_valid_commit_message(commit_message: str) -> bool:
    """
    Validate that a commit message follows conventional commits, with an
    optional gitmoji at the start of the header.
    """
    if commit_message.startswith("\n"):
        return False
    return bool(re.match(PATTERN, commit_message))


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        type=str,
        help="A file containing a git commit message. Pre-commit passes this in automatically.",
    )
    args = parser.parse_args(argv)

    with open(args.input, encoding="utf-8") as file:
        message = file.read()

    if not is_valid_commit_message(message):
        print("Commit message is not valid.")
        return FAILURE

    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
