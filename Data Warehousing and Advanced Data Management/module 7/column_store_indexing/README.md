# column_store_indexing
Column-store indexes store each column separately, greatly speeding up analytics queries. Databases like DuckDB or SQL Server columnstore use this format for fast scans and compression. By comparing columnar and row-based access, you can see the performance difference. The stub here sets up a table and hints at measuring both approaches.
