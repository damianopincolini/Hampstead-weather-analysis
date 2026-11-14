###################################################################
#
# --- SCRIPT: intermediate_files.py ---
#
# GOAL: save dataset for both EDA and
#       modeling in parquet format. 
#       Dataset for EDA referres to train set only and 
#       includes feature engineering columns.
#       Datasets for modeling (train and test) are
#       based on raw data and the serve the end-to-
#       end logic.
#
# INPUT: none
#
# OUTPUT:
#   1. save_eda_dataset and save_modeling_datasets functions,
#      where eda dataset is only one and derives from 
#      train dataset, while modeling datasets are two:
#      train and test. Eda dataset is the train dataset after
#      data wrangling; train/test dataset come from the 
#      plain splitting of data_origin
#
###################################################################


from pathlib import Path

import polars as pl


def save_eda_dataset(
    df_eda_polars: pl.DataFrame,
    output_dir: Path
):
    # Defining paths where output have to be saved
    train_output_path = output_dir / "data_train_eda.parquet"

    # Saving files
    df_eda_polars.write_parquet(train_output_path)



def save_modeling_datasets(
    df_train_polars: pl.DataFrame,
    df_test_polars: pl.DataFrame,
    output_dir: Path
):
    # Defining of paths where output have to be saved
    train_output_path = output_dir / "data_train_modeling.parquet"
    test_output_path = output_dir / "data_test_modeling.parquet"

    # Saving files
    df_train_polars.write_parquet(train_output_path)
    df_test_polars.write_parquet(test_output_path)
