"""
Unit tests for the ``bills_hooks.tidy_gitkeep.hook`` module.
"""

import pathlib
import shutil
import subprocess

import pytest

import bills_hooks
from bills_hooks.tidy_gitkeep import hook

FIXTURE_TEMPLATE_DIR = (
    bills_hooks.PROJECT_ROOT / "tests/tidy_gitkeep/fixtures/template"
)


@pytest.fixture(scope="module")
def working_dir(tmp_path_factory) -> pathlib.Path:
    """
    A working directory with some redundant .gitkeep files.
    """

    temp_dir = tmp_path_factory.mktemp("working_dir")
    shutil.copytree(
        FIXTURE_TEMPLATE_DIR,
        temp_dir,
        dirs_exist_ok=True,
    )

    return temp_dir


def test__redundant_files_are_removed(working_dir: pathlib.Path):
    """
    Redundant .gitkeep files are removed.

    Note: this piggybacks off of the current git directory, so any change
    to the current git configuration may affect this test.

    Ideally, the temporary directory should be created in a separate
    environment with its own git repository and configuration, but I
    cba right now.
    """

    other_files = [
        str(working_dir / "subdir-1/file-1.txt"),
        str(working_dir / "subdir-3/subdir-4/file-2.txt"),
        str(working_dir / "subdir-3/subdir-5/file-3.txt"),
        str(working_dir / "subdir-3/.gitignore"),
    ]
    kept_gitkeep_files = [
        str(working_dir / "subdir-1/subdir-2/.gitkeep"),
        str(working_dir / "subdir-3/subdir-5/.gitkeep"),
    ]
    removed_gitkeep_files = [
        str(working_dir / "subdir-3/subdir-4/.gitkeep"),
    ]

    rc = hook.main([*kept_gitkeep_files, *removed_gitkeep_files])

    assert rc == hook.SUCCESS
    for file in [*other_files, *kept_gitkeep_files]:
        assert pathlib.Path(file).exists()
    for file in removed_gitkeep_files:
        assert not pathlib.Path(file).exists()


def test__redundant_files_are_removed_using_dot_expression(
    monkeypatch: pytest.MonkeyPatch,
    working_dir: pathlib.Path,
):
    """
    Redundant .gitkeep files are removed.

    This emulates using this as a CLI and passing the `.` argument for filenames
    which is shorthand for "all files".
    """

    other_files = [
        str(working_dir / "subdir-1/file-1.txt"),
        str(working_dir / "subdir-3/subdir-4/file-2.txt"),
        str(working_dir / "subdir-3/subdir-5/file-3.txt"),
        str(working_dir / "subdir-3/.gitignore"),
    ]
    kept_gitkeep_files = [
        str(working_dir / "subdir-1/subdir-2/.gitkeep"),
        str(working_dir / "subdir-3/subdir-5/.gitkeep"),
    ]
    removed_gitkeep_files = [
        str(working_dir / "subdir-3/subdir-4/.gitkeep"),
    ]

    monkeypatch.chdir(working_dir)
    rc = hook.main(["."])

    assert rc == hook.SUCCESS
    for file in [*other_files, *kept_gitkeep_files]:
        assert pathlib.Path(file).exists()
    for file in removed_gitkeep_files:
        assert not pathlib.Path(file).exists()


def test__unexpected_subprocess_errors_are_raised(
    monkeypatch: pytest.MonkeyPatch,
):
    """
    Unexpected return codes from the subprocess raises exceptions.

    The subprocess call is expected to return:

    - exit code 0 if the file is ignored by git
    - exit code 1 if the file is not ignored by git

    Any other exit code is unexpected and should raise an exception.
    """

    err_msg = "Damn it, Jim, I'm a doctor, not a git repository"

    def run(*args, **kwargs):  # noqa: unused parameters
        return subprocess.CompletedProcess([], returncode=2, stderr=err_msg)

    monkeypatch.setattr(subprocess, "run", run)

    with pytest.raises(RuntimeError, match=err_msg):
        hook.main(["foo"])
