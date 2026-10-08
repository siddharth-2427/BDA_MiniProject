#!/usr/bin/env bash
set -e

echo "[HIVE_INIT] Waiting for HiveServer2 at localhost:10000..."
until nc -z localhost 10000; do
    echo "[HIVE_INIT] HiveServer2 is not ready yet... retrying in 3 seconds"
    sleep 3
done

echo "[HIVE_INIT] HiveServer2 is reachable. Creating database 'solar' if not exists..."
$HIVE_HOME/bin/beeline -u jdbc:hive2://localhost:10000 -e "CREATE DATABASE IF NOT EXISTS solar;"

echo "[HIVE_INIT] Hive database 'solar' initialized successfully."
