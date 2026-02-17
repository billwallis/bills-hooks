import pytest

from bills_hooks.check_filename_pattern import hook


def test__hook_can_be_run_without_arguments():
    """
    The hook is a no-op when run without arguments.
    """

    rc = hook.main([])
    assert rc == 0


@pytest.mark.parametrize(
    "filenames, regex, expected_outcome",
    [
        # Pattern matches all file paths -> success
        (["foo/bar/baz.txt", "foo/bar/qux.py"], r"^foo/bar/\w{3}\.\w{2,3}$", 0),
        # Pattern matches all file names, but no `--name-only` -> failure
        (["foo/bar/baz.txt", "foo/bar/qux.py"], r"^\w{3}\.\w{2,3}$", 1),
        # Pattern matches all but one file path --> failure
        (["foo/a", "foo/b", "foo/c", "foo/d"], r"^foo/[a-c]$", 1),
    ],
)
def test__regex_patterns_can_be_matched(
    filenames: list[str],
    regex: str,
    expected_outcome: int,
):
    """
    Regex patterns can be matched.
    """

    rc = hook.main([*filenames, "--regex", regex])
    assert rc == expected_outcome


@pytest.mark.parametrize(
    "filenames, regex, name_only, expected_outcome",
    [
        # Pattern matches all file paths, but no `--no-name-only` -> failure
        (
            ["foo/bar/baz.txt", "foo/bar/qux.py"],
            r"^foo/bar/\w{3}\.\w{2,3}$",
            "--name-only",
            1,
        ),
        # Pattern matches all file paths, and `--no-name-only` -> success
        (
            ["foo/bar/baz.txt", "foo/bar/qux.py"],
            r"^foo/bar/\w{3}\.\w{2,3}$",
            "--no-name-only",
            0,
        ),
        # Pattern matches all file names, -> success
        (
            ["foo/bar/baz.txt", "foo/bar/qux.py"],
            r"^\w{3}\.\w{2,3}$",
            "--name-only",
            0,
        ),
        # Pattern matches all but one file name --> failure
        (["a", "b", "c", "d"], r"^[a-c]$", "--name-only", 1),
    ],
)
def test__regex_patterns_can_be_matched_by_name_only(
    filenames: list[str],
    regex: str,
    name_only: str,
    expected_outcome: int,
):
    """
    Regex patterns can be matched.
    """

    rc = hook.main([*filenames, "--regex", regex, name_only])
    assert rc == expected_outcome
