#!/usr/bin/env bash
set -e

echo "[HDFS_INIT] Initializing HDFS directory structure for Solar Big Data..."

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/raw/generation
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/raw/weather
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/processed/features
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/analytics/daily
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/analytics/mr_daily
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /solar/uploads

$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /solar

echo "[HDFS_INIT] HDFS directory structure created successfully:"
$HADOOP_HOME/bin/hdfs dfs -ls -R /solar
