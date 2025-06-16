# Database Automation

**Objective:**  
Automate data load:
- Read `data.csv`
- Upsert rows into PostgreSQL table `public.data_table`
- Use `psycopg2` with transactions and parameterized queries

**Codex Prompt:**  
“Create a Python script using `psycopg2` that reads `data.csv` with Pandas and upserts each row into a PostgreSQL `data_table`. Use `ON CONFLICT` for upsert behavior and commit per batch of 100 rows.”
