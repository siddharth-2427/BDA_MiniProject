import sys
import json
import math
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

GENERATION_SCHEMA = StructType([
    StructField("DATE_TIME", StringType(), True),
    StructField("PLANT_ID", LongType(), True),
    StructField("SOURCE_KEY", StringType(), True),
    StructField("DC_POWER", DoubleType(), True),
    StructField("AC_POWER", DoubleType(), True),
    StructField("DAILY_YIELD", DoubleType(), True),
    StructField("TOTAL_YIELD", DoubleType(), True)
])

WEATHER_SCHEMA = StructType([
    StructField("DATE_TIME", StringType(), True),
    StructField("PLANT_ID", LongType(), True),
    StructField("SOURCE_KEY", StringType(), True),
    StructField("AMBIENT_TEMPERATURE", DoubleType(), True),
    StructField("MODULE_TEMPERATURE", DoubleType(), True),
    StructField("IRRADIATION", DoubleType(), True)
])

def run_etl(gen_input_path: str, weather_input_path: str, output_path: str):
    spark = SparkSession.builder \
        .appName("Solar_ETL_Clean_Join") \
        .config("spark.sql.parquet.outputTimestampType", "TIMESTAMP_MILLIS") \
        .getOrCreate()

    print(f"[SPARK_ETL] Reading generation data from: {gen_input_path}")
    gen_df = spark.read.csv(gen_input_path, header=True, schema=GENERATION_SCHEMA)
    rows_in_gen = gen_df.count()

    print(f"[SPARK_ETL] Reading weather data from: {weather_input_path}")
    weather_df = spark.read.csv(weather_input_path, header=True, schema=WEATHER_SCHEMA)
    rows_in_weather = weather_df.count()

    # Drop exact duplicates
    gen_df_dedup = gen_df.dropDuplicates()
    weather_df_dedup = weather_df.dropDuplicates()
    
    dups_removed_gen = rows_in_gen - gen_df_dedup.count()
    dups_removed_weather = rows_in_weather - weather_df_dedup.count()

    # Parse timestamps
    gen_ts = gen_df_dedup.withColumn(
        "timestamp",
        F.coalesce(
            F.to_timestamp("DATE_TIME", "dd-MM-yyyy HH:mm"),
            F.to_timestamp("DATE_TIME", "yyyy-MM-dd HH:mm:ss"),
            F.to_timestamp("DATE_TIME", "dd-MM-yyyy HH:mm:ss")
        )
    ).filter(F.col("timestamp").isNotNull() & F.col("AC_POWER").isNotNull() & F.col("PLANT_ID").isNotNull())

    weather_ts = weather_df_dedup.withColumn(
        "timestamp",
        F.coalesce(
            F.to_timestamp("DATE_TIME", "yyyy-MM-dd HH:mm:ss"),
            F.to_timestamp("DATE_TIME", "dd-MM-yyyy HH:mm"),
            F.to_timestamp("DATE_TIME", "dd-MM-yyyy HH:mm:ss")
        )
    ).filter(F.col("timestamp").isNotNull() & F.col("PLANT_ID").isNotNull())

    # Aggregate inverters -> plant-level AC/DC power per timestamp
    gen_plant = gen_ts.groupBy("PLANT_ID", "timestamp").agg(
        F.sum("AC_POWER").alias("AC_POWER_KW"),
        F.sum("DC_POWER").alias("DC_POWER_KW"),
        F.count("SOURCE_KEY").alias("inverter_count")
    )

    # Weather per plant per timestamp
    weather_plant = weather_ts.groupBy("PLANT_ID", "timestamp").agg(
        F.avg("AMBIENT_TEMPERATURE").alias("AMBIENT_TEMPERATURE"),
        F.avg("MODULE_TEMPERATURE").alias("MODULE_TEMPERATURE"),
        F.avg("IRRADIATION").alias("IRRADIATION")
    )

    # Inner Join generation and weather data
    joined_df = gen_plant.join(weather_plant, on=["PLANT_ID", "timestamp"], how="inner")

    # Feature Engineering
    TWO_PI = 2 * math.pi
    featured_df = joined_df \
        .withColumn("hour", F.hour("timestamp")) \
        .withColumn("minute_of_day", F.hour("timestamp") * 60 + F.minute("timestamp")) \
        .withColumn("sin_time", F.sin(F.col("minute_of_day") * (TWO_PI / 1440.0))) \
        .withColumn("cos_time", F.cos(F.col("minute_of_day") * (TWO_PI / 1440.0))) \
        .withColumn("day_index", F.datediff(F.col("timestamp"), F.to_date(F.lit("2020-05-01")))) \
        .withColumn("is_daylight", F.when(F.col("IRRADIATION") > 0.001, 1).otherwise(0)) \
        .withColumn("plant_id", F.col("PLANT_ID"))

    rows_out = featured_df.count()

    print(f"[SPARK_ETL] Writing features Parquet to: {output_path}")
    featured_df.write \
        .mode("overwrite") \
        .partitionBy("plant_id") \
        .parquet(output_path)

    metrics = {
        "rows_in_generation": rows_in_gen,
        "rows_in_weather": rows_in_weather,
        "duplicates_removed_gen": dups_removed_gen,
        "duplicates_removed_weather": dups_removed_weather,
        "rows_out_features": rows_out
    }
    print("[SPARK_ETL_METRICS_JSON] " + json.dumps(metrics))
    spark.stop()

if __name__ == "__main__":
    gen_path = sys.argv[1] if len(sys.argv) > 1 else "hdfs://namenode:9000/solar/raw/generation/*/*"
    weather_path = sys.argv[2] if len(sys.argv) > 2 else "hdfs://namenode:9000/solar/raw/weather/*/*"
    out_path = sys.argv[3] if len(sys.argv) > 3 else "hdfs://namenode:9000/solar/processed/features"
    run_etl(gen_path, weather_path, out_path)
