import sys
import json
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def run_analytics(features_input_path: str, output_path: str):
    spark = SparkSession.builder \
        .appName("Solar_Analytics_Daily") \
        .config("spark.sql.parquet.outputTimestampType", "TIMESTAMP_MILLIS") \
        .getOrCreate()

    print(f"[SPARK_ANALYTICS] Reading features from: {features_input_path}")
    df = spark.read.parquet(features_input_path)

    daily_analytics = df \
        .withColumn("date_str", F.date_format("timestamp", "yyyy-MM-dd")) \
        .groupBy("plant_id", "date_str") \
        .agg(
            (F.sum("AC_POWER_KW") * 0.25).alias("daily_energy_kwh"),
            F.max("AC_POWER_KW").alias("peak_power_kw"),
            F.avg("IRRADIATION").alias("mean_irradiation"),
            F.avg("AMBIENT_TEMPERATURE").alias("mean_ambient_temp"),
            F.max("MODULE_TEMPERATURE").alias("max_module_temp")
        ) \
        .orderBy("plant_id", "date_str")

    count = daily_analytics.count()
    print(f"[SPARK_ANALYTICS] Computed {count} daily summary rows. Writing Parquet to: {output_path}")

    daily_analytics.write \
        .mode("overwrite") \
        .parquet(output_path)

    metrics = {"daily_summary_rows": count}
    print("[SPARK_ANALYTICS_METRICS_JSON] " + json.dumps(metrics))
    spark.stop()

if __name__ == "__main__":
    inp_path = sys.argv[1] if len(sys.argv) > 1 else "hdfs://namenode:9000/solar/processed/features"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "hdfs://namenode:9000/solar/analytics/daily"
    run_analytics(inp_path, out_path)
