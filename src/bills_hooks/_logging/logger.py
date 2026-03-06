"""
Configure application logging.

Instructions followed from:

- https://youtu.be/9L77QExPmI0
"""

import logging.config
import logging.handlers

import yaml

from bills_hooks import SOURCE_ROOT

logger = logging.getLogger("bills-hooks")


def setup_logging() -> None:
    """
    Configure the logging configuration.
    """
    config_file = SOURCE_ROOT / "_logging/logger.yaml"
    logging.config.dictConfig(yaml.safe_load(config_file.read_text()))
