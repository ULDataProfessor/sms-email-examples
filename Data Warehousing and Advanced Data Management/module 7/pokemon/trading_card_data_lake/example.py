"""Organize trading card data in a date-partitioned lake."""

import json
from pathlib import Path
from typing import List, Dict


CARDS = [
    {"id": 1, "name": "Pikachu", "release": "2023-01-01"},
    {"id": 2, "name": "Bulbasaur", "release": "2023-01-02"},
]


def write_cards(base: Path) -> None:
    """Write card JSON files partitioned by release date."""

    for card in CARDS:
        folder = base / card["release"]
        folder.mkdir(parents=True, exist_ok=True)
        with open(folder / f"{card['id']}.json", "w") as f:
            json.dump(card, f)


def read_release(base: Path, release: str) -> List[Dict[str, object]]:
    """Read all cards for a given release date."""

    folder = base / release
    cards: List[Dict[str, object]] = []
    for file in folder.glob("*.json"):
        with open(file) as f:
            cards.append(json.load(f))
    return cards


def main() -> None:
    lake = Path("card_lake")
    write_cards(lake)
    jan1_cards = read_release(lake, "2023-01-01")
    print("Cards released on 2023-01-01:", jan1_cards)


if __name__ == "__main__":
    main()

