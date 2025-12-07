import matplotlib.pyplot as plt
import numpy as np

def read_results(filename):
    """Read clustering results from file."""
    x_coords = []
    y_coords = []
    labels = []
    
    with open(filename, 'r') as f:
        for line in f:
            # Skip comments and empty lines
            if line.startswith('#') or line.strip() == '':
                continue
            
            parts = line.strip().split()
            if len(parts) == 3:
                x_coords.append(float(parts[0]))
                y_coords.append(float(parts[1]))
                labels.append(int(parts[2]))
    
    return np.array(x_coords), np.array(y_coords), np.array(labels)

def read_centers(filename):
    """Read cluster centers from file."""
    centers = []
    
    with open(filename, 'r') as f:
        for line in f:
            # Skip comments
            if line.startswith('#'):
                continue
            
            parts = line.strip().split()
            if len(parts) == 2:
                centers.append([float(parts[0]), float(parts[1])])
    
    return np.array(centers)

def plot_clusters(x, y, labels, centers, title, save_path):
    """
    Create visualization of clustering results.
    
    Cluster 1 (label 0): Red crosses
    Cluster 2 (label 1): Blue circles
    Cluster 1 center: Red triangle
    Cluster 2 center: Blue square
    """
    plt.figure(figsize=(10, 8))
    
    # Separate data points by cluster
    cluster_0_mask = labels == 0
    cluster_1_mask = labels == 1
    
    # Plot Cluster 1 (label 0) - Red crosses
    plt.plot(x[cluster_0_mask], y[cluster_0_mask], 
             'rx',  # red crosses
             markersize=8, 
             markeredgewidth=2,
             label='Cluster 1',
             alpha=0.7)
    
    # Plot Cluster 2 (label 1) - Blue circles
    plt.plot(x[cluster_1_mask], y[cluster_1_mask], 
             'bo',  # blue circles
             markersize=8,
             markerfacecolor='none',
             markeredgewidth=2,
             label='Cluster 2',
             alpha=0.7)
    
    # Plot cluster centers
    # Cluster 1 center (corresponds to label 0) - Red triangle
    plt.plot(centers[0, 0], centers[0, 1], 
             '^r',  # red triangle
             markersize=15,
             markeredgewidth=2,
             markeredgecolor='darkred',
             label='Cluster 1 Center')
    
    # Cluster 2 center (corresponds to label 1) - Blue square
    plt.plot(centers[1, 0], centers[1, 1], 
             'bs',  # blue square
             markersize=15,
             markeredgewidth=2,
             markeredgecolor='darkblue',
             label='Cluster 2 Center')
    
    # Add labels and title
    plt.xlabel('X Coordinate (Feature 1)', fontsize=12)
    plt.ylabel('Y Coordinate (Feature 2)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # Add cluster center coordinates as text
    plt.text(centers[0, 0], centers[0, 1] - 0.15, 
             f'({centers[0, 0]:.3f}, {centers[0, 1]:.3f})',
             ha='center', fontsize=9, 
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.text(centers[1, 0], centers[1, 1] - 0.15, 
             f'({centers[1, 0]:.3f}, {centers[1, 1]:.3f})',
             ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to: {save_path}")
    
    # Show plot
    plt.show()

def main():
    """Main function to create visualizations."""
    print("=" * 80)
    print("K-MEANS CLUSTERING VISUALIZATION")
    print("=" * 80)
    
    # File paths
    results_file = "kmeans_results.txt"
    centers_file = "cluster_centers.txt"
    
    try:
        # Read data
        print(f"\nReading results from: {results_file}")
        x, y, labels = read_results(results_file)
        print(f"  - Loaded {len(x)} data points")
        
        print(f"\nReading cluster centers from: {centers_file}")
        centers = read_centers(centers_file)
        print(f"  - Loaded {len(centers)} cluster centers")
        
        # Display cluster centers
        print("\nCluster Centers:")
        for i, center in enumerate(centers):
            print(f"  Cluster {i+1}: ({center[0]:.4f}, {center[1]:.4f})")
        
        # Display cluster distribution
        unique, counts = np.unique(labels, return_counts=True)
        print("\nCluster Distribution:")
        for label, count in zip(unique, counts):
            print(f"  Cluster {label+1}: {count} points ({count/len(labels)*100:.1f}%)")
        
        # Create visualization
        print("\n" + "-" * 80)
        print("Creating visualization...")
        print("-" * 80)
        
        # Determine which cluster this is from
        import os
        hostname = os.environ.get('HOSTNAME', 'unknown')
        
        # Create a title
        title = "K-Means Clustering Results (K=2)"
        save_path = "kmeans_clustering_results.png"
        
        plot_clusters(x, y, labels, centers, title, save_path)
        
        print("\n" + "=" * 80)
        print("VISUALIZATION COMPLETED!")
        print("=" * 80)
        print()
        
    except FileNotFoundError as e:
        print(f"\nError: Could not find file - {e}")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()