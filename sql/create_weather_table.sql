CREATE TABLE IF NOT EXISTS weather_hampstead (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    location VARCHAR(100) NOT NULL DEFAULT 'Hampstead',
    temperature_2m DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION,
    wind_direction_10m DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT unique_time_location UNIQUE (time, location)
);