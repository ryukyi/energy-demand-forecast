"""run main models."""

from pathlib import Path
from zipfile import ZipFile

import pandas as pd

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
            print("Energy data loaded.")
        # Check if the file is the weather features dataset
        elif f.filename == "weather_features.csv":
            # Read the CSV file into a pandas DataFrame
            weather_df = pd.read_csv(zipdata.open(f.filename))
            print("Weather data loaded.")

# Now, energy_df and weather_df contain the data from the respective CSV files
