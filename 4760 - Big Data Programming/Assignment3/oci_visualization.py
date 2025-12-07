import matplotlib.pyplot as plt
import numpy as np

# --- Final Data ---
SPARK_CORE_DATA = {
    '1 Core': 1.8317,
    '4 Cores': 0.4352
}

RAY_CORE_DATA = {
    '1 Core': 0.5835,
    '6 Cores': 0.6603
}

SPARK_STEP_DATA = [
    {'Steps': 1000, 'Time': 0.2702},
    {'Steps': 10000, 'Time': 0.2327},
    {'Steps': 100000, 'Time': 0.2293},
    {'Steps': 1000000, 'Time': 0.4013}
]

RAY_STEP_DATA = [
    {'Steps': 1000, 'Time': 0.3087},
    {'Steps': 10000, 'Time': 0.1560},
    {'Steps': 100000, 'Time': 0.0139},
    {'Steps': 1000000, 'Time': 0.0578}
]


def plot_core_scaling(spark_data, ray_data):
    spark_times = [spark_data['1 Core'], spark_data['4 Cores']]
    ray_times = [ray_data['1 Core'], ray_data['6 Cores']]
    
    core_labels = ['1 Core', 'N Cores']

    x = np.arange(len(core_labels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x - width/2, spark_times, width, label='Spark (4 Cores Max)', color='skyblue')
    rects2 = ax.bar(x + width/2, ray_times, width, label='Ray (6 Cores Max)', color='lightcoral')

    ax.set_ylabel('Running Time (Seconds)')
    ax.set_xlabel('Core Configuration (Fixed Steps: 1,000,000)')
    ax.set_title('Core Scaling Comparison (Spark vs. Ray)')
    ax.set_xticks(x)
    ax.set_xticklabels(core_labels)
    ax.legend(loc='best')
    ax.grid(axis='y', linestyle='--')

    def autolabel(rects, times):
        for i, rect in enumerate(rects):
            height = rect.get_height()
            ax.annotate(f'{times[i]:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1, spark_times)
    autolabel(rects2, ray_times)

    fig.tight_layout()
    plt.show()


def plot_step_scaling(spark_data, ray_data):
    spark_steps = [d['Steps'] for d in spark_data]
    spark_times = [d['Time'] for d in spark_data]
    
    ray_steps = [d['Steps'] for d in ray_data]
    ray_times = [d['Time'] for d in ray_data]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(spark_steps, spark_times, marker='o', linestyle='-', color='purple', label='Spark (2 Cores)')
    ax.plot(ray_steps, ray_times, marker='o', linestyle='--', color='green', label='Ray (6 Cores)')

    ax.set_xscale('log')
    ax.set_xticks(spark_steps)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())

    ax.set_ylabel('Running Time (Seconds)')
    ax.set_xlabel('Number of Steps (Log Scale)')
    ax.set_title('Step Scaling Comparison (Spark vs. Ray)')
    ax.legend(loc='best')
    ax.grid(True, which="both", ls="--")
    
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_core_scaling(SPARK_CORE_DATA, RAY_CORE_DATA)
    plot_step_scaling(SPARK_STEP_DATA, RAY_STEP_DATA)