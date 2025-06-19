import pandas as pd

# Read data from a CSV file


def run_pipeline(src: str, dest: str) -> None:
    df = pd.read_csv(src)
    # simple transformation: keep rows with value > 5
    df = df[df["value"] > 5]
    df["value_doubled"] = df["value"] * 2
    df.to_csv(dest, index=False)


if __name__ == "__main__":
    # create sample input
    sample = pd.DataFrame({"value": range(10)})
    sample.to_csv("input.csv", index=False)
    run_pipeline("input.csv", "output.csv")

