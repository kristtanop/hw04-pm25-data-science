
import os
import json
import requests
import pandas as pd

# --------------------------------
# Configuration
# --------------------------------

LATITUDE = 18.80
LONGITUDE = 99.00

START_DATE = "2023-01-01"
END_DATE = "2026-08-31"

AIR_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)


# --------------------------------
# 1. Download Air Quality
# --------------------------------

air_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": "pm2_5,pm10,carbon_monoxide,dust",
    "start_date": START_DATE,
    "end_date": END_DATE,
    "timezone": "Asia/Bangkok"
}

air_response = requests.get(
    AIR_URL,
    params=air_params,
    timeout=60
)

air_response.raise_for_status()
air_data = air_response.json()

with open(
    "data/raw/open_meteo_air_quality.json",
    "w"
) as f:
    json.dump(air_data, f, indent=4)

print("Air-quality data downloaded.")


# --------------------------------
# 2. Download Weather
# --------------------------------

weather_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": (
        "temperature_2m,"
        "relative_humidity_2m,"
        "wind_speed_10m,"
        "wind_direction_10m,"
        "precipitation,"
        "surface_pressure"
    ),
    "start_date": START_DATE,
    "end_date": END_DATE,
    "timezone": "Asia/Bangkok"
}

weather_response = requests.get(
    WEATHER_URL,
    params=weather_params,
    timeout=60
)

weather_response.raise_for_status()
weather_data = weather_response.json()

with open(
    "data/raw/open_meteo_weather_archive.json",
    "w"
) as f:
    json.dump(weather_data, f, indent=4)

print("Weather data downloaded.")


# --------------------------------
# 3. Convert to DataFrames
# --------------------------------

air_df = pd.DataFrame(air_data["hourly"])
weather_df = pd.DataFrame(weather_data["hourly"])

air_df["time"] = pd.to_datetime(air_df["time"])
weather_df["time"] = pd.to_datetime(weather_df["time"])

print("Air rows:", len(air_df))
print("Weather rows:", len(weather_df))


# --------------------------------
# 4. Merge
# --------------------------------

hourly_df = pd.merge(
    air_df,
    weather_df,
    on="time",
    how="inner"
)

print("Rows after join:", len(hourly_df))

hourly_df.to_csv(
    "data/processed/hourly_merged.csv",
    index=False
)


# --------------------------------
# 5. Aggregate Hourly -> Daily
# --------------------------------

hourly_df["date"] = hourly_df["time"].dt.date

daily_df = hourly_df.groupby("date").agg({
    "pm2_5": "mean",
    "pm10": "mean",
    "carbon_monoxide": "mean",
    "dust": "mean",
    "temperature_2m": "mean",
    "relative_humidity_2m": "mean",
    "wind_speed_10m": "mean",
    "wind_direction_10m": "mean",
    "precipitation": "sum",
    "surface_pressure": "mean"
}).reset_index()

daily_df["date"] = pd.to_datetime(daily_df["date"])

daily_df.to_csv(
    "data/processed/daily_merged.csv",
    index=False
)

print("Daily rows:", len(daily_df))
print("Date range:", daily_df["date"].min(), "to", daily_df["date"].max())

print("\nData acquisition completed successfully.")
