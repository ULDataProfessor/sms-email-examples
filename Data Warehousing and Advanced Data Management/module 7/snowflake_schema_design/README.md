# snowflake_schema_design
A snowflake schema further normalizes dimension tables into additional sub-tables. While this reduces data redundancy, it introduces more joins for queries. Snowflake models work well when dimension hierarchies are complex or shared between facts. Here we model the same data as the star schema but spread dimensions across multiple tables.
