-- High-Churn Segments Ranking
-- Uses a CTE and DENSE_RANK() window function to rank segments with at least 30 customers by churn rate.
-- Shows segment size (total_customers, churned_customers) alongside churn_rate.

WITH segment_rates AS (
    SELECT
        'Contract' AS dimension,
        Contract AS segment_value,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
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
        CASE
            WHEN COUNT(*) = 0 THEN 0.0
            ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
        END AS churn_rate
    FROM customers
    GROUP BY segment_value

    UNION ALL

    SELECT
        'Contract + InternetService' AS dimension,
        Contract || ' | ' || InternetService AS segment_value,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        CASE
            WHEN COUNT(*) = 0 THEN 0.0
            ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
        END AS churn_rate
    FROM customers
    GROUP BY Contract, InternetService

    UNION ALL

    SELECT
        'Contract + PaymentMethod' AS dimension,
        Contract || ' | ' || PaymentMethod AS segment_value,
        COUNT(*) AS total_customers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
        CASE
            WHEN COUNT(*) = 0 THEN 0.0
            ELSE ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*), 4)
        END AS churn_rate
    FROM customers
    GROUP BY Contract, PaymentMethod
)
SELECT
    dimension,
    segment_value,
    total_customers,
    churned_customers,
    churn_rate,
    DENSE_RANK() OVER (ORDER BY churn_rate DESC) AS churn_rank
FROM segment_rates
WHERE total_customers >= 30
ORDER BY churn_rank, total_customers DESC;
