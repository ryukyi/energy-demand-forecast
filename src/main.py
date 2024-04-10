"""run main models."""

from pathlib import Path
from zipfile import ZipFile

p = Path("data/raw/hourly_energy_demand_generation.zip")

with ZipFile(p, "r") as zipdata:
    for f in zipdata.filelist:
        if f.filename == "energy_dataset.csv":
            print("energy data")
        if f.filename == "weather_features.csv":
            print("weather data")
