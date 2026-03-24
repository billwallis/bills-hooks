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


def _has_no_commit_comment(content: str) -> bool:
    tokens = tokenize.tokenize(io.BytesIO(content.encode()).readline)
    for token in tokens:
        if token.type == tokenize.COMMENT:
            if NO_COMMIT in token.string:
                return True
    return False


def _check_no_commit_comment__python(content: str) -> int:
    if not _is_parseable(content):
        # If we can't parse it, we don't know if it has the comment, so
        # we can't correctly fail
        return SUCCESS
    if _has_no_commit_comment(content):
        return FAILURE
    return SUCCESS


def _check_no_commit_comment__default(content: str) -> int:
    if NO_COMMIT in content:
        return FAILURE
    return SUCCESS


def _check_no_commit_comment(filename: str) -> int:
    """
    Check for presence of `NO_COMMIT` comments.
    """

    with open(filename) as f:
        content = f.read()

    tags = identify.identify.tags_from_filename(filename)
    if "python" in tags:
        return _check_no_commit_comment__python(content)
    else:
        return _check_no_commit_comment__default(content)


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
