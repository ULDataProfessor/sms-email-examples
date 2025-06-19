import pandas as pd

# Read JSON events representing changes
events = [
    {"op": "insert", "id": 1, "name": "Alice"},
    {"op": "insert", "id": 2, "name": "Bob"},
    {"op": "update", "id": 1, "name": "Alicia"},
]


def apply_events(events, table=None):
    if table is None:
        table = pd.DataFrame(columns=["id", "name"])

    for evt in events:
        if evt["op"] == "insert":
            table = pd.concat([table, pd.DataFrame([{"id": evt["id"], "name": evt["name"]}])], ignore_index=True)
        elif evt["op"] == "update":
            mask = table["id"] == evt["id"]
            table.loc[mask, "name"] = evt["name"]
    return table


def main() -> None:
    target = apply_events(events)
    print(target)


if __name__ == "__main__":
    main()

