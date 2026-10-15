# Data Quality & Ingestion Report

## 1. Overview
- **Dataset Title**: IBM Telco Customer Churn (Fictional Telecom Sample)
- **Total Raw Records**: 7043
- **Total Cleaned Records**: 7043
- **SQLite Database Record Count**: 7043
- **Record Retention Rate**: 100% (No records deleted during cleaning)

## 2. Missing Value & Cleaning Audit
- **Blank / Empty TotalCharges in Raw Data**: 11
- **Non-Empty Invalid TotalCharges Strings Coerced to NaN**: 0
- **Total Missing TotalCharges in Cleaned Data**: 11
- **Missing Value Handling Policy**:
  - Blank values in `TotalCharges` correspond to new customers with `tenure == 0`.
  - Rather than silently dropping records or fabricating values with 0 or mean imputations, missing `TotalCharges` values are safely converted to numeric `NaN` (float) to preserve data integrity for downstream analytical and modeling tasks.
  - Non-empty invalid strings (if present) are safely coerced to `NaN` and explicitly audited.

### Missing Values per Column in Processed Data:
- `customerID`: 0
- `gender`: 0
- `SeniorCitizen`: 0
- `Partner`: 0
- `Dependents`: 0
- `tenure`: 0
- `PhoneService`: 0
- `MultipleLines`: 0
- `InternetService`: 0
- `OnlineSecurity`: 0
- `OnlineBackup`: 0
- `DeviceProtection`: 0
- `TechSupport`: 0
- `StreamingTV`: 0
- `StreamingMovies`: 0
- `Contract`: 0
- `PaperlessBilling`: 0
- `PaymentMethod`: 0
- `MonthlyCharges`: 0
- `TotalCharges`: 11
- `Churn`: 0

## 3. Key Categorical Distribution
- **Churn Distribution**: {'No': 5174, 'Yes': 1869}

## 4. Pipeline Idempotency & Database Verification
- Primary Key (`customerID`) enforced in SQLite schema (with whitespace normalized).
- Re-running the pipeline uses `INSERT OR REPLACE`, ensuring database record count remains exactly **7043** without duplicate entries.
