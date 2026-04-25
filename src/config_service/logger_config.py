# pylint: disable= missing-module-docstring, missing-function-docstring
import logging
import os


def setup_logging():
    format_ = (
        "%(asctime)s | %(levelname)s | "
        "PID: %(process)d | %(filename)s:%(lineno)d:(%(funcName)s) | %(message)s"
    )
    time_format = "%Y-%m-%d %H:%M:%S"
    loglevel = os.environ.get("LOGLEVEL", "DEBUG").upper()

    logging.basicConfig(level=loglevel, format=format_, datefmt=time_format)
    logger = logging.getLogger(__name__)
    return logger
