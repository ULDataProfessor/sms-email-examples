"""Accounting firm invoice pipeline demonstration."""

import csv
from typing import List, Dict

def ingest_data(path: str) -> List[Dict[str, str]]:
    """Read invoice data from a CSV file."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def analyze_data(invoices: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Select unpaid invoices."""
    return [inv for inv in invoices if inv.get("paid", "no").lower() != "yes"]

def process_data(unpaid: List[Dict[str, str]]) -> List[str]:
    """Prepare reminder messages."""
    messages = []
    for inv in unpaid:
        client = inv.get("client", "Client")
        amount = inv.get("amount", "0")
        messages.append(f"Reminder: {client} owes ${amount}.")
    return messages

def output_results(messages: List[str]) -> None:
    for msg in messages:
        print(msg)

def main() -> None:
    path = input("Path to invoice CSV: ")
    invoices = ingest_data(path)
    unpaid = analyze_data(invoices)
    messages = process_data(unpaid)
    output_results(messages)

if __name__ == "__main__":
    main()
