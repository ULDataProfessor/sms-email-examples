"""Bank transaction analysis pipeline demonstration."""

import csv
from typing import List, Dict

def ingest_data(path: str) -> List[Dict[str, str]]:
    """Load transactions from a CSV file."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def analyze_data(transactions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Flag large transactions as potential fraud."""
    flagged = []
    for t in transactions:
        amount = float(t.get("amount", 0))
        if amount > 10000:
            flagged.append(t)
    return flagged

def process_data(flagged: List[Dict[str, str]]) -> List[str]:
    """Format flagged transactions for reporting."""
    return [f"Potential fraud: id={t.get('id')} amount=${t.get('amount')}" for t in flagged]

def output_results(reports: List[str]) -> None:
    for line in reports:
        print(line)

def main() -> None:
    path = input("Path to transactions CSV: ")
    transactions = ingest_data(path)
    flagged = analyze_data(transactions)
    reports = process_data(flagged)
    output_results(reports)

if __name__ == "__main__":
    main()
