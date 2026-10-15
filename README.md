# Customer Retention & Revenue Analytics (Phase 1)

## Overview
This repository contains Phase 1 of the **Customer Retention & Revenue Analytics** project. The project processes and analyzes customer churn data to support retention strategies.

> **Dataset Notice**: This dataset is a **fictional telecom sample** provided by IBM (`Telco-Customer-Churn`). It is strictly used for analytical demonstration purposes. No dates, machine-learning model performance metrics, or financial business savings are fabricated in this phase.

---

## Project Structure
```
customer-retention-analytics/
├── data/
│   ├── raw/                # Raw downloaded CSV (preserved unchanged)
│   └── processed/          # Processed & cleaned CSV dataset
├── docs/                   # Data quality reports and documentation
├── sql/
│   └── schema.sql          # SQLite table definitions and primary key constraints
├── src/
│   ├── download.py         # Module to download raw dataset
│   ├── validate.py         # Schema & data validation checks
│   ├── clean.py            # Data cleaning, whitespace normalization, and TotalCharges type coercion
│   ├── db.py               # SQLite loading with idempotency support
│   ├── report.py           # Data quality report generation with explicit missingness audit
│   └── pipeline.py         # End-to-end Phase 1 execution runner
├── tests/                  # Pytest unit and integration test suite
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Pytest and project configuration
├── README.md               # Project setup and documentation
├── AGENTS.md               # Agent guidelines and project conventions
└── requirements.txt        # Python dependencies
```

---

## Data Cleaning & Validation Policy
- **Customer ID Normalization**:
  - Surrounding whitespace in `customerID` is normalized in the cleaned copy prior to uniqueness validation and loading into SQLite.
  - IDs that become duplicates after whitespace normalization are strictly rejected.
  - Raw CSV files remain completely unchanged.
- **Churn Label Strictness**:
  - `Churn` labels must be non-null and strictly equal to `Yes` or `No`. Null/missing values or any other strings are rejected.
- **Senior Citizen Constraint**:
  - `SeniorCitizen` must be strictly `0` or `1`. Non-numeric or out-of-bounds values are rejected.
- **Tenure Constraint**:
  - `tenure` must be a non-negative integer. Fractional numbers, negative values, and infinite values are strictly rejected without silent truncation.
- **Numeric Charge Constraints**:
  - `MonthlyCharges`: Must be non-negative and finite (rejecting negative and infinite charges).
  - `TotalCharges`: Uses consistent whitespace trimming (`.str.strip()`) before numeric conversion. Legitimate missing entries (e.g. new customers with `tenure == 0`) are safely converted to numeric `NaN` (float) using coercion and preserved as `NULL` in SQLite. Positive and negative infinity (including whitespace-padded strings such as `" inf "`, `"\tInfinity\t"`) as well as negative `TotalCharges` values are strictly rejected.
- **Audit Reporting**:
  - The pipeline explicitly distinguishes and reports blank/empty missing `TotalCharges` from non-empty invalid strings coerced to `NaN`.

---

## Windows Setup & Execution Instructions

### Prerequisites
- Python 3.11 or Python 3.12 installed on Windows.
- PowerShell or Command Prompt (CMD).

### 1. Create and Activate Virtual Environment

**In PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**In Command Prompt (CMD):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

### 2. Install Dependencies
```cmd
pip install -r requirements.txt
```

### 3. Run End-to-End Pipeline
```cmd
python -m src.pipeline
```

### 4. Run Tests
```cmd
pytest
```

---

## Output Artifacts
- Processed Dataset: `data/processed/cleaned_telco_churn.csv`
- SQLite Database: `data/telco_churn.db`
- Data Quality Report: `docs/data_quality_report.md`
