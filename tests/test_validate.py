import numpy as np
import pandas as pd
import pytest
from src.validate import (
    validate_schema,
    validate_customer_ids,
    validate_churn_labels,
    validate_senior_citizen,
    validate_tenure,
    validate_monthly_charges,
    validate_total_charges,
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
    with pytest.raises(ValueError, match="empty string"):
        validate_customer_ids(df)


def test_validate_customer_ids_null():
    df = create_sample_df()
    df.loc[0, "customerID"] = None
    with pytest.raises(ValueError, match="missing or null"):
        validate_customer_ids(df)


def test_validate_customer_ids_whitespace_duplicate():
    df = create_sample_df()
    df.loc[0, "customerID"] = " 7590-VHVEG "
    df.loc[1, "customerID"] = "7590-VHVEG"
    with pytest.raises(ValueError, match="Duplicate customerID"):
        validate_customer_ids(df)


def test_validate_churn_labels_invalid():
    df = create_sample_df()
    df.loc[0, "Churn"] = "Maybe"
    with pytest.raises(ValueError, match="Invalid Churn values"):
        validate_churn_labels(df)


def test_validate_churn_labels_missing():
    df = create_sample_df()
    df.loc[0, "Churn"] = None
    with pytest.raises(ValueError, match="null or missing"):
        validate_churn_labels(df)


def test_validate_senior_citizen_invalid():
    df = create_sample_df()
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(object)
    df.loc[0, "SeniorCitizen"] = 2
    with pytest.raises(ValueError, match="strictly 0 or 1"):
        validate_senior_citizen(df)


def test_validate_senior_citizen_non_numeric():
    df = create_sample_df()
    df["SeniorCitizen"] = df["SeniorCitizen"].astype(object)
    df.loc[0, "SeniorCitizen"] = "Yes"
    with pytest.raises(ValueError, match="non-numeric values"):
        validate_senior_citizen(df)


def test_validate_tenure_negative():
    df = create_sample_df()
    df["tenure"] = df["tenure"].astype(object)
    df.loc[0, "tenure"] = -5
    with pytest.raises(ValueError, match="negative values"):
        validate_tenure(df)


def test_validate_tenure_fractional():
    df = create_sample_df()
    df["tenure"] = df["tenure"].astype(object)
    df.loc[0, "tenure"] = 5.5
    with pytest.raises(ValueError, match="fractional values"):
        validate_tenure(df)


def test_validate_tenure_infinite():
    df = create_sample_df()
    df["tenure"] = df["tenure"].astype(object)
    df.loc[0, "tenure"] = np.inf
    with pytest.raises(ValueError, match="infinite values"):
        validate_tenure(df)


def test_validate_monthly_charges_negative():
    df = create_sample_df()
    df.loc[0, "MonthlyCharges"] = -10.0
    with pytest.raises(ValueError, match="negative values"):
        validate_monthly_charges(df)


def test_validate_monthly_charges_infinite():
    df = create_sample_df()
    df.loc[0, "MonthlyCharges"] = np.inf
    with pytest.raises(ValueError, match="infinite values"):
        validate_monthly_charges(df)


def test_validate_total_charges_negative():
    df = create_sample_df()
    df.loc[0, "TotalCharges"] = "-100.0"
    with pytest.raises(ValueError, match="negative values"):
        validate_total_charges(df)


def test_validate_total_charges_infinite():
    df = create_sample_df()
    df.loc[0, "TotalCharges"] = "inf"
    with pytest.raises(ValueError, match="infinite values"):
        validate_total_charges(df)


def test_validate_dataset_valid():
    df = create_sample_df()
    validate_dataset(df)
