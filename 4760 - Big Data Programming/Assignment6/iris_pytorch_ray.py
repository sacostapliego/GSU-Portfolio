import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import json
import os
import ray
from ray.train import ScalingConfig
from ray.train.torch import TorchTrainer
import ray.train.torch

class IrisDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.LongTensor(y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class IrisNet(nn.Module):
    # Feedforward Neural Network for Iris classification
    def __init__(self, input_dim=4, hidden1=5, hidden2=6, num_classes=3):
        super(IrisNet, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden1)
        self.fc2 = nn.Linear(hidden1, hidden2)
        self.fc3 = nn.Linear(hidden2, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)
        return x

def load_and_preprocess_data(filepath='./data/iris.csv'):
    # Load and preprocess the Iris dataset
    df = pd.read_csv(filepath)
    
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    
    return X_train, X_test, y_train, y_test, label_encoder

def train_func(config):
    # Training function to be executed on each Ray worker
    X_train = config['X_train']
    y_train = config['y_train']
    X_test = config['X_test']
    y_test = config['y_test']
    
    # Create datasets and dataloaders
    train_dataset = IrisDataset(X_train, y_train)
    test_dataset = IrisDataset(X_test, y_test)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    
    # Prepare data loaders for Ray Train
    train_loader = ray.train.torch.prepare_data_loader(train_loader)
    test_loader = ray.train.torch.prepare_data_loader(test_loader)
    
    # Initialize model, loss function, and optimizer
    model = IrisNet()
    model = ray.train.torch.prepare_model(model)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    epochs = 100
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        if (epoch + 1) % 20 == 0:
            avg_loss = running_loss / len(train_loader)
            print(f"Epoch [{epoch+1}/{epochs}], Loss: {avg_loss:.4f}")
    
    model.eval()
    correct = 0
    total = 0
    test_loss = 0.0
    
    # Evaluation loop
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            test_loss += loss.item()
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    accuracy = correct / total
    avg_test_loss = test_loss / len(test_loader)
    
    # Report metrics to Ray Train
    ray.train.report({
        'test_loss': avg_test_loss,
        'test_accuracy': accuracy
    })

def main():
    print("=" * 80)
    print("Iris Classification - PyTorch with Ray")
    print("=" * 80)
    
    X_train, X_test, y_train, y_test, label_encoder = load_and_preprocess_data()
    
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")
    print(f"Classes: {list(label_encoder.classes_)}")
    print("-" * 80)
    
    ray.init(address='auto', ignore_reinit_error=True)
    
    # Configuration for training
    train_config = {
        'X_train': X_train,
        'y_train': y_train,
        'X_test': X_test,
        'y_test': y_test
    }
    
    # Scaling configuration for Ray Trainer
    scaling_config = ScalingConfig(
        num_workers=2,
        use_gpu=False,
        resources_per_worker={"CPU": 1}
    )
    
    # Initialize and run the Ray TorchTrainer
    trainer = TorchTrainer(
        train_loop_per_worker=train_func,
        train_loop_config=train_config,
        scaling_config=scaling_config
    )
    
    result = trainer.fit()
    
    print("-" * 80)
    
    # We need to re-evaluate the model to get final metrics
    test_dataset = IrisDataset(X_test, y_test)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
    
    # Retrain model locally to get final predictions
    model = IrisNet()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    train_dataset = IrisDataset(X_train, y_train)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    
    # Train the model
    for epoch in range(100):
        model.train()
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
    
    # Evaluate the model
    model.eval()
    predictions = []
    true_labels = []
    test_loss = 0.0
    correct = 0
    total = 0
    
    # Final evaluation on test set
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            test_loss += loss.item()
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            predictions.extend(predicted.numpy())
            true_labels.extend(labels.numpy())
    
    # Calculate final metrics
    test_accuracy = correct / total
    avg_test_loss = test_loss / len(test_loader)
    
    # Print final results
    print(f"Test Loss: {avg_test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Save results to JSON
    results = {
        'framework': 'PyTorch with Ray',
        'test_loss': float(avg_test_loss),
        'test_accuracy': float(test_accuracy),
        'predictions': [int(p) for p in predictions],
        'true_labels': [int(t) for t in true_labels],
        'class_names': label_encoder.classes_.tolist()
    }
    
    # Ensure results directory exists
    os.makedirs('results', exist_ok=True)
    with open('results/iris_pytorch_ray_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Final output
    print(f"Results saved to results/iris_pytorch_ray_results.json")
    print("=" * 80)
    
    # Shutdown Ray
    ray.shutdown()

if __name__ == "__main__":
    main()
