import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import json
import os

# Data Loading and Preprocessing
def load_and_preprocess_data(filepath='./data/iris.csv'):
    """Load and preprocess the Iris dataset"""
    df = pd.read_csv(filepath)
    
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    return X_train, X_test, y_train, y_test, label_encoder

# Model Definition
def build_model(input_dim=4, num_classes=3):
    """Build feedforward neural network"""
    model = keras.Sequential([
        layers.Dense(5, activation='relu', input_shape=(input_dim,)),
        layers.Dense(6, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    print("=" * 80)
    print("Iris Classification - TensorFlow")
    print("=" * 80)
    
    # Load and preprocess data
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data()
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Classes: {list(label_encoder.classes_)}")
    print("-" * 80)
    
    # Build and train the model
    model = build_model()
    
    print("Model Architecture:")
    model.summary()
    print("-" * 80)
    
    # Train the model
    history = model.fit(
        X_train, y_train,
        epochs=100,
        batch_size=16,
        validation_split=0.2,
        verbose=1
    )
    
    
    print("-" * 80)
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
        'framework': 'TensorFlow',
        'test_loss': float(test_loss),
        'test_accuracy': float(test_accuracy),
        'predictions': y_pred_classes.tolist(),
        'true_labels': y_test.tolist(),
        'class_names': label_encoder.classes_.tolist()
    }
    
    os.makedirs('results', exist_ok=True)
    with open('results/iris_tensorflow_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to results/iris_tensorflow_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
