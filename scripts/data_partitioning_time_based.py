###################################################################
#
# --- SCRIPT: data_partitioning_time_based.py ---
#
# GOAL: 1. set and check a proper chronological order in the data_origin rows
#       2. split raw dataset into raw train set and raw test set.
#
# INPUT: none
#
# OUTPUT:
#   1. time_based_data_splitting function that returns
#      a tuple with both train and test dataset.
#
###################################################################

import polars as pl

def time_based_data_split(
    df_polars: pl.DataFrame,
    time_column: str, # requires the name of the column expressed in a string type
    train_threshold: float
    ):

    # set the proper chronological ascending order based on time column
    df_polars_sorted = (
        df_polars
        .sort(
            by = time_column,
            descending = False
            )
    )

    # Split threshold definition (rows before threshold go to train, the rest to test)
    train_split_idx = int(len(df_polars_sorted) * train_threshold)
    test_split_idx = int(len(df_polars_sorted) - train_split_idx)

    # time based split: the rows included into the threshold create the train set,
    # while the remaining (the most recent) go into the test set.
    raw_data_train = df_polars_sorted.head(train_split_idx)
    raw_data_test = df_polars_sorted.tail(test_split_idx)

    # return the final datasets.
    return raw_data_train, raw_data_test



    




