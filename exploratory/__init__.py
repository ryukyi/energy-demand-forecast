"""Exploratory setup config.

Reads in datasets from raw zip folder.
"""

import os
import sys
from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from loguru import logger

# Project paths
ROOT_PATH = Path(__file__).parents[1].absolute()
EXPLORATORY_ROOT_PATH = ROOT_PATH / "exploratory"
DATA_PATH = ROOT_PATH / "data"

# default to INFO but expose so can be overrriden with env args
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

RAW_DATA = DATA_PATH / "raw/hourly_energy_demand_generation.zip"

# Open the zip file
with ZipFile(RAW_DATA, "r") as zipdata:
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
