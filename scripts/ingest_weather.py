import os
import requests
import polars as pl
import psycopg2
from dotenv import load_dotenv

# 1. Carica le variabili d'ambiente dal file .env (override=True forza l'aggiornamento)
load_dotenv(override=True)

# 🔍 DEBUG: Stampiamo le variabili lette per verificare il corretto caricamento
print(f"DEBUG - Host: {os.getenv('DB_HOST')}")
print(f"DEBUG - Port: {os.getenv('DB_PORT')}")
print(f"DEBUG - User: {os.getenv('DB_USER')}")

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# 2. Coordinate di Hampstead (Londra)
LATITUDE = 51.5556
LONGITUDE = -0.1783

def fetch_weather_data():
    """Scarica i dati meteo storici/correnti da Open-Meteo API"""
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}&"
        f"hourly=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,wind_direction_10m"
    )
    
    print("\nScaricamento dati da Open-Meteo in corso...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    
    # Estraiamo la sezione oraria dei dati
    hourly_data = data["hourly"]
    
    # Convertiamo in un DataFrame Polars
    df = pl.DataFrame({
        "time": hourly_data["time"],
        "temperature_2m": hourly_data["temperature_2m"],
        "relative_humidity_2m": hourly_data["relative_humidity_2m"],
        "precipitation": hourly_data["precipitation"],
        "wind_speed_10m": hourly_data["wind_speed_10m"],
        "wind_direction_10m": hourly_data["wind_direction_10m"]
    })
    
    # Aggiungiamo la colonna location fissa per la nostra tabella
    df = df.with_columns(pl.lit("Hampstead").alias("location"))
    
    print(f"Scaricate {len(df)} righe con successo!")
    return df

def save_to_supabase(df: pl.DataFrame):
    """Salva il DataFrame Polars nel database PostgreSQL su Supabase in modo idempotente"""
    print("Connessione al database Supabase...")
    
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cursor = conn.cursor()
    
    # Estraiamo le righe in modo sicuro e pulito per l'inserimento
    rows = [
        (
            row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        )
        for row in df.select([
            "time", "location", "temperature_2m", 
            "relative_humidity_2m", "precipitation", 
            "wind_speed_10m", "wind_direction_10m"
        ]).iter_rows()
    ]
    
    insert_query = """
        INSERT INTO weather_hampstead 
        (time, location, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m, wind_direction_10m)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (time, location) DO NOTHING;
    """
    
    print("Inserimento dei dati nel database...")
    cursor.executemany(insert_query, rows)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Dati salvati e caricati con successo su Supabase!")

if __name__ == "__main__":
    df_weather = fetch_weather_data()
    save_to_supabase(df_weather)