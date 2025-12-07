import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import os

def load_results(filename):
    # Load results from JSON file
    with open(filename, 'r') as f:
        return json.load(f)

def plot_confusion_matrix(y_true, y_pred, class_names, title, ax):
    # Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names, ax=ax)
    ax.set_title(title)
    ax.set_ylabel('True Label')
    ax.set_xlabel('Predicted Label')

def plot_accuracy_comparison(results_list):
    # Plot accuracy comparison across frameworks
    frameworks = [r['framework'] for r in results_list]
    accuracies = [r['test_accuracy'] * 100 for r in results_list]
    
    # Create bar plot for accuracy comparison
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(frameworks, accuracies, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    
    # Add labels and title
    ax.set_ylabel('Test Accuracy (%)', fontsize=12)
    ax.set_title('Iris Classification Accuracy Comparison', fontsize=14, fontweight='bold')
    ax.set_ylim([0, 105])
    
    # Add accuracy values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=10)
    
    # Customize x-axis ticks
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    plt.savefig('results/accuracy_comparison.png', dpi=300, bbox_inches='tight')
    print("Accuracy comparison saved to results/accuracy_comparison.png")
    plt.close()

def main():
    print("=" * 80)
    print("Iris Classification Results Visualization")
    print("=" * 80)
    
    # Load results from all four implementations
    result_files = [
        'results/iris_tensorflow_results.json',
        'results/iris_tensorflow_ray_results.json',
        'results/iris_pytorch_results.json',
        'results/iris_pytorch_ray_results.json'
    ]
    
    # Load results from JSON files
    results_list = []
    # Iterate through result files and load data
    for filename in result_files:
        if os.path.exists(filename):
            results = load_results(filename)
            results_list.append(results)
            print(f"\n{results['framework']}:")
            print(f"  Test Accuracy: {results['test_accuracy']:.4f}")
            print(f"  Test Loss: {results['test_loss']:.4f}")
        else:
            print(f"Warning: {filename} not found")
    
    print("\n" + "-" * 80)
    
    # Check if all result files were found
    if len(results_list) < 4:
        print("Warning: Not all result files found. Generating visualizations for available results.")
    
    # Plot confusion matrices
    if results_list:
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        axes = axes.flatten()
        
        # Plot confusion matrix for each framework
        for idx, results in enumerate(results_list):
            plot_confusion_matrix(
                results['true_labels'],
                results['predictions'],
                results['class_names'],
                f"{results['framework']}\nAccuracy: {results['test_accuracy']:.4f}",
                axes[idx]
            )
        
        # Hide unused subplots if any
        for idx in range(len(results_list), 4):
            axes[idx].axis('off')
        
        # Finalize and save confusion matrices figure
        plt.tight_layout()
        plt.savefig('results/confusion_matrices.png', dpi=300, bbox_inches='tight')
        print("\nConfusion matrices saved to results/confusion_matrices.png")
        plt.close()
        
        # Plot accuracy comparison
        plot_accuracy_comparison(results_list)
    
    print("=" * 80)

if __name__ == "__main__":
    main()
