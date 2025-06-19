import pandas as pd

# Extract and persist features for ML


def extract_features(raw: pd.DataFrame) -> pd.DataFrame:
    feats = raw.groupby("label")[["value"]].mean().rename(columns={"value": "avg_value"})
    feats.reset_index(inplace=True)
    return feats


def train_model(features: pd.DataFrame) -> None:
    try:
        from sklearn.linear_model import LogisticRegression
    except Exception:
        print("scikit-learn not installed; skipping model training")
        return

    X = features[["avg_value"]]
    y = features["label"]
    model = LogisticRegression().fit(X, y)
    print("Model coefficients:", model.coef_)


def main() -> None:
    raw = pd.DataFrame({"label": [0, 0, 1, 1], "value": [1.0, 2.0, 3.0, 4.0]})
    feats = extract_features(raw)
    feats.to_csv("features.csv", index=False)
    train_model(feats)


if __name__ == "__main__":
    main()

