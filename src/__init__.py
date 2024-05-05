"""Get env vars, configure logger and timing decorator."""

import os
import sys
from functools import wraps
from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from loguru import logger

# Use local `".env" file vars or fail silently if it doesn't exist
load_dotenv(dotenv_path=find_dotenv())

# Project paths
ROOT_PATH = Path(__file__).parents[1].absolute()
EXPLORATORY_ROOT_PATH = ROOT_PATH / "exploratory"
DATA_PATH = ROOT_PATH / "data"
RAW_ENERGY_ZIP_DATA = DATA_PATH / "raw/hourly_energy_demand_generation.zip"

# default to INFO but expose so can be overrriden
LOGLEVEL = os.getenv("LOGLEVEL", "INFO")

LOGGER_CONFIG = {
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
logger.configure(handlers=LOGGER_CONFIG["handlers"])


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


# Open the zip file
with ZipFile(RAW_ENERGY_ZIP_DATA, "r") as zipdata:
    # Iterate over the files in the zip file
    for f in zipdata.filelist:
        # Check if the file is the energy dataset
        if f.filename == "energy_dataset.csv":
            # Read the CSV file into a pandas DataFrame
            df_energy = pd.read_csv(zipdata.open(f.filename), parse_dates=["time"])
            logger.debug("Energy data loaded.")
        # Check if the file is the weather features dataset
        elif f.filename == "weather_features.csv":
            # Read the CSV file into a pandas DataFrame
            df_weather = pd.read_csv(zipdata.open(f.filename), parse_dates=["dt_iso"])
            logger.debug("Weather data loaded.")

# force time to be correctly parsed and typed
df_energy["time"] = pd.to_datetime(df_energy["time"], utc=True)
