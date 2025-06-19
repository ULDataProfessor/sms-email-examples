import pandas as pd
from datetime import date

# Track patient address changes with SCD Type 2


def insert_address(history: pd.DataFrame, patient_id: int, address: str, start: date) -> pd.DataFrame:
    if not history.empty:
        mask = (history["patient_id"] == patient_id) & (history["end_date"].isna())
        history.loc[mask, "end_date"] = start
    new_row = {"patient_id": patient_id, "address": address, "start_date": start, "end_date": pd.NaT}
    return pd.concat([history, pd.DataFrame([new_row])], ignore_index=True)


def main() -> None:
    history = pd.DataFrame(columns=["patient_id", "address", "start_date", "end_date"])
    history = insert_address(history, 1, "123 A St", date(2020, 1, 1))
    history = insert_address(history, 1, "456 B Ave", date(2021, 6, 1))
    print(history)


if __name__ == "__main__":
    main()

