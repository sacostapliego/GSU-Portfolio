import ray
import time
import argparse

FIXED_STEPS = 1000000 
STEP_COUNTS = [1000, 10000, 100000, 1000000]

@ray.remote
def calculate_pi_chunk(start_index, chunk_size, total_steps_n):
    total_area = 0.0
    delta_x = 1.0 / total_steps_n
    
    for index in range(start_index, start_index + chunk_size):
        x = delta_x * (index - 0.5) 
        area = 4.0 / (1.0 + x * x) * delta_x
        total_area += area
        
    return total_area

def run_ray_experiment(total_steps, num_cores):
    start_time = time.time()
    
    num_tasks = num_cores
    chunk_size = total_steps // num_tasks
    remainder = total_steps % num_tasks
    
    futures = []
    current_index = 1
    for i in range(num_tasks):
        current_chunk_size = chunk_size + (1 if i < remainder else 0)
        
        future = calculate_pi_chunk.remote(current_index, current_chunk_size, total_steps)
        futures.append(future)
        
        current_index += current_chunk_size
    
    results = ray.get(futures)
    estimated_pi = sum(results)
    
    runtime = time.time() - start_time
    
    return runtime, estimated_pi

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-cores', type=int, default=0)
    args = parser.parse_args()

    # Initialize Ray
    ray.init(address="auto")

    available_cores = ray.available_resources().get("CPU", 0)
    
    if args.num_cores > 0:
        total_cores = args.num_cores
    else:
        total_cores = int(available_cores)

    if total_cores == 0:
        print("Error: No CPU resources detected by Ray.")
        return

    print(f"\n--- Ray Cluster Detected: {int(available_cores)} total cores ---")
    print(f"--- Running Experiments with: {total_cores} cores ---")

    final_results = []

    # 1. Core Scaling Experiment
    print("\n--- Core Scaling Job ---")
    
    runtime, pi = run_ray_experiment(FIXED_STEPS, total_cores)
    result_key = f"{total_cores}_cores" 
    
    print(f"Key: {result_key}, Steps: {FIXED_STEPS}, Time: {runtime:.4f}s, Pi: {pi}")
    final_results.append({'Key': result_key, 'Steps': FIXED_STEPS, 'Time': runtime, 'Pi': pi})

    # 2. Step Scaling Experiment
    if total_cores > 1:
        print(f"\n--- Step Scaling Experiment (Fixed Cores: {total_cores}) ---")
        
        for steps in STEP_COUNTS:
            runtime, pi = run_ray_experiment(steps, total_cores)
            print(f"Key: {steps}, Steps: {steps}, Time: {runtime:.4f}s, Pi: {pi}")
            final_results.append({'Key': str(steps), 'Steps': steps, 'Time': runtime, 'Pi': pi})

    # --- Final Output ---
    print("\n--- Final Results Summary (Ray) ---")
    for res in final_results:
        print(f"Key: {res['Key']}, Steps: {res['Steps']}, Time: {res['Time']:.4f}s, Pi: {res['Pi']}")
        
    ray.shutdown()

if __name__ == "__main__":
    main()