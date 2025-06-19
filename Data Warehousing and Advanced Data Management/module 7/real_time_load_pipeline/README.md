# real_time_load_pipeline
Real-time pipelines ingest data continuously rather than in scheduled batches. They might use streaming platforms like Kafka to collect events as they occur. Such architectures keep the warehouse nearly synchronized with operational systems. This directory sketches a loop that appends incoming records to a table.
