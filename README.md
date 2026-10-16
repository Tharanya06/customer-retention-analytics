# Customer Retention & Revenue Analytics (Phase 1 & Phase 2)

## Overview
This repository contains Phase 1 and Phase 2 of the **Customer Retention & Revenue Analytics** project. The project processes, validates, loads, and analyzes customer churn data using SQLite and Python to deliver structured SQL business analytics and empirical retention insights.

> **Dataset Notice**: This dataset is a **fictional telecom sample** provided by IBM (`Telco-Customer-Churn`). It is strictly used for analytical demonstration purposes. No dates, machine-learning model performance metrics, financial savings, or causal claims are fabricated in these phases.

---

## Project Structure
```
customer-retention-analytics/
├── data/
│   ├── raw/                # Raw downloaded CSV (preserved unchanged)
│   ├── processed/          # Processed & cleaned CSV dataset and analytics exports
│   │   └── analytics/      # Phase 2 SQL analytics exported CSV results
│   └── telco_churn.db      # SQLite database storing validated customer records
├── docs/                   # Data quality reports, metrics dictionary, and business insights
│   ├── data_quality_report.md
│   ├── metrics_dictionary.md
│   └── business_insights.md
├── sql/
│   ├── schema.sql          # SQLite table definitions and primary key constraints
│   └── analytics/          # Phase 2 reusable SQL business analytics queries
│       ├── overall_summary.sql
│       ├── segment_analysis.sql
│       ├── charge_analysis.sql
│       └── high_churn_segments.sql
├── src/
│   ├── download.py         # Module to download raw dataset
│   ├── validate.py         # Schema & data validation checks
│   ├── clean.py            # Data cleaning, whitespace normalization, and TotalCharges coercion
│   ├── db.py               # SQLite loading with primary key idempotency support
│   ├── report.py           # Data quality report generation with missingness audit
│   ├── analytics.py        # Phase 2 SQL analytics runner and CSV exporter
│   └── pipeline.py         # End-to-end Phase 1 execution runner
├── tests/                  # Pytest unit and integration test suite
│   ├── test_analytics.py   # Phase 2 analytics query & boundary test suite
│   ├── test_clean.py
│   ├── test_db.py
│   ├── test_report.py
│   └── test_validate.py
├── .gitignore              # Git ignore rules
├── pyproject.toml          # Pytest and project configuration
├── README.md               # Project setup and execution documentation
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
  - `Churn` labels must be non-null and strictly equal to `Yes` or `No`.
- **Senior Citizen Constraint**:
  - `SeniorCitizen` must be strictly `0` or `1`.
- **Tenure Constraint**:
  - `tenure` must be a non-negative integer.
- **Numeric Charge Constraints**:
  - `MonthlyCharges`: Must be non-negative and finite.
  - `TotalCharges`: Uses consistent whitespace trimming before numeric conversion. Legitimate missing entries (e.g. new customers with `tenure == 0`) are safely converted to numeric `NaN` (float) and preserved as `NULL` in SQLite.
- **Audit Reporting**:
  - Distinguishes blank `TotalCharges` from non-empty invalid strings coerced to `NaN`.

---

## Setup & Execution Instructions

### Prerequisites
- Python 3.11 or Python 3.12 installed.
- Virtual environment created and activated.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Phase 1 Data Ingestion Pipeline
```bash
python -m src.pipeline
```

### 3. Run Phase 2 SQL Analytics Runner
```bash
python -m src.analytics
```

### 4. Run Test Suite
```bash
python -m pytest
```

---

## Output Artifacts
- Processed Dataset: `data/processed/cleaned_telco_churn.csv`
- SQLite Database: `data/telco_churn.db`
- Data Quality Report: `docs/data_quality_report.md`
- Metrics Dictionary: `docs/metrics_dictionary.md`
- Business Insights & Recommendations: `docs/business_insights.md`
- Exported Analytics Results (`data/processed/analytics/`):
  - `overall_summary.csv`
  - `segment_analysis.csv`
  - `charge_analysis.csv`
  - `high_churn_segments.csv`
