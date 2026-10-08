# Renewable Energy Generation Prediction Using Weather Analytics

A scalable Big Data engineering pipeline and predictive analytics application for solar power plants. Built with Hadoop 3.3.6, PySpark 3.5.3, YARN, Hive 3.1.3, MapReduce Streaming, Scikit-Learn ML, FastAPI backend, and React dashboard.

## Mandatory Pipeline Architecture

```
Weather Data + Historical Solar Data 
        │
        ▼
   Data Ingestion 
        │
        ▼
   HDFS Primary Storage 
        │
        ▼
Spark / MapReduce (on YARN)
        │
        ▼
   Hive Warehousing 
        │
        ▼
Python / scikit-learn ML 
        │
        ▼
Predicted Solar Generation (FastAPI & React Dashboard)
```

## System Features
- **HDFS Distributed Storage**: Pseudo-distributed NameNode and DataNode cluster storing raw CSVs, processed Parquet partitions, and MapReduce outputs.
- **Spark on YARN**: Distributed PySpark ETL job (`etl_clean_join.py`) and PySpark Daily Analytics job (`analytics_daily.py`).
- **MapReduce Hadoop Streaming**: Python MapReduce job (`mapreduce/mapper.py` & `mapreduce/reducer.py`) calculating daily energy yield directly from raw CSV for cross-verification.
- **Hive SQL Data Warehouse**: External Hive tables over Parquet and CSV paths with 5 analytical queries.
- **Weather-Conditioned Machine Learning**: Scikit-learn models (Linear Regression, Random Forest, Gradient Boosting, Naive Baseline) trained using chronological splits (overall vs daylight-only R² metrics).
- **FastAPI & React Web Interface**: Full RESTful backend with background job tracking (`state/jobs/`) and interactive React + Recharts frontend.

## Quick Start
1. **Clone repository & prepare environment**:
   ```bash
   cp .env.example .env
   ```
2. **Start Docker Cluster**:
   ```bash
   docker compose up -d --build
   ```
3. **Initialize Cluster Storage & Data Warehouse**:
   ```bash
   docker compose exec namenode /bin/bash /scripts/hdfs_init.sh
   docker compose exec hive /bin/bash /scripts/hive_init.sh
   ```
4. **Access Web Interfaces**:
   - **React Dashboard**: `http://localhost:3000`
   - **FastAPI Documentation**: `http://localhost:8000/docs`
   - **HDFS NameNode UI**: `http://localhost:9870`
   - **YARN ResourceManager UI**: `http://localhost:8088`
   - **HiveServer2 Web UI**: `http://localhost:10002`

## Documentation Links
- [System Architecture](docs/ARCHITECTURE.md)
- [Dataset Specifications](docs/DATASET.md)
- [Environment & Setup Guide](docs/SETUP.md)
- [Academic Demonstration Guide](docs/DEMO.md)
- [Testing & Verification Guide](docs/TESTING.md)
- [Troubleshooting & Gotchas](docs/TROUBLESHOOTING.md)
