###################################################################
#
# --- SCRIPT: data_describe.py ---
#
# GOAL: Create a function to import csv from a specific path
#
# INPUT: data_origin
#
# OUTPUT:
#   1. dataset_describe function
#
###################################################################


import polars as pl
import polars.selectors as cs
from great_tables import GT


def data_describe(df_polars: pl.DataFrame):

# describe function and transpose results
    df_polars_describe1 = (
        df_polars.describe()
        .with_columns(
            cs.float().round(2) # rounding to two decimals
        )
        .transpose(include_header=True, header_name="Statistics")
    )

# handle columns' names changes
    new_column_names = df_polars_describe1.row(0)[1:]
    old_column_names = [col for col in df_polars_describe1.columns if col.startswith("column_")]
    column_names_map = dict(zip(old_column_names, new_column_names))

# rename dataFrame
    df_polars_describe2 = (
        df_polars_describe1
        .rename(column_names_map)
        .slice(1)
        .select(
            pl.col("Statistics"),
            pl.col("count"),
            pl.col("null_count")
            ) 
    )

# visualize via GT
    return (
        GT(df_polars_describe2)
        .tab_header(
            title = "First glance statistics"
        )
        .tab_options(
            table_width = "100%",
            table_font_size = "8pt",
            column_labels_font_weight = "bold"
        )
    )