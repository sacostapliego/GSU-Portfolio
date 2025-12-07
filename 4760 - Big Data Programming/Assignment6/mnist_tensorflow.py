import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
import os

def build_cnn_model():
    # Build CNN model with specified architecture
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
    
    return model

def load_and_preprocess_data():
    # Load and preprocess MNIST dataset
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    
    # Normalize and reshape data
    x_train = x_train.astype('float32') / 255.0
    x_test = x_test.astype('float32') / 255.0
    
    # Add channel dimension for CNN input
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    
    return x_train, y_train, x_test, y_test

def main():
    print("=" * 80)
    print("MNIST Classification - TensorFlow CNN")
    print("=" * 80)
    
    # Load and preprocess data
    x_train, y_train, x_test, y_test = load_and_preprocess_data()
    
    # Display dataset information
    print(f"Training samples: {x_train.shape[0]}")
    print(f"Testing samples: {x_test.shape[0]}")
    print(f"Image shape: {x_train.shape[1:]}")
    print("-" * 80)
    
    #   Build and train the model
    model = build_cnn_model()
    
    # Display model architecture
    print("Model Architecture:")
    model.summary()
    print("-" * 80)
    
    # Train the model
    history = model.fit(
        x_train, y_train,
        batch_size=128,
        epochs=10,
        validation_split=0.1,
        verbose=1
    )
    
    print("-" * 80)
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    
    #  Display results
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Save results to JSON
    results = {
        'framework': 'TensorFlow',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'train_samples': int(x_train.shape[0]),
        'test_samples': int(x_test.shape[0])
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/mnist_tensorflow_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/mnist_tensorflow_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
