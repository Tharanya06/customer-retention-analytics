# Phase 2 Metrics Dictionary & Methodology

This document provides exact definitions, mathematical formulas, denominator logic, NULL handling rules, zero-denominator safeguards, and analytical limitations for all metrics produced in Phase 2 SQL Business Analytics.

---

## 1. Metrics Definitions & Formulas

### 1. Total Customer Count (`total_customers`)
- **Definition**: The total number of unique customer records in the dataset or segment.
- **Formula**:
  $$\text{total\_customers} = \text{COUNT(*)}$$
- **Denominator**: N/A (Count metric).
- **NULL Handling**: `COUNT(*)` includes all rows regardless of NULL values in individual columns. On an empty table or cohort, returns `0`.

### 2. Churned Customer Count (`churned_customers`)
- **Definition**: The total number of customers who have churned (`Churn = 'Yes'`).
- **Formula**:
  $$\text{churned\_customers} = \text{COALESCE}\left(\sum \mathbf{1}(\text{Churn} = \text{'Yes'}), 0\right)$$
- **Denominator**: N/A (Count metric).
- **NULL Handling**: `Churn` column is non-null for all 7,043 rows in validated datasets. On an empty table or cohort, returns `0`.

### 3. Retained Customer Count (`retained_customers`)
- **Definition**: The total number of active/retained customers (`Churn = 'No'`).
- **Formula**:
  $$\text{retained\_customers} = \text{COALESCE}\left(\sum \mathbf{1}(\text{Churn} = \text{'No'}), 0\right)$$
- **Denominator**: N/A (Count metric).
- **NULL Handling**: Non-null for all rows. On an empty table or cohort, returns `0`.

### 4. Churn Rate (`churn_rate`)
- **Definition**: The proportion of customers within a cohort or dataset who have churned.
- **Formula**:
  $$\text{churn\_rate} = \begin{cases} 0.0 & \text{if } \text{total\_customers} = 0 \\ \operatorname{ROUND}\left(\frac{\text{churned\_customers}}{\text{total\_customers}}, 4\right) & \text{if } \text{total\_customers} > 0 \end{cases}$$
- **Denominator**: `total_customers` ($\text{COUNT(*)}$ across the cohort).
- **Zero-Denominator Safeguard**: Handled explicitly with SQL `CASE WHEN COUNT(*) = 0 THEN 0.0 ELSE ... END` to prevent division-by-zero errors.

### 5. Average Monthly Charges (`avg_monthly_charges`)
- **Definition**: The arithmetic mean of `MonthlyCharges` for a cohort.
- **Formula**:
  $$\text{avg\_monthly\_charges} = \operatorname{ROUND}\left(\operatorname{AVG}(\text{MonthlyCharges}), 2\right)$$
- **Denominator**: `COUNT(MonthlyCharges)` (non-null monthly charges count).
- **Empty-Table / NULL Handling**: When `COUNT(MonthlyCharges) = 0` (e.g. on an empty table or cohort), SQLite `AVG()` yields `NULL` (or Python `None`), preserving the undefined nature of an average over zero items.

### 6. Retained Monthly Charges Total (`retained_monthly_charges_total`)
- **Definition**: The sum of `MonthlyCharges` contributed by retained customers (`Churn = 'No'`).
- **Labeling Standard**: Labeled descriptively as a monthly-charge total for retained customers. **Not** designated as recurring revenue, ARR, or financial profit.
- **Formula**:
  $$\text{retained\_monthly\_charges\_total} = \text{COALESCE}\left(\operatorname{ROUND}\left(\sum_{\text{Churn}=\text{'No'}} \text{MonthlyCharges}, 2\right), 0.0\right)$$
- **Denominator**: N/A (Sum metric).
- **Empty-Table / NULL Handling**: Wrapped with `COALESCE(..., 0.0)` to ensure a clean `0.0` sum when no matching retained customers exist.

### 7. Churned Monthly Charges Total (`churned_monthly_charges_total`)
- **Definition**: The sum of `MonthlyCharges` associated with customers who churned (`Churn = 'Yes'`).
- **Labeling Standard**: Labeled descriptively as a monthly-charge total associated with churned accounts. **Not** designated as measured revenue loss, future financial loss, or recoverable savings.
- **Formula**:
  $$\text{churned\_monthly\_charges\_total} = \text{COALESCE}\left(\operatorname{ROUND}\left(\sum_{\text{Churn}=\text{'Yes'}} \text{MonthlyCharges}, 2\right), 0.0\right)$$
- **Denominator**: N/A (Sum metric).
- **Empty-Table / NULL Handling**: Wrapped with `COALESCE(..., 0.0)` to ensure a clean `0.0` sum when no matching churned customers exist.

### 8. Non-Null Total Charges Count (`total_charges_non_null_count`)
- **Definition**: The count of customer records with valid, non-null `TotalCharges`.
- **Formula**:
  $$\text{total\_charges\_non\_null_count} = \operatorname{COUNT}(\text{TotalCharges})$$
- **NULL Handling**: SQLite `COUNT(column)` ignores NULL values. On the full dataset, exactly 11 customers (new accounts with `tenure = 0`) have NULL `TotalCharges`, yielding 7,032 non-null records. On an empty table, returns `0`.

### 9. Average Total Charges (`avg_total_charges`) & Sum (`total_charges_sum`)
- **Definition**: The arithmetic mean and aggregate sum of cumulative `TotalCharges` among non-null records.
- **Formula**:
  $$\text{avg\_total\_charges} = \operatorname{ROUND}\left(\operatorname{AVG}(\text{TotalCharges}), 2\right)$$
  $$\text{total\_charges\_sum} = \operatorname{ROUND}\left(\sum \text{TotalCharges}, 2\right)$$
- **Denominator**: `COUNT(TotalCharges)` (7,032 non-null records in full dataset).
- **Empty-Table / All-NULL Handling**: SQLite `AVG()` and `SUM()` automatically return `NULL` (Python `None`) when all records are NULL or when the table is empty, accurately reflecting that sum and average are undefined when no valid values exist.

---

## 2. Empty-Table & Null Aggregate Policy Summary

To maintain analytical rigor, Phase 2 SQL queries strictly follow this aggregation policy for empty tables or cohorts:
- **Count & Sum Metrics**: `total_customers`, `churned_customers`, `retained_customers`, `retained_monthly_charges_total`, `churned_monthly_charges_total`, and `total_charges_non_null_count` consistently return `0` or `0.0`.
- **Rate Metrics**: `churn_rate` uses explicit `CASE WHEN COUNT(*) = 0 THEN 0.0` logic to return `0.0` and avoid division-by-zero.
- **Average & All-Missing Metrics**: `avg_monthly_charges`, `avg_total_charges`, and `total_charges_sum` return `NULL` (represented as `None` / `NaN` in Python/Pandas) when there are zero records or when all target entries are missing/NULL.

---

## 3. Segmentation & Tenure Band Definitions

Segments are analyzed across single dimensions and multi-attribute combinations:
- **Contract**: `Month-to-month`, `One year`, `Two year`.
- **InternetService**: `DSL`, `Fiber optic`, `No`.
- **PaymentMethod**: `Bank transfer (automatic)`, `Credit card (automatic)`, `Electronic check`, `Mailed check`.
- **Tenure Bands**:
  - `0–12`: `tenure BETWEEN 0 AND 12` (Includes tenure boundaries 0 and 12).
  - `13–24`: `tenure BETWEEN 13 AND 24` (Includes tenure boundaries 13 and 24).
  - `25–48`: `tenure BETWEEN 25 AND 48` (Includes tenure boundaries 25 and 48).
  - `49–72`: `tenure BETWEEN 49 AND 72` (Includes tenure boundaries 49 and 72).
  - `73+`: `tenure >= 73` (Handled in SQL logic; no rows in actual dataset exceed tenure 72).

---

## 4. High-Churn Ranking & CTE Methodology

High-churn segments are identified using a Common Table Expression (CTE) combined with the `DENSE_RANK()` window function:
- **Filtering Threshold**: Only segments with `total_customers >= 30` are included in ranking to prevent small-sample distortion.
- **Ranking Function**: `DENSE_RANK() OVER (ORDER BY churn_rate DESC)` assigns consecutive rank numbers, ensuring ties receive equal rank without gaps in sequence.
- **Output Requirements**: Each ranked row displays segment size (`total_customers`, `churned_customers`) alongside `churn_rate` and `churn_rank`.

---

## 5. Analytical Limitations & Dataset Constraints

1. **Cross-Sectional Dataset**:
   - The data represents a single snapshot in time (`Telco-Customer-Churn` fictional dataset).
   - Historical timestamp tracking, subscription start/end dates, cohort evolution over calendar time, and panel tracking are absent.
2. **Correlation vs. Causation**:
   - High churn rates observed in specific segments (e.g., Fiber Optic + Month-to-month) reflect empirical associations, not causal relationships.
3. **No Financial Projection or Loss Claims**:
   - `MonthlyCharges` totals describe current snapshot sums across churned/retained cohorts. They do not represent financial loss over time, projected customer lifetime value (LTV), or guaranteed revenue recovery.
4. **No Fabricated Model Scores or Trends**:
   - All results are computed directly from raw SQL queries on validated data without machine learning scores, time-series projections, or fabricated benchmark metrics.
