#!/bin/bash
set -e

BASE_DIR="Data Warehousing and Advanced Data Management/module 7"

mkdir -p "$BASE_DIR"

# 1. oltp_vs_olap
mkdir -p "$BASE_DIR/oltp_vs_olap"
cat > "$BASE_DIR/oltp_vs_olap/README.md" <<'EOT'
# oltp_vs_olap
Online Transaction Processing (OLTP) focuses on quick, atomic transactions for day-to-day operations. Online Analytical Processing (OLAP) supports complex queries over historical data to drive business insights. OLTP emphasizes speed and data integrity, while OLAP optimizes for aggregations and reporting. This folder demonstrates how the two styles differ when inserting, updating, and summarizing data.
EOT
cat > "$BASE_DIR/oltp_vs_olap/example.py" <<'EOT'
import pandas as pd

# Load a sample transactional dataset
# TODO: Demonstrate insert and update operations
# TODO: Perform an aggregate query for analysis
EOT

# 2. star_schema_design
mkdir -p "$BASE_DIR/star_schema_design"
cat > "$BASE_DIR/star_schema_design/README.md" <<'EOT'
# star_schema_design
A star schema organizes data with a central fact table linked to several dimension tables. This design simplifies queries and accelerates analytics by minimizing joins. Facts store measurable business events, while dimensions provide descriptive attributes. In this example we define a small fact table and two dimensions to show how the pieces fit together.
EOT
cat > "$BASE_DIR/star_schema_design/example.py" <<'EOT'
import pandas as pd

# Create fact and dimension DataFrames
# TODO: Join them to produce a star-schema style result
EOT

# 3. snowflake_schema_design
mkdir -p "$BASE_DIR/snowflake_schema_design"
cat > "$BASE_DIR/snowflake_schema_design/README.md" <<'EOT'
# snowflake_schema_design
A snowflake schema further normalizes dimension tables into additional sub-tables. While this reduces data redundancy, it introduces more joins for queries. Snowflake models work well when dimension hierarchies are complex or shared between facts. Here we model the same data as the star schema but spread dimensions across multiple tables.
EOT
cat > "$BASE_DIR/snowflake_schema_design/example.py" <<'EOT'
import pandas as pd

# Create normalized dimension tables and a fact table
# TODO: Demonstrate joining three or more tables
EOT

# 4. etl_basic_pipeline
mkdir -p "$BASE_DIR/etl_basic_pipeline"
cat > "$BASE_DIR/etl_basic_pipeline/README.md" <<'EOT'
# etl_basic_pipeline
Extract-Transform-Load (ETL) pipelines move data from source systems into a warehouse. The extract step gathers raw records, transform cleans or reshapes them, and load writes them to the target store. Simple pipelines often work with CSV files or API responses. This folder illustrates a minimal pipeline that reads a file, filters rows, and writes out the result.
EOT
cat > "$BASE_DIR/etl_basic_pipeline/example.py" <<'EOT'
import pandas as pd

# Read data from a CSV file
# TODO: Apply transformations and load to a new destination
EOT

# 5. staging_area_pipeline
mkdir -p "$BASE_DIR/staging_area_pipeline"
cat > "$BASE_DIR/staging_area_pipeline/README.md" <<'EOT'
# staging_area_pipeline
A staging area temporarily stores raw data before final processing. Using staging tables lets you validate and clean records without impacting production tables. Once vetted, the data moves into its permanent location. This example outlines how to keep separate staging and production DataFrames.
EOT
cat > "$BASE_DIR/staging_area_pipeline/example.py" <<'EOT'
import pandas as pd

# Load raw data into a staging DataFrame
# TODO: Clean and transfer it to a production DataFrame
EOT

# 6. data_lake_ingestion
mkdir -p "$BASE_DIR/data_lake_ingestion"
cat > "$BASE_DIR/data_lake_ingestion/README.md" <<'EOT'
# data_lake_ingestion
Data lakes store large volumes of varied data in its native format. Proper ingestion organizes files by ingestion date or source, making retrieval easier. Many architectures land raw JSON or Parquet files in partitioned folders. This demo simulates depositing files into a date-based hierarchy.
EOT
cat > "$BASE_DIR/data_lake_ingestion/example.py" <<'EOT'
from pathlib import Path

# Simulate landing JSON or Parquet files by date
# TODO: Create dated folders and place sample files within them
EOT

# 7. lakehouse_architecture
mkdir -p "$BASE_DIR/lakehouse_architecture"
cat > "$BASE_DIR/lakehouse_architecture/README.md" <<'EOT'
# lakehouse_architecture
A lakehouse combines the storage flexibility of a data lake with the management features of a warehouse. Table formats such as Delta Lake or Apache Iceberg provide ACID transactions and schema enforcement on files. The approach allows both analytics and machine learning from the same underlying data. This folder contains a stub for creating a simple lakehouse table.
EOT
cat > "$BASE_DIR/lakehouse_architecture/example.py" <<'EOT'
# Example uses Delta Lake or Apache Iceberg libraries
# TODO: Create a table and demonstrate basic writes and reads
EOT

# 8. feature_store_workflow
mkdir -p "$BASE_DIR/feature_store_workflow"
cat > "$BASE_DIR/feature_store_workflow/README.md" <<'EOT'
# feature_store_workflow
Feature stores centralize curated features for machine learning projects. They keep training and serving data consistent and track metadata about how features are produced. Building a simple feature store requires extracting features from raw data and registering them for later reuse. This directory walks through that workflow with a small DataFrame example.
EOT
cat > "$BASE_DIR/feature_store_workflow/example.py" <<'EOT'
import pandas as pd

# Extract features from raw data
# TODO: Register them in a feature store DataFrame
EOT

# 9. cdc_streaming_load
mkdir -p "$BASE_DIR/cdc_streaming_load"
cat > "$BASE_DIR/cdc_streaming_load/README.md" <<'EOT'
# cdc_streaming_load
Change Data Capture (CDC) streams data modifications from source systems to targets in real time. By applying inserts and updates as they occur, warehouses stay current without batch loads. Streaming CDC is common for replicating operational databases into analytics platforms. This stub shows how to read a stream of events and apply them to a table.
EOT
cat > "$BASE_DIR/cdc_streaming_load/example.py" <<'EOT'
import pandas as pd

# Read JSON events representing changes
# TODO: Apply insert and update operations to a target DataFrame
EOT

# 10. partitioned_table_query
mkdir -p "$BASE_DIR/partitioned_table_query"
cat > "$BASE_DIR/partitioned_table_query/README.md" <<'EOT'
# partitioned_table_query
Partitioning splits a dataset into separate directories or files, often by date. Query engines can then read only the partitions relevant to a request, improving performance. This example generates a Parquet dataset with date partitions and demonstrates querying a single partition. Such techniques are essential for managing very large tables efficiently.
EOT
cat > "$BASE_DIR/partitioned_table_query/example.py" <<'EOT'
import pandas as pd

# Generate partitioned Parquet files
# TODO: Read only one partition for querying
EOT

# 11. materialized_view_demo
mkdir -p "$BASE_DIR/materialized_view_demo"
cat > "$BASE_DIR/materialized_view_demo/README.md" <<'EOT'
# materialized_view_demo
Materialized views store the results of a query physically on disk. They allow fast access to aggregated or precomputed data without running the base query each time. Periodic refreshes keep the view synchronized with the underlying tables. This folder includes a stub for creating and refreshing a summary table.
EOT
cat > "$BASE_DIR/materialized_view_demo/example.py" <<'EOT'
import pandas as pd

# Create a base and summary table
# TODO: Refresh the materialized view from the base table
EOT

# 12. column_store_indexing
mkdir -p "$BASE_DIR/column_store_indexing"
cat > "$BASE_DIR/column_store_indexing/README.md" <<'EOT'
# column_store_indexing
Column-store indexes store each column separately, greatly speeding up analytics queries. Databases like DuckDB or SQL Server columnstore use this format for fast scans and compression. By comparing columnar and row-based access, you can see the performance difference. The stub here sets up a table and hints at measuring both approaches.
EOT
cat > "$BASE_DIR/column_store_indexing/example.py" <<'EOT'
import duckdb

# Create a table and compare columnar vs row scans
# TODO: Show timing differences with EXPLAIN or benchmarking
EOT

# 13. acid_transactions_test
mkdir -p "$BASE_DIR/acid_transactions_test"
cat > "$BASE_DIR/acid_transactions_test/README.md" <<'EOT'
# acid_transactions_test
ACID properties—Atomicity, Consistency, Isolation, Durability—are critical for reliable databases. Testing these guarantees often involves running concurrent transactions and deliberately causing failures. A compliant system should roll back partial changes on errors. This directory illustrates how to simulate such a scenario with DataFrames.
EOT
cat > "$BASE_DIR/acid_transactions_test/example.py" <<'EOT'
import pandas as pd

# Simulate two concurrent transactions
# TODO: Demonstrate rollback behavior on error
EOT

# 14. data_lineage_tracking
mkdir -p "$BASE_DIR/data_lineage_tracking"
cat > "$BASE_DIR/data_lineage_tracking/README.md" <<'EOT'
# data_lineage_tracking
Data lineage explains how data moves and transforms across systems. Capturing lineage helps with debugging, auditing, and impact analysis for future changes. Even simple pipelines can track lineage by annotating transformations with metadata. This folder proposes a small lineage graph built from pandas operations.
EOT
cat > "$BASE_DIR/data_lineage_tracking/example.py" <<'EOT'
import pandas as pd

# Track transformations with metadata
# TODO: Output a simple lineage graph or report
EOT

# 15. semantic_layer_views
mkdir -p "$BASE_DIR/semantic_layer_views"
cat > "$BASE_DIR/semantic_layer_views/README.md" <<'EOT'
# semantic_layer_views
A semantic layer provides business-friendly views over raw tables. By defining consistent metrics and labels, it allows analysts to query data without knowing low-level details. Semantic views can be built with SQL or programmatically generated. This example outlines how to create such views using pandas or SQLAlchemy.
EOT
cat > "$BASE_DIR/semantic_layer_views/example.py" <<'EOT'
import pandas as pd

# Define semantic views over raw tables
# TODO: Expose them for easy analyst consumption
EOT

# 16. real_time_load_pipeline
mkdir -p "$BASE_DIR/real_time_load_pipeline"
cat > "$BASE_DIR/real_time_load_pipeline/README.md" <<'EOT'
# real_time_load_pipeline
Real-time pipelines ingest data continuously rather than in scheduled batches. They might use streaming platforms like Kafka to collect events as they occur. Such architectures keep the warehouse nearly synchronized with operational systems. This directory sketches a loop that appends incoming records to a table.
EOT
cat > "$BASE_DIR/real_time_load_pipeline/example.py" <<'EOT'
# Pseudo streaming ingestion example
# TODO: Append records to a table in real time using a loop or Kafka client
EOT

# 17. retail_data_warehouse_case
mkdir -p "$BASE_DIR/retail_data_warehouse_case"
cat > "$BASE_DIR/retail_data_warehouse_case/README.md" <<'EOT'
# retail_data_warehouse_case
Retail warehouses consolidate sales, inventory, and customer data for reporting. Key metrics like monthly sales and product performance drive merchandising decisions. This case study loads sample fact and dimension data to produce a simple summary. It showcases typical retail analytics patterns in a warehouse setting.
EOT
cat > "$BASE_DIR/retail_data_warehouse_case/example.py" <<'EOT'
import pandas as pd

# Load sales facts and store dimensions
# TODO: Produce a monthly sales summary
EOT

# 18. insurance_fraud_detection
mkdir -p "$BASE_DIR/insurance_fraud_detection"
cat > "$BASE_DIR/insurance_fraud_detection/README.md" <<'EOT'
# insurance_fraud_detection
Insurance companies analyze claims data to uncover fraudulent activity. Anomalies such as unusually high payouts or suspicious patterns can indicate fraud. Data warehouses store large claim histories that fuel these analyses. This example hints at loading claims and applying basic anomaly detection logic.
EOT
cat > "$BASE_DIR/insurance_fraud_detection/example.py" <<'EOT'
import pandas as pd

# Load claims data and check for anomalies
# TODO: Implement simple fraud detection logic
EOT

# 19. healthcare_data_warehouse
mkdir -p "$BASE_DIR/healthcare_data_warehouse"
cat > "$BASE_DIR/healthcare_data_warehouse/README.md" <<'EOT'
# healthcare_data_warehouse
Healthcare warehouses integrate patient records from many clinical systems. They often manage slowly changing dimensions to keep historical attributes like patient addresses. Proper handling ensures analytics maintain accuracy over time. This stub demonstrates a type 2 slowly changing dimension using pandas.
EOT
cat > "$BASE_DIR/healthcare_data_warehouse/example.py" <<'EOT'
import pandas as pd

# Track patient address changes with SCD Type 2
# TODO: Implement inserts with start and end dates for each version
EOT

# 20. iot_dashboard_warehouse
mkdir -p "$BASE_DIR/iot_dashboard_warehouse"
cat > "$BASE_DIR/iot_dashboard_warehouse/README.md" <<'EOT'
# iot_dashboard_warehouse
IoT devices generate time-series data that must be ingested and rolled up for dashboards. Warehouses aggregate readings by time intervals such as hourly or daily to highlight trends. This case shows how sensor data can be summarized after ingestion. It provides a framework for building an IoT reporting warehouse.
EOT
cat > "$BASE_DIR/iot_dashboard_warehouse/example.py" <<'EOT'
import pandas as pd

# Simulate time-series sensor ingestion
# TODO: Roll up readings by hour for dashboard use
EOT

# 21. ml_feature_store_example
mkdir -p "$BASE_DIR/ml_feature_store_example"
cat > "$BASE_DIR/ml_feature_store_example/README.md" <<'EOT'
# ml_feature_store_example
Machine learning projects benefit from a managed feature store that serves both training and online prediction. Features extracted from raw sources are stored with versioning so they remain consistent across datasets. This example saves derived features, then loads them into a scikit-learn pipeline. It illustrates the bridge between data engineering and ML workflows.
EOT
cat > "$BASE_DIR/ml_feature_store_example/example.py" <<'EOT'
import pandas as pd

# Extract and persist features for ML
# TODO: Load them into a scikit-learn training pipeline
EOT

# 22. cloud_vs_onprem_warehouse
mkdir -p "$BASE_DIR/cloud_vs_onprem_warehouse"
cat > "$BASE_DIR/cloud_vs_onprem_warehouse/README.md" <<'EOT'
# cloud_vs_onprem_warehouse
Choosing between cloud and on-premises data warehouses involves trade-offs in scalability, cost, and maintenance. Cloud solutions like AWS Redshift offer elasticity and managed services, while on-prem systems provide direct control over hardware. Organizations often evaluate security, performance, and budget when making this decision. This folder contrasts configuration steps for each approach.
EOT
cat > "$BASE_DIR/cloud_vs_onprem_warehouse/example.py" <<'EOT'
# Outline configuration for cloud vs. on-prem warehouses
# TODO: Compare setup steps for Redshift and PostgreSQL
EOT

# 23. performance_optimization
mkdir -p "$BASE_DIR/performance_optimization"
cat > "$BASE_DIR/performance_optimization/README.md" <<'EOT'
# performance_optimization
Query performance can be improved through indexing, partitioning, and query tuning. Measuring execution plans helps identify slow operations and opportunities for optimization. By comparing two versions of the same query, you can see the impact of changes. This directory contains a stub for timing and explaining queries.
EOT
cat > "$BASE_DIR/performance_optimization/example.py" <<'EOT'
import pandas as pd

# Prepare sample queries to compare performance
# TODO: Use EXPLAIN plans or timing to evaluate each query
EOT

