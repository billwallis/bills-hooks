"""
Unit tests for the ``bills_hooks.pre_commit_validate.hook`` module.
"""

import pathlib
import shutil

import pytest

from bills_hooks.pre_commit_validate import hook

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture(
    params=[
        "valid.1.pre-commit-config.yaml",
        "valid.2.pre-commit-config.yaml",
    ]
)
def valid_config_file(
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
) -> pathlib.Path:
    """
    Valid pre-commit configuration file.
    """

    filename = request.param
    config_file = tmp_path / filename
    shutil.copyfile(FIXTURES / filename, config_file)

    return config_file


@pytest.fixture
def invalid_config_file(tmp_path: pathlib.Path) -> pathlib.Path:
    """
    An invalid pre-commit configuration file.
    """

    filename = "invalid.pre-commit-config.yaml"
    config_file = tmp_path / filename
    shutil.copyfile(FIXTURES / filename, config_file)

    return config_file


def test__valid_config_passes(
    valid_config_file: pathlib.Path,
):
    """
    A valid pre-commit configuration file passes validation.
    """

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
