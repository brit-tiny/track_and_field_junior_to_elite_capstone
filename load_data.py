import sqlite3
import pandas as pd
from pathlib import Path

#-----DIM-ATHLETES-----
# Path to SQL database
DB_PATH = Path("track_jumps.db")

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("Connected to SQLite database:", DB_PATH.resolve())

CLEANED_DIR = Path("data/cleaned")

csv_files = list(CLEANED_DIR.glob("*.csv"))
print(f"Found {len(csv_files)} cleaned CSV files.")

all_athletes =[]

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Select columns
    athlete_df = df[["Competitor", "DOB", "Nat"]].copy()
    athlete_df = athlete_df.rename(columns={
        "Competitor": "name",
        "DOB": "dob",
        "Nat": "nat"
    })

    all_athletes.append(athlete_df)

# Combine
athlete_df = (
    pd.concat(all_athletes, ignore_index=True)
        .drop_duplicates(subset=["name", "dob"])
)

print(f"Unique athletes to insert: {len(athlete_df)}")

cursor.execute("DELETE FROM dim_athletes;")
conn.commit()

# Insert athletes into dim_athletes
athlete_df.to_sql(
    "dim_athletes",
    conn,
    if_exists="append",
    index=False
)

print("dim_athletes table populated.")

#-----DIM_EVENTS-----
all_events = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    event_df = df[["Event", "Gender"]].copy()
    event_df = event_df.rename(columns={
        "Event": "event_name",
        "Gender": "gender"
    })

    all_events.append(event_df)

event_df = (
    pd.concat(all_events, ignore_index=True)
        .drop_duplicates()
)

print(f"Unique events to insert: {len(event_df)}")

event_df.to_sql(
    "dim_events",
    conn,
    if_exists="append",
    index=False
)

print("dim_events table populated.")

#-----DIM_MEETS-----
print("Starting dim_meets block.")

cursor.execute("DELETE FROM dim_meets;")
conn.commit()

venues_path = Path("data/interim/venues/geocoded_venues.csv")
venues_df = pd.read_csv(venues_path)

venues_df = venues_df[["Venue", "elevation"]].drop_duplicates()

all_meets = []

for csv_file in csv_files:
    df = pd.read_csv(csv_file)

    # Selecting the columns
    meet_df = df[["Venue", "is_indoor"]].copy()
    all_meets.append(meet_df)

meet_df = (
    pd.concat(all_meets, ignore_index=True)
        .drop_duplicates()
)

meet_df = meet_df.merge(
    venues_df,
    on="Venue",
    how="left"
)
    
# Drop missing elevation rows
meet_df = meet_df.dropna(subset=["elevation"])

meet_df = meet_df.rename(columns={
    "Venue": "venue"
})

print(f"Unique meets to insert: {len(meet_df)}")

meet_df.to_sql(
    "dim_meets",
    conn,
    if_exists="append",
    index=False
)

print("dim_meets table populated.")