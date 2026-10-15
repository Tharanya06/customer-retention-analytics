import pandas as pd
import numpy as np
from src.clean import clean_data


def test_clean_data_total_charges_missing_and_numeric():
    raw_data = pd.DataFrame({
        "customerID": ["1111-AAA", "2222-BBB", "3333-CCC"],
        "gender": ["Female", "Male", "Male"],
        "SeniorCitizen": [0, 0, 1],
        "Partner": ["Yes", "No", "No"],
        "Dependents": ["No", "No", "No"],
        "tenure": [0, 12, 24],
        "PhoneService": ["Yes", "Yes", "Yes"],
        "MultipleLines": ["No", "No", "Yes"],
        "InternetService": ["No", "DSL", "Fiber optic"],
        "OnlineSecurity": ["No internet service", "Yes", "No"],
        "OnlineBackup": ["No internet service", "No", "Yes"],
        "DeviceProtection": ["No internet service", "Yes", "No"],
        "TechSupport": ["No internet service", "No", "Yes"],
        "StreamingTV": ["No internet service", "No", "Yes"],
        "StreamingMovies": ["No internet service", "No", "Yes"],
        "Contract": ["Two year", "Month-to-month", "One year"],
        "PaperlessBilling": ["No", "Yes", "Yes"],
        "PaymentMethod": ["Mailed check", "Electronic check", "Bank transfer"],
        "MonthlyCharges": [20.0, 50.0, 80.0],
        "TotalCharges": [" ", "600.0", "1920.0"],
        "Churn": ["No", "No", "Yes"],
    })

    cleaned_df = clean_data(raw_data)

    # Check row count preserved (no rows dropped)
    assert len(cleaned_df) == 3

    # Check TotalCharges conversion
    assert pd.isna(cleaned_df.loc[0, "TotalCharges"])
    assert cleaned_df.loc[1, "TotalCharges"] == 600.0
    assert cleaned_df.loc[2, "TotalCharges"] == 1920.0

    # Ensure missing value is NaN and not replaced with 0
    assert cleaned_df.loc[0, "TotalCharges"] != 0
    assert isinstance(cleaned_df["TotalCharges"].dtype, (np.dtype, type(np.float64)))
