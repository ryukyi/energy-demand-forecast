"""Exploratory setup config."""

import os
import sys

from loguru import logger

# default to INFO but expose so can be overrriden
LOGLEVEL = os.getenv("LOGLEVEL", "DEBUG")

loguru_config = {
    "handlers": [
        {
            "sink": sys.stdout,
            # engueue exposes async logs. False hides them.
            # https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.complete
            "enqueue": True,
            "level": LOGLEVEL,
            "format": (
                "<yellow>{time:%Y-%m-%d at %H:%M:%S %z (%Z)}</> | <level>{level}</level>"
                "| <green>{module}</>:<green>{function}</>:<green>{line}</> - "
                "<blue>{message}</> | {elapsed.seconds}s"
            ),
        },
    ],
    # "extra": {"user": "example_user"},
}

# root logger with "enqueue=True" to capture async
logger.configure(handlers=loguru_config["handlers"])