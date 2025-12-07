"""
CSC 4760/6760 Big Data Programming Assignment 4, Question 3
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# I placed the data files in this location 
WORKERS_JSON_PATH = "file:///opt/spark-data/assignment4/workers.json"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Q3 SQL Query Analysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.ansi.enabled", "false") \
    .getOrCreate()

print("\n" + "=" * 80)
print("METHOD 3: SPARK SQL QUERY SENTENCES (Question 3)")
print("=" * 80)
print("\nApproach: Using SQL queries on registered DataFrame table")
print("-" * 80)

# Load JSON using ABSOLUTE path
df = spark.read.json(WORKERS_JSON_PATH)

# Clean Salary column: remove commas and convert to numeric
df = df.withColumn("SalaryNumeric", 
                    regexp_replace(col("Salary"), ",", "").cast("double"))

# Create temporary SQL view
df.createOrReplaceTempView("workers")

# Define SQL query
sql_query = """
SELECT 
    Gender,
    Department,
    AVG(SalaryNumeric) as AvgSalary
FROM workers
WHERE Department IS NOT NULL AND Gender IS NOT NULL
GROUP BY Department, Gender
ORDER BY Gender, Department
"""

print("\nSQL Query:")
print("-" * 80)
print(sql_query)

# Execute SQL query
sql_result = spark.sql(sql_query)

# Display results
print("\nSQL Query Results (Table Format):")
print("-" * 80)
sql_result.show(truncate=False)

print("\nSQL Query Results (Formatted):")
print("-" * 80)

# We use collect to retrieve all the data from the DataFrame
sql_rows = sql_result.collect()
for row in sql_rows:
    print(f"{row['Gender']:8s} {row['Department']:10s}: ${row['AvgSalary']:12,.2f}")

# Stop Spark session
spark.stop()