import pathlib
import textwrap

import pytest

from bills_hooks.check_no_commit_comment import hook


@pytest.mark.parametrize(
    "filename, code, expected_outcome",
    [
        # No matches (default)
        ("f.txt", "", False),
        ("f.txt", "\0", False),
        ("f.txt", "foo bar\nbaz", False),
        ("f.txt", "foo  # no_commit", False),
        ("f.xml", "<note><heading>no_commit</heading></note>", False),
        ("f.svg", "<svg ...>no_commit</svg>", False),
        ("f.png", f"{0x89}NO_COMMIT", False),
        # Matches (default)
        ("f.txt", """NO_COMMIT""", True),
        ("f.txt", """Please NO_COMMIT this file""", True),
        ("f.xml", "<note><heading>NO_COMMIT</heading></note>", True),
        ("f.svg", "<svg ...>NO_COMMIT</svg>", True),
        # No matches (Python)
        ("f.py", "", False),
        ("f.py", "\0", False),
        ("f.py", "def garbage:", False),
        ("f.py", """def foo(): return 0""", False),
        ("f.py", """import NO_COMMIT""", False),
        ("f.py", """NO_COMMIT = 'NO_COMMIT'""", False),
        (
            "f.py",
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
        # Matches (Python)
        ("f.py", """# NO_COMMIT""", True),
        ("f.py", """def foo(): return 0  # NO_COMMIT""", True),
        ("f.py", """import NO_COMMIT  # NO_COMMIT""", True),
        ("f.py", """NO_COMMIT = 'NO_COMMIT'  # NO_COMMIT""", True),
        (
            "f.py",
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
    filename: str,
    code: str,
    expected_outcome: bool,
):
    tmp_file = tmp_path / filename
    tmp_file.write_text(code)

    assert hook.main([str(tmp_file)]) == expected_outcome
