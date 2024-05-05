"""Pre-processing of energy dataframe.

All logic included in equivalent notebook
"""

from loguru import logger

from exploratory import DATA_PATH, df_energy

# Updated path to reflect the .parquet file extension
PREPROCESS_DATA_PATH = (
    DATA_PATH / "processed/processed_energy_demand_generation.parquet"
)

# Drop columns which are zero, Nan or forecasts
df_energy = df_energy.drop(
    [
        "generation fossil coal-derived gas",
        "generation fossil oil shale",
        "generation fossil peat",
        "generation geothermal",
        "generation hydro pumped storage aggregated",
        "generation marine",
        "generation wind offshore",
        "forecast wind offshore eday ahead",
        "total load forecast",
        "forecast solar day ahead",
        "forecast wind onshore day ahead",
    ],
    axis=1,
)

# ensure time axis is parsed correctly
df_energy = df_energy.set_index("time")

# Interpolate remaining null values using simplest forward interpolation method
df_energy.interpolate(method="linear", limit_direction="forward", inplace=True, axis=0)

logger.info(df_energy.describe().round(2))
logger.info(df_energy.info())

# Output to a compressed Parquet file using snappy compression
df_energy.to_parquet(PREPROCESS_DATA_PATH, compression="snappy")
