import pandas as pd

# Load a sample transactional dataset


def main() -> None:
    transactions = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "product": ["A", "B", "A"],
            "qty": [2, 1, 4],
        }
    )
    # Insert
    transactions.loc[len(transactions)] = [4, "B", 2]
    # Update
    transactions.loc[transactions["id"] == 2, "qty"] = 3

    # Aggregate for OLAP style query
    summary = transactions.groupby("product")[["qty"]].sum()
    print("Transactions:\n", transactions)
    print("Summary:\n", summary)


if __name__ == "__main__":
    main()

