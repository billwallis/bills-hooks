import pathlib

import pytest

from bills_hooks import check_github_codeowners


def test__hook_can_be_run_without_arguments():
    """
    The hook is a no-op when run on files without arguments.
    """

    assert check_github_codeowners.main([]) == 0


@pytest.fixture
def mock_directory(tmp_path: pathlib.Path) -> pathlib.Path:
    (tmp_path / "src/foo").mkdir(parents=True)
    (tmp_path / "src/foo/__init__.py").touch()
    (tmp_path / "src/foo/main.py").touch()
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "tests/test__main.py").touch()

    return tmp_path


@pytest.mark.parametrize(
    "contents",
    [
        # base case
        "",
        # whole directory
        "*",
        "* @someone",
        "* @someone @org/team",
        # path relative to root
        "/src/",
        "/src/ @someone",
        "/src/ @someone @org/team",
        "/src/* @someone @org/team",
        "/src/**/*.py @someone @org/team",
        "/src/**/main.py @someone @org/team",
        # floating path
        "foo/",
        "foo/ @someone",
        "foo/ @someone @org/team",
        "foo/* @someone @org/team",
        "foo/main.py @someone @org/team",
        # mixed with comments
        "# foo bar baz\n* @everyone\n/src/ @someone\nfoo/* @someone @org/team",
    ],
)
def test__valid_files_pass_successfully(
    monkeypatch: pytest.MonkeyPatch,
    mock_directory: pathlib.Path,
    contents: str,
):
    """
    Valid CODEOWNERS file contents pass successfully.
    """

    monkeypatch.chdir(mock_directory)
    filepath = mock_directory / "CODEOWNERS"
    filepath.touch()
    filepath.write_text(contents, encoding="utf-8")

    assert check_github_codeowners.main([str(filepath)]) == 0


@pytest.mark.parametrize(
    "contents",
    [
        # multiple paths (caught by the owner parser)
        "* /src/ @someone",
        # invalid paths
        "/etc/",
        "/etc/*",
        "/etc/**",
        "etc/",
        "etc/*",
        "etc/**",
    ],
)
def test__invalid_files_fail_correctly(
    monkeypatch: pytest.MonkeyPatch,
    mock_directory: pathlib.Path,
    contents: str,
):
    """
    Invalid CODEOWNERS file contents fail correctly.
    """

    monkeypatch.chdir(mock_directory)
    filepath = mock_directory / "CODEOWNERS"
    filepath.touch()
    filepath.write_text(contents, encoding="utf-8")

    assert check_github_codeowners.main([str(filepath)]) == 1
