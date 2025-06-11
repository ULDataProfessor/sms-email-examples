import argparse
import joblib
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Score new customer data")
    parser.add_argument("model", help="Path to saved model")
    parser.add_argument("input_csv", help="CSV with customer features")
    parser.add_argument(
        "output_csv",
        nargs="?",
        default="scores.csv",
        help="Where to save predictions",
    )
    args = parser.parse_args()

    model = joblib.load(args.model)
    df = pd.read_csv(args.input_csv)
    user_ids = df.get("user_id")
    X = df.drop(columns=["user_id"], errors="ignore")

    preds = model.predict(X)
    probs = model.predict_proba(X)[:, 1]

    results = pd.DataFrame(
        {
            "user_id": user_ids,
            "churn_prediction": preds,
            "churn_probability": probs,
        }
    )
    results.to_csv(args.output_csv, index=False)
    print(f"Predictions saved to {args.output_csv}")


if __name__ == "__main__":
    main()
