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

    # Insert controlled records (21 column values per tuple)
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
    INSERT INTO customers (customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    assert row["total_customers"] == 10
    assert row["churned_customers"] == 4
    assert row["retained_customers"] == 6
    assert row["churn_rate"] == 0.4000
    assert row["retained_monthly_charges_total"] == 370.0
    assert row["churned_monthly_charges_total"] == 340.0
    assert row["avg_monthly_charges"] == 71.0
    assert row["total_charges_non_null_count"] == 9


def test_tenure_boundaries(analytics_test_db, tmp_path):
    output_dir = tmp_path / "output"
    results = run_analytics(db_path=analytics_test_db, output_dir=str(output_dir))

    df_segment = results["segment_analysis.csv"]
    df_tenure = df_segment[df_segment["dimension"] == "TenureBand"].set_index("segment_value")

    assert df_tenure.loc["0–12", "total_customers"] == 2
    assert df_tenure.loc["0–12", "churned_customers"] == 1
    assert df_tenure.loc["0–12", "churn_rate"] == 0.5000

    assert df_tenure.loc["13–24", "total_customers"] == 2
    assert df_tenure.loc["13–24", "churned_customers"] == 1
    assert df_tenure.loc["13–24", "churn_rate"] == 0.5000

    assert df_tenure.loc["25–48", "total_customers"] == 2
    assert df_tenure.loc["25–48", "churned_customers"] == 1
    assert df_tenure.loc["25–48", "churn_rate"] == 0.5000

    assert df_tenure.loc["49–72", "total_customers"] == 2
    assert df_tenure.loc["49–72", "churned_customers"] == 0
    assert df_tenure.loc["49–72", "churn_rate"] == 0.0000

    assert df_tenure.loc["73+", "total_customers"] == 2
    assert df_tenure.loc["73+", "churned_customers"] == 1
    assert df_tenure.loc["73+", "churn_rate"] == 0.5000


def test_ranking_threshold_ordering_and_ties(tmp_path):
    """Strengthened ranking test using a non-empty dataset.
    Verifies:
    1. Segments with total_customers < 30 (e.g. 29) are excluded.
    2. Segments with total_customers >= 30 are included.
    3. Ranks are assigned in descending order of churn_rate.
    4. Segments with tied churn_rate receive equal churn_rank.
    """
    db_path = tmp_path / "ranking_test.db"
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

    records = []
    cid = 1

    # High Churn Group: Contract='Month-to-month' AND InternetService='Fiber optic' -> 30 customers, 24 churned (churn_rate = 0.8000)
    # Also Contract + PaymentMethod combo: Contract='Month-to-month' | Electronic check -> 30 customers, 24 churned (churn_rate = 0.8000)
    # Both combos will tie at 0.8000 churn_rate and get rank 1.
    for i in range(30):
        churn = "Yes" if i < 24 else "No"
        records.append((f"C{cid}", "Female", 0, "No", "No", 10, "Yes", "No", "Fiber optic", "No", "No", "No", "No", "No", "No", "Month-to-month", "Yes", "Electronic check", 90.0, 900.0, churn))
        cid += 1

    # Medium Churn Group: Contract='One year' -> 30 customers, 15 churned (churn_rate = 0.5000)
    for i in range(30):
        churn = "Yes" if i < 15 else "No"
        records.append((f"C{cid}", "Male", 0, "No", "No", 20, "Yes", "No", "DSL", "No", "No", "No", "No", "No", "No", "One year", "Yes", "Mailed check", 50.0, 1000.0, churn))
        cid += 1

    # Sub-threshold Group: Contract='Two year' -> 29 customers, 25 churned (churn_rate = 0.8621, but count = 29 < 30 -> EXCLUDED)
    for i in range(29):
        churn = "Yes" if i < 25 else "No"
        records.append((f"C{cid}", "Male", 0, "No", "No", 60, "Yes", "No", "No", "No internet service", "No internet service", "No internet service", "No internet service", "No internet service", "No internet service", "Two year", "Yes", "Bank transfer (automatic)", 20.0, 1200.0, churn))
        cid += 1

    cursor.executemany("""
    INSERT INTO customers (customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    conn.commit()
    conn.close()

    output_dir = tmp_path / "output"
    results = run_analytics(db_path=str(db_path), output_dir=str(output_dir))

    df_rank = results["high_churn_segments.csv"]

    # Check 1: 29-customer Contract ('Two year') is EXCLUDED from ranking
    all_values = df_rank["segment_value"].tolist()
    assert "Two year" not in all_values

    # Check 2: Top tied churn_rate segments (0.8000) get rank 1
    top_ranks = df_rank[df_rank["churn_rate"] == 0.8000]
    assert len(top_ranks) >= 2
    assert (top_ranks["churn_rank"] == 1).all()

    # Check 3: Lower churn_rate segment (One year at 0.5000) gets a lower rank (rank > 1)
    one_yr = df_rank[df_rank["segment_value"] == "One year"]
    assert len(one_yr) == 1
    assert one_yr["churn_rank"].values[0] > 1


def test_empty_table_aggregate_behavior(tmp_path):
    """Verifies empty-table policy across overall_summary and charge_analysis:
    - total_customers: 0
    - churned_customers, retained_customers: 0
    - churn_rate: 0.0
    - retained_monthly_charges_total, churned_monthly_charges_total: 0.0
    - total_charges_non_null_count: 0
    - avg_monthly_charges, avg_total_charges, total_charges_sum: NULL (NaN/None)
    """
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

    # Test overall_summary empty table behavior
    df_overall = results["overall_summary.csv"]
    assert len(df_overall) == 1
    row_o = df_overall.iloc[0]

    assert row_o["total_customers"] == 0
    assert row_o["churned_customers"] == 0
    assert row_o["retained_customers"] == 0
    assert row_o["churn_rate"] == 0.0
    assert row_o["retained_monthly_charges_total"] == 0.0
    assert row_o["churned_monthly_charges_total"] == 0.0
    assert row_o["total_charges_non_null_count"] == 0
    assert pd.isna(row_o["avg_monthly_charges"])
    assert pd.isna(row_o["avg_total_charges"])

    # Test charge_analysis empty table behavior
    df_charge = results["charge_analysis.csv"]
    row_c = df_charge[df_charge["dimension"] == "Overall"].iloc[0]

    assert row_c["total_customers"] == 0
    assert row_c["retained_monthly_charges_total"] == 0.0
    assert row_c["churned_monthly_charges_total"] == 0.0
    assert row_c["total_charges_non_null_count"] == 0
    assert pd.isna(row_c["avg_monthly_charges"])
    assert pd.isna(row_c["total_charges_sum"])
