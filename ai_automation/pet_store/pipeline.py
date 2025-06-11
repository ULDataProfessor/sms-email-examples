"""Pet store adoption pipeline demonstration."""

import json
from typing import List, Dict

def ingest_data() -> List[Dict[str, str]]:
    """Collect adoption records as JSON lines from the user."""
    print("Enter adoption records as JSON (blank line to finish):")
    records = []
    while True:
        line = input()
        if not line:
            break
        records.append(json.loads(line))
    return records

def analyze_data(records: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Find young animals needing vet checks."""
    return [r for r in records if r.get("age", 0) < 1]

def process_data(needs_check: List[Dict[str, str]]) -> List[str]:
    """Create follow‑up messages."""
    messages = []
    for pet in needs_check:
        name = pet.get("name", "Unknown")
        species = pet.get("species", "pet")
        messages.append(f"Schedule first vet visit for {name} the {species}.")
    return messages

def output_results(messages: List[str]) -> None:
    for msg in messages:
        print(msg)

def main() -> None:
    records = ingest_data()
    needs_check = analyze_data(records)
    messages = process_data(needs_check)
    output_results(messages)

if __name__ == "__main__":
    main()
