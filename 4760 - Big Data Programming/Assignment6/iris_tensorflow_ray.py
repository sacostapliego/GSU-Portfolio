"""
Iris Classification using TensorFlow with Ray Train
Feedforward Neural Network with 2 hidden layers (5 and 6 neurons)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
import os
import ray
from ray.train import ScalingConfig
from ray.train.tensorflow import TensorflowTrainer

# Data Loading and Preprocessing
def load_and_preprocess_data(filepath='./data/iris.csv'):
    """Load and preprocess the Iris dataset"""
    df = pd.read_csv(filepath)
    
    X = df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values.astype(np.float32)
    y = df['species'].values
    
    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    return X_train, X_test, y_train, y_test, label_encoder

def train_func(config):
    """Training function to be executed on each Ray worker"""
    X_train = config['X_train']
    y_train = config['y_train']
    X_test = config['X_test']
    y_test = config['y_test']
    
    # Simple model without MultiWorkerMirroredStrategy
    # Ray handles the distribution
    model = keras.Sequential([
        layers.Dense(5, activation='relu', input_shape=(4,)),
        layers.Dense(6, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train the model
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=16,
        verbose=0,
        validation_data=(X_test, y_test)
    )
    
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    # Report metrics to Ray
    ray.train.report({
        'test_loss': test_loss,
        'test_accuracy': test_accuracy
    })

def main():
    print("=" * 80)
    print("Iris Classification - TensorFlow with Ray")
    print("=" * 80)
    
    # Load and preprocess data
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data()
    
    # Display dataset information
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Classes: {list(label_encoder.classes_)}")
    print("-" * 80)
    
    # Initialize Ray
    ray.init(address='auto', ignore_reinit_error=True)
    
    # Configuration for training
    train_config = {
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test
    }
    
    # Scaling configuration
    scaling_config = ScalingConfig(
        num_workers=2,
        use_gpu=False,
        resources_per_worker={"CPU": 1}
    )
    
    # Initialize and run the Ray TensorflowTrainer
    trainer = TensorflowTrainer(
        train_loop_per_worker=train_func,
        train_loop_config=train_config,
        scaling_config=scaling_config
    )
    
    # Run the training
    result = trainer.fit()
    
    print("-" * 80)
    print("Training completed on distributed Ray workers")
    print("-" * 80)
    
    # Train model locally for predictions
    model = keras.Sequential([
        layers.Dense(5, activation='relu', input_shape=(4,)),
        layers.Dense(6, activation='relu'),
        layers.Dense(3, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=100, batch_size=16, verbose=0)
    
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    # Display results
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Generate predictions
    y_pred = model.predict(X_test, verbose=0)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # Save results to JSON
    results = {
        'framework': 'TensorFlow with Ray',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'predictions': y_pred_classes.tolist(),
        'true_labels': y_test.tolist(),
        'class_names': label_encoder.classes_.tolist()
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/iris_tensorflow_ray_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/iris_tensorflow_ray_results.json")
    print("=" * 80)
    
    # Shutdown Ray
    ray.shutdown()

if __name__ == "__main__":
    main()