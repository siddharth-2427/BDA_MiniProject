#!/usr/bin/env bash
set -e

INPUT_PATH=${1:-"/solar/raw/generation/*/*"}
OUTPUT_PATH=${2:-"/solar/analytics/mr_daily"}

echo "[MAPREDUCE] Locating hadoop-streaming jar..."
STREAMING_JAR=$(find $HADOOP_HOME -name 'hadoop-streaming*.jar' | head -n 1)

if [ -z "$STREAMING_JAR" ]; then
    echo "[MAPREDUCE_ERROR] hadoop-streaming jar not found in $HADOOP_HOME"
    exit 1
fi

echo "[MAPREDUCE] Found streaming jar: $STREAMING_JAR"
echo "[MAPREDUCE] Cleaning previous output directory $OUTPUT_PATH if exists..."
$HADOOP_HOME/bin/hdfs dfs -rm -r -f $OUTPUT_PATH || true

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

echo "[MAPREDUCE] Submitting MapReduce job to YARN..."
$HADOOP_HOME/bin/hadoop jar $STREAMING_JAR \
    -files $SCRIPT_DIR/mapper.py,$SCRIPT_DIR/reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py" \
    -input $INPUT_PATH \
    -output $OUTPUT_PATH

echo "[MAPREDUCE] MapReduce job finished successfully. Output in $OUTPUT_PATH:"
$HADOOP_HOME/bin/hdfs dfs -ls $OUTPUT_PATH
