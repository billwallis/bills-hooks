"""
Unit tests for the ``bills_hooks.pre_commit_validate.hook`` module.
"""

import pathlib
import shutil

import pytest

from bills_hooks.pre_commit_validate import hook

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def valid_config_files(tmp_path: pathlib.Path):
    """
    Valid pre-commit configuration files.
    """

    config_file_1 = tmp_path / "valid.1.pre-commit-config.yaml"
    config_file_2 = tmp_path / "valid.2.pre-commit-config.yaml"
    shutil.copyfile(
        FIXTURES / "valid.1.pre-commit-config.yaml",
        config_file_1,
    )
    shutil.copyfile(
        FIXTURES / "valid.2.pre-commit-config.yaml",
        config_file_2,
    )

    return [config_file_1, config_file_2]


@pytest.fixture
def invalid_config_file(tmp_path: pathlib.Path):
    """
    An invalid pre-commit configuration file.
    """

    config_file = tmp_path / "invalid.pre-commit-config.yaml"
    shutil.copyfile(
        FIXTURES / "invalid.pre-commit-config.yaml",
        config_file,
    )

    return config_file


def test__valid_config_passes(
    valid_config_files: list[pathlib.Path],
):
    """
    A valid pre-commit configuration file passes validation.
    """

    for valid_config_file in valid_config_files:
        rc = hook.main(["--pre-commit-config-path", str(valid_config_file)])
        assert rc == hook.SUCCESS


def test__invalid_config_fails(
    invalid_config_file: pathlib.Path,
):
    """
    An invalid pre-commit configuration file fails validation.
    """

    rc = hook.main(["--pre-commit-config-path", str(invalid_config_file)])
    assert rc == hook.FAILURE
