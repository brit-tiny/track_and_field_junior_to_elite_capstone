# Track and Field Jumps Performance Analysis

This repository contains data scraped from worldathletics.org. The venue locations were isolated and geocode data was found using chatGPT.

## Overview:

This project aims to analyze top performance in long jump, triple jump, and high jump from U18 to senior (professional) level and build trajectory style projections. The project uses scraped competition results, structured data cleaning, a relational SQLite database, and SQL analysis to explore athlete development.

## Data Sources:

- [World Althetics](urlhttps://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior)

- Venue geocoding dataset: compiled using chatGPT

## Data Cleaning:

Steps:
- Removed records with missing DOB or invalid ages
- Standardized event names, gender labels, and age categories
- Removed wind data for high jumb; missing wind fields filled with '0.0' for all other events
- Elevation added to venues and indoor/outdoor flags applied
- Added athlete ages at the time of the meet.

## Getting Started:

NOTE: sqlite3 required. Download "sqlite-tools-win-x64-*.zip" from https://www.sqlite.org/download.html 

1. Clone the repository
2. Set Up the Python Environment
    - Create and activate a virtual environment
        - Windows:  .venv\Scripts\active
        - mac:      source .venv/bin/activate
3. Install dependencies:
    - pip install -r requirements.txt

## Project Structure:
"""
CAPSTONE/
├── data/
│   ├── raw/
│   ├── interim/
│   └── cleaned/  
├── notebooks/
│   ├── 01_scraping.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_sql_analysis.ipynb
│   └──  05_modeling.ipynb
├── src/
│   ├── cleaning.py
│   └──  utils.py
├── sql/
│   └── create_schema.sql
├── visuals/
├── load_data.py
├── load_fact_performace.py
├── track_jumps.db
└── README.

"""

## Loading the Database
sqlite3 track_jumps.db >sql/create_schema.sql

If the database does not exist in bash:
- pyhton load_data.py
- python load_fact_performances.py

#### This will load the database design:

Dimentional tables
- dim_athletes
- dim_events
- dim_meets

Fact tables
- fact_performances

## Run the Analysis Notebooks
1. 02_cleaning.ipynb
    - data cleaning decisions
    - handles missing values and normalization
2. 03_eda.ipynb
    - exploratory analysis
    - performance by age, gender, event, and elevaion
    - core visuals
3. 05_modeling.ipynb
    - athlete progression analysis
    - age category performance change
    - non-predictive projection logic

## Visuals/Figures Reproduction
Charts were created within the notebooks and save locally at execution

Plots created with:
- matplotlib
- seaborn
- custom color palette     "#BC94FF", "#DB8EA7", "#F2B762", "#5F4782"

Analysis Highlights:
Using SQL(joins, aggregations) the analysis explores:
- Performance trendes by age group and gender
- Athlete development from U18 to Senior
- Elevation and indoor/outdoor venues effect on performance results
- Identifying athletes who have competed at all age groups


Limitations:

This project does not take into account:
- an individual athlete's training regimen
- coaching styles
- genetics
- injury history

Status:

Cleaned datasets were finalized on 15/12/2025. All work after this date is analytical and does not modify the underlying data.

## Notes to Reviewer:

- Venue elevation was included where city level data was publicly available. Many venues were only listed by name and country lacking any precise information for geolocation thus resulting in a null elevation. I chose this approach to keep my dataset's integrity while not forcing a false narrative. 
- Raw World Athletics data was scraped and combined by event and gender into interim datasets using Python script prior to exploration, cleaning and analysis.
- This project does not account for:
    - training methods and frequency
    - injury history
    - genetics
    - weather conditions (wind assisted jumps)