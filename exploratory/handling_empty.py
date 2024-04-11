"""Decide what to do with the missing values."""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd
from loguru import logger
from scipy.stats import shapiro

from exploratory.visualise.skewness import plot_histogram

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


# Function to check if a column is normally distributed
def is_normally_distributed(column: pd.Series) -> bool:
    """Normal distribution helps understand if mean is sensible replacement of nan.

    Args:
        column (pd.Series): data inspected

    Returns:
        bool: confirms the data is normally distributed
    """
    # Check if the column has enough data points (at least 3)
    if len(column) < 3:
        return False, "Not enough data points"

    # Perform the Shapiro-Wilk test
    stat, p = shapiro(column)

    # If p > 0.05, we assume the data is normally distributed
    if p > 0.05:
        return True, f"p-value: {p:.5f}"
    else:
        return False, f"p-value: {p:.5f}"


# Cycle through each column
for col in energy_df.columns:
    # Check if the column has any NaN values
    if energy_df[col].isna().any():
        is_normal, result = is_normally_distributed(energy_df[col])
        logger.debug(f"Column '{col}' is normally distributed: {is_normal}. {result}")
        plot_histogram(energy_df[col])
        # logger.debug(energy_df[col])
        # Decide what to do with the missing values
        # Option 1: Drop the rows with missing values
        # logger.debug("Option 1: Drop rows with missing values.")
        # df.dropna(subset=[col], inplace=True)

        # Option 2: Fill the missing values with a specific value (e.g., 0)
        # logger.debug("Option 2: Fill missing values with 0.")
        # df[col].fillna(0, inplace=True)

        # Option 3: Fill the missing values with the mean of the column
        # logger.debug("Option 3: Fill missing values with the mean of the column.")
        # df[col].fillna(df[col].mean(), inplace=True)

        # Option 4: Fill the missing values with the median of the column
        # logger.debug("Option 4: Fill missing values with the median of the column.")
        # df[col].fillna(df[col].median(), inplace=True)

        # Option 5: Fill the missing values with the mode of the column
        # logger.debug("Option 5: Fill missing values with the mode of the column.")
        # df[col].fillna(df[col].mode()[0], inplace=True)

        # Option 6: Fill the missing values with a value from another column
        # This is more complex and depends on your specific use case
        # logger.debug("Option 6: Fill missing values with a value from another column.")

        # Option 7: Fill the missing values with a value from a related dataset
        # This is more complex and depends on your specific use case
        # logger.debug("Option 7: Fill missing values with a value from a related dataset.")

# logger.debug the DataFrame to see the result
logger.debug(energy_df)
