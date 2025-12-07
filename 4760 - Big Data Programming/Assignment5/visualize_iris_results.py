import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

def load_results(results_path):
    # Load classification results from CSV files
    
    # First, try to load the fixed filename (results.csv)
    fixed_csv = os.path.join(results_path, "results.csv")
    if os.path.exists(fixed_csv):
        print(f"  Loading from {fixed_csv}")
        return pd.read_csv(fixed_csv)
    
    # Otherwise, try to find Spark's part-*.csv files
    csv_files = glob.glob(os.path.join(results_path, "part-*.csv"))
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {results_path}. "
                              f"Expected either 'results.csv' or 'part-*.csv' files.")
    
    # Read the CSV file
    print(f"  Loading from {csv_files[0]}")
    df = pd.read_csv(csv_files[0])
    
    return df

def create_classification_plot(df, model_name, output_filename):
    # Create visualization of classification results

    # Map numeric labels to species names
    label_map = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle(f'{model_name} Classification Results - Iris Dataset', 
                 fontsize=16, fontweight='bold')
    
    # Define colors for each species
    colors = {0: 'red', 1: 'green', 2: 'blue'}
    markers = {0: 'o', 1: 's', 2: '^'}
    
    # Feature pairs to visualize
    feature_pairs = [
        ('sepal_length', 'sepal_width', 'Sepal Length vs Sepal Width'),
        ('petal_length', 'petal_width', 'Petal Length vs Petal Width'),
        ('sepal_length', 'petal_length', 'Sepal Length vs Petal Length'),
        ('sepal_width', 'petal_width', 'Sepal Width vs Petal Width')
    ]
    
    for idx, (feature_x, feature_y, title) in enumerate(feature_pairs):
        ax = axes[idx // 2, idx % 2]
        
        # Plot each class
        for class_label in [0, 1, 2]:
            # Correct predictions
            correct = df[(df['label'] == class_label) & (df['prediction'] == class_label)]
            ax.scatter(correct[feature_x], correct[feature_y], 
                      c=colors[class_label], marker=markers[class_label],
                      s=100, alpha=0.7, edgecolors='black', linewidth=1.5,
                      label=f'{label_map[class_label]} (correct)')
            
            # Incorrect predictions
            incorrect = df[(df['label'] == class_label) & (df['prediction'] != class_label)]
            if len(incorrect) > 0:
                ax.scatter(incorrect[feature_x], incorrect[feature_y],
                          c=colors[class_label], marker='x',
                          s=200, alpha=1.0, linewidth=3,
                          label=f'{label_map[class_label]} (incorrect)')
        
        ax.set_xlabel(feature_x.replace('_', ' ').title(), fontsize=11)
        ax.set_ylabel(feature_y.replace('_', ' ').title(), fontsize=11)
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.legend(loc='best', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {output_filename}")
    plt.show()

def create_confusion_matrix_plot(df, model_name, output_filename):
    # Create confusion matrix visualization

    from sklearn.metrics import confusion_matrix, classification_report
    
    # Create confusion matrix
    cm = confusion_matrix(df['label'], df['prediction'])
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot confusion matrix
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax)
    
    # Set labels
    classes = ['Setosa', 'Versicolor', 'Virginica']
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           xticklabels=classes, yticklabels=classes,
           title=f'Confusion Matrix - {model_name}',
           ylabel='True Label',
           xlabel='Predicted Label')
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add text annotations
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], 'd'),
                   ha="center", va="center",
                   color="white" if cm[i, j] > thresh else "black",
                   fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Confusion matrix saved to {output_filename}")
    plt.show()
    
    # Print classification report
    print(f"\n{model_name} Classification Report:")
    print("=" * 60)
    target_names = ['Setosa', 'Versicolor', 'Virginica']
    print(classification_report(df['label'], df['prediction'], target_names=target_names))

def create_accuracy_summary(svm_df, mlp_df, output_filename):
    # Create a summary comparison plot of both models
  
    # Calculate accuracies
    svm_accuracy = (svm_df['label'] == svm_df['prediction']).sum() / len(svm_df) * 100
    mlp_accuracy = (mlp_df['label'] == mlp_df['prediction']).sum() / len(mlp_df) * 100
    
    # Calculate per-class accuracies
    classes = ['Setosa', 'Versicolor', 'Virginica']
    svm_class_acc = []
    mlp_class_acc = []
    
    for class_label in [0, 1, 2]:
        svm_class = svm_df[svm_df['label'] == class_label]
        mlp_class = mlp_df[mlp_df['label'] == class_label]
        
        svm_class_acc.append((svm_class['label'] == svm_class['prediction']).sum() / len(svm_class) * 100)
        mlp_class_acc.append((mlp_class['label'] == mlp_class['prediction']).sum() / len(mlp_class) * 100)
    
    # Create figure
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Model Comparison - SVM vs MLP', fontsize=16, fontweight='bold')
    
    # Overall accuracy comparison
    ax1 = axes[0]
    models = ['Linear SVM', 'MLP']
    accuracies = [svm_accuracy, mlp_accuracy]
    colors_bar = ['#3498db', '#e74c3c']

    # Create bars for each model
    bars = ax1.bar(models, accuracies, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
    ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Overall Accuracy Comparison', fontsize=13, fontweight='bold')
    ax1.set_ylim([0, 105])
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, acc in zip(bars, accuracies):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{acc:.2f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Per-class accuracy comparison
    ax2 = axes[1]
    x = np.arange(len(classes))
    width = 0.35

    # Create bars for each model
    bars1 = ax2.bar(x - width/2, svm_class_acc, width, label='Linear SVM', 
                    color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
    bars2 = ax2.bar(x + width/2, mlp_class_acc, width, label='MLP',
                    color='#e74c3c', alpha=0.7, edgecolor='black', linewidth=1.5)

    # Add labels and title
    ax2.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Per-Class Accuracy Comparison', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(classes)
    ax2.legend(fontsize=11)
    ax2.set_ylim([0, 105])
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    print(f"Summary comparison saved to {output_filename}")
    plt.show()
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"\nLinear SVM Overall Accuracy: {svm_accuracy:.2f}%")
    print(f"MLP Overall Accuracy: {mlp_accuracy:.2f}%")
    print(f"\nAccuracy Difference: {abs(svm_accuracy - mlp_accuracy):.2f}%")
    print(f"Better Model: {'Linear SVM' if svm_accuracy > mlp_accuracy else 'MLP'}")

def main():
    """
    Main execution function
    """
    print("=" * 80)
    print("IRIS DATASET CLASSIFICATION RESULTS VISUALIZATION")
    print("=" * 80)
    
    try:
        # Paths to results
        svm_results_path = "/home/sacostapliego1/data/svm_results"
        mlp_results_path = "/home/sacostapliego1/data/mlp_results"
        
        # Output directory for plots
        output_dir = "/home/sacostapliego1/data/plots"
        os.makedirs(output_dir, exist_ok=True)
        
        print("\nLoading Linear SVM results...")
        svm_df = load_results(svm_results_path)
        print(f"Loaded {len(svm_df)} predictions from SVM model")
        
        print("\nLoading MLP results...")
        mlp_df = load_results(mlp_results_path)
        print(f"Loaded {len(mlp_df)} predictions from MLP model")
        
        print("\n" + "=" * 80)
        print("CREATING VISUALIZATIONS")
        print("=" * 80)
        
        # Create SVM visualizations
        print("\n1. Creating Linear SVM scatter plots...")
        create_classification_plot(svm_df, "Linear SVM", 
                                   os.path.join(output_dir, "svm_classification.png"))
        
        print("\n2. Creating Linear SVM confusion matrix...")
        create_confusion_matrix_plot(svm_df, "Linear SVM",
                                     os.path.join(output_dir, "svm_confusion_matrix.png"))
        
        # Create MLP visualizations
        print("\n3. Creating MLP scatter plots...")
        create_classification_plot(mlp_df, "Multilayer Perceptron",
                                   os.path.join(output_dir, "mlp_classification.png"))
        
        print("\n4. Creating MLP confusion matrix...")
        create_confusion_matrix_plot(mlp_df, "Multilayer Perceptron",
                                     os.path.join(output_dir, "mlp_confusion_matrix.png"))
        
        # Create comparison plot
        print("\n5. Creating model comparison plot...")
        create_accuracy_summary(svm_df, mlp_df,
                               os.path.join(output_dir, "model_comparison.png"))
        
        print("\n" + "=" * 80)
        print("VISUALIZATION COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\nAll plots have been saved to: {output_dir}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()