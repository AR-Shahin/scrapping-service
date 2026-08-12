import logging
import sys

from app.core.config import get_settings

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def setup_logging() -> None:
    logging.basicConfig(
        level=get_settings().log_level.upper(),
        format=_FORMAT,
        stream=sys.stdout,
        force=True,
    )
