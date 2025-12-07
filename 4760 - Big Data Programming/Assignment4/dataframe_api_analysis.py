"""
CSC 4760/6760 Big Data Programming Assignment 4, Question 2
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, regexp_replace

# I placed the data files in this location 
WORKERS_JSON_PATH = "file:///opt/spark-data/assignment4/workers.json"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Q2 DataFrame API Analysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.ansi.enabled", "false") \
    .getOrCreate()

print("\n" + "=" * 80)
print("METHOD 2: SPARK SQL DATAFRAME APIs (Question 2)")
print("=" * 80)
print("\nApproach: Using DataFrame groupBy and aggregation functions")
print("-" * 80)

# Load JSON using ABSOLUTE path
df = spark.read.json(WORKERS_JSON_PATH)

# Display schema
print("\nDataFrame Schema:")
df.printSchema()

# Clean Salary column: remove commas and convert to numeric
df = df.withColumn("SalaryNumeric", 
                    regexp_replace(col("Salary"), ",", "").cast("double"))

# Group by Department and Gender, then compute average salary
df_avg = df.groupBy("Department", "Gender") \
    .agg(avg("SalaryNumeric").alias("AvgSalary")) \
    .filter(col("Department").isNotNull() & col("Gender").isNotNull()) \
    .orderBy("Gender", "Department")

# Display results
print("\nDataFrame API Results (Table Format):")
print("-" * 80)
df_avg.show(truncate=False)

print("\nDataFrame API Results (Formatted):")
print("-" * 80)

# We use collect to retrieve all the data from the DataFrame
df_results = df_avg.collect()


for row in df_results:
    gender = row['Gender'] if row['Gender'] is not None else "Unknown"
    dept = row['Department'] if row['Department'] is not None else "Unknown"
    
    # Check if AvgSalary is None
    if row['AvgSalary'] is not None:
        print(f"{gender:8s} {dept:10s}: ${row['AvgSalary']:12,.2f}")

# Stop Spark session
spark.stop()