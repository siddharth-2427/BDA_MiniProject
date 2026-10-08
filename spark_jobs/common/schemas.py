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
