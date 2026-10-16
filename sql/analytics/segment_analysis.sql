-- Segment Analysis
-- Computes customer count, churned count, retained count, and churn rate across
-- Contract, InternetService, PaymentMethod, and tenure bands (0–12, 13–24, 25–48, 49–72, 73+).

SELECT
    'Contract' AS dimension,
    Contract AS segment_value,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    CASE
        WHEN COUNT(*) = 0 THEN 0.0
        ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
    END AS churn_rate
FROM customers
GROUP BY Contract

UNION ALL

SELECT
    'InternetService' AS dimension,
    InternetService AS segment_value,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    CASE
        WHEN COUNT(*) = 0 THEN 0.0
        ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
    END AS churn_rate
FROM customers
GROUP BY InternetService

UNION ALL

SELECT
    'PaymentMethod' AS dimension,
    PaymentMethod AS segment_value,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    CASE
        WHEN COUNT(*) = 0 THEN 0.0
        ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
    END AS churn_rate
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
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    CASE
        WHEN COUNT(*) = 0 THEN 0.0
        ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
    END AS churn_rate
FROM customers
GROUP BY segment_value;
