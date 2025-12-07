import time
import sys
from pyspark.sql import SparkSession

FIXED_STEPS = 1000000 
STEP_COUNTS = [1000, 10000, 100000, 1000000]

def pi_estimate_riemann(index, total_steps_n):
    delta_x = 1.0 / total_steps_n 
    x = delta_x * (index - 0.5) 
    area = 4.0 / (1.0 + x * x) * delta_x
    return area

def run_spark_experiment(spark, total_steps):
    start_time = time.time()
    
    rdd = spark.sparkContext.range(1, total_steps + 1)
    
    estimated_pi = rdd.map(lambda index: pi_estimate_riemann(index, total_steps)).sum()
    
    runtime = time.time() - start_time
    
    return runtime, estimated_pi

def main():
    spark = SparkSession.builder.appName("SparkPiEstimation").getOrCreate()

    num_cores = spark.sparkContext.getConf().get("spark.executor.cores")
    num_executors = spark.sparkContext.getConf().get("spark.executor.instances")

    if num_cores and num_executors:
        total_cores = int(num_cores) * int(num_executors)
        print(f"Detected Configuration: {num_executors} executors * {num_cores} cores/executor = {total_cores} total cores")
    else:
        total_cores = spark.sparkContext.defaultParallelism
        print(f"Using default parallelism: {total_cores} cores")

    final_results = []

    # 1. Core Scaling Experiment
    print("\n--- Core Scaling Job ---")
    runtime, pi = run_spark_experiment(spark, FIXED_STEPS)
    result_key = f"{total_cores}_cores" 
    print(f"Key: {result_key}, Steps: {FIXED_STEPS}, Time: {runtime:.4f}s, Pi: {pi}")
    final_results.append({'Key': result_key, 'Steps': FIXED_STEPS, 'Time': runtime, 'Pi': pi})

    # 2. Step Scaling Experiment
    print(f"\n--- Step Scaling Experiment (Fixed Cores: {total_cores}) ---")
    for steps in STEP_COUNTS:
        runtime, pi = run_spark_experiment(spark, steps)
        print(f"Key: {steps}, Steps: {steps}, Time: {runtime:.4f}s, Pi: {pi}")
        final_results.append({'Key': str(steps), 'Steps': steps, 'Time': runtime, 'Pi': pi})

    # --- Final Output ---
    print("\n--- Final Results Summary (Spark) ---")
    for res in final_results:
        print(f"Key: {res['Key']}, Steps: {res['Steps']}, Time: {res['Time']:.4f}s, Pi: {res['Pi']}")
        
    spark.stop()

if __name__ == "__main__":
    main()