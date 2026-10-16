# Phase 2 Business Insights & Recommendations

## Overview
This document summarizes empirical business findings derived directly from SQL analysis of the IBM Telco Customer Churn dataset (7,043 customers). All metrics reflect exact SQL query calculations from `data/telco_churn.db`. Practical business recommendations are explicitly framed as hypotheses for strategic testing.

---

## 1. Executive Summary & Overall Dataset Baseline

| Metric | SQL Calculated Value | Notes |
| :--- | :--- | :--- |
| **Total Customer Count** | 7,043 | Verified dataset baseline |
| **Churned Customer Count** | 1,869 | `Churn = 'Yes'` |
| **Retained Customer Count** | 5,174 | `Churn = 'No'` |
| **Overall Churn Rate** | 26.54% | 1,869 / 7,043 |
| **Average Monthly Charges** | $64.76 | Across all 7,043 customers |
| **Retained Monthly Charges Total** | $316,985.75 | Sum of `MonthlyCharges` for `Churn = 'No'` |
| **Churned Monthly Charges Total** | $139,130.85 | Sum of `MonthlyCharges` for `Churn = 'Yes'` |
| **Non-Null Total Charges Count** | 7,032 | 11 new customers with `tenure = 0` are NULL |
| **Average Total Charges** | $2,283.30 | Computed across 7,032 non-null records |

---

## 2. Key Empirical Findings by Segment

### Contract Type Comparison
- **Month-to-month**: 3,875 customers (55.02% of total). Churn rate is **42.71%** (1,655 churned).
- **One year**: 1,473 customers. Churn rate drops to **11.27%** (166 churned).
- **Two year**: 1,695 customers. Churn rate drops to **2.83%** (48 churned).
- *Observation*: Month-to-month contracts account for **88.55%** of all churned customers (1,655 out of 1,869).

### Internet Service Type Comparison
- **Fiber Optic**: 3,096 customers. Churn rate is **41.89%** (1,297 churned). Average monthly charge is high at **$91.50**.
- **DSL**: 2,421 customers. Churn rate is **18.96%** (459 churned). Average monthly charge is **$58.10**.
- **No Internet Service**: 1,526 customers. Churn rate is **7.40%** (113 churned). Average monthly charge is **$21.08**.
- *Observation*: Fiber optic customers exhibit double the churn rate of DSL customers despite higher average monthly billing ($91.50 vs $58.10). Fiber optic churned customers represent **$114,300.05** in monthly charges (82.15% of total churned monthly charges).

### Payment Method Comparison
- **Electronic Check**: 2,365 customers. Churn rate is **45.29%** (1,071 churned). Average monthly charge is **$76.26**.
- **Mailed Check**: 1,612 customers. Churn rate is **19.11%** (308 churned).
- **Bank Transfer (Automatic)**: 1,544 customers. Churn rate is **16.71%** (258 churned).
- **Credit Card (Automatic)**: 1,522 customers. Churn rate is **15.24%** (232 churned).
- *Observation*: Electronic check customers churn at nearly 3x the rate of automatic payment methods (Bank Transfer/Credit Card).

### Tenure Band Dynamics
- **0–12 Months**: 2,186 customers. Churn rate is **47.44%** (1,037 churned).
- **13–24 Months**: 1,024 customers. Churn rate is **28.71%** (294 churned).
- **25–48 Months**: 1,594 customers. Churn rate is **20.39%** (325 churned).
- **49–72 Months**: 2,239 customers. Churn rate is **9.51%** (213 churned).
- *Observation*: Nearly half (47.44%) of new customers churn in their first year. Churn rate steadily declines as tenure increases.

---

## 3. Top High-Churn Segments (Minimum 30 Customers)

Using CTE and `DENSE_RANK()`, the top highest-churn cohorts with at least 30 customers are:

| Rank | Segment Dimension | Segment Value | Size | Churned | Churn Rate |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **1** | Contract + InternetService | Month-to-month \| Fiber optic | 2,128 | 1,162 | **54.61%** |
| **2** | Contract + PaymentMethod | Month-to-month \| Electronic check | 1,850 | 994 | **53.73%** |
| **3** | TenureBand | 0–12 Months | 2,186 | 1,037 | **47.44%** |
| **4** | PaymentMethod | Electronic check | 2,365 | 1,071 | **45.29%** |
| **5** | Contract | Month-to-month | 3,875 | 1,655 | **42.71%** |
| **6** | InternetService | Fiber optic | 3,096 | 1,297 | **41.89%** |

---

## 4. Practical Business Recommendations (Framed as Hypotheses)

The following recommendations are action-oriented hypotheses based on empirical cross-sectional associations. They require pilot testing and experimental validation before full-scale deployment:

1. **Hypothesis 1: Onboarding Incentive for Fiber Optic Month-to-Month Subscribers**
   - *Rationale*: Month-to-month Fiber Optic subscribers exhibit the highest churn rate in the dataset (54.61%, 1,162 churned).
   - *Hypothesis*: Offering a modest bill discount or service perk in exchange for migrating from Month-to-month to a 1-Year Contract during the first 90 days will reduce 1st-year Fiber Optic churn.

2. **Hypothesis 2: Automatic Payment Migration Campaign**
   - *Rationale*: Electronic check users churn at 45.29% compared to ~16% for automatic payment options.
   - *Hypothesis*: Providing a small one-time account credit ($5–$10) for switching from Electronic Check to Automatic Credit Card / Bank Transfer will improve retention among high-risk payment cohorts.

3. **Hypothesis 3: Early-Tenure (First 12 Months) Retention Program**
   - *Rationale*: 47.44% of customers in tenure band 0–12 months churn, representing 55.48% of all churned customers (1,037 out of 1,869).
   - *Hypothesis*: Deploying proactive check-ins, technical onboarding support, and satisfaction surveys during months 1–6 will increase early customer engagement and lower first-year drop-off.
