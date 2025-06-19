import pandas as pd

# Track transformations with metadata


class LineageTracker:
    def __init__(self):
        self.steps = []

    def record(self, description: str):
        self.steps.append(description)

    def report(self):
        print("Lineage:")
        for i, step in enumerate(self.steps, 1):
            print(f"{i}. {step}")


def main() -> None:
    tracker = LineageTracker()
    df = pd.DataFrame({"value": [1, 2, 3, 4, 5]})
    tracker.record("Loaded initial data")

    df = df[df["value"] > 2]
    tracker.record("Filtered values greater than 2")

    df["value_squared"] = df["value"] ** 2
    tracker.record("Added squared column")

    tracker.report()


if __name__ == "__main__":
    main()

