# Troubleshooting Guide

## Common Issues & Solutions

### 1. Hive 3.1.3 Guava Conflict with Hadoop 3.3.6
- **Symptom**: `NoSuchMethodError: com.google.common.base.Preconditions.checkArgument` when starting HiveServer2 or running `schematool`.
- **Solution**: The Hive container build replaces Hive's bundled `lib/guava-19.0.jar` with Hadoop 3.3.6's `guava-27.0-jre.jar`.

### 2. YARN NodeManager Memory Limits on Laptop
- **Symptom**: Spark jobs killed or failing with memory allocation errors.
- **Solution**: `yarn-site.xml` sets `yarn.nodemanager.resource.memory-mb` to 4096MB and disables virtual memory check (`yarn.nodemanager.vmem-check-enabled=false`).

### 3. Timestamp Parquet Compatibility
- **Symptom**: Hive cannot read Spark Parquet timestamps.
- **Solution**: Spark jobs explicitly set `spark.sql.parquet.outputTimestampType=TIMESTAMP_MILLIS`.
