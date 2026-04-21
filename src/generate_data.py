from pathlib import Path
import numpy as np
import pandas as pd


def sigmoid(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-x))


def create_synthetic_loans(n_rows: int = 5000, random_seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(random_seed)

    grades = np.array(["A", "B", "C", "D", "E", "F"])
    purposes = np.array(["debt_consolidation", "home_improvement", "medical", "small_business", "education"])
    states = np.array(["CA", "TX", "NY", "FL", "IL", "WA", "GA", "NC"])
    home_ownership = np.array(["RENT", "MORTGAGE", "OWN"])

    loan_id = np.arange(100001, 100001 + n_rows)
    age = rng.integers(21, 67, size=n_rows)
    annual_income = np.clip(rng.normal(75000, 30000, size=n_rows), 18000, 250000).round(0)
    loan_amount = np.clip(rng.normal(18000, 9000, size=n_rows), 1000, 50000).round(0)
    term_months = rng.choice([36, 60], size=n_rows, p=[0.7, 0.3])
    employment_length = rng.integers(0, 16, size=n_rows)
    credit_score = np.clip(rng.normal(690, 60, size=n_rows), 500, 850).round(0)
    grade = rng.choice(grades, size=n_rows, p=[0.13, 0.23, 0.28, 0.2, 0.11, 0.05])
    purpose = rng.choice(purposes, size=n_rows)
    state = rng.choice(states, size=n_rows)
    home = rng.choice(home_ownership, size=n_rows, p=[0.44, 0.46, 0.10])
    inquiries_6m = rng.poisson(1.5, size=n_rows)
    delinquencies_2y = rng.poisson(0.4, size=n_rows)
    revolving_utilization = np.clip(rng.normal(0.48, 0.2, size=n_rows), 0.01, 0.99)
    dti = np.clip((loan_amount / annual_income) * 7 + rng.normal(0.18, 0.08, size=n_rows), 0.02, 0.90)
    int_rate = (
        0.06
        + (term_months == 60) * 0.02
        + (np.vectorize({"A": 0.00, "B": 0.01, "C": 0.03, "D": 0.05, "E": 0.08, "F": 0.11}.get)(grade))
        + (700 - credit_score) / 2500
        + rng.normal(0, 0.01, size=n_rows)
    )
    int_rate = np.clip(int_rate, 0.05, 0.36)

    # Default probability formula with business-like risk logic.
    risk_score = (
        -2.8
        + (loan_amount / annual_income) * 2.2
        + dti * 1.7
        + revolving_utilization * 1.1
        + inquiries_6m * 0.12
        + delinquencies_2y * 0.24
        + (term_months == 60) * 0.35
        + np.vectorize({"A": -0.8, "B": -0.45, "C": 0.0, "D": 0.38, "E": 0.72, "F": 1.0}.get)(grade)
        - (credit_score - 680) / 120
    )
    default_prob = sigmoid(risk_score)
    default_flag = rng.binomial(1, default_prob)

    issue_dates = pd.to_datetime("2022-01-01") + pd.to_timedelta(rng.integers(0, 730, size=n_rows), unit="D")

    df = pd.DataFrame(
        {
            "loan_id": loan_id,
            "issue_date": issue_dates,
            "age": age,
            "annual_income": annual_income.astype(float),
            "loan_amount": loan_amount.astype(float),
            "term_months": term_months,
            "employment_length_years": employment_length,
            "credit_score": credit_score.astype(float),
            "grade": grade,
            "purpose": purpose,
            "state": state,
            "home_ownership": home,
            "inquiries_last_6m": inquiries_6m,
            "delinquencies_last_2y": delinquencies_2y,
            "revolving_utilization": revolving_utilization.round(4),
            "dti_ratio": dti.round(4),
            "interest_rate": int_rate.round(4),
            "default_flag": default_flag,
        }
    )

    # Inject small missingness for realism.
    for col in ["annual_income", "employment_length_years", "revolving_utilization"]:
        mask = rng.random(n_rows) < 0.015
        df.loc[mask, col] = np.nan

    return df


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)

    loans = create_synthetic_loans()
    output_path = raw_dir / "loans_raw.csv"
    loans.to_csv(output_path, index=False)

    print(f"Generated dataset: {output_path}")
    print(f"Rows: {len(loans)} | Default rate: {loans['default_flag'].mean():.2%}")


if __name__ == "__main__":
    main()
