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
│   ├── clean.py            # Data cleaning and TotalCharges type coercion
│   ├── db.py               # SQLite loading with idempotency support
│   ├── report.py           # Data quality report generation
│   └── pipeline.py         # End-to-end Phase 1 execution runner
├── tests/                  # Pytest unit and integration test suite
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Pytest and project configuration
├── README.md               # Project setup and documentation
├── AGENTS.md               # Agent guidelines and project conventions
└── requirements.txt        # Python dependencies
```

---

## Data Cleaning Policy
- **TotalCharges Handling**:
  - Raw `TotalCharges` entries contain whitespace (`" "`) for 11 new customers with `tenure == 0`.
  - Missing values are safely converted to numeric `NaN` (float) using `pd.to_numeric(..., errors='coerce')`.
  - Missing values are **preserved and reported**; records are **not** silently deleted, nor are missing charges replaced with `0` or imputed without domain justification.
- **Validation Rules**:
  - `customerID`: Non-empty strings and strictly unique (Primary Key).
  - `Churn`: Strictly validated against `Yes` and `No` labels.
  - Numeric columns (`tenure`, `MonthlyCharges`): Verified non-negative.

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
