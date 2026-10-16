import sqlite3
import pandas as pd
import pytest
from src.analytics import run_analytics


@pytest.fixture
def analytics_test_db(tmp_path):
    """Creates a temporary SQLite database with a controlled fixture covering edge cases:
    - tenure boundaries: 0, 12, 13, 24, 25, 48, 49, 72, 73+
    - TotalCharges NULL (tenure 0) and non-null values
    - Churn Yes/No
    - Zero-denominator handling for segments
    """
    db_path = tmp_path / "test_telco.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE customers (
        customerID TEXT PRIMARY KEY,
        gender TEXT,
        SeniorCitizen INTEGER,
        Partner TEXT,
        Dependents TEXT,
        tenure INTEGER,
        PhoneService TEXT,
        MultipleLines TEXT,
        InternetService TEXT,
        OnlineSecurity TEXT,
        OnlineBackup TEXT,
        DeviceProtection TEXT,
        TechSupport TEXT,
        StreamingTV TEXT,
        StreamingMovies TEXT,
        Contract TEXT,
        PaperlessBilling TEXT,
        PaymentMethod TEXT,
        MonthlyCharges REAL,
        TotalCharges REAL,
        Churn TEXT
    )
    """)

    # Insert controlled records
    # Total records: 10
    # Churned: 4 (ID_01, ID_02, ID_05, ID_08)
    # Retained: 6 (ID_00, ID_03, ID_04, ID_06, ID_07, ID_09, ID_10)
    records = [
        # tenure boundary 0 -> NULL TotalCharges
        ("ID_00", "Female", 0, "No", "No", 0, "Yes", "No", "DSL", "No", "No", "No", "No", "No", "No", "Month-to-month", "Yes", "Electronic check", 20.0, None, "No"),
        # tenure boundary 12 -> band 0–12, churn Yes
        ("ID_01", "Male", 0, "No", "No", 12, "Yes", "No", "Fiber optic", "No", "No", "No", "No", "No", "No", "Month-to-month", "Yes", "Electronic check", 80.0, 960.0, "Yes"),
        # tenure boundary 13 -> band 13–24, churn Yes
        ("ID_02", "Female", 1, "No", "No", 13, "Yes", "Yes", "Fiber optic", "No", "No", "No", "No", "No", "No", "Month-to-month", "Yes", "Electronic check", 90.0, 1170.0, "Yes"),
        # tenure boundary 24 -> band 13–24, churn No
        ("ID_03", "Male", 0, "Yes", "Yes", 24, "Yes", "No", "DSL", "Yes", "Yes", "No", "No", "No", "No", "One year", "No", "Mailed check", 50.0, 1200.0, "No"),
        # tenure boundary 25 -> band 25–48, churn No
        ("ID_04", "Female", 0, "Yes", "No", 25, "Yes", "No", "DSL", "No", "No", "No", "No", "No", "No", "One year", "Yes", "Bank transfer (automatic)", 60.0, 1500.0, "No"),
        # tenure boundary 48 -> band 25–48, churn Yes
        ("ID_05", "Male", 0, "No", "No", 48, "Yes", "Yes", "Fiber optic", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Month-to-month", "Yes", "Electronic check", 100.0, 4800.0, "Yes"),
        # tenure boundary 49 -> band 49–72, churn No
        ("ID_06", "Female", 0, "Yes", "Yes", 49, "Yes", "No", "No", "No internet service", "No internet service", "No internet service", "No internet service", "No internet service", "No internet service", "Two year", "No", "Credit card (automatic)", 25.0, 1225.0, "No"),
        # tenure boundary 72 -> band 49–72, churn No
        ("ID_07", "Male", 1, "Yes", "No", 72, "Yes", "Yes", "Fiber optic", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Two year", "Yes", "Credit card (automatic)", 110.0, 7920.0, "No"),
        # tenure boundary 73 -> band 73+, churn Yes
        ("ID_08", "Female", 0, "No", "No", 73, "Yes", "No", "DSL", "No", "No", "No", "No", "No", "No", "Month-to-month", "No", "Electronic check", 70.0, 5110.0, "Yes"),
        # tenure boundary 80 -> band 73+, churn No
        ("ID_09", "Male", 0, "Yes", "Yes", 80, "Yes", "Yes", "Fiber optic", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Two year", "Yes", "Bank transfer (automatic)", 105.0, 8400.0, "No"),
    ]

    cursor.executemany("""
    INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    conn.commit()
    conn.close()
    return str(db_path)


def test_overall_summary_fixture(analytics_test_db, tmp_path):
    output_dir = tmp_path / "output"
    results = run_analytics(db_path=analytics_test_db, output_dir=str(output_dir))

    df_overall = results["overall_summary.csv"]
    assert len(df_overall) == 1

    row = df_overall.iloc[0]
    # Total customers: 10
    assert row["total_customers"] == 10
    # Churned: ID_01, ID_02, ID_05, ID_08 -> 4
    assert row["churned_customers"] == 4
    # Retained: ID_00, ID_03, ID_04, ID_06, ID_07, ID_09 -> 6
    assert row["retained_customers"] == 6
    # Churn rate: 4 / 10 = 0.4000
    assert row["churn_rate"] == 0.4000

    # MonthlyCharges sums
    # Retained: 20.0 + 50.0 + 60.0 + 25.0 + 110.0 + 105.0 = 370.0
    assert row["retained_monthly_charges_total"] == 370.0
    # Churned: 80.0 + 90.0 + 100.0 + 70.0 = 340.0
    assert row["churned_monthly_charges_total"] == 340.0
    # Avg monthly charges: (370 + 340) / 10 = 71.0
    assert row["avg_monthly_charges"] == 71.0

    # TotalCharges non-null count: 9 out of 10 (ID_00 is NULL)
    assert row["total_charges_non_null_count"] == 9


def test_tenure_boundaries(analytics_test_db, tmp_path):
    output_dir = tmp_path / "output"
    results = run_analytics(db_path=analytics_test_db, output_dir=str(output_dir))

    df_segment = results["segment_analysis.csv"]
    df_tenure = df_segment[df_segment["dimension"] == "TenureBand"].set_index("segment_value")

    # 0–12: ID_00 (0, No), ID_01 (12, Yes) -> Total: 2, Churned: 1
    assert df_tenure.loc["0–12", "total_customers"] == 2
    assert df_tenure.loc["0–12", "churned_customers"] == 1
    assert df_tenure.loc["0–12", "churn_rate"] == 0.5000

    # 13–24: ID_02 (13, Yes), ID_03 (24, No) -> Total: 2, Churned: 1
    assert df_tenure.loc["13–24", "total_customers"] == 2
    assert df_tenure.loc["13–24", "churned_customers"] == 1
    assert df_tenure.loc["13–24", "churn_rate"] == 0.5000

    # 25–48: ID_04 (25, No), ID_05 (48, Yes) -> Total: 2, Churned: 1
    assert df_tenure.loc["25–48", "total_customers"] == 2
    assert df_tenure.loc["25–48", "churned_customers"] == 1
    assert df_tenure.loc["25–48", "churn_rate"] == 0.5000

    # 49–72: ID_06 (49, No), ID_07 (72, No) -> Total: 2, Churned: 0
    assert df_tenure.loc["49–72", "total_customers"] == 2
    assert df_tenure.loc["49–72", "churned_customers"] == 0
    assert df_tenure.loc["49–72", "churn_rate"] == 0.0000

    # 73+: ID_08 (73, Yes), ID_09 (80, No) -> Total: 2, Churned: 1
    assert df_tenure.loc["73+", "total_customers"] == 2
    assert df_tenure.loc["73+", "churned_customers"] == 1
    assert df_tenure.loc["73+", "churn_rate"] == 0.5000


def test_high_churn_ranking_window_function(analytics_test_db, tmp_path):
    output_dir = tmp_path / "output"
    results = run_analytics(db_path=analytics_test_db, output_dir=str(output_dir))

    df_rank = results["high_churn_segments.csv"]
    # Since small fixture has < 30 customers per segment, df_rank should be empty (filtered by total_customers >= 30)
    assert len(df_rank) == 0


def test_zero_denominator_handling(tmp_path):
    """Verifies that an empty table or 0-customer segment returns 0.0 churn_rate without SQL error."""
    db_path = tmp_path / "empty_telco.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE customers (
        customerID TEXT PRIMARY KEY,
        gender TEXT,
        SeniorCitizen INTEGER,
        Partner TEXT,
        Dependents TEXT,
        tenure INTEGER,
        PhoneService TEXT,
        MultipleLines TEXT,
        InternetService TEXT,
        OnlineSecurity TEXT,
        OnlineBackup TEXT,
        DeviceProtection TEXT,
        TechSupport TEXT,
        StreamingTV TEXT,
        StreamingMovies TEXT,
        Contract TEXT,
        PaperlessBilling TEXT,
        PaymentMethod TEXT,
        MonthlyCharges REAL,
        TotalCharges REAL,
        Churn TEXT
    )
    """)
    conn.commit()
    conn.close()

    output_dir = tmp_path / "output"
    results = run_analytics(db_path=str(db_path), output_dir=str(output_dir))

    df_overall = results["overall_summary.csv"]
    assert len(df_overall) == 1
    assert df_overall.iloc[0]["total_customers"] == 0
    assert df_overall.iloc[0]["churn_rate"] == 0.0
