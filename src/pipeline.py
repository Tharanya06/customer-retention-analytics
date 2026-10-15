import os
import pandas as pd

from src.download import download_raw_data, DEFAULT_OUTPUT_PATH as RAW_PATH
from src.clean import clean_data, save_cleaned_data, DEFAULT_PROCESSED_PATH as PROCESSED_PATH
from src.db import load_data_to_sqlite, DEFAULT_DB_PATH as DB_PATH
from src.report import generate_report, DEFAULT_REPORT_PATH as REPORT_PATH


def run_pipeline():
    print("=== Step 1: Downloading Raw Data ===")
    if not os.path.exists(RAW_PATH):
        download_raw_data(output_path=RAW_PATH)
        print(f"Downloaded raw dataset to {RAW_PATH}")
    else:
        print(f"Raw dataset already exists at {RAW_PATH}")

    raw_df = pd.read_csv(RAW_PATH)
    print(f"Raw dataset shape: {raw_df.shape}")

    print("\n=== Step 2: Cleaning & Validating Data ===")
    cleaned_df = clean_data(raw_df)
    save_cleaned_data(cleaned_df, PROCESSED_PATH)
    print(f"Saved cleaned dataset to {PROCESSED_PATH} (Shape: {cleaned_df.shape})")

    print("\n=== Step 3: Loading Data into SQLite ===")
    db_count = load_data_to_sqlite(cleaned_df, DB_PATH)
    print(f"Loaded dataset into SQLite DB {DB_PATH}. Total DB rows: {db_count}")

    print("\n=== Step 4: Generating Data Quality Report ===")
    report_text = generate_report(raw_df, cleaned_df, db_count, REPORT_PATH)
    print(f"Data Quality Report saved to {REPORT_PATH}\n")
    print(report_text)


if __name__ == "__main__":
    run_pipeline()
