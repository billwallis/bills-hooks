"""
Unit tests for the ``bills_hooks.gitmoji_conventional_commit.hook`` module.
"""

import pathlib

import pytest

from bills_hooks.gitmoji_conventional_commit import hook


@pytest.mark.parametrize(
    "message, expected",
    [
        ("✨ feat(frontend): Add a new feature", True),
        ("🐛 fix: Fix a thing\n\nResolves #123", True),
        ("📝 docs: Update docs\n\nMake some changes", True),
        ("chore: Upgrade something", True),
        ("fix!: Fix something broken", True),
        ("\n📝 docs: Update docs", False),
        ("spin: something up", False),
        ("this is a comment", False),
    ],
)
def test__is_valid_commit_message(message: str, expected: bool):
    """
    Test the ``is_valid_commit_message`` function.
    """

    assert hook.is_valid_commit_message(message) == expected


@pytest.fixture
def message_path__success(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    A commit message that is valid.
    """

    file = tmp_path / "message-success.txt"
    file.write_text(
        "✨ feat(scope): This is a good message\n\nWith a good body",
        encoding="utf-8",
    )

    return file


@pytest.fixture
def message_path__failure(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    A commit message that is not valid.
    """

    file = tmp_path / "message-failure.txt"
    file.write_text("this is a bad message")

    return file


def test__main(
    message_path__success: pathlib.Path,
    message_path__failure: pathlib.Path,
):
    """
    Test the ``main`` function.
    """

    assert hook.main([str(message_path__success)]) == hook.SUCCESS
    assert hook.main([str(message_path__failure)]) == hook.FAILURE
