import pathlib
import textwrap

import pytest

from bills_hooks.banned_python_code import hook


@pytest.mark.parametrize(
    "code, expected_outcome",
    [
        # No matches
        ("", False),
        ("\0", False),
        (
            textwrap.dedent(
                """\
                def test__foo():
                    assert 1 == 1
                """
            ),
            False,
        ),
        (
            # TODO (enhancement): Handle this case
            textwrap.dedent(
                """\
                from pytest import raises

                def test__foo():
                    with raises(ZeroDivisionError, match="err"):
                        print(1 / 0)
                """
            ),
            False,
        ),
        (
            # TODO (enhancement): Handle this case
            textwrap.dedent(
                """\
                from pytest import raises as pytest_raises

                def test__foo():
                    with pytest_raises(ZeroDivisionError, match="err"):
                        print(1 / 0)
                """
            ),
            False,
        ),
        # Matches
        (
            textwrap.dedent(
                """\
                import pytest

                def test__foo():
                    with pytest.raises(ZeroDivisionError, match="err"):
                        print(1 / 0)
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
