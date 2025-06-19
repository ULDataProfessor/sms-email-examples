import pandas as pd

# Simulate time-series sensor ingestion

def rollup_hourly(df: pd.DataFrame) -> pd.DataFrame:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    return df.resample("H").mean().reset_index()


def main() -> None:
    data = pd.DataFrame(
        {
            "timestamp": pd.date_range("2023-01-01 00:00", periods=6, freq="30min"),
            "reading": [1, 2, 3, 4, 5, 6],
        }
    )
    hourly = rollup_hourly(data)
    print(hourly)


if __name__ == "__main__":
    main()

