# Track and Field Jumps Performance Analysis

This repository contains data scraped from worldathletics.org. The venue locations were isolated and geocode data was found using chatGPT.

## Overview:

This project aims to analyze top performance in long jump, triple jump, and high jump from U18 to senior (professional) level and build trajectory style projections. The project uses scraped competition results, structured data cleaning, a relational SQLite database, and SQL analysis to explore athlete development.

## Data Sources:

- [World Althetics](urlhttps://worldathletics.org/records/toplists/jumps/high-jump/all/women/senior/2025?regionType=world&page=1&bestResultsOnly=true&maxResultsByCountry=all&eventId=10229526&ageCategory=senior)

- Venue geocoding dataset: compiled using chatGPT

## Project Structure:
"""
CAPSTONE/
├── data/
|   ├── raw/
|   ├── interim/
|   └── cleaned/  
├── notebooks/
|   ├── 01_scraping.ipynb
|   ├── 02_cleaning.ipynb
|   ├── 03_eda.ipynb
|   ├── 04_sql_analysis.ipynb
|   └──  05_modeling.ipynb
├── src/
|   ├── cleaning.py
|   └──  utils.py
├── sql/
|   └── create_schema.sql
├── visuals/
├── load_data.py
├── load_fact_performace.py
├── track_jumps.db
└── README.

"""
Data Cleaning:

Steps:
- Removed records with missing DOB or invalid ages
- Standardized event names, gender labels, and age categories
- Removed wind data for high jumb; missing wind fields filled with '0.0' for all other events
- Elevation added to venues and indoor/outdoor flags applied
- Added athlete ages at the time of the meet.

Status:

Cleaned datasets were finalized on 15/12/2025. All work after this date is analytical and does not modify the underlying data.

Database Design:

Dimentional tables
- dim_athletes
- dim_events
- dim_meets

Fact tables
- fact_performances

Analysis Highlights:
Using SQL(joins, aggregations) the analysis explores:
- Performance trendes by age group and gender
- Athlete development from U18 to Senior
- Elevation and indoor/outdoor venues effect on performance results
- Identifying athletes who have competed at all age groups

Key Findings:


Limitations:

This project does not take into account:
- an individual athlete's training regimen
- coaching styles
- genetics
- injury history

How to Run:

sqlite3 track_jumps.db >sql/create_schema.sql
python load_data.py
python load_fact_performances.py




Missing Elevation Data

Venue elevation was included where city level data was publicly available. Many venues were only listed by name and country lacking any precise information for geolocation, thus resulting in a null elevation. I chose this approach to keep my dataset's integrity while not forcing a false narrative. 


Raw World Athletics data was scraped and combined by event and gender into interim datasets using Python script prior to exploration, cleaning and analysis.