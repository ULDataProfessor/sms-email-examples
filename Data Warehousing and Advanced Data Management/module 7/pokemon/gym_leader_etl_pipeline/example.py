"""Example ETL pipeline for gym leader battle records."""

import csv
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List


def extract(csv_file: Path) -> List[Dict[str, str]]:
    """Read battle records from a CSV file."""

    with open(csv_file, newline="") as f:
        return list(csv.DictReader(f))


def transform(records: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    """Normalize raw records to a common schema."""

    transformed = []
    for row in records:
        transformed.append(
            {
                "gym": row["gym"].title(),
                "leader": row["leader"].title(),
                "pokemon": row["pokemon"].title(),
                "result": row["result"].lower(),
            }
        )
    return transformed


def load(db_path: Path, rows: Iterable[Dict[str, str]]) -> None:
    """Load rows into a SQLite table."""

    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS gym_battles (gym TEXT, leader TEXT, pokemon TEXT, result TEXT)"
    )
    conn.executemany(
        "INSERT INTO gym_battles VALUES (:gym, :leader, :pokemon, :result)", rows
    )
    conn.commit()
    conn.close()


def main() -> None:
    sample_csv = Path("battles.csv")
    # Create a small sample CSV if one does not exist
    if not sample_csv.exists():
        with open(sample_csv, "w", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["gym", "leader", "pokemon", "result"]
            )
            writer.writeheader()
            writer.writerows(
                [
                    {
                        "gym": "Pewter",
                        "leader": "Brock",
                        "pokemon": "Onix",
                        "result": "WIN",
                    },
                    {
                        "gym": "Cerulean",
                        "leader": "Misty",
                        "pokemon": "Staryu",
                        "result": "LOSS",
                    },
                ]
            )

    raw = extract(sample_csv)
    rows = transform(raw)
    load(Path("gym_battles.db"), rows)
    print(f"Loaded {len(rows)} battle records")


if __name__ == "__main__":
    main()

