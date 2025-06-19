"""Demonstrate a tiny feature store for legendary Pokémon."""

import json
from pathlib import Path
from typing import Dict, Iterable, List


LEGENDARIES = [
    {"name": "Mewtwo", "base_power": 680, "generation": 1},
    {"name": "Lugia", "base_power": 680, "generation": 2},
]


def register_features(store: Path, features: Iterable[Dict[str, object]]) -> None:
    """Append feature dictionaries to a JSON file."""

    store.parent.mkdir(exist_ok=True)
    data: List[Dict[str, object]] = []
    if store.exists():
        with open(store) as f:
            data = json.load(f)
    data.extend(features)
    with open(store, "w") as f:
        json.dump(data, f)


def load_features(store: Path) -> List[Dict[str, object]]:
    """Retrieve all registered features."""

    if not store.exists():
        return []
    with open(store) as f:
        return json.load(f)


def main() -> None:
    store = Path("legendary_features.json")
    register_features(store, LEGENDARIES)
    all_features = load_features(store)
    print("Registered features:")
    for feat in all_features:
        print(feat)


if __name__ == "__main__":
    main()

