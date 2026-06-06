"""
Check filenames match patterns.
"""

from __future__ import annotations

import argparse
import pathlib
import re
from collections.abc import Sequence

# Return values
SUCCESS = 0
FAILURE = 1


def _is_valid_regex_pattern(
    filename: str,
    pattern: str,
) -> bool:
    if re.match(pattern, filename):
        return True

    print(
        f"File '{filename}' did not match regular expression pattern '{pattern}'"
    )
    return False


def _check_filename_pattern(filename: str, args: argparse.Namespace) -> int:
    """
    Check filenames match patterns.
    """

    name = pathlib.Path(filename).name if args.name_only else filename

    if args.regex:
        return SUCCESS if _is_valid_regex_pattern(name, args.regex) else FAILURE

    return SUCCESS


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    parser.add_argument(
        "--name-only",
        action=argparse.BooleanOptionalAction,
        help="only match on the file name and extension, not its path",
    )
    parser.add_argument("--regex", help="the regex pattern to test")
    args = parser.parse_args(argv)

    outcome = SUCCESS
    for filename in args.filenames:
        outcome |= _check_filename_pattern(filename, args)
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
