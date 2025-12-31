import logging

from rocket.config import RELEASE

_logger = logging.getLogger("app")

if not _logger.handlers:
    _logger.setLevel(logging.INFO if RELEASE else logging.DEBUG)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(threadName)s: %(message)s"
    )
    handler.setFormatter(formatter)
    _logger.addHandler(handler)


def log(message: str) -> None:
    _logger.debug(message)
