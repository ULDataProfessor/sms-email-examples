import pandas as pd

# Create a base and summary table


def refresh_materialized_view(base: pd.DataFrame) -> pd.DataFrame:
    return base.groupby("product")[["amount"]].sum().reset_index()


def main() -> None:
    base = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "product": ["A", "A", "B", "A"],
            "amount": [10, 5, 7, 3],
        }
    )
    view = refresh_materialized_view(base)
    print(view)


if __name__ == "__main__":
    main()

