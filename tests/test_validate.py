import pytest
import pandas as pd
from src.validate import (
    validate_schema,
    validate_customer_ids,
    validate_churn_labels,
    validate_non_negative_numeric,
    validate_dataset,
)


def create_sample_df():
    return pd.DataFrame({
        "customerID": ["7590-VHVEG", "5575-GNVDE"],
        "gender": ["Female", "Male"],
        "SeniorCitizen": [0, 0],
        "Partner": ["Yes", "No"],
        "Dependents": ["No", "No"],
        "tenure": [1, 34],
        "PhoneService": ["No", "Yes"],
        "MultipleLines": ["No phone service", "No"],
        "InternetService": ["DSL", "DSL"],
        "OnlineSecurity": ["No", "Yes"],
        "OnlineBackup": ["Yes", "No"],
        "DeviceProtection": ["No", "Yes"],
        "TechSupport": ["No", "No"],
        "StreamingTV": ["No", "No"],
        "StreamingMovies": ["No", "No"],
        "Contract": ["Month-to-month", "One year"],
        "PaperlessBilling": ["Yes", "No"],
        "PaymentMethod": ["Electronic check", "Mailed check"],
        "MonthlyCharges": [29.85, 56.95],
        "TotalCharges": ["29.85", "1889.5"],
        "Churn": ["No", "No"],
    })


def test_validate_schema_missing_column():
    df = create_sample_df().drop(columns=["gender"])
    with pytest.raises(ValueError, match="missing required columns"):
        validate_schema(df)


def test_validate_customer_ids_empty():
    df = create_sample_df()
    df.loc[0, "customerID"] = " "
    with pytest.raises(ValueError, match="missing or empty string"):
        validate_customer_ids(df)


def test_validate_customer_ids_duplicate():
    df = create_sample_df()
    df.loc[1, "customerID"] = "7590-VHVEG"
    with pytest.raises(ValueError, match="Duplicate customerID"):
        validate_customer_ids(df)


def test_validate_churn_labels_invalid():
    df = create_sample_df()
    df.loc[0, "Churn"] = "Maybe"
    with pytest.raises(ValueError, match="Invalid Churn values"):
        validate_churn_labels(df)


def test_validate_non_negative_numeric_negative_tenure():
    df = create_sample_df()
    df.loc[0, "tenure"] = -5
    with pytest.raises(ValueError, match="Negative values found"):
        validate_non_negative_numeric(df)


def test_validate_non_negative_numeric_negative_monthly_charges():
    df = create_sample_df()
    df.loc[0, "MonthlyCharges"] = -10.0
    with pytest.raises(ValueError, match="Negative values found"):
        validate_non_negative_numeric(df)


def test_validate_dataset_valid():
    df = create_sample_df()
    # Should not raise any exception
    validate_dataset(df)
