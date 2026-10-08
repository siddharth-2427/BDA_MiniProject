#!/usr/bin/env bash
set -e

echo "=== HDFS DFSADMIN REPORT ==="
$HADOOP_HOME/bin/hdfs dfsadmin -report

echo "=== HDFS DIRECTORY LISTING ==="
$HADOOP_HOME/bin/hdfs dfs -ls -R /solar || echo "HDFS directories not yet initialized."

echo "=== YARN NODE LIST ==="
$HADOOP_HOME/bin/yarn node -list

echo "=== YARN APPLICATIONS ==="
$HADOOP_HOME/bin/yarn application -list -appStates ALL

echo "=== HIVE TABLES ==="
$HIVE_HOME/bin/beeline -u jdbc:hive2://hive:10000 -e "SHOW TABLES IN solar;" || echo "Hive not yet initialized."
