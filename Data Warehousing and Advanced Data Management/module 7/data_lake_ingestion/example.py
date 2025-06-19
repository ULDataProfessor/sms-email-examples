from pathlib import Path
import json

# Simulate landing JSON or Parquet files by date

def ingest_files(base: Path) -> None:
    base.mkdir(exist_ok=True)
    for day in ["2023-01-01", "2023-01-02", "2023-01-03"]:
        folder = base / day
        folder.mkdir(parents=True, exist_ok=True)
        data = {"day": day, "value": 42}
        with open(folder / "data.json", "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    ingest_files(Path("lake"))

