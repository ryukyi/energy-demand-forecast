"""Get env vars, configure logger and timing decorator."""

import os
import sys
from functools import wraps
from time import perf_counter

from dotenv import find_dotenv, load_dotenv
from loguru import logger

# Use local `".env" file vars or fail silently if it doesn't exist
load_dotenv(dotenv_path=find_dotenv())

# default to INFO but expose so can be overrriden
LOGLEVEL = os.getenv("LOGLEVEL", "INFO")

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


def timing(func):
    """Decorator which returns runtime for a function.

    This is an alternative to using the python timeit module.

    :param func: decorate the function to time
    :return: nothing except info to std.out and logger sink
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        time_start = perf_counter()
        # run the func
        func_meta = func(*args, **kwargs)
        time_end = perf_counter()
        run_time = time_end - time_start
        # @NOTE: !r will return repr of func and :.8f is 8 decimal places
        meta = f"func: {func.__name__!r}, time taken: {run_time:.8f}, args:\n{[args, kwargs]}\n"
        logger.debug(meta)
        return func_meta

    return wrap
