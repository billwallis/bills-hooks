import pathlib
import textwrap

import pytest

from bills_hooks import check_no_commit_comment


@pytest.mark.parametrize(
    "filename, code, expected",
    [
        # No matches (default)
        ("f.txt", "", (False, "")),
        ("f.txt", "\0", (False, "")),
        ("f.txt", "foo bar\nbaz", (False, "")),
        ("f.txt", "foo  # no_commit", (False, "")),
        ("f.xml", "<note><heading>no_commit</heading></note>", (False, "")),
        ("f.svg", "<svg ...>no_commit</svg>", (False, "")),
        ("f.png", f"{0x89}NO_COMMIT", (False, "")),
        ("f.yaml", "foo: 🤓  # no_commit", (False, "")),
        # Matches (default)
        ("f.txt", """NO_COMMIT""", (True, "f.txt:1: NO_COMMIT")),
        (
            "f.txt",
            """Please NO_COMMIT this file""",
            (True, "f.txt:1: Please NO_COMMIT this file"),
        ),
        (
            "f.xml",
            "<note>\n<heading>\nNO_COMMIT\n</heading>\n</note>",
            (True, "f.xml:3: NO_COMMIT"),
        ),
        (
            "f.svg",
            "<svg ...>NO_COMMIT</svg>",
            (True, "f.svg:1: <svg ...>NO_COMMIT</svg>"),
        ),
        # No matches (Python)
        ("f.py", "", (False, "")),
        ("f.py", "\0", (False, "")),
        ("f.py", "def garbage:", (False, "")),
        ("f.py", """def foo(): return 0""", (False, "")),
        ("f.py", """import NO_COMMIT""", (False, "")),
        ("f.py", """NO_COMMIT = 'NO_COMMIT'""", (False, "")),
        ("f.py", """# This no_commit is fine""", (False, "")),
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
            (False, ""),
        ),
        # Matches (Python)
        ("f.py", """# NO_COMMIT""", (True, "f.py:1: # NO_COMMIT")),
        (
            "f.py",
            """def foo():\n    return 0  # NO_COMMIT""",
            (True, "f.py:2:     return 0  # NO_COMMIT"),
        ),
        (
            "f.py",
            """import NO_COMMIT  # NO_COMMIT""",
            (True, "f.py:1: import NO_COMMIT  # NO_COMMIT"),
        ),
        (
            "f.py",
            """NO_COMMIT = 'NO_COMMIT'  # NO_COMMIT""",
            (True, "f.py:1: NO_COMMIT = 'NO_COMMIT'  # NO_COMMIT"),
        ),
        (
            "f.py",
            textwrap.dedent(
                """\
                def foo():
                    '''
                    This NO_COMMIT is fine.
                    '''
                    # But not this NO_COMMIT message
                """
            ),
            (True, "f.py:5:     # But not this NO_COMMIT message"),
        ),
    ],
)
def test__has_no_commit_comment(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    filename: str,
    code: str,
    expected: tuple[bool, str],
):
    monkeypatch.chdir(tmp_path)
    tmp_file = tmp_path / filename
    tmp_file.write_text(code, encoding="utf-8")

    actual_result = check_no_commit_comment.main(
        [str(tmp_file.relative_to(tmp_path))]
    )
    assert actual_result == expected[0]

    captured = capsys.readouterr()
    assert captured.out.rstrip("\n") == expected[1]
