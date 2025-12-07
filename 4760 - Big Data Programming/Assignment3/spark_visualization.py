import matplotlib.pyplot as plt

CORE_DATA = {
    '1 Core': {'steps': 1000000, 'time': 18.9173},
    '4 Cores': {'steps': 1000000, 'time': 10.3712}
}

STEP_DATA = [
    {'steps': 1000, 'time': 16.9559},
    {'steps': 10000, 'time': 1.2583},
    {'steps': 100000, 'time': 0.9469},
    {'steps': 1000000, 'time': 2.9916}
]

# --- Core Comparison Bar Plot ---
core_labels = list(CORE_DATA.keys())
core_times = [data['time'] for data in CORE_DATA.values()]

plt.figure(figsize=(8, 6))
plt.bar(core_labels, core_times, color=['skyblue', 'lightcoral'])
plt.title('Running Time Comparison: 1 Core vs 4 Cores (Steps = 1M)')
plt.xlabel('Number of Cores')
plt.ylabel('Running Time (Seconds)')
plt.grid(axis='y', linestyle='--')
plt.show()

# --- Steps Comparison Bar Plot ---
step_labels = [str(data['steps']) for data in STEP_DATA]
step_times = [data['time'] for data in STEP_DATA]

plt.figure(figsize=(10, 6))
plt.bar(step_labels, step_times, color='lightgreen')
plt.title('Running Time vs. Number of Steps (4 Cores)')
plt.xlabel('Number of Steps')
plt.ylabel('Running Time (Seconds)')
plt.grid(axis='y', linestyle='--')
plt.show()

# --- Steps Comparison Line Plot (Log Scale) ---
step_values = [data['steps'] for data in STEP_DATA]
plt.figure(figsize=(10, 6))
plt.plot(step_values, step_times, marker='o', linestyle='-', color='purple')
plt.xscale('log')
plt.title('Running Time vs. Number of Steps (Log Scale)')
plt.xlabel('Number of Steps')
plt.ylabel('Running Time (Seconds)')
plt.grid(True, which="both", ls="--")
plt.show()