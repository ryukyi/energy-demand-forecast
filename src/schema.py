"""Declare acceptable schema for all types of data."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EnergyData(BaseModel):
    """Energy data schema."""

    time: datetime = Field(..., alias="time")
    generation_biomass: float = Field(..., alias="generation biomass")
    generation_fossil_brown_coal_lignite: float = Field(
        ..., alias="generation fossil brown coal/lignite"
    )
    generation_fossil_coal_derived_gas: float = Field(
        ..., alias="generation fossil coal-derived gas"
    )
    generation_fossil_gas: float = Field(..., alias="generation fossil gas")
    generation_fossil_hard_coal: float = Field(..., alias="generation fossil hard coal")
    generation_fossil_oil: float = Field(..., alias="generation fossil oil")
    generation_fossil_oil_shale: float = Field(..., alias="generation fossil oil shale")
    generation_fossil_peat: float = Field(..., alias="generation fossil peat")
    generation_geothermal: float = Field(..., alias="generation geothermal")
    generation_hydro_pumped_storage_aggregated: Optional[float] = Field(
        None, alias="generation hydro pumped storage aggregated"
    )
    generation_hydro_pumped_storage_consumption: Optional[float] = Field(
        None, alias="generation hydro pumped storage consumption"
    )
    generation_hydro_run_of_river_and_poundage: Optional[float] = Field(
        None, alias="generation hydro run-of-river and poundage"
    )
    generation_hydro_water_reservoir: Optional[float] = Field(
        None, alias="generation hydro water reservoir"
    )
    generation_marine: float = Field(..., alias="generation marine")
    generation_nuclear: float = Field(..., alias="generation nuclear")
    generation_other: float = Field(..., alias="generation other")
    generation_other_renewable: float = Field(..., alias="generation other renewable")
    generation_solar: float = Field(..., alias="generation solar")
    generation_waste: float = Field(..., alias="generation waste")
    generation_wind_offshore: float = Field(..., alias="generation wind offshore")
    generation_wind_onshore: float = Field(..., alias="generation wind onshore")
    forecast_solar_day_ahead: Optional[float] = Field(
        None, alias="forecast solar day ahead"
    )
    forecast_wind_offshore_eday_ahead: Optional[float] = Field(
        None, alias="forecast wind offshore eday ahead"
    )
    forecast_wind_onshore_day_ahead: Optional[float] = Field(
        None, alias="forecast wind onshore day ahead"
    )
    total_load_forecast: float = Field(..., alias="total load forecast")
    total_load_actual: float = Field(..., alias="total load actual")
    price_day_ahead: float = Field(..., alias="price day ahead")
    price_actual: float = Field(..., alias="price actual")
