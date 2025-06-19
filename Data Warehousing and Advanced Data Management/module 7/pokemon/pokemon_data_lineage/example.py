"""Track simple dataset lineage for Pokémon transformations."""

from typing import Any, Dict, List


class Dataset:
    def __init__(self, data: List[Dict[str, Any]], lineage: List[str] | None = None):
        self.data = data
        self.lineage = lineage or []

    def filter_fire(self) -> "Dataset":
        filtered = [row for row in self.data if row["type"] == "fire"]
        return Dataset(filtered, self.lineage + ["Filtered fire type"])

    def add_power_score(self) -> "Dataset":
        scored = [dict(row, power=row["base"] * 2) for row in self.data]
        return Dataset(scored, self.lineage + ["Added power score"])


def display_lineage(ds: Dataset) -> None:
    print("Lineage:")
    for i, step in enumerate(ds.lineage, 1):
        print(f"{i}. {step}")


def main() -> None:
    raw = Dataset([
        {"name": "Charmander", "type": "fire", "base": 39},
        {"name": "Squirtle", "type": "water", "base": 44},
    ], ["Loaded raw data"])

    fire_only = raw.filter_fire()
    scored = fire_only.add_power_score()
    display_lineage(scored)


if __name__ == "__main__":
    main()

