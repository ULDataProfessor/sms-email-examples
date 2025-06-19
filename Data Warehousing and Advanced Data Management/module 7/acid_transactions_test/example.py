import pandas as pd


def run_transaction(table: pd.DataFrame, operation):
    """Run an operation with basic rollback on failure."""
    working = table.copy()
    try:
        operation(working)
    except Exception as exc:  # rollback on any error
        print(f"Transaction failed: {exc}. Rolling back.")
        return table
    else:
        return working


def main() -> None:
    # Base table representing account balances
    balances = pd.DataFrame({"id": [1, 2], "balance": [100, 200]})

    def deposit_to_id1(df: pd.DataFrame) -> None:
        df.loc[df["id"] == 1, "balance"] += 50

    def withdraw_from_id2(df: pd.DataFrame) -> None:
        df.loc[df["id"] == 2, "balance"] -= 300
        if df.loc[df["id"] == 2, "balance"].iloc[0] < 0:
            raise ValueError("Negative balance not allowed")

    print("Before transactions:\n", balances)
    balances = run_transaction(balances, deposit_to_id1)
    balances = run_transaction(balances, withdraw_from_id2)
    print("After transactions:\n", balances)


if __name__ == "__main__":
    main()

