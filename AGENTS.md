# Project Conventions & Guidelines for AI Agents

## Overview
This repository follows Phase 1 standards for the Customer Retention & Revenue Analytics project.

## Project Structure
- `src/`: Python source files for pipeline components (`download.py`, `validate.py`, `clean.py`, `db.py`, `report.py`, `pipeline.py`).
- `tests/`: Pytest suite (`test_validate.py`, `test_clean.py`, `test_db.py`).
- `sql/`: SQL schema files (`schema.sql`).
- `data/`: Raw and processed datasets (`data/raw/`, `data/processed/`, `data/telco_churn.db`). All generated data is git-ignored.
- `docs/`: Generated data quality reports (`data_quality_report.md`).

## Coding & Data Conventions
1. **Python Version**: Python 3.11+.
2. **Data Preservation**: Never modify raw CSV files in `data/raw/`.
3. **Cleaning Standard**: Convert blank/invalid numeric strings using coercion (`pd.to_numeric(..., errors='coerce')`). Preserve `NaN` missing values without dropping rows or replacing with zeros unless explicitly instructed.
4. **Idempotency**: All database loaders must use Primary Key constraints (`customerID`) and `INSERT OR REPLACE` to avoid duplication upon repeated runs.
5. **No Fabrication**: Do not fabricate dates, machine-learning accuracy, or simulated monetary savings.

## Testing Guidelines
- All tests must pass using `pytest`.
- Run `pytest` before submitting changes.
- Ensure test coverage for:
  - Schema/validation checks (missing columns, invalid churn, negative numbers, duplicate IDs).
  - Missing value handling (`TotalCharges` coercion to `NaN`).
  - Idempotency in database loading.

## Pre-Commit Verification
- Always execute pre-commit steps to ensure testing, verification, review, and reflection are done before submitting PRs.
