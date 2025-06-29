"""
Unit tests for the ``bills_hooks.tidy_gitkeep.hook`` module.
"""

import pathlib
import shutil

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
    Test that redundant .gitkeep files are removed.

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
    args = [
        "--working-directory",
        str(working_dir),
    ]

    rc = hook.main([*kept_gitkeep_files, *removed_gitkeep_files, *args])

    assert rc == hook.FAILURE
    for file in [*other_files, *kept_gitkeep_files]:
        assert pathlib.Path(file).exists()
    for file in removed_gitkeep_files:
        assert not pathlib.Path(file).exists()

    rc = hook.main(["--working-directory", str(working_dir)])
    assert rc == hook.SUCCESS
