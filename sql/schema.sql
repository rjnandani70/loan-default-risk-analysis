-- Loan Default Risk Analysis - Schema
-- PostgreSQL-compatible SQL

DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS risk_scores;
DROP TABLE IF EXISTS kpi_summary;
DROP TABLE IF EXISTS segment_default_rates;

CREATE TABLE loans (
    loan_id BIGINT PRIMARY KEY,
    issue_date DATE,
    age INT,
    annual_income NUMERIC(12, 2),
    loan_amount NUMERIC(12, 2),
    term_months INT,
    employment_length_years NUMERIC(5, 2),
    credit_score NUMERIC(6, 2),
    grade VARCHAR(5),
    purpose VARCHAR(50),
    state VARCHAR(10),
    home_ownership VARCHAR(20),
    inquiries_last_6m INT,
    delinquencies_last_2y INT,
    revolving_utilization NUMERIC(8, 4),
    dti_ratio NUMERIC(8, 4),
    interest_rate NUMERIC(8, 4),
    default_flag INT,
    loan_to_income_ratio NUMERIC(8, 4),
    income_band VARCHAR(30),
    issue_month VARCHAR(10)
);

CREATE TABLE risk_scores (
    loan_id BIGINT PRIMARY KEY,
    grade VARCHAR(5),
    purpose VARCHAR(50),
    state VARCHAR(10),
    loan_amount NUMERIC(12, 2),
    interest_rate NUMERIC(8, 4),
    default_flag INT,
    pred_default_probability NUMERIC(8, 6),
    risk_band VARCHAR(10)
);

CREATE TABLE kpi_summary (
    metric_name VARCHAR(100),
    metric_value NUMERIC(18, 6)
);

CREATE TABLE segment_default_rates (
    grade VARCHAR(5),
    purpose VARCHAR(50),
    income_band VARCHAR(30),
    total_loans INT,
    defaults INT,
    default_rate NUMERIC(8, 6)
);
