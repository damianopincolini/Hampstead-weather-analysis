# 1. Introduction

[Provide a brief description of the analysis object, domain context, and the primary data sources used.]

## 1.1. Project Goal
[Define the main objective of the project, the expected deliverables, and the target performance or business impact.]

## 1.2. Problem Definition and Challenges
[Detail the machine learning task: target variable nature, class distribution (frequent/infrequent data), data quality issues, encoding requirements, and any specific analytical challenges.]

## 1.3. Contextual Background
[Explain why this topic is relevant, interesting, or critical from a technical, scientific, or operational perspective.]

The data source is Open-Meteo (https://open-meteo.com/en/docs) which is an open-source API (application programming interface) highly reliable designed to provide with weather forecast and weather time series.
Open-Meteo is well suited to these kind of data engineering e MLOps projects since:

1. it's free and does not require mandatory API keys (No-Auth) which simplies both ingestion script coding and .env file configuration.

2. World-wide coverage.

3. It's ideal for time-series ingestion. It's pretty suited to create an hystorical and incremental database on Supabase.


To quey Opn-Meteo, a python script will make an HTTP GET call provide the coordinates the exactly localize the area of interest (Hampstead). We'll also specify daily weather parameters we want to study, such as air temperature (temperature_2m), relative humidity (relative_humidity_2m), precipitation (precipitation) and wind and direction speed (wind_speed_10m, wind_direction_10m).
