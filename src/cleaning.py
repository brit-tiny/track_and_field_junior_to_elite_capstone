"""
cleaning.py

This script runs a cleaning function for all event .csv files scraped from worldathletics.org. I built this for
a consistent, repeatable workflow after many iterations of a manual cleaning process.

With 18 files (3-events, 2-genders, and 3-age groups) combined into 6 running this script processes all of them 
at once and saves the cleaned versions into the data/interim/cleaned folder.
"""

import pandas as pd

def calculate_age(dob, meet_date):
    # Returns the age at the time of competition.
    if pd.isna(dob) or pd.isna(meet_date):
        return pd.NA
    age = meet_date.year - dob.year
    if (meet_date.month, meet_date.day) < (dob.month, dob.day):
        age -= 1
    return age


# Clean Event File
def clean_event_file(filepath, event_name):

    df = pd.read_csv(filepath)

    df.columns = [c.strip() for c in df.columns]

    # 1. Rename Unnamed: 5 to Country

    if "Unnamed: 5" in df.columns:
        df = df.rename(columns={"Unnamed: 5": "Nat"})

    # 2. Remove unnecessary columns
    drop_cols = ["Pos", "Results Score", "Unnamed: 7", "Rank"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")

    # 3. WIND column: Remove WIND for high jump only, insert 0.0 for all other events where its missing
    if "high" in event_name.lower():
        df = df.drop(columns=[c for c in ["WIND"] if c in df.columns], errors="ignore")
    else:
        if "WIND" in df.columns:
            df["WIND"] = df["WIND"].fillna(0.0)
        else:
            df["WIND"] = 0.0

    # 4. Remove athletes with no DOB

    if "DOB" in df.columns:
        df = df[df["DOB"].notna()]

    # Convert date fields

    df["DOB"] = pd.to_datetime(df["DOB"], errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df[df["DOB"].notna()]

    # Calculate age

    df["Age"] = df.apply(lambda row: calculate_age(row["DOB"], row["Date"]), axis=1)
    df = df[df["Age"] >= 10]

    # 5. Gender Column

    if "Gender" not in df.columns:
        df["Gender"] = "M" if "m_" in filepath.name.lower() else "F"

    # 6. Identify indoor meets (i)

    if "Venue" in df.columns:
        df["is_indoor"] = (
            df["Venue"]
            .astype(str)
            .str.contains("(i)", case=False, regex=False)
            .fillna(False)
            .astype(int)
        )
    else:
        df["is_indoor"] = 0


    return df


