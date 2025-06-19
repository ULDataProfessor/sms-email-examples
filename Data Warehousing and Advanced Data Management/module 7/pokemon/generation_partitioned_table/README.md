# generation_partitioned_table
Each generation of Pokémon introduces new species and mechanics. This example demonstrates storing Pokémon data in Parquet files partitioned by generation for efficient queries. Analysts can quickly load a single generation without scanning the entire dataset. Partitioning also keeps storage manageable as new generations are released.
