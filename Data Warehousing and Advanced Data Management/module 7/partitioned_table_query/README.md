# partitioned_table_query
Partitioning splits a dataset into separate directories or files, often by date. Query engines can then read only the partitions relevant to a request, improving performance. This example generates a Parquet dataset with date partitions and demonstrates querying a single partition. Such techniques are essential for managing very large tables efficiently.
