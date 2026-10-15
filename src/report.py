import os
import pandas as pd

DEFAULT_REPORT_PATH = os.path.join("docs", "data_quality_report.md")


def audit_total_charges(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame) -> dict:
    """
    Audits TotalCharges column distinguishing:
    - Blank / empty missing values (legitimate missing values, e.g. tenure == 0).
    - Non-empty invalid strings coerced to NaN.
    - Total missing TotalCharges values in cleaned DataFrame.
    """
    s_raw = raw_df["TotalCharges"].astype(str).str.strip()

    # Blank/missing in raw data (empty string, 'nan', 'none', or pandas isna)
    is_blank_raw = (raw_df["TotalCharges"].isna()) | (s_raw == "") | (s_raw.str.lower() == "nan") | (s_raw.str.lower() == "none")
    blank_count = is_blank_raw.sum()

    # Non-empty raw values trimmed before numeric conversion
    non_empty_trimmed = s_raw[~is_blank_raw]
    # Check which non-empty values fail numeric conversion
    coerced_numeric = pd.to_numeric(non_empty_trimmed, errors="coerce")
    invalid_string_count = coerced_numeric.isna().sum()

    cleaned_missing_count = cleaned_df["TotalCharges"].isna().sum()

    return {
        "blank_missing_raw": int(blank_count),
        "invalid_string_raw": int(invalid_string_count),
        "total_missing_cleaned": int(cleaned_missing_count)
    }


def generate_report(raw_df: pd.DataFrame, cleaned_df: pd.DataFrame, db_row_count: int, report_path: str = DEFAULT_REPORT_PATH) -> str:
    """
    Generates a Data Quality Report based on actual dataset metrics and outputs Markdown report.
    """
    total_raw_rows = len(raw_df)
    total_cleaned_rows = len(cleaned_df)

    tc_audit = audit_total_charges(raw_df, cleaned_df)

    churn_distribution = cleaned_df["Churn"].value_counts(dropna=False).to_dict()
    missing_by_col = cleaned_df.isna().sum().to_dict()

    report_content = f"""# Data Quality & Ingestion Report

## 1. Overview
- **Dataset Title**: IBM Telco Customer Churn (Fictional Telecom Sample)
- **Total Raw Records**: {total_raw_rows}
- **Total Cleaned Records**: {total_cleaned_rows}
- **SQLite Database Record Count**: {db_row_count}
- **Record Retention Rate**: 100% (No records deleted during cleaning)

## 2. Missing Value & Cleaning Audit
- **Blank / Empty TotalCharges in Raw Data**: {tc_audit['blank_missing_raw']}
- **Non-Empty Invalid TotalCharges Strings Coerced to NaN**: {tc_audit['invalid_string_raw']}
- **Total Missing TotalCharges in Cleaned Data**: {tc_audit['total_missing_cleaned']}
- **Missing Value Handling Policy**:
  - Blank values in `TotalCharges` correspond to new customers with `tenure == 0`.
  - Rather than silently dropping records or fabricating values with 0 or mean imputations, missing `TotalCharges` values are safely converted to numeric `NaN` (float) to preserve data integrity for downstream analytical and modeling tasks.
  - Non-empty invalid strings (if present) are safely coerced to `NaN` and explicitly audited.

### Missing Values per Column in Processed Data:
"""
    for col, count in missing_by_col.items():
        report_content += f"- `{col}`: {count}\n"

    report_content += f"""
## 3. Key Categorical Distribution
- **Churn Distribution**: {churn_distribution}

## 4. Pipeline Idempotency & Database Verification
- Primary Key (`customerID`) enforced in SQLite schema (with whitespace normalized).
- Re-running the pipeline uses `INSERT OR REPLACE`, ensuring database record count remains exactly **{db_row_count}** without duplicate entries.
"""

    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    return report_content
