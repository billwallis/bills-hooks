"""
Check for presence of `NO_COMMIT` comments.

Inspired by:

- https://github.com/elementary-data/elementary/blob/ef5043811a72009126391a3f0c8a18f72ae00b18/.pre-commit-config.yaml
"""

from __future__ import annotations

import argparse
import ast
import io
import tokenize
from collections.abc import Sequence

import identify.identify

# Return values
SUCCESS = 0
FAILURE = 1
NO_COMMIT = "NO_COMMIT"


def _is_parseable(content: str) -> bool:
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False


def _print_found(filename: str, line_no: int, line: str) -> None:
    print(f"{filename}:{line_no}: {line}")


def _has_no_commit_comment(filename: str, content: str) -> bool:
    has_no_commit_comment = False
    tokens = tokenize.tokenize(io.BytesIO(content.encode()).readline)
    for token in tokens:
        if token.type == tokenize.COMMENT:
            if NO_COMMIT in token.string:
                has_no_commit_comment = True
                _print_found(filename, token.start[0], token.line.rstrip("\n"))
    return has_no_commit_comment


def _check_no_commit_comment__python(filename: str, content: str) -> int:
    if not _is_parseable(content):
        # If we can't parse it, we don't know if it has the comment, so
        # we can't correctly fail
        return SUCCESS
    if _has_no_commit_comment(filename, content):
        return FAILURE
    return SUCCESS


def _check_no_commit_comment__default(filename: str, content: str) -> int:
    ret = SUCCESS
    for line_no, line in enumerate(content.split("\n"), start=1):
        if NO_COMMIT in line:
            ret = FAILURE
            _print_found(filename, line_no, line)
    return ret


def _check_no_commit_comment(filename: str) -> int:
    """
    Check for presence of `NO_COMMIT` comments.
    """

    tags = identify.identify.tags_from_filename(filename)
    if "text" not in tags:
        return SUCCESS

    with open(filename, encoding="utf-8") as f:
        content = f.read()

    if "python" in tags:
        return _check_no_commit_comment__python(filename, content)
    else:
        return _check_no_commit_comment__default(filename, content)


def main(argv: Sequence[str] | None = None) -> int:
    """
    Parse the arguments and run the hook.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)

    outcome = SUCCESS
    for filename in args.filenames:
        outcome |= _check_no_commit_comment(filename)
    return outcome


if __name__ == "__main__":
    raise SystemExit(main())  # pragma: no cover
