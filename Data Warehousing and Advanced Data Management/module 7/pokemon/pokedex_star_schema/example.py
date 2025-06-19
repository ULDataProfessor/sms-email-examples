"""Star schema demonstration for Pokédex encounters."""

from typing import Dict, List


POKEMON_DIM = {
    1: {"pokemon_name": "Bulbasaur", "type": "grass"},
    4: {"pokemon_name": "Charmander", "type": "fire"},
}

TRAINER_DIM = {10: {"trainer_name": "Ash"}, 20: {"trainer_name": "Misty"}}

FACT_TABLE = [
    {"encounter_id": 100, "trainer_id": 10, "pokemon_id": 1, "location": "Pallet"},
    {"encounter_id": 101, "trainer_id": 20, "pokemon_id": 4, "location": "Cerulean"},
]


def star_join() -> List[Dict[str, str]]:
    """Join fact rows with dimension lookups."""

    results: List[Dict[str, str]] = []
    for row in FACT_TABLE:
        pokemon = POKEMON_DIM[row["pokemon_id"]]
        trainer = TRAINER_DIM[row["trainer_id"]]
        joined = {
            **row,
            **pokemon,
            **trainer,
        }
        results.append(joined)
    return results


def main() -> None:
    rows = star_join()
    for r in rows:
        print(r)


if __name__ == "__main__":
    main()

