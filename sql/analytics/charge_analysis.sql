-- Charge Analysis
-- Computes separate sums of MonthlyCharges for retained and churned customers across
-- overall dataset and key segments (Contract, InternetService, PaymentMethod, TenureBand),
-- as well as average MonthlyCharges and non-null TotalCharges counts/sums.

SELECT
    'Overall' AS dimension,
    'All Customers' AS segment_value,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(SUM(TotalCharges), 2) AS total_charges_sum
FROM customers

UNION ALL

SELECT
    'Contract' AS dimension,
    Contract AS segment_value,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(SUM(TotalCharges), 2) AS total_charges_sum
FROM customers
GROUP BY Contract

UNION ALL

SELECT
    'InternetService' AS dimension,
    InternetService AS segment_value,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(SUM(TotalCharges), 2) AS total_charges_sum
FROM customers
GROUP BY InternetService

UNION ALL

SELECT
    'PaymentMethod' AS dimension,
    PaymentMethod AS segment_value,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(SUM(TotalCharges), 2) AS total_charges_sum
FROM customers
GROUP BY PaymentMethod

UNION ALL

SELECT
    'TenureBand' AS dimension,
    CASE
        WHEN tenure BETWEEN 0 AND 12 THEN '0–12'
        WHEN tenure BETWEEN 13 AND 24 THEN '13–24'
        WHEN tenure BETWEEN 25 AND 48 THEN '25–48'
        WHEN tenure BETWEEN 49 AND 72 THEN '49–72'
        WHEN tenure >= 73 THEN '73+'
    END AS segment_value,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS retained_monthly_charges_total,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS churned_monthly_charges_total,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    COUNT(TotalCharges) AS total_charges_non_null_count,
    ROUND(SUM(TotalCharges), 2) AS total_charges_sum
FROM customers
GROUP BY segment_value;
