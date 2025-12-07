import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
import os
import ray
from ray.train import ScalingConfig
from ray.train.tensorflow import TensorflowTrainer

def load_and_preprocess_data():
    # Load and preprocess MNIST dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normalize and reshape data
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    return x_train, y_train, x_test, y_test

def train_func(config):
    # Training function to be executed on each Ray worker
    import ray.train
    
    # Extract data from config
    x_train = config['x_train']
    y_train = config['y_train']
    x_test = config['x_test']
    y_test = config['y_test']

    # Get worker info
    world_rank = ray.train.get_context().get_world_rank()
    world_size = ray.train.get_context().get_world_size()
    
    # Split data among workers
    split_size = len(x_train) // world_size
    start_idx = world_rank * split_size
    end_idx = start_idx + split_size if world_rank < world_size - 1 else len(x_train)
    
    # Create data splits for this worker
    x_train_split = x_train[start_idx:end_idx]
    y_train_split = y_train[start_idx:end_idx]
    
    # Print training info for this worker
    print(f"Worker {world_rank}/{world_size}: Training on {len(x_train_split)} samples")
    
    # Build the model
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        
        layers.Conv2D(16, kernel_size=(3, 3), activation='relu', strides=1, padding='valid'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu', strides=1, padding='valid'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Train the model
    history = model.fit(
        x_train_split, y_train_split,
        batch_size=128,
        epochs=10,
        validation_split=0.1,
        verbose=1 if world_rank == 0 else 0
    )
    
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    # Report metrics to Ray
    ray.train.report({
        'test_loss': test_loss,
        'test_accuracy': test_accuracy
    })

def main():
    print("=" * 80)
    print("MNIST Classification - TensorFlow with Ray")
    print("=" * 80)
    
    # Load and preprocess data
    x_train, y_train, x_test, y_test = load_and_preprocess_data()
    
    # Display dataset information
    print(f"Training samples: {x_train.shape[0]}")
    print(f"Testing samples: {x_test.shape[0]}")
    print(f"Image shape: {x_train.shape[1:]}")
    print("-" * 80)
    
    # Initialize Ray
    ray.init(address='auto', ignore_reinit_error=True)
    
    # Configuration for training
    train_config = {
        'x_train': x_train,
        'y_train': y_train,
        'x_test': x_test,
        'y_test': y_test
    }
    
    # Scaling configuration for Ray
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
    print("Distributed training completed. Retraining locally for final evaluation...")
    print("-" * 80)

    # Train model locally for final evaluation
    model = keras.Sequential([
        layers.Input(shape=(28, 28, 1)),
        layers.Conv2D(16, kernel_size=(3, 3), activation='relu', strides=1, padding='valid'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu', strides=1, padding='valid'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    # Compile the model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(x_train, y_train, batch_size=128, epochs=10, validation_split=0.1, verbose=1)
    
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    #   Display results
    print("-" * 80)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Save results to JSON
    results = {
        'framework': 'TensorFlow with Ray',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'train_samples': int(x_train.shape[0]),
        'test_samples': int(x_test.shape[0])
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/mnist_tensorflow_ray_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/mnist_tensorflow_ray_results.json")
    print("=" * 80)
    
    ray.shutdown()

if __name__ == "__main__":
    main()