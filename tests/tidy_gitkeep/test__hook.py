"""
Unit tests for the ``bills_hooks.tidy_gitkeep.hook`` module.
"""

import pathlib
import shutil

import pytest

import bills_hooks
from bills_hooks.tidy_gitkeep import hook


@pytest.fixture(scope="module")
def working_dir(tmp_path_factory) -> pathlib.Path:
    """
    A working directory with some redundant .gitkeep files.
    """

    temp_dir = tmp_path_factory.mktemp("working_dir")
    shutil.copytree(
        bills_hooks.PROJECT_ROOT / "tests/tidy_gitkeep/fixtures/template",
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
    rc = hook.main(["--working-directory", str(working_dir)])

    assert rc == hook.FAILURE
    assert (working_dir / "subdir-1/subdir-2/.gitkeep").exists()
    assert not (working_dir / "subdir-3/subdir-4/.gitkeep").exists()
    assert (working_dir / "subdir-3/subdir-5/.gitkeep").exists()

    rc = hook.main(["--working-directory", str(working_dir)])
    assert rc == hook.SUCCESS
