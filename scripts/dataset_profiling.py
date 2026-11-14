###################################################################
#
# --- SCRIPT: dataset_profiling.py ---
#
# GOAL: create a solid base for dataset analysis. The expected 
#       output is a complete report.
# 
# Note that, in order to use ydata_profiling library (a proficient 
# analysis tool which uses Pandas df), it's mandatory to transform
# the dataframe from Polars to Pandas.
#
# INPUT: none
#
# OUTPUT:
#   1. create_quality_report function.
#
###################################################################


import pandas as pd
from data_profiling import ProfileReport


def create_quality_report(df_polars, output_path):
    """
    Convert a Polars DataFrame to Pandas and generate a YData Profiling
    HTML report.

    Args:
        df_polars (pl.DataFrame): The source dataset in Polars format.
        output_path (Path): The full destination path, including the
        filename (e.g., report.html).

    Returns:
        None: The function saves the file directly to the specified
        path.
    """

    # 1. Convertion from polars to pandas
    df_pandas = df_polars.to_pandas()

    # 2. Report configuration
    data_origin_profile = ProfileReport(
        df_pandas,
        title="Profiling Report",
        explorative=True,
    )

    # 3. Report saving in the provided path
    data_origin_profile.to_file(output_path)
