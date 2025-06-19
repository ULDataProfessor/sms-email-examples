"""Minimal lakehouse style table using DuckDB and Parquet."""

import duckdb
import pandas as pd


def create_table(path: str) -> None:
    con = duckdb.connect()
    df = pd.DataFrame({"id": [1, 2, 3], "value": ["a", "b", "c"]})
    con.execute("CREATE TABLE tmp AS SELECT * FROM df")
    con.execute(f"COPY tmp TO '{path}' (FORMAT parquet)")
    con.close()


def read_table(path: str) -> pd.DataFrame:
    con = duckdb.connect()
    result = con.execute(f"SELECT * FROM read_parquet('{path}')").fetchdf()
    con.close()
    return result


def main() -> None:
    create_table("lakehouse.parquet")
    print(read_table("lakehouse.parquet"))


if __name__ == "__main__":
    main()

