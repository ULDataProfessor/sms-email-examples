"""Simulate Change Data Capture for Pokémon trades."""

from typing import Dict, List


def apply_event(target: Dict[int, Dict[str, str]], event: Dict[str, str]) -> None:
    """Apply an insert or update event to the target table."""

    trade_id = int(event["trade_id"])
    op = event.get("op")
    if op == "insert" or trade_id not in target:
        target[trade_id] = event
    elif op == "update":
        target[trade_id].update(event)


def main() -> None:
    events: List[Dict[str, str]] = [
        {
            "trade_id": 1,
            "op": "insert",
            "trainer_a": "Ash",
            "trainer_b": "Misty",
            "pokemon": "Staryu",
        },
        {
            "trade_id": 1,
            "op": "update",
            "pokemon": "Psyduck",
        },
    ]

    target: Dict[int, Dict[str, str]] = {}
    for e in events:
        apply_event(target, e)

    print("Current trades:")
    for trade in target.values():
        print(trade)


if __name__ == "__main__":
    main()

