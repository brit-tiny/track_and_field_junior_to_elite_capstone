import sqlite3
import pandas as pd
from pathlib import Path

print("load_fact_performances.py starting")

# Connect to the database
DB_PATH = Path("track_jumps.db")
conn = sqlite3.connect(DB_PATH)

# Load dim tables
athletes = pd.read_sql(
    "SELECT athlete_id, name, dob FROM dim_athletes", conn
)

events = pd.read_sql(
    "SELECT event_id, event_name, gender FROM dim_events", conn
)

meets = pd.read_sql(
    "SELECT meet_id, venue FROM dim_meets", conn
)

# Load cleaned performance data
CLEANED_DIR = Path("data/cleaned")
csv_files = list(CLEANED_DIR.glob("*.csv"))

print(f"Found {len(csv_files)} cleaned CSV files")

all_facts = []

for csv_file in csv_files:
    print(f"Processing: {csv_file.name}")
    df = pd.read_csv(csv_file)

    # Merge athlete_id
    df = df.merge(
        athletes,
        left_on=["Competitor", "DOB"],
        right_on=["name", "dob"],
        how="inner"
    )

    # Merge event_id
    df = df.merge(
        events,
        left_on=["Event", "Gender"],
        right_on=["event_name", "gender"],
        how="inner"
    )

    # Merge meet_id
    df = df.merge(
        meets,
        left_on="Venue",
        right_on="venue",
        how="inner"
    )

    # Select fact columns
    fact_df = df[[
        "athlete_id",
        "event_id",
        "meet_id",
        "Date",
        "Mark",
        "Age"
    ]].copy()

    fact_df = fact_df.rename(columns={
        "Date": "date",
        "Mark": "mark",
        "Age": "age"
    })

    all_facts.append(fact_df)

# Combining
facts = pd.concat(all_facts, ignore_index=True)

print(f"Total fact rows to insert: {len(facts)}")

facts.to_sql(
    "fact_performances",
    conn,
    if_exists="append",
    index=False
)

print("fact_performances populated")
conn.close()

