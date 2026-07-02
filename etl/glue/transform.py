# GridPulse — Transformation Layer
# Deployed as an AWS Glue Spark ETL job (gridpulse-transform)
# Engine: Glue 4.0, Spark, 2x G.1X workers
# Role: gridpulse-glue-role (AWSGlueServiceRole + S3 access)
#
# Reads raw OWID energy data, cleans it, computes derived year-over-year
# metrics, and writes curated Parquet output partitioned by year.

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.window import Window

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

RAW_PATH = "s3://gridpulse-preethi-ds/raw/owid-energy-data.csv"
CURATED_PATH = "s3://gridpulse-preethi-ds/curated/energy_curated/"

# --- Extract: read raw CSV ---
df = spark.read.option("header", "true").option("inferSchema", "true").csv(RAW_PATH)

# --- Transform ---
keep_cols = [
    "country", "year", "iso_code", "population",
    "electricity_generation", "electricity_demand",
    "coal_electricity", "gas_electricity", "oil_electricity",
    "nuclear_electricity", "hydro_electricity", "wind_electricity",
    "solar_electricity", "other_renewable_electricity",
    "fossil_electricity", "renewables_electricity", "low_carbon_electricity",
    "renewables_share_elec", "low_carbon_share_elec", "fossil_share_elec",
    "carbon_intensity_elec"
]
df = df.select(*keep_cols)

# Keep real countries only (drop null iso_code = regional aggregates like "World", "Europe")
# and focus on recent, analysis-ready years
df = df.filter((F.col("iso_code").isNotNull()) & (F.col("year") >= 2000))

# Drop rows with no generation data at all (nothing to analyze)
df = df.filter(F.col("electricity_generation").isNotNull())

# Fill remaining nulls in numeric fields with 0 (source didn't report that fuel type = none generated)
numeric_cols = [c for c in keep_cols if c not in ("country", "year", "iso_code")]
df = df.fillna(0, subset=numeric_cols)

# Derived metric: year-over-year change in renewable share, per country
w = Window.partitionBy("country").orderBy("year")
df = df.withColumn("renewables_share_yoy_change",
                    F.round(F.col("renewables_share_elec") - F.lag("renewables_share_elec").over(w), 2))

df = df.withColumn("generation_yoy_pct_change",
                    F.round(((F.col("electricity_generation") - F.lag("electricity_generation").over(w))
                              / F.lag("electricity_generation").over(w)) * 100, 2))

# --- Load: write curated Parquet, partitioned by year ---
df.write.mode("overwrite").partitionBy("year").parquet(CURATED_PATH)

job.commit()
