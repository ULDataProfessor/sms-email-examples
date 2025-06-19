import pandas as pd

# Extract features from raw data


def build_feature_store(raw: pd.DataFrame) -> pd.DataFrame:
    features = raw.groupby("user_id")[["event"]].count().rename(columns={"event": "event_count"})
    features.reset_index(inplace=True)
    return features


def main() -> None:
    raw = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 2, 2, 3],
            "event": ["a", "b", "a", "a", "c", "b"],
        }
    )
    store = build_feature_store(raw)
    print(store)


if __name__ == "__main__":
    main()

