import os
import pandas as pd
from src.validate import validate_dataset

DEFAULT_PROCESSED_PATH = os.path.join("data", "processed", "cleaned_telco_churn.csv")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataframe:
    - Normalizes surrounding whitespace on customerID.
    - Validates inputs (strictly checking churn, senior citizen, tenure, charges, including infinity checks after trimming).
    - Safely converts TotalCharges to float numeric using coerce (empty strings/spaces become NaN).
    - Preserves missing values (does NOT drop rows or fill missing TotalCharges with 0).
    """
    cleaned_df = df.copy()

    # Normalize surrounding whitespace on customerID before validation & loading
    if "customerID" in cleaned_df.columns and cleaned_df["customerID"].notna().all():
        cleaned_df["customerID"] = cleaned_df["customerID"].astype(str).str.strip()

    validate_dataset(cleaned_df)

    # Safely convert TotalCharges to numeric using trimmed strings.
    # Blank spaces " " or invalid non-empty strings will be converted to NaN.
    cleaned_df["TotalCharges"] = pd.to_numeric(cleaned_df["TotalCharges"].astype(str).str.strip(), errors="coerce")

    # Cast integer fields cleanly
    cleaned_df["SeniorCitizen"] = pd.to_numeric(cleaned_df["SeniorCitizen"], errors="coerce").astype(int)
    cleaned_df["tenure"] = pd.to_numeric(cleaned_df["tenure"], errors="coerce").astype(int)
    cleaned_df["MonthlyCharges"] = pd.to_numeric(cleaned_df["MonthlyCharges"], errors="coerce").astype(float)

    return cleaned_df


def save_cleaned_data(df: pd.DataFrame, output_path: str = DEFAULT_PROCESSED_PATH) -> str:
    """Saves cleaned DataFrame to CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
