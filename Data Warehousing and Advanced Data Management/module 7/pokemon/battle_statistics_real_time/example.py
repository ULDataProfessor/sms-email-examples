"""Simple simulation of real-time battle log ingestion."""

import time
from typing import Dict, List


def ingest_battles(max_events: int = 5, delay: float = 0.1) -> List[Dict[str, str]]:
    """Simulate streaming battle records.

    Each event is appended to an in-memory list representing the target table.

    Parameters
    ----------
    max_events:
        How many battle events to generate.
    delay:
        Time to wait between events to mimic streaming.
    """

    logs: List[Dict[str, str]] = []
    for i in range(max_events):
        event = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "attacker": f"Pokemon_{i % 3}",
            "defender": f"Pokemon_{(i + 1) % 3}",
            "winner": "attacker" if i % 2 == 0 else "defender",
        }
        logs.append(event)
        time.sleep(delay)
    return logs


if __name__ == "__main__":
    battle_logs = ingest_battles()
    for log in battle_logs:
        print(log)
