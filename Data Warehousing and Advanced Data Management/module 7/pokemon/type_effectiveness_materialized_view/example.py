"""Materialized view summarizing Pokémon type effectiveness."""

from typing import Dict, Tuple, Set


TYPE_MATCHUPS = [
    ("fire", "grass", "super"),
    ("water", "fire", "super"),
    ("grass", "water", "super"),
    ("fire", "water", "weak"),
]


def create_materialized_view(data: list[Tuple[str, str, str]]) -> Set[Tuple[str, str, str]]:
    """Build the materialized view as a set of matchups."""

    return set(data)


def refresh_view(view: Set[Tuple[str, str, str]], data: list[Tuple[str, str, str]]) -> Set[Tuple[str, str, str]]:
    """Refresh the view when base data changes."""

    return create_materialized_view(data)


def main() -> None:
    view = create_materialized_view(TYPE_MATCHUPS)
    print("Initial view:", view)

    # Add a new relationship and refresh
    TYPE_MATCHUPS.append(("electric", "water", "super"))
    view = refresh_view(view, TYPE_MATCHUPS)
    print("Refreshed view:", view)


if __name__ == "__main__":
    main()

