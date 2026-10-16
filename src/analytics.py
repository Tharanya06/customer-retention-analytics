import os
import sqlite3
import pandas as pd

DB_PATH = "data/telco_churn.db"
SQL_DIR = "sql/analytics"
OUTPUT_DIR = "data/processed/analytics"

QUERY_FILES = {
    "overall_summary.csv": "overall_summary.sql",
    "segment_analysis.csv": "segment_analysis.sql",
    "charge_analysis.csv": "charge_analysis.sql",
    "high_churn_segments.csv": "high_churn_segments.sql",
}


def run_analytics(db_path: str = DB_PATH, sql_dir: str = SQL_DIR, output_dir: str = OUTPUT_DIR) -> dict[str, pd.DataFrame]:
    """Reads SQL analytics queries from sql_dir, executes against db_path, and exports results to CSVs in output_dir."""
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at '{db_path}'. Run src.pipeline first.")

    os.makedirs(output_dir, exist_ok=True)
    conn = sqlite3.connect(db_path)
    results = {}

    try:
        for csv_filename, sql_filename in QUERY_FILES.items():
            sql_filepath = os.path.join(sql_dir, sql_filename)
            if not os.path.exists(sql_filepath):
                raise FileNotFoundError(f"SQL file not found at '{sql_filepath}'.")

            with open(sql_filepath, "r", encoding="utf-8") as f:
                query = f.read()

            df = pd.read_sql_query(query, conn)
            output_csv_path = os.path.join(output_dir, csv_filename)
            df.to_csv(output_csv_path, index=False)
            results[csv_filename] = df
            print(f"Exported {csv_filename} ({len(df)} rows) to {output_csv_path}")

    finally:
        conn.close()

    return results


if __name__ == "__main__":
    print("=== Running Phase 2 SQL Analytics Runner ===")
    run_analytics()
    print("=== Analytics Runner Completed Successfully ===")
