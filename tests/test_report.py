import pandas as pd
from src.clean import clean_data
from src.report import audit_total_charges, generate_report


def test_audit_total_charges_distinguishes_blank_and_invalid_string(tmp_path):
    raw_df = pd.DataFrame({
        "customerID": ["1111-AAA", "2222-BBB", "3333-CCC"],
        "gender": ["Female", "Male", "Male"],
        "SeniorCitizen": [0, 0, 1],
        "Partner": ["Yes", "No", "No"],
        "Dependents": ["No", "No", "No"],
        "tenure": [0, 12, 24],
        "PhoneService": ["Yes", "Yes", "Yes"],
        "MultipleLines": ["No", "No", "Yes"],
        "InternetService": ["No", "DSL", "Fiber optic"],
        "OnlineSecurity": ["No internet service", "Yes", "No"],
        "OnlineBackup": ["No internet service", "No", "Yes"],
        "DeviceProtection": ["No internet service", "Yes", "No"],
        "TechSupport": ["No internet service", "No", "Yes"],
        "StreamingTV": ["No internet service", "No", "Yes"],
        "StreamingMovies": ["No internet service", "No", "Yes"],
        "Contract": ["Two year", "Month-to-month", "One year"],
        "PaperlessBilling": ["No", "Yes", "Yes"],
        "PaymentMethod": ["Mailed check", "Electronic check", "Bank transfer"],
        "MonthlyCharges": [20.0, 50.0, 80.0],
        "TotalCharges": [" ", "invalid_str", "1920.0"],
        "Churn": ["No", "No", "Yes"],
    })

    cleaned_df = clean_data(raw_df)

    audit = audit_total_charges(raw_df, cleaned_df)

    assert audit["blank_missing_raw"] == 1
    assert audit["invalid_string_raw"] == 1
    assert audit["total_missing_cleaned"] == 2

    report_path = tmp_path / "report.md"
    report_text = generate_report(raw_df, cleaned_df, db_row_count=3, report_path=str(report_path))

    assert "Blank / Empty TotalCharges in Raw Data" in report_text
    assert "Non-Empty Invalid TotalCharges Strings Coerced to NaN" in report_text
