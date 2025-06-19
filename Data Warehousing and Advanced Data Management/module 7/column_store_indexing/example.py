import duckdb

# Create a table and compare columnar vs row scans

con = duckdb.connect()
con.execute("CREATE TABLE numbers AS SELECT i AS id, i*2 AS value FROM range(100000)")

# Columnar scan selecting a single column
print(con.execute("EXPLAIN SELECT value FROM numbers WHERE id < 10").fetchall()[0][0])

# Row scan selecting all columns
print(con.execute("EXPLAIN SELECT * FROM numbers WHERE id < 10").fetchall()[0][0])

con.close()

