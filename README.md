# HW04 - Data Science vs PM2.5

## Project Overview

This project analyzes PM2.5 air pollution in Chiang Mai, Thailand using air-quality and weather data from Open-Meteo.

The project investigates seasonal PM2.5 patterns, relationships between PM2.5 and weather conditions, and whether dangerous PM2.5 conditions can be predicted one day in advance.

A day is classified as dangerous when the daily mean PM2.5 concentration exceeds Thailand's 24-hour standard of 37.5 µg/m³.

## Study Area

- Location: Chiang Mai, Thailand
- Latitude: 18.80
- Longitude: 99.00
- Timezone: Asia/Bangkok
- Study period: 2023-01-01 to 2026-08-31

## Data Sources

Data are obtained programmatically from Open-Meteo APIs.

1. Open-Meteo Air Quality API
   - PM2.5
   - PM10
   - Carbon monoxide
   - Dust

2. Open-Meteo Historical Weather API
   - Temperature
   - Relative humidity
   - Wind speed
   - Wind direction
   - Precipitation
   - Surface pressure

Raw API responses are saved in `data/raw/`.

## Project Structure

    .
    ├── fetch_data.py
    ├── analysis.ipynb
    ├── requirements.txt
    ├── README.md
    ├── data/
    │   ├── raw/
    │   │   ├── open_meteo_air_quality.json
    │   │   └── open_meteo_weather_archive.json
    │   └── processed/
    │       ├── hourly_merged.csv
    │       ├── daily_merged.csv
    │       └── modeling_dataset.csv
    └── outputs/
        ├── figures/
        └── results/

## How to Reproduce

### 1. Install dependencies

    pip install -r requirements.txt

### 2. Download and prepare the data

    python fetch_data.py

This downloads the Open-Meteo data and creates the hourly and daily processed datasets.

### 3. Run the analysis

Open and run:

    analysis.ipynb

Run all notebook cells from top to bottom.

## Analysis

The project includes:

- PM2.5 descriptive statistics
- PM2.5 time-series analysis
- Monthly exceedance-rate analysis
- Weather and PM2.5 correlation analysis
- Next-day dangerous PM2.5 prediction
- Persistence baseline
- Logistic Regression
- Random Forest
- Accuracy, Precision, Recall and F1-score
- Confusion matrix
- False-negative error analysis

## Main Findings

PM2.5 shows a strong seasonal pattern in Chiang Mai, with the highest exceedance rates occurring during February-April.

March had the highest exceedance rate in the study data.

Relative humidity showed the strongest negative correlation with PM2.5 among the selected weather variables.

For next-day classification, Logistic Regression achieved high recall for dangerous days, while the Persistence Baseline achieved the highest F1-score among the evaluated approaches.

False-negative analysis showed that missed dangerous days tended to occur when PM2.5 increased rapidly from one day to the next.

## Limitations

The Open-Meteo data are gridded/model-based environmental data and may differ from measurements at individual ground stations.

The analysis represents one coordinate in Chiang Mai and does not capture all spatial variation across the province.

External factors such as wildfire hotspots, agricultural burning, traffic emissions and transboundary pollution were not directly included in the prediction models.

## Ground Truth Check

One overlapping observation will be compared with Air4Thai PM2.5 data as an external ground-truth sanity check.

## Author

HW04 - Data Science vs PM2.5
