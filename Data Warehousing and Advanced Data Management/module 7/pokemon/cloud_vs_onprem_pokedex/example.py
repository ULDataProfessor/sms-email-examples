"""Compare querying a cloud vs on-prem Pokédex warehouse."""

import sqlite3
from typing import List, Tuple


def setup_db(conn: sqlite3.Connection) -> None:
    """Create a simple Pokédex table and insert a few rows."""

    conn.execute(
        "CREATE TABLE IF NOT EXISTS pokedex (id INTEGER PRIMARY KEY, name TEXT)"
    )
    if not conn.execute("SELECT 1 FROM pokedex").fetchone():
        conn.executemany(
            "INSERT INTO pokedex (name) VALUES (?)",
            [("Bulbasaur",), ("Charmander",), ("Squirtle",)],
        )
        conn.commit()


def run_query(conn: sqlite3.Connection, query: str) -> List[Tuple[int, str]]:
    """Execute a query and return all rows."""

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def main() -> None:
    # Simulated cloud and on-prem databases using SQLite in-memory databases
    cloud_conn = sqlite3.connect(":memory:")
    onprem_conn = sqlite3.connect(":memory:")

    for conn in (cloud_conn, onprem_conn):
        setup_db(conn)

    query = "SELECT * FROM pokedex"
    cloud_results = run_query(cloud_conn, query)
    onprem_results = run_query(onprem_conn, query)

    print("Cloud results:", cloud_results)
    print("On-prem results:", onprem_results)


if __name__ == "__main__":
    main()
