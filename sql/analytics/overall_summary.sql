-- Overall Summary Metrics
-- Computes total customer count, churned count, retained count, churn rate, average MonthlyCharges,
-- total MonthlyCharges for retained and churned customers, non-null TotalCharges count, and average TotalCharges.

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    CASE
        WHEN COUNT(*) = 0 THEN 0.0
        ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
    END AS churn_rate,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(AVG(TotalCharges), 2) AS avg_total_charges
FROM customers;
