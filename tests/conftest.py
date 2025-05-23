import pathlib
import shutil

import pytest

HERE = pathlib.Path(__file__).parent


@pytest.fixture(scope="session", autouse=True)
def teardown():
    """
    Test session teardown.
    """

    yield

    shutil.rmtree(HERE.parent / "tests-temp", ignore_errors=True)
