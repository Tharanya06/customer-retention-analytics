import numpy as np
import pandas as pd

REQUIRED_COLUMNS = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport",
    "StreamingTV", "StreamingMovies", "Contract", "PaperlessBilling",
    "PaymentMethod", "MonthlyCharges", "TotalCharges", "Churn"
]

VALID_CHURN_VALUES = {"Yes", "No"}


def validate_schema(df: pd.DataFrame) -> None:
    """Ensure all required columns are present in the DataFrame."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")


def validate_customer_ids(df: pd.DataFrame) -> None:
    """Ensure customerID exists, has no missing/empty strings, and is unique after normalizing whitespace."""
    if "customerID" not in df.columns:
        raise ValueError("customerID column missing.")

    if df["customerID"].isna().any():
        raise ValueError("customerID contains missing or null values.")

    s = df["customerID"].astype(str).str.strip()
    if (s == "").any():
        raise ValueError("customerID contains empty string values.")

    if s.duplicated().any():
        duplicates = s[s.duplicated()].unique().tolist()
        raise ValueError(f"Duplicate customerID entries found after whitespace normalization: {duplicates[:5]}")


def validate_churn_labels(df: pd.DataFrame) -> None:
    """Ensure churn values are non-null and strictly 'Yes' or 'No'."""
    if "Churn" not in df.columns:
        raise ValueError("Churn column missing.")

    if df["Churn"].isna().any():
        raise ValueError("Churn column contains null or missing values.")

    unique_vals = set(df["Churn"].unique())
    invalid = unique_vals - VALID_CHURN_VALUES
    if invalid:
        raise ValueError(f"Invalid Churn values found: {invalid}")


def validate_senior_citizen(df: pd.DataFrame) -> None:
    """Ensure SeniorCitizen values are strictly 0 or 1."""
    if "SeniorCitizen" not in df.columns:
        raise ValueError("SeniorCitizen column missing.")

    if df["SeniorCitizen"].isna().any():
        raise ValueError("SeniorCitizen column contains missing or null values.")

    # Convert to numeric to check values without truncation
    numeric_sc = pd.to_numeric(df["SeniorCitizen"], errors="coerce")
    if numeric_sc.isna().any():
        raise ValueError("SeniorCitizen contains non-numeric values.")

    invalid = set(numeric_sc.unique()) - {0, 1, 0.0, 1.0}
    if invalid:
        raise ValueError(f"SeniorCitizen must be strictly 0 or 1. Invalid values found: {invalid}")


def validate_tenure(df: pd.DataFrame) -> None:
    """Ensure tenure is a non-negative integer (reject negative, infinite, or fractional numbers)."""
    if "tenure" not in df.columns:
        raise ValueError("tenure column missing.")

    if df["tenure"].isna().any():
        raise ValueError("tenure contains missing or null values.")

    numeric_tenure = pd.to_numeric(df["tenure"], errors="coerce")
    if numeric_tenure.isna().any():
        raise ValueError("tenure contains non-numeric values.")

    if np.isinf(numeric_tenure).any():
        raise ValueError("tenure contains infinite values.")

    if (numeric_tenure < 0).any():
        raise ValueError("tenure contains negative values.")

    # Check for fractional values (e.g. 5.5)
    if not (numeric_tenure % 1 == 0).all():
        raise ValueError("tenure contains fractional values; must be integers.")


def validate_monthly_charges(df: pd.DataFrame) -> None:
    """Ensure MonthlyCharges is non-negative and finite."""
    if "MonthlyCharges" not in df.columns:
        raise ValueError("MonthlyCharges column missing.")

    if df["MonthlyCharges"].isna().any():
        raise ValueError("MonthlyCharges contains missing or null values.")

    numeric_mc = pd.to_numeric(df["MonthlyCharges"], errors="coerce")
    if numeric_mc.isna().any():
        raise ValueError("MonthlyCharges contains non-numeric values.")

    if np.isinf(numeric_mc).any():
        raise ValueError("MonthlyCharges contains infinite values.")

    if (numeric_mc < 0).any():
        raise ValueError("MonthlyCharges contains negative values.")


def validate_total_charges(df: pd.DataFrame) -> None:
    """
    Validate TotalCharges:
    - Legitimate missing values (blank/spaces or NaN) are allowed.
    - If present and convertible to numeric, values must be non-negative and finite.
    - Negative or infinite TotalCharges are rejected.
    """
    if "TotalCharges" not in df.columns:
        raise ValueError("TotalCharges column missing.")

    # Convert non-blank strings to float to check validity
    s = df["TotalCharges"].astype(str).str.strip()
    is_blank = (df["TotalCharges"].isna()) | (s == "") | (s.str.lower() == "nan") | (s.str.lower() == "none")

    non_blank_vals = df.loc[~is_blank, "TotalCharges"]
    if len(non_blank_vals) > 0:
        converted = pd.to_numeric(non_blank_vals, errors="coerce")
        # Check if any non-blank value failed conversion to numeric
        # (Note: invalid strings that are non-empty will be checked/handled in clean/report, but if they convert to negative/inf we reject)
        valid_numeric = converted.dropna()

        if np.isinf(valid_numeric).any():
            raise ValueError("TotalCharges contains infinite values.")

        if (valid_numeric < 0).any():
            raise ValueError("TotalCharges contains negative values.")


def validate_dataset(df: pd.DataFrame) -> None:
    """Run full validation suite on the DataFrame."""
    validate_schema(df)
    validate_customer_ids(df)
    validate_churn_labels(df)
    validate_senior_citizen(df)
    validate_tenure(df)
    validate_monthly_charges(df)
    validate_total_charges(df)
