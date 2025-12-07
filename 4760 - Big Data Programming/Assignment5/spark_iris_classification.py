from pyspark.sql import SparkSession
from pyspark.ml.classification import LinearSVC, MultilayerPerceptronClassifier, OneVsRest
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col
import sys

def create_spark_session():
    # Create and configure Spark session for distributed processing
    spark = SparkSession.builder \
        .appName("Iris Classification - SVM and MLP") \
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()
    
    print("=" * 80)
    print("Spark Session Created Successfully")
    print(f"Spark Version: {spark.version}")
    print(f"Master URL: {spark.sparkContext.master}")
    print("=" * 80)
    
    return spark

def load_and_prepare_data(spark, csv_path):
    # Load the Iris dataset from CSV and prepare it for ML processing
    print("\n" + "=" * 80)
    print("LOADING AND PREPARING DATA")
    print("=" * 80)
    
    # Load CSV file
    df = spark.read.csv(csv_path, header=True, inferSchema=True)
    
    print(f"\nTotal records loaded: {df.count()}")
    print("\nSchema:")
    df.printSchema()
    
    # Debugging
    print("\nFirst 5 rows:")
    df.show(5)
    
    print("\nClass distribution:")
    df.groupBy("species").count().show()
    
    # Convert string labels to numeric indices
    # setosa=0, versicolor=1, virginica=2
    indexer = StringIndexer(inputCol="species", outputCol="label")
    df = indexer.fit(df).transform(df)
    
    # Combine feature columns into a single vector column
    feature_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df = assembler.transform(df)
    
    # Select only the necessary columns
    df = df.select("features", "label", "species", 
                   "sepal_length", "sepal_width", "petal_length", "petal_width")
    
    print("\nPrepared data with features vector:")
    df.show(5, truncate=False)
    
    return df

def split_data(df, train_ratio=0.8, seed=42):
    # Split data into training and testing sets
    print("\n" + "=" * 80)
    print("SPLITTING DATA")
    print("=" * 80)
    
    train_df, test_df = df.randomSplit([train_ratio, 1-train_ratio], seed=seed)
    
    print(f"\nTraining set size: {train_df.count()}")
    print(f"Testing set size: {test_df.count()}")
    print(f"Split ratio: {train_ratio*100}% train, {(1-train_ratio)*100}% test")
    
    return train_df, test_df

def train_linear_svm(train_df, test_df):
    # Train and evaluate Linear Support Vector Machine classifier
    print("\n" + "=" * 80)
    print("LINEAR SUPPORT VECTOR MACHINE (SVM)")
    print("=" * 80)
    
    print("\nTraining Linear SVM model...")
    
    # Import OneVsRest for multi-class classification
    from pyspark.ml.classification import OneVsRest
    
    # Create Linear SVM as base classifier
    # LinearSVC only supports binary classification, so we wrap it with OneVsRest
    svm = LinearSVC(featuresCol="features", labelCol="label", 
                    maxIter=100, regParam=0.01)
    
    # Wrap with OneVsRest for multi-class support
    ovr = OneVsRest(classifier=svm, featuresCol="features", labelCol="label")
    
    # Train the model
    svm_model = ovr.fit(train_df)
    
    print("Model training completed!")
    
    # Make predictions on test data
    print("\nMaking predictions on test data...")
    predictions = svm_model.transform(test_df)
    
    # Show sample predictions
    print("\nSample predictions (first 10):")
    predictions.select("features", "label", "prediction", "species").show(10, truncate=False)
    
    # Evaluate the model
    evaluate_model(predictions, "Linear SVM")
    
    return predictions, svm_model

def train_mlp(train_df, test_df):
    # Train and evaluate Multilayer Perceptron (Feedforward Neural Network) classifier
    print("\n" + "=" * 80)
    print("MULTILAYER PERCEPTRON CLASSIFIER (FEEDFORWARD NEURAL NETWORK)")
    print("=" * 80)
    
    print("\nTraining Multilayer Perceptron model...")
    
    # Define network architecture
    # Input layer: 4 nodes (4 features)
    # Hidden layer 1: 8 nodes
    # Hidden layer 2: 8 nodes
    # Output layer: 3 nodes (3 classes)
    layers = [4, 8, 8, 3]
    
    print(f"Network architecture: {layers}")
    
    # Create and configure MLP
    # maxIter: maximum number of iterations
    # blockSize: block size for stacking input data
    # seed: random seed for reproducibility
    mlp = MultilayerPerceptronClassifier(featuresCol="features", labelCol="label",
                                         layers=layers, maxIter=100, 
                                         blockSize=128, seed=42)
    
    # Train the model
    mlp_model = mlp.fit(train_df)
    
    print("\nModel training completed!")
    
    # Make predictions on test data
    print("\nMaking predictions on test data...")
    predictions = mlp_model.transform(test_df)
    
    # Show sample predictions
    print("\nSample predictions (first 10):")
    predictions.select("features", "label", "prediction", "species").show(10, truncate=False)
    
    # Evaluate the model
    evaluate_model(predictions, "Multilayer Perceptron")
    
    return predictions, mlp_model

def evaluate_model(predictions, model_name):
    # Evaluate classification model performance
    print(f"\n{'-' * 80}")
    print(f"EVALUATION RESULTS - {model_name}")
    print('-' * 80)
    
    # Create evaluators for different metrics
    evaluator_accuracy = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="accuracy")
    
    evaluator_precision = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="weightedPrecision")
    
    evaluator_recall = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="weightedRecall")
    
    evaluator_f1 = MulticlassClassificationEvaluator(
        labelCol="label", predictionCol="prediction", metricName="f1")
    
    # Calculate metrics
    accuracy = evaluator_accuracy.evaluate(predictions)
    precision = evaluator_precision.evaluate(predictions)
    recall = evaluator_recall.evaluate(predictions)
    f1 = evaluator_f1.evaluate(predictions)
    
    # Print results
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    
    # Show confusion matrix data
    print("\nPrediction distribution:")
    predictions.groupBy("label", "prediction").count().orderBy("label", "prediction").show()

def save_results(predictions, output_path, model_name):
    # Save prediction results to CSV file for visualization
    print(f"\nSaving {model_name} results to {output_path}...")
    
    # Select relevant columns
    results = predictions.select("sepal_length", "sepal_width", "petal_length", 
                                  "petal_width", "label", "prediction", "species")
    
    # Convert to Pandas and save as single CSV file
    # This is more reliable than Spark's CSV writer for small datasets
    pandas_df = results.toPandas()
    
    # Create output directory if it doesn't exist
    import os
    os.makedirs(output_path, exist_ok=True)
    
    # Save as a single CSV file with a fixed name
    csv_file = os.path.join(output_path, "results.csv")
    pandas_df.to_csv(csv_file, index=False)
    
    print(f"Results saved successfully to {csv_file}!")
    print(f"Saved {len(pandas_df)} predictions")


def main():
    """
    Main execution function
    """
    # Path to iris.csv
    csv_path = "/home/sacostapliego1/data/iris.csv"
    
    try:
        # Initialize Spark
        spark = create_spark_session()
        
        # Load and prepare data
        df = load_and_prepare_data(spark, csv_path)
        
        # Split data into train and test sets
        train_df, test_df = split_data(df, train_ratio=0.8, seed=42)
        
        # Train and evaluate Linear SVM
        svm_predictions, svm_model = train_linear_svm(train_df, test_df)
        
        # Save SVM results
        save_results(svm_predictions, "/home/sacostapliego1/data/svm_results", "Linear SVM")
        
        print("\n" + "=" * 80)
        
        # Train and evaluate Multilayer Perceptron
        mlp_predictions, mlp_model = train_mlp(train_df, test_df)
        
        # Save MLP results
        save_results(mlp_predictions, "/home/sacostapliego1/data/mlp_results", "MLP")
        
        print("\n" + "=" * 80)
        print("ALL CLASSIFICATIONS COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        # Stop Spark session
        spark.stop()
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()