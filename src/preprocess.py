from pathlib import Path
import pandas as pd


def build_income_band(income: float) -> str:
    if income < 40000:
        return "Low Income"
    if income < 90000:
        return "Middle Income"
    return "High Income"


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    raw_path = project_root / "data" / "raw" / "loans_raw.csv"
    processed_dir = project_root / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path, parse_dates=["issue_date"])

    # Basic cleaning
    df = df.drop_duplicates(subset=["loan_id"]).copy()
    df["annual_income"] = df["annual_income"].fillna(df["annual_income"].median())
    df["employment_length_years"] = df["employment_length_years"].fillna(df["employment_length_years"].median())
    df["revolving_utilization"] = df["revolving_utilization"].fillna(df["revolving_utilization"].median())

    # Feature engineering
    df["loan_to_income_ratio"] = (df["loan_amount"] / df["annual_income"]).round(4)
    df["income_band"] = df["annual_income"].apply(build_income_band)
    df["issue_month"] = df["issue_date"].dt.to_period("M").astype(str)

    # Save cleaned feature table
    feature_path = processed_dir / "loan_features.csv"
    df.to_csv(feature_path, index=False)

    # Power BI / SQL support tables
    kpi_summary = pd.DataFrame(
        {
            "metric_name": [
                "Total Loans",
                "Total Defaults",
                "Default Rate",
                "Average Loan Amount",
                "Average Interest Rate",
                "Average Credit Score",
            ],
            "metric_value": [
                len(df),
                int(df["default_flag"].sum()),
                float(df["default_flag"].mean()),
                float(df["loan_amount"].mean()),
                float(df["interest_rate"].mean()),
                float(df["credit_score"].mean()),
            ],
        }
    )
    kpi_summary.to_csv(processed_dir / "kpi_summary.csv", index=False)

    segment_default_rates = (
        df.groupby(["grade", "purpose", "income_band"], as_index=False)
        .agg(total_loans=("loan_id", "count"), defaults=("default_flag", "sum"))
    )
    segment_default_rates["default_rate"] = segment_default_rates["defaults"] / segment_default_rates["total_loans"]
    segment_default_rates.to_csv(processed_dir / "segment_default_rates.csv", index=False)

    print(f"Saved processed data to: {processed_dir}")
    print(f"Feature table rows: {len(df)}")


if __name__ == "__main__":
    main()
