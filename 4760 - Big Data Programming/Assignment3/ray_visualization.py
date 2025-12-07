import matplotlib.pyplot as plt
import numpy as np

# --- Core Scaling Data (for 1,000,000 Steps) ---
SPARK_CORE_DATA = {
    '1 Core': 18.9173,
    '4 Cores': 10.3712
}

RAY_CORE_DATA = {
    '1 Core': 0.6988,
    '4 Cores': 0.8429
}

labels = ['1 Core', '4 Cores']
spark_times = [SPARK_CORE_DATA[l] for l in labels]
ray_times = [RAY_CORE_DATA[l] for l in labels]

# --- Step Scaling Data (Fixed Cores = 4) ---
SPARK_STEP_DATA = [
    {'steps': 1000, 'time': 16.9559},
    {'steps': 10000, 'time': 1.2583},
    {'steps': 100000, 'time': 0.9469},
    {'steps': 1000000, 'time': 2.9916}
]

RAY_STEP_DATA = [
    {'steps': 1000, 'time': 0.1870},
    {'steps': 10000, 'time': 0.0389},
    {'steps': 100000, 'time': 0.1088},
    {'steps': 1000000, 'time': 0.2427}
]

spark_step_times = [d['time'] for d in SPARK_STEP_DATA]
ray_step_times = [d['time'] for d in RAY_STEP_DATA]
step_labels = [str(d['steps']) for d in SPARK_STEP_DATA]

# --- Plot 1: Core Scaling Comparison (Spark vs Ray) ---
def plot_core_comparison():
    x = np.arange(len(labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x - width/2, spark_times, width, label='Spark')
    ax.bar(x + width/2, ray_times, width, label='Ray', color='orange')

    ax.set_ylabel('Execution Time (seconds)')
    ax.set_xlabel('Core Configuration (Fixed Steps: 1M)')
    ax.set_title('Ray vs. Spark: Parallel Speedup Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    fig.tight_layout()
    plt.show()

# --- Plot 2: Step Scaling Comparison (Spark vs Ray) ---
def plot_step_comparison():
    x = np.arange(len(step_labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, spark_step_times, width, label='Spark', color='blue')
    ax.bar(x + width/2, ray_step_times, width, label='Ray', color='orange')

    ax.set_ylabel('Execution Time (seconds)')
    ax.set_xlabel('Number of Steps (Fixed Cores: 4)')
    ax.set_title('Ray vs. Spark: Runtime Scalability')
    ax.set_xticks(x)
    ax.set_xticklabels(step_labels)
    ax.legend()

    fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    plot_core_comparison()
    plot_step_comparison()