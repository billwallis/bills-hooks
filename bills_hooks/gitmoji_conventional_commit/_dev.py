"""
Collect the resources for the hook.

If this were an application, we'd just collect the resources when it
runs. However, I don't want the hook to have to rely on anything
external to run, so we'll collect the resources here.
"""

import logging
import urllib.request

import yaml

from bills_hooks import SOURCE_ROOT
from bills_hooks._logging.logger import setup_logging  # noqa

GITMOJIS_URL = "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/packages/gitmojis/src/gitmojis.json"

setup_logging()
logger = logging.getLogger("bills-hooks")


def collect_gitmoji() -> None:
    """
    Collect the gitmoji from the ``gitmojis.json`` file.
    """
    logger.debug(f"Using gitmoji URL: {GITMOJIS_URL}")
    with urllib.request.urlopen(GITMOJIS_URL) as response:
        gitmojis = yaml.safe_load(response.read())
        logger.debug(f"Collecting {len(gitmojis['gitmojis'])} gitmojis")

    target = SOURCE_ROOT / "gitmoji_conventional_commit/gitmojis.yaml"
    logger.debug(f"Writing to target: {target}")
    with open(target, "w+", encoding="utf-8") as file:
        yaml.dump(gitmojis, file, encoding="utf-8", allow_unicode=True)
        logger.debug(f"Gitmojis dumped to {file.name}")


if __name__ == "__main__":
    collect_gitmoji()  # pragma: no cover
