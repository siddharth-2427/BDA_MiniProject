# System Architecture

## Distributed Big Data & Analytics Pipeline

```mermaid
flowchart TD
    subgraph Data Layer
        A[Weather & Solar CSV Data] -->|Subprocess Ingestion| B[HDFS Primary Storage]
    end

    subgraph Processing Layer (YARN)
        B --> C[Spark PySpark ETL & Analytics]
        B --> D[MapReduce Hadoop Streaming]
        C -->|Parquet Files| E[HDFS Processed Zone]
        D -->|Text/CSV Files| F[HDFS MR Daily Zone]
    end

    subgraph Data Warehousing
        E --> G[Hive External Tables]
        F --> G
    end

    subgraph Machine Learning & Application
        E -->|hdfs dfs -get| H[Scikit-Learn ML Training]
        H -->|joblib model artifacts| I[FastAPI REST Server]
        G -->|Beeline JDBC CSV| I
    end

    subgraph Frontend User Interface
        I --> J[React + Vite + Recharts Dashboard]
    end
```

## Implemented vs Theoretical Scalability
- **Local Cluster Environment**: This deployment operates as a fully functional pseudo-distributed Hadoop cluster running inside Docker containers on a single host. It provides full YARN resource management, Spark submission, HDFS storage, and Hive query execution.
- **Production Scalability**: In a multi-node production deployment, HDFS DataNodes and YARN NodeManagers scale horizontally across physical worker nodes. Scale testing with synthetic replicated data demonstrates Spark vs Pandas runtime performance scaling under increasing dataset volumes.
