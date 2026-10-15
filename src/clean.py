import os
import pandas as pd
from src.validate import validate_dataset

DEFAULT_PROCESSED_PATH = os.path.join("data", "processed", "cleaned_telco_churn.csv")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw dataframe:
    - Validates inputs.
    - Safely converts TotalCharges to float numeric using coerce (empty strings/spaces become NaN).
    - Preserves missing values (does NOT drop rows or fill missing TotalCharges with 0).
    """
    validate_dataset(df)

    cleaned_df = df.copy()

    # Safely convert TotalCharges to numeric.
    # Blank spaces " " or invalid strings will be converted to NaN.
    cleaned_df["TotalCharges"] = pd.to_numeric(cleaned_df["TotalCharges"].astype(str).str.strip(), errors="coerce")

    # Verify that SeniorCitizen is numeric
    cleaned_df["SeniorCitizen"] = pd.to_numeric(cleaned_df["SeniorCitizen"], errors="coerce").astype(int)
    cleaned_df["tenure"] = pd.to_numeric(cleaned_df["tenure"], errors="coerce").astype(int)
    cleaned_df["MonthlyCharges"] = pd.to_numeric(cleaned_df["MonthlyCharges"], errors="coerce").astype(float)

    return cleaned_df


def save_cleaned_data(df: pd.DataFrame, output_path: str = DEFAULT_PROCESSED_PATH) -> str:
    """Saves cleaned DataFrame to CSV file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
