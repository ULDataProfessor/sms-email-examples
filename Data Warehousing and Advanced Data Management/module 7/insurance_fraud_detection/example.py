import pandas as pd

# Load claims data and check for anomalies


def detect_fraud(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    mean = df["amount"].mean()
    std = df["amount"].std()
    return df[(df["amount"] - mean).abs() > threshold * std]


def main() -> None:
    claims = pd.DataFrame({"claim_id": [1, 2, 3, 4], "amount": [100.0, 120.0, 5000.0, 110.0]})
    flagged = detect_fraud(claims)
    print(flagged)


if __name__ == "__main__":
    main()

