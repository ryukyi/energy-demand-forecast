"""Decide what to do with the missing values."""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from loguru import logger

from exploratory.visualise.skewness import (
    is_normally_distributed,
    plot_histogram,
    skewness,
)

# Define the path to the zip file
p = Path("data/raw/hourly_energy_demand_generation.zip")

# Initialize empty DataFrames
energy_df = pd.DataFrame()
weather_df = pd.DataFrame()

# Open the zip file
with ZipFile(p, "r") as zipdata:
    # Iterate over the files in the zip file
    for f in zipdata.filelist:
        # Check if the file is the energy dataset
        if f.filename == "energy_dataset.csv":
            # Read the CSV file into a pandas DataFrame
            energy_df = pd.read_csv(zipdata.open(f.filename))
            logger.debug("Energy data loaded.")
        # Check if the file is the weather features dataset
        elif f.filename == "weather_features.csv":
            # Read the CSV file into a pandas DataFrame
            weather_df = pd.read_csv(zipdata.open(f.filename))
            logger.debug("Weather data loaded.")


# Cycle through each column
for col in energy_df.columns:
    # Check if the column has any NaN values then determine how to manage
    if energy_df[col].isna().any():
        is_normal, result = is_normally_distributed(energy_df[col])
        logger.debug(f"Column '{col}' is normally distributed: {is_normal}. {result}")
        skew = skewness(energy_df[col])
        logger.debug(f"Column '{col}'skew: {is_normal}. {result}")
        plot_histogram(energy_df[col])
# logger.debug the DataFrame to see the result
logger.debug(energy_df)
