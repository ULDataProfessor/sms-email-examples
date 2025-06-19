import pandas as pd
from pathlib import Path

# Generate partitioned Parquet files


def create_partitions(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame({"date": ["2023-01-01", "2023-01-02"], "value": [1, 2]})
    for date, group in df.groupby("date"):
        sub = path / date
        sub.mkdir(parents=True, exist_ok=True)
        group.to_parquet(sub / "data.parquet", index=False)


def read_partition(path: Path, date: str) -> pd.DataFrame:
    return pd.read_parquet(path / date / "data.parquet")


def main() -> None:
    base = Path("partitions")
    create_partitions(base)
    print(read_partition(base, "2023-01-02"))


if __name__ == "__main__":
    main()

