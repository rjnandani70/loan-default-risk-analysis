from pathlib import Path
import warnings
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def main() -> None:
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="sklearn")

    project_root = Path(__file__).resolve().parents[1]
    processed_dir = project_root / "data" / "processed"
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    data_path = processed_dir / "loan_features.csv"
    df = pd.read_csv(data_path)

    target_col = "default_flag"
    drop_cols = ["loan_id", "issue_date", "issue_month"]
    X = df.drop(columns=[target_col] + drop_cols)
    y = df[target_col]

    numeric_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    solver="liblinear",
                    C=0.5,
                ),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    auc = roc_auc_score(y_test, y_prob)
    report = classification_report(y_test, y_pred)

    metrics_text = (
        "Loan Default Model Results\n"
        "==========================\n"
        f"ROC-AUC: {auc:.4f}\n\n"
        "Classification Report:\n"
        f"{report}\n"
    )

    metrics_path = reports_dir / "model_metrics.txt"
    metrics_path.write_text(metrics_text, encoding="utf-8")

    scored = df[["loan_id", "grade", "purpose", "state", "loan_amount", "interest_rate", "default_flag"]].copy()
    scored["pred_default_probability"] = model.predict_proba(X)[:, 1]
    scored["risk_band"] = pd.cut(
        scored["pred_default_probability"],
        bins=[0.0, 0.30, 0.60, 1.0],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    )
    scored.to_csv(processed_dir / "risk_scored_loans.csv", index=False)

    print(f"Model metrics saved: {metrics_path}")
    print(f"ROC-AUC: {auc:.4f}")


if __name__ == "__main__":
    main()
