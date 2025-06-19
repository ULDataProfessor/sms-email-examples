"""Store Pokémon data partitioned by generation using CSV files."""

import csv
from pathlib import Path
from typing import Dict, List


POKEMON = [
    {"id": 1, "name": "Bulbasaur", "generation": 1},
    {"id": 4, "name": "Charmander", "generation": 1},
    {"id": 152, "name": "Chikorita", "generation": 2},
    {"id": 255, "name": "Torchic", "generation": 3},
]


def write_partitioned(base: Path) -> None:
    """Write sample data into generation-specific folders."""

    for row in POKEMON:
        folder = base / f"generation_{row['generation']}"
        folder.mkdir(parents=True, exist_ok=True)
        file = folder / "pokemon.csv"
        write_header = not file.exists()
        with open(file, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "generation"])
            if write_header:
                writer.writeheader()
            writer.writerow(row)


def read_generation(base: Path, generation: int) -> List[Dict[str, str]]:
    """Load Pokémon rows for the given generation."""

    file = base / f"generation_{generation}" / "pokemon.csv"
    if not file.exists():
        return []
    with open(file, newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    base = Path("pokemon_by_generation")
    write_partitioned(base)
    gen1 = read_generation(base, 1)
    print("Generation 1:", gen1)


if __name__ == "__main__":
    main()

