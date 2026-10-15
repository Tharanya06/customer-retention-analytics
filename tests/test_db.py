import sqlite3
import pandas as pd
from src.clean import clean_data
from src.db import load_data_to_sqlite


def test_repeated_database_loading(tmp_path):
    db_file = tmp_path / "test_telco.db"

    raw_df = pd.DataFrame({
        "customerID": ["1111-AAA", "2222-BBB"],
        "gender": ["Female", "Male"],
        "SeniorCitizen": [0, 0],
        "Partner": ["Yes", "No"],
        "Dependents": ["No", "No"],
        "tenure": [1, 12],
        "PhoneService": ["Yes", "Yes"],
        "MultipleLines": ["No", "No"],
        "InternetService": ["No", "DSL"],
        "OnlineSecurity": ["No internet service", "Yes"],
        "OnlineBackup": ["No internet service", "No"],
        "DeviceProtection": ["No internet service", "Yes"],
        "TechSupport": ["No internet service", "No"],
        "StreamingTV": ["No internet service", "No"],
        "StreamingMovies": ["No internet service", "No"],
        "Contract": ["Month-to-month", "One year"],
        "PaperlessBilling": ["No", "Yes"],
        "PaymentMethod": ["Mailed check", "Electronic check"],
        "MonthlyCharges": [20.0, 50.0],
        "TotalCharges": ["20.0", "600.0"],
        "Churn": ["No", "No"],
    })

    cleaned_df = clean_data(raw_df)

    # First load
    count1 = load_data_to_sqlite(cleaned_df, db_path=str(db_file))
    assert count1 == 2

    # Second load (repeated operation)
    count2 = load_data_to_sqlite(cleaned_df, db_path=str(db_file))
    assert count2 == 2

    # Verify directly via sqlite query
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_rows = cursor.fetchone()[0]
        assert total_rows == 2
