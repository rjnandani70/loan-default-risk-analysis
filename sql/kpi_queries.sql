-- Core KPI queries

-- 1) Portfolio level KPIs
SELECT
    COUNT(*) AS total_loans,
    SUM(default_flag) AS total_defaults,
    ROUND(AVG(default_flag::numeric), 4) AS default_rate,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(interest_rate), 4) AS avg_interest_rate
FROM loans;

-- 2) Default rate by credit grade
SELECT
    grade,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS defaults,
    ROUND(AVG(default_flag::numeric), 4) AS default_rate
FROM loans
GROUP BY grade
ORDER BY default_rate DESC;

-- 3) Default rate by purpose
SELECT
    purpose,
    COUNT(*) AS total_loans,
    SUM(default_flag) AS defaults,
    ROUND(AVG(default_flag::numeric), 4) AS default_rate
FROM loans
GROUP BY purpose
ORDER BY default_rate DESC;

-- 4) Monthly issuance and default trend
SELECT
    issue_month,
    COUNT(*) AS loans_issued,
    SUM(default_flag) AS defaults,
    ROUND(AVG(default_flag::numeric), 4) AS default_rate
FROM loans
GROUP BY issue_month
ORDER BY issue_month;

-- 5) Model score quality by risk band
SELECT
    risk_band,
    COUNT(*) AS loans,
    ROUND(AVG(pred_default_probability), 4) AS avg_predicted_pd,
    ROUND(AVG(default_flag::numeric), 4) AS actual_default_rate
FROM risk_scores
GROUP BY risk_band
ORDER BY
    CASE risk_band
        WHEN 'Low' THEN 1
        WHEN 'Medium' THEN 2
        WHEN 'High' THEN 3
        ELSE 4
    END;
