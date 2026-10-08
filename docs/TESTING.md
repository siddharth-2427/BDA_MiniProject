# Comprehensive Testing Documentation

## Mandatory Verification Commands

```bash
# Docker Stack Status
docker compose ps

# HDFS Cluster Health
docker compose exec namenode hdfs dfsadmin -report

# HDFS Directory Inspection
docker compose exec namenode hdfs dfs -ls -R /solar

# YARN Node Status
docker compose exec resourcemanager yarn node -list

# YARN Application History
docker compose exec resourcemanager yarn application -list -appStates ALL

# Hive Table Verification
docker compose exec hive beeline -u jdbc:hive2://localhost:10000 -e "SHOW TABLES IN solar;"

# FastAPI Backend Health Check
curl http://localhost:8000/health
```

## Backend Unit & Integration Tests
Run pytest from the backend directory:
```bash
pytest backend/tests/
```

## Frontend Unit & Component Tests
Run Vitest from the frontend directory:
```bash
npm --prefix frontend test
```
