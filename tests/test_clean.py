import pandas as pd
import numpy as np
import pytest
from src.clean import clean_data


def test_clean_data_whitespace_normalization_and_types():
    raw_data = pd.DataFrame({
        "customerID": [" 1111-AAA ", "2222-BBB", "3333-CCC"],
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

    # Check customerID whitespace normalized
    assert cleaned_df.loc[0, "customerID"] == "1111-AAA"

    # Check TotalCharges conversion
    assert pd.isna(cleaned_df.loc[0, "TotalCharges"])
    assert cleaned_df.loc[1, "TotalCharges"] == 600.0
    assert cleaned_df.loc[2, "TotalCharges"] == 1920.0

    # Ensure missing value is NaN and not replaced with 0
    assert cleaned_df.loc[0, "TotalCharges"] != 0
    assert isinstance(cleaned_df["TotalCharges"].dtype, (np.dtype, type(np.float64)))


@pytest.mark.parametrize("inf_val", [" inf ", " -inf ", "\tInfinity\t", "-Infinity"])
def test_clean_data_rejects_infinite_total_charges(inf_val):
    raw_data = pd.DataFrame({
        "customerID": ["1111-AAA"],
        "gender": ["Female"],
        "SeniorCitizen": [0],
        "Partner": ["Yes"],
        "Dependents": ["No"],
        "tenure": [1],
        "PhoneService": ["Yes"],
        "MultipleLines": ["No"],
        "InternetService": ["No"],
        "OnlineSecurity": ["No internet service"],
        "OnlineBackup": ["No internet service"],
        "DeviceProtection": ["No internet service"],
        "TechSupport": ["No internet service"],
        "StreamingTV": ["No internet service"],
        "StreamingMovies": ["No internet service"],
        "Contract": ["Two year"],
        "PaperlessBilling": ["No"],
        "PaymentMethod": ["Mailed check"],
        "MonthlyCharges": [20.0],
        "TotalCharges": [inf_val],
        "Churn": ["No"],
    })

    with pytest.raises(ValueError, match="infinite values"):
        clean_data(raw_data)
