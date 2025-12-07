"""
CSC 4760/6760 Big Data Programming Assignment 4, Question 4
"""

from pyspark.sql import SparkSession
import pyspark.pandas as ps

# I placed the data files in this location 
WORKERS_JSON_PATH = "file:///opt/spark-data/assignment4/workers.json"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Q4 Pandas on Spark Analysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.ansi.enabled", "false") \
    .getOrCreate()

print("\n" + "=" * 80)
print("METHOD 4: PANDAS ON SPARK (Question 4)")
print("=" * 80)
print("\nApproach: Using Pandas API on distributed Spark DataFrames")
print("-" * 80)

# Load JSON using ABSOLUTE path
ps_df = ps.read_json(WORKERS_JSON_PATH)

# Display first few rows
print("\nPandas on Spark DataFrame (First 5 rows):")
print("-" * 80)
print(ps_df.head())

# Clean salary column
ps_df['Salary'] = ps_df['Salary'].str.replace(',', '').astype(float)

# Drop rows where Department or Gender is null
ps_df = ps_df.dropna(subset=['Department', 'Gender'])

# Group and compute mean
ps_avg = ps_df.groupby(['Department', 'Gender'])['Salary'].mean()

# Display results
print("\nPandas on Spark Results:")
print("-" * 80)
print(ps_avg)
print()

# Convert for formatted display
ps_results = ps_avg.to_frame().reset_index()
ps_results = ps_results.sort_values(['Gender', 'Department'])

print("\nPandas on Spark Results (Formatted):")
print("-" * 80)
for idx, row in ps_results.iterrows():
    print(f"{row['Gender']:8s} {row['Department']:10s}: ${row['Salary']:12,.2f}")

# Stop Spark session
spark.stop()