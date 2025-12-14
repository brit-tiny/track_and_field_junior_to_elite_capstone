"""
run_cleaning.py

This script cleans the 6 combined event files created earlier.
"""
import pandas as pd
from pathlib import Path

from src.cleaning import clean_event_file
from src.utils import ensure_directory

def main():
    print("\n Starting Full Cleaning Pipeline")

    input_dir = Path("../capstone/data/interim/combined")

    output_dir = ensure_directory("../capstone/data/cleaned")

    csv_files = list(input_dir.glob("*csv"))
    print(f"Found {len(csv_files)} files to clean.\n")
    
    if not csv_files:
        print("No combined .csv files found.")
        return
    for csv_path in csv_files:
        event_name = csv_path.stem  
        output_path = output_dir / f"{event_name}.csv"

        print(f"Cleaning file: {csv_path.name}")

        # Perform cleaning
        cleaned_df = clean_event_file(csv_path, event_name)

        # Save cleaned CSV
        cleaned_df.to_csv(output_path, index=False)

        print(f"Saved cleaned file → {output_path}\n")

    print("All files cleaned! Clean versions saved to data/processed/.\n")


if __name__ == "__main__":
    main()

