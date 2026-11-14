###################################################################
#
# --- SCRIPT: data_wrangling.py ---
#
# GOAL: 1. prepare a function that calls all needed transformations and feature
#       creations.
#       2. execute data validation according to a defined schema
#
# INPUT: none
#
# OUTPUT:
#   1. feature_engineering function which returns a new Polars
#      DataFrame (data) with modified/new feature.
#
###################################################################


# Feature engineering

import pandera.polars as pa
import polars as pl
import polars.selectors as cs
from datetime import datetime, timezone


# 1. Validation scheme
weather_schema = pa.DataFrameSchema({
    "temperature_2m": pa.Column(pl.Float64, pa.Check.between(-40.0, 50.0), nullable=True),
    "relative_humidity_2m": pa.Column(pl.Float64, pa.Check.between(0.0, 100.0), nullable=True),
    "precipitation": pa.Column(pl.Float64, pa.Check.ge(0.0), nullable=True),
    "value_origin": pa.Column(pl.String, pa.Check.isin(["real", "forecast"])),
    "date": pa.Column(pl.Date),
})

# 2. Validation check @pa.check_output + feature 
# engineering function

# The `@pa.check_output(weather_schema)` decorator wraps the feature engineering function 
# to automatically validate the returned Polars DataFrame against predefined constraints.

@pa.check_output(weather_schema)

def feature_engineering (df_polars: pl.DataFrame):

    data = (
        df_polars
        # splitting timestamps into date and time
        .with_columns(
            pl.col("time").dt.date().alias("date"),
            pl.col("time").dt.hour().alias("hour")
        )
        # boolean setting real and forecast row values
        .with_columns(
            pl.when(pl.col("time") <= datetime.now(timezone.utc))
            .then(pl.lit("real"))
            .otherwise(pl.lit("forecast"))
            .alias("value_origin")
        )
        # cancelling useless columns
        .drop(
            [
                "id",
                "location",
                "created_at"
            ],
            strict = False
        )
    )
    return data

