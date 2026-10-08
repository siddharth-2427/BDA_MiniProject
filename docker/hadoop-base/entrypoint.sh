#!/usr/bin/env bash
set -e

ROLE=${NODE_ROLE:-$1}

echo "[HADOOP-BASE] Starting node role: ${ROLE}"

if [ "$ROLE" = "namenode" ]; then
    if [ ! -d "/hadoop/dfs/name/current" ]; then
        echo "[HADOOP-BASE] Formatting NameNode..."
        $HADOOP_HOME/bin/hdfs namenode -format -force -nonInteractive
    fi
    echo "[HADOOP-BASE] Executing NameNode..."
    exec $HADOOP_HOME/bin/hdfs namenode

elif [ "$ROLE" = "datanode" ]; then
    echo "[HADOOP-BASE] Executing DataNode..."
    exec $HADOOP_HOME/bin/hdfs datanode

elif [ "$ROLE" = "resourcemanager" ]; then
    echo "[HADOOP-BASE] Executing ResourceManager..."
    exec $HADOOP_HOME/bin/yarn resourcemanager

elif [ "$ROLE" = "nodemanager" ]; then
    echo "[HADOOP-BASE] Executing NodeManager..."
    exec $HADOOP_HOME/bin/yarn nodemanager

elif [ "$ROLE" = "hive" ]; then
    if [ ! -d "/opt/hive/metastore_db" ]; then
        echo "[HADOOP-BASE] Initializing Hive Metastore DB..."
        $HIVE_HOME/bin/schematool -dbType derby -initSchema
    fi
    echo "[HADOOP-BASE] Executing HiveServer2..."
    exec $HIVE_HOME/bin/hiveserver2

else
    exec "$@"
fi
