###################################################################
#
# --- SCRIPT: project_config.py ---
#
# GOAL: Set core project paths, global Polars configurations, 
#       and database connection settings.
#
# INPUT: none
#
# OUTPUT:
#   1. ROOT_DIR and paths dictionary.
#   2. db_uri for database connection.
#
###################################################################

import os
from pathlib import Path
import polars as pl
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Determine the root directory dynamically and safely (one level above 'scripts')
ROOT_DIR = Path(__file__).resolve().parent.parent

# Paths configuration dictionary
paths = {
    "root": ROOT_DIR,
    "scripts": ROOT_DIR / "scripts",
    "notebooks": ROOT_DIR / "notebooks",
    "data": ROOT_DIR / "data",
    "raw_data_dir": ROOT_DIR / "data" / "raw_data",
    "processed_data_dir": ROOT_DIR / "data" / "processed_data",
    "outputs": ROOT_DIR / "outputs",
    "report_dir": ROOT_DIR / "outputs" / "reports",
    "plots_dir": ROOT_DIR / "outputs" / "plots",
}

# Database connection URI for Supabase / PostgreSQL
db_uri = os.getenv("SUPABASE_DB_URI", "postgresql://user:password@host:port/dbname")

# Polars global editing setup
pl.Config.set_tbl_rows(20)          # Sets how many rows are shown in the preview
pl.Config.set_fmt_str_lengths(100)  # Prevents Polars from cutting long strings
pl.Config.set_float_precision(2)    # Forces floats to show only 2 decimal places
pl.Config.set_tbl_width_chars(80)   # Limits the table width in characters