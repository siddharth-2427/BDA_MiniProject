# Academic Review Demonstration Guide

## Step-by-Step Walkthrough

1. **Cluster Verification**:
   - Access NameNode Web UI: `http://localhost:9870`
   - Access YARN ResourceManager UI: `http://localhost:8088`
   - Access Hive UI: `http://localhost:10002`

2. **Data Ingestion & HDFS Check**:
   - Demonstrate raw CSV upload to `/solar/raw/` in HDFS.
   - Run `hdfs dfs -ls -R /solar`.

3. **Spark & MapReduce Execution**:
   - Run Spark ETL job: PySpark on YARN parses, cleans, joins generation and weather data.
   - Run MapReduce job: Hadoop Streaming calculates daily plant energy directly from raw CSV.
   - Show YARN application execution in ResourceManager UI (`http://localhost:8088`).

4. **Hive Warehousing**:
   - Show Beeline execution & query external Parquet tables.

5. **ML Training & Serving**:
   - Chronological split, scikit-learn model evaluation (MAE, RMSE, R²).
   - Real-time weather-conditioned inference API & React Dashboard.
