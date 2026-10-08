CREATE DATABASE IF NOT EXISTS solar;
USE solar;

-- External Hive table over PySpark processed features Parquet
CREATE EXTERNAL TABLE IF NOT EXISTS solar.features (
    `timestamp` TIMESTAMP,
    `AC_POWER_KW` DOUBLE,
    `DC_POWER_KW` DOUBLE,
    `inverter_count` INT,
    `AMBIENT_TEMPERATURE` DOUBLE,
    `MODULE_TEMPERATURE` DOUBLE,
    `IRRADIATION` DOUBLE,
    `hour` INT,
    `minute_of_day` INT,
    `sin_time` DOUBLE,
    `cos_time` DOUBLE,
    `day_index` INT,
    `is_daylight` INT
)
PARTITIONED BY (plant_id BIGINT)
STORED AS PARQUET
LOCATION '/solar/processed/features';

MSCK REPAIR TABLE solar.features;

-- External Hive table over PySpark daily analytics Parquet
CREATE EXTERNAL TABLE IF NOT EXISTS solar.daily_energy (
    `date_str` STRING,
    `daily_energy_kwh` DOUBLE,
    `peak_power_kw` DOUBLE,
    `mean_irradiation` DOUBLE,
    `mean_ambient_temp` DOUBLE,
    `max_module_temp` DOUBLE
)
PARTITIONED BY (plant_id BIGINT)
STORED AS PARQUET
LOCATION '/solar/analytics/daily';

MSCK REPAIR TABLE solar.daily_energy;

-- External Hive table over MapReduce daily energy output
CREATE EXTERNAL TABLE IF NOT EXISTS solar.mr_daily_energy (
    plant_date_key STRING,
    daily_energy_kwh DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LOCATION '/solar/analytics/mr_daily';
