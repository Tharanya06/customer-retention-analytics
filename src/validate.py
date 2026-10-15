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
    """Ensure customerID exists, has no missing/empty strings, and is unique."""
    if "customerID" not in df.columns:
        raise ValueError("customerID column missing.")

    s = df["customerID"].astype(str).str.strip()
    if (s == "").any() or df["customerID"].isna().any():
        raise ValueError("customerID contains missing or empty string values.")

    if df["customerID"].duplicated().any():
        duplicates = df[df["customerID"].duplicated()]["customerID"].unique().tolist()
        raise ValueError(f"Duplicate customerID entries found: {duplicates[:5]}")


def validate_churn_labels(df: pd.DataFrame) -> None:
    """Ensure churn values are valid (e.g., 'Yes' or 'No')."""
    if "Churn" not in df.columns:
        raise ValueError("Churn column missing.")

    invalid = set(df["Churn"].dropna().unique()) - VALID_CHURN_VALUES
    if invalid:
        raise ValueError(f"Invalid Churn values found: {invalid}")


def validate_non_negative_numeric(df: pd.DataFrame) -> None:
    """Ensure tenure and MonthlyCharges are non-negative numeric values."""
    for col in ["tenure", "MonthlyCharges"]:
        if col in df.columns:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.isna().any():
                raise ValueError(f"Non-numeric values found in column {col}")
            if (converted < 0).any():
                raise ValueError(f"Negative values found in numeric column {col}")


def validate_dataset(df: pd.DataFrame) -> None:
    """Run full validation suite on the DataFrame."""
    validate_schema(df)
    validate_customer_ids(df)
    validate_churn_labels(df)
    validate_non_negative_numeric(df)
