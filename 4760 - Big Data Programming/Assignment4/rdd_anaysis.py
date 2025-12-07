"""
CSC 4760/6760 Big Data Programming Assignment 4, Question 1
"""

from pyspark.sql import SparkSession

# I placed the data files in this location 
WORKERS_TXT_PATH = "file:///opt/spark-data/assignment4/workers.txt"

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Q1 RDD Analysis") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.ansi.enabled", "false") \
    .getOrCreate()

print("METHOD 1: SPARK RDD ANALYSIS (Question 1)")
print("\nApproach: Using RDD transformations and aggregateByKey")
print("-" * 80)

# Load data using ABSOLUTE path
rdd = spark.sparkContext.textFile(WORKERS_TXT_PATH)

# Parse each line by splitting on tab character
parsed_rdd = rdd.map(lambda line: line.split("\t"))

# Transform to key-value pairs for aggregation
salary_rdd = parsed_rdd.map(lambda x: (
    (x[1], x[2]),                  # Key: (Department, Gender)
    float(x[3].replace(",", ""))   # Value: Salary as float
))

# Define aggregation functions
def seq_func(accumulator, value):
    """Combines accumulator with new value within partition"""
    return (accumulator[0] + value, accumulator[1] + 1)

def comb_func(acc1, acc2):
    """Merges two accumulators from different partitions"""
    return (acc1[0] + acc2[0], acc1[1] + acc2[1])

# Aggregate salaries by key
aggregated_rdd = salary_rdd.aggregateByKey(
    (0.0, 0),      # Initial accumulator: (sum, count)
    seq_func,      # Sequential operation
    comb_func      # Combine operation
)

# Calculate average
avg_salary_rdd = aggregated_rdd.mapValues(lambda x: x[0] / x[1])

# Collect and display results
print("\nRDD Results:")
print("-" * 80)

# Spark execution starts here (and logs are generated)
rdd_results = avg_salary_rdd.collect()

print("\n RDD")
for (dept, gender), avg_sal in sorted(rdd_results):
    print(f"{gender:8s} {dept:10s}: ${avg_sal:12,.2f}")

# Stop Spark session
spark.stop()