from duckdb_io_manager import DuckDBPartitionedParquetIOManager
from postgres_io_manager import PostgresIOManager



RESOURCES_STAGING = {
    "warehouse_io_manager": PostgresIOManager(database="DEMO_DB_STAGING", **SHARED_SNOWFLAKE_CONF),
}


RESOURCES_LOCAL = {
    "warehouse_io_manager": DuckDBPartitionedParquetIOManager(
        pyspark=configured_pyspark,
        duckdb_path=os.path.join(DBT_PROJECT_DIR, "tutorial.duckdb"),
    ),
}