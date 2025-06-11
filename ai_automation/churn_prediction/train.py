import argparse
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report


def load_data(csv_path: str):
    """Load customer activity CSV."""
    return pd.read_csv(csv_path)


def build_pipeline(df: pd.DataFrame):
    """Create preprocessing and modeling pipeline."""
    X = df.drop(columns=["churn_flag", "user_id"], errors="ignore")
    y = df["churn_flag"]

    categorical_cols = X.select_dtypes(include=["object", "category"]).columns
    numeric_cols = X.select_dtypes(include=["number"]).columns

    preprocessor = ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("numeric", StandardScaler(), numeric_cols),
    ])

    clf = RandomForestClassifier(random_state=42)
    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", clf),
    ])
    return pipeline, X, y


def main():
    parser = argparse.ArgumentParser(description="Train churn prediction model")
    parser.add_argument("csv", help="Path to training CSV file")
    parser.add_argument("model_output", help="Path to save the trained model")
    args = parser.parse_args()

    df = load_data(args.csv)
    pipeline, X, y = build_pipeline(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline.fit(X_train, y_train)

    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, preds)
    roc_auc = roc_auc_score(y_test, probs)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"ROC-AUC: {roc_auc:.4f}")
    print(classification_report(y_test, preds))

    joblib.dump(pipeline, args.model_output)
    print(f"Model saved to {args.model_output}")


if __name__ == "__main__":
    main()
