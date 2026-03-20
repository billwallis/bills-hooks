import pathlib
import textwrap

import pytest

from bills_hooks.check_no_commit_comment import hook


@pytest.mark.parametrize(
    "code, expected_outcome",
    [
        # No matches
        ("", False),
        ("\0", False),
        ("def garbage:", False),
        ("""def foo(): return 0""", False),
        ("""import NO_COMMIT""", False),
        ("""NO_COMMIT = 'NO_COMMIT'""", False),
        (
            textwrap.dedent(
                """
                def foo():
                    '''
                    This NO_COMMIT is fine.
                    '''
                """
            ),
            False,
        ),
        # Matches
        ("""# NO_COMMIT""", True),
        ("""def foo(): return 0  # NO_COMMIT""", True),
        ("""import NO_COMMIT  # NO_COMMIT""", True),
        ("""NO_COMMIT = 'NO_COMMIT'  # NO_COMMIT""", True),
        (
            textwrap.dedent(
                """
                def foo():
                    '''
                    This NO_COMMIT is fine.
                    '''
                    # But not this NO_COMMIT message
                """
            ),
            True,
        ),
    ],
)
def test__has_no_commit_comment(
    tmp_path: pathlib.Path,
    code: str,
    expected_outcome: bool,
):
    tmp_file = tmp_path / "f.py"
    tmp_file.write_text(code)

    assert hook.main([str(tmp_file)]) == expected_outcome
