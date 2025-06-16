# Multi-Source Data Extraction

**Objective:**  
Build a reusable Python module that:
- Connects to a REST API (JSON) and a local SQLite database
- Extracts data from both sources
- Normalizes into a single Pandas DataFrame

**Codex Prompt:**  
“Write a Python module with two functions: `fetch_api_data()` (uses `requests` to GET JSON from `https://api.example.com/data`) and `fetch_db_data()` (uses `sqlite3` to SELECT rows from `data.db`). Combine results into a Pandas DataFrame and return it.”
