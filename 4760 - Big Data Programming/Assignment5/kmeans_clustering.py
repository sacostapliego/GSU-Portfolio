from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
import sys

def main():
    # Initialize Spark Session
    print("Initializing Spark Session...")
    spark = SparkSession.builder \
        .appName("KMeans Clustering - Assignment 5") \
        .getOrCreate()
    
    # Set log level to reduce verbose output
    spark.sparkContext.setLogLevel("WARN")
    
    print("=" * 80)
    print("K-MEANS CLUSTERING - ASSIGNMENT 5 PROBLEM 2")
    print("=" * 80)
    
    # Path to the input file
    input_path = "/home/sacostapliego1/data/kmeans_input_libsvm.txt"
    
    # Try to read the dataset
    try:
        print(f"\nReading dataset from: {input_path}")
        dataset = spark.read.format("libsvm").load(input_path)
        
        print(f"Dataset loaded successfully!")
        print(f"Total number of data points: {dataset.count()}")
        print("\nDataset schema:")
        dataset.printSchema()
        
        print("\nFirst 5 rows of the dataset:")
        dataset.show(5, truncate=False)
        
    except Exception as e:
        print(f"Error reading dataset: {e}")
        spark.stop()
        sys.exit(1)
    
    # Configure K-Means algorithm
    print("\n" + "=" * 80)
    print("CONFIGURING K-MEANS ALGORITHM")
    print("=" * 80)
    
    # Set K=2 since we know there are two clusters
    k = 2
    print(f"\nNumber of clusters (K): {k}")
    
    # Create K-Means model
    kmeans = KMeans() \
        .setK(k) \
        .setSeed(42) \
        .setMaxIter(20) \
        .setFeaturesCol("features") \
        .setPredictionCol("prediction")
    
    # Train the model
    print("\nTraining K-Means model...")
    model = kmeans.fit(dataset)
    print("Model training completed!")
    
    # Make predictions (assign cluster labels)
    print("\nAssigning cluster labels to data points...")
    predictions = model.transform(dataset)
    
    # Evaluate clustering by computing silhouette score
    evaluator = ClusteringEvaluator()
    silhouette = evaluator.evaluate(predictions)
    
    print("\n" + "=" * 80)
    print("CLUSTERING RESULTS")
    print("=" * 80)
    
    print(f"\nSilhouette Score: {silhouette:.4f}")
    print("(Higher is better, range: -1 to 1)")
    
    # Get cluster centers
    centers = model.clusterCenters()
    print("\n" + "-" * 80)
    print("CLUSTER CENTERS:")
    print("-" * 80)
    for i, center in enumerate(centers):
        print(f"Cluster {i+1} Center: [{center[0]:.4f}, {center[1]:.4f}]")
    print("-" * 80)
    
    # Show sample predictions
    print("\nSample of clustered data (first 20 rows):")
    predictions.select("label", "features", "prediction").show(20, truncate=False)
    
    # Count data points in each cluster
    print("\nCluster distribution:")
    cluster_counts = predictions.groupBy("prediction").count().orderBy("prediction")
    cluster_counts.show()
    
    # Prepare output data for visualization
    print("\n" + "=" * 80)
    print("PREPARING OUTPUT FOR VISUALIZATION")
    print("=" * 80)
    
    # Extract features and predictions for easier visualization
    # Convert to Pandas DataFrame for easier file writing
    print("\nExtracting features and predictions...")
    
    # Collect all predictions with features
    results = predictions.select("features", "prediction").collect()
    
    # Output path for results
    output_path = "kmeans_results.txt"
    
    print(f"\nWriting results to: {output_path}")
    with open(output_path, 'w') as f:
        # Write header
        f.write("# K-Means Clustering Results\n")
        f.write("# Format: x_coordinate y_coordinate cluster_label\n")
        f.write(f"# Total points: {len(results)}\n")
        f.write(f"# Number of clusters: {k}\n")
        f.write("\n")
        
        # Write data points with cluster labels
        for row in results:
            features = row['features']
            cluster = row['prediction']
            f.write(f"{features[0]:.5f} {features[1]:.5f} {cluster}\n")
        
        # Write cluster centers at the end
        f.write("\n# Cluster Centers:\n")
        for i, center in enumerate(centers):
            f.write(f"# Cluster {i+1}: {center[0]:.5f} {center[1]:.5f}\n")
    
    print("Results written successfully!")
    
    # Also save cluster centers separately for easy access
    centers_path = "cluster_centers.txt"
    print(f"\nWriting cluster centers to: {centers_path}")
    with open(centers_path, 'w') as f:
        f.write("# Cluster Centers (x, y)\n")
        for i, center in enumerate(centers):
            f.write(f"{center[0]:.5f} {center[1]:.5f}\n")
    
    print("\n" + "=" * 80)
    print("K-MEANS CLUSTERING COMPLETED SUCCESSFULLY!")
    print("-" * 80)
    print("\n")
    
    # Stop Spark session
    spark.stop()
    print("Spark session stopped.")

if __name__ == "__main__":
    main()