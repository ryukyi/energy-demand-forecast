from zipfile import ZipFile
from pathlib import Path 

p = Path("fixtures/hourly_energy_demand_generation.zip")

with ZipFile(p, 'r') as zipdata:
    for f in zipdata.filelist:
        if f.filename == "energy_dataset.csv":
            print("energy data")
        if f.filename == "weather_features.csv":
            print("weather data")