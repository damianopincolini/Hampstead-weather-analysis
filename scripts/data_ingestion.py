###################################################################
#
# --- SCRIPT: data_ingestion.py ---
#
# GOAL: Connect directly to the PostgreSQL database and load 
#       weather data into a Polars DataFrame using environment variables.
#
###################################################################

# Import operating system module to access system environment variables
import os

# Import polars for high-performance data manipulation and database reading
import polars as pl

# Import load_dotenv to load configuration settings from the local .env file
from dotenv import load_dotenv

# Load environment variables from the .env file into the runtime environment
load_dotenv()

def dataset_import() -> pl.DataFrame:
    """
    Connects directly to the PostgreSQL database using environment credentials,
    executes a SQL query, and returns the result as a Polars DataFrame.
    """
    
    # Retrieve individual database connection parameters from environment variables
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    
    # Validate that all required database credentials are present in the environment
    if not all([db_host, db_port, db_name, db_user, db_password]):
        raise ValueError("One or more database environment variables (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD) are missing in the .env file.")
        
    # Construct the PostgreSQL connection URI string with SSL mode enabled for Supabase
    connection_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?sslmode=require"
    
    # Define the SQL query to select all records from the weather table
    query = "SELECT * FROM weather_hampstead;"
    
    # Execute the query and load the results directly into a Polars DataFrame
    df = pl.read_database_uri(query=query, uri=connection_uri)
    
    # Return the loaded DataFrame
    return df