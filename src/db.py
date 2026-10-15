import os
import sqlite3
import pandas as pd

DEFAULT_DB_PATH = os.path.join("data", "telco_churn.db")
DEFAULT_SCHEMA_PATH = os.path.join("sql", "schema.sql")


def init_db(db_path: str = DEFAULT_DB_PATH, schema_path: str = DEFAULT_SCHEMA_PATH) -> None:
    """Creates database tables according to schema.sql if not existing."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                conn.executescript(f.read())


def load_data_to_sqlite(df: pd.DataFrame, db_path: str = DEFAULT_DB_PATH, table_name: str = "customers") -> int:
    """
    Loads DataFrame into SQLite database table.
    Ensures idempotency by using INSERT OR REPLACE based on Primary Key (customerID).
    Re-running does not produce duplicate records.
    Returns total rows count in the table after insertion.
    """
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Ensure schema table exists
        if os.path.exists(DEFAULT_SCHEMA_PATH):
            with open(DEFAULT_SCHEMA_PATH, "r") as f:
                cursor.executescript(f.read())

        records = df.to_dict(orient="records")
        columns = list(df.columns)
        placeholders = ", ".join([":" + col for col in columns])
        cols_str = ", ".join([f'"{col}"' for col in columns])

        sql = f"INSERT OR REPLACE INTO {table_name} ({cols_str}) VALUES ({placeholders})"
        cursor.executemany(sql, records)
        conn.commit()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

    return count
